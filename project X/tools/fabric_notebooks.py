"""Convert and compare Fabric notebook source without executing notebook code.

The .py files are Fabric documents, not standalone Python scripts. Keep cell
markers, parameter markers, language metadata and %run commands intact.
"""

import argparse
import difflib
import json
from pathlib import Path
import re


PROJECT = Path(__file__).resolve().parents[1]
HEADER = "# Fabric notebook source"
MARKER = re.compile(r"^# (METADATA|MARKDOWN|PARAMETERS CELL|CELL) \*{20}[ \t]*$", re.M)
# Preserve configuration, but omit editor state, execution history and widgets.
NOTEBOOK_METADATA = (
    "kernel_info", "dependencies", "spark_compute",
    "sessionKeepAliveTimeout", "a365ComputeOptions",
)


def cell_source(cell):
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def normalized_source(cell):
    """Ignore only separator newlines at cell boundaries, never code indentation."""
    return cell_source(cell).replace("\r\n", "\n").strip("\n")


def _comment(text, prefix):
    return "\n".join(prefix + (" " + line if line else "") for line in text.split("\n"))


def _uncomment(text, prefix):
    lines = []
    for line in text.split("\n"):
        if line == prefix:
            lines.append("")
        elif line.startswith(prefix + " "):
            lines.append(line[len(prefix) + 1:])
        else:
            raise ValueError(f"Expected {prefix!r} prefix, found {line[:80]!r}")
    return "\n".join(lines)


def _metadata_block(metadata):
    return "# METADATA ********************\n\n" + _comment(
        json.dumps(metadata, indent=2, ensure_ascii=False), "# META"
    )


def fabric_metadata(notebook):
    metadata = notebook.get("metadata", {})
    return {key: metadata[key] for key in NOTEBOOK_METADATA if key in metadata}


def language_metadata(cell):
    return {
        key: value for key, value in cell.get("metadata", {}).get("microsoft", {}).items()
        if key in ("language", "language_group")
    }


def to_fabric_source(notebook):
    if notebook.get("nbformat") != 4:
        raise ValueError("Only nbformat 4 notebooks are supported")
    blocks = [HEADER, _metadata_block(fabric_metadata(notebook))]
    for cell in notebook["cells"]:
        text = normalized_source(cell)
        if MARKER.search(text):
            raise ValueError("Cell source contains a reserved Fabric section marker")
        if cell.get("attachments"):
            raise ValueError("Markdown attachments require a separate resource migration")
        kind = cell["cell_type"]
        metadata = language_metadata(cell)
        if kind == "markdown":
            marker = "MARKDOWN"
            text = _comment(text, "#")
        elif kind == "code":
            tags = cell.get("metadata", {}).get("tags", [])
            if set(tags) - {"parameters"}:
                raise ValueError(f"Unsupported cell tags: {tags}")
            marker = "PARAMETERS CELL" if "parameters" in tags else "CELL"
            metadata.setdefault("language", "python")
            metadata.setdefault("language_group", "synapse_pyspark")
            if metadata["language"] != "python" or text.lstrip().startswith("%%"):
                text = _comment(text, "# MAGIC")
        else:
            raise ValueError(f"Unsupported cell type: {kind}")
        blocks.append(f"# {marker} ********************\n\n{text}")
        if kind == "code":
            blocks.append(_metadata_block(metadata))
    return "\n\n".join(blocks) + "\n"


def parse_fabric_source(text):
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    if not text.splitlines() or text.splitlines()[0] != HEADER:
        raise ValueError("Missing Fabric notebook source header")
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []}
    markers = list(MARKER.finditer(text))
    if not markers or markers[0].group(1) != "METADATA":
        raise ValueError("Missing notebook metadata")
    for index, match in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        body = text[match.end():end].strip("\n")
        kind = match.group(1)
        if kind == "METADATA":
            metadata = json.loads(_uncomment(body, "# META"))
            if not notebook["cells"]:
                notebook["metadata"] = metadata
            else:
                notebook["cells"][-1]["metadata"]["microsoft"] = metadata
            continue
        markdown = kind == "MARKDOWN"
        if markdown:
            body = _uncomment(body, "#")
        elif body.startswith("# MAGIC ") or body == "# MAGIC":
            body = _uncomment(body, "# MAGIC")
        cell = {
            "cell_type": "markdown" if markdown else "code",
            "source": (body + "\n" if body else "").splitlines(keepends=True),
            "metadata": {},
        }
        if kind == "PARAMETERS CELL":
            cell["metadata"]["tags"] = ["parameters"]
        if not markdown:
            cell.update(outputs=[], execution_count=None)
        notebook["cells"].append(cell)
    return notebook


def load_notebook(path):
    """Read the requested format explicitly; never fall back to stale .ipynb.

    In the deployed client repo the primary ``<name>.py`` sources do not
    exist; notebooks live as ``notebooks/<name>.Notebook/`` directories
    synced by Fabric Git integration. When a ``.py`` path is missing, fall
    back to that layout so the same validators run in both repos.
    """
    path = Path(path)
    if path.suffix == ".py" and not path.exists():
        deployed = path.parent / "notebooks" / f"{path.stem}.Notebook"
        if deployed.is_dir():
            path = deployed
    if path.is_dir():
        path = path / "notebook-content.py"
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".ipynb":
        return json.loads(text)
    return parse_fabric_source(text)


def semantic_cells(notebook, kind):
    return [normalized_source(c) for c in notebook["cells"] if c["cell_type"] == kind]


def cell_contract(notebook):
    return [
        {
            "type": cell["cell_type"],
            "parameters": "parameters" in cell.get("metadata", {}).get("tags", []),
            "language": language_metadata(cell) if cell["cell_type"] == "code" else {},
        }
        for cell in notebook["cells"]
    ]


def _diff(before, after, before_name, after_name):
    return "".join(difflib.unified_diff(
        before.splitlines(keepends=True), after.splitlines(keepends=True),
        fromfile=before_name, tofile=after_name,
    ))


def compare(project, deployed, output):
    """Write raw and decoded diffs with a fixed original -> client direction."""
    if not deployed.is_dir():
        raise FileNotFoundError(deployed)
    output.mkdir(parents=True, exist_ok=True)
    originals = sorted(project.glob("[0-9]*.py"))
    if not originals:
        raise ValueError(f"No converted notebooks in {project}")
    rows = []
    for original in originals:
        target = deployed / f"{original.stem}.Notebook" / "notebook-content.py"
        if not target.exists():
            rows.append({"notebook": original.stem, "status": "Missing from client snapshot"})
            continue
        left, right = load_notebook(original), load_notebook(target)
        row = {"notebook": original.stem, "status": "Compared"}
        for kind in ("code", "markdown"):
            a, b = semantic_cells(left, kind), semantic_cells(right, kind)
            row[kind] = a != b
            diff = _diff("\n\n".join(a) + "\n", "\n\n".join(b) + "\n",
                         f"original/{original.name}:{kind}", f"client/{target.parent.name}:{kind}")
            (output / f"{original.stem}.{kind}.diff").write_text(diff, encoding="utf-8")
        row["cell_contract"] = cell_contract(left) != cell_contract(right)
        row["metadata"] = left["metadata"] != right["metadata"]
        row["cells"] = [len(left["cells"]), len(right["cells"])]
        (output / f"{original.stem}.metadata.diff").write_text(_diff(
            json.dumps({"notebook": left["metadata"], "cells": cell_contract(left)},
                       indent=2, sort_keys=True) + "\n",
            json.dumps({"notebook": right["metadata"], "cells": cell_contract(right)},
                       indent=2, sort_keys=True) + "\n",
            f"original/{original.name}:metadata", f"client/{target.parent.name}:metadata",
        ), encoding="utf-8")
        (output / f"{original.stem}.raw.diff").write_text(_diff(
            original.read_text(encoding="utf-8-sig"), target.read_text(encoding="utf-8-sig"),
            f"original/{original.name}", f"client/{target.parent.name}/notebook-content.py",
        ), encoding="utf-8")
        rows.append(row)
    expected = {f"{p.stem}.Notebook" for p in originals}
    extras = [p.relative_to(deployed).as_posix() for p in sorted(deployed.rglob("*.Notebook"))
              if p.parent != deployed or p.name not in expected]
    stray_ipynb = [p.relative_to(deployed).as_posix() for p in sorted(deployed.rglob("*.ipynb"))]
    (output / "comparison.json").write_text(json.dumps(
        {"notebooks": rows, "client_only_items": extras, "client_ipynb_files": stray_ipynb},
        indent=2,
    ) + "\n", encoding="utf-8")
    lines = [
        "# Original notebooks versus client Fabric snapshot", "",
        "Generated by `project X/tools/fabric_notebooks.py compare`.", "",
        "Original: primary `[0-9]*.py` notebooks in `project X`. Client snapshot: "
        "`project X/reports/current/WMPP/notebooks`. This is a local snapshot comparison, "
        "not a live query of Azure DevOps or Fabric.", "",
        "Diff direction: **minus = original; plus = client**. Code/Markdown comparisons "
        "decode Fabric sections and ignore only line endings and boundary newlines. "
        "Cell order, parameter tags and code language are checked separately. "
        "Metadata differences include original Spark/session configuration omitted "
        "from the client source format; these are not assumed to be code changes.", "",
        "| Notebook | Code | Markdown | Cell contract | Notebook metadata | Cells original/client |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        name = row["notebook"]
        if row["status"] != "Compared":
            lines.append(f"| `{name}` | **Missing from client snapshot** | — | — | — | — |")
        else:
            flags = ["Changed" if row[key] else "Same"
                     for key in ("code", "markdown", "cell_contract", "metadata")]
            if row["code"]:
                flags[0] = f"[Changed]({name}.code.diff)"
            lines.append(f"| `{name}` | {' | '.join(flags)} | {row['cells'][0]}/{row['cells'][1]} |")
    lines += ["", "Client-only notebook items:", ""]
    lines += [f"- `{p}`" for p in extras] or ["- None"]
    lines += ["", "Additional client `.ipynb` files (not used as deployed source):", ""]
    lines += [f"- `{p}`" for p in stray_ipynb] or ["- None"]
    lines += ["", "Each matched notebook has `.raw.diff`, `.code.diff`, `.markdown.diff`, "
              "and `.metadata.diff` files. Empty files mean no differences in that view.", ""]
    (output / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    convert = commands.add_parser("convert", help="One-time .ipynb migration; refuses overwrites")
    convert.add_argument("sources", type=Path, nargs="+")
    comparison = commands.add_parser("compare", help="Compare primary .py notebooks with client snapshot")
    comparison.add_argument("--project", type=Path, default=PROJECT)
    comparison.add_argument("--deployed", type=Path, default=PROJECT / "reports/current/WMPP/notebooks")
    comparison.add_argument("--output", type=Path, default=PROJECT / "reports/notebook-comparison")
    args = parser.parse_args()
    if args.command == "convert":
        # Preflight all paths and conversions before writing any files.
        pending = []
        for source in args.sources:
            if source.suffix != ".ipynb":
                raise ValueError(f"Expected .ipynb: {source}")
            target = source.with_suffix(".py")
            if target.exists():
                raise FileExistsError(f"Primary source already exists; edit it directly: {target}")
            pending.append((target, to_fabric_source(load_notebook(source))))
        for target, text in pending:
            with target.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
            print(f"Converted {target.name}")
    else:
        rows = compare(args.project, args.deployed, args.output)
        print(f"Compared {len(rows)} original notebooks; report: {args.output / 'comparison.md'}")


if __name__ == "__main__":
    main()

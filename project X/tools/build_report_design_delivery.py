"""Build local, inspectable PBIP delivery copies; never publish or edit current ZIPs.

Native PBIR visuals and TMDL extensions only. Original replaced pages are retained
outside the deployable projects. Run with the already extracted delivery directory.
Keep its name short, for example reports/client-deliverables/WMPP v16.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import uuid

import rebuild_mission_control_dashboard_v16 as ui


def ident(value):
    return hashlib.sha256(value.encode()).hexdigest()[:20]


def guid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "wmpp-delivery/" + value))


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


L = ui.literal


def fill(color):
    return {"solid": {"color": L(repr(color))}}


def obj(**properties):
    return [{"properties": properties}]


def field(table, name, measure=False):
    return {
        "Measure" if measure else "Column": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": name,
        }
    }


def project(table, name, measure=False, label=None):
    return {
        "field": field(table, name, measure),
        "queryRef": table + "." + name,
        "nativeQueryRef": label or name,
    }


def quoted(name):
    return "'" + name.replace("'", "''") + "'"


def col(name, dtype="string", expression=None, extra=""):
    body = "\n\t\t\t" + expression if expression else ""
    return (
        f"\n\tcolumn {quoted(name)}"
        + (" =" if expression else "")
        + body
        + f"\n\t\tdataType: {dtype}\n\t\tlineageTag: {guid(name + str(expression))}"
        + "\n\t\tsummarizeBy: none\n"
        + ("" if expression else f"\t\tsourceColumn: {name}\n")
        + extra
    )


def add_columns(model, table, columns):
    path = model / "tables" / (table + ".tmdl")
    text = path.read_text(encoding="utf-8-sig")
    for name, dtype, expression, extra in columns:
        # Repair only this generator's former name-only tag, never a source tag.
        text = text.replace(
            "lineageTag: " + guid(name + str(expression)),
            "lineageTag: " + guid(table + name),
        )
        if not re.search(
            r"(?m)^\tcolumn (?:" + re.escape(quoted(name)) + "|" + re.escape(name) + r")(?:\s|$)",
            text,
        ):
            index = text.index("\n\tpartition ")
            addition = col(name, dtype, expression, extra).replace(
                guid(name + str(expression)), guid(table + name)
            )
            text = text[:index] + addition + text[index:]
    path.write_text(text, encoding="utf-8")


def table(model, name, columns, source, mode="calculated", hidden=False):
    content = f"table {quoted(name)}\n\tlineageTag: {guid(name)}\n" + (
        "\tisHidden\n" if hidden else ""
    )
    for column, dtype, extra in columns:
        # Calculated-table columns bind names emitted by the table expression.
        content += (
            col(column, dtype, extra=extra)
            .replace(guid(column + "None"), guid(name + column))
            .replace(
                f"sourceColumn: {column}",
                f"sourceColumn: [{column}]" if mode == "calculated" else f"sourceColumn: {column}",
            )
        )
    content += f"\n\tpartition {quoted(name)} = {mode}\n\t\tmode: import\n\t\tsource =\n"
    content += "\n".join("\t\t\t" + line for line in source.splitlines()) + "\n"
    (model / "tables" / (name + ".tmdl")).write_text(content, encoding="utf-8")
    path = model / "model.tmdl"
    text = path.read_text(encoding="utf-8-sig")
    ref = "ref table " + quoted(name)
    if ref not in text:
        path.write_text(text.rstrip() + "\n" + ref + "\n", encoding="utf-8")


def measures(model, name, definitions):
    # Measures share a case-insensitive namespace across the entire model.
    # Check before replacing the generated table, not after writing a bad model.
    definitions = list(definitions)
    occupied = {}
    pattern = r"(?m)^\s*measure\s+(?:'((?:[^']|'')+)'|([^=\r\n]+?))\s*="
    target = model / "tables" / (name + ".tmdl")
    for existing in (model / "tables").glob("*.tmdl"):
        if existing == target:
            continue
        for match in re.finditer(pattern, existing.read_text(encoding="utf-8-sig")):
            label = (match[1].replace("''", "'") if match[1] else match[2]).strip()
            occupied[label.casefold()] = existing.name
    for label, _, _ in definitions:
        key = label.casefold()
        if key in occupied:
            raise ValueError(f"Measure {label!r} already exists in {occupied[key]}")
        occupied[key] = target.name
    table(model, name, [], "#table(type table [], {})", mode="m")
    path = model / "tables" / (name + ".tmdl")
    text = path.read_text(encoding="utf-8")
    parts = []
    for label, dax, fmt in definitions:
        parts.append(
            f"\n\tmeasure {quoted(label)} =\n"
            + "\n".join("\t\t\t" + line for line in dax.splitlines())
            + f"\n\t\tlineageTag: {guid(name + label)}\n\t\tdisplayFolder: Report experience\n"
            + (f"\t\tformatString: {fmt}\n" if fmt else "")
        )
    text = text.replace("\n\tpartition ", "".join(parts) + "\n\tpartition ", 1)
    path.write_text(text, encoding="utf-8")


def relation(model, source_table, source_col, target_table, target_col):
    path = model / "relationships.tmdl"
    text = path.read_text(encoding="utf-8-sig")
    key = guid(source_table + source_col + target_table + target_col)
    if key not in text:
        text += f"\nrelationship {key}\n\tfromColumn: {quoted(source_table)}.{quoted(source_col)}\n\ttoColumn: {quoted(target_table)}.{quoted(target_col)}\n"
        path.write_text(text, encoding="utf-8")


def parameter(model, name, entries):
    template = (model / "tables" / "Dashboard Metric Selector.tmdl").read_text(encoding="utf-8-sig")
    template = template.replace("Dashboard Metric Selector", name)
    template = re.sub(r"lineageTag: [\w-]+", lambda m: "lineageTag: " + guid(name + m[0]), template)
    start = template.index("\t\tsource =")
    rows = ",\n".join(
        f'\t\t\t("{label}", NAMEOF({quoted(t)}[{c}]), {i})'
        for i, (label, t, c) in enumerate(entries)
    )
    template = template[:start] + "\t\tsource =\n\t\t\t{\n" + rows + "\n\t\t\t}\n"
    (model / "tables" / (name + ".tmdl")).write_text(template, encoding="utf-8")
    path = model / "model.tmdl"
    text = path.read_text(encoding="utf-8-sig")
    if "ref table " + quoted(name) not in text:
        path.write_text(text.rstrip() + "\nref table " + quoted(name) + "\n", encoding="utf-8")


def selection(table_name, column, value):
    return {
        "Version": 2,
        "From": [{"Name": "s", "Entity": table_name, "Type": 0}],
        "Where": [
            {
                "Condition": {
                    "In": {
                        "Expressions": [
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "s"}},
                                    "Property": column,
                                }
                            }
                        ],
                        "Values": [[{"Literal": {"Value": quoted(value)}}]],
                    }
                }
            }
        ],
    }


class Page:
    def __init__(self, bundle, report, page_id, title, subtitle, dark=False):
        self.bundle, self.report, self.id, self.dark = bundle, report, page_id, dark
        self.path = report / "definition/pages" / page_id
        backup = bundle / "_review/original-pages" / report.name / page_id
        if self.path.exists() and not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            # Exact scoped move, originals remain recoverable outside the PBIP.
            shutil.move(str(self.path), str(backup))
        self.data = (
            read(backup / "page.json")
            if backup.exists()
            else ui.page_json(page_id, title, 945, 1680)
        )
        self.data.update(displayName=title, height=945, width=1680, displayOption="FitToPage")
        self.data.pop("visualInteractions", None)
        self.bg, self.panel, self.ink, self.muted, self.accent = (
            ("#101713", "#1B241E", "#F3F7EF", "#A7B6A9", "#CBF576")
            if dark
            else ("#F8F5F1", "#FFFFFF", "#2B2427", "#61575C", "#E96B7D")
        )
        self.data["objects"] = {"background": obj(color=fill(self.bg), transparency=L("0D"))}
        self.visuals = []
        self.svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="945"><rect width="1680" height="945" fill="{self.bg}"/>'
        ]
        if not dark:
            self.svg += [
                '<defs><linearGradient id="glass" x2=".8" y2="1"><stop stop-color="#FFFFFF" stop-opacity=".92"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".58"/></linearGradient>'
                '<radialGradient id="rose"><stop stop-color="#F7BDC9" stop-opacity=".65"/><stop offset="1" stop-color="#F7BDC9" stop-opacity="0"/></radialGradient>'
                '<radialGradient id="teal"><stop stop-color="#72AEB5" stop-opacity=".20"/><stop offset="1" stop-color="#72AEB5" stop-opacity="0"/></radialGradient>'
                '<filter id="softShadow" x="-15%" y="-25%" width="130%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#3A2A31" flood-opacity=".12"/></filter></defs>',
                '<ellipse cx="1480" cy="180" rx="540" ry="400" fill="url(#rose)"/><ellipse cx="170" cy="900" rx="620" ry="420" fill="url(#teal)"/>',
            ]
        self.text(
            "eyebrow",
            "OPERATIONS / MISSION CONTROL" if dark else "WMPP / PLACEMENT INTELLIGENCE",
            (36, 22, 1200, 22),
            12,
            self.accent,
        )
        self.text("title", title, (36, 53, 1400, 44), 30)
        self.text("subtitle", subtitle, (36, 102, 1580, 28), 13, self.muted, False)

    def shell(self, key, kind, pos):
        v = ui.visual_shell(ident(self.id + key), kind, ui.position(*pos, len(self.visuals) + 1))
        v["visual"]["visualContainerObjects"] = {
            k: obj(show=L("false"))
            for k in ("background", "border", "dropShadow", "title", "subTitle")
        }
        v["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted(key)))
        v["visual"]["visualContainerObjects"]["padding"] = obj(
            top=L("0D"), bottom=L("0D"), left=L("0D"), right=L("0D")
        )
        self.visuals.append(v)
        return v

    def text(self, key, text, pos, size=16, color=None, bold=True):
        v = self.shell(key, "textbox", pos)
        v["visual"]["objects"] = {
            "general": obj(
                paragraphs=[
                    {
                        "textRuns": [
                            {
                                "value": text,
                                "textStyle": {
                                    "fontFamily": "Segoe UI",
                                    "fontSize": f"{size}px",
                                    "fontWeight": "bold" if bold else "normal",
                                    "color": color or self.ink,
                                },
                            }
                        ]
                    }
                ]
            )
        }
        return v

    def panel_box(self, pos, title=None, caption=None, color=None):
        from apply_report_soft_glow import native_panel

        self.visuals.append(native_panel(self.id, pos, self.dark, color))
        x, y, w, h = pos
        self.svg.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{color or (self.panel if self.dark else "url(#glass)")}"'
            + (
                "/>"
                if self.dark
                else ' stroke="#FFFFFF" stroke-opacity=".86" filter="url(#softShadow)"/>'
            )
        )
        if title:
            self.text("panel-" + title, title, (x + 22, y + 17, w - 44, 28), 18)
        if caption:
            self.text(
                "caption-" + title, caption, (x + 22, y + 48, w - 44, 34), 11, self.muted, False
            )

    def card(self, key, table_name, measure, pos, caption, index=0):
        x, y, w, h = pos
        self.panel_box(pos)
        # Project-authored, dependency-free line icons; never externally fetched.
        glyphs = [
            '<path d="M2 20V10h5v10m3 0V4h5v16m3 0V1h5v19"/>',
            '<circle cx="12" cy="12" r="9"/><path d="m7 12 3 3 7-7"/>',
            '<path d="m12 2 11 20H1Z M12 8v6m0 3v1"/>',
            '<circle cx="12" cy="12" r="9"/><path d="M12 5v8l4 2"/>',
            '<path d="m2 11 10-9 10 9M5 10v12h14V10M10 22v-8h4v8"/>',
        ]
        self.svg.append(
            f'<g transform="translate({x + w - 49},{y + 22})" fill="none" stroke="{self.accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{glyphs[index % 5]}</g>'
        )
        self.text(key + "-label", key, (x + 20, y + 16, w - 80, 27), 13, self.muted)
        v = self.shell(key, "cardVisual", (x + 17, y + 48, w - 36, 50))
        v["visual"]["query"] = {
            "queryState": {"Data": {"projections": [project(table_name, measure, True)]}}
        }

        def default(**properties):
            return [{"properties": properties, "selector": {"id": "default"}}]

        v["visual"]["objects"] = {
            "value": default(
                fontSize=L("29D"),
                fontColor=fill(self.ink),
                fontFamily=L("'Segoe UI Semibold'"),
                horizontalAlignment=L("'left'"),
            ),
            "layout": default(
                autoGrid=L("true"),
                rowCount=L("1L"),
                columnCount=L("1L"),
                cellPadding=L("0L"),
                leftOuterMargin=L("0L"),
                rightOuterMargin=L("0L"),
                topOuterMargin=L("0L"),
                bottomOuterMargin=L("0L"),
                backgroundShow=L("false"),
            ),
            "padding": default(
                paddingSelection=L("'Custom'"),
                paddingIndividual=L("true"),
                leftMargin=L("0D"),
                rightMargin=L("0D"),
                topMargin=L("0D"),
                bottomMargin=L("0D"),
            ),
        }
        for group in (
            "label",
            "fillCustom",
            "outline",
            "shadowCustom",
            "accentBar",
            "divider",
            "image",
            "cardImage",
            "border",
        ):
            v["visual"]["objects"][group] = default(show=L("false"))
        self.text(key + "-caption", caption, (x + 20, y + 106, w - 36, 30), 11, self.muted, False)

    def slicer(self, key, t, c, pos, default=None, single=False):
        self.panel_box(pos)
        v = self.shell(key, "slicer", pos)
        v["visual"]["query"] = {
            "queryState": {"Values": {"projections": [{**project(t, c), "active": True}]}}
        }
        v["visual"]["objects"] = {
            "data": obj(mode=L("'Dropdown'")),
            "selection": obj(
                singleSelect=L(str(single).lower()),
                selectAllCheckboxEnabled=L(str(not single).lower()),
            ),
            "header": obj(
                show=L("true"),
                text=L(quoted(key)),
                fontColor=fill(self.muted),
                background=fill(self.panel),
                textSize=L("10D"),
            ),
            "items": obj(
                fontColor=fill(self.ink),
                background=fill(self.panel),
                textSize=L("11D"),
                padding=L("2D"),
            ),
            "general": obj(selfFilterEnabled=L("true")),
        }
        if default:
            v["visual"]["objects"]["general"][0]["properties"]["filter"] = {
                "filter": selection(t, c, default)
            }
        return v

    def query(self, key, kind, pos, roles):
        v = self.shell(key, kind, pos)
        v["visual"]["query"] = {"queryState": {k: {"projections": p} for k, p in roles.items()}}
        v["visual"]["objects"] = {
            "categoryAxis": obj(
                labelColor=fill(self.muted),
                fontSize=L("10D"),
                showAxisTitle=L("false"),
                gridlineShow=L("false"),
            ),
            "valueAxis": obj(
                labelColor=fill(self.muted),
                fontSize=L("10D"),
                showAxisTitle=L("false"),
                gridlineShow=L("false"),
            ),
            "legend": obj(show=L("false")),
            "labels": obj(show=L("true"), color=fill(self.ink), fontSize=L("10D")),
            "dataPoint": obj(defaultColor=fill(self.accent)),
        }
        return v

    def table(self, key, pos, fields):
        v = self.query(key, "tableEx", pos, {"Values": [project(*f) for f in fields]})
        v["visual"]["objects"] = {
            "columnHeaders": obj(
                fontColor=fill(self.muted), backColor=fill(self.panel), fontSize=L("10D")
            ),
            "values": obj(
                fontColor=fill(self.ink),
                backColorPrimary=fill(self.panel),
                backColorSecondary=fill(self.panel),
                fontSize=L("10D"),
            ),
            "grid": obj(gridVertical=L("false"), gridHorizontal=L("false"), rowPadding=L("9D")),
            "total": obj(totals=L("false")),
        }
        return v

    def map(self, key, pos, table_name, location, measure_table, measure):
        v = self.query(
            key,
            "azureMap",
            pos,
            {
                "Location": [project(table_name, location)],
                "Size": [project(measure_table, measure, True)],
                "Tooltips": [project(measure_table, measure, True)],
            },
        )
        v["visual"]["objects"] = {
            "mapControls": obj(showZoomButtons=L("true")),
            "legend": obj(show=L("false")),
            "bubbleLayer": obj(show=L("true"), color=fill(self.accent)),
            "mapSettings": obj(style=L("'grayscale_light'")),
        }
        return v

    def nav(self, items):
        for i, (label, dest) in enumerate(items):
            x = 36 + i * 228
            self.text("navlabel-" + label, label + "  →", (x, 901, 218, 28), 12, self.accent)
            v = self.shell("nav-" + label, "actionButton", (x, 896, 220, 38))
            v["visual"]["visualContainerObjects"]["visualLink"] = obj(
                show=L("true"), type=L("'PageNavigation'"), navigationSection=L(quoted(dest))
            )
            v["visual"]["objects"] = {
                k: obj(show=L("false")) for k in ("fill", "outline", "icon", "text")
            }

    def switch_views(self, views, positions):
        """Display-only bookmarks preserve calendar/pipeline filtering."""
        names = [v["name"] for _, v in views]
        folder = self.report / "definition/bookmarks"
        metadata_path = folder / "bookmarks.json"
        metadata = (
            read(metadata_path)
            if metadata_path.exists()
            else {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json",
                "items": [],
            }
        )
        for index, ((label, target), pos) in enumerate(zip(views, positions)):
            target["isHidden"] = index != 0
            bookmark = ident(self.id + ":view:" + label)
            states = {
                v["name"]: {
                    "singleVisual": {
                        "visualType": v["visual"]["visualType"],
                        "objects": {},
                        **({"display": {"mode": "hidden"}} if v["name"] != target["name"] else {}),
                    }
                }
                for _, v in views
            }
            save(
                folder / (bookmark + ".bookmark.json"),
                {
                    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json",
                    "name": bookmark,
                    "displayName": label,
                    "options": {
                        "applyOnlyToTargetVisuals": True,
                        "targetVisualNames": names,
                        "suppressData": True,
                        "suppressActiveSection": True,
                    },
                    "explorationState": {
                        "version": "1.3",
                        "activeSection": self.id,
                        "sections": {self.id: {"visualContainers": states}},
                    },
                },
            )
            if not any(item["name"] == bookmark for item in metadata["items"]):
                metadata["items"].append({"name": bookmark})
            self.text("switch-label-" + label, label, pos, 12, self.accent)
            button = self.shell("switch-" + label, "actionButton", pos)
            button["visual"]["visualContainerObjects"]["visualLink"] = obj(
                show=L("true"),
                type=L("'Bookmark'"),
                bookmark=L(quoted(bookmark)),
                tooltip=L(quoted("Show " + label + "; keep current filters")),
            )
            button["visual"]["objects"] = {
                k: obj(show=L("false")) for k in ("fill", "outline", "icon", "text")
            }
        save(metadata_path, metadata)

    def finish(self):
        # The requested plain surface uses the native page colour only. Do not
        # reintroduce a composite skin or baked-in icons. Soft shadows belong
        # to individual editable native panels produced by panel_box.
        self.svg = self.svg[:1]
        save(self.path / "page.json", self.data)
        for visual in self.visuals:
            save(self.path / "visuals" / visual["name"] / "visual.json", visual)
        written = {visual["name"] for visual in self.visuals}
        for old in (self.path / "visuals").glob("*/visual.json"):
            if old.parent.name not in written:
                source = old.parent.resolve()
                target = (
                    self.bundle
                    / "_review/superseded-generated-visuals"
                    / self.report.name
                    / self.id
                    / source.name
                ).resolve()
                if not source.is_relative_to(self.path.resolve()) or not target.is_relative_to(
                    (self.bundle / "_review").resolve()
                ):
                    raise ValueError("Visual archive path outside delivery review scope")
                if target.exists():
                    target = target.with_name(target.name + "-" + uuid.uuid4().hex[:8])
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(target))
        path = self.report / "definition/pages/pages.json"
        pages = read(path)
        if self.id not in pages["pageOrder"]:
            pages["pageOrder"].append(self.id)
        save(path, pages)
        self.preview()

    def preview(self):
        """Layout-only proof, not a Power BI render or client-data screenshot."""
        svg = list(self.svg)
        for v in self.visuals:
            if v.get("isHidden"):
                continue
            pos = v["position"]
            x, y, w, h = (pos[k] for k in ("x", "y", "width", "height"))
            visual = v["visual"]
            kind = visual["visualType"]
            if kind in ("image", "actionButton"):
                continue
            if kind == "textbox":
                for paragraph in visual["objects"]["general"][0]["properties"]["paragraphs"]:
                    for run in paragraph["textRuns"]:
                        style = run["textStyle"]
                        size = float(style["fontSize"][:-2])
                        # Native textboxes wrap; approximate their line breaks for layout proof.
                        words = run["value"].split()
                        lines = []
                        line = ""
                        for word in words:
                            if len(line + " " + word) * size * 0.50 > w and line:
                                lines.append(line)
                                line = word
                            else:
                                line = (line + " " + word).strip()
                        lines.append(line)
                        for j, line in enumerate(lines):
                            svg.append(
                                f'<text x="{x + 4}" y="{y + size + j * size * 1.25}" fill="{style["color"]}" font-family="Segoe UI,Arial" font-size="{size}" font-weight="{style["fontWeight"]}">{html.escape(line)}</text>'
                            )
            elif kind == "cardVisual":
                svg.append(
                    f'<text x="{x + 5}" y="{y + 36}" fill="{self.ink}" font-family="Segoe UI" font-size="36">—</text>'
                )
            elif kind == "slicer":
                label = visual["objects"]["header"][0]["properties"]["text"]["expr"]["Literal"][
                    "Value"
                ][1:-1]
                svg.append(
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{self.panel}"/><text x="{x + 12}" y="{y + 24}" fill="{self.muted}" font-family="Segoe UI" font-size="13">{html.escape(label)}</text><text x="{x + 12}" y="{y + 49}" fill="{self.ink}" font-family="Segoe UI" font-size="15">Select…</text><path d="m{x + w - 28} {y + 41} 6 6 6-6" fill="none" stroke="{self.muted}"/>'
                )
            elif kind == "pivotTable":
                for d, label in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
                    svg.append(
                        f'<text x="{x + d * w / 7 + 14}" y="{y + 18}" fill="{self.muted}" font-family="Segoe UI" font-size="13">{label}</text>'
                    )
                for n in range(35):
                    cx = x + (n % 7) * w / 7
                    cy = y + 32 + (n // 7) * (h - 36) / 5
                    color = [
                        "#345B3D",
                        "#345B3D",
                        "#4C854F",
                        "#242F28",
                        "#A43C49",
                        "#345B3D",
                        "#66512B",
                    ][n % 7]
                    svg.append(
                        f'<rect x="{cx + 3}" y="{cy + 3}" width="{w / 7 - 6}" height="{(h - 36) / 5 - 6}" rx="8" fill="{color}"/><text x="{cx + 16}" y="{cy + 28}" fill="{self.ink}" font-family="Segoe UI" font-size="15">{n + 1 if n < 30 else "—"}</text>'
                    )
            elif kind == "deneb7E15AEF80B9E4D4F8E12924291ECE89A":
                label = visual["visualContainerObjects"]["general"][0]["properties"]["altText"][
                    "expr"
                ]["Literal"]["Value"][1:-1]
                proof = self.bundle / "_review/chart-proofs" / (label + ".svg")
                if proof.exists():
                    data = base64.b64encode(proof.read_bytes()).decode("ascii")
                    svg.append(
                        f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/svg+xml;base64,{data}"/>'
                    )
                    svg.append(
                        f'<text x="{x + 10}" y="{y + h - 5}" fill="{self.muted}" font-family="Segoe UI" font-size="11">Illustrative chart states only — not client data</text>'
                    )
                else:
                    svg.append(
                        f'<text x="{x + 20}" y="{y + 32}" fill="{self.muted}" font-family="Segoe UI" font-size="15">Select a day · Gantt with historical quartiles and failure markers</text>'
                    )
            else:
                label = {
                    "azureMap": "Interactive city map",
                    "tableEx": "Live detail register",
                    "clusteredBarChart": "Interactive breakdown",
                    "Gantt1448688115699": "Interactive Gantt timeline",
                }.get(kind, kind)
                svg.append(
                    f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="12" fill="none" stroke="{self.muted}" stroke-opacity=".25" stroke-dasharray="5 6"/><text x="{x + 24}" y="{y + 42}" fill="{self.muted}" font-family="Segoe UI" font-size="16">{label}</text><text x="{x + 24}" y="{y + 68}" fill="{self.muted}" font-family="Segoe UI" font-size="12">Data-bound visual — verify after model refresh in Power BI</text>'
                )
        svg.append(
            '<rect x="1120" y="0" width="560" height="24" fill="#735425"/><text x="1134" y="17" fill="white" font-family="Segoe UI" font-size="12">LAYOUT PROOF · NOT A POWER BI RENDER · NO CLIENT DATA</text></svg>'
        )
        path = self.bundle / "_review/layout-previews" / f"{self.report.name}-{self.id}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(svg), encoding="utf-8")


def monitoring_model(model):
    job = "rpt_job_run_summary"
    add_columns(
        model,
        job,
        [
            (
                "Run Date",
                "dateTime",
                f"IF(NOT ISBLANK({job}[started_at]), INT({job}[started_at]))",
                "\t\tformatString: dd MMM yyyy\n",
            ),
            (
                "Outcome",
                "string",
                f'VAR s = UPPER(TRIM({job}[status])) RETURN SWITCH(TRUE(), {job}[steps_failed] > 0 || s IN {{"FAILED","FAIL","ERROR"}}, "Failed", s IN {{"SUCCESS","SUCCEEDED","COMPLETED"}}, "Successful", s IN {{"RUNNING","IN_PROGRESS","STARTED"}}, "Running", "Other")',
                "",
            ),
        ],
    )
    table(
        model,
        "Load Calendar",
        [
            ("Date", "dateTime", "\t\tformatString: dd MMM yyyy\n"),
            ("Week", "int64", ""),
            ("Weekday", "string", "\t\tsortByColumn: WeekdayOrder\n"),
            ("WeekdayOrder", "int64", "\t\tisHidden\n"),
            ("Month", "string", "\t\tsortByColumn: MonthOrder\n"),
            ("MonthOrder", "int64", "\t\tisHidden\n"),
        ],
        f"""VAR firstDate = COALESCE(MIN({job}[Run Date]), TODAY())
VAR lastDate = MAX(TODAY(), MAX({job}[Run Date]))
RETURN ADDCOLUMNS(CALENDAR(DATE(YEAR(firstDate),MONTH(firstDate),1), EOMONTH(lastDate,0)),
"Week", INT((DAY([Date]) + WEEKDAY(DATE(YEAR([Date]),MONTH([Date]),1),2) - 2)/7)+1,
"Weekday", FORMAT([Date],"ddd"), "WeekdayOrder", WEEKDAY([Date],2),
"Month", IF(YEAR([Date])=YEAR(TODAY()) && MONTH([Date])=MONTH(TODAY()),"This month",FORMAT([Date],"yyyy MMM")),
"MonthOrder", YEAR([Date])*100+MONTH([Date]))""",
    )
    relation(model, job, "Run Date", "Load Calendar", "Date")
    measures(
        model,
        "_Load Experience",
        [
            ("Runs", f"DISTINCTCOUNT({job}[job_run_id])", "#,0"),
            ("Successful", f'CALCULATE([Runs], KEEPFILTERS({job}[Outcome]="Successful"))', "#,0"),
            ("Failures", f'CALCULATE([Runs], KEEPFILTERS({job}[Outcome]="Failed"))', "#,0"),
            (
                "In progress or other",
                f'CALCULATE([Runs], KEEPFILTERS({job}[Outcome] IN {{"Running","Other"}}))',
                "#,0",
            ),
            ("Success rate", "DIVIDE([Successful],[Successful]+[Failures])", "0.0%"),
            (
                "P95 duration min",
                f"PERCENTILEX.INC(FILTER({job}, NOT ISBLANK({job}[ended_at]) && {job}[job_duration_seconds]>=0), DIVIDE({job}[job_duration_seconds],60),0.95)",
                "0.0",
            ),
            ("Rows written", f"SUM({job}[rows_written])", "#,0"),
            (
                "Day tile",
                """VAR d=SELECTEDVALUE('Load Calendar'[Date])
VAR n=COALESCE([Runs],0)
RETURN IF(NOT ISBLANK(d), FORMAT(d,"d") & UNICHAR(10) & IF(d>TODAY(),"Future",SWITCH(TRUE(),[Failures]>0,"! " & FORMAT([Failures],"0") & " failed",[In progress or other]>0,"~ " & FORMAT(n,"0") & " runs",n>0,FORMAT(n,"0") & " OK","No loads")))""",
                "",
            ),
            (
                "Day colour",
                'SWITCH(TRUE(),[Failures]>0,"#A43C49",[In progress or other]>0,"#66512B",[Successful]>=10,"#4C854F",[Successful]>0,"#345B3D","#242F28")',
                "",
            ),
            ("Day text colour", '"#F3F7EF"', ""),
        ],
    )


def duration_benchmarks(model):
    """Descriptive historical quartiles, not forecast limits or failure rules."""
    job, step = "rpt_job_run_summary", "rpt_job_step_timing"
    add_columns(
        model,
        step,
        [
            ("Pipeline", "string", f"RELATED({job}[pipeline_name])", ""),
            (
                "Outcome",
                "string",
                f'VAR s=UPPER(TRIM({step}[status])) RETURN SWITCH(TRUE(),s IN {{"FAILED","FAIL","ERROR"}},"Failed",s IN {{"SUCCESS","SUCCEEDED","COMPLETED"}},"Successful",s IN {{"RUNNING","IN_PROGRESS","STARTED"}},"Running","Other")',
                "",
            ),
        ],
    )
    definitions = []
    for label, fact, duration in [
        ("Job", job, "job_duration_seconds"),
        ("Step", step, "step_duration_seconds"),
    ]:
        pipeline = "pipeline_name" if label == "Job" else "Pipeline"
        cohort = f"""VAR anchor=SELECTEDVALUE('{fact}'[started_at])
VAR pipeline=SELECTEDVALUE('{fact}'[{pipeline}])
VAR currentJob=SELECTEDVALUE('{fact}'[job_run_id])
"""
        if label == "Step":
            cohort += f"VAR notebook=SELECTEDVALUE('{fact}'[notebook_name])\nVAR sequence=SELECTEDVALUE('{fact}'[step_sequence])\n"
        cohort += f'''VAR history=FILTER(CALCULATETABLE('{fact}',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('{job}'),REMOVEFILTERS('{fact}')),
    '{fact}'[{pipeline}]=pipeline && '{fact}'[job_run_id]<>currentJob
    && '{fact}'[started_at]>=anchor-30 && '{fact}'[ended_at]<anchor
    && NOT ISBLANK('{fact}'[ended_at]) && '{fact}'[ended_at]>='{fact}'[started_at]
    && NOT ISBLANK('{fact}'[{duration}]) && '{fact}'[{duration}]>=0
    && '{fact}'[Outcome]="Successful"'''
        if label == "Step":
            cohort += f" && '{fact}'[notebook_name]=notebook && '{fact}'[step_sequence]=sequence && RELATED('{job}'[Outcome])=\"Successful\""
        cohort += ")\n"
        valid = "NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob)"
        if label == "Step":
            valid += " && NOT ISBLANK(notebook) && NOT ISBLANK(sequence)"
        definitions.append(
            (label + " baseline n", cohort + f"RETURN IF({valid},COUNTROWS(history))", "#,0")
        )
        for stat, expr in [
            ("mean", f"AVERAGEX(history,DIVIDE('{fact}'[{duration}],60))"),
            ("median", f"MEDIANX(history,DIVIDE('{fact}'[{duration}],60))"),
            ("p25", f"PERCENTILEX.INC(history,DIVIDE('{fact}'[{duration}],60),0.25)"),
            ("p75", f"PERCENTILEX.INC(history,DIVIDE('{fact}'[{duration}],60),0.75)"),
        ]:
            definitions.append(
                (
                    label + " prior " + stat + " min",
                    cohort + f"RETURN IF({valid} && COUNTROWS(history)>=5,{expr})",
                    "0.0",
                )
            )
        definitions.append(
            (label + " actual min", f"DIVIDE(SELECTEDVALUE('{fact}'[{duration}]),60)", "0.0")
        )
        definitions.append(
            (
                label + " comparison",
                f"""VAR n=[{label} baseline n]
VAR actual=[{label} actual min]
RETURN SWITCH(TRUE(),ISBLANK(n),"Select one {label.lower()}",n<5,"Insufficient history",ISBLANK(actual),"No duration recorded",actual<[{label} prior p25 min],"Below prior P25",actual>[{label} prior p75 min],"Above prior P75","Within prior IQR")""",
                "",
            )
        )
    definitions.append(("Single calendar day", "IF(HASONEVALUE('Load Calendar'[Date]),1,0)", "0"))
    measures(model, "_Run Benchmarks", definitions)


def duration_gantt(page, key, pos, step=False, day_only=False):
    """The same Vega-Lite spec drives PBIR and the separately labelled proof."""
    t = "rpt_job_step_timing" if step else "rpt_job_run_summary"
    label = "Step" if step else "Job"
    mt = "_Run Benchmarks"
    cols = ["job_run_id", "started_at", "ended_at", "Outcome"] + (
        ["Pipeline", "notebook_name", "step_sequence"] if step else ["pipeline_name"]
    )
    fields = [project(t, c) for c in cols]
    fields += [
        project(mt, label + " " + suffix, True)
        for suffix in [
            "actual min",
            "baseline n",
            "prior mean min",
            "prior median min",
            "prior p25 min",
            "prior p75 min",
            "comparison",
        ]
    ]
    fields += [project(mt, "Single calendar day", True)]
    display = (
        "datum.Outcome + ' · ' + datum.notebook_name + ' · ' + datum.step_sequence + ' · ' + datum.job_run_id"
        if step
        else "datum.Outcome + ' · ' + datum.pipeline_name + ' · ' + datum.job_run_id"
    )
    transforms = [
        {"filter": "isValid(datum.started_at)"},
        {"calculate": display, "as": "Run label"},
        {
            "calculate": "isValid(datum.ended_at) ? toDate(datum.ended_at) : toDate(datum.started_at)",
            "as": "Plot end",
        },
    ]
    for suffix in ["p25", "p75", "mean"]:
        transforms.append(
            {
                "calculate": f"isValid(datum['{label} prior {suffix} min']) ? toNumber(toDate(datum.started_at)) + datum['{label} prior {suffix} min']*60000 : null",
                "as": suffix + " end",
            }
        )
    if day_only:
        transforms.insert(0, {"filter": "datum['Single calendar day'] == 1"})
    tooltip = [
        {"field": c, "type": "nominal"}
        for c in ["job_run_id"]
        + (["notebook_name", "step_sequence"] if step else ["pipeline_name"])
        + ["Outcome"]
    ]
    tooltip += [
        {"field": c, "type": "temporal", "format": "%d %b %H:%M:%S"}
        for c in ["started_at", "ended_at"]
    ]
    tooltip += [
        {"field": label + " " + suffix, "type": "quantitative", "format": ".1f"}
        for suffix in [
            "actual min",
            "prior mean min",
            "prior median min",
            "prior p25 min",
            "prior p75 min",
        ]
    ]
    tooltip += [
        {"field": label + " baseline n", "type": "quantitative", "format": ".0f"},
        {"field": label + " comparison", "type": "nominal"},
    ]
    enc = {
        "y": {
            "field": "Run label",
            "type": "nominal",
            "sort": {"field": "started_at", "order": "ascending"},
            "axis": {"title": None, "labelLimit": 175, "labelFontSize": 10},
        },
        "tooltip": tooltip,
    }
    colour = {
        "field": "Outcome",
        "type": "nominal",
        "scale": {
            "domain": ["Successful", "Failed", "Running", "Other"],
            "range": ["#91C977", "#FF6377", "#E0B568", "#95A5A0"],
        },
        "legend": None,
    }
    layers = [
        {
            "transform": [{"filter": "isValid(datum['p25 end'])"}],
            "mark": {
                "type": "bar",
                "size": 22,
                "color": "#82958A",
                "opacity": 0.28,
                "cornerRadius": 4,
            },
            "encoding": {
                "x": {"field": "p25 end", "type": "temporal", "title": None},
                "x2": {"field": "p75 end"},
            },
        },
        {
            "mark": {"type": "bar", "size": 8, "cornerRadius": 3},
            "encoding": {
                "x": {
                    "field": "started_at",
                    "type": "temporal",
                    "title": None,
                    "axis": {"format": "%H:%M", "labelAngle": 0},
                },
                "x2": {"field": "Plot end"},
                "color": colour,
                "opacity": {
                    "condition": {"test": "datum.__selected__ === 'off'", "value": 0.25},
                    "value": 0.9,
                },
            },
        },
        {
            "transform": [{"filter": "isValid(datum['mean end'])"}],
            "mark": {"type": "tick", "color": "#DFF5D8", "thickness": 2, "size": 25},
            "encoding": {
                "x": {"field": "mean end", "type": "temporal"},
                "opacity": {
                    "condition": {"test": "datum.__selected__ === 'off'", "value": 0.2},
                    "value": 0.9,
                },
            },
        },
    ]
    # Concentric translucent marks create a deterministic glow without animation,
    # unsupported SVG filters, or a external-image dependency.
    layers.append(
        {
            "transform": [{"filter": "datum.Outcome !== 'Failed'"}],
            "mark": {"type": "circle", "size": 25},
            "encoding": {"x": {"field": "Plot end", "type": "temporal"}, "color": colour},
        }
    )
    for size, opacity in [(500, 0.07), (270, 0.13), (120, 0.25), (35, 1)]:
        layers.append(
            {
                "transform": [{"filter": "datum.Outcome === 'Failed'"}],
                "mark": {"type": "circle", "size": size, "color": "#FF526B", "opacity": opacity},
                "encoding": {"x": {"field": "Plot end", "type": "temporal"}},
            }
        )
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"name": "dataset"},
        "width": "container",
        "height": {"step": 32},
        "background": "transparent",
        "padding": 8,
        "transform": transforms,
        "encoding": enc,
        "layer": layers,
        "config": {
            "view": {"stroke": None},
            "axis": {
                "labelColor": "#A7B6A9",
                "titleColor": "#A7B6A9",
                "gridColor": "#304137",
                "domain": False,
                "tickColor": "#304137",
                "labelFont": "Segoe UI",
            },
            "font": "Segoe UI",
        },
    }
    v = page.query(key, "deneb7E15AEF80B9E4D4F8E12924291ECE89A", pos, {"dataset": fields})
    v["visual"]["objects"] = {
        "vega": obj(
            jsonSpec=L(quoted(json.dumps(spec))),
            jsonConfig=L("'{}'"),
            provider=L("'vegaLite'"),
            renderMode=L("'svg'"),
            enableSelection=L("true"),
            enableTooltips=L("true"),
            enableContextMenu=L("true"),
        ),
        "display": obj(scrollbarColor=fill("#91C977"), scrollbarOpacity=L("45D")),
    }
    save(page.bundle / "_review/chart-specifications" / (key + ".vega-lite.json"), spec)
    return v


def monitoring_pages(bundle, report):
    t = "_Load Experience"
    job = "rpt_job_run_summary"
    overview, timeline = "803165f7d2f5aaccd8ac", "ed27e90d06816c7c1eee"
    p = Page(
        bundle,
        report,
        overview,
        "Every load. One clear picture.",
        "Select a calendar day for its load timeline. Switch between Day Gantt and Register without clearing the selected day or pipeline.",
        True,
    )
    p.slicer("Month", "Load Calendar", "Month", (36, 147, 280, 63), "This month", True)
    p.slicer("Pipeline", job, "pipeline_name", (338, 147, 360, 63))
    p.text(
        "legend",
        "● Successful   /   ! Failed   /   ~ Running or other   /   No loads",
        (735, 167, 885, 30),
        13,
        p.muted,
        False,
    )
    for i, (label, m, hint) in enumerate(
        [
            ("Job runs", "Runs", "In the selected period"),
            ("Success rate", "Success rate", "Completed outcomes only"),
            ("Failed jobs", "Failures", "Includes failed steps"),
            ("P95 duration · min", "P95 duration min", "Completed runs only"),
            ("Rows written", "Rows written", "Across selected jobs"),
        ]
    ):
        p.card(label, t, m, (36 + i * 326, 232, 304, 146), hint, i)
    p.panel_box(
        (36, 400, 696, 474),
        "Load activity",
        "Green = all completed successfully · Red = at least one failed job",
    )
    cal = p.query(
        "load-calendar",
        "pivotTable",
        (58, 485, 648, 363),
        {
            "Rows": [project("Load Calendar", "Week")],
            "Columns": [project("Load Calendar", "Weekday")],
            "Values": [project(t, "Day tile", True)],
        },
    )
    cal["visual"]["objects"] = {
        "rowHeaders": obj(show=L("false"), fontColor=fill(p.panel), fontSize=L("1D")),
        "columnHeaders": obj(
            fontColor=fill(p.muted),
            backColor=fill(p.panel),
            fontSize=L("11D"),
            alignment=L("'Center'"),
            autoSizeColumnWidth=L("false"),
        ),
        "values": obj(
            fontColor=fill(p.ink),
            fontSize=L("12D"),
            wordWrap=L("true"),
            backColorPrimary=fill(p.panel),
            backColorSecondary=fill(p.panel),
        ),
        "grid": obj(
            gridVertical=L("true"),
            gridHorizontal=L("true"),
            gridVerticalColor=fill(p.panel),
            gridHorizontalColor=fill(p.panel),
            gridVerticalWeight=L("6D"),
            gridHorizontalWeight=L("6D"),
            rowPadding=L("13D"),
        ),
        "subTotals": obj(rowSubtotals=L("false"), columnSubtotals=L("false")),
        "rowTotal": obj(show=L("false")),
        "columnTotal": obj(show=L("false")),
    }
    cal["visual"]["objects"]["values"].append(
        {
            "properties": {
                "backColor": {"solid": {"color": {"expr": field(t, "Day colour", True)}}},
                "fontColor": {"solid": {"color": {"expr": field(t, "Day text colour", True)}}},
            },
            "selector": {
                "data": [{"dataViewWildcard": {"matchingOption": 1}}],
                "metadata": t + ".Day tile",
            },
        }
    )
    p.panel_box(
        (754, 400, 890, 474),
        "Day explorer",
        "Choose a day · Grey band: prior P25–P75 · Tick: mean · Glowing red dot: failure",
    )
    register = p.table(
        "job-register",
        (773, 519, 850, 329),
        [
            (job, "job_run_id"),
            (job, "pipeline_name"),
            (job, "Outcome"),
            (job, "started_at"),
            (job, "job_duration_seconds"),
            (job, "steps_failed"),
        ],
    )
    register["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": field(job, "started_at"), "direction": "Descending"}],
        "isDefaultSort": False,
    }
    gantt = duration_gantt(p, "calendar-day-gantt", (773, 519, 850, 329), day_only=True)
    p.switch_views(
        [("Day Gantt", gantt), ("Register", register)], [(777, 482, 155, 29), (954, 482, 155, 29)]
    )
    p.data["visualInteractions"] = [
        {"source": cal["name"], "target": v["name"], "type": "DataFilter"}
        for v in (register, gantt)
    ]
    p.data["visualInteractions"] += [
        {"source": v["name"], "target": cal["name"], "type": "NoFilter"} for v in (register, gantt)
    ]
    p.nav(
        [
            ("Job & step timelines", timeline),
            ("Quality & schema", "d807778066085fbd96dc"),
            ("Archive & replay", "5133b9c7cfcf12cf7f74"),
        ]
    )
    p.finish()
    p = Page(
        bundle,
        report,
        timeline,
        "Follow the run. Find the delay.",
        "Last 14 days. Select a job to filter steps. Bands: previous 30-day successful-run P25–P75; ticks: mean; red glow: failure.",
        True,
    )
    p.data["filterConfig"] = {"filters": [ui.page_filter_last_14_days()]}
    p.slicer("Pipeline", job, "pipeline_name", (36, 145, 360, 62))
    p.slicer("Job ID · search", job, "job_run_id", (418, 145, 650, 62))
    p.slicer("Status", job, "Outcome", (1090, 145, 550, 62))
    ids = []
    for i, (label, entity) in enumerate(
        [("Job runs", job), ("Steps in selected job", "rpt_job_step_timing")]
    ):
        x = 36 + i * 815
        p.panel_box((x, 230, 792, 370), label, "Select a bar or use the register below")
        v = duration_gantt(
            p,
            "step-duration-gantt" if i else "job-duration-gantt",
            (x + 16, 306, 760, 276),
            step=bool(i),
        )
        ids.append(v["name"])
    p.panel_box((36, 620, 792, 254), "Job register")
    j = p.table(
        "jobs",
        (53, 674, 758, 181),
        [(job, "job_run_id"), (job, "pipeline_name"), (job, "status"), (job, "started_at")],
    )
    p.panel_box((851, 620, 792, 254), "Step register · prior history in minutes")
    s = p.table(
        "steps",
        (867, 674, 758, 181),
        [
            ("rpt_job_step_timing", c)
            for c in (
                "step_sequence",
                "notebook_name",
                "status",
                "step_duration_seconds",
                "error_message",
            )
        ]
        + [
            ("_Run Benchmarks", "Step " + name, True)
            for name in (
                "prior mean min",
                "prior median min",
                "prior p25 min",
                "prior p75 min",
                "baseline n",
            )
        ],
    )
    p.data["visualInteractions"] = [
        {"source": a, "target": b, "type": "DataFilter"}
        for a in (ids[0], j["name"])
        for b in (ids[1], s["name"])
    ]
    p.nav(
        [
            ("Load calendar", overview),
            ("Quality & schema", "d807778066085fbd96dc"),
            ("Archive & replay", "5133b9c7cfcf12cf7f74"),
        ]
    )
    p.finish()
    p = Page(
        bundle,
        report,
        "d807778066085fbd96dc",
        "Keep quality in focus.",
        "Quality-check results and schema inventory have independent filters. Select a quality row to inspect its rule, failures and message.",
        True,
    )
    dq = "cfg_data_quality_result"
    mt = "_MissionControl_Measures"
    for i, (label, c) in enumerate(
        [
            ("Quality run", "job_run_id"),
            ("Severity", "severity"),
            ("Source table", "source_table"),
            ("Check status", "status"),
        ]
    ):
        p.slicer(label, dq, c, (36 + i * 407, 146, 385, 64))
    for i, (label, m, hint) in enumerate(
        [
            ("Evaluated checks", "DQ Evaluated Checks", "Completed quality evaluations"),
            ("Failed checks", "DQ Failed Checks", "Within quality selection"),
            ("Failed rows", "DQ Failed Rows", "Rows counted per check"),
            ("Critical rules failing", "Critical Rules Failing", "Prioritise these investigations"),
        ]
    ):
        p.card(label, mt, m, (36 + i * 407, 232, 385, 146), hint, i)
    p.panel_box(
        (36, 400, 1020, 474),
        "Quality register",
        "Use run / severity / table / status filters above. Inspect rule messages before remediation.",
    )
    p.table(
        "quality-register",
        (54, 485, 984, 365),
        [
            (dq, c)
            for c in (
                "rule_id",
                "source_table",
                "column_name",
                "severity",
                "status",
                "failed_row_count",
                "checked_row_count",
                "message",
            )
        ],
    )
    p.panel_box(
        (1078, 400, 566, 474),
        "Schema inventory",
        "Separate inventory context: quality filters do not filter this register.",
    )
    p.table(
        "schema-register",
        (1096, 485, 530, 365),
        [
            ("cfg_archived_schema_live", c)
            for c in ("schema_name", "table_name", "column_name", "data_type", "is_nullable")
        ],
    )
    p.nav(
        [
            ("Load calendar", overview),
            ("Job & step timelines", timeline),
            ("Archive & replay", "5133b9c7cfcf12cf7f74"),
        ]
    )
    p.finish()
    p = Page(
        bundle,
        report,
        "5133b9c7cfcf12cf7f74",
        "Archive. Replay. Recover.",
        "Separate archive and Gold snapshot controls. ZIP filters affect ZIP metrics; snapshot metrics retain their own context.",
        True,
    )
    z = "cfg_archive_zip_load"
    p.slicer("Archive status", z, "status", (36, 146, 390, 64))
    p.slicer("Archive export date", z, "export_date", (448, 146, 390, 64))
    p.slicer("Snapshot status", "cfg_month_end_gold_run", "status", (860, 146, 390, 64))
    for i, (label, m, hint) in enumerate(
        [
            ("Archive batches", "Archive ZIP Batches", "In the ZIP filter context"),
            ("Failed batches", "Failed Archive ZIP Batches", "ZIP loads needing attention"),
            ("Reload requested", "Archive ZIP Batches Awaiting Reload", "ZIP control flag"),
            ("Failed snapshots", "Failed Gold Snapshots", "Snapshot status context"),
        ]
    ):
        p.card(label, mt, m, (36 + i * 407, 232, 385, 146), hint, i)
    p.panel_box(
        (36, 400, 790, 474),
        "Archive control register",
        "Review the error before requesting a replay through the established pipeline process.",
    )
    p.table(
        "archive-register",
        (54, 485, 754, 365),
        [
            (z, c)
            for c in (
                "export_date",
                "status",
                "reload",
                "attempt_count",
                "file_count",
                "error_message",
            )
        ],
    )
    p.panel_box(
        (848, 400, 796, 474),
        "Gold snapshot register",
        "These records are separate from ZIP loads; selecting a ZIP does not imply a snapshot relationship.",
    )
    p.table(
        "snapshot-register",
        (866, 485, 760, 365),
        [
            ("cfg_month_end_gold_run", c)
            for c in (
                "snapshot_date",
                "status",
                "reload",
                "attempt_count",
                "dq_result",
                "error_message",
            )
        ],
    )
    p.nav(
        [
            ("Load calendar", overview),
            ("Job & step timelines", timeline),
            ("Quality & schema", "d807778066085fbd96dc"),
        ]
    )
    p.finish()


def wmpp_model(model, report):
    add_columns(
        model,
        "fact_referral",
        [
            (n, t, None, "")
            for n, t in [
                ("framework_category_id", "int64"),
                ("framework_category_count", "int64"),
                ("location", "string"),
                ("location_match_status", "string"),
                ("location_is_default", "boolean"),
                ("location_requires_review", "boolean"),
            ]
        ],
    )
    add_columns(
        model,
        "fact_referral",
        [
            (
                "Map city",
                "string",
                "IF('fact_referral'[location_match_status]=\"CITY_MATCH\" && NOT ISBLANK('fact_referral'[location]), 'fact_referral'[location] & \", United Kingdom\")",
                "\t\tdataCategory: City\n",
            )
        ],
    )
    offer_columns = [
        ("framework_category_id", "int64"),
        ("provider_home_framework_category_id", "int64"),
        ("provider_home_framework_category_count", "int64"),
        ("referral_location", "string"),
        ("location_match_status", "string"),
        ("location_is_default", "boolean"),
        ("location_requires_review", "boolean"),
        ("provider_home_postcode", "string"),
        ("referral_to_home_distance_km", "double"),
        ("referral_to_home_distance_status", "string"),
        ("referral_to_home_distance_basis", "string"),
    ]
    add_columns(model, "fact_offer", [(n, t, None, "") for n, t in offer_columns])
    # The Gold contract now emits provider_home_id. Preserve the existing column's
    # lineage tag and fix only bindings scoped to fact_offer.
    path = model / "tables/fact_offer.tmdl"
    text = (
        path.read_text(encoding="utf-8")
        .replace("\tcolumn home_id\n", "\tcolumn provider_home_id\n")
        .replace("sourceColumn: home_id", "sourceColumn: provider_home_id")
    )
    path.write_text(text, encoding="utf-8")
    for path in model.rglob("*.tmdl"):
        text = path.read_text(encoding="utf-8-sig")
        new = (
            text.replace("'fact_offer'[home_id]", "'fact_offer'[provider_home_id]")
            .replace("fact_offer[home_id]", "fact_offer[provider_home_id]")
            .replace("fact_offer.home_id", "fact_offer.provider_home_id")
        )
        if new != text:
            path.write_text(new, encoding="utf-8")

    def fix_json(value):
        if isinstance(value, dict):
            for key, val in list(value.items()):
                if (
                    key == "Column"
                    and val.get("Expression", {}).get("SourceRef", {}).get("Entity") == "fact_offer"
                    and val.get("Property") == "home_id"
                ):
                    val["Property"] = "provider_home_id"
                elif key in ("queryRef", "queryName") and isinstance(val, str):
                    value[key] = val.replace("fact_offer.home_id", "fact_offer.provider_home_id")
                fix_json(val)
        elif isinstance(value, list):
            for val in value:
                fix_json(val)

    for path in report.rglob("*.json"):
        value = read(path)
        before = json.dumps(value)
        fix_json(value)
        if json.dumps(value) != before:
            save(path, value)
    offer_source = (model / "tables/fact_offer.tmdl").read_text(encoding="utf-8-sig")
    source = re.search(r"Source = Sql.Database\([^\n]+", offer_source).group(0).rstrip(",")
    table(
        model,
        "bridge_referral_framework_category",
        [("referral_id", "string", ""), ("framework_category_id", "int64", "")],
        f'let\n{source},\nData = Source{{[Schema="gold",Item="bridge_referral_framework_category"]}}[Data]\nin Data',
        mode="m",
        hidden=True,
    )
    relation(
        model, "bridge_referral_framework_category", "referral_id", "fact_referral", "referral_id"
    )
    for name in ("Referral Category", "Offer Category"):
        table(
            model,
            name,
            [
                ("Category ID", "int64", "\t\tisHidden\n"),
                ("Category", "string", ""),
                ("Framework", "string", ""),
            ],
            """SELECTCOLUMNS('dim_framework_category', "Category ID", 'dim_framework_category'[framework_category_id], "Category", 'dim_framework_category'[category_name], "Framework", 'dim_framework_category'[framework_code])""",
        )
    relation(model, "fact_offer", "framework_category_id", "Offer Category", "Category ID")
    base = [
        ("Referrals", "Total Referrals"),
        ("Category-aware open referrals", "Referrals Currently Active"),
        ("Awaiting offer", "Referrals Awaiting Offer"),
        ("Under offer", "Referrals Under Offer"),
        ("Offers", "Offers Submitted"),
        ("Completed IPAs", "IPA Completed"),
    ]
    defs = []
    for label, measure in base:
        defs.append(
            (
                label,
                f"""VAR selectedCategories=VALUES('Referral Category'[Category ID])
VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([{measure}],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[{measure}])""",
                "#,0",
            )
        )
    defs += [
        (
            "Mapped referrals",
            "CALCULATE([Referrals],KEEPFILTERS('fact_referral'[location_match_status]=\"CITY_MATCH\"))",
            "#,0",
        ),
        (
            "Location review",
            "CALCULATE([Referrals],KEEPFILTERS(FILTER('fact_referral',ISBLANK('fact_referral'[location_match_status]) || 'fact_referral'[location_match_status]<>\"CITY_MATCH\")))",
            "#,0",
        ),
        (
            "Median preferred-city distance km",
            "MEDIANX(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]=\"APPROXIMATE_PREFERENCE_CITY\" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km])),'fact_offer'[referral_to_home_distance_km])",
            "0.0",
        ),
        (
            "Offers with preferred-city distance",
            "CALCULATE([Offers Submitted],KEEPFILTERS(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]=\"APPROXIMATE_PREFERENCE_CITY\" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km]))))",
            "#,0",
        ),
        (
            "Offers without preferred-city distance",
            "[Offers Submitted]-[Offers with preferred-city distance]",
            "#,0",
        ),
        (
            "Preferred-city distance coverage",
            "DIVIDE([Offers with preferred-city distance],[Offers Submitted])",
            "0.0%",
        ),
    ]
    measures(model, "_Explore Measures", defs)
    add_columns(
        model,
        "fact_offer",
        [
            (
                "Distance band",
                "string",
                'VAR d=\'fact_offer\'[referral_to_home_distance_km] RETURN SWITCH(TRUE(),\'fact_offer\'[referral_to_home_distance_status]="APPROXIMATE_DEFAULT_CITY","Default city estimate",ISBLANK(d),"Unavailable / review",d<=25,"01 · Up to 25 km",d<=50,"02 · 25–50 km",d<=100,"03 · 50–100 km","04 · Over 100 km")',
                "",
            )
        ],
    )
    parameter(
        model,
        "Referral Breakdown",
        [
            ("City", "fact_referral", "location"),
            ("Category", "Referral Category", "Category"),
            ("Framework", "Referral Category", "Framework"),
            ("Urgency", "fact_referral", "placement_urgency_band"),
            ("Placement type", "fact_referral", "placement_type_required"),
            ("Status", "fact_referral", "current_status"),
        ],
    )
    parameter(
        model,
        "Referral Metric",
        [
            (
                "Open referrals" if label == "Category-aware open referrals" else label,
                "_Explore Measures",
                label,
            )
            for label, _ in base
        ],
    )


def wmpp_pages(bundle, report):
    ref = "f028a4be56d03e8404d7"
    offers = ident("offer-location-page")
    single = "f3070e87127b751f89d4"
    mt = "_Explore Measures"
    p = Page(
        bundle,
        report,
        ref,
        "Where referrals need support.",
        "City-level placement preferences, current referral categories and a flexible breakdown. Select a bubble or bar to explore.",
    )
    for i, (label, t, c, default) in enumerate(
        [
            ("Framework", "Referral Category", "Framework", None),
            ("Category", "Referral Category", "Category", None),
            ("Break down by", "Referral Breakdown", "Referral Breakdown", "City"),
            ("Measure", "Referral Metric", "Referral Metric", "Referrals"),
        ]
    ):
        p.slicer(label, t, c, (36 + i * 407, 146, 386, 64), default, default is not None)
    for i, (label, m, hint) in enumerate(
        [
            ("Referrals", "Referrals", "Distinct referrals in scope"),
            ("Open referrals", "Category-aware open referrals", "Current active caseload"),
            ("Awaiting offer", "Awaiting offer", "Still awaiting an offer"),
            ("Location review", "Location review", "Defaulted, missing or ambiguous"),
        ]
    ):
        p.card(label, mt, m, (36 + i * 407, 232, 385, 146), hint, i)
    p.panel_box(
        (36, 400, 790, 474),
        "Referral preference map",
        "Bubble size = referrals. Only recognised cities; defaulted or ambiguous locations are excluded.",
    )
    p.map(
        "referral-city-map",
        (53, 485, 756, 365),
        "fact_referral",
        "Map city",
        mt,
        "Mapped referrals",
    )
    p.panel_box(
        (848, 400, 796, 474),
        "Your question, your breakdown",
        "Switch both the grouping and metric above. Multi-category referrals may appear in more than one bar.",
    )
    v = p.query(
        "category-breakdown",
        "clusteredBarChart",
        (870, 485, 748, 365),
        {"Category": [project("fact_referral", "location")], "Y": [project(mt, "Referrals", True)]},
    )
    for role, param in [("Category", "Referral Breakdown"), ("Y", "Referral Metric")]:
        v["visual"]["query"]["queryState"][role]["fieldParameters"] = [
            {"parameterExpr": field(param, param), "index": 0, "length": 1}
        ]
    p.nav(
        [
            ("Single referral", single),
            ("Offer locations", offers),
            ("Board dashboard", "5038cffdd48af9a80dd1"),
            ("Referral snapshots", "dd3a58c056d723048dbf"),
        ]
    )
    p.finish()
    p = Page(
        bundle,
        report,
        offers,
        "A clearer view of placement distance.",
        "Approximate straight-line distance: referral preferred-city centroid to provider-home postcode. Not a child address or road journey.",
    )
    for i, (label, t, c) in enumerate(
        [
            ("Provider", "dim_provider", "provider_name"),
            ("Offer framework", "Offer Category", "Framework"),
            ("Offer category", "Offer Category", "Category"),
            ("Referral ID · search", "fact_referral", "referral_id"),
        ]
    ):
        p.slicer(label, t, c, (36 + i * 407, 146, 386, 64))
    for i, (label, t, m, hint) in enumerate(
        [
            ("Offers", "_Measures", "Offers Submitted", "All offers in scope"),
            (
                "Median distance · km",
                mt,
                "Median preferred-city distance km",
                "Recognised preference cities only",
            ),
            (
                "Distance coverage",
                mt,
                "Preferred-city distance coverage",
                "Share with preference-city estimate",
            ),
            (
                "Needs location review",
                mt,
                "Offers without preferred-city distance",
                "Includes default-city estimates",
            ),
        ]
    ):
        p.card(label, t, m, (36 + i * 407, 232, 385, 146), hint, i)
    p.panel_box(
        (36, 400, 574, 474),
        "Distance distribution",
        "Default estimates and unavailable distances stay visible as separate groups.",
    )
    p.query(
        "distance-bands",
        "clusteredBarChart",
        (54, 485, 538, 365),
        {
            "Category": [project("fact_offer", "Distance band")],
            "Y": [project("_Measures", "Offers Submitted", True)],
        },
    )
    p.panel_box(
        (632, 400, 1012, 474),
        "Offer location register",
        "Search a referral above to compare its homes. Blank distances are not zero.",
    )
    p.table(
        "offer-distance-register",
        (650, 485, 976, 365),
        [
            ("fact_offer", "referral_id"),
            ("fact_offer", "offer_id"),
            ("fact_offer", "referral_location"),
            ("dim_provider", "provider_name"),
            ("dim_provider_home", "home_name"),
            ("fact_offer", "provider_home_postcode"),
            ("fact_offer", "referral_to_home_distance_km"),
            ("fact_offer", "referral_to_home_distance_status"),
        ],
    )
    p.nav(
        [
            ("Referral geography", ref),
            ("Single referral", single),
            ("Offer overview", "1f33996970651e846183"),
        ]
    )
    p.finish()
    # Compact individual referral view. Existing search uses initials + person ID;
    # the source deliberately has no full-name field.
    p = Page(
        bundle,
        report,
        single,
        "One referral. The full picture.",
        "Search by person initials / ID and referral ID. Exact child addresses are not exposed in this model.",
    )
    # This is a visible search page; hidden drillthrough page is retained unchanged.
    p.data.pop("pageBinding", None)
    p.data.pop("filterConfig", None)
    p.slicer("Person · search", "dim_person", "person_search_label", (36, 146, 600, 64))
    p.slicer("Referral · search", "fact_referral", "referral_id", (658, 146, 600, 64), single=True)
    for i, (label, m, hint) in enumerate(
        [
            ("Referrals", "Total Referrals", "Select one referral to inspect"),
            ("Provider assignments", "Provider Assignments", "Providers approached"),
            ("Offers", "Offers Submitted", "All linked offers"),
            ("Completed IPAs", "IPA Completed", "Completed agreements"),
        ]
    ):
        p.card(label, "_Measures", m, (36 + i * 407, 232, 385, 146), hint, i)
    p.panel_box(
        (36, 400, 485, 474),
        "Preferred city",
        "City-level preference; not the child’s home address.",
    )
    p.map(
        "single-referral-map",
        (52, 485, 453, 363),
        "fact_referral",
        "Map city",
        mt,
        "Mapped referrals",
    )
    p.panel_box((543, 400, 1101, 224), "Offers & homes")
    p.table(
        "single-offers",
        (559, 455, 1069, 150),
        [
            ("fact_offer", "offer_id"),
            ("dim_provider", "provider_name"),
            ("dim_provider_home", "home_name"),
            ("fact_offer", "offer_status"),
            ("fact_offer", "referral_to_home_distance_km"),
            ("fact_offer", "referral_to_home_distance_status"),
        ],
    )
    p.panel_box((543, 646, 540, 228), "Provider referrals")
    p.table(
        "single-provider-referrals",
        (559, 701, 508, 151),
        [
            ("fact_referral_provider", "referral_provider_id"),
            ("dim_provider", "provider_name"),
            ("fact_referral_provider", "is_declined"),
        ],
    )
    p.panel_box((1105, 646, 539, 228), "Individual placement agreements")
    p.table(
        "single-ipas",
        (1121, 701, 507, 151),
        [
            ("fact_ipa", "ipa_id"),
            ("fact_ipa", "placement_status"),
            ("fact_ipa", "is_ipa_completed"),
            ("fact_ipa", "estimated_weekly_cost"),
        ],
    )
    p.nav(
        [
            ("Referral geography", ref),
            ("Offer locations", offers),
            ("Provider single view", "08ef33dc6a87d1b14392"),
        ]
    )
    p.finish()


def render_chart_proofs(bundle):
    """Render the exact specs with synthetic data, isolated from model/report data."""
    import vl_convert as vlc

    from datetime import datetime, timedelta

    folder = bundle / "_review/chart-proofs"
    folder.mkdir(parents=True, exist_ok=True)
    for path in (bundle / "_review/chart-specifications").glob("*.vega-lite.json"):
        spec = read(path)
        is_step = path.name.startswith("step-")
        label = "Step" if is_step else "Job"
        rows = []
        for i, (status, duration) in enumerate(
            [
                ("Successful", 12),
                ("Successful", 18),
                ("Failed", 9),
                ("Successful", 11),
                ("Running", None),
                ("Successful", 14),
            ]
        ):
            start = datetime(2026, 9, 26, 8) + timedelta(minutes=i * 18)
            row = {
                "job_run_id": f"DEMO-{i + 1:02}",
                "pipeline_name": "Example pipeline",
                "Pipeline": "Example pipeline",
                "notebook_name": f"Example step {i + 1}",
                "step_sequence": i + 1,
                "started_at": start.isoformat(),
                "ended_at": (start + timedelta(minutes=duration)).isoformat()
                if duration is not None
                else None,
                "Outcome": status,
                "Single calendar day": 1,
                "__selected__": "neutral",
            }
            row.update(
                {
                    label + " actual min": duration,
                    label + " baseline n": 20,
                    label + " prior mean min": 12,
                    label + " prior median min": 11.5,
                    label + " prior p25 min": 10,
                    label + " prior p75 min": 15,
                    label + " comparison": "Illustrative only",
                }
            )
            rows.append(row)
        spec["datasets"] = {"dataset": rows}
        spec["width"] = 620
        spec["background"] = "#1B241E"
        spec["title"] = {
            "text": "ILLUSTRATIVE DATA · SAME CHART SPECIFICATION",
            "color": "#A7B6A9",
            "fontSize": 11,
            "anchor": "start",
        }
        (folder / (path.stem.replace(".vega-lite", "") + ".svg")).write_text(
            vlc.vegalite_to_svg(spec), encoding="utf-8"
        )
        (folder / (path.stem.replace(".vega-lite", "") + ".png")).write_bytes(
            vlc.vegalite_to_png(spec, scale=2)
        )
    print("Rendered chart-spec proofs with synthetic data only.")


def plain_surfaces(bundle):
    """Update only the generated report surfaces; do not rebuild semantic models."""
    for report in bundle.glob("*/*.Report"):
        for page_path in report.glob("definition/pages/*/page.json"):
            page_id = page_path.parent.name
            skin = page_path.parent / "visuals" / ident(page_id + "page-background")
            if not (skin / "visual.json").exists():
                continue
            backup = bundle / "_review/pre-plain" / report.name / page_id
            if backup.exists():
                raise ValueError(f"Preserve existing surface backup: {backup}")
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(page_path.parent, backup)
            source = skin.resolve()
            target = (backup / "removed-skin").resolve()
            if not source.is_relative_to(report.resolve()) or not target.is_relative_to(
                (bundle / "_review").resolve()
            ):
                raise ValueError("Skin archive outside scoped delivery paths")
            shutil.move(str(source), str(target))
            data = read(page_path)
            dark = "Mission Control" in report.name
            panel = "#1B241E" if dark else "#FFFFFF"
            visuals = []
            for path in page_path.parent.glob("visuals/*/visual.json"):
                value = read(path)
                visual = value["visual"]
                visual.setdefault("visualContainerObjects", {})["padding"] = obj(
                    top=L("0D"), bottom=L("0D"), left=L("0D"), right=L("0D")
                )
                if visual["visualType"] == "slicer":
                    visual["objects"]["items"][0]["properties"]["padding"] = L("2D")
                    visual["objects"]["header"][0]["properties"]["background"] = fill(panel)
                save(path, value)
                visuals.append(value)
            # Regenerate the honest layout-only proof from the edited report,
            # retaining actual queries, bookmarks, positions and text content.
            preview = Page.__new__(Page)
            preview.bundle, preview.report, preview.id = bundle, report, page_id
            preview.bg = "#101713" if dark else "#F8F5F1"
            preview.panel = panel
            preview.ink = "#F3F7EF" if dark else "#2B2427"
            preview.muted = "#A7B6A9" if dark else "#61575C"
            preview.accent = "#CBF576" if dark else "#E96B7D"
            preview.visuals = sorted(visuals, key=lambda v: v["position"].get("z", 0))
            preview.svg = [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="945"><rect width="1680" height="945" fill="{preview.bg}"/>'
            ]
            preview.preview()
            print("Plain surface and explicit padding:", report.name, data["displayName"])


def validate_delivery_paths(bundle):
    """Guard Desktop's observed legacy path limits; review archives are not loaded."""
    for root in bundle.iterdir():
        if not root.is_dir() or root.name.startswith("_"):
            continue
        for path in root.rglob("*"):
            limit = 248 if path.is_dir() else 260
            length = len(str(path.resolve()).encode("utf-16-le")) // 2
            if length >= limit:
                raise ValueError(
                    f"Desktop path too long ({length} characters): {path}. "
                    "Shorten the delivery folder before generating or opening the project."
                )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument(
        "--plain-surfaces-only",
        action="store_true",
        help="Remove generated skins and override inherited padding without changing models",
    )
    parser.add_argument(
        "--render-proofs",
        action="store_true",
        help="Render isolated synthetic Vega-Lite proofs; requires vl-convert-python",
    )
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    allowed = Path(__file__).resolve().parents[1] / "reports/client-deliverables"
    if not bundle.is_relative_to(allowed.resolve()) or bundle == allowed.resolve():
        raise ValueError("Use a dedicated extracted directory under client-deliverables.")
    validate_delivery_paths(bundle)
    if args.plain_surfaces_only:
        plain_surfaces(bundle)
        validate_delivery_paths(bundle)
        return
    for root in sorted(bundle.iterdir()):
        if not root.is_dir() or root.name.startswith("_"):
            continue
        models = list(root.glob("*.SemanticModel/definition"))
        reports = list(root.glob("*.Report"))
        if len(models) != 1 or len(reports) != 1:
            continue
        model, report = models[0], reports[0]
        if (model / "tables/rpt_job_run_summary.tmdl").exists():
            monitoring_model(model)
            duration_benchmarks(model)
            monitoring_pages(bundle, report)
        elif (model / "tables/fact_referral.tmdl").exists():
            wmpp_model(model, report)
            wmpp_pages(bundle, report)
        titles = {
            "803165f7d2f5aaccd8ac": "Load Calendar",
            "ed27e90d06816c7c1eee": "Job & Step Timelines",
            "d807778066085fbd96dc": "Quality & Schema",
            "5133b9c7cfcf12cf7f74": "Archive & Replay",
            "f028a4be56d03e8404d7": "Referral Geography",
            "f3070e87127b751f89d4": "Referral Single View",
            ident("offer-location-page"): "Offer Locations",
        }
        for page_id, title in titles.items():
            path = report / "definition/pages" / page_id / "page.json"
            if path.exists():
                value = read(path)
                value["displayName"] = title
                save(path, value)
        path = report / "definition/pages/pages.json"
        pages = read(path)
        pages["activePageName"] = (
            "803165f7d2f5aaccd8ac"
            if (model / "tables/rpt_job_run_summary.tmdl").exists()
            else "f028a4be56d03e8404d7"
        )
        save(path, pages)
        # Source ZIP contains one legacy tooltip flag outside its declared PBIR
        # schema. Remove that flag in the delivery only, retaining tooltip content.
        for path in report.glob("definition/pages/*/visuals/*/visual.json"):
            value = read(path)
            changed = False
            for tooltip in (
                value.get("visual", {}).get("visualContainerObjects", {}).get("visualTooltip", [])
            ):
                properties = tooltip.get("properties", {})
                if "showActionsInTooltips" in properties:
                    properties.pop("showActionsInTooltips")
                    changed = True
            if changed:
                save(path, value)
        print("Updated", root.name)
    validate_delivery_paths(bundle)
    if args.render_proofs:
        render_chart_proofs(bundle)
        for report in bundle.glob("*/*.Report"):
            if "Mission Control" in report.name:
                monitoring_pages(bundle, report)
                for page_id, title in titles.items():
                    path = report / "definition/pages" / page_id / "page.json"
                    if path.exists():
                        value = read(path)
                        value["displayName"] = title
                        save(path, value)


if __name__ == "__main__":
    main()

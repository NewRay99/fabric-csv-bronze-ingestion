"""Shrink the new KPI/guide artwork 25% inside its existing layout slots."""

from datetime import datetime
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

from build_report_design_delivery import read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    icon_root = ROOT / "assets/brand-pack/icons"
    manifests = [icon_root / "LUCIDE_KPI_SOURCES.json", REPORT.parent / "LUCIDE_KPI_SOURCES.json"]
    audit = read(manifests[0])
    assert not audit.get("artwork_scale"), "Icon sizing already applied."
    backup = BUNDLE / "_review" / ("smaller-kpi-icons-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    protected = {
        p: sha(p.read_bytes())
        for folder in [REPORT / "definition", REPORT.parent / "SM_WMPP_v16.SemanticModel"]
        for p in folder.rglob("*")
        if p.is_file()
    }
    planned = {}
    for asset in audit["assets"]:
        filename = asset["file"]
        assert filename.startswith("lucide-kpi-")
        source = icon_root / filename
        embedded = REPORT / "StaticResources/RegisteredResources" / filename
        data = source.read_bytes()
        assert data == embedded.read_bytes()
        assert sha(data) == asset["variant_sha256"]
        assert ET.fromstring(data).attrib["viewBox"] == "0 0 24 24"
        resized = data.replace(b'viewBox="0 0 24 24"', b'viewBox="-4 -4 32 32"')
        assert ET.fromstring(resized).attrib["viewBox"] == "-4 -4 32 32"
        # 24/32 = 0.75: centre the original paths without moving text or cards.
        planned[source] = resized
        planned[embedded] = resized
        asset["variant_sha256"] = sha(resized)
    audit["artwork_scale"] = 0.75
    audit["modification"] = (
        "Stroke colour replaced; viewBox expanded symmetrically to -4 -4 32 32 for 25% smaller centred artwork. Paths unchanged; no background added."
    )
    for path in [*planned, *manifests]:
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for path, content in planned.items():
        path.write_bytes(content)
        assert path.read_bytes() == content
    for path in manifests:
        save(path, audit)
    assert all(sha(p.read_bytes()) == digest for p, digest in protected.items())
    result = {
        "icon_variants_resized": len(audit["assets"]),
        "artwork_scale": 0.75,
        "report_layout_and_model_unchanged": True,
        "information_badges_and_navigation_unchanged": True,
        "native_render_verified": False,
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

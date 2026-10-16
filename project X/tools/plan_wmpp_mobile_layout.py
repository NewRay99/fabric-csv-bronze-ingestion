"""Build and verify native PBIR phone layouts through apply_patch.

Emit an apply_patch payload, or use the supplied patch executable for batch edits.
Existing Desktop visuals, page metadata, queries and model files are immutable.
The only existing file changed is the bookmark index, by appending a mobile group.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import subprocess
import difflib

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "reports/WIP/SM WMPP v16 updated WIP"
REPORT = PROJECT / "SM_WMPP_v16.Report/definition"
BASE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
MOBILE_SCHEMA = BASE + "visualContainerMobileState/2.4.0/schema.json"
WIDTH = 323
GAP = 12
EXCLUDE = {
    "d36f423c734eb63066af",  # scratch Page 2
    "d3c23d81b598b278384c",  # tooltip
    "6fac3b57c0a06055b0c6",  # tooltip
    "4be6f15f15a086c98c33",  # superseded explorer
    "7b4c90309550bd42911c",  # historical scratch page
}
DESTINATIONS = [
    ("Home", "364f2cdd67ba7822850c"),
    ("Overall performance", "5038cffdd48af9a80dd1"),
    ("Target & urgency", "6ae319c8916a5d63a4ff"),
    ("Referrals", "78d576b289e5fe3d2af6"),
    ("Offers overview", "1f33996970651e846183"),
    ("Offer locations", "1cd52e9c7e4016f342ce"),
    ("Draft offers", "ad5ab4aa6928c9178a35"),
    ("IPA overview", "58d36c775c032a42e01b"),
    ("Provider supply", "510f9f9501ccc5ae8a74"),
    ("Requirements", "b95eb4c0b53cd8c60710"),
    ("Referral Explorer", "f3070e87127b751f89d4"),
    ("Provider Explorer", "08ef33dc6a87d1b14392"),
]
CARDS = {"card", "cardVisual", "multiRowCard", "kpi", "gauge"}
TABLES = {"tableEx", "pivotTable"}
MAPS = {"azureMap", "map", "filledMap", "shapeMap"}
CHROME = {"shape", "image", "textbox", "actionButton"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def ident(value):
    return hashlib.sha256(("wmpp-phone-v1:" + value).encode()).hexdigest()[:20]


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def quote(value):
    return "'" + value.replace("'", "''") + "'"


def color(value):
    return {"solid": {"color": literal(quote(value))}}


def obj(**props):
    return [{"properties": props}]


def decode(value):
    return value.get("expr", {}).get("Literal", {}).get("Value", "").strip("'").replace("''", "'")


def vtype(v):
    return v.get("visual", {}).get("visualType", "group")


def plain(v):
    return " ".join(
        run.get("value", "") if isinstance(run.get("value", ""), str) else ""
        for o in v.get("visual", {}).get("objects", {}).get("general", [])
        for para in o.get("properties", {}).get("paragraphs", [])
        for run in para.get("textRuns", [])
    )


def prop(v, container, group, field):
    for o in v.get("visual", {}).get(container, {}).get(group, []):
        if field in o.get("properties", {}):
            return decode(o["properties"][field])
    return ""


def title(v):
    return prop(v, "visualContainerObjects", "title", "text")


def alt(v):
    return prop(v, "visualContainerObjects", "general", "altText")


def label(v):
    return prop(v, "objects", "text", "text")


def projections(v):
    return [
        p for q in v.get("visual", {}).get("query", {}).get("queryState", {}).values()
        for p in q.get("projections", [])
    ]


def references(v):
    return [p.get("queryRef", "") for p in projections(v)]


def position(x, y, w, h, z=1000, tab=1000):
    return dict(x=x, y=y, width=w, height=h, z=z, tabOrder=tab)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def add_file(path, value):
    compact_bookmark = isinstance(value, dict) and "Go to" in value.get("displayName", "") and path.name.endswith(".bookmark.json")
    text = value if isinstance(value, str) else (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n" if compact_bookmark else json_text(value))
    if path.exists():
        assert read(path) == value, f"Existing file differs from the plan: {path}"
        return ""
    return "*** Add File: " + path.as_posix() + "\n" + "\n".join("+" + line for line in text.splitlines()) + "\n"


def new_text(pid, key, words, desktop, hidden=False, size=13, background=None):
    value = {
        "$schema": BASE + "visualContainer/2.7.0/schema.json",
        "name": ident(pid + ":" + key), "position": desktop,
        "visual": {
            "visualType": "textbox",
            "objects": {"general": obj(paragraphs=[{
                "textRuns": [{"value": words, "textStyle": {
                    "fontFamily": "Segoe UI", "fontSize": f"{size}pt", "color": "#2B2427"
                }}]
            }])},
            "visualContainerObjects": {
                "title": obj(show=literal("false")),
                "background": obj(show=literal("true" if background else "false"),
                                  color=color(background or "#FFFFFF"), transparency=literal("0D")),
                "border": obj(show=literal("false")),
                "general": obj(altText=literal(quote("Mobile: " + words))),
            },
        },
    }
    if hidden:
        value["isHidden"] = True
    return value


def new_button(pid, key, words, desktop, bookmark, hidden=False, background="#FFFFFF", transparency=0):
    text_props = dict(show=literal("true"), text=literal(quote(words)),
                      fontFamily=literal("'Segoe UI'"), fontSize=literal("12D"),
                      bold=literal("false"), fontColor=color("#2B2427"),
                      horizontalAlignment=literal("'left'"), verticalAlignment=literal("'middle'"),
                      leftMargin=literal("12D"), rightMargin=literal("8D"))
    fills, texts = [], []
    for state in (None, "default", "hover", "selected", "disabled"):
        item = {"properties": dict(show=literal("true"),
                fillColor=color("#FCA356" if words and state == "hover" else background),
                transparency=literal(f"{transparency}D"))}
        if state:
            item["selector"] = {"id": state}
        fills.append(item)
        texts.append({"properties": deepcopy(text_props),
                      **({"selector": {"id": state}} if state else {})})
    value = {
        "$schema": BASE + "visualContainer/2.7.0/schema.json",
        "name": ident(pid + ":" + key), "position": desktop,
        "visual": {
            "visualType": "actionButton",
            "objects": {"shape": obj(tileShape=literal("'rectangle'"), roundEdge=literal("8D")),
                        "text": texts, "fill": fills,
                        "outline": obj(show=literal("false")), "icon": obj(show=literal("false"))},
            "visualContainerObjects": {
                "title": obj(show=literal("false")),
                "background": obj(show=literal("false")),
                "border": obj(show=literal("false")),
                "general": obj(altText=literal(quote("Mobile: " + (words or "Dismiss navigation")))),
                "visualLink": obj(show=literal("true"), type=literal("'Bookmark'"),
                                  bookmark=literal(quote(bookmark)), tooltip=literal(quote(words or "Close menu"))),
            },
        },
    }
    if hidden:
        value["isHidden"] = True
    return value


def formatting(v, caption=None, compact=False, context=False):
    """Only mobile overrides: inherit colours, icons, rules and all query bindings."""
    kind = vtype(v)
    out = {}
    source = v.get("visual", {}).get("objects", {})
    date_or_unknown = any("Journey detail label" in r or r.endswith("Journey providers 4") for r in references(v))
    font_by_group = {
        "value": 12 if context else 10 if compact and date_or_unknown else 18 if compact else 26, "label": 11, "labels": 10,
        "categoryLabels": 10, "categoryAxis": 10, "valueAxis": 10,
        "legend": 10, "columnHeaders": 10, "values": 11,
        "referenceLabelValue": 11, "referenceLabelTitle": 10,
        "text": 12, "items": 12, "header": 12,
    }
    for group, entries in source.items():
        changed = []
        for entry in entries:
            props = {}
            for key, value in entry.get("properties", {}).items():
                if key in {"fontSize", "textSize"} and group in font_by_group:
                    props[key] = literal(f"{font_by_group[group]}D")
                elif kind == "textbox" and key == "paragraphs":
                    paras = deepcopy(value)
                    for para in paras:
                        for run in para.get("textRuns", []):
                            run.setdefault("textStyle", {})["fontSize"] = "12pt"
                    props[key] = paras
                elif kind in CARDS and group in {"image", "cardImage"} and key in {"height", "width", "imageSize"}:
                    props[key] = literal("24D")
            if props:
                changed_entry = {"properties": props}
                if "selector" in entry:
                    changed_entry["selector"] = deepcopy(entry["selector"])
                changed.append(changed_entry)
        if changed:
            out[group] = changed
    if kind in TABLES:
        out["grid"] = obj(rowPadding=literal("8D"))
        out.setdefault("columnHeaders", obj(fontSize=literal("10D")))
        out.setdefault("values", obj(fontSize=literal("11D")))
    if kind == "actionButton":
        for entry in out.get("text", []):
            source_entry = next((e for e in source.get("text", [])
                                 if e.get("selector") == entry.get("selector")), {})
            entry["properties"] = {**deepcopy(source_entry.get("properties", {})),
                                   **entry["properties"]}
            entry["properties"].update(topMargin=literal("0D"), bottomMargin=literal("0D"),
                                       leftMargin=literal("12D"), rightMargin=literal("12D"),
                                       verticalAlignment=literal("'middle'"))
        out["icon"] = [{"properties": {"show": literal("false")}, **({"selector": e["selector"]} if "selector" in e else {})}
                       for e in source.get("icon", [{}])]
        out["shape"] = [{"properties": {"tileShape": literal("'rectangle'"), "roundEdge": literal("8D")},
                         **({"selector": e["selector"]} if "selector" in e else {})}
                        for e in source.get("shape", [{}])]
    container = {"title": obj(fontSize=literal("12D"), titleWrap=literal("true"))}
    if caption:
        container["title"] = obj(show=literal("true"), text=literal(quote(caption)),
                                 fontSize=literal("12D"), titleWrap=literal("true"))
    if kind in CARDS and compact:
        container["title"] = obj(show=literal("false"))
    return out, container


class PhonePage:
    def __init__(self, pid, page, visuals):
        self.pid, self.page, self.visuals = pid, page, visuals
        self.mobile = {}
        self.records = []
        self.used = set()
        self.y = 72
        self.tab = 100

    def absolute(self, v):
        p = deepcopy(v["position"])
        parent = v.get("parentGroupName")
        while parent:
            g = self.visuals[parent]
            p["x"] += g["position"]["x"]
            p["y"] += g["position"]["y"]
            parent = g.get("parentGroupName")
        return p

    def hidden(self, v):
        if v.get("isHidden"):
            return True
        parent = v.get("parentGroupName")
        return self.hidden(self.visuals[parent]) if parent else False

    def put(self, v, rect, role="body", caption=None, compact=False, overrides=None):
        assert v["name"] not in self.mobile, (self.pid, v["name"])
        rect["tabOrder"] = 0 if role == "header" else 10 if role == "menu opener" else self.tab
        self.tab += 10
        props, container = formatting(v, caption, compact, role in {"context", "freshness"})
        if role.startswith("drawer") or role in {"header", "menu opener"}:
            props, container = {}, {}
        if overrides:
            props.update(overrides)
        mobile = {"$schema": MOBILE_SCHEMA, "position": rect}
        if props:
            mobile["objects"] = props
        if container and vtype(v) != "group":
            mobile["visualContainerObjects"] = container
        self.mobile[v["name"]] = mobile
        self.used.add(v["name"])
        self.records.append(dict(id=v["name"], role=role, type=vtype(v),
                                 text=caption or title(v) or plain(v) or label(v),
                                 position=deepcopy(rect), hidden=self.hidden(v)))

    def block(self, v, height, role="body", caption=None):
        self.put(v, position(0, self.y, WIDTH, height, self.tab), role, caption)
        self.y += height + GAP

    def text_height(self, text, width=WIDTH):
        return max(40, 24 + 18 * ((len(text) + int(width / 7) - 1) // int(width / 7)))

    def plan(self):
        guide = self.page["displayName"].endswith(" - Guide")
        threshold = 0 if guide or self.pid == "1fd2b1f8c98559e99f4d" else 290
        filter_groups = [v for v in self.visuals.values() if "Filters drawer" in v.get("visualGroup", {}).get("displayName", "")]
        filter_buttons = [v for v in self.visuals.values() if vtype(v) == "actionButton" and "filters" in alt(v).lower()]
        if filter_groups:
            self.y = 136
        candidates = [v for v in self.visuals.values() if not self.hidden(v) and not alt(v).startswith("Mobile:")
                      and (self.absolute(v)["x"] >= threshold or prop(v, "visualContainerObjects", "visualLink", "type") == "Back")]
        texts = [v for v in candidates if vtype(v) == "textbox" and plain(v).strip()]
        data = [v for v in candidates if vtype(v) not in CHROME | {"group"}]

        # Journey milestones are a vertical, touch-sized list, not a squeezed rail.
        journey_icons = [v for v in candidates if vtype(v) == "image" and
                         (alt(v).startswith("Filter to ") or alt(v).startswith("Focus activity for ") or alt(v).startswith("Unavailable: separate provider confirmation"))]
        journey_cards = [v for v in data if any(re.search(r"(Journey providers|Rail referrals|Journey detail label) \d$", r) for r in references(v))]
        journey = []
        for icon in sorted(journey_icons, key=lambda v: self.absolute(v)["x"]):
            ip = self.absolute(icon)
            nearby = [v for v in texts if abs((self.absolute(v)["x"] + self.absolute(v)["width"] / 2)
                          - (ip["x"] + ip["width"] / 2)) < 100 and 0 <= self.absolute(v)["y"] - ip["y"] < 120]
            counts = [v for v in journey_cards if abs((self.absolute(v)["x"] + self.absolute(v)["width"] / 2)
                          - (ip["x"] + ip["width"] / 2)) < 100]
            if nearby and counts:
                journey.append((icon, min(nearby, key=lambda v: self.absolute(v)["y"]), counts[0]))
        journey_ids = {v["name"] for triplet in journey for v in triplet}

        # Headline card labels and chart headings belong to their visual, not extra rows.
        captions = {}
        assigned_text = set()
        for v in data:
            if v["name"] in journey_ids:
                continue
            p = self.absolute(v)
            if vtype(v) in CARDS and p["height"] < 80 and p["width"] < 320 and p["y"] > 160:
                pool = [t for t in texts if t["name"] not in journey_ids and
                        abs(self.absolute(t)["x"] - p["x"]) < 24 and
                        0 <= self.absolute(t)["y"] - (p["y"] + p["height"]) < 40]
            elif vtype(v) not in CARDS and not title(v):
                pool = [t for t in texts if t["name"] not in journey_ids and
                        abs(self.absolute(t)["x"] - p["x"]) < 24 and
                        0 <= p["y"] - (self.absolute(t)["y"] + self.absolute(t)["height"]) < 90
                        and self.absolute(t)["height"] <= 40 and len(plain(t)) < 100]
            else:
                pool = []
            if pool:
                caption = min(pool, key=lambda t: abs(self.absolute(t)["y"] - p["y"]))
                captions[v["name"]] = plain(caption)
                assigned_text.add(caption["name"])

        units = []
        for v in candidates:
            if v["name"] in journey_ids or v["name"] in assigned_text or vtype(v) == "group" or v in filter_buttons:
                continue
            p, kind = self.absolute(v), vtype(v)
            words = plain(v)
            if kind in {"shape", "image"}:
                continue  # decorative surrounds; native data-card icons still inherit
            if kind == "textbox":
                if not words.strip() or p["height"] <= 4 or "Version:" in words:
                    continue
                if not guide and p["y"] < 160:
                    continue
                if "WMPP" in words and " / " in words:
                    continue
                if words in {"Referral created", "Provider search", "Offers received", "Offer accepted", "IPA created", "IPA signed", "Provider signed", "Message activity only", "Provider confirmation", "Offers made"}:
                    continue
                if "Right-click" in words or "right-click" in words:
                    continue  # Desktop gesture; the existing detail button is retained
            if kind == "actionButton":
                is_back = prop(v, "visualContainerObjects", "visualLink", "type") == "Back"
                if (p["y"] < 160 and not is_back) or label(v) == "i" or (label(v).strip() == "" and not is_back):
                    continue
            if kind in CARDS:
                if any(r.startswith("Min(") for r in references(v)):
                    continue  # raw technical identifiers added as card overlays
                if p["y"] < 160 or any("As Of" in r or "Gold Model Last Refreshed" in r for r in references(v)):
                    continue  # timestamps move to the footer below
            units.append((p["y"], p["x"], "visual", v))
        if journey:
            units.append((min(self.absolute(x[0])["y"] for x in journey), 0, "journey", journey))
        units.sort(key=lambda u: (round(u[0] / 50) * 50, u[1]))
        if self.pid == "364f2cdd67ba7822850c":
            buttons = [u for u in units if u[2] == "visual" and vtype(u[3]) == "actionButton"]
            paired = []
            used_home = set()
            for button in buttons:
                bp = self.absolute(button[3])
                choices = [u for u in units if vtype(u[3]) == "textbox" and u[3]["name"] not in used_home
                           and self.absolute(u[3])["y"] > bp["y"] and
                           abs(self.absolute(u[3])["x"] + self.absolute(u[3])["width"] / 2 - bp["x"] - bp["width"] / 2) < 160]
                paired.append(button)
                used_home.add(button[3]["name"])
                if choices:
                    chosen = min(choices, key=lambda u: self.absolute(u[3])["y"])
                    paired.append(chosen)
                    used_home.add(chosen[3]["name"])
            units = [u for u in units if u[3]["name"] not in used_home and self.absolute(u[3])["y"] < 700] + paired + [u for u in units if u[3]["name"] not in used_home and self.absolute(u[3])["y"] >= 700]

        i = 0
        while i < len(units):
            oy, _ox, kind, value = units[i]
            if kind == "journey":
                for icon, text, card in value:
                    self.put(icon, position(0, self.y, 48, 48, self.tab), "journey icon")
                    self.put(text, position(60, self.y, 180, 48, self.tab), "journey label")
                    unavailable = alt(icon).startswith("Unavailable:")
                    self.put(card, position(240 if unavailable else 252, self.y, 83 if unavailable else 71, 48, self.tab), "journey count", compact=True)
                    self.y += 60
                self.y += 8
                i += 1
                continue
            v = value
            vt = vtype(v)
            caption = captions.get(v["name"])
            if vt in CARDS:
                p = self.absolute(v)
                is_sentence = p["width"] > 1000 or any("summary" in r.lower() or "context" in r.lower() or "coverage" in r.lower() for r in references(v))
                ref_shown = any(decode(e.get("properties", {}).get("show", {})) == "true"
                                for e in v.get("visual", {}).get("objects", {}).get("referenceLabel", []))
                if is_sentence:
                    self.block(v, 100, "context")
                elif ref_shown or vt == "multiRowCard" or len(projections(v)) > 1:
                    self.block(v, 200, "KPI", caption)
                else:
                    pair = None
                    if i + 1 < len(units):
                        ny, nx, nk, nv = units[i + 1]
                        if nk == "visual" and vtype(nv) in CARDS and abs(ny - oy) < 70 and self.absolute(nv)["width"] < 1000:
                            nr = any(decode(e.get("properties", {}).get("show", {})) == "true" for e in nv.get("visual", {}).get("objects", {}).get("referenceLabel", []))
                            if not nr and len(projections(nv)) == 1:
                                pair = nv
                    self.put(v, position(0, self.y, 158 if pair else WIDTH, 136, self.tab), "KPI", caption)
                    if pair:
                        self.put(pair, position(165, self.y, 158, 136, self.tab), "KPI", captions.get(pair["name"]))
                        i += 1
                    self.y += 148
            elif vt in TABLES:
                self.block(v, 180 if len(projections(v)) <= 4 and self.absolute(v)["height"] < 180 else 360, "table", caption)
            elif vt in MAPS:
                self.block(v, 340, "map", caption)
            elif vt == "slicer" or "Filter" in vt or "searchBox" in vt:
                self.block(v, 104, "filter")
            elif vt == "textbox":
                self.block(v, self.text_height(plain(v)), "text")
            elif vt == "actionButton":
                pair = None
                if label(v) in {"Chart", "Table"} and i + 1 < len(units):
                    ny, nx, nk, nv = units[i + 1]
                    if nk == "visual" and label(nv) in {"Chart", "Table"} and abs(ny - oy) < 12:
                        pair = nv
                if pair:
                    self.put(v, position(0, self.y, 158, 48, self.tab), "view toggle")
                    self.put(pair, position(165, self.y, 158, 48, self.tab), "view toggle")
                    self.y += 60
                    i += 1
                else:
                    self.block(v, 64 if self.pid == "364f2cdd67ba7822850c" else 48, "action")
            else:
                self.block(v, 280, "chart", caption)
            i += 1

        # Existing hidden chart/table alternatives share their counterpart's slot.
        for v in self.visuals.values():
            if v["name"] in self.used or vtype(v) in CHROME | CARDS | {"slicer", "group"} or not self.hidden(v):
                continue
            p = self.absolute(v)
            pool = [u for u in data if u["name"] in self.mobile and vtype(u) not in CARDS and
                    abs(self.absolute(u)["x"] - p["x"]) < 50 and abs(self.absolute(u)["y"] - p["y"]) < 100]
            if pool:
                base = min(pool, key=lambda u: abs(self.absolute(u)["y"] - p["y"]))
                self.put(v, deepcopy(self.mobile[base["name"]]["position"]), "alternative", captions.get(base["name"]))

        # Keep source-model timestamps readable, secondary and at the end.
        timestamps = [v for v in candidates if vtype(v) in CARDS and
                      (self.absolute(v)["y"] < 160 or any("As Of" in r or "Gold Model Last Refreshed" in r for r in references(v)))]
        for v in timestamps:
            self.block(v, 72, "freshness", compact_caption(v))

        # Reuse native filter bookmarks, including their exact filter fields.
        # Parent-group positions are absolute; children remain local to the group.
        for group in filter_groups:
            children = [v for v in self.visuals.values() if v.get("parentGroupName") == group["name"]]
            fields = sorted([v for v in children if vtype(v) == "slicer" or "Filter" in vtype(v)], key=lambda v: v["position"]["y"])
            height = 64 + len(fields) * 112 + 12
            self.put(group, position(0, 136, WIDTH, height, 700000), "filter group")
            for index, field in enumerate(fields):
                self.put(field, position(12, 56 + index * 112, 299, 100, 10 + index), "drawer filter")
            for child in children:
                if child["name"] in self.used:
                    continue
                if vtype(child) == "shape":
                    self.put(child, position(0, 0, WIDTH, height, 0), "filter background")
                elif vtype(child) == "textbox" and plain(child):
                    self.put(child, position(12, 12, 211, 36, 5), "filter heading")

        # Preserve grouped children: PBIR positions are relative to their parent.
        for gid, group in self.visuals.items():
            children = [v for v in self.visuals.values() if v.get("parentGroupName") == gid and v["name"] in self.mobile]
            if not children or self.hidden(group):
                continue
            rects = [self.mobile[v["name"]]["position"] for v in children]
            x, y = min(p["x"] for p in rects), min(p["y"] for p in rects)
            right, bottom = max(p["x"] + p["width"] for p in rects), max(p["y"] + p["height"] for p in rects)
            self.put(group, position(x, y, right - x, bottom - y, group["position"]["z"]), "group")
            for child in children:
                self.mobile[child["name"]]["position"]["x"] -= x
                self.mobile[child["name"]]["position"]["y"] -= y
        return self


def compact_caption(v):
    return "Data as of" if any("As Of" in r for r in references(v)) else "Gold model updated"


def snapshot():
    return {p.relative_to(PROJECT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PROJECT.rglob("*") if p.is_file() and
            ("/definition/" in p.as_posix() or p.name == "definition.pbir")}


def digest_mapping(values):
    return hashlib.sha256("\n".join(k + ":" + v for k, v in sorted(values.items())).encode()).hexdigest()


def transport_checksum(text):
    result = 2166136261
    encoded = text.encode("utf-16-le")
    for index in range(0, len(encoded), 2):
        unit = encoded[index] | encoded[index + 1] << 8
        result = ((result ^ unit) * 16777619) & 0xFFFFFFFF
    return result


def patch_chunks(pieces):
    chunks, current = [], ""
    for piece in pieces:
        if current and len(current) + len(piece) > 35000:
            chunks.append(current)
            current = ""
        current += piece
    if current:
        chunks.append(current)
    return chunks


def apply_through_cli(pieces, executable, limit=None):
    """Use the supplied apply_patch executable; never write files directly.

    Small append-at-EOF patches avoid Windows' command-line length limit.
    Large new JSON files finish before the next file is started.
    """
    completed = 0

    def invoke(patch):
        command = [executable, "--codex-run-as-apply-patch", patch]
        assert len(subprocess.list2cmdline(command)) < 30000, "Windows argument limit"
        result = subprocess.run(command, cwd=ROOT.parent, capture_output=True,
                                encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stderr or result.stdout

    for piece in pieces:
        if not piece:
            continue
        lines = piece.splitlines()
        if lines[0].startswith("*** Add File: "):
            path = lines[0].split(": ", 1)[1]
            assert Path(path).resolve().is_relative_to(PROJECT.resolve()), path
            content_lines = [line[1:] for line in lines[1:]]
            if any(len(line) > 10000 for line in content_lines):
                content_lines = json_text(json.loads("\n".join(content_lines))).splitlines()
            cursor, previous = 0, []
            while cursor < len(content_lines):
                first = cursor == 0
                header = f"*** Add File: {path}\n" if first else f"*** Update File: {path}\n@@\n" + "\n".join(" " + line for line in previous[-3:]) + "\n"
                tail = "" if first else "*** End of File\n"
                end = cursor
                body = ""
                while end < len(content_lines):
                    next_body = body + "+" + content_lines[end] + "\n"
                    payload = "*** Begin Patch\n" + header + next_body + tail + "*** End Patch"
                    if len(subprocess.list2cmdline([executable, "--codex-run-as-apply-patch", payload])) > 22000:
                        break
                    body = next_body
                    end += 1
                assert end > cursor, path
                invoke("*** Begin Patch\n" + header + body + tail + "*** End Patch")
                previous = content_lines[:end]
                cursor = end
            assert read(Path(path)) == json.loads("\n".join(content_lines)), path
        else:
            invoke("*** Begin Patch\n" + piece + "*** End Patch")
        completed += 1
        if completed % 25 == 0:
            print(json.dumps({"applied_files": completed}), flush=True)
        if limit and completed >= limit:
            break
    return completed


def validate_documents(documents):
    from jsonschema import Draft7Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT7

    cache = {}

    def retrieve(uri):
        base_uri = uri.split("#")[0]
        if base_uri not in cache:
            assert base_uri.startswith("https://developer.microsoft.com/json-schemas/"), base_uri
            with urlopen(base_uri, timeout=30) as response:
                cache[base_uri] = json.load(response)
        return Resource.from_contents(cache[base_uri], default_specification=DRAFT7)

    registry = Registry(retrieve=retrieve)
    count = 0
    for name, value in documents:
        if "$schema" not in value:
            continue
        schema = retrieve(value["$schema"]).contents
        errors = list(Draft7Validator(schema, registry=registry).iter_errors(value))
        assert not errors, name + ": " + "; ".join(e.message for e in errors[:5])
        count += 1
    return {"schema_documents": count, "schema_resources": len(cache)}


def verify_saved(validate_schema=False):
    manifest = read(PROJECT / "MOBILE_LAYOUT_DELIVERY.json")
    expected_new = {vid for page in manifest["pages"] for vid in page["new_visual_ids"]}
    new_bookmarks = set(manifest["new_bookmark_ids"])
    hashes = snapshot()
    model = {k: v for k, v in hashes.items() if k.startswith("SM_WMPP_v16.SemanticModel/")}
    protected = {k: v for k, v in hashes.items() if k.startswith("SM_WMPP_v16.Report/") and
                 not k.endswith("/mobile.json") and k != "SM_WMPP_v16.Report/definition/bookmarks/bookmarks.json" and
                 not (k.endswith("/visual.json") and Path(k).parent.name in expected_new) and
                 not (k.endswith(".bookmark.json") and Path(k).name.split(".")[0] in new_bookmarks)}
    assert len(protected) == manifest["original_report_files"], "Original report-file inventory changed"
    assert digest_mapping(protected) == manifest["original_report_hash"], "Original Desktop definitions changed"
    assert digest_mapping(model) == manifest["original_model_hash"], "Semantic model changed"
    metadata = read(REPORT / "bookmarks/bookmarks.json")
    assert metadata["items"][:-1] == manifest["original_bookmark_index"]["items"], "Original bookmark index changed"
    assert set(metadata["items"][-1]["children"]) == new_bookmarks
    documents, pages_checked, overlaps, filter_ids = [], [], [], set()
    for page in manifest["pages"]:
        folder = REPORT / "pages" / page["id"] / "visuals"
        visuals = {v["name"]: v for f in folder.glob("*/visual.json") if (v := read(f))}
        mobile = {f.parent.name: read(f) for f in folder.glob("*/mobile.json")}
        filter_ids.update(v["name"] for v in visuals.values() if "Filters drawer" in v.get("visualGroup", {}).get("displayName", ""))
        assert set(mobile) == set(page["original_mobile_visual_ids"]) | set(page["new_visual_ids"]), page["name"]
        records = []
        for vid, state in mobile.items():
            source = visuals[vid]
            rect = deepcopy(state["position"])
            parent = source.get("parentGroupName")
            hidden = bool(source.get("isHidden"))
            while parent:
                assert parent in mobile, (page["name"], vid, parent)
                rect["x"] += mobile[parent]["position"]["x"]
                rect["y"] += mobile[parent]["position"]["y"]
                hidden |= bool(visuals[parent].get("isHidden"))
                parent = visuals[parent].get("parentGroupName")
            assert rect["x"] >= 0 and rect["x"] + rect["width"] <= WIDTH + 0.001, (page["name"], vid, rect)
            assert rect["y"] >= 0 and rect["height"] > 0
            if not hidden and vtype(source) != "group":
                records.append((vid, rect))
            if vtype(source) == "actionButton" or prop(source, "visualContainerObjects", "visualLink", "show") == "true":
                assert rect["height"] >= 44 and rect["width"] >= 44, (page["name"], vid, "Small touch target")
            documents.append((str(folder / vid / "mobile.json"), state))
            if vid in expected_new:
                assert source["position"]["x"] > read(folder.parent / "page.json")["width"], (page["name"], vid, "Desktop intrusion")
                if vtype(source) == "actionButton":
                    linked = prop(source, "visualContainerObjects", "visualLink", "bookmark")
                    assert (REPORT / "bookmarks" / (linked + ".bookmark.json")).exists(), (page["name"], vid, linked)
                documents.append((str(folder / vid / "visual.json"), source))
        for index, (a, ar) in enumerate(records):
            for b, br in records[index + 1:]:
                if min(ar["x"] + ar["width"], br["x"] + br["width"]) - max(ar["x"], br["x"]) > 0.01 and min(ar["y"] + ar["height"], br["y"] + br["height"]) - max(ar["y"], br["y"]) > 0.01:
                    overlaps.append((page["name"], a, b))
        pages_checked.append({"name": page["name"], "phone_visuals": len(mobile), "height": page["content_height"]})
    assert not overlaps, f"Visible phone visuals overlap: {overlaps[:10]}"
    for bid in new_bookmarks:
        b = read(REPORT / "bookmarks" / (bid + ".bookmark.json"))
        assert b["options"]["suppressData"] is True
        assert set(b["options"]["targetVisualNames"]) <= expected_new | filter_ids
        assert b["explorationState"]["activeSection"] not in manifest["excluded_pages"]
        assert b["explorationState"]["activeSection"] != "1fd2b1f8c98559e99f4d" or "Go to" not in b["displayName"], "Restricted extract exposed"
        for pid, section in b["explorationState"]["sections"].items():
            for vid in section["visualContainers"]:
                assert (REPORT / "pages" / pid / "visuals" / vid / "visual.json").exists()
        documents.append((bid, b))
    documents.append(("bookmark index", metadata))
    checks = validate_documents(documents) if validate_schema else {}
    return {"pages": len(pages_checked), "mobile_visuals": sum(p["phone_visuals"] for p in pages_checked),
            "original_report_files_preserved": len(protected), "semantic_model_unchanged": True,
            "visible_overlaps": len(overlaps), "bookmarks": len(new_bookmarks),
            "display_only_bookmarks": True, "desktop_render_verified": False, "phone_render_verified": False,
            "checks": checks, "page_inventory": pages_checked}


def refine_navigation_states(executable):
    """Keep new drawer buttons neutral except on hover; never touch old visuals."""
    manifest = read(PROJECT / "MOBILE_LAYOUT_DELIVERY.json")
    pieces = []
    for page in manifest["pages"]:
        for vid in page["new_visual_ids"]:
            path = REPORT / "pages" / page["id"] / "visuals" / vid / "visual.json"
            value = read(path)
            if vtype(value) != "actionButton":
                continue
            old = path.read_text(encoding="utf-8-sig")
            fills = value["visual"]["objects"]["fill"]
            neutral = deepcopy(fills[0]["properties"]["fillColor"])
            for entry in fills:
                if entry.get("selector", {}).get("id") == "selected" or not label(value):
                    entry["properties"]["fillColor"] = deepcopy(neutral)
            new = json_text(value)
            if old == new:
                continue
            pieces.append("*** Update File: " + path.as_posix() + "\n@@\n" +
                          "\n".join("-" + line for line in old.splitlines()) + "\n" +
                          "\n".join("+" + line for line in new.splitlines()) + "\n")
    return apply_through_cli(pieces, executable)


def separate_filter_close_controls(executable):
    """Keep mobile-only close buttons out of original Desktop groups."""
    path = PROJECT / "MOBILE_LAYOUT_DELIVERY.json"
    manifest = read(path)
    pieces = []

    def replace_file(target, value):
        old = target.read_text(encoding="utf-8-sig").splitlines()
        new = json_text(value).splitlines()
        diff = list(difflib.unified_diff(old, new, n=8, lineterm=""))[2:]
        if not diff:
            return
        pieces.append("*** Update File: " + target.as_posix() + "\n" +
                      "\n".join("@@" if line.startswith("@@") else line for line in diff) + "\n")

    for page in manifest["pages"]:
        pid = page["id"]
        close_path = REPORT / "pages" / pid / "visuals" / ident(pid + ":filter-close") / "visual.json"
        if not close_path.exists():
            continue
        close = read(close_path)
        group_id = close.pop("parentGroupName", None)
        if group_id is None:
            continue
        close["isHidden"] = True
        close["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]["bookmark"] = literal(quote(ident(pid + ":filter-close-bookmark")))
        replace_file(close_path, close)
        close_mobile_path = close_path.with_name("mobile.json")
        close_mobile = read(close_mobile_path)
        close_mobile["position"]["y"] = 144
        replace_file(close_mobile_path, close_mobile)
        opener_path = REPORT / "pages" / pid / "visuals" / ident(pid + ":filter-open") / "visual.json"
        opener = read(opener_path)
        opener["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]["bookmark"] = literal(quote(ident(pid + ":filter-open-bookmark")))
        replace_file(opener_path, opener)
        for verb in ("open", "close"):
            bid = ident(pid + ":filter-" + verb + "-bookmark")
            section = {"visualContainers": {close["name"]: {"singleVisual": {"visualType": "actionButton", "objects": {}, **({} if verb == "open" else {"display": {"mode": "hidden"}})}}},
                       "visualContainerGroups": {group_id: {"isHidden": verb != "open"}}}
            b = {"$schema": BASE + "bookmark/2.1.0/schema.json", "name": bid,
                 "displayName": "Mobile | " + page["name"] + " | " + verb + " filters",
                 "options": {"applyOnlyToTargetVisuals": True, "targetVisualNames": [close["name"], group_id], "suppressActiveSection": True, "suppressData": True},
                 "explorationState": {"version": "1.0", "activeSection": pid, "sections": {pid: section}}}
            pieces.append(add_file(REPORT / "bookmarks" / (bid + ".bookmark.json"), b))
            manifest["new_bookmark_ids"].append(bid)
    for mobile_path in REPORT.glob("pages/*/visuals/*/mobile.json"):
        source = read(mobile_path.with_name("visual.json"))
        parent = source.get("parentGroupName")
        if not parent:
            continue
        group = read(mobile_path.parent.parent / parent / "visual.json")
        if "Filters drawer" not in group.get("visualGroup", {}).get("displayName", ""):
            continue
        mobile = read(mobile_path)
        if mobile["position"]["z"] >= 700000:
            mobile["position"]["z"] -= 700000
            replace_file(mobile_path, mobile)
    manifest["new_bookmarks"] = len(manifest["new_bookmark_ids"])
    replace_file(path, manifest)
    metadata_path = REPORT / "bookmarks/bookmarks.json"
    metadata = read(metadata_path)
    metadata["items"][-1]["children"] = manifest["new_bookmark_ids"]
    replace_file(metadata_path, metadata)
    return apply_through_cli(pieces, executable)


def build_plan():
    assert not (PROJECT / "MOBILE_LAYOUT_DELIVERY.json").exists(), "Mobile layout already delivered; inspect before revising."
    old_hashes = snapshot()
    pages = {p.parent.name: read(p) for p in REPORT.glob("pages/*/page.json") if p.parent.name not in EXCLUDE}
    phones, additions, patches = {}, {}, []
    drawer_states = {}
    for pid, page in pages.items():
        visuals = {v["name"]: v for p in (REPORT / "pages" / pid).glob("visuals/*/visual.json") if (v := read(p))}
        phone = PhonePage(pid, page, visuals).plan()
        phones[pid] = phone
        # New navigation is parked outside Desktop's fixed canvas, not over content.
        desktop = position(page["width"] + 80, 20, 323, 48, 1000000)
        new = []
        short_title = page["displayName"].replace(" (Drillthrough)", "").replace("WMPP Homepage", "WMPP").replace(" - Guide", " guide")
        header = new_text(pid, "header", short_title, deepcopy(desktop), size=17)
        new.append((header, position(0, 8, 243, 56, 500000), "header"))
        opener = new_button(pid, "open", "☰ Menu", deepcopy(desktop), ident(pid + ":open-bookmark"))
        new.append((opener, position(247, 8, 76, 48, 500001), "menu opener"))
        scrim = new_button(pid, "scrim", "", deepcopy(desktop), ident(pid + ":close-bookmark"), True, "#2B2427", 45)
        new.append((scrim, position(0, 0, WIDTH, 704, 1000000), "drawer scrim"))
        panel = new_text(pid, "panel", "", deepcopy(desktop), True, background="#FFFFFF")
        new.append((panel, position(0, 0, 276, 704, 1000010), "drawer panel"))
        heading = new_text(pid, "drawer-title", "WMPP", deepcopy(desktop), True, size=17)
        new.append((heading, position(12, 12, 180, 40, 1000020), "drawer heading"))
        closer = new_button(pid, "close", "✕ Close", deepcopy(desktop), ident(pid + ":close-bookmark"), True)
        new.append((closer, position(192, 8, 84, 48, 1000030), "drawer close"))
        filter_groups = [v for v in visuals.values() if "Filters drawer" in v.get("visualGroup", {}).get("displayName", "")]
        for group in filter_groups:
            relevant = [(b, read(b)) for b in (REPORT / "bookmarks").glob("*.bookmark.json")]
            opened = [b for path, b in relevant if b.get("explorationState", {}).get("activeSection") == pid and
                      b.get("explorationState", {}).get("sections", {}).get(pid, {}).get("visualContainerGroups", {}).get(group["name"], {}).get("isHidden") is False and
                      "open filters" in b["displayName"].lower()]
            closed = [b for path, b in relevant if b.get("explorationState", {}).get("activeSection") == pid and
                      "close overlays" in b["displayName"].lower()]
            assert len(opened) == len(closed) == 1, (page["displayName"], len(opened), len(closed))
            filter_open = new_button(pid, "filter-open", "Filters", deepcopy(desktop), ident(pid + ":filter-open-bookmark"))
            new.append((filter_open, position(0, 76, WIDTH, 48, 700050), "filter toggle"))
            filter_close = new_button(pid, "filter-close", "✕ Close", deepcopy(desktop), ident(pid + ":filter-close-bookmark"), True)
            new.append((filter_close, position(235, 144, 76, 44, 700030), "filter close"))
        for index, (words, target) in enumerate(DESTINATIONS):
            row_y = 64 + index * 48 + (24 if index >= 10 else 0)
            item = new_button(pid, "go:" + target, words, deepcopy(desktop), ident("go:" + target), True)
            new.append((item, position(8, row_y, 260, 44, 1000100 + index), "drawer link"))
        explorer_heading = new_text(pid, "explorers-heading", "EXPLORERS", deepcopy(desktop), True, size=10)
        new.append((explorer_heading, position(20, 544, 248, 24, 1000099), "drawer heading"))
        state = {}
        for visual, mobile_rect, role in new:
            phone.put(visual, mobile_rect, role)
            path = REPORT / "pages" / pid / "visuals" / visual["name"] / "visual.json"
            additions[path] = visual
            if role not in {"header", "filter toggle", "filter close"}:
                state[visual["name"]] = {"singleVisual": {"visualType": vtype(visual), "objects": {}}}
                if role != "menu opener":
                    state[visual["name"]]["singleVisual"]["display"] = {"mode": "hidden"}
        drawer_states[pid] = {"visualContainers": state}

    def bookmark(name, words, active, sections, navigate=False):
        return {"$schema": BASE + "bookmark/2.1.0/schema.json", "name": name, "displayName": words,
                "options": {"applyOnlyToTargetVisuals": True,
                            "targetVisualNames": sorted({vid for s in sections.values() for vid in s["visualContainers"]}),
                            "suppressActiveSection": not navigate, "suppressData": True},
                "explorationState": {"version": "1.0", "activeSection": active, "sections": sections}}

    bookmarks = []
    for pid, section in drawer_states.items():
        opened = deepcopy(section)
        for vid, entry in opened["visualContainers"].items():
            if vid == ident(pid + ":open"):
                entry["singleVisual"]["display"] = {"mode": "hidden"}
            else:
                entry["singleVisual"].pop("display", None)
        for state_name, sections in (("open", {pid: opened}), ("close", {pid: section})):
            bookmarks.append(bookmark(ident(pid + ":" + state_name + "-bookmark"),
                                      "Mobile | " + pages[pid]["displayName"] + " | " + state_name,
                                      pid, sections))
    for pid, phone in phones.items():
        groups = [v for v in phone.visuals.values() if "Filters drawer" in v.get("visualGroup", {}).get("displayName", "")]
        for group in groups:
            for verb in ("open", "close"):
                is_open = verb == "open"
                close_id = ident(pid + ":filter-close")
                section = {"visualContainers": {close_id: {"singleVisual": {"visualType": "actionButton", "objects": {}, **({} if is_open else {"display": {"mode": "hidden"}})}}},
                           "visualContainerGroups": {group["name"]: {"isHidden": not is_open}}}
                b = bookmark(ident(pid + ":filter-" + verb + "-bookmark"), "Mobile | " + pages[pid]["displayName"] + " | " + verb + " filters", pid, {pid: section})
                b["options"]["targetVisualNames"].append(group["name"])
                bookmarks.append(b)
    for words, target in DESTINATIONS:
        bookmarks.append(bookmark(ident("go:" + target), "Mobile | Go to " + words,
                                  target, deepcopy(drawer_states), True))

    for path, visual in additions.items():
        patches.append(add_file(path, visual))
    for pid, phone in phones.items():
        for vid, mobile in phone.mobile.items():
            patches.append(add_file(REPORT / "pages" / pid / "visuals" / vid / "mobile.json", mobile))
    for b in bookmarks:
        patches.append(add_file(REPORT / "bookmarks" / (b["name"] + ".bookmark.json"), b))
    index_path = REPORT / "bookmarks/bookmarks.json"
    old_index = index_path.read_text(encoding="utf-8-sig")
    metadata = read(index_path)
    group_metadata = {"name": ident("mobile-bookmark-group"), "displayName": "Mobile navigation",
                      "children": [b["name"] for b in bookmarks]}
    metadata["items"].append(group_metadata)
    # Exact replacement via apply_patch; everything preceding the append is unchanged.
    old_tail = old_index.splitlines()[-5:]
    assert old_tail[0].strip() == "{", "Inspect the last existing bookmark-index item"
    new_tail = old_tail[:2] + [old_tail[2] + ","] + ["    " + line for line in json_text(group_metadata).splitlines()] + old_tail[3:]
    patches.append("*** Update File: " + index_path.as_posix() + "\n@@\n" +
                   "\n".join("-" + line for line in old_tail) + "\n" +
                   "\n".join("+" + line for line in new_tail) + "\n")
    added_paths = {p.relative_to(PROJECT).as_posix() for p in additions}
    original_report = {k: v for k, v in old_hashes.items() if k.startswith("SM_WMPP_v16.Report/") and
                       k != "SM_WMPP_v16.Report/definition/bookmarks/bookmarks.json" and k not in added_paths}
    original_model = {k: v for k, v in old_hashes.items() if k.startswith("SM_WMPP_v16.SemanticModel/")}
    manifest = {"version": 1, "date": "2026-10-12", "project": str(PROJECT), "canvas_width": WIDTH,
                "pages": [{"id": pid, "name": p.page["displayName"], "content_height": p.y,
                           "placed_visuals": len(p.mobile), "original_mobile_visual_ids": sorted(set(p.mobile) - {v["name"] for path, v in additions.items() if path.parents[2].name == pid}),
                           "new_visual_ids": sorted(v["name"] for path, v in additions.items() if path.parents[2].name == pid)} for pid, p in phones.items()],
                "excluded_pages": sorted(EXCLUDE), "new_desktop_visuals": len(additions),
                "new_bookmarks": len(bookmarks), "new_bookmark_ids": [b["name"] for b in bookmarks],
                "original_report_hash": digest_mapping(original_report), "original_report_files": len(original_report),
                "original_model_hash": digest_mapping(original_model),
                "original_bookmark_index": read(index_path),
                "desktop_geometry_preserved": True, "semantic_model_unchanged": True,
                "native_render_verified": False,
                "limitations": ["Power BI uses show/hide bookmarks, not an animated slide transition.",
                                "Phone layouts are for the Power BI mobile app in portrait orientation.",
                                "Wide tables preserve every column and require horizontal panning.",
                                "Reopen Desktop and check Mobile layout before publishing."]}
    patches.append(add_file(PROJECT / "MOBILE_LAYOUT_DELIVERY.json", manifest))
    documents = [(str(path), v) for path, v in additions.items()]
    documents += [(pid + ":" + vid, v) for pid, p in phones.items() for vid, v in p.mobile.items()]
    documents += [(b["name"], b) for b in bookmarks] + [(str(index_path), metadata)]
    return {"patch": "*** Begin Patch\n" + "".join(patches) + "*** End Patch", "manifest": manifest, "pieces": patches, "documents": documents}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--page")
    parser.add_argument("--chunk", type=int)
    parser.add_argument("--serve-plan", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--serve-http", type=int)
    parser.add_argument("--apply-via")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--refine-navigation-via")
    parser.add_argument("--separate-filters-via")
    args = parser.parse_args()
    if args.separate_filters_via:
        print(json.dumps({"filter_controls_refined_files": separate_filter_close_controls(args.separate_filters_via)}))
    elif args.refine_navigation_via:
        print(json.dumps({"refined_navigation_visuals": refine_navigation_states(args.refine_navigation_via)}))
    elif args.verify:
        print(json.dumps(verify_saved(args.validate), ensure_ascii=False))
    elif args.apply_via:
        plan = build_plan()
        checks = validate_documents(plan["documents"]) if args.validate else {}
        print(json.dumps({"validated": checks, "remaining_files": sum(bool(p) for p in plan["pieces"])}), flush=True)
        count = apply_through_cli(plan["pieces"], args.apply_via, args.limit)
        print(json.dumps({"applied_files": count, "complete": args.limit is None}), flush=True)
    elif args.serve_http is not None:
        plan = build_plan()
        checks = validate_documents(plan["documents"]) if args.validate else {}
        chunks = patch_chunks(plan["pieces"])

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *unused):
                pass

            def do_GET(self):
                if self.path == "/stop":
                    result = {"stopped": True}
                    Thread(target=self.server.shutdown, daemon=True).start()
                elif self.path.startswith("/chunk/"):
                    index = int(self.path.rsplit("/", 1)[1])
                    payload = "*** Begin Patch\n" + chunks[index] + "*** End Patch"
                    result = {"patch": payload, "length": len(payload.encode("utf-16-le")) // 2,
                              "checksum": transport_checksum(payload)}
                else:
                    self.send_error(404)
                    return
                body = json.dumps(result, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        server = HTTPServer(("127.0.0.1", args.serve_http), Handler)
        print(json.dumps({"ready": True, "port": server.server_port,
                          "chunks": len(chunks), "files": len(plan["pieces"]), "checks": checks}), flush=True)
        server.serve_forever()
        server.server_close()
    elif args.serve_plan:
        plan = build_plan()
        checks = validate_documents(plan["documents"]) if args.validate else {}
        pieces = plan["pieces"]
        chunks = patch_chunks(pieces)
        print(json.dumps({"ready": True, "chunks": len(chunks),
                          "files": len(pieces), "checks": checks}), flush=True)
        for line in sys.stdin:
            request = json.loads(line)
            if request.get("stop"):
                break
            chunk = request["chunk"]
            payload = "*** Begin Patch\n" + chunks[chunk] + "*** End Patch"
            print(json.dumps({"patch": payload, "length": len(payload.encode("utf-16-le")) // 2,
                              "checksum": transport_checksum(payload)}, ensure_ascii=False), flush=True)
    elif args.plan:
        plan = build_plan()
        if args.chunk is not None:
            pieces = plan["pieces"]
            if args.chunk == -1:
                print(json.dumps({"chunks": (len(pieces) + 11) // 12,
                                  "files": len(pieces), "new_visuals": plan["manifest"]["new_desktop_visuals"],
                                  "bookmarks": plan["manifest"]["new_bookmarks"]}))
            else:
                print(json.dumps({"patch": "*** Begin Patch\n" + "".join(pieces[args.chunk * 12:(args.chunk + 1) * 12]) + "*** End Patch"}, ensure_ascii=False))
        else:
            print(json.dumps({k: v for k, v in plan.items() if k not in {"pieces", "documents"}}, ensure_ascii=False))
    else:
        result = []
        for p in REPORT.glob("pages/*/page.json"):
            if p.parent.name in EXCLUDE:
                continue
            if args.page and p.parent.name != args.page:
                continue
            page = read(p)
            visuals = {v["name"]: v for f in p.parent.glob("visuals/*/visual.json") if (v := read(f))}
            phone = PhonePage(page["name"], page, visuals).plan()
            result.append({"page": page["displayName"], "height": phone.y, "visuals": len(phone.mobile),
                           "filters": sum(r["role"] == "filter" for r in phone.records),
                           "tables": sum(r["role"] == "table" for r in phone.records),
                           **({} if args.summary else {"layout": phone.records})})
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

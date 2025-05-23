#!/usr/bin/env python3
"""
get_control_text.py  –  Dump the full official statement for one control ID.

Usage:
    python scripts/get_control_text.py ac-2 > ac2_official.txt
    python scripts/get_control_text.py ac-2 --catalog 800-171 > ...

By default it looks in controls/800-53.json.
"""
import argparse, json, pathlib, sys, textwrap
from typing import Dict, List, Optional

def cli() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("control_id", help="e.g. ac-2  (case-insensitive)")
    p.add_argument("--catalog", default="800-53", help="800-53 or 800-171")
    return p.parse_args()

args     = cli()
ctl_id   = args.control_id.lower()
json_path = pathlib.Path("controls") / f"{args.catalog}.json"

try:
    data = json.load(open(json_path))
except FileNotFoundError:
    sys.exit(f"❌ Catalog file {json_path} not found. Run fetch_controls.py first.")

def label(part: Dict) -> str:
    """Return the 'a.', '1.' etc. label if present."""
    for prop in part.get("props", []):
        if prop.get("name") == "label":
            return prop["value"] + " "
    return ""

def collect(part: Dict, out: List[str]) -> None:
    """Depth-first: append label+prose for this part, then recurse."""
    if "prose" in part:
        out.append(label(part) + part["prose"])
    for sub in part.get("parts", []):
        collect(sub, out)

def match_control(ctl: Dict) -> Optional[str]:
    if ctl["id"].lower() == ctl_id:
        lines: List[str] = [ctl["title"], ""]          # title + blank line
        for p in ctl.get("parts", []):
            collect(p, lines)
        return "\n".join(textwrap.fill(l, 90) if i > 1 else l   # wrap body only
                         for i, l in enumerate(lines))
    for sub in ctl.get("controls", []):
        txt = match_control(sub)
        if txt:
            return txt
    return None

for group in data["catalog"]["groups"]:
    for ctl in group.get("controls", []):
        txt = match_control(ctl)
        if txt:
            print(txt)
            sys.exit(0)

sys.exit(f"❌ Control {ctl_id.upper()} not found in {args.catalog}.")

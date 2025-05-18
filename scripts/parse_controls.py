#!/usr/bin/env python
import csv, json, pathlib, re

root = pathlib.Path(__file__).resolve().parents[1]
index_file = root / "controls_index.csv"

with open(index_file, "w", newline="") as out:
    w = csv.writer(out)
    w.writerow(["catalog", "control_id", "title"])

    for cat in (root / "controls").glob("*.json"):
        data = json.load(open(cat))
        for grp in data["catalog"]["groups"]:
            for ctl in grp.get("controls", []):
                w.writerow([cat.stem, ctl["id"], re.sub(r"\s+", " ", ctl["title"])])
print(f"Wrote {index_file}")

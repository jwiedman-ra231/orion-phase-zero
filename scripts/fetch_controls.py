#!/usr/bin/env python
"""Grab OSCAL JSON catalogs into ./controls."""
import pathlib, ssl, urllib.request as u, shutil

BASE = "https://raw.githubusercontent.com/usnistgov/oscal-content/main"
CATALOGS = {
    "800-53": f"{BASE}/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
    "800-171": f"{BASE}/nist.gov/SP800-171/rev2/json/NIST_SP-800-171_rev2_catalog.json",
}

dest = pathlib.Path(__file__).resolve().parents[1] / "controls"
dest.mkdir(exist_ok=True)

for name, url in CATALOGS.items():
    out = dest / f"{name}.json"
    print(f"Downloading {name} …", end=" ", flush=True)
    with u.urlopen(url, context=ssl.create_default_context()) as r, open(out, "wb") as f:
        shutil.copyfileobj(r, f)
    print("done")

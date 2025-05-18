#!/usr/bin/env python
"""
Download OSCAL catalogs into ./controls
• Authenticates with GITHUB_TOKEN if present (5 000 req/hr)
• Falls back to community 800-171 Rev 2 when Rev 3 404/403/429
"""

import os
import pathlib
import ssl
import urllib.request as u
import urllib.error as ue
import shutil
from dotenv import load_dotenv

# ---------- configuration ---------- #
CATALOGS = {
    "800-53": [
        "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json"
    ],
    "800-171": [
        # Try official Rev 3 first
        "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-171/rev3/json/NIST_SP-800-171_rev3_catalog.json",
        # Fallback to community Rev 2
        "https://raw.githubusercontent.com/FATHOM5/oscal/main/"
        "content/SP800-171/oscal-content/catalogs/"
        "NIST_SP-800-171_rev2_catalog.json",
    ],
}
# ----------------------------------- #

load_dotenv()                                # pulls in .env
TOKEN = os.getenv("GITHUB_TOKEN")            # may be None
ssl_ctx = ssl.create_default_context()

dest = pathlib.Path(__file__).resolve().parents[1] / "controls"
dest.mkdir(exist_ok=True)


def download(url: str, outfile: pathlib.Path) -> bool:
    """
    Return True on success.
    Return False on 404 / 403 / 429 so caller may try fallback.
    """
    headers = {"User-Agent": "orion-phase-zero"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    req = u.Request(url, headers=headers)

    try:
        with u.urlopen(req, context=ssl_ctx) as r, open(outfile, "wb") as f:
            shutil.copyfileobj(r, f)
        return True
    except ue.HTTPError as e:
        if e.code in (404, 403, 429):
            return False
        raise


for name, url_list in CATALOGS.items():
    out_file = dest / f"{name}.json"
    for url in url_list:
        print(f"{name}: trying {url.split('/')[-1]} …", end=" ", flush=True)
        if download(url, out_file):
            print("done")
            break
        else:
            print("skipped")
    else:
        raise RuntimeError(f"❌ All URLs failed for {name}")

print("✅ All catalogs downloaded to", dest.resolve())

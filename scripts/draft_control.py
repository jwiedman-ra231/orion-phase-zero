#!/usr/bin/env python3
"""
draft_control.py  – End-to-end Phase-Zero helper

Example:
    python scripts/draft_control.py ac-2 acme proj-001 \
        --odv '{"review_period":"30"}' \
        --context "Covers individual, shared, emergency accounts." \
        --evidence "List of active accounts" "Notifications of transfers"
"""

import argparse, json, subprocess, sys
from pathlib import Path

from build_prompt import build_prompt
# match_control isn’t used in this script, so no import needed
from bedrock_generate import generate
from record_control import main as record_control

def cli() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("control_id")
    p.add_argument("client_id")
    p.add_argument("project_id")
    p.add_argument("--odv", required=True,
                   help='JSON string, e.g. \'{"review_period":"30"}\'')
    p.add_argument("--context", default="", help="1-2-sentence blurb")
    p.add_argument("--evidence", nargs="*", default=[],
                   help="Bullet list for assessor evidence")
    return p.parse_args()

def load_control_text(control_id: str) -> str:
    txt = subprocess.check_output(
        ["python", "scripts/get_control_text.py", control_id],
        text=True)
    return txt

def run():
    args = cli()
    ctl_text = load_control_text(args.control_id)
    odv      = json.loads(args.odv)

    prompt = build_prompt(
        control_statement = ctl_text,
        context_blurb     = args.context,
        evidence_list     = args.evidence,
        odv               = odv,
        system_description= "(see system description)",  # tweak or parametrize
    )

    impl = generate(prompt)
    print("\n----- AI Draft -----\n")
    print(impl)
    print("\n--------------------\n")

    # Ask user to edit/approve
    input("Press Enter to accept and record, or Ctrl-C to abort…")

    record_control([
        args.client_id,
        args.project_id,
        args.control_id.upper(),
        json.dumps(odv),
        impl,
        "prompt-opus-v1"
    ])

if __name__ == "__main__":
    run()

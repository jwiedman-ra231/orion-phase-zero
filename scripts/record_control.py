#!/usr/bin/env python3
"""
record_control.py  –  Phase-Zero helper

Usage
-----
python scripts/record_control.py \
       <client_id> <project_id> <control_id> \
       '<ODV JSON string>' \
       '<final text>' \
       '<prompt hash or short name>'

Example
-------
python scripts/record_control.py \
       acme proj-001 AC-2 \
       '{"review_period":"30"}' \
       "$(cat ac2_final.txt)" \
       "prompt-2025-05-19"
"""

import argparse, json, datetime, pathlib, sys

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Save a completed control implementation to /records/"
    )
    p.add_argument("client_id")
    p.add_argument("project_id")
    p.add_argument("control_id")
    p.add_argument("odv_json",  help='e.g. \'{"review_period":"30"}\'')
    p.add_argument("final_text", help="The approved implementation paragraph")
    p.add_argument("prompt_used", help="Prompt identifier or hash")
    return p.parse_args()

def main() -> None:
    args = parse_args()

    try:
        odv = json.loads(args.odv_json)
    except json.JSONDecodeError as e:
        sys.exit(f"ODV JSON is invalid: {e}")

    record = {
        "client_id":   args.client_id,
        "project_id":  args.project_id,
        "control_id":  args.control_id,
        "odv":         odv,
        "final_text":  args.final_text,
        "prompt_used": args.prompt_used,
        "timestamp_utc": datetime.datetime.utcnow().isoformat(timespec="seconds"),
    }

    root = pathlib.Path(__file__).resolve().parents[1]   # repo root
    outdir = root / "records" / args.client_id
    outdir.mkdir(parents=True, exist_ok=True)

    outfile = outdir / f"{args.control_id}.json"
    outfile.write_text(json.dumps(record, indent=2))
    print(f"✅ saved {outfile.relative_to(root)}")

if __name__ == "__main__":
    main()

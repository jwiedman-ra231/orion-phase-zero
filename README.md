# Orion • Phase Zero   🚀

*Concierge‑style minimum‑viable workflow for drafting NIST 800‑53 / 800‑171 System Security Plan (SSP) control implementations with AI assistance.*

This repo shows how a two‑person security team can generate high‑quality control write‑ups in days —not weeks—using:

* **Static control catalogs** (800‑53 Rev 5 and 800‑171 Rev 2) downloaded once.
* **Amazon Bedrock** (Anthropic Claude 3 Opus on‑demand) for first‑draft text.
* **Lightweight JSON records** per control so nothing gets lost.
* **Manual interview & review** so quality remains human‑grade.

Phase Zero is file‑based—run everything from VS Code on a laptop; no web server or database required.

---

## Repository layout

```text
orion-phase-zero/
│
├── controls/               # raw OSCAL JSON catalogs (git‑ignored)
├── controls_index.csv      # ID → Title lookup table
├── records/                # one JSON per completed control
│   └── <client>/<ID>.json
├── scripts/
│   ├── fetch_controls.py   # download OSCAL catalogs
│   ├── parse_controls.py   # build controls_index.csv
│   ├── get_control_text.py # pull official prose for 1 control
│   ├── bedrock_generate.py # call Bedrock + Claude 3
│   └── record_control.py   # save final JSON record
├── templates/
│   └── SSP_template.docx   # Word skeleton for client delivery
├── interview/              # question lists + ODV cheat‑sheets
├── lessons/                # post‑engagement retrospectives
├── .env.example            # sample AWS / model vars
└── README.md
```

---

## Prerequisites

| Tool          | Version (tested) | Notes                                  |
| ------------- | ---------------- | -------------------------------------- |
| Python        | 3.9 +            | `python -m venv .venv`                 |
| AWS CLI       | 2.16 +           | SSO profile with `bedrock:InvokeModel` |
| AWS Bedrock   | us‑east‑1        | Claude 3 Opus **on‑demand** enabled    |
| Git & VS Code | any              | GitHub CLI optional                    |

---

## Quick‑start

```bash
# 1) clone & bootstrap
git clone https://github.com/<you>/orion-phase-zero.git
cd orion-phase-zero
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) set credentials
cp .env.example .env        # edit AWS_PROFILE / BR_MODEL

# 3) fetch & index catalogs (one‑time)
python scripts/fetch_controls.py
python scripts/parse_controls.py

# 4) draft first control
python scripts/get_control_text.py ac-2 > ac2.txt
python - <<'PY'
from scripts.bedrock_generate import generate
print(generate(open('ac2.txt').read(),
               {'review_period':'30'},
               'SaaS on AWS GovCloud'))
PY
# review → save final text
python scripts/record_control.py acme proj-001 AC-2 '{"review_period":"30"}' \
       "$(cat ac2_final.txt)" prompt-opus-v1
```

---

## Working cycle

1. **Interview** client – fill ODVs & system description.
2. **Pull** official control text (`get_control_text.py`).
3. **Generate** draft via Bedrock (`bedrock_generate.py`).
4. **Review / tweak** manually.
5. **Record** JSON (`record_control.py`).
6. **Paste** into Word template.
7. **Repeat** → export PDF – deliver.

---

## Model options

| Model ID                                    | Best use‑case                | Cost (in/out)         |
| ------------------------------------------- | ---------------------------- | --------------------- |
| `anthropic.claude-3-haiku-20240307-v1:0`    | Fast, cheap brainstorming    | \$0.00025 / \$0.00125 |
| `anthropic.claude-3-sonnet-20240229-v1:0`   | Balanced quality vs. cost    | \$0.003 / \$0.015     |
| **`anthropic.claude-3-opus-20240229-v1:0`** | Highest reasoning, 200 k ctx | \$0.015 / \$0.075     |
| `meta.llama3-70b-instruct-v1:0`             | OSS, good coding tasks       | \$0.0007 / \$0.0035   |

*(IDs that require an inference profile—e.g. Claude 3 .7—use the profile ARN instead.)*

---

## Roadmap beyond Phase Zero

* Auto‑generate Word & OSCAL via Jinja/Pandoc.
* S3 bucket + DynamoDB index for /records.
* Streamlit or Flask front‑end for client self‑service.
* Prompt library versioning & eval harness.

---

> **License**
> Private proprietary code © 2025 Orion LLC. No distribution without permission.

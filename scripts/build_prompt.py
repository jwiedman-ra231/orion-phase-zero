import json, pathlib
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=False,           # plain text, not HTML
    keep_trailing_newline=True,
)

TPL = env.get_template("prompt_template.txt")

def build_prompt(control_text: str,
                 context_blurb: str,
                 evidence: list[str],
                 odv: dict,
                 sys_desc: str) -> str:
    return TPL.render(
        control_statement = control_text.strip(),
        context_blurb     = context_blurb.strip(),
        evidence_list     = evidence,
        odv_json          = json.dumps(odv, indent=2),
        system_description= sys_desc.strip(),
    )

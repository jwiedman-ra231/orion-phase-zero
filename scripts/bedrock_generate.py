import boto3, json, os
from dotenv import load_dotenv
load_dotenv()

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL  = os.getenv("BR_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def generate(control_text: str, odv: dict, sys_desc: str) -> str:
    user_msg = (
        "You are drafting a System Security Plan control implementation for a client.\n\n"
        f"Control text:\n\"\"\"{control_text}\"\"\"\n\n"
        f"Organizationally-defined values: {json.dumps(odv)}\n"
        f"System description: {sys_desc}\n\n"
        "Write <250 words, first-person singular (“We…”), concrete implementation details only."
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_msg}],
            }
        ],
        # optional tunables:
        # "temperature": 0.7,
        # "top_p": 0.95,
    }

    resp = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=MODEL,
        accept="application/json",
        contentType="application/json",
    )

    # Claude 3 returns: {"content":[{"type":"text","text":"…"}], ...}
    return json.loads(resp["body"].read())["content"][0]["text"]

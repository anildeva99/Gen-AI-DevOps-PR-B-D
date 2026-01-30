import os
import json
import requests
from mistralai import Mistral

# ---------------------------
#  CONFIG
# ---------------------------
GITHUB_PAT = os.environ.get("GITHUB_PAT")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

REPO = "adinarayanap/Gen-AI-DevOps"
WORKFLOW_FILE = "ai-orchestrator.yml"       # You can change if you want
MODEL_NAME = "mistral-large-latest"         # FREE TIER SAFE

if not GITHUB_PAT:
    raise Exception("❌ ERROR: GITHUB_PAT environment variable not set")

if not MISTRAL_API_KEY:
    raise Exception("❌ ERROR: MISTRAL_API_KEY environment variable not set")


# ---------------------------
#  SELECT STAGE USING MISTRAL
# ---------------------------
def decide_stage(user_prompt: str) -> str:
    """
    Uses Mistral to classify which CI/CD stage should run based on prompt.
    """

    system_prompt = """
    You are an AI pipeline orchestrator.
    Based on the user prompt, choose ONE CI/CD stage from this list:
    
    - PR_REVIEW
    - BUILD
    - TEST
    - DEPLOY
    - SECURITY_SCAN

    Respond with ONLY the stage name, no explanation.
    """

    client = Mistral(api_key=MISTRAL_API_KEY)

    try:
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        stage = response.choices[0].message.content.strip()
        return stage

    except Exception as e:
        print("❌ Mistral API Error:", str(e))
        return "ERROR"


# ---------------------------
#  TRIGGER GITHUB PIPELINE
# ---------------------------
def trigger_github(stage: str, prompt: str):
    """
    Calls your GitHub Actions workflow with selected stage.
    """

    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_PAT}"
    }

    data = {
        "ref": "main",
        "inputs": {
            "stage": stage,
            "prompt": prompt
        }
    }

    print(f"🚀 Triggering GitHub Workflow: {WORKFLOW_FILE}")
    print(f"   Stage: {stage}")

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print("🔍 GitHub API Response:", response.status_code, response.text)


# ---------------------------
#  MAIN LOGIC
# ---------------------------
if __name__ == "__main__":
    user_prompt = input("Enter pipeline instruction: ")

    stage = decide_stage(user_prompt)

    print("🧠 Mistral Selected Stage:", stage)

    if stage == "ERROR":
        print("❌ Could not determine stage. Check API key or model.")
    else:
        trigger_github(stage, user_prompt)


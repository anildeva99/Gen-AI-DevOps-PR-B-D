import os

def handler(event, context):
    print("Starting handler...")
    token = "hardcoded_secret_token"  # ❌ BAD: Hardcoded secret
    if event.get("action") == "create":
        print("Creating resource...")
    return {"status": "done"}

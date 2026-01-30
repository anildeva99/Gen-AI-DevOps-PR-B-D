#!/usr/bin/env python3
import os
import json
import requests
from google.auth import default
from google.auth.transport.requests import Request

# === CONFIG ===
PROJECT_ID = "testadi-459816"
LOCATION = "us-central1"
MODEL_ID = "gemini-2.5-flash"  #  from available models
ENDPOINT = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:generateContent"

# === Get Access Token ===
creds, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds.refresh(Request())
access_token = creds.token

def analyze_logs(log_text: str):
    """Send logs to Gemini for RCA summary"""
    prompt = f"""
You are an AI-powered AIOps assistant.
Analyze these logs and summarize the key issues.

Incident Summary:
Root Cause:
Impacted Component:
Evidence:
Recommended Fixes:

Logs:
{log_text}
"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"[ERROR {response.status_code}] {response.text}"

# === MAIN ===
if __name__ == "__main__":
    logs = """
    2025-10-31 18:25:22 ERROR Service X – CPU utilization 98%
    2025-10-31 18:25:30 WARNING Auto-restart triggered
    2025-10-31 18:25:45 INFO Service X recovered successfully
    """
    print("🔍 AI Root-Cause Analysis Result:\n")
    print(analyze_logs(logs))

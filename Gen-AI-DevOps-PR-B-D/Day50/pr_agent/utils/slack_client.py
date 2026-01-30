import os
import requests

def send_slack_message(message: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️ SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Slack notification sent")
    except Exception as e:
        print(f"❌ Slack notification failed: {e}")

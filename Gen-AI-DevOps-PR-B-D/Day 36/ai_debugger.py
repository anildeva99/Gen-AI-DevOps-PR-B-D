import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GITHUB_REPO = "adinarayanap/Gen-AI-DevOps"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_latest_failed_run_id():
    """Fetch the latest FAILED GitHub Actions run automatically"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs?status=failure"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers).json()

    if "workflow_runs" in response and len(response["workflow_runs"]) > 0:
        latest_run = response["workflow_runs"][0]
        return latest_run["id"]

    return None


def fetch_run_logs(run_id):
    """Fetch logs for a specific GitHub Actions run"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs/{run_id}/logs"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return None

    return r.content.decode("latin-1")


@app.route("/debug", methods=["POST"])
def debug_ci():
    data = request.get_json()

    run_id = data.get("run_id")

    # If user didn't pass run_id → fetch automatically
    if not run_id:
        run_id = get_latest_failed_run_id()
        if not run_id:
            return jsonify({"error": "No failed GitHub Actions runs found."})

    logs = fetch_run_logs(run_id)

    if logs is None:
        return jsonify({"error": "Unable to fetch logs from GitHub."})

    # Very basic error pattern detection
    if "ERROR" in logs or "Error" in logs or "failed" in logs.lower():
        return jsonify({
            "run_id": run_id,
            "status": "Error detected",
            "summary": "The pipeline failed. Check error details.",
            "log_snippet": logs[:500]
        })

    return jsonify({
        "run_id": run_id,
        "status": "No known errors detected in the logs."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


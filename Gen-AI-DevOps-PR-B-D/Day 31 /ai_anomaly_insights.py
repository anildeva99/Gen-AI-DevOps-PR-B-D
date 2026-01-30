from flask import Flask, request, jsonify
import requests, sqlite3, datetime, uuid, os

app = Flask(__name__)

DB_PATH = os.path.expanduser("~/aiops-incident/incidents.db")
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def _ensure_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE,
        alertname TEXT,
        description TEXT,
        assigned_team TEXT,
        status TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()

@app.route("/alert", methods=["POST"])
def handle_alert():
    data = request.get_json()
    alerts = data.get("alerts", [])
    tickets = []

    for alert in alerts:
        name = alert["labels"].get("alertname")
        desc = alert["annotations"].get("description")
        team = "Server Team" if "CPU" in name else "DBA Team"

        ticket_id = f"INC-{datetime.datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4]}"
        created_at = datetime.datetime.utcnow().isoformat()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO incidents(ticket_id, alertname, description, assigned_team, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (ticket_id, name, desc, team, "Open", created_at))
        conn.commit()
        conn.close()

        msg = {
            "text": f"🚨 *AIOps Alert Triggered!*\n*Ticket ID:* {ticket_id}\n*Team:* {team}\n*Alert:* {name}\n*Status:* Open\n*Description:* {desc}\n*Created:* {created_at}"
        }
        requests.post(SLACK_WEBHOOK_URL, json=msg)
        tickets.append(ticket_id)

    return jsonify({"status": "ok", "tickets": tickets})

if __name__ == "__main__":
    _ensure_schema()
    app.run(host="0.0.0.0", port=5000)

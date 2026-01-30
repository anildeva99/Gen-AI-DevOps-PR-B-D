import os, re, time, random, requests, pandas as pd
from datetime import datetime, timezone
from flask import Flask, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sklearn.ensemble import IsolationForest
from threading import Thread

# Flask Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
db = SQLAlchemy(app)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300))
    severity = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Open")
    timestamp = db.Column(db.String(50))

# Slack Webhook
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def notify_slack(message, color="red"):
    emoji = "🚨" if color == "red" else "✅"
    payload = {"text": f"{emoji} {message}"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print("Slack Error:", e)

# HTML Dashboard
HTML = """
<!DOCTYPE html><html><head><title>AIOps Incident Ticketing System</title>
<style>
body{font-family:sans-serif;background:#f8fafc;margin:40px;}
h1{color:#222;} table{border-collapse:collapse;width:100%;}
th,td{padding:12px;border:1px solid #ccc;text-align:left;}
th{background:#f4f4f4;} button{background:#007bff;color:#fff;
padding:6px 12px;border:none;border-radius:4px;}
button:hover{background:#0056b3;}
</style></head><body>
<h1>🪶 AIOps Incident Ticketing System</h1>
<table><tr><th>ID</th><th>Severity</th><th>Message</th><th>Status</th><th>Time</th><th>Action</th></tr>
{% for inc in incidents %}
<tr><td>{{inc.id}}</td><td>{{inc.severity}}</td><td>{{inc.message}}</td>
<td>{{inc.status}}</td><td>{{inc.timestamp}}</td>
<td><a href="{{url_for('resolve_ticket',id=inc.id)}}"><button>Resolve</button></a></td></tr>
{% endfor %}</table></body></html>
"""

@app.route("/")
def index():
    incidents = Incident.query.order_by(Incident.id.desc()).all()
    return render_template_string(HTML, incidents=incidents)

@app.route("/resolve/<int:id>")
def resolve_ticket(id):
    inc = Incident.query.get(id)
    if inc:
        inc.status = "Resolved"
        db.session.commit()
        notify_slack(f"✅ Incident Resolved\n> {inc.message}\nStatus: Resolved\nTime: {datetime.now(timezone.utc)}", "green")
    return redirect(url_for("index"))

# Anomaly Detection
def anomaly_detector():
    if not os.path.exists("incidents.db"):
        with app.app_context():
            db.create_all()
    while True:
        lines = []
        for _ in range(10):
            latency = random.randint(100, 1600)
            line = f"{datetime.now(timezone.utc)} ERROR payment timeout latency={latency}ms"
            lines.append(line)
            with open("/tmp/app.log", "a") as f:
                f.write(line + "\n")
        lats = [int(re.findall(r"latency=(\d+)", l)[0]) for l in lines]
        if max(lats) > 400:
            msg = f"High latency spike: {max(lats)} ms | errors={len(lats)}"
            with app.app_context():
                inc = Incident(message=msg, severity="Critical", timestamp=str(datetime.now(timezone.utc)))
                db.session.add(inc)
                db.session.commit()
            notify_slack(f" New AIOps Incident Detected!\n> {msg}\nStatus: Open\nTime: {datetime.now(timezone.utc)}")
        time.sleep(10)

if __name__ == "__main__":
    Thread(target=anomaly_detector, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)

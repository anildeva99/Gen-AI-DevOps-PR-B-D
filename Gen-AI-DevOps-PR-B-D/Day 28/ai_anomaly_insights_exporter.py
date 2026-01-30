from prometheus_client import Gauge, start_http_server
import random, time

ai_summary = Gauge('ai_insights_summary', 'AI-generated anomaly summary (0=Normal, 0.5=Moderate, 1=Critical)')

def ai_generate_summary():
    while True:
        summary_level = random.choice([0, 0.5, 1])
        ai_summary.set(summary_level)
        if summary_level == 0:
            print(" AI Summary: System Normal")
        elif summary_level == 0.5:
            print(" AI Summary: Moderate anomalies detected. Review logs.")
        else:
            print(" AI Summary: Critical anomaly detected! Investigate immediately.")
        time.sleep(15)

if __name__ == "__main__":
    PORT = 9105
    print(f"🚀 Starting AI Insights exporter with summary on port {PORT}")
    start_http_server(PORT)
    ai_generate_summary()

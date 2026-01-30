from prometheus_client import Gauge, start_http_server
import random, time

cpu_usage = Gauge('ai_insights_cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('ai_insights_memory_usage_percent', 'Memory usage percentage')
anomalies_detected = Gauge('ai_insights_anomalies_total', 'Number of anomalies detected')

def collect_metrics():
    while True:
        cpu_usage.set(random.uniform(10, 90))
        memory_usage.set(random.uniform(20, 80))
        anomalies_detected.set(random.randint(0, 5))
        time.sleep(5)

if __name__ == "__main__":
    PORT = 9105
    print(f" Starting AI Insights metrics exporter on port {PORT}")
    start_http_server(PORT)
    collect_metrics()

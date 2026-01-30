import requests
import pandas as pd
from openai import OpenAI
import os

PROMETHEUS_URL = "http://localhost:9090/api/v1/query?query=node_cpu_seconds_total"

print("Fetching metrics from Prometheus...")
response = requests.get(PROMETHEUS_URL).json()
data = response["data"]["result"]

print(f"Retrieved {len(data)} metrics from Prometheus.")
print("Running anomaly detection on metrics...")

# Convert metric values
metrics = [float(item["value"][1]) for item in data]
mean = pd.Series(metrics).mean()
std = pd.Series(metrics).std()

# Simple anomaly detection (3-sigma rule)
anomalies = [m for m in metrics if abs(m - mean) > 3 * std]
print(f"{len(anomalies)} anomalies detected.")

# Explain anomaly using OpenAI
if anomalies:
    anomaly_value = anomalies[0]
    print(f"\nMetric Value: {anomaly_value}")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    You are an AI observability assistant. Analyze this Prometheus metric value ({anomaly_value})
    that deviates from normal mean ({mean:.2f}). Explain the possible cloud reason for anomaly.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in cloud monitoring and observability."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    insight = completion.choices[0].message.content
    print("OpenAI Insight:\n", insight)
else:
    print("No anomalies detected.")

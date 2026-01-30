#!/usr/bin/env python3
"""
AI-Powered Anomaly Detection using Prometheus + Gemini 2.5 Flash
"""
import pandas as pd
from sklearn.ensemble import IsolationForest
import vertexai
from vertexai.generative_models import GenerativeModel
import requests, sys

PROJECT_ID = "testadi-459816"
LOCATION = "us-central1"
PROMETHEUS_URL = "http://localhost:9090"
QUERY = "node_cpu_seconds_total"

def fetch_metrics():
    resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query={QUERY}", timeout=10)
    data = resp.json()["data"]["result"]
    df = pd.DataFrame(data)
    df["value"] = df["value"].apply(lambda x: float(x[1]))
    return df

def detect_anomalies(df):
    model = IsolationForest(contamination=0.02, random_state=42)
    df["anomaly"] = model.fit_predict(df[["value"]])
    return df[df["anomaly"] == -1]

def explain_with_gemini(anomalies):
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-2.5-flash")
    for _, row in anomalies.iterrows():
        val = row["value"]
        prompt = (
            f"Analyze this Prometheus metric anomaly:\n"
            f"Metric: {QUERY}\nValue: {val}\n"
            f"Explain possible causes in cloud infrastructure context."
        )
        result = model.generate_content(prompt)
        print(result.text.strip())

def main():
    print("Fetching metrics from Prometheus...")
    df = fetch_metrics()
    anomalies = detect_anomalies(df)
    explain_with_gemini(anomalies)

if __name__ == "__main__":
    main()

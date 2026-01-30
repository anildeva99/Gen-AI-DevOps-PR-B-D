#!/usr/bin/env python3
import openai
import argparse
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
# Set your API key as ENV variable: export OPENAI_API_KEY="your_api_key"
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# AI Log Analysis Function
# -----------------------------
def analyze_logs_with_ai(log_text, refine_level="normal"):
    """
    Send logs to LLM for analysis and anomaly detection.
    """
    prompt = f"""
You are a log analysis expert. Analyze the following logs and identify:
- Critical errors and their possible causes
- Warning patterns or repeated anomalies
- Any unusual activities or security concerns
- Recommended next steps to fix them

Refine the analysis to {refine_level} detail.

Logs:
{log_text[:6000]}  # limited to 6000 chars to avoid token overflow
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # works with GPT-4o / gpt-4o-mini
        messages=[{"role": "system", "content": "You are an expert DevOps log analyst."},
                  {"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message["content"]

# -----------------------------
# CLI Execution
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="AI-Powered Log Analyzer")
    parser.add_argument("--file", required=True, help="Path to the log file")
    parser.add_argument("--refine", default="normal", choices=["normal", "detailed", "deep"], help="Refinement level")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print(" ERROR: OPENAI_API_KEY not set. Use: export OPENAI_API_KEY='your_key_here'")
        exit(1)

    with open(args.file, "r") as f:
        logs = f.read()

    print(" Analyzing logs with AI...")
    analysis = analyze_logs_with_ai(logs, refine_level=args.refine)
    print("\n Analysis Report:\n")
    print(analysis)

if __name__ == "__main__":
    main()

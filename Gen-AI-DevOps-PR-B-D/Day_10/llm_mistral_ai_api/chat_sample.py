#!/usr/bin/env python3
import os
import requests
from datetime import datetime

# Load API key from environment
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    print(" Please export your MISTRAL_API_KEY first.")
    exit(1)

API_URL = "https://api.mistral.ai/v1/chat/completions"
OUTPUT_DIR = "outputs"

def ask_mistral(prompt, model="codestral-latest"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" API Request Failed:", e)
        return None

    data = response.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")

def save_output(prompt, output):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"output_{timestamp}.txt")
    with open(filename, "w") as f:
        f.write("Prompt:\n" + prompt + "\n\n")
        f.write("Mistral Output:\n" + output + "\n")
    print(f"Saved output to: {filename}")

def main():
    print(" Mistral Interactive DevOps Chat (type 'exit' to quit)")
    while True:
        try:
            prompt = input(" Enter your DevOps prompt: ").strip()
            if prompt.lower() in ["exit", "quit"]:
                print(" Exiting.")
                break

            output = ask_mistral(prompt)
            if output:
                print("\n📝 Mistral Output:\n")
                print(output)
                print("\n" + "="*60 + "\n")
                save_output(prompt, output)
            else:
                print("No output received from Mistral.")

        except KeyboardInterrupt:
            print("\n Exiting.")
            break

if __name__ == "__main__":
    main()

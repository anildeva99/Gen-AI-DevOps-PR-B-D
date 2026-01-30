#!/usr/bin/env python3
import os, requests

API_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.mistral.ai/v1/chat/completions"
history = []

print("🤖 Raw Mistral API Chat (no LangChain). Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Goodbye ")
        break

    history.append({"role": "user", "content": user_input})

    payload = {"model": "mistral-small-latest", "messages": history}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, headers=headers, json=payload).json()
        reply = response["choices"][0]["message"]["content"]
        print(f"Mistral: {reply}\n")
        history.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f" Error: {e}")

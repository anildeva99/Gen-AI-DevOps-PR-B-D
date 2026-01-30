#!/usr/bin/env python3
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from mistralai import Mistral   # ✅ use new client

# ---------------------------
# Load API Key
# ---------------------------
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please export your MISTRAL_API_KEY first:\n\n"
                     "   export MISTRAL_API_KEY=your_api_key_here\n")

# Init client (new API)
client = Mistral(api_key=API_KEY)

# ---------------------------
# Call Mistral API
# ---------------------------
def mistral_call(task: str) -> str:
    response = client.chat.complete(
        model="mistral-small-latest",   # or mistral-medium-latest, mistral-large-latest
        messages=[{"role": "user", "content": task}]
    )
    return response.choices[0].message.content

# ---------------------------
# Build LangChain pipeline
# ---------------------------
prompt = ChatPromptTemplate.from_template(
    "Answer in detail as a DevOps trainer.\nQuestion: {task}"
)

# Convert ChatPromptValue → string before sending
chain = prompt | RunnableLambda(lambda x: mistral_call(x.to_string()))

# ---------------------------
# Interactive CLI
# ---------------------------
def main():
    print("🤖 LangChain + Mistral (new client) Interactive Demo (type 'exit' to quit)")
    while True:
        try:
            task = input("\nYou: ")
            if task.lower() in ["exit", "quit"]:
                break
            answer = chain.invoke({"task": task})
            print(f"\nMistral: {answer}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

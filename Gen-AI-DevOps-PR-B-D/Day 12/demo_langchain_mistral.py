#!/usr/bin/env python3
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from mistralai.client import MistralClient

# ---------------------------
# Load API Key
# ---------------------------
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please export your MISTRAL_API_KEY first:\n\n"
                     "   export MISTRAL_API_KEY=your_api_key_here\n")

# Init client
client = MistralClient(api_key=API_KEY)

# ---------------------------
# Call Mistral API
# ---------------------------
def mistral_call(task: str) -> str:
    response = client.chat(
        model="mistral-small-latest",   # you can switch to mistral-medium-latest
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
    print("🤖 LangChain + Mistral (old client) Interactive Demo (type 'exit' to quit)")
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

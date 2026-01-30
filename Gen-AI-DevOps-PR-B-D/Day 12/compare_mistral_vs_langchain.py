#!/usr/bin/env python3
import os
from mistralai.client import MistralClient
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load API key
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError(" Please set your MISTRAL_API_KEY")

# Init Mistral client
client = MistralClient(api_key=api_key)

# -------------------
# Case 1: Only Mistral
# -------------------
def only_mistral(question: str) -> str:
    response = client.chat(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content

# -------------------
# Case 2: Mistral + LangChain
# -------------------
def mistral_call(prompt) -> str:
    # Convert LangChain PromptValue → string
    if not isinstance(prompt, str):
        prompt = str(prompt)

    response = client.chat(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": "You are a DevOps trainer. Answer in structured detail."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

llm = RunnableLambda(mistral_call)

prompt_template = PromptTemplate(
    template="""Question: {task}
Answer with clear explanation and examples.
""",
    input_variables=["task"],
)
chain = prompt_template | llm

# -------------------
# Interactive Loop
# -------------------
print("🤖 Interactive mode: type your prompt (Ctrl+C to exit)\n")

try:
    while True:
        user_input = input("You: ")

        print("\n\033[94m🔹 Only Mistral Output:\033[0m\n")
        print(f"\033[92m{only_mistral(user_input)}\033[0m")

        print("\n\033[94m🔹 Mistral + LangChain Output:\033[0m\n")
        print(f"\033[93m{chain.invoke({'task': user_input})}\033[0m\n")

except KeyboardInterrupt:
    print("\n👋 Exiting...")

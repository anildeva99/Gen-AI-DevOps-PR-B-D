#!/usr/bin/env python3
import os
import shutil
import textwrap
from mistralai import Mistral
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ===========================
# Terminal Colors
# ===========================
RESET  = "\033[0m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"

# ===========================
# Load API Key
# ===========================
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please export your MISTRAL_API_KEY first")

# Init client
client = Mistral(api_key=API_KEY)

# ===========================
# Raw Mistral Call
# ===========================
def mistral_raw_call(prompt: str) -> str:
    try:
        response = client.chat.complete(
            model="mistral-small-latest",  # or mistral-medium-latest, mistral-large-latest
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Raw API Error: {e}"

# ===========================
# LangChain + Mistral Call
# ===========================
prompt_template = ChatPromptTemplate.from_template("{task}")

def lc_to_mistral(chat_prompt_value):
    """Convert ChatPromptValue → string and pass to Mistral API"""
    text = chat_prompt_value.to_string()
    return mistral_raw_call(text)

# Chain: prompt → mistral call
chain = prompt_template | RunnableLambda(lc_to_mistral)

def mistral_langchain_call(prompt: str) -> str:
    try:
        return chain.invoke({"task": prompt})
    except Exception as e:
        return f"⚠️ LangChain Error: {e}"

# ===========================
# Utility: Print Side by Side
# ===========================
def print_side_by_side(raw_output, lc_output):
    """Print two outputs side by side in columns"""
    terminal_width = shutil.get_terminal_size((160, 20)).columns
    col_width = terminal_width // 2 - 4

    raw_output = raw_output.replace("\n", "\n\n")
    lc_output = lc_output.replace("\n", "\n\n")

    raw_lines = textwrap.wrap(raw_output, col_width)
    lc_lines = textwrap.wrap(lc_output, col_width)

    max_lines = max(len(raw_lines), len(lc_lines))
    raw_lines += [""] * (max_lines - len(raw_lines))
    lc_lines += [""] * (max_lines - len(lc_lines))

    print(f"{YELLOW}{'Raw Mistral API'.ljust(col_width)}{RESET} || "
          f"{GREEN}{'LangChain + Mistral'.ljust(col_width)}{RESET}")
    print("─" * terminal_width)

    for r, l in zip(raw_lines, lc_lines):
        print(f"{YELLOW}{r.ljust(col_width)}{RESET} || {GREEN}{l.ljust(col_width)}{RESET}")

    print("\n" + "═" * terminal_width + "\n")

# ===========================
# Interactive Loop
# ===========================
print(f"{CYAN}🤖 Compare Raw Mistral vs LangChain+Mistral "
      f"(type 'exit' to quit){RESET}\n")

while True:
    try:
        user_input = input(f"{CYAN}You: {RESET}")
        if user_input.lower() in ["exit", "quit", "q"]:
            print(f"{CYAN}Goodbye! 👋{RESET}")
            break

        raw_output = mistral_raw_call(user_input)
        lc_output = mistral_langchain_call(user_input)

        print_side_by_side(raw_output, lc_output)

    except KeyboardInterrupt:
        print(f"\n{RED}⛔ Interrupted by user. Exiting...{RESET}")
        break
    except Exception as e:
        print(f"{RED}⚠️ Error: {e}{RESET}")

#!/usr/bin/env python3
import os, glob, shutil, textwrap
from mistralai import Mistral
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# 🎨 Terminal colors
RESET  = "\033[0m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"

# 🔑 Load Mistral API Key
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please export your MISTRAL_API_KEY first.\n   export MISTRAL_API_KEY=your_api_key_here")

client = Mistral(api_key=API_KEY)

# ------------------ 1️⃣ LLM-Only Mode ------------------
def llm_only(description: str) -> str:
    prompt = f"Generate a Kubernetes deployment YAML for this app:\n{description}"
    resp = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

# ------------------ 2️⃣ Build RAG Knowledge Base ------------------
def build_index():
    docs = []
    for f in glob.glob("docs/*.txt"):
        with open(f, "r", encoding="utf-8") as fh:
            docs.append(Document(page_content=fh.read(), metadata={"source": f}))
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, embeddings)

# ------------------ 3️⃣ LLM + RAG Mode ------------------
def with_rag(description: str) -> str:
    vectorstore = build_index()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.get_relevant_documents(description)
    context = "\n\n".join([d.page_content for d in retrieved_docs])
    prompt = f"Context:\n{context}\n\nNow, using these best practices, generate a Kubernetes deployment YAML for:\n{description}"
    resp = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

# ------------------ 🧪 Run Interactive Demo ------------------
if __name__ == "__main__":
    print(GREEN + "\n🚀 LLM vs RAG Demo - Kubernetes Manifest Generator\n" + RESET)
    while True:
        desc = input(CYAN + "💡 Describe your app (or 'exit'): " + RESET)
        if desc.strip().lower() in {"exit", "quit", "q"}:
            break

        print("\n🔎 LLM Only Output (No RAG):")
        print("-" * 120)
        print(textwrap.fill(llm_only(desc), width=120))

        print("\n📚 With RAG Output (Mistral + LangChain + FAISS):")
        print("-" * 120)
        print(textwrap.fill(with_rag(desc), width=120))

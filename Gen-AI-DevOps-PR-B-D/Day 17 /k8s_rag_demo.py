#!/usr/bin/env python3
import os
from mistralai import Mistral
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("❌ Please export your MISTRAL_API_KEY first")

client = Mistral(api_key=API_KEY)

def build_index():
    docs = []
    for f in os.listdir("docs"):
        if f.endswith(".txt"):
            with open(f"docs/{f}", "r", encoding="utf-8") as fh:
                docs.append(Document(page_content=fh.read(), metadata={"source": f}))
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, embeddings)

def compare_llm_vs_rag(prompt):
    print("\n🔎 LLM-Only Output:")
    llm_resp = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": f"Generate a Kubernetes YAML: {prompt}"}]
    )
    print(llm_resp.choices[0].message.content)

    print("\n📚 RAG-Enhanced Output:")
    vectorstore = build_index()
    retrieved_docs = vectorstore.similarity_search(prompt, k=3)
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    rag_prompt = f"Use this context:\n{context}\n\nGenerate a Kubernetes manifest: {prompt}"
    rag_resp = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": rag_prompt}]
    )
    print(rag_resp.choices[0].message.content)

if __name__ == "__main__":
    user_prompt = input("💡 Enter a Kubernetes deployment scenario: ")
    compare_llm_vs_rag(user_prompt)

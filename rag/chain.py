"""
RAG pipeline: retrieve relevant knowledge-base entries (rag/retriever.py),
then generate a contextual answer with Groq via LangChain.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from rag.retriever import search

SYSTEM_PROMPT = """\
Kamu adalah customer service assistant yang ramah dan membantu.
Jawab pertanyaan pengguna HANYA berdasarkan konteks yang diberikan di bawah.
Jika konteks tidak mengandung jawaban yang relevan, katakan dengan jujur \
bahwa kamu tidak punya informasi itu dan sarankan menghubungi customer \
service manusia, JANGAN mengarang jawaban.
Jawab singkat, jelas, dan dalam Bahasa Indonesia.

Konteks yang relevan:
{context}
"""

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, max_retries=2)
    return _llm


def answer(user_query: str, top_k=3):
    results, elapsed_ms = search(user_query, top_k=top_k)

    if not results:
        context = "(Tidak ada informasi relevan ditemukan di knowledge base.)"
    else:
        context = "\n\n".join(
            f"Q: {r['prompt']}\nA: {r['response']}" for r in results
        )

    messages = [
        ("system", SYSTEM_PROMPT.format(context=context)),
        ("human", user_query),
    ]

    llm = _get_llm()
    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "retrieved": results,
        "retrieval_ms": elapsed_ms,
    }

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

try:
    for key in ("DATABASE_URL", "GROQ_API_KEY"):
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass

from rag.chain import answer

st.set_page_config(page_title="Intelligent Customer Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Intelligent Customer Assistant")
st.caption(
    "Chatbot customer service berbasis RAG (Retrieval-Augmented Generation) "
    "— jawaban dihasilkan dari knowledge base yang tersimpan di PostgreSQL + pgvector."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Ada yang bisa saya bantu terkait akun, pesanan, pembayaran, atau hal lainnya?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not os.environ.get("GROQ_API_KEY"):
    st.warning("GROQ_API_KEY belum diset — chatbot belum bisa merespons sampai key-nya diisi.")

user_input = st.chat_input("Tulis pertanyaan kamu di sini...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        result = None
        with st.spinner("Mencari informasi relevan & menyusun jawaban..."):
            try:
                result = answer(user_input)
                response_text = result["answer"]
            except Exception as e:
                response_text = f"Maaf, terjadi kesalahan: {e}"
        st.markdown(response_text)

        with st.expander("Lihat sumber knowledge base yang dipakai"):
            if result and result.get("retrieved"):
                for r in result["retrieved"]:
                    st.markdown(f"**[{r['category']}]** (similarity: {r['similarity']}) {r['prompt']}")
                    st.caption(r["response"])
            else:
                st.caption("Tidak ada entri knowledge base yang cukup relevan ditemukan.")

    st.session_state.messages.append({"role": "assistant", "content": response_text})
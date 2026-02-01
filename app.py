import streamlit as st
import agent as Agent
import utils as Utils
import embed
import os as OS

def create_chat(chat_id: str):
    chat = st.container()

    # ---------- INIT STATE ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "newschat" not in st.session_state:
        st.session_state.newschat = Agent.NewsChat(chat_id)

    # ---------- DISPLAY HISTORY ----------
    for msg in st.session_state.messages:
        if msg["id"] == chat_id:
            with chat.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ---------- INPUT ----------
    prompt = st.chat_input(
        placeholder="Ask me about AI legal stuff in the EU",
        key=chat_id
    )

    if prompt:
        # show user message
        with chat.chat_message("user"):
            st.markdown(prompt)

        # get assistant response
        with chat.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = st.session_state.newschat.ask(prompt)
                st.markdown(answer)

        # save to history
        st.session_state.messages.append({
            "id": chat_id,
            "role": "user",
            "content": prompt
        })
        st.session_state.messages.append({
            "id": chat_id,
            "role": "assistant",
            "content": answer
        })

# ---------- MAIN ----------
if __name__ == "__main__":
    st.set_page_config(page_title="EU AI Legal Assistant")

    if not OS.path.exists(Utils.DB_FOLDER):
        document_name = "Artificial Intelligence Act"
        document_description = "Artificial Intelligence Act"
        text = embed.pdf_to_text(Utils.EUROPEAN_ACT_URL)
        embed.embed_text_in_chromadb(text, document_name, document_description)

    create_chat("chat1")

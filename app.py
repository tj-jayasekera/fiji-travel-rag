import streamlit as st

from src.generation.generate_answer import generate_answer


st.set_page_config(
    page_title="Fiji Travel Intelligence",
    page_icon="🌴",
    layout="centered"
)

st.title("🌴 Fiji Travel Intelligence")

st.caption(
    "Ask questions about Fiji using a curated travel knowledge base."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input(
    "Ask a Fiji travel question..."
)

if user_question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Searching Fiji travel sources..."):
            result = generate_answer(user_question)

        answer = result["answer"]

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
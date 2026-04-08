import streamlit as st

from db.conversations import (
    create_new_conversation,
    add_message,
    get_all_conversations,
    get_conversation,)
from services.get_title import get_title
from services.get_models_list import get_ollama_models_list
from services.chat_utilities import get_answer

st.set_page_config(page_title="ChatGPT clone")
st.title("ChatGPT clone")

if("OLLAMA_MODELS" not in st.session_state):
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

selected_model = st.selectbox("Select Model", st.session_state.OLLAMA_MODELS)

st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])

with st.sidebar:
    st.header("Chat History")
    conversations = get_all_conversations()

    if st.button(" New Conversation"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []

    for cid, title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title
        if st.button(label, key=f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title", "Untitled")
            st.session_state.chat_history = [
                {"role": m["role"], "content": m["content"]} for m in doc.get("messages", [])
            ]
conversations = get_all_conversations()
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask AI")
if user_query:
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    if st.session_state.conversation_id is None:
        try:
            title = get_title(selected_model, user_query) or "New Chat"
        except Exception as e:
            title = "New Chat"
        conv_id = create_new_conversation(title,role="user",content=user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_message(st.session_state.conversation_id, "user", user_query)

    try:
        assistant_text = get_answer(selected_model, st.session_state.chat_history)
    except Exception as e:
        assistant_text = f"**{e}**"

    with st.chat_message("assistant"):
        st.markdown(assistant_text)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id, "assistant", assistant_text)

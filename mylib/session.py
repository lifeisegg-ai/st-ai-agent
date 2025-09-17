import streamlit as st
from agents import SQLiteSession


def set_session():
    if "session" not in st.session_state:
        st.session_state["session"] = SQLiteSession(
            "chat-history",
            "chat-gpt-clone-memory.db",
        )
    return st.session_state["session"]


# end

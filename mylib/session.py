import streamlit as st
from agents import SQLiteSession


def set_memory_session(name, db):
    if "session" not in st.session_state:
        st.session_state["session"] = SQLiteSession(name, db)
    return st.session_state["session"]


def set_session(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


def clear_session(key):
    del st.session_state[key]


# end

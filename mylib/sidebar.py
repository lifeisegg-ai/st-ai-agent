import asyncio

import streamlit as st


def display_sidebar(session):
    with st.sidebar:
        reset = st.button("Reset memory")
        if reset:
            asyncio.run(session.clear_session())
        st.write(asyncio.run(session.get_items()))


# end

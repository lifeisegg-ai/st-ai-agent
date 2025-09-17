import streamlit as st

from mylib.session import clear_session, set_session


def key_validate(val) -> bool:
    if val is not None or val != "":
        return True
    return False


# save_clone_chatGPT
def save_clone_chatGPT(key_openai_api: str, key_vector_store_id: str):
    if key_validate(key_openai_api) and key_validate(key_vector_store_id):
        # Session 보존
        # 별도로 Session에 넣으면 저장된 것이 페이지 전환시 상실하므로 Dict화해서 넣음
        clone_chatGPT_keys = {
            "key_openai_api": key_openai_api,
            "key_vector_store_id": key_vector_store_id,
        }
        set_session("clone_chatGPT", clone_chatGPT_keys)
        return True
    else:
        # 무효화
        clear_session("clone_chatGPT")
        return False


tab1, tab2 = st.tabs(["clone chatGPT", "test"])

with tab1:
    with st.form("preference_form"):
        st.header("clone chatGPT key Setting")
        key_openai_api = st.text_input(
            "Input the openai api key",
            "",
            key="key_openai_api",
        )
        key_vector_store_id = st.text_input(
            "Input the key vector store id",
            "",
            key="key_vector_store_id",
        )

        submit = st.form_submit_button("Save")

with tab2:
    st.header("test")


if submit:
    st.write(f"test {key_openai_api} {key_vector_store_id}")
    r = save_clone_chatGPT(key_openai_api, key_vector_store_id)
    if r:
        st.write(st.session_state)
        st.switch_page("main.py")
    else:
        # 에러메세지
        st.error(
            "Invalid OpenAI API or Vector Store ID. Please check the input."
        )

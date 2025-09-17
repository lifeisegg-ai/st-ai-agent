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
        # 별도로 Session에 넣으면 저장된 것이 페이지 전환시 상실하므로 DIct화해서 넣음
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
        st.subheader("clone chatGPT 를 이용하기 위한 개인용 키를 입력하세요!")
        st.markdown(
            "※여기서 사용된 키는 세션에만 등록됩니다.  \n※강제적인 페이지 리로드할 경우 등록된 키는 리셋됩니다."
        )
        key_openai_api = st.text_input(
            "openai api key 를 입력해 주세요",
            "",
            key="key_openai_api",
            type="password",
        )
        key_vector_store_id = st.text_input(
            "key vector store id 를 입력해 주세요",
            "",
            key="key_vector_store_id",
            type="password",
        )

        submit = st.form_submit_button("Session State 에 저장")

with tab2:
    st.header("test")


if submit:
    st.write(f"test {key_openai_api} {key_vector_store_id}")
    result = save_clone_chatGPT(key_openai_api, key_vector_store_id)
    if result:
        # st.write(st.session_state)
        st.switch_page("main.py")
    else:
        # 에러메세지
        st.error(
            "Invalid OpenAI API or Vector Store ID. Please check the input."
        )

# end

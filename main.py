import asyncio
import base64
import os

import dotenv

dotenv.load_dotenv()
import streamlit as st
from agents import Runner
from openai import OpenAI

from mylib.agent import set_agent
from mylib.fnc import update_status
from mylib.history import paint_history
from mylib.session import set_session
from mylib.sidebar import display_sidebar
from mylib.variable import FILE_TYPES, create_input_image

client = OpenAI()

VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")

# mylib/agent.py
agent = set_agent(VECTOR_STORE_ID)
# mylib/session.py
session = set_session()

# mylib/history.py
asyncio.run(paint_history(set_session()))

# mylib/fnc.py
# update_status(status_container, event):


async def run_agent(message):
    with st.chat_message("ai"):
        status_container = st.status("⏳", expanded=False)
        text_placeholder = st.empty()
        response = ""

        stream = Runner.run_streamed(
            agent,
            message,
            session=session,
        )

        async for event in stream.stream_events():
            if event.type == "raw_response_event":

                update_status(status_container, event.data.type)

                if event.data.type == "response.output_text.delta":
                    response += event.data.delta
                    text_placeholder.write(response.replace("$", "\$"))


prompt = st.chat_input(
    "Write a message for your assistant",
    accept_file=True,
    file_type=FILE_TYPES,
)

if prompt:

    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳ Uploading file...") as status:
                    uploaded_file = client.files.create(
                        file=(file.name, file.getvalue()),
                        purpose="user_data",
                    )
                    status.update(label="⏳ Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID,
                        file_id=uploaded_file.id,
                    )
                    status.update(label="✅ File uploaded", state="complete")
        elif file.type.startswith("image/"):
            with st.status("⏳ Uploading image...") as status:
                file_bytes = file.getvalue()
                base64_data = base64.b64encode(file_bytes).decode("utf-8")
                data_uri = f"data:{file.type};base64,{base64_data}"
                asyncio.run(
                    session.add_items(
                        create_input_image(data_uri),
                    )
                )
                status.update(label="✅ Image uploaded", state="complete")
            with st.chat_message("human"):
                st.image(data_uri)

    if prompt.text:
        with st.chat_message("human"):
            st.write(prompt.text)
        asyncio.run(run_agent(prompt.text))


# mylib/sidebar.py
display_sidebar(session)

print("Done!")

# end
# end

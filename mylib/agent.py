import streamlit as st
from agents import Agent, FileSearchTool, WebSearchTool


def set_agent(vector_store_id: str):
    if "agent" not in st.session_state:
        st.session_state["agent"] = Agent(
            name="ChatGPT Clone",
            instructions="""
            You are a helpful assistant.

            You have access to the followign tools:
                - Web Search Tool: Use this when the user asks a questions that isn't in your training data. Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first.
                - File Search Tool: Use this tool when the user asks a question about facts related to themselves. Or when they ask questions about specific files.
            """,
            tools=[
                WebSearchTool(),
                FileSearchTool(
                    vector_store_ids=[vector_store_id],
                    max_num_results=3,
                ),
            ],
        )
    return st.session_state["agent"]


# end

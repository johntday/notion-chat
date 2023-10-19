import os

import streamlit as st

from notion_chat.utils import llm_chain

from utils.layout import Layout
from utils.sidebar import Sidebar

topic = "Hybris"
app_name = f"{topic} ChatBot"


def load_api_key() -> str:
    """
    Loads the OpenAI API key from the .env file or from the user's input
    and returns it
    """
    if "OPENAI_API_KEY" in st.secrets:
        user_api_key = st.secrets["OPENAI_API_KEY"]
        st.sidebar.success("API key loaded", icon="🚀")
    else:
        user_api_key = st.sidebar.text_input(
            label="#### Your OpenAI API key 👇", placeholder="Paste your openAI API key, sk-", type="password"
        )
        if user_api_key:
            st.sidebar.success("API key loaded", icon="🚀")
            os.environ["OPENAI_API_KEY"] = user_api_key
    return user_api_key


def is_verbose() -> bool:
    if 'verbose' not in st.session_state:
        st.session_state['verbose'] = False
    return st.session_state["verbose"]


def main():
    st.set_page_config(layout="wide", page_icon="💬", page_title=app_name)
    sidebar = Sidebar()
    layout = Layout()
    layout.show_header()

    user_api_key = load_api_key()

    if not user_api_key:
        layout.show_api_key_missing()
    else:
        sidebar.show_options()
        sidebar.about(app_name)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "history" not in st.session_state:
            st.session_state.history = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me a question about Hybris"):
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                for response in llm_chain.qa(
                        query=prompt,
                        model_name=st.session_state["model"],
                        temperature=st.session_state["temperature"],
                        k=st.session_state["k_slider"],
                        search_type=st.session_state["search_type"],
                        history=st.session_state["history"],
                        verbose=is_verbose(),
                ):
                    full_response += response
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.history.append((prompt, full_response))
            sidebar.show_sources(st.session_state["chat_sources"])


if __name__ == "__main__":
    main()

import os

import streamlit as st
from notion_chat.utils.llm_chain import setup_chatbot

from utils.history import ChatHistory
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
        if "chatbot" not in st.session_state:
            print("Setting up chatbot...") if is_verbose() else None
            setup_chatbot(
                model_name=st.session_state["model"],
                temperature=st.session_state["temperature"],
                k=st.session_state["k_slider"],
                search_type=st.session_state["search_type"],
                verbose=is_verbose(),
            )
            st.session_state["ready"] = True

        history = ChatHistory()
        sidebar.show_options()

        try:
            if st.session_state["ready"]:
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    is_ready, user_input = layout.prompt_form()
                    history.initialize(topic)

                    if st.session_state["reset_chat"]:
                        history.reset(topic)

                    if is_ready:
                        if st.session_state["chatbot_reset"]:
                            print("Resetting chatbot...") if is_verbose() else None
                            setup_chatbot(
                                model_name=st.session_state["model"],
                                temperature=st.session_state["temperature"],
                                k=st.session_state["k_slider"],
                                search_type=st.session_state["search_type"],
                                verbose=is_verbose(),
                            )

                        print("chat_history before call: " + str(st.session_state["history"])) if is_verbose() else None

                        result = st.session_state["chatbot"](
                            {"question": user_input, "chat_history": st.session_state["history"]},
                        )

                        # print(*result['source_documents'], sep="\n\n")
                        st.session_state["history"].append((user_input, result["answer"]))
                        st.session_state["chat_sources"] = result['source_documents']

                        history.append("user", user_input)
                        history.append("assistant", result["answer"])

                        sidebar.show_sources(st.session_state["chat_sources"])

                history.generate_messages(response_container)

        except Exception as e:
            st.error(f"ERROR: {str(e)}")

    sidebar.about(app_name)


if __name__ == "__main__":
    main()

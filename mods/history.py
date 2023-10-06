import streamlit as st
from streamlit_chat import message


class ChatHistory:
    primed_history = [("What do you know", "I am an AI expert in SAP Commerce Cloud also known as Hybris")]

    def __init__(self):
        self.history = st.session_state.get("history", self.primed_history)
        st.session_state["history"] = self.history

    @staticmethod
    def default_greeting():
        return "Hello"

    @staticmethod
    def default_prompt(topic):
        return f"Hi, ask me a question about {topic}"

    def initialize_user_history(self):
        st.session_state["user"] = [self.default_greeting()]

    def initialize_assistant_history(self, topic):
        st.session_state["assistant"] = [self.default_prompt(topic)]

    def initialize(self, topic):
        if "assistant" not in st.session_state:
            self.initialize_assistant_history(topic)
        if "user" not in st.session_state:
            self.initialize_user_history()

    def reset(self, topic):
        st.session_state["history"] = self.primed_history
        self.initialize_user_history()
        self.initialize_assistant_history(topic)
        st.session_state["reset_chat"] = False

    @staticmethod
    def append(mode, msg):
        st.session_state[mode].append(msg)

    @staticmethod
    def generate_messages(container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    message(
                        st.session_state["user"][i],
                        is_user=True,
                        key=f"{i}_user",
                        avatar_style="big-smile",
                        seed="aneka",
                    )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="bottts", seed="felix")

    # def load(self):
    #     if os.path.exists(self.history_file):
    #         with open(self.history_file, "r") as f:
    #             self.history = f.read().splitlines()
    #
    # def save(self):
    #     with open(self.history_file, "w") as f:
    #         f.write("\n".join(self.history))

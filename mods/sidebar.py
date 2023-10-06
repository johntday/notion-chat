import streamlit as st


class Sidebar:
    MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
    SEARCH_TYPE_OPTIONS = ["similarity", "mmr"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.1
    TEMPERATURE_STEP = 0.1
    K_MIN_VALUE = 1
    K_MAX_VALUE = 10
    K_DEFAULT_VALUE = 4
    K_STEP = 1
    VERBOSE_DEFAULT_VALUE = False

    def __init__(self):
        st.session_state["k_slider"] = self.K_DEFAULT_VALUE
        st.session_state["temperature"] = self.TEMPERATURE_DEFAULT_VALUE
        st.session_state["model"] = self.MODEL_OPTIONS[0]
        st.session_state["search_type"] = self.SEARCH_TYPE_OPTIONS[0]
        st.session_state["verbose"] = self.VERBOSE_DEFAULT_VALUE

    @staticmethod
    def about(app_name: str):
        about = st.sidebar.expander("🤖 About")
        sections = [
            f"- {app_name} is an AI chatbot with Hybris knowledge.  It has been trained on the following sources of Hybris documentation: "
            "[SAP Hybris Help v2211](https://help.sap.com/docs/SAP_COMMERCE_CLOUD_PUBLIC_CLOUD?version=v2211), "
            "[Hybrismart Articles](https://hybrismart.com), "
            "[CX Works](https://www.sap.com/cxworks/expert-recommendations/articles/commerce-cloud.html), "
            "[Worldpay SAP Hybris Addon](https://github.com/Worldpay/hybris)",
            "- The app is created with the following Python packages: "
            "[Langchain](https://github.com/hwchase17/langchain), "
            "[OpenAI](https://platform.openai.com/docs/models/gpt-3-5), "
            "[Streamlit](https://github.com/streamlit/streamlit), and [qdrant Vector Database](https://github.com/qdrant/qdrant)",
        ]
        for section in sections:
            about.write(section)

    # fixme: create usage

    @staticmethod
    def on_change():
        st.session_state["chatbot_reset"] = True

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox(label="Model", options=self.MODEL_OPTIONS, on_change=self.on_change)
        st.session_state["model"] = model

    def search_type_selector(self):
        search_type = st.selectbox(label="Search Type", options=self.SEARCH_TYPE_OPTIONS)
        st.session_state["search_type"] = search_type

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
            on_change=self.on_change,
        )
        st.session_state["temperature"] = temperature

    def k_slider(self):
        k_slider = st.slider(
            label="K",
            min_value=self.K_MIN_VALUE,
            max_value=self.K_MAX_VALUE,
            value=self.K_DEFAULT_VALUE,
            step=self.K_STEP,
            on_change=self.on_change
        )
        st.session_state["k_slider"] = k_slider

    def verbose_toggle(self):
        verbose = st.toggle(
            "Verbose Logging",
            value=self.VERBOSE_DEFAULT_VALUE,
            on_change=self.on_change
        )
        st.session_state["verbose"] = verbose

    def show_options(self):
        with st.sidebar.expander("🛠️ Settings", expanded=False):
            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            self.k_slider()
            self.search_type_selector()
            self.verbose_toggle()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)
            st.session_state.setdefault("k_slider", self.K_DEFAULT_VALUE)
            st.session_state.setdefault("search_type", self.SEARCH_TYPE_OPTIONS[0])

    @staticmethod
    def show_sources(chat_sources):
        sources = st.sidebar.expander("🛠️ Top Sources for Answer", expanded=False)
        sources.empty()
        i = 0
        for chat_source in chat_sources:
            i += 1
            # page_content = chat_source.page_content
            metadata = chat_source.metadata

            sources.write(f"{i}. [{metadata['title']}]({metadata['source']}) was published {metadata['published']} by {metadata['source id']}")
            # sources.write(page_content)
            sources.write()

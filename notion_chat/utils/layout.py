import streamlit as st


class Layout:
    @staticmethod
    def show_header():
        """
        Displays the header of the app
        """
        st.markdown(
            """
            <h1 style='text-align: center;'>Hybris Chatbot 💬</h1>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def show_api_key_missing():
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div style='text-align: center;'>
                <h4>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a>. 
                Use the link to create a free API key.</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

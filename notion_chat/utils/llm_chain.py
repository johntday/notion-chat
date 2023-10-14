import os
import streamlit as st

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from notion_load.qdrant_util import get_vector_db
from notion_load.qdrant_util import get_qdrant_client


def setup_chatbot(model_name,
                  temperature,
                  k,
                  search_type,
                  verbose
                  ):
    """
    Sets up the chatbot with the uploaded file, model, and temperature
    """
    print("setup_chatbot") if verbose else None
    prompt_template = """SYSTEM: You are an AI expert with SAP Commerce Cloud, also known as Hybris.  Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. Do not make up an answer, say you do not know.
        ---
        Chat History:
        {chat_history}
        ---
        Follow Up Input: {question}
        ---
        Standalone question:"""
    qa_prompt = PromptTemplate.from_template(prompt_template)

    """Get Qdrant client"""
    q_client = get_qdrant_client(os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY"))

    """Qdrant Vector DB"""
    embeddings = OpenAIEmbeddings()
    collection_name = os.getenv("QDRANT_COLLECTION_NAME")
    vectors = get_vector_db(q_client, collection_name, embeddings)

    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name=model_name, temperature=temperature),
        retriever=vectors.as_retriever(search_type=search_type, search_kwargs={'k': k}),
        condense_question_prompt=qa_prompt,
        return_source_documents=True,
        verbose=verbose,
    )

    st.session_state["chatbot"] = qa
    st.session_state["chatbot_reset"] = False

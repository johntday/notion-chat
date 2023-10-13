import os
import streamlit as st

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from notion_utils.MyNotionDBLoader import MyNotionDBLoader
from mods.load_util import split_documents


def get_qdrant_client(url: str, api_key: str) -> QdrantClient:
    qclient = QdrantClient(
        url=url,
        prefer_grpc=True,
        api_key=api_key,
    )
    return qclient


def get_vector_db(q_client: QdrantClient, collection_name: str, embeddings) -> Qdrant:
    vectors = Qdrant(
        client=q_client,
        collection_name=collection_name,
        embeddings=embeddings
    )
    return vectors


def recreate_collection(q_client: QdrantClient) -> None:
    q_client.recreate_collection(
        # https://qdrant.tech/documentation/how_to/#prefer-high-precision-with-high-speed-search
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                always_ram=True,
            ),
        ),
    )


def load_qdrant(args):
    """Fetch documents from Notion"""
    notion_loader = MyNotionDBLoader(
        os.getenv("NOTION_TOKEN"),
        os.getenv("NOTION_DATABASE_ID"),
        args.verbose,
    )
    docs = notion_loader.load()
    print(f"\nFetched {len(docs)} documents from Notion")

    """Split documents into chunks"""
    doc_chunks = split_documents(docs)

    """Get Qdrant client"""
    q_client = get_qdrant_client(os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY"))

    if args.reset:
        print("\nStart recreating Qdrant collection...")
        recreate_collection(q_client)
        print("Finished recreating Qdrant collection")

    if args.verbose:
        collection_info = q_client.get_collection(collection_name=os.getenv("QDRANT_COLLECTION_NAME"))
        print(f"\nCollection info: {collection_info.json()}")

    """Qdrant Vector DB"""
    embeddings = OpenAIEmbeddings()
    collection_name = os.getenv("QDRANT_COLLECTION_NAME")
    vectors = get_vector_db(q_client, collection_name, embeddings)

    print("\nStart loading documents to Qdrant...")

    batch_chunk_size = 50
    print(f"Number of documents: {len(doc_chunks)}")
    doc_chunks_list = [doc_chunks[i:i + batch_chunk_size] for i in range(0, len(doc_chunks), batch_chunk_size)]
    number_of_batches = len(doc_chunks_list)
    print(f"Number of batches: {number_of_batches}")

    for j in range(0, len(doc_chunks_list)):
        print(f"Loading batch number {j + 1} of {number_of_batches}...")

        Qdrant.add_documents(
            self=vectors,
            documents=doc_chunks_list[j],
        )

    print("Finished loading documents to Qdrant")

    if args.verbose:
        collection_info = q_client.get_collection(collection_name=os.getenv("QDRANT_COLLECTION_NAME"))
        print(f"\nCollection info: {collection_info.json()}")


def setup_chatbot(model_name, temperature, k, search_type, verbose):
    print("setup_chatbot") if verbose else None
    """
    Sets up the chatbot with the uploaded file, model, and temperature
    """
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

    # if "chatbot_memory" not in st.session_state or st.session_state["chatbot_reset"]:
    #     st.session_state["chatbot_memory"] = ConversationBufferMemory(
    #         memory_key="chat_history",
    #         input_key='question',
    #         output_key='answer',
    #         return_messages=True
    #     )

    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name=model_name, temperature=temperature),
        retriever=vectors.as_retriever(search_type=search_type, search_kwargs={'k': k}),
        condense_question_prompt=qa_prompt,
        # memory=st.session_state["chatbot_memory"],
        return_source_documents=True,
        verbose=verbose,
    )

    st.session_state["chatbot"] = qa
    st.session_state["chatbot_reset"] = False

# Chatbot to answer your questions as a conversational agent from a Notion knowledge base
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://johntday-notion-chat-chat-xcbtq4.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Purpose
An experimental [RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) chatbot using Notion database as knowledge base. The chatbot is built using
- [Streamlit](https://streamlit.io/) web app for the chatbot
- [Qdrant](https://qdrant.tech/) for vector search
- [OpenAI](https://openai.com/blog/openai-api/) for text generation and embeddings
- [Notion](https://developers.notion.com/) for fetching content and metadata from Notion database

[Article](https://medium.com/@johntday/creating-a-custom-ai-rag-from-your-notion-database-openai-python-langchain-notion-qdrant-f778e2bee3b8) with step-by-step details.

## Features

- Chatbot using OpenAI models for RAG text generation and embeddings
- Uses Notion database documents for document embeddings
- Uses Qdrant for vector search
- Streamlit web app for the chatbot
- Settings for search are configurable
- Search result embeddings from Notion database are shown


## Example

Example of the chatbot answering questions from a [Notion database](https://www.notion.so/johntday/db0ee43b057247c9a897d8dd57ff34a3?v=e16d4dba585746de9c067f4c32c0b020&pvs=4).  The database is a knowledge base about SAP Commerce (Hybris) - an eCommerce platform by SAP.

![AI-RAG-using-notion-db.gif](docs/images/AI-RAG-using-notion-db.gif)



## HOW TO RUN THE APP LOCALLY
Follow these steps to set up and run the python app locally :

### Prerequisites
- Python 3.8 or higher
- Git
- Poetry

### Installation
Clone the repository :

```bash
git clone https://github.com/johntday/notion-chat.git
```

Navigate to the project directory :

```bash
cd notion-chat
# now at project root
```

Create a virtual environment and install requirements using Poetry :
```bash
poetry install
```

Setup Environment Variables :
```bash
# at project root
cp notion_chat/.streamlit/secrets.toml.example notion_chat/.streamlit/secrets.toml

# edit the "secrets.toml" file and add your OpenAI API key
```

Run the app locally :

```bash
cd notion_chat
streamlit run chat.py
```

### Pycharm Run Configuration

If you are using Pycharm, you can create a run configuration to run the app locally :

![img.png](docs/images/img.png)

## References
- [Streamlit](https://streamlit.io/)
- [Qdrant](https://qdrant.tech/)
- [OpenAI](https://openai.com/blog/openai-api/)
- [Notion](https://developers.notion.com/)
- [Langchain](https://python.langchain.com/)
- [Using Poetry](https://johntday.github.io/python-poetry/)
- [Article with Step by Step Details](https://medium.com/@johntday/creating-a-custom-ai-rag-from-your-notion-database-openai-python-langchain-notion-qdrant-f778e2bee3b8)

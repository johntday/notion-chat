# Chatbot to answer your questions as a conversational agent from a Notion knowledge base
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://johntday-notion-chat-chat-xcbtq4.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Purpose
An experimental AI chatbot using Notion database as knowledge base. The chatbot is built using
- [Streamlit](https://streamlit.io/) for the web app
- [Qdrant](https://qdrant.tech/) for vector search
- [OpenAI](https://openai.com/blog/openai-api/) for text generation and embeddings
- [Notion](https://developers.notion.com/) for fetching content and metadata from Notion database

## DEMO
Use the following link to try it out :
[Chatbot using a knowledge base pulled from Notion database](https://johntday-notion-chat-chat-xcbtq4.streamlit.app/)

fixme: qdrant

fixme: notion

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
```

Create a virtual environment and install requirements using Poetry :
```bash
poetry install
```

Run the app locally :

```bash
cd notion_chat
streamlit run chat.py
```

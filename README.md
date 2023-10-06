# Chatbot to answer your questions as a conversational agent from a Notion knowledge base 
[![Build Status](https://travis-ci.com/johntday/hybris-chatbot.svg?branch=main)](https://travis-ci.com/johntday/hybris-chatbot)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/johntday/hybris-chatbot/chat.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Purpose
An experimental AI chatbot using Notion database as knowledge base. The chatbot is built using
- [Streamlit](https://streamlit.io/) for the web app, and 
- [Qdrant](https://qdrant.tech/) for vector search, and
- [OpenAI](https://openai.com/blog/openai-api/) for text generation and embeddings, and
- [Notion](https://developers.notion.com/) for fetching content and metadata from Notion database.

## Demo
Use the following link to try it out :
[Chatbot using a knowledge base pulled from Notion database](https://johntday-notion-chat-chat-xcbtq4.streamlit.app/)

## How to Run Locally
Follow these steps to set up and run the python app locally :

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
Clone the repository :

```bash
git clone https://github.com/johntday/hybris-chatbot.git
```

Navigate to the project directory :

```bash
cd hybris-chatbot
```

Create a virtual environment :
```bash
python -m venv venv
source venv/bin/activate
```

Install the required dependencies in the virtual environment :

```bash
pip install -r requirements.txt
```

Launch the chat service locally :

```bash
streamlit run chat.py
```

Crontab to load the Notion embeddings to Qdrant on a schedule :

```bash
crontab -e
```

Add the following line to the crontab file and write-quit (ESC and wq) :

```bash
0 0 * * * "cd /path/to/hybris-chatbot && source venv/bin/activate && python3 load.py notion qdrant -r >> /path to/notion-qdrant-load.log 2>&1"
```

This will run the load script every day at midnight and log the output to a file.

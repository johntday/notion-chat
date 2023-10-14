from langchain.llms import OpenAI
from langchain.chains import AnalyzeDocumentChain
import os
from typing import Any, Dict

from dotenv import load_dotenv

from notion_utils.MyNotionDBLoader import MyNotionDBLoader


def analyze_long_doc():
    page_id = "fbff439b-1686-4616-901b-2ca28cc220fb"
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    notion_token = os.getenv("NOTION_TOKEN")

    notion = MyNotionDBLoader(
        integration_token=notion_token,
        database_id=NOTION_DATABASE_ID,
        verbose=True,
        validate_missing_content=False,
        validate_missing_metadata=[],
    )
    page_summary: Dict[str, Any] = {"id": page_id, "properties": {"type": "xxx"}}
    docs = notion.load_page(page_summary)
    if not docs or len(docs) == 0:
        raise ValueError("No documents found")

    print(docs[0].page_content)

    exit(1)

    with open("../../state_of_the_union.txt") as f:
        state_of_the_union = f.read()

    llm = OpenAI(temperature=0)

    from langchain.chains.question_answering import load_qa_chain

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")

    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    qa_document_chain.run(input_document=state_of_the_union, question="what did the president say about justice breyer?")


if __name__ == '__main__':
    load_dotenv(".streamlit/secrets.toml")

    analyze_long_doc()

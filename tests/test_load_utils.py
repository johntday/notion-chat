import os

from notion_utils.MyNotionDBLoader import MyNotionDBLoader
from dotenv import load_dotenv

load_dotenv()

NOTION_MOVIE_DATABASE_ID1 = os.getenv("NOTION_MOVIE_DATABASE_ID1")
NOTION_SERIES_DATABASE_ID2 = os.getenv("NOTION_SERIES_DATABASE_ID2")

notion_token = os.getenv("NOTION_TOKEN")

notion = MyNotionDBLoader(
    integration_token=notion_token,
    database_id=NOTION_MOVIE_DATABASE_ID1,
    verbose=True,
    metadata_filter_list=['title', 'plot'],
    validate_missing_content=False,
    validate_missing_metadata=['title', 'genres'],
)
docs = notion.load(query_dict={})

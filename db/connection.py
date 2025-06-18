from langchain_community.utilities import SQLDatabase
from config.db_settings import DBSettings

def get_database(settings: DBSettings):
    uri = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    return SQLDatabase.from_uri(uri)

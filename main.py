import os
from dotenv import load_dotenv
from graphs.sql_chat_bot_graph import SQLChatBotGraph
from config.db_settings import get_settings
from db.connection import get_database, get_store_uri
from llm.llm_provider import get_llm 

def main():
    load_dotenv()
    chat = get_llm()
    dbSettings = get_settings()
    db = get_database(dbSettings)
    db_admin_settings = get_settings(is_admin = True)
    store_uri = get_store_uri(db_admin_settings)
    SQLChatBotGraph.run_graph(chat, db, store_uri)

if __name__ == "__main__":
    main()

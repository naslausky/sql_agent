import os
from dotenv import load_dotenv
from graphs.sql_chat_bot_graph import SQLChatBotGraph
from graphs.sql_chat_bot_graph_state import initial_state
from config.db_settings import get_settings
from db.connection import get_database
from llm.llm_provider import get_llm 

def main():
    load_dotenv()
    chat = get_llm()
    dbSettings = get_settings()
    db = get_database(dbSettings)
    graph = SQLChatBotGraph(chat, db).build_sql_chatbot_graph()
    print("---Iniciando SQL Agent---")
    result = graph.invoke(initial_state)

if __name__ == "__main__":
    main()

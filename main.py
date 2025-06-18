import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from agents.sql_agent import create_sql_agent_with_safety, memoryConfig
from chains.sql_query_graph import SQLQueryGraph
from config.db_settings import get_settings
from db.connection import get_database
from llm.llm_provider import get_llm 
from prompts.prompts import Prompts

def main():
    load_dotenv()
    chat = get_llm()
    dbSettings = get_settings()
    db = get_database(dbSettings)
    graph = SQLQueryGraph(chat, db).build_sql_graph()
    SQLAgent = create_sql_agent_with_safety(db, chat)
    print("---Iniciando SQL Agent---")
    while True:
        pergunta = input("Pergunta: ")
        deveSair = "yes" in chat.invoke(Prompts.should_end_conversation_prompt(pergunta)).content.lower()
        if deveSair:
            break
        content = SQLAgent.invoke({"messages": [{"role": "user", "content": pergunta}]}, memoryConfig, )
        resposta = content["messages"][-1].content
        print("Resposta:", resposta)

if __name__ == "__main__":
    main()

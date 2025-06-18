from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model

from langchain_community.utilities import SQLDatabase

from langchain_core.prompts import ChatPromptTemplate

#Disponível apenas a partir do Python 3.8
from typing_extensions import TypedDict

from llm.llm_provider import get_llm 
from db.connection import get_database
from chains.sql_query_graph import SQLQueryGraph
from config.db_settings import get_settings
from agents.sql_agent import create_sql_agent 

def main():
    load_dotenv()
    chat = get_llm()
    dbSettings = get_settings()
    db = get_database(dbSettings)
    #db.run("DROP TABLE abacaxi;")
    print(db.get_usable_table_names())
    graph = SQLQueryGraph(chat, db).build_sql_graph()
    SQLAgent = create_sql_agent(db, chat)
    config = {"configurable": {"thread_id": "1"}}
    print("Iniciando SQL_Agent:")
    while True:
        pergunta = input("Pergunta: ")
        content = SQLAgent.invoke({"messages": [{"role": "user", "content": pergunta}]}, config,)
        resposta = content["messages"][-1].content
        if "EXIT" in resposta:
            break
        print("Resposta:", resposta)

if __name__ == "__main__":
    main()

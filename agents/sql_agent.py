from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.agent import RunnableAgent
from prompts.prompts import Prompts


memoryConfig = {"configurable": {"thread_id": "1"}}
def create_sql_agent(db, chat):
    toolkit = SQLDatabaseToolkit(db=db, llm=chat)
    tools = toolkit.get_tools() + []
    system_message = Prompts.sql_agent_system_message.format(
        dialect=db.dialect,
        top_k=5,
    )
    memory = MemorySaver()
    agent_executor = create_react_agent(chat, tools, prompt=system_message, checkpointer = memory)
    return agent_executor

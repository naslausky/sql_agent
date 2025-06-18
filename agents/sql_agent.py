from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import BaseTool
from langchain_community.utilities import SQLDatabase
from pydantic import Field
from typing import Type
from prompts.prompts import Prompts

memoryConfig = {"configurable": {"thread_id": "1"}}
def create_sql_agent(db, chat):
    """
    Creates a default sql agent without any SQL validations.
    """
    toolkit = SQLDatabaseToolkit(db=db, llm=chat)
    tools = toolkit.get_tools() + []
    system_message = Prompts.sql_agent_system_message.format(
        dialect=db.dialect,
        top_k=5,
    )
    memory = MemorySaver()
    agent_executor = create_react_agent(chat, tools, prompt=system_message, checkpointer = memory)
    return agent_executor

class SecureSQLQueryTool(BaseTool):
    """
    Custom tool to run queries SQL in a secure way.
    It checks for dangerous keywords before running the query.
    """
    name: str = "secure_sql_query_executor"
    description: str = """
        Useful to run syntactically correct SQL queries in the database.
        Input must be a well formed SQL query.
        This tool automatically makes a security check.
        This tool will NOT execute queries with keywords like 'DROP', 'DELETE', 'UPDATE', 'INSERT', or 'CREATE'. 
        If an unsafe query is detected, she will return a safety warning instead of running the query.
        Use this tool only to SELECT queries.
    """
    db: SQLDatabase = Field(exclude=True)

    def _run(self, query: str) -> str:
        """Runs the SQL query after a safety check."""
        q_upper = query.upper()
        is_safe = all(keyword not in q_upper for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER"])
        
        if not is_safe:
            return Prompts.unsafe_message
        return self.db.run(query) 

def create_sql_agent_with_safety(db, chat):
    """
    Creates a SQL agent with safety validation for running queries.
    It replaces the default SQL tool that runs the SQL to a custom tool with validation.
    """
    toolkit = SQLDatabaseToolkit(db=db, llm=chat)
    original_tools = toolkit.get_tools()
    secure_query_tool = SecureSQLQueryTool(db=db)
    safe_tools = [tool for tool in original_tools if tool.name != "query_sql_database"]
    safe_tools.append(secure_query_tool)
    system_message = Prompts.sql_agent_system_message.format(
        dialect=db.dialect,
        top_k=5,
    )
    memory = MemorySaver() 
    agent_executor = create_react_agent(chat, safe_tools, prompt=system_message, checkpointer=memory)
    return agent_executor

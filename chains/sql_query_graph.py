from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, START
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.prompts import ChatPromptTemplate
from prompts.prompts import Prompts
from .state import State

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, "Syntactically valid SQL query."]

class SQLQueryGraph:
    def __init__(self, chat, db):
        self.chat = chat
        self.db = db

    def is_query_safe(self, query: str) -> bool:
        """Helper function to determine if a query is safe. Not being used as its part of"""
        q_upper = query.upper()
        return all(keyword not in q_upper for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"])

    def prompt_template(self,):
        """Method to obtain the graph prompt template"""
        system_message = Prompts.graph_system_prompt 
        user_prompt = "Question: {input}"
        
        query_prompt_template = ChatPromptTemplate(
            [("system", system_message), ("user", user_prompt)]
        )
        return query_prompt_template


    def write_query(self, state: State):
        """Generate SQL query to fetch information."""
        prompt = self.prompt_template().invoke(
            {
                "dialect": self.db.dialect,
                "top_k": 10,
                "table_info": self.db.get_table_info(),
                "input": state["question"],
            }
        )
        structured_llm = self.chat.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}

    def execute_query(self, state: State):
        """Execute SQL query."""
        execute_query_tool = QuerySQLDatabaseTool(db=self.db)
        return {"result": execute_query_tool.invoke(state["query"])}

    def generate_answer(self, state: State):
        """Answer question using retrieved information as context."""
        prompt = Prompts.graph_prompt_formulate_answer(state)
        response = self.chat.invoke(prompt)
        return {"answer": response.content}

    def build_sql_graph(self):
        """Method to create the Graph chain."""
        graph_builder = StateGraph(State).add_sequence(
            [self.write_query, 
            self.execute_query, 
            self.generate_answer]
        )
        graph_builder.add_edge(START, "write_query")
        graph = graph_builder.compile()
        return graph

    def debugGraph(graph, initial_question): 
        for step in graph.stream(
        {"question": initial_question}, stream_mode="updates"
        ):
            print(step)

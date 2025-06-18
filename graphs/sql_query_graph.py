from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, START
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.prompts import ChatPromptTemplate
from prompts.prompts import Prompts
from .sql_query_graph_state import SQLQueryGraphState as State

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, "Syntactically valid SQL query."]

class SQLQueryGraph:
    """
    Class to show a default sql query graph without any premade agents.
    """
    def __init__(self, chat, db):
        self.chat = chat
        self.db = db

    def check_query_safety(self, state: State) -> bool:
        """Helper function to determine if a query is safe."""
        query = state["query"]
        q_upper = query.upper()
        isSafe = all(keyword not in q_upper for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE"])
        if not isSafe:
            return {"answer": Prompts.unsafeMessage}
        return state

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
        if SQLQueryGraph.is_query_blocked(state):
            return state
        prompt = Prompts.graph_prompt_formulate_answer(state)
        response = self.chat.invoke(prompt)
        return {"answer": response.content}

    def is_query_blocked(state):
        return "answer" in state and Prompts.unsafeMessage == state["answer"]

    def build_sql_graph(self):
        """Method to create the Graph chain."""

        graph_builder = StateGraph(State)

        graph_builder.add_node("write_query", self.write_query)
        graph_builder.add_node("check_query_safety", self.check_query_safety)
        graph_builder.add_node("execute_query", self.execute_query)
        graph_builder.add_node("generate_answer", self.generate_answer)

        graph_builder.add_edge(START, "write_query")
        graph_builder.add_edge("write_query", "check_query_safety")

        graph_builder.add_conditional_edges(
            "check_query_safety",
            SQLQueryGraph.is_query_blocked, 
            {
                True: "generate_answer",
                False: "execute_query"
            }
        )

        graph_builder.add_edge("execute_query", "generate_answer")
        graph = graph_builder.compile()
        return graph

    def debugGraph(graph, initial_question): 
        for step in graph.stream(
        {"question": initial_question}, stream_mode="updates"
        ):
            print(step)

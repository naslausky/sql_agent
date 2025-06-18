from langgraph.graph import StateGraph, START
from agents.sql_agent import create_sql_agent_with_safety, memoryConfig
from prompts.prompts import Prompts
from .sql_chat_bot_graph_state import SQLChatBotGraphState

class SQLChatBotGraph:
    """
    Graph with custom chat and validation with an SQLAgent node.
    """
    def __init__(self, chat, db):
        self.chat = chat
        self.db = db
        self.sqlAgent = create_sql_agent_with_safety(db, chat)

    def get_user_input(self, state: SQLChatBotGraphState) -> SQLChatBotGraphState:
        """
        LangGraph node to receive user input.
        """
        pergunta = input("Pergunta: ")
        state["user_input"] = pergunta
        return state
    
    def check_exit_intent(self, state: SQLChatBotGraphState) -> SQLChatBotGraphState:
        pergunta = state["user_input"]
        should_end_response = self.chat.invoke(Prompts.should_end_conversation_prompt(pergunta)).content.lower()
        state["should_end"] = "yes" in should_end_response
        return state

    def run_sql_agent(self, state: SQLChatBotGraphState) -> SQLChatBotGraphState:
        pergunta = state["user_input"]
        content = self.sqlAgent.invoke({"messages": [{"role": "user", "content": pergunta}]}, memoryConfig)
        state["response"] = content["messages"][-1].content
        return state

    def print_agent_answer(self, state: SQLChatBotGraphState) -> SQLChatBotGraphState:
        resposta = state["response"]
        print("Resposta:", resposta)
        return state

    def end_conversation(self, state: SQLChatBotGraphState) -> SQLChatBotGraphState:
        print("A conversa foi encerrada.")
        return state

    def should_end_conversation(state):
        return state.get("should_end", False)

    def build_sql_chatbot_graph(self):
        """Method to create the Chatbot Graph."""
        graph_builder = StateGraph(SQLChatBotGraphState)
        graph_builder.add_node("get_user_input", self.get_user_input)
        graph_builder.add_node("check_exit_intent", self.check_exit_intent)
        graph_builder.add_node("run_sql_agent", self.run_sql_agent)
        graph_builder.add_node("print_agent_answer", self.print_agent_answer)
        graph_builder.add_node("end_conversation", self.end_conversation)

        graph_builder.add_edge(START, "get_user_input")
        graph_builder.add_edge("get_user_input", "check_exit_intent")

        graph_builder.add_conditional_edges(
            "check_exit_intent",
            SQLChatBotGraph.should_end_conversation, 
            {
                True: "end_conversation",
                False: "run_sql_agent"
            }
        )

        graph_builder.add_edge("run_sql_agent", "print_agent_answer")
        graph_builder.add_edge("print_agent_answer", "get_user_input") 
        graph = graph_builder.compile()
        return graph

    def debugGraph(graph, initial_question): 
        for step in graph.stream(
            {"question": initial_question}, stream_mode="updates"
            ):
            print(step)

from typing_extensions import TypedDict

class SQLChatBotGraphState(TypedDict):
    should_end: bool
    user_input: str
    response: str
    user_id: str

initial_state = {"should_end": False, "user_input": "", "response": "", "user_id": ""}

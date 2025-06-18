from typing_extensions import TypedDict

class SQLChatBotGraphState(TypedDict):
    should_end: bool
    user_input: str
    response: str

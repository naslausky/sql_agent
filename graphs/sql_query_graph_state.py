from typing_extensions import TypedDict

class SQLQueryGraphState(TypedDict):
    question: str
    query: str
    result: str
    answer: str

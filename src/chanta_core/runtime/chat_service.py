
from __future__ import annotations
from chanta_core import LLMClient

class ChatService:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, user_input: str) -> str:
        return self.llm.chat(user_message=user_input)
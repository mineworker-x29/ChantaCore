from chanta_core.skills.builtin.llm_chat import (
    create_llm_chat_skill,
    execute_llm_chat_skill,
)

builtin_llm_chat_skill = create_llm_chat_skill

__all__ = [
    "builtin_llm_chat_skill",
    "create_llm_chat_skill",
    "execute_llm_chat_skill",
]

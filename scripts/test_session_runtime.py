from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.skills.builtin import create_llm_chat_skill
from chanta_core.skills.registry import SkillRegistry


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return "Fake runtime response."


def main() -> None:
    registry = SkillRegistry(include_builtins=False)
    registry.register(create_llm_chat_skill())
    runtime = AgentRuntime(llm_client=FakeLLMClient(), skill_registry=registry)
    result = runtime.run("Run OCEL-native session smoke test.")

    print(f"session_id={result.session_id}")
    print(f"process_instance_id={result.metadata.get('process_instance_id')}")
    print(f"turn_id={result.metadata.get('turn_id')}")
    print(f"user_message_id={result.metadata.get('user_message_id')}")
    print(f"assistant_message_id={result.metadata.get('assistant_message_id')}")
    print(f"response_text={result.response_text}")


if __name__ == "__main__":
    main()

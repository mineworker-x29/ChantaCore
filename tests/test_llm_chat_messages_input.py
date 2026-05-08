from chanta_core.skills.builtin.llm_chat import create_llm_chat_skill, execute_llm_chat_skill
from chanta_core.skills.context import SkillExecutionContext


class FakeLLMClient:
    settings = type("Settings", (), {"provider": "fake", "model": "fake-model"})()

    def __init__(self) -> None:
        self.messages = None

    def chat_messages(self, *, messages, temperature, max_tokens):
        self.messages = messages
        return "ok"


class FailingAssembler:
    def assemble_for_llm_chat(self, **_):
        raise AssertionError("prompt_messages path should not assemble prompt-only context")


class RecordingTraceService:
    def record_context_assembled(self, *_, **__):
        return None

    def record_llm_call_started(self, *_, **__):
        return None

    def record_llm_response_received(self, *_, **__):
        return None


def _context(context_attrs):
    return SkillExecutionContext(
        process_instance_id="process_instance:test",
        session_id="session:test",
        agent_id="agent:test",
        user_input="current",
        system_prompt="system",
        event_attrs={},
        context_attrs=context_attrs,
    )


def test_llm_chat_accepts_messages_input() -> None:
    client = FakeLLMClient()
    result = execute_llm_chat_skill(
        skill=create_llm_chat_skill(),
        context=_context(
            {
                "prompt_messages": [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "hello", "reasoning_content": "hidden"},
                ],
                "temperature": 0.0,
                "max_tokens": 32,
            }
        ),
        llm_client=client,
        context_assembler=FailingAssembler(),
        trace_service=RecordingTraceService(),
    )

    assert result.success is True
    assert client.messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello"},
    ]


def test_llm_chat_prompt_only_path_still_works() -> None:
    class PromptAssembler:
        def assemble_for_llm_chat(self, **_):
            return [{"role": "user", "content": "prompt only"}]

    client = FakeLLMClient()
    result = execute_llm_chat_skill(
        skill=create_llm_chat_skill(),
        context=_context({"temperature": 0.0, "max_tokens": 32}),
        llm_client=client,
        context_assembler=PromptAssembler(),
        trace_service=RecordingTraceService(),
    )

    assert result.success is True
    assert client.messages == [{"role": "user", "content": "prompt only"}]

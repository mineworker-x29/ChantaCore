from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_prompt_activation import PersonalPromptActivationResult
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.runtime.chat_service import ChatService
from chanta_core.traces.trace_service import TraceService


class CapturingLLMClient:
    settings = type("Settings", (), {"provider": "fake", "model": "fake-model"})()

    def __init__(self) -> None:
        self.calls: list[list[dict[str, str]]] = []

    def chat_messages(self, *, messages, temperature, max_tokens):
        self.calls.append(messages)
        return "fake response"


class StubPersonalPromptActivationService:
    def __init__(self) -> None:
        self.result = PersonalPromptActivationResult(
            result_id="personal_prompt_activation_result:test",
            request_id="personal_prompt_activation_request:test",
            status="attached",
            activation_scope="prompt_context_only",
            attached_block_ids=["personal_prompt_activation_block:test"],
            total_chars=20,
            truncated=False,
            denied=False,
            finding_ids=[],
            created_at="2026-01-01T00:00:00Z",
        )

    def activate_for_prompt_context(self, **kwargs):
        return self.result

    def render_activation_blocks(self, *, result):
        return "Personal Mode Prompt Activation:\nActivation scope: prompt_context_only."


def test_agent_runtime_inserts_personal_prompt_activation_between_persona_and_capability(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "runtime.sqlite")),
        personal_prompt_activation_service=StubPersonalPromptActivationService(),
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat("hello", session_id="session:personal-prompt-activation")
    messages = client.calls[-1]
    contents = [message["content"] for message in messages]

    assert response == "fake response"
    persona_index = next(i for i, content in enumerate(contents) if "Persona projection:" in content)
    activation_index = next(
        i for i, content in enumerate(contents) if "Personal Mode Prompt Activation:" in content
    )
    capability_index = next(
        i for i, content in enumerate(contents) if "Runtime capability decision surface:" in content
    )
    assert persona_index < activation_index < capability_index

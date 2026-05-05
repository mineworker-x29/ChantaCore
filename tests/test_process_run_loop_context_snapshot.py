from __future__ import annotations

from dataclasses import dataclass, field

from chanta_core.context import ContextSnapshotPolicy
from chanta_core.llm.types import ChatMessage
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


@dataclass
class CapturingFakeLLMClient:
    settings: FakeLLMSettings = field(default_factory=FakeLLMSettings)
    received_messages: list[list[ChatMessage]] = field(default_factory=list)

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        self.received_messages.append(messages)
        return "snapshot response"


def test_process_run_loop_can_create_context_snapshot_without_lm_studio() -> None:
    fake_llm = CapturingFakeLLMClient()
    loop = ProcessRunLoop(
        llm_client=fake_llm,
        policy=ProcessRunPolicy(
            enable_context_snapshot=True,
            context_snapshot_policy=ContextSnapshotPolicy(
                enabled=True,
                storage_mode="preview",
            ),
        ),
    )

    result = loop.run(
        process_instance_id="process:snapshot-loop",
        session_id="session:snapshot-loop",
        agent_id="chanta_core_default",
        user_input="hello API_KEY=secret",
        system_prompt="system",
    )

    assert result.status == "completed"
    assert fake_llm.received_messages
    assert loop.context_assembler.last_snapshot is not None
    assert loop.context_assembler.last_snapshot.process_instance_id == (
        "process:snapshot-loop"
    )
    previews = [
        snapshot.content_preview or ""
        for snapshot in loop.context_assembler.last_snapshot.message_snapshots
    ]
    assert any("API_KEY=[REDACTED]" in preview for preview in previews)
    assert all("secret" not in preview for preview in previews)

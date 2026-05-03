from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
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
        raise AssertionError("PI artifact skills must not call LLM")


def pi_context(tmp_path) -> SkillExecutionContext:
    return SkillExecutionContext(
        process_instance_id="process_instance:pi-skills",
        session_id="session-pi-skills",
        agent_id="chanta_core_default",
        user_input="Repeated fail_skill_execution suggests review_skill_failure.",
        system_prompt=None,
        context_attrs={
            "pi_artifact_store_path": str(tmp_path / "pi_artifacts.jsonl"),
            "artifact_type": "diagnostic",
            "confidence": 0.7,
        },
    )


def test_pi_artifact_skills_execute_without_llm(tmp_path) -> None:
    registry = SkillRegistry()
    executor = SkillExecutor(llm_client=FakeLLMClient())
    context = pi_context(tmp_path)

    ingest_result = executor.execute(
        registry.require("skill:ingest_human_pi"),
        context,
    )
    summarize_result = executor.execute(
        registry.require("skill:summarize_pi_artifacts"),
        SkillExecutionContext(
            **{
                **context.to_dict(),
                "user_input": "summarize",
                "context_attrs": {
                    "pi_artifact_store_path": str(tmp_path / "pi_artifacts.jsonl")
                },
                "pig_context": None,
            }
        ),
    )
    artifacts = PIArtifactStore(tmp_path / "pi_artifacts.jsonl").load_all()

    assert ingest_result.success is True
    assert ingest_result.output_attrs["artifact_id"]
    assert ingest_result.output_attrs["artifact_type"] == "diagnostic"
    assert ingest_result.output_attrs["source_type"] == "human_pi"
    assert ingest_result.output_attrs["confidence"] == 0.7
    assert len(artifacts) == 1

    assert summarize_result.success is True
    assert summarize_result.output_attrs["artifact_count"] == 1
    assert summarize_result.output_attrs["artifact_types"] == {"diagnostic": 1}
    assert summarize_result.output_attrs["recent_titles"]

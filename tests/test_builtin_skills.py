from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService
from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.trace_service import TraceService


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
        return "Fake summary."


def skill_context(name: str) -> SkillExecutionContext:
    return SkillExecutionContext(
        process_instance_id=f"process_instance:{name}",
        session_id=f"test-session-{name}",
        agent_id="chanta_core_default",
        user_input=f"{name} input text",
        system_prompt="You are a test agent.",
        event_attrs={},
        context_attrs={"iteration": 0},
    )


def test_registry_registers_all_builtin_skills() -> None:
    registry = SkillRegistry()

    assert PIGContext is not None
    assert PIGFeedbackService is not None
    assert [skill.skill_id for skill in registry.list_skills()] == [
        "skill:agent_behavior_infer",
        "skill:agent_observation_normalize",
        "skill:agent_observation_source_inspect",
        "skill:agent_process_narrative",
        "skill:agent_trace_observe",
        "skill:apply_approved_patch",
        "skill:check_self_conformance",
        "skill:echo",
        "skill:external_behavior_fingerprint",
        "skill:external_skill_adapter_candidate",
        "skill:external_skill_assimilate",
        "skill:external_skill_source_inspect",
        "skill:external_skill_static_digest",
        "skill:ingest_human_pi",
        "skill:inspect_ocel_recent",
        "skill:list_workspace_files",
        "skill:llm_chat",
        "skill:propose_file_edit",
        "skill:read_workspace_text_file",
        "skill:run_scheduler_once",
        "skill:run_worker_once",
        "skill:summarize_pi_artifacts",
        "skill:summarize_process_trace",
        "skill:summarize_text",
        "skill:summarize_workspace_markdown",
    ]


def test_builtin_echo_executes_without_llm(tmp_path) -> None:
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "echo.sqlite")),
    )
    skill = SkillRegistry().require("skill:echo")

    result = executor.execute(skill, skill_context("echo"))

    assert result.success is True
    assert result.output_text == "echo input text"
    assert result.output_attrs["echoed"] is True


def test_builtin_summarize_text_executes_with_fake_llm(tmp_path) -> None:
    store = OCELStore(tmp_path / "summarize_text.sqlite")
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        context_assembler=ProcessContextAssembler(),
        trace_service=TraceService(ocel_store=store),
    )
    skill = SkillRegistry().require("skill:summarize_text")

    result = executor.execute(skill, skill_context("summarize-text"))

    assert result.success is True
    assert result.output_text == "Fake summary."
    assert result.output_attrs["summary_mode"] == "builtin_summarize_text"
    assert [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-summarize-text")
    ] == ["call_llm", "receive_llm_response"]


def test_builtin_pi_skills_execute_without_llm(tmp_path) -> None:
    store = OCELStore(tmp_path / "pi_builtins.sqlite")
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )
    loop.run(
        process_instance_id="process_instance:pi-builtins",
        session_id="test-session-pi-builtins",
        agent_id="chanta_core_default",
        user_input="seed process trace",
        system_prompt="You are a test agent.",
        skill_id="skill:echo",
    )
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )

    inspect_result = executor.execute(
        SkillRegistry().require("skill:inspect_ocel_recent"),
        skill_context("inspect-ocel"),
    )
    trace_result = executor.execute(
        SkillRegistry().require("skill:summarize_process_trace"),
        SkillExecutionContext(
            process_instance_id="process_instance:pi-builtins",
            session_id="test-session-summarize-trace",
            agent_id="chanta_core_default",
            user_input="summarize trace",
            system_prompt=None,
            event_attrs={},
            context_attrs={"process_instance_id": "process_instance:pi-builtins"},
        ),
    )

    assert inspect_result.success is True
    assert inspect_result.output_attrs["event_count"] > 0
    assert trace_result.success is True
    assert trace_result.output_attrs["scope"] == "process_instance"
    assert trace_result.output_attrs["activity_sequence"]

    conformance_result = executor.execute(
        SkillRegistry().require("skill:check_self_conformance"),
        SkillExecutionContext(
            process_instance_id="process_instance:pi-builtins",
            session_id="test-session-check-conformance",
            agent_id="chanta_core_default",
            user_input="check self conformance",
            system_prompt=None,
            event_attrs={},
            context_attrs={"process_instance_id": "process_instance:pi-builtins"},
        ),
    )

    assert conformance_result.success is True
    assert conformance_result.output_attrs["scope"] == "process_instance"
    assert conformance_result.output_attrs["diagnostic_only"] is True

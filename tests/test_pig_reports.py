from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.instructions import InstructionService
from chanta_core.hooks import HookLifecycleService
from chanta_core.memory import MemoryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.reports import PIGReportService, ProcessRunReport
from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.session import SessionContinuityService, SessionService
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
        return "fake"


def seed_trace(store: OCELStore) -> tuple[str, str]:
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )
    result = loop.run(
        process_instance_id="process_instance:report-test",
        session_id="session-report-test",
        agent_id="chanta_core_default",
        user_input="report trace",
        skill_id="skill:echo",
    )
    return result.process_instance_id, result.session_id


def test_build_recent_report_returns_process_run_report(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report.sqlite")
    seed_trace(store)
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=50)
    data = report.to_dict()

    assert isinstance(report, ProcessRunReport)
    assert "ChantaCore PI Report" in report.report_text
    assert isinstance(report.activity_sequence, list)
    assert report.relation_coverage
    assert report.conformance_report is not None
    assert report.skill_usage_summary is not None
    assert report.tool_usage_summary is not None
    assert data["report_text"] == report.report_text


def test_build_process_instance_and_session_reports(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_scopes.sqlite")
    process_instance_id, session_id = seed_trace(store)
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    process_report = service.build_process_instance_report(process_instance_id)
    session_report = service.build_session_report(session_id)

    assert process_report.scope == "process_instance"
    assert process_report.process_instance_id == process_instance_id
    assert session_report.scope == "session"
    assert session_report.session_id == session_id
    for report in [process_report, session_report]:
        assert report.variant_summary
        assert report.performance_summary
        assert report.decision_summary is not None
        assert report.guidance_summary is not None


def test_report_includes_memory_instruction_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_memory_instruction.sqlite")
    trace_service = TraceService(ocel_store=store)
    memory_service = MemoryService(trace_service=trace_service)
    instruction_service = InstructionService(trace_service=trace_service)
    memory = memory_service.create_memory_entry(
        memory_type="semantic",
        title="Memory",
        content="Memory report count.",
        session_id="session-report-memory",
    )
    memory_service.revise_memory_entry(
        memory=memory,
        new_content="Memory report count updated.",
    )
    instruction = instruction_service.register_instruction_artifact(
        instruction_type="project",
        title="Instruction",
        body="Instruction report count.",
        session_id="session-report-memory",
    )
    instruction_service.register_project_rule(
        rule_type="constraint",
        text="Report memory counts.",
        source_instruction_id=instruction.instruction_id,
    )
    instruction_service.register_user_preference(
        preference_key="report",
        preference_value="include counts",
        session_id="session-report-memory",
    )
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=50)
    summary = report.report_attrs["memory_instruction_summary"]

    assert summary["memory_entry_count"] >= 1
    assert summary["memory_revision_count"] >= 1
    assert summary["instruction_artifact_count"] >= 1
    assert summary["project_rule_count"] >= 1
    assert summary["user_preference_count"] >= 1
    assert summary["memory_event_count"] >= 2
    assert summary["instruction_event_count"] >= 3
    assert "Memory / Instruction Substrate" in report.report_text


def test_report_includes_hook_lifecycle_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_hooks.sqlite")
    hook_service = HookLifecycleService(trace_service=TraceService(ocel_store=store))
    hook = hook_service.register_hook_definition(
        hook_name="Report hook",
        hook_type="observer",
        lifecycle_stage="pre_process_run",
    )
    hook_service.register_hook_policy(hook_id=hook.hook_id)
    hook_service.observe_lifecycle_point(
        lifecycle_stage="pre_process_run",
        process_instance_id="process_instance:hook-report",
    )
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=50)
    summary = report.report_attrs["hook_lifecycle_summary"]

    assert summary["hook_definition_count"] >= 1
    assert summary["hook_invocation_count"] >= 1
    assert summary["hook_result_count"] >= 1
    assert summary["hook_policy_count"] >= 1
    assert summary["hook_invoked_count"] >= 1
    assert summary["hook_completed_count"] >= 1
    assert summary["hook_invocation_by_stage"]["pre_process_run"] >= 1
    assert "Hook Lifecycle Observability" in report.report_text


def test_report_includes_session_continuity_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_continuity.sqlite")
    trace_service = TraceService(ocel_store=store)
    session_service = SessionService(trace_service=trace_service)
    session = session_service.start_session(session_name="continuity-report")
    session_service.record_user_message(
        session_id=session.session_id,
        turn_id=None,
        content="continue",
    )
    continuity = SessionContinuityService(trace_service=trace_service)
    continuity.resume_session(session_id=session.session_id)
    continuity.fork_session(parent_session_id=session.session_id)
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=100)
    summary = report.report_attrs["session_continuity_summary"]

    assert summary["session_resume_count"] >= 1
    assert summary["session_fork_count"] >= 1
    assert summary["session_context_snapshot_count"] >= 1
    assert summary["session_permission_reset_count"] >= 2
    assert summary["fork_lineage_count"] >= 1
    assert "Session Continuity" in report.report_text

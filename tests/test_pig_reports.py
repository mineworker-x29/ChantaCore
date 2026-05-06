from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.instructions import InstructionService
from chanta_core.hooks import HookLifecycleService
from chanta_core.memory import MemoryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.outcomes import ProcessOutcomeEvaluationService
from chanta_core.pig.reports import PIGReportService, ProcessRunReport
from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.session import SessionContinuityService, SessionService
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.read_only_skills import ReadOnlyVerificationSkillService


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


def test_report_includes_tool_registry_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_tool_registry.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = ToolRegistryViewService(trace_service=trace_service, root=tmp_path)
    read_tool = service.register_tool_descriptor(
        tool_name="read_file",
        tool_type="builtin",
        risk_level="read_only",
    )
    write_tool = service.register_tool_descriptor(
        tool_name="write_file",
        tool_type="builtin",
        risk_level="high",
    )
    snapshot = service.create_registry_snapshot(tools=[read_tool, write_tool])
    note = service.register_tool_policy_note(
        tool_id=write_tool.tool_id,
        tool_name=write_tool.tool_name,
        note_type="review_needed",
        text="Review write operations.",
    )
    annotation = service.register_tool_risk_annotation(
        tool_id=write_tool.tool_id,
        risk_level="high",
        risk_category="write",
    )
    service.write_tool_views(
        tools=[read_tool, write_tool],
        snapshot=snapshot,
        policy_notes=[note],
        risk_annotations=[annotation],
        root=tmp_path,
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["tool_registry_summary"]

    assert summary["tool_descriptor_count"] >= 2
    assert summary["tool_registry_snapshot_count"] >= 1
    assert summary["tool_policy_note_count"] >= 1
    assert summary["tool_risk_annotation_count"] >= 1
    assert summary["tool_type_distribution"]["builtin"] >= 2
    assert summary["tool_risk_level_distribution"]["high"] >= 1
    assert "Tool Registry / Policy View" in report.report_text


def test_report_includes_verification_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_verification.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = VerificationService(trace_service=trace_service)
    contract = service.register_contract(
        contract_name="README contract",
        contract_type="file_existence",
    )
    target = service.register_target(target_type="file", target_ref="README.md")
    service.register_requirement(
        contract_id=contract.contract_id,
        requirement_type="must_exist",
        description="README must be represented by supplied evidence.",
    )
    run = service.start_run(contract_id=contract.contract_id, target_ids=[target.target_id])
    evidence = service.record_evidence(
        run_id=run.run_id,
        target_id=target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Manual observation.",
    )
    service.record_result(
        contract_id=contract.contract_id,
        run_id=run.run_id,
        target_id=target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
    )
    service.complete_run(run=run)
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["verification_summary"]

    assert summary["verification_contract_count"] >= 1
    assert summary["verification_target_count"] >= 1
    assert summary["verification_requirement_count"] >= 1
    assert summary["verification_run_count"] >= 1
    assert summary["verification_evidence_count"] >= 1
    assert summary["verification_result_count"] >= 1
    assert summary["verification_passed_count"] >= 1
    assert summary["verification_result_by_contract_type"]["file_existence"] >= 1
    assert summary["verification_result_by_target_type"]["file"] >= 1
    assert "Verification Contract Foundation" in report.report_text


def test_report_includes_read_only_verification_skill_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_read_only_verification.sqlite")
    trace_service = TraceService(ocel_store=store)
    skill_service = ReadOnlyVerificationSkillService(
        verification_service=VerificationService(trace_service=trace_service),
        root=tmp_path,
        ocel_store=store,
    )
    target_file = tmp_path / "exists.txt"
    target_file.write_text("present", encoding="utf-8")
    view = tmp_path / "MEMORY.md"
    view.write_text(
        "Generated materialized view\nCanonical source: OCEL\nThis file is not canonical.\nEdits do not update canonical source.",
        encoding="utf-8",
    )

    skill_service.verify_file_exists(path="exists.txt")
    skill_service.verify_tool_available(tool_name="definitely_missing_tool")
    skill_service.verify_ocel_object_type_exists(
        object_type="verification_result",
        known_object_types=["verification_result"],
    )
    skill_service.verify_materialized_view_warning(path="MEMORY.md")
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["verification_summary"]

    assert summary["read_only_verification_skill_run_count"] >= 4
    assert summary["file_existence_verification_count"] >= 1
    assert summary["tool_availability_verification_count"] >= 1
    assert summary["ocel_shape_verification_count"] >= 1
    assert summary["materialized_view_warning_verification_count"] >= 1
    assert summary["verification_skill_passed_count"] >= 3
    assert summary["verification_skill_failed_count"] >= 1


def test_report_includes_process_outcome_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_process_outcome.sqlite")
    trace_service = TraceService(ocel_store=store)
    verification_service = VerificationService(trace_service=trace_service)
    outcome_service = ProcessOutcomeEvaluationService(trace_service=trace_service)
    verification_contract = verification_service.register_contract(
        contract_name="Manual verification",
        contract_type="manual",
    )
    verification_target = verification_service.register_target(
        target_type="process_instance",
        target_ref="process_instance:outcome-report",
    )
    run = verification_service.start_run(
        contract_id=verification_contract.contract_id,
        target_ids=[verification_target.target_id],
    )
    evidence = verification_service.record_evidence(
        run_id=run.run_id,
        target_id=verification_target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Report evidence.",
    )
    verification_result = verification_service.record_result(
        contract_id=verification_contract.contract_id,
        run_id=run.run_id,
        target_id=verification_target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
    )
    outcome_contract = outcome_service.register_contract(
        contract_name="Outcome report",
        contract_type="process_completion",
        target_type="process_instance",
    )
    outcome_service.register_criterion(
        contract_id=outcome_contract.contract_id,
        criterion_type="verification_passed",
        description="Verification must pass.",
    )
    outcome_target = outcome_service.register_target(
        target_type="process_instance",
        target_ref="process_instance:outcome-report",
    )
    outcome_service.evaluate_from_verification_results(
        contract=outcome_contract,
        target=outcome_target,
        verification_results=[verification_result],
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["process_outcome_summary"]

    assert summary["process_outcome_contract_count"] >= 1
    assert summary["process_outcome_criterion_count"] >= 1
    assert summary["process_outcome_target_count"] >= 1
    assert summary["process_outcome_signal_count"] >= 1
    assert summary["process_outcome_evaluation_count"] >= 1
    assert summary["process_outcome_success_count"] >= 1
    assert summary["average_evidence_coverage"] == 1.0
    assert summary["average_outcome_score"] == 1.0
    assert summary["process_outcome_by_contract_type"]["process_completion"] >= 1
    assert summary["process_outcome_by_target_type"]["process_instance"] >= 1
    assert "Process Outcome Evaluation" in report.report_text

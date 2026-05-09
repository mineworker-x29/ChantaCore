from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.capabilities import CapabilityDecisionSurfaceService
from chanta_core.instructions import InstructionService
from chanta_core.hooks import HookLifecycleService
from chanta_core.delegation import DelegatedProcessRunService, SidechainContextService
from chanta_core.delegation import DelegationConformanceService
from chanta_core.external import (
    ExternalAdapterReviewService,
    ExternalCapabilityImportService,
    ExternalCapabilityRegistryViewService,
    ExternalOCELImportCandidateService,
    MCPPluginDescriptorSkeletonService,
)
from chanta_core.memory import MemoryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.outcomes import ProcessOutcomeEvaluationService
from chanta_core.permissions import PermissionModelService, SessionPermissionService
from chanta_core.persona import (
    PersonalConformanceService,
    PersonalModeBindingService,
    PersonalRuntimeSmokeTestService,
    PersonaLoadingService,
    PersonaSourceStagedImportService,
    PersonalModeLoadoutService,
    PersonalOverlayLoaderService,
)
from chanta_core.pig.reports import PIGReportService, ProcessRunReport
from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.sandbox import WorkspaceWriteSandboxService
from chanta_core.session import SessionContextAssembler, SessionContinuityService, SessionService
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.read_only_skills import ReadOnlyVerificationSkillService
from chanta_core.workspace import WorkspaceReadService


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


def test_report_includes_session_context_projection_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_session_context_projection.sqlite")
    trace_service = TraceService(ocel_store=store)
    session_service = SessionService(trace_service=trace_service)
    assembler = SessionContextAssembler(trace_service=trace_service)
    session_service.start_session(session_id="session:pig-context")
    first = session_service.record_user_message(
        session_id="session:pig-context",
        turn_id=None,
        content="first",
    )
    second = session_service.record_assistant_message(
        session_id="session:pig-context",
        turn_id=None,
        content="second",
    )
    projection = assembler.assemble_projection_from_messages(
        session_id="session:pig-context",
        messages=[first, second],
    )
    assembler.render_projection_to_llm_messages(
        projection=projection,
        system_prompt="system",
        current_user_message="current",
    )
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=50)
    summary = report.report_attrs["session_context_projection_summary"]

    assert summary["session_context_policy_count"] >= 1
    assert summary["session_context_projection_count"] >= 1
    assert summary["session_prompt_render_count"] >= 1
    assert summary["average_session_context_projection_messages"] >= 2
    assert "Context projections" in report.report_text


def test_report_includes_capability_decision_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_capability_decision.sqlite")
    CapabilityDecisionSurfaceService(
        trace_service=TraceService(ocel_store=store)
    ).build_decision_surface("powershell ?ㅽ뻾", session_id="session:capability")
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=50)
    summary = report.report_attrs["capability_decision_summary"]

    assert summary["capability_request_intent_count"] >= 1
    assert summary["capability_requirement_count"] >= 1
    assert summary["capability_decision_count"] >= 1
    assert summary["capability_decision_surface_count"] >= 1
    assert summary["capability_requires_permission_count"] >= 1
    assert summary["capability_unfulfillable_request_count"] >= 1
    assert "Runtime Capability Decision Surface" in report.report_text


def test_report_includes_workspace_read_counts(tmp_path) -> None:
    (tmp_path / "doc.md").write_text("# Main\nBody", encoding="utf-8")
    store = OCELStore(tmp_path / "pig_report_workspace_read.sqlite")
    workspace_read = WorkspaceReadService(trace_service=TraceService(ocel_store=store))
    root = workspace_read.register_read_root(tmp_path)
    workspace_read.list_workspace_files(root=root)
    workspace_read.read_workspace_text_file(root=root, relative_path="doc.md")
    workspace_read.summarize_workspace_markdown(root=root, relative_path="doc.md")
    workspace_read.read_workspace_text_file(root=root, relative_path="../outside.md")
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=100)
    summary = report.report_attrs["workspace_read_summary"]

    assert summary["workspace_read_root_count"] >= 1
    assert summary["workspace_file_list_result_count"] >= 1
    assert summary["workspace_text_file_read_result_count"] >= 2
    assert summary["workspace_markdown_summary_result_count"] >= 1
    assert summary["workspace_read_violation_count"] >= 1
    assert summary["workspace_read_path_traversal_violation_count"] >= 1
    assert "Workspace Read Skills" in report.report_text


def test_report_includes_persona_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_persona.sqlite")
    persona = PersonaLoadingService(trace_service=TraceService(ocel_store=store))
    bundle = persona.create_default_agent_persona()
    persona.render_projection_block(bundle.projection)
    service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = service.build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["soul_identity_count"] >= 1
    assert summary["persona_profile_count"] >= 1
    assert summary["persona_instruction_artifact_count"] >= 1
    assert summary["agent_role_binding_count"] >= 1
    assert summary["persona_loadout_count"] >= 1
    assert summary["persona_projection_count"] >= 1
    assert summary["persona_capability_boundary_count"] >= 1
    assert summary["persona_projection_attached_to_prompt_count"] >= 1
    assert "Persona Projection" in report.report_text


def test_report_includes_persona_source_import_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_persona_source_import.sqlite")
    service = PersonaSourceStagedImportService(trace_service=TraceService(ocel_store=store))
    source = service.register_source_from_text(
        source_name="profile.md",
        text="identity: public dummy\nboundary: review before activation",
        source_ref="profile.md",
        media_type="text/markdown",
        private=True,
    )
    manifest = service.create_manifest(
        manifest_name="dummy",
        source_root=str(tmp_path),
        sources=[source],
    )
    candidate = service.create_ingestion_candidate(
        manifest=manifest,
        sources=[source],
        private=True,
    )
    service.validate_candidate(candidate, [source])
    draft = service.create_assimilation_draft(candidate=candidate, sources=[source])
    service.create_projection_candidate(draft=draft, candidate=candidate)
    service.record_risk_note(
        source_id=source.source_id,
        candidate_id=candidate.candidate_id,
        risk_level="low",
        risk_categories=["review"],
        message="Review before use.",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["persona_source_count"] >= 1
    assert summary["persona_source_manifest_count"] >= 1
    assert summary["persona_source_ingestion_candidate_count"] >= 1
    assert summary["persona_source_validation_result_count"] >= 1
    assert summary["persona_assimilation_draft_count"] >= 1
    assert summary["persona_projection_candidate_count"] >= 1
    assert summary["persona_source_risk_note_count"] >= 1
    assert summary["persona_source_needs_review_count"] >= 1
    assert summary["persona_candidate_pending_review_count"] >= 1
    assert summary["persona_candidate_canonical_import_enabled_count"] == 0
    assert summary["persona_source_by_type"]["markdown"] >= 1
    assert summary["persona_source_by_risk_level"]["low"] >= 1
    assert summary["persona_private_source_count"] >= 1
    assert "Source import objects" in report.report_text


def test_report_includes_personal_overlay_counts(tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    (root / "overlay").mkdir(parents=True)
    (root / "overlay" / "core.md").write_text("projection", encoding="utf-8")
    store = OCELStore(tmp_path / "pig_report_personal_overlay.sqlite")
    service = PersonalOverlayLoaderService(trace_service=TraceService(ocel_store=store))
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)
    findings = service.check_overlay_boundaries(manifest, public_repo_root=tmp_path / "public_repo")
    refs = service.register_projection_refs(manifest)
    service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        boundary_findings=findings,
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_directory_config_count"] >= 1
    assert summary["personal_directory_manifest_count"] >= 1
    assert summary["personal_projection_ref_count"] >= 1
    assert summary["personal_overlay_load_request_count"] >= 1
    assert summary["personal_overlay_load_result_count"] >= 1
    assert summary["personal_overlay_load_denied_count"] == 0
    assert summary["personal_overlay_boundary_failed_count"] == 0
    assert summary["personal_overlay_safe_projection_count"] >= 1
    assert summary["personal_projection_attached_to_prompt_count"] >= 1
    assert "Personal Directory / Overlay objects" in report.report_text


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


def test_report_includes_permission_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_permission.sqlite")
    trace_service = TraceService(ocel_store=store)
    permission_service = PermissionModelService(trace_service=trace_service)
    scope = permission_service.register_scope(
        scope_name="Tool read",
        scope_type="tool",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
    )
    request = permission_service.create_request(
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
        scope_id=scope.scope_id,
    )
    permission_service.record_decision(
        request_id=request.request_id,
        decision="ask",
        decision_mode="manual",
    )
    permission_service.record_grant(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    permission_service.record_denial(
        request_id=request.request_id,
        scope_id=scope.scope_id,
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="write",
    )
    permission_service.register_policy_note(
        scope_id=scope.scope_id,
        note_type="review_needed",
        text="Review.",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["permission_summary"]

    assert summary["permission_scope_count"] >= 1
    assert summary["permission_request_count"] >= 1
    assert summary["permission_decision_count"] >= 1
    assert summary["permission_grant_count"] >= 1
    assert summary["permission_denial_count"] >= 1
    assert summary["permission_policy_note_count"] >= 1
    assert summary["permission_request_by_type"]["tool_use"] >= 1
    assert summary["permission_request_by_operation"]["read"] >= 1
    assert summary["permission_decision_ask_count"] >= 1
    assert summary["permission_grant_active_count"] >= 1
    assert "Permission Model" in report.report_text


def test_report_includes_session_permission_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_session_permission.sqlite")
    trace_service = TraceService(ocel_store=store)
    permission_service = PermissionModelService(trace_service=trace_service)
    session_service = SessionPermissionService(permission_model_service=permission_service)
    context = session_service.create_context(session_id="session:permission-report")
    request = session_service.create_session_permission_request(
        session_id="session:permission-report",
        request_type="tool_use",
        target_type="tool_descriptor",
        target_ref="tool_descriptor:workspace",
        operation="read",
    )
    grant = session_service.attach_grant_to_session(
        session_id="session:permission-report",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation=request.operation,
    )
    denial = session_service.attach_denial_to_session(
        session_id="session:permission-report",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="write",
    )
    expired_grant = session_service.attach_grant_to_session(
        session_id="session:permission-report",
        target_type=request.target_type,
        target_ref=request.target_ref,
        operation="list",
        expires_at="2020-01-01T00:00:00Z",
    )
    expired_grant = session_service.expire_session_grants(
        session_id="session:permission-report",
        grants=[expired_grant],
        now_iso="2026-01-01T00:00:00Z",
    )[0]
    session_service.resolve_request(
        session_id="session:permission-report",
        request=request,
        grants=[grant],
        denials=[],
    )
    revoked_grant = session_service.revoke_session_grant(grant=grant)
    session_service.build_snapshot(
        session_id="session:permission-report",
        context_id=context.context_id,
        grants=[expired_grant, revoked_grant],
        denials=[denial],
        requests=[request],
        now_iso="2026-01-01T00:00:00Z",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["permission_summary"]

    assert summary["session_permission_context_count"] >= 1
    assert summary["session_permission_snapshot_count"] >= 1
    assert summary["session_permission_resolution_count"] >= 1
    assert summary["session_permission_resolution_allow_count"] >= 1
    assert summary["session_expired_grant_count"] >= 1
    assert summary["session_revoked_grant_count"] >= 1
    assert summary["session_denial_count"] >= 1
    assert summary["session_pending_permission_request_count"] >= 1
    assert "Session Permission Read-model" in report.report_text


def test_report_includes_workspace_write_sandbox_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_workspace_write_sandbox.sqlite")
    trace_service = TraceService(ocel_store=store)
    sandbox_service = WorkspaceWriteSandboxService(trace_service=trace_service)
    root = sandbox_service.register_workspace_root(root_path=str(tmp_path / "workspace"))
    protected = sandbox_service.register_write_boundary(
        workspace_root_id=root.workspace_root_id,
        boundary_type="protected_path",
        path_ref="protected",
    )
    inside = sandbox_service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "ok.txt"),
        operation="write_file",
    )
    outside = sandbox_service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "outside.txt"),
        operation="write_file",
    )
    protected_intent = sandbox_service.create_write_intent(
        workspace_root_id=root.workspace_root_id,
        target_path=str(tmp_path / "workspace" / "protected" / "secret.txt"),
        operation="write_file",
    )
    sandbox_service.evaluate_write_intent(intent=inside, workspace_root=root)
    sandbox_service.evaluate_write_intent(intent=outside, workspace_root=root)
    sandbox_service.evaluate_write_intent(intent=protected_intent, workspace_root=root, boundaries=[protected])
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["workspace_write_sandbox_summary"]

    assert summary["workspace_root_count"] >= 1
    assert summary["workspace_write_boundary_count"] >= 1
    assert summary["workspace_write_intent_count"] >= 3
    assert summary["workspace_write_sandbox_decision_count"] >= 3
    assert summary["workspace_write_sandbox_violation_count"] >= 2
    assert summary["workspace_write_allowed_count"] >= 1
    assert summary["workspace_write_denied_count"] >= 2
    assert summary["workspace_write_outside_workspace_violation_count"] >= 1
    assert summary["workspace_write_protected_path_violation_count"] >= 1
    assert "Workspace Write Sandbox" in report.report_text


def test_report_includes_delegation_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_delegation.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = DelegatedProcessRunService(trace_service=trace_service)
    packet = service.create_delegation_packet(
        goal="Report delegation counts.",
        permission_request_ids=["permission_request:report"],
        session_permission_resolution_ids=["session_permission_resolution:report"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:report"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:report"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:report"],
    )
    run = service.create_delegated_process_run(
        packet_id=packet.packet_id,
        delegation_type="analysis",
        isolation_mode="packet_only",
    )
    run = service.request_delegated_process_run(run=run)
    run = service.start_delegated_process_run(run=run)
    run = service.complete_delegated_process_run(run=run)
    service.record_delegation_result(
        delegated_run_id=run.delegated_run_id,
        packet_id=packet.packet_id,
        status="completed",
    )
    service.record_delegation_link(delegated_run_id=run.delegated_run_id)
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["delegation_summary"]

    assert summary["delegation_packet_count"] >= 1
    assert summary["delegated_process_run_count"] >= 1
    assert summary["delegation_result_count"] >= 1
    assert summary["delegation_link_count"] >= 1
    assert summary["delegated_process_created_count"] >= 1
    assert summary["delegated_process_requested_count"] >= 1
    assert summary["delegated_process_started_count"] >= 1
    assert summary["delegated_process_completed_count"] >= 1
    assert summary["delegation_by_type"]["analysis"] >= 1
    assert summary["delegation_by_isolation_mode"]["packet_only"] >= 1
    assert summary["delegation_permission_reference_count"] >= 2
    assert summary["delegation_safety_reference_count"] >= 3
    assert "Delegated Process Runs" in report.report_text


def test_report_includes_sidechain_context_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_sidechain.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(
        goal="Report sidechain counts.",
        context_summary="Summary.",
        permission_request_ids=["permission_request:sidechain"],
        session_permission_resolution_ids=["session_permission_resolution:sidechain"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:sidechain"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:sidechain"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:sidechain"],
    )
    run = delegation_service.create_delegated_process_run(
        packet_id=packet.packet_id,
        delegation_type="analysis",
        isolation_mode="packet_only",
    )
    context = sidechain_service.create_sidechain_context_from_packet(
        packet=packet,
        delegated_run=run,
        context_type="analysis",
        isolation_mode="packet_only",
    )
    entries = sidechain_service.build_entries_from_packet(context=context, packet=packet)
    context = sidechain_service.mark_context_ready(context=context, entry_ids=[entry.entry_id for entry in entries])
    context = sidechain_service.seal_context(context=context)
    sidechain_service.build_snapshot(context=context, entries=entries, summary="Snapshot.")
    sidechain_service.record_return_envelope(
        sidechain_context_id=context.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=run.delegated_run_id,
        status="completed",
        summary="Summary only.",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["sidechain_summary"]

    assert summary["sidechain_context_count"] >= 1
    assert summary["sidechain_context_entry_count"] >= 1
    assert summary["sidechain_context_snapshot_count"] >= 1
    assert summary["sidechain_return_envelope_count"] >= 1
    assert summary["sidechain_ready_count"] >= 1
    assert summary["sidechain_sealed_count"] >= 1
    assert summary["sidechain_parent_transcript_excluded_count"] >= 1
    assert summary["sidechain_permission_inheritance_prevented_count"] >= 1
    assert summary["sidechain_safety_ref_count"] >= 5
    assert summary["sidechain_context_by_type"]["analysis"] >= 1
    assert summary["sidechain_context_by_isolation_mode"]["packet_only"] >= 1
    assert "Sidechain Context" in report.report_text


def test_report_includes_delegation_conformance_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_delegation_conformance.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    conformance_service = DelegationConformanceService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(goal="Report conformance.")
    delegated_run = delegation_service.create_delegated_process_run(packet_id=packet.packet_id)
    sidechain_context = sidechain_service.create_sidechain_context_from_packet(
        packet=packet,
        delegated_run=delegated_run,
    )
    return_envelope = sidechain_service.record_return_envelope(
        sidechain_context_id=sidechain_context.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=delegated_run.delegated_run_id,
        status="completed",
    )
    contract = conformance_service.register_contract(
        contract_name="Report conformance",
        contract_type="delegation_structure",
    )
    rules = conformance_service.register_default_rules(contract_id=contract.contract_id)
    conformance_service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=packet,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["delegation_conformance_summary"]

    assert summary["delegation_conformance_contract_count"] >= 1
    assert summary["delegation_conformance_rule_count"] >= 9
    assert summary["delegation_conformance_run_count"] >= 1
    assert summary["delegation_conformance_finding_count"] >= 9
    assert summary["delegation_conformance_result_count"] >= 1
    assert summary["delegation_conformance_passed_count"] >= 1
    assert summary["delegation_conformance_by_rule_type"]["packet_exists"] >= 1
    assert summary["average_delegation_conformance_score"] == 1.0
    assert "Delegation Conformance" in report.report_text


def test_report_includes_external_capability_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_external_capability.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = ExternalCapabilityImportService(trace_service=trace_service)
    source = service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
            "entrypoint": "external.module:run",
        },
        source=source,
    )
    service.import_descriptors(
        raw_descriptors=[{"name": "external_skill", "type": "skill"}],
        source_id=source.source_id,
        batch_name="report",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["external_capability_summary"]

    assert descriptor.descriptor_id
    assert normalization.normalized_capability_type == "tool"
    assert candidate.execution_enabled is False
    assert summary["external_capability_source_count"] >= 1
    assert summary["external_capability_descriptor_count"] >= 2
    assert summary["external_capability_import_batch_count"] >= 1
    assert summary["external_capability_normalization_result_count"] >= 1
    assert summary["external_assimilation_candidate_count"] >= 1
    assert summary["external_capability_risk_note_count"] >= 1
    assert summary["external_candidate_disabled_count"] >= 1
    assert summary["external_candidate_pending_review_count"] >= 1
    assert summary["external_candidate_execution_enabled_count"] == 0
    assert summary["external_capability_by_type"]["tool"] >= 1
    assert summary["external_capability_by_risk_level"]["high"] >= 1
    assert summary["external_capability_review_required_count"] >= 1
    assert "External Capability Import" in report.report_text


def test_report_includes_external_capability_view_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_external_capability_views.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    view_service = ExternalCapabilityRegistryViewService(trace_service=trace_service, root=tmp_path)
    source = import_service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
        },
        source=source,
    )
    risk_note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=["shell_execution"],
        message="Review.",
    )
    view_service.refresh_default_external_views(
        root=tmp_path,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[risk_note],
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["external_capability_summary"]

    assert summary["external_capability_registry_snapshot_count"] >= 1
    assert summary["external_capability_registry_view_written_count"] >= 1
    assert summary["external_capability_review_view_written_count"] >= 1
    assert summary["external_capability_risk_view_written_count"] >= 1
    assert summary["external_view_disabled_candidate_count"] >= 1
    assert summary["external_view_pending_review_count"] >= 1
    assert summary["external_view_execution_enabled_candidate_count"] == 0
    assert summary["external_view_high_risk_count"] >= 1
    assert "Registry snapshots" in report.report_text


def test_report_includes_external_adapter_review_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_external_adapter_review.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    review_service = ExternalAdapterReviewService(trace_service=trace_service)
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "permissions": ["write_file"],
            "risks": ["filesystem_write"],
        },
    )
    risk_note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=normalization.normalized_risk_categories,
        message="Review.",
    )
    queue = review_service.create_review_queue(queue_name="external review")
    item = review_service.create_review_item(
        queue_id=queue.queue_id,
        candidate=candidate,
        risk_note_ids=[risk_note.risk_note_id],
    )
    checklist = review_service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[risk_note],
    )
    finding = review_service.record_finding(
        item_id=item.item_id,
        finding_type="risk",
        message="High risk.",
        severity="high",
    )
    review_service.record_decision(
        item=item,
        decision="approved_for_design",
        finding_ids=[finding.finding_id],
        checklist_id=checklist.checklist_id,
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["external_capability_summary"]

    assert summary["external_adapter_review_queue_count"] >= 1
    assert summary["external_adapter_review_item_count"] >= 1
    assert summary["external_adapter_review_checklist_count"] >= 1
    assert summary["external_adapter_review_finding_count"] >= 1
    assert summary["external_adapter_review_decision_count"] >= 1
    assert summary["external_review_pending_count"] >= 1
    assert summary["external_review_open_finding_count"] >= 1
    assert summary["external_review_high_risk_finding_count"] >= 1
    assert summary["external_review_non_activating_decision_count"] >= 1
    assert summary["external_review_runtime_activation_count"] == 0
    assert "Review queues/items/checklists/findings/decisions" in report.report_text


def test_report_includes_mcp_plugin_descriptor_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_mcp_plugin_descriptors.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = MCPPluginDescriptorSkeletonService(trace_service=trace_service)
    server = service.import_mcp_server_descriptor(
        raw_descriptor={
            "name": "sample_mcp_server",
            "transport": "stdio",
            "tools": [{"name": "read_resource"}],
            "permissions": ["read_file"],
            "risks": ["filesystem_read"],
        },
    )
    service.import_mcp_tool_descriptor(
        raw_tool_descriptor={"name": "read_resource", "risks": ["filesystem_read"]},
        mcp_server_id=server.mcp_server_id,
    )
    plugin = service.import_plugin_descriptor(
        raw_descriptor={
            "name": "sample_plugin",
            "type": "python",
            "entrypoints": [{"name": "register", "ref": "sample_plugin:register"}],
            "permissions": ["network"],
            "risks": ["network_access"],
        },
    )
    service.import_plugin_entrypoint_descriptor(
        raw_entrypoint={"name": "register", "ref": "sample_plugin:register", "type": "python_module"},
        plugin_id=plugin.plugin_id,
    )
    skeleton = service.create_skeleton_from_plugin(plugin=plugin)
    validation = service.validate_skeleton(skeleton=skeleton)
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["external_capability_summary"]

    assert validation.status == "passed"
    assert summary["mcp_server_descriptor_count"] >= 1
    assert summary["mcp_tool_descriptor_count"] >= 1
    assert summary["plugin_descriptor_count"] >= 1
    assert summary["plugin_entrypoint_descriptor_count"] >= 1
    assert summary["external_descriptor_skeleton_count"] >= 1
    assert summary["external_descriptor_skeleton_validation_count"] >= 1
    assert summary["skeleton_validation_passed_count"] >= 1
    assert summary["mcp_plugin_execution_enabled_count"] == 0
    assert summary["mcp_plugin_activation_enabled_count"] == 0
    assert summary["mcp_plugin_descriptor_by_type"]["plugin:python"] >= 1
    assert summary["mcp_plugin_risk_category_count"]["network_access"] >= 1
    assert "MCP/plugin descriptors" in report.report_text


def test_report_includes_external_ocel_import_candidate_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_external_ocel.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = ExternalOCELImportCandidateService(trace_service=trace_service)
    source = service.register_source(source_name="provided dict", trust_level="untrusted")
    descriptor, validation, preview, candidate = service.register_as_candidate(
        payload={
            "events": [
                {"id": "e1", "activity": "start", "timestamp": "2026-01-01T00:00:00Z"},
                {"id": "e2", "activity": "finish", "timestamp": "2026-01-01T00:01:00Z"},
            ],
            "objects": [{"id": "o1", "type": "case"}],
            "relations": [{"type": "event_object", "event_id": "e1", "object_id": "o1"}],
        },
        source=source,
        payload_name="external ocel report",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["external_capability_summary"]

    assert descriptor.descriptor_id
    assert validation.status == "valid"
    assert preview.event_count == 2
    assert candidate.canonical_import_enabled is False
    assert summary["external_ocel_source_count"] >= 1
    assert summary["external_ocel_payload_descriptor_count"] >= 1
    assert summary["external_ocel_import_candidate_count"] >= 1
    assert summary["external_ocel_validation_result_count"] >= 1
    assert summary["external_ocel_preview_snapshot_count"] >= 1
    assert summary["external_ocel_risk_note_count"] >= 1
    assert summary["external_ocel_valid_count"] >= 1
    assert summary["external_ocel_invalid_count"] == 0
    assert summary["external_ocel_candidate_pending_review_count"] >= 1
    assert summary["external_ocel_candidate_canonical_import_enabled_count"] == 0
    assert summary["external_ocel_candidate_not_merged_count"] >= 1
    assert summary["external_ocel_total_preview_event_count"] >= 2
    assert summary["external_ocel_total_preview_object_count"] >= 1
    assert summary["external_ocel_total_preview_relation_count"] >= 1
    assert summary["external_ocel_by_schema_status"]["ocel_like"] >= 1
    assert summary["external_ocel_by_risk_level"]["medium"] >= 1
    assert "External OCEL sources/descriptors/candidates" in report.report_text


def test_report_includes_personal_mode_loadout_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_personal_mode_loadout.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = PersonalModeLoadoutService(trace_service=trace_service)
    core = service.register_core_profile(
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity.",
        private=True,
    )
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="research_mode",
        mode_type="research_mode",
        role_statement="Analyze provided documents.",
        private=True,
    )
    boundary = service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Runtime capability profile is authoritative.",
        severity="high",
    )
    service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="privacy_boundary",
        boundary_text="Do not expose local personal directory contents.",
        severity="high",
    )
    binding = service.register_capability_binding(
        mode_profile_id=mode.mode_profile_id,
        capability_name="document_reasoning",
        capability_category="reasoning",
        availability="available_now",
        can_execute_now=True,
    )
    service.register_capability_binding(
        mode_profile_id=mode.mode_profile_id,
        capability_name="local_execution",
        capability_category="runtime",
        availability="not_implemented",
        can_execute_now=False,
        requires_permission=True,
    )
    service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
        capability_bindings=[binding],
    )
    service.create_mode_loadout_draft(
        core_profile=core,
        mode_profile=mode,
        projected_blocks=[{"kind": "role", "content": "Analyze provided documents."}],
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_core_profile_count"] >= 1
    assert summary["personal_mode_profile_count"] >= 1
    assert summary["personal_mode_boundary_count"] >= 2
    assert summary["personal_mode_capability_binding_count"] >= 2
    assert summary["personal_mode_loadout_count"] >= 1
    assert summary["personal_mode_loadout_draft_count"] >= 1
    assert summary["personal_mode_private_count"] >= 2
    assert summary["personal_mode_boundary_by_type"]["capability_boundary"] >= 1
    assert summary["personal_mode_by_type"]["research_mode"] >= 1
    assert summary["personal_mode_capability_available_now_count"] >= 1
    assert summary["personal_mode_capability_requires_permission_count"] >= 1
    assert summary["personal_mode_capability_not_implemented_count"] >= 1
    assert "Personal Core / Mode objects" in report.report_text


def test_report_includes_personal_mode_binding_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_personal_mode_binding.sqlite")
    trace_service = TraceService(ocel_store=store)
    loadout_service = PersonalModeLoadoutService(trace_service=trace_service)
    core = loadout_service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity.",
    )
    mode = loadout_service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="local_runtime_mode",
        mode_type="local_runtime_mode",
        role_statement="Use explicitly bound runtime context.",
    )
    loadout = loadout_service.create_mode_loadout(core_profile=core, mode_profile=mode)
    binding_service = PersonalModeBindingService(trace_service=trace_service)
    selection = binding_service.select_mode(mode_profile=mode, loadout=loadout)
    runtime_binding = binding_service.bind_runtime(
        selection=selection,
        runtime_kind="local_runtime",
    )
    binding_service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="workspace_read",
        capability_category="workspace",
        availability="available_now",
        can_execute_now=True,
    )
    binding_service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="network_access",
        capability_category="network",
        availability="not_implemented",
        can_execute_now=False,
        requires_permission=True,
    )
    request = binding_service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        loadout_id=loadout.loadout_id,
        runtime_kind="local_runtime",
    )
    binding_service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="local_runtime",
    )
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))

    report = report_service.build_recent_report(limit=200)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_mode_selection_count"] >= 1
    assert summary["personal_runtime_binding_count"] >= 1
    assert summary["personal_runtime_capability_binding_count"] >= 2
    assert summary["personal_mode_activation_request_count"] >= 1
    assert summary["personal_mode_activation_result_count"] >= 1
    assert summary["personal_mode_prompt_context_activation_count"] >= 1
    assert summary["personal_runtime_binding_by_kind"]["local_runtime"] >= 1
    assert summary["personal_context_ingress_by_type"]["local_runtime_context"] >= 1
    assert summary["personal_runtime_capability_available_now_count"] >= 1
    assert summary["personal_runtime_capability_requires_permission_count"] >= 1
    assert summary["personal_runtime_capability_not_implemented_count"] >= 1
    assert "Personal Mode Binding objects" in report.report_text


def test_report_includes_personal_conformance_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_personal_conformance.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = PersonalConformanceService(trace_service=trace_service)
    contract, _ = service.register_default_rules()
    run = service.start_run(contract_id=contract.contract_id, target_kind="manual")
    finding = service.record_finding(
        run_id=run.run_id,
        rule_type="canonical_import_disabled",
        status="passed",
        message="Dummy conformance check passed.",
    )
    service.record_result(
        run_id=run.run_id,
        contract_id=contract.contract_id,
        findings=[finding],
    )

    report = PIGReportService(ocpx_loader=OCPXLoader(store=store)).build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_conformance_contract_count"] >= 1
    assert summary["personal_conformance_rule_count"] >= 18
    assert summary["personal_conformance_run_count"] >= 1
    assert summary["personal_conformance_finding_count"] >= 1
    assert summary["personal_conformance_result_count"] >= 1
    assert summary["personal_conformance_passed_count"] >= 1
    assert summary["personal_conformance_by_rule_type"]["canonical_import_disabled"] >= 1
    assert "Personal Conformance objects" in report.report_text


def test_report_includes_personal_smoke_test_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_report_personal_smoke_test.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = PersonalRuntimeSmokeTestService(trace_service=trace_service)
    scenario = service.create_scenario(
        scenario_name="sample_personal_assistant_smoke",
        scenario_type="mode_self_report",
    )
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="mode_self_report",
        input_prompt="Who are you?",
        expected_behavior="Report current mode.",
        required_claims=["research_mode"],
        expected_mode="research_mode",
    )
    service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "research_mode"},
        observed_mode="research_mode",
    )

    report = PIGReportService(ocpx_loader=OCPXLoader(store=store)).build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_smoke_test_scenario_count"] >= 1
    assert summary["personal_smoke_test_case_count"] >= 1
    assert summary["personal_smoke_test_run_count"] >= 1
    assert summary["personal_smoke_test_observation_count"] >= 1
    assert summary["personal_smoke_test_assertion_count"] >= 1
    assert summary["personal_smoke_test_result_count"] >= 1
    assert summary["personal_smoke_test_passed_count"] >= 1
    assert summary["personal_smoke_test_by_scenario_type"]["mode_self_report"] >= 1
    assert "Personal Smoke Test objects" in report.report_text






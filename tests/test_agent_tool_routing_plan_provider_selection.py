from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_TOOL_ROUTING_EFFECT_TYPES,
    AGENT_TOOL_ROUTING_EVENT_TYPES,
    AGENT_TOOL_ROUTING_OBJECT_TYPES,
    AGENT_TOOL_ROUTING_RELATION_TYPES,
    AGENT_TOOL_ROUTING_VERSION,
    AgentIntentClassificationReportService,
    AgentProviderCapabilityCatalogService,
    AgentProviderCapabilityCatalogView,
    AgentProviderCapabilityRef,
    AgentProviderSelection,
    AgentProviderSelectionCandidate,
    AgentRouteIntentMapping,
    AgentRoutePrecondition,
    AgentRouteRiskReview,
    AgentSafetyGateReportService,
    AgentToolRouteDependency,
    AgentToolRoutePlan,
    AgentToolRouteStep,
    AgentToolRoutingPolicyService,
    AgentToolRoutingReportService,
    AgentToolRoutingRequest,
)
from chanta_core.agent_surface.tool_routing import (
    AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP,
    AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP,
    AgentRouteIntentMappingService,
)
from chanta_core.cli.main import main


def _service() -> AgentToolRoutingReportService:
    return AgentToolRoutingReportService()


def test_tool_routing_policy_builds_with_v0254_boundaries() -> None:
    policy = AgentToolRoutingPolicyService().build_policy()

    assert policy.version == AGENT_TOOL_ROUTING_VERSION
    assert policy.layer == "agent_surface"
    assert policy.deterministic_default is True
    assert policy.external_llm_routing_enabled is False
    assert policy.llm_routing_judge_enabled is False
    assert policy.require_safety_gate_allow_route is True
    assert policy.create_route_plan_enabled is True
    assert policy.provider_selection_enabled is True
    assert policy.route_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.provider_execution_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.response_assembly_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_provider_adapter_enabled is False
    assert policy.external_agent_adapter_enabled is False
    assert policy.respect_v024_provider_boundaries is True
    assert policy.respect_v024_local_runtime_gate is True
    assert policy.read_only_before_execution is True
    assert policy.search_before_file_read is True
    assert policy.command_candidate_before_safety is True
    assert policy.safety_before_execution is True
    assert policy.execution_before_output_explanation is True
    assert policy.evidence_refs_required is True


def test_tool_routing_models_build() -> None:
    request = AgentToolRoutingRequest(request_id="routing-request:test", sanitized_request_text="Explain")
    provider_ref = AgentProviderCapabilityRef(
        capability_ref_id="provider-ref:test",
        provider_id="internal_provider:workspace",
        provider_type="workspace_read_provider",
        capability_id="workspace_tree",
        capability_name="Workspace Tree",
        source_version="v0.24.9",
        read_only=True,
        bounded_execution_capable=False,
        requires_safety_gate=True,
        requires_v024_gate=False,
        allowed_for_route_plan=True,
    )
    catalog = AgentProviderCapabilityCatalogView(
        catalog_view_id="catalog:test",
        provider_capabilities=[provider_ref],
        provider_count=1,
        capability_count=1,
    )
    mapping = AgentRouteIntentMapping(
        mapping_id="mapping:test",
        intent_category="workspace_overview",
        recommended_route_kind="workspace_read",
        required_provider_types=["workspace_read_provider"],
        optional_provider_types=[],
        route_constraints=["read_only_before_execution"],
        next_stage=AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP,
    )
    candidate = AgentProviderSelectionCandidate(
        selection_candidate_id="selection-candidate:test",
        provider_ref=provider_ref,
        route_kind="workspace_read",
        reason="required",
        priority=1,
        required=True,
        preconditions=["gate_allow_route"],
        expected_output_ref_type="workspace_snapshot_ref",
        risk_notes=[],
        selected=True,
    )
    selection = AgentProviderSelection(
        selection_id="selection:test",
        selected_candidates=[candidate],
        provider_count=1,
        required_provider_count=1,
    )
    precondition = AgentRoutePrecondition(
        precondition_id="precondition:test",
        precondition_type="gate_allow_route",
        description="gate must allow route",
        required=True,
        satisfied_now=True,
        required_future_stage=None,
    )
    step = AgentToolRouteStep(
        route_step_id="route-step:test",
        step_index=1,
        step_name="Workspace Tree",
        route_kind="workspace_read",
        provider_id=provider_ref.provider_id,
        provider_type=provider_ref.provider_type,
        capability_id=provider_ref.capability_id,
        planned_action="Plan only",
        expected_input_refs=[],
        expected_output_ref_type="workspace_snapshot_ref",
        preconditions=[precondition],
        route_step_status="planned",
    )
    dependency = AgentToolRouteDependency(
        dependency_id="dependency:test",
        upstream_step_id=step.route_step_id,
        downstream_step_id="next",
        dependency_type="output_to_input",
        required=True,
    )
    risk = AgentRouteRiskReview(
        risk_review_id="risk:test",
        route_kind="workspace_read",
        risk_level="medium",
        risk_categories=["provider_boundary"],
        requires_v0255_invocation_boundary=True,
        rationale="planning only",
    )
    plan = AgentToolRoutePlan(
        route_plan_id="route-plan:test",
        safety_gate_report_id="safety:test",
        primary_intent_category="workspace_overview",
        route_kind="workspace_read",
        provider_selection=selection,
        route_steps=[step],
        route_dependencies=[dependency],
        risk_review=risk,
        route_plan_status="planned",
        provider_invocation_required=True,
    )

    assert request.version == "v0.25.4"
    assert catalog.external_provider_adapter_count == 0
    assert mapping.recommended_route_kind == "workspace_read"
    assert selection.provider_invoked is False
    assert step.executes_now is False
    assert dependency.required is True
    assert risk.requires_v0255_invocation_boundary is True
    assert plan.provider_invocation_allowed_now is False


def test_v0253_safety_gate_report_can_be_loaded() -> None:
    safety = AgentSafetyGateReportService().build_report("Explain the project structure")
    report = _service().build_report("Explain the project structure", safety_gate_report=safety)

    assert report.request.safety_gate_report_id == safety.report_id
    assert report.safety_gate_was_allow_route is True


def test_routing_requires_allow_route_for_provider_backed_plan() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.safety_gate_was_allow_route is True
    assert report.route_plan.route_kind == "workspace_read"
    assert report.route_plan.route_plan_status == "planned"
    assert report.ready_for_v0_25_5 is True
    assert report.ready_for_v0_25_6 is False


def test_non_allow_route_creates_no_route_due_to_gate() -> None:
    report = _service().build_report("Do nothing and stop here")

    assert report.safety_gate_was_allow_route is False
    assert report.route_plan.route_plan_status == "no_route_due_to_gate"
    assert report.route_plan.provider_invocation_required is False
    assert report.route_plan.provider_selection.provider_count == 0
    assert all(step.provider_id is None for step in report.route_plan.route_steps)
    assert report.ready_for_v0_25_6 is True


def test_provider_capability_catalog_views_v024_providers() -> None:
    catalog = AgentProviderCapabilityCatalogService().build_catalog_view()
    provider_types = {ref.provider_type for ref in catalog.provider_capabilities}

    assert "workspace_read_provider" in provider_types
    assert "repository_search_provider" in provider_types
    assert "file_read_provider" in provider_types
    assert "ocel_inspection_provider" in provider_types
    assert "pig_inspection_provider" in provider_types
    assert "ocpx_projection_provider" in provider_types
    assert "local_runtime_provider" in provider_types
    assert catalog.external_provider_adapter_count == 0
    assert all(ref.invocation_enabled_in_v025_4 is False for ref in catalog.provider_capabilities)
    assert all(ref.executable_in_v025_4 is False for ref in catalog.provider_capabilities)
    assert all(ref.allowed_for_route_plan is True for ref in catalog.provider_capabilities)
    assert next(ref for ref in catalog.provider_capabilities if ref.provider_type == "local_runtime_provider").requires_v024_gate is True


def test_route_mapping_coverage() -> None:
    mappings = AgentRouteIntentMappingService().build_route_mappings()
    route_by_intent = {mapping.intent_category: mapping.recommended_route_kind for mapping in mappings}

    assert route_by_intent["general_answer"] == "response_only"
    assert route_by_intent["workspace_overview"] == "workspace_read"
    assert route_by_intent["repository_search"] == "repository_search"
    assert route_by_intent["file_read"] == "file_read"
    assert route_by_intent["process_state_inspection"] == "process_state_inspection"
    assert route_by_intent["local_runtime_candidate"] == "local_runtime_candidate"
    assert route_by_intent["local_runtime_execution_request"] == "local_runtime_execution_flow"
    assert route_by_intent["diagnostic_request"] == "diagnostic_flow"
    assert route_by_intent["implementation_prompt_request"] == "prompt_generation_flow"
    assert route_by_intent["verification_prompt_request"] == "verification_flow"
    assert route_by_intent["checklist_request"] == "checklist_flow"
    assert route_by_intent["consolidation_request"] == "consolidation_flow"
    assert route_by_intent["no_action_candidate"] == "no_route"
    assert route_by_intent["needs_more_input_candidate"] == "no_route"
    assert route_by_intent["blocked_candidate"] == "no_route"


def test_provider_selection_created_with_selected_and_rejected_candidates() -> None:
    report = _service().build_report("Process state inspection report")
    selection = report.route_plan.provider_selection

    assert selection.selection_status in {"selected", "warning"}
    assert selection.provider_invoked is False
    assert selection.route_executed is False
    assert selection.selected_candidates
    assert selection.rejected_candidates
    assert all(candidate.selected for candidate in selection.selected_candidates)
    assert all(not candidate.selected for candidate in selection.rejected_candidates)


def test_response_only_route_can_have_zero_providers() -> None:
    safety = AgentSafetyGateReportService().build_report("Explain the project structure")
    intent = AgentIntentClassificationReportService().build_report("What is 2 plus 2?")
    report = _service().build_report("What is 2 plus 2?", safety_gate_report=safety, intent_report=intent)

    assert report.route_plan.route_kind == "response_only"
    assert report.route_plan.provider_selection.provider_count == 0
    assert report.route_plan.route_plan_status == "response_only"
    assert report.ready_for_v0_25_6 is True


def test_repository_and_file_routes_are_planned_without_provider_calls() -> None:
    repo_report = _service().build_report("Search repository for provider")
    file_report = _service().build_report("Read src/chanta_core/__init__.py")

    assert repo_report.route_plan.route_kind == "repository_search"
    assert repo_report.route_plan.provider_invoked is False
    assert file_report.route_plan.route_kind == "file_read"
    dependency_types = {dependency.dependency_type for dependency in file_report.route_plan.route_dependencies}
    assert "search_before_file_read" in dependency_types
    assert all(step.executes_now is False for step in file_report.route_plan.route_steps)
    assert all(step.provider_invoked_now is False for step in file_report.route_plan.route_steps)


def test_local_runtime_execution_route_preserves_v024_gate_sequence() -> None:
    report = _service().build_report("Run pytest for this project")
    route_plan = report.route_plan

    assert route_plan.route_kind == "local_runtime_execution_flow"
    assert route_plan.risk_review.requires_v024_gate is True
    assert route_plan.local_runtime_execution_allowed_now is False
    dependency_types = {dependency.dependency_type for dependency in route_plan.route_dependencies}
    assert "candidate_before_safety" in dependency_types
    assert "safety_before_execution" in dependency_types
    assert "execution_before_explanation" in dependency_types
    assert any(pre.required_future_stage and pre.required_future_stage.startswith("v0.24") for step in route_plan.route_steps for pre in step.preconditions)


def test_route_risk_review_and_route_plan_flags() -> None:
    report = _service().build_report("Explain the project structure")
    route_plan = report.route_plan

    assert route_plan.risk_review is not None
    assert route_plan.risk_review.risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert route_plan.risk_review.requires_v0255_invocation_boundary is True
    assert route_plan.expected_next_stage == AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP
    assert route_plan.provider_invocation_required is True
    assert route_plan.provider_invocation_allowed_now is False
    assert route_plan.route_execution_allowed_now is False
    assert route_plan.local_runtime_execution_allowed_now is False
    assert route_plan.tool_route_created is True
    assert route_plan.tool_route_executed is False
    assert route_plan.provider_invoked is False
    assert route_plan.local_command_executed is False


def test_report_flags_remain_route_plan_only() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.ready_for_v0_26 is False
    assert report.tool_route_plan_created is True
    assert report.provider_selection_created is True
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.response_assembled is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_pig_and_ocpx_reports_cover_v0254() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.25.4"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "tool_routing_plan_provider_selection"
    assert "tool route plan is not provider invocation" in pig["principles"]
    assert pig["safety_boundary"]["tool_route_plan_created"] == "conditional"
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["response_assembled"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_tool_route_plan_created"
    assert "AgentToolRoutingState" in ocpx["target_read_models"]
    assert "AgentToolRoutePlanState" in ocpx["target_read_models"]


def test_ocel_mapping_constants_exist() -> None:
    assert "agent_tool_routing_policy" in AGENT_TOOL_ROUTING_OBJECT_TYPES
    assert "agent_tool_route_plan" in AGENT_TOOL_ROUTING_OBJECT_TYPES
    assert "agent_tool_routing_requested" in AGENT_TOOL_ROUTING_EVENT_TYPES
    assert "agent_provider_selection_created" in AGENT_TOOL_ROUTING_EVENT_TYPES
    assert "creates_tool_route_plan" in AGENT_TOOL_ROUTING_RELATION_TYPES
    assert "defers_provider_invocation_to_v0_25_5" in AGENT_TOOL_ROUTING_RELATION_TYPES
    assert "agent_tool_route_plan_created" in AGENT_TOOL_ROUTING_EFFECT_TYPES
    assert "agent_provider_selection_created" in AGENT_TOOL_ROUTING_EFFECT_TYPES


def test_cli_route_commands_work(capsys) -> None:
    assert main(["agent", "route", "plan", "--text", "Explain the project structure"]) == 0
    assert "version=v0.25.4" in capsys.readouterr().out

    assert main(["agent", "route", "providers"]) == 0
    assert "workspace_read_provider" in capsys.readouterr().out

    assert main(["agent", "route", "mappings"]) == 0
    assert "workspace_overview->workspace_read" in capsys.readouterr().out

    assert main(["agent", "route", "report", "--report-id", "demo"]) == 0
    assert "tool_route_plan_created=true" in capsys.readouterr().out

    assert main(["agent", "route", "findings", "--report-id", "demo"]) == 0
    assert "provider_invocation_deferred" in capsys.readouterr().out

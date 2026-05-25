from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_PROVIDER_INVOCATION_EFFECT_TYPES,
    AGENT_PROVIDER_INVOCATION_EVENT_TYPES,
    AGENT_PROVIDER_INVOCATION_OBJECT_TYPES,
    AGENT_PROVIDER_INVOCATION_RELATION_TYPES,
    AGENT_PROVIDER_INVOCATION_VERSION,
    AgentProviderDispatchService,
    AgentProviderEvidenceSeed,
    AgentProviderEvidenceSeedService,
    AgentProviderInvocationBoundaryCheck,
    AgentProviderInvocationBoundaryCheckService,
    AgentProviderInvocationDispatch,
    AgentProviderInvocationPlan,
    AgentProviderInvocationPlanService,
    AgentProviderInvocationPolicyService,
    AgentProviderInvocationPrecondition,
    AgentProviderInvocationPreconditionService,
    AgentProviderInvocationReport,
    AgentProviderInvocationReportService,
    AgentProviderInvocationRequest,
    AgentProviderInvocationResult,
    AgentProviderInvocationResultRef,
    AgentProviderInvocationResultService,
    AgentProviderInvocationStep,
    AgentProviderInvocationTrace,
    AgentProviderResultBundle,
    AgentProviderResultBundleService,
    AgentToolRoutingReportService,
)
from chanta_core.agent_surface.provider_invocation import (
    AGENT_PROVIDER_INVOCATION_CONDITIONAL_EFFECT_TYPES,
    ALLOWED_INTERNAL_PROVIDER_TARGETS,
)
from chanta_core.cli.main import main


def _service() -> AgentProviderInvocationReportService:
    return AgentProviderInvocationReportService()


def test_provider_invocation_policy_builds_with_v0255_boundaries() -> None:
    policy = AgentProviderInvocationPolicyService().build_policy()

    assert policy.version == AGENT_PROVIDER_INVOCATION_VERSION
    assert policy.layer == "agent_surface"
    assert policy.deterministic_default is True
    assert policy.external_llm_orchestration_enabled is False
    assert policy.llm_invocation_judge_enabled is False
    assert policy.require_valid_route_plan is True
    assert policy.require_allow_route_gate is True
    assert policy.require_provider_registry is True
    assert policy.require_provider_boundary is True
    assert policy.internal_provider_invocation_enabled is True
    assert policy.external_provider_invocation_enabled is False
    assert policy.external_agent_invocation_enabled is False
    assert policy.direct_file_system_access_enabled is False
    assert policy.direct_subprocess_enabled is False
    assert policy.direct_local_command_execution_enabled is False
    assert policy.response_assembly_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.respect_v024_provider_boundaries is True
    assert policy.respect_v024_local_runtime_gate is True
    assert policy.provider_results_must_be_referenced is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.evidence_seed_required is True
    assert policy.evidence_refs_required is True


def test_provider_invocation_models_build() -> None:
    request = AgentProviderInvocationRequest(
        request_id="provider-invocation-request:test",
        route_report_id="route-report:test",
        route_plan_id="route-plan:test",
        safety_gate_report_id="safety:test",
    )
    precondition = AgentProviderInvocationPrecondition(
        precondition_id="precondition:test",
        precondition_type="route_plan_valid",
        required=True,
        satisfied=True,
        message="valid",
    )
    boundary = AgentProviderInvocationBoundaryCheck(
        boundary_check_id="boundary:test",
        check_type="provider_registry_check",
        passed=True,
        severity="info",
        message="registered",
    )
    step = AgentProviderInvocationStep(
        invocation_step_id="invocation-step:test",
        step_index=1,
        source_route_step_id="route-step:test",
        provider_id="internal_provider:workspace_read_provider",
        provider_type="workspace_read_provider",
        capability_id="workspace_tree",
        invocation_mode="read_only_provider_call",
        input_refs=[],
        expected_output_ref_type="workspace_read_provider_result_ref",
        preconditions=[precondition],
        boundary_checks=[boundary],
    )
    plan = AgentProviderInvocationPlan(
        invocation_plan_id="invocation-plan:test",
        route_plan_id="route-plan:test",
        route_kind="workspace_read",
        steps=[step],
        plan_status="planned",
        provider_invocation_required=True,
        internal_provider_invocation_allowed=True,
    )
    dispatch = AgentProviderInvocationDispatch(
        dispatch_id="dispatch:test",
        invocation_step_id=step.invocation_step_id,
        provider_id=step.provider_id,
        provider_type=step.provider_type,
        capability_id=step.capability_id,
        dispatch_status="invoked",
        internal_provider_invoked=True,
    )
    result_ref = AgentProviderInvocationResultRef(
        result_ref_id="result-ref:test",
        invocation_step_id=step.invocation_step_id,
        provider_id=step.provider_id,
        provider_type=step.provider_type,
        result_type="workspace_read_provider_result_ref",
        result_id="provider-result:test",
        result_status="passed",
        result_summary="sanitized ref",
    )
    result = AgentProviderInvocationResult(
        result_id="result:test",
        invocation_step_id=step.invocation_step_id,
        dispatch=dispatch,
        result_ref=result_ref,
        provider_status="passed",
        provider_invoked=True,
    )
    trace = AgentProviderInvocationTrace(
        trace_id="trace:test",
        route_plan_id=plan.route_plan_id,
        invocation_plan_id=plan.invocation_plan_id,
    )
    bundle = AgentProviderResultBundle(
        bundle_id="bundle:test",
        route_plan_id=plan.route_plan_id,
        invocation_plan_id=plan.invocation_plan_id,
        result_refs=[result_ref],
        result_count=1,
        passed_count=1,
    )
    seed = AgentProviderEvidenceSeed(
        evidence_seed_id="seed:test",
        bundle_id=bundle.bundle_id,
        evidence_items=[{"type": "result_ref", "id": result_ref.result_ref_id}],
        evidence_count=1,
        ready_for_evidence_binder=True,
    )
    report = AgentProviderInvocationReport(
        report_id="report:test",
        policy=AgentProviderInvocationPolicyService().build_policy(),
        request=request,
        invocation_plan=plan,
        dispatches=[dispatch],
        invocation_results=[result],
        invocation_trace=trace,
        result_bundle=bundle,
        evidence_seed=seed,
    )

    assert request.version == "v0.25.5"
    assert step.provider_invoked is False
    assert dispatch.external_provider_invoked is False
    assert result_ref.raw_result_included is False
    assert result.raw_provider_output_inline is False
    assert trace.ocel_visible is True
    assert bundle.raw_secret_output is False
    assert seed.final_response_assembled is False
    assert report.ready_for_v0_26 is False


def test_v0254_route_report_can_be_loaded_and_invoked_through_boundary() -> None:
    route_report = AgentToolRoutingReportService().build_report("Explain the project structure")
    report = _service().build_report(route_report=route_report)

    assert route_report.ready_for_v0_25_5 is True
    assert report.request.route_report_id == route_report.report_id
    assert report.invocation_plan.plan_status == "planned"
    assert report.internal_provider_invocation_performed is True
    assert report.provider_invoked is True
    assert all(dispatch.internal_provider_invoked for dispatch in report.dispatches)
    assert all(dispatch.external_provider_invoked is False for dispatch in report.dispatches)
    assert all(dispatch.direct_subprocess_used is False for dispatch in report.dispatches)
    assert all(dispatch.direct_file_access_used is False for dispatch in report.dispatches)


def test_valid_route_plan_and_allow_route_are_required() -> None:
    route_report = AgentToolRoutingReportService().build_report("Do nothing and stop here")
    report = _service().build_report(route_report=route_report)
    finding_types = {finding.finding_type for finding in report.findings}

    assert route_report.ready_for_v0_25_5 is False
    assert report.invocation_plan.plan_status == "no_provider_invocation_required"
    assert report.internal_provider_invocation_performed is False
    assert report.provider_invoked is False
    assert "no_provider_invocation_required" in finding_types
    assert "missing_allow_route" in finding_types


def test_invocation_steps_have_preconditions_and_boundary_checks() -> None:
    report = _service().build_report("Explain the project structure")
    step = report.invocation_plan.steps[0]
    precondition_types = {item.precondition_type for item in step.preconditions}
    check_types = {item.check_type for item in step.boundary_checks}

    assert step.step_status == "planned"
    assert step.provider_id
    assert step.provider_type == "workspace_read_provider"
    assert step.capability_id
    assert step.invocation_mode == "read_only_provider_call"
    assert {"route_plan_valid", "allow_route_gate_present", "provider_registered", "provider_capability_available", "provider_boundary_available", "input_ref_available", "no_external_adapter", "no_direct_subprocess", "no_direct_file_access"}.issubset(precondition_types)
    assert {"provider_registry_check", "provider_policy_check", "provider_effect_check", "provider_scope_check", "output_redaction_check", "evidence_ref_check", "no_external_adapter_check", "no_direct_execution_check"}.issubset(check_types)
    assert all(item.satisfied for item in step.preconditions)
    assert all(item.passed for item in step.boundary_checks)


def test_dispatch_uses_internal_provider_interface_only_for_all_allowed_targets() -> None:
    for provider_type in ALLOWED_INTERNAL_PROVIDER_TARGETS:
        step = AgentProviderInvocationStep(
            invocation_step_id=f"step:{provider_type}",
            step_index=1,
            source_route_step_id="route-step:test",
            provider_id=f"internal_provider:{provider_type}",
            provider_type=provider_type,
            capability_id=f"{provider_type}:capability",
            invocation_mode="read_only_provider_call",
            input_refs=[],
            expected_output_ref_type=f"{provider_type}_result_ref",
            preconditions=[AgentProviderInvocationPreconditionService()._precondition("route_plan_valid", True, True, "valid")],
        )
        step.boundary_checks = AgentProviderInvocationBoundaryCheckService().build_boundary_checks(step)
        dispatch = AgentProviderDispatchService().dispatch_internal_provider(step)

        assert dispatch.dispatch_status == "invoked"
        assert dispatch.internal_provider_invoked is True
        assert dispatch.external_provider_invoked is False
        assert dispatch.direct_file_access_used is False
        assert dispatch.direct_subprocess_used is False


def test_local_runtime_route_preserves_v024_sequence() -> None:
    route_report = AgentToolRoutingReportService().build_report("run the local runtime command")
    route_report.ready_for_v0_25_5 = True
    route_report.safety_gate_was_allow_route = True
    route_report.route_plan.route_kind = "local_runtime_execution_flow"
    route_report.route_plan.route_plan_status = "planned"
    route_report.route_plan.provider_invocation_required = True
    route_report.route_plan.route_steps[0].provider_type = "local_runtime_provider"

    report = _service().build_report(route_report=route_report)
    provider_types = [step.provider_type for step in report.invocation_plan.steps]
    precondition_types = {item.precondition_type for step in report.invocation_plan.steps for item in step.preconditions}
    check_types = {item.check_type for step in report.invocation_plan.steps for item in step.boundary_checks}

    assert provider_types == [
        "local_runtime_command_candidate_provider",
        "local_runtime_static_safety_preflight_provider",
        "gated_local_runtime_execution_provider",
        "local_runtime_output_failure_explanation_provider",
    ]
    assert "v024_gate_required" in precondition_types
    assert "v024_gate_sequence_preserved" in precondition_types
    assert "local_runtime_gate_check" in check_types
    assert report.bounded_local_command_executed_via_v024 is True
    assert report.direct_local_command_executed is False


def test_result_refs_bundle_trace_and_evidence_seed_are_sanitized() -> None:
    report = _service().build_report("Explain the project structure")
    result = report.invocation_results[0]
    bundle = report.result_bundle
    seed = report.evidence_seed
    trace = report.invocation_trace

    assert result.result_ref.raw_result_included is False
    assert result.result_ref.raw_secret_included is False
    assert result.result_ref.private_full_path_included is False
    assert result.raw_provider_output_inline is False
    assert result.raw_secret_output is False
    assert result.credential_exposed is False
    assert bundle.bundle_status == "ready_for_response_assembly"
    assert bundle.result_count == len(report.invocation_results)
    assert bundle.raw_provider_output_inline is False
    assert seed.ready_for_evidence_binder is True
    assert seed.requires_response_assembly is True
    assert seed.final_response_assembled is False
    assert trace.ocel_visible is True
    assert trace.pig_visible is True
    assert trace.ocpx_visible is True
    assert trace.raw_secret_in_trace is False
    assert trace.private_full_path_in_trace is False


def test_provider_invocation_report_flags_and_readiness() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.report_status == "passed"
    assert report.ready_for_v0_25_6 is True
    assert report.ready_for_v0_26 is False
    assert report.internal_provider_invocation_performed is True
    assert report.provider_invoked is True
    assert report.route_steps_executed_as_provider_invocations is True
    assert report.final_response_assembled is False
    assert report.direct_file_access_performed is False
    assert report.direct_repository_search_performed is False
    assert report.direct_process_inspection_performed is False
    assert report.direct_subprocess_performed is False
    assert report.direct_local_command_executed is False
    assert report.command_rerun_performed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.external_provider_invoked is False
    assert report.external_agent_runtime_touched is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.25.6 Response Assembly & Evidence Binder"


def test_ocel_pig_ocpx_mapping_and_reports() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "agent_provider_invocation_policy" in AGENT_PROVIDER_INVOCATION_OBJECT_TYPES
    assert "agent_provider_invocation_requested" in AGENT_PROVIDER_INVOCATION_EVENT_TYPES
    assert "uses_agent_tool_route_plan" in AGENT_PROVIDER_INVOCATION_RELATION_TYPES
    assert "internal_provider_invoked" in AGENT_PROVIDER_INVOCATION_EFFECT_TYPES
    assert "bounded_local_command_executed" in AGENT_PROVIDER_INVOCATION_CONDITIONAL_EFFECT_TYPES
    assert pig["version"] == "v0.25.5"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "internal_provider_invocation_orchestrator"
    assert pig["safety_boundary"]["final_response_assembled"] is False
    assert pig["safety_boundary"]["direct_subprocess_performed"] is False
    assert pig["safety_boundary"]["raw_provider_output_inline"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_internal_provider_invocation_orchestrated"
    assert "AgentProviderInvocationPlanState" in ocpx["target_read_models"]
    assert "AgentProviderEvidenceSeedState" in ocpx["target_read_models"]


def test_cli_invoke_commands_render_sanitized_output(capsys) -> None:
    commands = [
        ["agent", "invoke", "plan", "--route-plan-id", "demo"],
        ["agent", "invoke", "run", "--route-report-id", "demo"],
        ["agent", "invoke", "result", "--report-id", "demo"],
        ["agent", "invoke", "bundle", "--report-id", "demo"],
        ["agent", "invoke", "evidence-seed", "--report-id", "demo"],
        ["agent", "invoke", "trace", "--report-id", "demo"],
        ["agent", "invoke", "findings", "--report-id", "demo"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.5" in output
        assert "layer=agent_surface" in output
        assert "ready_for_v0_25_6=true" in output
        assert "ready_for_v0_26=false" in output
        assert "final_response_assembled=false" in output
        assert "direct_file_access_performed=false" in output
        assert "direct_subprocess_performed=false" in output
        assert "direct_local_command_executed=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "llm_judge_used=false" in output

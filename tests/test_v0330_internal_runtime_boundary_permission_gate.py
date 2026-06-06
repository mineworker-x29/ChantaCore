import pytest

from chanta_core.agent_runtime import (
    InternalRuntimeActionKind,
    InternalRuntimeAllowedSurface,
    InternalRuntimeBoundary,
    InternalRuntimeBoundaryStatus,
    InternalRuntimeCapabilityFlagSet,
    InternalRuntimeCapabilityKind,
    InternalRuntimeGateEvaluation,
    InternalRuntimeNoExternalSideEffectGuarantee,
    InternalRuntimePermissionDecision,
    InternalRuntimePermissionDecisionKind,
    InternalRuntimeReadinessLevel,
    InternalRuntimeReferenceCorpusBoundary,
    InternalRuntimeReferenceCorpusPosture,
    InternalRuntimeRiskSurfaceKind,
    InternalRuntimeSurfaceKind,
    InternalRuntimeTrackKind,
    V0330ReadinessReport,
    V033RoadmapOverview,
    build_internal_runtime_allowed_surface,
    build_internal_runtime_boundary,
    build_internal_runtime_capability_flags,
    build_internal_runtime_denied_action,
    build_internal_runtime_gate_evaluation,
    build_internal_runtime_no_external_side_effect_guarantee,
    build_internal_runtime_permission_decision,
    build_internal_runtime_permission_request,
    build_internal_runtime_prohibited_surface,
    build_internal_runtime_reference_corpus_boundary,
    build_v0330_readiness_report,
    build_v033_roadmap_overview,
    internal_runtime_boundary_is_not_execution,
    internal_runtime_flags_preserve_runtime_false,
    permission_decision_preserves_no_execution,
    reference_corpus_boundary_preserves_no_reference_execution,
    v0330_readiness_report_is_not_runtime_ready,
)
from chanta_core.agent_runtime.boundary import (
    DEFAULT_PROHIBITED_FILE_PATTERNS,
    DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS,
    DEFAULT_V033_STAGES,
    RUNTIME_FLAG_NAMES,
)


def test_internal_runtime_taxonomies_and_capability_flags_are_boundary_only():
    assert {item.value for item in InternalRuntimeTrackKind} == {
        "boundary_permission_gate",
        "agent_profile_runtime",
        "prompt_assembly_pipeline",
        "session_runtime_turn_state_machine",
        "safe_readonly_tool_registry",
        "safe_workspace_inspection",
        "agent_step_runner",
        "runtime_ocel_trace_emitter",
        "cli_agent_run_surface",
        "consolidation",
        "unknown",
    }
    assert "permission_gate" in {item.value for item in InternalRuntimeSurfaceKind}
    assert "shell_command" in {item.value for item in InternalRuntimeSurfaceKind}
    assert "evaluate_permission" in {item.value for item in InternalRuntimeCapabilityKind}
    assert "inspect_workspace_readonly" in {item.value for item in InternalRuntimeCapabilityKind}
    assert "run_shell_command" in {item.value for item in InternalRuntimeCapabilityKind}
    assert {item.value for item in InternalRuntimeActionKind} == {
        "allow_design_stage_handoff",
        "allow_internal_boundary_definition",
        "deny",
        "block",
        "no_op",
        "defer",
        "ask_user",
        "require_review",
        "future_gate",
        "unknown",
    }
    assert "provider_invocation" in {item.value for item in InternalRuntimeRiskSurfaceKind}
    assert "allowed_design_stage_only" in {item.value for item in InternalRuntimePermissionDecisionKind}
    assert "boundary_ready" in {item.value for item in InternalRuntimeBoundaryStatus}
    assert "design_handoff_ready_for_v0331" in {item.value for item in InternalRuntimeReadinessLevel}
    assert "path_reference_only" in {item.value for item in InternalRuntimeReferenceCorpusPosture}

    flags = build_internal_runtime_capability_flags(
        ready_for_v0331_agent_profile_runtime=True,
        ready_for_v0332_prompt_assembly=True,
        max_grantable_level="D3_SIMULATE",
    )

    assert flags.ready_for_v0331_agent_profile_runtime is True
    assert flags.ready_for_v0332_prompt_assembly is True
    assert internal_runtime_flags_preserve_runtime_false(flags)
    assert flags.production_certified is False
    assert flags.live_adapter_certified is False
    assert {"D4", "D5", "D6", "D7", "D8", "D9"}.issubset(set(flags.future_track_levels))

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            InternalRuntimeCapabilityFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.0",
                **{flag_name: True},
            )
    for cert_name in ("production_certified", "live_adapter_certified"):
        with pytest.raises(ValueError):
            InternalRuntimeCapabilityFlagSet(
                flag_set_id=f"flags:bad:{cert_name}",
                version="v0.33.0",
                **{cert_name: True},
            )
    with pytest.raises(ValueError):
        build_internal_runtime_capability_flags(max_grantable_level="D4_APPROVE")


def test_allowed_prohibited_reference_and_runtime_boundary_are_non_execution():
    allowed = build_internal_runtime_allowed_surface(
        "allowed:permission_gate",
        InternalRuntimeSurfaceKind.PERMISSION_GATE,
        InternalRuntimeCapabilityKind.EVALUATE_PERMISSION,
        "Permission evaluation is allowed only as boundary definition metadata.",
        evidence_refs=["evidence:allowed"],
    )
    prohibited = build_internal_runtime_prohibited_surface(
        "prohibited:shell",
        InternalRuntimeSurfaceKind.SHELL_COMMAND,
        InternalRuntimeRiskSurfaceKind.SHELL_SUBPROCESS,
        InternalRuntimeCapabilityKind.RUN_SHELL_COMMAND,
        "Shell execution is prohibited in v0.33.0.",
    )
    reference_boundary = build_internal_runtime_reference_corpus_boundary(
        "reference-boundary:1",
        known_reference_path_refs=["references/OpenCode", "references/Hermes", "references/OpenClaw"],
    )
    flags = build_internal_runtime_capability_flags(ready_for_v0331_agent_profile_runtime=True)
    boundary = build_internal_runtime_boundary(
        "boundary:1",
        flags,
        allowed_surfaces=[allowed],
        prohibited_surfaces=[prohibited],
        reference_corpus_boundary=reference_boundary,
        ready_for_v0331_agent_profile_runtime=True,
        ready_for_v0332_prompt_assembly=True,
    )

    assert allowed.executable_in_v0330 is False
    assert allowed.runtime_execution is False
    assert prohibited.blocks_execution is True
    assert prohibited.blocks_runtime_readiness is True
    assert prohibited.runtime_enforcement is False
    assert reference_boundary.open_code_reference_path_ref == "references/OpenCode"
    assert reference_boundary.hermes_reference_path_ref == "references/Hermes"
    assert reference_corpus_boundary_preserves_no_reference_execution(reference_boundary)
    assert set(DEFAULT_PROHIBITED_FILE_PATTERNS).issubset(set(reference_boundary.prohibited_file_patterns))
    assert internal_runtime_boundary_is_not_execution(boundary)
    assert boundary.ready_for_execution is False

    with pytest.raises(ValueError):
        InternalRuntimeAllowedSurface(
            allowed_surface_id="allowed:bad",
            surface_kind=InternalRuntimeSurfaceKind.PERMISSION_GATE,
            capability_kind=InternalRuntimeCapabilityKind.EVALUATE_PERMISSION,
            description="bad",
            executable_in_v0330=True,
        )
    with pytest.raises(ValueError):
        build_internal_runtime_prohibited_surface(
            "prohibited:bad",
            InternalRuntimeSurfaceKind.SHELL_COMMAND,
            InternalRuntimeRiskSurfaceKind.SHELL_SUBPROCESS,
            InternalRuntimeCapabilityKind.RUN_SHELL_COMMAND,
            "bad",
            blocks_execution=False,
        )
    for ref_flag in (
        "ready_for_reference_code_execution",
        "ready_for_reference_import",
        "ready_for_reference_dependency_install",
        "ready_for_reference_test_execution",
        "ready_for_reference_readonly_inspection",
    ):
        with pytest.raises(ValueError):
            InternalRuntimeReferenceCorpusBoundary(
                reference_boundary_id=f"reference-boundary:bad:{ref_flag}",
                version="v0.33.0",
                **{ref_flag: True},
            )
    with pytest.raises(ValueError):
        InternalRuntimeBoundary(
            boundary_id="boundary:bad",
            version="v0.33.0",
            release_name="bad",
            allowed_surfaces=[],
            prohibited_surfaces=[],
            reference_corpus_boundary=reference_boundary,
            capability_flags=flags,
            status=InternalRuntimeBoundaryStatus.BLOCKED,
            readiness_level=InternalRuntimeReadinessLevel.BOUNDARY_CONTRACT_READY,
            summary="bad",
            blocked_reasons=["blocking gap"],
            ready_for_v0331_agent_profile_runtime=True,
        )


def test_permission_request_decision_denied_action_and_gate_evaluation_are_not_grants():
    request = build_internal_runtime_permission_request(
        "request:1",
        requested_surface=InternalRuntimeSurfaceKind.READ_ONLY_TOOL_REGISTRY,
        requested_capability=InternalRuntimeCapabilityKind.INSPECT_TOOL_REGISTRY_READONLY,
        requested_action_summary="Ask for future read-only registry design handoff.",
        source_artifact_refs=["handoff:v0329"],
    )
    decision = build_internal_runtime_permission_decision(
        "decision:1",
        request.request_id,
        decision_kind=InternalRuntimePermissionDecisionKind.FUTURE_GATE_REQUIRED,
        allowed_only_for_design_stage=True,
        required_reviews=["v0.33.4 review"],
        denied_risk_surfaces=[InternalRuntimeRiskSurfaceKind.REGISTRY_MUTATION],
    )
    denied = build_internal_runtime_denied_action(
        "denied:1",
        request_id=request.request_id,
        decision_id=decision.decision_id,
        denied_surface=InternalRuntimeSurfaceKind.SHELL_COMMAND,
        denied_capability=InternalRuntimeCapabilityKind.RUN_SHELL_COMMAND,
        risk_surfaces=[InternalRuntimeRiskSurfaceKind.SHELL_SUBPROCESS],
        safe_alternatives=["record design-stage boundary only"],
    )
    evaluation = build_internal_runtime_gate_evaluation(
        "evaluation:1",
        "boundary:1",
        request.request_id,
        decision,
        denied_actions=[denied],
    )

    assert request.permission_grant is False
    assert request.execution is False
    assert permission_decision_preserves_no_execution(decision)
    assert denied.safe_outcome is True
    assert evaluation.execution_allowed is False
    assert evaluation.runtime_side_effect_allowed is False
    assert evaluation.execution is False

    with pytest.raises(ValueError):
        InternalRuntimePermissionDecision(
            decision_id="decision:bad",
            request_id=request.request_id,
            decision_kind=InternalRuntimePermissionDecisionKind.ALLOWED_DESIGN_STAGE_ONLY,
            reason="bad",
            execution_allowed=True,
        )
    with pytest.raises(ValueError):
        InternalRuntimePermissionDecision(
            decision_id="decision:bad-side-effect",
            request_id=request.request_id,
            decision_kind=InternalRuntimePermissionDecisionKind.ALLOWED_DESIGN_STAGE_ONLY,
            reason="bad",
            runtime_side_effect_allowed=True,
        )
    with pytest.raises(ValueError):
        InternalRuntimeGateEvaluation(
            evaluation_id="evaluation:bad",
            boundary_id="boundary",
            request_id=request.request_id,
            decision=decision,
            denied_actions=[],
            allowed_design_stage_only=True,
            execution_allowed=True,
            runtime_side_effect_allowed=False,
            summary="bad",
        )


def test_no_side_effect_guarantee_roadmap_and_readiness_report_preserve_future_stages():
    guarantee = build_internal_runtime_no_external_side_effect_guarantee("guarantee:1")
    roadmap = build_v033_roadmap_overview("roadmap:1")
    readiness = build_v0330_readiness_report(
        "readiness:1",
        boundary_id="boundary:1",
        roadmap_id=roadmap.roadmap_id,
        ready_for_v0331_agent_profile_runtime=True,
        ready_for_v0332_prompt_assembly=True,
        completed_items=["v0.33.0 boundary contract"],
        future_track_items=["read-only tool execution", "workspace inspection execution", "agent step execution"],
    )

    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert set(DEFAULT_V033_STAGES).issubset({InternalRuntimeTrackKind(stage).value for stage in roadmap.stages})
    assert "read-only design/reference corpus only" in roadmap.opencode_reference_role.lower()
    assert "read-only design/reference corpus only" in roadmap.hermes_reference_role.lower()
    assert roadmap.implementation is False
    assert readiness.ready_for_v0331_agent_profile_runtime is True
    assert readiness.ready_for_v0332_prompt_assembly is True
    assert v0330_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_V0330_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        InternalRuntimeNoExternalSideEffectGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.0",
            no_ocel_emission=False,
        )
    with pytest.raises(ValueError):
        V033RoadmapOverview(
            roadmap_id="roadmap:bad",
            version="v0.33.0",
            release_name="bad",
            stages=list(DEFAULT_V033_STAGES),
            stage_summaries={stage: stage for stage in DEFAULT_V033_STAGES},
            references_context_summary="refs",
            opencode_reference_role="can execute",
            hermes_reference_role="read-only design/reference corpus only",
            openclaw_reference_role=None,
            runtime_boundary_summary="boundary",
            prohibited_runtime_summary="prohibited",
            v034_handoff_preview="handoff",
        )
    with pytest.raises(ValueError):
        V0330ReadinessReport(
            report_id="readiness:bad-blocked",
            version="v0.33.0",
            ready_for_v0331_agent_profile_runtime=True,
            blocked_items=["blocked"],
        )
    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0330ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.0",
                **{flag_name: True},
            )


def test_helpers_are_pure_conservative_contract_builders():
    flags = build_internal_runtime_capability_flags()
    reference_boundary = build_internal_runtime_reference_corpus_boundary()
    allowed = build_internal_runtime_allowed_surface(
        "allowed:boundary",
        InternalRuntimeSurfaceKind.INTERNAL_PROFILE_RESOLUTION,
        InternalRuntimeCapabilityKind.RESOLVE_AGENT_PROFILE,
        "Profile resolution is a v0.33.1 design-stage handoff only in v0.33.0.",
    )
    prohibited = build_internal_runtime_prohibited_surface(
        "prohibited:provider",
        InternalRuntimeSurfaceKind.PROVIDER_BOUNDARY,
        InternalRuntimeRiskSurfaceKind.PROVIDER_INVOCATION,
        InternalRuntimeCapabilityKind.INVOKE_PROVIDER,
        "Provider invocation remains prohibited.",
    )
    boundary = build_internal_runtime_boundary(
        "boundary:helpers",
        flags,
        allowed_surfaces=[allowed],
        prohibited_surfaces=[prohibited],
        reference_corpus_boundary=reference_boundary,
    )
    request = build_internal_runtime_permission_request("request:helpers")
    decision = build_internal_runtime_permission_decision("decision:helpers", request.request_id)
    evaluation = build_internal_runtime_gate_evaluation("evaluation:helpers", boundary.boundary_id, request.request_id, decision)
    readiness = build_v0330_readiness_report("readiness:helpers")

    assert internal_runtime_flags_preserve_runtime_false(flags)
    assert reference_corpus_boundary_preserves_no_reference_execution(reference_boundary)
    assert internal_runtime_boundary_is_not_execution(boundary)
    assert permission_decision_preserves_no_execution(decision)
    assert evaluation.execution is False
    assert v0330_readiness_report_is_not_runtime_ready(readiness)

from __future__ import annotations

import inspect

import pytest

from chanta_core.external_dominion import DominionLevel
from chanta_core.internal_triad import (
    DominionControlBoundary,
    DominionControlBoundaryKind,
    DominionControlSurface,
    DominionDecisionReasonKind,
    DominionDecisionRunPreview,
    DominionFutureGateItem,
    DominionFutureGateKind,
    DominionNoOpDecision,
    DominionRiskSurface,
    DominionTargetDecisionSet,
    DominionTargetSourceRef,
    InternalDominionDecision,
    InternalDominionDecisionType,
    InternalDominionTarget,
    InternalDominionTargetKind,
    InternalDominionTargetStatus,
    V0316ReadinessReport,
    build_dominion_control_boundary,
    build_dominion_decision_run_preview,
    build_dominion_future_gate_item,
    build_dominion_target_decision_set,
    build_dominion_target_no_op_decision,
    build_dominion_target_source_ref,
    build_internal_dominion_decision,
    build_internal_dominion_target,
    build_v0316_readiness_report,
    decision_grants_no_authority,
    decision_set_preserves_no_runtime,
    dominion_decision_run_preview_preserves_no_execution,
    future_gate_is_not_ready,
    internal_dominion_decision_type_grants_execution,
    internal_dominion_target_kind_controls_runtime,
    normalize_dominion_control_boundary_kind,
    normalize_dominion_control_surface,
    normalize_dominion_decision_reason_kind,
    normalize_dominion_future_gate_kind,
    normalize_dominion_risk_surface,
    normalize_internal_dominion_decision_type,
    normalize_internal_dominion_target_kind,
    normalize_internal_dominion_target_status,
    target_preserves_no_external_control,
    v0316_readiness_report_is_not_runtime_ready,
)
from chanta_core.internal_triad import dominion_decisions


REQUIRED_TARGET_PROHIBITIONS = {
    "external_control",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "delegation_runtime",
}

REQUIRED_READINESS_PROHIBITIONS = {
    "external_control",
    "authority_grant",
    "external_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "delegation_runtime",
    "registry_mutation",
    "memory_mutation",
    "rollback",
    "retry",
    "D4-D9",
}


def test_v0316_taxonomies_are_complete_and_conservative() -> None:
    assert {kind.value for kind in InternalDominionTargetKind} == {
        "external_runtime_target",
        "external_agent_harness_target",
        "external_provider_target",
        "external_gateway_target",
        "external_rpa_target",
        "browser_runtime_target",
        "command_runtime_target",
        "credential_bound_target",
        "network_bound_target",
        "memory_boundary_target",
        "registry_boundary_target",
        "policy_boundary_target",
        "delegation_boundary_target",
        "future_track_target",
        "unknown",
    }
    assert normalize_internal_dominion_target_kind("unknown") is InternalDominionTargetKind.UNKNOWN
    assert internal_dominion_target_kind_controls_runtime(InternalDominionTargetKind.EXTERNAL_RUNTIME_TARGET) is False

    assert {status.value for status in InternalDominionTargetStatus} == {
        "unknown",
        "target_candidate",
        "target_recorded",
        "requires_review",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_internal_dominion_target_status("target_recorded") is InternalDominionTargetStatus.TARGET_RECORDED

    assert {decision.value for decision in InternalDominionDecisionType} == {
        "deny",
        "defer",
        "no_op",
        "require_review",
        "require_future_gate",
        "record_target_only",
        "plan_only",
        "simulate_only",
        "block",
        "future_track",
    }
    assert normalize_internal_dominion_decision_type("simulate_only") is InternalDominionDecisionType.SIMULATE_ONLY
    assert internal_dominion_decision_type_grants_execution(InternalDominionDecisionType.RECORD_TARGET_ONLY) is False

    assert {kind.value for kind in DominionControlBoundaryKind} == {
        "no_external_control",
        "no_provider_invocation",
        "no_network_access",
        "no_credential_access",
        "no_command_execution",
        "no_browser_automation",
        "no_rpa_control",
        "no_gateway_control",
        "no_packet_send",
        "no_raw_output_persistence",
        "no_memory_mutation",
        "no_registry_mutation",
        "no_policy_activation",
        "approval_required",
        "audit_required",
        "result_boundary_required",
        "rollback_no_op_required",
        "ocel_trace_required",
        "future_gate_required",
        "unknown",
    }
    assert normalize_dominion_control_boundary_kind("no_network_access") is DominionControlBoundaryKind.NO_NETWORK_ACCESS

    assert {kind.value for kind in DominionFutureGateKind} == {
        "external_execution_gate",
        "provider_invocation_gate",
        "network_access_gate",
        "credential_access_gate",
        "command_execution_gate",
        "browser_runtime_gate",
        "rpa_runtime_gate",
        "gateway_control_gate",
        "external_agent_delegation_gate",
        "registry_mutation_gate",
        "memory_mutation_gate",
        "policy_activation_gate",
        "tool_execution_gate",
        "mission_installation_gate",
        "production_certification_gate",
        "unknown",
    }
    assert normalize_dominion_future_gate_kind("external_execution_gate") is DominionFutureGateKind.EXTERNAL_EXECUTION_GATE

    assert {kind.value for kind in DominionDecisionReasonKind} == {
        "insufficient_evidence",
        "high_risk_surface",
        "missing_boundary",
        "missing_audit",
        "missing_approval",
        "missing_result_boundary",
        "missing_rollback_no_op",
        "incompatible_with_ocel_spine",
        "future_gate_required",
        "blocked_by_policy",
        "no_op_preferred",
        "descriptive_record_only",
        "conservative_routing",
        "unknown",
    }
    assert normalize_dominion_decision_reason_kind("conservative_routing") is DominionDecisionReasonKind.CONSERVATIVE_ROUTING

    assert {surface.value for surface in DominionControlSurface} == {
        "external_runtime",
        "provider",
        "network",
        "credential",
        "command",
        "browser",
        "rpa",
        "gateway",
        "packet",
        "delegation",
        "memory",
        "registry",
        "policy",
        "tool",
        "mission",
        "ocel_trace",
        "unknown",
    }
    assert normalize_dominion_control_surface("provider") is DominionControlSurface.PROVIDER

    assert {surface.value for surface in DominionRiskSurface} == {
        "private_data",
        "credential_exposure",
        "network_side_effect",
        "command_execution",
        "provider_invocation",
        "browser_automation",
        "rpa_control",
        "gateway_send",
        "external_delegation",
        "memory_contamination",
        "raw_output_persistence",
        "registry_mutation",
        "policy_activation",
        "mission_installation",
        "tool_execution",
        "ocel_schema_drift",
        "unknown",
    }
    assert normalize_dominion_risk_surface("credential_exposure") is DominionRiskSurface.CREDENTIAL_EXPOSURE


def _source_ref() -> DominionTargetSourceRef:
    return build_dominion_target_source_ref(
        "dominion_target_source_ref:1",
        "dominion_control_boundary_signal",
        "dominion_signal:1",
        signal_id="dominion_signal:1",
        route_decision_id="dominion_route_decision:1",
        evidence_ref_ids=["evidence:1"],
    )


def _target() -> InternalDominionTarget:
    return build_internal_dominion_target(
        "internal_dominion_target:1",
        "Provider target record",
        "Governance record only for provider boundary.",
        target_kind=InternalDominionTargetKind.EXTERNAL_PROVIDER_TARGET,
        source_refs=[_source_ref()],
        control_surfaces=[DominionControlSurface.PROVIDER, DominionControlSurface.NETWORK],
        risk_surfaces=[DominionRiskSurface.PROVIDER_INVOCATION],
        control_boundary_ids=["boundary:1"],
        future_gate_ids=["future_gate:1"],
        evidence_ref_ids=["evidence:1"],
    )


def test_source_ref_and_target_are_governance_only() -> None:
    source_ref = _source_ref()
    target = _target()

    assert isinstance(source_ref, DominionTargetSourceRef)
    assert source_ref.fetches_source is False
    assert isinstance(target, InternalDominionTarget)
    assert target.ready_for_external_control is False
    assert target.ready_for_authority_grant is False
    assert target.ready_for_execution is False
    assert target.external_runtime_control is False
    assert target.governance_artifact_only is True
    assert target.max_allowed_level == DominionLevel.D3_SIMULATE
    assert REQUIRED_TARGET_PROHIBITIONS.issubset(set(target.prohibited_runtime_actions))
    assert target_preserves_no_external_control(target) is True

    with pytest.raises(ValueError, match="source_ref_id"):
        build_dominion_target_source_ref("", "kind", "source")
    with pytest.raises(ValueError, match="source_kind"):
        build_dominion_target_source_ref("source:bad", "", "source")
    with pytest.raises(ValueError, match="source_id"):
        build_dominion_target_source_ref("source:bad", "kind", "")
    with pytest.raises(ValueError, match="source fetch"):
        build_dominion_target_source_ref("source:bad", "kind", "source", metadata={"source_ref_fetch": True})
    with pytest.raises(ValueError, match="dominion_target_id"):
        build_internal_dominion_target("", "title", "summary")
    with pytest.raises(ValueError, match="title"):
        build_internal_dominion_target("target:bad", "", "summary")
    with pytest.raises(ValueError, match="max_allowed_level"):
        build_internal_dominion_target(
            "target:bad",
            "title",
            "summary",
            max_allowed_level=DominionLevel.D4_EXECUTE_READ,
        )
    with pytest.raises(ValueError, match="ready_for_external_control"):
        InternalDominionTarget(
            "target:bad",
            None,
            InternalDominionTargetKind.UNKNOWN,
            InternalDominionTargetStatus.TARGET_RECORDED,
            "title",
            "summary",
            [],
            [],
            [],
            [],
            [],
            [],
            ready_for_external_control=True,
        )
    with pytest.raises(ValueError, match="governance artifact"):
        build_internal_dominion_target("target:bad", "title", "summary", metadata={"external_control": True})


def test_boundary_decision_future_gate_and_no_op_are_non_runtime() -> None:
    target = _target()
    boundary = build_dominion_control_boundary(
        "boundary:1",
        target.dominion_target_id,
        DominionControlBoundaryKind.NO_PROVIDER_INVOCATION,
        control_surfaces=[DominionControlSurface.PROVIDER],
        risk_surfaces=[DominionRiskSurface.PROVIDER_INVOCATION],
        required_future_gates=[DominionFutureGateKind.PROVIDER_INVOCATION_GATE],
    )
    decision = build_internal_dominion_decision(
        "dominion_decision:1",
        target.dominion_target_id,
        InternalDominionDecisionType.RECORD_TARGET_ONLY,
        DominionDecisionReasonKind.CONSERVATIVE_ROUTING,
        "Record target only; no authority granted.",
        granted_level=DominionLevel.D3_SIMULATE,
        required_boundaries=[DominionControlBoundaryKind.NO_PROVIDER_INVOCATION],
        required_future_gates=[DominionFutureGateKind.PROVIDER_INVOCATION_GATE],
        blocked_reasons=["provider invocation remains prohibited"],
    )
    future_gate = build_dominion_future_gate_item(
        "future_gate:1",
        DominionFutureGateKind.PROVIDER_INVOCATION_GATE,
        "Provider invocation requires later gate.",
        dominion_target_id=target.dominion_target_id,
        required_artifacts=["provider runtime control design"],
    )
    no_op = build_dominion_target_no_op_decision(
        "dominion_noop:1",
        "No external control should be performed.",
        dominion_target_id=target.dominion_target_id,
        safe_alternatives=["record target only"],
    )
    module_no_op = dominion_decisions.build_dominion_no_op_decision("dominion_noop:module", "Module exact helper remains available.")

    assert isinstance(boundary, DominionControlBoundary)
    assert boundary.blocks_execution is True
    assert boundary.blocks_external_control is True
    assert boundary.blocks_authority_grant is True
    assert boundary.is_permission is False
    assert isinstance(decision, InternalDominionDecision)
    assert decision.granted_level == DominionLevel.D3_SIMULATE
    assert decision.approved_for_execution is False
    assert decision.approved_for_external_control is False
    assert decision.authority_granted is False
    assert decision.ready_for_execution is False
    assert decision.is_execution is False
    assert decision.grants_authority is False
    assert decision_grants_no_authority(decision) is True
    assert isinstance(future_gate, DominionFutureGateItem)
    assert future_gate.ready_now is False
    assert future_gate.is_readiness is False
    assert future_gate_is_not_ready(future_gate) is True
    assert isinstance(no_op, DominionNoOpDecision)
    assert no_op.is_failure is False
    assert no_op.executes_anything is False
    assert isinstance(module_no_op, DominionNoOpDecision)

    with pytest.raises(ValueError, match="blocks_execution"):
        DominionControlBoundary("boundary:bad", target.dominion_target_id, DominionControlBoundaryKind.UNKNOWN, blocks_execution=False)
    with pytest.raises(ValueError, match="permission"):
        build_dominion_control_boundary("boundary:bad", target.dominion_target_id, DominionControlBoundaryKind.UNKNOWN, metadata={"permission": True})
    with pytest.raises(ValueError, match="granted_level"):
        build_internal_dominion_decision(
            "decision:bad",
            target.dominion_target_id,
            InternalDominionDecisionType.SIMULATE_ONLY,
            DominionDecisionReasonKind.UNKNOWN,
            "reason",
            granted_level=DominionLevel.D9_GATEWAY_CONTROL,
        )
    with pytest.raises(ValueError, match="authority_granted"):
        InternalDominionDecision(
            "decision:bad",
            target.dominion_target_id,
            InternalDominionDecisionType.PLAN_ONLY,
            DominionDecisionReasonKind.UNKNOWN,
            "reason",
            authority_granted=True,
        )
    with pytest.raises(ValueError, match="ready_now"):
        DominionFutureGateItem("gate:bad", target.dominion_target_id, DominionFutureGateKind.UNKNOWN, "reason", ready_now=True)
    with pytest.raises(ValueError, match="no_op_id"):
        build_dominion_target_no_op_decision("", "reason")
    with pytest.raises(ValueError, match="failure"):
        build_dominion_target_no_op_decision("noop:bad", "reason", metadata={"failure": True})


def test_decision_set_run_preview_and_readiness_are_not_runtime_enablement() -> None:
    target = _target()
    boundary = build_dominion_control_boundary("boundary:1", target.dominion_target_id, DominionControlBoundaryKind.NO_EXTERNAL_CONTROL)
    decision = build_internal_dominion_decision(
        "dominion_decision:1",
        target.dominion_target_id,
        InternalDominionDecisionType.DENY,
        DominionDecisionReasonKind.HIGH_RISK_SURFACE,
        "Deny external control.",
    )
    future_gate = build_dominion_future_gate_item("future_gate:1", DominionFutureGateKind.EXTERNAL_EXECUTION_GATE, "Later gate required.")
    no_op = build_dominion_target_no_op_decision("dominion_noop:1", "No-op preferred.")
    decision_set = build_dominion_target_decision_set(
        "dominion_decision_set:1",
        targets=[target],
        boundaries=[boundary],
        decisions=[decision],
        future_gates=[future_gate],
        no_op_decisions=[no_op],
        evidence_ref_ids=["evidence:1"],
    )
    preview = build_dominion_decision_run_preview("dominion_decision_preview:1", decision_set.decision_set_id)
    readiness = build_v0316_readiness_report(decision_set)

    assert isinstance(decision_set, DominionTargetDecisionSet)
    assert decision_set.ready_for_v0317_ocel_trace_integration is True
    assert decision_set.ready_for_execution is False
    assert decision_set.ready_for_external_control is False
    assert decision_set.ready_for_authority_grant is False
    assert decision_set.runtime_registry is False
    assert decision_set_preserves_no_runtime(decision_set) is True
    assert isinstance(preview, DominionDecisionRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_external_control_guarantee is True
    assert preview.no_authority_grant_guarantee is True
    assert preview.no_provider_invocation_guarantee is True
    assert preview.no_network_access_guarantee is True
    assert preview.no_credential_access_guarantee is True
    assert preview.no_command_execution_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False
    assert dominion_decision_run_preview_preserves_no_execution(preview) is True
    assert isinstance(readiness, V0316ReadinessReport)
    assert "v0.31.6" in readiness.version
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_external_control is False
    assert readiness.ready_for_authority_grant is False
    assert readiness.ready_for_dominion_runtime is False
    assert readiness.runtime_enablement is False
    assert REQUIRED_READINESS_PROHIBITIONS.issubset(set(readiness.prohibited_until_later_gate))
    assert v0316_readiness_report_is_not_runtime_ready(readiness) is True

    with pytest.raises(ValueError, match="decision_set_id"):
        build_dominion_target_decision_set("")
    with pytest.raises(ValueError, match="ready_for_execution"):
        DominionTargetDecisionSet("set:bad", None, [], [], [], [], [], ready_for_execution=True)
    with pytest.raises(ValueError, match="runtime registry"):
        build_dominion_target_decision_set("set:bad", metadata={"runtime_registry": True})
    with pytest.raises(ValueError, match="run_preview_id"):
        build_dominion_decision_run_preview("")
    with pytest.raises(ValueError, match="no_external_control_guarantee"):
        DominionDecisionRunPreview("preview:bad", no_external_control_guarantee=False)
    with pytest.raises(ValueError, match="v0.31.6"):
        V0316ReadinessReport("readiness:bad", "v0.31.5", None, "summary", True)
    with pytest.raises(ValueError, match="ready_for_dominion_runtime"):
        V0316ReadinessReport("readiness:bad", "v0.31.6", None, "summary", True, ready_for_dominion_runtime=True)


def test_helpers_are_pure_conservative_governance_builders() -> None:
    helpers = [
        build_dominion_target_source_ref,
        build_internal_dominion_target,
        build_dominion_control_boundary,
        build_internal_dominion_decision,
        build_dominion_future_gate_item,
        dominion_decisions.build_dominion_no_op_decision,
        build_dominion_target_decision_set,
        build_dominion_decision_run_preview,
        build_v0316_readiness_report,
        target_preserves_no_external_control,
        decision_grants_no_authority,
        decision_set_preserves_no_runtime,
        future_gate_is_not_ready,
        dominion_decision_run_preview_preserves_no_execution,
        v0316_readiness_report_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "approved_for_execution=True" not in source
        assert "approved_for_external_control=True" not in source
        assert "authority_granted=True" not in source
        assert "ready_for_execution=True" not in source
        assert "ready_for_external_control=True" not in source
        assert "ready_for_authority_grant=True" not in source
        assert "ready_now=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = inspect.getsource(dominion_decisions)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source

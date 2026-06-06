import pytest

from chanta_core.external_harness import (
    ExternalCapabilityRiskClass,
    ExternalCapabilityRiskRoute,
    ExternalCapabilityRiskSeverity,
    ExternalDominionAuthorityPosture,
    ExternalDominionBlockerKind,
    ExternalDominionCandidateKind,
    ExternalDominionCandidateStatus,
    ExternalDominionControlSurfaceKind,
    ExternalDominionEmissionRoute,
    ExternalDominionEvidenceQuality,
    ExternalDominionReviewRequirementKind,
    ExternalDominionRiskSurfaceKind,
    ExternalDominionSourceKind,
    build_emitted_dominion_control_boundary_candidate,
    build_emitted_dominion_future_gate_item,
    build_emitted_dominion_no_op_decision,
    build_emitted_internal_dominion_target_candidate,
    build_external_capability_risk_classification,
    build_external_capability_risk_factor,
    build_external_digestibility_assessment,
    build_external_digestion_blocker,
    build_external_digestion_pattern_signal,
    build_external_digestion_source_ref,
    build_external_dominion_blocker,
    build_external_dominion_candidate_emission_finding,
    build_external_dominion_candidate_emission_input,
    build_external_dominion_candidate_emission_report,
    build_external_dominion_candidate_no_runtime_guarantee,
    build_external_dominion_candidate_run_preview,
    build_external_dominion_control_boundary_candidate,
    build_external_dominion_evidence_ref,
    build_external_dominion_review_requirement,
    build_external_dominion_risk_signal,
    build_external_dominion_source_ref,
    build_external_harness_digestion_candidate,
    build_external_harness_dominion_candidate,
    build_external_harness_dominion_candidate_set,
    build_v0328_readiness_report,
    dominion_candidate_preserves_no_external_control,
    dominion_candidate_set_is_not_runtime_registry,
    dominion_target_candidate_is_not_active_target,
    infer_external_dominion_blockers_from_risk_surfaces,
    infer_external_dominion_candidate_kind_from_risk_classification,
    infer_external_dominion_control_surfaces_from_risk_surfaces,
    infer_external_dominion_route_from_source,
    v0328_readiness_report_is_not_runtime_ready,
)
from chanta_core.external_harness.digestion_generation import (
    ExternalDigestibilityPosture,
    ExternalDigestionBlockerKind,
    ExternalDigestionCandidateKind,
    ExternalDigestionPatternKind,
    ExternalDigestionRoute,
)
from chanta_core.external_harness.dominion_candidate_emitter import (
    DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS,
    EmittedDominionFutureGateItem,
    EmittedInternalDominionTargetCandidate,
    ExternalDominionCandidateEmissionReport,
    ExternalDominionControlBoundaryCandidate,
    ExternalDominionEvidenceRef,
    ExternalDominionReviewRequirement,
    ExternalDominionSourceRef,
    V0328ReadinessReport,
)


def test_external_dominion_taxonomies_include_required_values():
    assert {item.value for item in ExternalDominionCandidateKind} == {
        "external_runtime_control_candidate",
        "provider_invocation_candidate",
        "network_access_candidate",
        "credential_access_candidate",
        "command_execution_candidate",
        "browser_runtime_candidate",
        "rpa_control_candidate",
        "gateway_connection_candidate",
        "channel_access_candidate",
        "message_send_candidate",
        "webhook_call_candidate",
        "plugin_loading_candidate",
        "external_plugin_loading_candidate",
        "tool_invocation_candidate",
        "tool_registration_candidate",
        "mission_execution_candidate",
        "mission_installation_candidate",
        "delegation_execution_candidate",
        "memory_mutation_candidate",
        "registry_mutation_candidate",
        "private_data_access_candidate",
        "raw_output_persistence_candidate",
        "ocel_emission_candidate",
        "approval_boundary_candidate",
        "audit_boundary_candidate",
        "future_track_candidate",
        "no_op_candidate",
        "unknown",
    }
    assert "provider" in {item.value for item in ExternalDominionControlSurfaceKind}
    assert "command_execution" in {item.value for item in ExternalDominionRiskSurfaceKind}
    assert {item.value for item in ExternalDominionEmissionRoute} == {
        "emit_for_v0329_consolidation",
        "require_review",
        "require_future_gate",
        "defer",
        "reject",
        "block",
        "future_track",
        "no_op",
        "unknown",
    }
    assert "emitted_with_gaps" in {item.value for item in ExternalDominionCandidateStatus}
    assert {item.value for item in ExternalDominionAuthorityPosture} == {
        "no_authority",
        "descriptive_only",
        "boundary_only",
        "future_gate_only",
        "no_op",
        "blocked",
        "future_track",
        "unknown",
    }
    assert "sufficient_for_dominion_candidate" in {item.value for item in ExternalDominionEvidenceQuality}
    assert "authority_grant_required" in {item.value for item in ExternalDominionBlockerKind}
    assert "manual_dominion_review" in {item.value for item in ExternalDominionSourceKind}
    assert "human_review" in {item.value for item in ExternalDominionReviewRequirementKind}


def test_source_evidence_risk_boundary_review_and_blocker_are_governance_only():
    source_ref = build_external_dominion_source_ref(
        "dominion-source:1",
        ExternalDominionSourceKind.EXTERNAL_CAPABILITY_RISK_CLASSIFICATION,
        "risk-classification:1",
        reference_entry_ids=["reference:1"],
        evidence_refs=["evidence:1"],
    )
    evidence_ref = build_external_dominion_evidence_ref(
        "evidence:1",
        evidence_kind="risk_classification_summary",
        evidence_summary="Static dominion evidence only.",
        quality=ExternalDominionEvidenceQuality.SUFFICIENT_FOR_DOMINION_CANDIDATE,
        limitations=["human review required"],
    )
    risk_signal = build_external_dominion_risk_signal(
        "risk-signal:1",
        [source_ref.source_ref_id],
        ExternalDominionCandidateKind.COMMAND_EXECUTION_CANDIDATE,
        control_surfaces=[ExternalDominionControlSurfaceKind.COMMAND],
        risk_surfaces=[ExternalDominionRiskSurfaceKind.COMMAND_EXECUTION],
        severity="critical",
        summary="Command execution requires dominion boundary review.",
        recommended_boundary_kinds=["no_command_execution"],
        recommended_review_kinds=[ExternalDominionReviewRequirementKind.COMMAND_REVIEW],
        evidence_refs=[evidence_ref],
    )
    boundary = build_external_dominion_control_boundary_candidate(
        "boundary:1",
        "No command execution",
        "Blocks command execution and authority grant.",
        control_surfaces=[ExternalDominionControlSurfaceKind.COMMAND],
        risk_surfaces=[ExternalDominionRiskSurfaceKind.COMMAND_EXECUTION],
        required_reviews=[ExternalDominionReviewRequirementKind.COMMAND_REVIEW],
        evidence_refs=[evidence_ref],
    )
    review = build_external_dominion_review_requirement(
        "review:1",
        ExternalDominionReviewRequirementKind.COMMAND_REVIEW,
        target_candidate_ids=["target:1"],
        required_evidence_refs=[evidence_ref.evidence_ref_id],
    )
    blocker = build_external_dominion_blocker(
        "blocker:1",
        ExternalDominionBlockerKind.COMMAND_EXECUTION_SURFACE,
        source_ref_ids=[source_ref.source_ref_id],
        reason="Command execution surface is governance-blocked.",
        evidence_refs=[evidence_ref],
    )

    assert source_ref.source_fetch is False
    assert source_ref.execution is False
    assert evidence_ref.runtime_trust is False
    assert evidence_ref.authority_grant is False
    assert risk_signal.proof is False
    assert risk_signal.authority_grant is False
    assert boundary.blocks_execution is True
    assert boundary.blocks_external_control is True
    assert boundary.blocks_authority_grant is True
    assert boundary.permission is False
    assert boundary.runtime_enforcement is False
    assert review.approval_granted is False
    assert review.approval is False
    assert blocker.remediation_execution is False

    with pytest.raises(ValueError):
        ExternalDominionSourceRef(
            source_ref_id="source:bad",
            source_kind=ExternalDominionSourceKind.UNKNOWN,
            source_id="source",
            metadata={"source_fetch": True},
        )
    with pytest.raises(ValueError):
        ExternalDominionEvidenceRef(
            evidence_ref_id="evidence:bad",
            evidence_kind="static",
            evidence_summary="Static.",
            metadata={"authority_grant": True},
        )
    with pytest.raises(ValueError):
        build_external_dominion_risk_signal(
            "risk-signal:bad",
            ["source"],
            ExternalDominionCandidateKind.COMMAND_EXECUTION_CANDIDATE,
            severity="critical",
            summary="Missing boundary and review.",
        )
    with pytest.raises(ValueError):
        ExternalDominionControlBoundaryCandidate(
            boundary_candidate_id="boundary:bad",
            boundary_name="bad",
            boundary_summary="bad",
            metadata={"permission": True},
        )
    with pytest.raises(ValueError):
        ExternalDominionReviewRequirement(
            review_requirement_id="review:bad",
            requirement_kind=ExternalDominionReviewRequirementKind.HUMAN_REVIEW,
            approval_granted=True,
        )
    with pytest.raises(ValueError):
        build_external_dominion_blocker(
            "blocker:bad",
            ExternalDominionBlockerKind.UNKNOWN,
            metadata={"remediation": True},
        )


def test_emitted_dominion_artifacts_are_not_active_control_or_authority():
    source_ref = build_external_dominion_source_ref(
        "source:target",
        ExternalDominionSourceKind.EXTERNAL_DIGESTION_CANDIDATE,
        "digestion:1",
    )
    evidence_ref = build_external_dominion_evidence_ref("evidence:target")
    risk_signal = build_external_dominion_risk_signal(
        "risk-signal:target",
        [source_ref.source_ref_id],
        ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
        control_surfaces=[ExternalDominionControlSurfaceKind.PROVIDER],
        risk_surfaces=[ExternalDominionRiskSurfaceKind.PROVIDER_INVOCATION],
        severity="high",
        summary="Provider invocation requires boundary review.",
        recommended_boundary_kinds=["no_provider_invocation"],
        evidence_refs=[evidence_ref],
    )
    target = build_emitted_internal_dominion_target_candidate(
        "target:1",
        ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
        "Provider dominion target candidate",
        "Design-stage provider dominion target candidate only.",
        source_refs=[source_ref],
        control_surfaces=[ExternalDominionControlSurfaceKind.PROVIDER],
        risk_surfaces=[ExternalDominionRiskSurfaceKind.PROVIDER_INVOCATION],
        risk_signals=[risk_signal],
        max_allowed_level="D3_SIMULATE",
        evidence_refs=[evidence_ref],
    )
    boundary_candidate = build_external_dominion_control_boundary_candidate(
        "boundary:provider",
        "No provider invocation",
        "Blocks provider invocation.",
        control_surfaces=[ExternalDominionControlSurfaceKind.PROVIDER],
        risk_surfaces=[ExternalDominionRiskSurfaceKind.PROVIDER_INVOCATION],
    )
    emitted_boundary = build_emitted_dominion_control_boundary_candidate(
        "emitted-boundary:provider",
        target.dominion_target_candidate_id,
        boundary_candidate,
        evidence_refs=[evidence_ref],
    )
    future_gate = build_emitted_dominion_future_gate_item(
        "future-gate:provider",
        target_candidate_id=target.dominion_target_candidate_id,
        gate_kind="provider_authority_review",
        required_reviews=[ExternalDominionReviewRequirementKind.PROVIDER_REVIEW],
    )
    no_op = build_emitted_dominion_no_op_decision(
        "no-op:provider",
        target_candidate_id=target.dominion_target_candidate_id,
        reason="No runtime dominion action is permitted.",
        safe_alternatives=["describe only"],
    )

    assert dominion_target_candidate_is_not_active_target(target)
    assert target.active_internal_dominion_target is False
    assert target.external_control is False
    assert target.d4_d9_grant is False
    assert emitted_boundary.permission is False
    assert emitted_boundary.ready_for_runtime_enforcement is False
    assert emitted_boundary.ready_for_external_control is False
    assert future_gate.ready_now is False
    assert future_gate.readiness is False
    assert no_op.ready_for_execution is False
    assert no_op.failure is False

    with pytest.raises(ValueError):
        build_emitted_internal_dominion_target_candidate(
            "target:bad-control",
            ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
            "bad",
            "bad",
            ready_for_external_control=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_dominion_target_candidate(
            "target:bad-authority",
            ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
            "bad",
            "bad",
            ready_for_authority_grant=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_dominion_target_candidate(
            "target:bad-active",
            ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
            "bad",
            "bad",
            ready_for_active_dominion_target_creation=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_dominion_target_candidate(
            "target:bad-level",
            ExternalDominionCandidateKind.PROVIDER_INVOCATION_CANDIDATE,
            "bad",
            "bad",
            max_allowed_level="D4_APPROVE",
        )
    with pytest.raises(ValueError):
        EmittedDominionFutureGateItem(
            future_gate_id="future-gate:bad",
            gate_kind="gate",
            ready_now=True,
        )


def test_candidate_set_input_finding_report_preview_guarantee_and_readiness_are_non_runtime():
    target = build_emitted_internal_dominion_target_candidate(
        "target:set",
        ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE,
        "Gateway target candidate",
        "Design-stage gateway target candidate only.",
    )
    boundary = build_external_dominion_control_boundary_candidate(
        "boundary:set",
        "No gateway connection",
        "Blocks gateway connection.",
    )
    emitted_boundary = build_emitted_dominion_control_boundary_candidate(
        "emitted-boundary:set",
        target.dominion_target_candidate_id,
        boundary,
    )
    candidate = build_external_harness_dominion_candidate(
        "dominion-candidate:1",
        ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE,
        ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION,
        ExternalDominionCandidateStatus.EMITTED_WITH_GAPS,
        "Gateway dominion candidate",
        "Design-stage gateway dominion candidate only.",
        target_candidate=target,
        boundary_candidates=[emitted_boundary],
        ready_for_v0329_consolidation=True,
    )
    candidate_set = build_external_harness_dominion_candidate_set(
        "candidate-set:1",
        candidates=[candidate],
        target_candidates=[target],
        boundary_candidates=[emitted_boundary],
        emitted_candidate_ids=[candidate.dominion_candidate_id, target.dominion_target_candidate_id],
        ready_for_v0329_consolidation=True,
    )
    source_ref = build_external_dominion_source_ref(
        "source:input",
        ExternalDominionSourceKind.EXTERNAL_CAPABILITY_RISK_CLASSIFICATION,
        "risk:1",
    )
    emission_input = build_external_dominion_candidate_emission_input(
        "input:1",
        risk_classification_ids=["risk:1"],
        external_digestion_candidate_ids=["digestion:1"],
        internal_candidate_emission_report_ids=["internal-report:1"],
        source_refs=[source_ref],
        requested_candidate_kinds=[ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE],
    )
    finding = build_external_dominion_candidate_emission_finding(
        "finding:1",
        emission_input.emission_input_id,
        [source_ref.source_ref_id],
        candidate.dominion_candidate_id,
        ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE,
        ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION,
        ExternalDominionCandidateStatus.EMITTED_WITH_GAPS,
        ExternalDominionAuthorityPosture.BOUNDARY_ONLY,
        "Static dominion finding.",
    )
    report = build_external_dominion_candidate_emission_report(
        "report:1",
        emission_input.emission_input_id,
        candidate_set_id=candidate_set.candidate_set_id,
        findings=[finding],
        emitted_candidate_count=1,
        target_candidate_count=1,
        boundary_candidate_count=1,
        ready_for_v0329_consolidation=True,
    )
    preview = build_external_dominion_candidate_run_preview(
        "preview:1",
        planned_steps=["read static dominion metadata"],
        expected_artifacts=["external dominion candidate records"],
        explicitly_not_performed=["external control", "authority grant", "execution"],
    )
    guarantee = build_external_dominion_candidate_no_runtime_guarantee("guarantee:1")
    readiness = build_v0328_readiness_report(
        "readiness:1",
        emission_report_id=report.report_id,
        candidate_set_id=candidate_set.candidate_set_id,
        ready_for_v0329_external_observation_digestion_consolidation=True,
    )

    assert dominion_candidate_preserves_no_external_control(candidate)
    assert dominion_candidate_set_is_not_runtime_registry(candidate_set)
    assert emission_input.execution_request is False
    assert finding.active_target is False
    assert finding.authority_grant is False
    assert report.runtime_result is False
    assert preview.execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert guarantee.no_d4_d9_grant is True
    assert v0328_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(emission_input.prohibited_runtime_actions))
    assert set(DEFAULT_DOMINION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        build_external_harness_dominion_candidate(
            "dominion-candidate:bad",
            ExternalDominionCandidateKind.GATEWAY_CONNECTION_CANDIDATE,
            ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION,
            ExternalDominionCandidateStatus.EMITTED,
            "bad",
            "bad",
            ready_for_dominion_decision_creation=True,
        )
    with pytest.raises(ValueError):
        build_external_harness_dominion_candidate_set(
            "candidate-set:bad",
            metadata={"runtime_registry": True},
        )
    with pytest.raises(ValueError):
        ExternalDominionCandidateEmissionReport(
            report_id="report:bad",
            version="v0.32.8",
            emission_input_id="input",
            ready_for_external_control=True,
        )
    for flag_name in (
        "ready_for_execution",
        "ready_for_external_control",
        "ready_for_authority_grant",
        "ready_for_active_dominion_target_creation",
        "ready_for_dominion_decision_creation",
        "ready_for_dominion_runtime",
        "ready_for_provider_invocation",
        "ready_for_gateway_connection",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
        "ready_for_browser_runtime_control",
        "ready_for_rpa_runtime_control",
        "ready_for_packet_send",
        "ready_for_registry_mutation",
        "ready_for_memory_mutation",
    ):
        with pytest.raises(ValueError):
            V0328ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.32.8",
                **{flag_name: True},
            )


def test_fake_risk_and_digestion_candidates_emit_dominion_candidates_without_execution():
    risk_factor = build_external_capability_risk_factor(
        "risk-factor:command",
        risk_surface="command_execution",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        severity=ExternalCapabilityRiskSeverity.HIGH,
        summary="Command execution is routed to dominion candidate emission.",
        boundary_kinds=["no_command_execution"],
        review_requirements=["command_review"],
    )
    classification = build_external_capability_risk_classification(
        "classification:command",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER,
        severity=ExternalCapabilityRiskSeverity.HIGH,
        risk_factors=[risk_factor],
        ready_for_v0328_dominion_candidate_emitter=True,
    )
    digestion_source = build_external_digestion_source_ref(
        "digestion-source:1",
        "external_capability_risk_classification",
        classification.classification_id,
    )
    signal = build_external_digestion_pattern_signal(
        "digestion-signal:1",
        [digestion_source.source_ref_id],
        ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE,
        ExternalDigestionPatternKind.SCHEMA_PATTERN,
        "Static tool command pattern",
        "Static command surface pattern.",
        "Command execution remains dominion-routed.",
    )
    assessment = build_external_digestibility_assessment(
        "assessment:dominion",
        digestibility_posture=ExternalDigestibilityPosture.REQUIRES_REVIEW,
        route=ExternalDigestionRoute.SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER,
        ready_for_v0328_dominion_candidate_emitter=True,
    )
    blocker = build_external_digestion_blocker(
        "digestion-blocker:dominion",
        ExternalDigestionBlockerKind.DOMINION_REQUIRED_ROUTE,
        routes_to_v0328=True,
    )
    digestion_candidate = build_external_harness_digestion_candidate(
        "digestion:dominion",
        ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE,
        [digestion_source],
        [signal],
        assessment,
        blockers=[blocker],
        ready_for_v0328_dominion_candidate_emitter=True,
        status=ExternalDigestibilityPosture.REQUIRES_REVIEW,
        route=ExternalDigestionRoute.SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER,
    )

    assert infer_external_dominion_candidate_kind_from_risk_classification(classification) == ExternalDominionCandidateKind.COMMAND_EXECUTION_CANDIDATE
    assert infer_external_dominion_route_from_source(classification) == ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION
    assert infer_external_dominion_route_from_source(digestion_candidate) == ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION
    surfaces = [ExternalDominionRiskSurfaceKind.COMMAND_EXECUTION, ExternalDominionRiskSurfaceKind.NETWORK_SIDE_EFFECT]
    assert infer_external_dominion_control_surfaces_from_risk_surfaces(surfaces) == [
        ExternalDominionControlSurfaceKind.COMMAND,
        ExternalDominionControlSurfaceKind.NETWORK,
    ]
    blockers = infer_external_dominion_blockers_from_risk_surfaces(surfaces)
    assert ExternalDominionBlockerKind.COMMAND_EXECUTION_SURFACE in blockers
    assert ExternalDominionBlockerKind.NETWORK_ACCESS_SURFACE in blockers

    target = build_emitted_internal_dominion_target_candidate(
        "target:from-risk",
        infer_external_dominion_candidate_kind_from_risk_classification(classification),
        "Command target candidate",
        "Design-stage command dominion target candidate only.",
        control_surfaces=infer_external_dominion_control_surfaces_from_risk_surfaces(surfaces),
        risk_surfaces=surfaces,
    )
    candidate = build_external_harness_dominion_candidate(
        "dominion-candidate:from-risk",
        target.candidate_kind,
        ExternalDominionEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION,
        ExternalDominionCandidateStatus.EMITTED_WITH_GAPS,
        "Command dominion candidate",
        "Design-stage command dominion candidate only.",
        target_candidate=target,
    )

    assert dominion_target_candidate_is_not_active_target(target)
    assert dominion_candidate_preserves_no_external_control(candidate)

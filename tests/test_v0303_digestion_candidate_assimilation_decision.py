from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    AssimilationDecision,
    AssimilationDecisionType,
    CapabilityObservationReport,
    DigestionBlockReason,
    DigestionCandidate,
    DigestionCandidateKind,
    DigestionFeasibilityReport,
    DigestionFeasibilityStatus,
    DominionDecision,
    DominionLevel,
    ExternalBoundarySurface,
    ExternalCapabilityDescriptor,
    ExternalCapabilityKind,
    ExternalCapabilityObservationStatus,
    ExternalEffectSurface,
    ExternalRiskSignal,
    InternalArtifactCandidateKind,
    InternalizationPlan,
    aggregate_capability_surfaces,
    aggregate_risk_signals,
    build_digestion_candidates_from_observation_report,
    can_create_digestion_candidate_from_report,
    classify_digestion_candidate_from_capability,
    infer_digestion_block_reasons_from_observation,
    infer_effect_surfaces_from_risk_signals,
    infer_internal_artifact_candidate_kind,
    is_dangerous_for_digestion,
    make_assimilation_decision,
    make_internalization_plan,
    summarize_digestion_feasibility,
)


def _descriptor(**overrides) -> ExternalCapabilityDescriptor:
    data = {
        "capability_id": "capability:tool-contract",
        "target_id": "target:external",
        "name": "Read-only tool contract manifest",
        "kind": ExternalCapabilityKind.TOOL,
        "description": "A metadata-only tool contract pattern.",
        "observation_status": ExternalCapabilityObservationStatus.EVIDENCE_LINKED,
        "effect_surfaces": [ExternalEffectSurface.READ_ONLY],
        "boundary_surfaces": [ExternalBoundarySurface.DATA_BOUNDARY],
        "risk_signals": [],
        "declared_inputs": ["input_schema"],
        "declared_outputs": ["result_envelope"],
        "evidence_refs": ["evidence:manifest"],
        "confidence": "low",
        "conflict_notes": [],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalCapabilityDescriptor(**data)


def _report(capabilities: list[ExternalCapabilityDescriptor]) -> CapabilityObservationReport:
    effects, boundaries = aggregate_capability_surfaces(capabilities)
    risks = aggregate_risk_signals(capabilities)
    return CapabilityObservationReport(
        "capability_observation_report:target:external",
        "target:external",
        "inventory:target:external",
        "manifest",
        "source-ref:not-fetched",
        capabilities,
        effects,
        boundaries,
        risks,
        ExternalEffectSurface.CREDENTIAL_REQUIRED in effects,
        ExternalEffectSurface.NETWORK_POSSIBLE in effects,
        ExternalEffectSurface.COMMAND_POSSIBLE in effects,
        ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE in effects,
        ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE in effects,
        ExternalEffectSurface.RPA_CONTROL_POSSIBLE in effects,
        ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE in effects,
        ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE in effects,
        ExternalEffectSurface.DELEGATION_POSSIBLE in effects,
        "low",
        evidence_refs=["evidence:manifest"],
    )


def _candidate(**overrides) -> DigestionCandidate:
    data = {
        "candidate_id": "digestion_candidate:capability:tool-contract",
        "target_id": "target:external",
        "source_report_id": "capability_observation_report:target:external",
        "source_capability_ids": ["capability:tool-contract"],
        "candidate_kind": DigestionCandidateKind.TOOL_CONTRACT_PATTERN,
        "proposed_internal_artifact_kind": InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        "title": "Tool contract candidate",
        "summary": "Pattern-only candidate.",
        "extracted_pattern": {"schema": "descriptive"},
        "supporting_evidence_refs": ["evidence:manifest"],
        "risk_signals": [],
        "effect_surfaces": [ExternalEffectSurface.READ_ONLY],
        "boundary_surfaces": [ExternalBoundarySurface.DATA_BOUNDARY],
        "feasibility_status": DigestionFeasibilityStatus.DIGESTIBLE_PATTERN_ONLY,
        "blocked_reasons": [],
        "assumptions": ["pattern only"],
        "withdrawal_conditions": ["candidate is treated as runtime artifact"],
        "metadata": {},
    }
    data.update(overrides)
    return DigestionCandidate(**data)


def test_valid_digestion_candidate_creation_is_contract_only() -> None:
    candidate = _candidate()

    assert candidate.creates_internal_artifact is False
    assert candidate.creates_dominion_target is False
    assert candidate.grants_permission is False
    assert candidate.executes is False
    assert candidate.proposed_internal_artifact_kind == InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE


def test_digestion_candidate_rejects_blank_required_fields() -> None:
    with pytest.raises(ValueError, match="candidate_id"):
        _candidate(candidate_id="")
    with pytest.raises(ValueError, match="target_id"):
        _candidate(target_id="")
    with pytest.raises(ValueError, match="source_report_id"):
        _candidate(source_report_id="")
    with pytest.raises(ValueError, match="title"):
        _candidate(title=" ")


def test_digestion_candidate_validates_list_and_dict_fields() -> None:
    with pytest.raises(TypeError, match="source_capability_ids"):
        _candidate(source_capability_ids="not-list")
    with pytest.raises(TypeError, match="supporting_evidence_refs"):
        _candidate(supporting_evidence_refs="not-list")
    with pytest.raises(TypeError, match="extracted_pattern"):
        _candidate(extracted_pattern=[])


def test_blocked_or_unsafe_feasibility_requires_blocked_reasons() -> None:
    with pytest.raises(ValueError, match="blocked_reasons"):
        _candidate(feasibility_status=DigestionFeasibilityStatus.BLOCKED, blocked_reasons=[])
    with pytest.raises(ValueError, match="blocked_reasons"):
        _candidate(feasibility_status=DigestionFeasibilityStatus.UNSAFE_TO_DIGEST, blocked_reasons=[])

    blocked = _candidate(
        feasibility_status=DigestionFeasibilityStatus.BLOCKED,
        proposed_internal_artifact_kind=InternalArtifactCandidateKind.NONE,
        blocked_reasons=[DigestionBlockReason.TRUST_BOUNDARY_BLOCKED],
    )
    assert blocked.creates_internal_artifact is False


def test_digestible_or_schema_feasibility_requires_supporting_evidence() -> None:
    with pytest.raises(ValueError, match="supporting_evidence_refs"):
        _candidate(supporting_evidence_refs=[])
    with pytest.raises(ValueError, match="supporting_evidence_refs"):
        _candidate(
            feasibility_status=DigestionFeasibilityStatus.SCHEMA_EXTRACTABLE,
            supporting_evidence_refs=[],
        )


def test_feasibility_report_counts_and_target_match_are_validated() -> None:
    candidate = _candidate()
    report = summarize_digestion_feasibility(
        [candidate],
        target_id="target:external",
        source_report_id="capability_observation_report:target:external",
    )

    assert report.digestible_count == 1
    assert report.deferred_count == 0
    assert report.rejected_count == 0
    assert report.dominion_required_count == 0
    assert report.blocked_count == 0
    assert report.creates_internal_skill is False
    assert report.creates_dominion_target is False
    assert report.grants_permission is False

    with pytest.raises(ValueError, match="target_ids"):
        DigestionFeasibilityReport(
            "digestion_feasibility_report:bad",
            "target:other",
            "capability_observation_report:target:external",
            [candidate],
            1,
            0,
            0,
            0,
            0,
        )
    with pytest.raises(ValueError, match="counts"):
        DigestionFeasibilityReport(
            "digestion_feasibility_report:bad-count",
            "target:external",
            "capability_observation_report:target:external",
            [candidate],
            0,
            0,
            0,
            0,
            0,
        )


def test_assimilation_decision_validation_and_non_authority() -> None:
    with pytest.raises(ValueError, match="decision_id"):
        AssimilationDecision(
            "",
            "digestion_candidate:1",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.CANDIDATE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            "candidate only",
            evidence_refs=["evidence:manifest"],
        )
    with pytest.raises(ValueError, match="candidate_id"):
        AssimilationDecision(
            "assimilation_decision:1",
            "",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.CANDIDATE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            "candidate only",
            evidence_refs=["evidence:manifest"],
        )
    with pytest.raises(ValueError, match="target_id"):
        AssimilationDecision(
            "assimilation_decision:1",
            "digestion_candidate:1",
            "",
            "capability_observation_report:target:external",
            AssimilationDecisionType.CANDIDATE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            "candidate only",
            evidence_refs=["evidence:manifest"],
        )
    with pytest.raises(ValueError, match="reason"):
        AssimilationDecision(
            "assimilation_decision:1",
            "digestion_candidate:1",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.CANDIDATE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            " ",
            evidence_refs=["evidence:manifest"],
        )
    with pytest.raises(ValueError, match="evidence_refs"):
        AssimilationDecision(
            "assimilation_decision:no-evidence",
            "digestion_candidate:1",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.CANDIDATE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            "candidate requires evidence",
            evidence_refs=[],
        )

    decision = make_assimilation_decision(_candidate())
    assert decision.decision == AssimilationDecisionType.CANDIDATE
    assert decision.approval_required is False
    assert decision.approval_granted is False
    assert decision.grants_permission is False
    assert decision.grants_dominion_authority is False
    assert decision.creates_active_artifact is False
    assert decision.max_inferred_dominion_level == DominionLevel.D3_SIMULATE


def test_dominion_required_and_future_track_decisions_set_required_flags() -> None:
    dominion_candidate = _candidate(
        feasibility_status=DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW,
        proposed_internal_artifact_kind=InternalArtifactCandidateKind.NONE,
        blocked_reasons=[DigestionBlockReason.DANGEROUS_GATEWAY_SURFACE],
    )
    dominion_decision = make_assimilation_decision(dominion_candidate)

    assert dominion_decision.decision == AssimilationDecisionType.DOMINION_REQUIRED
    assert dominion_decision.dominion_review_required is True
    assert dominion_decision.grants_dominion_authority is False
    assert not isinstance(dominion_decision, DominionDecision)

    with pytest.raises(ValueError, match="dominion_review_required"):
        AssimilationDecision(
            "assimilation_decision:bad-dominion",
            "digestion_candidate:1",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.DOMINION_REQUIRED,
            InternalArtifactCandidateKind.NONE,
            "must set flag",
        )

    future = _candidate(
        feasibility_status=DigestionFeasibilityStatus.FUTURE_TRACK,
        proposed_internal_artifact_kind=InternalArtifactCandidateKind.NONE,
    )
    future_decision = make_assimilation_decision(future)
    assert future_decision.decision == AssimilationDecisionType.FUTURE_TRACK
    assert future_decision.future_gate_required is True

    with pytest.raises(ValueError, match="future_gate_required"):
        AssimilationDecision(
            "assimilation_decision:bad-future",
            "digestion_candidate:1",
            "target:external",
            "capability_observation_report:target:external",
            AssimilationDecisionType.FUTURE_TRACK,
            InternalArtifactCandidateKind.NONE,
            "must set flag",
        )


def test_reject_or_block_decision_requires_reason_and_remains_non_runtime() -> None:
    rejected_candidate = _candidate(
        feasibility_status=DigestionFeasibilityStatus.UNSAFE_TO_DIGEST,
        proposed_internal_artifact_kind=InternalArtifactCandidateKind.NONE,
        blocked_reasons=[DigestionBlockReason.RAW_OUTPUT_PERSISTENCE_RISK],
    )
    decision = make_assimilation_decision(rejected_candidate)

    assert decision.decision == AssimilationDecisionType.REJECT
    assert decision.grants_permission is False
    assert decision.grants_dominion_authority is False


def test_internalization_plan_is_plan_only_and_requires_guarantees() -> None:
    decision = make_assimilation_decision(_candidate())
    plan = make_internalization_plan(decision)

    assert plan is not None
    assert plan.no_execution_guarantee is True
    assert plan.no_runtime_registration_guarantee is True
    assert plan.creates_files is False
    assert plan.registers_runtime_artifact is False
    assert plan.executes is False
    assert "runtime registration prohibited" in plan.explicitly_out_of_scope

    with pytest.raises(ValueError, match="no_execution_guarantee"):
        InternalizationPlan(
            "internalization_plan:bad",
            decision.decision_id,
            decision.candidate_id,
            decision.target_id,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            ["Review only."],
            [],
            [],
            [],
            [],
            False,
            True,
        )
    with pytest.raises(ValueError, match="no_runtime_registration_guarantee"):
        InternalizationPlan(
            "internalization_plan:bad",
            decision.decision_id,
            decision.candidate_id,
            decision.target_id,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            ["Review only."],
            [],
            [],
            [],
            [],
            True,
            False,
        )
    with pytest.raises(ValueError, match="planned_steps"):
        InternalizationPlan(
            "internalization_plan:bad-step",
            decision.decision_id,
            decision.candidate_id,
            decision.target_id,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
            ["Execute the external tool."],
            [],
            [],
            [],
            [],
            True,
            True,
        )


def test_helper_mapping_for_read_only_and_manifest_like_patterns_is_candidate_only() -> None:
    skill = _descriptor(
        capability_id="capability:skill-manifest",
        name="Skill manifest pattern",
        kind=ExternalCapabilityKind.SKILL,
    )
    mission = _descriptor(
        capability_id="capability:scheduler",
        name="Scheduler mission manifest",
        kind=ExternalCapabilityKind.SCHEDULER,
    )
    result = _descriptor(
        capability_id="capability:result-envelope",
        name="Result envelope schema",
        kind=ExternalCapabilityKind.TOOL,
    )

    assert classify_digestion_candidate_from_capability(skill) == DigestionCandidateKind.SKILL_MANIFEST_PATTERN
    assert classify_digestion_candidate_from_capability(mission) == DigestionCandidateKind.MISSION_MANIFEST_PATTERN
    assert classify_digestion_candidate_from_capability(result) == DigestionCandidateKind.RESULT_ENVELOPE_PATTERN
    assert infer_internal_artifact_candidate_kind(DigestionCandidateKind.SKILL_MANIFEST_PATTERN) == InternalArtifactCandidateKind.INTERNAL_SKILL_CANDIDATE

    candidates = build_digestion_candidates_from_observation_report(_report([skill, mission, result]))
    assert len(candidates) == 3
    assert all(candidate.creates_internal_artifact is False for candidate in candidates)
    assert all(candidate.creates_dominion_target is False for candidate in candidates)


@pytest.mark.parametrize(
    ("risk", "expected_reason", "capability_kind", "active_kind"),
    [
        (
            ExternalRiskSignal.PROVIDER_INVOCATION_POSSIBLE,
            DigestionBlockReason.DANGEROUS_PROVIDER_SURFACE,
            ExternalCapabilityKind.PROVIDER,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
        (
            ExternalRiskSignal.GATEWAY_SEND_POSSIBLE,
            DigestionBlockReason.DANGEROUS_GATEWAY_SURFACE,
            ExternalCapabilityKind.GATEWAY_CHANNEL,
            InternalArtifactCandidateKind.INTERNAL_GATEWAY_MANIFEST_CANDIDATE,
        ),
        (
            ExternalRiskSignal.COMMAND_EXECUTION_POSSIBLE,
            DigestionBlockReason.DANGEROUS_COMMAND_SURFACE,
            ExternalCapabilityKind.COMMAND_SURFACE,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
        (
            ExternalRiskSignal.RPA_CONTROL_POSSIBLE,
            DigestionBlockReason.DANGEROUS_RPA_SURFACE,
            ExternalCapabilityKind.RPA_ACTION,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
        (
            ExternalRiskSignal.MEMORY_CONTAMINATION_POSSIBLE,
            DigestionBlockReason.MEMORY_CONTAMINATION_RISK,
            ExternalCapabilityKind.MEMORY_SURFACE,
            InternalArtifactCandidateKind.INTERNAL_MEMORY_SCHEMA_CANDIDATE,
        ),
        (
            ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE,
            DigestionBlockReason.DANGEROUS_NETWORK_SURFACE,
            ExternalCapabilityKind.TOOL,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
        (
            ExternalRiskSignal.CREDENTIAL_ACCESS_POSSIBLE,
            DigestionBlockReason.DANGEROUS_CREDENTIAL_SURFACE,
            ExternalCapabilityKind.TOOL,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
        (
            ExternalRiskSignal.BROWSER_AUTOMATION_POSSIBLE,
            DigestionBlockReason.DANGEROUS_BROWSER_SURFACE,
            ExternalCapabilityKind.BROWSER_ACTION,
            InternalArtifactCandidateKind.INTERNAL_TOOL_CONTRACT_CANDIDATE,
        ),
    ],
)
def test_dangerous_surfaces_do_not_become_active_internal_runtime(
    risk: ExternalRiskSignal,
    expected_reason: DigestionBlockReason,
    capability_kind: ExternalCapabilityKind,
    active_kind: InternalArtifactCandidateKind,
) -> None:
    descriptor = _descriptor(
        capability_id=f"capability:{risk.value}",
        name=f"{risk.value} capability",
        kind=capability_kind,
        risk_signals=[risk],
        effect_surfaces=infer_effect_surfaces_from_risk_signals([risk]),
        boundary_surfaces=[],
    )
    report = _report([descriptor])
    candidates = build_digestion_candidates_from_observation_report(report)
    decision = make_assimilation_decision(candidates[0])

    assert can_create_digestion_candidate_from_report(report) is True
    assert expected_reason in infer_digestion_block_reasons_from_observation(descriptor)
    assert is_dangerous_for_digestion(candidates[0]) is True
    assert candidates[0].feasibility_status == DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW
    assert candidates[0].proposed_internal_artifact_kind != active_kind
    assert decision.decision == AssimilationDecisionType.DOMINION_REQUIRED
    assert decision.grants_dominion_authority is False
    assert make_internalization_plan(decision) is None


def test_insufficient_evidence_defers_and_unknown_is_conservative() -> None:
    descriptor = _descriptor(
        capability_id="capability:unknown",
        name="Unknown capability",
        kind=ExternalCapabilityKind.UNKNOWN,
        observation_status=ExternalCapabilityObservationStatus.DECLARED,
        evidence_refs=[],
        confidence="declared_only",
    )
    report = _report([descriptor])
    candidates = build_digestion_candidates_from_observation_report(report)
    decision = make_assimilation_decision(candidates[0])

    assert classify_digestion_candidate_from_capability(descriptor) == DigestionCandidateKind.UNKNOWN
    assert candidates[0].feasibility_status == DigestionFeasibilityStatus.REQUIRES_REVIEW
    assert DigestionBlockReason.INSUFFICIENT_EVIDENCE in candidates[0].blocked_reasons
    assert decision.decision == AssimilationDecisionType.DEFER
    assert decision.grants_permission is False


def test_blocked_report_does_not_create_digestion_candidates() -> None:
    descriptor = _descriptor()
    report = CapabilityObservationReport(
        "capability_observation_report:blocked",
        "target:external",
        "inventory:target:external",
        "manifest",
        "source-ref:not-fetched",
        [descriptor],
        [ExternalEffectSurface.READ_ONLY],
        [ExternalBoundarySurface.DATA_BOUNDARY],
        [],
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        "low",
        evidence_refs=["evidence:manifest"],
        blocked_reasons=["trust boundary blocked"],
    )

    assert can_create_digestion_candidate_from_report(report) is False
    assert build_digestion_candidates_from_observation_report(report) == []


def test_d7_d8_d9_cannot_be_inferred_from_digestion_decision() -> None:
    candidate = _candidate(
        feasibility_status=DigestionFeasibilityStatus.REQUIRES_DOMINION_REVIEW,
        proposed_internal_artifact_kind=InternalArtifactCandidateKind.NONE,
        blocked_reasons=[DigestionBlockReason.DELEGATION_SURFACE_UNCLEAR],
    )
    decision = make_assimilation_decision(candidate)

    assert decision.max_inferred_dominion_level == DominionLevel.D3_SIMULATE
    assert decision.max_inferred_dominion_level not in {
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }
    assert decision.grants_permission is False
    assert decision.grants_dominion_authority is False

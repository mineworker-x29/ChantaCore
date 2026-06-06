from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    CapabilityObservationInput,
    CapabilityObservationReport,
    DominionAuthorityRequest,
    DominionDecision,
    DominionLevel,
    ExternalBoundarySurface,
    ExternalCapabilityDescriptor,
    ExternalCapabilityKind,
    ExternalCapabilityObservationStatus,
    ExternalEffectSurface,
    ExternalRiskSignal,
    ExternalTargetInventory,
    ExternalTargetKind,
    ExternalTargetRegistrationRequest,
    aggregate_capability_surfaces,
    aggregate_risk_signals,
    build_capability_observation_from_inventory,
    build_capability_observation_report,
    capability_observation_infers_dominion_level,
    capability_report_can_enter_digestion_review,
    capability_report_has_dangerous_surface,
    capability_report_requires_dominion_review,
    infer_boundary_surfaces_from_effects,
    infer_effect_surfaces_from_risk_signals,
    make_v030_contract,
    normalize_capability_kind,
    summarize_capability_observation,
)


def _descriptor(**overrides) -> ExternalCapabilityDescriptor:
    data = {
        "capability_id": "capability:read-docs",
        "target_id": "target:agent",
        "name": "Read docs",
        "kind": ExternalCapabilityKind.TOOL,
        "description": "Declared metadata-only docs reading capability",
        "observation_status": ExternalCapabilityObservationStatus.EVIDENCE_LINKED,
        "effect_surfaces": [ExternalEffectSurface.READ_ONLY],
        "boundary_surfaces": [ExternalBoundarySurface.DATA_BOUNDARY],
        "risk_signals": [],
        "declared_inputs": ["path_ref"],
        "declared_outputs": ["summary"],
        "evidence_refs": ["evidence:manifest"],
        "confidence": "low",
        "conflict_notes": [],
        "metadata": {"note": "not evidence"},
    }
    data.update(overrides)
    return ExternalCapabilityDescriptor(**data)


def _report(capabilities: list[ExternalCapabilityDescriptor]) -> CapabilityObservationReport:
    effects, boundaries = aggregate_capability_surfaces(capabilities)
    risks = aggregate_risk_signals(capabilities)
    return CapabilityObservationReport(
        "capability_observation_report:target:agent",
        "target:agent",
        "inventory:target:agent",
        "manifest",
        "manifest:local-ref",
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


def test_valid_descriptor_and_report_creation_are_non_executable() -> None:
    descriptor = _descriptor()
    report = _report([descriptor])
    summary = summarize_capability_observation(report)

    assert descriptor.grants_permission is False
    assert descriptor.executes is False
    assert descriptor.is_internal_skill is False
    assert report.grants_dominion_level is False
    assert report.creates_dominion_decision is False
    assert report.creates_internal_skill is False
    assert report.creates_dominion_target is False
    assert summary.grants_permission is False
    assert summary.runtime_ready is False
    assert summary.recommendation == "digestion_candidate_possible"


def test_descriptor_rejects_blank_ids_and_name() -> None:
    with pytest.raises(ValueError, match="capability_id"):
        _descriptor(capability_id="")
    with pytest.raises(ValueError, match="target_id"):
        _descriptor(target_id="")
    with pytest.raises(ValueError, match="name"):
        _descriptor(name=" ")


def test_evidence_linked_and_conflict_status_validate_supporting_fields() -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        _descriptor(evidence_refs=[], observation_status=ExternalCapabilityObservationStatus.EVIDENCE_LINKED)

    with pytest.raises(ValueError, match="conflict_notes"):
        _descriptor(
            capability_id="capability:conflict",
            observation_status=ExternalCapabilityObservationStatus.CONFLICT_DETECTED,
            conflict_notes=[],
        )

    conflict = _descriptor(
        capability_id="capability:conflict",
        observation_status=ExternalCapabilityObservationStatus.CONFLICT_DETECTED,
        conflict_notes=["manifest and docs disagree"],
    )
    assert conflict.grants_permission is False


def test_confidence_is_conservative_without_evidence_and_metadata_is_not_evidence() -> None:
    descriptor = _descriptor(
        capability_id="capability:metadata-only",
        evidence_refs=[],
        observation_status=ExternalCapabilityObservationStatus.DECLARED,
        confidence="declared_only",
        metadata={"evidence_refs": ["metadata:not-real-evidence"]},
    )
    assert descriptor.evidence_refs == []

    with pytest.raises(ValueError, match="confidence"):
        _descriptor(
            capability_id="capability:overconfident",
            evidence_refs=[],
            observation_status=ExternalCapabilityObservationStatus.DECLARED,
            confidence="high",
        )


def test_report_rejects_mismatched_capability_target_id() -> None:
    with pytest.raises(ValueError, match="target_ids"):
        _report([_descriptor(target_id="target:other")])


def test_risk_to_effect_and_boundary_mappings_cover_dangerous_surfaces() -> None:
    cases = [
        (ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE, ExternalEffectSurface.NETWORK_POSSIBLE, ExternalBoundarySurface.NETWORK_BOUNDARY),
        (ExternalRiskSignal.CREDENTIAL_ACCESS_POSSIBLE, ExternalEffectSurface.CREDENTIAL_REQUIRED, ExternalBoundarySurface.CREDENTIAL_BOUNDARY),
        (ExternalRiskSignal.COMMAND_EXECUTION_POSSIBLE, ExternalEffectSurface.COMMAND_POSSIBLE, ExternalBoundarySurface.COMMAND_BOUNDARY),
        (ExternalRiskSignal.PROVIDER_INVOCATION_POSSIBLE, ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE, ExternalBoundarySurface.PROVIDER_BOUNDARY),
        (ExternalRiskSignal.BROWSER_AUTOMATION_POSSIBLE, ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE, ExternalBoundarySurface.BROWSER_BOUNDARY),
        (ExternalRiskSignal.RPA_CONTROL_POSSIBLE, ExternalEffectSurface.RPA_CONTROL_POSSIBLE, ExternalBoundarySurface.RPA_BOUNDARY),
        (ExternalRiskSignal.GATEWAY_SEND_POSSIBLE, ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE, ExternalBoundarySurface.GATEWAY_BOUNDARY),
        (ExternalRiskSignal.DELEGATED_AGENT_POSSIBLE, ExternalEffectSurface.DELEGATION_POSSIBLE, ExternalBoundarySurface.DELEGATION_BOUNDARY),
    ]

    for risk, effect, boundary in cases:
        effects = infer_effect_surfaces_from_risk_signals([risk])
        boundaries = infer_boundary_surfaces_from_effects(effects)
        assert effect in effects
        assert boundary in boundaries


def test_report_aggregates_surfaces_and_risks_and_requires_review_not_execution() -> None:
    network = _descriptor(
        capability_id="capability:network",
        name="Network possible",
        risk_signals=[ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE],
        effect_surfaces=infer_effect_surfaces_from_risk_signals([ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE]),
        boundary_surfaces=[],
    )
    gateway = _descriptor(
        capability_id="capability:gateway",
        name="Gateway possible",
        risk_signals=[ExternalRiskSignal.GATEWAY_SEND_POSSIBLE],
        effect_surfaces=infer_effect_surfaces_from_risk_signals([ExternalRiskSignal.GATEWAY_SEND_POSSIBLE]),
        boundary_surfaces=[],
    )
    report = _report([network, gateway])

    assert ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE in report.aggregate_risk_signals
    assert ExternalRiskSignal.GATEWAY_SEND_POSSIBLE in report.aggregate_risk_signals
    assert ExternalEffectSurface.NETWORK_POSSIBLE in report.aggregate_effect_surfaces
    assert ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE in report.aggregate_effect_surfaces
    assert ExternalBoundarySurface.NETWORK_BOUNDARY in report.aggregate_boundary_surfaces
    assert ExternalBoundarySurface.GATEWAY_BOUNDARY in report.aggregate_boundary_surfaces
    assert report.network_need_observed is True
    assert report.gateway_surface_observed is True
    assert capability_report_has_dangerous_surface(report) is True
    assert capability_report_requires_dominion_review(report) is True
    assert capability_report_can_enter_digestion_review(report) is True
    assert summarize_capability_observation(report).recommendation == "dominion_review_required"
    assert capability_observation_infers_dominion_level(report) == DominionLevel.D3_SIMULATE


def test_blocked_or_future_track_report_cannot_enter_digestion_review() -> None:
    blocked = _descriptor(
        capability_id="capability:blocked",
        observation_status=ExternalCapabilityObservationStatus.BLOCKED,
    )
    report = _report([blocked])

    assert capability_report_can_enter_digestion_review(report) is False


def test_build_from_inventory_uses_refs_only_and_does_not_fetch_source_ref() -> None:
    inventory = ExternalTargetInventory()
    record = inventory.register(
        ExternalTargetRegistrationRequest(
            "target:hermes",
            ExternalTargetKind.EXTERNAL_AGENT_HARNESS,
            "Hermes docs reference",
            source_ref="https://example.invalid/not-fetched",
            declared_capabilities=["agent messaging"],
            evidence_refs=["evidence:provided-doc"],
            metadata={"source_ref_contents": "not fetched"},
        )
    )
    report = build_capability_observation_from_inventory(record)

    assert report.source_ref == "https://example.invalid/not-fetched"
    assert report.inventory_id == record.inventory_id
    assert report.evidence_refs == ["evidence:provided-doc"]
    assert report.capabilities[0].name == "agent messaging"
    assert report.creates_dominion_decision is False
    assert report.creates_internal_skill is False
    assert report.creates_dominion_target is False


def test_observation_input_and_report_do_not_grant_authority_or_create_decision() -> None:
    observation_input = CapabilityObservationInput(
        "target:agent",
        source_kind="documentation",
        source_ref="docs:agent",
        declared_capabilities=[],
        evidence_refs=[],
        metadata={"evidence": "not evidence"},
    )
    report = build_capability_observation_report(observation_input)

    assert observation_input.source_ref_fetched is False
    assert observation_input.executes is False
    assert not isinstance(report, DominionDecision)
    assert not isinstance(report, DominionAuthorityRequest)
    assert report.grants_dominion_level is False
    assert report.aggregate_effect_surfaces == [ExternalEffectSurface.NONE_OBSERVED]


def test_d7_d8_d9_cannot_be_inferred_from_capability_observation() -> None:
    report = _report(
        [
            _descriptor(
                capability_id="capability:network",
                name="Network preview claim",
                risk_signals=[ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE],
                effect_surfaces=[ExternalEffectSurface.NETWORK_POSSIBLE],
            ),
            _descriptor(
                capability_id="capability:delegate",
                name="Delegation claim",
                risk_signals=[ExternalRiskSignal.DELEGATED_AGENT_POSSIBLE],
                effect_surfaces=[ExternalEffectSurface.DELEGATION_POSSIBLE],
            ),
            _descriptor(
                capability_id="capability:gateway",
                name="Gateway claim",
                risk_signals=[ExternalRiskSignal.GATEWAY_SEND_POSSIBLE],
                effect_surfaces=[ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE],
            ),
        ]
    )

    assert capability_observation_infers_dominion_level(report) == DominionLevel.D3_SIMULATE
    assert capability_observation_infers_dominion_level(report) not in {
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }
    assert make_v030_contract().max_grantable_level == DominionLevel.D3_SIMULATE


def test_unknown_capability_kind_is_descriptive_only() -> None:
    assert normalize_capability_kind("unknown") == ExternalCapabilityKind.UNKNOWN
    descriptor = _descriptor(kind=ExternalCapabilityKind.UNKNOWN)
    assert descriptor.grants_permission is False
    assert descriptor.executes is False
    assert descriptor.is_internal_skill is False

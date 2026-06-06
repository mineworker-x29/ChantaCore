from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    ApprovalAuditRollbackCoverage,
    CertificationMatrixCoverage,
    DigestionCandidateCoverageMatrix,
    DominionAuthorityCoverageMatrix,
    DominionLevel,
    DominionTargetCoverageMatrix,
    ExternalCapabilityObservationCoverage,
    ExternalDelegationDryRunCoverage,
    ExternalDominionConsolidationStatus,
    ExternalDominionFoundationSnapshot,
    ExternalDominionGapRegister,
    ExternalDominionReleaseFlagSet,
    ExternalDominionReleaseManifest,
    ExternalDominionReleaseReadinessLevel,
    ExternalDominionRiskRegister,
    ExternalDominionV031HandoffPacket,
    ExternalDominionV0309ConsolidationHandoff,
    ExternalTargetCoverageMatrix,
    LimitedPreviewGateCoverage,
    V030ConsolidationAuditTrail,
    V030ConsolidationReport,
    build_consolidation_audit_trail,
    build_coverage_matrix,
    build_foundation_snapshot,
    build_gap_register,
    build_release_manifest,
    build_risk_register,
    build_v0309_release_flags,
    build_v030_consolidation_report,
    build_v031_handoff_packet,
    consolidation_preserves_no_execution,
    consolidation_report_is_not_runtime_ready,
    handoff_packet_is_v031_only,
    release_flags_preserve_runtime_false,
)


REQUIRED_VERSIONS = [f"v0.30.{index}" for index in range(0, 9)]
PROHIBITED_SURFACES = {
    "external_execution",
    "limited_preview_execution",
    "network",
    "credential",
    "command",
    "provider",
    "browser",
    "rpa",
    "gateway",
    "delegation",
    "packet_send",
    "rollback_execution",
    "retry_execution",
}


def _flags(**overrides) -> ExternalDominionReleaseFlagSet:
    data = {
        "flag_set_id": "flags:v0.30.9",
        "version": "v0.30.9",
        "external_dominion_control_plane_foundation_ready": True,
        "ready_for_v031_internal_triad_skill_foundation": True,
    }
    data.update(overrides)
    return ExternalDominionReleaseFlagSet(**data)


def _snapshot(**overrides) -> ExternalDominionFoundationSnapshot:
    data = {
        "snapshot_id": "snapshot:v0.30.9",
        "version": "v0.30.9",
        "release_name": "External Dominion Control Plane Foundation v1",
        "included_versions": list(REQUIRED_VERSIONS),
        "included_artifact_groups": ["target", "observation", "digestion", "dominion"],
        "release_flags": _flags(),
        "consolidation_status": ExternalDominionConsolidationStatus.CONSOLIDATED,
        "readiness_level": ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031,
        "summary": "Consolidation only; not runtime enablement.",
    }
    data.update(overrides)
    return ExternalDominionFoundationSnapshot(**data)


def _manifest(snapshot: ExternalDominionFoundationSnapshot | None = None, **overrides) -> ExternalDominionReleaseManifest:
    snapshot = snapshot or _snapshot()
    data = {
        "release_manifest_id": "manifest:v0.30.9",
        "version": "v0.30.9",
        "release_name": "External Dominion Control Plane Foundation v1",
        "snapshot_id": snapshot.snapshot_id,
        "included_versions": list(REQUIRED_VERSIONS),
        "included_docs": ["docs/versions/v0.30/v0.30.9_external_dominion_control_plane_consolidation.md"],
        "included_modules": ["consolidation"],
        "included_tests": ["tests/test_v0309_external_dominion_control_plane_consolidation.py"],
        "release_flags": snapshot.release_flags,
        "test_command": "py -m pytest tests/test_v0309_external_dominion_control_plane_consolidation.py",
    }
    data.update(overrides)
    return ExternalDominionReleaseManifest(**data)


def test_release_flag_set_preserves_no_runtime_readiness() -> None:
    flags = build_v0309_release_flags()

    assert flags.external_dominion_control_plane_foundation_ready is True
    assert flags.ready_for_v031_internal_triad_skill_foundation is True
    assert flags.ready_for_external_execution is False
    assert flags.ready_for_limited_preview_execution is False
    assert flags.limited_preview_execution_ready_now is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_rpa_runtime_control is False
    assert flags.ready_for_browser_runtime_control is False
    assert flags.ready_for_gateway_control is False
    assert flags.ready_for_external_agent_delegation_runtime is False
    assert flags.production_certified is False
    assert flags.live_adapter_certified is False
    assert flags.max_grantable_level == DominionLevel.D3_SIMULATE
    assert {
        DominionLevel.D4_EXECUTE_READ,
        DominionLevel.D5_EXECUTE_WRITE_PROPOSAL,
        DominionLevel.D6_EXECUTE_SANDBOX,
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }.issubset(set(flags.future_track_levels))
    assert release_flags_preserve_runtime_false(flags) is True

    with pytest.raises(ValueError, match="flag_set_id"):
        _flags(flag_set_id="")
    with pytest.raises(ValueError, match="v0.30.9"):
        _flags(version="v0.30.8")
    with pytest.raises(ValueError, match="ready_for_external_execution"):
        _flags(ready_for_external_execution=True)
    with pytest.raises(ValueError, match="ready_for_limited_preview_execution"):
        _flags(ready_for_limited_preview_execution=True)
    with pytest.raises(ValueError, match="limited_preview_execution_ready_now"):
        _flags(limited_preview_execution_ready_now=True)
    with pytest.raises(ValueError, match="ready_for_provider_invocation"):
        _flags(ready_for_provider_invocation=True)
    with pytest.raises(ValueError, match="ready_for_network_access"):
        _flags(ready_for_network_access=True)
    with pytest.raises(ValueError, match="ready_for_credential_access"):
        _flags(ready_for_credential_access=True)
    with pytest.raises(ValueError, match="ready_for_command_execution"):
        _flags(ready_for_command_execution=True)
    with pytest.raises(ValueError, match="ready_for_rpa_runtime_control"):
        _flags(ready_for_rpa_runtime_control=True)
    with pytest.raises(ValueError, match="ready_for_browser_runtime_control"):
        _flags(ready_for_browser_runtime_control=True)
    with pytest.raises(ValueError, match="ready_for_gateway_control"):
        _flags(ready_for_gateway_control=True)
    with pytest.raises(ValueError, match="ready_for_external_agent_delegation_runtime"):
        _flags(ready_for_external_agent_delegation_runtime=True)
    with pytest.raises(ValueError, match="production_certified"):
        _flags(production_certified=True)
    with pytest.raises(ValueError, match="live_adapter_certified"):
        _flags(live_adapter_certified=True)
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        _flags(max_grantable_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW)


def test_foundation_snapshot_includes_v030_line_without_runtime_enablement() -> None:
    snapshot = build_foundation_snapshot()

    assert all(version in snapshot.included_versions for version in REQUIRED_VERSIONS)
    assert snapshot.runtime_enablement is False
    assert consolidation_preserves_no_execution(snapshot) is True
    assert release_flags_preserve_runtime_false(snapshot.release_flags) is True

    with pytest.raises(ValueError, match="included_versions"):
        _snapshot(included_versions=["v0.30.8"])
    with pytest.raises(ValueError, match="summary"):
        _snapshot(summary="")


def test_v0308_consolidation_handoff_can_seed_snapshot_without_execution_readiness() -> None:
    handoff = ExternalDominionV0309ConsolidationHandoff(
        handoff_id="handoff:v0.30.8",
        target_id="target:external",
        candidate_id="candidate:1",
        preview_gate_report_id="preview_report:1",
        preview_decision_id="preview_decision:1",
        ready_for_v0309_consolidation=True,
        ready_for_limited_preview_execution=False,
        ready_for_execution=False,
        approved_for_v0309_consolidation=True,
        approved_for_limited_preview_execution=False,
        approved_for_execution=False,
        unresolved_requirements=[],
        limitations=[],
        evidence_refs=["evidence:v0308"],
        withdrawal_conditions=["handoff is treated as runtime readiness"],
    )

    snapshot = build_foundation_snapshot(consolidation_handoff=handoff)

    assert snapshot.metadata["source_v0308_handoff_id"] == "handoff:v0.30.8"
    assert snapshot.metadata["source_v0308_approved_for_consolidation"] is True
    assert snapshot.evidence_refs == ["evidence:v0308"]
    assert snapshot.release_flags.ready_for_external_execution is False
    assert snapshot.release_flags.ready_for_limited_preview_execution is False
    assert snapshot.runtime_enablement is False


def test_coverage_matrices_validate_refs_and_blocking_gaps() -> None:
    coverage_classes = [
        ExternalTargetCoverageMatrix,
        ExternalCapabilityObservationCoverage,
        DigestionCandidateCoverageMatrix,
        DominionTargetCoverageMatrix,
        DominionAuthorityCoverageMatrix,
        ExternalDelegationDryRunCoverage,
        ApprovalAuditRollbackCoverage,
        CertificationMatrixCoverage,
        LimitedPreviewGateCoverage,
    ]

    for cls in coverage_classes:
        coverage = build_coverage_matrix(
            cls,
            f"{cls.__name__}:coverage",
            covered_artifact_refs=["artifact:covered"],
            missing_artifact_refs=[],
            blocking_gaps=[],
        )
        assert isinstance(coverage, cls)
        assert coverage.coverage_complete is True
        assert coverage.runtime_readiness is False

        blocked = build_coverage_matrix(
            cls,
            f"{cls.__name__}:blocked",
            blocking_gaps=["missing required artifact"],
        )
        assert blocked.coverage_complete is False

    with pytest.raises(ValueError, match="coverage_id"):
        ExternalTargetCoverageMatrix(coverage_id="")
    with pytest.raises(TypeError, match="covered_artifact_refs"):
        ExternalTargetCoverageMatrix(coverage_id="coverage:bad", covered_artifact_refs="not-list")
    with pytest.raises(ValueError, match="coverage_complete"):
        ExternalTargetCoverageMatrix(
            coverage_id="coverage:bad",
            coverage_complete=True,
            blocking_gaps=["blocking gap"],
        )


def test_gap_and_risk_registers_are_non_permission_artifacts() -> None:
    gap_register = build_gap_register(non_blocking_gaps=["doc index pending"])
    risk_register = build_risk_register(unresolved_risks=["external runtime remains future-track"])

    assert gap_register.blocks_handoff is False
    assert "D4-D9 future-track" in gap_register.future_track_items
    assert PROHIBITED_SURFACES.issubset(set(risk_register.prohibited_runtime_surfaces))
    assert risk_register.proves_exploitability is False
    assert risk_register.grants_permission is False

    blocking = build_gap_register(blocking_gaps=["missing consolidation test"])
    assert blocking.blocks_handoff is True

    with pytest.raises(ValueError, match="D4-D9"):
        ExternalDominionGapRegister("gap:bad", "v0.30.9", future_track_items=["D4 only"])
    with pytest.raises(ValueError, match="runtime surfaces"):
        ExternalDominionRiskRegister(
            "risk:bad",
            "v0.30.9",
            prohibited_runtime_surfaces=["network"],
        )


def test_v031_handoff_packet_is_internal_triad_only_and_non_executing() -> None:
    snapshot = _snapshot()
    packet = build_v031_handoff_packet(snapshot)

    assert packet.target_version_track.startswith("v0.31")
    assert "observation" in " ".join(packet.internal_triad_focus)
    assert "digestion" in " ".join(packet.internal_triad_focus)
    assert "dominion" in " ".join(packet.internal_triad_focus)
    assert PROHIBITED_SURFACES.issubset(set(packet.prohibited_until_later_gate))
    assert packet.ready_for_v031 is True
    assert packet.ready_for_execution is False
    assert packet.is_implementation is False
    assert handoff_packet_is_v031_only(packet) is True

    blocked = build_v031_handoff_packet(snapshot, blocking_gaps=["blocking gap"])
    assert blocked.ready_for_v031 is False
    assert blocked.ready_for_execution is False

    with pytest.raises(ValueError, match="ready_for_execution"):
        ExternalDominionV031HandoffPacket(
            handoff_id="handoff:bad",
            source_version="v0.30.9",
            target_version_track="v0.31 Internal Triad Skill Foundation",
            source_snapshot_id=snapshot.snapshot_id,
            release_manifest_id=None,
            recommended_next_track="v0.31 Internal Triad Skill Foundation",
            recommended_next_release="v0.31.0",
            internal_triad_focus=["observation", "digestion", "dominion"],
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_v031"):
        ExternalDominionV031HandoffPacket(
            handoff_id="handoff:bad",
            source_version="v0.30.9",
            target_version_track="v0.31 Internal Triad Skill Foundation",
            source_snapshot_id=snapshot.snapshot_id,
            release_manifest_id=None,
            recommended_next_track="v0.31 Internal Triad Skill Foundation",
            recommended_next_release="v0.31.0",
            internal_triad_focus=["observation", "digestion", "dominion"],
            readiness_level=ExternalDominionReleaseReadinessLevel.NOT_READY,
            ready_for_v031=True,
        )


def test_release_manifest_is_not_production_release_or_runtime_readiness() -> None:
    snapshot = _snapshot()
    manifest = build_release_manifest(snapshot)

    assert all(version in manifest.included_versions for version in REQUIRED_VERSIONS)
    assert manifest.is_production_release is False
    assert manifest.runtime_readiness is False
    assert release_flags_preserve_runtime_false(manifest.release_flags) is True

    with pytest.raises(ValueError, match="included_versions"):
        _manifest(snapshot, included_versions=["v0.30.9"])


def test_consolidation_audit_trail_is_metadata_only() -> None:
    audit = build_consolidation_audit_trail()

    assert audit.no_execution_confirmed is True
    assert audit.runtime_readiness_flags_false_confirmed is True
    assert audit.d4_d9_future_track_confirmed is True
    assert audit.executes_audit is False

    with pytest.raises(ValueError, match="no_execution_confirmed"):
        V030ConsolidationAuditTrail(
            audit_trail_id="audit:bad",
            version="v0.30.9",
            reviewed_artifact_refs=[],
            reviewed_test_refs=[],
            reviewed_doc_refs=[],
            boundary_checks=[],
            negative_runtime_checks=[],
            no_execution_confirmed=False,
            runtime_readiness_flags_false_confirmed=True,
            d4_d9_future_track_confirmed=True,
        )
    with pytest.raises(ValueError, match="runtime_readiness_flags_false_confirmed"):
        V030ConsolidationAuditTrail(
            audit_trail_id="audit:bad",
            version="v0.30.9",
            reviewed_artifact_refs=[],
            reviewed_test_refs=[],
            reviewed_doc_refs=[],
            boundary_checks=[],
            negative_runtime_checks=[],
            no_execution_confirmed=True,
            runtime_readiness_flags_false_confirmed=False,
            d4_d9_future_track_confirmed=True,
        )
    with pytest.raises(ValueError, match="d4_d9_future_track_confirmed"):
        V030ConsolidationAuditTrail(
            audit_trail_id="audit:bad",
            version="v0.30.9",
            reviewed_artifact_refs=[],
            reviewed_test_refs=[],
            reviewed_doc_refs=[],
            boundary_checks=[],
            negative_runtime_checks=[],
            no_execution_confirmed=True,
            runtime_readiness_flags_false_confirmed=True,
            d4_d9_future_track_confirmed=False,
        )


def test_consolidation_report_is_v031_handoff_only_not_runtime_ready() -> None:
    snapshot = _snapshot()
    manifest = _manifest(snapshot)
    packet = build_v031_handoff_packet(snapshot, manifest.release_manifest_id)
    report = build_v030_consolidation_report(snapshot, manifest, packet)

    assert report.ready_for_v031 is True
    assert report.ready_for_execution is False
    assert report.runtime_enablement is False
    assert report.production_certification is False
    assert consolidation_report_is_not_runtime_ready(report) is True
    assert consolidation_preserves_no_execution(report) is True

    blocked = build_v030_consolidation_report(snapshot, manifest, packet, blocking_gaps=["missing required artifact"])
    assert blocked.ready_for_v031 is False
    assert blocked.ready_for_execution is False

    with pytest.raises(ValueError, match="ready_for_execution"):
        V030ConsolidationReport(
            report_id="report:bad",
            version="v0.30.9",
            release_name="External Dominion Control Plane Foundation v1",
            snapshot_id=snapshot.snapshot_id,
            release_manifest_id=manifest.release_manifest_id,
            handoff_id=packet.handoff_id,
            consolidation_status=ExternalDominionConsolidationStatus.CONSOLIDATED,
            readiness_level=ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031,
            summary="summary",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_v031"):
        V030ConsolidationReport(
            report_id="report:bad",
            version="v0.30.9",
            release_name="External Dominion Control Plane Foundation v1",
            snapshot_id=snapshot.snapshot_id,
            release_manifest_id=manifest.release_manifest_id,
            handoff_id=packet.handoff_id,
            consolidation_status=ExternalDominionConsolidationStatus.BLOCKED,
            readiness_level=ExternalDominionReleaseReadinessLevel.BLOCKED,
            summary="summary",
            blocked_items=["blocking gap"],
            ready_for_v031=True,
        )

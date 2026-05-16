import subprocess
import sys

from chanta_core.deep_self_introspection import (
    SelfCapabilityRecord,
    SelfCapabilityRegistryAwarenessService,
    SelfCapabilityRegistrySourceService,
    SelfCapabilityRegistryViewRequest,
    SelfCapabilityTruthCheckService,
)


def test_capability_registry_snapshot_builds_and_counts() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    assert snapshot.snapshot_id
    assert snapshot.total_count == len(snapshot.records)
    assert snapshot.implemented_count > 0
    assert snapshot.contract_only_count > 0
    assert snapshot.future_track_count == 0
    assert snapshot.dangerous_capability_count == 0
    assert snapshot.execution_enabled_count == 0
    assert snapshot.materialization_enabled_count == 0
    assert snapshot.canonical_promotion_enabled_count == 0
    assert snapshot.limitations


def test_snapshot_includes_required_registry_sources() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    layers = {record.layer for record in snapshot.records}
    assert "self_awareness" in layers
    assert "deep_self_introspection" in layers
    assert "internal_observation" in layers
    assert "internal_digestion" in layers
    assert any(record.skill_id == "skill:deep_self_capability_registry_view" for record in snapshot.records)
    assert any(record.skill_id == "skill:deep_self_capability_truth_check" for record in snapshot.records)


def test_external_candidates_are_forced_non_executable_future_track() -> None:
    source = SelfCapabilityRegistrySourceService(external_candidate_records=[_record("external", status="implemented")])
    records = source.load_registry_records()
    external = [record for record in records if record.capability_id == "external"][0]
    assert external.status == "future_track"
    assert external.execution_enabled is False
    assert external.materialization_enabled is False
    assert external.canonical_promotion_enabled is False


def test_request_filters_by_status_and_layer() -> None:
    service = SelfCapabilityRegistryAwarenessService()
    implemented = service.view_registry(SelfCapabilityRegistryViewRequest(status_filter="implemented"))
    assert implemented.records
    assert {record.status for record in implemented.records} == {"implemented"}
    self_awareness = service.view_registry(SelfCapabilityRegistryViewRequest(layer_filter="self_awareness"))
    assert self_awareness.records
    assert {record.layer for record in self_awareness.records} == {"self_awareness"}


def test_risk_gate_and_observability_views_build() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    assert len(snapshot.risk_views) == snapshot.total_count
    assert len(snapshot.gate_views) == snapshot.total_count
    assert len(snapshot.observability_views) == snapshot.total_count
    assert all(view.risk_level in {"none", "low", "medium", "high", "blocked"} for view in snapshot.risk_views)
    assert all(view.permission_grant_allowed is False for view in snapshot.gate_views)
    assert all(view.observability_status in {"complete", "partial", "missing"} for view in snapshot.observability_views)


def test_truth_check_passes_for_safe_registry() -> None:
    service = SelfCapabilityRegistryAwarenessService()
    report = service.truth_check()
    assert report.status == "passed"
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.registry_truth_summary["principle"] == "Capability truth > persona claim"


def test_truth_check_fails_when_dangerous_capability_is_enabled() -> None:
    snapshot = _snapshot_with_records([_record("danger", execution_enabled=True)])
    report = SelfCapabilityTruthCheckService().check_truth(snapshot)
    assert report.status == "failed"
    assert any(item.finding_type == "dangerous_capability_enabled" for item in report.findings)


def test_truth_check_fails_when_future_track_is_claimed_implemented() -> None:
    snapshot = _snapshot_with_records([_record("future", status="future_track")])
    report = SelfCapabilityTruthCheckService().check_truth(
        snapshot,
        optional_claims=[{"capability_id": "future", "claimed_status": "implemented"}],
    )
    assert report.status == "failed"
    assert any(item.finding_type == "future_track_claimed_as_implemented" for item in report.findings)


def test_truth_check_fails_when_contract_only_is_executable() -> None:
    snapshot = _snapshot_with_records([_record("contract", status="contract_only", execution_enabled=True)])
    report = SelfCapabilityTruthCheckService().check_truth(snapshot)
    assert report.status == "failed"
    assert any(item.finding_type == "contract_only_claimed_as_executable" for item in report.findings)


def test_truth_check_fails_when_candidate_only_is_materialized_or_promoted() -> None:
    snapshot = _snapshot_with_records(
        [
            _record(
                "candidate",
                candidate_only=True,
                materialization_enabled=True,
                canonical_promotion_enabled=True,
            )
        ]
    )
    report = SelfCapabilityTruthCheckService().check_truth(snapshot)
    assert report.status == "failed"
    assert any(item.finding_type == "candidate_only_claimed_as_materialized" for item in report.findings)


def test_optional_claim_unknown_capability_is_detected() -> None:
    snapshot = _snapshot_with_records([_record("known")])
    report = SelfCapabilityTruthCheckService().check_truth(
        snapshot,
        optional_claims=[{"capability_id": "unknown", "claimed_status": "implemented"}],
    )
    assert report.status == "warning"
    assert any(item.finding_type == "unknown_capability_claim" for item in report.findings)


def test_missing_gate_and_observability_are_reported() -> None:
    snapshot = _snapshot_with_records([_record("nogate", gate_contract_ref=None, ocel_object_types=[])])
    report = SelfCapabilityTruthCheckService().check_truth(snapshot)
    assert report.status == "failed"
    assert report.missing_gate_count == 1
    assert report.missing_observability_count == 1
    assert any(item.finding_type == "implemented_without_ocel_mapping" for item in report.findings)
    assert any(item.finding_type == "implemented_without_gate" for item in report.findings)


def test_no_registry_mutation_permission_grant_or_skill_enablement_occurs() -> None:
    source = SelfCapabilityRegistrySourceService()
    before = [record.to_dict() for record in source.load_registry_records()]
    after = [record.to_dict() for record in source.load_registry_records()]
    assert before == after
    assert all(record["execution_enabled"] is False for record in after)
    assert all(record["canonical_promotion_enabled"] is False for record in after)


def test_pig_and_ocpx_projection_build() -> None:
    service = SelfCapabilityRegistryAwarenessService()
    pig = service.build_pig_report()
    assert pig["version"] == "v0.21.1"
    assert pig["subject"] == "capability_registry"
    assert pig["principle"] == "Capability truth > persona claim"
    assert "implemented_count" in pig["capability_truth"]
    assert "contract_only_count" in pig["capability_truth"]
    assert "future_track_count" in pig["capability_truth"]
    assert pig["capability_truth"]["dangerous_capability_count"] == 0
    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "self_capability_registry_awareness"
    assert "SelfAwarenessReleaseState" in ocpx["source_read_models"]
    assert "DeepSelfIntrospectionContractState" in ocpx["source_read_models"]
    assert "SelfCapabilityRegistryState" in ocpx["target_read_models"]
    assert "SelfCapabilityTruthState" in ocpx["target_read_models"]
    assert "SelfCapabilityRiskState" in ocpx["target_read_models"]
    assert "SelfCapabilityContradictionState" in ocpx["target_read_models"]


def test_cli_capability_views_work() -> None:
    commands = [
        ["deep-self", "capability", "registry"],
        ["deep-self", "capability", "registry", "--status", "implemented"],
        ["deep-self", "capability", "registry", "--layer", "self_awareness"],
        ["deep-self", "capability", "truth-check"],
        ["deep-self", "capability", "risks"],
        ["deep-self", "capability", "observability"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "Self-Capability Registry Awareness" in result.stdout
        assert "Capability truth > persona claim" in result.stdout
        assert "dangerous_capability_count=" in result.stdout
        assert "execution_enabled_count=" in result.stdout
        assert "materialization_enabled_count=" in result.stdout
        assert "canonical_promotion_enabled_count=" in result.stdout
        assert "raw_file_content_printed=False" in result.stdout
        assert "private_full_paths_printed=False" in result.stdout
        assert "raw_secrets_printed=False" in result.stdout


def _record(
    capability_id: str,
    *,
    status: str = "implemented",
    execution_enabled: bool = False,
    candidate_only: bool = False,
    materialization_enabled: bool = False,
    canonical_promotion_enabled: bool = False,
    gate_contract_ref: str | None = "gate",
    ocel_object_types: list[str] | None = None,
) -> SelfCapabilityRecord:
    return SelfCapabilityRecord(
        capability_id=capability_id,
        skill_id=f"skill:{capability_id}",
        layer="test",
        name=capability_id,
        description="test record",
        status=status,
        introduced_in="test",
        execution_enabled=execution_enabled,
        materialization_enabled=materialization_enabled,
        canonical_promotion_enabled=canonical_promotion_enabled,
        read_only=not execution_enabled,
        candidate_only=candidate_only,
        effect_types=["read_only_observation"],
        risk_profile_ref="risk",
        gate_contract_ref=gate_contract_ref,
        observability_ref="observability",
        ocel_object_types=["capability_record"] if ocel_object_types is None else ocel_object_types,
        ocel_event_types=["deep_self_capability_registry_snapshot_created"],
        ocel_relation_types=["contains_capability"],
        source_refs=[{"source": "test"}],
        evidence_refs=[{"evidence": "test"}],
    )


def _snapshot_with_records(records: list[SelfCapabilityRecord]):
    service = SelfCapabilityRegistryAwarenessService(source_service=SelfCapabilityRegistrySourceService())
    risk_views = service.risk_service.build_risk_views(records)
    gate_views = service.gate_service.build_gate_views(records)
    observability_views = service.observability_service.build_observability_views(records)
    request = SelfCapabilityRegistryViewRequest()
    from chanta_core.deep_self_introspection import SelfCapabilityRegistrySnapshot
    from chanta_core.utility.time import utc_now_iso

    return SelfCapabilityRegistrySnapshot(
        snapshot_id="snapshot:test",
        created_at=utc_now_iso(),
        request=request,
        records=records,
        risk_views=risk_views,
        gate_views=gate_views,
        observability_views=observability_views,
        total_count=len(records),
        implemented_count=sum(1 for item in records if item.status == "implemented"),
        contract_only_count=sum(1 for item in records if item.status == "contract_only"),
        stub_count=sum(1 for item in records if item.status == "stub"),
        blocked_count=sum(1 for item in records if item.status == "blocked"),
        future_track_count=sum(1 for item in records if item.status == "future_track"),
        dangerous_capability_count=sum(1 for item in risk_views if item.dangerous_capability),
        execution_enabled_count=sum(1 for item in records if item.execution_enabled),
        materialization_enabled_count=sum(1 for item in records if item.materialization_enabled),
        canonical_promotion_enabled_count=sum(1 for item in records if item.canonical_promotion_enabled),
        limitations=[],
    )

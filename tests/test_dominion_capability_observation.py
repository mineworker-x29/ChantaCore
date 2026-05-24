from __future__ import annotations

import subprocess
import sys

from chanta_core.internal_dominion import (
    CAPABILITY_OBSERVATION_NEXT_STEP,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    ActionVerbNormalizer,
    CapabilityBoundaryDescriptor,
    CapabilityObservationDigestReportService,
    CapabilityObservationSourceService,
    CapabilityRiskProfile,
    CapabilitySchemaDescriptor,
    DominionCapabilityObservationRequest,
    ExternalCapabilityCandidate,
    ExternalCapabilityDescriptor,
    InternalDominionRegistryService,
)


def _request(items: list[dict]) -> DominionCapabilityObservationRequest:
    return DominionCapabilityObservationRequest(source_refs=[{"items": items}])


def test_capability_doc_records_v0_23_2_identity_and_boundaries() -> None:
    text = open("docs/versions/v0.23.2_capability_observation_digestion.md", encoding="utf-8").read()

    assert "Capability Observation & Digestion for Dominion" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Capability observation is not provider API discovery" in text
    assert "Capability digestion is not execution" in text
    assert "Capability candidate is not control request" in text
    assert "Capability candidate is not dispatch" in text
    assert "v0.23.3 Control Request & Action Candidate" in text


def test_capability_report_builds_and_counts_candidates() -> None:
    report = CapabilityObservationDigestReportService().build_report(
        _request(
            [
                {
                    "kind": "capability",
                    "descriptor_id": "descriptor:read",
                    "capability_name": "Read status",
                    "capability_type": "status",
                    "runtime_id": "runtime:declared-local",
                    "provider_ref_id": "provider:declared-local-runtime",
                    "control_surface_id": "surface:manual-only",
                    "declared_action_verbs": ["observe"],
                    "declared_input_schema_ref": {"required_fields": [], "optional_fields": ["target"]},
                    "declared_output_schema_ref": {"required_fields": ["status"]},
                    "environment": "local",
                },
                {
                    "kind": "capability",
                    "descriptor_id": "descriptor:prod",
                    "capability_name": "Production update",
                    "capability_type": "workflow_action",
                    "declared_action_verbs": ["update"],
                    "declared_input_schema_ref": {"required_fields": ["business_id"]},
                    "environment": "production",
                    "dispatch_supported": True,
                },
            ]
        )
    )

    assert report.descriptor_count == 2
    assert report.candidate_count == 2
    assert report.read_only_count == 1
    assert report.mutating_count == 1
    assert report.production_impacting_count == 1
    assert report.finding_count >= 1
    assert report.next_required_step == CAPABILITY_OBSERVATION_NEXT_STEP
    assert report.snapshot.dispatch_enabled is False
    assert report.snapshot.external_runtime_touched is False
    assert report.snapshot.provider_api_call_performed is False
    assert report.snapshot.credential_exposed is False


def test_capability_sources_are_sanitized_static_descriptors() -> None:
    source = CapabilityObservationSourceService().load_sources(
        DominionCapabilityObservationRequest(
            source_type="operator_input",
            source_refs=[{"credential_value": "hidden", "private_full_path": "hidden", "name": "descriptor"}],
        )
    )[0]

    assert source.source_type == "operator_input"
    assert source.raw_descriptor_included is False
    assert source.credential_values_included is False
    assert source.private_full_paths_included is False
    assert source.provider_api_call_performed is False
    assert source.external_runtime_touched is False
    assert "credential_value" not in source.source_ref


def test_descriptor_verb_schema_boundary_risk_and_candidate_models() -> None:
    descriptor = ExternalCapabilityDescriptor(
        descriptor_id="descriptor:model",
        capability_name="Model capability",
        capability_type="api_action",
        provider_ref_id="provider:p1",
        runtime_id="runtime:r1",
        agent_id="agent:a1",
        tool_id="tool:t1",
        system_id="system:s1",
        control_surface_id="surface:c1",
        declared_action_verbs=["observe", "delete"],
        dispatch_supported=True,
    )
    verbs = ActionVerbNormalizer().normalize_verbs(descriptor)
    input_schema = CapabilitySchemaDescriptor(
        "schema:in",
        descriptor.descriptor_id,
        "input",
        True,
        "declared_descriptor",
        sensitive_fields=["credential_ref"],
        credential_fields_present=True,
    )
    output_schema = CapabilitySchemaDescriptor("schema:out", descriptor.descriptor_id, "output", True, "declared_descriptor")
    boundary = CapabilityBoundaryDescriptor(
        "boundary:1",
        descriptor.descriptor_id,
        "production",
        production_impacting=True,
        credential_sensitive=True,
        mutating=True,
        destructive=True,
        external_system_touch_required=True,
        status_tracking_required=True,
        outcome_record_required=True,
        cancel_or_stop_required=True,
        idempotency_key_required=True,
        rate_limit_required=True,
    )
    risk = CapabilityRiskProfile(
        "risk:1",
        descriptor.descriptor_id,
        "destructive",
        ["delete"],
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    )
    candidate = ExternalCapabilityCandidate(
        "candidate:1",
        descriptor.descriptor_id,
        descriptor.provider_ref_id,
        descriptor.runtime_id,
        descriptor.capability_name,
        descriptor.capability_type,
        verbs,
        {"schema_id": input_schema.schema_id},
        {"schema_id": output_schema.schema_id},
        {"boundary_id": boundary.boundary_id},
        {"risk_profile_id": risk.risk_profile_id},
    )

    assert descriptor.dispatch_supported is True
    assert descriptor.dispatch_enabled_v0_23_2 is False
    assert verbs[0].risk_class == "read_only"
    assert verbs[1].risk_class == "destructive"
    assert input_schema.credential_fields_present is True
    assert input_schema.raw_schema_included is False
    assert boundary.dispatch_allowed_in_v0_23_2 is False
    assert risk.dispatch_enabled is False
    assert candidate.candidate_status == "candidate_only"
    assert candidate.control_request_created is False
    assert candidate.control_plan_created is False
    assert candidate.preflight_checked is False
    assert candidate.human_gate_opened is False
    assert candidate.dispatch_enabled is False
    assert candidate.dispatched is False
    assert candidate.provider_api_call_performed is False
    assert candidate.external_runtime_touched is False
    assert candidate.credential_exposed is False


def test_capability_findings_cover_policy_risks() -> None:
    report = CapabilityObservationDigestReportService().build_report(
        _request(
            [
                {
                    "kind": "capability",
                    "descriptor_id": "descriptor:bad",
                    "capability_name": "self_execution vendor hardcoding",
                    "description": "requires GrowthKernel dependency and vendor hardcoding",
                    "capability_type": "unknown",
                    "declared_action_verbs": ["mystery"],
                    "declared_input_schema_ref": {"required_fields": ["credential_token"]},
                    "dispatch_supported": True,
                }
            ]
        )
    )
    finding_types = {item.finding_type for item in report.snapshot.findings}

    assert "unknown_capability_type" in finding_types
    assert "unknown_action_verb" in finding_types
    assert "input_schema_missing" not in finding_types
    assert "output_schema_missing" in finding_types
    assert "credential_field_detected" in finding_types
    assert "status_tracking_missing" in finding_types
    assert "outcome_mapping_missing" in finding_types
    assert "provider_adapter_required" in finding_types
    assert "self_execution_legacy_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types


def test_capability_ocel_pig_ocpx_and_skill_statuses() -> None:
    reports = CapabilityObservationDigestReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_capability_observation_request",
        "capability_observation_source",
        "external_capability_descriptor",
        "dominion_action_verb_descriptor",
        "capability_schema_descriptor",
        "capability_boundary_descriptor",
        "capability_risk_profile",
        "capability_digestion_rule",
        "capability_digestion_result",
        "external_capability_candidate",
        "capability_observation_finding",
        "capability_observation_digest_snapshot",
        "capability_observation_digest_report",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    assert "dominion_capability_observation_requested" in DOMINION_OCEL_EVENT_TYPES
    assert "external_capability_candidate_created" in DOMINION_OCEL_EVENT_TYPES
    assert "produces_external_capability_candidate" in DOMINION_OCEL_RELATION_TYPES
    assert "candidate_requires_future_control_plan" in DOMINION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.23.2"
    assert pig["subject"] == "capability_observation_digestion"
    assert pig["safety_boundary"]["dispatch_enabled"] is False
    assert pig["safety_boundary"]["control_request_created"] is False
    assert pig["safety_boundary"]["control_plan_created"] is False
    assert ocpx["state"] == "dominion_capability_candidates_digested"
    assert "ExternalCapabilityCandidateState" in ocpx["target_read_models"]
    assert skills["skill:dominion_capability_observe"]["status"] == "read_only"
    assert skills["skill:dominion_capability_digest"]["status"] == "read_only"
    assert skills["skill:dominion_control_request_create"]["status"] == "candidate_only"


def test_capability_cli_views_are_sanitized() -> None:
    for args in [
        ["capability", "observe"],
        ["capability", "digest"],
        ["capability", "report", "--report-id", "capability_observation_digest_report:v0.23.2"],
        ["capability", "candidates"],
        ["capability", "descriptors"],
        ["capability", "risks"],
        ["capability", "findings"],
    ]:
        completed = subprocess.run(
            [sys.executable, "-m", "chantacore.cli", "dominion", *args],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "descriptor_count=" in completed.stdout
        assert "candidate_count=" in completed.stdout
        assert "read_only_count=" in completed.stdout
        assert "mutating_count=" in completed.stdout
        assert "production_impacting_count=" in completed.stdout
        assert "credential_sensitive_count=" in completed.stdout
        assert "dispatch_enabled=false" in completed.stdout
        assert "external_runtime_touched=false" in completed.stdout
        assert "provider_api_call_performed=false" in completed.stdout
        assert "credential_exposed=false" in completed.stdout
        assert "next_required_step=v0.23.3 Control Request & Action Candidate" in completed.stdout
        assert "raw_descriptor_printed=False" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "private_full_paths_printed=False" in completed.stdout

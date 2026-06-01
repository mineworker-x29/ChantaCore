from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    DURABLE_MEMORY_REGISTRY_CONDITIONAL_EFFECT_TYPES,
    DURABLE_MEMORY_REGISTRY_EFFECT_TYPES,
    DURABLE_MEMORY_REGISTRY_EVENT_TYPES,
    DURABLE_MEMORY_REGISTRY_FORBIDDEN_EFFECT_TYPES,
    DURABLE_MEMORY_REGISTRY_OBJECT_TYPES,
    DurableMemoryDryRunRecord,
    DurableMemoryRecord,
    DurableMemoryRecordPreview,
    DurableMemoryRegistry,
    DurableMemoryRegistryEntry,
    DurableMemoryRegistryFinding,
    DurableMemoryRegistryIntegrityReport,
    DurableMemoryRegistryPolicy,
    DurableMemoryRegistryReport,
    DurableMemoryRegistryReportService,
    DurableMemoryWriteBlockedRecord,
    DurableMemoryWriteDecision,
    DurableMemoryWriteGate,
    DurableMemoryWritePolicy,
    DurableMemoryWriteRequest,
    MemoryRecordAuditTrail,
    MemoryRecordConflictMarker,
    MemoryRecordEvidenceIndex,
    MemoryRecordForgetRevokeBinding,
    MemoryRecordLifecyclePolicy,
    MemoryRecordPrivacyBoundary,
    MemoryRecordProvenance,
    MemoryRecordScope,
    MemoryRecordStatus,
    MemoryRecordVersion,
)


def _parts() -> dict:
    return DurableMemoryRegistryReportService().build_all_parts()


def _write_parts() -> dict:
    return DurableMemoryRegistryReportService().build_all_parts(
        release_hygiene_gate_passed=True,
        runtime_data_hygiene_gate_passed=True,
        requested_write_mode="write_if_gate_passed",
    )


def test_durable_memory_registry_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["write_policy"], DurableMemoryWritePolicy)
    assert isinstance(parts["registry_policy"], DurableMemoryRegistryPolicy)
    assert isinstance(parts["write_request"], DurableMemoryWriteRequest)
    assert isinstance(parts["write_gate"], DurableMemoryWriteGate)
    assert isinstance(parts["write_decision"], DurableMemoryWriteDecision)
    assert isinstance(parts["dry_run_records"][0], DurableMemoryDryRunRecord)
    assert isinstance(parts["record_previews"][0], DurableMemoryRecordPreview)
    assert isinstance(parts["registry"], DurableMemoryRegistry)
    assert isinstance(parts["scope"], MemoryRecordScope)
    assert isinstance(parts["provenance"], MemoryRecordProvenance)
    assert isinstance(parts["evidence_index"], MemoryRecordEvidenceIndex)
    assert isinstance(parts["lifecycle_policy"], MemoryRecordLifecyclePolicy)
    assert isinstance(parts["version_info"], MemoryRecordVersion)
    assert isinstance(parts["status_record"], MemoryRecordStatus)
    assert isinstance(parts["privacy_boundary"], MemoryRecordPrivacyBoundary)
    assert isinstance(parts["conflict_markers"][0], MemoryRecordConflictMarker)
    assert isinstance(parts["forget_revoke_binding"], MemoryRecordForgetRevokeBinding)
    assert isinstance(parts["audit_trail"], MemoryRecordAuditTrail)
    assert isinstance(parts["integrity_report"], DurableMemoryRegistryIntegrityReport)
    assert isinstance(parts["findings"][0], DurableMemoryRegistryFinding)
    assert isinstance(parts["report"], DurableMemoryRegistryReport)


def test_write_and_registry_policies_are_gated() -> None:
    parts = _parts()
    write_policy = parts["write_policy"]
    registry_policy = parts["registry_policy"]

    assert write_policy.version == "v0.27.5"
    assert write_policy.layer == "memory_candidate_continuity"
    assert write_policy.durable_memory_record_creation_enabled is True
    assert write_policy.durable_memory_registry_enabled is True
    assert write_policy.persistent_memory_write_conditionally_enabled is True
    assert write_policy.persistent_memory_write_requires_write_gate is True
    assert write_policy.release_hygiene_gate_required_for_persistent_write is True
    assert write_policy.runtime_data_hygiene_required_for_persistent_write is True
    assert write_policy.promote_decision_required is True
    assert write_policy.evidence_bundle_required is True
    assert write_policy.score_required is True
    assert write_policy.source_refs_required is True
    assert write_policy.scope_required is True
    assert write_policy.lifecycle_policy_required is True
    assert write_policy.forget_revoke_path_required is True
    assert write_policy.audit_trail_required is True
    assert write_policy.provenance_required is True
    assert write_policy.evidence_index_required is True
    assert write_policy.privacy_boundary_required is True
    assert write_policy.dry_run_allowed_when_gate_missing is True
    assert write_policy.no_write_allowed is True
    assert write_policy.automatic_write_forbidden is True
    assert write_policy.persona_mutation_forbidden is True
    assert write_policy.behavior_policy_mutation_forbidden is True
    assert write_policy.raw_transcript_memory_forbidden is True
    assert write_policy.raw_provider_output_memory_forbidden is True
    assert write_policy.raw_secret_memory_forbidden is True
    assert write_policy.credential_memory_forbidden is True
    assert write_policy.private_full_path_memory_forbidden is True
    assert write_policy.pig_guidance_is_not_memory_authority is True
    assert write_policy.provider_invocation_enabled_now is False
    assert write_policy.command_execution_enabled_now is False
    assert write_policy.safety_bypass_enabled_now is False
    assert write_policy.session_continuity_injection_enabled_now is False
    assert write_policy.llm_judge_as_sole_write_authority_forbidden is True
    assert registry_policy.registry_enabled is True
    assert registry_policy.registry_is_not_persona is True
    assert registry_policy.registry_is_not_behavior_policy is True
    assert registry_policy.registry_allows_only_gated_records is True
    assert registry_policy.registry_blocks_raw_memory is True


def test_default_write_gate_dry_runs_when_hygiene_missing() -> None:
    parts = _parts()
    gate = parts["write_gate"]
    decision = parts["write_decision"]
    dry_run = parts["dry_run_records"][0]
    report = parts["report"]

    assert gate.promotion_decision_present is True
    assert gate.promotion_decision_is_promote is True
    assert gate.candidate_ref_present is True
    assert gate.evidence_bundle_present is True
    assert gate.score_ref_present is True
    assert gate.source_refs_present is True
    assert gate.scope_present is True
    assert gate.lifecycle_or_expiry_present is True
    assert gate.forget_revoke_path_present is True
    assert gate.audit_ready is True
    assert gate.provenance_ready is True
    assert gate.evidence_index_ready is True
    assert gate.privacy_boundary_passed is True
    assert gate.contradiction_review_passed_or_not_required is True
    assert gate.release_hygiene_gate_passed is False
    assert gate.runtime_data_hygiene_gate_passed is False
    assert gate.raw_memory_blockers_absent is True
    assert gate.gate_status == "dry_run_only"
    assert gate.may_create_durable_record is True
    assert gate.may_write_persistent_memory is False
    assert decision.decision_type == "dry_run_only"
    assert decision.creates_durable_record is False
    assert decision.updates_registry is False
    assert decision.writes_persistent_memory is False
    assert dry_run.would_create_record is True
    assert dry_run.actual_durable_record_created is False
    assert dry_run.actual_persistent_memory_written is False
    assert report.durable_record_count == 0
    assert report.registry_entry_count == 0
    assert report.dry_run_count == 1
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.durable_registry_updated is False


def test_durable_record_and_registry_entry_build_only_when_gate_passes() -> None:
    parts = _write_parts()
    gate = parts["write_gate"]
    decision = parts["write_decision"]
    record = parts["durable_memory_records"][0]
    entry = parts["registry_entries"][0]
    registry = parts["registry"]
    report = parts["report"]

    assert gate.gate_status == "passed"
    assert gate.may_create_durable_record is True
    assert gate.may_write_persistent_memory is True
    assert decision.decision_type == "write_durable_memory"
    assert decision.creates_durable_record is True
    assert decision.updates_registry is True
    assert decision.writes_persistent_memory is True
    assert isinstance(record, DurableMemoryRecord)
    assert isinstance(entry, DurableMemoryRegistryEntry)
    assert record.refs_only is True
    assert record.candidate_ref
    assert record.promotion_decision_record_ref
    assert record.title
    assert record.summary
    assert record.memory_type in {
        "task_preference",
        "workflow_preference",
        "project_state",
        "decision_pattern",
        "skill_usage_pattern",
        "provider_route_pattern",
        "approval_preference",
        "failure_pattern",
        "context_summary",
        "long_task_continuity",
        "user_instruction",
        "system_boundary",
        "do_nothing_preference",
        "safety_preference",
        "unknown",
    }
    assert record.status in {"promoted", "active", "superseded", "revoked", "forgotten", "expired", "archived", "blocked"}
    assert record.scope.scope_status == "valid"
    assert record.provenance.provenance_complete is True
    assert record.evidence_index.index_status == "ready"
    assert record.lifecycle_policy.lifecycle_status == "ready"
    assert record.version_info.content_version == 1
    assert record.privacy_boundary.privacy_boundary_status == "passed"
    assert record.conflict_markers[0].conflict_level == "none"
    assert record.forget_revoke_binding.binding_status == "ready"
    assert entry.memory_record_id == record.memory_record_id
    assert entry.entry_status == "active"
    assert registry.registry_is_persona is False
    assert registry.registry_is_behavior_policy is False
    assert registry.entry_count == 1
    assert registry.active_count == 1
    assert report.durable_record_count == 1
    assert report.registry_entry_count == 1
    assert report.persistent_memory_written is True
    assert report.durable_memory_written is True
    assert report.durable_registry_updated is True


def test_record_components_and_integrity_are_refs_only_and_non_mutating() -> None:
    parts = _write_parts()
    record = parts["durable_memory_records"][0]
    integrity = parts["integrity_report"]

    assert record.raw_transcript_included is False
    assert record.raw_provider_output_included is False
    assert record.raw_secret_included is False
    assert record.credential_included is False
    assert record.private_full_path_included is False
    assert record.persona_mutation is False
    assert record.behavior_policy_mutation is False
    assert record.provider_invoked is False
    assert record.command_executed is False
    assert record.safety_gate_bypassed is False
    assert record.evidence_index.raw_evidence_included is False
    assert record.lifecycle_policy.revoke_allowed is True
    assert record.lifecycle_policy.forget_allowed is True
    assert record.lifecycle_policy.archive_allowed is True
    assert record.forget_revoke_binding.revoke_supported is True
    assert record.forget_revoke_binding.forget_supported is True
    assert record.forget_revoke_binding.forget_executed_now is False
    assert record.forget_revoke_binding.revoke_executed_now is False
    assert integrity.missing_provenance_count == 0
    assert integrity.missing_evidence_index_count == 0
    assert integrity.missing_scope_count == 0
    assert integrity.missing_lifecycle_count == 0
    assert integrity.missing_forget_revoke_binding_count == 0
    assert integrity.raw_memory_violation_count == 0
    assert integrity.persona_mutation_count == 0
    assert integrity.behavior_policy_mutation_count == 0
    assert integrity.provider_invocation_count == 0
    assert integrity.command_execution_count == 0
    assert integrity.safety_bypass_count == 0
    assert integrity.integrity_status == "passed"


def test_report_pig_ocpx_and_cli_outputs() -> None:
    service = DurableMemoryRegistryReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.ready_for_v0_27_6 is True
    assert report.ready_for_v0_28 is False
    assert report.write_gate_created is True
    assert report.write_decision_created is True
    assert report.registry_created is True
    assert report.audit_trail_created is True
    assert report.integrity_report_created is True
    assert report.session_continuity_injected is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_memory_created is False
    assert report.raw_provider_output_memory_created is False
    assert report.raw_secret_memory_created is False
    assert report.credential_memory_created is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.6 Session Continuity Context Builder"
    assert "durable_memory_write_gate" in DURABLE_MEMORY_REGISTRY_OBJECT_TYPES
    assert "durable_memory_write_gate_evaluated" in DURABLE_MEMORY_REGISTRY_EVENT_TYPES
    assert "durable_memory_write_gate_evaluated" in DURABLE_MEMORY_REGISTRY_EFFECT_TYPES
    assert "persistent_memory_written" in DURABLE_MEMORY_REGISTRY_CONDITIONAL_EFFECT_TYPES
    assert "memory_written_without_promotion_decision" in DURABLE_MEMORY_REGISTRY_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.5"
    assert pig["subject"] == "durable_memory_record_registry"
    assert pig["safety_boundary"]["durable_memory_record_created"] == "conditional"
    assert pig["safety_boundary"]["session_continuity_injected"] is False
    assert ocpx["state"] == "durable_memory_record_registry_created"
    assert "DurableMemoryRecordState" in ocpx["target_read_models"]
    assert "persistent_memory_written" in ocpx["conditional_effect_types"]
    assert main(["memory", "registry", "policy"]) == 0
    assert main(["memory", "registry", "write-gate"]) == 0
    assert main(["memory", "registry", "write-decision"]) == 0
    assert main(["memory", "registry", "dry-run"]) == 0
    assert main(["memory", "registry", "create-record", "--candidate-id", "memory_candidate:v0.27.2:1"]) == 0
    assert main(["memory", "registry", "entries"]) == 0
    assert main(["memory", "registry", "inspect"]) == 0
    assert main(["memory", "registry", "provenance"]) == 0
    assert main(["memory", "registry", "evidence-index"]) == 0
    assert main(["memory", "registry", "lifecycle"]) == 0
    assert main(["memory", "registry", "privacy"]) == 0
    assert main(["memory", "registry", "forget-revoke"]) == 0
    assert main(["memory", "registry", "integrity"]) == 0
    assert main(["memory", "registry", "audit"]) == 0
    assert main(["memory", "registry", "report", "--report-id", "durable_memory_registry_report:test"]) == 0

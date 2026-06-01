from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_LIFECYCLE_EFFECT_TYPES,
    MEMORY_LIFECYCLE_EVENT_TYPES,
    MEMORY_LIFECYCLE_FORBIDDEN_EFFECT_TYPES,
    MEMORY_LIFECYCLE_OBJECT_TYPES,
    MemoryArchiveDecision,
    MemoryArchiveRecord,
    MemoryConflictResolutionRecord,
    MemoryExpirationDecision,
    MemoryExpirationRecord,
    MemoryForgetDecision,
    MemoryForgetRecord,
    MemoryForgetRequest,
    MemoryForgetTombstone,
    MemoryLifecycleAuditTrail,
    MemoryLifecycleControlPolicy,
    MemoryLifecycleEvidenceReview,
    MemoryLifecycleFinding,
    MemoryLifecycleNoOpDecision,
    MemoryLifecycleOperationGate,
    MemoryLifecyclePIGGuidanceAttachment,
    MemoryLifecyclePrivacyGate,
    MemoryLifecycleRegistryUpdatePreview,
    MemoryLifecycleRegistryUpdateRecord,
    MemoryLifecycleReport,
    MemoryLifecycleReportService,
    MemoryLifecycleRequest,
    MemoryLifecycleScope,
    MemoryLifecycleSourceView,
    MemoryReviewRecord,
    MemoryReviewRequest,
    MemoryRevokeDecision,
    MemoryRevokeRecord,
    MemoryRevokeRequest,
    MemorySupersedeRecord,
    MemoryUpdateCandidate,
    MemoryUpdateDecision,
    MemoryUpdateRecord,
)


def _parts() -> dict:
    return MemoryLifecycleReportService().build_all_parts()


def test_memory_lifecycle_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], MemoryLifecycleControlPolicy)
    assert isinstance(parts["request"], MemoryLifecycleRequest)
    assert isinstance(parts["source_view"], MemoryLifecycleSourceView)
    assert isinstance(parts["operation_gates"][0], MemoryLifecycleOperationGate)
    assert isinstance(parts["review_request"], MemoryReviewRequest)
    assert isinstance(parts["review_records"][0], MemoryReviewRecord)
    assert isinstance(parts["update_candidates"][0], MemoryUpdateCandidate)
    assert isinstance(parts["update_decisions"][0], MemoryUpdateDecision)
    assert isinstance(parts["update_records"][0], MemoryUpdateRecord)
    assert isinstance(parts["supersede_records"][0], MemorySupersedeRecord)
    assert isinstance(parts["revoke_requests"][0], MemoryRevokeRequest)
    assert isinstance(parts["revoke_decisions"][0], MemoryRevokeDecision)
    assert isinstance(parts["revoke_records"][0], MemoryRevokeRecord)
    assert isinstance(parts["forget_requests"][0], MemoryForgetRequest)
    assert isinstance(parts["forget_decisions"][0], MemoryForgetDecision)
    assert isinstance(parts["forget_records"][0], MemoryForgetRecord)
    assert isinstance(parts["forget_tombstones"][0], MemoryForgetTombstone)
    assert isinstance(parts["archive_decisions"][0], MemoryArchiveDecision)
    assert isinstance(parts["archive_records"][0], MemoryArchiveRecord)
    assert isinstance(parts["expiration_decisions"][0], MemoryExpirationDecision)
    assert isinstance(parts["expiration_records"][0], MemoryExpirationRecord)
    assert isinstance(parts["conflict_resolution_records"][0], MemoryConflictResolutionRecord)
    assert isinstance(parts["privacy_gates"][0], MemoryLifecyclePrivacyGate)
    assert isinstance(parts["evidence_reviews"][0], MemoryLifecycleEvidenceReview)
    assert isinstance(parts["lifecycle_scopes"][0], MemoryLifecycleScope)
    assert isinstance(parts["pig_guidance_attachments"][0], MemoryLifecyclePIGGuidanceAttachment)
    assert isinstance(parts["no_op_decisions"][0], MemoryLifecycleNoOpDecision)
    assert isinstance(parts["registry_update_previews"][0], MemoryLifecycleRegistryUpdatePreview)
    assert isinstance(parts["registry_update_records"][0], MemoryLifecycleRegistryUpdateRecord)
    assert isinstance(parts["audit_trail"], MemoryLifecycleAuditTrail)
    assert isinstance(parts["findings"][0], MemoryLifecycleFinding)
    assert isinstance(parts["report"], MemoryLifecycleReport)


def test_lifecycle_policy_source_view_and_gate_require_audit_and_no_source_deletion() -> None:
    parts = _parts()
    policy = parts["policy"]
    source_view = parts["source_view"]
    gate = parts["operation_gates"][0]

    assert policy.version == "v0.27.8"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.lifecycle_control_enabled is True
    assert policy.review_enabled is True
    assert policy.update_candidate_enabled is True
    assert policy.update_decision_enabled is True
    assert policy.update_execution_conditionally_enabled is True
    assert policy.supersede_enabled is True
    assert policy.revoke_enabled is True
    assert policy.forget_enabled is True
    assert policy.archive_enabled is True
    assert policy.expiration_enabled is True
    assert policy.conflict_resolution_enabled is True
    assert policy.no_op_decision_enabled is True
    assert policy.lifecycle_gate_required is True
    assert policy.audit_required is True
    assert policy.source_data_deletion_enabled_now is False
    assert policy.silent_overwrite_forbidden is True
    assert policy.unlogged_deletion_forbidden is True
    assert policy.forget_is_not_source_data_deletion_by_default is True
    assert policy.persona_mutation_enabled_now is False
    assert policy.behavior_policy_mutation_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.safety_bypass_enabled_now is False
    assert policy.continuity_injection_enabled_now is False
    assert policy.pig_guidance_is_not_lifecycle_authority is True
    assert policy.llm_judge_as_sole_lifecycle_authority_forbidden is True
    assert source_view.durable_registry_report_ref
    assert source_view.durable_registry_ref
    assert source_view.selected_memory_record_refs
    assert source_view.registry_entry_refs
    assert source_view.lifecycle_policy_refs
    assert source_view.privacy_boundary_refs
    assert source_view.forget_revoke_binding_refs
    assert source_view.evidence_index_refs
    assert source_view.provenance_refs
    assert source_view.continuity_context_refs
    assert source_view.injection_boundary_refs
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert gate.gate_status == "passed"
    assert gate.memory_record_ref_present is True
    assert gate.operation_allowed_by_lifecycle_policy is True
    assert gate.operation_allowed_by_forget_revoke_binding is True
    assert gate.evidence_available is True
    assert gate.privacy_gate_passed is True
    assert gate.audit_ready is True
    assert gate.source_data_deletion_allowed_now is False
    assert gate.raw_memory_restoration_absent is True
    assert gate.persona_mutation_absent is True
    assert gate.behavior_policy_mutation_absent is True


def test_review_update_revoke_forget_archive_expire_conflict_and_no_op_records() -> None:
    parts = _parts()
    update_parts = MemoryLifecycleReportService().build_all_parts(requested_operation="update")
    revoke_parts = MemoryLifecycleReportService().build_all_parts(requested_operation="revoke")
    forget_parts = MemoryLifecycleReportService().build_all_parts(requested_operation="forget")
    archive_parts = MemoryLifecycleReportService().build_all_parts(requested_operation="archive")
    expire_parts = MemoryLifecycleReportService().build_all_parts(requested_operation="expire")
    report = parts["report"]
    review = parts["review_records"][0]
    candidate = parts["update_candidates"][0]
    update_decision = update_parts["update_decisions"][0]
    update_record = update_parts["update_records"][0]
    supersede = parts["supersede_records"][0]
    revoke = revoke_parts["revoke_records"][0]
    forget = forget_parts["forget_records"][0]
    tombstone = forget_parts["forget_tombstones"][0]
    archive = archive_parts["archive_records"][0]
    expiration = expire_parts["expiration_records"][0]
    conflict = parts["conflict_resolution_records"][0]
    no_op = parts["no_op_decisions"][0]

    assert review.no_mutation_performed is True
    assert report.memory_updated is False
    assert report.memory_revoked is False
    assert report.memory_forgotten is False
    assert report.memory_archived is False
    assert report.memory_expired is False
    assert candidate.update_applied_now is False
    assert candidate.persona_mutation is False
    assert candidate.behavior_policy_mutation is False
    assert update_decision.applies_update_now is True
    assert update_decision.mutates_persona_now is False
    assert update_decision.mutates_behavior_policy_now is False
    assert update_record.update_applied is True
    assert update_record.registry_updated is True
    assert update_record.raw_content_added is False
    assert update_record.persona_mutation is False
    assert update_record.behavior_policy_mutation is False
    assert supersede.source_deleted is False
    assert revoke.new_status == "revoked"
    assert revoke.active_use_removed is True
    assert revoke.source_deleted is False
    assert forget.new_status == "forgotten"
    assert forget.recallable_content_removed is True
    assert forget.active_use_removed is True
    assert forget.source_deleted is False
    assert tombstone.contains_recallable_memory_content is False
    assert tombstone.contains_raw_source_content is False
    assert tombstone.contains_secret is False
    assert tombstone.audit_only is True
    assert archive.new_status == "archived"
    assert archive.active_use_removed is True
    assert archive.source_deleted is False
    assert expiration.new_status == "expired"
    assert expiration.active_use_removed is True
    assert expiration.source_deleted is False
    assert conflict.resolution_type == "surface_only"
    assert conflict.automatically_resolved is False
    assert no_op.no_mutation_performed is True
    assert report.review_records_created is True
    assert report.update_candidates_created is True
    assert report.update_decisions_created is True
    assert report.update_records_created is True
    assert report.revoke_records_created is True
    assert report.forget_records_created is True
    assert report.archive_records_created is True
    assert report.expiration_records_created is True
    assert report.conflict_resolution_records_created is True


def test_lifecycle_report_pig_ocpx_ocel_and_cli_commands_work() -> None:
    service = MemoryLifecycleReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status == "passed"
    assert report.ready_for_v0_27_9 is True
    assert report.ready_for_v0_28 is False
    assert report.source_data_deleted is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_restored is False
    assert report.raw_provider_output_restored is False
    assert report.raw_secret_output is False
    assert report.credential_exposed is False
    assert report.pig_guidance_used_as_authority is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.continuity_injected is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.9 Memory Candidate & Continuity Consolidation"
    assert "memory_lifecycle_control_policy" in MEMORY_LIFECYCLE_OBJECT_TYPES
    assert "memory_lifecycle_report_created" in MEMORY_LIFECYCLE_EVENT_TYPES
    assert "memory_forget_tombstone_created" in MEMORY_LIFECYCLE_EFFECT_TYPES
    assert "source_data_deleted" in MEMORY_LIFECYCLE_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.8"
    assert pig["subject"] == "memory_audit_update_revoke_forget"
    assert pig["safety_boundary"]["source_data_deleted"] is False
    assert ocpx["state"] == "memory_lifecycle_control_created"
    assert "MemoryForgetTombstoneState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "gate",
        "conflicts",
        "no-op",
        "audit",
        "report",
    ]:
        assert main(["memory", "lifecycle", command]) == 0
    for command in ["review", "update-candidate", "update", "revoke", "forget", "archive", "expire"]:
        assert main(["memory", "lifecycle", command, "--record-id", "durable_memory_record:v0.27.5:active"]) == 0

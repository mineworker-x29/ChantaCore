from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MEMORY_PROMOTION_GATE_EFFECT_TYPES,
    MEMORY_PROMOTION_GATE_EVENT_TYPES,
    MEMORY_PROMOTION_GATE_FORBIDDEN_EFFECT_TYPES,
    MEMORY_PROMOTION_GATE_OBJECT_TYPES,
    MEMORY_PROMOTION_GATE_REQUIRED_RULES,
    DurableMemoryReadinessPreview,
    MemoryArchiveOnlyDecisionRecord,
    MemoryEphemeralMemoryDecisionRecord,
    MemoryPromotionAuditTrail,
    MemoryPromotionCandidateView,
    MemoryPromotionContradictionGate,
    MemoryPromotionDecision,
    MemoryPromotionDecisionRecord,
    MemoryPromotionDeferredRecord,
    MemoryPromotionEvidenceReview,
    MemoryPromotionExpiry,
    MemoryPromotionForgetRevokePath,
    MemoryPromotionGateFinding,
    MemoryPromotionGatePolicyRuntime,
    MemoryPromotionGateReport,
    MemoryPromotionGateReportService,
    MemoryPromotionGateRequest,
    MemoryPromotionGateRule,
    MemoryPromotionGateSourceView,
    MemoryPromotionLifecycleBoundary,
    MemoryPromotionMoreEvidenceRequest,
    MemoryPromotionPIGGuidanceAttachment,
    MemoryPromotionPrivacyGate,
    MemoryPromotionRejectedRecord,
    MemoryPromotionRequirement,
    MemoryPromotionScope,
    MemoryPromotionScoreReview,
    MemoryPromotionUserConfirmationRequest,
    MemoryPromotionUserControlGate,
)


def _parts() -> dict:
    return MemoryPromotionGateReportService().build_all_parts()


def test_memory_promotion_gate_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["promotion_gate_policy"], MemoryPromotionGatePolicyRuntime)
    assert isinstance(parts["request"], MemoryPromotionGateRequest)
    assert isinstance(parts["source_view"], MemoryPromotionGateSourceView)
    assert isinstance(parts["gate_rules"][0], MemoryPromotionGateRule)
    assert isinstance(parts["candidate_views"][0], MemoryPromotionCandidateView)
    assert isinstance(parts["requirements"][0], MemoryPromotionRequirement)
    assert isinstance(parts["evidence_reviews"][0], MemoryPromotionEvidenceReview)
    assert isinstance(parts["score_reviews"][0], MemoryPromotionScoreReview)
    assert isinstance(parts["privacy_gates"][0], MemoryPromotionPrivacyGate)
    assert isinstance(parts["contradiction_gates"][0], MemoryPromotionContradictionGate)
    assert isinstance(parts["user_control_gates"][0], MemoryPromotionUserControlGate)
    assert isinstance(parts["scopes"][0], MemoryPromotionScope)
    assert isinstance(parts["expiries"][0], MemoryPromotionExpiry)
    assert isinstance(parts["lifecycle_boundaries"][0], MemoryPromotionLifecycleBoundary)
    assert isinstance(parts["forget_revoke_paths"][0], MemoryPromotionForgetRevokePath)
    assert isinstance(parts["pig_guidance_attachments"][0], MemoryPromotionPIGGuidanceAttachment)
    assert isinstance(parts["promotion_decisions"][0], MemoryPromotionDecision)
    assert isinstance(parts["promotion_decision_records"][0], MemoryPromotionDecisionRecord)
    assert isinstance(parts["durable_readiness_previews"][0], DurableMemoryReadinessPreview)
    assert isinstance(parts["audit_trail"], MemoryPromotionAuditTrail)
    assert isinstance(parts["findings"][0], MemoryPromotionGateFinding)
    assert isinstance(parts["report"], MemoryPromotionGateReport)


def test_policy_source_view_rules_and_candidate_views() -> None:
    parts = _parts()
    policy = parts["promotion_gate_policy"]
    source_view = parts["source_view"]
    rule_names = {rule.rule_name for rule in parts["gate_rules"]}
    candidate_view = parts["candidate_views"][0]

    assert policy.version == "v0.27.4"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.promotion_gate_enabled is True
    assert policy.promotion_decision_record_enabled is True
    assert policy.reject_decision_record_enabled is True
    assert policy.defer_decision_record_enabled is True
    assert policy.request_more_evidence_enabled is True
    assert policy.request_user_confirmation_enabled is True
    assert policy.mark_ephemeral_enabled is True
    assert policy.mark_archive_only_enabled is True
    assert policy.promote_decision_is_not_durable_write is True
    assert policy.durable_memory_write_enabled_now is False
    assert policy.persistent_memory_write_enabled_now is False
    assert policy.durable_registry_update_enabled_now is False
    assert policy.session_continuity_injection_enabled_now is False
    assert policy.persona_mutation_enabled_now is False
    assert policy.behavior_policy_mutation_enabled_now is False
    assert policy.automatic_promotion_forbidden is True
    assert policy.promotion_requires_source_refs is True
    assert policy.promotion_requires_evidence_bundle is True
    assert policy.promotion_requires_score is True
    assert policy.promotion_requires_privacy_risk_assessment is True
    assert policy.promotion_requires_contradiction_check is True
    assert policy.promotion_requires_user_control_assessment is True
    assert policy.promotion_requires_scope is True
    assert policy.promotion_requires_expiry_or_lifecycle is True
    assert policy.promotion_requires_audit_trail is True
    assert policy.promotion_requires_forget_revoke_path is True
    assert policy.high_score_cannot_bypass_gate is True
    assert policy.pig_guidance_cannot_promote_memory is True
    assert policy.raw_transcript_promotion_forbidden is True
    assert policy.raw_provider_output_promotion_forbidden is True
    assert policy.raw_secret_promotion_forbidden is True
    assert policy.credential_promotion_forbidden is True
    assert policy.private_full_path_promotion_forbidden is True
    assert policy.llm_judge_as_sole_promotion_authority_forbidden is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.safety_bypass_enabled_now is False
    assert source_view.evidence_scoring_report_ref is not None
    assert source_view.scoring_batch_ref is not None
    assert source_view.candidate_refs
    assert source_view.evidence_bundle_refs
    assert source_view.score_refs
    assert source_view.promotion_readiness_preview_refs
    assert source_view.privacy_assessment_refs
    assert source_view.contradiction_check_refs
    assert source_view.user_control_assessment_refs
    assert source_view.pig_guidance_refs
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert source_view.private_full_path_included is False
    assert set(MEMORY_PROMOTION_GATE_REQUIRED_RULES).issubset(rule_names)
    assert candidate_view.score_ref is not None
    assert candidate_view.evidence_bundle_ref is not None
    assert candidate_view.privacy_assessment_ref is not None
    assert candidate_view.contradiction_check_ref is not None
    assert candidate_view.user_control_assessment_ref is not None
    assert candidate_view.eligible_for_promotion_decision is True
    assert candidate_view.eligible_for_durable_write_now is False
    assert candidate_view.promoted_to_memory_now is False
    assert candidate_view.durable_memory_written_now is False


def test_reviews_gates_scope_lifecycle_and_pig_attachment() -> None:
    parts = _parts()

    assert all(item.satisfied for item in parts["requirements"])
    assert parts["evidence_reviews"][0].evidence_review_status in {"sufficient", "weak", "missing", "contradicted", "blocked", "unknown"}
    assert parts["score_reviews"][0].score_band in {"low", "medium", "high", "blocked", "unknown"}
    assert parts["score_reviews"][0].promotion_readiness in {"not_ready", "needs_more_evidence", "needs_user_confirmation", "ready_for_gate_review", "blocked", "unknown"}
    assert parts["score_reviews"][0].high_score_bypassed_gate is False
    assert parts["privacy_gates"][0].gate_status in {"passed", "warning", "failed", "blocked", "unknown"}
    assert parts["contradiction_gates"][0].gate_status in {"passed", "warning", "failed", "blocked", "unknown"}
    assert parts["user_control_gates"][0].gate_status in {"passed", "warning", "failed", "blocked", "unknown"}
    assert parts["scopes"][0].scope_status in {"valid", "incomplete", "blocked", "unknown"}
    assert parts["scopes"][0].grants_durable_write_now is False
    assert parts["expiries"][0].expiry_status in {"valid", "incomplete", "blocked", "unknown"}
    assert parts["lifecycle_boundaries"][0].lifecycle_status in {"ready", "partial", "warning", "blocked"}
    assert parts["lifecycle_boundaries"][0].durable_record_created_now is False
    assert parts["forget_revoke_paths"][0].forget_executed_now is False
    assert parts["forget_revoke_paths"][0].revoke_executed_now is False
    assert parts["pig_guidance_attachments"][0].pig_guidance_is_memory is False
    assert parts["pig_guidance_attachments"][0].pig_guidance_promotes_memory is False
    assert parts["pig_guidance_attachments"][0].pig_guidance_mutates_policy is False
    assert parts["pig_guidance_attachments"][0].pig_guidance_executes is False


def test_decisions_records_previews_and_report_are_non_writing() -> None:
    parts = _parts()
    decision = parts["promotion_decisions"][0]
    record = parts["promotion_decision_records"][0]
    preview = parts["durable_readiness_previews"][0]
    audit = parts["audit_trail"]
    report = parts["report"]

    assert decision.decision_type == "promote"
    assert decision.creates_durable_memory_now is False
    assert decision.writes_persistent_memory_now is False
    assert decision.mutates_persona_now is False
    assert decision.mutates_behavior_policy_now is False
    assert record.ocel_visible is True
    assert record.durable_memory_created is False
    assert record.persistent_memory_written is False
    assert preview.ready_for_v0275_durable_registry is True
    assert preview.preview_is_not_durable_write is True
    assert preview.durable_memory_created_now is False
    assert preview.persistent_memory_written_now is False
    assert set(preview.required_v0275_inputs) == {
        "promotion_decision_record",
        "candidate_ref",
        "evidence_bundle_ref",
        "score_ref",
        "source_refs",
        "scope_ref",
        "expiry_or_lifecycle_ref",
        "forget_revoke_path_ref",
        "audit_trail_ref",
    }
    assert audit.raw_content_included is False
    assert audit.durable_memory_created is False
    assert audit.persistent_memory_written is False
    assert report.ready_for_v0_27_5 is True
    assert report.ready_for_v0_28 is False
    assert report.promotion_gate_created is True
    assert report.candidate_views_created is True
    assert report.requirements_created is True
    assert report.gate_reviews_created is True
    assert report.scopes_created is True
    assert report.expiries_created is True
    assert report.forget_revoke_paths_created is True
    assert report.promotion_decisions_recorded is True
    assert report.durable_readiness_previews_created is True
    assert report.audit_trail_created is True
    assert report.promote_decision_count > 0
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.durable_registry_updated is False
    assert report.session_continuity_injected is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_memory_created is False
    assert report.raw_provider_output_memory_created is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_secret_output is False
    assert report.credential_exposed is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.5 Durable Memory Record & Registry"


def test_non_promote_decision_record_variants_build() -> None:
    service = MemoryPromotionGateReportService()

    reject = service.build_all_parts(requested_decision_type="reject")
    assert isinstance(reject["rejected_records"][0], MemoryPromotionRejectedRecord)
    assert reject["rejected_records"][0].source_deleted is False
    assert reject["rejected_records"][0].durable_memory_created is False

    defer = service.build_all_parts(requested_decision_type="defer")
    assert isinstance(defer["deferred_records"][0], MemoryPromotionDeferredRecord)
    assert defer["deferred_records"][0].durable_memory_created is False

    more = service.build_all_parts(requested_decision_type="request_more_evidence")
    assert isinstance(more["more_evidence_requests"][0], MemoryPromotionMoreEvidenceRequest)
    assert more["more_evidence_requests"][0].candidate_mutated_now is False
    assert more["more_evidence_requests"][0].durable_memory_created is False

    confirm = service.build_all_parts(requested_decision_type="request_user_confirmation")
    assert isinstance(confirm["user_confirmation_requests"][0], MemoryPromotionUserConfirmationRequest)
    assert confirm["user_confirmation_requests"][0].confirmation_received_now is False
    assert confirm["user_confirmation_requests"][0].durable_memory_created is False

    ephemeral = service.build_all_parts(requested_decision_type="mark_ephemeral")
    assert isinstance(ephemeral["ephemeral_records"][0], MemoryEphemeralMemoryDecisionRecord)
    assert ephemeral["ephemeral_records"][0].active_memory_created is False
    assert ephemeral["ephemeral_records"][0].durable_memory_created is False

    archive = service.build_all_parts(requested_decision_type="mark_archive_only")
    assert isinstance(archive["archive_only_records"][0], MemoryArchiveOnlyDecisionRecord)
    assert archive["archive_only_records"][0].active_memory_created is False
    assert archive["archive_only_records"][0].durable_memory_created is False


def test_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = MemoryPromotionGateReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "memory_promotion_gate_report" in MEMORY_PROMOTION_GATE_OBJECT_TYPES
    assert "memory_promotion_decision_recorded" in MEMORY_PROMOTION_GATE_EVENT_TYPES
    assert "memory_promotion_decision_recorded" in MEMORY_PROMOTION_GATE_EFFECT_TYPES
    assert "memory_promoted" in MEMORY_PROMOTION_GATE_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.4"
    assert pig["subject"] == "memory_promotion_gate"
    assert pig["safety_boundary"]["memory_promoted"] is False
    assert pig["safety_boundary"]["durable_registry_updated"] is False
    assert ocpx["state"] == "memory_promotion_gate_created"
    assert "MemoryPromotionGateState" in ocpx["target_read_models"]
    assert "DurableMemoryReadinessPreviewState" in ocpx["target_read_models"]

    assert main(["memory", "promotion", "gate"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.27.4" in output
    assert "promotion_gate_created=true" in output
    assert "promotion_decisions_recorded=true" in output
    assert "ready_for_v0_27_5=true" in output
    assert "ready_for_v0_28=false" in output
    assert "memory_promoted=false" in output
    assert "persistent_memory_written=false" in output
    assert "durable_memory_written=false" in output
    assert "durable_registry_updated=false" in output
    assert "provider_invoked=false" in output
    assert "command_executed=false" in output
    assert "safety_gate_bypassed=false" in output
    assert "next_required_step=v0.27.5 Durable Memory Record & Registry" in output

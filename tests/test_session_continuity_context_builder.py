from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    ContinuityConflictReport,
    ContinuityContextItem,
    ContinuityContextPack,
    ContinuityPrivacyFilter,
    ContinuityRecencyWindow,
    ContinuityRelevancePolicy,
    ContinuityRelevanceScore,
    ContinuityStalenessWarning,
    SESSION_CONTINUITY_EFFECT_TYPES,
    SESSION_CONTINUITY_EVENT_TYPES,
    SESSION_CONTINUITY_FORBIDDEN_EFFECT_TYPES,
    SESSION_CONTINUITY_OBJECT_TYPES,
    SESSION_CONTINUITY_REQUIRED_RULES,
    SessionContinuityBuildAuditTrail,
    SessionContinuityBuildDecision,
    SessionContinuityContext,
    SessionContinuityContextBuildReport,
    SessionContinuityContextBuildReportService,
    SessionContinuityContextFinding,
    SessionContinuityContextPolicy,
    SessionContinuityContextRequest,
    SessionContinuityContextPreview,
    SessionContinuityEligibilityRule,
    SessionContinuityMemoryRef,
    SessionContinuityRefBundle,
    SessionContinuitySourceView,
)


def _parts() -> dict:
    return SessionContinuityContextBuildReportService().build_all_parts()


def test_session_continuity_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], SessionContinuityContextPolicy)
    assert isinstance(parts["request"], SessionContinuityContextRequest)
    assert isinstance(parts["source_view"], SessionContinuitySourceView)
    assert isinstance(parts["eligibility_rules"][0], SessionContinuityEligibilityRule)
    assert isinstance(parts["memory_refs"][0], SessionContinuityMemoryRef)
    assert isinstance(parts["continuity_ref_bundle"], SessionContinuityRefBundle)
    assert isinstance(parts["relevance_policy"], ContinuityRelevancePolicy)
    assert isinstance(parts["relevance_scores"][0], ContinuityRelevanceScore)
    assert isinstance(parts["recency_windows"][0], ContinuityRecencyWindow)
    assert isinstance(parts["staleness_warnings"][0], ContinuityStalenessWarning)
    assert isinstance(parts["conflict_reports"][0], ContinuityConflictReport)
    assert isinstance(parts["privacy_filters"][0], ContinuityPrivacyFilter)
    assert isinstance(parts["context_items"][0], ContinuityContextItem)
    assert isinstance(parts["context_pack"], ContinuityContextPack)
    assert isinstance(parts["continuity_context"], SessionContinuityContext)
    assert isinstance(parts["build_decisions"][0], SessionContinuityBuildDecision)
    assert isinstance(parts["context_previews"][0], SessionContinuityContextPreview)
    assert isinstance(parts["audit_trail"], SessionContinuityBuildAuditTrail)
    assert isinstance(parts["findings"][0], SessionContinuityContextFinding)
    assert isinstance(parts["report"], SessionContinuityContextBuildReport)


def test_policy_and_required_eligibility_rules_are_present() -> None:
    parts = _parts()
    policy = parts["policy"]
    rules = {rule.rule_name for rule in parts["eligibility_rules"]}

    assert policy.version == "v0.27.6"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.session_continuity_context_builder_enabled is True
    assert policy.context_pack_enabled is True
    assert policy.relevance_scoring_enabled is True
    assert policy.privacy_filter_enabled is True
    assert policy.conflict_report_enabled is True
    assert policy.staleness_warning_enabled is True
    assert policy.continuity_injection_enabled_now is False
    assert policy.default_agent_context_mutation_enabled_now is False
    assert policy.decision_service_mutation_enabled_now is False
    assert policy.skill_router_mutation_enabled_now is False
    assert policy.safety_gate_mutation_enabled_now is False
    assert policy.permission_policy_mutation_enabled_now is False
    assert policy.memory_update_enabled_now is False
    assert policy.memory_revoke_enabled_now is False
    assert policy.memory_forget_enabled_now is False
    assert policy.persona_mutation_enabled_now is False
    assert policy.behavior_policy_mutation_enabled_now is False
    assert policy.raw_transcript_replay_forbidden is True
    assert policy.raw_provider_output_replay_forbidden is True
    assert policy.revoked_memory_active_use_forbidden is True
    assert policy.forgotten_memory_active_use_forbidden is True
    assert policy.expired_memory_active_use_forbidden is True
    assert policy.safety_gate_bypass_forbidden is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.llm_judge_as_sole_continuity_authority_forbidden is True
    assert set(SESSION_CONTINUITY_REQUIRED_RULES).issubset(rules)


def test_source_view_separates_statuses_and_omits_raw_content() -> None:
    source_view = _parts()["source_view"]

    assert source_view.durable_registry_report_ref
    assert source_view.durable_registry_ref
    assert source_view.active_memory_record_refs
    assert source_view.archived_memory_record_refs
    assert source_view.revoked_memory_record_refs
    assert source_view.forgotten_memory_record_refs
    assert source_view.expired_memory_record_refs
    assert source_view.blocked_memory_record_refs
    assert source_view.memory_scope_refs
    assert source_view.memory_provenance_refs
    assert source_view.memory_evidence_index_refs
    assert source_view.memory_lifecycle_refs
    assert source_view.memory_privacy_boundary_refs
    assert source_view.pig_guidance_refs
    assert source_view.session_context_refs
    assert source_view.trace_summary_refs
    assert source_view.approval_decision_refs
    assert source_view.command_candidate_refs
    assert source_view.failure_cause_refs
    assert source_view.active_memory_count == 1
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert source_view.private_full_path_included is False


def test_memory_refs_and_bundle_enforce_active_context_boundary() -> None:
    parts = _parts()
    memory_refs = parts["memory_refs"]
    by_status = {item.memory_status: item for item in memory_refs}
    bundle = parts["continuity_ref_bundle"]

    assert by_status["active"].use_role == "active_context"
    assert by_status["active"].eligible_for_context_pack is True
    assert by_status["active"].eligible_for_injection_now is False
    assert by_status["active"].raw_content_included is False
    assert by_status["archived"].use_role == "archive_reference"
    assert by_status["archived"].eligible_for_context_pack is True
    for status in ["revoked", "forgotten", "expired", "blocked"]:
        assert by_status[status].use_role != "active_context"
        assert by_status[status].eligible_for_context_pack is False
    assert bundle.active_context_refs
    assert bundle.background_reference_refs
    assert bundle.blocked_refs
    assert bundle.continuity_injected_now is False


def test_relevance_staleness_conflict_and_privacy_artifacts_build() -> None:
    parts = _parts()
    relevance_policy = parts["relevance_policy"]
    scores = parts["relevance_scores"]
    warnings = parts["staleness_warnings"]
    conflicts = parts["conflict_reports"]
    privacy_filters = parts["privacy_filters"]

    assert relevance_policy.relevance_score_is_not_authority is True
    assert relevance_policy.pig_guidance_is_not_authority is True
    assert any(score.relevance_band == "high" for score in scores)
    assert all(score.relevance_score_is_authority is False for score in scores)
    assert any(warning.surface_to_user_later for warning in warnings)
    assert all(conflict.automatically_resolved is False for conflict in conflicts)
    assert all(item.raw_sensitive_content_included is False for item in privacy_filters)


def test_context_pack_context_preview_and_report_are_non_injection() -> None:
    parts = _parts()
    item = parts["context_items"][0]
    pack = parts["context_pack"]
    context = parts["continuity_context"]
    decision = parts["build_decisions"][0]
    preview = parts["context_previews"][0]
    audit = parts["audit_trail"]
    report = parts["report"]

    assert item.refs_only is True
    assert item.raw_transcript_included is False
    assert item.raw_provider_output_included is False
    assert item.raw_secret_included is False
    assert item.injects_runtime_now is False
    assert item.mutates_persona_now is False
    assert item.mutates_behavior_policy_now is False
    assert pack.refs_only is True
    assert pack.raw_transcript_included is False
    assert pack.raw_provider_output_included is False
    assert pack.raw_secret_included is False
    assert pack.continuity_injected_now is False
    assert context.is_runtime_injected is False
    assert context.default_agent_context_mutated is False
    assert context.decision_service_mutated is False
    assert context.skill_router_mutated is False
    assert context.safety_gate_mutated is False
    assert context.permission_policy_mutated is False
    assert context.persona_mutated is False
    assert context.behavior_policy_mutated is False
    assert decision.creates_context_pack is True
    assert decision.injects_context_now is False
    assert decision.updates_memory_now is False
    assert preview.preview_is_not_injection is True
    assert preview.injection_performed_now is False
    assert audit.raw_content_included is False
    assert report.report_status == "passed"
    assert report.ready_for_v0_27_7 is True
    assert report.ready_for_v0_28 is False
    assert report.continuity_injected is False
    assert report.default_agent_context_mutated is False
    assert report.decision_service_mutated is False
    assert report.skill_router_mutated is False
    assert report.safety_gate_mutated is False
    assert report.permission_policy_mutated is False
    assert report.memory_updated is False
    assert report.memory_revoked is False
    assert report.memory_forgotten is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_replayed is False
    assert report.raw_provider_output_replayed is False
    assert report.raw_secret_output is False
    assert report.credential_exposed is False
    assert report.pig_guidance_used_as_authority is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.7 Continuity Injection Boundary"


def test_ocel_pig_ocpx_and_cli_continuity_commands_work() -> None:
    service = SessionContinuityContextBuildReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "session_continuity_context_policy" in SESSION_CONTINUITY_OBJECT_TYPES
    assert "session_continuity_context_created" in SESSION_CONTINUITY_EVENT_TYPES
    assert "continuity_context_pack_created" in SESSION_CONTINUITY_EFFECT_TYPES
    assert "continuity_injected" in SESSION_CONTINUITY_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.6"
    assert pig["subject"] == "session_continuity_context_builder"
    assert pig["safety_boundary"]["continuity_injected"] is False
    assert ocpx["state"] == "session_continuity_context_builder_created"
    assert "SessionContinuityContextPreviewState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "eligibility-rules",
        "refs",
        "bundle",
        "relevance",
        "recency",
        "stale",
        "conflicts",
        "privacy",
        "items",
        "pack",
        "context",
        "preview",
        "audit",
        "report",
    ]:
        assert main(["memory", "continuity", command]) == 0

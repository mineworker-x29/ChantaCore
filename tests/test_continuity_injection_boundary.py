from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    CONTINUITY_INJECTION_EFFECT_TYPES,
    CONTINUITY_INJECTION_EVENT_TYPES,
    CONTINUITY_INJECTION_FORBIDDEN_EFFECT_TYPES,
    CONTINUITY_INJECTION_OBJECT_TYPES,
    CONTINUITY_INJECTION_REQUIRED_RULES,
    CONTINUITY_INJECTION_TARGET_SURFACES,
    ContinuityInjectionAuditTrail,
    ContinuityInjectionBoundaryFinding,
    ContinuityInjectionBoundaryPolicy,
    ContinuityInjectionBoundaryReport,
    ContinuityInjectionBoundaryReportService,
    ContinuityInjectionBoundaryTrace,
    ContinuityInjectionBundle,
    ContinuityInjectionCompatibilityRule,
    ContinuityInjectionContextItemBinding,
    ContinuityInjectionDecision,
    ContinuityInjectionDecisionRecord,
    ContinuityInjectionDeferredRecord,
    ContinuityInjectionEligibilityEvaluation,
    ContinuityInjectionPreview,
    ContinuityInjectionRejectedRecord,
    ContinuityInjectionRequest,
    ContinuityInjectionSourceView,
    ContinuityInjectionTargetSurface,
    ContinuityInjectionTargetSurfaceCatalog,
    ContinuityInstructionPriorityPolicy,
    ContinuityMemoryUserIntentPriorityRule,
    ContinuityPermissionBoundaryRule,
    ContinuitySafetyBoundaryRule,
)


def _parts() -> dict:
    return ContinuityInjectionBoundaryReportService().build_all_parts()


def test_continuity_injection_boundary_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], ContinuityInjectionBoundaryPolicy)
    assert isinstance(parts["request"], ContinuityInjectionRequest)
    assert isinstance(parts["source_view"], ContinuityInjectionSourceView)
    assert isinstance(parts["target_catalog"], ContinuityInjectionTargetSurfaceCatalog)
    assert isinstance(parts["target_surfaces"][0], ContinuityInjectionTargetSurface)
    assert isinstance(parts["compatibility_rules"][0], ContinuityInjectionCompatibilityRule)
    assert isinstance(parts["eligibility_evaluations"][0], ContinuityInjectionEligibilityEvaluation)
    assert isinstance(parts["instruction_priority_policy"], ContinuityInstructionPriorityPolicy)
    assert isinstance(parts["memory_user_intent_priority_rules"][0], ContinuityMemoryUserIntentPriorityRule)
    assert isinstance(parts["safety_boundary_rules"][0], ContinuitySafetyBoundaryRule)
    assert isinstance(parts["permission_boundary_rules"][0], ContinuityPermissionBoundaryRule)
    assert isinstance(parts["context_item_bindings"][0], ContinuityInjectionContextItemBinding)
    assert isinstance(parts["injection_bundles"][0], ContinuityInjectionBundle)
    assert isinstance(parts["injection_previews"][0], ContinuityInjectionPreview)
    assert isinstance(parts["injection_decisions"][0], ContinuityInjectionDecision)
    assert isinstance(parts["decision_records"][0], ContinuityInjectionDecisionRecord)
    assert isinstance(parts["rejected_records"][0], ContinuityInjectionRejectedRecord)
    assert isinstance(parts["deferred_records"][0], ContinuityInjectionDeferredRecord)
    assert isinstance(parts["boundary_traces"][0], ContinuityInjectionBoundaryTrace)
    assert isinstance(parts["audit_trail"], ContinuityInjectionAuditTrail)
    assert isinstance(parts["findings"][0], ContinuityInjectionBoundaryFinding)
    assert isinstance(parts["report"], ContinuityInjectionBoundaryReport)


def test_injection_boundary_policy_disables_runtime_mutation() -> None:
    policy = _parts()["policy"]

    assert policy.version == "v0.27.7"
    assert policy.layer == "memory_candidate_continuity"
    assert policy.injection_boundary_enabled is True
    assert policy.injection_preview_enabled is True
    assert policy.injection_bundle_enabled is True
    assert policy.injection_decision_record_enabled is True
    assert policy.target_surface_compatibility_enabled is True
    assert policy.actual_runtime_injection_enabled_now is False
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
    assert policy.explicit_user_instruction_outranks_memory is True
    assert policy.memory_context_is_guidance_not_authority is True
    assert policy.safety_gate_must_remain_active is True
    assert policy.permission_boundary_must_remain_active is True
    assert policy.stale_memory_warning_required is True
    assert policy.contradiction_surface_required is True
    assert policy.privacy_filter_must_remain_active is True
    assert policy.raw_transcript_replay_forbidden is True
    assert policy.raw_provider_output_replay_forbidden is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.safety_bypass_enabled_now is False
    assert policy.pig_guidance_is_not_authority is True
    assert policy.llm_judge_as_sole_injection_authority_forbidden is True


def test_source_view_and_target_catalog_are_refs_only_and_non_mutating() -> None:
    parts = _parts()
    source_view = parts["source_view"]
    catalog = parts["target_catalog"]
    names = {surface.target_surface_name for surface in catalog.supported_target_surfaces}

    assert source_view.continuity_context_build_report_ref
    assert source_view.continuity_context_ref
    assert source_view.context_pack_ref
    assert source_view.context_item_refs
    assert source_view.conflict_report_refs
    assert source_view.staleness_warning_refs
    assert source_view.privacy_filter_refs
    assert source_view.pig_guidance_refs
    assert source_view.memory_record_refs
    assert source_view.evidence_index_refs
    assert source_view.context_item_count == len(source_view.context_item_refs)
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert set(CONTINUITY_INJECTION_TARGET_SURFACES).issubset(names)
    assert all(surface.runtime_mutation_allowed_now is False for surface in catalog.supported_target_surfaces)
    assert all(surface.provider_invocation_allowed_now is False for surface in catalog.supported_target_surfaces)
    assert all(surface.command_execution_allowed_now is False for surface in catalog.supported_target_surfaces)
    assert all(surface.requires_safety_boundary is True for surface in catalog.supported_target_surfaces)
    assert all(surface.requires_permission_boundary is True for surface in catalog.supported_target_surfaces)
    assert all(surface.requires_user_instruction_priority is True for surface in catalog.supported_target_surfaces)


def test_compatibility_eligibility_priority_safety_and_permission_rules() -> None:
    parts = _parts()
    rule_names = {rule.rule_name for rule in parts["compatibility_rules"]}
    evaluation = parts["eligibility_evaluations"][0]
    priority_policy = parts["instruction_priority_policy"]
    priority_rule = parts["memory_user_intent_priority_rules"][0]
    safety_rule = parts["safety_boundary_rules"][0]
    permission_rule = parts["permission_boundary_rules"][0]

    assert set(CONTINUITY_INJECTION_REQUIRED_RULES).issubset(rule_names)
    assert evaluation.eligibility_status == "eligible_for_preview"
    assert evaluation.runtime_injection_allowed_now is False
    assert evaluation.mutation_allowed_now is False
    assert priority_policy.explicit_user_instruction_outranks_memory is True
    assert priority_policy.current_task_context_outranks_stale_memory is True
    assert priority_policy.safety_policy_outranks_memory is True
    assert priority_policy.permission_policy_outranks_memory is True
    assert priority_policy.memory_must_not_override_user_intent is True
    assert priority_rule.priority_order[0] == "safety_policy"
    assert priority_rule.conflict_handling == "surface_conflict"
    assert safety_rule.safety_gate_must_remain_active is True
    assert safety_rule.memory_cannot_bypass_safety is True
    assert safety_rule.memory_cannot_lower_safety_level is True
    assert permission_rule.permission_boundary_must_remain_active is True
    assert permission_rule.memory_cannot_grant_permission is True
    assert permission_rule.memory_cannot_expand_scope is True


def test_bindings_bundle_preview_decision_trace_audit_are_not_runtime_injection() -> None:
    parts = _parts()
    binding = parts["context_item_bindings"][0]
    bundle = parts["injection_bundles"][0]
    preview = parts["injection_previews"][0]
    decision = parts["injection_decisions"][0]
    record = parts["decision_records"][0]
    rejected = parts["rejected_records"][0]
    deferred = parts["deferred_records"][0]
    trace = parts["boundary_traces"][0]
    audit = parts["audit_trail"]

    assert binding.refs_only is True
    assert binding.preserved_warning_refs
    assert binding.preserved_conflict_refs
    assert binding.preserved_privacy_filter_refs
    assert binding.runtime_applied_now is False
    assert bundle.refs_only is True
    assert bundle.runtime_injection_performed is False
    assert bundle.default_agent_context_mutated is False
    assert bundle.decision_service_mutated is False
    assert bundle.skill_router_mutated is False
    assert bundle.safety_gate_mutated is False
    assert bundle.permission_policy_mutated is False
    assert preview.preview_is_not_runtime_injection is True
    assert preview.runtime_injection_performed is False
    assert preview.warnings_to_surface
    assert preview.conflicts_to_surface
    assert preview.privacy_filters_to_preserve
    assert decision.decision_type == "create_preview"
    assert decision.creates_preview is True
    assert decision.applies_runtime_injection_now is False
    assert decision.mutates_runtime_now is False
    assert record.runtime_injection_performed is False
    assert rejected.source_context_retained is True
    assert rejected.context_deleted is False
    assert rejected.runtime_injection_performed is False
    assert deferred.runtime_injection_performed is False
    assert trace.boundary_bypassed is False
    assert trace.runtime_mutation_performed is False
    assert trace.provider_invoked is False
    assert trace.command_executed is False
    assert audit.raw_content_included is False
    assert audit.runtime_injection_performed is False


def test_report_pig_ocpx_and_cli_injection_commands_work() -> None:
    service = ContinuityInjectionBoundaryReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status == "passed"
    assert report.ready_for_v0_27_8 is True
    assert report.ready_for_v0_28 is False
    assert report.runtime_injection_performed is False
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
    assert report.file_mutated is False
    assert report.safety_gate_bypassed is False
    assert report.permission_boundary_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.27.8 Memory Audit / Update / Revoke / Forget"
    assert "continuity_injection_boundary_policy" in CONTINUITY_INJECTION_OBJECT_TYPES
    assert "continuity_injection_boundary_report_created" in CONTINUITY_INJECTION_EVENT_TYPES
    assert "continuity_injection_preview_created" in CONTINUITY_INJECTION_EFFECT_TYPES
    assert "runtime_injection_performed" in CONTINUITY_INJECTION_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.27.7"
    assert pig["subject"] == "continuity_injection_boundary"
    assert pig["safety_boundary"]["runtime_injection_performed"] is False
    assert ocpx["state"] == "continuity_injection_boundary_created"
    assert "ContinuityInjectionBoundaryTraceState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "targets",
        "compatibility",
        "eligibility",
        "priority",
        "safety-boundary",
        "permission-boundary",
        "bindings",
        "bundle",
        "preview",
        "boundary-trace",
        "audit",
        "report",
    ]:
        assert main(["memory", "injection", command]) == 0
    assert main(["memory", "injection", "decide", "--decision", "create_future_handoff_bundle"]) == 0

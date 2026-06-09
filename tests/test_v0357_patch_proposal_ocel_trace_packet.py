import inspect

import pytest

from chanta_core.agent_runtime import (
    DigestionDominionDisposition,
    DigestionDominionTraceRecord,
    ExternalAgentControlPatternKind,
    ExternalAgentControlPatternRecord,
    PatchProposalTraceAttribute,
    PatchProposalTraceAttributeKind,
    PatchProposalTraceDecisionKind,
    PatchProposalTraceEmissionDecision,
    PatchProposalTraceEmissionInput,
    PatchProposalTraceEmissionReport,
    PatchProposalTraceEmitter,
    PatchProposalTraceEvent,
    PatchProposalTraceEventKind,
    PatchProposalTraceFlagSet,
    PatchProposalTraceNoPersistenceGuarantee,
    PatchProposalTraceObject,
    PatchProposalTraceObjectType,
    PatchProposalTracePacket,
    PatchProposalTracePolicy,
    PatchProposalTraceReadinessLevel,
    PatchProposalTraceRelation,
    PatchProposalTraceRelationType,
    PatchProposalTraceRiskKind,
    PatchProposalTraceRunPreview,
    PatchProposalTraceSinkKind,
    PatchProposalTraceSourceKind,
    PatchProposalTraceSourceRef,
    PatchProposalTraceStatus,
    PatchProposalTraceValidationReport,
    V0357ReadinessReport,
    build_diff_proposal_envelope,
    build_digestion_dominion_records_from_reference_digest,
    build_digestion_dominion_trace_record,
    build_external_agent_control_pattern_record,
    build_external_agent_pattern_records_from_metadata,
    build_patch_plan,
    build_patch_proposal_risk_report_from_scan,
    build_patch_proposal_trace_attribute,
    build_patch_proposal_trace_emission_decision,
    build_patch_proposal_trace_emission_input,
    build_patch_proposal_trace_emission_report,
    build_patch_proposal_trace_emitter,
    build_patch_proposal_trace_event,
    build_patch_proposal_trace_flags,
    build_patch_proposal_trace_no_persistence_guarantee,
    build_patch_proposal_trace_object,
    build_patch_proposal_trace_packet,
    build_patch_proposal_trace_packet_from_diff_envelope,
    build_patch_proposal_trace_packet_from_patch_plan,
    build_patch_proposal_trace_packet_from_review_packet,
    build_patch_proposal_trace_packet_from_risk_report,
    build_patch_proposal_trace_policy,
    build_patch_proposal_trace_relation,
    build_patch_proposal_trace_run_preview,
    build_patch_proposal_trace_source_ref,
    build_patch_proposal_trace_validation_report,
    build_patch_review_packet,
    build_reference_harness_pattern,
    build_reference_pattern_digest,
    build_v0357_readiness_report,
    decide_patch_proposal_trace_emission,
    default_patch_proposal_trace_policy,
    digestion_dominion_record_is_not_runtime,
    emit_patch_proposal_trace_packet,
    external_agent_pattern_record_is_not_execution,
    patch_proposal_trace_flags_preserve_unsafe_false,
    patch_proposal_trace_packet_is_not_persistence,
    patch_proposal_trace_policy_blocks_persistence,
    sanitize_patch_proposal_trace_attribute_value,
    validate_patch_proposal_trace_packet,
    v0357_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import patch_ocel_trace as trace_module
from chanta_core.agent_runtime.patch_proposal_boundary import (
    ReferenceHarnessPatternKind,
    ReferencePatternDisposition,
)


def test_v0357_taxonomies_have_required_values() -> None:
    assert {item.value for item in PatchProposalTraceEventKind} == {
        "patch_intent_created",
        "patch_scope_validated",
        "patch_context_collected",
        "reference_pattern_digest_consumed",
        "reference_pattern_adapted",
        "reference_pattern_rejected",
        "patch_plan_created",
        "change_set_graph_created",
        "diff_proposal_created",
        "structured_patch_proposal_created",
        "unified_diff_proposal_created",
        "patch_risk_scanned",
        "patch_conformance_scanned",
        "patch_safety_regression_scanned",
        "patch_scope_violation_scanned",
        "human_review_packet_created",
        "review_checklist_created",
        "approval_gate_metadata_created",
        "reviewer_decision_placeholder_created",
        "reviewer_decision_recorded",
        "patch_proposal_ready_for_review",
        "patch_proposal_blocked",
        "patch_proposal_needs_revision",
        "patch_proposal_future_gated",
        "digestion_first_policy_applied",
        "external_agent_control_pattern_observed",
        "dominion_like_loop_detected",
        "dominion_escalation_rejected",
        "dominion_escalation_future_gated",
        "external_agent_execution_blocked",
        "infinite_agent_loop_blocked",
        "reference_harness_execution_blocked",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceObjectType} == {
        "patch_intent_envelope",
        "patch_scope_policy",
        "patch_target_selector",
        "reference_pattern_digest",
        "reference_harness_pattern",
        "patch_context_snapshot",
        "patch_context_evidence_bundle",
        "patch_plan",
        "patch_change_set_graph",
        "patch_change_node",
        "patch_dependency_edge",
        "diff_proposal_envelope",
        "unified_diff_proposal",
        "structured_patch_proposal",
        "patch_file_proposal",
        "patch_hunk_proposal",
        "patch_risk_signal",
        "patch_proposal_risk_report",
        "patch_review_packet",
        "patch_review_checklist",
        "patch_approval_gate_metadata",
        "patch_reviewer_decision_placeholder",
        "patch_reviewer_decision_record",
        "external_agent_control_pattern",
        "digestion_dominion_record",
        "reference_context",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceRelationType} == {
        "intent_has_scope",
        "scope_selects_target",
        "digest_informs_intent",
        "digest_informs_plan",
        "context_supports_plan",
        "plan_contains_change_node",
        "plan_contains_dependency_edge",
        "change_node_targets_file",
        "graph_produces_diff_envelope",
        "diff_envelope_contains_structured_patch",
        "diff_envelope_contains_unified_diff",
        "structured_patch_contains_file_proposal",
        "file_proposal_contains_hunk",
        "risk_report_scans_diff",
        "risk_signal_blocks_proposal",
        "review_packet_summarizes_diff",
        "review_packet_includes_risk_report",
        "review_packet_has_checklist",
        "review_packet_has_approval_gate",
        "review_decision_records_outcome",
        "trace_packet_contains_event",
        "trace_packet_contains_object",
        "digestion_prefers_pattern_adaptation",
        "dominion_pattern_future_gated",
        "external_agent_pattern_blocked",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceAttributeKind} == {
        "summary",
        "status",
        "readiness_level",
        "decision_kind",
        "outcome_kind",
        "risk_kind",
        "severity",
        "target_path_ref",
        "proposal_ref",
        "review_status",
        "approval_gate_kind",
        "approved_for_review",
        "approved_for_apply",
        "redaction_status",
        "truncation_status",
        "source_ref",
        "evidence_ref",
        "digest_ref",
        "context_snapshot_ref",
        "patch_plan_ref",
        "diff_envelope_ref",
        "risk_report_ref",
        "review_packet_ref",
        "external_agent_pattern_kind",
        "digestion_dominion_disposition",
        "timestamp",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceSinkKind} == {
        "returned_trace_packet",
        "in_memory_test_sink",
        "disabled",
        "future_internal_ocel_store",
        "external_trace_sink_blocked",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceStatus} == {
        "unknown",
        "planned",
        "policy_checked",
        "emitted_as_packet",
        "emitted_to_in_memory_sink",
        "blocked",
        "skipped",
        "no_op",
        "safe_failed",
    }
    assert {item.value for item in PatchProposalTraceDecisionKind} == {
        "allow_trace_packet_creation",
        "allow_in_memory_test_sink",
        "deny",
        "block",
        "skip",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceRiskKind} == {
        "raw_diff_persistence_risk",
        "raw_source_persistence_risk",
        "raw_review_packet_persistence_risk",
        "secret_content_trace_risk",
        "credential_content_trace_risk",
        "token_content_trace_risk",
        "unbounded_payload_risk",
        "full_file_content_trace_risk",
        "patch_apply_confusion_risk",
        "write_edit_confusion_risk",
        "approval_metadata_confusion_risk",
        "external_agent_execution_confusion_risk",
        "dominion_runtime_confusion_risk",
        "infinite_agent_loop_risk",
        "reference_execution_confusion_risk",
        "persistent_trace_write_risk",
        "external_trace_sink_risk",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceSourceKind} == {
        "v0356_patch_review_packet",
        "v0356_approval_gate_metadata",
        "v0356_reviewer_decision_record",
        "v0355_patch_proposal_risk_report",
        "v0355_patch_risk_scan_decision",
        "v0354_diff_proposal_envelope",
        "v0354_unified_diff_proposal",
        "v0354_structured_patch_proposal",
        "v0353_patch_plan",
        "v0353_change_set_graph",
        "v0352_context_snapshot",
        "v0352_evidence_bundle",
        "v0351_intent_scope_bundle",
        "v0350_reference_pattern_digest",
        "external_agent_control_observation",
        "digestion_dominion_policy_note",
        "test_fixture",
        "opencode_reference_context_ref",
        "hermes_reference_context_ref",
        "openclaw_reference_context_ref",
        "unknown",
    }
    assert {item.value for item in PatchProposalTraceReadinessLevel} == {
        "not_ready",
        "trace_contract_ready",
        "trace_packet_ready",
        "bounded_patch_proposal_trace_ready",
        "digestion_dominion_trace_ready",
        "design_handoff_ready_for_v0358",
        "design_handoff_ready_for_v0359",
        "blocked",
        "future_track",
    }
    assert {item.value for item in ExternalAgentControlPatternKind} == {
        "codex_to_claude_code_loop",
        "codex_to_external_agent_chain",
        "claude_code_unbounded_loop",
        "opencode_execution_loop",
        "hermes_execution_loop",
        "openclaw_execution_loop",
        "recursive_agent_self_invocation",
        "infinite_agent_loop",
        "harness_orchestration_pattern",
        "dominion_like_external_control",
        "safe_static_digest_pattern",
        "no_external_agent_control",
        "unknown",
    }
    assert {item.value for item in DigestionDominionDisposition} == {
        "digestion_first",
        "safely_digested",
        "adapted_without_execution",
        "rejected_for_safety",
        "dominion_future_gated",
        "dominion_blocked",
        "external_agent_execution_blocked",
        "infinite_loop_blocked",
        "insufficient_evidence",
        "unknown",
    }


def test_required_models_are_exported() -> None:
    for model in (
        PatchProposalTraceFlagSet,
        PatchProposalTraceSourceRef,
        PatchProposalTracePolicy,
        PatchProposalTraceObject,
        PatchProposalTraceEvent,
        PatchProposalTraceRelation,
        PatchProposalTraceAttribute,
        ExternalAgentControlPatternRecord,
        DigestionDominionTraceRecord,
        PatchProposalTracePacket,
        PatchProposalTraceEmissionInput,
        PatchProposalTraceEmissionDecision,
        PatchProposalTraceValidationReport,
        PatchProposalTraceEmissionReport,
        PatchProposalTraceEmitter,
        PatchProposalTraceRunPreview,
        PatchProposalTraceNoPersistenceGuarantee,
        V0357ReadinessReport,
    ):
        assert inspect.isclass(model)


def test_trace_flags_allow_trace_readiness_and_block_unsafe() -> None:
    flags = build_patch_proposal_trace_flags()
    assert flags.patch_proposal_trace_layer_constructed is True
    assert flags.trace_packet_creation_available is True
    assert flags.trace_validation_available is True
    assert flags.digestion_dominion_trace_metadata_available is True
    assert flags.external_agent_control_pattern_trace_available is True
    assert flags.ready_for_v0358_cli_patch_proposal_surface is True
    assert flags.ready_for_v0359_consolidation is True
    assert flags.ready_for_patch_proposal_trace_packet_creation is True
    assert flags.ready_for_bounded_patch_proposal_ocel_trace_emission is True
    assert flags.ready_for_digestion_dominion_trace_metadata is True
    assert flags.ready_for_external_agent_control_pattern_trace is True
    assert patch_proposal_trace_flags_preserve_unsafe_false(flags) is True

    unsafe_flags = (
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_dominion_runtime",
        "ready_for_infinite_agent_loop",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_general_agent_execution",
        "ready_for_autonomous_agent_runtime",
        "ready_for_general_tool_execution",
        "ready_for_unquarantined_action_execution",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "ready_for_ui_runtime",
        "ready_for_external_control",
        "ready_for_authority_grant",
        "production_certified",
    )
    for flag_name in unsafe_flags:
        with pytest.raises(ValueError):
            build_patch_proposal_trace_flags(**{flag_name: True})


def test_trace_policy_blocks_raw_payloads_persistence_and_external_agents() -> None:
    policy = default_patch_proposal_trace_policy()
    assert patch_proposal_trace_policy_blocks_persistence(policy) is True
    assert policy.allow_raw_diff is False
    assert policy.allow_raw_source is False
    assert policy.allow_raw_review_packet is False
    assert policy.allow_secret_content is False
    assert policy.allow_credential_content is False
    assert policy.allow_token_content is False
    assert policy.allow_full_file_content is False
    assert policy.allow_persistent_write is False
    assert policy.allow_external_sink is False
    assert policy.allow_external_agent_execution is False
    assert policy.allow_dominion_runtime is False
    assert policy.allow_infinite_agent_loop is False
    assert {"secret", "key", "token", "credential", "pem", "id_rsa"}.issubset(set(policy.prohibited_payload_patterns))

    for blocked_field in (
        "allow_raw_diff",
        "allow_raw_source",
        "allow_raw_review_packet",
        "allow_secret_content",
        "allow_credential_content",
        "allow_token_content",
        "allow_full_file_content",
        "allow_persistent_write",
        "allow_external_sink",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
        "allow_infinite_agent_loop",
    ):
        with pytest.raises(ValueError):
            build_patch_proposal_trace_policy(**{blocked_field: True})

    with pytest.raises(ValueError):
        build_patch_proposal_trace_policy(allowed_sink_kinds=[PatchProposalTraceSinkKind.FUTURE_INTERNAL_OCEL_STORE])
    with pytest.raises(ValueError):
        build_patch_proposal_trace_policy(allowed_sink_kinds=[PatchProposalTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED])
    with pytest.raises(ValueError):
        build_patch_proposal_trace_policy(prohibited_payload_patterns=["secret", "key"])


def test_trace_source_and_artifacts_are_bounded_sanitized_metadata() -> None:
    policy = build_patch_proposal_trace_policy(max_attribute_chars=32)
    source_ref = build_patch_proposal_trace_source_ref(
        source_kind=PatchProposalTraceSourceKind.TEST_FIXTURE,
        source_id="fixture:trace",
        source_summary="Bounded fixture metadata.",
    )
    attr = build_patch_proposal_trace_attribute(
        attribute_kind=PatchProposalTraceAttributeKind.SUMMARY,
        key="summary",
        value="x" * 80,
        policy=policy,
    )
    assert len(attr.value_preview) <= 32
    assert attr.truncated is True

    redacted = build_patch_proposal_trace_attribute(
        attribute_kind=PatchProposalTraceAttributeKind.EVIDENCE_REF,
        key="evidence",
        value="token=abc123",
        policy=policy,
    )
    assert redacted.redacted is True
    assert "[redacted]" in redacted.value_preview
    assert "abc123" not in redacted.value_preview

    obj = build_patch_proposal_trace_object(
        object_type=PatchProposalTraceObjectType.PATCH_REVIEW_PACKET,
        object_key="review:1",
        object_summary="Review packet metadata only.",
        source_refs=[source_ref],
    )
    event = build_patch_proposal_trace_event(
        event_kind=PatchProposalTraceEventKind.HUMAN_REVIEW_PACKET_CREATED,
        event_summary="Review packet traced.",
        source_refs=[source_ref],
    )
    relation = build_patch_proposal_trace_relation(
        relation_type=PatchProposalTraceRelationType.TRACE_PACKET_CONTAINS_OBJECT,
        source_object_id="trace:1",
        target_object_id=obj.object_id,
    )
    assert not hasattr(obj, "ready_for_execution")
    assert not hasattr(event, "ready_for_execution")
    assert not hasattr(relation, "ready_for_execution")
    with pytest.raises(ValueError):
        build_patch_proposal_trace_attribute(
            attribute_kind=PatchProposalTraceAttributeKind.EVIDENCE_REF,
            key="evidence",
            value_preview="token=abc123",
            redacted=False,
            policy=policy,
        )


def test_external_agent_and_digestion_records_never_execute() -> None:
    record = build_external_agent_control_pattern_record(
        pattern_kind=ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP,
        pattern_summary="Codex-to-Claude-Code-like loop observed as metadata.",
    )
    assert record.rejected is True
    assert record.future_gated is True
    assert external_agent_pattern_record_is_not_execution(record) is True

    safe_record = build_external_agent_control_pattern_record(
        pattern_kind=ExternalAgentControlPatternKind.SAFE_STATIC_DIGEST_PATTERN,
        disposition=DigestionDominionDisposition.SAFELY_DIGESTED,
        pattern_summary="Static digest pattern.",
        rejected=False,
        future_gated=False,
    )
    assert safe_record.execution_allowed is False
    assert safe_record.dominion_runtime_allowed is False

    with pytest.raises(ValueError):
        build_external_agent_control_pattern_record(execution_allowed=True)
    with pytest.raises(ValueError):
        build_external_agent_control_pattern_record(dominion_runtime_allowed=True)
    with pytest.raises(ValueError):
        build_external_agent_control_pattern_record(
            pattern_kind=ExternalAgentControlPatternKind.INFINITE_AGENT_LOOP,
            rejected=False,
            future_gated=False,
        )

    digestion = build_digestion_dominion_trace_record()
    assert digestion_dominion_record_is_not_runtime(digestion) is True
    with pytest.raises(ValueError):
        build_digestion_dominion_trace_record(execution_allowed=True)
    with pytest.raises(ValueError):
        build_digestion_dominion_trace_record(dominion_runtime_allowed=True)
    with pytest.raises(ValueError):
        build_digestion_dominion_trace_record(infinite_loop_allowed=True)


def test_trace_packet_emission_validation_guarantee_and_readiness() -> None:
    packet = build_patch_proposal_trace_packet()
    assert patch_proposal_trace_packet_is_not_persistence(packet) is True
    assert packet.sink_kind == PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_execution is False

    with pytest.raises(ValueError):
        build_patch_proposal_trace_packet(ready_for_persistent_write=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_packet(ready_for_external_sink=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_packet(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_packet(sink_kind=PatchProposalTraceSinkKind.FUTURE_INTERNAL_OCEL_STORE)

    emission_input = build_patch_proposal_trace_emission_input()
    assert emission_input.allow_raw_diff is False
    assert emission_input.allow_secret_content is False
    assert emission_input.allow_external_agent_execution is False
    assert emission_input.allow_dominion_runtime is False
    assert emission_input.allow_persistent_write is False
    for blocked_field in (
        "allow_raw_diff",
        "allow_raw_source",
        "allow_raw_review_packet",
        "allow_secret_content",
        "allow_credential_content",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
        "allow_persistent_write",
    ):
        with pytest.raises(ValueError):
            build_patch_proposal_trace_emission_input(**{blocked_field: True})

    decision = build_patch_proposal_trace_emission_decision()
    assert decision.persistent_write_allowed is False
    assert decision.external_sink_allowed is False
    assert decision.ready_for_execution is False
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emission_decision(persistent_write_allowed=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emission_decision(external_sink_allowed=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emission_decision(ready_for_execution=True)

    report = build_patch_proposal_trace_validation_report(blocked_items=["secret-like attribute"], valid=False)
    assert report.valid is False
    assert report.ready_for_persistent_write is False
    with pytest.raises(ValueError):
        build_patch_proposal_trace_validation_report(blocked_items=["blocked"], valid=True)
    with pytest.raises(ValueError):
        build_patch_proposal_trace_validation_report(ready_for_execution=True)

    emitter = build_patch_proposal_trace_emitter()
    assert emitter.ready_for_persistent_write is False
    assert emitter.ready_for_external_sink is False
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emitter(supported_sink_kinds=[PatchProposalTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED])
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emitter(ready_for_persistent_write=True)

    emission_report = build_patch_proposal_trace_emission_report()
    assert emission_report.persistent_write_performed is False
    assert emission_report.external_sink_used is False
    with pytest.raises(ValueError):
        build_patch_proposal_trace_emission_report(persistent_write_performed=True)

    preview = build_patch_proposal_trace_run_preview()
    guarantee = build_patch_proposal_trace_no_persistence_guarantee()
    readiness = build_v0357_readiness_report()
    assert preview.no_trace_persistence_guarantee is True
    assert preview.no_external_agent_execution_guarantee is True
    assert preview.no_dominion_runtime_guarantee is True
    assert all(value is True for key, value in guarantee.__dict__.items() if key.startswith("no_"))
    assert v0357_readiness_report_is_not_execution_ready(readiness) is True
    assert readiness.ready_for_v0358_cli_patch_proposal_surface is True
    assert readiness.ready_for_v0359_consolidation is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_persistent_trace_write is False


def test_trace_packet_builders_consume_review_risk_diff_and_plan_metadata() -> None:
    diff_envelope = build_diff_proposal_envelope()
    risk_report = build_patch_proposal_risk_report_from_scan(diff_envelope)
    review_packet = build_patch_review_packet()
    patch_plan = build_patch_plan()

    review_trace = build_patch_proposal_trace_packet_from_review_packet(review_packet)
    risk_trace = build_patch_proposal_trace_packet_from_risk_report(risk_report)
    diff_trace = build_patch_proposal_trace_packet_from_diff_envelope(diff_envelope)
    plan_trace = build_patch_proposal_trace_packet_from_patch_plan(patch_plan)

    assert review_trace.objects[0].object_type == PatchProposalTraceObjectType.PATCH_REVIEW_PACKET
    assert risk_trace.objects[0].object_type == PatchProposalTraceObjectType.PATCH_PROPOSAL_RISK_REPORT
    assert diff_trace.objects[0].object_type == PatchProposalTraceObjectType.DIFF_PROPOSAL_ENVELOPE
    assert plan_trace.objects[0].object_type == PatchProposalTraceObjectType.PATCH_PLAN
    assert any(event.event_kind == PatchProposalTraceEventKind.HUMAN_REVIEW_PACKET_CREATED for event in review_trace.events)
    assert any(event.event_kind == PatchProposalTraceEventKind.PATCH_RISK_SCANNED for event in risk_trace.events)
    assert any(event.event_kind == PatchProposalTraceEventKind.DIFF_PROPOSAL_CREATED for event in diff_trace.events)
    assert any(event.event_kind == PatchProposalTraceEventKind.PATCH_PLAN_CREATED for event in plan_trace.events)
    for packet in (review_trace, risk_trace, diff_trace, plan_trace):
        assert patch_proposal_trace_packet_is_not_persistence(packet) is True


def test_missing_inputs_return_blocked_trace_metadata() -> None:
    for packet in (
        build_patch_proposal_trace_packet_from_review_packet(None),
        build_patch_proposal_trace_packet_from_risk_report(None),
        build_patch_proposal_trace_packet_from_diff_envelope(None),
        build_patch_proposal_trace_packet_from_patch_plan(None),
    ):
        assert packet.status == PatchProposalTraceStatus.BLOCKED
        assert packet.ready_for_execution is False
        assert packet.ready_for_persistent_write is False


def test_digest_and_external_agent_metadata_records_are_blocked_or_future_gated() -> None:
    pattern = build_reference_harness_pattern(
        pattern_id="pattern:agent-loop",
        pattern_kind=ReferenceHarnessPatternKind.AGENT_LOOP_PATTERN,
        disposition=ReferencePatternDisposition.FUTURE_TRACK,
        pattern_summary="External agent control loop observed.",
        chantacore_adaptation="Trace as blocked/future-gated metadata only.",
        future_track_note="Requires future Dominion gate.",
    )
    rejected = build_reference_harness_pattern(
        pattern_id="pattern:unsafe-reference",
        pattern_kind=ReferenceHarnessPatternKind.UNSAFE_EXECUTION_PATTERN,
        disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY,
        pattern_summary="Reference execution rejected.",
        chantacore_adaptation="Do not execute reference harness.",
        rejection_reason="Reference harness execution blocked.",
    )
    digest = build_reference_pattern_digest(patterns=[pattern, rejected])
    records = build_digestion_dominion_records_from_reference_digest(digest)
    assert records[0].disposition == DigestionDominionDisposition.DOMINION_FUTURE_GATED
    assert "future gated Dominion review" in records[0].future_track_items
    assert records[1].disposition == DigestionDominionDisposition.REJECTED_FOR_SAFETY
    assert all(digestion_dominion_record_is_not_runtime(record) for record in records)

    missing_digest_records = build_digestion_dominion_records_from_reference_digest(None)
    assert missing_digest_records[0].disposition == DigestionDominionDisposition.INSUFFICIENT_EVIDENCE
    assert missing_digest_records[0].execution_allowed is False

    pattern_records = build_external_agent_pattern_records_from_metadata(
        {"external_agent_patterns": [ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP]}
    )
    assert pattern_records[0].pattern_kind == ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP
    assert pattern_records[0].rejected is True
    assert pattern_records[0].future_gated is True
    assert pattern_records[0].execution_allowed is False


def test_emission_decision_and_emit_return_packet_only() -> None:
    policy = default_patch_proposal_trace_policy()
    emission_input = build_patch_proposal_trace_emission_input()
    decision = decide_patch_proposal_trace_emission(emission_input, policy)
    assert decision.decision_kind == PatchProposalTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION
    assert decision.persistent_write_allowed is False

    in_memory_input = build_patch_proposal_trace_emission_input(requested_sink_kind=PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK)
    in_memory_decision = decide_patch_proposal_trace_emission(in_memory_input, policy)
    assert in_memory_decision.decision_kind == PatchProposalTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK
    assert in_memory_decision.external_sink_allowed is False

    blocked_input = build_patch_proposal_trace_emission_input(requested_sink_kind=PatchProposalTraceSinkKind.FUTURE_INTERNAL_OCEL_STORE)
    blocked_decision = decide_patch_proposal_trace_emission(blocked_input, policy)
    assert blocked_decision.decision_kind == PatchProposalTraceDecisionKind.BLOCK

    emitter = build_patch_proposal_trace_emitter()
    supplied = build_patch_proposal_trace_packet(trace_packet_id="trace_packet:test:supplied")
    emitted = emit_patch_proposal_trace_packet(emission_input, emitter, supplied_packet=supplied)
    assert emitted is supplied

    blocked_packet = emit_patch_proposal_trace_packet(blocked_input, emitter, supplied_packet=supplied)
    assert blocked_packet.status == PatchProposalTraceStatus.BLOCKED
    assert blocked_packet.ready_for_persistent_write is False
    assert blocked_packet.ready_for_external_sink is False

    invalid_attribute = build_patch_proposal_trace_attribute(
        attribute_kind=PatchProposalTraceAttributeKind.EVIDENCE_REF,
        key="evidence",
        value_preview="token=abc123",
        redacted=True,
    )
    invalid_packet = build_patch_proposal_trace_packet(attributes=[invalid_attribute])
    validation = validate_patch_proposal_trace_packet(invalid_packet)
    assert validation.valid is True


def test_readiness_report_blocks_all_unsafe_true_overrides() -> None:
    for field in (
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_dominion_runtime",
        "ready_for_infinite_agent_loop",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "production_certified",
    ):
        with pytest.raises(ValueError):
            build_v0357_readiness_report(**{field: True})


def test_helpers_do_not_use_forbidden_runtime_capabilities() -> None:
    source = inspect.getsource(trace_module)
    forbidden_tokens = (
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        ".write_text(",
        ".write_bytes(",
        "import subprocess",
        "subprocess.",
        "os.system(",
        "shell=True",
        " open(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
        "json.dump",
        "sqlite",
    )
    for token in forbidden_tokens:
        assert token not in source

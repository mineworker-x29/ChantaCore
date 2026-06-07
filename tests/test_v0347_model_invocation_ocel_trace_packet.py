import inspect

import pytest

from chanta_core.agent_runtime import (
    ModelBackedStepOutcomeKind,
    ModelBackedStepStatus,
    ModelInvocationTraceAttribute,
    ModelInvocationTraceAttributeKind,
    ModelInvocationTraceDecisionKind,
    ModelInvocationTraceEmissionDecision,
    ModelInvocationTraceEmissionReport,
    ModelInvocationTraceEventKind,
    ModelInvocationTraceFlagSet,
    ModelInvocationTraceNoPersistenceGuarantee,
    ModelInvocationTraceObjectType,
    ModelInvocationTracePacket,
    ModelInvocationTracePolicy,
    ModelInvocationTraceReadinessLevel,
    ModelInvocationTraceRelationType,
    ModelInvocationTraceRiskKind,
    ModelInvocationTraceRunPreview,
    ModelInvocationTraceSinkKind,
    ModelInvocationTraceSourceKind,
    ModelInvocationTraceSourceRef,
    ModelInvocationTraceStatus,
    V0347ReadinessReport,
    ExistingProviderBoundaryOutcomeKind,
    build_existing_provider_boundary_invocation_result,
    build_model_backed_step_execution_record,
    build_model_backed_step_output,
    build_model_invocation_trace_attribute,
    build_model_invocation_trace_emission_input,
    build_model_invocation_trace_emission_report,
    build_model_invocation_trace_emitter,
    build_model_invocation_trace_event,
    build_model_invocation_trace_flags,
    build_model_invocation_trace_no_persistence_guarantee,
    build_model_invocation_trace_object,
    build_model_invocation_trace_packet,
    build_model_invocation_trace_packet_from_model_backed_step_output,
    build_model_invocation_trace_packet_from_provider_boundary_result,
    build_model_invocation_trace_packet_from_quarantine_packet,
    build_model_invocation_trace_policy,
    build_model_invocation_trace_relation,
    build_model_invocation_trace_run_preview,
    build_model_invocation_trace_source_ref,
    build_model_invocation_trace_validation_report,
    build_model_output_action_candidate,
    build_model_output_action_quarantine_packet_from_candidates,
    build_v0347_readiness_report,
    decide_model_invocation_trace_emission,
    default_model_invocation_trace_policy,
    emit_model_invocation_trace_packet,
    model_invocation_trace_flags_preserve_unsafe_false,
    model_invocation_trace_packet_is_not_persistence,
    model_invocation_trace_policy_blocks_raw_payloads,
    model_invocation_trace_report_is_not_persistent_write,
    sanitize_model_invocation_trace_attribute_value,
    v0347_readiness_report_is_not_execution_ready,
    validate_model_invocation_trace_packet,
)
from chanta_core.agent_runtime import model_invocation_trace
from chanta_core.agent_runtime.model_invocation_trace import (
    DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS,
    DEFAULT_V0347_PROHIBITED_UNTIL_LATER_GATE,
    UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES,
)
from chanta_core.agent_runtime.model_output_quarantine import ModelOutputActionCandidateKind


def _fake_model_backed_step_output(secret_text=""):
    record = build_model_backed_step_execution_record(
        "record:model_step",
        step_input_id="step_input:model",
        decision_id="decision:model",
        status=ModelBackedStepStatus.BOUNDED_STEP_COMPLETED,
        executed_bounded_model_backed_step=True,
    )
    return build_model_backed_step_output(
        "output:model_step",
        step_input_id="step_input:model",
        status=ModelBackedStepStatus.BOUNDED_STEP_COMPLETED,
        outcome_kind=ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT,
        final_response_text=f"Raw model output should not be traced token={secret_text}",
        execution_record=record,
        quarantine_packet_ref="packet:quarantine",
        agent_step_output_ref="agent_step_output:1",
        redacted=True,
        summary="Model-backed step output summary.",
    )


def _fake_quarantine_packet():
    candidate = build_model_output_action_candidate(
        "candidate:final",
        candidate_kind=ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE,
        candidate_preview="Final preview token=should-not-leak",
    )
    return build_model_output_action_quarantine_packet_from_candidates([candidate])


def test_model_invocation_trace_taxonomies_and_flags_are_conservative():
    assert "model_request_envelope_created" in {item.value for item in ModelInvocationTraceEventKind}
    assert "model_backed_step_output" in {item.value for item in ModelInvocationTraceObjectType}
    assert "model_backed_step_has_execution_record" in {item.value for item in ModelInvocationTraceRelationType}
    assert "bounded_payload" in {item.value for item in ModelInvocationTraceAttributeKind}
    assert "returned_trace_packet" in {item.value for item in ModelInvocationTraceSinkKind}
    assert "emitted_as_packet" in {item.value for item in ModelInvocationTraceStatus}
    assert "allow_trace_packet_creation" in {item.value for item in ModelInvocationTraceDecisionKind}
    assert "raw_prompt_persistence_risk" in {item.value for item in ModelInvocationTraceRiskKind}
    assert "v0346_model_backed_step_output" in {item.value for item in ModelInvocationTraceSourceKind}
    assert "bounded_model_invocation_trace_ready" in {item.value for item in ModelInvocationTraceReadinessLevel}

    flags = build_model_invocation_trace_flags(
        model_invocation_trace_packet_constructed=True,
        model_invocation_trace_validation_available=True,
        bounded_model_invocation_ocel_trace_emission_enabled=True,
        ready_for_v0348_cli_model_backed_agent_step_surface=True,
        ready_for_model_invocation_trace_packet_creation=True,
        ready_for_bounded_model_invocation_ocel_trace_emission=True,
    )

    assert flags.ready_for_model_invocation_trace_packet_creation is True
    assert flags.ready_for_bounded_model_invocation_ocel_trace_emission is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_ocel_emission is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_external_trace_sink is False
    assert flags.ready_for_provider_invocation is False
    assert model_invocation_trace_flags_preserve_unsafe_false(flags)

    for flag_name in UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES:
        with pytest.raises(ValueError):
            ModelInvocationTraceFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.34.7",
                **{flag_name: True},
            )


def test_source_ref_and_policy_block_raw_secret_persistent_external_content():
    source = build_model_invocation_trace_source_ref(
        "source:opencode",
        ModelInvocationTraceSourceKind.OPENCODE_REFERENCE_CONTEXT_REF,
        "references/OpenCode",
        "OpenCode path ref only.",
    )
    policy = default_model_invocation_trace_policy()

    assert isinstance(source, ModelInvocationTraceSourceRef)
    assert source.execution is False
    assert source.provider_call is False
    assert source.file_read is False
    assert model_invocation_trace_policy_blocks_raw_payloads(policy)
    assert set(DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS).issubset(set(policy.prohibited_payload_patterns))
    assert policy.allow_raw_prompt is False
    assert policy.allow_raw_response is False
    assert policy.allow_raw_model_output is False
    assert policy.allow_secret_content is False
    assert policy.allow_credential_content is False
    assert policy.allow_token_content is False
    assert policy.allow_full_file_content is False
    assert policy.allow_persistent_write is False
    assert policy.allow_external_sink is False

    with pytest.raises(ValueError):
        build_model_invocation_trace_source_ref("source:bad", metadata={"file_read": True})
    for field_name in (
        "allow_raw_prompt",
        "allow_raw_response",
        "allow_raw_model_output",
        "allow_secret_content",
        "allow_credential_content",
        "allow_token_content",
        "allow_full_file_content",
        "allow_persistent_write",
        "allow_external_sink",
    ):
        with pytest.raises(ValueError):
            ModelInvocationTracePolicy(
                trace_policy_id=f"policy:bad:{field_name}",
                prohibited_payload_patterns=list(DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS),
                **{field_name: True},
            )


def test_trace_artifacts_are_bounded_sanitized_and_not_persistence():
    policy = build_model_invocation_trace_policy(max_attribute_chars=24)
    redacted_attribute = sanitize_model_invocation_trace_attribute_value("api token should be removed", policy)
    truncated_attribute = sanitize_model_invocation_trace_attribute_value("x" * 100, policy)
    obj = build_model_invocation_trace_object(
        "object:model_step",
        ModelInvocationTraceObjectType.MODEL_BACKED_STEP_OUTPUT,
        "step_output:1",
        {"summary": "short", "source_ref": "references/OpenCode"},
        policy=policy,
    )
    event = build_model_invocation_trace_event(
        "event:model_step",
        ModelInvocationTraceEventKind.MODEL_BACKED_STEP_COMPLETED,
        "Model step completed",
        {"status": "completed"},
        [obj.object_id],
        policy=policy,
    )
    relation = build_model_invocation_trace_relation(
        "relation:step:record",
        ModelInvocationTraceRelationType.MODEL_BACKED_STEP_HAS_EXECUTION_RECORD,
        obj.object_id,
        "object:record",
        policy=policy,
    )
    attribute = build_model_invocation_trace_attribute(
        "attribute:summary",
        ModelInvocationTraceAttributeKind.SUMMARY,
        "summary",
        "bounded",
        policy=policy,
    )
    packet = build_model_invocation_trace_packet(
        "packet:trace",
        objects=[obj],
        events=[event],
        relations=[relation],
        attributes=[attribute, redacted_attribute, truncated_attribute],
        redaction_applied=True,
        truncated=True,
    )

    assert redacted_attribute.value_preview == "[redacted]"
    assert redacted_attribute.redacted is True
    assert truncated_attribute.truncated is True
    assert len(truncated_attribute.value_preview) <= policy.max_attribute_chars
    assert isinstance(packet, ModelInvocationTracePacket)
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_execution is False
    assert model_invocation_trace_packet_is_not_persistence(packet)

    report = validate_model_invocation_trace_packet(packet, policy)
    assert report.validation_passed is True
    assert report.ready_for_persistent_write is False
    assert report.ready_for_execution is False

    with pytest.raises(ValueError):
        ModelInvocationTraceAttribute(
            attribute_id="attribute:bad",
            attribute_kind=ModelInvocationTraceAttributeKind.SUMMARY,
            key="summary",
            value_preview="token=not allowed",
        )
    with pytest.raises(ValueError):
        build_model_invocation_trace_packet("packet:bad", ready_for_persistent_write=True)


def test_emission_input_decision_reports_emitter_preview_guarantee_readiness():
    emission_input = build_model_invocation_trace_emission_input(
        "emission:1",
        model_backed_step_output_id="output:1",
    )
    policy = default_model_invocation_trace_policy()
    decision = decide_model_invocation_trace_emission(emission_input, policy)
    validation = build_model_invocation_trace_validation_report(
        "validation:1",
        blocked_items=["unsafe_attribute"],
        validation_passed=False,
    )
    report = build_model_invocation_trace_emission_report(
        "report:1",
        emission_input_id=emission_input.emission_input_id,
        trace_packet_id="packet:1",
        validation_report_id=validation.validation_report_id,
        event_count=1,
        object_count=1,
        relation_count=1,
        ready_for_v0348_cli_model_backed_agent_step_surface=True,
        ready_for_model_invocation_trace_packet_creation=True,
        ready_for_bounded_model_invocation_ocel_trace_emission=True,
    )
    emitter = build_model_invocation_trace_emitter()
    preview = build_model_invocation_trace_run_preview(emitter_id=emitter.emitter_id)
    guarantee = build_model_invocation_trace_no_persistence_guarantee()
    readiness = build_v0347_readiness_report(
        emitter_id=emitter.emitter_id,
        trace_packet_id="packet:1",
        trace_emission_report_id=report.report_id,
        validation_report_id=validation.validation_report_id,
    )

    assert set(emission_input.prohibited_trace_content) >= {
        "raw prompt",
        "raw response",
        "raw model output",
        "file content",
        "secrets",
        "credentials",
        "tokens",
        "unbounded output",
    }
    assert decision.decision_kind == ModelInvocationTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION
    assert isinstance(decision, ModelInvocationTraceEmissionDecision)
    assert decision.persistent_write_allowed is False
    assert decision.external_sink_allowed is False
    assert decision.ready_for_execution is False
    assert validation.validation_passed is False
    assert report.ready_for_model_invocation_trace_packet_creation is True
    assert report.ready_for_bounded_model_invocation_ocel_trace_emission is True
    assert model_invocation_trace_report_is_not_persistent_write(report)
    assert emitter.ready_for_model_invocation_trace_packet_creation is True
    assert emitter.ready_for_persistent_trace_write is False
    assert emitter.ready_for_external_sink is False
    assert emitter.ready_for_execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(preview, ModelInvocationTraceRunPreview)
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, ModelInvocationTraceNoPersistenceGuarantee)
    assert readiness.ready_for_model_invocation_trace_packet_creation is True
    assert readiness.ready_for_bounded_model_invocation_ocel_trace_emission is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_general_ocel_emission is False
    assert readiness.ready_for_persistent_trace_write is False
    assert readiness.ready_for_external_trace_sink is False
    assert v0347_readiness_report_is_not_execution_ready(readiness)
    assert set(DEFAULT_V0347_PROHIBITED_UNTIL_LATER_GATE).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        build_model_invocation_trace_validation_report(
            "validation:bad",
            blocked_items=["blocked"],
            validation_passed=True,
        )
    for flag_name in UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0347ReadinessReport(report_id=f"readiness:bad:{flag_name}", version="v0.34.7", **{flag_name: True})


def test_trace_packet_from_model_backed_step_output_omits_raw_output_and_secrets():
    policy = default_model_invocation_trace_policy()
    step_output = _fake_model_backed_step_output(secret_text="secret-value")
    packet = build_model_invocation_trace_packet_from_model_backed_step_output(step_output, policy)
    packet_text = str(packet)

    assert any(event.event_kind == ModelInvocationTraceEventKind.MODEL_BACKED_STEP_COMPLETED for event in packet.events)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_BACKED_STEP_OUTPUT for obj in packet.objects)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_BACKED_STEP_EXECUTION_RECORD for obj in packet.objects)
    assert any(rel.relation_type == ModelInvocationTraceRelationType.MODEL_BACKED_STEP_HAS_EXECUTION_RECORD for rel in packet.relations)
    assert "secret-value" not in packet_text
    assert "Raw model output should not be traced" not in packet_text
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_execution is False
    assert validate_model_invocation_trace_packet(packet, policy).validation_passed is True


def test_trace_packet_from_provider_boundary_result_omits_raw_response():
    policy = default_model_invocation_trace_policy()
    result = build_existing_provider_boundary_invocation_result(
        "provider_result:1",
        outcome_kind=ExistingProviderBoundaryOutcomeKind.EXISTING_BOUNDARY_RESPONSE_RETURNED,
        response_text_preview="raw response token=secret-value",
        response_char_count=31,
        response_envelope_id="response_envelope:1",
        redacted=True,
    )
    packet = build_model_invocation_trace_packet_from_provider_boundary_result(result, policy)
    packet_text = str(packet)

    assert any(event.event_kind == ModelInvocationTraceEventKind.EXISTING_PROVIDER_BOUNDARY_CALL_COMPLETED for event in packet.events)
    assert any(obj.object_type == ModelInvocationTraceObjectType.EXISTING_PROVIDER_BOUNDARY_INVOCATION for obj in packet.objects)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_RESPONSE_ENVELOPE for obj in packet.objects)
    assert any(rel.relation_type == ModelInvocationTraceRelationType.BOUNDARY_CALL_RETURNS_RESPONSE for rel in packet.relations)
    assert "secret-value" not in packet_text
    assert "raw response token" not in packet_text
    assert packet.ready_for_persistent_write is False
    assert validate_model_invocation_trace_packet(packet, policy).validation_passed is True


def test_trace_packet_from_quarantine_packet_records_candidates_decisions_routes_only():
    policy = default_model_invocation_trace_policy()
    quarantine_packet = _fake_quarantine_packet()
    packet = build_model_invocation_trace_packet_from_quarantine_packet(quarantine_packet, policy)
    packet_text = str(packet)

    assert any(event.event_kind == ModelInvocationTraceEventKind.MODEL_OUTPUT_ACTION_QUARANTINED for event in packet.events)
    assert any(event.event_kind == ModelInvocationTraceEventKind.MODEL_OUTPUT_ACTION_CANDIDATE_EXTRACTED for event in packet.events)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_OUTPUT_QUARANTINE_PACKET for obj in packet.objects)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_OUTPUT_ACTION_CANDIDATE for obj in packet.objects)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_OUTPUT_QUARANTINE_DECISION for obj in packet.objects)
    assert any(obj.object_type == ModelInvocationTraceObjectType.MODEL_OUTPUT_SAFE_ROUTE for obj in packet.objects)
    assert any(rel.relation_type == ModelInvocationTraceRelationType.QUARANTINE_PACKET_CONTAINS_CANDIDATE for rel in packet.relations)
    assert any(rel.relation_type == ModelInvocationTraceRelationType.CANDIDATE_ROUTED_TO_SAFE_ROUTE for rel in packet.relations)
    assert "should-not-leak" not in packet_text
    assert packet.ready_for_persistent_write is False
    assert validate_model_invocation_trace_packet(packet, policy).validation_passed is True


def test_emit_trace_packet_returns_artifact_only_and_blocks_external_sink():
    step_output = _fake_model_backed_step_output()
    emitter = build_model_invocation_trace_emitter()
    emission_input = build_model_invocation_trace_emission_input(
        "emission:step",
        model_backed_step_output_id=step_output.step_output_id,
    )
    packet = emit_model_invocation_trace_packet(emission_input, emitter, {"model_backed_step_output": step_output})

    assert packet.status == ModelInvocationTraceStatus.EMITTED_AS_PACKET
    assert model_invocation_trace_packet_is_not_persistence(packet)

    blocked_input = build_model_invocation_trace_emission_input(
        "emission:external",
        requested_sink_kind=ModelInvocationTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED,
    )
    blocked_packet = emit_model_invocation_trace_packet(blocked_input, emitter)
    assert blocked_packet.status == ModelInvocationTraceStatus.BLOCKED
    assert blocked_packet.ready_for_persistent_write is False
    assert blocked_packet.ready_for_external_sink is False


def test_model_invocation_trace_static_negative_patterns():
    source = inspect.getsource(model_invocation_trace)
    forbidden_fragments = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "eval(",
        "exec(",
        "importlib",
        "write_text(",
        "write_bytes(",
        "read_text(",
        "read_bytes(",
        "open(",
        "unlink(",
        "rmdir(",
        "mkdir(",
        "rename(",
        "replace(",
        "chmod(",
        "chown(",
        "shutil.",
        "sqlite",
        "logging.",
        "os.environ",
        "dotenv",
    ]
    unsafe_true_fragments = [
        "ready_for_execution=True",
        "ready_for_general_ocel_emission=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_external_trace_sink=True",
        "ready_for_provider_invocation=True",
        "ready_for_existing_boundary_invocation=True",
        "ready_for_agent_step_execution=True",
        "ready_for_tool_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_raw_prompt_persistence=True",
        "ready_for_raw_response_persistence=True",
        "ready_for_raw_model_output_persistence=True",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)
    assert not any(fragment in source for fragment in unsafe_true_fragments)

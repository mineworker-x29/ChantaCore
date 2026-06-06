import inspect

import pytest

from chanta_core.agent_runtime import (
    AgentActionDecisionKind,
    AgentActionProposalKind,
    AgentStepResultKind,
    AgentStepStatus,
    RuntimeOCELAttribute,
    RuntimeOCELAttributeKind,
    RuntimeOCELFlagSet,
    RuntimeOCELNoExternalSideEffectGuarantee,
    RuntimeOCELObjectType,
    RuntimeOCELRelationType,
    RuntimeOCELRunPreview,
    RuntimeOCELSourceRef,
    RuntimeOCELTraceDecisionKind,
    RuntimeOCELTraceEmissionDecision,
    RuntimeOCELTraceEmissionReport,
    RuntimeOCELTraceEventKind,
    RuntimeOCELTracePacket,
    RuntimeOCELTracePolicy,
    RuntimeOCELTraceReadinessLevel,
    RuntimeOCELTraceRiskKind,
    RuntimeOCELTraceSinkKind,
    RuntimeOCELTraceSourceKind,
    RuntimeOCELTraceStatus,
    V0337ReadinessReport,
    build_agent_action_decision,
    build_agent_action_proposal,
    build_agent_safe_tool_execution_result,
    build_agent_step_execution_record,
    build_agent_step_output,
    build_agent_supplied_model_output,
    build_agent_runtime_session,
    build_agent_runtime_session_snapshot,
    build_runtime_ocel_attribute,
    build_runtime_ocel_event,
    build_runtime_ocel_flags,
    build_runtime_ocel_no_external_side_effect_guarantee,
    build_runtime_ocel_object,
    build_runtime_ocel_packet_from_agent_step_output,
    build_runtime_ocel_packet_from_session_snapshot,
    build_runtime_ocel_relation,
    build_runtime_ocel_run_preview,
    build_runtime_ocel_source_ref,
    build_runtime_ocel_trace_emission_decision,
    build_runtime_ocel_trace_emission_input,
    build_runtime_ocel_trace_emission_report,
    build_runtime_ocel_trace_emitter,
    build_runtime_ocel_trace_packet,
    build_runtime_ocel_trace_policy,
    build_runtime_ocel_trace_validation_report,
    build_v0337_readiness_report,
    decide_runtime_ocel_trace_emission,
    default_runtime_ocel_trace_policy,
    emit_runtime_ocel_trace_packet,
    runtime_ocel_flags_preserve_unsafe_runtime_false,
    runtime_ocel_packet_is_not_persistence,
    runtime_ocel_policy_blocks_raw_outputs,
    runtime_ocel_trace_report_is_not_persistent_write,
    sanitize_runtime_ocel_attribute_value,
    v0337_readiness_report_is_not_general_runtime_ready,
    validate_runtime_ocel_trace_packet,
)
from chanta_core.agent_runtime import ocel_trace
from chanta_core.agent_runtime.ocel_trace import (
    DEFAULT_PROHIBITED_TRACE_CONTENT,
    DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS,
    DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE,
    UNSAFE_RUNTIME_OCEL_FLAG_NAMES,
)


def _fake_final_step_output(secret_text: str = ""):
    proposal = build_agent_action_proposal(
        "proposal:final",
        AgentActionProposalKind.FINAL_RESPONSE,
        model_output_id="model_output:1",
        proposed_final_response=f"Visible response should not be traced raw. {secret_text}",
    )
    decision = build_agent_action_decision(
        "decision:final",
        proposal.proposal_id,
        AgentActionDecisionKind.ALLOW_FINAL_RESPONSE,
        reason="Final response from supplied/mock output only.",
    )
    record = build_agent_step_execution_record(
        "record:final",
        "step_input:final",
        AgentStepStatus.RESPONSE_READY,
        proposal_id=proposal.proposal_id,
        decision_id=decision.decision_id,
        executed_bounded_step=True,
    )
    return build_agent_step_output(
        "step_output:final",
        "step_input:final",
        AgentStepStatus.RESPONSE_READY,
        AgentStepResultKind.FINAL_RESPONSE_RESULT,
        record,
        action_proposal=proposal,
        action_decision=decision,
        final_response_text=f"Raw final output omitted from trace. {secret_text}",
        summary="Final response output artifact.",
    )


def test_trace_taxonomies_and_flags_are_conservative():
    assert "agent_step_completed" in {item.value for item in RuntimeOCELTraceEventKind}
    assert "agent_step" in {item.value for item in RuntimeOCELObjectType}
    assert "step_proposes_action" in {item.value for item in RuntimeOCELRelationType}
    assert "bounded_output" in {item.value for item in RuntimeOCELAttributeKind}
    assert "returned_trace_packet" in {item.value for item in RuntimeOCELTraceSinkKind}
    assert "emitted_as_packet" in {item.value for item in RuntimeOCELTraceStatus}
    assert "allow_trace_packet_creation" in {item.value for item in RuntimeOCELTraceDecisionKind}
    assert "secret_content_trace_risk" in {item.value for item in RuntimeOCELTraceRiskKind}
    assert "v0336_agent_step_output" in {item.value for item in RuntimeOCELTraceSourceKind}
    assert "bounded_internal_trace_emission_ready" in {item.value for item in RuntimeOCELTraceReadinessLevel}

    flags = build_runtime_ocel_flags(
        trace_emitter_constructed=True,
        trace_artifact_creation_enabled=True,
        bounded_runtime_ocel_trace_emission_enabled=True,
        in_memory_trace_sink_enabled=True,
        ready_for_v0338_cli_agent_run_surface=True,
        ready_for_bounded_internal_ocel_trace_emission=True,
    )
    assert flags.trace_emitter_constructed is True
    assert flags.trace_artifact_creation_enabled is True
    assert flags.bounded_runtime_ocel_trace_emission_enabled is True
    assert flags.ready_for_bounded_internal_ocel_trace_emission is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_ocel_emission is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_external_trace_sink is False
    assert runtime_ocel_flags_preserve_unsafe_runtime_false(flags)

    for flag_name in UNSAFE_RUNTIME_OCEL_FLAG_NAMES:
        with pytest.raises(ValueError):
            RuntimeOCELFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.7",
                **{flag_name: True},
            )


def test_source_ref_and_policy_block_raw_secret_persistent_external_content():
    source = build_runtime_ocel_source_ref(
        "source:1",
        RuntimeOCELTraceSourceKind.OPENCODE_REFERENCE_CONTEXT_REF,
        "references/OpenCode",
        "OpenCode reference context label only.",
    )
    policy = default_runtime_ocel_trace_policy()

    assert isinstance(source, RuntimeOCELSourceRef)
    assert source.fetch is False
    assert source.file_read is False
    assert source.execution is False
    assert runtime_ocel_policy_blocks_raw_outputs(policy)
    assert set(DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS).issubset(set(policy.prohibited_payload_patterns))
    assert policy.allow_raw_model_output is False
    assert policy.allow_raw_tool_output is False
    assert policy.allow_file_content is False
    assert policy.allow_secret_content is False
    assert policy.allow_credential_content is False
    assert policy.allow_persistent_write is False
    assert policy.allow_external_sink is False

    with pytest.raises(ValueError):
        build_runtime_ocel_source_ref("source:bad", metadata={"file_read": True})
    for field_name in (
        "allow_raw_model_output",
        "allow_raw_tool_output",
        "allow_file_content",
        "allow_secret_content",
        "allow_credential_content",
        "allow_persistent_write",
        "allow_external_sink",
    ):
        with pytest.raises(ValueError):
            RuntimeOCELTracePolicy(
                trace_policy_id=f"policy:bad:{field_name}",
                prohibited_payload_patterns=list(DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS),
                **{field_name: True},
            )


def test_trace_artifacts_are_bounded_sanitized_and_not_persistence():
    policy = build_runtime_ocel_trace_policy(max_attribute_chars=24)
    redacted_attribute = sanitize_runtime_ocel_attribute_value("api token should be removed", policy)
    truncated_attribute = sanitize_runtime_ocel_attribute_value("x" * 100, policy)
    obj = build_runtime_ocel_object(
        "object:step:1",
        RuntimeOCELObjectType.AGENT_STEP,
        "step:1",
        {"summary": "short", "path_ref": "references/OpenCode"},
        policy=policy,
    )
    event = build_runtime_ocel_event(
        "event:step:1",
        RuntimeOCELTraceEventKind.AGENT_STEP_STARTED,
        "Agent step started",
        {"status": "planned"},
        [obj.object_id],
        policy=policy,
    )
    relation = build_runtime_ocel_relation(
        "relation:step:proposal",
        RuntimeOCELRelationType.STEP_PROPOSES_ACTION,
        obj.object_id,
        "object:proposal:1",
        policy=policy,
    )
    attribute = build_runtime_ocel_attribute(
        "attribute:summary",
        RuntimeOCELAttributeKind.SUMMARY,
        "summary",
        "bounded",
        policy=policy,
    )
    packet = build_runtime_ocel_trace_packet(
        "packet:1",
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
    assert isinstance(packet, RuntimeOCELTracePacket)
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_execution is False
    assert runtime_ocel_packet_is_not_persistence(packet)

    report = validate_runtime_ocel_trace_packet(packet, policy)
    assert report.validation_passed is True
    assert report.ready_for_persistent_write is False
    assert report.ready_for_execution is False

    with pytest.raises(ValueError):
        RuntimeOCELAttribute(
            attribute_id="attribute:bad",
            attribute_kind=RuntimeOCELAttributeKind.SUMMARY,
            key="summary",
            value_preview="token=not allowed",
        )
    with pytest.raises(ValueError):
        RuntimeOCELTracePacket(
            trace_packet_id="packet:bad",
            version="v0.33.7",
            sink_kind=RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
            ready_for_persistent_write=True,
        )


def test_emission_input_decision_reports_emitter_preview_and_guarantee():
    emission_input = build_runtime_ocel_trace_emission_input(
        "emission:1",
        agent_step_output_id="step_output:1",
    )
    policy = default_runtime_ocel_trace_policy()
    decision = decide_runtime_ocel_trace_emission(emission_input, policy)
    validation = build_runtime_ocel_trace_validation_report(
        "validation:1",
        blocked_items=["unsafe_attribute"],
        validation_passed=False,
    )
    report = build_runtime_ocel_trace_emission_report(
        "report:1",
        emission_input.emission_input_id,
        trace_packet_id="packet:1",
        validation_report_id=validation.validation_report_id,
        event_count=1,
        object_count=1,
        relation_count=0,
        ready_for_v0338_cli_agent_run_surface=True,
        ready_for_bounded_internal_ocel_trace_emission=True,
    )
    emitter = build_runtime_ocel_trace_emitter()
    preview = build_runtime_ocel_run_preview("preview:1", emitter_id=emitter.emitter_id)
    guarantee = build_runtime_ocel_no_external_side_effect_guarantee("guarantee:1")
    readiness = build_v0337_readiness_report(
        "readiness:1",
        emitter_id=emitter.emitter_id,
        trace_packet_id="packet:1",
        trace_emission_report_id=report.report_id,
        validation_report_id=validation.validation_report_id,
        bounded_runtime_ocel_trace_emission_enabled=True,
        trace_artifact_creation_enabled=True,
        ready_for_v0338_cli_agent_run_surface=True,
        ready_for_bounded_internal_ocel_trace_emission=True,
    )

    assert set(DEFAULT_PROHIBITED_TRACE_CONTENT).issubset(set(emission_input.prohibited_trace_content))
    assert decision.decision_kind == RuntimeOCELTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION
    assert isinstance(decision, RuntimeOCELTraceEmissionDecision)
    assert decision.persistent_write_allowed is False
    assert decision.external_sink_allowed is False
    assert decision.ready_for_execution is False
    assert validation.validation_passed is False
    assert report.ready_for_bounded_internal_ocel_trace_emission is True
    assert runtime_ocel_trace_report_is_not_persistent_write(report)
    assert emitter.ready_for_bounded_internal_trace_emission is True
    assert emitter.ready_for_persistent_trace_write is False
    assert emitter.ready_for_external_sink is False
    assert emitter.ready_for_execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(preview, RuntimeOCELRunPreview)
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, RuntimeOCELNoExternalSideEffectGuarantee)
    assert readiness.ready_for_bounded_internal_ocel_trace_emission is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_general_ocel_emission is False
    assert readiness.ready_for_persistent_trace_write is False
    assert readiness.ready_for_external_trace_sink is False
    assert v0337_readiness_report_is_not_general_runtime_ready(readiness)
    assert set(DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        build_runtime_ocel_trace_validation_report(
            "validation:bad",
            blocked_items=["blocked"],
            validation_passed=True,
        )
    for flag_name in UNSAFE_RUNTIME_OCEL_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0337ReadinessReport(report_id=f"readiness:bad:{flag_name}", version="v0.33.7", **{flag_name: True})


def test_trace_packet_from_fake_agent_step_output_omits_raw_output_and_secrets():
    policy = default_runtime_ocel_trace_policy()
    step_output = _fake_final_step_output(secret_text="token=secret-value")
    packet = build_runtime_ocel_packet_from_agent_step_output(step_output, policy)
    packet_text = str(packet)

    assert any(event.event_kind == RuntimeOCELTraceEventKind.AGENT_STEP_STARTED for event in packet.events)
    assert any(event.event_kind == RuntimeOCELTraceEventKind.ACTION_PROPOSED for event in packet.events)
    assert any(event.event_kind == RuntimeOCELTraceEventKind.ACTION_ALLOWED for event in packet.events)
    assert any(event.event_kind == RuntimeOCELTraceEventKind.FINAL_RESPONSE_READY for event in packet.events)
    assert any(obj.object_type == RuntimeOCELObjectType.AGENT_STEP for obj in packet.objects)
    assert any(obj.object_type == RuntimeOCELObjectType.ACTION_PROPOSAL for obj in packet.objects)
    assert any(obj.object_type == RuntimeOCELObjectType.ACTION_DECISION for obj in packet.objects)
    assert any(rel.relation_type == RuntimeOCELRelationType.STEP_PROPOSES_ACTION for rel in packet.relations)
    assert "secret-value" not in packet_text
    assert "Raw final output omitted from trace" not in packet_text
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_execution is False
    assert validate_runtime_ocel_trace_packet(packet, policy).validation_passed is True


def test_trace_packet_from_fake_session_snapshot_has_session_turn_relations():
    policy = default_runtime_ocel_trace_policy()
    session = build_agent_runtime_session(
        "session:1",
        active_turn_ids=["turn:1"],
        completed_turn_ids=["turn:2"],
        summary="Session snapshot summary only.",
    )
    snapshot = build_agent_runtime_session_snapshot("snapshot:1", session)
    packet = build_runtime_ocel_packet_from_session_snapshot(snapshot, policy)

    assert any(obj.object_type == RuntimeOCELObjectType.AGENT_SESSION for obj in packet.objects)
    assert sum(1 for obj in packet.objects if obj.object_type == RuntimeOCELObjectType.AGENT_TURN) == 2
    assert any(event.event_kind == RuntimeOCELTraceEventKind.AGENT_SESSION_CREATED for event in packet.events)
    assert any(rel.relation_type == RuntimeOCELRelationType.SESSION_HAS_TURN for rel in packet.relations)
    assert validate_runtime_ocel_trace_packet(packet, policy).validation_passed is True


def test_trace_packet_from_fake_safe_tool_output_records_request_result_refs_only():
    policy = default_runtime_ocel_trace_policy()
    proposal = build_agent_action_proposal(
        "proposal:tool",
        AgentActionProposalKind.READ_TEXT_FILE_SAFE,
        model_output_id="model_output:tool",
        proposed_tool_name="read_text_file_safe",
        proposed_tool_input={"path_ref": "safe.txt"},
    )
    decision = build_agent_action_decision(
        "decision:tool",
        proposal.proposal_id,
        AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION,
        reason="Safe workspace inspection only.",
        allowed_tool_name="read_text_file_safe",
        allowed_only_for_safe_workspace_inspection=True,
        execution_allowed=True,
    )
    safe_result = build_agent_safe_tool_execution_result(
        "safe_tool_result:1",
        "safe_tool_request:1",
        "read_text_file_safe",
        workspace_inspection_result_ref="workspace_result:1",
        result_summary="Safe bounded read summary only.",
        bounded_readonly=True,
    )
    record = build_agent_step_execution_record(
        "record:tool",
        "step_input:tool",
        AgentStepStatus.SAFE_TOOL_EXECUTED,
        proposal_id=proposal.proposal_id,
        decision_id=decision.decision_id,
        safe_tool_result_id=safe_result.safe_tool_result_id,
        executed_bounded_step=True,
    )
    step_output = build_agent_step_output(
        "step_output:tool",
        "step_input:tool",
        AgentStepStatus.SAFE_TOOL_EXECUTED,
        AgentStepResultKind.SAFE_TOOL_RESULT,
        record,
        action_proposal=proposal,
        action_decision=decision,
        safe_tool_result=safe_result,
        summary="Safe tool output artifact.",
    )
    packet = build_runtime_ocel_packet_from_agent_step_output(step_output, policy)

    assert any(obj.object_type == RuntimeOCELObjectType.SAFE_TOOL_REQUEST for obj in packet.objects)
    assert any(obj.object_type == RuntimeOCELObjectType.SAFE_TOOL_RESULT for obj in packet.objects)
    assert any(obj.object_type == RuntimeOCELObjectType.WORKSPACE_INSPECTION_RESULT for obj in packet.objects)
    assert any(event.event_kind == RuntimeOCELTraceEventKind.SAFE_TOOL_REQUEST_CREATED for event in packet.events)
    assert any(event.event_kind == RuntimeOCELTraceEventKind.SAFE_TOOL_RESULT_ATTACHED for event in packet.events)
    assert any(rel.relation_type == RuntimeOCELRelationType.SAFE_TOOL_REQUEST_FOR_PROPOSAL for rel in packet.relations)
    assert any(rel.relation_type == RuntimeOCELRelationType.SAFE_TOOL_RESULT_FOR_REQUEST for rel in packet.relations)
    assert "Safe bounded read summary only." not in str(packet)
    assert validate_runtime_ocel_trace_packet(packet, policy).validation_passed is True


def test_emit_trace_packet_returns_artifact_only_and_blocks_external_sink():
    step_output = _fake_final_step_output()
    emitter = build_runtime_ocel_trace_emitter()
    emission_input = build_runtime_ocel_trace_emission_input(
        "emission:step",
        agent_step_output_id=step_output.step_output_id,
    )
    packet = emit_runtime_ocel_trace_packet(emission_input, emitter, {"step_output": step_output})

    assert packet.status == RuntimeOCELTraceStatus.EMITTED_AS_PACKET
    assert runtime_ocel_packet_is_not_persistence(packet)

    blocked_input = build_runtime_ocel_trace_emission_input(
        "emission:external",
        requested_sink_kind=RuntimeOCELTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED,
    )
    blocked_packet = emit_runtime_ocel_trace_packet(blocked_input, emitter)
    assert blocked_packet.status == RuntimeOCELTraceStatus.BLOCKED
    assert blocked_packet.ready_for_persistent_write is False
    assert blocked_packet.ready_for_external_sink is False


def test_runtime_ocel_static_negative_patterns_and_no_provider_tool_workspace_execution():
    source = inspect.getsource(ocel_trace)
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
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)

    readiness_true_fragments = [
        "ready_for_execution=True",
        "ready_for_general_ocel_emission=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_external_trace_sink=True",
        "ready_for_provider_invocation=True",
        "ready_for_general_tool_execution=True",
        "ready_for_command_execution=True",
        "ready_for_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_ui_runtime=True",
    ]
    assert not any(fragment in source for fragment in readiness_true_fragments)

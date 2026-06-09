from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime.agentic_operation_cycle import build_agentic_operation_run_packet
from chanta_core.agent_runtime.patch_apply_candidate import build_apply_candidate_envelope
from chanta_core.agent_runtime.patch_apply_dry_run import build_dry_run_apply_simulation_result
from chanta_core.agent_runtime.patch_apply_engine import build_sandbox_patch_apply_result
from chanta_core.agent_runtime.patch_apply_trace import (
    AgenticTaskLifecycleTraceRecord,
    DigestionDominionApplyTraceRecord,
    PatchApplySandboxTracePacket,
    PatchApplyTraceAttributeKind,
    PatchApplyTraceDecisionKind,
    PatchApplyTraceEventKind,
    PatchApplyTraceFlagSet,
    PatchApplyTraceLifecyclePhase,
    PatchApplyTraceObjectType,
    PatchApplyTracePolicy,
    PatchApplyTraceReadinessLevel,
    PatchApplyTraceRelationType,
    PatchApplyTraceRiskKind,
    PatchApplyTraceSinkKind,
    PatchApplyTraceSourceKind,
    PatchApplyTraceStatus,
    SandboxApplyLifecycleTraceRecord,
    V0367ReadinessReport,
    agentic_task_lifecycle_record_is_not_runtime,
    build_agentic_task_lifecycle_record_from_run_packet,
    build_digestion_dominion_apply_trace_record,
    build_patch_apply_sandbox_trace_packet,
    build_patch_apply_trace_attribute,
    build_patch_apply_trace_emission_input,
    build_patch_apply_trace_emitter,
    build_patch_apply_trace_flags,
    build_patch_apply_trace_no_persistence_guarantee,
    build_patch_apply_trace_policy,
    build_patch_apply_trace_validation_finding,
    build_patch_apply_trace_validation_report,
    build_sandbox_apply_lifecycle_trace_record,
    build_trace_packet_from_agentic_operation_run_packet,
    build_trace_packet_from_apply_candidate,
    build_trace_packet_from_dry_run_result,
    build_trace_packet_from_post_apply_validation_report,
    build_trace_packet_from_sandbox_apply_result,
    build_v0367_readiness_report,
    decide_patch_apply_trace_emission,
    default_patch_apply_trace_policy,
    digestion_dominion_apply_trace_record_is_not_runtime,
    emit_patch_apply_trace_packet,
    patch_apply_trace_flags_preserve_no_persistence,
    patch_apply_trace_packet_is_not_persistence,
    patch_apply_trace_policy_blocks_persistence,
    sandbox_apply_lifecycle_record_is_not_live_apply,
    sanitize_patch_apply_trace_attribute_value,
    v0367_readiness_report_is_not_execution_ready,
    validate_patch_apply_sandbox_trace_packet,
)
from chanta_core.agent_runtime.patch_apply_validation import build_sandbox_post_apply_validation_report


def test_v0367_enum_values_are_complete():
    assert {item.value for item in PatchApplyTraceEventKind} == {
        "apply_candidate_created",
        "human_approval_contract_attached",
        "human_approval_contract_validated",
        "dry_run_simulation_started",
        "dry_run_simulation_completed",
        "dry_run_conflict_detected",
        "sandbox_workspace_policy_created",
        "sandbox_manifest_created",
        "sandbox_workspace_materialization_planned",
        "sandbox_workspace_materialized",
        "sandbox_file_write_recorded",
        "sandbox_patch_apply_started",
        "sandbox_patch_apply_completed",
        "sandbox_patch_apply_blocked",
        "post_apply_validation_started",
        "post_apply_validation_completed",
        "reconciliation_report_created",
        "safety_regression_scan_completed",
        "scope_validation_completed",
        "agentic_operation_cycle_started",
        "agentic_operation_step_recorded",
        "agentic_operation_cycle_completed",
        "agentic_operation_cycle_stopped",
        "human_handoff_required",
        "live_workspace_write_blocked",
        "external_agent_execution_blocked",
        "dominion_runtime_blocked",
        "infinite_agent_loop_blocked",
        "automatic_repair_loop_blocked",
        "trace_packet_created",
        "trace_emission_blocked",
        "no_op_event",
        "unknown",
    }
    assert "sandbox_patch_apply_result" in {item.value for item in PatchApplyTraceObjectType}
    assert "trace_packet_contains_relation" in {item.value for item in PatchApplyTraceRelationType}
    assert "ready_for_execution" in {item.value for item in PatchApplyTraceAttributeKind}
    assert "returned_trace_packet" in {item.value for item in PatchApplyTraceSinkKind}
    assert "emitted_as_packet" in {item.value for item in PatchApplyTraceStatus}
    assert "allow_trace_packet_creation" in {item.value for item in PatchApplyTraceDecisionKind}
    assert "persistent_trace_write_risk" in {item.value for item in PatchApplyTraceRiskKind}
    assert "v0366_agentic_operation_run_packet" in {item.value for item in PatchApplyTraceSourceKind}
    assert "trace_packet_ready" in {item.value for item in PatchApplyTraceReadinessLevel}
    assert "bounded_agentic_operation" in {item.value for item in PatchApplyTraceLifecyclePhase}


def _unsafe_trace_flag_fields(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_")
        and field.name
        not in {
            "ready_for_v0368_cli_sandbox_apply_agentic_surface",
            "ready_for_v0369_patch_apply_sandbox_consolidation",
            "ready_for_patch_apply_sandbox_trace_packet_creation",
            "ready_for_bounded_patch_apply_ocel_trace_emission",
            "ready_for_sandbox_apply_lifecycle_trace",
            "ready_for_agentic_operation_lifecycle_trace",
            "ready_for_digestion_dominion_trace_metadata",
            "ready_for_future_cli_trace_preview_input",
        }
    ]


def test_trace_flags_allow_trace_readiness_and_block_unsafe_readiness():
    flags = build_patch_apply_trace_flags()
    assert flags.patch_apply_trace_layer_constructed
    assert flags.ready_for_v0368_cli_sandbox_apply_agentic_surface
    assert flags.ready_for_v0369_patch_apply_sandbox_consolidation
    assert flags.ready_for_patch_apply_sandbox_trace_packet_creation
    assert flags.ready_for_bounded_patch_apply_ocel_trace_emission
    assert flags.ready_for_sandbox_apply_lifecycle_trace
    assert flags.ready_for_agentic_operation_lifecycle_trace
    assert flags.ready_for_digestion_dominion_trace_metadata
    assert flags.ready_for_future_cli_trace_preview_input
    assert patch_apply_trace_flags_preserve_no_persistence(flags)
    for name in _unsafe_trace_flag_fields(PatchApplyTraceFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "ready_for_ocel_file_write",
        "ready_for_jsonl_trace_write",
        "ready_for_sandbox_file_write",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
    ],
)
def test_trace_flags_reject_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_patch_apply_trace_flags(**{field_name: True})


def test_trace_policy_blocks_raw_payloads_persistence_and_runtime():
    policy = default_patch_apply_trace_policy()
    assert isinstance(policy, PatchApplyTracePolicy)
    assert PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET in policy.allowed_sink_kinds
    assert "secret" in policy.prohibited_payload_patterns
    assert "key" in policy.prohibited_payload_patterns
    assert "token" in policy.prohibited_payload_patterns
    assert "credential" in policy.prohibited_payload_patterns
    assert "pem" in policy.prohibited_payload_patterns
    assert "id_rsa" in policy.prohibited_payload_patterns
    assert patch_apply_trace_policy_blocks_persistence(policy)


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_raw_diff",
        "allow_raw_source",
        "allow_raw_sandbox_file_content",
        "allow_raw_validation_report",
        "allow_secret_content",
        "allow_credential_content",
        "allow_token_content",
        "allow_full_file_content",
        "allow_persistent_write",
        "allow_external_sink",
        "allow_ocel_file_write",
        "allow_jsonl_write",
        "allow_log_write",
        "allow_database_write",
        "allow_sandbox_file_write",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_test_execution",
        "allow_shell",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_trace_policy_rejects_unsafe_allow_true_values(field_name):
    with pytest.raises(ValueError):
        build_patch_apply_trace_policy(**{field_name: True})


def test_trace_artifacts_are_bounded_sanitized_metadata():
    attribute = build_patch_apply_trace_attribute(value="secret token key credential pem id_rsa " + "x" * 400)
    assert "[redacted]" in attribute.value
    assert "secret" not in attribute.value.lower()
    assert "token" not in attribute.value.lower()
    assert len(attribute.value) <= 240
    assert attribute.redacted
    assert attribute.truncated


def test_sandbox_apply_lifecycle_record_is_not_live_apply():
    record = build_sandbox_apply_lifecycle_trace_record(
        sandbox_apply_successful=True,
        post_apply_validation_successful=True,
    )
    assert isinstance(record, SandboxApplyLifecycleTraceRecord)
    assert sandbox_apply_lifecycle_record_is_not_live_apply(record)
    assert record.live_write_performed is False
    assert record.patch_application_performed is False
    assert record.production_certified is False
    with pytest.raises(ValueError):
        build_sandbox_apply_lifecycle_trace_record(live_write_performed=True)


def test_agentic_lifecycle_record_is_single_cycle_trace_not_runtime():
    record = build_agentic_task_lifecycle_record_from_run_packet(build_agentic_operation_run_packet())
    assert isinstance(record, AgenticTaskLifecycleTraceRecord)
    assert agentic_task_lifecycle_record_is_not_runtime(record)
    assert record.single_cycle_only
    assert record.human_handoff_required
    assert record.automatic_retry_allowed is False
    assert record.automatic_repair_allowed is False
    assert record.independent_agent_runtime is False
    assert record.multi_cycle_loop is False
    with pytest.raises(ValueError):
        AgenticTaskLifecycleTraceRecord(
            agentic_lifecycle_record_id="bad",
            version="v0.36.7",
            agentic_run_packet_id=None,
            operation_result_id=None,
            stop_reason_id=None,
            step_record_ids=[],
            lifecycle_summary="bad",
            single_cycle_only=True,
            human_handoff_required=True,
            automatic_retry_allowed=True,
        )


def test_digestion_dominion_record_blocks_runtime_patterns():
    record = build_digestion_dominion_apply_trace_record()
    assert isinstance(record, DigestionDominionApplyTraceRecord)
    assert digestion_dominion_apply_trace_record_is_not_runtime(record)
    assert record.digestion_first_policy_applied
    assert record.dominion_runtime_blocked
    assert record.external_agent_execution_blocked
    assert record.infinite_agent_loop_blocked
    assert record.automatic_repair_loop_blocked
    assert record.recursive_self_invocation_blocked


def test_trace_packet_is_returned_metadata_not_persistence():
    packet = build_patch_apply_sandbox_trace_packet()
    assert isinstance(packet, PatchApplySandboxTracePacket)
    assert patch_apply_trace_packet_is_not_persistence(packet)
    assert packet.ready_for_persistent_write is False
    assert packet.ready_for_external_sink is False
    assert packet.ready_for_ocel_file_write is False
    assert packet.ready_for_jsonl_write is False
    assert packet.ready_for_execution is False
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_trace_packet(ready_for_persistent_write=True)


def test_emission_decision_and_emitter_are_returned_or_in_memory_only():
    packet = build_patch_apply_sandbox_trace_packet()
    emission_input = build_patch_apply_trace_emission_input(trace_packet=packet)
    decision = decide_patch_apply_trace_emission(emission_input)
    assert decision.allow_trace_packet_creation
    assert decision.allow_persistent_write is False
    assert decision.allow_external_sink is False
    assert decision.allow_ocel_file_write is False
    assert decision.allow_jsonl_write is False
    report = emit_patch_apply_trace_packet(emission_input)
    assert report.emitted
    assert report.persisted is False
    assert report.wrote_ocel_file is False
    assert report.wrote_jsonl_file is False
    assert report.wrote_log_or_database is False
    with pytest.raises(ValueError):
        build_patch_apply_trace_emitter(allowed_sink_kinds=[PatchApplyTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED])


def test_validation_report_fails_with_blocked_items():
    report = build_patch_apply_trace_validation_report(
        findings=[build_patch_apply_trace_validation_finding(summary="blocked raw payload")]
    )
    assert report.blocked
    assert not report.validation_successful
    with pytest.raises(ValueError):
        build_patch_apply_trace_validation_report(
            findings=[build_patch_apply_trace_validation_finding()],
            validation_successful=True,
        )


def test_no_persistence_guarantee_all_no_fields_true():
    guarantee = build_patch_apply_trace_no_persistence_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True


def test_v0367_readiness_report_unsafe_flags_false():
    report = build_v0367_readiness_report()
    assert isinstance(report, V0367ReadinessReport)
    assert report.ready_for_v0368_cli_sandbox_apply_agentic_surface
    assert report.ready_for_v0369_patch_apply_sandbox_consolidation
    assert report.ready_for_patch_apply_sandbox_trace_packet_creation
    assert v0367_readiness_report_is_not_execution_ready(report)
    for name in _unsafe_trace_flag_fields(V0367ReadinessReport) + ["production_certified"]:
        assert getattr(report, name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "ready_for_ocel_file_write",
        "ready_for_jsonl_trace_write",
        "ready_for_log_write",
        "ready_for_database_write",
        "ready_for_sandbox_file_write",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
    ],
)
def test_v0367_readiness_report_rejects_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_v0367_readiness_report(**{field_name: True})


def test_fake_agentic_operation_run_packet_produces_trace_packet():
    run_packet = build_agentic_operation_run_packet()
    packet = build_trace_packet_from_agentic_operation_run_packet(run_packet)
    assert packet.agentic_task_lifecycle_record is not None
    assert packet.agentic_task_lifecycle_record.agentic_run_packet_id == run_packet.run_packet_id
    assert any(event.event_kind == PatchApplyTraceEventKind.AGENTIC_OPERATION_CYCLE_COMPLETED for event in packet.events)
    assert patch_apply_trace_packet_is_not_persistence(packet)


def test_fake_post_apply_validation_report_produces_trace_packet():
    report = build_sandbox_post_apply_validation_report()
    packet = build_trace_packet_from_post_apply_validation_report(report)
    assert packet.sandbox_lifecycle_record is not None
    assert packet.sandbox_lifecycle_record.post_apply_validation_report_id == report.validation_report_id
    assert any(event.event_kind == PatchApplyTraceEventKind.POST_APPLY_VALIDATION_COMPLETED for event in packet.events)
    assert patch_apply_trace_packet_is_not_persistence(packet)


def test_fake_sandbox_apply_result_produces_trace_packet():
    result = build_sandbox_patch_apply_result()
    packet = build_trace_packet_from_sandbox_apply_result(result)
    assert packet.sandbox_lifecycle_record is not None
    assert packet.sandbox_lifecycle_record.sandbox_apply_result_id == result.sandbox_apply_result_id
    assert any(obj.object_type == PatchApplyTraceObjectType.SANDBOX_FILE_WRITE_RECORD for obj in packet.objects)
    assert any(event.event_kind == PatchApplyTraceEventKind.SANDBOX_FILE_WRITE_RECORDED for event in packet.events)
    assert patch_apply_trace_packet_is_not_persistence(packet)


def test_fake_dry_run_result_and_apply_candidate_produce_trace_packets():
    dry_run_packet = build_trace_packet_from_dry_run_result(build_dry_run_apply_simulation_result())
    candidate_packet = build_trace_packet_from_apply_candidate(build_apply_candidate_envelope())
    assert any(obj.object_type == PatchApplyTraceObjectType.DRY_RUN_APPLY_SIMULATION_RESULT for obj in dry_run_packet.objects)
    assert any(obj.object_type == PatchApplyTraceObjectType.APPLY_CANDIDATE_ENVELOPE for obj in candidate_packet.objects)
    assert patch_apply_trace_packet_is_not_persistence(dry_run_packet)
    assert patch_apply_trace_packet_is_not_persistence(candidate_packet)


def test_validate_trace_packet_blocks_raw_secret_attribute():
    unsafe_attribute = build_patch_apply_trace_attribute(value="safe")
    object.__setattr__(unsafe_attribute, "value", "raw secret token")
    packet = build_patch_apply_sandbox_trace_packet(attributes=[unsafe_attribute])
    report = validate_patch_apply_sandbox_trace_packet(packet)
    assert report.blocked
    assert not report.validation_successful


def test_helpers_do_not_contain_file_io_or_execution_patterns():
    import chanta_core.agent_runtime.patch_apply_trace as module

    source = inspect.getsource(module)
    forbidden = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        "open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "while ",
    ]
    for pattern in forbidden:
        assert pattern not in source
    assert "apply_patch(" not in source
    assert "git apply" not in source
    assert "write_text(" not in source
    assert "write_bytes(" not in source

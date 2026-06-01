from __future__ import annotations

from pathlib import Path

from chanta_core.memory_candidate_continuity import (
    MemoryLifecycleFindingService,
    MemoryLifecycleReportService,
)


def test_source_data_deletion_request_is_blocked_and_does_not_delete_source() -> None:
    parts = MemoryLifecycleReportService().build_all_parts(
        requested_operation="forget",
        source_data_deletion_requested=True,
    )
    report = parts["report"]
    forget_decision = parts["forget_decisions"][0]
    forget_record = parts["forget_records"][0]
    tombstone = parts["forget_tombstones"][0]
    finding_types = {finding.finding_type for finding in parts["findings"]}
    forget_gate = next(gate for gate in parts["operation_gates"] if gate.gate_id.endswith(":forget"))

    assert forget_gate.gate_status == "blocked"
    assert forget_gate.source_data_deletion_requested is True
    assert forget_gate.source_data_deletion_allowed_now is False
    assert forget_decision.decision_type == "block_forget"
    assert forget_decision.deletes_source_data_now is False
    assert forget_record.source_deleted is False
    assert forget_record.recallable_content_removed is False
    assert tombstone.contains_recallable_memory_content is False
    assert tombstone.contains_raw_source_content is False
    assert tombstone.contains_secret is False
    assert report.report_status == "blocked"
    assert report.ready_for_v0_27_9 is False
    assert report.source_data_deleted is False
    assert "source_data_deletion_attempted" in finding_types


def test_missing_registry_is_warning_only_and_does_not_mutate_or_restore_raw_content() -> None:
    parts = MemoryLifecycleReportService().build_all_parts(registry_available=False)
    report = parts["report"]
    source_view = parts["source_view"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert source_view.source_status == "partial"
    assert source_view.durable_registry_report_ref is None
    assert source_view.raw_transcript_included is False
    assert source_view.raw_provider_output_included is False
    assert source_view.raw_secret_included is False
    assert source_view.credential_included is False
    assert report.report_status == "warning"
    assert report.source_data_deleted is False
    assert report.raw_transcript_restored is False
    assert report.raw_provider_output_restored is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False
    assert report.continuity_injected is False
    assert "missing_durable_memory_registry_report" in finding_types


def test_blocked_finding_types_cover_lifecycle_non_goals() -> None:
    blocked = MemoryLifecycleFindingService.BLOCKED_FINDINGS

    assert "silent_overwrite_attempted" in blocked
    assert "unlogged_deletion_attempted" in blocked
    assert "source_data_deletion_attempted" in blocked
    assert "raw_transcript_restoration_attempted" in blocked
    assert "raw_provider_output_restoration_attempted" in blocked
    assert "persona_mutation_attempted" in blocked
    assert "behavior_policy_mutation_attempted" in blocked
    assert "pig_guidance_as_authority_detected" in blocked
    assert "provider_invocation_attempted" in blocked
    assert "command_execution_attempted" in blocked
    assert "safety_bypass_attempted" in blocked
    assert "continuity_injection_attempted" in blocked
    assert "external_adapter_detected" in blocked
    assert "schumpeter_split_detected" in blocked
    assert "raw_secret_output_detected" in blocked
    assert "credential_exposure_detected" in blocked
    assert "llm_judge_detected" in blocked


def test_changed_code_does_not_contain_forbidden_true_markers_or_runtime_execution() -> None:
    files = [
        Path("src/chanta_core/memory_candidate_continuity.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    forbidden_true_markers = [
        "silent_memory_overwrite" + "=True",
        "unlogged_memory_deletion" + "=True",
        "source_data_deleted" + "=True",
        "raw_transcript_restored" + "=True",
        "raw_provider_output_restored" + "=True",
        "persona_mutated" + "=True",
        "behavior_policy_auto_mutated" + "=True",
        "behavior_policy_mutated" + "=True",
        "pig_guidance_used_as_authority" + "=True",
        "pig_policy_mutated" + "=True",
        "pig_executed" + "=True",
        "provider_invoked" + "=True",
        "command_executed" + "=True",
        "safety_gate_bypassed" + "=True",
        "continuity_injected" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "raw_secret_output" + "=True",
        "credential_exposed" + "=True",
    ]
    forbidden_runtime_markers = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "open" + "ai",
        "anth" + "ropic",
        "com" + "pletion",
        "chat" + "." + "com" + "pletions",
        "exec" + "(",
        "eval" + "(",
    ]

    for marker in forbidden_true_markers + forbidden_runtime_markers:
        assert marker not in text

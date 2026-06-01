from __future__ import annotations

from pathlib import Path

from chanta_core.memory_candidate_continuity import (
    DurableMemoryRegistryFindingService,
    DurableMemoryRegistryReportService,
)


def test_missing_promotion_gate_blocks_durable_record_creation() -> None:
    parts = DurableMemoryRegistryReportService().build_all_parts(promotion_gate_available=False)
    gate = parts["write_gate"]
    decision = parts["write_decision"]
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert gate.promotion_decision_present is False
    assert gate.promotion_decision_is_promote is False
    assert gate.may_create_durable_record is False
    assert gate.may_write_persistent_memory is False
    assert gate.gate_status == "blocked"
    assert decision.decision_type == "block_write"
    assert decision.creates_durable_record is False
    assert decision.updates_registry is False
    assert decision.writes_persistent_memory is False
    assert report.durable_record_count == 0
    assert report.registry_entry_count == 0
    assert report.blocked_write_count == 1
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.durable_registry_updated is False
    assert "missing_promotion_gate_report" in finding_types
    assert "missing_promotion_decision_record" in finding_types


def test_persistent_write_requires_release_and_runtime_hygiene() -> None:
    release_missing = DurableMemoryRegistryReportService().build_all_parts(
        release_hygiene_gate_passed=False,
        runtime_data_hygiene_gate_passed=True,
    )
    runtime_missing = DurableMemoryRegistryReportService().build_all_parts(
        release_hygiene_gate_passed=True,
        runtime_data_hygiene_gate_passed=False,
    )
    both_passed = DurableMemoryRegistryReportService().build_all_parts(
        release_hygiene_gate_passed=True,
        runtime_data_hygiene_gate_passed=True,
    )

    assert release_missing["write_gate"].may_create_durable_record is True
    assert release_missing["write_gate"].may_write_persistent_memory is False
    assert release_missing["write_decision"].writes_persistent_memory is False
    assert release_missing["report"].persistent_memory_written is False
    assert runtime_missing["write_gate"].may_create_durable_record is True
    assert runtime_missing["write_gate"].may_write_persistent_memory is False
    assert runtime_missing["write_decision"].writes_persistent_memory is False
    assert runtime_missing["report"].persistent_memory_written is False
    assert both_passed["write_gate"].may_create_durable_record is True
    assert both_passed["write_gate"].may_write_persistent_memory is True
    assert both_passed["write_decision"].writes_persistent_memory is True


def test_dry_run_and_blocked_records_never_write_memory() -> None:
    dry_run = DurableMemoryRegistryReportService().build_all_parts()
    blocked = DurableMemoryRegistryReportService().build_all_parts(promotion_gate_available=False)

    assert dry_run["dry_run_records"][0].actual_durable_record_created is False
    assert dry_run["dry_run_records"][0].actual_persistent_memory_written is False
    assert dry_run["report"].durable_memory_records_created is False
    assert blocked["blocked_records"][0].durable_record_created is False
    assert blocked["blocked_records"][0].persistent_memory_written is False
    assert blocked["blocked_records"][0].registry_updated is False
    assert blocked["report"].durable_memory_records_created is False
    assert blocked["report"].registry_entries_created is False


def test_blocked_finding_types_cover_write_without_gate_and_non_goals() -> None:
    blocked = DurableMemoryRegistryFindingService.BLOCKED_FINDINGS

    assert "durable_write_without_promotion_decision_detected" in blocked
    assert "durable_write_without_evidence_detected" in blocked
    assert "durable_write_without_source_refs_detected" in blocked
    assert "durable_write_without_scope_detected" in blocked
    assert "durable_write_without_forget_revoke_path_detected" in blocked
    assert "durable_write_without_audit_detected" in blocked
    assert "persistent_write_without_release_hygiene_detected" in blocked
    assert "raw_transcript_memory_attempted" in blocked
    assert "raw_provider_output_memory_attempted" in blocked
    assert "raw_secret_memory_attempted" in blocked
    assert "credential_memory_attempted" in blocked
    assert "persona_mutation_attempted" in blocked
    assert "behavior_policy_mutation_attempted" in blocked
    assert "pig_guidance_as_memory_authority_detected" in blocked
    assert "pig_policy_mutation_detected" in blocked
    assert "pig_execution_detected" in blocked
    assert "provider_invocation_attempted" in blocked
    assert "command_execution_attempted" in blocked
    assert "safety_bypass_attempted" in blocked
    assert "session_continuity_injection_attempted" in blocked
    assert "external_adapter_detected" in blocked
    assert "schumpeter_split_detected" in blocked
    assert "llm_judge_detected" in blocked


def test_changed_code_does_not_contain_forbidden_true_markers_or_runtime_execution() -> None:
    files = [
        Path("src/chanta_core/memory_candidate_continuity.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    forbidden_true_markers = [
        "durable_memory_record_created_without_gate" + "=True",
        "durable_memory_registry_updated_without_gate" + "=True",
        "persistent_memory_written_without_release_hygiene" + "=True",
        "persistent_memory_written_without_runtime_data_hygiene" + "=True",
        "memory_written_without_promotion_decision" + "=True",
        "memory_written_without_evidence" + "=True",
        "memory_written_without_source_refs" + "=True",
        "memory_written_without_scope" + "=True",
        "memory_written_without_forget_revoke_path" + "=True",
        "memory_written_without_audit" + "=True",
        "session_continuity_context_created" + "=True",
        "continuity_injection_bundle_created" + "=True",
        "persona_mutated" + "=True",
        "behavior_policy_auto_mutated" + "=True",
        "behavior_policy_mutated" + "=True",
        "raw_transcript_persisted_as_memory" + "=True",
        "raw_provider_output_persisted_as_memory" + "=True",
        "raw_transcript_memory_created" + "=True",
        "raw_provider_output_memory_created" + "=True",
        "raw_secret_memory_created" + "=True",
        "credential_memory_created" + "=True",
        "pig_memory_promoted" + "=True",
        "pig_policy_mutated" + "=True",
        "pig_executed" + "=True",
        "provider_invoked" + "=True",
        "command_executed" + "=True",
        "safety_gate_bypassed" + "=True",
        "safety_gate_bypassed_by_memory" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
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

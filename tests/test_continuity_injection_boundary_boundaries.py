from __future__ import annotations

from pathlib import Path

from chanta_core.memory_candidate_continuity import (
    ContinuityInjectionBoundaryFindingService,
    ContinuityInjectionBoundaryReportService,
)


def test_missing_context_pack_creates_warning_without_runtime_injection() -> None:
    parts = ContinuityInjectionBoundaryReportService().build_all_parts(continuity_context_available=False)
    report = parts["report"]
    decision = parts["injection_decisions"][0]
    trace = parts["boundary_traces"][0]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert parts["source_view"].context_pack_ref is None
    assert parts["injection_bundles"] == []
    assert parts["injection_previews"] == []
    assert decision.decision_type == "reject_injection"
    assert decision.applies_runtime_injection_now is False
    assert decision.mutates_runtime_now is False
    assert trace.boundary_bypassed is False
    assert trace.runtime_mutation_performed is False
    assert report.report_status == "warning"
    assert report.ready_for_v0_27_8 is True
    assert report.runtime_injection_performed is False
    assert report.default_agent_context_mutated is False
    assert report.memory_updated is False
    assert "missing_context_pack" in finding_types


def test_requested_defer_and_reject_decisions_are_records_only() -> None:
    defer_parts = ContinuityInjectionBoundaryReportService().build_all_parts(
        requested_decision_type="defer_conflict_review"
    )
    reject_parts = ContinuityInjectionBoundaryReportService().build_all_parts(
        requested_decision_type="reject_injection"
    )

    for parts in [defer_parts, reject_parts]:
        decision = parts["injection_decisions"][0]
        record = parts["decision_records"][0]
        assert decision.decision_type in {"defer_conflict_review", "reject_injection"}
        assert decision.applies_runtime_injection_now is False
        assert decision.mutates_runtime_now is False
        assert record.runtime_injection_performed is False
        assert parts["report"].runtime_injection_performed is False


def test_blocked_finding_types_cover_injection_non_goals() -> None:
    blocked = ContinuityInjectionBoundaryFindingService.BLOCKED_FINDINGS

    assert "runtime_injection_attempted" in blocked
    assert "default_agent_context_mutation_attempted" in blocked
    assert "decision_service_mutation_attempted" in blocked
    assert "skill_router_mutation_attempted" in blocked
    assert "safety_gate_mutation_attempted" in blocked
    assert "permission_policy_mutation_attempted" in blocked
    assert "memory_update_attempted" in blocked
    assert "memory_revoke_attempted" in blocked
    assert "memory_forget_attempted" in blocked
    assert "persona_mutation_attempted" in blocked
    assert "behavior_policy_mutation_attempted" in blocked
    assert "raw_transcript_replay_attempted" in blocked
    assert "raw_provider_output_replay_attempted" in blocked
    assert "pig_guidance_as_authority_detected" in blocked
    assert "provider_invocation_attempted" in blocked
    assert "command_execution_attempted" in blocked
    assert "file_mutation_attempted" in blocked
    assert "safety_bypass_attempted" in blocked
    assert "permission_bypass_attempted" in blocked
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
        "continuity_injected" + "=True",
        "runtime_injection_performed" + "=True",
        "default_agent_context_mutated" + "=True",
        "decision_service_mutated" + "=True",
        "skill_router_mutated" + "=True",
        "safety_gate_mutated" + "=True",
        "permission_policy_mutated" + "=True",
        "memory_updated" + "=True",
        "memory_revoked" + "=True",
        "memory_forgotten" + "=True",
        "persona_mutated" + "=True",
        "behavior_policy_auto_mutated" + "=True",
        "behavior_policy_mutated" + "=True",
        "raw_transcript_replayed" + "=True",
        "raw_provider_output_replayed" + "=True",
        "pig_guidance_used_as_authority" + "=True",
        "pig_policy_mutated" + "=True",
        "pig_executed" + "=True",
        "provider_invoked" + "=True",
        "command_executed" + "=True",
        "file_mutated" + "=True",
        "safety_gate_bypassed" + "=True",
        "permission_boundary_bypassed" + "=True",
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

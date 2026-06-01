from __future__ import annotations

from pathlib import Path

from chanta_core.memory_candidate_continuity import (
    SessionContinuityContextBuildReportService,
    SessionContinuityContextFindingService,
)


def test_no_active_memory_builds_warning_only_context_without_injection() -> None:
    parts = SessionContinuityContextBuildReportService().build_all_parts(active_registry_available=False)
    source_view = parts["source_view"]
    pack = parts["context_pack"]
    decision = parts["build_decisions"][0]
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert source_view.active_memory_count == 0
    assert pack.item_count == 1
    assert decision.decision_type == "build_context_pack"
    assert decision.injects_context_now is False
    assert report.report_status == "passed"
    assert report.ready_for_v0_27_7 is True
    assert report.continuity_injected is False
    assert report.default_agent_context_mutated is False
    assert report.memory_updated is False
    assert "missing_active_memory_records" in finding_types


def test_blocked_status_memory_is_never_active_context() -> None:
    parts = SessionContinuityContextBuildReportService().build_all_parts()

    for memory_ref in parts["memory_refs"]:
        if memory_ref.memory_status in {"revoked", "forgotten", "expired", "blocked"}:
            assert memory_ref.use_role != "active_context"
            assert memory_ref.eligible_for_context_pack is False
            assert memory_ref.eligible_for_injection_now is False
    assert all(item.item_role != "primary_context" for item in parts["context_items"] if "archived" in item.memory_record_ref["id"])


def test_blocked_finding_types_cover_session_continuity_non_goals() -> None:
    blocked = SessionContinuityContextFindingService.BLOCKED_FINDINGS

    assert "revoked_memory_active_use_attempted" in blocked
    assert "forgotten_memory_active_use_attempted" in blocked
    assert "expired_memory_active_use_attempted" in blocked
    assert "blocked_memory_active_use_attempted" in blocked
    assert "raw_transcript_replay_attempted" in blocked
    assert "raw_provider_output_replay_attempted" in blocked
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
    assert "pig_guidance_as_authority_detected" in blocked
    assert "provider_invocation_attempted" in blocked
    assert "command_execution_attempted" in blocked
    assert "safety_bypass_attempted" in blocked
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
        "default_agent_context_mutated" + "=True",
        "decision_service_mutated" + "=True",
        "skill_router_mutated" + "=True",
        "safety_gate_mutated" + "=True",
        "permission_policy_mutated" + "=True",
        "memory_updated" + "=True",
        "memory_revoked" + "=True",
        "memory_forgotten" + "=True",
        "persistent_memory_written" + "=True",
        "durable_memory_record_created" + "=True",
        "durable_memory_registry_updated" + "=True",
        "persona_mutated" + "=True",
        "behavior_policy_auto_mutated" + "=True",
        "behavior_policy_mutated" + "=True",
        "raw_transcript_replayed" + "=True",
        "raw_provider_output_replayed" + "=True",
        "raw_transcript_persisted_as_memory" + "=True",
        "raw_provider_output_persisted_as_memory" + "=True",
        "pig_guidance_used_as_authority" + "=True",
        "pig_policy_mutated" + "=True",
        "pig_executed" + "=True",
        "provider_invoked" + "=True",
        "command_executed" + "=True",
        "safety_gate_bypassed" + "=True",
        "safety_gate_bypassed_by_memory" + "=True",
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

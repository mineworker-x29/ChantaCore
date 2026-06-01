from __future__ import annotations

from pathlib import Path

from chanta_core.memory_candidate_continuity import MemoryConsolidationFindingService, MemoryConsolidationReportService


def test_blocked_consolidation_findings_block_readiness() -> None:
    service = MemoryConsolidationReportService()
    for finding_type in MemoryConsolidationFindingService.BLOCKED_FINDINGS:
        report = service.build_report(extra_findings=[finding_type])
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.readiness_status == "blocked"
        assert report.release_status == "blocked"
        assert report.ready_for_v0_28 is False
        assert finding_type in finding_types


def test_consolidation_report_forbidden_flags_remain_false() -> None:
    report = MemoryConsolidationReportService().build_report()

    assert report.runtime_injection_performed is False
    assert report.default_agent_context_mutated is False
    assert report.decision_service_mutated is False
    assert report.skill_router_mutated is False
    assert report.safety_gate_mutated is False
    assert report.permission_policy_mutated is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.file_mutated is False
    assert report.safety_gate_bypassed is False
    assert report.permission_boundary_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_transcript_replayed is False
    assert report.raw_provider_output_replayed is False
    assert report.raw_secret_output is False
    assert report.credential_exposed is False
    assert report.pig_guidance_used_as_authority is False
    assert report.llm_judge_used is False
    assert report.public_alpha_ready is False
    assert report.ready_for_v0_29 is False


def test_v0279_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "memory_candidate_continuity.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_memory_candidate_continuity_consolidation.py",
        root / "tests" / "test_memory_candidate_continuity_consolidation_boundaries.py",
        root / "docs" / "versions" / "v0.27" / "v0.27.9_memory_candidate_continuity_consolidation.md",
    ]
    forbidden_names = [
        "memory_candidate_created",
        "memory_candidate_scored",
        "memory_promoted",
        "persistent_memory_written",
        "durable_memory_record_created",
        "durable_memory_registry_updated",
        "memory_updated",
        "memory_revoked",
        "memory_forgotten",
        "continuity_injected",
        "runtime_injection_performed",
        "default_agent_context_mutated",
        "decision_service_mutated",
        "skill_router_mutated",
        "safety_gate_mutated",
        "permission_policy_mutated",
        "persona_mutated",
        "behavior_policy_auto_mutated",
        "behavior_policy_mutated",
        "provider_invoked",
        "command_executed",
        "file_mutated",
        "safety_gate_bypassed",
        "permission_boundary_bypassed",
        "raw_transcript_replayed",
        "raw_provider_output_replayed",
        "raw_transcript_persisted_as_memory",
        "raw_provider_output_persisted_as_memory",
        "raw_secret_memory_created",
        "credential_memory_created",
        "pig_guidance_used_as_authority",
        "pig_policy_mutated",
        "pig_executed",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "schumpeter_split_introduced",
    ]
    forbidden_runtime_markers = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "open" + "ai",
        "anth" + "ropic",
        "comple" + "tion",
        "chat" + ".comple" + "tions",
        "exec" + "(",
        "eval" + "(",
    ]

    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text

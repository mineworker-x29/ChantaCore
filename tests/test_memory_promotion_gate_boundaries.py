from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MemoryPromotionGateFindingService,
    MemoryPromotionGateReportService,
)


def test_missing_scoring_report_warns_without_durable_or_persistent_write() -> None:
    report = MemoryPromotionGateReportService().build_all_parts(scoring_available=False)["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert report.ready_for_v0_27_5 is False
    assert "missing_evidence_scoring_report" in finding_types
    assert "missing_candidate_scores" in finding_types
    assert "missing_evidence_bundle" in finding_types
    assert report.candidate_views_created is False
    assert report.promotion_decisions_recorded is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.durable_registry_updated is False
    assert report.session_continuity_injected is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False


def test_forbidden_attempt_findings_block_promotion_gate() -> None:
    service = MemoryPromotionGateReportService()
    for finding_type in MemoryPromotionGateFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_27_5 is False
        assert finding_type in finding_types
        assert report.memory_promoted is False
        assert report.persistent_memory_written is False
        assert report.durable_memory_written is False
        assert report.durable_registry_updated is False
        assert report.session_continuity_injected is False


def test_memory_promotion_cli_commands_are_gate_decision_only(capsys) -> None:
    commands = [
        ["memory", "promotion", "gate"],
        ["memory", "promotion", "source-view"],
        ["memory", "promotion", "rules"],
        ["memory", "promotion", "candidates"],
        ["memory", "promotion", "requirements"],
        ["memory", "promotion", "evidence-review"],
        ["memory", "promotion", "score-review"],
        ["memory", "promotion", "privacy"],
        ["memory", "promotion", "contradictions"],
        ["memory", "promotion", "user-control"],
        ["memory", "promotion", "scope"],
        ["memory", "promotion", "expiry"],
        ["memory", "promotion", "lifecycle"],
        ["memory", "promotion", "forget-revoke"],
        ["memory", "promotion", "decide", "--decision", "promote"],
        ["memory", "promotion", "readiness"],
        ["memory", "promotion", "audit"],
        ["memory", "promotion", "report"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.27.4" in output
        assert "promotion_gate_created=true" in output
        assert "candidate_views_created=true" in output
        assert "requirements_created=true" in output
        assert "gate_reviews_created=true" in output
        assert "scopes_created=true" in output
        assert "expiries_created=true" in output
        assert "forget_revoke_paths_created=true" in output
        assert "promotion_decisions_recorded=true" in output
        assert "durable_readiness_previews_created=true" in output
        assert "audit_trail_created=true" in output
        assert "ready_for_v0_27_5=true" in output
        assert "ready_for_v0_28=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "durable_memory_written=false" in output
        assert "durable_registry_updated=false" in output
        assert "session_continuity_injected=false" in output
        assert "persona_mutated=false" in output
        assert "behavior_policy_mutated=false" in output
        assert "raw_transcript_memory_created=false" in output
        assert "raw_provider_output_memory_created=false" in output
        assert "pig_memory_promoted=false" in output
        assert "pig_policy_mutated=false" in output
        assert "pig_executed=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "safety_gate_bypassed=false" in output
        assert "external_provider_adapter_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "raw_secret_output=false" in output
        assert "credential_exposed=false" in output
        assert "llm_judge_used=false" in output
        assert "next_required_step=v0.27.5 Durable Memory Record & Registry" in output


def test_v0274_changed_files_do_not_contain_forbidden_true_or_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "memory_candidate_continuity.py",
        root / "tests" / "test_memory_promotion_gate.py",
        root / "tests" / "test_memory_promotion_gate_boundaries.py",
        root / "docs" / "versions" / "v0.27" / "v0.27.4_memory_promotion_gate.md",
    ]
    forbidden_names = [
        "memory_promoted",
        "persistent_memory_written",
        "durable_memory_written",
        "durable_memory_record_created",
        "durable_memory_registry_updated",
        "session_continuity_context_created",
        "continuity_injection_bundle_created",
        "persona_mutated",
        "behavior_policy_auto_mutated",
        "behavior_policy_mutated",
        "raw_transcript_persisted_as_memory",
        "raw_provider_output_persisted_as_memory",
        "raw_transcript_memory_created",
        "raw_provider_output_memory_created",
        "pig_memory_promoted",
        "pig_policy_mutated",
        "pig_executed",
        "provider_invoked",
        "command_executed",
        "safety_gate_bypassed",
        "safety_gate_bypassed_by_memory",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "schumpeter_split_introduced",
        "raw_secret_output",
        "credential_exposed",
    ]
    forbidden_runtime_markers = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "open" + "ai",
        "anth" + "ropic",
        "chat" + "." + "com" + "pletions",
        "exec" + "(",
        "eval" + "(",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text

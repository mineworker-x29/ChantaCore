from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MemoryEvidenceScoringFindingService,
    MemoryEvidenceScoringReportService,
)


def test_missing_candidate_extraction_warns_without_promotion_or_writes() -> None:
    report = MemoryEvidenceScoringReportService().build_all_parts(extraction_available=False)["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert report.ready_for_v0_27_4 is False
    assert "missing_candidate_extraction_report" in finding_types
    assert "missing_candidate_batch" in finding_types
    assert "missing_candidates" in finding_types
    assert report.evidence_bundles_created is False
    assert report.candidate_scores_created is False
    assert report.memory_scored is False
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


def test_forbidden_attempt_findings_block_evidence_scoring() -> None:
    service = MemoryEvidenceScoringReportService()
    for finding_type in MemoryEvidenceScoringFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_27_4 is False
        assert finding_type in finding_types
        assert report.memory_promoted is False
        assert report.persistent_memory_written is False
        assert report.durable_memory_written is False
        assert report.durable_registry_updated is False
        assert report.session_continuity_injected is False


def test_memory_scoring_cli_commands_are_scoring_only(capsys) -> None:
    commands = [
        ["memory", "scoring", "bind-evidence"],
        ["memory", "scoring", "source-view"],
        ["memory", "scoring", "rules"],
        ["memory", "scoring", "bundles"],
        ["memory", "scoring", "evidence-items"],
        ["memory", "scoring", "support"],
        ["memory", "scoring", "assessments"],
        ["memory", "scoring", "privacy"],
        ["memory", "scoring", "contradictions"],
        ["memory", "scoring", "pig-signals"],
        ["memory", "scoring", "dimensions"],
        ["memory", "scoring", "scores"],
        ["memory", "scoring", "decisions"],
        ["memory", "scoring", "readiness"],
        ["memory", "scoring", "audit"],
        ["memory", "scoring", "report"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.27.3" in output
        assert "evidence_bundles_created=true" in output
        assert "candidate_scores_created=true" in output
        assert "scoring_batch_created=true" in output
        assert "promotion_readiness_previews_created=true" in output
        assert "memory_scored=true" in output
        assert "ready_for_v0_27_4=true" in output
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
        assert "next_required_step=v0.27.4 Memory Promotion Gate" in output


def test_v0273_changed_files_do_not_contain_forbidden_true_or_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "memory_candidate_continuity.py",
        root / "tests" / "test_memory_evidence_binder_scoring.py",
        root / "tests" / "test_memory_evidence_binder_scoring_boundaries.py",
        root / "docs" / "versions" / "v0.27" / "v0.27.3_memory_evidence_binder_scoring.md",
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

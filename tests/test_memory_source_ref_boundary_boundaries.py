from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import (
    MemoryForbiddenSourceReportService,
    MemorySourceBoundaryFindingService,
    MemorySourceBoundaryReportService,
    MemorySourceEligibilityDecisionService,
    MemorySourceEligibilityEvaluationService,
    MemorySourceEligibilityRuleService,
    MemorySourceRefService,
)


def test_missing_contract_or_handoff_warns_without_memory_creation() -> None:
    report = MemorySourceBoundaryReportService().build_all_parts(contract_available=False, handoff_available=False)["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert report.ready_for_v0_27_2 is True
    assert "missing_memory_contract" in finding_types
    assert "missing_v0269_handoff" in finding_types
    assert "release_hygiene_unknown" in finding_types
    assert report.memory_candidate_extracted is False
    assert report.memory_scored is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.durable_memory_written is False
    assert report.session_continuity_injected is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.provider_invoked is False
    assert report.command_executed is False


def test_raw_sources_are_blocked_by_evaluation_and_forbidden_report() -> None:
    source = MemorySourceRefService().build_source_refs()[0]
    source.source_category = "raw_transcript"
    source.raw_content_included = True
    source.raw_transcript_included = True
    rules = MemorySourceEligibilityRuleService().build_rules()
    evaluation = MemorySourceEligibilityEvaluationService().evaluate_sources([source], rules)[0]
    decision = MemorySourceEligibilityDecisionService().decide_eligibility([evaluation])[0]
    forbidden = MemoryForbiddenSourceReportService().build_report([source])

    assert evaluation.evaluation_status == "blocked"
    assert "memory_source_eligibility_rule:raw_transcript_forbidden" in evaluation.failed_rule_ids
    assert "memory_source_eligibility_rule:raw_content_source_blocked" in evaluation.blocking_rule_ids
    assert evaluation.memory_candidate_created is False
    assert decision.decision_type == "blocked_for_raw_content"
    assert decision.candidate_extraction_performed_now is False
    assert decision.memory_created_now is False
    assert forbidden.report_status == "blocked"
    assert forbidden.blocked_count == 1
    assert forbidden.raw_transcript_detected is True


def test_forbidden_attempt_findings_block_source_boundary() -> None:
    service = MemorySourceBoundaryReportService()
    for finding_type in MemorySourceBoundaryFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_27_2 is False
        assert finding_type in finding_types


def test_memory_source_cli_commands_are_boundary_only(capsys) -> None:
    commands = [
        ["memory", "sources", "boundary"],
        ["memory", "sources", "catalog"],
        ["memory", "sources", "refs"],
        ["memory", "sources", "bundle"],
        ["memory", "sources", "registry-view"],
        ["memory", "sources", "eligibility-rules"],
        ["memory", "sources", "evaluate"],
        ["memory", "sources", "decisions"],
        ["memory", "sources", "redaction"],
        ["memory", "sources", "quality"],
        ["memory", "sources", "forbidden"],
        ["memory", "sources", "readiness"],
        ["memory", "sources", "report"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.27.1" in output
        assert "source_boundary_created=true" in output
        assert "source_refs_created=true" in output
        assert "source_bundle_created=true" in output
        assert "eligibility_evaluations_created=true" in output
        assert "eligibility_decisions_created=true" in output
        assert "redaction_report_created=true" in output
        assert "source_quality_report_created=true" in output
        assert "forbidden_source_report_created=true" in output
        assert "candidate_readiness_boundary_created=true" in output
        assert "ready_for_v0_27_2=true" in output
        assert "ready_for_v0_28=false" in output
        assert "memory_candidate_extracted=false" in output
        assert "memory_scored=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "durable_memory_written=false" in output
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


def test_v0271_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "memory_candidate_continuity.py",
        root / "tests" / "test_memory_source_ref_boundary.py",
        root / "tests" / "test_memory_source_ref_boundary_boundaries.py",
        root / "docs" / "versions" / "v0.27" / "v0.27.1_memory_source_ref_boundary.md",
    ]
    forbidden_names = [
        "memory_candidate_created",
        "memory_candidate_extracted",
        "memory_candidate_scored",
        "memory_scored",
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
        "exec" + "(",
        "eval" + "(",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text

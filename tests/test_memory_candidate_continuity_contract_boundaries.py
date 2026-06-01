from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.memory_candidate_continuity import MemoryContractFindingService, MemoryContractReportService


def test_missing_handoff_warns_but_contract_remains_non_mutating() -> None:
    report = MemoryContractReportService().build_all_parts(v0269_handoff_available=False)["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert report.ready_for_v0_27_1 is True
    assert "missing_v0269_handoff" in finding_types
    assert "v02610_hardening_not_verified" in finding_types
    assert report.memory_candidate_extracted is False
    assert report.memory_scored is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.behavior_policy_mutated is False
    assert report.raw_transcript_memory_created is False
    assert report.raw_provider_output_memory_created is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.safety_gate_bypassed is False


def test_forbidden_attempt_findings_block_contract() -> None:
    service = MemoryContractReportService()
    for finding_type in MemoryContractFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_27_1 is False
        assert finding_type in finding_types


def test_memory_contract_cli_commands_are_contract_only(capsys) -> None:
    commands = [
        ["memory", "contract"],
        ["memory", "roadmap"],
        ["memory", "source-policy"],
        ["memory", "candidate-policy"],
        ["memory", "candidate-types"],
        ["memory", "evidence-policy"],
        ["memory", "scoring-policy"],
        ["memory", "promotion-policy"],
        ["memory", "durable-policy"],
        ["memory", "continuity-policy"],
        ["memory", "injection-policy"],
        ["memory", "audit-policy"],
        ["memory", "privacy-policy"],
        ["memory", "pig-policy"],
        ["memory", "safety-boundary"],
        ["memory", "contract-report"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.27.0" in output
        assert "layer=memory_candidate_continuity" in output
        assert "status=contract_only" in output
        assert "ready_for_v0_27_1=true" in output
        assert "ready_for_v0_28=false" in output
        assert "memory_candidate_extracted=false" in output
        assert "memory_scored=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
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


def test_v0270_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "memory_candidate_continuity.py",
        root / "tests" / "test_memory_candidate_continuity_contract.py",
        root / "tests" / "test_memory_candidate_continuity_contract_boundaries.py",
        root / "docs" / "versions" / "v0.27" / "v0.27.0_memory_candidate_continuity_contract.md",
    ]
    forbidden_names = [
        "memory_candidate_created",
        "memory_candidate_extracted",
        "memory_candidate_scored",
        "memory_scored",
        "memory_promoted",
        "persistent_memory_written",
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

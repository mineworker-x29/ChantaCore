from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import V028ContractFindingService, V028ContractReportService


def test_blocked_v028_findings_block_contract_report() -> None:
    service = V028ContractReportService()
    for finding_type in V028ContractFindingService.BLOCKED_FINDINGS:
        report = service.build_report(extra_findings=[finding_type])
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_28_1 is False
        assert report.ready_for_v0_29 is False
        assert finding_type in finding_types


def test_v028_forbidden_action_flags_remain_false() -> None:
    report = V028ContractReportService().build_report()

    assert report.public_alpha_implemented is False
    assert report.public_alpha_ready is False
    assert report.schumpeter_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.external_adapter_implemented is False
    assert report.external_dominion_bridge_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.autonomous_memory_execution_enabled is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.references_schumpeter_runtime_dependency_added is False
    assert report.references_schumpeter_code_copied is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False


def test_v028_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_public_alpha_schumpeter_preparation_contract.py",
        root / "tests" / "test_public_alpha_schumpeter_preparation_contract_boundaries.py",
        root
        / "docs"
        / "versions"
        / "v0.28"
        / "v0.28.0_public_alpha_schumpeter_split_preparation_contract.md",
    ]
    forbidden_names = [
        "public_alpha_implemented",
        "package_published",
        "release_tag_created",
        "schumpeter_split_implemented",
        "company_wrapper_implemented",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "external_dominion_bridge_implemented",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "references_schumpeter_runtime_dependency_added",
        "references_schumpeter_code_copied",
        "company_private_material_exposed",
        "credential_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
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

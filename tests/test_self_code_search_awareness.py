from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfCodeSearchAwarenessSkillService,
    SelfWorkspacePathPolicyService,
    SelfWorkspaceSearchRequest,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture()
def workspace_root(tmp_path: Path) -> Path:
    (tmp_path / "notes.txt").write_text("alpha\nNeedle appears here\nomega\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("def run():\n    return 'needle'\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\nChantaCore search awareness\n", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> SelfCodeSearchAwarenessSkillService:
    return SelfCodeSearchAwarenessSkillService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_literal_search_finds_expected_line(workspace_root: Path) -> None:
    result = _service(workspace_root).search_workspace(SelfWorkspaceSearchRequest(query="Needle"))
    assert not result.blocked
    assert result.matches
    first = result.matches[0]
    assert first.relative_path == "notes.txt"
    assert first.line_number == 2
    assert first.snippet.line == "Needle appears here"
    assert first.column_start > 0


def test_case_modes_and_context_lines(workspace_root: Path) -> None:
    service = _service(workspace_root)
    insensitive = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", context_lines=1))
    assert any(match.relative_path == "notes.txt" for match in insensitive.matches)
    assert insensitive.matches[0].snippet.before
    sensitive_miss = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", case_sensitive=True))
    assert all(match.relative_path != "notes.txt" for match in sensitive_miss.matches)
    sensitive_hit = service.search_workspace(SelfWorkspaceSearchRequest(query="Needle", case_sensitive=True))
    assert any(match.relative_path == "notes.txt" for match in sensitive_hit.matches)


def test_globs_no_match_and_budget_limits(workspace_root: Path) -> None:
    service = _service(workspace_root)
    py_only = service.search_workspace(
        SelfWorkspaceSearchRequest(query="def", include_globs=["*.py", "src/*.py"])
    )
    assert py_only.matches[0].relative_path == "src/app.py"
    none = service.search_workspace(SelfWorkspaceSearchRequest(query="NO_SUCH_MATCH_EXPECTED_12345"))
    assert none.matches == []
    assert none.files_scanned >= 1

    for index in range(4):
        (workspace_root / f"many_{index}.txt").write_text("needle\n", encoding="utf-8")
    file_limited = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", max_files=1))
    assert file_limited.files_scanned == 1
    assert file_limited.truncated
    assert file_limited.truncated_reason in {"max_files", "candidate_inventory_limit"}

    match_limited = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", max_matches=1))
    assert len(match_limited.matches) == 1
    assert match_limited.truncated
    assert match_limited.truncated_reason == "max_matches"


def test_per_file_and_total_byte_budgets(workspace_root: Path) -> None:
    (workspace_root / "late.txt").write_text(("x" * 120) + "needle\n", encoding="utf-8")
    service = _service(workspace_root)
    per_file_limited = service.search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path="late.txt", max_bytes_per_file=20)
    )
    assert per_file_limited.matches == []
    assert per_file_limited.truncated
    assert per_file_limited.truncated_reason == "max_bytes_per_file"

    total_limited = service.search_workspace(SelfWorkspaceSearchRequest(query="alpha", max_total_bytes=20))
    assert total_limited.truncated
    assert total_limited.truncated_reason in {"max_bytes_per_file", "max_total_bytes"}


def test_match_limit_per_file(workspace_root: Path) -> None:
    (workspace_root / "repeat.txt").write_text("needle\nneedle\nneedle\n", encoding="utf-8")
    result = _service(workspace_root).search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path="repeat.txt", max_matches_per_file=2)
    )
    assert len(result.matches) == 2
    assert result.truncated
    assert result.truncated_reason == "max_matches_per_file"


def test_secret_context_is_redacted(workspace_root: Path) -> None:
    (workspace_root / "secrets_nearby.txt").write_text(
        "alpha\npassword = hunter2\nneedle\n",
        encoding="utf-8",
    )
    result = _service(workspace_root).search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path="secrets_nearby.txt", context_lines=1)
    )
    assert result.matches
    match = result.matches[0]
    assert match.snippet.redacted
    payload = str(result.to_dict())
    assert "hunter2" not in payload
    assert "[REDACTED]" in payload
    assert match.redaction_findings


def test_workspace_search_contract_and_later_skills() -> None:
    registry = SelfAwarenessRegistryService()
    contract = registry.get_contract("skill:self_awareness_workspace_search")
    assert contract is not None
    assert contract.implementation_status == "implemented"
    assert contract.effect_type == READ_ONLY_OBSERVATION_EFFECT
    assert contract.execution_enabled is False
    assert contract.canonical_mutation_enabled is False
    assert contract.risk_profile.mutates_workspace is False
    assert contract.risk_profile.mutates_memory is False
    assert contract.risk_profile.mutates_persona is False
    assert contract.risk_profile.uses_shell is False
    assert contract.risk_profile.uses_network is False
    assert contract.risk_profile.uses_mcp is False
    assert contract.risk_profile.loads_plugin is False
    assert contract.risk_profile.executes_external_harness is False
    assert contract.risk_profile.dangerous_capability is False

    for skill_id in [
        "skill:self_awareness_config_surface",
        "skill:self_awareness_test_surface",
        "skill:self_awareness_capability_registry",
        "skill:self_awareness_runtime_boundary",
    ]:
        later = registry.get_contract(skill_id)
        assert later is not None
        assert later.implementation_status == "contract_only"
        assert later.gate_contract.allow_skill_execution is False


def test_gate_invokes_workspace_search_read_only(workspace_root: Path) -> None:
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_workspace_search",
        input_payload={"root_path": str(workspace_root), "query": "needle", "relative_path": "."},
        invocation_mode="test_self_code_search_awareness",
    )
    output = invocation.last_result.output_payload["output_attrs"]
    assert result.executed is True
    assert output["effect_type"] == READ_ONLY_OBSERVATION_EFFECT
    assert output["matches"]
    assert output["result_attrs"]["workspace_write_used"] is False
    assert output["result_attrs"]["shell_execution_used"] is False


def test_cli_search_and_no_match_output(capsys) -> None:
    exit_code = main(["self-awareness", "search", "OCEL", "--path", "README.md", "--max-files", "50", "--max-matches", "20"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Self-Code Search Awareness" in output
    assert "effect=read_only_observation" in output
    assert "match_count=" in output
    assert "README.md" in output

    no_match_code = main(["self-awareness", "search", "NO_SUCH_MATCH_EXPECTED_12345", "--max-files", "20"])
    no_match_output = capsys.readouterr().out
    assert no_match_code == 0
    assert "matches=none" in no_match_output


def test_pig_and_ocpx_report_search_coverage() -> None:
    report_service = SelfAwarenessReportService()
    pig = report_service.build_pig_report()
    ocpx = report_service.build_ocpx_projection()
    assert pig["version"] == "0.20.9"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workspace_awareness_coverage"]["workspace_search"] == "implemented_bounded_literal"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert ocpx["workspace_awareness_state"]["workspace_search"] == "implemented_bounded_literal"
    assert "self_workspace_search_completed" in ocpx["event_coverage"]

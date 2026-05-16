from __future__ import annotations

import inspect
import tempfile
from pathlib import Path

import pytest

from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfWorkspaceAwarenessSkillService,
    SelfWorkspaceInventoryService,
    SelfWorkspacePathPolicyService,
    WorkspaceInventoryRequest,
)
from chanta_core.self_awareness.workspace_awareness import DEFAULT_EXCLUDED_NAMES
from chanta_core.cli.main import main
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture
def workspace_root() -> Path:
    with tempfile.TemporaryDirectory() as directory:
        yield Path(directory)


def test_workspace_roots_list_returns_primary_root(workspace_root: Path) -> None:
    service = SelfWorkspacePathPolicyService(workspace_root=workspace_root)

    roots = service.list_workspace_roots()

    assert len(roots) == 1
    assert roots[0].is_primary is True
    assert roots[0].root_id == "workspace_root:primary"
    assert roots[0].root_attrs["metadata_only"] is True


def test_verify_path_dot_is_allowed(workspace_root: Path) -> None:
    service = SelfWorkspaceAwarenessSkillService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    resolution = service.verify_path(".")

    assert resolution.within_workspace is True
    assert resolution.blocked is False
    assert resolution.finding_type == "allowed"


def test_inventory_returns_metadata_only_entries(workspace_root: Path) -> None:
    (workspace_root / "alpha.txt").write_text("secret body should not appear", encoding="utf-8")
    (workspace_root / "docs").mkdir()
    (workspace_root / "docs" / "readme.md").write_text("# title", encoding="utf-8")
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    report = service.build_inventory(WorkspaceInventoryRequest(max_depth=2))

    paths = {entry.relative_path for entry in report.entries}
    assert "alpha.txt" in paths
    assert "docs" in paths
    assert "docs/readme.md" in paths
    assert report.report_attrs["metadata_only"] is True
    assert report.report_attrs["file_content_read"] is False
    assert all("body" not in entry.to_dict() for entry in report.entries)
    assert all("content" not in entry.to_dict() for entry in report.entries)


def test_inventory_respects_max_depth(workspace_root: Path) -> None:
    nested = workspace_root / "a" / "b"
    nested.mkdir(parents=True)
    (nested / "c.txt").write_text("x", encoding="utf-8")
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    report = service.build_inventory(WorkspaceInventoryRequest(max_depth=1))

    paths = {entry.relative_path for entry in report.entries}
    assert "a" in paths
    assert "a/b" not in paths


def test_inventory_respects_max_entries_and_sets_truncated(workspace_root: Path) -> None:
    for index in range(5):
        (workspace_root / f"file_{index}.txt").write_text(str(index), encoding="utf-8")
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    report = service.build_inventory(WorkspaceInventoryRequest(max_depth=1, max_entries=2))

    assert report.total_entries_returned == 2
    assert report.truncated is True


def test_inventory_excludes_hidden_and_noisy_paths_by_default(workspace_root: Path) -> None:
    (workspace_root / ".hidden").write_text("hidden", encoding="utf-8")
    for name in sorted(DEFAULT_EXCLUDED_NAMES):
        path = workspace_root / name
        path.mkdir() if "." not in Path(name).suffix else path.write_text("ignored", encoding="utf-8")
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    report = service.build_inventory(WorkspaceInventoryRequest(max_depth=1))

    paths = {entry.relative_path for entry in report.entries}
    assert ".hidden" not in paths
    assert DEFAULT_EXCLUDED_NAMES.isdisjoint(paths)
    assert report.excluded_count >= 1


def test_inventory_service_does_not_use_content_reading_or_process_execution() -> None:
    source = inspect.getsource(SelfWorkspaceInventoryService)

    forbidden = [
        "read_text",
        "read_bytes",
        "open(",
        ".read(",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
    ]
    assert all(token not in source for token in forbidden)


def test_implemented_contracts_have_read_only_observation_effect() -> None:
    registry = SelfAwarenessRegistryService()

    for skill_id in [
        "skill:self_awareness_workspace_inventory",
        "skill:self_awareness_path_verify",
    ]:
        contract = registry.get_contract(skill_id)
        assert contract is not None
        assert contract.implementation_status == "implemented"
        assert contract.effect_type == READ_ONLY_OBSERVATION_EFFECT
        assert contract.execution_enabled is False
        assert contract.canonical_mutation_enabled is False
        assert contract.risk_profile.mutates_workspace is False
        assert contract.risk_profile.uses_shell is False
        assert contract.risk_profile.uses_network is False
        assert contract.risk_profile.uses_mcp is False
        assert contract.risk_profile.loads_plugin is False
        assert contract.risk_profile.executes_external_harness is False


def test_other_self_awareness_contracts_remain_non_executable() -> None:
    registry = SelfAwarenessRegistryService()
    implemented = {
        "skill:self_awareness_workspace_inventory",
        "skill:self_awareness_path_verify",
        "skill:self_awareness_text_read",
        "skill:self_awareness_workspace_search",
        "skill:self_awareness_markdown_structure",
        "skill:self_awareness_python_symbols",
        "skill:self_awareness_project_structure",
        "skill:self_awareness_surface_verify",
        "skill:self_awareness_plan_candidate",
        "skill:self_awareness_todo_candidate",
    }

    for contract in registry.list_contracts():
        if contract.skill_id not in implemented:
            assert contract.implementation_status == "contract_only"
            assert contract.execution_enabled is False


def test_gate_invokes_workspace_inventory_read_only(workspace_root: Path) -> None:
    (workspace_root / "visible.txt").write_text("x", encoding="utf-8")
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)

    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_workspace_inventory",
        input_payload={"root_path": str(workspace_root), "relative_path": ".", "max_depth": 1, "max_entries": 10},
    )

    assert result.executed is True
    assert result.blocked is False
    assert invocation.last_result is not None
    assert invocation.last_result.output_payload["output_attrs"]["effect_type"] == READ_ONLY_OBSERVATION_EFFECT


def test_gate_invokes_path_verify_read_only(workspace_root: Path) -> None:
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)

    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_path_verify",
        input_payload={"root_path": str(workspace_root), "input_path": "."},
    )

    assert result.executed is True
    assert result.blocked is False
    assert invocation.last_result is not None
    assert invocation.last_result.output_payload["output_attrs"]["effect_type"] == READ_ONLY_OBSERVATION_EFFECT


def test_pig_and_ocpx_include_v0201_workspace_coverage() -> None:
    service = SelfAwarenessReportService()

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["workspace_awareness_coverage"]["path_verification"] == "implemented"
    assert pig["workspace_awareness_coverage"]["workspace_inventory"] == "implemented"
    assert pig["workspace_awareness_coverage"]["text_read"] == "implemented_limited_preview"
    assert ocpx["workspace_awareness_state"]["path_verification"] == "implemented"
    assert ocpx["effect_type"] == READ_ONLY_OBSERVATION_EFFECT


def test_cli_workspace_verify_and_inventory_work(capsys) -> None:
    verify_code = main(["self-awareness", "workspace", "verify-path", "."])
    verify_output = capsys.readouterr()
    inventory_code = main(
        [
            "self-awareness",
            "workspace",
            "inventory",
            ".",
            "--max-depth",
            "1",
            "--max-entries",
            "20",
        ]
    )
    inventory_output = capsys.readouterr()

    assert verify_code == 0
    assert "effect=read_only_observation" in verify_output.out
    assert "blocked=false" in verify_output.out
    assert inventory_code == 0
    assert "effect=read_only_observation" in inventory_output.out
    assert "truncated=" in inventory_output.out
    assert "total_entries_returned=" in inventory_output.out

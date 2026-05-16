from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfProjectStructureAwarenessService,
    SelfProjectStructureRequest,
    SelfWorkspacePathPolicyService,
)


@pytest.fixture()
def workspace_root(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# Public\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('not executed')\n", encoding="utf-8")
    (tmp_path / "private").mkdir()
    (tmp_path / "private" / "note.md").write_text("# Private\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=value\n", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> SelfProjectStructureAwarenessService:
    return SelfProjectStructureAwarenessService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def _inspect(root: Path, path: str) -> object:
    return _service(root).inspect_project_structure(SelfProjectStructureRequest(relative_path=path))


@pytest.mark.parametrize("path", ["../", "..\\", "../../"])
def test_traversal_paths_block(workspace_root: Path, path: str) -> None:
    candidate = _inspect(workspace_root, path)
    assert candidate.policy_decision is not None
    assert candidate.policy_decision.blocked is True
    assert candidate.policy_decision.finding_type == "path_traversal"
    assert candidate.tree_nodes == []


def test_outside_workspace_absolute_path_blocks(workspace_root: Path, tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside"
    candidate = _inspect(workspace_root, str(outside))
    assert candidate.policy_decision is not None
    assert candidate.policy_decision.blocked is True
    assert candidate.policy_decision.finding_type == "absolute_path_not_allowed"


def test_private_boundary_blocks(workspace_root: Path) -> None:
    candidate = _inspect(workspace_root, "private")
    assert candidate.policy_decision is not None
    assert candidate.policy_decision.blocked is True
    assert candidate.policy_decision.finding_type == "private_boundary"


def test_missing_and_file_targets_block(workspace_root: Path) -> None:
    missing = _inspect(workspace_root, "missing")
    file_target = _inspect(workspace_root, "README.md")
    assert missing.policy_decision is not None
    assert missing.policy_decision.finding_type == "not_found"
    assert file_target.policy_decision is not None
    assert file_target.policy_decision.finding_type == "not_directory"


def test_secret_file_is_not_exposed_by_project_structure(workspace_root: Path) -> None:
    candidate = _inspect(workspace_root, ".")
    rendered = str(candidate.to_dict())
    assert "SECRET=value" not in rendered
    assert ".env" not in {node.relative_path for node in candidate.tree_nodes}


def test_no_non_goal_surface_outputs(workspace_root: Path) -> None:
    candidate = _inspect(workspace_root, ".")
    assert candidate.candidate_attrs["llm_architecture_inference_used"] is False
    assert candidate.candidate_attrs["dependency_graph_created"] is False
    assert candidate.candidate_attrs["import_resolution_used"] is False
    assert candidate.candidate_attrs["runtime_introspection_used"] is False
    rendered = str(candidate.to_dict()).casefold()
    assert "call_graph" not in rendered
    assert "architecture summary" not in rendered


def test_cli_blocked_file_output_has_no_content(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["self-awareness", "project", "structure", "--path", "README.md"]) == 1
    output = capsys.readouterr().out
    assert "Self-Project Structure Awareness" in output
    assert "finding_type=not_directory" in output
    assert "content_printed=false" in output

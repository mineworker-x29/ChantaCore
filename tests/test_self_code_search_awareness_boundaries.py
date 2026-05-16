from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfCodeSearchAwarenessSkillService,
    SelfWorkspacePathPolicyService,
    SelfWorkspaceSearchRequest,
)


@pytest.fixture()
def workspace_root(tmp_path: Path) -> Path:
    (tmp_path / "safe.txt").write_text("needle\n", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> SelfCodeSearchAwarenessSkillService:
    return SelfCodeSearchAwarenessSkillService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_policy_blocks_empty_query_and_unsupported_mode(workspace_root: Path) -> None:
    service = _service(workspace_root)
    empty = service.search_workspace(SelfWorkspaceSearchRequest(query=""))
    assert empty.blocked
    assert empty.policy_decision.finding_type == "empty_query"
    unsupported = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", match_mode="pattern"))
    assert unsupported.blocked
    assert unsupported.policy_decision.finding_type == "unsupported_match_mode"


def test_path_boundary_blocks(workspace_root: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_text("needle\n", encoding="utf-8")
    service = _service(workspace_root)
    for value in ["../", "..\\", "../../"]:
        result = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", relative_path=value))
        assert result.blocked
        assert result.policy_decision.finding_type in {"path_traversal", "outside_workspace"}
    absolute = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", relative_path=str(outside)))
    assert absolute.blocked
    assert absolute.policy_decision.finding_type == "outside_workspace"


def test_private_boundary_blocks(workspace_root: Path) -> None:
    private_dir = workspace_root / "private"
    private_dir.mkdir()
    (private_dir / "note.txt").write_text("needle\n", encoding="utf-8")
    result = _service(workspace_root).search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path="private")
    )
    assert result.blocked
    assert result.policy_decision.finding_type == "private_boundary"
    assert result.matches == []


def test_binary_and_secret_candidates_are_blocked(workspace_root: Path) -> None:
    (workspace_root / "blob.bin").write_bytes(b"\x00\x01needle")
    (workspace_root / ".env").write_text("SECRET=needle\n", encoding="utf-8")
    service = _service(workspace_root)
    binary = service.search_workspace(SelfWorkspaceSearchRequest(query="needle", relative_path="blob.bin"))
    assert binary.files_blocked == 1
    assert binary.matches == []
    assert binary.skipped_candidates[0].candidate_status == "blocked"
    secret = service.search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path=".env", include_hidden=True)
    )
    assert secret.files_blocked == 1
    assert secret.matches == []
    assert secret.skipped_candidates[0].finding_type == "secret_file_blocked"


def test_private_path_literal_is_redacted(workspace_root: Path) -> None:
    private_path = (
        "D:\\Chanta"
        + "ResearchGroup\\"
        + "Chanta"
        + "ResearchGroup"
        + "_Members\\Ve"
        + "ra\\letter.txt"
    )
    (workspace_root / "public_note.txt").write_text(
        f"needle\npath={private_path}\n",
        encoding="utf-8",
    )
    result = _service(workspace_root).search_workspace(
        SelfWorkspaceSearchRequest(query="needle", relative_path="public_note.txt", context_lines=1)
    )
    payload = str(result.to_dict())
    assert "letter.txt" not in payload
    assert "[REDACTED]" in payload
    assert result.matches[0].snippet.redacted


def test_cli_blocked_file_does_not_show_content(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("SECRET=needle\n", encoding="utf-8")
    exit_code = main(["self-awareness", "search", "needle", "--path", ".env"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "files_blocked=1" in output
    assert "match_count=0" in output
    assert "SECRET=needle" not in output


def test_search_result_attrs_show_no_external_or_mutating_effects(workspace_root: Path) -> None:
    result = _service(workspace_root).search_workspace(SelfWorkspaceSearchRequest(query="needle"))
    attrs = result.result_attrs
    assert attrs["bounded_search"] is True
    assert attrs["literal_match_only"] is True
    assert attrs["workspace_write_used"] is False
    assert attrs["shell_execution_used"] is False
    assert attrs["network_access_used"] is False
    assert attrs["mcp_connection_used"] is False
    assert attrs["plugin_loading_used"] is False
    assert attrs["external_harness_execution_used"] is False
    assert attrs["memory_mutation_used"] is False
    assert attrs["persona_mutation_used"] is False
    assert attrs["overlay_mutation_used"] is False
    assert attrs["summary_used"] is False
    assert attrs["symbol_parse_used"] is False

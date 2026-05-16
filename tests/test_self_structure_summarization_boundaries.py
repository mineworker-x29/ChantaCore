from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfStructureSummaryRequest,
    SelfStructureSummaryService,
    SelfWorkspacePathPolicyService,
)


@pytest.fixture()
def workspace_root(tmp_path: Path) -> Path:
    (tmp_path / "safe.md").write_text("# Safe\n", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> SelfStructureSummaryService:
    return SelfStructureSummaryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_path_boundary_blocks(workspace_root: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    service = _service(workspace_root)
    for value in ["../", "..\\", "../../"]:
        candidate = service.summarize(SelfStructureSummaryRequest(path=value, summary_mode="markdown"))
        assert candidate.policy_decision is not None
        assert candidate.policy_decision.blocked
        assert candidate.policy_decision.finding_type in {"path_traversal", "outside_workspace"}
    absolute = service.summarize(SelfStructureSummaryRequest(path=str(outside), summary_mode="markdown"))
    assert absolute.policy_decision is not None
    assert absolute.policy_decision.blocked
    assert absolute.policy_decision.finding_type == "outside_workspace"


def test_private_directory_directory_missing_binary_and_secret_files_block(workspace_root: Path) -> None:
    (workspace_root / "private").mkdir()
    (workspace_root / "private" / "note.md").write_text("# Private\n", encoding="utf-8")
    (workspace_root / "dir").mkdir()
    (workspace_root / "blob.bin").write_bytes(b"\x00\x01")
    (workspace_root / ".env").write_text("SECRET=value\n", encoding="utf-8")
    (workspace_root / "id_rsa").write_text("PRIVATE KEY\n", encoding="utf-8")
    service = _service(workspace_root)
    cases = {
        "private/note.md": "private_boundary",
        "dir": "not_file",
        "missing.md": "not_found",
        "blob.bin": "binary_file_blocked",
        ".env": "secret_file_blocked",
        "id_rsa": "secret_file_blocked",
    }
    for path, finding in cases.items():
        candidate = service.summarize(SelfStructureSummaryRequest(path=path, summary_mode="auto"))
        assert candidate.policy_decision is not None
        assert candidate.policy_decision.blocked
        assert candidate.policy_decision.finding_type == finding
        assert not candidate.markdown
        assert not candidate.python


def test_secret_like_values_are_not_exposed_in_markdown_or_plain_text(workspace_root: Path) -> None:
    private_path = (
        "D:\\Chanta"
        + "ResearchGroup\\"
        + "Chanta"
        + "ResearchGroup"
        + "_Members\\Ve"
        + "ra\\secret.txt"
    )
    (workspace_root / "note.md").write_text(
        "---\ntoken: SECRET_VALUE\n---\n# Title\npassword=rawsecret\n",
        encoding="utf-8",
    )
    (workspace_root / "note.txt").write_text(f"alpha\npath={private_path}\n", encoding="utf-8")
    service = _service(workspace_root)
    markdown = service.summarize(SelfStructureSummaryRequest(path="note.md", summary_mode="markdown"))
    plain = service.summarize(SelfStructureSummaryRequest(path="note.txt", summary_mode="plain_text"))
    assert "SECRET_VALUE" not in str(markdown.to_dict())
    assert "rawsecret" not in str(markdown.to_dict())
    assert "secret.txt" not in str(plain.to_dict())
    assert plain.redaction_findings


def test_unsupported_kind_blocks_unless_plain_text_or_auto(workspace_root: Path) -> None:
    (workspace_root / "unknown.xyz").write_text("alpha\n", encoding="utf-8")
    service = _service(workspace_root)
    forced = service.summarize(SelfStructureSummaryRequest(path="unknown.xyz", summary_mode="markdown"))
    assert forced.policy_decision is not None
    assert forced.policy_decision.blocked
    assert forced.policy_decision.finding_type == "unsupported_extension"
    auto = service.summarize(SelfStructureSummaryRequest(path="safe.md", summary_mode="plain_text"))
    assert auto.plain_text is not None


def test_cli_blocked_summary_does_not_show_content(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("SECRET=raw\n", encoding="utf-8")
    exit_code = main(["self-awareness", "summarize", "auto", ".env"])
    output = capsys.readouterr().out
    assert exit_code == 1
    assert "content_printed=false" in output
    assert "SECRET=raw" not in output


def test_candidate_attrs_show_no_external_or_mutating_effects(workspace_root: Path) -> None:
    candidate = _service(workspace_root).summarize(SelfStructureSummaryRequest(path="safe.md"))
    attrs = candidate.candidate_attrs
    assert attrs["deterministic_structure_extraction"] is True
    assert attrs["model_summary_used"] is False
    assert attrs["canonical_promotion_enabled"] is False
    assert attrs["promoted"] is False
    assert attrs["workspace_write_used"] is False
    assert attrs["shell_execution_used"] is False
    assert attrs["network_access_used"] is False
    assert attrs["mcp_connection_used"] is False
    assert attrs["plugin_loading_used"] is False
    assert attrs["external_harness_execution_used"] is False
    assert attrs["memory_mutation_used"] is False
    assert attrs["persona_mutation_used"] is False
    assert attrs["overlay_mutation_used"] is False

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfCodeTextPerceptionSkillService,
    SelfTextReadRequest,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture
def workspace_root() -> Path:
    with tempfile.TemporaryDirectory() as directory:
        yield Path(directory)


def _service(root: Path, **policy_kwargs) -> SelfCodeTextPerceptionSkillService:
    return SelfCodeTextPerceptionSkillService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root, **policy_kwargs)
    )


def test_traversal_and_outside_workspace_paths_block(workspace_root: Path) -> None:
    service = _service(workspace_root)

    traversal = service.read_text(SelfTextReadRequest(path="../secret.txt"))
    outside = service.read_text(SelfTextReadRequest(path=str(workspace_root.parent / "outside.txt")))

    assert traversal.blocked is True
    assert traversal.policy_decision.finding_type == "path_traversal"
    assert outside.blocked is True
    assert outside.policy_decision.finding_type == "outside_workspace"


def test_private_boundary_path_blocks(workspace_root: Path) -> None:
    private_dir = workspace_root / "private_zone"
    private_dir.mkdir()
    (private_dir / "note.txt").write_text("hidden", encoding="utf-8")
    service = _service(workspace_root, private_boundary_names={"private_zone"})

    result = service.read_text(SelfTextReadRequest(path="private_zone/note.txt"))

    assert result.blocked is True
    assert result.policy_decision.finding_type == "private_boundary"
    assert result.slice is None


def test_directory_and_missing_file_block(workspace_root: Path) -> None:
    (workspace_root / "docs").mkdir()
    service = _service(workspace_root)

    directory = service.read_text(SelfTextReadRequest(path="docs"))
    missing = service.read_text(SelfTextReadRequest(path="missing.txt"))

    assert directory.blocked is True
    assert directory.policy_decision.finding_type == "not_file"
    assert missing.blocked is True
    assert missing.policy_decision.finding_type == "not_found"


def test_binary_file_blocks(workspace_root: Path) -> None:
    (workspace_root / "binary.txt").write_bytes(b"\x00\x01\x02\x03")
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="binary.txt"))

    assert result.blocked is True
    assert result.policy_decision.finding_type == "binary_file_blocked"
    assert result.slice is None


def test_secret_files_block_by_default(workspace_root: Path) -> None:
    (workspace_root / ".env").write_text("TOKEN=secret", encoding="utf-8")
    (workspace_root / ".env.local").write_text("TOKEN=secret", encoding="utf-8")
    (workspace_root / "id_rsa").write_text("PRIVATE KEY", encoding="utf-8")
    (workspace_root / "server.pem").write_text("PRIVATE KEY", encoding="utf-8")
    service = _service(workspace_root)

    for path in [".env", ".env.local", "id_rsa", "server.pem"]:
        result = service.read_text(SelfTextReadRequest(path=path))
        assert result.blocked is True
        assert result.policy_decision.finding_type == "secret_file_blocked"
        assert result.slice is None


def test_unsupported_extension_blocks(workspace_root: Path) -> None:
    (workspace_root / "image.bin").write_text("text but unsupported", encoding="utf-8")
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="image.bin"))

    assert result.blocked is True
    assert result.policy_decision.finding_type == "unsupported_extension"


def test_symlink_path_blocks_by_default(workspace_root: Path) -> None:
    target = workspace_root / "target.txt"
    target.write_text("target", encoding="utf-8")
    link = workspace_root / "link.txt"
    try:
        link.symlink_to(target)
    except OSError:
        return
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="link.txt"))

    assert result.blocked is True
    assert result.policy_decision.finding_type == "symlink_escape"


def test_private_path_literal_is_redacted(workspace_root: Path) -> None:
    private_path = (
        "D:"
        + "\\"
        + "ChantaResearchGroup"
        + "\\"
        + "ChantaResearchGroup"
        + "_Members"
        + r"\Sample\secret.txt"
    )
    (workspace_root / "paths.txt").write_text(private_path, encoding="utf-8")
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="paths.txt"))

    assert result.slice is not None
    assert private_path not in result.slice.content
    assert "[REDACTED]" in result.slice.content
    assert any(finding.finding_type == "private_path" for finding in result.redaction_findings)


def test_cli_blocked_result_does_not_show_content(capsys) -> None:
    exit_code = main(["self-awareness", "text", "read", ".env"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "finding_type=secret_file_blocked" in captured.out
    assert "content_printed=false" in captured.out


def test_gate_blocks_traversal_before_text_read_invocation(workspace_root: Path) -> None:
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)

    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_text_read",
        input_payload={"root_path": str(workspace_root), "path": "../secret.txt"},
    )

    assert result.executed is False
    assert result.blocked is True
    assert gate.last_decision is not None
    assert gate.last_decision.decision_basis == "path_traversal"
    assert invocation.last_result is None

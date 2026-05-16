from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
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


def _service(root: Path) -> SelfCodeTextPerceptionSkillService:
    return SelfCodeTextPerceptionSkillService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_text_read_allowed_for_small_text_markdown_and_python(workspace_root: Path) -> None:
    for name, content in {
        "note.txt": "alpha\nbeta\n",
        "README.md": "# Title\nbody\n",
        "module.py": "print('hello')\n",
    }.items():
        (workspace_root / name).write_text(content, encoding="utf-8")

    service = _service(workspace_root)

    for name in ["note.txt", "README.md", "module.py"]:
        result = service.read_text(SelfTextReadRequest(path=name))
        assert result.blocked is False
        assert result.slice is not None
        assert result.slice.relative_path == name
        assert result.slice.content


def test_preview_respects_max_bytes_and_max_lines(workspace_root: Path) -> None:
    (workspace_root / "long.txt").write_text("one\ntwo\nthree\nfour\n", encoding="utf-8")
    service = _service(workspace_root)

    by_bytes = service.read_text(SelfTextReadRequest(path="long.txt", max_bytes=5, max_lines=100))
    by_lines = service.read_text(SelfTextReadRequest(path="long.txt", max_bytes=100, max_lines=2))

    assert by_bytes.slice is not None
    assert by_bytes.slice.bytes_read <= 5
    assert by_bytes.slice.truncated is True
    assert by_lines.slice is not None
    assert by_lines.slice.lines_read == 2
    assert by_lines.slice.truncated is True


def test_line_range_reads_only_requested_lines(workspace_root: Path) -> None:
    (workspace_root / "range.txt").write_text("l1\nl2\nl3\nl4\n", encoding="utf-8")
    service = _service(workspace_root)

    result = service.read_text(
        SelfTextReadRequest(path="range.txt", mode="line_range", start_line=2, end_line=3)
    )

    assert result.slice is not None
    assert result.slice.start_line == 2
    assert result.slice.end_line == 3
    assert result.slice.content == "l2\nl3\n"
    assert result.slice.truncated is False


def test_head_and_tail_modes(workspace_root: Path) -> None:
    (workspace_root / "modes.txt").write_text("l1\nl2\nl3\nl4\n", encoding="utf-8")
    service = _service(workspace_root)

    head = service.read_text(SelfTextReadRequest(path="modes.txt", mode="head", max_lines=2))
    tail = service.read_text(SelfTextReadRequest(path="modes.txt", mode="tail", max_lines=2))

    assert head.slice is not None
    assert head.slice.content == "l1\nl2\n"
    assert tail.slice is not None
    assert tail.slice.content == "l3\nl4\n"


def test_oversized_file_returns_truncated_bounded_preview(workspace_root: Path) -> None:
    (workspace_root / "oversized.txt").write_text("x" * 1000, encoding="utf-8")
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="oversized.txt", max_bytes=20, max_lines=20))

    assert result.slice is not None
    assert result.slice.bytes_read <= 20
    assert result.slice.truncated is True


def test_redaction_applies_to_secret_like_content(workspace_root: Path) -> None:
    secret = "api_key = AKIAABCDEFGHIJKLMNOP\npassword=supersecret\n"
    (workspace_root / "config.txt").write_text(secret, encoding="utf-8")
    service = _service(workspace_root)

    result = service.read_text(SelfTextReadRequest(path="config.txt"))

    assert result.slice is not None
    assert result.slice.redacted is True
    assert "AKIAABCDEFGHIJKLMNOP" not in result.slice.content
    assert "supersecret" not in result.slice.content
    assert "[REDACTED]" in result.slice.content
    assert result.redaction_findings


def test_text_read_contract_has_read_only_safety_flags() -> None:
    contract = SelfAwarenessRegistryService().get_contract("skill:self_awareness_text_read")

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


def test_later_self_awareness_skills_remain_contract_only() -> None:
    registry = SelfAwarenessRegistryService()
    contract_only_ids = {
        "skill:self_awareness_config_surface",
        "skill:self_awareness_test_surface",
        "skill:self_awareness_capability_registry",
        "skill:self_awareness_runtime_boundary",
    }

    for skill_id in contract_only_ids:
        contract = registry.get_contract(skill_id)
        assert contract is not None
        assert contract.implementation_status == "contract_only"
        assert contract.execution_enabled is False


def test_gate_invokes_text_read_read_only(workspace_root: Path) -> None:
    (workspace_root / "note.txt").write_text("hello\n", encoding="utf-8")
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)

    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_text_read",
        input_payload={"root_path": str(workspace_root), "path": "note.txt", "max_lines": 10},
    )

    assert result.executed is True
    assert result.blocked is False
    assert invocation.last_result is not None
    output = invocation.last_result.output_payload["output_attrs"]
    assert output["effect_type"] == READ_ONLY_OBSERVATION_EFFECT
    assert output["slice"]["content"] == "hello\n"


def test_cli_text_read_works(capsys) -> None:
    exit_code = main(["self-awareness", "text", "read", "README.md", "--max-lines", "1"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "effect=read_only_observation" in captured.out
    assert "relative_path=README.md" in captured.out
    assert "lines_read=1" in captured.out


def test_pig_and_ocpx_include_v0202_text_coverage() -> None:
    service = SelfAwarenessReportService()

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workspace_awareness_coverage"]["text_read"] == "implemented_limited_preview"
    assert pig["workspace_awareness_coverage"]["workspace_search"] == "implemented_bounded_literal"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert ocpx["workspace_awareness_state"]["text_read"] == "implemented_limited_preview"
    assert "self_text_read_completed" in ocpx["event_coverage"]

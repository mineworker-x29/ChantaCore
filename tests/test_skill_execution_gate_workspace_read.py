from chanta_core.ocel.store import OCELStore
from chanta_core.skills.execution_gate import SkillExecutionGateService


def test_gate_run_workspace_read_preserves_workspace_service_boundaries(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    outside = tmp_path.parent / "outside_gate_read.txt"
    outside.write_bytes(b"outside")
    service = SkillExecutionGateService(ocel_store=OCELStore(tmp_path / "gate.sqlite"))

    allowed = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    denied_by_workspace = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside_gate_read.txt"},
        invocation_mode="test",
    )

    assert allowed.executed is True
    assert denied_by_workspace.executed is False
    assert denied_by_workspace.blocked is True
    assert denied_by_workspace.explicit_invocation_result_id is None
    assert denied_by_workspace.status == "blocked"
    assert any(finding.finding_type == "path_traversal" for finding in service.last_findings)


def test_gate_denies_absolute_relative_path(tmp_path) -> None:
    service = SkillExecutionGateService()

    result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": str(tmp_path / "secret.txt")},
        invocation_mode="test",
    )

    assert result.executed is False
    assert result.blocked is True
    assert result.explicit_invocation_result_id is None
    assert any(finding.finding_type == "absolute_path_not_allowed" for finding in service.last_findings)


def test_gate_denies_list_workspace_files_traversal_path(tmp_path) -> None:
    service = SkillExecutionGateService()

    result = service.gate_explicit_invocation(
        skill_id="skill:list_workspace_files",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside"},
        invocation_mode="test",
    )

    assert result.executed is False
    assert result.blocked is True
    assert any(finding.finding_type == "path_traversal" for finding in service.last_findings)


def test_gate_denies_markdown_summary_traversal_path(tmp_path) -> None:
    service = SkillExecutionGateService()

    result = service.gate_explicit_invocation(
        skill_id="skill:summarize_workspace_markdown",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside.md"},
        invocation_mode="test",
    )

    assert result.executed is False
    assert result.blocked is True
    assert any(finding.finding_type == "path_traversal" for finding in service.last_findings)


def test_boundary_denied_gate_does_not_call_explicit_invocation(tmp_path) -> None:
    class Probe:
        def __init__(self) -> None:
            self.calls = 0

        def invoke_explicit_skill(self, **_) -> object:
            self.calls += 1
            return object()

    probe = Probe()
    service = SkillExecutionGateService(explicit_skill_invocation_service=probe)

    result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside.txt"},
        invocation_mode="test",
    )

    assert result.executed is False
    assert result.blocked is True
    assert probe.calls == 0

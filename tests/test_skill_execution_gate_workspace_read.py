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
    assert denied_by_workspace.executed is True
    assert denied_by_workspace.explicit_invocation_result_id is not None
    assert service.last_result.status == "executed"

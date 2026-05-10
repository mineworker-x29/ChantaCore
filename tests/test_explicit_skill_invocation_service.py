from chanta_core.ocel.store import OCELStore
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_unsupported_skill_returns_controlled_result(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:write_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    assert result.status == "unsupported"
    assert result.violation_ids
    assert service.last_violations[0].violation_type == "unsupported_skill"
    assert result.result_attrs["permission_grants_created"] is False


def test_missing_input_returns_invalid_input(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path)},
        invocation_mode="test",
    )

    assert result.status == "denied"
    assert result.violation_ids
    assert any(item.violation_type == "invalid_input" for item in service.last_violations)


def test_explicit_skill_id_required(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="",
        input_payload={"root_path": str(tmp_path)},
        invocation_mode="test",
    )

    assert result.status == "denied"
    assert any(item.violation_type == "invalid_input" for item in service.last_violations)
    assert service.last_request is not None
    assert service.last_request.request_attrs["nl_route_used"] is False

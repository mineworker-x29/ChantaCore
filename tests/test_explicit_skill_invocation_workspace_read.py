from chanta_core.ocel.store import OCELStore
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_explicit_workspace_file_list_works_with_temp_root(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.txt").write_bytes(b"public-safe text")
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:list_workspace_files",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs"},
        invocation_mode="test",
    )

    assert result.status == "completed"
    assert result.output_payload["success"] is True
    assert result.output_payload["output_attrs"]["total_entries"] == 1


def test_explicit_workspace_text_read_works_with_safe_relative_path(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    assert result.status == "completed"
    assert result.output_payload["success"] is True
    assert result.output_payload["output_text"] == "public-safe text"


def test_explicit_workspace_markdown_summary_is_deterministic(tmp_path) -> None:
    (tmp_path / "note.md").write_bytes(b"# Title\n\nPublic-safe body")
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:summarize_workspace_markdown",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.md"},
        invocation_mode="test",
    )

    assert result.status == "completed"
    assert "Title: Title" in result.output_payload["output_text"]
    assert result.output_payload["output_attrs"]["uses_llm"] is False


def test_outside_root_read_is_denied_by_workspace_service(tmp_path) -> None:
    outside = tmp_path.parent / "outside_explicit_skill_invocation.txt"
    outside.write_bytes(b"outside")
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside_explicit_skill_invocation.txt"},
        invocation_mode="test",
    )

    assert result.status == "failed"
    assert result.error_message == "Workspace text file read denied"
    assert result.output_payload["success"] is False


def test_explicit_workspace_text_read_rejects_absolute_relative_path(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": str(tmp_path / "secret.txt")},
        invocation_mode="test",
    )

    assert result.status == "denied"
    assert result.output_payload == {}
    assert result.violation_ids


def test_explicit_workspace_file_list_traversal_is_not_completed_success(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:list_workspace_files",
        input_payload={"root_path": str(tmp_path), "relative_path": "..\\outside"},
        invocation_mode="test",
    )

    assert result.status == "failed"
    assert result.output_payload["success"] is False

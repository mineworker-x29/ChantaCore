from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_write_shell_network_like_skill_ids_are_unsupported(tmp_path) -> None:
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )
    for skill_id in [
        "skill:write_file",
        "skill:shell",
        "skill:network",
        "skill:mcp",
        "skill:plugin",
    ]:
        result = service.invoke_explicit_skill(
            skill_id=skill_id,
            input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
            invocation_mode="test",
        )
        assert result.status == "unsupported"


def test_invocation_result_has_no_disallowed_execution_flags(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    service = ExplicitSkillInvocationService(
        ocel_store=OCELStore(tmp_path / "invocation.sqlite")
    )

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    assert result.result_attrs["nl_route_used"] is False
    assert result.result_attrs["llm_call_used"] is False
    assert result.result_attrs["shell_execution_used"] is False
    assert result.result_attrs["network_access_used"] is False
    assert result.result_attrs["mcp_connection_used"] is False
    assert result.result_attrs["plugin_loading_used"] is False
    assert result.result_attrs["workspace_write_used"] is False
    assert result.result_attrs["permission_grants_created"] is False


def test_invocation_source_has_no_forbidden_terms() -> None:
    text = Path("src/chanta_core/skills/invocation.py").read_text(encoding="utf-8")
    forbidden = [
        "natural_" + "language_route",
        "infer_" + "skill_from_prompt",
        "auto_" + "route_skill",
        "sub" + "process",
        "os." + "system",
        "requests" + ".",
        "httpx" + ".",
        "socket" + ".",
        "connect_" + "mcp",
        "load_" + "plugin",
        "apply_" + "grant",
        "complete_" + "text",
        "complete_" + "json",
        "runtime_store.json",
    ]
    for token in forbidden:
        assert token not in text

import inspect

import chanta_core.skills.execution_gate as gate_module
from chanta_core.skills.execution_gate import SkillExecutionGateService


def test_write_shell_network_mcp_plugin_are_denied() -> None:
    service = SkillExecutionGateService()
    skill_ids = [
        "skill:write_file",
        "skill:run_shell",
        "skill:network_request",
        "skill:mcp_call",
        "skill:load_" + "plugin",
    ]

    results = [
        service.gate_explicit_invocation(skill_id=skill_id, input_payload={})
        for skill_id in skill_ids
    ]

    assert all(result.executed is False for result in results)
    assert all(result.blocked is True for result in results)


def test_gate_source_avoids_disallowed_runtime_paths() -> None:
    source = inspect.getsource(gate_module)
    blocked_terms = [
        "natural_language_" + "execute",
        "auto_" + "execute_skill",
        "infer_" + "and_run",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "request" + "s.",
        "http" + "x.",
        "socket" + ".",
        "connect_" + "mcp",
        "apply_" + "grant",
        "write_" + "text",
        "jso" + "nl",
    ]

    for term in blocked_terms:
        assert term not in source


def test_gate_source_does_not_mutate_dispatchers() -> None:
    source = inspect.getsource(gate_module)

    assert "ToolDispatcher" not in source
    assert "SkillExecutor" not in source
    assert "PermissionGrant" not in source
    assert "create_permission" not in source

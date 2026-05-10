import inspect

import chanta_core.skills.proposal as proposal_module
from chanta_core.skills.proposal import SkillProposalRouterService


def test_skill_proposal_result_flags_show_no_execution_or_grants() -> None:
    service = SkillProposalRouterService()

    result = service.propose_from_prompt(
        user_prompt="read file docs/example.txt",
        root_path="<WORKSPACE_ROOT>",
    )

    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["permission_grants_created"] is False
    assert result.result_attrs["llm_classifier_used"] is False
    assert service.last_proposals[0].executable_now is False
    assert service.last_decisions[0].can_execute_now is False


def test_skill_proposal_source_avoids_disallowed_runtime_paths() -> None:
    source = inspect.getsource(proposal_module)
    blocked_terms = [
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "request" + "s.",
        "http" + "x.",
        "socket" + ".",
        "connect_" + "mcp",
        "load_" + "plugin",
        "apply_" + "grant",
        "write_" + "text",
        "jso" + "nl",
    ]

    for term in blocked_terms:
        assert term not in source


def test_skill_proposal_source_does_not_reference_dispatch_mutation() -> None:
    source = inspect.getsource(proposal_module)

    assert "ToolDispatcher" not in source
    assert "SkillExecutor" not in source
    assert "invoke_explicit_skill(" not in source

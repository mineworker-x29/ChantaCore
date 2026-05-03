from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from tests.test_edit_tool import context, setup


def test_proposal_only_operations_allowed_in_safe_internal(tmp_path) -> None:
    result = setup(tmp_path).dispatch(
        ToolRequest.create(
            tool_id="tool:edit",
            operation="propose_comment_only",
            process_instance_id="process_instance:edit-tool",
            session_id="session-edit-tool",
            agent_id="chanta_core_default",
            input_attrs={
                "target_path": "app.py",
                "title": "Comment",
                "rationale": "Proposal only",
            },
        ),
        context(),
    )

    assert result.success is True
    assert result.output_attrs["proposal_only"] is True


def test_apply_patch_operation_is_not_executed(tmp_path) -> None:
    result = ToolDispatcher().dispatch(
        ToolRequest.create(
            tool_id="tool:edit",
            operation="apply_patch",
            process_instance_id="process_instance:edit-tool",
            session_id="session-edit-tool",
            agent_id="chanta_core_default",
        ),
        context(),
    )

    assert result.success is False
    assert result.output_attrs["authorization_decision"]["decision"] == "deny"
    assert (tmp_path / "app.py").exists() is False

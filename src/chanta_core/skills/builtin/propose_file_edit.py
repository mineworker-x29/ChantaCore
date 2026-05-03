from __future__ import annotations

from pathlib import Path

from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def create_propose_file_edit_skill() -> Skill:
    return Skill(
        skill_id="skill:propose_file_edit",
        skill_name="propose_file_edit",
        description="Create a structured edit proposal without modifying files.",
        execution_type="builtin_edit_proposal",
        input_schema={},
        output_schema={},
        tags=["builtin", "editing", "proposal", "readonly-workspace"],
        skill_attrs={
            "is_builtin": True,
            "proposal_only": True,
            "allows_file_mutation": False,
            "requires_llm": False,
        },
    )


def execute_propose_file_edit_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    **_,
) -> SkillExecutionResult:
    target_path = str(context.context_attrs.get("target_path") or "")
    proposed_text = context.context_attrs.get("proposed_text")
    workspace_root = context.context_attrs.get("workspace_root")
    store_path = context.context_attrs.get("edit_proposal_store_path")
    workspace_inspector = WorkspaceInspector(
        WorkspaceConfig(workspace_root=Path(workspace_root) if workspace_root else Path.cwd())
    )
    store = EditProposalStore(store_path) if store_path else EditProposalStore()
    edit_service = EditProposalService(workspace_inspector=workspace_inspector, store=store)
    operation = "propose_text_replacement" if proposed_text is not None else "propose_comment_only"
    input_attrs = {
        "target_path": target_path,
        "title": str(context.context_attrs.get("title") or "Proposed file edit"),
        "rationale": str(context.context_attrs.get("rationale") or context.user_input),
    }
    if proposed_text is not None:
        input_attrs["proposed_text"] = str(proposed_text)
    tool_context = ToolExecutionContext(
        process_instance_id=context.process_instance_id,
        session_id=context.session_id,
        agent_id=context.agent_id,
        context_attrs=context.context_attrs,
    )
    tool_result = ToolDispatcher(
        trace_service=trace_service,
        edit_service=edit_service,
    ).dispatch(
        ToolRequest.create(
            tool_id="tool:edit",
            operation=operation,
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs=input_attrs,
            request_attrs={"source_skill_id": skill.skill_id},
        ),
        tool_context,
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=tool_result.success,
        output_text=tool_result.output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "tool_result": tool_result.to_dict(),
            **tool_result.output_attrs,
        },
        error=tool_result.error,
    )

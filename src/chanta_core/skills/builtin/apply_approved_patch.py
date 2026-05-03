from __future__ import annotations

from pathlib import Path

from chanta_core.editing import EditProposalStore, PatchApplicationStore, PatchApplicationService
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def create_apply_approved_patch_skill() -> Skill:
    return Skill(
        skill_id="skill:apply_approved_patch",
        skill_name="apply_approved_patch",
        description="Apply an approved edit proposal through tool policy.",
        execution_type="builtin_patch_application",
        input_schema={},
        output_schema={},
        tags=["builtin", "editing", "patch", "approval-required"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_approval": True,
            "bypasses_tool_policy": False,
        },
    )


def execute_apply_approved_patch_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    **_,
) -> SkillExecutionResult:
    workspace_root = context.context_attrs.get("workspace_root")
    inspector = WorkspaceInspector(
        WorkspaceConfig(workspace_root=Path(workspace_root) if workspace_root else Path.cwd())
    )
    proposal_store = EditProposalStore(
        context.context_attrs.get("edit_proposal_store_path")
        or "data/editing/edit_proposals.jsonl"
    )
    patch_store = PatchApplicationStore(
        context.context_attrs.get("patch_application_store_path")
        or "data/editing/patch_applications.jsonl"
    )
    patch_service = PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=patch_store,
    )
    tool_context = ToolExecutionContext(
        process_instance_id=context.process_instance_id,
        session_id=context.session_id,
        agent_id=context.agent_id,
        context_attrs=context.context_attrs,
    )
    tool_result = ToolDispatcher(
        trace_service=trace_service,
        policy=ToolPolicy(
            allow_approved_writes=bool(context.context_attrs.get("allow_approved_writes", False))
        ),
        patch_application_service=patch_service,
    ).dispatch(
        ToolRequest.create(
            tool_id="tool:edit",
            operation="apply_approved_proposal",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs={
                "proposal_id": str(context.context_attrs.get("proposal_id") or ""),
                "approved_by": str(context.context_attrs.get("approved_by") or ""),
                "approval_text": str(context.context_attrs.get("approval_text") or ""),
            },
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

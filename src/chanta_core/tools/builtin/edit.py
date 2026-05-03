from __future__ import annotations

from chanta_core.editing import (
    EditProposalService,
    EditProposalStore,
    PatchApplicationService,
    PatchApplicationStore,
    PatchApproval,
)
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool
from chanta_core.workspace import WorkspaceInspector


def create_edit_tool() -> Tool:
    return Tool(
        tool_id="tool:edit",
        tool_name="edit",
        description="Proposal-only edit planning gateway. Does not modify files.",
        tool_kind="internal",
        safety_level="write",
        supported_operations=[
            "propose_text_replacement",
            "propose_comment_only",
            "summarize_recent_proposals",
            "apply_approved_proposal",
            "dry_run_approved_proposal",
            "summarize_recent_patch_applications",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={
            "is_builtin": True,
            "proposal_only": True,
            "read_only_workspace": True,
            "allows_file_mutation": False,
            "requires_approval_for_application": True,
        },
    )


def execute_edit_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    edit_service: EditProposalService | None = None,
    patch_application_service: PatchApplicationService | None = None,
    workspace_inspector: WorkspaceInspector | None = None,
    edit_proposal_store: EditProposalStore | None = None,
    patch_application_store: PatchApplicationStore | None = None,
    **_,
) -> ToolResult:
    inspector = workspace_inspector or WorkspaceInspector()
    proposal_store = edit_proposal_store or EditProposalStore()
    service = edit_service or EditProposalService(
        workspace_inspector=inspector,
        store=proposal_store,
    )
    patch_service = patch_application_service or PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=patch_application_store,
    )
    operation = request.operation
    try:
        if operation == "propose_text_replacement":
            proposal = service.propose_text_replacement(
                target_path=str(request.input_attrs.get("target_path") or ""),
                proposed_text=str(request.input_attrs.get("proposed_text") or ""),
                title=str(request.input_attrs.get("title") or "Proposed file edit"),
                rationale=str(request.input_attrs.get("rationale") or ""),
                evidence_refs=list(request.input_attrs.get("evidence_refs") or []),
                proposal_attrs=dict(request.input_attrs.get("proposal_attrs") or {}),
            )
            return _proposal_result(tool, request, proposal)
        if operation == "propose_comment_only":
            proposal = service.propose_comment_only(
                target_path=str(request.input_attrs.get("target_path") or ""),
                title=str(request.input_attrs.get("title") or "Edit proposal note"),
                rationale=str(request.input_attrs.get("rationale") or ""),
                evidence_refs=list(request.input_attrs.get("evidence_refs") or []),
                proposal_attrs=dict(request.input_attrs.get("proposal_attrs") or {}),
            )
            return _proposal_result(tool, request, proposal)
        if operation == "summarize_recent_proposals":
            summary = service.summarize_recent_proposals(
                limit=int(request.input_attrs.get("limit", 20))
            )
            return ToolResult.create(
                tool_request_id=request.tool_request_id,
                tool_id=tool.tool_id,
                operation=request.operation,
                success=True,
                output_text=f"Edit proposals: {summary['proposal_count']}",
                output_attrs={
                    "summary": summary,
                    "proposal_only": True,
                    "workspace_file_mutated": False,
                },
            )
        if operation == "apply_approved_proposal":
            approval = _approval_from_request(request)
            application = patch_service.apply_approved_proposal(
                proposal_id=str(request.input_attrs.get("proposal_id") or ""),
                approval=approval,
            )
            return _patch_result(tool, request, application)
        if operation == "dry_run_approved_proposal":
            approval = _approval_from_request(request)
            application = patch_service.dry_run_approved_proposal(
                proposal_id=str(request.input_attrs.get("proposal_id") or ""),
                approval=approval,
            )
            return _patch_result(tool, request, application)
        if operation == "summarize_recent_patch_applications":
            summary = patch_service.summarize_recent_patch_applications(
                limit=int(request.input_attrs.get("limit", 20))
            )
            return ToolResult.create(
                tool_request_id=request.tool_request_id,
                tool_id=tool.tool_id,
                operation=request.operation,
                success=True,
                output_text=f"Patch applications: {summary['patch_application_count']}",
                output_attrs={"summary": summary},
            )
    except Exception as error:
        return ToolResult.create(
            tool_request_id=request.tool_request_id,
            tool_id=tool.tool_id,
            operation=request.operation,
            success=False,
            output_text=None,
            output_attrs={
                "exception_type": type(error).__name__,
                "failure_stage": "edit_tool",
            },
            error=str(error),
        )

    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=False,
        output_text=None,
        output_attrs={
            "exception_type": "ToolDispatchError",
            "failure_stage": "edit_tool",
        },
        error=f"Unsupported tool:edit operation: {operation}",
    )


def _proposal_result(tool: Tool, request: ToolRequest, proposal) -> ToolResult:
    diff_length = len(proposal.proposed_diff or "")
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=(
            f"Edit proposal created: {proposal.proposal_id} "
            f"for {proposal.target_path}"
        ),
        output_attrs={
            "proposal": proposal.to_dict(),
            "proposal_id": proposal.proposal_id,
            "target_path": proposal.target_path,
            "risk_level": proposal.risk_level,
            "status": proposal.status,
            "proposed_diff": proposal.proposed_diff,
            "proposed_diff_length": diff_length,
            "proposal_only": True,
            "workspace_file_mutated": False,
        },
    )


def _approval_from_request(request: ToolRequest) -> PatchApproval:
    return PatchApproval.create(
        proposal_id=str(request.input_attrs.get("proposal_id") or ""),
        approved_by=str(request.input_attrs.get("approved_by") or ""),
        approval_text=str(request.input_attrs.get("approval_text") or ""),
        approval_attrs=dict(request.input_attrs.get("approval_attrs") or {}),
    )


def _patch_result(tool: Tool, request: ToolRequest, application) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=application.status in {"applied", "pending"},
        output_text=(
            f"Patch application {application.status}: "
            f"{application.patch_application_id}"
        ),
        output_attrs={
            "patch_application": application.to_dict(),
            "patch_application_id": application.patch_application_id,
            "proposal_id": application.proposal_id,
            "approval_id": application.approval_id,
            "target_path": application.target_path,
            "status": application.status,
            "backup_path": application.backup_path,
            "workspace_file_mutated": application.status == "applied",
        },
        error=application.error,
    )

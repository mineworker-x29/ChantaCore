from __future__ import annotations

from typing import Any, Callable

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.tools.builtin import (
    execute_edit_tool,
    execute_echo_tool,
    execute_ocel_tool,
    execute_ocpx_tool,
    execute_pig_tool,
    execute_repo_tool,
    execute_workspace_tool,
)
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.errors import ToolDispatchError
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool


class ToolDispatcher:
    def __init__(
        self,
        *,
        registry: ToolRegistry | None = None,
        policy: ToolPolicy | None = None,
        trace_service=None,
        ocel_store: OCELStore | None = None,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
        pig_feedback_service=None,
        pig_guidance_service=None,
        pig_conformance_service=None,
        artifact_store=None,
        workspace_inspector=None,
        repo_scanner=None,
        repo_search_service=None,
        repo_symbol_scanner=None,
        edit_service=None,
        edit_proposal_store=None,
        patch_application_service=None,
        patch_application_store=None,
    ) -> None:
        self.registry = registry or ToolRegistry()
        self.policy = policy or ToolPolicy()
        self.trace_service = trace_service
        self.ocel_store = ocel_store or getattr(trace_service, "ocel_store", None)
        self.ocpx_loader = ocpx_loader
        self.ocpx_engine = ocpx_engine
        self.pig_feedback_service = pig_feedback_service
        self.pig_guidance_service = pig_guidance_service
        self.pig_conformance_service = pig_conformance_service
        self.artifact_store = artifact_store
        self.workspace_inspector = workspace_inspector
        self.repo_scanner = repo_scanner
        self.repo_search_service = repo_search_service
        self.repo_symbol_scanner = repo_symbol_scanner
        self.edit_service = edit_service
        self.edit_proposal_store = edit_proposal_store
        self.patch_application_service = patch_application_service
        self.patch_application_store = patch_application_store
        self._handlers: dict[str, Callable[..., ToolResult]] = {
            "tool:edit": execute_edit_tool,
            "tool:echo": execute_echo_tool,
            "tool:ocel": execute_ocel_tool,
            "tool:ocpx": execute_ocpx_tool,
            "tool:pig": execute_pig_tool,
            "tool:repo": execute_repo_tool,
            "tool:workspace": execute_workspace_tool,
        }

    def dispatch(
        self,
        request: ToolRequest,
        context: ToolExecutionContext,
    ) -> ToolResult:
        tool = self.registry.require(request.tool_id)
        self._record("create_tool_request", tool, request, context)
        authorization = self.policy.authorize(tool, request)
        self._record(
            "authorize_tool_request",
            tool,
            request,
            context,
            authorization=authorization.to_dict(),
        )
        if authorization.requires_approval:
            result = ToolResult.create(
                tool_request_id=request.tool_request_id,
                tool_id=tool.tool_id,
                operation=request.operation,
                success=False,
                output_text=None,
                output_attrs={
                    "authorization_decision": authorization.to_dict(),
                    "requires_approval": True,
                    "risk_level": authorization.risk_level,
                    "permission_mode": authorization.mode,
                    "approval_required": True,
                },
                error=f"Tool operation requires approval: {authorization.reason}",
            )
            self._record(
                "fail_tool_operation",
                tool,
                request,
                context,
                result=result,
                error=result.error,
            )
            return result

        if not authorization.allowed:
            result = ToolResult.create(
                tool_request_id=request.tool_request_id,
                tool_id=tool.tool_id,
                operation=request.operation,
                success=False,
                output_text=None,
                output_attrs={
                    "authorization": authorization.to_dict(),
                    "authorization_decision": authorization.to_dict(),
                    "requires_approval": authorization.requires_approval,
                    "risk_level": authorization.risk_level,
                    "permission_mode": authorization.mode,
                },
                error=authorization.reason,
            )
            self._record(
                "fail_tool_operation",
                tool,
                request,
                context,
                result=result,
                error=authorization.reason,
            )
            return result

        if request.operation not in tool.supported_operations:
            return self._failure(
                tool=tool,
                request=request,
                context=context,
                error=f"Unsupported operation for {tool.tool_id}: {request.operation}",
            )

        self._record("dispatch_tool", tool, request, context)
        self._record("execute_tool_operation", tool, request, context)
        try:
            handler = self._handlers.get(tool.tool_id)
            if handler is None:
                raise ToolDispatchError(f"No handler for tool: {tool.tool_id}")
            result = handler(
                tool=tool,
                request=request,
                context=context,
                ocel_store=self.ocel_store,
                ocpx_loader=self.ocpx_loader,
                ocpx_engine=self.ocpx_engine,
                pig_feedback_service=self.pig_feedback_service,
                pig_guidance_service=self.pig_guidance_service,
                pig_conformance_service=self.pig_conformance_service,
                artifact_store=self.artifact_store,
                workspace_inspector=self.workspace_inspector,
                repo_scanner=self.repo_scanner,
                repo_search_service=self.repo_search_service,
                repo_symbol_scanner=self.repo_symbol_scanner,
                edit_service=self.edit_service,
                edit_proposal_store=self.edit_proposal_store,
                patch_application_service=self.patch_application_service,
                patch_application_store=self.patch_application_store,
            )
        except Exception as error:
            return self._failure(
                tool=tool,
                request=request,
                context=context,
                error=str(error),
                exception_type=type(error).__name__,
            )

        if result.success:
            self._record("complete_tool_operation", tool, request, context, result=result)
            self._record("observe_tool_result", tool, request, context, result=result)
        else:
            self._record(
                "fail_tool_operation",
                tool,
                request,
                context,
                result=result,
                error=result.error,
            )
        return result

    def _failure(
        self,
        *,
        tool: Tool,
        request: ToolRequest,
        context: ToolExecutionContext,
        error: str,
        exception_type: str = "ToolDispatchError",
    ) -> ToolResult:
        result = ToolResult.create(
            tool_request_id=request.tool_request_id,
            tool_id=tool.tool_id,
            operation=request.operation,
            success=False,
            output_text=None,
            output_attrs={"exception_type": exception_type},
            error=error,
        )
        self._record(
            "fail_tool_operation",
            tool,
            request,
            context,
            result=result,
            error=error,
        )
        return result

    def _record(
        self,
        event_activity: str,
        tool: Tool,
        request: ToolRequest,
        context: ToolExecutionContext,
        *,
        result: ToolResult | None = None,
        authorization: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        if self.trace_service is None:
            return
        recorder = getattr(self.trace_service, "record_tool_lifecycle_event", None)
        if recorder is None:
            return
        recorder(
            tool=tool,
            request=request,
            context=context,
            event_activity=event_activity,
            result=result,
            authorization=authorization,
            error=error,
        )

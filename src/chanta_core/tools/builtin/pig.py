from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.pig.feedback import PIGFeedbackService
from chanta_core.pig.guidance import PIGGuidanceService
from chanta_core.pig.service import PIGService
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.errors import ToolDispatchError
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.result import ToolResult
from chanta_core.tools.tool import Tool


def create_pig_tool() -> Tool:
    return Tool(
        tool_id="tool:pig",
        tool_name="pig",
        description="Internal intelligence gateway for PIG context, guidance, and diagnostics.",
        tool_kind="internal",
        safety_level="internal_intelligence",
        supported_operations=[
            "build_context",
            "build_guidance",
            "check_self_conformance",
            "summarize_pi_artifacts",
            "build_recommendations",
        ],
        input_schema={},
        output_schema={},
        tool_attrs={"is_builtin": True, "uses_pig": True},
    )


def execute_pig_tool(
    *,
    tool: Tool,
    request: ToolRequest,
    context: ToolExecutionContext,
    ocel_store: OCELStore | None = None,
    pig_feedback_service: PIGFeedbackService | None = None,
    pig_guidance_service: PIGGuidanceService | None = None,
    pig_conformance_service: PIGConformanceService | None = None,
    artifact_store: PIArtifactStore | None = None,
    **_,
) -> ToolResult:
    store = ocel_store or OCELStore()
    loader = OCPXLoader(store=store)
    operation = request.operation
    if operation == "build_context":
        feedback = pig_feedback_service or PIGFeedbackService(ocpx_loader=loader)
        pig_context = _build_context(request, context, feedback)
        return _result(
            tool,
            request,
            output_text=pig_context.context_text,
            output_attrs={
                "pig_context": pig_context.to_dict(),
                "context_text": pig_context.context_text,
            },
        )
    if operation == "build_guidance":
        guidance_service = pig_guidance_service or PIGGuidanceService(
            feedback_service=pig_feedback_service
            or PIGFeedbackService(ocpx_loader=loader)
        )
        guidance = _build_guidance(request, context, guidance_service)
        return _result(
            tool,
            request,
            output_attrs={"guidance": [item.to_dict() for item in guidance]},
        )
    if operation == "check_self_conformance":
        service = pig_conformance_service or PIGConformanceService(ocpx_loader=loader)
        report = _check_conformance(request, context, service)
        return _result(
            tool,
            request,
            output_text=(
                f"Self-conformance: status={report.status}, issues={len(report.issues)}"
            ),
            output_attrs={
                "conformance_report": report.to_dict(),
                "status": report.status,
                "issue_count": len(report.issues),
            },
        )
    if operation == "summarize_pi_artifacts":
        artifacts = (artifact_store or PIArtifactStore()).recent(
            limit=int(request.input_attrs.get("limit", 20))
        )
        artifact_types: dict[str, int] = {}
        for artifact in artifacts:
            artifact_types[artifact.artifact_type] = (
                artifact_types.get(artifact.artifact_type, 0) + 1
            )
        return _result(
            tool,
            request,
            output_text=f"PI artifacts: {len(artifacts)}",
            output_attrs={
                "artifact_count": len(artifacts),
                "artifact_types": artifact_types,
                "recent_titles": [artifact.title for artifact in artifacts[-5:]],
            },
        )
    if operation == "build_recommendations":
        pig_service = PIGService(loader=loader)
        scope = str(request.input_attrs.get("scope") or "recent")
        if scope == "process_instance":
            result = pig_service.analyze_process_instance(
                str(request.input_attrs.get("process_instance_id") or context.process_instance_id)
            )
        elif scope == "session":
            result = pig_service.analyze_session(
                str(request.input_attrs.get("session_id") or context.session_id)
            )
        else:
            result = pig_service.analyze_recent(limit=int(request.input_attrs.get("limit", 20)))
        return _result(
            tool,
            request,
            output_attrs={"recommendations": result.get("recommendations", [])},
        )
    raise ToolDispatchError(f"Unsupported tool:pig operation: {operation}")


def _build_context(
    request: ToolRequest,
    context: ToolExecutionContext,
    feedback: PIGFeedbackService,
):
    scope = str(request.input_attrs.get("scope") or "recent")
    if scope == "process_instance":
        return feedback.build_process_instance_context(
            str(request.input_attrs.get("process_instance_id") or context.process_instance_id)
        )
    if scope == "session":
        return feedback.build_session_context(
            str(request.input_attrs.get("session_id") or context.session_id)
        )
    return feedback.build_recent_context(limit=int(request.input_attrs.get("limit", 20)))


def _build_guidance(
    request: ToolRequest,
    context: ToolExecutionContext,
    guidance_service: PIGGuidanceService,
):
    scope = str(request.input_attrs.get("scope") or "recent")
    if scope == "process_instance":
        return guidance_service.build_process_instance_guidance(
            str(request.input_attrs.get("process_instance_id") or context.process_instance_id)
        )
    return guidance_service.build_recent_guidance(limit=int(request.input_attrs.get("limit", 20)))


def _check_conformance(
    request: ToolRequest,
    context: ToolExecutionContext,
    service: PIGConformanceService,
):
    scope = str(request.input_attrs.get("scope") or "recent")
    if scope == "process_instance":
        return service.check_process_instance(
            str(request.input_attrs.get("process_instance_id") or context.process_instance_id)
        )
    if scope == "session":
        return service.check_session(
            str(request.input_attrs.get("session_id") or context.session_id)
        )
    return service.check_recent(limit=int(request.input_attrs.get("limit", 20)))


def _result(
    tool: Tool,
    request: ToolRequest,
    *,
    output_attrs: dict,
    output_text: str | None = None,
) -> ToolResult:
    return ToolResult.create(
        tool_request_id=request.tool_request_id,
        tool_id=tool.tool_id,
        operation=request.operation,
        success=True,
        output_text=output_text,
        output_attrs=output_attrs,
    )

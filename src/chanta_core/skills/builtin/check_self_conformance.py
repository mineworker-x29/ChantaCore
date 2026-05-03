from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


def create_check_self_conformance_skill() -> Skill:
    return Skill(
        skill_id="skill:check_self_conformance",
        skill_name="check_self_conformance",
        description=(
            "Check whether recent or process-instance ChantaCore runtime traces "
            "conform to expected ProcessRunLoop contracts."
        ),
        execution_type="builtin_process_intelligence",
        input_schema={},
        output_schema={},
        tags=["builtin", "pig", "conformance", "process-intelligence", "readonly"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_ocpx": True,
            "uses_pig": True,
        },
    )


def execute_check_self_conformance_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    ocel_store: OCELStore | None = None,
    trace_service=None,
    **_,
) -> SkillExecutionResult:
    store = ocel_store or OCELStore()
    process_instance_id = context.context_attrs.get("process_instance_id")
    input_attrs = {"limit": int(context.context_attrs.get("limit", 20))}
    if process_instance_id:
        input_attrs.update(
            {
                "scope": "process_instance",
                "process_instance_id": str(process_instance_id),
            }
        )
    else:
        input_attrs["scope"] = "recent"
    tool_result = ToolDispatcher(
        trace_service=trace_service,
        ocel_store=store,
    ).dispatch(
        ToolRequest.create(
            tool_id="tool:pig",
            operation="check_self_conformance",
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs=input_attrs,
            request_attrs={"source_skill_id": skill.skill_id},
        ),
        ToolExecutionContext(
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            context_attrs=context.context_attrs,
        ),
    )
    report_data = dict(tool_result.output_attrs.get("conformance_report") or {})
    status = str(tool_result.output_attrs.get("status") or "unknown")
    issue_count = int(tool_result.output_attrs.get("issue_count") or 0)
    output_text = (
        "Self-conformance check: "
        f"status={status}, issues={issue_count}, scope={report_data.get('scope')}."
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=tool_result.success,
        output_text=output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "status": status,
            "issue_count": issue_count,
            "issues": list(report_data.get("issues") or []),
            "scope": report_data.get("scope"),
            "report": report_data,
            "advisory": True,
            "diagnostic_only": True,
            "tool_result": tool_result.to_dict(),
        },
        error=tool_result.error,
    )

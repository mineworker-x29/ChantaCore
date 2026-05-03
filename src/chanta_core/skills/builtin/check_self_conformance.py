from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


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
    **_,
) -> SkillExecutionResult:
    store = ocel_store or OCELStore()
    service = PIGConformanceService(ocpx_loader=OCPXLoader(store=store))
    process_instance_id = context.context_attrs.get("process_instance_id")
    if process_instance_id:
        report = service.check_process_instance(str(process_instance_id))
    else:
        limit = int(context.context_attrs.get("limit", 20))
        report = service.check_recent(limit=limit)

    report_data = report.to_dict()
    issue_count = len(report.issues)
    output_text = (
        "Self-conformance check: "
        f"status={report.status}, issues={issue_count}, scope={report.scope}."
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "status": report.status,
            "issue_count": issue_count,
            "issues": [issue.to_dict() for issue in report.issues],
            "scope": report.scope,
            "report": report_data,
            "advisory": True,
            "diagnostic_only": True,
        },
    )

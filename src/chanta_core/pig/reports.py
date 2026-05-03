from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.pig.guidance import PIGGuidanceService
from chanta_core.pig.service import PIGService
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class ProcessRunReport:
    report_id: str
    scope: str
    process_instance_id: str | None
    session_id: str | None
    generated_at: str
    activity_sequence: list[str]
    object_type_counts: dict[str, int]
    event_activity_counts: dict[str, int]
    relation_coverage: dict[str, Any]
    variant_summary: dict[str, Any]
    performance_summary: dict[str, Any]
    conformance_report: dict[str, Any] | None
    decision_summary: dict[str, Any] | None
    guidance_summary: dict[str, Any] | None
    tool_usage_summary: dict[str, Any] | None
    skill_usage_summary: dict[str, Any] | None
    report_text: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "scope": self.scope,
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "generated_at": self.generated_at,
            "activity_sequence": self.activity_sequence,
            "object_type_counts": self.object_type_counts,
            "event_activity_counts": self.event_activity_counts,
            "relation_coverage": self.relation_coverage,
            "variant_summary": self.variant_summary,
            "performance_summary": self.performance_summary,
            "conformance_report": self.conformance_report,
            "decision_summary": self.decision_summary,
            "guidance_summary": self.guidance_summary,
            "tool_usage_summary": self.tool_usage_summary,
            "skill_usage_summary": self.skill_usage_summary,
            "report_text": self.report_text,
            "report_attrs": self.report_attrs,
        }


class PIGReportService:
    def __init__(
        self,
        *,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
        pig_service: PIGService | None = None,
        conformance_service: PIGConformanceService | None = None,
        guidance_service: PIGGuidanceService | None = None,
    ) -> None:
        self.ocpx_loader = ocpx_loader or OCPXLoader()
        self.ocpx_engine = ocpx_engine or OCPXEngine()
        self.pig_service = pig_service or PIGService(loader=self.ocpx_loader)
        self.conformance_service = conformance_service or PIGConformanceService(
            ocpx_loader=self.ocpx_loader,
            ocpx_engine=self.ocpx_engine,
        )
        self.guidance_service = guidance_service or PIGGuidanceService()

    def build_recent_report(self, limit: int = 50) -> ProcessRunReport:
        view = self.ocpx_loader.load_recent_view(limit=limit)
        return self._build_report(view=view, scope="recent", context_attrs={"limit": limit})

    def build_process_instance_report(
        self,
        process_instance_id: str,
    ) -> ProcessRunReport:
        view = self.ocpx_loader.load_process_instance_view(process_instance_id)
        return self._build_report(
            view=view,
            scope="process_instance",
            process_instance_id=process_instance_id,
            context_attrs={},
        )

    def build_session_report(self, session_id: str) -> ProcessRunReport:
        view = self.ocpx_loader.load_session_view(session_id)
        return self._build_report(
            view=view,
            scope="session",
            session_id=session_id,
            context_attrs={},
        )

    def _build_report(
        self,
        *,
        view: OCPXProcessView,
        scope: str,
        process_instance_id: str | None = None,
        session_id: str | None = None,
        context_attrs: dict[str, Any],
    ) -> ProcessRunReport:
        activity_sequence = self.ocpx_engine.activity_sequence(view)
        object_type_counts = self.ocpx_engine.count_objects_by_type(view)
        event_activity_counts = self.ocpx_engine.count_events_by_activity(view)
        relation_coverage = self.ocpx_engine.compute_relation_coverage(view)
        variant_summary = self.ocpx_engine.compute_variant_summary(view).to_dict()
        performance_summary = self.ocpx_engine.compute_basic_performance(view)
        conformance_report = self.conformance_service.check_view(
            view,
            scope=scope,
        ).to_dict()
        decision_summary = self._decision_summary(view)
        guidance_summary = self._guidance_summary(view)
        skill_usage_summary = self._skill_usage_summary(view)
        tool_usage_summary = self._tool_usage_summary(view)
        generated_at = utc_now_iso()
        report_text = self._render_report_text(
            scope=scope,
            generated_at=generated_at,
            activity_sequence=activity_sequence,
            object_type_counts=object_type_counts,
            relation_coverage=relation_coverage,
            variant_summary=variant_summary,
            performance_summary=performance_summary,
            conformance_report=conformance_report,
            decision_summary=decision_summary,
            guidance_summary=guidance_summary,
            skill_usage_summary=skill_usage_summary,
            tool_usage_summary=tool_usage_summary,
        )
        return ProcessRunReport(
            report_id=f"pig_report:{uuid4()}",
            scope=scope,
            process_instance_id=process_instance_id or self._process_instance_id(view),
            session_id=session_id or view.session_id,
            generated_at=generated_at,
            activity_sequence=activity_sequence,
            object_type_counts=object_type_counts,
            event_activity_counts=event_activity_counts,
            relation_coverage=relation_coverage,
            variant_summary=variant_summary,
            performance_summary=performance_summary,
            conformance_report=conformance_report,
            decision_summary=decision_summary,
            guidance_summary=guidance_summary,
            tool_usage_summary=tool_usage_summary,
            skill_usage_summary=skill_usage_summary,
            report_text=report_text,
            report_attrs={
                **context_attrs,
                "read_only": True,
                "view_id": view.view_id,
                "view_source": view.source,
                "diagnostic_only": True,
            },
        )

    def _guidance_summary(self, view: OCPXProcessView) -> dict[str, Any]:
        try:
            guidance = self.guidance_service.build_from_variant_summary(
                self.ocpx_engine.compute_variant_summary(view)
            )
        except Exception as error:
            return {"available": False, "warning": str(error)}
        active = [item for item in guidance if item.status == "active"]
        suggested_skills: dict[str, int] = {}
        for item in active:
            if item.suggested_skill_id:
                suggested_skills[item.suggested_skill_id] = (
                    suggested_skills.get(item.suggested_skill_id, 0) + 1
                )
        top_suggested_skill = (
            sorted(suggested_skills.items(), key=lambda item: (-item[1], item[0]))[0][0]
            if suggested_skills
            else None
        )
        return {
            "active_guidance_count": len(active),
            "guidance_count": len(guidance),
            "top_suggested_skill": top_suggested_skill,
            "suggested_skills": suggested_skills,
            "guidance": [item.to_dict() for item in guidance[:5]],
        }

    @staticmethod
    def _decision_summary(view: OCPXProcessView) -> dict[str, Any]:
        decision_modes: dict[str, int] = {}
        selected_skills: dict[str, int] = {}
        fallback_count = 0
        tie_break_count = 0
        for event in view.events:
            if event.event_activity != "decide_skill":
                continue
            mode = str(event.event_attrs.get("decision_mode") or "unknown")
            decision_modes[mode] = decision_modes.get(mode, 0) + 1
            selected_skill_id = event.event_attrs.get("selected_skill_id")
            if selected_skill_id:
                selected_skills[str(selected_skill_id)] = (
                    selected_skills.get(str(selected_skill_id), 0) + 1
                )
            if event.event_attrs.get("fallback_used"):
                fallback_count += 1
            if event.event_attrs.get("tie_break_used"):
                tie_break_count += 1
        return {
            "decision_event_count": sum(decision_modes.values()),
            "decision_modes": decision_modes,
            "selected_skills": selected_skills,
            "fallback_count": fallback_count,
            "tie_break_count": tie_break_count,
        }

    @staticmethod
    def _skill_usage_summary(view: OCPXProcessView) -> dict[str, Any]:
        selected_skills: dict[str, int] = {}
        executed_skills: dict[str, int] = {}
        skill_objects: dict[str, int] = {}
        failed_skill_execution_count = 0
        for event in view.events:
            if event.event_activity == "fail_skill_execution":
                failed_skill_execution_count += 1
            if event.event_activity == "select_skill" and event.event_attrs.get("skill_id"):
                skill_id = str(event.event_attrs["skill_id"])
                selected_skills[skill_id] = selected_skills.get(skill_id, 0) + 1
            if event.event_activity == "execute_skill" and event.event_attrs.get("skill_id"):
                skill_id = str(event.event_attrs["skill_id"])
                executed_skills[skill_id] = executed_skills.get(skill_id, 0) + 1
            for related in event.related_objects:
                qualifier = related.get("qualifier")
                object_type = related.get("object_type")
                object_id = str(related.get("object_id"))
                if object_type == "skill":
                    skill_objects[object_id] = skill_objects.get(object_id, 0) + 1
                if qualifier == "selected_skill":
                    selected_skills[object_id] = selected_skills.get(object_id, 0) + 1
                if qualifier == "executed_skill":
                    executed_skills[object_id] = executed_skills.get(object_id, 0) + 1
        return {
            "selected_skills": selected_skills,
            "executed_skills": executed_skills,
            "skill_objects": skill_objects,
            "failed_skill_execution_count": failed_skill_execution_count,
        }

    @staticmethod
    def _tool_usage_summary(view: OCPXProcessView) -> dict[str, Any]:
        tools: dict[str, int] = {}
        operations: dict[str, int] = {}
        tool_operation_count = 0
        failed_tool_operation_count = 0
        lifecycle_activities = {
            "create_tool_request",
            "dispatch_tool",
            "execute_tool_operation",
            "complete_tool_operation",
            "fail_tool_operation",
        }
        for event in view.events:
            if event.event_activity in lifecycle_activities:
                tool_operation_count += 1
            if event.event_activity == "fail_tool_operation":
                failed_tool_operation_count += 1
            tool_id = event.event_attrs.get("tool_id")
            if tool_id:
                tools[str(tool_id)] = tools.get(str(tool_id), 0) + 1
            operation = event.event_attrs.get("operation")
            if operation:
                operations[str(operation)] = operations.get(str(operation), 0) + 1
            for related in event.related_objects:
                if related.get("object_type") == "tool":
                    object_id = str(related.get("object_id"))
                    tools[object_id] = tools.get(object_id, 0) + 1
        return {
            "tool_operation_count": tool_operation_count,
            "failed_tool_operation_count": failed_tool_operation_count,
            "tools": tools,
            "operations": operations,
        }

    @staticmethod
    def _render_report_text(
        *,
        scope: str,
        generated_at: str,
        activity_sequence: list[str],
        object_type_counts: dict[str, int],
        relation_coverage: dict[str, Any],
        variant_summary: dict[str, Any],
        performance_summary: dict[str, Any],
        conformance_report: dict[str, Any] | None,
        decision_summary: dict[str, Any] | None,
        guidance_summary: dict[str, Any] | None,
        skill_usage_summary: dict[str, Any] | None,
        tool_usage_summary: dict[str, Any] | None,
    ) -> str:
        conformance_issues = (
            len(conformance_report.get("issues") or []) if conformance_report else 0
        )
        relation_ratio = float(relation_coverage.get("coverage_ratio") or 0.0)
        skill_lines = PIGReportService._count_lines(
            (skill_usage_summary or {}).get("executed_skills") or {}
        )
        tool_lines = PIGReportService._count_lines(
            (tool_usage_summary or {}).get("tools") or {}
        )
        return "\n".join(
            [
                "ChantaCore PI Report",
                f"Scope: {scope}",
                f"Generated at: {generated_at}",
                "",
                "Activity Sequence:",
                f"- {PIGReportService._sequence_text(activity_sequence)}",
                "",
                "Counts:",
                f"- Events: {len(activity_sequence)}",
                f"- Objects: {sum(object_type_counts.values())}",
                f"- Relation coverage: {relation_ratio * 100:.1f}%",
                "",
                "Variant:",
                f"- Key: {variant_summary.get('variant_key') or 'none'}",
                f"- Success count: {variant_summary.get('success_count', 0)}",
                f"- Failure count: {variant_summary.get('failure_count', 0)}",
                "",
                "Performance:",
                f"- Duration seconds: {performance_summary.get('duration_seconds')}",
                f"- LLM calls: {performance_summary.get('llm_call_count', 0)}",
                f"- Skill executions: {performance_summary.get('skill_execution_count', 0)}",
                f"- Tool operations: {(tool_usage_summary or {}).get('tool_operation_count', 0)}",
                f"- Failures: {performance_summary.get('failure_count', 0)}",
                "",
                "Conformance:",
                f"- Status: {(conformance_report or {}).get('status', 'unknown')}",
                f"- Issues: {conformance_issues}",
                "",
                "Guidance:",
                f"- Active guidance: {(guidance_summary or {}).get('active_guidance_count', 0)}",
                f"- Top suggested skill: {(guidance_summary or {}).get('top_suggested_skill') or 'none'}",
                "",
                "Decision:",
                f"- Decision events: {(decision_summary or {}).get('decision_event_count', 0)}",
                "",
                "Skill Usage:",
                skill_lines,
                "",
                "Tool Usage:",
                tool_lines,
            ]
        )

    @staticmethod
    def _sequence_text(activity_sequence: list[str], max_items: int = 16) -> str:
        if not activity_sequence:
            return "none"
        visible = activity_sequence[:max_items]
        suffix = " -> ..." if len(activity_sequence) > max_items else ""
        return f"{' -> '.join(visible)}{suffix}"

    @staticmethod
    def _count_lines(counts: dict[str, int]) -> str:
        if not counts:
            return "- none"
        return "\n".join(f"- {key}: {counts[key]}" for key in sorted(counts))

    @staticmethod
    def _process_instance_id(view: OCPXProcessView) -> str | None:
        process_instance_id = view.view_attrs.get("process_instance_id")
        if process_instance_id:
            return str(process_instance_id)
        for item in view.objects:
            if item.object_type == "process_instance":
                return item.object_id
        for event in view.events:
            if event.event_attrs.get("process_instance_id"):
                return str(event.event_attrs["process_instance_id"])
        return None

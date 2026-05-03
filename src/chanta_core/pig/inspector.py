from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.registry import SkillRegistry
from chanta_core.tools.registry import ToolRegistry
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class PISubstrateInspection:
    inspection_id: str
    generated_at: str
    ocel_summary: dict[str, Any]
    ocpx_summary: dict[str, Any]
    pig_summary: dict[str, Any]
    skill_summary: dict[str, Any]
    tool_summary: dict[str, Any]
    conformance_summary: dict[str, Any]
    warnings: list[str]
    inspection_text: str
    inspection_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "inspection_id": self.inspection_id,
            "generated_at": self.generated_at,
            "ocel_summary": self.ocel_summary,
            "ocpx_summary": self.ocpx_summary,
            "pig_summary": self.pig_summary,
            "skill_summary": self.skill_summary,
            "tool_summary": self.tool_summary,
            "conformance_summary": self.conformance_summary,
            "warnings": self.warnings,
            "inspection_text": self.inspection_text,
            "inspection_attrs": self.inspection_attrs,
        }


class PISubstrateInspector:
    def __init__(
        self,
        *,
        ocel_store: OCELStore | None = None,
        ocel_validator: OCELValidator | None = None,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
        pig_report_service: PIGReportService | None = None,
        pig_conformance_service: PIGConformanceService | None = None,
        skill_registry: SkillRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        self.ocel_store = ocel_store or OCELStore()
        self.ocel_validator = ocel_validator or OCELValidator(self.ocel_store)
        self.ocpx_loader = ocpx_loader or OCPXLoader(store=self.ocel_store)
        self.ocpx_engine = ocpx_engine or OCPXEngine()
        self.pig_report_service = pig_report_service or PIGReportService(
            ocpx_loader=self.ocpx_loader,
            ocpx_engine=self.ocpx_engine,
        )
        self.pig_conformance_service = (
            pig_conformance_service
            or PIGConformanceService(
                ocpx_loader=self.ocpx_loader,
                ocpx_engine=self.ocpx_engine,
            )
        )
        self.skill_registry = skill_registry or SkillRegistry()
        self.tool_registry = tool_registry or ToolRegistry()

    def inspect(self, limit: int = 50) -> PISubstrateInspection:
        view = self.ocpx_loader.load_recent_view(limit=limit)
        report = self.pig_report_service.build_recent_report(limit=limit)
        conformance = self.pig_conformance_service.check_view(
            view,
            scope="recent",
        )
        duplicate_validation = self.ocel_validator.validate_duplicate_relations()
        ocel_summary = {
            "event_count": self.ocel_store.fetch_event_count(),
            "object_count": self.ocel_store.fetch_object_count(),
            "event_object_relation_count": self.ocel_store.fetch_event_object_relation_count(),
            "object_object_relation_count": self.ocel_store.fetch_object_object_relation_count(),
            "duplicate_relation_validation": duplicate_validation,
        }
        ocpx_summary = {
            "activity_sequence": self.ocpx_engine.activity_sequence(view),
            "event_activity_counts": self.ocpx_engine.count_events_by_activity(view),
            "object_type_counts": self.ocpx_engine.count_objects_by_type(view),
            "relation_coverage": self.ocpx_engine.compute_relation_coverage(view),
        }
        pig_summary = {
            "recent_report_status": report.conformance_report.get("status")
            if report.conformance_report
            else "unknown",
            "guidance_count": (report.guidance_summary or {}).get("guidance_count", 0),
            "diagnostics_count": 0,
            "recommendations_count": 0,
        }
        conformance_summary = {
            "status": conformance.status,
            "issue_count": len(conformance.issues),
        }
        skill_ids = [skill.skill_id for skill in self.skill_registry.list_skills()]
        tool_items = self.tool_registry.list_tools()
        tool_ids = [tool.tool_id for tool in tool_items]
        skill_summary = {
            "built_in_skill_count": len(skill_ids),
            "skill_ids": skill_ids,
        }
        tool_summary = {
            "built_in_tool_count": len(tool_ids),
            "tool_ids": tool_ids,
            "safety_levels": {tool.tool_id: tool.safety_level for tool in tool_items},
        }
        warnings = self._warnings(
            ocel_summary=ocel_summary,
            ocpx_summary=ocpx_summary,
            skill_ids=skill_ids,
            tool_ids=tool_ids,
        )
        generated_at = utc_now_iso()
        inspection_text = self._render_text(
            generated_at=generated_at,
            ocel_summary=ocel_summary,
            ocpx_summary=ocpx_summary,
            pig_summary=pig_summary,
            conformance_summary=conformance_summary,
            skill_summary=skill_summary,
            tool_summary=tool_summary,
            warnings=warnings,
        )
        return PISubstrateInspection(
            inspection_id=f"pi_substrate_inspection:{uuid4()}",
            generated_at=generated_at,
            ocel_summary=ocel_summary,
            ocpx_summary=ocpx_summary,
            pig_summary=pig_summary,
            skill_summary=skill_summary,
            tool_summary=tool_summary,
            conformance_summary=conformance_summary,
            warnings=warnings,
            inspection_text=inspection_text,
            inspection_attrs={"read_only": True, "limit": limit},
        )

    @staticmethod
    def _warnings(
        *,
        ocel_summary: dict[str, Any],
        ocpx_summary: dict[str, Any],
        skill_ids: list[str],
        tool_ids: list[str],
    ) -> list[str]:
        warnings: list[str] = []
        if int(ocel_summary.get("event_count") or 0) == 0:
            warnings.append("no events")
        if int(ocel_summary.get("object_count") or 0) == 0:
            warnings.append("no objects")
        coverage = float(
            (ocpx_summary.get("relation_coverage") or {}).get("coverage_ratio") or 0.0
        )
        if coverage < 1.0:
            warnings.append("relation coverage below 1.0")
        validation = ocel_summary.get("duplicate_relation_validation") or {}
        if validation.get("valid") is False:
            warnings.append("duplicate relations invalid")
        if not {"tool:ocel", "tool:ocpx", "tool:pig"}.issubset(set(tool_ids)):
            warnings.append("no internal PI tools registered")
        if not {
            "skill:inspect_ocel_recent",
            "skill:summarize_process_trace",
            "skill:check_self_conformance",
        }.issubset(set(skill_ids)):
            warnings.append("no built-in PI skills registered")
        return warnings

    @staticmethod
    def _render_text(
        *,
        generated_at: str,
        ocel_summary: dict[str, Any],
        ocpx_summary: dict[str, Any],
        pig_summary: dict[str, Any],
        conformance_summary: dict[str, Any],
        skill_summary: dict[str, Any],
        tool_summary: dict[str, Any],
        warnings: list[str],
    ) -> str:
        coverage = float(
            (ocpx_summary.get("relation_coverage") or {}).get("coverage_ratio") or 0.0
        )
        return "\n".join(
            [
                "ChantaCore PI Substrate Inspection",
                f"Generated at: {generated_at}",
                "",
                "OCEL:",
                f"- Events: {ocel_summary.get('event_count', 0)}",
                f"- Objects: {ocel_summary.get('object_count', 0)}",
                f"- Event-object relations: {ocel_summary.get('event_object_relation_count', 0)}",
                f"- Object-object relations: {ocel_summary.get('object_object_relation_count', 0)}",
                "",
                "OCPX:",
                f"- Recent activities: {PISubstrateInspector._sequence_text(ocpx_summary.get('activity_sequence') or [])}",
                f"- Relation coverage: {coverage * 100:.1f}%",
                "",
                "PIG:",
                f"- Recent report status: {pig_summary.get('recent_report_status')}",
                f"- Guidance count: {pig_summary.get('guidance_count', 0)}",
                "",
                "Conformance:",
                f"- Status: {conformance_summary.get('status')}",
                f"- Issues: {conformance_summary.get('issue_count', 0)}",
                "",
                "Skills:",
                f"- Built-in skills: {skill_summary.get('built_in_skill_count', 0)}",
                "",
                "Tools:",
                f"- Built-in tools: {tool_summary.get('built_in_tool_count', 0)}",
                "",
                "Warnings:",
                f"- {', '.join(warnings) if warnings else 'none'}",
            ]
        )

    @staticmethod
    def _sequence_text(activity_sequence: list[str], max_items: int = 12) -> str:
        if not activity_sequence:
            return "none"
        visible = activity_sequence[:max_items]
        suffix = " -> ..." if len(activity_sequence) > max_items else ""
        return f"{' -> '.join(visible)}{suffix}"

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.editing.patch_store import PatchApplicationStore
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.pig.queue_conformance import PIGQueueConformanceService
from chanta_core.pig.reports import PIGReportService
from chanta_core.scheduler.store import ProcessScheduleStore
from chanta_core.skills.registry import SkillRegistry
from chanta_core.tools.registry import ToolRegistry
from chanta_core.utility.time import utc_now_iso
from chanta_core.workers.store import ProcessJobStore


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
        queue_conformance_service: PIGQueueConformanceService | None = None,
        skill_registry: SkillRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
        process_job_store: ProcessJobStore | None = None,
        process_schedule_store: ProcessScheduleStore | None = None,
        patch_application_store: PatchApplicationStore | None = None,
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
        self.queue_conformance_service = (
            queue_conformance_service or PIGQueueConformanceService()
        )
        self.skill_registry = skill_registry or SkillRegistry()
        self.tool_registry = tool_registry or ToolRegistry()
        self.process_job_store = process_job_store or ProcessJobStore()
        self.process_schedule_store = process_schedule_store or ProcessScheduleStore()
        self.patch_application_store = patch_application_store or PatchApplicationStore()

    def inspect(self, limit: int = 50) -> PISubstrateInspection:
        view = self.ocpx_loader.load_recent_view(limit=limit)
        report = self.pig_report_service.build_recent_report(limit=limit)
        conformance = self.pig_conformance_service.check_view(view, scope="recent")
        queue_conformance = self.queue_conformance_service.check_recent_jobs(limit=limit)
        duplicate_validation = self.ocel_validator.validate_duplicate_relations()
        canonical_validation = self.ocel_validator.validate_canonical_model()
        export_readiness = self.ocel_validator.validate_export_readiness()
        ocel_summary = {
            "event_count": self.ocel_store.fetch_event_count(),
            "object_count": self.ocel_store.fetch_object_count(),
            "event_object_relation_count": self.ocel_store.fetch_event_object_relation_count(),
            "object_object_relation_count": self.ocel_store.fetch_object_object_relation_count(),
            "duplicate_relation_validation": duplicate_validation,
            "canonical_validation": canonical_validation,
            "export_readiness": export_readiness,
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
            "verification_summary": report.report_attrs.get("verification_summary", {}),
            "process_outcome_summary": report.report_attrs.get("process_outcome_summary", {}),
            "permission_summary": report.report_attrs.get("permission_summary", {}),
            "workspace_write_sandbox_summary": report.report_attrs.get("workspace_write_sandbox_summary", {}),
        }
        conformance_summary = {
            "status": conformance.status,
            "issue_count": len(conformance.issues),
            "queue_status": queue_conformance.status,
            "queue_issue_count": len(queue_conformance.issues),
        }
        skill_ids = [skill.skill_id for skill in self.skill_registry.list_skills()]
        tool_items = self.tool_registry.list_tools()
        tool_ids = [tool.tool_id for tool in tool_items]
        skill_summary = {"built_in_skill_count": len(skill_ids), "skill_ids": skill_ids}
        tool_summary = {
            "built_in_tool_count": len(tool_ids),
            "tool_ids": tool_ids,
            "safety_levels": {tool.tool_id: tool.safety_level for tool in tool_items},
        }
        worker_summary = self._worker_summary()
        scheduler_summary = self._scheduler_summary()
        patch_summary = self._patch_summary()
        warnings = self._warnings(
            ocel_summary=ocel_summary,
            ocpx_summary=ocpx_summary,
            skill_ids=skill_ids,
            tool_ids=tool_ids,
            worker_summary=worker_summary,
            scheduler_summary=scheduler_summary,
            patch_summary=patch_summary,
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
            worker_summary=worker_summary,
            scheduler_summary=scheduler_summary,
            patch_summary=patch_summary,
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
            inspection_attrs={
                "read_only": True,
                "limit": limit,
                "worker_summary": worker_summary,
                "scheduler_summary": scheduler_summary,
                "patch_summary": patch_summary,
                "verification_summary": pig_summary.get("verification_summary", {}),
                "process_outcome_summary": pig_summary.get("process_outcome_summary", {}),
                "permission_summary": pig_summary.get("permission_summary", {}),
                "workspace_write_sandbox_summary": pig_summary.get("workspace_write_sandbox_summary", {}),
            },
        )

    @staticmethod
    def _warnings(
        *,
        ocel_summary: dict[str, Any],
        ocpx_summary: dict[str, Any],
        skill_ids: list[str],
        tool_ids: list[str],
        worker_summary: dict[str, Any],
        scheduler_summary: dict[str, Any],
        patch_summary: dict[str, Any],
    ) -> list[str]:
        warnings: list[str] = []
        if int(ocel_summary.get("event_count") or 0) == 0:
            warnings.append("no OCEL events")
        if int(ocel_summary.get("object_count") or 0) == 0:
            warnings.append("no OCEL objects")
        coverage = float(
            (ocpx_summary.get("relation_coverage") or {}).get("coverage_ratio") or 0.0
        )
        if coverage < 1.0:
            warnings.append("relation coverage below 1.0")
        validation = ocel_summary.get("duplicate_relation_validation") or {}
        if validation.get("valid") is False:
            warnings.append("duplicate relation validation failed")
        required_tools = {
            "tool:ocel",
            "tool:ocpx",
            "tool:pig",
            "tool:workspace",
            "tool:repo",
            "tool:edit",
            "tool:worker",
            "tool:scheduler",
        }
        if not required_tools.issubset(set(tool_ids)):
            warnings.append("missing core internal tools")
        if not {
            "skill:inspect_ocel_recent",
            "skill:summarize_process_trace",
            "skill:check_self_conformance",
        }.issubset(set(skill_ids)):
            warnings.append("missing core built-in PI skills")
        if int((worker_summary.get("job_counts_by_status") or {}).get("failed", 0)) > 0:
            warnings.append("worker jobs failed")
        if int(scheduler_summary.get("due_count") or 0) > 0:
            warnings.append("schedule due but not enqueued")
        if int(patch_summary.get("failed_patch_count") or 0) > 0:
            warnings.append("patch failures detected")
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
        worker_summary: dict[str, Any],
        scheduler_summary: dict[str, Any],
        patch_summary: dict[str, Any],
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
                "OCEL Health:",
                f"- Events: {ocel_summary.get('event_count', 0)}",
                f"- Objects: {ocel_summary.get('object_count', 0)}",
                f"- Event-object relations: {ocel_summary.get('event_object_relation_count', 0)}",
                f"- Object-object relations: {ocel_summary.get('object_object_relation_count', 0)}",
                f"- Canonical model valid: {(ocel_summary.get('canonical_validation') or {}).get('valid')}",
                f"- Export readiness valid: {(ocel_summary.get('export_readiness') or {}).get('valid')}",
                "",
                "OCPX Health:",
                f"- Recent activities: {PISubstrateInspector._sequence_text(ocpx_summary.get('activity_sequence') or [])}",
                f"- Relation coverage: {coverage * 100:.1f}%",
                "",
                "PIG Health:",
                f"- Recent report status: {pig_summary.get('recent_report_status')}",
                f"- Guidance count: {pig_summary.get('guidance_count', 0)}",
                f"- Verification contracts: {(pig_summary.get('verification_summary') or {}).get('verification_contract_count', 0)}",
                f"- Verification results: {(pig_summary.get('verification_summary') or {}).get('verification_result_count', 0)}",
                f"- Outcome evaluations: {(pig_summary.get('process_outcome_summary') or {}).get('process_outcome_evaluation_count', 0)}",
                f"- Permission requests: {(pig_summary.get('permission_summary') or {}).get('permission_request_count', 0)}",
                f"- Session permission resolutions: {(pig_summary.get('permission_summary') or {}).get('session_permission_resolution_count', 0)}",
                f"- Workspace write sandbox decisions: {(pig_summary.get('workspace_write_sandbox_summary') or {}).get('workspace_write_sandbox_decision_count', 0)}",
                "",
                "Conformance:",
                f"- Process status: {conformance_summary.get('status')}",
                f"- Process issues: {conformance_summary.get('issue_count', 0)}",
                f"- Queue status: {conformance_summary.get('queue_status')}",
                f"- Queue issues: {conformance_summary.get('queue_issue_count', 0)}",
                "",
                "Skills:",
                f"- Built-in skills: {skill_summary.get('built_in_skill_count', 0)}",
                "",
                "Tools:",
                f"- Built-in tools: {tool_summary.get('built_in_tool_count', 0)}",
                "",
                "Worker Queue:",
                f"- Jobs: {worker_summary.get('job_count', 0)}",
                f"- Counts: {PISubstrateInspector._inline_counts(worker_summary.get('job_counts_by_status') or {})}",
                "",
                "Scheduler:",
                f"- Schedules: {scheduler_summary.get('schedule_count', 0)}",
                f"- Counts: {PISubstrateInspector._inline_counts(scheduler_summary.get('schedule_counts_by_status') or {})}",
                "",
                "Editing / Patch:",
                f"- Patch applications: {patch_summary.get('patch_application_count', 0)}",
                f"- Failed patches: {patch_summary.get('failed_patch_count', 0)}",
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

    @staticmethod
    def _inline_counts(counts: dict[str, int]) -> str:
        if not counts:
            return "none"
        return ", ".join(f"{key}={counts[key]}" for key in sorted(counts))

    def _worker_summary(self) -> dict[str, Any]:
        jobs = list(self.process_job_store._state_by_id().values())
        counts: dict[str, int] = {}
        for job in jobs:
            counts[job.status] = counts.get(job.status, 0) + 1
        return {"job_count": len(jobs), "job_counts_by_status": counts}

    def _scheduler_summary(self) -> dict[str, Any]:
        schedules = self.process_schedule_store.load_all()
        by_id = {item.schedule_id: item for item in schedules}
        counts: dict[str, int] = {}
        for schedule in by_id.values():
            counts[schedule.status] = counts.get(schedule.status, 0) + 1
        return {
            "schedule_count": len(by_id),
            "schedule_counts_by_status": counts,
            "due_count": 0,
        }

    def _patch_summary(self) -> dict[str, Any]:
        patches = self.patch_application_store.recent(50)
        return {
            "patch_application_count": len(patches),
            "failed_patch_count": sum(1 for item in patches if item.status == "failed"),
        }

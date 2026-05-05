from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.conformance import PIGConformanceService
from chanta_core.pig.guidance import PIGGuidanceService
from chanta_core.pig.queue_conformance import PIGQueueConformanceService
from chanta_core.pig.service import PIGService
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.editing.store import EditProposalStore
from chanta_core.editing.patch_store import PatchApplicationStore
from chanta_core.scheduler.store import ProcessScheduleStore
from chanta_core.workers.heartbeat import WorkerHeartbeatStore
from chanta_core.workers.store import ProcessJobStore
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

    def to_context_block(self, priority: int = 50):
        from chanta_core.context.block import from_process_report

        return from_process_report(self, priority=priority)


class PIGReportService:
    def __init__(
        self,
        *,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
        pig_service: PIGService | None = None,
        conformance_service: PIGConformanceService | None = None,
        guidance_service: PIGGuidanceService | None = None,
        queue_conformance_service: PIGQueueConformanceService | None = None,
        artifact_store: PIArtifactStore | None = None,
        edit_proposal_store: EditProposalStore | None = None,
        patch_application_store: PatchApplicationStore | None = None,
        process_job_store: ProcessJobStore | None = None,
        heartbeat_store: WorkerHeartbeatStore | None = None,
        process_schedule_store: ProcessScheduleStore | None = None,
    ) -> None:
        self.ocpx_loader = ocpx_loader or OCPXLoader()
        self.ocpx_engine = ocpx_engine or OCPXEngine()
        self.pig_service = pig_service or PIGService(loader=self.ocpx_loader)
        self.conformance_service = conformance_service or PIGConformanceService(
            ocpx_loader=self.ocpx_loader,
            ocpx_engine=self.ocpx_engine,
        )
        self.guidance_service = guidance_service or PIGGuidanceService()
        self.queue_conformance_service = (
            queue_conformance_service or PIGQueueConformanceService()
        )
        self.artifact_store = artifact_store or PIArtifactStore()
        self.edit_proposal_store = edit_proposal_store or EditProposalStore()
        self.patch_application_store = patch_application_store or PatchApplicationStore()
        self.process_job_store = process_job_store or ProcessJobStore()
        self.heartbeat_store = heartbeat_store or WorkerHeartbeatStore()
        self.process_schedule_store = process_schedule_store or ProcessScheduleStore()

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
        queue_conformance = self.queue_conformance_service.check_recent_jobs(limit=20).to_dict()
        editing_summary = self._editing_summary()
        worker_summary = self._worker_summary()
        scheduler_summary = self._scheduler_summary()
        pi_artifact_summary = self._pi_artifact_summary()
        memory_instruction_summary = self._memory_instruction_summary(
            object_type_counts,
            event_activity_counts,
        )
        hook_lifecycle_summary = self._hook_lifecycle_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        generated_at = utc_now_iso()
        report_text = self._render_report_text(
            report_id="pending",
            scope=scope,
            generated_at=generated_at,
            process_instance_id=process_instance_id or self._process_instance_id(view),
            session_id=session_id or view.session_id,
            activity_sequence=activity_sequence,
            event_activity_counts=event_activity_counts,
            object_type_counts=object_type_counts,
            relation_coverage=relation_coverage,
            variant_summary=variant_summary,
            performance_summary=performance_summary,
            conformance_report=conformance_report,
            queue_conformance=queue_conformance,
            decision_summary=decision_summary,
            guidance_summary=guidance_summary,
            skill_usage_summary=skill_usage_summary,
            tool_usage_summary=tool_usage_summary,
            editing_summary=editing_summary,
            worker_summary=worker_summary,
            scheduler_summary=scheduler_summary,
            pi_artifact_summary=pi_artifact_summary,
            memory_instruction_summary=memory_instruction_summary,
            hook_lifecycle_summary=hook_lifecycle_summary,
        )
        report_id = f"pig_report:{uuid4()}"
        report_text = report_text.replace("Report ID: pending", f"Report ID: {report_id}")
        return ProcessRunReport(
            report_id=report_id,
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
                "queue_conformance": queue_conformance,
                "editing_summary": editing_summary,
                "worker_summary": worker_summary,
                "scheduler_summary": scheduler_summary,
                "pi_artifact_summary": pi_artifact_summary,
                "memory_instruction_summary": memory_instruction_summary,
                "hook_lifecycle_summary": hook_lifecycle_summary,
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
        report_id: str,
        scope: str,
        generated_at: str,
        process_instance_id: str | None,
        session_id: str | None,
        activity_sequence: list[str],
        event_activity_counts: dict[str, int],
        object_type_counts: dict[str, int],
        relation_coverage: dict[str, Any],
        variant_summary: dict[str, Any],
        performance_summary: dict[str, Any],
        conformance_report: dict[str, Any] | None,
        queue_conformance: dict[str, Any] | None,
        decision_summary: dict[str, Any] | None,
        guidance_summary: dict[str, Any] | None,
        skill_usage_summary: dict[str, Any] | None,
        tool_usage_summary: dict[str, Any] | None,
        editing_summary: dict[str, Any] | None,
        worker_summary: dict[str, Any] | None,
        scheduler_summary: dict[str, Any] | None,
        pi_artifact_summary: dict[str, Any] | None,
        memory_instruction_summary: dict[str, Any] | None,
        hook_lifecycle_summary: dict[str, Any] | None,
    ) -> str:
        conformance_issues = (
            len(conformance_report.get("issues") or []) if conformance_report else 0
        )
        queue_issues = len((queue_conformance or {}).get("issues") or [])
        relation_ratio = float(relation_coverage.get("coverage_ratio") or 0.0)
        important_object_counts = {
            key: object_type_counts.get(key, 0)
            for key in [
                "process_instance",
                "skill",
                "tool",
                "tool_request",
                "tool_result",
                "process_job",
                "process_schedule",
                "edit_proposal",
                "patch_application",
                "error",
            ]
        }
        skill_lines = PIGReportService._count_lines(
            (skill_usage_summary or {}).get("executed_skills") or {}
        )
        tool_lines = PIGReportService._count_lines(
            (tool_usage_summary or {}).get("tools") or {}
        )
        return "\n".join(
            [
                "ChantaCore PI Report",
                f"Report ID: {report_id}",
                f"Scope: {scope}",
                f"Generated at: {generated_at}",
                f"Process instance: {process_instance_id or 'unknown'}",
                f"Session: {session_id or 'unknown'}",
                "",
                "Trace:",
                f"- {PIGReportService._sequence_text(activity_sequence)}",
                f"- Event count: {len(activity_sequence)}",
                f"- Top event activities: {PIGReportService._top_counts_text(event_activity_counts)}",
                "",
                "Objects:",
                f"- Total objects: {sum(object_type_counts.values())}",
                f"- Important object types: {PIGReportService._inline_counts(important_object_counts)}",
                "",
                "Relation:",
                f"- Relation coverage: {relation_ratio * 100:.1f}%",
                f"- Events without related objects: {relation_coverage.get('events_without_related_objects', 0)}",
                "",
                "Variant:",
                f"- Key: {variant_summary.get('variant_key') or 'none'}",
                f"- Success count: {variant_summary.get('success_count', 0)}",
                f"- Failure count: {variant_summary.get('failure_count', 0)}",
                f"- Trace count: {variant_summary.get('trace_count', 'unknown')}",
                "",
                "Performance Precursor:",
                f"- Duration seconds: {performance_summary.get('duration_seconds')}",
                f"- LLM calls: {performance_summary.get('llm_call_count', 0)}",
                f"- Skill executions: {performance_summary.get('skill_execution_count', 0)}",
                f"- Tool operations: {(tool_usage_summary or {}).get('tool_operation_count', 0)}",
                f"- Failures: {performance_summary.get('failure_count', 0)}",
                "",
                "Conformance:",
                f"- Process status: {(conformance_report or {}).get('status', 'unknown')}",
                f"- Process issues: {conformance_issues}",
                f"- Queue status: {(queue_conformance or {}).get('status', 'unknown')}",
                f"- Queue issues: {queue_issues}",
                "",
                "Guidance / Decision:",
                f"- Active guidance: {(guidance_summary or {}).get('active_guidance_count', 0)}",
                f"- Top suggested skill: {(guidance_summary or {}).get('top_suggested_skill') or 'none'}",
                f"- Decision events: {(decision_summary or {}).get('decision_event_count', 0)}",
                f"- Fallback count: {(decision_summary or {}).get('fallback_count', 0)}",
                f"- Tie-break count: {(decision_summary or {}).get('tie_break_count', 0)}",
                "",
                "Skill Usage:",
                skill_lines,
                "",
                "Tool Usage:",
                tool_lines,
                f"- Failed tool operations: {(tool_usage_summary or {}).get('failed_tool_operation_count', 0)}",
                "",
                "Editing / Patch:",
                f"- Proposals: {(editing_summary or {}).get('proposal_count', 0)}",
                f"- Patch applications: {(editing_summary or {}).get('patch_application_count', 0)}",
                f"- Failed patches: {(editing_summary or {}).get('failed_patch_count', 0)}",
                f"- Approved/applied patches: {(editing_summary or {}).get('applied_patch_count', 0)}",
                "",
                "Worker / Scheduler:",
                f"- Job counts: {PIGReportService._inline_counts((worker_summary or {}).get('job_counts_by_status') or {})}",
                f"- Heartbeats: {(worker_summary or {}).get('heartbeat_count', 0)}",
                f"- Schedule counts: {PIGReportService._inline_counts((scheduler_summary or {}).get('schedule_counts_by_status') or {})}",
                "",
                "Human / External PI:",
                f"- Artifact count: {(pi_artifact_summary or {}).get('artifact_count', 0)}",
                f"- Recent artifacts: {PIGReportService._recent_artifacts_text((pi_artifact_summary or {}).get('recent_artifacts') or [])}",
                "- Reminder: PI artifacts are advisory.",
                "",
                "Memory / Instruction Substrate:",
                f"- Memory entries: {(memory_instruction_summary or {}).get('memory_entry_count', 0)}",
                f"- Memory revisions: {(memory_instruction_summary or {}).get('memory_revision_count', 0)}",
                f"- Instruction artifacts: {(memory_instruction_summary or {}).get('instruction_artifact_count', 0)}",
                f"- Project rules: {(memory_instruction_summary or {}).get('project_rule_count', 0)}",
                f"- User preferences: {(memory_instruction_summary or {}).get('user_preference_count', 0)}",
                f"- Memory events: {(memory_instruction_summary or {}).get('memory_event_count', 0)}",
                f"- Instruction events: {(memory_instruction_summary or {}).get('instruction_event_count', 0)}",
                "",
                "Hook Lifecycle Observability:",
                f"- Hook definitions: {(hook_lifecycle_summary or {}).get('hook_definition_count', 0)}",
                f"- Hook invocations: {(hook_lifecycle_summary or {}).get('hook_invocation_count', 0)}",
                f"- Hook results: {(hook_lifecycle_summary or {}).get('hook_result_count', 0)}",
                f"- Hook policies: {(hook_lifecycle_summary or {}).get('hook_policy_count', 0)}",
                f"- Hook invoked events: {(hook_lifecycle_summary or {}).get('hook_invoked_count', 0)}",
                f"- Hook completed events: {(hook_lifecycle_summary or {}).get('hook_completed_count', 0)}",
                f"- Hook failed events: {(hook_lifecycle_summary or {}).get('hook_failed_count', 0)}",
                f"- Hook skipped events: {(hook_lifecycle_summary or {}).get('hook_skipped_count', 0)}",
                f"- Hook invocations by stage: {PIGReportService._inline_counts((hook_lifecycle_summary or {}).get('hook_invocation_by_stage') or {})}",
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
    def _inline_counts(counts: dict[str, int]) -> str:
        visible = {key: value for key, value in counts.items() if value}
        if not visible:
            return "none"
        return ", ".join(f"{key}={visible[key]}" for key in sorted(visible))

    @staticmethod
    def _top_counts_text(counts: dict[str, int], limit: int = 5) -> str:
        if not counts:
            return "none"
        top = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
        return ", ".join(f"{key}={value}" for key, value in top)

    @staticmethod
    def _recent_artifacts_text(items: list[dict[str, Any]]) -> str:
        if not items:
            return "none"
        return ", ".join(
            str(item.get("title") or item.get("artifact_type") or item.get("artifact_id"))
            for item in items[:3]
        )

    def _editing_summary(self) -> dict[str, Any]:
        proposals = self.edit_proposal_store.recent(50)
        patches = self.patch_application_store.recent(50)
        return {
            "proposal_count": len(proposals),
            "patch_application_count": len(patches),
            "failed_patch_count": sum(1 for item in patches if item.status == "failed"),
            "applied_patch_count": sum(1 for item in patches if item.status == "applied"),
            "proposal_targets": sorted({item.target_path for item in proposals})[:10],
        }

    def _worker_summary(self) -> dict[str, Any]:
        jobs = list(self.process_job_store._state_by_id().values())
        counts: dict[str, int] = {}
        for job in jobs:
            counts[job.status] = counts.get(job.status, 0) + 1
        return {
            "job_count": len(jobs),
            "job_counts_by_status": counts,
            "heartbeat_count": len(self.heartbeat_store.recent(50)),
        }

    def _scheduler_summary(self) -> dict[str, Any]:
        schedules = self.process_schedule_store.load_all()
        by_id = {item.schedule_id: item for item in schedules}
        counts: dict[str, int] = {}
        for schedule in by_id.values():
            counts[schedule.status] = counts.get(schedule.status, 0) + 1
        return {
            "schedule_count": len(by_id),
            "schedule_counts_by_status": counts,
        }

    def _pi_artifact_summary(self) -> dict[str, Any]:
        artifacts = self.artifact_store.recent(20)
        return {
            "artifact_count": len(artifacts),
            "recent_artifacts": [
                {
                    "artifact_id": item.artifact_id,
                    "artifact_type": item.artifact_type,
                    "title": item.title,
                }
                for item in artifacts[:5]
            ],
        }

    @staticmethod
    def _memory_instruction_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
    ) -> dict[str, Any]:
        memory_events = {
            "memory_entry_created",
            "memory_entry_revised",
            "memory_entry_superseded",
            "memory_entry_archived",
            "memory_entry_withdrawn",
            "memory_revision_recorded",
            "memory_derived_from_message",
            "memory_attached_to_session",
            "memory_attached_to_turn",
        }
        instruction_events = {
            "instruction_artifact_registered",
            "instruction_artifact_revised",
            "instruction_artifact_deprecated",
            "project_rule_registered",
            "project_rule_revised",
            "user_preference_registered",
            "user_preference_revised",
        }
        return {
            "memory_entry_count": object_type_counts.get("memory_entry", 0),
            "memory_revision_count": object_type_counts.get("memory_revision", 0),
            "instruction_artifact_count": object_type_counts.get("instruction_artifact", 0),
            "project_rule_count": object_type_counts.get("project_rule", 0),
            "user_preference_count": object_type_counts.get("user_preference", 0),
            "memory_event_count": sum(
                event_activity_counts.get(activity, 0) for activity in memory_events
            ),
            "instruction_event_count": sum(
                event_activity_counts.get(activity, 0)
                for activity in instruction_events
            ),
        }

    @staticmethod
    def _hook_lifecycle_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_stage: dict[str, int] = {}
        for event in view.events:
            if event.event_activity != "hook_invoked":
                continue
            stage = str(event.event_attrs.get("lifecycle_stage") or "other")
            by_stage[stage] = by_stage.get(stage, 0) + 1
        return {
            "hook_definition_count": object_type_counts.get("hook_definition", 0),
            "hook_invocation_count": object_type_counts.get("hook_invocation", 0),
            "hook_result_count": object_type_counts.get("hook_result", 0),
            "hook_policy_count": object_type_counts.get("hook_policy", 0),
            "hook_invoked_count": event_activity_counts.get("hook_invoked", 0),
            "hook_completed_count": event_activity_counts.get("hook_completed", 0),
            "hook_failed_count": event_activity_counts.get("hook_failed", 0),
            "hook_skipped_count": event_activity_counts.get("hook_skipped", 0),
            "hook_result_recorded_count": event_activity_counts.get("hook_result_recorded", 0),
            "hook_invocation_by_stage": by_stage,
        }

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

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
        session_continuity_summary = self._session_continuity_summary(
            object_type_counts,
            event_activity_counts,
        )
        session_context_projection_summary = self._session_context_projection_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        capability_decision_summary = self._capability_decision_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        persona_summary = self._persona_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        personal_runtime_workbench_summary = self._personal_runtime_workbench_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        tool_registry_summary = self._tool_registry_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        verification_summary = self._verification_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        outcome_summary = self._process_outcome_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        permission_summary = self._permission_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        workspace_write_sandbox_summary = self._workspace_write_sandbox_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        workspace_read_summary = self._workspace_read_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        shell_network_pre_sandbox_summary = self._shell_network_pre_sandbox_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        delegation_summary = self._delegation_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        sidechain_summary = self._sidechain_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        delegation_conformance_summary = self._delegation_conformance_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        external_capability_summary = self._external_capability_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_digest_summary = self._observation_digest_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        skill_registry_summary = self._skill_registry_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_digest_proposal_summary = self._observation_digest_proposal_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_digest_invocation_summary = self._observation_digest_invocation_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_digest_conformance_summary = self._observation_digest_conformance_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        external_skill_static_digestion_summary = self._external_skill_static_digestion_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        agent_observation_spine_summary = self._agent_observation_spine_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        cross_harness_trace_adapter_summary = self._cross_harness_trace_adapter_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_to_digestion_adapter_summary = self._observation_to_digestion_adapter_summary(
            object_type_counts,
            event_activity_counts,
            view,
        )
        observation_digestion_ecosystem_summary = self._observation_digestion_ecosystem_summary(
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
            session_continuity_summary=session_continuity_summary,
            session_context_projection_summary=session_context_projection_summary,
            capability_decision_summary=capability_decision_summary,
            persona_summary=persona_summary,
            personal_runtime_workbench_summary=personal_runtime_workbench_summary,
            tool_registry_summary=tool_registry_summary,
            verification_summary=verification_summary,
            outcome_summary=outcome_summary,
            permission_summary=permission_summary,
            workspace_write_sandbox_summary=workspace_write_sandbox_summary,
            workspace_read_summary=workspace_read_summary,
            shell_network_pre_sandbox_summary=shell_network_pre_sandbox_summary,
            delegation_summary=delegation_summary,
            sidechain_summary=sidechain_summary,
            delegation_conformance_summary=delegation_conformance_summary,
            external_capability_summary=external_capability_summary,
            observation_digest_summary=observation_digest_summary,
            skill_registry_summary=skill_registry_summary,
            observation_digest_proposal_summary=observation_digest_proposal_summary,
            observation_digest_invocation_summary=observation_digest_invocation_summary,
            observation_digest_conformance_summary=observation_digest_conformance_summary,
            external_skill_static_digestion_summary=external_skill_static_digestion_summary,
            agent_observation_spine_summary=agent_observation_spine_summary,
            cross_harness_trace_adapter_summary=cross_harness_trace_adapter_summary,
            observation_to_digestion_adapter_summary=observation_to_digestion_adapter_summary,
            observation_digestion_ecosystem_summary=observation_digestion_ecosystem_summary,
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
                "session_continuity_summary": session_continuity_summary,
                "session_context_projection_summary": session_context_projection_summary,
                "capability_decision_summary": capability_decision_summary,
                "persona_summary": persona_summary,
                "personal_runtime_workbench_summary": personal_runtime_workbench_summary,
                "tool_registry_summary": tool_registry_summary,
                "verification_summary": verification_summary,
                "process_outcome_summary": outcome_summary,
                "permission_summary": permission_summary,
                "workspace_write_sandbox_summary": workspace_write_sandbox_summary,
                "workspace_read_summary": workspace_read_summary,
                "shell_network_pre_sandbox_summary": shell_network_pre_sandbox_summary,
                "delegation_summary": delegation_summary,
                "sidechain_summary": sidechain_summary,
                "delegation_conformance_summary": delegation_conformance_summary,
                "external_capability_summary": external_capability_summary,
                "observation_digest_summary": observation_digest_summary,
                "skill_registry_summary": skill_registry_summary,
                "observation_digest_proposal_summary": observation_digest_proposal_summary,
                "observation_digest_invocation_summary": observation_digest_invocation_summary,
                "observation_digest_conformance_summary": observation_digest_conformance_summary,
                "external_skill_static_digestion_summary": external_skill_static_digestion_summary,
                "agent_observation_spine_summary": agent_observation_spine_summary,
                "cross_harness_trace_adapter_summary": cross_harness_trace_adapter_summary,
                "observation_to_digestion_adapter_summary": observation_to_digestion_adapter_summary,
                "observation_digestion_ecosystem_summary": observation_digestion_ecosystem_summary,
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
        explicit_by_skill_id: dict[str, int] = {}
        explicit_violation_by_type: dict[str, int] = {}
        proposal_by_skill_id: dict[str, int] = {}
        proposal_by_requested_operation: dict[str, int] = {}
        review_by_skill_id: dict[str, int] = {}
        review_by_decision: dict[str, int] = {}
        bridge_by_skill_id: dict[str, int] = {}
        bridge_violation_by_type: dict[str, int] = {}
        gate_by_skill_id: dict[str, int] = {}
        gate_finding_by_type: dict[str, int] = {}
        onboarding_by_capability_category: dict[str, int] = {}
        onboarding_by_risk_class: dict[str, int] = {}
        onboarding_finding_by_type: dict[str, int] = {}
        execution_by_kind: dict[str, int] = {}
        execution_by_skill_id: dict[str, int] = {}
        failed_skill_execution_count = 0
        explicit_completed_count = 0
        explicit_denied_count = 0
        explicit_unsupported_count = 0
        explicit_failed_count = 0
        proposal_available_count = 0
        proposal_incomplete_count = 0
        proposal_unsupported_count = 0
        proposal_needs_review_count = 0
        review_approved_count = 0
        review_rejected_count = 0
        review_no_action_count = 0
        review_needs_more_input_count = 0
        review_bridge_candidate_count = 0
        bridge_allowed_count = 0
        bridge_denied_count = 0
        bridge_executed_count = 0
        bridge_blocked_count = 0
        bridge_needs_more_input_count = 0
        bridge_unsupported_count = 0
        gate_allowed_count = 0
        gate_denied_count = 0
        gate_needs_review_count = 0
        gate_unsupported_count = 0
        gate_executed_count = 0
        gate_blocked_count = 0
        onboarding_accepted_count = 0
        onboarding_rejected_count = 0
        onboarding_needs_fix_count = 0
        onboarding_blocked_count = 0
        execution_completed_count = 0
        execution_blocked_count = 0
        execution_failed_count = 0
        execution_skipped_count = 0
        execution_with_gate_count = 0
        execution_without_gate_count = 0
        execution_full_input_stored_count = 0
        execution_full_output_stored_count = 0
        execution_audit_not_found_count = 0
        execution_audit_empty_count = 0
        execution_audit_blocked_view_count = 0
        execution_audit_failed_view_count = 0
        execution_audit_by_query_type: dict[str, int] = {}
        promotion_pending_review_count = 0
        promotion_approved_for_later_count = 0
        promotion_rejected_count = 0
        promotion_no_action_count = 0
        promotion_private_risk_count = 0
        promotion_by_target_kind: dict[str, int] = {}
        object_type_counts: dict[str, int] = {}
        for item in view.objects:
            object_type_counts[item.object_type] = object_type_counts.get(item.object_type, 0) + 1
            if item.object_type == "explicit_skill_invocation_request":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                explicit_by_skill_id[skill_id] = explicit_by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "explicit_skill_invocation_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "completed":
                    explicit_completed_count += 1
                if status == "denied":
                    explicit_denied_count += 1
                if status == "unsupported":
                    explicit_unsupported_count += 1
                if status in {"failed", "error"}:
                    explicit_failed_count += 1
            if item.object_type == "explicit_skill_invocation_violation":
                violation_type = str(item.object_attrs.get("violation_type") or "unknown")
                explicit_violation_by_type[violation_type] = (
                    explicit_violation_by_type.get(violation_type, 0) + 1
                )
            if item.object_type == "skill_proposal_intent":
                operation = str(item.object_attrs.get("requested_operation") or "unknown")
                proposal_by_requested_operation[operation] = (
                    proposal_by_requested_operation.get(operation, 0) + 1
                )
            if item.object_type == "skill_invocation_proposal":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                proposal_by_skill_id[skill_id] = proposal_by_skill_id.get(skill_id, 0) + 1
                status = str(item.object_attrs.get("proposal_status") or "")
                if status == "proposed":
                    proposal_available_count += 1
                if status == "incomplete":
                    proposal_incomplete_count += 1
                if status == "unsupported":
                    proposal_unsupported_count += 1
                if status == "needs_review":
                    proposal_needs_review_count += 1
            if item.object_type == "skill_proposal_review_request":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                review_by_skill_id[skill_id] = review_by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "skill_proposal_review_decision":
                decision = str(item.object_attrs.get("decision") or "unknown")
                review_by_decision[decision] = review_by_decision.get(decision, 0) + 1
            if item.object_type == "skill_proposal_review_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "approved":
                    review_approved_count += 1
                if status == "rejected":
                    review_rejected_count += 1
                if status == "no_action":
                    review_no_action_count += 1
                if status == "needs_more_input":
                    review_needs_more_input_count += 1
                if bool(item.object_attrs.get("bridge_candidate")):
                    review_bridge_candidate_count += 1
            if item.object_type == "reviewed_execution_bridge_request":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                bridge_by_skill_id[skill_id] = bridge_by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "reviewed_execution_bridge_decision":
                decision = str(item.object_attrs.get("decision") or "")
                if decision == "allow":
                    bridge_allowed_count += 1
                if decision == "deny":
                    bridge_denied_count += 1
                if decision == "needs_more_input":
                    bridge_needs_more_input_count += 1
                if decision == "unsupported":
                    bridge_unsupported_count += 1
            if item.object_type == "reviewed_execution_bridge_result":
                if bool(item.object_attrs.get("executed")):
                    bridge_executed_count += 1
                if bool(item.object_attrs.get("blocked")):
                    bridge_blocked_count += 1
            if item.object_type == "reviewed_execution_bridge_violation":
                violation_type = str(item.object_attrs.get("violation_type") or "unknown")
                bridge_violation_by_type[violation_type] = (
                    bridge_violation_by_type.get(violation_type, 0) + 1
                )
            if item.object_type == "skill_execution_gate_request":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                gate_by_skill_id[skill_id] = gate_by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "skill_execution_gate_decision":
                decision = str(item.object_attrs.get("decision") or "")
                if decision == "allow":
                    gate_allowed_count += 1
                if decision == "deny":
                    gate_denied_count += 1
                if decision == "needs_review":
                    gate_needs_review_count += 1
                if decision == "unsupported":
                    gate_unsupported_count += 1
            if item.object_type == "skill_execution_gate_result":
                if bool(item.object_attrs.get("executed")):
                    gate_executed_count += 1
                if bool(item.object_attrs.get("blocked")):
                    gate_blocked_count += 1
            if item.object_type == "skill_execution_gate_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                gate_finding_by_type[finding_type] = gate_finding_by_type.get(finding_type, 0) + 1
            if item.object_type == "internal_skill_descriptor":
                category = str(item.object_attrs.get("capability_category") or "unknown")
                risk_class = str(item.object_attrs.get("risk_class") or "unknown")
                onboarding_by_capability_category[category] = (
                    onboarding_by_capability_category.get(category, 0) + 1
                )
                onboarding_by_risk_class[risk_class] = onboarding_by_risk_class.get(risk_class, 0) + 1
            if item.object_type == "internal_skill_onboarding_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                onboarding_finding_by_type[finding_type] = (
                    onboarding_finding_by_type.get(finding_type, 0) + 1
                )
            if item.object_type == "internal_skill_onboarding_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "accepted":
                    onboarding_accepted_count += 1
                if status == "rejected":
                    onboarding_rejected_count += 1
                if status == "needs_fix":
                    onboarding_needs_fix_count += 1
                if status == "blocked":
                    onboarding_blocked_count += 1
            if item.object_type == "execution_envelope":
                kind = str(item.object_attrs.get("execution_kind") or "unknown")
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                status = str(item.object_attrs.get("status") or "")
                execution_by_kind[kind] = execution_by_kind.get(kind, 0) + 1
                execution_by_skill_id[skill_id] = execution_by_skill_id.get(skill_id, 0) + 1
                if status == "completed":
                    execution_completed_count += 1
                if status in {"blocked", "denied", "unsupported", "needs_review"}:
                    execution_blocked_count += 1
                if status in {"failed", "error"}:
                    execution_failed_count += 1
                if status == "skipped":
                    execution_skipped_count += 1
            if item.object_type == "execution_provenance_record":
                if item.object_attrs.get("gate_result_id"):
                    execution_with_gate_count += 1
                else:
                    execution_without_gate_count += 1
            if item.object_type == "execution_input_snapshot" and bool(
                item.object_attrs.get("full_input_stored")
            ):
                execution_full_input_stored_count += 1
            if item.object_type == "execution_output_snapshot" and bool(
                item.object_attrs.get("full_output_stored")
            ):
                execution_full_output_stored_count += 1
            if item.object_type == "execution_audit_query":
                query_type = str(item.object_attrs.get("query_type") or "unknown")
                execution_audit_by_query_type[query_type] = (
                    execution_audit_by_query_type.get(query_type, 0) + 1
                )
            if item.object_type == "execution_audit_record_view":
                if bool(item.object_attrs.get("blocked")):
                    execution_audit_blocked_view_count += 1
                if str(item.object_attrs.get("status") or "") in {"failed", "error"}:
                    execution_audit_failed_view_count += 1
            if item.object_type == "execution_audit_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "not_found":
                    execution_audit_not_found_count += 1
                if status == "empty":
                    execution_audit_empty_count += 1
            if item.object_type == "execution_result_promotion_candidate":
                target_kind = str(item.object_attrs.get("target_kind") or "unknown")
                promotion_by_target_kind[target_kind] = (
                    promotion_by_target_kind.get(target_kind, 0) + 1
                )
                if str(item.object_attrs.get("review_status") or "") == "pending_review":
                    promotion_pending_review_count += 1
            if item.object_type == "execution_result_promotion_decision":
                decision = str(item.object_attrs.get("decision") or "")
                if decision == "approved_for_later_promotion":
                    promotion_approved_for_later_count += 1
                if decision == "rejected":
                    promotion_rejected_count += 1
                if decision == "no_action":
                    promotion_no_action_count += 1
            if item.object_type == "execution_result_promotion_finding":
                if str(item.object_attrs.get("finding_type") or "") == "private_content_risk":
                    promotion_private_risk_count += 1
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
            "explicit_skill_invocation_request_count": object_type_counts.get(
                "explicit_skill_invocation_request", 0
            ),
            "explicit_skill_invocation_input_count": object_type_counts.get(
                "explicit_skill_invocation_input", 0
            ),
            "explicit_skill_invocation_decision_count": object_type_counts.get(
                "explicit_skill_invocation_decision", 0
            ),
            "explicit_skill_invocation_result_count": object_type_counts.get(
                "explicit_skill_invocation_result", 0
            ),
            "explicit_skill_invocation_violation_count": object_type_counts.get(
                "explicit_skill_invocation_violation", 0
            ),
            "explicit_skill_invocation_completed_count": explicit_completed_count,
            "explicit_skill_invocation_denied_count": explicit_denied_count,
            "explicit_skill_invocation_unsupported_count": explicit_unsupported_count,
            "explicit_skill_invocation_failed_count": explicit_failed_count,
            "explicit_skill_invocation_by_skill_id": explicit_by_skill_id,
            "explicit_skill_invocation_violation_by_type": explicit_violation_by_type,
            "skill_proposal_intent_count": object_type_counts.get("skill_proposal_intent", 0),
            "skill_proposal_requirement_count": object_type_counts.get(
                "skill_proposal_requirement", 0
            ),
            "skill_invocation_proposal_count": object_type_counts.get(
                "skill_invocation_proposal", 0
            ),
            "skill_proposal_decision_count": object_type_counts.get(
                "skill_proposal_decision", 0
            ),
            "skill_proposal_review_note_count": object_type_counts.get(
                "skill_proposal_review_note", 0
            ),
            "skill_proposal_result_count": object_type_counts.get("skill_proposal_result", 0),
            "skill_proposal_available_count": proposal_available_count,
            "skill_proposal_incomplete_count": proposal_incomplete_count,
            "skill_proposal_unsupported_count": proposal_unsupported_count,
            "skill_proposal_needs_review_count": proposal_needs_review_count,
            "skill_proposal_by_skill_id": proposal_by_skill_id,
            "skill_proposal_by_requested_operation": proposal_by_requested_operation,
            "skill_proposal_review_contract_count": object_type_counts.get(
                "skill_proposal_review_contract", 0
            ),
            "skill_proposal_review_request_count": object_type_counts.get(
                "skill_proposal_review_request", 0
            ),
            "skill_proposal_review_decision_count": object_type_counts.get(
                "skill_proposal_review_decision", 0
            ),
            "skill_proposal_review_finding_count": object_type_counts.get(
                "skill_proposal_review_finding", 0
            ),
            "skill_proposal_review_result_count": object_type_counts.get(
                "skill_proposal_review_result", 0
            ),
            "skill_proposal_review_approved_count": review_approved_count,
            "skill_proposal_review_rejected_count": review_rejected_count,
            "skill_proposal_review_no_action_count": review_no_action_count,
            "skill_proposal_review_needs_more_input_count": review_needs_more_input_count,
            "skill_proposal_review_bridge_candidate_count": review_bridge_candidate_count,
            "skill_proposal_review_by_skill_id": review_by_skill_id,
            "skill_proposal_review_by_decision": review_by_decision,
            "reviewed_execution_bridge_request_count": object_type_counts.get(
                "reviewed_execution_bridge_request", 0
            ),
            "reviewed_execution_bridge_decision_count": object_type_counts.get(
                "reviewed_execution_bridge_decision", 0
            ),
            "reviewed_execution_bridge_result_count": object_type_counts.get(
                "reviewed_execution_bridge_result", 0
            ),
            "reviewed_execution_bridge_violation_count": object_type_counts.get(
                "reviewed_execution_bridge_violation", 0
            ),
            "reviewed_execution_bridge_allowed_count": bridge_allowed_count,
            "reviewed_execution_bridge_denied_count": bridge_denied_count,
            "reviewed_execution_bridge_executed_count": bridge_executed_count,
            "reviewed_execution_bridge_blocked_count": bridge_blocked_count,
            "reviewed_execution_bridge_needs_more_input_count": bridge_needs_more_input_count,
            "reviewed_execution_bridge_unsupported_count": bridge_unsupported_count,
            "reviewed_execution_bridge_by_skill_id": bridge_by_skill_id,
            "reviewed_execution_bridge_violation_by_type": bridge_violation_by_type,
            "skill_execution_gate_request_count": object_type_counts.get(
                "skill_execution_gate_request", 0
            ),
            "skill_execution_gate_decision_count": object_type_counts.get(
                "skill_execution_gate_decision", 0
            ),
            "skill_execution_gate_finding_count": object_type_counts.get(
                "skill_execution_gate_finding", 0
            ),
            "skill_execution_gate_result_count": object_type_counts.get(
                "skill_execution_gate_result", 0
            ),
            "skill_execution_gate_allowed_count": gate_allowed_count,
            "skill_execution_gate_denied_count": gate_denied_count,
            "skill_execution_gate_needs_review_count": gate_needs_review_count,
            "skill_execution_gate_unsupported_count": gate_unsupported_count,
            "skill_execution_gate_executed_count": gate_executed_count,
            "skill_execution_gate_blocked_count": gate_blocked_count,
            "skill_execution_gate_by_skill_id": gate_by_skill_id,
            "skill_execution_gate_finding_by_type": gate_finding_by_type,
            "internal_skill_descriptor_count": object_type_counts.get("internal_skill_descriptor", 0),
            "internal_skill_input_contract_count": object_type_counts.get(
                "internal_skill_input_contract", 0
            ),
            "internal_skill_output_contract_count": object_type_counts.get(
                "internal_skill_output_contract", 0
            ),
            "internal_skill_risk_profile_count": object_type_counts.get(
                "internal_skill_risk_profile", 0
            ),
            "internal_skill_gate_contract_count": object_type_counts.get(
                "internal_skill_gate_contract", 0
            ),
            "internal_skill_observability_contract_count": object_type_counts.get(
                "internal_skill_observability_contract", 0
            ),
            "internal_skill_onboarding_review_count": object_type_counts.get(
                "internal_skill_onboarding_review", 0
            ),
            "internal_skill_onboarding_finding_count": object_type_counts.get(
                "internal_skill_onboarding_finding", 0
            ),
            "internal_skill_onboarding_result_count": object_type_counts.get(
                "internal_skill_onboarding_result", 0
            ),
            "internal_skill_onboarding_accepted_count": onboarding_accepted_count,
            "internal_skill_onboarding_rejected_count": onboarding_rejected_count,
            "internal_skill_onboarding_needs_fix_count": onboarding_needs_fix_count,
            "internal_skill_onboarding_blocked_count": onboarding_blocked_count,
            "internal_skill_onboarding_by_capability_category": onboarding_by_capability_category,
            "internal_skill_onboarding_by_risk_class": onboarding_by_risk_class,
            "internal_skill_onboarding_finding_by_type": onboarding_finding_by_type,
            "execution_envelope_count": object_type_counts.get("execution_envelope", 0),
            "execution_provenance_record_count": object_type_counts.get(
                "execution_provenance_record", 0
            ),
            "execution_input_snapshot_count": object_type_counts.get("execution_input_snapshot", 0),
            "execution_output_snapshot_count": object_type_counts.get("execution_output_snapshot", 0),
            "execution_artifact_ref_count": object_type_counts.get("execution_artifact_ref", 0),
            "execution_outcome_summary_count": object_type_counts.get("execution_outcome_summary", 0),
            "execution_completed_count": execution_completed_count,
            "execution_blocked_count": execution_blocked_count,
            "execution_failed_count": execution_failed_count,
            "execution_skipped_count": execution_skipped_count,
            "execution_by_kind": execution_by_kind,
            "execution_by_skill_id": execution_by_skill_id,
            "execution_with_gate_count": execution_with_gate_count,
            "execution_without_gate_count": execution_without_gate_count,
            "execution_full_input_stored_count": execution_full_input_stored_count,
            "execution_full_output_stored_count": execution_full_output_stored_count,
            "execution_audit_query_count": object_type_counts.get("execution_audit_query", 0),
            "execution_audit_filter_count": object_type_counts.get("execution_audit_filter", 0),
            "execution_audit_record_view_count": object_type_counts.get(
                "execution_audit_record_view", 0
            ),
            "execution_audit_result_count": object_type_counts.get("execution_audit_result", 0),
            "execution_audit_finding_count": object_type_counts.get("execution_audit_finding", 0),
            "execution_audit_not_found_count": execution_audit_not_found_count,
            "execution_audit_empty_count": execution_audit_empty_count,
            "execution_audit_blocked_view_count": execution_audit_blocked_view_count,
            "execution_audit_failed_view_count": execution_audit_failed_view_count,
            "execution_audit_by_query_type": execution_audit_by_query_type,
            "execution_result_promotion_policy_count": object_type_counts.get(
                "execution_result_promotion_policy", 0
            ),
            "execution_result_promotion_candidate_count": object_type_counts.get(
                "execution_result_promotion_candidate", 0
            ),
            "execution_result_promotion_review_request_count": object_type_counts.get(
                "execution_result_promotion_review_request", 0
            ),
            "execution_result_promotion_decision_count": object_type_counts.get(
                "execution_result_promotion_decision", 0
            ),
            "execution_result_promotion_finding_count": object_type_counts.get(
                "execution_result_promotion_finding", 0
            ),
            "execution_result_promotion_result_count": object_type_counts.get(
                "execution_result_promotion_result", 0
            ),
            "execution_result_promotion_pending_review_count": promotion_pending_review_count,
            "execution_result_promotion_approved_for_later_count": promotion_approved_for_later_count,
            "execution_result_promotion_rejected_count": promotion_rejected_count,
            "execution_result_promotion_no_action_count": promotion_no_action_count,
            "execution_result_promotion_private_risk_count": promotion_private_risk_count,
            "execution_result_promotion_by_target_kind": promotion_by_target_kind,
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
        session_continuity_summary: dict[str, Any] | None,
        session_context_projection_summary: dict[str, Any] | None,
        capability_decision_summary: dict[str, Any] | None,
        persona_summary: dict[str, Any] | None,
        personal_runtime_workbench_summary: dict[str, Any] | None,
        tool_registry_summary: dict[str, Any] | None,
        verification_summary: dict[str, Any] | None,
        outcome_summary: dict[str, Any] | None,
        permission_summary: dict[str, Any] | None,
        workspace_write_sandbox_summary: dict[str, Any] | None,
        workspace_read_summary: dict[str, Any] | None,
        shell_network_pre_sandbox_summary: dict[str, Any] | None,
        delegation_summary: dict[str, Any] | None,
        sidechain_summary: dict[str, Any] | None,
        delegation_conformance_summary: dict[str, Any] | None,
        external_capability_summary: dict[str, Any] | None,
        observation_digest_summary: dict[str, Any] | None,
        skill_registry_summary: dict[str, Any] | None,
        observation_digest_proposal_summary: dict[str, Any] | None,
        observation_digest_invocation_summary: dict[str, Any] | None,
        observation_digest_conformance_summary: dict[str, Any] | None,
        external_skill_static_digestion_summary: dict[str, Any] | None,
        agent_observation_spine_summary: dict[str, Any] | None,
        cross_harness_trace_adapter_summary: dict[str, Any] | None,
        observation_to_digestion_adapter_summary: dict[str, Any] | None,
        observation_digestion_ecosystem_summary: dict[str, Any] | None,
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
                f"- Explicit Skill Invocation objects: {(skill_usage_summary or {}).get('explicit_skill_invocation_request_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_input_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_decision_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_result_count', 0)}",
                f"- Explicit Skill Invocation status: completed/denied/unsupported/failed {(skill_usage_summary or {}).get('explicit_skill_invocation_completed_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_denied_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_unsupported_count', 0)}/{(skill_usage_summary or {}).get('explicit_skill_invocation_failed_count', 0)}",
                f"- Explicit Skill Invocation by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('explicit_skill_invocation_by_skill_id') or {})}",
                f"- Explicit Skill Invocation violations: {PIGReportService._inline_counts((skill_usage_summary or {}).get('explicit_skill_invocation_violation_by_type') or {})}",
                f"- Skill Proposal objects: {(skill_usage_summary or {}).get('skill_proposal_intent_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_requirement_count', 0)}/{(skill_usage_summary or {}).get('skill_invocation_proposal_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_decision_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_result_count', 0)}",
                f"- Skill Proposal status: available/incomplete/unsupported/needs_review {(skill_usage_summary or {}).get('skill_proposal_available_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_incomplete_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_unsupported_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_needs_review_count', 0)}",
                f"- Skill Proposal by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_proposal_by_skill_id') or {})}",
                f"- Skill Proposal by operation: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_proposal_by_requested_operation') or {})}",
                f"- Skill Proposal Review objects: {(skill_usage_summary or {}).get('skill_proposal_review_contract_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_request_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_decision_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_finding_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_result_count', 0)}",
                f"- Skill Proposal Review status: approved/rejected/no_action/needs_more_input {(skill_usage_summary or {}).get('skill_proposal_review_approved_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_rejected_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_no_action_count', 0)}/{(skill_usage_summary or {}).get('skill_proposal_review_needs_more_input_count', 0)}",
                f"- Skill Proposal Review bridge candidates: {(skill_usage_summary or {}).get('skill_proposal_review_bridge_candidate_count', 0)}",
                f"- Skill Proposal Review by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_proposal_review_by_skill_id') or {})}",
                f"- Skill Proposal Review by decision: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_proposal_review_by_decision') or {})}",
                f"- Reviewed Execution Bridge objects: {(skill_usage_summary or {}).get('reviewed_execution_bridge_request_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_decision_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_result_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_violation_count', 0)}",
                f"- Reviewed Execution Bridge decision: allowed/denied/needs_more_input/unsupported {(skill_usage_summary or {}).get('reviewed_execution_bridge_allowed_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_denied_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_needs_more_input_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_unsupported_count', 0)}",
                f"- Reviewed Execution Bridge result: executed/blocked {(skill_usage_summary or {}).get('reviewed_execution_bridge_executed_count', 0)}/{(skill_usage_summary or {}).get('reviewed_execution_bridge_blocked_count', 0)}",
                f"- Reviewed Execution Bridge by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('reviewed_execution_bridge_by_skill_id') or {})}",
                f"- Reviewed Execution Bridge violations: {PIGReportService._inline_counts((skill_usage_summary or {}).get('reviewed_execution_bridge_violation_by_type') or {})}",
                f"- Skill Execution Gate objects: {(skill_usage_summary or {}).get('skill_execution_gate_request_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_decision_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_finding_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_result_count', 0)}",
                f"- Skill Execution Gate status: allowed/denied/needs_review/unsupported {(skill_usage_summary or {}).get('skill_execution_gate_allowed_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_denied_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_needs_review_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_unsupported_count', 0)}",
                f"- Skill Execution Gate result: executed/blocked {(skill_usage_summary or {}).get('skill_execution_gate_executed_count', 0)}/{(skill_usage_summary or {}).get('skill_execution_gate_blocked_count', 0)}",
                f"- Skill Execution Gate by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_execution_gate_by_skill_id') or {})}",
                f"- Skill Execution Gate findings: {PIGReportService._inline_counts((skill_usage_summary or {}).get('skill_execution_gate_finding_by_type') or {})}",
                f"- Internal Skill Onboarding objects: {(skill_usage_summary or {}).get('internal_skill_descriptor_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_input_contract_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_output_contract_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_risk_profile_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_gate_contract_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_observability_contract_count', 0)}",
                f"- Internal Skill Onboarding review/findings/results: {(skill_usage_summary or {}).get('internal_skill_onboarding_review_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_onboarding_finding_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_onboarding_result_count', 0)}",
                f"- Internal Skill Onboarding status: accepted/rejected/needs_fix/blocked {(skill_usage_summary or {}).get('internal_skill_onboarding_accepted_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_onboarding_rejected_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_onboarding_needs_fix_count', 0)}/{(skill_usage_summary or {}).get('internal_skill_onboarding_blocked_count', 0)}",
                f"- Internal Skill Onboarding by category: {PIGReportService._inline_counts((skill_usage_summary or {}).get('internal_skill_onboarding_by_capability_category') or {})}",
                f"- Internal Skill Onboarding by risk: {PIGReportService._inline_counts((skill_usage_summary or {}).get('internal_skill_onboarding_by_risk_class') or {})}",
                f"- Internal Skill Onboarding findings: {PIGReportService._inline_counts((skill_usage_summary or {}).get('internal_skill_onboarding_finding_by_type') or {})}",
                f"- Execution Envelope objects: {(skill_usage_summary or {}).get('execution_envelope_count', 0)}/{(skill_usage_summary or {}).get('execution_provenance_record_count', 0)}/{(skill_usage_summary or {}).get('execution_input_snapshot_count', 0)}/{(skill_usage_summary or {}).get('execution_output_snapshot_count', 0)}/{(skill_usage_summary or {}).get('execution_outcome_summary_count', 0)}",
                f"- Execution Envelope status: completed/blocked/failed/skipped {(skill_usage_summary or {}).get('execution_completed_count', 0)}/{(skill_usage_summary or {}).get('execution_blocked_count', 0)}/{(skill_usage_summary or {}).get('execution_failed_count', 0)}/{(skill_usage_summary or {}).get('execution_skipped_count', 0)}",
                f"- Execution Envelope by kind: {PIGReportService._inline_counts((skill_usage_summary or {}).get('execution_by_kind') or {})}",
                f"- Execution Envelope by skill: {PIGReportService._inline_counts((skill_usage_summary or {}).get('execution_by_skill_id') or {})}",
                f"- Execution Envelope gate refs: with/without {(skill_usage_summary or {}).get('execution_with_gate_count', 0)}/{(skill_usage_summary or {}).get('execution_without_gate_count', 0)}",
                f"- Execution Envelope full snapshots: input/output {(skill_usage_summary or {}).get('execution_full_input_stored_count', 0)}/{(skill_usage_summary or {}).get('execution_full_output_stored_count', 0)}",
                f"- Execution Audit objects: {(skill_usage_summary or {}).get('execution_audit_query_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_filter_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_record_view_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_result_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_finding_count', 0)}",
                f"- Execution Audit status: not_found/empty {(skill_usage_summary or {}).get('execution_audit_not_found_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_empty_count', 0)}",
                f"- Execution Audit views: blocked/failed {(skill_usage_summary or {}).get('execution_audit_blocked_view_count', 0)}/{(skill_usage_summary or {}).get('execution_audit_failed_view_count', 0)}",
                f"- Execution Audit by query: {PIGReportService._inline_counts((skill_usage_summary or {}).get('execution_audit_by_query_type') or {})}",
                f"- Execution Result Promotion objects: {(skill_usage_summary or {}).get('execution_result_promotion_policy_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_candidate_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_review_request_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_decision_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_finding_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_result_count', 0)}",
                f"- Execution Result Promotion status: pending/approved_later/rejected/no_action {(skill_usage_summary or {}).get('execution_result_promotion_pending_review_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_approved_for_later_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_rejected_count', 0)}/{(skill_usage_summary or {}).get('execution_result_promotion_no_action_count', 0)}",
                f"- Execution Result Promotion private risk: {(skill_usage_summary or {}).get('execution_result_promotion_private_risk_count', 0)}",
                f"- Execution Result Promotion by target: {PIGReportService._inline_counts((skill_usage_summary or {}).get('execution_result_promotion_by_target_kind') or {})}",
                f"- Personal Runtime Workbench objects: {(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_snapshot_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_panel_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_pending_item_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_recent_activity_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_finding_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_result_count', 0)}",
                f"- Personal Runtime Workbench status: pending_review/blocked/failed/candidates {(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_pending_review_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_blocked_activity_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_failed_activity_count', 0)}/{(personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_candidate_count', 0)}",
                f"- Personal Runtime Workbench by command: {PIGReportService._inline_counts((personal_runtime_workbench_summary or {}).get('personal_runtime_workbench_by_command') or {})}",
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
                "",
                "Session Continuity:",
                f"- Session resumes: {(session_continuity_summary or {}).get('session_resume_count', 0)}",
                f"- Session forks: {(session_continuity_summary or {}).get('session_fork_count', 0)}",
                f"- Context snapshots: {(session_continuity_summary or {}).get('session_context_snapshot_count', 0)}",
                f"- Permission resets: {(session_continuity_summary or {}).get('session_permission_reset_count', 0)}",
                f"- Fork lineage relations: {(session_continuity_summary or {}).get('fork_lineage_count', 0)}",
                f"- Context policies: {(session_context_projection_summary or {}).get('session_context_policy_count', 0)}",
                f"- Context projections: {(session_context_projection_summary or {}).get('session_context_projection_count', 0)}",
                f"- Truncated projections: {(session_context_projection_summary or {}).get('session_context_projection_truncated_count', 0)}",
                f"- Prompt renders: {(session_context_projection_summary or {}).get('session_prompt_render_count', 0)}",
                f"- Avg projection messages/chars: {(session_context_projection_summary or {}).get('average_session_context_projection_messages', 0)}/{(session_context_projection_summary or {}).get('average_session_context_projection_chars', 0)}",
                "",
                "Runtime Capability Decision Surface:",
                f"- Request intents: {(capability_decision_summary or {}).get('capability_request_intent_count', 0)}",
                f"- Requirements: {(capability_decision_summary or {}).get('capability_requirement_count', 0)}",
                f"- Decisions: {(capability_decision_summary or {}).get('capability_decision_count', 0)}",
                f"- Surfaces: {(capability_decision_summary or {}).get('capability_decision_surface_count', 0)}",
                f"- Available/metadata/disabled/review/permission/not-implemented/unknown: {(capability_decision_summary or {}).get('capability_available_now_count', 0)}/{(capability_decision_summary or {}).get('capability_metadata_only_count', 0)}/{(capability_decision_summary or {}).get('capability_disabled_candidate_count', 0)}/{(capability_decision_summary or {}).get('capability_requires_review_count', 0)}/{(capability_decision_summary or {}).get('capability_requires_permission_count', 0)}/{(capability_decision_summary or {}).get('capability_not_implemented_count', 0)}/{(capability_decision_summary or {}).get('capability_unknown_count', 0)}",
                f"- Unfulfillable/limitations: {(capability_decision_summary or {}).get('capability_unfulfillable_request_count', 0)}/{(capability_decision_summary or {}).get('capability_limitation_detected_count', 0)}",
                "",
                "Persona Projection:",
                f"- Soul identities: {(persona_summary or {}).get('soul_identity_count', 0)}",
                f"- Persona profiles: {(persona_summary or {}).get('persona_profile_count', 0)}",
                f"- Instruction artifacts: {(persona_summary or {}).get('persona_instruction_artifact_count', 0)}",
                f"- Agent role bindings: {(persona_summary or {}).get('agent_role_binding_count', 0)}",
                f"- Loadouts/projections: {(persona_summary or {}).get('persona_loadout_count', 0)}/{(persona_summary or {}).get('persona_projection_count', 0)}",
                f"- Capability boundaries/prompt attachments: {(persona_summary or {}).get('persona_capability_boundary_count', 0)}/{(persona_summary or {}).get('persona_projection_attached_to_prompt_count', 0)}",
                f"- Source import objects: {(persona_summary or {}).get('persona_source_count', 0)}/{(persona_summary or {}).get('persona_source_ingestion_candidate_count', 0)}/{(persona_summary or {}).get('persona_assimilation_draft_count', 0)}/{(persona_summary or {}).get('persona_projection_candidate_count', 0)}",
                f"- Source valid/invalid/review/private: {(persona_summary or {}).get('persona_source_valid_count', 0)}/{(persona_summary or {}).get('persona_source_invalid_count', 0)}/{(persona_summary or {}).get('persona_source_needs_review_count', 0)}/{(persona_summary or {}).get('persona_private_source_count', 0)}",
                f"- Source types: {PIGReportService._inline_counts((persona_summary or {}).get('persona_source_by_type') or {})}",
                f"- Source risk levels: {PIGReportService._inline_counts((persona_summary or {}).get('persona_source_by_risk_level') or {})}",
                f"- Personal Directory / Overlay objects: {(persona_summary or {}).get('personal_directory_config_count', 0)}/{(persona_summary or {}).get('personal_directory_manifest_count', 0)}/{(persona_summary or {}).get('personal_projection_ref_count', 0)}/{(persona_summary or {}).get('personal_overlay_load_result_count', 0)}",
                f"- Personal Overlay denied/failed/safe/attached: {(persona_summary or {}).get('personal_overlay_load_denied_count', 0)}/{(persona_summary or {}).get('personal_overlay_boundary_failed_count', 0)}/{(persona_summary or {}).get('personal_overlay_safe_projection_count', 0)}/{(persona_summary or {}).get('personal_projection_attached_to_prompt_count', 0)}",
                f"- Personal Core / Mode objects: {(persona_summary or {}).get('personal_core_profile_count', 0)}/{(persona_summary or {}).get('personal_mode_profile_count', 0)}/{(persona_summary or {}).get('personal_mode_boundary_count', 0)}/{(persona_summary or {}).get('personal_mode_loadout_count', 0)}/{(persona_summary or {}).get('personal_mode_loadout_draft_count', 0)}",
                f"- Personal Mode capabilities: available/requires-permission/not-implemented {(persona_summary or {}).get('personal_mode_capability_available_now_count', 0)}/{(persona_summary or {}).get('personal_mode_capability_requires_permission_count', 0)}/{(persona_summary or {}).get('personal_mode_capability_not_implemented_count', 0)}",
                f"- Personal Mode types: {PIGReportService._inline_counts((persona_summary or {}).get('personal_mode_by_type') or {})}",
                f"- Personal Mode boundary types: {PIGReportService._inline_counts((persona_summary or {}).get('personal_mode_boundary_by_type') or {})}",
                f"- Personal Mode Binding objects: {(persona_summary or {}).get('personal_mode_selection_count', 0)}/{(persona_summary or {}).get('personal_runtime_binding_count', 0)}/{(persona_summary or {}).get('personal_runtime_capability_binding_count', 0)}/{(persona_summary or {}).get('personal_mode_activation_result_count', 0)}",
                f"- Personal Mode Binding activation: denied/prompt-context {(persona_summary or {}).get('personal_mode_activation_denied_count', 0)}/{(persona_summary or {}).get('personal_mode_prompt_context_activation_count', 0)}",
                f"- Personal runtime kinds: {PIGReportService._inline_counts((persona_summary or {}).get('personal_runtime_binding_by_kind') or {})}",
                f"- Personal context ingress: {PIGReportService._inline_counts((persona_summary or {}).get('personal_context_ingress_by_type') or {})}",
                f"- Personal Conformance objects: {(persona_summary or {}).get('personal_conformance_contract_count', 0)}/{(persona_summary or {}).get('personal_conformance_rule_count', 0)}/{(persona_summary or {}).get('personal_conformance_run_count', 0)}/{(persona_summary or {}).get('personal_conformance_result_count', 0)}",
                f"- Personal Conformance status: passed/failed/review/inconclusive {(persona_summary or {}).get('personal_conformance_passed_count', 0)}/{(persona_summary or {}).get('personal_conformance_failed_count', 0)}/{(persona_summary or {}).get('personal_conformance_needs_review_count', 0)}/{(persona_summary or {}).get('personal_conformance_inconclusive_count', 0)}",
                f"- Personal Conformance findings: failed/warning {(persona_summary or {}).get('personal_conformance_failed_finding_count', 0)}/{(persona_summary or {}).get('personal_conformance_warning_finding_count', 0)}",
                f"- Personal Conformance rule types: {PIGReportService._inline_counts((persona_summary or {}).get('personal_conformance_by_rule_type') or {})}",
                f"- Personal Smoke Test objects: {(persona_summary or {}).get('personal_smoke_test_scenario_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_case_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_run_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_result_count', 0)}",
                f"- Personal Smoke Test status: passed/failed/review {(persona_summary or {}).get('personal_smoke_test_passed_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_failed_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_needs_review_count', 0)}",
                f"- Personal Smoke Test assertions: failed/warning {(persona_summary or {}).get('personal_smoke_test_failed_assertion_count', 0)}/{(persona_summary or {}).get('personal_smoke_test_warning_assertion_count', 0)}",
                f"- Personal Smoke Test scenario types: {PIGReportService._inline_counts((persona_summary or {}).get('personal_smoke_test_by_scenario_type') or {})}",
                f"- Personal Runtime Surface objects: {(persona_summary or {}).get('personal_runtime_config_view_count', 0)}/{(persona_summary or {}).get('personal_runtime_status_snapshot_count', 0)}/{(persona_summary or {}).get('personal_runtime_health_check_count', 0)}/{(persona_summary or {}).get('personal_cli_command_result_count', 0)}",
                f"- Personal Runtime Surface config: configured/missing {(persona_summary or {}).get('personal_directory_configured_count', 0)}/{(persona_summary or {}).get('personal_directory_missing_count', 0)}",
                f"- Personal Runtime Surface commands: validate/smoke {(persona_summary or {}).get('personal_cli_validate_run_count', 0)}/{(persona_summary or {}).get('personal_cli_smoke_run_count', 0)}",
                f"- Personal Runtime Surface health: failed/warning {(persona_summary or {}).get('personal_runtime_health_failed_count', 0)}/{(persona_summary or {}).get('personal_runtime_health_warning_count', 0)}",
                f"- Personal Prompt Activation objects: {(persona_summary or {}).get('personal_prompt_activation_config_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_request_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_block_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_result_count', 0)}",
                f"- Personal Prompt Activation lifecycle: attached/skipped/denied {(persona_summary or {}).get('personal_prompt_activation_attached_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_skipped_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_denied_count', 0)}",
                f"- Personal Prompt Activation scope/unsafe: prompt-context/unsafe-finding {(persona_summary or {}).get('personal_prompt_activation_prompt_context_only_count', 0)}/{(persona_summary or {}).get('personal_prompt_activation_unsafe_finding_count', 0)}",
                "",
                "Tool Registry / Policy View:",
                f"- Tool descriptors: {(tool_registry_summary or {}).get('tool_descriptor_count', 0)}",
                f"- Registry snapshots: {(tool_registry_summary or {}).get('tool_registry_snapshot_count', 0)}",
                f"- Policy notes: {(tool_registry_summary or {}).get('tool_policy_note_count', 0)}",
                f"- Risk annotations: {(tool_registry_summary or {}).get('tool_risk_annotation_count', 0)}",
                f"- Tool types: {PIGReportService._inline_counts((tool_registry_summary or {}).get('tool_type_distribution') or {})}",
                f"- Risk levels: {PIGReportService._inline_counts((tool_registry_summary or {}).get('tool_risk_level_distribution') or {})}",
                "",
                "Verification Contract Foundation:",
                f"- Contracts: {(verification_summary or {}).get('verification_contract_count', 0)}",
                f"- Targets: {(verification_summary or {}).get('verification_target_count', 0)}",
                f"- Requirements: {(verification_summary or {}).get('verification_requirement_count', 0)}",
                f"- Runs: {(verification_summary or {}).get('verification_run_count', 0)}",
                f"- Evidence: {(verification_summary or {}).get('verification_evidence_count', 0)}",
                f"- Results: {(verification_summary or {}).get('verification_result_count', 0)}",
                f"- Passed: {(verification_summary or {}).get('verification_passed_count', 0)}",
                f"- Failed: {(verification_summary or {}).get('verification_failed_count', 0)}",
                f"- Inconclusive: {(verification_summary or {}).get('verification_inconclusive_count', 0)}",
                f"- Result by contract type: {PIGReportService._inline_counts((verification_summary or {}).get('verification_result_by_contract_type') or {})}",
                f"- Result by target type: {PIGReportService._inline_counts((verification_summary or {}).get('verification_result_by_target_type') or {})}",
                f"- Read-only skill runs: {(verification_summary or {}).get('read_only_verification_skill_run_count', 0)}",
                f"- Read-only passed: {(verification_summary or {}).get('verification_skill_passed_count', 0)}",
                f"- Read-only failed: {(verification_summary or {}).get('verification_skill_failed_count', 0)}",
                "",
                "Process Outcome Evaluation:",
                f"- Contracts: {(outcome_summary or {}).get('process_outcome_contract_count', 0)}",
                f"- Criteria: {(outcome_summary or {}).get('process_outcome_criterion_count', 0)}",
                f"- Targets: {(outcome_summary or {}).get('process_outcome_target_count', 0)}",
                f"- Signals: {(outcome_summary or {}).get('process_outcome_signal_count', 0)}",
                f"- Evaluations: {(outcome_summary or {}).get('process_outcome_evaluation_count', 0)}",
                f"- Success: {(outcome_summary or {}).get('process_outcome_success_count', 0)}",
                f"- Partial success: {(outcome_summary or {}).get('process_outcome_partial_success_count', 0)}",
                f"- Failed: {(outcome_summary or {}).get('process_outcome_failed_count', 0)}",
                f"- Inconclusive: {(outcome_summary or {}).get('process_outcome_inconclusive_count', 0)}",
                f"- Needs review: {(outcome_summary or {}).get('process_outcome_needs_review_count', 0)}",
                f"- Error: {(outcome_summary or {}).get('process_outcome_error_count', 0)}",
                f"- Average evidence coverage: {(outcome_summary or {}).get('average_evidence_coverage')}",
                f"- Average score: {(outcome_summary or {}).get('average_outcome_score')}",
                f"- Outcome by contract type: {PIGReportService._inline_counts((outcome_summary or {}).get('process_outcome_by_contract_type') or {})}",
                f"- Outcome by target type: {PIGReportService._inline_counts((outcome_summary or {}).get('process_outcome_by_target_type') or {})}",
                "",
                "Permission Model:",
                f"- Scopes: {(permission_summary or {}).get('permission_scope_count', 0)}",
                f"- Requests: {(permission_summary or {}).get('permission_request_count', 0)}",
                f"- Decisions: {(permission_summary or {}).get('permission_decision_count', 0)}",
                f"- Grants: {(permission_summary or {}).get('permission_grant_count', 0)}",
                f"- Denials: {(permission_summary or {}).get('permission_denial_count', 0)}",
                f"- Policy notes: {(permission_summary or {}).get('permission_policy_note_count', 0)}",
                f"- Request types: {PIGReportService._inline_counts((permission_summary or {}).get('permission_request_by_type') or {})}",
                f"- Operations: {PIGReportService._inline_counts((permission_summary or {}).get('permission_request_by_operation') or {})}",
                f"- Decision allow/deny/ask/defer: {(permission_summary or {}).get('permission_decision_allow_count', 0)}/{(permission_summary or {}).get('permission_decision_deny_count', 0)}/{(permission_summary or {}).get('permission_decision_ask_count', 0)}/{(permission_summary or {}).get('permission_decision_defer_count', 0)}",
                f"- Active grants: {(permission_summary or {}).get('permission_grant_active_count', 0)}",
                "",
                "Session Permission Read-model:",
                f"- Contexts: {(permission_summary or {}).get('session_permission_context_count', 0)}",
                f"- Snapshots: {(permission_summary or {}).get('session_permission_snapshot_count', 0)}",
                f"- Resolutions: {(permission_summary or {}).get('session_permission_resolution_count', 0)}",
                f"- Resolution allow/deny/ask/inconclusive: {(permission_summary or {}).get('session_permission_resolution_allow_count', 0)}/{(permission_summary or {}).get('session_permission_resolution_deny_count', 0)}/{(permission_summary or {}).get('session_permission_resolution_ask_count', 0)}/{(permission_summary or {}).get('session_permission_resolution_inconclusive_count', 0)}",
                f"- Session active/expired/revoked grants: {(permission_summary or {}).get('session_active_grant_count', 0)}/{(permission_summary or {}).get('session_expired_grant_count', 0)}/{(permission_summary or {}).get('session_revoked_grant_count', 0)}",
                f"- Session denials: {(permission_summary or {}).get('session_denial_count', 0)}",
                f"- Pending session permission requests: {(permission_summary or {}).get('session_pending_permission_request_count', 0)}",
                "",
                "Workspace Write Sandbox:",
                f"- Workspace roots: {(workspace_write_sandbox_summary or {}).get('workspace_root_count', 0)}",
                f"- Boundaries: {(workspace_write_sandbox_summary or {}).get('workspace_write_boundary_count', 0)}",
                f"- Intents: {(workspace_write_sandbox_summary or {}).get('workspace_write_intent_count', 0)}",
                f"- Decisions: {(workspace_write_sandbox_summary or {}).get('workspace_write_sandbox_decision_count', 0)}",
                f"- Violations: {(workspace_write_sandbox_summary or {}).get('workspace_write_sandbox_violation_count', 0)}",
                f"- Allowed/denied/review/inconclusive/error: {(workspace_write_sandbox_summary or {}).get('workspace_write_allowed_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_denied_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_needs_review_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_inconclusive_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_error_count', 0)}",
                f"- Outside/protected/denied violations: {(workspace_write_sandbox_summary or {}).get('workspace_write_outside_workspace_violation_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_protected_path_violation_count', 0)}/{(workspace_write_sandbox_summary or {}).get('workspace_write_denied_path_violation_count', 0)}",
                "",
                "Workspace Read Skills:",
                f"- Roots: {(workspace_read_summary or {}).get('workspace_read_root_count', 0)}",
                f"- File list requests/results: {(workspace_read_summary or {}).get('workspace_file_list_request_count', 0)}/{(workspace_read_summary or {}).get('workspace_file_list_result_count', 0)}",
                f"- Text read requests/results: {(workspace_read_summary or {}).get('workspace_text_file_read_request_count', 0)}/{(workspace_read_summary or {}).get('workspace_text_file_read_result_count', 0)}",
                f"- Markdown summary requests/results: {(workspace_read_summary or {}).get('workspace_markdown_summary_request_count', 0)}/{(workspace_read_summary or {}).get('workspace_markdown_summary_result_count', 0)}",
                f"- Violations/denied/binary/oversize: {(workspace_read_summary or {}).get('workspace_read_violation_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_denied_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_binary_rejected_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_oversize_rejected_count', 0)}",
                f"- Outside/path traversal violations: {(workspace_read_summary or {}).get('workspace_read_outside_workspace_violation_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_path_traversal_violation_count', 0)}",
                f"- Workspace Read Summary objects: {(workspace_read_summary or {}).get('workspace_read_summary_policy_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_request_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_section_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_result_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_candidate_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_finding_count', 0)}",
                f"- Workspace Read Summary status: completed/failed/unsupported {(workspace_read_summary or {}).get('workspace_read_summary_completed_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_failed_count', 0)}/{(workspace_read_summary or {}).get('workspace_read_summary_unsupported_count', 0)}",
                f"- Workspace Read Summary candidates pending: {(workspace_read_summary or {}).get('workspace_read_summary_candidate_pending_count', 0)}",
                f"- Workspace Read Summary by kind: {PIGReportService._inline_counts((workspace_read_summary or {}).get('workspace_read_summary_by_input_kind') or {})}",
                f"- Workspace Read Summary findings: {PIGReportService._inline_counts((workspace_read_summary or {}).get('workspace_read_summary_finding_by_type') or {})}",
                "",
                "Shell / Network Risk Pre-Sandbox:",
                f"- Shell intents: {(shell_network_pre_sandbox_summary or {}).get('shell_command_intent_count', 0)}",
                f"- Network intents: {(shell_network_pre_sandbox_summary or {}).get('network_access_intent_count', 0)}",
                f"- Assessments: {(shell_network_pre_sandbox_summary or {}).get('shell_network_risk_assessment_count', 0)}",
                f"- Decisions: {(shell_network_pre_sandbox_summary or {}).get('shell_network_pre_sandbox_decision_count', 0)}",
                f"- Violations: {(shell_network_pre_sandbox_summary or {}).get('shell_network_risk_violation_count', 0)}",
                f"- Shell low/medium/high/critical: {(shell_network_pre_sandbox_summary or {}).get('shell_risk_low_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('shell_risk_medium_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('shell_risk_high_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('shell_risk_critical_count', 0)}",
                f"- Network low/medium/high/critical: {(shell_network_pre_sandbox_summary or {}).get('network_risk_low_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('network_risk_medium_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('network_risk_high_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('network_risk_critical_count', 0)}",
                f"- Recommended allow/deny/review/inconclusive/error: {(shell_network_pre_sandbox_summary or {}).get('pre_sandbox_allow_recommended_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('pre_sandbox_deny_recommended_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('pre_sandbox_needs_review_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('pre_sandbox_inconclusive_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('pre_sandbox_error_count', 0)}",
                f"- Destructive/network/credential/exfiltration violations: {(shell_network_pre_sandbox_summary or {}).get('destructive_command_violation_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('network_access_violation_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('credential_exposure_violation_count', 0)}/{(shell_network_pre_sandbox_summary or {}).get('exfiltration_risk_violation_count', 0)}",
                "",
                "Delegated Process Runs:",
                f"- Packets: {(delegation_summary or {}).get('delegation_packet_count', 0)}",
                f"- Runs: {(delegation_summary or {}).get('delegated_process_run_count', 0)}",
                f"- Results: {(delegation_summary or {}).get('delegation_result_count', 0)}",
                f"- Links: {(delegation_summary or {}).get('delegation_link_count', 0)}",
                f"- Created/requested/started/completed: {(delegation_summary or {}).get('delegated_process_created_count', 0)}/{(delegation_summary or {}).get('delegated_process_requested_count', 0)}/{(delegation_summary or {}).get('delegated_process_started_count', 0)}/{(delegation_summary or {}).get('delegated_process_completed_count', 0)}",
                f"- Failed/cancelled/skipped: {(delegation_summary or {}).get('delegated_process_failed_count', 0)}/{(delegation_summary or {}).get('delegated_process_cancelled_count', 0)}/{(delegation_summary or {}).get('delegated_process_skipped_count', 0)}",
                f"- By type: {PIGReportService._inline_counts((delegation_summary or {}).get('delegation_by_type') or {})}",
                f"- By isolation: {PIGReportService._inline_counts((delegation_summary or {}).get('delegation_by_isolation_mode') or {})}",
                f"- Permission/safety refs: {(delegation_summary or {}).get('delegation_permission_reference_count', 0)}/{(delegation_summary or {}).get('delegation_safety_reference_count', 0)}",
                "",
                "Sidechain Context:",
                f"- Contexts: {(sidechain_summary or {}).get('sidechain_context_count', 0)}",
                f"- Entries: {(sidechain_summary or {}).get('sidechain_context_entry_count', 0)}",
                f"- Snapshots: {(sidechain_summary or {}).get('sidechain_context_snapshot_count', 0)}",
                f"- Return envelopes: {(sidechain_summary or {}).get('sidechain_return_envelope_count', 0)}",
                f"- Ready/sealed/error: {(sidechain_summary or {}).get('sidechain_ready_count', 0)}/{(sidechain_summary or {}).get('sidechain_sealed_count', 0)}/{(sidechain_summary or {}).get('sidechain_error_count', 0)}",
                f"- Parent transcript excluded: {(sidechain_summary or {}).get('sidechain_parent_transcript_excluded_count', 0)}",
                f"- Permission inheritance prevented: {(sidechain_summary or {}).get('sidechain_permission_inheritance_prevented_count', 0)}",
                f"- Safety refs: {(sidechain_summary or {}).get('sidechain_safety_ref_count', 0)}",
                f"- By type: {PIGReportService._inline_counts((sidechain_summary or {}).get('sidechain_context_by_type') or {})}",
                f"- By isolation: {PIGReportService._inline_counts((sidechain_summary or {}).get('sidechain_context_by_isolation_mode') or {})}",
                "",
                "Delegation Conformance:",
                f"- Contracts: {(delegation_conformance_summary or {}).get('delegation_conformance_contract_count', 0)}",
                f"- Rules: {(delegation_conformance_summary or {}).get('delegation_conformance_rule_count', 0)}",
                f"- Runs: {(delegation_conformance_summary or {}).get('delegation_conformance_run_count', 0)}",
                f"- Findings: {(delegation_conformance_summary or {}).get('delegation_conformance_finding_count', 0)}",
                f"- Results: {(delegation_conformance_summary or {}).get('delegation_conformance_result_count', 0)}",
                f"- Passed/failed/review/inconclusive: {(delegation_conformance_summary or {}).get('delegation_conformance_passed_count', 0)}/{(delegation_conformance_summary or {}).get('delegation_conformance_failed_count', 0)}/{(delegation_conformance_summary or {}).get('delegation_conformance_needs_review_count', 0)}/{(delegation_conformance_summary or {}).get('delegation_conformance_inconclusive_count', 0)}",
                f"- Failed/warning findings: {(delegation_conformance_summary or {}).get('delegation_conformance_failed_finding_count', 0)}/{(delegation_conformance_summary or {}).get('delegation_conformance_warning_finding_count', 0)}",
                f"- By rule: {PIGReportService._inline_counts((delegation_conformance_summary or {}).get('delegation_conformance_by_rule_type') or {})}",
                f"- Average score: {(delegation_conformance_summary or {}).get('average_delegation_conformance_score')}",
                "",
                "External Capability Import:",
                f"- Sources: {(external_capability_summary or {}).get('external_capability_source_count', 0)}",
                f"- Descriptors: {(external_capability_summary or {}).get('external_capability_descriptor_count', 0)}",
                f"- Batches: {(external_capability_summary or {}).get('external_capability_import_batch_count', 0)}",
                f"- Normalizations: {(external_capability_summary or {}).get('external_capability_normalization_result_count', 0)}",
                f"- Candidates: {(external_capability_summary or {}).get('external_assimilation_candidate_count', 0)}",
                f"- Risk notes: {(external_capability_summary or {}).get('external_capability_risk_note_count', 0)}",
                f"- Disabled/pending/execution-enabled candidates: {(external_capability_summary or {}).get('external_candidate_disabled_count', 0)}/{(external_capability_summary or {}).get('external_candidate_pending_review_count', 0)}/{(external_capability_summary or {}).get('external_candidate_execution_enabled_count', 0)}",
                f"- Capability types: {PIGReportService._inline_counts((external_capability_summary or {}).get('external_capability_by_type') or {})}",
                f"- Risk levels: {PIGReportService._inline_counts((external_capability_summary or {}).get('external_capability_by_risk_level') or {})}",
                f"- Review required: {(external_capability_summary or {}).get('external_capability_review_required_count', 0)}",
                f"- Registry snapshots: {(external_capability_summary or {}).get('external_capability_registry_snapshot_count', 0)}",
                f"- View writes registry/review/risks: {(external_capability_summary or {}).get('external_capability_registry_view_written_count', 0)}/{(external_capability_summary or {}).get('external_capability_review_view_written_count', 0)}/{(external_capability_summary or {}).get('external_capability_risk_view_written_count', 0)}",
                f"- View disabled/pending/execution-enabled: {(external_capability_summary or {}).get('external_view_disabled_candidate_count', 0)}/{(external_capability_summary or {}).get('external_view_pending_review_count', 0)}/{(external_capability_summary or {}).get('external_view_execution_enabled_candidate_count', 0)}",
                f"- View high/critical risks: {(external_capability_summary or {}).get('external_view_high_risk_count', 0)}/{(external_capability_summary or {}).get('external_view_critical_risk_count', 0)}",
                f"- Review queues/items/checklists/findings/decisions: {(external_capability_summary or {}).get('external_adapter_review_queue_count', 0)}/{(external_capability_summary or {}).get('external_adapter_review_item_count', 0)}/{(external_capability_summary or {}).get('external_adapter_review_checklist_count', 0)}/{(external_capability_summary or {}).get('external_adapter_review_finding_count', 0)}/{(external_capability_summary or {}).get('external_adapter_review_decision_count', 0)}",
                f"- Review pending/in-review/more-info/design/rejected: {(external_capability_summary or {}).get('external_review_pending_count', 0)}/{(external_capability_summary or {}).get('external_review_in_review_count', 0)}/{(external_capability_summary or {}).get('external_review_needs_more_info_count', 0)}/{(external_capability_summary or {}).get('external_review_approved_for_design_count', 0)}/{(external_capability_summary or {}).get('external_review_rejected_count', 0)}",
                f"- Review open/high/critical findings: {(external_capability_summary or {}).get('external_review_open_finding_count', 0)}/{(external_capability_summary or {}).get('external_review_high_risk_finding_count', 0)}/{(external_capability_summary or {}).get('external_review_critical_risk_finding_count', 0)}",
                f"- Review non-activating/runtime activation: {(external_capability_summary or {}).get('external_review_non_activating_decision_count', 0)}/{(external_capability_summary or {}).get('external_review_runtime_activation_count', 0)}",
                f"- MCP/plugin descriptors server/tool/plugin/entrypoint: {(external_capability_summary or {}).get('mcp_server_descriptor_count', 0)}/{(external_capability_summary or {}).get('mcp_tool_descriptor_count', 0)}/{(external_capability_summary or {}).get('plugin_descriptor_count', 0)}/{(external_capability_summary or {}).get('plugin_entrypoint_descriptor_count', 0)}",
                f"- MCP/plugin skeletons/validations: {(external_capability_summary or {}).get('external_descriptor_skeleton_count', 0)}/{(external_capability_summary or {}).get('external_descriptor_skeleton_validation_count', 0)}",
                f"- MCP/plugin needs-review server/plugin: {(external_capability_summary or {}).get('mcp_descriptor_needs_review_count', 0)}/{(external_capability_summary or {}).get('plugin_descriptor_needs_review_count', 0)}",
                f"- Skeleton validation passed/failed/review: {(external_capability_summary or {}).get('skeleton_validation_passed_count', 0)}/{(external_capability_summary or {}).get('skeleton_validation_failed_count', 0)}/{(external_capability_summary or {}).get('skeleton_validation_needs_review_count', 0)}",
                f"- MCP/plugin execution-enabled/activation-enabled: {(external_capability_summary or {}).get('mcp_plugin_execution_enabled_count', 0)}/{(external_capability_summary or {}).get('mcp_plugin_activation_enabled_count', 0)}",
                f"- MCP/plugin descriptor types: {PIGReportService._inline_counts((external_capability_summary or {}).get('mcp_plugin_descriptor_by_type') or {})}",
                f"- MCP/plugin risk categories: {PIGReportService._inline_counts((external_capability_summary or {}).get('mcp_plugin_risk_category_count') or {})}",
                f"- External OCEL sources/descriptors/candidates: {(external_capability_summary or {}).get('external_ocel_source_count', 0)}/{(external_capability_summary or {}).get('external_ocel_payload_descriptor_count', 0)}/{(external_capability_summary or {}).get('external_ocel_import_candidate_count', 0)}",
                f"- External OCEL validations/previews/risks: {(external_capability_summary or {}).get('external_ocel_validation_result_count', 0)}/{(external_capability_summary or {}).get('external_ocel_preview_snapshot_count', 0)}/{(external_capability_summary or {}).get('external_ocel_risk_note_count', 0)}",
                f"- External OCEL valid/invalid/review: {(external_capability_summary or {}).get('external_ocel_valid_count', 0)}/{(external_capability_summary or {}).get('external_ocel_invalid_count', 0)}/{(external_capability_summary or {}).get('external_ocel_needs_review_count', 0)}",
                f"- External OCEL pending/canonical-enabled/not-merged: {(external_capability_summary or {}).get('external_ocel_candidate_pending_review_count', 0)}/{(external_capability_summary or {}).get('external_ocel_candidate_canonical_import_enabled_count', 0)}/{(external_capability_summary or {}).get('external_ocel_candidate_not_merged_count', 0)}",
                f"- External OCEL preview events/objects/relations: {(external_capability_summary or {}).get('external_ocel_total_preview_event_count', 0)}/{(external_capability_summary or {}).get('external_ocel_total_preview_object_count', 0)}/{(external_capability_summary or {}).get('external_ocel_total_preview_relation_count', 0)}",
                f"- External OCEL schema status: {PIGReportService._inline_counts((external_capability_summary or {}).get('external_ocel_by_schema_status') or {})}",
                f"- External OCEL risk levels: {PIGReportService._inline_counts((external_capability_summary or {}).get('external_ocel_by_risk_level') or {})}",
                "",
                "Observation and Digestion:",
                f"- Observation sources/batches/events/runs: {(observation_digest_summary or {}).get('agent_observation_source_count', 0)}/{(observation_digest_summary or {}).get('agent_observation_batch_count', 0)}/{(observation_digest_summary or {}).get('agent_observation_normalized_event_count', 0)}/{(observation_digest_summary or {}).get('observed_agent_run_count', 0)}",
                f"- Inferences/narratives: {(observation_digest_summary or {}).get('agent_behavior_inference_count', 0)}/{(observation_digest_summary or {}).get('agent_process_narrative_count', 0)}",
                f"- External source/profile/fingerprint/candidate/adapter: {(observation_digest_summary or {}).get('external_skill_source_descriptor_count', 0)}/{(observation_digest_summary or {}).get('external_skill_static_profile_count', 0)}/{(observation_digest_summary or {}).get('external_skill_behavior_fingerprint_count', 0)}/{(observation_digest_summary or {}).get('external_skill_assimilation_candidate_count', 0)}/{(observation_digest_summary or {}).get('external_skill_adapter_candidate_count', 0)}",
                f"- Findings/results: {(observation_digest_summary or {}).get('observation_digestion_finding_count', 0)}/{(observation_digest_summary or {}).get('observation_digestion_result_count', 0)}",
                f"- Observed activity: {PIGReportService._inline_counts((observation_digest_summary or {}).get('observed_event_by_activity') or {})}",
                f"- Candidate risks: {PIGReportService._inline_counts((observation_digest_summary or {}).get('external_candidate_by_risk_class') or {})}",
                "",
                "Skill Registry View:",
                f"- Views/entries/filters/findings/results: {(skill_registry_summary or {}).get('skill_registry_view_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_entry_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_filter_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_finding_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_result_count', 0)}",
                f"- Observation/digestion/external candidates: {(skill_registry_summary or {}).get('skill_registry_observation_skill_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_digestion_skill_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_external_candidate_count', 0)}",
                f"- Enabled/disabled/blocked: {(skill_registry_summary or {}).get('skill_registry_enabled_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_disabled_count', 0)}/{(skill_registry_summary or {}).get('skill_registry_blocked_count', 0)}",
                f"- Missing contract findings: {(skill_registry_summary or {}).get('skill_registry_missing_contract_finding_count', 0)}",
                f"- Registry by layer: {PIGReportService._inline_counts((skill_registry_summary or {}).get('skill_registry_by_layer') or {})}",
                f"- Registry by risk: {PIGReportService._inline_counts((skill_registry_summary or {}).get('skill_registry_by_risk_class') or {})}",
                "",
                "Observation/Digestion Proposals:",
                f"- Policies/intents/bindings/sets/findings/results: {(observation_digest_proposal_summary or {}).get('observation_digest_proposal_policy_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_intent_candidate_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_binding_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_set_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_finding_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_result_count', 0)}",
                f"- Observation/digestion/mixed: {(observation_digest_proposal_summary or {}).get('observation_digest_proposal_observation_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_digestion_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_mixed_count', 0)}",
                f"- Needs input/no match: {(observation_digest_proposal_summary or {}).get('observation_digest_proposal_needs_more_input_count', 0)}/{(observation_digest_proposal_summary or {}).get('observation_digest_proposal_no_matching_skill_count', 0)}",
                f"- Proposal by family: {PIGReportService._inline_counts((observation_digest_proposal_summary or {}).get('observation_digest_proposal_by_intent_family') or {})}",
                f"- Proposal by skill: {PIGReportService._inline_counts((observation_digest_proposal_summary or {}).get('observation_digest_proposal_by_skill_id') or {})}",
                "",
                "Observation/Digestion Invocations:",
                f"- Bindings/policies/results/findings: {(observation_digest_invocation_summary or {}).get('observation_digest_runtime_binding_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_policy_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_result_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_finding_count', 0)}",
                f"- Completed/blocked/failed/enveloped: {(observation_digest_invocation_summary or {}).get('observation_digest_invocation_completed_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_blocked_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_failed_count', 0)}/{(observation_digest_invocation_summary or {}).get('observation_digest_invocation_envelope_count', 0)}",
                f"- Invocation by skill: {PIGReportService._inline_counts((observation_digest_invocation_summary or {}).get('observation_digest_invocation_by_skill_id') or {})}",
                f"- Invocation by family: {PIGReportService._inline_counts((observation_digest_invocation_summary or {}).get('observation_digest_invocation_by_family') or {})}",
                f"- Invocation findings: {PIGReportService._inline_counts((observation_digest_invocation_summary or {}).get('observation_digest_invocation_finding_by_type') or {})}",
                "",
                "Observation/Digestion Conformance:",
                f"- Policies/checks/smoke cases/smoke results/findings/reports: {(observation_digest_conformance_summary or {}).get('observation_digest_conformance_policy_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_conformance_check_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_smoke_case_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_smoke_result_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_conformance_finding_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_conformance_report_count', 0)}",
                f"- Passed/failed skills: {(observation_digest_conformance_summary or {}).get('observation_digest_conformance_passed_skill_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_conformance_failed_skill_count', 0)}",
                f"- Smoke passed/failed: {(observation_digest_conformance_summary or {}).get('observation_digest_smoke_passed_count', 0)}/{(observation_digest_conformance_summary or {}).get('observation_digest_smoke_failed_count', 0)}",
                f"- Conformance findings: {PIGReportService._inline_counts((observation_digest_conformance_summary or {}).get('observation_digest_conformance_finding_by_type') or {})}",
                f"- Conformance checks: {PIGReportService._inline_counts((observation_digest_conformance_summary or {}).get('observation_digest_conformance_check_by_type') or {})}",
                "",
                "External Skill Static Digestion:",
                f"- Inventories/manifests/instructions/capabilities/risks/reports/findings: {(external_skill_static_digestion_summary or {}).get('external_skill_resource_inventory_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_manifest_profile_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_instruction_profile_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_declared_capability_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_risk_profile_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digestion_report_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digestion_finding_count', 0)}",
                f"- Manifest kinds: {PIGReportService._inline_counts((external_skill_static_digestion_summary or {}).get('external_skill_static_digest_by_manifest_kind') or {})}",
                f"- Capability categories: {PIGReportService._inline_counts((external_skill_static_digestion_summary or {}).get('external_skill_static_digest_by_capability_category') or {})}",
                f"- Risk classes: {PIGReportService._inline_counts((external_skill_static_digestion_summary or {}).get('external_skill_static_digest_by_risk_class') or {})}",
                f"- Scripts/shell/network/write/mcp/plugin: {(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_script_detected_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_shell_declared_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_network_declared_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_write_declared_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_mcp_declared_count', 0)}/{(external_skill_static_digestion_summary or {}).get('external_skill_static_digest_plugin_declared_count', 0)}",
                "",
                "Agent Observation Spine:",
                f"- Agents/runtimes/environments/collectors/adapters/ontology: {(agent_observation_spine_summary or {}).get('agent_instance_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_runtime_descriptor_count', 0)}/{(agent_observation_spine_summary or {}).get('runtime_environment_snapshot_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_observation_collector_contract_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_observation_adapter_profile_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_movement_ontology_term_count', 0)}",
                f"- Events/objects/relations/inferences/reviews/corrections: {(agent_observation_spine_summary or {}).get('agent_observation_normalized_event_v2_count', 0)}/{(agent_observation_spine_summary or {}).get('observed_agent_object_count', 0)}/{(agent_observation_spine_summary or {}).get('observed_agent_relation_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_behavior_inference_v2_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_observation_review_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_observation_correction_count', 0)}",
                f"- Redaction/export/fleet/findings: {(agent_observation_spine_summary or {}).get('observation_redaction_policy_count', 0)}/{(agent_observation_spine_summary or {}).get('observation_export_policy_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_fleet_observation_snapshot_count', 0)}/{(agent_observation_spine_summary or {}).get('agent_observation_spine_finding_count', 0)}",
                f"- Action types: {PIGReportService._inline_counts((agent_observation_spine_summary or {}).get('observed_event_v2_by_action_type') or {})}",
                f"- Object types: {PIGReportService._inline_counts((agent_observation_spine_summary or {}).get('observed_object_by_type') or {})}",
                f"- Relation types: {PIGReportService._inline_counts((agent_observation_spine_summary or {}).get('observed_relation_by_type') or {})}",
                f"- Inference confidence: {PIGReportService._inline_counts((agent_observation_spine_summary or {}).get('behavior_inference_by_confidence_class') or {})}",
                "",
                "Cross-Harness Trace Adapters:",
                f"- Policies/contracts/inspections/rules/plans/results/coverage/findings: {(cross_harness_trace_adapter_summary or {}).get('cross_harness_trace_adapter_policy_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_adapter_contract_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_source_inspection_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_mapping_rule_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_normalization_plan_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_normalization_result_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_adapter_coverage_report_count', 0)}/{(cross_harness_trace_adapter_summary or {}).get('harness_trace_adapter_finding_count', 0)}",
                f"- Normalized events: {(cross_harness_trace_adapter_summary or {}).get('harness_trace_normalized_event_count', 0)}",
                f"- By runtime: {PIGReportService._inline_counts((cross_harness_trace_adapter_summary or {}).get('harness_trace_normalization_by_runtime') or {})}",
                f"- By adapter: {PIGReportService._inline_counts((cross_harness_trace_adapter_summary or {}).get('harness_trace_normalization_by_adapter') or {})}",
                f"- Adapter implemented: {PIGReportService._inline_counts((cross_harness_trace_adapter_summary or {}).get('harness_trace_adapter_by_implemented') or {})}",
                f"- Findings: {PIGReportService._inline_counts((cross_harness_trace_adapter_summary or {}).get('harness_trace_adapter_finding_by_type') or {})}",
                "",
                "Observation-to-Digestion Adapter Builder:",
                f"- Policies/capabilities/targets/input maps/output maps: {(observation_to_digestion_adapter_summary or {}).get('observation_to_digestion_adapter_policy_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('observed_capability_candidate_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('chantacore_target_skill_candidate_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('adapter_input_mapping_spec_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('adapter_output_mapping_spec_count', 0)}",
                f"- Unsupported/reviews/findings/results: {(observation_to_digestion_adapter_summary or {}).get('adapter_unsupported_feature_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('observation_digestion_adapter_review_request_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('observation_digestion_adapter_finding_count', 0)}/{(observation_to_digestion_adapter_summary or {}).get('observation_digestion_adapter_build_result_count', 0)}",
                f"- Adapter candidates: {(observation_to_digestion_adapter_summary or {}).get('observation_digestion_adapter_candidate_count', 0)}",
                f"- Candidate risk: {PIGReportService._inline_counts((observation_to_digestion_adapter_summary or {}).get('adapter_candidate_by_risk_class') or {})}",
                f"- Candidate target skill: {PIGReportService._inline_counts((observation_to_digestion_adapter_summary or {}).get('adapter_candidate_by_target_skill_id') or {})}",
                f"- Candidate mapping type: {PIGReportService._inline_counts((observation_to_digestion_adapter_summary or {}).get('adapter_candidate_by_mapping_type') or {})}",
                f"- Unsupported feature type: {PIGReportService._inline_counts((observation_to_digestion_adapter_summary or {}).get('unsupported_feature_by_type') or {})}",
                f"- Observed capability category: {PIGReportService._inline_counts((observation_to_digestion_adapter_summary or {}).get('observed_capability_by_category') or {})}",
                "",
                "Observation/Digestion Ecosystem Consolidation:",
                f"- Snapshots/components/capabilities/safety/gaps/manifests/findings/reports: {(observation_digestion_ecosystem_summary or {}).get('observation_digestion_ecosystem_snapshot_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_ecosystem_component_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_capability_map_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_safety_boundary_report_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_gap_register_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_release_manifest_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_consolidation_finding_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_consolidation_report_count', 0)}",
                f"- Ready/partial/contract-only/blocked: {(observation_digestion_ecosystem_summary or {}).get('observation_digestion_ready_component_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_partial_component_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_contract_only_component_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_blocked_component_count', 0)}",
                f"- Future gaps/executable external candidates: {(observation_digestion_ecosystem_summary or {}).get('observation_digestion_future_track_gap_count', 0)}/{(observation_digestion_ecosystem_summary or {}).get('observation_digestion_executable_external_candidate_count', 0)}",
                f"- Component kinds: {PIGReportService._inline_counts((observation_digestion_ecosystem_summary or {}).get('observation_digestion_by_component_kind') or {})}",
                f"- Readiness levels: {PIGReportService._inline_counts((observation_digestion_ecosystem_summary or {}).get('observation_digestion_by_readiness_level') or {})}",
                f"- Capability families: {PIGReportService._inline_counts((observation_digestion_ecosystem_summary or {}).get('observation_digestion_by_capability_family') or {})}",
                f"- Gap types: {PIGReportService._inline_counts((observation_digestion_ecosystem_summary or {}).get('observation_digestion_gap_by_type') or {})}",
                f"- Finding types: {PIGReportService._inline_counts((observation_digestion_ecosystem_summary or {}).get('observation_digestion_finding_by_type') or {})}",
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
    def _session_continuity_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
    ) -> dict[str, Any]:
        return {
            "session_resume_count": object_type_counts.get("session_resume", 0),
            "session_fork_count": object_type_counts.get("session_fork", 0),
            "session_context_snapshot_count": object_type_counts.get("session_context_snapshot", 0),
            "session_permission_reset_count": event_activity_counts.get("session_permissions_reset", 0),
            "session_resumed_count": event_activity_counts.get("session_resumed", 0),
            "session_forked_count": event_activity_counts.get("session_forked", 0),
            "fork_lineage_count": event_activity_counts.get("session_forked", 0),
        }

    @staticmethod
    def _session_context_projection_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        projection_objects = [
            item for item in view.objects if item.object_type == "session_context_projection"
        ]
        total_messages = sum(
            int(item.object_attrs.get("total_messages") or 0)
            for item in projection_objects
        )
        total_chars = sum(
            int(item.object_attrs.get("total_chars") or 0)
            for item in projection_objects
        )
        projection_count = object_type_counts.get("session_context_projection", 0)
        return {
            "session_context_policy_count": object_type_counts.get(
                "session_context_policy", 0
            ),
            "session_context_projection_count": projection_count,
            "session_context_projection_truncated_count": event_activity_counts.get(
                "session_context_projection_truncated", 0
            ),
            "session_prompt_render_count": object_type_counts.get(
                "session_prompt_render", 0
            ),
            "session_prompt_rendered_count": event_activity_counts.get(
                "session_prompt_rendered", 0
            ),
            "average_session_context_projection_messages": (
                round(total_messages / projection_count, 2) if projection_count else 0
            ),
            "average_session_context_projection_chars": (
                round(total_chars / projection_count, 2) if projection_count else 0
            ),
        }

    @staticmethod
    def _capability_decision_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        availability_counts: dict[str, int] = {
            "available_now": 0,
            "metadata_only": 0,
            "disabled_candidate": 0,
            "requires_review": 0,
            "requires_permission": 0,
            "requires_explicit_skill": 0,
            "not_implemented": 0,
            "unknown": 0,
        }
        for item in view.objects:
            if item.object_type != "capability_decision":
                continue
            availability = str(item.object_attrs.get("availability") or "unknown")
            if availability not in availability_counts:
                availability = "unknown"
            availability_counts[availability] += 1
        return {
            "capability_request_intent_count": object_type_counts.get(
                "capability_request_intent", 0
            ),
            "capability_requirement_count": object_type_counts.get(
                "capability_requirement", 0
            ),
            "capability_decision_count": object_type_counts.get(
                "capability_decision", 0
            ),
            "capability_decision_surface_count": object_type_counts.get(
                "capability_decision_surface", 0
            ),
            "capability_available_now_count": availability_counts["available_now"],
            "capability_metadata_only_count": availability_counts["metadata_only"],
            "capability_disabled_candidate_count": availability_counts[
                "disabled_candidate"
            ],
            "capability_requires_review_count": availability_counts["requires_review"],
            "capability_requires_permission_count": availability_counts[
                "requires_permission"
            ],
            "capability_requires_explicit_skill_count": availability_counts[
                "requires_explicit_skill"
            ],
            "capability_not_implemented_count": availability_counts["not_implemented"],
            "capability_unknown_count": availability_counts["unknown"],
            "capability_unfulfillable_request_count": event_activity_counts.get(
                "capability_request_unfulfillable", 0
            ),
            "capability_limitation_detected_count": event_activity_counts.get(
                "capability_limitation_detected", 0
            ),
        }

    @staticmethod
    def _persona_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        capability_boundary_count = 0
        persona_source_by_type: dict[str, int] = {}
        persona_source_by_risk_level: dict[str, int] = {}
        persona_private_source_count = 0
        persona_candidate_canonical_import_enabled_count = 0
        personal_overlay_safe_projection_count = 0
        personal_overlay_boundary_failed_count = 0
        personal_mode_private_count = 0
        personal_mode_boundary_by_type: dict[str, int] = {}
        personal_mode_by_type: dict[str, int] = {}
        personal_mode_capability_available_now_count = 0
        personal_mode_capability_requires_permission_count = 0
        personal_mode_capability_not_implemented_count = 0
        personal_runtime_binding_by_kind: dict[str, int] = {}
        personal_context_ingress_by_type: dict[str, int] = {}
        personal_runtime_capability_available_now_count = 0
        personal_runtime_capability_requires_permission_count = 0
        personal_runtime_capability_not_implemented_count = 0
        personal_mode_prompt_context_activation_count = 0
        personal_conformance_passed_count = 0
        personal_conformance_failed_count = 0
        personal_conformance_needs_review_count = 0
        personal_conformance_inconclusive_count = 0
        personal_conformance_failed_finding_count = 0
        personal_conformance_warning_finding_count = 0
        personal_conformance_by_rule_type: dict[str, int] = {}
        personal_conformance_score_total = 0.0
        personal_conformance_score_count = 0
        personal_smoke_test_passed_count = 0
        personal_smoke_test_failed_count = 0
        personal_smoke_test_needs_review_count = 0
        personal_smoke_test_failed_assertion_count = 0
        personal_smoke_test_warning_assertion_count = 0
        personal_smoke_test_by_scenario_type: dict[str, int] = {}
        personal_smoke_test_score_total = 0.0
        personal_smoke_test_score_count = 0
        personal_directory_configured_count = 0
        personal_directory_missing_count = 0
        personal_runtime_health_failed_count = 0
        personal_runtime_health_warning_count = 0
        personal_prompt_activation_prompt_context_only_count = 0
        personal_prompt_activation_unsafe_finding_count = 0
        for item in view.objects:
            if item.object_type == "persona_profile":
                capability_boundary_count += len(
                    item.object_attrs.get("capability_boundaries") or []
                )
            if item.object_type == "persona_instruction_artifact":
                if item.object_attrs.get("artifact_type") == "capability_boundary":
                    capability_boundary_count += 1
            if item.object_type == "persona_source":
                source_type = str(item.object_attrs.get("source_type") or "unknown")
                persona_source_by_type[source_type] = persona_source_by_type.get(source_type, 0) + 1
                if bool(item.object_attrs.get("private")):
                    persona_private_source_count += 1
            if item.object_type == "persona_source_risk_note":
                risk_level = str(item.object_attrs.get("risk_level") or "unknown")
                persona_source_by_risk_level[risk_level] = (
                    persona_source_by_risk_level.get(risk_level, 0) + 1
                )
            if item.object_type in {
                "persona_source_ingestion_candidate",
                "persona_projection_candidate",
            }:
                if bool(item.object_attrs.get("canonical_import_enabled")):
                    persona_candidate_canonical_import_enabled_count += 1
            if item.object_type == "personal_projection_ref":
                if bool(item.object_attrs.get("safe_for_prompt")):
                    personal_overlay_safe_projection_count += 1
            if item.object_type == "personal_overlay_boundary_finding":
                if item.object_attrs.get("status") == "failed":
                    personal_overlay_boundary_failed_count += 1
            if item.object_type == "personal_core_profile":
                if bool(item.object_attrs.get("private")):
                    personal_mode_private_count += 1
            if item.object_type == "personal_mode_profile":
                mode_type = str(item.object_attrs.get("mode_type") or "unknown")
                personal_mode_by_type[mode_type] = personal_mode_by_type.get(mode_type, 0) + 1
                if bool(item.object_attrs.get("private")):
                    personal_mode_private_count += 1
            if item.object_type == "personal_mode_boundary":
                boundary_type = str(item.object_attrs.get("boundary_type") or "unknown")
                personal_mode_boundary_by_type[boundary_type] = (
                    personal_mode_boundary_by_type.get(boundary_type, 0) + 1
                )
            if item.object_type == "personal_mode_capability_binding":
                availability = str(item.object_attrs.get("availability") or "unknown")
                if availability == "available_now":
                    personal_mode_capability_available_now_count += 1
                if bool(item.object_attrs.get("requires_permission")):
                    personal_mode_capability_requires_permission_count += 1
                if availability == "not_implemented":
                    personal_mode_capability_not_implemented_count += 1
            if item.object_type == "personal_runtime_binding":
                runtime_kind = str(item.object_attrs.get("runtime_kind") or "unknown")
                context_ingress = str(item.object_attrs.get("context_ingress") or "unknown")
                personal_runtime_binding_by_kind[runtime_kind] = (
                    personal_runtime_binding_by_kind.get(runtime_kind, 0) + 1
                )
                personal_context_ingress_by_type[context_ingress] = (
                    personal_context_ingress_by_type.get(context_ingress, 0) + 1
                )
            if item.object_type == "personal_runtime_capability_binding":
                availability = str(item.object_attrs.get("availability") or "unknown")
                if availability == "available_now":
                    personal_runtime_capability_available_now_count += 1
                if bool(item.object_attrs.get("requires_permission")):
                    personal_runtime_capability_requires_permission_count += 1
                if availability == "not_implemented":
                    personal_runtime_capability_not_implemented_count += 1
            if item.object_type == "personal_mode_activation_result":
                if item.object_attrs.get("activation_scope") == "prompt_context_only":
                    personal_mode_prompt_context_activation_count += 1
            if item.object_type == "personal_conformance_finding":
                rule_type = str(item.object_attrs.get("rule_type") or "unknown")
                personal_conformance_by_rule_type[rule_type] = (
                    personal_conformance_by_rule_type.get(rule_type, 0) + 1
                )
                status = str(item.object_attrs.get("status") or "")
                if status in {"failed", "error"}:
                    personal_conformance_failed_finding_count += 1
                if status == "warning":
                    personal_conformance_warning_finding_count += 1
            if item.object_type == "personal_conformance_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "passed":
                    personal_conformance_passed_count += 1
                if status == "failed":
                    personal_conformance_failed_count += 1
                if status == "needs_review":
                    personal_conformance_needs_review_count += 1
                if status == "inconclusive":
                    personal_conformance_inconclusive_count += 1
                score = item.object_attrs.get("score")
                if isinstance(score, (int, float)):
                    personal_conformance_score_total += float(score)
                    personal_conformance_score_count += 1
            if item.object_type == "personal_smoke_test_scenario":
                scenario_type = str(item.object_attrs.get("scenario_type") or "unknown")
                personal_smoke_test_by_scenario_type[scenario_type] = (
                    personal_smoke_test_by_scenario_type.get(scenario_type, 0) + 1
                )
            if item.object_type == "personal_smoke_test_assertion":
                status = str(item.object_attrs.get("status") or "")
                if status in {"failed", "error"}:
                    personal_smoke_test_failed_assertion_count += 1
                if status == "warning":
                    personal_smoke_test_warning_assertion_count += 1
            if item.object_type == "personal_smoke_test_result":
                status = str(item.object_attrs.get("status") or "")
                if status == "passed":
                    personal_smoke_test_passed_count += 1
                if status == "failed":
                    personal_smoke_test_failed_count += 1
                if status == "needs_review":
                    personal_smoke_test_needs_review_count += 1
                score = item.object_attrs.get("score")
                if isinstance(score, (int, float)):
                    personal_smoke_test_score_total += float(score)
                    personal_smoke_test_score_count += 1
            if item.object_type == "personal_runtime_config_view":
                if bool(item.object_attrs.get("personal_directory_configured")):
                    personal_directory_configured_count += 1
                else:
                    personal_directory_missing_count += 1
            if item.object_type == "personal_runtime_health_check":
                status = str(item.object_attrs.get("status") or "")
                if status in {"failed", "error"}:
                    personal_runtime_health_failed_count += 1
                if status == "warning":
                    personal_runtime_health_warning_count += 1
            if item.object_type == "personal_prompt_activation_result":
                if item.object_attrs.get("activation_scope") == "prompt_context_only":
                    personal_prompt_activation_prompt_context_only_count += 1
            if item.object_type == "personal_prompt_activation_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "")
                status = str(item.object_attrs.get("status") or "")
                if status in {"failed", "error"} or finding_type in {
                    "unsafe_overlay_projection",
                    "private_source_body_detected",
                }:
                    personal_prompt_activation_unsafe_finding_count += 1
        return {
            "soul_identity_count": object_type_counts.get("soul_identity", 0),
            "persona_profile_count": object_type_counts.get("persona_profile", 0),
            "persona_instruction_artifact_count": object_type_counts.get(
                "persona_instruction_artifact", 0
            ),
            "agent_role_binding_count": object_type_counts.get("agent_role_binding", 0),
            "persona_loadout_count": object_type_counts.get("persona_loadout", 0),
            "persona_projection_count": object_type_counts.get("persona_projection", 0),
            "persona_capability_boundary_count": capability_boundary_count,
            "persona_source_count": object_type_counts.get("persona_source", 0),
            "persona_source_manifest_count": object_type_counts.get(
                "persona_source_manifest", 0
            ),
            "persona_source_ingestion_candidate_count": object_type_counts.get(
                "persona_source_ingestion_candidate", 0
            ),
            "persona_source_validation_result_count": object_type_counts.get(
                "persona_source_validation_result", 0
            ),
            "persona_assimilation_draft_count": object_type_counts.get(
                "persona_assimilation_draft", 0
            ),
            "persona_projection_candidate_count": object_type_counts.get(
                "persona_projection_candidate", 0
            ),
            "persona_source_risk_note_count": object_type_counts.get(
                "persona_source_risk_note", 0
            ),
            "persona_source_valid_count": sum(
                1
                for item in view.objects
                if item.object_type == "persona_source_validation_result"
                and item.object_attrs.get("status") == "valid"
            ),
            "persona_source_invalid_count": sum(
                1
                for item in view.objects
                if item.object_type == "persona_source_validation_result"
                and item.object_attrs.get("status") == "invalid"
            ),
            "persona_source_needs_review_count": sum(
                1
                for item in view.objects
                if item.object_type == "persona_source_validation_result"
                and item.object_attrs.get("status") == "needs_review"
            ),
            "persona_candidate_pending_review_count": sum(
                1
                for item in view.objects
                if item.object_type == "persona_source_ingestion_candidate"
                and item.object_attrs.get("review_status") == "pending_review"
            ),
            "persona_candidate_canonical_import_enabled_count": persona_candidate_canonical_import_enabled_count,
            "persona_source_by_type": persona_source_by_type,
            "persona_source_by_risk_level": persona_source_by_risk_level,
            "persona_private_source_count": persona_private_source_count,
            "personal_directory_config_count": object_type_counts.get(
                "personal_directory_config", 0
            ),
            "personal_directory_manifest_count": object_type_counts.get(
                "personal_directory_manifest", 0
            ),
            "personal_projection_ref_count": object_type_counts.get(
                "personal_projection_ref", 0
            ),
            "personal_overlay_load_request_count": object_type_counts.get(
                "personal_overlay_load_request", 0
            ),
            "personal_overlay_load_result_count": object_type_counts.get(
                "personal_overlay_load_result", 0
            ),
            "personal_overlay_boundary_finding_count": object_type_counts.get(
                "personal_overlay_boundary_finding", 0
            ),
            "personal_overlay_load_denied_count": event_activity_counts.get(
                "personal_overlay_load_denied", 0
            ),
            "personal_overlay_boundary_failed_count": personal_overlay_boundary_failed_count,
            "personal_projection_attached_to_prompt_count": event_activity_counts.get(
                "personal_projection_attached_to_prompt", 0
            ),
            "personal_overlay_safe_projection_count": personal_overlay_safe_projection_count,
            "personal_core_profile_count": object_type_counts.get(
                "personal_core_profile", 0
            ),
            "personal_mode_profile_count": object_type_counts.get(
                "personal_mode_profile", 0
            ),
            "personal_mode_boundary_count": object_type_counts.get(
                "personal_mode_boundary", 0
            ),
            "personal_mode_capability_binding_count": object_type_counts.get(
                "personal_mode_capability_binding", 0
            ),
            "personal_mode_loadout_count": object_type_counts.get(
                "personal_mode_loadout", 0
            ),
            "personal_mode_loadout_draft_count": object_type_counts.get(
                "personal_mode_loadout_draft", 0
            ),
            "personal_mode_private_count": personal_mode_private_count,
            "personal_mode_boundary_by_type": personal_mode_boundary_by_type,
            "personal_mode_by_type": personal_mode_by_type,
            "personal_mode_capability_available_now_count": (
                personal_mode_capability_available_now_count
            ),
            "personal_mode_capability_requires_permission_count": (
                personal_mode_capability_requires_permission_count
            ),
            "personal_mode_capability_not_implemented_count": (
                personal_mode_capability_not_implemented_count
            ),
            "personal_mode_selection_count": object_type_counts.get(
                "personal_mode_selection", 0
            ),
            "personal_runtime_binding_count": object_type_counts.get(
                "personal_runtime_binding", 0
            ),
            "personal_runtime_capability_binding_count": object_type_counts.get(
                "personal_runtime_capability_binding", 0
            ),
            "personal_mode_activation_request_count": object_type_counts.get(
                "personal_mode_activation_request", 0
            ),
            "personal_mode_activation_result_count": object_type_counts.get(
                "personal_mode_activation_result", 0
            ),
            "personal_mode_activation_denied_count": event_activity_counts.get(
                "personal_mode_activation_denied", 0
            ),
            "personal_mode_prompt_context_activation_count": (
                personal_mode_prompt_context_activation_count
            ),
            "personal_runtime_binding_by_kind": personal_runtime_binding_by_kind,
            "personal_context_ingress_by_type": personal_context_ingress_by_type,
            "personal_runtime_capability_available_now_count": (
                personal_runtime_capability_available_now_count
            ),
            "personal_runtime_capability_requires_permission_count": (
                personal_runtime_capability_requires_permission_count
            ),
            "personal_runtime_capability_not_implemented_count": (
                personal_runtime_capability_not_implemented_count
            ),
            "personal_conformance_contract_count": object_type_counts.get(
                "personal_conformance_contract", 0
            ),
            "personal_conformance_rule_count": object_type_counts.get(
                "personal_conformance_rule", 0
            ),
            "personal_conformance_run_count": object_type_counts.get(
                "personal_conformance_run", 0
            ),
            "personal_conformance_finding_count": object_type_counts.get(
                "personal_conformance_finding", 0
            ),
            "personal_conformance_result_count": object_type_counts.get(
                "personal_conformance_result", 0
            ),
            "personal_conformance_passed_count": personal_conformance_passed_count,
            "personal_conformance_failed_count": personal_conformance_failed_count,
            "personal_conformance_needs_review_count": personal_conformance_needs_review_count,
            "personal_conformance_inconclusive_count": personal_conformance_inconclusive_count,
            "personal_conformance_failed_finding_count": personal_conformance_failed_finding_count,
            "personal_conformance_warning_finding_count": personal_conformance_warning_finding_count,
            "personal_conformance_by_rule_type": personal_conformance_by_rule_type,
            "average_personal_conformance_score": (
                personal_conformance_score_total / personal_conformance_score_count
                if personal_conformance_score_count
                else None
            ),
            "personal_smoke_test_scenario_count": object_type_counts.get(
                "personal_smoke_test_scenario", 0
            ),
            "personal_smoke_test_case_count": object_type_counts.get(
                "personal_smoke_test_case", 0
            ),
            "personal_smoke_test_run_count": object_type_counts.get(
                "personal_smoke_test_run", 0
            ),
            "personal_smoke_test_observation_count": object_type_counts.get(
                "personal_smoke_test_observation", 0
            ),
            "personal_smoke_test_assertion_count": object_type_counts.get(
                "personal_smoke_test_assertion", 0
            ),
            "personal_smoke_test_result_count": object_type_counts.get(
                "personal_smoke_test_result", 0
            ),
            "personal_smoke_test_passed_count": personal_smoke_test_passed_count,
            "personal_smoke_test_failed_count": personal_smoke_test_failed_count,
            "personal_smoke_test_needs_review_count": personal_smoke_test_needs_review_count,
            "personal_smoke_test_failed_assertion_count": personal_smoke_test_failed_assertion_count,
            "personal_smoke_test_warning_assertion_count": personal_smoke_test_warning_assertion_count,
            "personal_smoke_test_by_scenario_type": personal_smoke_test_by_scenario_type,
            "average_personal_smoke_test_score": (
                personal_smoke_test_score_total / personal_smoke_test_score_count
                if personal_smoke_test_score_count
                else None
            ),
            "personal_runtime_config_view_count": object_type_counts.get(
                "personal_runtime_config_view", 0
            ),
            "personal_runtime_status_snapshot_count": object_type_counts.get(
                "personal_runtime_status_snapshot", 0
            ),
            "personal_runtime_health_check_count": object_type_counts.get(
                "personal_runtime_health_check", 0
            ),
            "personal_runtime_diagnostic_count": object_type_counts.get(
                "personal_runtime_diagnostic", 0
            ),
            "personal_cli_command_result_count": object_type_counts.get(
                "personal_cli_command_result", 0
            ),
            "personal_directory_configured_count": personal_directory_configured_count,
            "personal_directory_missing_count": personal_directory_missing_count,
            "personal_cli_validate_run_count": sum(
                1
                for item in view.objects
                if item.object_type == "personal_cli_command_result"
                and item.object_attrs.get("command_name") == "personal validate"
            ),
            "personal_cli_smoke_run_count": sum(
                1
                for item in view.objects
                if item.object_type == "personal_cli_command_result"
                and item.object_attrs.get("command_name") == "personal smoke"
            ),
            "personal_runtime_health_failed_count": personal_runtime_health_failed_count,
            "personal_runtime_health_warning_count": personal_runtime_health_warning_count,
            "personal_prompt_activation_config_count": object_type_counts.get(
                "personal_prompt_activation_config", 0
            ),
            "personal_prompt_activation_request_count": object_type_counts.get(
                "personal_prompt_activation_request", 0
            ),
            "personal_prompt_activation_block_count": object_type_counts.get(
                "personal_prompt_activation_block", 0
            ),
            "personal_prompt_activation_result_count": object_type_counts.get(
                "personal_prompt_activation_result", 0
            ),
            "personal_prompt_activation_finding_count": object_type_counts.get(
                "personal_prompt_activation_finding", 0
            ),
            "personal_prompt_activation_attached_count": event_activity_counts.get(
                "personal_prompt_activation_attached", 0
            ),
            "personal_prompt_activation_skipped_count": event_activity_counts.get(
                "personal_prompt_activation_skipped", 0
            ),
            "personal_prompt_activation_denied_count": event_activity_counts.get(
                "personal_prompt_activation_denied", 0
            ),
            "personal_prompt_activation_prompt_context_only_count": (
                personal_prompt_activation_prompt_context_only_count
            ),
            "personal_prompt_activation_unsafe_finding_count": (
                personal_prompt_activation_unsafe_finding_count
            ),
            "persona_projection_attached_to_prompt_count": event_activity_counts.get(
                "persona_projection_attached_to_prompt", 0
            ),
            "soul_identity_registered_count": event_activity_counts.get(
                "soul_identity_registered", 0
            ),
            "persona_profile_registered_count": event_activity_counts.get(
                "persona_profile_registered", 0
            ),
            "persona_instruction_artifact_registered_count": event_activity_counts.get(
                "persona_instruction_artifact_registered", 0
            ),
            "agent_role_binding_registered_count": event_activity_counts.get(
                "agent_role_binding_registered", 0
            ),
            "persona_loadout_created_count": event_activity_counts.get(
                "persona_loadout_created", 0
            ),
            "persona_projection_created_count": event_activity_counts.get(
                "persona_projection_created", 0
            ),
            "persona_capability_boundary_attached_count": event_activity_counts.get(
                "persona_capability_boundary_attached", 0
            ),
        }

    @staticmethod
    def _tool_registry_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        tool_type_distribution: dict[str, int] = {}
        risk_level_distribution: dict[str, int] = {}
        for item in view.objects:
            if item.object_type != "tool_descriptor":
                continue
            tool_type = str(item.object_attrs.get("tool_type") or "other")
            risk_level = str(item.object_attrs.get("risk_level") or "unknown")
            tool_type_distribution[tool_type] = tool_type_distribution.get(tool_type, 0) + 1
            risk_level_distribution[risk_level] = risk_level_distribution.get(risk_level, 0) + 1
        return {
            "tool_descriptor_count": object_type_counts.get("tool_descriptor", 0),
            "tool_registry_snapshot_count": object_type_counts.get("tool_registry_snapshot", 0),
            "tool_policy_note_count": object_type_counts.get("tool_policy_note", 0),
            "tool_risk_annotation_count": object_type_counts.get("tool_risk_annotation", 0),
            "tool_descriptor_registered_count": event_activity_counts.get("tool_descriptor_registered", 0),
            "tool_registry_snapshot_created_count": event_activity_counts.get("tool_registry_snapshot_created", 0),
            "tool_policy_note_registered_count": event_activity_counts.get("tool_policy_note_registered", 0),
            "tool_risk_annotation_registered_count": event_activity_counts.get("tool_risk_annotation_registered", 0),
            "tool_registry_view_written_count": event_activity_counts.get("tool_registry_view_written", 0),
            "tool_policy_view_written_count": event_activity_counts.get("tool_policy_view_written", 0),
            "tool_type_distribution": tool_type_distribution,
            "tool_risk_level_distribution": risk_level_distribution,
        }

    @staticmethod
    def _verification_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        contracts_by_id: dict[str, str] = {}
        targets_by_id: dict[str, str] = {}
        for item in view.objects:
            if item.object_type == "verification_contract":
                contract_type = str(item.object_attrs.get("contract_type") or "unknown")
                contracts_by_id[item.object_id] = contract_type
            if item.object_type == "verification_target":
                target_type = str(item.object_attrs.get("target_type") or "unknown")
                targets_by_id[item.object_id] = target_type

        status_counts = {
            "passed": 0,
            "failed": 0,
            "inconclusive": 0,
            "skipped": 0,
            "error": 0,
        }
        by_contract_type: dict[str, int] = {}
        by_target_type: dict[str, int] = {}
        read_only_skill_run_count = 0
        skill_passed_count = 0
        skill_failed_count = 0
        contract_type_by_read_only_run: dict[str, int] = {}
        skill_run_by_name: dict[str, int] = {}
        for item in view.objects:
            if item.object_type != "verification_run":
                continue
            if not item.object_attrs.get("run_attrs", {}).get("read_only_verification_skill"):
                continue
            read_only_skill_run_count += 1
            contract_type = contracts_by_id.get(str(item.object_attrs.get("contract_id") or ""), "unknown")
            contract_type_by_read_only_run[contract_type] = contract_type_by_read_only_run.get(contract_type, 0) + 1
            skill_name = str(item.object_attrs.get("run_attrs", {}).get("skill_name") or "unknown")
            skill_run_by_name[skill_name] = skill_run_by_name.get(skill_name, 0) + 1
        for item in view.objects:
            if item.object_type != "verification_result":
                continue
            status = str(item.object_attrs.get("status") or "unknown")
            if status in status_counts:
                status_counts[status] += 1
            contract_id = str(item.object_attrs.get("contract_id") or "")
            target_id = str(item.object_attrs.get("target_id") or "")
            contract_type = contracts_by_id.get(contract_id, "unknown")
            target_type = targets_by_id.get(target_id, "unknown")
            by_contract_type[contract_type] = by_contract_type.get(contract_type, 0) + 1
            by_target_type[target_type] = by_target_type.get(target_type, 0) + 1
            if item.object_attrs.get("result_attrs", {}).get("read_only_verification_skill"):
                if status == "passed":
                    skill_passed_count += 1
                if status == "failed":
                    skill_failed_count += 1

        return {
            "verification_contract_count": object_type_counts.get("verification_contract", 0),
            "verification_target_count": object_type_counts.get("verification_target", 0),
            "verification_requirement_count": object_type_counts.get("verification_requirement", 0),
            "verification_run_count": object_type_counts.get("verification_run", 0),
            "verification_evidence_count": object_type_counts.get("verification_evidence", 0),
            "verification_result_count": object_type_counts.get("verification_result", 0),
            "verification_passed_count": status_counts["passed"],
            "verification_failed_count": status_counts["failed"],
            "verification_inconclusive_count": status_counts["inconclusive"],
            "verification_skipped_count": status_counts["skipped"],
            "verification_error_count": status_counts["error"],
            "verification_contract_registered_count": event_activity_counts.get("verification_contract_registered", 0),
            "verification_target_registered_count": event_activity_counts.get("verification_target_registered", 0),
            "verification_requirement_registered_count": event_activity_counts.get("verification_requirement_registered", 0),
            "verification_run_started_count": event_activity_counts.get("verification_run_started", 0),
            "verification_run_completed_count": event_activity_counts.get("verification_run_completed", 0),
            "verification_evidence_recorded_count": event_activity_counts.get("verification_evidence_recorded", 0),
            "verification_result_recorded_count": event_activity_counts.get("verification_result_recorded", 0),
            "verification_result_by_contract_type": by_contract_type,
            "verification_result_by_target_type": by_target_type,
            "read_only_verification_skill_run_count": read_only_skill_run_count,
            "file_existence_verification_count": contract_type_by_read_only_run.get("file_existence", 0),
            "tool_availability_verification_count": contract_type_by_read_only_run.get("tool_availability", 0),
            "ocel_shape_verification_count": contract_type_by_read_only_run.get("ocel_shape", 0),
            "materialized_view_warning_verification_count": skill_run_by_name.get("verify_materialized_view_warning", 0),
            "tool_registry_view_warning_verification_count": skill_run_by_name.get("verify_tool_registry_view_warning", 0),
            "verification_skill_passed_count": skill_passed_count,
            "verification_skill_failed_count": skill_failed_count,
            "read_only_verification_skill_runs_by_name": skill_run_by_name,
        }

    @staticmethod
    def _process_outcome_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        contracts_by_id: dict[str, str] = {}
        targets_by_id: dict[str, str] = {}
        for item in view.objects:
            if item.object_type == "process_outcome_contract":
                contracts_by_id[item.object_id] = str(item.object_attrs.get("contract_type") or "unknown")
            if item.object_type == "process_outcome_target":
                targets_by_id[item.object_id] = str(item.object_attrs.get("target_type") or "unknown")

        status_counts = {
            "success": 0,
            "partial_success": 0,
            "failed": 0,
            "inconclusive": 0,
            "needs_review": 0,
            "skipped": 0,
            "error": 0,
        }
        by_contract_type: dict[str, int] = {}
        by_target_type: dict[str, int] = {}
        coverages: list[float] = []
        scores: list[float] = []
        for item in view.objects:
            if item.object_type != "process_outcome_evaluation":
                continue
            status = str(item.object_attrs.get("outcome_status") or "unknown")
            if status in status_counts:
                status_counts[status] += 1
            contract_type = contracts_by_id.get(str(item.object_attrs.get("contract_id") or ""), "unknown")
            target_type = targets_by_id.get(str(item.object_attrs.get("target_id") or ""), "unknown")
            by_contract_type[contract_type] = by_contract_type.get(contract_type, 0) + 1
            by_target_type[target_type] = by_target_type.get(target_type, 0) + 1
            evidence_coverage = item.object_attrs.get("evidence_coverage")
            score = item.object_attrs.get("score")
            if evidence_coverage is not None:
                coverages.append(float(evidence_coverage))
            if score is not None:
                scores.append(float(score))

        return {
            "process_outcome_contract_count": object_type_counts.get("process_outcome_contract", 0),
            "process_outcome_criterion_count": object_type_counts.get("process_outcome_criterion", 0),
            "process_outcome_target_count": object_type_counts.get("process_outcome_target", 0),
            "process_outcome_signal_count": object_type_counts.get("process_outcome_signal", 0),
            "process_outcome_evaluation_count": object_type_counts.get("process_outcome_evaluation", 0),
            "process_outcome_success_count": status_counts["success"],
            "process_outcome_partial_success_count": status_counts["partial_success"],
            "process_outcome_failed_count": status_counts["failed"],
            "process_outcome_inconclusive_count": status_counts["inconclusive"],
            "process_outcome_needs_review_count": status_counts["needs_review"],
            "process_outcome_skipped_count": status_counts["skipped"],
            "process_outcome_error_count": status_counts["error"],
            "process_outcome_contract_registered_count": event_activity_counts.get("process_outcome_contract_registered", 0),
            "process_outcome_criterion_registered_count": event_activity_counts.get("process_outcome_criterion_registered", 0),
            "process_outcome_target_registered_count": event_activity_counts.get("process_outcome_target_registered", 0),
            "process_outcome_signal_recorded_count": event_activity_counts.get("process_outcome_signal_recorded", 0),
            "process_outcome_evaluation_recorded_count": event_activity_counts.get("process_outcome_evaluation_recorded", 0),
            "process_outcome_by_contract_type": by_contract_type,
            "process_outcome_by_target_type": by_target_type,
            "average_evidence_coverage": round(sum(coverages) / len(coverages), 6) if coverages else None,
            "average_outcome_score": round(sum(scores) / len(scores), 6) if scores else None,
        }

    @staticmethod
    def _permission_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        request_by_type: dict[str, int] = {}
        request_by_operation: dict[str, int] = {}
        decision_counts = {"allow": 0, "deny": 0, "ask": 0, "defer": 0, "inconclusive": 0}
        resolution_counts = {"allow": 0, "deny": 0, "ask": 0, "defer": 0, "inconclusive": 0}
        active_grants = 0
        session_active_grants = 0
        session_expired_grants = 0
        session_revoked_grants = 0
        session_denials = 0
        session_pending_requests = 0
        for item in view.objects:
            if item.object_type == "permission_request":
                request_type = str(item.object_attrs.get("request_type") or "unknown")
                operation = str(item.object_attrs.get("operation") or "unknown")
                request_by_type[request_type] = request_by_type.get(request_type, 0) + 1
                request_by_operation[operation] = request_by_operation.get(operation, 0) + 1
                if item.object_attrs.get("session_id") and item.object_attrs.get("status") == "pending":
                    session_pending_requests += 1
            if item.object_type == "permission_decision":
                decision = str(item.object_attrs.get("decision") or "unknown")
                if decision in decision_counts:
                    decision_counts[decision] += 1
            if item.object_type == "permission_grant":
                if item.object_attrs.get("status") == "active":
                    active_grants += 1
                if item.object_attrs.get("session_id"):
                    if item.object_attrs.get("status") == "active":
                        session_active_grants += 1
                    if item.object_attrs.get("status") == "expired":
                        session_expired_grants += 1
                    if item.object_attrs.get("status") == "revoked":
                        session_revoked_grants += 1
            if item.object_type == "permission_denial" and item.object_attrs.get("session_id"):
                session_denials += 1
            if item.object_type == "session_permission_resolution":
                resolved = str(item.object_attrs.get("resolved_decision") or "unknown")
                if resolved in resolution_counts:
                    resolution_counts[resolved] += 1
        return {
            "permission_scope_count": object_type_counts.get("permission_scope", 0),
            "permission_request_count": object_type_counts.get("permission_request", 0),
            "permission_decision_count": object_type_counts.get("permission_decision", 0),
            "permission_grant_count": object_type_counts.get("permission_grant", 0),
            "permission_denial_count": object_type_counts.get("permission_denial", 0),
            "permission_policy_note_count": object_type_counts.get("permission_policy_note", 0),
            "permission_request_by_type": request_by_type,
            "permission_request_by_operation": request_by_operation,
            "permission_decision_allow_count": decision_counts["allow"],
            "permission_decision_deny_count": decision_counts["deny"],
            "permission_decision_ask_count": decision_counts["ask"],
            "permission_decision_defer_count": decision_counts["defer"],
            "permission_decision_inconclusive_count": decision_counts["inconclusive"],
            "permission_grant_active_count": active_grants,
            "session_permission_context_count": object_type_counts.get("session_permission_context", 0),
            "session_permission_snapshot_count": object_type_counts.get("session_permission_snapshot", 0),
            "session_permission_resolution_count": object_type_counts.get("session_permission_resolution", 0),
            "session_permission_resolution_allow_count": resolution_counts["allow"],
            "session_permission_resolution_deny_count": resolution_counts["deny"],
            "session_permission_resolution_ask_count": resolution_counts["ask"],
            "session_permission_resolution_defer_count": resolution_counts["defer"],
            "session_permission_resolution_inconclusive_count": resolution_counts["inconclusive"],
            "session_active_grant_count": session_active_grants,
            "session_expired_grant_count": session_expired_grants,
            "session_revoked_grant_count": session_revoked_grants,
            "session_denial_count": session_denials,
            "session_pending_permission_request_count": session_pending_requests,
            "permission_scope_registered_count": event_activity_counts.get("permission_scope_registered", 0),
            "permission_request_created_count": event_activity_counts.get("permission_request_created", 0),
            "permission_decision_recorded_count": event_activity_counts.get("permission_decision_recorded", 0),
            "permission_grant_recorded_count": event_activity_counts.get("permission_grant_recorded", 0),
            "permission_denial_recorded_count": event_activity_counts.get("permission_denial_recorded", 0),
            "permission_policy_note_registered_count": event_activity_counts.get("permission_policy_note_registered", 0),
            "session_permission_context_created_count": event_activity_counts.get("session_permission_context_created", 0),
            "session_permission_request_created_count": event_activity_counts.get("session_permission_request_created", 0),
            "session_permission_grant_attached_count": event_activity_counts.get("session_permission_grant_attached", 0),
            "session_permission_denial_attached_count": event_activity_counts.get("session_permission_denial_attached", 0),
            "session_permission_snapshot_created_count": event_activity_counts.get("session_permission_snapshot_created", 0),
            "session_permission_resolution_recorded_count": event_activity_counts.get("session_permission_resolution_recorded", 0),
        }

    @staticmethod
    def _workspace_write_sandbox_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        decision_counts = {"allowed": 0, "denied": 0, "needs_review": 0, "inconclusive": 0, "error": 0}
        violation_counts = {"outside_workspace": 0, "protected_path": 0, "denied_path": 0}
        for item in view.objects:
            if item.object_type == "workspace_write_sandbox_decision":
                decision = str(item.object_attrs.get("decision") or "unknown")
                if decision in decision_counts:
                    decision_counts[decision] += 1
            if item.object_type == "workspace_write_sandbox_violation":
                violation_type = str(item.object_attrs.get("violation_type") or "unknown")
                if violation_type in violation_counts:
                    violation_counts[violation_type] += 1
        return {
            "workspace_root_count": object_type_counts.get("workspace_root", 0),
            "workspace_write_boundary_count": object_type_counts.get("workspace_write_boundary", 0),
            "workspace_write_intent_count": object_type_counts.get("workspace_write_intent", 0),
            "workspace_write_sandbox_decision_count": object_type_counts.get("workspace_write_sandbox_decision", 0),
            "workspace_write_sandbox_violation_count": object_type_counts.get("workspace_write_sandbox_violation", 0),
            "workspace_write_allowed_count": decision_counts["allowed"],
            "workspace_write_denied_count": decision_counts["denied"],
            "workspace_write_needs_review_count": decision_counts["needs_review"],
            "workspace_write_inconclusive_count": decision_counts["inconclusive"],
            "workspace_write_error_count": decision_counts["error"],
            "workspace_write_outside_workspace_violation_count": violation_counts["outside_workspace"],
            "workspace_write_protected_path_violation_count": violation_counts["protected_path"],
            "workspace_write_denied_path_violation_count": violation_counts["denied_path"],
            "workspace_root_registered_count": event_activity_counts.get("workspace_root_registered", 0),
            "workspace_write_boundary_registered_count": event_activity_counts.get("workspace_write_boundary_registered", 0),
            "workspace_write_intent_created_count": event_activity_counts.get("workspace_write_intent_created", 0),
            "workspace_write_sandbox_evaluated_count": event_activity_counts.get("workspace_write_sandbox_evaluated", 0),
            "workspace_write_sandbox_decision_recorded_count": event_activity_counts.get("workspace_write_sandbox_decision_recorded", 0),
            "workspace_write_sandbox_violation_recorded_count": event_activity_counts.get("workspace_write_sandbox_violation_recorded", 0),
        }

    @staticmethod
    def _workspace_read_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        violation_counts = {
            "outside_workspace": 0,
            "path_traversal": 0,
            "binary_rejected": 0,
            "file_too_large": 0,
        }
        summary_completed_count = 0
        summary_failed_count = 0
        summary_unsupported_count = 0
        summary_candidate_pending_count = 0
        summary_by_input_kind: dict[str, int] = {}
        summary_finding_by_type: dict[str, int] = {}
        local_object_type_counts = dict(object_type_counts)
        for item in view.objects:
            local_object_type_counts[item.object_type] = local_object_type_counts.get(item.object_type, 0) + 1
            if item.object_type == "workspace_read_violation":
                violation_type = str(item.object_attrs.get("violation_type") or "unknown")
                if violation_type in violation_counts:
                    violation_counts[violation_type] += 1
            if item.object_type == "workspace_read_summary_result":
                status = str(item.object_attrs.get("status") or "")
                input_kind = str(item.object_attrs.get("input_kind") or "unknown")
                summary_by_input_kind[input_kind] = summary_by_input_kind.get(input_kind, 0) + 1
                if status == "completed":
                    summary_completed_count += 1
                if status in {"failed", "error"}:
                    summary_failed_count += 1
                if status == "unsupported":
                    summary_unsupported_count += 1
            if item.object_type == "workspace_read_summary_candidate":
                if str(item.object_attrs.get("review_status") or "") == "pending_review":
                    summary_candidate_pending_count += 1
            if item.object_type == "workspace_read_summary_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                summary_finding_by_type[finding_type] = summary_finding_by_type.get(finding_type, 0) + 1
        denied_count = (
            event_activity_counts.get("workspace_file_list_denied", 0)
            + event_activity_counts.get("workspace_text_file_read_denied", 0)
            + event_activity_counts.get("workspace_markdown_summary_denied", 0)
        )
        return {
            "workspace_read_root_count": local_object_type_counts.get("workspace_read_root", 0),
            "workspace_read_boundary_count": local_object_type_counts.get("workspace_read_boundary", 0),
            "workspace_file_list_request_count": local_object_type_counts.get("workspace_file_list_request", 0),
            "workspace_file_list_result_count": local_object_type_counts.get("workspace_file_list_result", 0),
            "workspace_text_file_read_request_count": local_object_type_counts.get("workspace_text_file_read_request", 0),
            "workspace_text_file_read_result_count": local_object_type_counts.get("workspace_text_file_read_result", 0),
            "workspace_markdown_summary_request_count": local_object_type_counts.get("workspace_markdown_summary_request", 0),
            "workspace_markdown_summary_result_count": local_object_type_counts.get("workspace_markdown_summary_result", 0),
            "workspace_read_violation_count": local_object_type_counts.get("workspace_read_violation", 0),
            "workspace_read_denied_count": denied_count,
            "workspace_read_binary_rejected_count": violation_counts["binary_rejected"],
            "workspace_read_oversize_rejected_count": violation_counts["file_too_large"],
            "workspace_read_outside_workspace_violation_count": violation_counts["outside_workspace"],
            "workspace_read_path_traversal_violation_count": violation_counts["path_traversal"],
            "workspace_read_root_registered_count": event_activity_counts.get("workspace_read_root_registered", 0),
            "workspace_read_boundary_registered_count": event_activity_counts.get("workspace_read_boundary_registered", 0),
            "workspace_file_list_requested_count": event_activity_counts.get("workspace_file_list_requested", 0),
            "workspace_file_list_completed_count": event_activity_counts.get("workspace_file_list_completed", 0),
            "workspace_file_list_denied_count": event_activity_counts.get("workspace_file_list_denied", 0),
            "workspace_text_file_read_requested_count": event_activity_counts.get("workspace_text_file_read_requested", 0),
            "workspace_text_file_read_completed_count": event_activity_counts.get("workspace_text_file_read_completed", 0),
            "workspace_text_file_read_denied_count": event_activity_counts.get("workspace_text_file_read_denied", 0),
            "workspace_markdown_summary_requested_count": event_activity_counts.get("workspace_markdown_summary_requested", 0),
            "workspace_markdown_summary_completed_count": event_activity_counts.get("workspace_markdown_summary_completed", 0),
            "workspace_markdown_summary_denied_count": event_activity_counts.get("workspace_markdown_summary_denied", 0),
            "workspace_read_violation_recorded_count": event_activity_counts.get("workspace_read_violation_recorded", 0),
            "workspace_read_summary_policy_count": local_object_type_counts.get("workspace_read_summary_policy", 0),
            "workspace_read_summary_request_count": local_object_type_counts.get("workspace_read_summary_request", 0),
            "workspace_read_summary_section_count": local_object_type_counts.get("workspace_read_summary_section", 0),
            "workspace_read_summary_result_count": local_object_type_counts.get("workspace_read_summary_result", 0),
            "workspace_read_summary_candidate_count": local_object_type_counts.get("workspace_read_summary_candidate", 0),
            "workspace_read_summary_finding_count": local_object_type_counts.get("workspace_read_summary_finding", 0),
            "workspace_read_summary_completed_count": summary_completed_count,
            "workspace_read_summary_failed_count": summary_failed_count,
            "workspace_read_summary_unsupported_count": summary_unsupported_count,
            "workspace_read_summary_candidate_pending_count": summary_candidate_pending_count,
            "workspace_read_summary_by_input_kind": summary_by_input_kind,
            "workspace_read_summary_finding_by_type": summary_finding_by_type,
        }

    @staticmethod
    def _personal_runtime_workbench_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        local_object_type_counts = dict(object_type_counts)
        for item in view.objects:
            local_object_type_counts[item.object_type] = local_object_type_counts.get(item.object_type, 0) + 1
        pending_review_count = 0
        blocked_activity_count = 0
        failed_activity_count = 0
        candidate_count = 0
        by_command: dict[str, int] = {}
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "personal_runtime_workbench_pending_item":
                if attrs.get("status") in {"pending_review", "needs_review", "open"}:
                    pending_review_count += 1
                if attrs.get("item_type") in {"promotion_candidate", "workspace_summary_candidate"}:
                    candidate_count += 1
            if item.object_type == "personal_runtime_workbench_recent_activity":
                if attrs.get("blocked") is True:
                    blocked_activity_count += 1
                if attrs.get("failed") is True:
                    failed_activity_count += 1
            if item.object_type == "personal_runtime_workbench_result":
                command = str(attrs.get("command_name") or "unknown")
                by_command[command] = by_command.get(command, 0) + 1
        return {
            "personal_runtime_workbench_snapshot_count": local_object_type_counts.get("personal_runtime_workbench_snapshot", 0),
            "personal_runtime_workbench_panel_count": local_object_type_counts.get("personal_runtime_workbench_panel", 0),
            "personal_runtime_workbench_pending_item_count": local_object_type_counts.get("personal_runtime_workbench_pending_item", 0),
            "personal_runtime_workbench_recent_activity_count": local_object_type_counts.get("personal_runtime_workbench_recent_activity", 0),
            "personal_runtime_workbench_finding_count": local_object_type_counts.get("personal_runtime_workbench_finding", 0),
            "personal_runtime_workbench_result_count": local_object_type_counts.get("personal_runtime_workbench_result", 0),
            "personal_runtime_workbench_pending_review_count": pending_review_count,
            "personal_runtime_workbench_blocked_activity_count": blocked_activity_count,
            "personal_runtime_workbench_failed_activity_count": failed_activity_count,
            "personal_runtime_workbench_candidate_count": candidate_count,
            "personal_runtime_workbench_by_command": by_command,
            "personal_runtime_workbench_snapshot_created_count": event_activity_counts.get("personal_runtime_workbench_snapshot_created", 0),
            "personal_runtime_workbench_result_recorded_count": event_activity_counts.get("personal_runtime_workbench_result_recorded", 0),
        }

    @staticmethod
    def _shell_network_pre_sandbox_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        shell_risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        network_risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        decision_counts = {
            "allow_recommended": 0,
            "deny_recommended": 0,
            "needs_review": 0,
            "inconclusive": 0,
            "error": 0,
        }
        violation_counts = {
            "destructive_command": 0,
            "network_access_risk": 0,
            "credential_exposure_risk": 0,
            "exfiltration_risk": 0,
        }
        for item in view.objects:
            if item.object_type == "shell_network_risk_assessment":
                risk_level = str(item.object_attrs.get("risk_level") or "unknown")
                intent_kind = str(item.object_attrs.get("intent_kind") or "unknown")
                if intent_kind == "shell_command" and risk_level in shell_risk_counts:
                    shell_risk_counts[risk_level] += 1
                if intent_kind == "network_access" and risk_level in network_risk_counts:
                    network_risk_counts[risk_level] += 1
            if item.object_type == "shell_network_pre_sandbox_decision":
                decision = str(item.object_attrs.get("decision") or "unknown")
                if decision in decision_counts:
                    decision_counts[decision] += 1
            if item.object_type == "shell_network_risk_violation":
                violation_type = str(item.object_attrs.get("violation_type") or "unknown")
                if violation_type in violation_counts:
                    violation_counts[violation_type] += 1
        return {
            "shell_command_intent_count": object_type_counts.get("shell_command_intent", 0),
            "network_access_intent_count": object_type_counts.get("network_access_intent", 0),
            "shell_network_risk_assessment_count": object_type_counts.get("shell_network_risk_assessment", 0),
            "shell_network_pre_sandbox_decision_count": object_type_counts.get("shell_network_pre_sandbox_decision", 0),
            "shell_network_risk_violation_count": object_type_counts.get("shell_network_risk_violation", 0),
            "shell_risk_low_count": shell_risk_counts["low"],
            "shell_risk_medium_count": shell_risk_counts["medium"],
            "shell_risk_high_count": shell_risk_counts["high"],
            "shell_risk_critical_count": shell_risk_counts["critical"],
            "network_risk_low_count": network_risk_counts["low"],
            "network_risk_medium_count": network_risk_counts["medium"],
            "network_risk_high_count": network_risk_counts["high"],
            "network_risk_critical_count": network_risk_counts["critical"],
            "pre_sandbox_allow_recommended_count": decision_counts["allow_recommended"],
            "pre_sandbox_deny_recommended_count": decision_counts["deny_recommended"],
            "pre_sandbox_needs_review_count": decision_counts["needs_review"],
            "pre_sandbox_inconclusive_count": decision_counts["inconclusive"],
            "pre_sandbox_error_count": decision_counts["error"],
            "destructive_command_violation_count": violation_counts["destructive_command"],
            "network_access_violation_count": violation_counts["network_access_risk"],
            "credential_exposure_violation_count": violation_counts["credential_exposure_risk"],
            "exfiltration_risk_violation_count": violation_counts["exfiltration_risk"],
            "shell_command_intent_created_count": event_activity_counts.get("shell_command_intent_created", 0),
            "network_access_intent_created_count": event_activity_counts.get("network_access_intent_created", 0),
            "shell_network_risk_assessment_recorded_count": event_activity_counts.get("shell_network_risk_assessment_recorded", 0),
            "shell_network_pre_sandbox_evaluated_count": event_activity_counts.get("shell_network_pre_sandbox_evaluated", 0),
            "shell_network_pre_sandbox_decision_recorded_count": event_activity_counts.get("shell_network_pre_sandbox_decision_recorded", 0),
            "shell_network_risk_violation_recorded_count": event_activity_counts.get("shell_network_risk_violation_recorded", 0),
        }

    @staticmethod
    def _delegation_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        by_isolation_mode: dict[str, int] = {}
        permission_reference_count = 0
        safety_reference_count = 0
        for item in view.objects:
            if item.object_type == "delegated_process_run":
                delegation_type = str(item.object_attrs.get("delegation_type") or "unknown")
                isolation_mode = str(item.object_attrs.get("isolation_mode") or "unknown")
                by_type[delegation_type] = by_type.get(delegation_type, 0) + 1
                by_isolation_mode[isolation_mode] = by_isolation_mode.get(isolation_mode, 0) + 1
            if item.object_type == "delegation_packet":
                permission_reference_count += len(item.object_attrs.get("permission_request_ids") or [])
                permission_reference_count += len(item.object_attrs.get("session_permission_resolution_ids") or [])
                safety_reference_count += len(item.object_attrs.get("workspace_write_sandbox_decision_ids") or [])
                safety_reference_count += len(item.object_attrs.get("shell_network_pre_sandbox_decision_ids") or [])
                safety_reference_count += len(item.object_attrs.get("process_outcome_evaluation_ids") or [])
        return {
            "delegation_packet_count": object_type_counts.get("delegation_packet", 0),
            "delegated_process_run_count": object_type_counts.get("delegated_process_run", 0),
            "delegation_result_count": object_type_counts.get("delegation_result", 0),
            "delegation_link_count": object_type_counts.get("delegation_link", 0),
            "delegated_process_created_count": event_activity_counts.get("delegated_process_run_created", 0),
            "delegated_process_requested_count": event_activity_counts.get("delegated_process_requested", 0),
            "delegated_process_started_count": event_activity_counts.get("delegated_process_started", 0),
            "delegated_process_completed_count": event_activity_counts.get("delegated_process_completed", 0),
            "delegated_process_failed_count": event_activity_counts.get("delegated_process_failed", 0),
            "delegated_process_cancelled_count": event_activity_counts.get("delegated_process_cancelled", 0),
            "delegated_process_skipped_count": event_activity_counts.get("delegated_process_skipped", 0),
            "delegation_packet_created_count": event_activity_counts.get("delegation_packet_created", 0),
            "delegation_result_recorded_count": event_activity_counts.get("delegation_result_recorded", 0),
            "delegation_link_recorded_count": event_activity_counts.get("delegation_link_recorded", 0),
            "delegation_by_type": by_type,
            "delegation_by_isolation_mode": by_isolation_mode,
            "delegation_permission_reference_count": permission_reference_count,
            "delegation_safety_reference_count": safety_reference_count,
        }

    @staticmethod
    def _sidechain_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        by_isolation_mode: dict[str, int] = {}
        safety_ref_count = 0
        safety_entry_count = 0
        for item in view.objects:
            if item.object_type == "sidechain_context":
                context_type = str(item.object_attrs.get("context_type") or "unknown")
                isolation_mode = str(item.object_attrs.get("isolation_mode") or "unknown")
                by_type[context_type] = by_type.get(context_type, 0) + 1
                by_isolation_mode[isolation_mode] = by_isolation_mode.get(isolation_mode, 0) + 1
                safety_ref_count += len(item.object_attrs.get("safety_ref_ids") or [])
            if item.object_type == "sidechain_context_entry" and item.object_attrs.get("entry_type") in {
                "permission_ref",
                "sandbox_ref",
                "risk_ref",
                "outcome_ref",
            }:
                safety_entry_count += 1
        if safety_ref_count == 0:
            safety_ref_count = safety_entry_count
        return {
            "sidechain_context_count": object_type_counts.get("sidechain_context", 0),
            "sidechain_context_entry_count": object_type_counts.get("sidechain_context_entry", 0),
            "sidechain_context_snapshot_count": object_type_counts.get("sidechain_context_snapshot", 0),
            "sidechain_return_envelope_count": object_type_counts.get("sidechain_return_envelope", 0),
            "sidechain_ready_count": event_activity_counts.get("sidechain_context_ready", 0),
            "sidechain_sealed_count": event_activity_counts.get("sidechain_context_sealed", 0),
            "sidechain_error_count": event_activity_counts.get("sidechain_context_error", 0),
            "sidechain_parent_transcript_excluded_count": event_activity_counts.get(
                "sidechain_parent_transcript_excluded",
                0,
            ),
            "sidechain_permission_inheritance_prevented_count": event_activity_counts.get(
                "sidechain_permission_inheritance_prevented",
                0,
            ),
            "sidechain_safety_ref_count": safety_ref_count,
            "sidechain_context_by_type": by_type,
            "sidechain_context_by_isolation_mode": by_isolation_mode,
        }

    @staticmethod
    def _delegation_conformance_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        result_counts = {"passed": 0, "failed": 0, "needs_review": 0, "inconclusive": 0}
        failed_finding_count = 0
        warning_finding_count = 0
        by_rule_type: dict[str, int] = {}
        scores: list[float] = []
        for item in view.objects:
            if item.object_type == "delegation_conformance_finding":
                rule_type = str(item.object_attrs.get("rule_type") or "unknown")
                by_rule_type[rule_type] = by_rule_type.get(rule_type, 0) + 1
                status = str(item.object_attrs.get("status") or "unknown")
                if status == "failed":
                    failed_finding_count += 1
                if status == "warning":
                    warning_finding_count += 1
            if item.object_type == "delegation_conformance_result":
                status = str(item.object_attrs.get("status") or "unknown")
                if status in result_counts:
                    result_counts[status] += 1
                score = item.object_attrs.get("score")
                if score is not None:
                    scores.append(float(score))
        return {
            "delegation_conformance_contract_count": object_type_counts.get("delegation_conformance_contract", 0),
            "delegation_conformance_rule_count": object_type_counts.get("delegation_conformance_rule", 0),
            "delegation_conformance_run_count": object_type_counts.get("delegation_conformance_run", 0),
            "delegation_conformance_finding_count": object_type_counts.get("delegation_conformance_finding", 0),
            "delegation_conformance_result_count": object_type_counts.get("delegation_conformance_result", 0),
            "delegation_conformance_passed_count": result_counts["passed"],
            "delegation_conformance_failed_count": result_counts["failed"],
            "delegation_conformance_needs_review_count": result_counts["needs_review"],
            "delegation_conformance_inconclusive_count": result_counts["inconclusive"],
            "delegation_conformance_failed_finding_count": failed_finding_count,
            "delegation_conformance_warning_finding_count": warning_finding_count,
            "delegation_conformance_by_rule_type": by_rule_type,
            "average_delegation_conformance_score": round(sum(scores) / len(scores), 6) if scores else None,
            "delegation_conformance_contract_registered_count": event_activity_counts.get(
                "delegation_conformance_contract_registered",
                0,
            ),
            "delegation_conformance_rule_registered_count": event_activity_counts.get(
                "delegation_conformance_rule_registered",
                0,
            ),
            "delegation_conformance_run_started_count": event_activity_counts.get(
                "delegation_conformance_run_started",
                0,
            ),
            "delegation_conformance_finding_recorded_count": event_activity_counts.get(
                "delegation_conformance_finding_recorded",
                0,
            ),
            "delegation_conformance_result_recorded_count": event_activity_counts.get(
                "delegation_conformance_result_recorded",
                0,
            ),
            "delegation_conformance_run_completed_count": event_activity_counts.get(
                "delegation_conformance_run_completed",
                0,
            ),
            "delegation_conformance_run_failed_count": event_activity_counts.get(
                "delegation_conformance_run_failed",
                0,
            ),
            "delegation_conformance_run_skipped_count": event_activity_counts.get(
                "delegation_conformance_run_skipped",
                0,
            ),
        }

    @staticmethod
    def _external_capability_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        by_risk_level: dict[str, int] = {}
        disabled_count = 0
        pending_review_count = 0
        execution_enabled_count = 0
        review_required_count = 0
        view_disabled_candidate_count = 0
        view_execution_enabled_candidate_count = 0
        view_pending_review_count = 0
        view_high_risk_count = 0
        view_critical_risk_count = 0
        review_pending_count = 0
        review_in_review_count = 0
        review_needs_more_info_count = 0
        review_approved_for_design_count = 0
        review_rejected_count = 0
        review_open_finding_count = 0
        review_high_risk_finding_count = 0
        review_critical_risk_finding_count = 0
        review_non_activating_decision_count = 0
        review_runtime_activation_count = 0
        mcp_descriptor_needs_review_count = 0
        plugin_descriptor_needs_review_count = 0
        skeleton_validation_passed_count = 0
        skeleton_validation_failed_count = 0
        skeleton_validation_needs_review_count = 0
        mcp_plugin_execution_enabled_count = 0
        mcp_plugin_activation_enabled_count = 0
        mcp_plugin_descriptor_by_type: dict[str, int] = {}
        mcp_plugin_risk_category_count: dict[str, int] = {}
        external_ocel_valid_count = 0
        external_ocel_invalid_count = 0
        external_ocel_needs_review_count = 0
        external_ocel_candidate_pending_review_count = 0
        external_ocel_candidate_canonical_import_enabled_count = 0
        external_ocel_candidate_not_merged_count = 0
        external_ocel_total_preview_event_count = 0
        external_ocel_total_preview_object_count = 0
        external_ocel_total_preview_relation_count = 0
        external_ocel_by_schema_status: dict[str, int] = {}
        external_ocel_by_risk_level: dict[str, int] = {}
        for item in view.objects:
            if item.object_type == "external_capability_descriptor":
                capability_type = str(item.object_attrs.get("capability_type") or "other")
                by_type[capability_type] = by_type.get(capability_type, 0) + 1
            if item.object_type == "external_assimilation_candidate":
                if item.object_attrs.get("activation_status") == "disabled":
                    disabled_count += 1
                if item.object_attrs.get("review_status") == "pending_review":
                    pending_review_count += 1
                if item.object_attrs.get("execution_enabled") is True:
                    execution_enabled_count += 1
            if item.object_type == "external_capability_risk_note":
                risk_level = str(item.object_attrs.get("risk_level") or "unknown")
                by_risk_level[risk_level] = by_risk_level.get(risk_level, 0) + 1
                if item.object_attrs.get("review_required") is True:
                    review_required_count += 1
            if item.object_type == "external_capability_registry_snapshot":
                view_disabled_candidate_count += int(item.object_attrs.get("disabled_candidate_count") or 0)
                view_execution_enabled_candidate_count += int(
                    item.object_attrs.get("execution_enabled_candidate_count") or 0
                )
                view_pending_review_count += int(item.object_attrs.get("pending_review_count") or 0)
                view_high_risk_count += int(item.object_attrs.get("high_risk_count") or 0)
                view_critical_risk_count += int(item.object_attrs.get("critical_risk_count") or 0)
            if item.object_type == "external_adapter_review_item":
                review_status = str(item.object_attrs.get("review_status") or "")
                if review_status == "pending_review":
                    review_pending_count += 1
                if review_status == "in_review":
                    review_in_review_count += 1
                if review_status == "needs_more_info":
                    review_needs_more_info_count += 1
                if review_status == "approved_for_design":
                    review_approved_for_design_count += 1
                if review_status == "rejected":
                    review_rejected_count += 1
            if item.object_type == "external_adapter_review_finding":
                status = str(item.object_attrs.get("status") or "")
                severity = str(item.object_attrs.get("severity") or "")
                if status == "open":
                    review_open_finding_count += 1
                if severity == "high":
                    review_high_risk_finding_count += 1
                if severity == "critical":
                    review_critical_risk_finding_count += 1
            if item.object_type == "external_adapter_review_decision":
                activation_allowed = item.object_attrs.get("activation_allowed") is True
                registration_allowed = item.object_attrs.get("runtime_registration_allowed") is True
                after_decision = item.object_attrs.get("execution_enabled_after_decision") is True
                if not activation_allowed and not registration_allowed and not after_decision:
                    review_non_activating_decision_count += 1
                if activation_allowed or registration_allowed or after_decision:
                    review_runtime_activation_count += 1
            if item.object_type == "mcp_server_descriptor":
                transport = str(item.object_attrs.get("transport") or "unknown")
                mcp_plugin_descriptor_by_type[f"mcp_server:{transport}"] = (
                    mcp_plugin_descriptor_by_type.get(f"mcp_server:{transport}", 0) + 1
                )
                if item.object_attrs.get("status") == "needs_review":
                    mcp_descriptor_needs_review_count += 1
                if item.object_attrs.get("execution_enabled") is True:
                    mcp_plugin_execution_enabled_count += 1
                for category in item.object_attrs.get("declared_risks") or []:
                    mcp_plugin_risk_category_count[str(category)] = mcp_plugin_risk_category_count.get(str(category), 0) + 1
            if item.object_type == "mcp_tool_descriptor":
                mcp_plugin_descriptor_by_type["mcp_tool"] = mcp_plugin_descriptor_by_type.get("mcp_tool", 0) + 1
                if item.object_attrs.get("execution_enabled") is True:
                    mcp_plugin_execution_enabled_count += 1
                for category in item.object_attrs.get("declared_risks") or []:
                    mcp_plugin_risk_category_count[str(category)] = mcp_plugin_risk_category_count.get(str(category), 0) + 1
            if item.object_type == "plugin_descriptor":
                plugin_type = str(item.object_attrs.get("plugin_type") or "unknown")
                mcp_plugin_descriptor_by_type[f"plugin:{plugin_type}"] = (
                    mcp_plugin_descriptor_by_type.get(f"plugin:{plugin_type}", 0) + 1
                )
                if item.object_attrs.get("status") == "needs_review":
                    plugin_descriptor_needs_review_count += 1
                if item.object_attrs.get("execution_enabled") is True:
                    mcp_plugin_execution_enabled_count += 1
                for category in item.object_attrs.get("declared_risks") or []:
                    mcp_plugin_risk_category_count[str(category)] = mcp_plugin_risk_category_count.get(str(category), 0) + 1
            if item.object_type == "plugin_entrypoint_descriptor":
                entrypoint_type = str(item.object_attrs.get("entrypoint_type") or "unknown")
                mcp_plugin_descriptor_by_type[f"entrypoint:{entrypoint_type}"] = (
                    mcp_plugin_descriptor_by_type.get(f"entrypoint:{entrypoint_type}", 0) + 1
                )
                if item.object_attrs.get("execution_enabled") is True:
                    mcp_plugin_execution_enabled_count += 1
                for category in item.object_attrs.get("declared_risks") or []:
                    mcp_plugin_risk_category_count[str(category)] = mcp_plugin_risk_category_count.get(str(category), 0) + 1
            if item.object_type == "external_descriptor_skeleton":
                if item.object_attrs.get("execution_enabled") is True:
                    mcp_plugin_execution_enabled_count += 1
                if item.object_attrs.get("activation_status") == "active":
                    mcp_plugin_activation_enabled_count += 1
                skeleton_type = str(item.object_attrs.get("skeleton_type") or "other")
                mcp_plugin_descriptor_by_type[f"skeleton:{skeleton_type}"] = (
                    mcp_plugin_descriptor_by_type.get(f"skeleton:{skeleton_type}", 0) + 1
                )
                for category in item.object_attrs.get("declared_risk_categories") or []:
                    mcp_plugin_risk_category_count[str(category)] = mcp_plugin_risk_category_count.get(str(category), 0) + 1
            if item.object_type == "external_descriptor_skeleton_validation":
                validation_status = str(item.object_attrs.get("status") or "")
                if validation_status == "passed":
                    skeleton_validation_passed_count += 1
                if validation_status == "failed":
                    skeleton_validation_failed_count += 1
                if validation_status == "needs_review":
                    skeleton_validation_needs_review_count += 1
            if item.object_type == "external_ocel_import_candidate":
                if item.object_attrs.get("review_status") == "pending_review":
                    external_ocel_candidate_pending_review_count += 1
                if item.object_attrs.get("canonical_import_enabled") is True:
                    external_ocel_candidate_canonical_import_enabled_count += 1
                if item.object_attrs.get("merge_status") == "not_merged":
                    external_ocel_candidate_not_merged_count += 1
            if item.object_type == "external_ocel_validation_result":
                validation_status = str(item.object_attrs.get("status") or "")
                schema_status = str(item.object_attrs.get("schema_status") or "unknown")
                external_ocel_by_schema_status[schema_status] = (
                    external_ocel_by_schema_status.get(schema_status, 0) + 1
                )
                if validation_status in {"valid", "valid_with_warnings"}:
                    external_ocel_valid_count += 1
                if validation_status in {"invalid", "error"}:
                    external_ocel_invalid_count += 1
                if validation_status in {"needs_review", "valid_with_warnings"}:
                    external_ocel_needs_review_count += 1
            if item.object_type == "external_ocel_preview_snapshot":
                external_ocel_total_preview_event_count += int(item.object_attrs.get("event_count") or 0)
                external_ocel_total_preview_object_count += int(item.object_attrs.get("object_count") or 0)
                external_ocel_total_preview_relation_count += int(item.object_attrs.get("relation_count") or 0)
            if item.object_type == "external_ocel_import_risk_note":
                risk_level = str(item.object_attrs.get("risk_level") or "unknown")
                external_ocel_by_risk_level[risk_level] = external_ocel_by_risk_level.get(risk_level, 0) + 1
        return {
            "external_capability_source_count": object_type_counts.get("external_capability_source", 0),
            "external_capability_descriptor_count": object_type_counts.get("external_capability_descriptor", 0),
            "external_capability_import_batch_count": object_type_counts.get("external_capability_import_batch", 0),
            "external_capability_normalization_result_count": object_type_counts.get(
                "external_capability_normalization_result",
                0,
            ),
            "external_assimilation_candidate_count": object_type_counts.get("external_assimilation_candidate", 0),
            "external_capability_risk_note_count": object_type_counts.get("external_capability_risk_note", 0),
            "external_candidate_disabled_count": disabled_count,
            "external_candidate_pending_review_count": pending_review_count,
            "external_candidate_execution_enabled_count": execution_enabled_count,
            "external_capability_by_type": by_type,
            "external_capability_by_risk_level": by_risk_level,
            "external_capability_review_required_count": review_required_count,
            "external_capability_registry_snapshot_count": object_type_counts.get(
                "external_capability_registry_snapshot",
                0,
            ),
            "external_capability_registry_view_written_count": event_activity_counts.get(
                "external_capability_registry_view_written",
                0,
            ),
            "external_capability_review_view_written_count": event_activity_counts.get(
                "external_capability_review_view_written",
                0,
            ),
            "external_capability_risk_view_written_count": event_activity_counts.get(
                "external_capability_risk_view_written",
                0,
            ),
            "external_view_disabled_candidate_count": view_disabled_candidate_count,
            "external_view_execution_enabled_candidate_count": view_execution_enabled_candidate_count,
            "external_view_pending_review_count": view_pending_review_count,
            "external_view_high_risk_count": view_high_risk_count,
            "external_view_critical_risk_count": view_critical_risk_count,
            "external_adapter_review_queue_count": object_type_counts.get("external_adapter_review_queue", 0),
            "external_adapter_review_item_count": object_type_counts.get("external_adapter_review_item", 0),
            "external_adapter_review_checklist_count": object_type_counts.get("external_adapter_review_checklist", 0),
            "external_adapter_review_finding_count": object_type_counts.get("external_adapter_review_finding", 0),
            "external_adapter_review_decision_count": object_type_counts.get("external_adapter_review_decision", 0),
            "external_review_pending_count": review_pending_count,
            "external_review_in_review_count": review_in_review_count,
            "external_review_needs_more_info_count": review_needs_more_info_count,
            "external_review_approved_for_design_count": review_approved_for_design_count,
            "external_review_rejected_count": review_rejected_count,
            "external_review_open_finding_count": review_open_finding_count,
            "external_review_high_risk_finding_count": review_high_risk_finding_count,
            "external_review_critical_risk_finding_count": review_critical_risk_finding_count,
            "external_review_non_activating_decision_count": review_non_activating_decision_count,
            "external_review_runtime_activation_count": review_runtime_activation_count,
            "external_capability_source_registered_count": event_activity_counts.get(
                "external_capability_source_registered",
                0,
            ),
            "external_capability_descriptor_imported_count": event_activity_counts.get(
                "external_capability_descriptor_imported",
                0,
            ),
            "external_capability_import_started_count": event_activity_counts.get(
                "external_capability_import_started",
                0,
            ),
            "external_capability_import_completed_count": event_activity_counts.get(
                "external_capability_import_completed",
                0,
            ),
            "external_capability_normalized_count": event_activity_counts.get("external_capability_normalized", 0),
            "external_assimilation_candidate_created_count": event_activity_counts.get(
                "external_assimilation_candidate_created",
                0,
            ),
            "external_capability_risk_note_recorded_count": event_activity_counts.get(
                "external_capability_risk_note_recorded",
                0,
            ),
            "external_adapter_review_queue_created_count": event_activity_counts.get(
                "external_adapter_review_queue_created",
                0,
            ),
            "external_adapter_review_item_created_count": event_activity_counts.get(
                "external_adapter_review_item_created",
                0,
            ),
            "external_adapter_review_checklist_created_count": event_activity_counts.get(
                "external_adapter_review_checklist_created",
                0,
            ),
            "external_adapter_review_finding_recorded_count": event_activity_counts.get(
                "external_adapter_review_finding_recorded",
                0,
            ),
            "external_adapter_review_decision_recorded_count": event_activity_counts.get(
                "external_adapter_review_decision_recorded",
                0,
            ),
            "external_adapter_review_decision_marked_non_activating_count": event_activity_counts.get(
                "external_adapter_review_decision_marked_non_activating",
                0,
            ),
            "mcp_server_descriptor_count": object_type_counts.get("mcp_server_descriptor", 0),
            "mcp_tool_descriptor_count": object_type_counts.get("mcp_tool_descriptor", 0),
            "plugin_descriptor_count": object_type_counts.get("plugin_descriptor", 0),
            "plugin_entrypoint_descriptor_count": object_type_counts.get("plugin_entrypoint_descriptor", 0),
            "external_descriptor_skeleton_count": object_type_counts.get("external_descriptor_skeleton", 0),
            "external_descriptor_skeleton_validation_count": object_type_counts.get(
                "external_descriptor_skeleton_validation",
                0,
            ),
            "mcp_descriptor_needs_review_count": mcp_descriptor_needs_review_count,
            "plugin_descriptor_needs_review_count": plugin_descriptor_needs_review_count,
            "skeleton_validation_passed_count": skeleton_validation_passed_count,
            "skeleton_validation_failed_count": skeleton_validation_failed_count,
            "skeleton_validation_needs_review_count": skeleton_validation_needs_review_count,
            "mcp_plugin_execution_enabled_count": mcp_plugin_execution_enabled_count,
            "mcp_plugin_activation_enabled_count": mcp_plugin_activation_enabled_count,
            "mcp_plugin_descriptor_by_type": mcp_plugin_descriptor_by_type,
            "mcp_plugin_risk_category_count": mcp_plugin_risk_category_count,
            "mcp_server_descriptor_imported_count": event_activity_counts.get("mcp_server_descriptor_imported", 0),
            "mcp_tool_descriptor_imported_count": event_activity_counts.get("mcp_tool_descriptor_imported", 0),
            "plugin_descriptor_imported_count": event_activity_counts.get("plugin_descriptor_imported", 0),
            "plugin_entrypoint_descriptor_imported_count": event_activity_counts.get(
                "plugin_entrypoint_descriptor_imported",
                0,
            ),
            "external_descriptor_skeleton_created_count": event_activity_counts.get(
                "external_descriptor_skeleton_created",
                0,
            ),
            "external_descriptor_skeleton_validated_count": event_activity_counts.get(
                "external_descriptor_skeleton_validated",
                0,
            ),
            "external_descriptor_skeleton_validation_failed_count": event_activity_counts.get(
                "external_descriptor_skeleton_validation_failed",
                0,
            ),
            "mcp_plugin_descriptor_marked_non_executable_count": event_activity_counts.get(
                "mcp_plugin_descriptor_marked_non_executable",
                0,
            ),
            "external_ocel_source_count": object_type_counts.get("external_ocel_source", 0),
            "external_ocel_payload_descriptor_count": object_type_counts.get(
                "external_ocel_payload_descriptor",
                0,
            ),
            "external_ocel_import_candidate_count": object_type_counts.get(
                "external_ocel_import_candidate",
                0,
            ),
            "external_ocel_validation_result_count": object_type_counts.get(
                "external_ocel_validation_result",
                0,
            ),
            "external_ocel_preview_snapshot_count": object_type_counts.get(
                "external_ocel_preview_snapshot",
                0,
            ),
            "external_ocel_risk_note_count": object_type_counts.get("external_ocel_import_risk_note", 0),
            "external_ocel_valid_count": external_ocel_valid_count,
            "external_ocel_invalid_count": external_ocel_invalid_count,
            "external_ocel_needs_review_count": external_ocel_needs_review_count,
            "external_ocel_candidate_pending_review_count": external_ocel_candidate_pending_review_count,
            "external_ocel_candidate_canonical_import_enabled_count": (
                external_ocel_candidate_canonical_import_enabled_count
            ),
            "external_ocel_candidate_not_merged_count": external_ocel_candidate_not_merged_count,
            "external_ocel_total_preview_event_count": external_ocel_total_preview_event_count,
            "external_ocel_total_preview_object_count": external_ocel_total_preview_object_count,
            "external_ocel_total_preview_relation_count": external_ocel_total_preview_relation_count,
            "external_ocel_by_schema_status": external_ocel_by_schema_status,
            "external_ocel_by_risk_level": external_ocel_by_risk_level,
            "external_ocel_payload_registered_count": event_activity_counts.get("external_ocel_payload_registered", 0),
            "external_ocel_candidate_created_count": event_activity_counts.get("external_ocel_candidate_created", 0),
            "external_ocel_validation_recorded_count": event_activity_counts.get(
                "external_ocel_validation_recorded",
                0,
            ),
            "external_ocel_preview_created_count": event_activity_counts.get("external_ocel_preview_created", 0),
            "external_ocel_risk_note_recorded_count": event_activity_counts.get(
                "external_ocel_risk_note_recorded",
                0,
            ),
        }

    @staticmethod
    def _observation_digest_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        observed_event_by_activity: dict[str, int] = {}
        observed_run_by_source_runtime: dict[str, int] = {}
        external_candidate_by_risk_class: dict[str, int] = {}
        external_candidate_pending_review_count = 0
        adapter_candidate_pending_review_count = 0
        for item in view.objects:
            if item.object_type == "agent_observation_normalized_event":
                activity = str(item.object_attrs.get("observed_activity") or "unknown_event_observed")
                observed_event_by_activity[activity] = observed_event_by_activity.get(activity, 0) + 1
            if item.object_type == "observed_agent_run":
                runtime = str(item.object_attrs.get("inferred_runtime") or "unknown")
                observed_run_by_source_runtime[runtime] = observed_run_by_source_runtime.get(runtime, 0) + 1
            if item.object_type == "external_skill_assimilation_candidate":
                risk_class = str(item.object_attrs.get("risk_class") or "unknown")
                external_candidate_by_risk_class[risk_class] = external_candidate_by_risk_class.get(risk_class, 0) + 1
                if item.object_attrs.get("review_status") == "pending_review":
                    external_candidate_pending_review_count += 1
            if item.object_type == "external_skill_adapter_candidate":
                if item.object_attrs.get("requires_review") is True:
                    adapter_candidate_pending_review_count += 1
        return {
            "agent_observation_source_count": object_type_counts.get("agent_observation_source", 0),
            "agent_observation_batch_count": object_type_counts.get("agent_observation_batch", 0),
            "agent_observation_normalized_event_count": object_type_counts.get(
                "agent_observation_normalized_event",
                0,
            ),
            "observed_agent_run_count": object_type_counts.get("observed_agent_run", 0),
            "agent_behavior_inference_count": object_type_counts.get("agent_behavior_inference", 0),
            "agent_process_narrative_count": object_type_counts.get("agent_process_narrative", 0),
            "external_skill_source_descriptor_count": object_type_counts.get(
                "external_skill_source_descriptor",
                0,
            ),
            "external_skill_static_profile_count": object_type_counts.get("external_skill_static_profile", 0),
            "external_skill_behavior_fingerprint_count": object_type_counts.get(
                "external_skill_behavior_fingerprint",
                0,
            ),
            "external_skill_assimilation_candidate_count": object_type_counts.get(
                "external_skill_assimilation_candidate",
                0,
            ),
            "external_skill_adapter_candidate_count": object_type_counts.get(
                "external_skill_adapter_candidate",
                0,
            ),
            "observation_digestion_finding_count": object_type_counts.get("observation_digestion_finding", 0),
            "observation_digestion_result_count": object_type_counts.get("observation_digestion_result", 0),
            "observed_event_by_activity": observed_event_by_activity,
            "observed_run_by_source_runtime": observed_run_by_source_runtime,
            "external_candidate_by_risk_class": external_candidate_by_risk_class,
            "external_candidate_pending_review_count": external_candidate_pending_review_count,
            "adapter_candidate_pending_review_count": adapter_candidate_pending_review_count,
            "agent_observation_source_inspected_count": event_activity_counts.get(
                "agent_observation_source_inspected",
                0,
            ),
            "external_skill_assimilation_candidate_created_count": event_activity_counts.get(
                "external_skill_assimilation_candidate_created",
                0,
            ),
        }

    @staticmethod
    def _skill_registry_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_layer: dict[str, int] = {}
        by_origin: dict[str, int] = {}
        by_risk_class: dict[str, int] = {}
        by_status: dict[str, int] = {}
        observation_count = 0
        digestion_count = 0
        external_candidate_count = 0
        enabled_count = 0
        disabled_count = 0
        blocked_count = 0
        missing_contract_count = 0
        for item in view.objects:
            if item.object_type == "skill_registry_entry":
                layer = str(item.object_attrs.get("skill_layer") or "unknown")
                origin = str(item.object_attrs.get("skill_origin") or "unknown")
                risk_class = str(item.object_attrs.get("risk_class") or "unknown")
                status = str(item.object_attrs.get("status") or "unknown")
                by_layer[layer] = by_layer.get(layer, 0) + 1
                by_origin[origin] = by_origin.get(origin, 0) + 1
                by_risk_class[risk_class] = by_risk_class.get(risk_class, 0) + 1
                by_status[status] = by_status.get(status, 0) + 1
                if layer == "internal_observation":
                    observation_count += 1
                if layer == "internal_digestion":
                    digestion_count += 1
                if layer in {"external_candidate", "external_adapted"}:
                    external_candidate_count += 1
                if item.object_attrs.get("enabled") is True:
                    enabled_count += 1
                else:
                    disabled_count += 1
                if status == "blocked" or layer == "blocked":
                    blocked_count += 1
            if item.object_type == "skill_registry_finding":
                if item.object_attrs.get("finding_type") == "missing_contract":
                    missing_contract_count += 1
        return {
            "skill_registry_view_count": object_type_counts.get("skill_registry_view", 0),
            "skill_registry_entry_count": object_type_counts.get("skill_registry_entry", 0),
            "skill_registry_filter_count": object_type_counts.get("skill_registry_filter", 0),
            "skill_registry_finding_count": object_type_counts.get("skill_registry_finding", 0),
            "skill_registry_result_count": object_type_counts.get("skill_registry_result", 0),
            "skill_registry_observation_skill_count": observation_count,
            "skill_registry_digestion_skill_count": digestion_count,
            "skill_registry_external_candidate_count": external_candidate_count,
            "skill_registry_enabled_count": enabled_count,
            "skill_registry_disabled_count": disabled_count,
            "skill_registry_blocked_count": blocked_count,
            "skill_registry_missing_contract_finding_count": missing_contract_count,
            "skill_registry_by_layer": by_layer,
            "skill_registry_by_origin": by_origin,
            "skill_registry_by_risk_class": by_risk_class,
            "skill_registry_by_status": by_status,
            "skill_registry_view_created_count": event_activity_counts.get("skill_registry_view_created", 0),
            "skill_registry_rendered_count": event_activity_counts.get("skill_registry_rendered", 0),
        }

    @staticmethod
    def _observation_digest_proposal_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_skill_id: dict[str, int] = {}
        by_intent_family: dict[str, int] = {}
        finding_by_type: dict[str, int] = {}
        observation_count = 0
        digestion_count = 0
        mixed_count = 0
        needs_more_input_count = 0
        no_matching_skill_count = 0
        for item in view.objects:
            if item.object_type == "observation_digest_intent_candidate":
                family = str(item.object_attrs.get("intent_family") or "unknown")
                by_intent_family[family] = by_intent_family.get(family, 0) + 1
                if family == "observation":
                    observation_count += 1
                elif family == "digestion":
                    digestion_count += 1
                elif family == "mixed_observation_digestion":
                    mixed_count += 1
            if item.object_type == "observation_digest_proposal_binding":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                by_skill_id[skill_id] = by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "observation_digest_proposal_set":
                if item.object_attrs.get("status") == "needs_more_input":
                    needs_more_input_count += 1
                if item.object_attrs.get("status") == "no_matching_skill":
                    no_matching_skill_count += 1
            if item.object_type == "observation_digest_proposal_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                finding_by_type[finding_type] = finding_by_type.get(finding_type, 0) + 1
        return {
            "observation_digest_proposal_policy_count": object_type_counts.get("observation_digest_proposal_policy", 0),
            "observation_digest_intent_candidate_count": object_type_counts.get("observation_digest_intent_candidate", 0),
            "observation_digest_proposal_binding_count": object_type_counts.get("observation_digest_proposal_binding", 0),
            "observation_digest_proposal_set_count": object_type_counts.get("observation_digest_proposal_set", 0),
            "observation_digest_proposal_finding_count": object_type_counts.get("observation_digest_proposal_finding", 0),
            "observation_digest_proposal_result_count": object_type_counts.get("observation_digest_proposal_result", 0),
            "observation_digest_proposal_observation_count": observation_count,
            "observation_digest_proposal_digestion_count": digestion_count,
            "observation_digest_proposal_mixed_count": mixed_count,
            "observation_digest_proposal_needs_more_input_count": needs_more_input_count,
            "observation_digest_proposal_no_matching_skill_count": no_matching_skill_count,
            "observation_digest_proposal_by_skill_id": by_skill_id,
            "observation_digest_proposal_by_intent_family": by_intent_family,
            "observation_digest_proposal_finding_by_type": finding_by_type,
            "observation_digest_proposal_needs_more_input_event_count": event_activity_counts.get(
                "observation_digest_proposal_needs_more_input",
                0,
            ),
            "observation_digest_proposal_no_matching_skill_event_count": event_activity_counts.get(
                "observation_digest_proposal_no_matching_skill",
                0,
            ),
        }

    @staticmethod
    def _observation_digest_invocation_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_skill_id: dict[str, int] = {}
        by_family: dict[str, int] = {}
        finding_by_type: dict[str, int] = {}
        completed_count = 0
        blocked_count = 0
        failed_count = 0
        envelope_count = 0
        for item in view.objects:
            if item.object_type == "observation_digest_skill_runtime_binding":
                family = str(item.object_attrs.get("skill_family") or "unknown")
                by_family[family] = by_family.get(family, 0) + 1
            if item.object_type == "observation_digest_invocation_result":
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                by_skill_id[skill_id] = by_skill_id.get(skill_id, 0) + 1
                status = str(item.object_attrs.get("status") or "unknown")
                if bool(item.object_attrs.get("blocked")):
                    blocked_count += 1
                elif status == "failed":
                    failed_count += 1
                else:
                    completed_count += 1
                if item.object_attrs.get("envelope_id"):
                    envelope_count += 1
            if item.object_type == "observation_digest_invocation_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                finding_by_type[finding_type] = finding_by_type.get(finding_type, 0) + 1
        return {
            "observation_digest_runtime_binding_count": object_type_counts.get(
                "observation_digest_skill_runtime_binding",
                0,
            ),
            "observation_digest_invocation_policy_count": object_type_counts.get(
                "observation_digest_invocation_policy",
                0,
            ),
            "observation_digest_invocation_result_count": object_type_counts.get(
                "observation_digest_invocation_result",
                0,
            ),
            "observation_digest_invocation_finding_count": object_type_counts.get(
                "observation_digest_invocation_finding",
                0,
            ),
            "observation_digest_invocation_completed_count": completed_count,
            "observation_digest_invocation_blocked_count": blocked_count,
            "observation_digest_invocation_failed_count": failed_count,
            "observation_digest_invocation_by_skill_id": by_skill_id,
            "observation_digest_invocation_by_family": by_family,
            "observation_digest_invocation_finding_by_type": finding_by_type,
            "observation_digest_invocation_envelope_count": envelope_count,
            "observation_digest_invocation_completed_event_count": event_activity_counts.get(
                "observation_digest_skill_invocation_completed",
                0,
            ),
            "observation_digest_invocation_blocked_event_count": event_activity_counts.get(
                "observation_digest_skill_invocation_blocked",
                0,
            ),
            "observation_digest_invocation_failed_event_count": event_activity_counts.get(
                "observation_digest_skill_invocation_failed",
                0,
            ),
        }

    @staticmethod
    def _observation_digest_conformance_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        finding_by_type: dict[str, int] = {}
        check_by_type: dict[str, int] = {}
        by_skill_id: dict[str, int] = {}
        passed_skill_count = 0
        failed_skill_count = 0
        smoke_passed_count = 0
        smoke_failed_count = 0
        for item in view.objects:
            if item.object_type == "observation_digest_conformance_check":
                check_type = str(item.object_attrs.get("check_type") or "unknown")
                skill_id = str(item.object_attrs.get("skill_id") or "unknown")
                check_by_type[check_type] = check_by_type.get(check_type, 0) + 1
                by_skill_id[skill_id] = by_skill_id.get(skill_id, 0) + 1
            if item.object_type == "observation_digest_conformance_finding":
                finding_type = str(item.object_attrs.get("finding_type") or "unknown")
                finding_by_type[finding_type] = finding_by_type.get(finding_type, 0) + 1
            if item.object_type == "observation_digest_smoke_result":
                if bool(item.object_attrs.get("passed")):
                    smoke_passed_count += 1
                else:
                    smoke_failed_count += 1
            if item.object_type == "observation_digest_conformance_report":
                passed_skill_count = max(
                    passed_skill_count,
                    int(item.object_attrs.get("passed_skill_count") or 0),
                )
                failed_skill_count = max(
                    failed_skill_count,
                    int(item.object_attrs.get("failed_skill_count") or 0),
                )
        return {
            "observation_digest_conformance_policy_count": object_type_counts.get(
                "observation_digest_conformance_policy",
                0,
            ),
            "observation_digest_conformance_check_count": object_type_counts.get(
                "observation_digest_conformance_check",
                0,
            ),
            "observation_digest_smoke_case_count": object_type_counts.get("observation_digest_smoke_case", 0),
            "observation_digest_smoke_result_count": object_type_counts.get("observation_digest_smoke_result", 0),
            "observation_digest_conformance_finding_count": object_type_counts.get(
                "observation_digest_conformance_finding",
                0,
            ),
            "observation_digest_conformance_report_count": object_type_counts.get(
                "observation_digest_conformance_report",
                0,
            ),
            "observation_digest_conformance_passed_skill_count": passed_skill_count,
            "observation_digest_conformance_failed_skill_count": failed_skill_count,
            "observation_digest_smoke_passed_count": smoke_passed_count,
            "observation_digest_smoke_failed_count": smoke_failed_count,
            "observation_digest_conformance_finding_by_type": finding_by_type,
            "observation_digest_conformance_check_by_type": check_by_type,
            "observation_digest_conformance_by_skill_id": by_skill_id,
            "observation_digest_conformance_report_recorded_count": event_activity_counts.get(
                "observation_digest_conformance_report_recorded",
                0,
            ),
        }

    @staticmethod
    def _external_skill_static_digestion_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        manifest_kind: dict[str, int] = {}
        capability_category: dict[str, int] = {}
        risk_class: dict[str, int] = {}
        script_detected_count = 0
        shell_declared_count = 0
        network_declared_count = 0
        write_declared_count = 0
        mcp_declared_count = 0
        plugin_declared_count = 0
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "external_skill_resource_inventory":
                script_detected_count += len(attrs.get("script_files") or [])
            if item.object_type == "external_skill_manifest_profile":
                key = str(attrs.get("manifest_kind") or "unknown")
                manifest_kind[key] = manifest_kind.get(key, 0) + 1
            if item.object_type == "external_skill_declared_capability":
                key = str(attrs.get("capability_category") or "unknown")
                capability_category[key] = capability_category.get(key, 0) + 1
            if item.object_type == "external_skill_static_risk_profile":
                key = str(attrs.get("risk_class") or "unknown")
                risk_class[key] = risk_class.get(key, 0) + 1
                shell_declared_count += 1 if attrs.get("declared_shell") else 0
                network_declared_count += 1 if attrs.get("declared_network") else 0
                write_declared_count += 1 if attrs.get("declared_write") else 0
                mcp_declared_count += 1 if attrs.get("declared_mcp") else 0
                plugin_declared_count += 1 if attrs.get("declared_plugin") else 0
        return {
            "external_skill_resource_inventory_count": object_type_counts.get("external_skill_resource_inventory", 0),
            "external_skill_manifest_profile_count": object_type_counts.get("external_skill_manifest_profile", 0),
            "external_skill_instruction_profile_count": object_type_counts.get("external_skill_instruction_profile", 0),
            "external_skill_declared_capability_count": object_type_counts.get("external_skill_declared_capability", 0),
            "external_skill_static_risk_profile_count": object_type_counts.get("external_skill_static_risk_profile", 0),
            "external_skill_static_digestion_report_count": object_type_counts.get(
                "external_skill_static_digestion_report",
                0,
            ),
            "external_skill_static_digestion_finding_count": object_type_counts.get(
                "external_skill_static_digestion_finding",
                0,
            ),
            "external_skill_static_digest_by_manifest_kind": manifest_kind,
            "external_skill_static_digest_by_capability_category": capability_category,
            "external_skill_static_digest_by_risk_class": risk_class,
            "external_skill_static_digest_script_detected_count": script_detected_count,
            "external_skill_static_digest_shell_declared_count": shell_declared_count,
            "external_skill_static_digest_network_declared_count": network_declared_count,
            "external_skill_static_digest_write_declared_count": write_declared_count,
            "external_skill_static_digest_mcp_declared_count": mcp_declared_count,
            "external_skill_static_digest_plugin_declared_count": plugin_declared_count,
            "external_skill_static_digestion_report_created_count": event_activity_counts.get(
                "external_skill_static_digestion_report_created",
                0,
            ),
        }

    @staticmethod
    def _agent_observation_spine_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        action_type: dict[str, int] = {}
        object_type: dict[str, int] = {}
        relation_type: dict[str, int] = {}
        confidence_class: dict[str, int] = {}
        adapter_by_runtime: dict[str, int] = {}
        collector_by_kind: dict[str, int] = {}
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "agent_observation_normalized_event_v2":
                key = str(attrs.get("canonical_action_type") or "unknown_action")
                action_type[key] = action_type.get(key, 0) + 1
            if item.object_type == "observed_agent_object":
                key = str(attrs.get("object_type") or "unknown_object")
                object_type[key] = object_type.get(key, 0) + 1
            if item.object_type == "observed_agent_relation":
                key = str(attrs.get("relation_type") or "unknown_relation")
                relation_type[key] = relation_type.get(key, 0) + 1
            if item.object_type == "agent_behavior_inference_v2":
                attrs_dict = attrs.get("inference_attrs") or {}
                key = str(attrs_dict.get("confidence_class") or "behavior_inference")
                confidence_class[key] = confidence_class.get(key, 0) + 1
            if item.object_type == "agent_observation_adapter_profile":
                key = str(attrs.get("source_runtime") or "unknown")
                adapter_by_runtime[key] = adapter_by_runtime.get(key, 0) + 1
            if item.object_type == "agent_observation_collector_contract":
                key = str(attrs.get("collector_kind") or "unknown")
                collector_by_kind[key] = collector_by_kind.get(key, 0) + 1
        return {
            "agent_instance_count": object_type_counts.get("agent_instance", 0),
            "agent_runtime_descriptor_count": object_type_counts.get("agent_runtime_descriptor", 0),
            "runtime_environment_snapshot_count": object_type_counts.get("runtime_environment_snapshot", 0),
            "agent_observation_collector_contract_count": object_type_counts.get("agent_observation_collector_contract", 0),
            "agent_observation_adapter_profile_count": object_type_counts.get("agent_observation_adapter_profile", 0),
            "agent_movement_ontology_term_count": object_type_counts.get("agent_movement_ontology_term", 0),
            "agent_observation_normalized_event_v2_count": object_type_counts.get("agent_observation_normalized_event_v2", 0),
            "observed_agent_object_count": object_type_counts.get("observed_agent_object", 0),
            "observed_agent_relation_count": object_type_counts.get("observed_agent_relation", 0),
            "agent_behavior_inference_v2_count": object_type_counts.get("agent_behavior_inference_v2", 0),
            "agent_observation_review_count": object_type_counts.get("agent_observation_review", 0),
            "agent_observation_correction_count": object_type_counts.get("agent_observation_correction", 0),
            "observation_redaction_policy_count": object_type_counts.get("observation_redaction_policy", 0),
            "observation_export_policy_count": object_type_counts.get("observation_export_policy", 0),
            "agent_fleet_observation_snapshot_count": object_type_counts.get("agent_fleet_observation_snapshot", 0),
            "agent_observation_spine_finding_count": object_type_counts.get("agent_observation_spine_finding", 0),
            "observed_event_v2_by_action_type": action_type,
            "observed_object_by_type": object_type,
            "observed_relation_by_type": relation_type,
            "behavior_inference_by_confidence_class": confidence_class,
            "adapter_profile_by_runtime": adapter_by_runtime,
            "collector_contract_by_kind": collector_by_kind,
            "agent_observation_event_v2_normalized_count": event_activity_counts.get(
                "agent_observation_event_v2_normalized",
                0,
            ),
        }

    @staticmethod
    def _cross_harness_trace_adapter_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_runtime: dict[str, int] = {}
        by_adapter: dict[str, int] = {}
        by_implemented: dict[str, int] = {}
        finding_by_type: dict[str, int] = {}
        rule_by_action: dict[str, int] = {}
        normalized_event_count = 0
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "harness_trace_adapter_contract":
                key = "implemented" if bool(attrs.get("implemented")) else "stub"
                by_implemented[key] = by_implemented.get(key, 0) + 1
            if item.object_type == "harness_trace_normalization_plan":
                runtime = str(attrs.get("source_runtime") or "unknown")
                by_runtime[runtime] = by_runtime.get(runtime, 0) + 1
                plan_attrs = attrs.get("plan_attrs") or {}
                adapter = str(plan_attrs.get("adapter_name") or "unknown")
                by_adapter[adapter] = by_adapter.get(adapter, 0) + 1
            if item.object_type == "harness_trace_adapter_finding":
                key = str(attrs.get("finding_type") or "unknown")
                finding_by_type[key] = finding_by_type.get(key, 0) + 1
            if item.object_type == "harness_trace_mapping_rule":
                key = str(attrs.get("target_action_type") or "unknown_action")
                rule_by_action[key] = rule_by_action.get(key, 0) + 1
            if item.object_type == "agent_observation_normalized_event_v2":
                event_attrs = attrs.get("event_attrs") or {}
                if str(event_attrs.get("adapter_name") or "").endswith("Adapter"):
                    normalized_event_count += 1
        return {
            "cross_harness_trace_adapter_policy_count": object_type_counts.get("cross_harness_trace_adapter_policy", 0),
            "harness_trace_adapter_contract_count": object_type_counts.get("harness_trace_adapter_contract", 0),
            "harness_trace_source_inspection_count": object_type_counts.get("harness_trace_source_inspection", 0),
            "harness_trace_mapping_rule_count": object_type_counts.get("harness_trace_mapping_rule", 0),
            "harness_trace_normalization_plan_count": object_type_counts.get("harness_trace_normalization_plan", 0),
            "harness_trace_normalization_result_count": object_type_counts.get("harness_trace_normalization_result", 0),
            "harness_trace_adapter_coverage_report_count": object_type_counts.get("harness_trace_adapter_coverage_report", 0),
            "harness_trace_adapter_finding_count": object_type_counts.get("harness_trace_adapter_finding", 0),
            "harness_trace_adapter_result_count": object_type_counts.get("harness_trace_adapter_result", 0),
            "harness_trace_normalized_event_count": normalized_event_count,
            "harness_trace_normalization_by_runtime": by_runtime,
            "harness_trace_normalization_by_adapter": by_adapter,
            "harness_trace_adapter_by_implemented": by_implemented,
            "harness_trace_adapter_finding_by_type": finding_by_type,
            "harness_trace_mapping_rule_by_action_type": rule_by_action,
            "harness_trace_normalization_completed_count": event_activity_counts.get(
                "harness_trace_normalization_completed",
                0,
            ),
        }

    @staticmethod
    def _observation_to_digestion_adapter_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_risk: dict[str, int] = {}
        by_target_skill: dict[str, int] = {}
        by_mapping_type: dict[str, int] = {}
        unsupported_by_type: dict[str, int] = {}
        capability_by_category: dict[str, int] = {}
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "observation_digestion_adapter_candidate":
                risk = str(attrs.get("risk_class") or "unknown")
                by_risk[risk] = by_risk.get(risk, 0) + 1
                target_skill = str(attrs.get("target_skill_id") or "unknown")
                by_target_skill[target_skill] = by_target_skill.get(target_skill, 0) + 1
                mapping_type = str(attrs.get("mapping_type") or "unknown")
                by_mapping_type[mapping_type] = by_mapping_type.get(mapping_type, 0) + 1
            if item.object_type == "adapter_unsupported_feature":
                feature_type = str(attrs.get("feature_type") or "unknown")
                unsupported_by_type[feature_type] = unsupported_by_type.get(feature_type, 0) + 1
            if item.object_type == "observed_capability_candidate":
                category = str(attrs.get("capability_category") or "unknown")
                capability_by_category[category] = capability_by_category.get(category, 0) + 1
        return {
            "observation_to_digestion_adapter_policy_count": object_type_counts.get(
                "observation_to_digestion_adapter_policy",
                0,
            ),
            "observed_capability_candidate_count": object_type_counts.get("observed_capability_candidate", 0),
            "chantacore_target_skill_candidate_count": object_type_counts.get(
                "chantacore_target_skill_candidate",
                0,
            ),
            "adapter_input_mapping_spec_count": object_type_counts.get("adapter_input_mapping_spec", 0),
            "adapter_output_mapping_spec_count": object_type_counts.get("adapter_output_mapping_spec", 0),
            "adapter_unsupported_feature_count": object_type_counts.get("adapter_unsupported_feature", 0),
            "observation_digestion_adapter_candidate_count": object_type_counts.get(
                "observation_digestion_adapter_candidate",
                0,
            ),
            "observation_digestion_adapter_review_request_count": object_type_counts.get(
                "observation_digestion_adapter_review_request",
                0,
            ),
            "observation_digestion_adapter_finding_count": object_type_counts.get(
                "observation_digestion_adapter_finding",
                0,
            ),
            "observation_digestion_adapter_build_result_count": object_type_counts.get(
                "observation_digestion_adapter_build_result",
                0,
            ),
            "adapter_candidate_by_risk_class": by_risk,
            "adapter_candidate_by_target_skill_id": by_target_skill,
            "adapter_candidate_by_mapping_type": by_mapping_type,
            "unsupported_feature_by_type": unsupported_by_type,
            "observed_capability_by_category": capability_by_category,
            "observation_to_digestion_adapter_candidate_created_count": event_activity_counts.get(
                "observation_digestion_adapter_candidate_created",
                0,
            ),
        }

    @staticmethod
    def _observation_digestion_ecosystem_summary(
        object_type_counts: dict[str, int],
        event_activity_counts: dict[str, int],
        view: OCPXProcessView,
    ) -> dict[str, Any]:
        by_component_kind: dict[str, int] = {}
        by_readiness: dict[str, int] = {}
        by_capability_family: dict[str, int] = {}
        gap_by_type: dict[str, int] = {}
        finding_by_type: dict[str, int] = {}
        future_track_gap_count = 0
        executable_external_candidate_count = 0
        for item in view.objects:
            attrs = item.object_attrs
            if item.object_type == "observation_digestion_ecosystem_component":
                kind = str(attrs.get("component_kind") or "unknown")
                by_component_kind[kind] = by_component_kind.get(kind, 0) + 1
                readiness = str(attrs.get("readiness_level") or "unknown")
                by_readiness[readiness] = by_readiness.get(readiness, 0) + 1
            if item.object_type == "observation_digestion_capability_map":
                family = str(attrs.get("capability_family") or "unknown")
                by_capability_family[family] = by_capability_family.get(family, 0) + 1
            if item.object_type == "observation_digestion_gap_register":
                gap_type = str(attrs.get("gap_type") or "unknown")
                gap_by_type[gap_type] = gap_by_type.get(gap_type, 0) + 1
                gap_attrs = attrs.get("gap_attrs") or {}
                if bool(gap_attrs.get("future_track")):
                    future_track_gap_count += 1
            if item.object_type == "observation_digestion_consolidation_finding":
                finding_type = str(attrs.get("finding_type") or "unknown")
                finding_by_type[finding_type] = finding_by_type.get(finding_type, 0) + 1
            if item.object_type == "observation_digestion_ecosystem_snapshot":
                executable_external_candidate_count += int(attrs.get("executable_external_candidate_count") or 0)
        return {
            "observation_digestion_ecosystem_snapshot_count": object_type_counts.get(
                "observation_digestion_ecosystem_snapshot",
                0,
            ),
            "observation_digestion_ecosystem_component_count": object_type_counts.get(
                "observation_digestion_ecosystem_component",
                0,
            ),
            "observation_digestion_capability_map_count": object_type_counts.get(
                "observation_digestion_capability_map",
                0,
            ),
            "observation_digestion_safety_boundary_report_count": object_type_counts.get(
                "observation_digestion_safety_boundary_report",
                0,
            ),
            "observation_digestion_gap_register_count": object_type_counts.get(
                "observation_digestion_gap_register",
                0,
            ),
            "observation_digestion_release_manifest_count": object_type_counts.get(
                "observation_digestion_release_manifest",
                0,
            ),
            "observation_digestion_consolidation_finding_count": object_type_counts.get(
                "observation_digestion_consolidation_finding",
                0,
            ),
            "observation_digestion_consolidation_report_count": object_type_counts.get(
                "observation_digestion_consolidation_report",
                0,
            ),
            "observation_digestion_ready_component_count": by_readiness.get("ready", 0),
            "observation_digestion_partial_component_count": by_readiness.get("partial", 0),
            "observation_digestion_contract_only_component_count": by_readiness.get("contract_only", 0),
            "observation_digestion_blocked_component_count": by_readiness.get("blocked", 0),
            "observation_digestion_future_track_gap_count": future_track_gap_count,
            "observation_digestion_executable_external_candidate_count": executable_external_candidate_count,
            "observation_digestion_by_component_kind": by_component_kind,
            "observation_digestion_by_readiness_level": by_readiness,
            "observation_digestion_by_capability_family": by_capability_family,
            "observation_digestion_gap_by_type": gap_by_type,
            "observation_digestion_finding_by_type": finding_by_type,
            "observation_digestion_ecosystem_snapshot_created_count": event_activity_counts.get(
                "observation_digestion_ecosystem_snapshot_created",
                0,
            ),
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




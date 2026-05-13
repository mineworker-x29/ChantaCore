from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.ids import (
    new_personal_runtime_workbench_finding_id,
    new_personal_runtime_workbench_panel_id,
    new_personal_runtime_workbench_pending_item_id,
    new_personal_runtime_workbench_recent_activity_id,
    new_personal_runtime_workbench_result_id,
    new_personal_runtime_workbench_snapshot_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


PATH_KEYS = {
    "path",
    "root_path",
    "relative_path",
    "directory_root",
    "directory_root_raw",
    "source_ref",
    "artifact_ref",
    "output_ref",
}
SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "private_key", "credential"}


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchSnapshot:
    snapshot_id: str
    personal_directory_configured: bool
    selected_mode_name: str | None
    selected_profile_name: str | None
    runtime_kind: str | None
    activation_status: str
    conformance_status: str
    smoke_status: str
    pending_proposal_count: int
    pending_review_count: int
    recent_execution_count: int
    blocked_execution_count: int
    failed_execution_count: int
    promotion_candidate_count: int
    summary_candidate_count: int
    created_at: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "personal_directory_configured": self.personal_directory_configured,
            "selected_mode_name": self.selected_mode_name,
            "selected_profile_name": self.selected_profile_name,
            "runtime_kind": self.runtime_kind,
            "activation_status": self.activation_status,
            "conformance_status": self.conformance_status,
            "smoke_status": self.smoke_status,
            "pending_proposal_count": self.pending_proposal_count,
            "pending_review_count": self.pending_review_count,
            "recent_execution_count": self.recent_execution_count,
            "blocked_execution_count": self.blocked_execution_count,
            "failed_execution_count": self.failed_execution_count,
            "promotion_candidate_count": self.promotion_candidate_count,
            "summary_candidate_count": self.summary_candidate_count,
            "created_at": self.created_at,
            "snapshot_attrs": dict(self.snapshot_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchPanel:
    panel_id: str
    snapshot_id: str
    panel_type: str
    title: str
    status: str
    item_count: int
    summary: str
    created_at: str
    panel_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "snapshot_id": self.snapshot_id,
            "panel_type": self.panel_type,
            "title": self.title,
            "status": self.status,
            "item_count": self.item_count,
            "summary": self.summary,
            "created_at": self.created_at,
            "panel_attrs": dict(self.panel_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchPendingItem:
    pending_item_id: str
    snapshot_id: str
    item_type: str
    item_ref: str | None
    title: str
    status: str
    priority: str
    reason: str | None
    created_at: str
    item_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pending_item_id": self.pending_item_id,
            "snapshot_id": self.snapshot_id,
            "item_type": self.item_type,
            "item_ref": self.item_ref,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "reason": self.reason,
            "created_at": self.created_at,
            "item_attrs": dict(self.item_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchRecentActivity:
    activity_id: str
    snapshot_id: str
    activity_type: str
    activity_ref: str | None
    title: str
    status: str
    blocked: bool
    failed: bool
    skill_id: str | None
    created_at: str
    activity_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "activity_id": self.activity_id,
            "snapshot_id": self.snapshot_id,
            "activity_type": self.activity_type,
            "activity_ref": self.activity_ref,
            "title": self.title,
            "status": self.status,
            "blocked": self.blocked,
            "failed": self.failed,
            "skill_id": self.skill_id,
            "created_at": self.created_at,
            "activity_attrs": dict(self.activity_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchFinding:
    finding_id: str
    snapshot_id: str
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "snapshot_id": self.snapshot_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeWorkbenchResult:
    result_id: str
    snapshot_id: str
    command_name: str
    status: str
    panel_ids: list[str]
    pending_item_ids: list[str]
    recent_activity_ids: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "snapshot_id": self.snapshot_id,
            "command_name": self.command_name,
            "status": self.status,
            "panel_ids": list(self.panel_ids),
            "pending_item_ids": list(self.pending_item_ids),
            "recent_activity_ids": list(self.recent_activity_ids),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class PersonalRuntimeWorkbenchService:
    def __init__(
        self,
        *,
        personal_runtime_surface_service: Any | None = None,
        personal_prompt_activation_service: Any | None = None,
        conformance_service: Any | None = None,
        smoke_test_service: Any | None = None,
        skill_proposal_source: Any | None = None,
        skill_proposal_review_source: Any | None = None,
        reviewed_execution_bridge_source: Any | None = None,
        execution_audit_source: Any | None = None,
        promotion_source: Any | None = None,
        workspace_summary_source: Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.ocel_store = ocel_store or OCELStore()
        self.trace_service = trace_service or TraceService(ocel_store=self.ocel_store)
        self.sources = {
            "runtime": personal_runtime_surface_service,
            "activation": personal_prompt_activation_service,
            "conformance": conformance_service,
            "smoke": smoke_test_service,
            "proposal": skill_proposal_source,
            "review": skill_proposal_review_source,
            "bridge": reviewed_execution_bridge_source,
            "audit": execution_audit_source,
            "promotion": promotion_source,
            "summary": workspace_summary_source,
        }
        self.last_snapshot: PersonalRuntimeWorkbenchSnapshot | None = None
        self.last_panels: list[PersonalRuntimeWorkbenchPanel] = []
        self.last_pending_items: list[PersonalRuntimeWorkbenchPendingItem] = []
        self.last_recent_activities: list[PersonalRuntimeWorkbenchRecentActivity] = []
        self.last_findings: list[PersonalRuntimeWorkbenchFinding] = []
        self.last_result: PersonalRuntimeWorkbenchResult | None = None

    def build_snapshot(self, *, limit: int = 20, show_paths: bool = False) -> PersonalRuntimeWorkbenchSnapshot:
        self.last_panels = []
        self.last_pending_items = []
        self.last_recent_activities = []
        self.last_findings = []
        source_data = self._read_source_data(limit=limit, show_paths=show_paths)
        runtime_status = self.collect_runtime_status(source_data=source_data, show_paths=show_paths)
        pending_specs = self.collect_pending_items(source_data=source_data, snapshot=None, limit=limit)
        recent_specs = self.collect_recent_activities(source_data=source_data, snapshot=None, limit=limit)
        promotion_candidates = self.collect_candidates(source_data=source_data, snapshot=None, limit=limit)
        summary_candidates = self.collect_summary_candidates(source_data=source_data, snapshot=None, limit=limit)
        blocked_specs = [item for item in recent_specs if item.get("blocked") or item.get("failed")]
        snapshot = PersonalRuntimeWorkbenchSnapshot(
            snapshot_id=new_personal_runtime_workbench_snapshot_id(),
            personal_directory_configured=runtime_status["personal_directory_configured"],
            selected_mode_name=runtime_status.get("selected_mode_name"),
            selected_profile_name=runtime_status.get("selected_profile_name"),
            runtime_kind=runtime_status.get("runtime_kind"),
            activation_status=str(runtime_status.get("activation_status") or "unknown"),
            conformance_status=str(runtime_status.get("conformance_status") or "not_run"),
            smoke_status=str(runtime_status.get("smoke_status") or "not_run"),
            pending_proposal_count=sum(1 for item in pending_specs if item.get("item_type") == "skill_invocation_proposal"),
            pending_review_count=sum(1 for item in pending_specs if "review" in str(item.get("item_type"))),
            recent_execution_count=len(recent_specs),
            blocked_execution_count=sum(1 for item in recent_specs if item.get("blocked")),
            failed_execution_count=sum(1 for item in recent_specs if item.get("failed")),
            promotion_candidate_count=len(promotion_candidates),
            summary_candidate_count=len(summary_candidates),
            created_at=utc_now_iso(),
            snapshot_attrs={
                "read_only": True,
                "paths_redacted": not show_paths,
                "source_bodies_printed": False,
                "skills_executed": False,
                "reviews_auto_approved": False,
                "bridge_auto_executed": False,
                "permission_grants_created": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_snapshot = snapshot
        self._record(
            "personal_runtime_workbench_snapshot_created",
            objects=[_object("personal_runtime_workbench_snapshot", snapshot.snapshot_id, snapshot.to_dict())],
            links=[("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)],
            object_links=[],
            attrs={"activation_status": snapshot.activation_status},
        )
        if not snapshot.personal_directory_configured:
            self.record_finding(
                snapshot=snapshot,
                finding_type="missing_personal_directory",
                status="warning",
                severity="medium",
                message="Personal Directory is not configured; Workbench remains read-only.",
                subject_ref=None,
            )
        self.collect_pending_items(source_data=source_data, snapshot=snapshot, limit=limit)
        self.collect_recent_activities(source_data=source_data, snapshot=snapshot, limit=limit)
        self.collect_blockers(snapshot=snapshot)
        self.collect_candidates(source_data=source_data, snapshot=snapshot, limit=limit)
        self.collect_summary_candidates(source_data=source_data, snapshot=snapshot, limit=limit)
        self.collect_health_findings(snapshot=snapshot, runtime_status=runtime_status)
        self._record_default_panels(snapshot)
        return snapshot

    def collect_runtime_status(self, *, source_data: dict[str, list[dict[str, Any]]], show_paths: bool = False) -> dict[str, Any]:
        status_rows = source_data.get("personal_runtime_status_snapshot") or []
        activation_rows = source_data.get("personal_prompt_activation_config") or []
        status = status_rows[0] if status_rows else {}
        activation = activation_rows[0] if activation_rows else {}
        directory_configured = bool(
            status.get("personal_directory_configured")
            or activation.get("personal_directory_configured")
            or os.environ.get("CHANTA_PERSONAL_DIRECTORY")
        )
        return _redact_mapping(
            {
                "personal_directory_configured": directory_configured,
                "selected_mode_name": activation.get("selected_mode_name"),
                "selected_profile_name": activation.get("selected_profile_name"),
                "runtime_kind": activation.get("runtime_kind") or status.get("runtime_kind"),
                "activation_status": activation.get("status") or "inactive",
                "conformance_status": status.get("conformance_status") or _latest_status(source_data.get("personal_conformance_result")),
                "smoke_status": status.get("smoke_status") or _latest_status(source_data.get("personal_smoke_test_result")),
            },
            show_paths=show_paths,
        )

    def collect_pending_items(self, *, source_data: dict[str, list[dict[str, Any]]], snapshot: PersonalRuntimeWorkbenchSnapshot | None, limit: int = 20) -> list[dict[str, Any]]:
        specs: list[dict[str, Any]] = []
        for item in source_data.get("skill_invocation_proposal") or []:
            status = str(item.get("proposal_status") or item.get("status") or "proposed")
            if status in {"proposed", "incomplete", "needs_review"} or item.get("review_required"):
                specs.append(_pending_spec("skill_invocation_proposal", item.get("proposal_id"), "Skill Proposal", status, "medium", item.get("reason")))
        for item in source_data.get("skill_proposal_review_request") or []:
            status = str(item.get("status") or "pending_review")
            if status in {"pending_review", "needs_review", "open"}:
                specs.append(_pending_spec("skill_proposal_review", item.get("review_request_id"), "Skill Proposal Review", status, "high", "Human review is pending."))
        for item in source_data.get("execution_result_promotion_candidate") or []:
            if str(item.get("review_status") or "") == "pending_review":
                specs.append(_pending_spec("promotion_candidate", item.get("candidate_id"), str(item.get("candidate_title") or "Promotion Candidate"), "pending_review", "medium", "Promotion candidate awaits review.", {"source_ref": item.get("source_ref"), "target_kind": item.get("target_kind")}))
        for item in source_data.get("workspace_read_summary_candidate") or []:
            if str(item.get("review_status") or "") == "pending_review":
                specs.append(_pending_spec("workspace_summary_candidate", item.get("summary_candidate_id"), str(item.get("candidate_title") or "Workspace Summary Candidate"), "pending_review", "medium", "Summary candidate awaits review.", {"target_kind": item.get("target_kind")}))
        specs = specs[: _limit(limit)]
        if snapshot is not None:
            for item in specs:
                self.record_pending_item(snapshot=snapshot, **item)
        return specs

    def collect_recent_activities(self, *, source_data: dict[str, list[dict[str, Any]]], snapshot: PersonalRuntimeWorkbenchSnapshot | None, limit: int = 20) -> list[dict[str, Any]]:
        specs: list[dict[str, Any]] = []
        for item in source_data.get("execution_envelope") or []:
            status = str(item.get("status") or "unknown")
            specs.append(
                {
                    "activity_type": "execution_envelope",
                    "activity_ref": item.get("envelope_id"),
                    "title": f"Execution Envelope: {item.get('skill_id') or 'unknown skill'}",
                    "status": status,
                    "blocked": bool(item.get("blocked")),
                    "failed": status in {"failed", "error"},
                    "skill_id": item.get("skill_id"),
                    "activity_attrs": {"execution_performed": bool(item.get("execution_performed"))},
                }
            )
        for item in source_data.get("reviewed_execution_bridge_result") or []:
            status = str(item.get("status") or "unknown")
            specs.append(
                {
                    "activity_type": "reviewed_execution_bridge_result",
                    "activity_ref": item.get("bridge_result_id"),
                    "title": "Reviewed Execution Bridge",
                    "status": status,
                    "blocked": bool(item.get("blocked")),
                    "failed": status in {"failed", "error"},
                    "skill_id": None,
                    "activity_attrs": {"executed": bool(item.get("executed"))},
                }
            )
        specs = sorted(specs, key=lambda row: str(row.get("created_at") or ""), reverse=True)[: _limit(limit)]
        if snapshot is not None:
            for item in specs:
                self.record_recent_activity(snapshot=snapshot, **item)
        return specs

    def collect_blockers(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot) -> list[PersonalRuntimeWorkbenchRecentActivity]:
        blocked = [item for item in self.last_recent_activities if item.blocked or item.failed]
        if not blocked:
            self.record_panel(snapshot=snapshot, panel_type="blockers", title="Blockers", status="clear", item_count=0, summary="No blocked or failed recent activities.")
        return blocked

    def collect_candidates(self, *, source_data: dict[str, list[dict[str, Any]]], snapshot: PersonalRuntimeWorkbenchSnapshot | None, limit: int = 20) -> list[dict[str, Any]]:
        candidates = (source_data.get("execution_result_promotion_candidate") or [])[: _limit(limit)]
        if snapshot is not None and not candidates:
            self.record_panel(snapshot=snapshot, panel_type="promotion_candidates", title="Promotion Candidates", status="empty", item_count=0, summary="No promotion candidates found.")
        return candidates

    def collect_summary_candidates(self, *, source_data: dict[str, list[dict[str, Any]]], snapshot: PersonalRuntimeWorkbenchSnapshot | None, limit: int = 20) -> list[dict[str, Any]]:
        candidates = (source_data.get("workspace_read_summary_candidate") or [])[: _limit(limit)]
        if snapshot is not None and not candidates:
            self.record_panel(snapshot=snapshot, panel_type="summary_candidates", title="Summary Candidates", status="empty", item_count=0, summary="No workspace summary candidates found.")
        return candidates

    def collect_health_findings(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, runtime_status: dict[str, Any]) -> list[PersonalRuntimeWorkbenchFinding]:
        if snapshot.conformance_status in {"failed", "error"}:
            self.record_finding(snapshot=snapshot, finding_type="conformance_failed", status=snapshot.conformance_status, severity="high", message="Conformance status requires operator attention.", subject_ref=None)
        if snapshot.smoke_status in {"failed", "error"}:
            self.record_finding(snapshot=snapshot, finding_type="smoke_failed", status=snapshot.smoke_status, severity="high", message="Smoke status requires operator attention.", subject_ref=None)
        if runtime_status.get("activation_status") in {"missing_config", "denied"}:
            self.record_finding(snapshot=snapshot, finding_type="activation_attention", status=str(runtime_status.get("activation_status")), severity="medium", message="Activation status requires operator attention.", subject_ref=None)
        return self.last_findings

    def record_panel(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, panel_type: str, title: str, status: str, item_count: int, summary: str, panel_attrs: dict[str, Any] | None = None) -> PersonalRuntimeWorkbenchPanel:
        panel = PersonalRuntimeWorkbenchPanel(new_personal_runtime_workbench_panel_id(), snapshot.snapshot_id, panel_type, title, status, item_count, summary, utc_now_iso(), {"read_only": True, **dict(panel_attrs or {})})
        self.last_panels.append(panel)
        self._record("personal_runtime_workbench_panel_created", objects=[_object("personal_runtime_workbench_panel", panel.panel_id, panel.to_dict())], links=[("personal_runtime_workbench_panel_object", panel.panel_id), ("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)], object_links=[(panel.panel_id, snapshot.snapshot_id, "belongs_to_snapshot")], attrs={"panel_type": panel.panel_type, "status": panel.status})
        return panel

    def record_pending_item(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, item_type: str, item_ref: str | None, title: str, status: str, priority: str, reason: str | None, item_attrs: dict[str, Any] | None = None) -> PersonalRuntimeWorkbenchPendingItem:
        item = PersonalRuntimeWorkbenchPendingItem(new_personal_runtime_workbench_pending_item_id(), snapshot.snapshot_id, item_type, item_ref, title, status, priority, reason, utc_now_iso(), {"read_only": True, **dict(item_attrs or {})})
        self.last_pending_items.append(item)
        self._record("personal_runtime_workbench_pending_item_recorded", objects=[_object("personal_runtime_workbench_pending_item", item.pending_item_id, item.to_dict())], links=[("personal_runtime_workbench_pending_item_object", item.pending_item_id), ("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)] + ([("source_object", item_ref)] if item_ref else []), object_links=[(item.pending_item_id, snapshot.snapshot_id, "belongs_to_snapshot")], attrs={"item_type": item.item_type, "status": item.status})
        return item

    def record_recent_activity(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, activity_type: str, activity_ref: str | None, title: str, status: str, blocked: bool, failed: bool, skill_id: str | None, activity_attrs: dict[str, Any] | None = None) -> PersonalRuntimeWorkbenchRecentActivity:
        item = PersonalRuntimeWorkbenchRecentActivity(new_personal_runtime_workbench_recent_activity_id(), snapshot.snapshot_id, activity_type, activity_ref, title, status, blocked, failed, skill_id, utc_now_iso(), {"read_only": True, **dict(activity_attrs or {})})
        self.last_recent_activities.append(item)
        self._record("personal_runtime_workbench_recent_activity_recorded", objects=[_object("personal_runtime_workbench_recent_activity", item.activity_id, item.to_dict())], links=[("personal_runtime_workbench_recent_activity_object", item.activity_id), ("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)] + ([("source_object", activity_ref)] if activity_ref else []), object_links=[(item.activity_id, snapshot.snapshot_id, "belongs_to_snapshot")], attrs={"activity_type": item.activity_type, "status": item.status, "blocked": item.blocked, "failed": item.failed})
        return item

    def record_finding(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, finding_type: str, status: str, severity: str, message: str, subject_ref: str | None, finding_attrs: dict[str, Any] | None = None) -> PersonalRuntimeWorkbenchFinding:
        finding = PersonalRuntimeWorkbenchFinding(new_personal_runtime_workbench_finding_id(), snapshot.snapshot_id, finding_type, status, severity, message, subject_ref, utc_now_iso(), {"read_only": True, **dict(finding_attrs or {})})
        self.last_findings.append(finding)
        self._record("personal_runtime_workbench_finding_recorded", objects=[_object("personal_runtime_workbench_finding", finding.finding_id, finding.to_dict())], links=[("personal_runtime_workbench_finding_object", finding.finding_id), ("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)], object_links=[(finding.finding_id, snapshot.snapshot_id, "belongs_to_snapshot")], attrs={"finding_type": finding.finding_type, "status": finding.status})
        return finding

    def record_result(self, *, snapshot: PersonalRuntimeWorkbenchSnapshot, command_name: str, status: str | None = None, summary: str | None = None) -> PersonalRuntimeWorkbenchResult:
        result = PersonalRuntimeWorkbenchResult(
            result_id=new_personal_runtime_workbench_result_id(),
            snapshot_id=snapshot.snapshot_id,
            command_name=command_name,
            status=status or ("needs_review" if self.last_findings else "completed"),
            panel_ids=[item.panel_id for item in self.last_panels],
            pending_item_ids=[item.pending_item_id for item in self.last_pending_items],
            recent_activity_ids=[item.activity_id for item in self.last_recent_activities],
            finding_ids=[item.finding_id for item in self.last_findings],
            summary=summary or f"Workbench {command_name} rendered read-only status.",
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "paths_redacted": bool(snapshot.snapshot_attrs.get("paths_redacted")),
                "skills_executed": False,
                "reviews_auto_approved": False,
                "bridge_auto_executed": False,
                "promotion_performed": False,
                "permission_grants_created": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_result = result
        self._record(
            "personal_runtime_workbench_result_recorded",
            objects=[_object("personal_runtime_workbench_result", result.result_id, result.to_dict())],
            links=[("personal_runtime_workbench_result_object", result.result_id), ("personal_runtime_workbench_snapshot_object", snapshot.snapshot_id)],
            object_links=[(result.result_id, snapshot.snapshot_id, "summarizes_snapshot")],
            attrs={"command_name": command_name, "status": result.status},
        )
        self._record("personal_runtime_workbench_rendered", objects=[_object("personal_runtime_workbench_result", result.result_id, result.to_dict())], links=[("personal_runtime_workbench_result_object", result.result_id)], object_links=[], attrs={"command_name": command_name, "status": result.status})
        return result

    def render_workbench_status(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="status", result=result)

    def render_workbench_recent(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="recent", result=result, include_recent=True)

    def render_workbench_pending(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="pending", result=result, include_pending=True)

    def render_workbench_blockers(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="blockers", result=result, include_recent=True, only_blockers=True)

    def render_workbench_candidates(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="candidates", result=result, include_pending=True, item_filter={"promotion_candidate"})

    def render_workbench_summaries(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="summaries", result=result, include_pending=True, item_filter={"workspace_summary_candidate"})

    def render_workbench_health(self, result: PersonalRuntimeWorkbenchResult | None = None) -> str:
        return self._render(command_name="health", result=result, include_findings=True)

    def _record_default_panels(self, snapshot: PersonalRuntimeWorkbenchSnapshot) -> None:
        self.record_panel(snapshot=snapshot, panel_type="status", title="Runtime Status", status=snapshot.activation_status, item_count=1, summary=f"Activation={snapshot.activation_status}; conformance={snapshot.conformance_status}; smoke={snapshot.smoke_status}.")
        self.record_panel(snapshot=snapshot, panel_type="pending", title="Pending Work", status="pending" if self.last_pending_items else "empty", item_count=len(self.last_pending_items), summary=f"{len(self.last_pending_items)} pending items.")
        self.record_panel(snapshot=snapshot, panel_type="recent", title="Recent Activity", status="available" if self.last_recent_activities else "empty", item_count=len(self.last_recent_activities), summary=f"{len(self.last_recent_activities)} recent activities.")
        self.record_panel(snapshot=snapshot, panel_type="health", title="Health", status="needs_review" if self.last_findings else "clear", item_count=len(self.last_findings), summary=f"{len(self.last_findings)} findings.")

    def _read_source_data(self, *, limit: int, show_paths: bool) -> dict[str, list[dict[str, Any]]]:
        object_types = [
            "personal_runtime_status_snapshot",
            "personal_prompt_activation_config",
            "personal_conformance_result",
            "personal_smoke_test_result",
            "skill_invocation_proposal",
            "skill_proposal_review_request",
            "reviewed_execution_bridge_result",
            "execution_envelope",
            "execution_result_promotion_candidate",
            "workspace_read_summary_candidate",
        ]
        data: dict[str, list[dict[str, Any]]] = {}
        for object_type in object_types:
            data[object_type] = [_redact_mapping(row["object_attrs"], show_paths=show_paths) for row in self.ocel_store.fetch_objects_by_type(object_type)][- _limit(limit):]
        for object_type, source in self.sources.items():
            if source is None:
                continue
            data[f"source:{object_type}"] = [_redact_mapping(_to_public_dict(item), show_paths=show_paths) for item in _as_items(source)]
        return data

    def _render(self, *, command_name: str, result: PersonalRuntimeWorkbenchResult | None, include_pending: bool = False, include_recent: bool = False, include_findings: bool = False, only_blockers: bool = False, item_filter: set[str] | None = None) -> str:
        active_result = result or self.last_result
        snapshot = self.last_snapshot
        if active_result is None or snapshot is None:
            return "Personal Runtime Workbench: unavailable"
        lines = [
            "Personal Runtime Workbench",
            f"command={command_name}",
            f"status={active_result.status}",
            f"personal_directory_configured={str(snapshot.personal_directory_configured).lower()}",
            f"activation_status={snapshot.activation_status}",
            f"conformance_status={snapshot.conformance_status}",
            f"smoke_status={snapshot.smoke_status}",
            f"pending_proposals={snapshot.pending_proposal_count}",
            f"pending_reviews={snapshot.pending_review_count}",
            f"recent_executions={snapshot.recent_execution_count}",
            f"blocked_executions={snapshot.blocked_execution_count}",
            f"failed_executions={snapshot.failed_execution_count}",
            f"promotion_candidates={snapshot.promotion_candidate_count}",
            f"summary_candidates={snapshot.summary_candidate_count}",
            f"paths_redacted={str(snapshot.snapshot_attrs.get('paths_redacted')).lower()}",
        ]
        if include_pending:
            selected = [item for item in self.last_pending_items if item_filter is None or item.item_type in item_filter]
            lines.append("pending_items=none" if not selected else "pending_items:")
            lines.extend(f"- {item.item_type} | {item.status} | {item.title} | ref={item.item_ref or 'none'}" for item in selected)
        if include_recent:
            selected_recent = [item for item in self.last_recent_activities if (item.blocked or item.failed) or not only_blockers]
            lines.append("recent_activities=none" if not selected_recent else "recent_activities:")
            lines.extend(f"- {item.activity_type} | {item.status} | blocked={str(item.blocked).lower()} | failed={str(item.failed).lower()} | skill={item.skill_id or 'none'}" for item in selected_recent)
        if include_findings:
            lines.append("findings=none" if not self.last_findings else "findings:")
            lines.extend(f"- {item.finding_type} | {item.status} | {item.severity} | {item.message}" for item in self.last_findings)
        lines.extend(
            [
                "source_bodies_printed=false",
                "skills_executed=false",
                "reviews_auto_approved=false",
                "bridge_auto_executed=false",
                "promotion_performed=false",
                "permission_grants_created=false",
                "memory_entries_written=false",
                "persona_updated=false",
                "overlay_updated=false",
            ]
        )
        return "\n".join(lines)

    def _record(self, activity: str, *, objects: list[OCELObject], links: list[tuple[str, str | None]], object_links: list[tuple[str, str | None, str]], attrs: dict[str, Any]) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "personal_runtime_workbench": True,
                "read_only": True,
                "skills_executed": False,
                "reviews_auto_approved": False,
                "bridge_auto_executed": False,
                "permission_grants_created": False,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
                "model_call_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
            },
        )
        relations = [OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier) for qualifier, object_id in links if object_id]
        relations.extend(OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier) for source_id, target_id, qualifier in object_links if source_id and target_id)
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _pending_spec(item_type: str, item_ref: Any, title: str, status: str, priority: str, reason: Any, item_attrs: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "item_type": item_type,
        "item_ref": str(item_ref) if item_ref else None,
        "title": title,
        "status": status,
        "priority": priority,
        "reason": str(reason) if reason else None,
        "item_attrs": dict(item_attrs or {}),
    }


def _latest_status(items: list[dict[str, Any]] | None) -> str:
    if not items:
        return "not_run"
    return str(items[0].get("status") or "unknown")


def _limit(value: int | None) -> int:
    return max(1, min(int(value or 20), 100))


def _as_items(source: Any) -> list[Any]:
    if isinstance(source, list):
        return source
    if isinstance(source, tuple):
        return list(source)
    if hasattr(source, "last_result") and source.last_result is not None:
        return [source.last_result]
    if hasattr(source, "last_candidate") and source.last_candidate is not None:
        return [source.last_candidate]
    if hasattr(source, "last_snapshot") and source.last_snapshot is not None:
        return [source.last_snapshot]
    return []


def _to_public_dict(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return dict(item)
    if hasattr(item, "to_dict"):
        return dict(item.to_dict())
    return {"value": str(item)}


def _redact_mapping(value: dict[str, Any], *, show_paths: bool) -> dict[str, Any]:
    return {str(key): _redact_value(item, key=str(key), show_paths=show_paths) for key, item in value.items()}


def _redact_value(value: Any, *, key: str, show_paths: bool) -> Any:
    normalized = key.lower()
    if normalized in SENSITIVE_KEYS:
        return "<REDACTED>"
    if not show_paths and (normalized in PATH_KEYS or normalized.endswith("_path")):
        return "<REDACTED_PATH>"
    if isinstance(value, dict):
        return _redact_mapping(value, show_paths=show_paths)
    if isinstance(value, list):
        return [_redact_value(item, key=key, show_paths=show_paths) for item in value]
    return value


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id, "display_name": object_id, **attrs})

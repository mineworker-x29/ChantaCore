from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.execution.ids import (
    new_execution_audit_filter_id,
    new_execution_audit_finding_id,
    new_execution_audit_query_id,
    new_execution_audit_record_view_id,
    new_execution_audit_result_id,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SENSITIVE_KEYS = {"password", "token", "secret", "api_key", "private_key", "credential"}
PATH_KEYS = {
    "path",
    "root_path",
    "relative_path",
    "file_path",
    "workspace_root",
    "output_ref",
    "artifact_ref",
}


@dataclass(frozen=True)
class ExecutionAuditQuery:
    audit_query_id: str
    query_type: str
    requested_by: str | None
    session_id: str | None
    turn_id: str | None
    limit: int
    show_paths: bool
    show_full_payloads: bool
    created_at: str
    query_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_query_id": self.audit_query_id,
            "query_type": self.query_type,
            "requested_by": self.requested_by,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "limit": self.limit,
            "show_paths": self.show_paths,
            "show_full_payloads": self.show_full_payloads,
            "created_at": self.created_at,
            "query_attrs": dict(self.query_attrs),
        }


@dataclass(frozen=True)
class ExecutionAuditFilter:
    audit_filter_id: str
    audit_query_id: str
    envelope_id: str | None
    skill_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    status: str | None
    execution_kind: str | None
    blocked: bool | None
    failed: bool | None
    since: str | None
    until: str | None
    limit: int
    created_at: str
    filter_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_filter_id": self.audit_filter_id,
            "audit_query_id": self.audit_query_id,
            "envelope_id": self.envelope_id,
            "skill_id": self.skill_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "execution_kind": self.execution_kind,
            "blocked": self.blocked,
            "failed": self.failed,
            "since": self.since,
            "until": self.until,
            "limit": self.limit,
            "created_at": self.created_at,
            "filter_attrs": dict(self.filter_attrs),
        }


@dataclass(frozen=True)
class ExecutionAuditRecordView:
    record_view_id: str
    audit_query_id: str
    envelope_id: str
    execution_kind: str
    skill_id: str | None
    status: str
    execution_allowed: bool
    execution_performed: bool
    blocked: bool
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    gate_decision_id: str | None
    gate_result_id: str | None
    explicit_invocation_result_id: str | None
    output_snapshot_id: str | None
    output_preview: dict[str, Any]
    input_preview: dict[str, Any]
    redacted: bool
    created_at: str
    view_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_view_id": self.record_view_id,
            "audit_query_id": self.audit_query_id,
            "envelope_id": self.envelope_id,
            "execution_kind": self.execution_kind,
            "skill_id": self.skill_id,
            "status": self.status,
            "execution_allowed": self.execution_allowed,
            "execution_performed": self.execution_performed,
            "blocked": self.blocked,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "gate_decision_id": self.gate_decision_id,
            "gate_result_id": self.gate_result_id,
            "explicit_invocation_result_id": self.explicit_invocation_result_id,
            "output_snapshot_id": self.output_snapshot_id,
            "output_preview": dict(self.output_preview),
            "input_preview": dict(self.input_preview),
            "redacted": self.redacted,
            "created_at": self.created_at,
            "view_attrs": dict(self.view_attrs),
        }


@dataclass(frozen=True)
class ExecutionAuditResult:
    audit_result_id: str
    audit_query_id: str
    filter_id: str
    status: str
    matched_count: int
    returned_count: int
    record_view_ids: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_result_id": self.audit_result_id,
            "audit_query_id": self.audit_query_id,
            "filter_id": self.filter_id,
            "status": self.status,
            "matched_count": self.matched_count,
            "returned_count": self.returned_count,
            "record_view_ids": list(self.record_view_ids),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class ExecutionAuditFinding:
    finding_id: str
    audit_query_id: str
    envelope_id: str | None
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
            "audit_query_id": self.audit_query_id,
            "envelope_id": self.envelope_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


class ExecutionAuditService:
    def __init__(
        self,
        *,
        execution_envelope_store: OCELStore | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.ocel_store = execution_envelope_store or ocel_store or OCELStore()
        if trace_service is not None:
            self.trace_service = trace_service
        else:
            self.trace_service = TraceService(ocel_store=self.ocel_store)
        self.last_query: ExecutionAuditQuery | None = None
        self.last_filter: ExecutionAuditFilter | None = None
        self.last_record_views: list[ExecutionAuditRecordView] = []
        self.last_findings: list[ExecutionAuditFinding] = []
        self.last_result: ExecutionAuditResult | None = None

    def create_query(
        self,
        *,
        query_type: str,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        limit: int | None = None,
        show_paths: bool = False,
        show_full_payloads: bool = False,
        query_attrs: dict[str, Any] | None = None,
    ) -> ExecutionAuditQuery:
        item = ExecutionAuditQuery(
            audit_query_id=new_execution_audit_query_id(),
            query_type=query_type,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            limit=_limit(limit),
            show_paths=show_paths,
            show_full_payloads=show_full_payloads,
            created_at=utc_now_iso(),
            query_attrs={
                "read_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "promotion_candidates_created": False,
                **dict(query_attrs or {}),
            },
        )
        self.last_query = item
        self._record(
            "execution_audit_query_requested",
            objects=[_object("execution_audit_query", item.audit_query_id, item.to_dict())],
            links=[("execution_audit_query_object", item.audit_query_id)],
            object_links=[],
            attrs={"query_type": item.query_type},
        )
        return item

    def create_filter(
        self,
        *,
        query: ExecutionAuditQuery,
        envelope_id: str | None = None,
        skill_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        status: str | None = None,
        execution_kind: str | None = None,
        blocked: bool | None = None,
        failed: bool | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        filter_attrs: dict[str, Any] | None = None,
    ) -> ExecutionAuditFilter:
        item = ExecutionAuditFilter(
            audit_filter_id=new_execution_audit_filter_id(),
            audit_query_id=query.audit_query_id,
            envelope_id=envelope_id,
            skill_id=skill_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status=status,
            execution_kind=execution_kind,
            blocked=blocked,
            failed=failed,
            since=since,
            until=until,
            limit=_limit(limit if limit is not None else query.limit),
            created_at=utc_now_iso(),
            filter_attrs=dict(filter_attrs or {}),
        )
        self.last_filter = item
        self._record(
            "execution_audit_filter_applied",
            objects=[_object("execution_audit_filter", item.audit_filter_id, item.to_dict())],
            links=[
                ("execution_audit_filter_object", item.audit_filter_id),
                ("execution_audit_query_object", query.audit_query_id),
            ],
            object_links=[(item.audit_filter_id, query.audit_query_id, "belongs_to_query")],
            attrs={"query_type": query.query_type},
        )
        return item

    def query_envelopes(
        self,
        *,
        query_type: str = "list",
        envelope_id: str | None = None,
        skill_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        status: str | None = None,
        execution_kind: str | None = None,
        blocked: bool | None = None,
        failed: bool | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        show_paths: bool = False,
        show_full_payloads: bool = False,
        requested_by: str | None = None,
    ) -> ExecutionAuditResult:
        self.last_record_views = []
        self.last_findings = []
        query = self.create_query(
            query_type=query_type,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            limit=limit,
            show_paths=show_paths,
            show_full_payloads=show_full_payloads,
        )
        audit_filter = self.create_filter(
            query=query,
            envelope_id=envelope_id,
            skill_id=skill_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status=status,
            execution_kind=execution_kind,
            blocked=blocked,
            failed=failed,
            since=since,
            until=until,
            limit=limit,
        )
        all_records = self._read_execution_records()
        matched = [item for item in all_records if _matches_filter(item["envelope"], audit_filter)]
        returned = matched[: audit_filter.limit]
        if envelope_id and not matched:
            self.record_finding(
                query=query,
                envelope_id=envelope_id,
                finding_type="envelope_not_found",
                status="not_found",
                severity="medium",
                message="Execution envelope was not found.",
                subject_ref=envelope_id,
            )
            return self.record_result(query=query, audit_filter=audit_filter, status="not_found", matched_count=0)
        if not matched:
            self.record_finding(
                query=query,
                envelope_id=None,
                finding_type="empty_result",
                status="empty",
                severity="low",
                message="No execution envelopes matched the query.",
                subject_ref=None,
            )
        for record in returned:
            view = self.create_record_view(
                query=query,
                record=record,
                show_paths=show_paths,
                show_full_payloads=show_full_payloads,
            )
            if record.get("input") and not show_full_payloads:
                self.record_finding(
                    query=query,
                    envelope_id=view.envelope_id,
                    finding_type="full_payload_hidden",
                    status="hidden",
                    severity="low",
                    message="Full input payload is hidden by default.",
                    subject_ref=view.envelope_id,
                )
            if record.get("output") and not show_full_payloads:
                self.record_finding(
                    query=query,
                    envelope_id=view.envelope_id,
                    finding_type="full_payload_hidden",
                    status="hidden",
                    severity="low",
                    message="Full output payload is hidden by default.",
                    subject_ref=view.envelope_id,
                )
            if view.blocked:
                self.record_finding(
                    query=query,
                    envelope_id=view.envelope_id,
                    finding_type="blocked_execution",
                    status="blocked",
                    severity="high",
                    message="Execution envelope is blocked.",
                    subject_ref=view.envelope_id,
                )
            if _is_failed_status(view.status):
                self.record_finding(
                    query=query,
                    envelope_id=view.envelope_id,
                    finding_type="failed_execution",
                    status="failed",
                    severity="high",
                    message="Execution envelope failed.",
                    subject_ref=view.envelope_id,
                )
        result_status = "empty" if not matched else "completed"
        return self.record_result(
            query=query,
            audit_filter=audit_filter,
            status=result_status,
            matched_count=len(matched),
        )

    def recent_envelopes(self, **kwargs: Any) -> ExecutionAuditResult:
        kwargs.setdefault("query_type", "recent")
        return self.query_envelopes(**kwargs)

    def show_envelope(self, envelope_id: str, **kwargs: Any) -> ExecutionAuditResult:
        kwargs.setdefault("query_type", "show")
        kwargs["envelope_id"] = envelope_id
        kwargs.setdefault("limit", 1)
        return self.query_envelopes(**kwargs)

    def audit_envelopes(self, **kwargs: Any) -> ExecutionAuditResult:
        kwargs.setdefault("query_type", "audit")
        return self.query_envelopes(**kwargs)

    def create_record_view(
        self,
        *,
        query: ExecutionAuditQuery,
        record: dict[str, Any],
        show_paths: bool = False,
        show_full_payloads: bool = False,
    ) -> ExecutionAuditRecordView:
        envelope = record["envelope"]
        provenance = record.get("provenance") or {}
        output = record.get("output") or {}
        input_item = record.get("input") or {}
        input_preview = _safe_preview(input_item.get("input_preview"), show_paths=show_paths)
        output_preview = _safe_preview(output.get("output_preview"), show_paths=show_paths)
        if not show_full_payloads:
            input_preview = _mark_preview_only(input_preview)
            output_preview = _mark_preview_only(output_preview)
        view = ExecutionAuditRecordView(
            record_view_id=new_execution_audit_record_view_id(),
            audit_query_id=query.audit_query_id,
            envelope_id=str(envelope["envelope_id"]),
            execution_kind=str(envelope.get("execution_kind") or "unknown"),
            skill_id=envelope.get("skill_id"),
            status=str(envelope.get("status") or "unknown"),
            execution_allowed=bool(envelope.get("execution_allowed")),
            execution_performed=bool(envelope.get("execution_performed")),
            blocked=bool(envelope.get("blocked")),
            session_id=envelope.get("session_id"),
            turn_id=envelope.get("turn_id"),
            process_instance_id=envelope.get("process_instance_id"),
            gate_decision_id=provenance.get("gate_decision_id"),
            gate_result_id=provenance.get("gate_result_id"),
            explicit_invocation_result_id=provenance.get("explicit_invocation_result_id"),
            output_snapshot_id=output.get("output_snapshot_id"),
            output_preview=output_preview,
            input_preview=input_preview,
            redacted=(not show_paths) or (not show_full_payloads),
            created_at=utc_now_iso(),
            view_attrs={
                "full_payloads_shown": bool(show_full_payloads),
                "paths_shown": bool(show_paths),
                "read_only": True,
                "permission_grants_created": False,
                "promotion_candidates_created": False,
            },
        )
        self.last_record_views.append(view)
        self._record(
            "execution_audit_record_view_created",
            objects=[_object("execution_audit_record_view", view.record_view_id, view.to_dict())],
            links=[
                ("execution_audit_record_view_object", view.record_view_id),
                ("execution_audit_query_object", query.audit_query_id),
                ("execution_envelope_object", view.envelope_id),
            ],
            object_links=[
                (view.record_view_id, query.audit_query_id, "belongs_to_query"),
                (view.record_view_id, view.envelope_id, "views_execution_envelope"),
            ],
            attrs={"status": view.status, "skill_id": view.skill_id},
        )
        return view

    def record_finding(
        self,
        *,
        query: ExecutionAuditQuery,
        envelope_id: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ExecutionAuditFinding:
        finding = ExecutionAuditFinding(
            finding_id=new_execution_audit_finding_id(),
            audit_query_id=query.audit_query_id,
            envelope_id=envelope_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "read_only": True,
                "permission_grants_created": False,
                "promotion_candidates_created": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record(
            "execution_audit_finding_recorded",
            objects=[_object("execution_audit_finding", finding.finding_id, finding.to_dict())],
            links=[
                ("execution_audit_finding_object", finding.finding_id),
                ("execution_audit_query_object", query.audit_query_id),
            ]
            + ([("execution_envelope_object", envelope_id)] if envelope_id else []),
            object_links=[
                (finding.finding_id, query.audit_query_id, "belongs_to_query"),
            ]
            + ([(finding.finding_id, envelope_id, "references_execution_envelope")] if envelope_id else []),
            attrs={"finding_type": finding.finding_type, "status": finding.status},
        )
        return finding

    def record_result(
        self,
        *,
        query: ExecutionAuditQuery,
        audit_filter: ExecutionAuditFilter,
        status: str,
        matched_count: int,
    ) -> ExecutionAuditResult:
        result = ExecutionAuditResult(
            audit_result_id=new_execution_audit_result_id(),
            audit_query_id=query.audit_query_id,
            filter_id=audit_filter.audit_filter_id,
            status=status,
            matched_count=matched_count,
            returned_count=len(self.last_record_views),
            record_view_ids=[item.record_view_id for item in self.last_record_views],
            finding_ids=[item.finding_id for item in self.last_findings],
            summary=f"{status}: matched={matched_count}; returned={len(self.last_record_views)}",
            created_at=utc_now_iso(),
            result_attrs={
                "query_type": query.query_type,
                "read_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "promotion_candidates_created": False,
            },
        )
        self.last_result = result
        self._record(
            "execution_audit_result_recorded",
            objects=[_object("execution_audit_result", result.audit_result_id, result.to_dict())],
            links=[
                ("execution_audit_result_object", result.audit_result_id),
                ("execution_audit_query_object", query.audit_query_id),
                ("execution_audit_filter_object", audit_filter.audit_filter_id),
            ]
            + [
                ("execution_audit_record_view_object", item.record_view_id)
                for item in self.last_record_views
            ],
            object_links=[
                (result.audit_result_id, query.audit_query_id, "summarizes_query"),
            ]
            + [
                (item.record_view_id, result.audit_result_id, "belongs_to_result")
                for item in self.last_record_views
            ],
            attrs={"status": result.status, "query_type": query.query_type},
        )
        if status == "empty":
            self._record_simple("execution_audit_empty", result=result)
        if status == "not_found":
            self._record_simple("execution_audit_not_found", result=result)
        self._record_simple("execution_audit_rendered", result=result)
        return result

    def render_audit_table(self, result: ExecutionAuditResult | None = None) -> str:
        item = result or self.last_result
        if item is None:
            return "Execution Audit: unavailable"
        if not self.last_record_views:
            return "\n".join(
                [
                    "Execution Audit",
                    f"status={item.status}",
                    f"matched_count={item.matched_count}",
                    "records=none",
                ]
            )
        rows = [
            "Execution Audit",
            f"status={item.status}",
            f"matched_count={item.matched_count}",
            f"returned_count={item.returned_count}",
            "envelope_id | skill_id | status | blocked | performed",
        ]
        rows.extend(
            f"{view.envelope_id} | {view.skill_id or 'none'} | {view.status} | "
            f"{str(view.blocked).lower()} | {str(view.execution_performed).lower()}"
            for view in self.last_record_views
        )
        return "\n".join(rows)

    def render_audit_detail(self, result: ExecutionAuditResult | None = None) -> str:
        item = result or self.last_result
        if item is None:
            return "Execution Audit: unavailable"
        if not self.last_record_views:
            return self.render_audit_table(item)
        view = self.last_record_views[0]
        return "\n".join(
            [
                "Execution Audit Detail",
                f"status={item.status}",
                f"envelope_id={view.envelope_id}",
                f"skill_id={view.skill_id or 'none'}",
                f"execution_kind={view.execution_kind}",
                f"execution_allowed={str(view.execution_allowed).lower()}",
                f"execution_performed={str(view.execution_performed).lower()}",
                f"blocked={str(view.blocked).lower()}",
                f"gate_decision_id={view.gate_decision_id or 'none'}",
                f"gate_result_id={view.gate_result_id or 'none'}",
                f"explicit_invocation_result_id={view.explicit_invocation_result_id or 'none'}",
                f"output_snapshot_id={view.output_snapshot_id or 'none'}",
                f"input_preview={view.input_preview}",
                f"output_preview={view.output_preview}",
                f"redacted={str(view.redacted).lower()}",
                "permission_grants_created=false",
                "promotion_candidates_created=false",
            ]
        )

    def _read_execution_records(self) -> list[dict[str, Any]]:
        envelopes = [
            row["object_attrs"] for row in self.ocel_store.fetch_objects_by_type("execution_envelope")
        ]
        provenance_by_envelope = _latest_by_envelope(
            self.ocel_store.fetch_objects_by_type("execution_provenance_record"),
            "envelope_id",
        )
        inputs_by_envelope = _latest_by_envelope(
            self.ocel_store.fetch_objects_by_type("execution_input_snapshot"),
            "envelope_id",
        )
        outputs_by_envelope = _latest_by_envelope(
            self.ocel_store.fetch_objects_by_type("execution_output_snapshot"),
            "envelope_id",
        )
        records = [
            {
                "envelope": envelope,
                "provenance": provenance_by_envelope.get(str(envelope.get("envelope_id"))),
                "input": inputs_by_envelope.get(str(envelope.get("envelope_id"))),
                "output": outputs_by_envelope.get(str(envelope.get("envelope_id"))),
            }
            for envelope in envelopes
        ]
        return sorted(records, key=lambda item: str(item["envelope"].get("created_at") or ""), reverse=True)

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "execution_audit": True,
                "read_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "promotion_candidates_created": False,
                "shell_execution_used": False,
                "network_access_used": False,
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _record_simple(self, activity: str, *, result: ExecutionAuditResult) -> None:
        self._record(
            activity,
            objects=[_object("execution_audit_result", result.audit_result_id, result.to_dict())],
            links=[("execution_audit_result_object", result.audit_result_id)],
            object_links=[],
            attrs={"status": result.status},
        )


def _limit(value: int | None) -> int:
    if value is None:
        return 20
    return max(1, min(int(value), 100))


def _latest_by_envelope(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        attrs = row["object_attrs"]
        envelope_id = str(attrs.get(key) or "")
        if not envelope_id:
            continue
        current = result.get(envelope_id)
        if current is None or str(attrs.get("created_at") or "") >= str(current.get("created_at") or ""):
            result[envelope_id] = attrs
    return result


def _matches_filter(envelope: dict[str, Any], audit_filter: ExecutionAuditFilter) -> bool:
    if audit_filter.envelope_id and envelope.get("envelope_id") != audit_filter.envelope_id:
        return False
    if audit_filter.skill_id and envelope.get("skill_id") != audit_filter.skill_id:
        return False
    if audit_filter.session_id and envelope.get("session_id") != audit_filter.session_id:
        return False
    if audit_filter.turn_id and envelope.get("turn_id") != audit_filter.turn_id:
        return False
    if audit_filter.process_instance_id and envelope.get("process_instance_id") != audit_filter.process_instance_id:
        return False
    if audit_filter.status and envelope.get("status") != audit_filter.status:
        return False
    if audit_filter.execution_kind and envelope.get("execution_kind") != audit_filter.execution_kind:
        return False
    if audit_filter.blocked is not None and bool(envelope.get("blocked")) is not audit_filter.blocked:
        return False
    if audit_filter.failed is not None and _is_failed_status(str(envelope.get("status") or "")) is not audit_filter.failed:
        return False
    created_at = str(envelope.get("created_at") or "")
    if audit_filter.since and created_at < audit_filter.since:
        return False
    if audit_filter.until and created_at > audit_filter.until:
        return False
    return True


def _is_failed_status(status: str) -> bool:
    return status in {"failed", "error"}


def _safe_preview(value: Any, *, show_paths: bool) -> dict[str, Any]:
    if isinstance(value, dict):
        return _redact_mapping(value, show_paths=show_paths)
    return {"value": _redact_value(value, key="value", show_paths=show_paths)}


def _redact_mapping(value: dict[str, Any], *, show_paths: bool) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, item in value.items():
        result[str(key)] = _redact_value(item, key=str(key), show_paths=show_paths)
    return result


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


def _mark_preview_only(value: dict[str, Any]) -> dict[str, Any]:
    return {**value, "_full_payload": "<HIDDEN>"}


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )

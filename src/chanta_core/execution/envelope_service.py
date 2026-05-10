from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import uuid4

from chanta_core.execution.ids import (
    new_execution_artifact_ref_id,
    new_execution_envelope_id,
    new_execution_input_snapshot_id,
    new_execution_outcome_summary_id,
    new_execution_output_snapshot_id,
    new_execution_provenance_record_id,
)
from chanta_core.execution.models import (
    ExecutionArtifactRef,
    ExecutionEnvelope,
    ExecutionInputSnapshot,
    ExecutionOutcomeSummary,
    ExecutionOutputSnapshot,
    ExecutionProvenanceRecord,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.execution_gate import (
    SkillExecutionGateDecision,
    SkillExecutionGateRequest,
    SkillExecutionGateResult,
)
from chanta_core.skills.invocation import (
    ExplicitSkillInvocationInput,
    ExplicitSkillInvocationRequest,
    ExplicitSkillInvocationResult,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


DEFAULT_SENSITIVE_KEYS = ["password", "token", "secret", "api_key", "private_key", "credential"]


class ExecutionEnvelopeService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.last_envelope: ExecutionEnvelope | None = None
        self.last_provenance: ExecutionProvenanceRecord | None = None
        self.last_input_snapshot: ExecutionInputSnapshot | None = None
        self.last_output_snapshot: ExecutionOutputSnapshot | None = None
        self.last_artifact_refs: list[ExecutionArtifactRef] = []
        self.last_outcome_summary: ExecutionOutcomeSummary | None = None

    def create_envelope(
        self,
        *,
        execution_kind: str,
        execution_subject_id: str | None,
        skill_id: str | None,
        status: str,
        execution_allowed: bool,
        execution_performed: bool,
        blocked: bool,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        started_at: str | None = None,
        completed_at: str | None = None,
        envelope_attrs: dict[str, Any] | None = None,
    ) -> ExecutionEnvelope:
        envelope = ExecutionEnvelope(
            envelope_id=new_execution_envelope_id(),
            execution_kind=execution_kind,
            execution_subject_id=execution_subject_id,
            skill_id=skill_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status=status,
            execution_allowed=execution_allowed,
            execution_performed=execution_performed,
            blocked=blocked,
            started_at=started_at,
            completed_at=completed_at,
            created_at=utc_now_iso(),
            envelope_attrs={
                "capabilities_granted": False,
                "skills_executed_by_envelope": False,
                "full_input_stored": False,
                "full_output_stored": False,
                "line_delimited_store_created": False,
                **dict(envelope_attrs or {}),
            },
        )
        self.last_envelope = envelope
        self._record(
            "execution_envelope_created",
            objects=[_object("execution_envelope", envelope.envelope_id, envelope.to_dict())],
            links=[("execution_envelope_object", envelope.envelope_id)],
            object_links=[],
            attrs={"status": envelope.status, "execution_kind": envelope.execution_kind},
        )
        return envelope

    def record_provenance(
        self,
        *,
        envelope: ExecutionEnvelope,
        actor_type: str | None = None,
        actor_id: str | None = None,
        runtime_kind: str | None = None,
        invocation_mode: str | None = None,
        proposal_id: str | None = None,
        explicit_invocation_request_id: str | None = None,
        explicit_invocation_result_id: str | None = None,
        gate_request_id: str | None = None,
        gate_decision_id: str | None = None,
        gate_result_id: str | None = None,
        capability_decision_id: str | None = None,
        permission_request_id: str | None = None,
        permission_decision_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        sandbox_ref_ids: list[str] | None = None,
        risk_ref_ids: list[str] | None = None,
        provenance_attrs: dict[str, Any] | None = None,
    ) -> ExecutionProvenanceRecord:
        record = ExecutionProvenanceRecord(
            provenance_id=new_execution_provenance_record_id(),
            envelope_id=envelope.envelope_id,
            actor_type=actor_type,
            actor_id=actor_id,
            runtime_kind=runtime_kind,
            invocation_mode=invocation_mode,
            proposal_id=proposal_id,
            explicit_invocation_request_id=explicit_invocation_request_id,
            explicit_invocation_result_id=explicit_invocation_result_id,
            gate_request_id=gate_request_id,
            gate_decision_id=gate_decision_id,
            gate_result_id=gate_result_id,
            capability_decision_id=capability_decision_id,
            permission_request_id=permission_request_id,
            permission_decision_id=permission_decision_id,
            session_permission_resolution_id=session_permission_resolution_id,
            sandbox_ref_ids=list(sandbox_ref_ids or []),
            risk_ref_ids=list(risk_ref_ids or []),
            created_at=utc_now_iso(),
            provenance_attrs={
                "capabilities_granted": False,
                "skills_executed_by_envelope": False,
                **dict(provenance_attrs or {}),
            },
        )
        self.last_provenance = record
        self._record(
            "execution_provenance_recorded",
            objects=[_object("execution_provenance_record", record.provenance_id, record.to_dict())],
            links=[("execution_provenance_record_object", record.provenance_id), ("execution_envelope_object", envelope.envelope_id)]
            + _reference_links(record),
            object_links=[(record.provenance_id, envelope.envelope_id, "belongs_to_execution_envelope")],
            attrs={"execution_kind": envelope.execution_kind},
        )
        return record

    def record_input_snapshot(
        self,
        *,
        envelope: ExecutionEnvelope,
        input_payload: Any,
        input_kind: str = "explicit_skill_input",
        input_attrs: dict[str, Any] | None = None,
    ) -> ExecutionInputSnapshot:
        redacted_payload, redacted_fields = redact_sensitive_fields(_as_mapping(input_payload))
        snapshot = ExecutionInputSnapshot(
            input_snapshot_id=new_execution_input_snapshot_id(),
            envelope_id=envelope.envelope_id,
            input_kind=input_kind,
            input_preview=preview_payload(redacted_payload),
            input_hash=hash_payload(input_payload),
            redacted_fields=redacted_fields,
            full_input_stored=False,
            created_at=utc_now_iso(),
            input_attrs={
                "preview_only": True,
                "body_stored": False,
                **dict(input_attrs or {}),
            },
        )
        self.last_input_snapshot = snapshot
        self._record(
            "execution_input_snapshot_recorded",
            objects=[_object("execution_input_snapshot", snapshot.input_snapshot_id, snapshot.to_dict())],
            links=[("execution_input_snapshot_object", snapshot.input_snapshot_id), ("execution_envelope_object", envelope.envelope_id)],
            object_links=[(snapshot.input_snapshot_id, envelope.envelope_id, "belongs_to_execution_envelope")],
            attrs={"input_kind": snapshot.input_kind, "full_input_stored": snapshot.full_input_stored},
        )
        return snapshot

    def record_output_snapshot(
        self,
        *,
        envelope: ExecutionEnvelope,
        output_payload: Any,
        output_kind: str = "explicit_skill_output",
        output_ref: str | None = None,
        truncated: bool = False,
        output_attrs: dict[str, Any] | None = None,
    ) -> ExecutionOutputSnapshot:
        redacted_payload, redacted_fields = redact_sensitive_fields(_as_mapping(output_payload))
        snapshot = ExecutionOutputSnapshot(
            output_snapshot_id=new_execution_output_snapshot_id(),
            envelope_id=envelope.envelope_id,
            output_kind=output_kind,
            output_preview=preview_payload(redacted_payload),
            output_hash=hash_payload(output_payload),
            output_ref=output_ref,
            truncated=truncated,
            redacted_fields=redacted_fields,
            full_output_stored=False,
            created_at=utc_now_iso(),
            output_attrs={
                "preview_only": True,
                "body_stored": False,
                **dict(output_attrs or {}),
            },
        )
        self.last_output_snapshot = snapshot
        self._record(
            "execution_output_snapshot_recorded",
            objects=[_object("execution_output_snapshot", snapshot.output_snapshot_id, snapshot.to_dict())],
            links=[("execution_output_snapshot_object", snapshot.output_snapshot_id), ("execution_envelope_object", envelope.envelope_id)],
            object_links=[(snapshot.output_snapshot_id, envelope.envelope_id, "belongs_to_execution_envelope")],
            attrs={"output_kind": snapshot.output_kind, "full_output_stored": snapshot.full_output_stored},
        )
        return snapshot

    def record_artifact_ref(
        self,
        *,
        envelope: ExecutionEnvelope,
        artifact_kind: str,
        artifact_ref: str,
        artifact_payload: Any | None = None,
        private: bool = False,
        artifact_attrs: dict[str, Any] | None = None,
    ) -> ExecutionArtifactRef:
        artifact = ExecutionArtifactRef(
            artifact_ref_id=new_execution_artifact_ref_id(),
            envelope_id=envelope.envelope_id,
            artifact_kind=artifact_kind,
            artifact_ref=artifact_ref,
            artifact_hash=hash_payload(artifact_payload if artifact_payload is not None else artifact_ref),
            artifact_preview=preview_payload(artifact_payload if artifact_payload is not None else {"artifact_ref": artifact_ref}),
            private=private,
            created_at=utc_now_iso(),
            artifact_attrs=dict(artifact_attrs or {}),
        )
        self.last_artifact_refs.append(artifact)
        self._record(
            "execution_artifact_ref_recorded",
            objects=[_object("execution_artifact_ref", artifact.artifact_ref_id, artifact.to_dict())],
            links=[("execution_artifact_ref_object", artifact.artifact_ref_id), ("execution_envelope_object", envelope.envelope_id)],
            object_links=[(artifact.artifact_ref_id, envelope.envelope_id, "belongs_to_execution_envelope")],
            attrs={"artifact_kind": artifact.artifact_kind, "private": artifact.private},
        )
        return artifact

    def record_outcome_summary(
        self,
        *,
        envelope: ExecutionEnvelope,
        violation_ids: list[str] | None = None,
        finding_ids: list[str] | None = None,
        output_snapshot_id: str | None = None,
        reason: str | None = None,
        summary_attrs: dict[str, Any] | None = None,
    ) -> ExecutionOutcomeSummary:
        summary = ExecutionOutcomeSummary(
            summary_id=new_execution_outcome_summary_id(),
            envelope_id=envelope.envelope_id,
            status=envelope.status,
            succeeded=envelope.status == "completed",
            blocked=envelope.blocked or envelope.status == "blocked",
            failed=envelope.status in {"failed", "error"},
            skipped=envelope.status in {"skipped", "unsupported", "needs_review"},
            violation_ids=list(violation_ids or []),
            finding_ids=list(finding_ids or []),
            output_snapshot_id=output_snapshot_id,
            reason=reason,
            created_at=utc_now_iso(),
            summary_attrs={
                "execution_performed": envelope.execution_performed,
                "full_input_stored": False,
                "full_output_stored": False,
                **dict(summary_attrs or {}),
            },
        )
        self.last_outcome_summary = summary
        event_name = _event_for_envelope_status(envelope.status)
        self._record(
            "execution_outcome_summary_recorded",
            objects=[_object("execution_outcome_summary", summary.summary_id, summary.to_dict())],
            links=[("execution_outcome_summary_object", summary.summary_id), ("execution_envelope_object", envelope.envelope_id)],
            object_links=[(summary.summary_id, envelope.envelope_id, "summarizes_execution_envelope")],
            attrs={"status": summary.status},
        )
        self._record(
            event_name,
            objects=[_object("execution_envelope", envelope.envelope_id, envelope.to_dict())],
            links=[("execution_envelope_object", envelope.envelope_id)],
            object_links=[],
            attrs={"status": envelope.status, "execution_kind": envelope.execution_kind},
        )
        return summary

    def wrap_explicit_invocation_result(
        self,
        *,
        invocation_result: ExplicitSkillInvocationResult,
        invocation_request: ExplicitSkillInvocationRequest | None = None,
        invocation_input: ExplicitSkillInvocationInput | None = None,
        proposal_id: str | None = None,
    ) -> ExecutionEnvelope:
        status = _status_from_invocation(invocation_result.status)
        envelope = self.create_envelope(
            execution_kind="explicit_skill_invocation",
            execution_subject_id=invocation_result.result_id,
            skill_id=invocation_result.skill_id,
            session_id=invocation_request.session_id if invocation_request else None,
            turn_id=invocation_request.turn_id if invocation_request else None,
            process_instance_id=invocation_request.process_instance_id if invocation_request else None,
            status=status,
            execution_allowed=invocation_result.status == "completed",
            execution_performed=invocation_result.status in {"completed", "failed"},
            blocked=invocation_result.status in {"denied", "unsupported"},
            started_at=invocation_result.started_at,
            completed_at=invocation_result.completed_at,
        )
        input_payload = invocation_input.input_payload if invocation_input else {}
        input_snapshot = self.record_input_snapshot(envelope=envelope, input_payload=input_payload)
        output_snapshot = self.record_output_snapshot(
            envelope=envelope,
            output_payload=invocation_result.output_payload,
            output_ref=invocation_result.result_id,
            truncated=bool(invocation_result.output_payload.get("truncated", False)),
        )
        self.record_provenance(
            envelope=envelope,
            actor_type=invocation_request.requester_type if invocation_request else None,
            actor_id=invocation_request.requester_id if invocation_request else None,
            runtime_kind="explicit_skill_invocation",
            invocation_mode=invocation_request.invocation_mode if invocation_request else None,
            proposal_id=proposal_id,
            explicit_invocation_request_id=invocation_result.request_id,
            explicit_invocation_result_id=invocation_result.result_id,
            capability_decision_id=invocation_request.capability_decision_id if invocation_request else None,
            permission_request_id=invocation_request.permission_request_id if invocation_request else None,
            session_permission_resolution_id=(
                invocation_request.session_permission_resolution_id if invocation_request else None
            ),
            sandbox_ref_ids=[invocation_request.workspace_sandbox_decision_id] if invocation_request and invocation_request.workspace_sandbox_decision_id else [],
            risk_ref_ids=[invocation_request.shell_network_decision_id] if invocation_request and invocation_request.shell_network_decision_id else [],
            provenance_attrs={"input_snapshot_id": input_snapshot.input_snapshot_id},
        )
        self.record_outcome_summary(
            envelope=envelope,
            violation_ids=invocation_result.violation_ids,
            output_snapshot_id=output_snapshot.output_snapshot_id,
            reason=invocation_result.error_message,
        )
        return envelope

    def wrap_gated_invocation_result(
        self,
        *,
        gate_result: SkillExecutionGateResult,
        gate_request: SkillExecutionGateRequest | None = None,
        gate_decision: SkillExecutionGateDecision | None = None,
        invocation_result: ExplicitSkillInvocationResult | None = None,
        invocation_request: ExplicitSkillInvocationRequest | None = None,
        invocation_input: ExplicitSkillInvocationInput | None = None,
        proposal_id: str | None = None,
    ) -> ExecutionEnvelope:
        status = _status_from_gate(gate_result, invocation_result)
        skill_id = gate_request.skill_id if gate_request else (invocation_result.skill_id if invocation_result else None)
        envelope = self.create_envelope(
            execution_kind="gated_skill_invocation",
            execution_subject_id=gate_result.gate_result_id,
            skill_id=skill_id,
            session_id=gate_request.session_id if gate_request else None,
            turn_id=gate_request.turn_id if gate_request else None,
            process_instance_id=gate_request.process_instance_id if gate_request else None,
            status=status,
            execution_allowed=bool(gate_decision.can_execute) if gate_decision else gate_result.executed,
            execution_performed=bool(gate_result.executed and invocation_result and invocation_result.status == "completed"),
            blocked=gate_result.blocked,
            started_at=invocation_result.started_at if invocation_result else None,
            completed_at=invocation_result.completed_at if invocation_result else gate_result.created_at,
        )
        input_payload = (
            invocation_input.input_payload
            if invocation_input
            else gate_request.request_attrs.get("input_payload", {})
            if gate_request
            else {}
        )
        input_snapshot = self.record_input_snapshot(envelope=envelope, input_payload=input_payload)
        output_snapshot = None
        if invocation_result is not None:
            output_snapshot = self.record_output_snapshot(
                envelope=envelope,
                output_payload=invocation_result.output_payload,
                output_ref=invocation_result.result_id,
                truncated=bool(invocation_result.output_payload.get("truncated", False)),
            )
        self.record_provenance(
            envelope=envelope,
            actor_type=gate_request.requester_type if gate_request else None,
            actor_id=gate_request.requester_id if gate_request else None,
            runtime_kind="gated_skill_invocation",
            invocation_mode=gate_request.invocation_mode if gate_request else None,
            proposal_id=proposal_id,
            explicit_invocation_request_id=invocation_request.request_id if invocation_request else None,
            explicit_invocation_result_id=gate_result.explicit_invocation_result_id,
            gate_request_id=gate_result.gate_request_id,
            gate_decision_id=gate_result.gate_decision_id,
            gate_result_id=gate_result.gate_result_id,
            capability_decision_id=gate_request.capability_decision_id if gate_request else None,
            permission_request_id=gate_request.permission_request_id if gate_request else None,
            permission_decision_id=gate_request.permission_decision_id if gate_request else None,
            session_permission_resolution_id=(
                gate_request.session_permission_resolution_id if gate_request else None
            ),
            sandbox_ref_ids=[gate_request.workspace_sandbox_decision_id] if gate_request and gate_request.workspace_sandbox_decision_id else [],
            risk_ref_ids=[gate_request.shell_network_decision_id] if gate_request and gate_request.shell_network_decision_id else [],
            provenance_attrs={"input_snapshot_id": input_snapshot.input_snapshot_id},
        )
        self.record_outcome_summary(
            envelope=envelope,
            violation_ids=invocation_result.violation_ids if invocation_result else [],
            finding_ids=gate_result.finding_ids,
            output_snapshot_id=output_snapshot.output_snapshot_id if output_snapshot else None,
            reason=gate_decision.reason if gate_decision else None,
        )
        return envelope

    def render_envelope_summary(self, envelope: ExecutionEnvelope | None = None) -> str:
        item = envelope or self.last_envelope
        if item is None:
            return "Execution Envelope: unavailable"
        lines = [
            "Execution Envelope",
            f"envelope_id={item.envelope_id}",
            f"status={item.status}",
            f"execution_kind={item.execution_kind}",
            f"execution_performed={str(item.execution_performed).lower()}",
            f"blocked={str(item.blocked).lower()}",
            "full_input_stored=false",
            "full_output_stored=false",
        ]
        if item.skill_id:
            lines.append(f"skill_id={item.skill_id}")
        return "\n".join(lines)

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
                "execution_envelope": True,
                "capabilities_granted": False,
                "skills_executed_by_envelope": False,
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


def hash_payload(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preview_payload(value: Any, max_chars: int = 2000) -> dict[str, Any]:
    return _preview_value(value, max_chars=max_chars)


def redact_sensitive_fields(
    payload: dict[str, Any],
    sensitive_keys: list[str] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    keys = [item.lower() for item in (sensitive_keys or DEFAULT_SENSITIVE_KEYS)]
    redacted_fields: list[str] = []

    def redact(value: Any, path: str = "") -> Any:
        if isinstance(value, dict):
            result: dict[str, Any] = {}
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else str(key)
                if str(key).lower() in keys:
                    redacted_fields.append(next_path)
                    result[str(key)] = "<REDACTED>"
                else:
                    result[str(key)] = redact(item, next_path)
            return result
        if isinstance(value, list):
            return [redact(item, f"{path}[]") for item in value]
        return value

    return redact(payload), redacted_fields


def summarize_status(status: str, *, blocked: bool = False) -> dict[str, bool]:
    return {
        "succeeded": status == "completed",
        "blocked": blocked or status == "blocked",
        "failed": status in {"failed", "error"},
        "skipped": status in {"skipped", "unsupported", "needs_review"},
    }


def _preview_value(value: Any, *, max_chars: int) -> dict[str, Any]:
    if isinstance(value, dict):
        preview: dict[str, Any] = {}
        for key, item in value.items():
            preview[str(key)] = _preview_scalar(item, max_chars=max_chars)
        return preview
    return {"value": _preview_scalar(value, max_chars=max_chars)}


def _preview_scalar(value: Any, *, max_chars: int) -> Any:
    if isinstance(value, str):
        return value[:max_chars]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return {"list_count": len(value)}
    if isinstance(value, dict):
        return {"dict_keys": sorted(str(key) for key in value)[:20]}
    return str(type(value).__name__)


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return {"value": value}


def _status_from_invocation(status: str) -> str:
    if status == "completed":
        return "completed"
    if status in {"denied", "unsupported", "failed", "skipped", "error"}:
        return status
    return "error"


def _status_from_gate(
    gate_result: SkillExecutionGateResult,
    invocation_result: ExplicitSkillInvocationResult | None,
) -> str:
    if gate_result.blocked:
        return "blocked"
    if not gate_result.executed:
        return "skipped"
    if invocation_result is None:
        return "error"
    return _status_from_invocation(invocation_result.status)


def _event_for_envelope_status(status: str) -> str:
    if status == "completed":
        return "execution_envelope_completed"
    if status in {"blocked", "denied", "unsupported", "needs_review"}:
        return "execution_envelope_blocked"
    if status in {"failed", "error"}:
        return "execution_envelope_failed"
    return "execution_envelope_skipped"


def _reference_links(record: ExecutionProvenanceRecord) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for qualifier, value in [
        ("proposal", record.proposal_id),
        ("explicit_invocation_request", record.explicit_invocation_request_id),
        ("explicit_invocation_result", record.explicit_invocation_result_id),
        ("gate_request", record.gate_request_id),
        ("gate_decision", record.gate_decision_id),
        ("gate_result", record.gate_result_id),
        ("capability_decision", record.capability_decision_id),
        ("permission_request", record.permission_request_id),
        ("permission_decision", record.permission_decision_id),
        ("session_permission_resolution", record.session_permission_resolution_id),
    ]:
        if value:
            links.append((qualifier, value))
    for value in record.sandbox_ref_ids:
        links.append(("sandbox_ref", value))
    for value in record.risk_ref_ids:
        links.append(("risk_ref", value))
    return links


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

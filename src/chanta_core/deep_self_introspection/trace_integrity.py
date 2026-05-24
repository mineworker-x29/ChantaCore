from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from chanta_core.execution.models import ExecutionEnvelope
from chanta_core.ocel.store import OCELStore
from chanta_core.utility.time import utc_now_iso


TraceIntegrityStatus = Literal["passed", "warning", "failed", "blocked"]
TraceScope = Literal["self_awareness", "deep_self", "all"]


@dataclass(frozen=True)
class SelfTraceIntegrityRequest:
    scope: str = "self_awareness"
    root_id: str | None = None
    session_id: str | None = None
    process_instance_id: str | None = None
    candidate_id: str | None = None
    envelope_id: str | None = None
    event_id: str | None = None
    include_envelope_checks: bool = True
    include_event_object_checks: bool = True
    include_relation_checks: bool = True
    include_candidate_lineage_checks: bool = True
    include_process_chain_checks: bool = True
    include_blocked_event_checks: bool = True
    max_events: int = 1000
    max_findings: int = 200
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class TraceElementRef:
    ref_type: str
    ref_id: str
    object_type: str | None = None
    event_type: str | None = None
    summary: str | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_type": self.ref_type,
            "ref_id": self.ref_id,
            "object_type": self.object_type,
            "event_type": self.event_type,
            "summary": self.summary,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class EnvelopeOCELLinkCheck:
    check_id: str
    envelope_id: str
    expected_event_id: str | None
    linked_event_ids: list[str]
    skill_id: str | None
    effect_types: list[str]
    blocked: bool
    link_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "linked_event_ids": list(self.linked_event_ids), "effect_types": list(self.effect_types), "notes": list(self.notes)}


@dataclass(frozen=True)
class EventObjectCoverageCheck:
    check_id: str
    event_id: str
    event_type: str
    required_object_types: list[str]
    present_object_types: list[str]
    missing_object_types: list[str]
    relation_count: int
    coverage_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "required_object_types": list(self.required_object_types),
            "present_object_types": list(self.present_object_types),
            "missing_object_types": list(self.missing_object_types),
            "relation_count": self.relation_count,
            "coverage_status": self.coverage_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class ObjectRelationIntegrityCheck:
    check_id: str
    source_object_id: str
    source_object_type: str
    relation_type: str
    target_object_id: str | None
    target_object_type: str | None
    relation_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class CandidateLineageCheck:
    check_id: str
    candidate_id: str
    candidate_type: str
    source_refs: list[TraceElementRef]
    evidence_refs: list[dict[str, Any]]
    has_source_event: bool
    has_source_object: bool
    has_evidence_refs: bool
    has_verification_ref: bool
    lineage_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "candidate_id": self.candidate_id,
            "candidate_type": self.candidate_type,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "has_source_event": self.has_source_event,
            "has_source_object": self.has_source_object,
            "has_evidence_refs": self.has_evidence_refs,
            "has_verification_ref": self.has_verification_ref,
            "lineage_status": self.lineage_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class ProcessChainIntegrityCheck:
    check_id: str
    process_instance_id: str | None
    chain_name: str
    expected_event_sequence: list[str]
    observed_event_sequence: list[str]
    missing_events: list[str]
    unexpected_events: list[str]
    chain_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "process_instance_id": self.process_instance_id,
            "chain_name": self.chain_name,
            "expected_event_sequence": list(self.expected_event_sequence),
            "observed_event_sequence": list(self.observed_event_sequence),
            "missing_events": list(self.missing_events),
            "unexpected_events": list(self.unexpected_events),
            "chain_status": self.chain_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class TraceIntegrityFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    trace_refs: list[TraceElementRef]
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "trace_refs": [item.to_dict() for item in self.trace_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfTraceIntegritySnapshot:
    snapshot_id: str
    created_at: str
    request: SelfTraceIntegrityRequest
    trace_refs: list[TraceElementRef]
    envelope_link_checks: list[EnvelopeOCELLinkCheck]
    event_object_coverage_checks: list[EventObjectCoverageCheck]
    relation_integrity_checks: list[ObjectRelationIntegrityCheck]
    candidate_lineage_checks: list[CandidateLineageCheck]
    process_chain_checks: list[ProcessChainIntegrityCheck]
    findings: list[TraceIntegrityFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "trace_refs": [item.to_dict() for item in self.trace_refs],
            "envelope_link_checks": [item.to_dict() for item in self.envelope_link_checks],
            "event_object_coverage_checks": [item.to_dict() for item in self.event_object_coverage_checks],
            "relation_integrity_checks": [item.to_dict() for item in self.relation_integrity_checks],
            "candidate_lineage_checks": [item.to_dict() for item in self.candidate_lineage_checks],
            "process_chain_checks": [item.to_dict() for item in self.process_chain_checks],
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfTraceIntegrityReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: TraceIntegrityStatus
    checked_event_count: int
    checked_object_count: int
    checked_relation_count: int
    checked_envelope_count: int
    checked_candidate_count: int
    finding_count: int
    findings: list[TraceIntegrityFinding]
    integrity_summary: dict[str, Any]
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "status": self.status,
            "checked_event_count": self.checked_event_count,
            "checked_object_count": self.checked_object_count,
            "checked_relation_count": self.checked_relation_count,
            "checked_envelope_count": self.checked_envelope_count,
            "checked_candidate_count": self.checked_candidate_count,
            "finding_count": self.finding_count,
            "findings": [item.to_dict() for item in self.findings],
            "integrity_summary": dict(self.integrity_summary),
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class TraceIntegritySourceService:
    def __init__(
        self,
        *,
        ocel_store: OCELStore | None = None,
        events: list[dict[str, Any]] | None = None,
        objects: list[dict[str, Any]] | None = None,
        relations: list[dict[str, Any]] | None = None,
        envelopes: list[ExecutionEnvelope | dict[str, Any]] | None = None,
        candidates: list[dict[str, Any]] | None = None,
        source_available: bool = True,
        uses_jsonl_as_canonical: bool = False,
    ) -> None:
        self.ocel_store = ocel_store
        self._events = list(events) if events is not None else None
        self._objects = list(objects) if objects is not None else None
        self._relations = list(relations) if relations is not None else None
        self._envelopes = list(envelopes or [])
        self._candidates = list(candidates or [])
        self.source_available = source_available
        self.uses_jsonl_as_canonical = uses_jsonl_as_canonical

    def load_ocel_events(self, request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
        if self._events is not None:
            return _filter_events(self._events, request)
        if self.ocel_store is None or not self.source_available:
            return []
        events = self.ocel_store.fetch_recent_events(limit=max(1, request.max_events))
        return _filter_events(events, request)

    def load_ocel_objects(self, request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
        if self._objects is not None:
            return list(self._objects)
        if self.ocel_store is None:
            return []
        objects: dict[str, dict[str, Any]] = {}
        for event in self.load_ocel_events(request):
            for item in self.ocel_store.fetch_related_objects_for_event(str(event.get("event_id"))):
                objects[str(item.get("object_id"))] = item
        return list(objects.values())

    def load_ocel_relations(self, request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
        if self._relations is not None:
            return list(self._relations)
        relations: list[dict[str, Any]] = []
        for event in self.load_ocel_events(request):
            for item in self.load_ocel_objects(request):
                qualifier = item.get("qualifier")
                if qualifier:
                    relations.append(
                        {
                            "relation_kind": "event_object",
                            "source_id": event.get("event_id"),
                            "target_id": item.get("object_id"),
                            "qualifier": qualifier,
                        }
                    )
        return relations

    def load_execution_envelopes(self, request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
        envelopes = [_as_mapping(item) for item in self._envelopes]
        if request.envelope_id:
            envelopes = [item for item in envelopes if item.get("envelope_id") == request.envelope_id]
        return envelopes

    def load_candidate_refs(self, request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
        candidates = [dict(item) for item in self._candidates]
        if request.candidate_id:
            candidates = [item for item in candidates if item.get("candidate_id") == request.candidate_id]
        return candidates


class EnvelopeOCELConsistencyVerifier:
    def verify(
        self,
        request: SelfTraceIntegrityRequest,
        events: list[dict[str, Any]],
        envelopes: list[dict[str, Any]],
    ) -> list[EnvelopeOCELLinkCheck]:
        checks: list[EnvelopeOCELLinkCheck] = []
        events_by_id = {str(item.get("event_id")): item for item in events if item.get("event_id")}
        for envelope in envelopes:
            envelope_id = str(envelope.get("envelope_id") or "")
            expected_event_id = _nested_attr(envelope, "event_id") or _nested_attr(envelope, "ocel_event_id")
            linked = [
                str(event.get("event_id"))
                for event in events
                if _event_links_envelope(event, envelope_id)
                or (expected_event_id and str(event.get("event_id")) == expected_event_id)
            ]
            if not envelope_id:
                status = "missing_envelope"
            elif expected_event_id and expected_event_id not in events_by_id:
                status = "missing_event"
            elif len(linked) > 1:
                status = "ambiguous"
            elif linked:
                status = "linked"
            else:
                status = "missing_event"
            checks.append(
                EnvelopeOCELLinkCheck(
                    check_id=f"envelope_ocel_link_check:{uuid4().hex}",
                    envelope_id=envelope_id,
                    expected_event_id=expected_event_id,
                    linked_event_ids=linked,
                    skill_id=envelope.get("skill_id"),
                    effect_types=list(_nested_list(envelope, "effect_types")),
                    blocked=bool(envelope.get("blocked")),
                    link_status=status,
                    notes=["Envelope to OCEL relation is read-only checked."],
                )
            )
        if request.include_blocked_event_checks:
            envelope_ids = {str(item.get("envelope_id")) for item in envelopes}
            for event in events:
                attrs = _attrs(event, "event_attrs")
                if bool(attrs.get("blocked")) or bool(attrs.get("requires_envelope")) or str(attrs.get("status")) == "blocked":
                    envelope_id = str(attrs.get("envelope_id") or attrs.get("execution_envelope_id") or "")
                    if not envelope_id or envelope_id not in envelope_ids:
                        checks.append(
                            EnvelopeOCELLinkCheck(
                                check_id=f"envelope_ocel_link_check:{uuid4().hex}",
                                envelope_id=envelope_id,
                                expected_event_id=str(event.get("event_id") or ""),
                                linked_event_ids=[],
                                skill_id=attrs.get("skill_id"),
                                effect_types=list(_nested_list(event, "effect_types")),
                                blocked=True,
                                link_status="missing_envelope",
                                notes=["Blocked event is not envelope-visible."],
                            )
                        )
        return checks


class EventObjectCoverageVerifier:
    def verify(
        self,
        events: list[dict[str, Any]],
        objects: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> list[EventObjectCoverageCheck]:
        object_types = {str(item.get("object_id")): str(item.get("object_type")) for item in objects}
        checks: list[EventObjectCoverageCheck] = []
        for event in events:
            event_id = str(event.get("event_id") or "")
            event_type = str(event.get("event_activity") or event.get("event_type") or "")
            attrs = _attrs(event, "event_attrs")
            required = list(attrs.get("required_object_types") or [])
            event_relations = [
                relation
                for relation in relations
                if relation.get("relation_kind", "event_object") == "event_object"
                and str(relation.get("source_id") or relation.get("event_id")) == event_id
            ]
            present = sorted({object_types.get(str(item.get("target_id") or item.get("object_id")), "unknown") for item in event_relations})
            missing = [item for item in required if item not in present]
            if not required:
                status = "not_applicable"
            elif not present:
                status = "missing"
            elif missing:
                status = "partial"
            else:
                status = "complete"
            effect_types = [str(item) for item in attrs.get("effect_types") or []]
            notes = ["Required OCEL event-object coverage is read-only checked."]
            if any(item in {"mutation", "execution", "write", "shell_execution"} for item in effect_types):
                notes.append("effect_type_mismatch")
            checks.append(
                EventObjectCoverageCheck(
                    check_id=f"event_object_coverage_check:{uuid4().hex}",
                    event_id=event_id,
                    event_type=event_type,
                    required_object_types=required,
                    present_object_types=present,
                    missing_object_types=missing,
                    relation_count=len(event_relations),
                    coverage_status=status,
                    notes=notes,
                )
            )
        return checks


class ObjectRelationIntegrityVerifier:
    def verify(
        self,
        objects: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> list[ObjectRelationIntegrityCheck]:
        object_types = {str(item.get("object_id")): str(item.get("object_type")) for item in objects}
        seen: set[tuple[str, str, str, str]] = set()
        checks: list[ObjectRelationIntegrityCheck] = []
        for relation in relations:
            if relation.get("relation_kind") != "object_object":
                continue
            source_id = str(relation.get("source_id") or relation.get("source_object_id") or "")
            target_id = str(relation.get("target_id") or relation.get("target_object_id") or "")
            qualifier = str(relation.get("qualifier") or "")
            key = (source_id, target_id, qualifier, str(relation.get("relation_type") or "object_object"))
            if key in seen:
                status = "duplicate"
            elif source_id not in object_types or target_id not in object_types:
                status = "dangling"
            else:
                status = "valid"
            seen.add(key)
            checks.append(
                ObjectRelationIntegrityCheck(
                    check_id=f"object_relation_integrity_check:{uuid4().hex}",
                    source_object_id=source_id,
                    source_object_type=object_types.get(source_id, "unknown"),
                    relation_type=qualifier,
                    target_object_id=target_id or None,
                    target_object_type=object_types.get(target_id),
                    relation_status=status,
                    notes=["Object-object relation is read-only checked."],
                )
            )
        return checks


class CandidateLineageVerifier:
    def verify(
        self,
        candidates: list[dict[str, Any]],
        events: list[dict[str, Any]],
        objects: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> list[CandidateLineageCheck]:
        event_ids = {str(item.get("event_id")) for item in events}
        object_ids = {str(item.get("object_id")) for item in objects}
        checks: list[CandidateLineageCheck] = []
        for candidate in candidates:
            candidate_id = str(candidate.get("candidate_id") or candidate.get("id") or "")
            candidate_type = str(candidate.get("candidate_type") or candidate.get("type") or "candidate")
            raw_source_refs = list(candidate.get("source_refs") or [])
            source_refs = [_trace_ref(item) for item in raw_source_refs]
            evidence_refs = [dict(item) for item in candidate.get("evidence_refs") or []]
            has_source_event = any(item.ref_type == "event" and item.ref_id in event_ids for item in source_refs)
            has_source_object = any(item.ref_type == "object" and item.ref_id in object_ids for item in source_refs)
            has_evidence_refs = bool(evidence_refs)
            has_verification_ref = bool(candidate.get("verification_ref") or candidate.get("verification_report_id"))
            if has_source_event and has_source_object and has_evidence_refs:
                status = "complete"
            elif has_source_event or has_source_object or has_evidence_refs:
                status = "partial"
            else:
                status = "missing"
            checks.append(
                CandidateLineageCheck(
                    check_id=f"candidate_lineage_check:{uuid4().hex}",
                    candidate_id=candidate_id,
                    candidate_type=candidate_type,
                    source_refs=source_refs,
                    evidence_refs=evidence_refs,
                    has_source_event=has_source_event,
                    has_source_object=has_source_object,
                    has_evidence_refs=has_evidence_refs,
                    has_verification_ref=has_verification_ref,
                    lineage_status=status,
                    notes=["Candidate lineage is read-only checked against source/evidence refs."],
                )
            )
        return checks


class ProcessChainIntegrityVerifier:
    def verify(
        self,
        request: SelfTraceIntegrityRequest,
        events: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> list[ProcessChainIntegrityCheck]:
        if not request.include_process_chain_checks:
            return []
        process_events = [
            event
            for event in events
            if not request.process_instance_id
            or _attrs(event, "event_attrs").get("process_instance_id") == request.process_instance_id
        ]
        observed = [str(event.get("event_activity") or event.get("event_type") or "") for event in process_events]
        expected = _expected_sequence(request.scope)
        if not observed:
            status = "unknown"
            missing = expected
        else:
            missing = [item for item in expected if item not in observed]
            status = "complete" if not missing else "broken"
        unexpected = [item for item in observed if expected and item not in expected]
        return [
            ProcessChainIntegrityCheck(
                check_id=f"process_chain_integrity_check:{uuid4().hex}",
                process_instance_id=request.process_instance_id,
                chain_name=f"{request.scope}_trace_chain",
                expected_event_sequence=expected,
                observed_event_sequence=observed,
                missing_events=missing,
                unexpected_events=unexpected,
                chain_status=status,
                notes=["Process chain is checked without replaying events."],
            )
        ]


class TraceIntegrityFindingService:
    def evaluate(self, snapshot: SelfTraceIntegritySnapshot) -> list[TraceIntegrityFinding]:
        findings: list[TraceIntegrityFinding] = []
        if snapshot.request.scope not in {"self_awareness", "deep_self", "all"}:
            findings.append(_finding("critical", "unsupported_scope", "Unsupported trace integrity scope.", [_request_ref(snapshot.request)]))
        for check in snapshot.envelope_link_checks:
            if check.link_status == "missing_event":
                findings.append(_finding("error", "missing_ocel_event", "Execution envelope has no linked OCEL event.", [_envelope_ref(check.envelope_id)]))
            elif check.link_status == "missing_envelope":
                finding_type = "blocked_attempt_not_enveloped" if check.blocked else "missing_envelope_link"
                findings.append(_finding("error", finding_type, "OCEL event or blocked attempt has no envelope link.", [_event_ref(check.expected_event_id or check.envelope_id)]))
            elif check.link_status == "ambiguous":
                findings.append(_finding("warning", "missing_envelope_link", "Envelope has ambiguous OCEL event links.", [_envelope_ref(check.envelope_id)]))
        for check in snapshot.event_object_coverage_checks:
            if check.coverage_status in {"partial", "missing"}:
                findings.append(_finding("error", "missing_required_object", "Required OCEL object relation is missing.", [_event_ref(check.event_id)]))
            if "effect_type_mismatch" in ",".join(check.notes).lower():
                findings.append(_finding("error", "effect_type_mismatch", "Event effect type is incompatible with read-only trace integrity.", [_event_ref(check.event_id)]))
        for check in snapshot.relation_integrity_checks:
            if check.relation_status == "dangling":
                findings.append(_finding("error", "dangling_object_relation", "Object relation target or source is missing.", [_object_ref(check.source_object_id)]))
            elif check.relation_status == "duplicate":
                findings.append(_finding("warning", "duplicate_relation", "Duplicate object relation is visible.", [_object_ref(check.source_object_id)]))
        for check in snapshot.candidate_lineage_checks:
            refs = [_candidate_ref(check.candidate_id)]
            if not check.has_source_event:
                findings.append(_finding("error", "missing_candidate_source", "Candidate has no source event.", refs))
            if not check.has_source_object:
                findings.append(_finding("error", "missing_candidate_source", "Candidate has no source object.", refs))
            if not check.has_evidence_refs:
                findings.append(_finding("error", "missing_candidate_evidence", "Candidate has no evidence refs.", refs))
            if not check.has_verification_ref:
                findings.append(_finding("warning", "missing_verification_ref", "Candidate has no verification ref.", refs))
            if check.candidate_type == "state_candidate_created" and not check.has_source_event:
                findings.append(_finding("error", "state_candidate_without_source", "State candidate has no source event.", refs))
            if check.candidate_type == "no_action" and not any("policy" in str(item).lower() for item in check.evidence_refs):
                findings.append(_finding("warning", "no_action_candidate_without_policy_ref", "No-action candidate has no policy ref.", refs))
        for check in snapshot.process_chain_checks:
            if check.chain_status == "broken":
                findings.append(_finding("error", "trace_chain_broken", "Process chain is missing expected events.", [_process_ref(check.process_instance_id or check.chain_name)]))
            elif check.chain_status == "unknown":
                findings.append(_finding("warning", "missing_process_instance_link", "Process chain is unknown for this scope.", [_process_ref(check.process_instance_id or check.chain_name)]))
        if any("JSONL canonical source" in item for item in snapshot.limitations):
            findings.append(_finding("error", "jsonl_canonical_leak", "JSONL was treated as canonical trace source.", [_request_ref(snapshot.request)]))
        if not findings:
            findings.append(_finding("info", "ok", "Trace integrity checks passed.", [_request_ref(snapshot.request)]))
        return findings[: max(0, snapshot.request.max_findings)]


class SelfTraceIntegrityAwarenessService:
    def __init__(
        self,
        *,
        source_service: TraceIntegritySourceService | None = None,
        envelope_verifier: EnvelopeOCELConsistencyVerifier | None = None,
        event_object_verifier: EventObjectCoverageVerifier | None = None,
        relation_verifier: ObjectRelationIntegrityVerifier | None = None,
        candidate_verifier: CandidateLineageVerifier | None = None,
        process_verifier: ProcessChainIntegrityVerifier | None = None,
        finding_service: TraceIntegrityFindingService | None = None,
    ) -> None:
        self.source_service = source_service or TraceIntegritySourceService()
        self.envelope_verifier = envelope_verifier or EnvelopeOCELConsistencyVerifier()
        self.event_object_verifier = event_object_verifier or EventObjectCoverageVerifier()
        self.relation_verifier = relation_verifier or ObjectRelationIntegrityVerifier()
        self.candidate_verifier = candidate_verifier or CandidateLineageVerifier()
        self.process_verifier = process_verifier or ProcessChainIntegrityVerifier()
        self.finding_service = finding_service or TraceIntegrityFindingService()
        self.last_snapshot: SelfTraceIntegritySnapshot | None = None
        self.last_report: SelfTraceIntegrityReport | None = None

    def check_trace_integrity(
        self,
        request: SelfTraceIntegrityRequest | None = None,
    ) -> SelfTraceIntegrityReport:
        request = request or SelfTraceIntegrityRequest()
        snapshot = self.build_snapshot(request)
        status = _status_from_findings(snapshot.findings)
        report = SelfTraceIntegrityReport(
            report_id=f"self_trace_integrity_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            checked_event_count=len([item for item in snapshot.trace_refs if item.ref_type == "event"]),
            checked_object_count=len([item for item in snapshot.trace_refs if item.ref_type == "object"]),
            checked_relation_count=len([item for item in snapshot.trace_refs if item.ref_type == "relation"]),
            checked_envelope_count=len(snapshot.envelope_link_checks),
            checked_candidate_count=len(snapshot.candidate_lineage_checks),
            finding_count=len(snapshot.findings),
            findings=snapshot.findings,
            integrity_summary={
                "scope": request.scope,
                "missing_or_dangling_findings": sum(
                    1
                    for item in snapshot.findings
                    if "missing" in item.finding_type or "dangling" in item.finding_type or "orphan" in item.finding_type
                ),
                "repairs_trace": False,
                "rewrites_events": False,
                "uses_jsonl_as_canonical": self.source_service.uses_jsonl_as_canonical,
                "no_repair_performed": True,
            },
            limitations=snapshot.limitations,
            withdrawal_conditions=[
                "Withdraw if trace integrity awareness modifies OCEL events, objects, relations, envelopes, or candidates.",
                "Withdraw if missing trace is silently changed instead of being reported as a finding.",
            ],
            validity_horizon="Valid until v0.21.5 Self-Context Projection Awareness changes context projection assumptions.",
        )
        self.last_report = report
        return report

    def build_snapshot(self, request: SelfTraceIntegrityRequest) -> SelfTraceIntegritySnapshot:
        events = self.source_service.load_ocel_events(request)
        objects = self.source_service.load_ocel_objects(request)
        relations = self.source_service.load_ocel_relations(request)
        envelopes = self.source_service.load_execution_envelopes(request)
        candidates = self.source_service.load_candidate_refs(request)
        limitations: list[str] = [
            "Trace integrity awareness is read-only.",
            "Missing trace becomes a finding, not an implicit patch.",
            "No private full paths, raw file content, or raw secrets are emitted.",
        ]
        if not self.source_service.source_available:
            limitations.append("OCEL source unavailable.")
        if self.source_service.uses_jsonl_as_canonical:
            limitations.append("JSONL canonical source violation.")
        if len(events) >= request.max_events:
            limitations.append("Scope partially truncated by max_events.")
        snapshot = SelfTraceIntegritySnapshot(
            snapshot_id=f"self_trace_integrity_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            trace_refs=_trace_refs(events, objects, relations, envelopes, candidates),
            envelope_link_checks=self.envelope_verifier.verify(request, events, envelopes)
            if request.include_envelope_checks
            else [],
            event_object_coverage_checks=self.event_object_verifier.verify(events, objects, relations)
            if request.include_event_object_checks
            else [],
            relation_integrity_checks=self.relation_verifier.verify(objects, relations)
            if request.include_relation_checks
            else [],
            candidate_lineage_checks=self.candidate_verifier.verify(candidates, events, objects, relations)
            if request.include_candidate_lineage_checks
            else [],
            process_chain_checks=self.process_verifier.verify(request, events, relations)
            if request.include_process_chain_checks
            else [],
            findings=[],
            limitations=limitations,
        )
        snapshot = replace(snapshot, findings=self.finding_service.evaluate(snapshot))
        self.last_snapshot = snapshot
        return snapshot

    def build_pig_report(self) -> dict[str, Any]:
        report = self.last_report or self.check_trace_integrity()
        return {
            "version": "v0.21.4",
            "layer": "deep_self_introspection",
            "subject": "trace_integrity",
            "principles": [
                "trace integrity awareness is not trace repair",
                "missing trace is a finding, not an implicit backfill",
                "OCEL remains canonical",
            ],
            "checks_envelope_links": True,
            "checks_event_object_coverage": True,
            "checks_candidate_lineage": True,
            "checks_process_chain": True,
            "repairs_trace": False,
            "rewrites_events": False,
            "uses_jsonl_as_canonical": report.integrity_summary["uses_jsonl_as_canonical"],
            "status": report.status,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_trace_integrity_awareness",
            "version": "v0.21.4",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfAwarenessReleaseState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfTraceIntegrityState",
                "SelfEnvelopeOCELLinkState",
                "SelfEventObjectCoverageState",
                "SelfCandidateLineageState",
                "SelfProcessChainIntegrityState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(self, command: str, report: SelfTraceIntegrityReport | None = None) -> str:
        report = report or self.last_report or self.check_trace_integrity()
        summary = report.integrity_summary
        lines = [
            "Self-Trace Integrity Awareness",
            f"command={command}",
            f"scope={summary.get('scope')}",
            f"status={report.status}",
            f"checked_event_count={report.checked_event_count}",
            f"checked_object_count={report.checked_object_count}",
            f"checked_relation_count={report.checked_relation_count}",
            f"checked_envelope_count={report.checked_envelope_count}",
            f"checked_candidate_count={report.checked_candidate_count}",
            f"finding_count={report.finding_count}",
            f"missing_or_dangling_findings={summary.get('missing_or_dangling_findings')}",
            "No repair performed.",
            "trace_mutation_performed=False",
            "event_rewrite_performed=False",
            "relation_patch_performed=False",
            "candidate_lineage_auto_fix_performed=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)


def _filter_events(events: list[dict[str, Any]], request: SelfTraceIntegrityRequest) -> list[dict[str, Any]]:
    result = list(events)
    if request.event_id:
        result = [item for item in result if item.get("event_id") == request.event_id]
    if request.session_id:
        result = [item for item in result if _attrs(item, "event_attrs").get("session_id") == request.session_id]
    if request.process_instance_id:
        result = [item for item in result if _attrs(item, "event_attrs").get("process_instance_id") == request.process_instance_id]
    return result[: max(0, request.max_events)]


def _attrs(item: dict[str, Any], key: str) -> dict[str, Any]:
    value = item.get(key) or item.get("attributes") or item.get("attrs") or {}
    return dict(value) if isinstance(value, dict) else {}


def _nested_attr(item: dict[str, Any], key: str) -> str | None:
    if key in item and item[key]:
        return str(item[key])
    for attrs_key in ["envelope_attrs", "event_attrs", "attributes"]:
        attrs = item.get(attrs_key)
        if isinstance(attrs, dict) and attrs.get(key):
            return str(attrs[key])
    return None


def _nested_list(item: dict[str, Any], key: str) -> list[str]:
    value = item.get(key)
    if value is None:
        value = _attrs(item, "event_attrs").get(key)
    if isinstance(value, list):
        return [str(child) for child in value]
    if value:
        return [str(value)]
    return []


def _event_links_envelope(event: dict[str, Any], envelope_id: str) -> bool:
    attrs = _attrs(event, "event_attrs")
    return envelope_id in {
        str(attrs.get("envelope_id") or ""),
        str(attrs.get("execution_envelope_id") or ""),
        str(attrs.get("execution_envelope") or ""),
    }


def _trace_refs(
    events: list[dict[str, Any]],
    objects: list[dict[str, Any]],
    relations: list[dict[str, Any]],
    envelopes: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
) -> list[TraceElementRef]:
    refs: list[TraceElementRef] = []
    refs.extend(TraceElementRef("event", str(item.get("event_id")), event_type=str(item.get("event_activity") or item.get("event_type"))) for item in events)
    refs.extend(TraceElementRef("object", str(item.get("object_id")), object_type=str(item.get("object_type"))) for item in objects)
    refs.extend(TraceElementRef("relation", f"{item.get('source_id')}->{item.get('target_id')}", summary=str(item.get("qualifier"))) for item in relations)
    refs.extend(TraceElementRef("envelope", str(item.get("envelope_id")), summary=str(item.get("status"))) for item in envelopes)
    refs.extend(TraceElementRef("candidate", str(item.get("candidate_id") or item.get("id")), object_type=str(item.get("candidate_type") or item.get("type"))) for item in candidates)
    return refs


def _trace_ref(value: dict[str, Any]) -> TraceElementRef:
    return TraceElementRef(
        ref_type=str(value.get("ref_type") or value.get("type") or "object"),
        ref_id=str(value.get("ref_id") or value.get("id") or ""),
        object_type=value.get("object_type"),
        event_type=value.get("event_type"),
        summary=value.get("summary"),
        evidence_refs=[dict(item) for item in value.get("evidence_refs") or []],
    )


def _request_ref(request: SelfTraceIntegrityRequest) -> TraceElementRef:
    return TraceElementRef(ref_type="report", ref_id=f"trace_integrity_request:{request.scope}", summary=request.scope)


def _event_ref(event_id: str) -> TraceElementRef:
    return TraceElementRef(ref_type="event", ref_id=event_id)


def _object_ref(object_id: str) -> TraceElementRef:
    return TraceElementRef(ref_type="object", ref_id=object_id)


def _envelope_ref(envelope_id: str) -> TraceElementRef:
    return TraceElementRef(ref_type="envelope", ref_id=envelope_id)


def _candidate_ref(candidate_id: str) -> TraceElementRef:
    return TraceElementRef(ref_type="candidate", ref_id=candidate_id)


def _process_ref(process_instance_id: str) -> TraceElementRef:
    return TraceElementRef(ref_type="process_instance", ref_id=process_instance_id)


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    trace_refs: list[TraceElementRef],
    evidence_refs: list[dict[str, Any]] | None = None,
) -> TraceIntegrityFinding:
    return TraceIntegrityFinding(
        finding_id=f"trace_integrity_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        trace_refs=list(trace_refs),
        evidence_refs=[dict(item) for item in evidence_refs or [ref.to_dict() for ref in trace_refs]],
        withdrawal_condition="Withdraw trace integrity judgment unless the source trace evidence is corrected.",
    )


def _expected_sequence(scope: str) -> list[str]:
    if scope == "deep_self":
        return [
            "deep_self_introspection_contract_registered",
            "deep_self_capability_registry_snapshot_created",
            "deep_self_runtime_boundary_snapshot_created",
            "deep_self_policy_gate_map_created",
            "deep_self_trace_integrity_report_created",
        ]
    if scope == "self_awareness":
        return [
            "self_awareness_ecosystem_snapshot_created",
            "self_awareness_release_manifest_created",
            "self_awareness_consolidation_report_created",
        ]
    return []


def _status_from_findings(findings: list[TraceIntegrityFinding]) -> TraceIntegrityStatus:
    if any(item.finding_type == "unsupported_scope" for item in findings):
        return "blocked"
    if any(item.severity in {"error", "critical"} for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"


def _as_mapping(value: ExecutionEnvelope | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return {"value": value}

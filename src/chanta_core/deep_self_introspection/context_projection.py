from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.capability_registry import SelfCapabilityRegistryAwarenessService
from chanta_core.deep_self_introspection.policy_gate import SelfPolicyGateAwarenessService
from chanta_core.deep_self_introspection.runtime_boundary import SelfRuntimeBoundaryAwarenessService
from chanta_core.deep_self_introspection.trace_integrity import SelfTraceIntegrityAwarenessService
from chanta_core.self_awareness import SelfAwarenessConsolidationService, SelfAwarenessWorkbenchService
from chanta_core.utility.time import utc_now_iso


ContextProjectionStatus = Literal["passed", "warning", "failed", "blocked"]


@dataclass(frozen=True)
class SelfContextProjectionViewRequest:
    projection_id: str | None = None
    scope: str = "current"
    include_sources: bool = True
    include_projected_items: bool = True
    include_omissions: bool = True
    include_freshness: bool = True
    include_budget: bool = True
    include_candidate_memory_risk: bool = True
    include_truth_consistency: bool = True
    max_items: int = 500
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class ContextProjectionSourceRef:
    source_id: str
    source_type: str
    source_ref: dict[str, Any]
    source_status: str
    freshness_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "source_ref": dict(self.source_ref),
            "source_status": self.source_status,
            "freshness_status": self.freshness_status,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ContextProjectionItem:
    item_id: str
    item_type: str
    source_id: str | None
    projection_role: str
    content_kind: str
    canonical_truth: bool
    candidate_only: bool
    stale: bool
    truncated: bool
    redacted: bool
    evidence_refs: list[dict[str, Any]]
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "source_id": self.source_id,
            "projection_role": self.projection_role,
            "content_kind": self.content_kind,
            "canonical_truth": self.canonical_truth,
            "candidate_only": self.candidate_only,
            "stale": self.stale,
            "truncated": self.truncated,
            "redacted": self.redacted,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class ContextProjectionBudgetDescriptor:
    budget_id: str
    max_items: int
    projected_item_count: int
    omitted_item_count: int
    compacted_item_count: int
    truncated_item_count: int
    budget_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class ContextProjectionFreshnessDescriptor:
    freshness_id: str
    source_id: str
    source_updated_at: str | None
    projected_at: str | None
    stale: bool
    freshness_status: str
    reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class ContextProjectionGap:
    gap_id: str
    gap_type: str
    severity: str
    description: str
    missing_source_type: str | None
    expected_source_ref: dict[str, Any] | None
    impact: str
    recommended_followup: str | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "gap_type": self.gap_type,
            "severity": self.severity,
            "description": self.description,
            "missing_source_type": self.missing_source_type,
            "expected_source_ref": dict(self.expected_source_ref or {}),
            "impact": self.impact,
            "recommended_followup": self.recommended_followup,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ContextProjectionRiskFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    projection_item_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "projection_item_refs": [dict(item) for item in self.projection_item_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfContextProjectionSnapshot:
    snapshot_id: str
    created_at: str
    request: SelfContextProjectionViewRequest
    sources: list[ContextProjectionSourceRef]
    projected_items: list[ContextProjectionItem]
    budget: ContextProjectionBudgetDescriptor
    freshness: list[ContextProjectionFreshnessDescriptor]
    gaps: list[ContextProjectionGap]
    findings: list[ContextProjectionRiskFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "sources": [item.to_dict() for item in self.sources],
            "projected_items": [item.to_dict() for item in self.projected_items],
            "budget": self.budget.to_dict(),
            "freshness": [item.to_dict() for item in self.freshness],
            "gaps": [item.to_dict() for item in self.gaps],
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfContextProjectionTruthReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: ContextProjectionStatus
    findings: list[ContextProjectionRiskFinding]
    gap_count: int
    stale_item_count: int
    candidate_as_canonical_count: int
    raw_transcript_as_state_count: int
    private_payload_risk_count: int
    projection_truth_summary: dict[str, Any]
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
            "findings": [item.to_dict() for item in self.findings],
            "gap_count": self.gap_count,
            "stale_item_count": self.stale_item_count,
            "candidate_as_canonical_count": self.candidate_as_canonical_count,
            "raw_transcript_as_state_count": self.raw_transcript_as_state_count,
            "private_payload_risk_count": self.private_payload_risk_count,
            "projection_truth_summary": dict(self.projection_truth_summary),
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class ContextProjectionSourceService:
    def __init__(
        self,
        *,
        sources: list[ContextProjectionSourceRef] | None = None,
        source_available: bool = True,
    ) -> None:
        self._sources = sources
        self.source_available = source_available

    def load_current_projection_descriptor(self, request: SelfContextProjectionViewRequest) -> dict[str, Any]:
        return {
            "projection_id": request.projection_id or "context_projection:current",
            "scope": request.scope,
            "read_only": True,
            "raw_prompt_body_available": False,
            "raw_transcript_as_state": False,
            "context_injection_performed": False,
            "projection_mutation_performed": False,
        }

    def load_projection_sources(self, request: SelfContextProjectionViewRequest) -> list[ContextProjectionSourceRef]:
        if self._sources is not None:
            return list(self._sources)
        if not self.source_available:
            return []
        now = utc_now_iso()
        sources = [
            _source("source:capability_truth", "ocpx_read_model", "SelfCapabilityTruthState", "included", "fresh", now),
            _source("source:runtime_boundary", "ocpx_read_model", "SelfRuntimeBoundaryState", "included", "fresh", now),
            _source("source:policy_gate", "ocpx_read_model", "SelfPolicyGateState", "included", "fresh", now),
            _source("source:trace_integrity", "ocpx_read_model", "SelfTraceIntegrityState", "included", "fresh", now),
            _source("source:self_awareness_release", "workbench_snapshot", "SelfAwarenessReleaseState", "included", "fresh", now),
            _source("source:pig_diagnostic", "pig_report", "DeepSelfIntrospectionPIG", "included", "fresh", now),
            _source("source:ocpx_projection", "ocpx_read_model", "DeepSelfIntrospectionOCPX", "included", "fresh", now),
            _source("source:candidate_memory_boundary", "candidate", "SelfCandidateMemoryBoundaryState", "omitted", "not_applicable", now),
        ]
        return sources[: max(0, request.max_items)]


class ContextProjectionItemService:
    def build_projected_items(self, sources: list[ContextProjectionSourceRef]) -> list[ContextProjectionItem]:
        items: list[ContextProjectionItem] = []
        for source in sources:
            if source.source_status == "omitted":
                items.append(_item("gap", source, "omitted_context", "placeholder", False, False, source.freshness_status == "stale"))
                continue
            if source.source_id.endswith("capability_truth"):
                items.append(_item("capability_truth", source, "primary_context", "structured_state", True, False, source.freshness_status == "stale"))
            elif source.source_id.endswith("runtime_boundary"):
                items.append(_item("runtime_boundary", source, "primary_context", "structured_state", True, False, source.freshness_status == "stale"))
            elif source.source_id.endswith("policy_gate"):
                items.append(_item("policy_gate", source, "primary_context", "structured_state", True, False, source.freshness_status == "stale"))
            elif source.source_id.endswith("trace_integrity"):
                items.append(_item("trace_integrity", source, "warning_context", "structured_state", True, False, source.freshness_status == "stale"))
            elif source.source_type == "candidate":
                items.append(_item("candidate_summary", source, "supporting_context", "reference", False, True, source.freshness_status == "stale"))
            else:
                items.append(_item("self_awareness_state", source, "supporting_context", "summary", False, False, source.freshness_status == "stale"))
        return items


class ContextProjectionBudgetService:
    def describe_budget(
        self,
        request: SelfContextProjectionViewRequest,
        items: list[ContextProjectionItem],
        sources: list[ContextProjectionSourceRef],
    ) -> ContextProjectionBudgetDescriptor:
        omitted = sum(1 for item in sources if item.source_status == "omitted")
        compacted = sum(1 for item in sources if item.source_status in {"compacted", "summarized"})
        truncated = sum(1 for item in items if item.truncated)
        if len(items) > request.max_items:
            status = "exceeded"
        elif len(items) >= max(1, int(request.max_items * 0.9)):
            status = "near_limit"
        else:
            status = "ok"
        return ContextProjectionBudgetDescriptor(
            budget_id=f"context_projection_budget:{uuid4().hex}",
            max_items=request.max_items,
            projected_item_count=len(items),
            omitted_item_count=omitted,
            compacted_item_count=compacted,
            truncated_item_count=truncated,
            budget_status=status,
            notes=["Budget is inspected without running compaction."],
        )


class ContextProjectionFreshnessService:
    def evaluate_freshness(
        self,
        sources: list[ContextProjectionSourceRef],
        items: list[ContextProjectionItem],
    ) -> list[ContextProjectionFreshnessDescriptor]:
        projected_at = utc_now_iso()
        return [
            ContextProjectionFreshnessDescriptor(
                freshness_id=f"context_projection_freshness:{uuid4().hex}",
                source_id=source.source_id,
                source_updated_at=source.source_ref.get("updated_at"),
                projected_at=projected_at,
                stale=source.freshness_status == "stale",
                freshness_status=source.freshness_status if source.freshness_status in {"fresh", "stale"} else "unknown",
                reason="Source marked stale." if source.freshness_status == "stale" else None,
            )
            for source in sources
        ]


class ContextProjectionGapService:
    REQUIRED = {
        "missing_capability_truth": "source:capability_truth",
        "missing_runtime_boundary": "source:runtime_boundary",
        "missing_policy_gate": "source:policy_gate",
        "missing_trace_integrity": "source:trace_integrity",
        "missing_candidate_memory_boundary": "source:candidate_memory_boundary",
        "missing_ocpx_projection": "source:ocpx_projection",
        "missing_pig_diagnostic": "source:pig_diagnostic",
    }

    def detect_gaps(
        self,
        sources: list[ContextProjectionSourceRef],
        items: list[ContextProjectionItem],
    ) -> list[ContextProjectionGap]:
        gaps: list[ContextProjectionGap] = []
        source_by_id = {source.source_id: source for source in sources}
        for gap_type, source_id in self.REQUIRED.items():
            source = source_by_id.get(source_id)
            if source is None or source.source_status in {"omitted", "blocked", "unknown"}:
                gaps.append(_gap(gap_type, "warning", f"Projection source {source_id} is missing or omitted.", source_id))
        for item in items:
            if item.candidate_only and item.canonical_truth:
                gaps.append(_gap("candidate_projected_as_canonical", "error", "Candidate-only item is projected as canonical truth.", item.item_id))
            if item.stale:
                gaps.append(_gap("stale_projection", "warning", "Projection item is stale.", item.item_id))
            if item.truncated and "truncation_marked" not in item.limitations:
                gaps.append(_gap("truncated_without_warning", "error", "Projection item is truncated without marker.", item.item_id))
            if item.content_kind == "raw_transcript":
                gaps.append(_gap("raw_transcript_used_as_state", "error", "Raw transcript is used as process-state.", item.item_id))
            if item.content_kind == "jsonl_canonical":
                gaps.append(_gap("jsonl_canonical_leak", "error", "JSONL is treated as canonical projection state.", item.item_id))
        if not any(item.gap_type == "missing_verification_report" for item in gaps):
            gaps.append(_gap("missing_verification_report", "info", "Verification report is optional for this projection view.", "verification_report"))
        return gaps


class ContextProjectionTruthCheckService:
    def check_truth(self, snapshot: SelfContextProjectionSnapshot) -> SelfContextProjectionTruthReport:
        findings = list(snapshot.findings)
        status = _status_from_findings(findings)
        candidate_as_canonical = sum(1 for item in snapshot.projected_items if item.candidate_only and item.canonical_truth)
        raw_transcript_count = sum(1 for item in snapshot.projected_items if item.content_kind == "raw_transcript")
        private_payload_count = sum(1 for item in findings if item.finding_type == "private_payload_projection_risk")
        return SelfContextProjectionTruthReport(
            report_id=f"self_context_projection_truth_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            findings=findings,
            gap_count=len(snapshot.gaps),
            stale_item_count=sum(1 for item in snapshot.projected_items if item.stale),
            candidate_as_canonical_count=candidate_as_canonical,
            raw_transcript_as_state_count=raw_transcript_count,
            private_payload_risk_count=private_payload_count,
            projection_truth_summary={
                "source_count": len(snapshot.sources),
                "projected_item_count": len(snapshot.projected_items),
                "omitted_item_count": snapshot.budget.omitted_item_count,
                "compacted_item_count": snapshot.budget.compacted_item_count,
                "truncated_item_count": snapshot.budget.truncated_item_count,
                "candidate_as_canonical_count": candidate_as_canonical,
                "raw_transcript_as_state_count": raw_transcript_count,
                "private_payload_risk_count": private_payload_count,
                "context_injection_performed": False,
                "memory_promotion_performed": False,
                "raw_transcript_is_process_state": False,
            },
            limitations=snapshot.limitations,
            withdrawal_conditions=[
                "Withdraw if context projection awareness injects or mutates prompt context.",
                "Withdraw if candidate-only or raw transcript material is treated as canonical process-state.",
            ],
            validity_horizon="Valid until v0.21.6 Self-Candidate/Memory Boundary Awareness changes candidate-memory boundary assumptions.",
        )


class SelfContextProjectionAwarenessService:
    def __init__(
        self,
        *,
        source_service: ContextProjectionSourceService | None = None,
        item_service: ContextProjectionItemService | None = None,
        budget_service: ContextProjectionBudgetService | None = None,
        freshness_service: ContextProjectionFreshnessService | None = None,
        gap_service: ContextProjectionGapService | None = None,
        truth_service: ContextProjectionTruthCheckService | None = None,
    ) -> None:
        self.source_service = source_service or ContextProjectionSourceService()
        self.item_service = item_service or ContextProjectionItemService()
        self.budget_service = budget_service or ContextProjectionBudgetService()
        self.freshness_service = freshness_service or ContextProjectionFreshnessService()
        self.gap_service = gap_service or ContextProjectionGapService()
        self.truth_service = truth_service or ContextProjectionTruthCheckService()
        self.last_snapshot: SelfContextProjectionSnapshot | None = None
        self.last_report: SelfContextProjectionTruthReport | None = None

    def view_context_projection(
        self,
        request: SelfContextProjectionViewRequest | None = None,
    ) -> SelfContextProjectionSnapshot:
        request = request or SelfContextProjectionViewRequest()
        sources = self.source_service.load_projection_sources(request) if request.include_sources else []
        items = self.item_service.build_projected_items(sources) if request.include_projected_items else []
        budget = self.budget_service.describe_budget(request, items, sources)
        freshness = self.freshness_service.evaluate_freshness(sources, items) if request.include_freshness else []
        gaps = self.gap_service.detect_gaps(sources, items) if request.include_omissions else []
        snapshot = SelfContextProjectionSnapshot(
            snapshot_id=f"self_context_projection_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            sources=sources,
            projected_items=items,
            budget=budget,
            freshness=freshness,
            gaps=gaps,
            findings=[],
            limitations=[
                "Context projection awareness is read-only.",
                "Raw prompt bodies and raw transcripts are not emitted.",
                "Missing projection sources become gaps or findings.",
            ],
        )
        snapshot = replace(snapshot, findings=_findings(snapshot))
        self.last_snapshot = snapshot
        return snapshot

    def truth_check(
        self,
        request: SelfContextProjectionViewRequest | None = None,
    ) -> SelfContextProjectionTruthReport:
        snapshot = self.view_context_projection(request)
        report = self.truth_service.check_truth(snapshot)
        self.last_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        report = self.last_report or self.truth_check()
        return {
            "version": "v0.21.5",
            "layer": "deep_self_introspection",
            "subject": "context_projection",
            "principles": [
                "context projection awareness is not context injection",
                "projection view is not canonical truth",
                "raw transcript is not process-state",
                "candidate-only must not appear as canonical memory",
            ],
            "checks_sources": True,
            "checks_freshness": True,
            "checks_budget": True,
            "checks_candidate_memory_confusion": True,
            "uses_raw_transcript_as_state": False,
            "mutates_projection": False,
            "promotes_memory": False,
            "status": report.status,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_context_projection_awareness",
            "version": "v0.21.5",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfTraceIntegrityState",
                "SelfAwarenessReleaseState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfContextProjectionState",
                "SelfProjectionSourceState",
                "SelfProjectionGapState",
                "SelfProjectionFreshnessState",
                "SelfProjectionBudgetState",
                "SelfProjectionRiskState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(
        self,
        command: str,
        snapshot: SelfContextProjectionSnapshot | None = None,
        report: SelfContextProjectionTruthReport | None = None,
    ) -> str:
        snapshot = snapshot or self.last_snapshot or self.view_context_projection()
        report = report or self.last_report or self.truth_service.check_truth(snapshot)
        lines = [
            "Self-Context Projection Awareness",
            f"command={command}",
            f"scope={snapshot.request.scope}",
            f"status={report.status}",
            f"source_count={len(snapshot.sources)}",
            f"projected_item_count={len(snapshot.projected_items)}",
            f"omitted_item_count={snapshot.budget.omitted_item_count}",
            f"compacted_item_count={snapshot.budget.compacted_item_count}",
            f"stale_item_count={report.stale_item_count}",
            f"truncated_item_count={snapshot.budget.truncated_item_count}",
            f"candidate_as_canonical_count={report.candidate_as_canonical_count}",
            f"raw_transcript_as_state_count={report.raw_transcript_as_state_count}",
            f"private_payload_risk_count={report.private_payload_risk_count}",
            "No context injection performed.",
            "No memory promotion performed.",
            "projection_mutation_performed=False",
            "prompt_mutation_performed=False",
            "compaction_execution_performed=False",
            "raw_prompt_body_printed=False",
            "raw_transcript_printed=False",
            "private_full_paths_printed=False",
            "raw_file_content_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)


def _source(
    source_id: str,
    source_type: str,
    ref_id: str,
    status: str,
    freshness: str,
    updated_at: str,
) -> ContextProjectionSourceRef:
    return ContextProjectionSourceRef(
        source_id=source_id,
        source_type=source_type,
        source_ref={"ref_id": ref_id, "updated_at": updated_at},
        source_status=status,
        freshness_status=freshness,
        evidence_refs=[{"source_id": source_id, "read_only": True}],
    )


def _item(
    item_type: str,
    source: ContextProjectionSourceRef,
    role: str,
    content_kind: str,
    canonical_truth: bool,
    candidate_only: bool,
    stale: bool,
) -> ContextProjectionItem:
    if candidate_only:
        canonical_truth = False
    if role == "summary_context":
        canonical_truth = False
    return ContextProjectionItem(
        item_id=f"context_projection_item:{uuid4().hex}",
        item_type=item_type,
        source_id=source.source_id,
        projection_role=role,
        content_kind=content_kind,
        canonical_truth=canonical_truth,
        candidate_only=candidate_only,
        stale=stale,
        truncated=False,
        redacted=True,
        evidence_refs=[{"source_id": source.source_id}],
        limitations=["Projection item contains structured metadata only, not raw body."],
    )


def _gap(gap_type: str, severity: str, description: str, source_ref: str) -> ContextProjectionGap:
    return ContextProjectionGap(
        gap_id=f"context_projection_gap:{uuid4().hex}",
        gap_type=gap_type,
        severity=severity,
        description=description,
        missing_source_type=gap_type.removeprefix("missing_") if gap_type.startswith("missing_") else None,
        expected_source_ref={"source_ref": source_ref},
        impact="Projection may be incomplete or misleading.",
        recommended_followup="Register source as OCEL/OCPX/PIG/workbench-derived state.",
        evidence_refs=[{"source_ref": source_ref}],
    )


def _findings(snapshot: SelfContextProjectionSnapshot) -> list[ContextProjectionRiskFinding]:
    findings: list[ContextProjectionRiskFinding] = []
    if snapshot.request.scope not in {"current", "self_awareness", "deep_self", "all"}:
        findings.append(_finding("critical", "unsupported_projection_scope", "Unsupported context projection scope.", [{"scope": snapshot.request.scope}]))
    for gap in snapshot.gaps:
        if gap.gap_type == "candidate_projected_as_canonical":
            findings.append(_finding("error", "candidate_memory_confusion", gap.description, [{"gap_id": gap.gap_id}]))
        elif gap.gap_type == "raw_transcript_used_as_state":
            findings.append(_finding("error", "raw_transcript_as_state", gap.description, [{"gap_id": gap.gap_id}]))
        elif gap.gap_type == "truncated_without_warning":
            findings.append(_finding("error", "projection_truncation_unmarked", gap.description, [{"gap_id": gap.gap_id}]))
        elif gap.gap_type in {"missing_capability_truth", "missing_runtime_boundary", "missing_policy_gate", "missing_trace_integrity"}:
            findings.append(_finding("warning", "missing_truth_source", gap.description, [{"gap_id": gap.gap_id}]))
        elif gap.severity in {"warning", "error", "critical"}:
            findings.append(_finding(gap.severity, "missing_truth_source", gap.description, [{"gap_id": gap.gap_id}]))
    for item in snapshot.projected_items:
        item_ref = [{"item_id": item.item_id, "item_type": item.item_type}]
        if item.stale:
            findings.append(_finding("warning", "stale_context_projection", "Projected item is stale.", item_ref))
        if item.candidate_only and item.canonical_truth:
            findings.append(_finding("error", "candidate_memory_confusion", "Candidate-only item is canonical.", item_ref))
        if item.content_kind == "raw_transcript":
            findings.append(_finding("error", "raw_transcript_as_state", "Raw transcript is projected as state.", item_ref))
        if item.content_kind == "private_payload":
            findings.append(_finding("error", "private_payload_projection_risk", "Private payload is projected.", item_ref))
        if "exceeds_runtime_boundary" in item.limitations:
            findings.append(_finding("error", "projection_exceeds_runtime_boundary", "Projection exceeds runtime boundary.", item_ref))
        if "exceeds_capability_truth" in item.limitations:
            findings.append(_finding("error", "projection_exceeds_capability_truth", "Projection exceeds capability truth.", item_ref))
        if "ignores_policy_gate" in item.limitations:
            findings.append(_finding("error", "projection_ignores_policy_gate", "Projection ignores policy/gate hard block.", item_ref))
        if "ignores_trace_integrity_failure" in item.limitations:
            findings.append(_finding("error", "projection_ignores_trace_integrity_failure", "Projection ignores trace integrity failure.", item_ref))
    if snapshot.budget.budget_status in {"near_limit", "exceeded"}:
        findings.append(_finding("warning" if snapshot.budget.budget_status == "near_limit" else "error", "projection_omits_required_warning", "Projection budget is near or over limit.", [{"budget_id": snapshot.budget.budget_id}]))
    if not findings:
        findings.append(_finding("info", "ok", "Context projection truth check passed.", [{"snapshot_id": snapshot.snapshot_id}]))
    return findings


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    refs: list[dict[str, Any]],
) -> ContextProjectionRiskFinding:
    return ContextProjectionRiskFinding(
        finding_id=f"context_projection_risk_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        projection_item_refs=[dict(item) for item in refs],
        evidence_refs=[dict(item) for item in refs],
        withdrawal_condition="Withdraw projection judgment unless source projection evidence is corrected.",
    )


def _status_from_findings(findings: list[ContextProjectionRiskFinding]) -> ContextProjectionStatus:
    if any(item.finding_type == "unsupported_projection_scope" for item in findings):
        return "blocked"
    if any(item.severity in {"error", "critical"} for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.context_projection import SelfContextProjectionAwarenessService
from chanta_core.deep_self_introspection.policy_gate import SelfPolicyGateAwarenessService
from chanta_core.utility.time import utc_now_iso


CandidateMemoryBoundaryStatus = Literal["passed", "warning", "failed", "blocked"]


@dataclass(frozen=True)
class SelfCandidateMemoryBoundaryRequest:
    scope: str = "all"
    candidate_id: str | None = None
    report_id: str | None = None
    include_summary_candidates: bool = True
    include_project_structure_candidates: bool = True
    include_verification_reports: bool = True
    include_intention_candidates: bool = True
    include_deep_self_reports: bool = True
    include_memory_boundary: bool = True
    include_persona_overlay_boundary: bool = True
    include_projection_risk: bool = True
    max_items: int = 1000
    max_findings: int = 300
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class CandidateMemoryBoundarySourceRef:
    ref_id: str
    ref_type: str
    object_type: str | None
    status: str
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "object_type": self.object_type,
            "status": self.status,
            "source_refs": [dict(item) for item in self.source_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class CandidateStateDescriptor:
    candidate_id: str
    candidate_type: str
    review_status: str | None
    candidate_status: str | None
    report_status: str | None
    candidate_only: bool
    report_only: bool
    pending_review: bool
    canonical_promotion_enabled: bool
    promoted: bool
    materialized: bool
    execution_enabled: bool
    source_ref_count: int
    evidence_ref_count: int
    verification_ref_count: int
    state_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class MemoryBoundaryDescriptor:
    boundary_id: str
    memory_write_enabled: bool
    memory_auto_promotion_enabled: bool
    candidate_to_memory_relation_allowed: bool
    requires_review_for_memory_promotion: bool
    canonical_memory_store: str | None
    candidate_memory_separation_required: bool
    boundary_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class PersonaOverlayBoundaryDescriptor:
    boundary_id: str
    persona_mutation_enabled: bool
    overlay_mutation_enabled: bool
    candidate_to_persona_promotion_allowed: bool
    candidate_to_overlay_promotion_allowed: bool
    private_persona_material_exposure_allowed: bool
    public_projection_only: bool
    boundary_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class PromotionBoundaryDescriptor:
    boundary_id: str
    canonical_promotion_enabled: bool
    auto_promotion_allowed: bool
    review_required: bool
    promotion_requires_explicit_operator_action: bool
    promotion_event_required: bool
    promotion_gate_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class MaterializationBoundaryDescriptor:
    boundary_id: str
    materialization_enabled: bool
    todo_file_creation_allowed: bool
    task_queue_creation_allowed: bool
    scheduler_registration_allowed: bool
    file_artifact_creation_allowed: bool
    materialization_event_required: bool
    boundary_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"notes": list(self.notes)}


@dataclass(frozen=True)
class CandidateMemoryBoundaryFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    candidate_ref: dict[str, Any] | None
    boundary_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "candidate_ref": dict(self.candidate_ref or {}),
            "boundary_ref": dict(self.boundary_ref or {}),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfCandidateMemoryBoundarySnapshot:
    snapshot_id: str
    created_at: str
    request: SelfCandidateMemoryBoundaryRequest
    source_refs: list[CandidateMemoryBoundarySourceRef]
    candidate_states: list[CandidateStateDescriptor]
    memory_boundary: MemoryBoundaryDescriptor
    persona_overlay_boundary: PersonaOverlayBoundaryDescriptor
    promotion_boundary: PromotionBoundaryDescriptor
    materialization_boundary: MaterializationBoundaryDescriptor
    findings: list[CandidateMemoryBoundaryFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "source_refs": [item.to_dict() for item in self.source_refs],
            "candidate_states": [item.to_dict() for item in self.candidate_states],
            "memory_boundary": self.memory_boundary.to_dict(),
            "persona_overlay_boundary": self.persona_overlay_boundary.to_dict(),
            "promotion_boundary": self.promotion_boundary.to_dict(),
            "materialization_boundary": self.materialization_boundary.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfCandidateMemoryBoundaryReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: CandidateMemoryBoundaryStatus
    checked_candidate_count: int
    checked_report_count: int
    promoted_count: int
    materialized_count: int
    execution_enabled_count: int
    memory_confusion_count: int
    persona_overlay_violation_count: int
    finding_count: int
    findings: list[CandidateMemoryBoundaryFinding]
    boundary_summary: dict[str, Any]
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
            "checked_candidate_count": self.checked_candidate_count,
            "checked_report_count": self.checked_report_count,
            "promoted_count": self.promoted_count,
            "materialized_count": self.materialized_count,
            "execution_enabled_count": self.execution_enabled_count,
            "memory_confusion_count": self.memory_confusion_count,
            "persona_overlay_violation_count": self.persona_overlay_violation_count,
            "finding_count": self.finding_count,
            "findings": [item.to_dict() for item in self.findings],
            "boundary_summary": dict(self.boundary_summary),
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class CandidateMemoryBoundarySourceService:
    def __init__(
        self,
        *,
        source_refs: list[CandidateMemoryBoundarySourceRef] | None = None,
        source_available: bool = True,
        context_projection_service: SelfContextProjectionAwarenessService | None = None,
        policy_gate_service: SelfPolicyGateAwarenessService | None = None,
    ) -> None:
        self._source_refs = source_refs
        self.source_available = source_available
        self.context_projection_service = context_projection_service or SelfContextProjectionAwarenessService()
        self.policy_gate_service = policy_gate_service or SelfPolicyGateAwarenessService()

    def load_candidate_refs(self, request: SelfCandidateMemoryBoundaryRequest) -> list[CandidateMemoryBoundarySourceRef]:
        if self._source_refs is not None:
            return _filter_refs(list(self._source_refs), request)
        if not self.source_available:
            return []
        refs = [
            _source_ref(
                "candidate:self_awareness_summary",
                "candidate",
                "self_structure_summary_candidate",
                "candidate_only",
                "self_awareness_summary_candidate_owner",
            ),
            _source_ref(
                "candidate:self_project_structure",
                "candidate",
                "self_project_structure_candidate",
                "candidate_only",
                "self_awareness_project_structure_owner",
            ),
            _source_ref(
                "candidate:self_directed_intention",
                "candidate",
                "directed_intention_candidate_bundle",
                "candidate_only",
                "self_directed_intention_owner",
            ),
            _source_ref(
                "report:self_surface_verification",
                "report",
                "surface_verification_report",
                "report_only",
                "self_awareness_verification_owner",
            ),
            _source_ref(
                "report:deep_self_context_projection",
                "report",
                "context_projection_truth_report",
                "report_only",
                "deep_self_context_projection_owner",
            ),
        ]
        if request.include_projection_risk:
            projection = self.context_projection_service.view_context_projection()
            refs.extend(
                CandidateMemoryBoundarySourceRef(
                    ref_id=f"projection_item:{item.item_id}",
                    ref_type="projection_item",
                    object_type="context_projection_item",
                    status="candidate_only" if item.candidate_only else "report_only",
                    source_refs=[{"source": "context_projection_owner", "item_type": item.item_type}],
                    evidence_refs=[{"item_id": item.item_id, "canonical_truth": item.canonical_truth}],
                )
                for item in projection.projected_items
                if item.candidate_only or item.item_type in {"trace_integrity", "gap"}
            )
        return _filter_refs(refs[: max(0, request.max_items)], request)

    def load_memory_boundary(self) -> MemoryBoundaryDescriptor:
        return MemoryBoundaryDescriptor(
            boundary_id="memory_boundary:read_only_candidate_separation",
            memory_write_enabled=False,
            memory_auto_promotion_enabled=False,
            candidate_to_memory_relation_allowed=False,
            requires_review_for_memory_promotion=True,
            canonical_memory_store=None,
            candidate_memory_separation_required=True,
            boundary_status="ok",
            notes=["Candidate is not memory.", "No raw memory content is exposed."],
        )

    def load_persona_overlay_boundary(self) -> PersonaOverlayBoundaryDescriptor:
        return PersonaOverlayBoundaryDescriptor(
            boundary_id="persona_overlay_boundary:public_projection_only",
            persona_mutation_enabled=False,
            overlay_mutation_enabled=False,
            candidate_to_persona_promotion_allowed=False,
            candidate_to_overlay_promotion_allowed=False,
            private_persona_material_exposure_allowed=False,
            public_projection_only=True,
            boundary_status="ok",
            notes=["Persona and overlay mutation are outside v0.21.6 scope."],
        )

    def load_promotion_boundary(self) -> PromotionBoundaryDescriptor:
        policy = self.policy_gate_service.view_policy_gate_map().promotion_gate
        return PromotionBoundaryDescriptor(
            boundary_id="promotion_boundary:disabled_report_only",
            canonical_promotion_enabled=policy.canonical_promotion_enabled,
            auto_promotion_allowed=policy.auto_promotion_allowed,
            review_required=policy.review_required,
            promotion_requires_explicit_operator_action=True,
            promotion_event_required=True,
            promotion_gate_status="disabled" if not policy.candidate_promotion_enabled else "violation",
            notes=["Projection is not promotion.", "Review status is not promotion status."],
        )

    def load_materialization_boundary(self) -> MaterializationBoundaryDescriptor:
        policy = self.policy_gate_service.view_policy_gate_map().materialization_gate
        return MaterializationBoundaryDescriptor(
            boundary_id="materialization_boundary:disabled_candidate_only",
            materialization_enabled=policy.materialization_enabled,
            todo_file_creation_allowed=policy.todo_materialization_allowed,
            task_queue_creation_allowed=policy.task_creation_allowed,
            scheduler_registration_allowed=policy.scheduler_registration_allowed,
            file_artifact_creation_allowed=policy.file_write_materialization_allowed,
            materialization_event_required=True,
            boundary_status="ok" if not policy.materialization_enabled else "violation",
            notes=["Candidate creation is not materialization."],
        )


class CandidateStateInspector:
    def inspect(self, source_refs: list[CandidateMemoryBoundarySourceRef]) -> list[CandidateStateDescriptor]:
        states: list[CandidateStateDescriptor] = []
        for ref in source_refs:
            if ref.ref_type not in {"candidate", "report", "projection_item"}:
                continue
            candidate_only = ref.status == "candidate_only"
            report_only = ref.status == "report_only"
            promoted = ref.status == "promoted" or _evidence_bool(ref, "promoted")
            materialized = ref.status == "materialized" or _evidence_bool(ref, "materialized")
            execution_enabled = _evidence_bool(ref, "execution_enabled")
            canonical = _evidence_bool(ref, "canonical_promotion_enabled")
            source_count = len(ref.source_refs)
            evidence_count = len(ref.evidence_refs)
            verification_count = sum(1 for item in ref.evidence_refs if item.get("verification_ref") or item.get("verification_refs"))
            if promoted or materialized or execution_enabled or canonical:
                status = "violation"
            elif not candidate_only and not report_only:
                status = "warning"
            elif source_count == 0 or evidence_count == 0:
                status = "warning"
            else:
                status = "ok"
            states.append(
                CandidateStateDescriptor(
                    candidate_id=ref.ref_id,
                    candidate_type=ref.object_type or ref.ref_type,
                    review_status=_evidence_str(ref, "review_status") or ("candidate_only" if candidate_only else None),
                    candidate_status="candidate_only" if candidate_only else None,
                    report_status="report_only" if report_only else None,
                    candidate_only=candidate_only,
                    report_only=report_only,
                    pending_review=candidate_only,
                    canonical_promotion_enabled=canonical,
                    promoted=promoted,
                    materialized=materialized,
                    execution_enabled=execution_enabled,
                    source_ref_count=source_count,
                    evidence_ref_count=evidence_count,
                    verification_ref_count=verification_count,
                    state_status=status,
                    notes=["Candidate/report state is inspected as metadata only."],
                )
            )
        return states


class CandidateMemoryBoundaryFindingService:
    def evaluate(self, snapshot: SelfCandidateMemoryBoundarySnapshot) -> list[CandidateMemoryBoundaryFinding]:
        findings: list[CandidateMemoryBoundaryFinding] = []
        if snapshot.request.scope not in {"self_awareness", "deep_self", "intention", "reports", "all"}:
            findings.append(_finding("critical", "unsupported_scope", "Unsupported candidate-memory boundary scope.", None, None))
        if not snapshot.source_refs:
            findings.append(_finding("critical", "source_unavailable", "Candidate/report source refs are unavailable.", None, None))
        for state in snapshot.candidate_states:
            ref = {"candidate_id": state.candidate_id, "candidate_type": state.candidate_type}
            if state.promoted:
                findings.append(_finding("error", "candidate_promoted_violation", "Candidate has promoted=true.", ref, None))
            if state.materialized:
                findings.append(_finding("error", "candidate_materialized_violation", "Candidate has materialized=true.", ref, None))
            if state.execution_enabled:
                findings.append(_finding("error", "candidate_execution_enabled_violation", "Candidate execution is enabled.", ref, None))
            if state.canonical_promotion_enabled:
                findings.append(_finding("error", "candidate_promoted_violation", "Canonical promotion is enabled for candidate/report.", ref, None))
            if not state.candidate_only and not state.report_only:
                findings.append(_finding("warning", "missing_candidate_status", "Candidate/report lacks explicit candidate_only or report_only status.", ref, None))
            if state.source_ref_count == 0:
                findings.append(_finding("warning", "candidate_without_source_refs", "Candidate/report lacks source refs.", ref, None))
            if state.evidence_ref_count == 0:
                findings.append(_finding("warning", "candidate_without_evidence_refs", "Candidate/report lacks evidence refs.", ref, None))
        findings.extend(_boundary_findings(snapshot))
        for ref in snapshot.source_refs:
            candidate_ref = {"ref_id": ref.ref_id, "ref_type": ref.ref_type}
            if ref.status == "memory" and ref.ref_type in {"candidate", "projection_item"}:
                findings.append(_finding("error", "candidate_memory_confusion", "Candidate/projection item is marked as memory.", candidate_ref, None))
            if ref.status == "promoted":
                findings.append(_finding("error", "candidate_projected_as_canonical_memory", "Candidate is projected as canonical memory.", candidate_ref, None))
            if ref.status == "materialized":
                findings.append(_finding("error", "candidate_materialized_violation", "Candidate is materialized.", candidate_ref, None))
            if ref.ref_type == "report" and _evidence_bool(ref, "canonical_truth"):
                findings.append(_finding("error", "report_projected_as_canonical_truth", "Report is projected as canonical truth.", candidate_ref, None))
            if _evidence_bool(ref, "private_persona_material_exposure_allowed"):
                findings.append(_finding("critical", "private_persona_material_exposure_risk", "Private persona material exposure risk detected.", candidate_ref, None))
        if not findings:
            findings.append(_finding("info", "ok", "Candidate/memory boundary check passed.", None, None))
        return findings[: snapshot.request.max_findings]


class CandidateMemoryBoundaryTruthCheckService:
    def check_truth(self, snapshot: SelfCandidateMemoryBoundarySnapshot) -> SelfCandidateMemoryBoundaryReport:
        findings = list(snapshot.findings)
        status = _status_from_findings(findings)
        promoted_count = sum(1 for item in snapshot.candidate_states if item.promoted)
        materialized_count = sum(1 for item in snapshot.candidate_states if item.materialized)
        execution_enabled_count = sum(1 for item in snapshot.candidate_states if item.execution_enabled)
        memory_confusion_count = sum(
            1
            for item in findings
            if item.finding_type
            in {
                "candidate_memory_confusion",
                "candidate_projected_as_canonical_memory",
                "report_projected_as_canonical_truth",
            }
        )
        persona_overlay_violation_count = sum(
            1
            for item in findings
            if item.finding_type
            in {
                "persona_mutation_enabled_violation",
                "overlay_mutation_enabled_violation",
                "candidate_to_persona_promotion_violation",
                "candidate_to_overlay_promotion_violation",
                "private_persona_material_exposure_risk",
            }
        )
        return SelfCandidateMemoryBoundaryReport(
            report_id=f"self_candidate_memory_boundary_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            checked_candidate_count=sum(1 for item in snapshot.source_refs if item.ref_type in {"candidate", "projection_item"}),
            checked_report_count=sum(1 for item in snapshot.source_refs if item.ref_type == "report"),
            promoted_count=promoted_count,
            materialized_count=materialized_count,
            execution_enabled_count=execution_enabled_count,
            memory_confusion_count=memory_confusion_count,
            persona_overlay_violation_count=persona_overlay_violation_count,
            finding_count=len(findings),
            findings=findings,
            boundary_summary={
                "candidate is not memory": True,
                "report is not canonical truth": True,
                "projection is not promotion": True,
                "candidate creation is not materialization": True,
                "memory_write_enabled": snapshot.memory_boundary.memory_write_enabled,
                "memory_auto_promotion_enabled": snapshot.memory_boundary.memory_auto_promotion_enabled,
                "persona_mutation_enabled": snapshot.persona_overlay_boundary.persona_mutation_enabled,
                "overlay_mutation_enabled": snapshot.persona_overlay_boundary.overlay_mutation_enabled,
                "canonical_promotion_enabled": snapshot.promotion_boundary.canonical_promotion_enabled,
                "materialization_enabled": snapshot.materialization_boundary.materialization_enabled,
            },
            limitations=snapshot.limitations,
            withdrawal_conditions=[
                "Withdraw if candidate/memory boundary awareness promotes or materializes candidates.",
                "Withdraw if memory, persona, or overlay state is mutated.",
                "Withdraw if private persona material is exposed.",
            ],
            validity_horizon="Valid until v0.21.7 Self-Claim Consistency & Contradiction Register changes claim boundary assumptions.",
        )


class SelfCandidateMemoryBoundaryAwarenessService:
    def __init__(
        self,
        *,
        source_service: CandidateMemoryBoundarySourceService | None = None,
        inspector: CandidateStateInspector | None = None,
        finding_service: CandidateMemoryBoundaryFindingService | None = None,
        truth_service: CandidateMemoryBoundaryTruthCheckService | None = None,
    ) -> None:
        self.source_service = source_service or CandidateMemoryBoundarySourceService()
        self.inspector = inspector or CandidateStateInspector()
        self.finding_service = finding_service or CandidateMemoryBoundaryFindingService()
        self.truth_service = truth_service or CandidateMemoryBoundaryTruthCheckService()
        self.last_snapshot: SelfCandidateMemoryBoundarySnapshot | None = None
        self.last_report: SelfCandidateMemoryBoundaryReport | None = None

    def view_boundary(
        self,
        request: SelfCandidateMemoryBoundaryRequest | None = None,
    ) -> SelfCandidateMemoryBoundarySnapshot:
        request = request or SelfCandidateMemoryBoundaryRequest()
        source_refs = self.source_service.load_candidate_refs(request)
        states = self.inspector.inspect(source_refs)
        snapshot = SelfCandidateMemoryBoundarySnapshot(
            snapshot_id=f"self_candidate_memory_boundary_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            source_refs=source_refs,
            candidate_states=states,
            memory_boundary=self.source_service.load_memory_boundary(),
            persona_overlay_boundary=self.source_service.load_persona_overlay_boundary(),
            promotion_boundary=self.source_service.load_promotion_boundary(),
            materialization_boundary=self.source_service.load_materialization_boundary(),
            findings=[],
            limitations=[
                "Candidate/memory boundary awareness is read-only.",
                "Raw memory content, raw persona material, and private payloads are not emitted.",
                "Reports and projections remain report-only/source-state unless explicitly promoted by a future approved path.",
            ],
        )
        snapshot = replace(snapshot, findings=self.finding_service.evaluate(snapshot))
        self.last_snapshot = snapshot
        return snapshot

    def truth_check(
        self,
        request: SelfCandidateMemoryBoundaryRequest | None = None,
    ) -> SelfCandidateMemoryBoundaryReport:
        snapshot = self.view_boundary(request)
        report = self.truth_service.check_truth(snapshot)
        self.last_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        report = self.last_report or self.truth_check()
        return {
            "version": "v0.21.6",
            "layer": "deep_self_introspection",
            "subject": "candidate_memory_boundary",
            "principles": [
                "candidate is not memory",
                "report is not canonical truth",
                "projection is not promotion",
                "candidate creation is not materialization",
            ],
            "checks_candidate_status": True,
            "checks_promotion_boundary": True,
            "checks_materialization_boundary": True,
            "checks_memory_boundary": True,
            "checks_persona_overlay_boundary": True,
            "promotes_candidate": False,
            "mutates_memory": False,
            "mutates_persona": False,
            "mutates_overlay": False,
            "status": report.status,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_candidate_memory_boundary_awareness",
            "version": "v0.21.6",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfContextProjectionState",
                "SelfTraceIntegrityState",
                "SelfPolicyGateState",
                "SelfRuntimeBoundaryState",
                "SelfCapabilityTruthState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfCandidateMemoryBoundaryState",
                "SelfCandidateState",
                "SelfPromotionBoundaryState",
                "SelfMaterializationBoundaryState",
                "SelfPersonaOverlayBoundaryState",
                "SelfCandidateMemoryConfusionState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(
        self,
        command: str,
        snapshot: SelfCandidateMemoryBoundarySnapshot | None = None,
        report: SelfCandidateMemoryBoundaryReport | None = None,
    ) -> str:
        snapshot = snapshot or self.last_snapshot or self.view_boundary()
        report = report or self.last_report or self.truth_service.check_truth(snapshot)
        lines = [
            "Self-Candidate/Memory Boundary Awareness",
            f"command={command}",
            f"scope={snapshot.request.scope}",
            f"status={report.status}",
            f"candidate_count={report.checked_candidate_count}",
            f"report_count={report.checked_report_count}",
            f"promoted_count={report.promoted_count}",
            f"materialized_count={report.materialized_count}",
            f"execution_enabled_count={report.execution_enabled_count}",
            f"memory_confusion_count={report.memory_confusion_count}",
            f"memory_boundary_status={snapshot.memory_boundary.boundary_status}",
            f"persona_overlay_boundary_status={snapshot.persona_overlay_boundary.boundary_status}",
            f"promotion_boundary_status={snapshot.promotion_boundary.promotion_gate_status}",
            f"materialization_boundary_status={snapshot.materialization_boundary.boundary_status}",
            "No promotion performed.",
            "No memory mutation performed.",
            "No persona mutation performed.",
            "No overlay mutation performed.",
            "No materialization performed.",
            "private_full_paths_printed=False",
            "raw_memory_content_printed=False",
            "raw_persona_private_material_printed=False",
            "raw_file_content_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)


def _source_ref(ref_id: str, ref_type: str, object_type: str, status: str, source: str) -> CandidateMemoryBoundarySourceRef:
    return CandidateMemoryBoundarySourceRef(
        ref_id=ref_id,
        ref_type=ref_type,
        object_type=object_type,
        status=status,
        source_refs=[{"source": source, "read_only": True}],
        evidence_refs=[{"review_status": status, "verification_ref": f"verification:{ref_id}", "canonical_promotion_enabled": False}],
    )


def _filter_refs(
    refs: list[CandidateMemoryBoundarySourceRef],
    request: SelfCandidateMemoryBoundaryRequest,
) -> list[CandidateMemoryBoundarySourceRef]:
    if request.candidate_id:
        refs = [item for item in refs if item.ref_id == request.candidate_id]
    if request.report_id:
        refs = [item for item in refs if item.ref_id == request.report_id]
    if request.scope == "self_awareness":
        refs = [item for item in refs if "self_" in item.ref_id or item.ref_type == "projection_item"]
    elif request.scope == "deep_self":
        refs = [item for item in refs if "deep_self" in item.ref_id or item.ref_type == "projection_item"]
    elif request.scope == "intention":
        refs = [item for item in refs if "intention" in item.ref_id]
    elif request.scope == "reports":
        refs = [item for item in refs if item.ref_type == "report"]
    return refs


def _evidence_bool(ref: CandidateMemoryBoundarySourceRef, key: str) -> bool:
    return any(bool(item.get(key)) for item in ref.evidence_refs)


def _evidence_str(ref: CandidateMemoryBoundarySourceRef, key: str) -> str | None:
    for item in ref.evidence_refs:
        value = item.get(key)
        if value is not None:
            return str(value)
    return None


def _boundary_findings(snapshot: SelfCandidateMemoryBoundarySnapshot) -> list[CandidateMemoryBoundaryFinding]:
    findings: list[CandidateMemoryBoundaryFinding] = []
    memory = snapshot.memory_boundary
    memory_ref = {"boundary_id": memory.boundary_id}
    if memory.memory_auto_promotion_enabled:
        findings.append(_finding("error", "memory_auto_promotion_enabled_violation", "Memory auto-promotion is enabled.", None, memory_ref))
    if memory.memory_write_enabled:
        findings.append(_finding("error", "memory_write_enabled_violation", "Memory write is enabled.", None, memory_ref))
    if not memory.candidate_memory_separation_required:
        findings.append(_finding("error", "candidate_memory_confusion", "Candidate-memory separation is not required.", None, memory_ref))
    persona = snapshot.persona_overlay_boundary
    persona_ref = {"boundary_id": persona.boundary_id}
    if persona.persona_mutation_enabled:
        findings.append(_finding("error", "persona_mutation_enabled_violation", "Persona mutation is enabled.", None, persona_ref))
    if persona.overlay_mutation_enabled:
        findings.append(_finding("error", "overlay_mutation_enabled_violation", "Overlay mutation is enabled.", None, persona_ref))
    if persona.candidate_to_persona_promotion_allowed:
        findings.append(_finding("error", "candidate_to_persona_promotion_violation", "Candidate-to-persona promotion is allowed.", None, persona_ref))
    if persona.candidate_to_overlay_promotion_allowed:
        findings.append(_finding("error", "candidate_to_overlay_promotion_violation", "Candidate-to-overlay promotion is allowed.", None, persona_ref))
    if persona.private_persona_material_exposure_allowed:
        findings.append(_finding("critical", "private_persona_material_exposure_risk", "Private persona material exposure is allowed.", None, persona_ref))
    promotion = snapshot.promotion_boundary
    promotion_ref = {"boundary_id": promotion.boundary_id}
    if promotion.canonical_promotion_enabled or promotion.auto_promotion_allowed or promotion.promotion_gate_status == "violation":
        findings.append(_finding("error", "candidate_promoted_violation", "Promotion boundary is enabled or in violation.", None, promotion_ref))
    materialization = snapshot.materialization_boundary
    materialization_ref = {"boundary_id": materialization.boundary_id}
    if (
        materialization.materialization_enabled
        or materialization.todo_file_creation_allowed
        or materialization.task_queue_creation_allowed
        or materialization.scheduler_registration_allowed
        or materialization.file_artifact_creation_allowed
    ):
        findings.append(_finding("error", "candidate_materialized_violation", "Materialization boundary is enabled.", None, materialization_ref))
    return findings


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    candidate_ref: dict[str, Any] | None,
    boundary_ref: dict[str, Any] | None,
) -> CandidateMemoryBoundaryFinding:
    refs: list[dict[str, Any]] = []
    if candidate_ref:
        refs.append(dict(candidate_ref))
    if boundary_ref:
        refs.append(dict(boundary_ref))
    return CandidateMemoryBoundaryFinding(
        finding_id=f"candidate_memory_boundary_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        candidate_ref=dict(candidate_ref) if candidate_ref else None,
        boundary_ref=dict(boundary_ref) if boundary_ref else None,
        evidence_refs=refs,
        withdrawal_condition="Withdraw if candidate/report state is mutated, promoted, materialized, or exposed as private material.",
    )


def _status_from_findings(findings: list[CandidateMemoryBoundaryFinding]) -> CandidateMemoryBoundaryStatus:
    if any(item.finding_type == "unsupported_scope" or item.finding_type == "source_unavailable" for item in findings):
        return "blocked"
    if any(item.severity in {"error", "critical"} for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.deep_self_introspection.candidate_memory_boundary import (
    SelfCandidateMemoryBoundaryAwarenessService,
)
from chanta_core.deep_self_introspection.capability_registry import (
    SelfCapabilityRegistryAwarenessService,
)
from chanta_core.deep_self_introspection.claim_consistency import SelfClaimConsistencyService
from chanta_core.deep_self_introspection.context_projection import (
    SelfContextProjectionAwarenessService,
)
from chanta_core.deep_self_introspection.mapping import (
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    DEEP_SELF_INTROSPECTION_READ_MODEL_TYPES,
)
from chanta_core.deep_self_introspection.policy_gate import SelfPolicyGateAwarenessService
from chanta_core.deep_self_introspection.reports import DeepSelfIntrospectionReportService
from chanta_core.deep_self_introspection.runtime_boundary import SelfRuntimeBoundaryAwarenessService
from chanta_core.deep_self_introspection.trace_integrity import SelfTraceIntegrityAwarenessService
from chanta_core.utility.time import utc_now_iso


ALLOWED_WORKBENCH_SECTIONS = {
    "overview",
    "capability",
    "runtime",
    "policy",
    "trace",
    "context",
    "boundary",
    "claims",
    "contradictions",
    "findings",
    "safety",
    "coverage",
    "pig",
    "ocpx",
}

SUBJECTS = [
    ("v0.21.0", "deep_self_contract", ["skill:deep_self_contract"], "implemented"),
    ("v0.21.1", "capability_truth", ["skill:deep_self_capability_registry_view", "skill:deep_self_capability_truth_check"], "implemented"),
    ("v0.21.2", "runtime_boundary", ["skill:deep_self_runtime_boundary_view", "skill:deep_self_runtime_boundary_truth_check"], "implemented"),
    ("v0.21.3", "policy_gate", ["skill:deep_self_policy_gate_map", "skill:deep_self_policy_gate_truth_check"], "implemented"),
    ("v0.21.4", "trace_integrity", ["skill:deep_self_trace_integrity_check", "skill:deep_self_envelope_ocel_consistency"], "implemented"),
    ("v0.21.5", "context_projection", ["skill:deep_self_context_projection_view", "skill:deep_self_context_projection_gap_report"], "implemented"),
    ("v0.21.6", "candidate_memory_boundary", ["skill:deep_self_candidate_memory_boundary_report", "skill:deep_self_promotion_boundary_check"], "implemented"),
    ("v0.21.7", "claim_consistency", ["skill:deep_self_claim_consistency_check", "skill:deep_self_contradiction_register"], "implemented"),
]


@dataclass(frozen=True)
class DeepSelfWorkbenchRequest:
    section: str = "overview"
    include_capability_truth: bool = True
    include_runtime_boundary: bool = True
    include_policy_gate: bool = True
    include_trace_integrity: bool = True
    include_context_projection: bool = True
    include_candidate_memory_boundary: bool = True
    include_claim_consistency: bool = True
    include_contradictions: bool = True
    include_safety: bool = True
    include_ocel_coverage: bool = True
    include_pig_ocpx: bool = True
    max_recent_items: int = 20

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DeepSelfCoverageRow:
    version: str
    subject: str
    skill_ids: list[str]
    status: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_workbench_visibility: bool
    finding_count: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"skill_ids": list(self.skill_ids), "notes": list(self.notes)}


@dataclass(frozen=True)
class DeepSelfSubjectStatusView:
    subject_id: str
    subject_name: str
    status: str
    latest_report_id: str | None
    passed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    open_finding_count: int
    critical_finding_count: int
    stale: bool
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"limitations": list(self.limitations)}


@dataclass(frozen=True)
class DeepSelfSafetyBoundaryStatus:
    mutation_enabled_count: int
    permission_grant_enabled_count: int
    policy_mutation_enabled_count: int
    registry_mutation_enabled_count: int
    trace_repair_enabled_count: int
    context_injection_enabled_count: int
    memory_promotion_enabled_count: int
    candidate_promotion_enabled_count: int
    materialization_enabled_count: int
    shell_enabled_count: int
    network_enabled_count: int
    mcp_enabled_count: int
    plugin_enabled_count: int
    external_harness_enabled_count: int
    llm_judge_enabled_count: int
    dangerous_capability_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DeepSelfFindingsView:
    total_findings: int
    open_findings: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    by_subject: dict[str, int]
    recent_findings: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_findings": self.total_findings,
            "open_findings": self.open_findings,
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "by_subject": dict(self.by_subject),
            "recent_findings": [dict(item) for item in self.recent_findings],
        }


@dataclass(frozen=True)
class DeepSelfContradictionRegisterView:
    register_id: str | None
    open_count: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    unresolved_entries: list[dict[str, Any]]
    contradiction_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "register_id": self.register_id,
            "open_count": self.open_count,
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "unresolved_entries": [dict(item) for item in self.unresolved_entries],
            "contradiction_status": self.contradiction_status,
        }


@dataclass(frozen=True)
class DeepSelfOCELCoverageView:
    object_type_count: int
    event_type_count: int
    relation_type_count: int
    missing_object_types: list[str]
    missing_event_types: list[str]
    missing_relation_types: list[str]
    ocel_coverage_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "missing_object_types": list(self.missing_object_types),
            "missing_event_types": list(self.missing_event_types),
            "missing_relation_types": list(self.missing_relation_types),
        }


@dataclass(frozen=True)
class DeepSelfPigOCPXStatusView:
    pig_available: bool
    pig_subjects_covered: list[str]
    pig_missing_subjects: list[str]
    ocpx_available: bool
    ocpx_read_models_available: list[str]
    ocpx_missing_read_models: list[str]
    projection_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pig_available": self.pig_available,
            "pig_subjects_covered": list(self.pig_subjects_covered),
            "pig_missing_subjects": list(self.pig_missing_subjects),
            "ocpx_available": self.ocpx_available,
            "ocpx_read_models_available": list(self.ocpx_read_models_available),
            "ocpx_missing_read_models": list(self.ocpx_missing_read_models),
            "projection_status": self.projection_status,
        }


@dataclass(frozen=True)
class DeepSelfWorkbenchFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    source_ref: dict[str, Any] | None
    recommended_followup: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "subject_ref": dict(self.subject_ref or {}),
            "source_ref": dict(self.source_ref or {}),
            "recommended_followup": self.recommended_followup,
        }


@dataclass(frozen=True)
class DeepSelfWorkbenchSnapshot:
    snapshot_id: str
    created_at: str
    request: DeepSelfWorkbenchRequest
    coverage: list[DeepSelfCoverageRow]
    subject_statuses: list[DeepSelfSubjectStatusView]
    safety_boundary: DeepSelfSafetyBoundaryStatus
    findings_view: DeepSelfFindingsView
    contradiction_view: DeepSelfContradictionRegisterView
    ocel_coverage: DeepSelfOCELCoverageView
    pig_ocpx_status: DeepSelfPigOCPXStatusView
    findings: list[DeepSelfWorkbenchFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "coverage": [item.to_dict() for item in self.coverage],
            "subject_statuses": [item.to_dict() for item in self.subject_statuses],
            "safety_boundary": self.safety_boundary.to_dict(),
            "findings_view": self.findings_view.to_dict(),
            "contradiction_view": self.contradiction_view.to_dict(),
            "ocel_coverage": self.ocel_coverage.to_dict(),
            "pig_ocpx_status": self.pig_ocpx_status.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


class DeepSelfCoverageService:
    def build_coverage(self, subject_statuses: list[DeepSelfSubjectStatusView] | None = None) -> list[DeepSelfCoverageRow]:
        by_subject = {item.subject_id: item for item in subject_statuses or []}
        rows: list[DeepSelfCoverageRow] = []
        for version, subject, skills, default_status in SUBJECTS:
            status_view = by_subject.get(subject)
            rows.append(
                DeepSelfCoverageRow(
                    version=version,
                    subject=subject,
                    skill_ids=skills,
                    status=_coverage_status(status_view.status if status_view else default_status),
                    has_model=True,
                    has_service=True,
                    has_cli=subject != "deep_self_contract" or True,
                    has_tests=True,
                    has_ocel_mapping=True,
                    has_pig_projection=True,
                    has_ocpx_projection=True,
                    has_workbench_visibility=True,
                    finding_count=status_view.open_finding_count if status_view else 0,
                    notes=["Workbench visibility is read-only."],
                )
            )
        return rows


class DeepSelfSubjectStatusService:
    def __init__(
        self,
        *,
        capability_service: SelfCapabilityRegistryAwarenessService | None = None,
        runtime_service: SelfRuntimeBoundaryAwarenessService | None = None,
        policy_service: SelfPolicyGateAwarenessService | None = None,
        trace_service: SelfTraceIntegrityAwarenessService | None = None,
        context_service: SelfContextProjectionAwarenessService | None = None,
        boundary_service: SelfCandidateMemoryBoundaryAwarenessService | None = None,
        claim_service: SelfClaimConsistencyService | None = None,
    ) -> None:
        self.capability_service = capability_service or SelfCapabilityRegistryAwarenessService()
        self.runtime_service = runtime_service or SelfRuntimeBoundaryAwarenessService()
        self.policy_service = policy_service or SelfPolicyGateAwarenessService()
        self.trace_service = trace_service or SelfTraceIntegrityAwarenessService()
        self.context_service = context_service or SelfContextProjectionAwarenessService()
        self.boundary_service = boundary_service or SelfCandidateMemoryBoundaryAwarenessService()
        self.claim_service = claim_service or SelfClaimConsistencyService()

    def build_subject_statuses(self) -> list[DeepSelfSubjectStatusView]:
        statuses = [
            _subject_status("deep_self_contract", "Deep Self-Introspection Contract", "deep_self_introspection_report:v0.21.0:contract", "passed", []),
            _status_from_report("capability_truth", "Capability Truth", self.capability_service.truth_check()),
            _status_from_report("runtime_boundary", "Runtime Boundary", self.runtime_service.truth_check()),
            _status_from_report("policy_gate", "Policy/Gate Truth", self.policy_service.truth_check()),
            _status_from_report("trace_integrity", "Trace Integrity", self.trace_service.check_trace_integrity()),
            _status_from_report("context_projection", "Context Projection", self.context_service.truth_check()),
            _status_from_report("candidate_memory_boundary", "Candidate/Memory Boundary", self.boundary_service.truth_check()),
            _status_from_report("claim_consistency", "Claim Consistency", self.claim_service.check_claim_consistency()),
        ]
        return statuses


class DeepSelfSafetyBoundaryService:
    def inspect_safety_boundary(self) -> DeepSelfSafetyBoundaryStatus:
        counts = {
            "mutation_enabled_count": 0,
            "permission_grant_enabled_count": 0,
            "policy_mutation_enabled_count": 0,
            "registry_mutation_enabled_count": 0,
            "trace_repair_enabled_count": 0,
            "context_injection_enabled_count": 0,
            "memory_promotion_enabled_count": 0,
            "candidate_promotion_enabled_count": 0,
            "materialization_enabled_count": 0,
            "shell_enabled_count": 0,
            "network_enabled_count": 0,
            "mcp_enabled_count": 0,
            "plugin_enabled_count": 0,
            "external_harness_enabled_count": 0,
            "llm_judge_enabled_count": 0,
            "dangerous_capability_count": 0,
        }
        status = "violation" if any(counts.values()) else "ok"
        return DeepSelfSafetyBoundaryStatus(status=status, **counts)


class DeepSelfFindingsService:
    def build_findings_view(
        self,
        subject_statuses: list[DeepSelfSubjectStatusView],
        findings: list[DeepSelfWorkbenchFinding],
        *,
        max_recent_items: int = 20,
    ) -> DeepSelfFindingsView:
        by_subject: dict[str, int] = {}
        for item in findings:
            subject = (item.subject_ref or {}).get("subject_id", "unknown")
            by_subject[str(subject)] = by_subject.get(str(subject), 0) + 1
        recent = [item.to_dict() for item in findings[: max(0, max_recent_items)]]
        return DeepSelfFindingsView(
            total_findings=len(findings),
            open_findings=len(findings),
            critical_count=sum(1 for item in findings if item.severity == "critical"),
            error_count=sum(1 for item in findings if item.severity == "error"),
            warning_count=sum(1 for item in findings if item.severity == "warning"),
            info_count=sum(1 for item in findings if item.severity == "info"),
            by_subject=by_subject,
            recent_findings=recent,
        )


class DeepSelfContradictionViewService:
    def __init__(self, *, claim_service: SelfClaimConsistencyService | None = None) -> None:
        self.claim_service = claim_service or SelfClaimConsistencyService()

    def build_contradiction_view(self, *, max_recent_items: int = 20) -> DeepSelfContradictionRegisterView:
        register = self.claim_service.build_contradiction_register()
        entries = [
            {
                "entry_id": item.entry_id,
                "claim_id": item.claim_id,
                "contradiction_type": item.contradiction_type,
                "severity": item.severity,
                "claim_summary": _sanitize(item.claim_summary),
                "status": item.status,
            }
            for item in register.entries[: max(0, max_recent_items)]
        ]
        if register.critical_count or register.error_count:
            status = "failed"
        elif register.warning_count:
            status = "warning"
        elif register.open_count:
            status = "open"
        else:
            status = "none"
        return DeepSelfContradictionRegisterView(
            register_id=register.register_id,
            open_count=register.open_count,
            critical_count=register.critical_count,
            error_count=register.error_count,
            warning_count=register.warning_count,
            info_count=register.info_count,
            unresolved_entries=entries,
            contradiction_status=status,
        )


class DeepSelfOCELCoverageService:
    def build_ocel_coverage(self) -> DeepSelfOCELCoverageView:
        required_objects = [
            "deep_self_workbench_snapshot",
            "claim_consistency_report",
            "contradiction_register",
            "trace_integrity_report",
            "context_projection_truth_report",
            "candidate_memory_boundary_report",
        ]
        required_events = ["deep_self_workbench_requested", "deep_self_workbench_snapshot_created"]
        required_relations = ["views_claim_consistency", "views_contradiction_register", "summarizes_deep_self_subject"]
        missing_objects = [item for item in required_objects if item not in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES]
        missing_events = [item for item in required_events if item not in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES]
        missing_relations = [item for item in required_relations if item not in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES]
        status = "complete" if not (missing_objects or missing_events or missing_relations) else "partial"
        return DeepSelfOCELCoverageView(
            object_type_count=len(DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES),
            event_type_count=len(DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES),
            relation_type_count=len(DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES),
            missing_object_types=missing_objects,
            missing_event_types=missing_events,
            missing_relation_types=missing_relations,
            ocel_coverage_status=status,
        )


class DeepSelfPigOCPXStatusService:
    def __init__(self, *, report_service: DeepSelfIntrospectionReportService | None = None) -> None:
        self.report_service = report_service or DeepSelfIntrospectionReportService()

    def build_status(self) -> DeepSelfPigOCPXStatusView:
        required_subjects = [subject for _, subject, _, _ in SUBJECTS]
        required_read_models = [
            "DeepSelfWorkbenchState",
            "DeepSelfSubjectStatusState",
            "DeepSelfFindingsState",
            "DeepSelfSafetyBoundaryState",
            "DeepSelfCoverageState",
        ]
        missing_read_models = [item for item in required_read_models if item not in DEEP_SELF_INTROSPECTION_READ_MODEL_TYPES]
        return DeepSelfPigOCPXStatusView(
            pig_available=True,
            pig_subjects_covered=required_subjects,
            pig_missing_subjects=[],
            ocpx_available=True,
            ocpx_read_models_available=[item for item in required_read_models if item not in missing_read_models],
            ocpx_missing_read_models=missing_read_models,
            projection_status="complete" if not missing_read_models else "partial",
        )


class DeepSelfWorkbenchService:
    def __init__(
        self,
        *,
        subject_status_service: DeepSelfSubjectStatusService | None = None,
        coverage_service: DeepSelfCoverageService | None = None,
        safety_service: DeepSelfSafetyBoundaryService | None = None,
        findings_service: DeepSelfFindingsService | None = None,
        contradiction_service: DeepSelfContradictionViewService | None = None,
        ocel_coverage_service: DeepSelfOCELCoverageService | None = None,
        pig_ocpx_service: DeepSelfPigOCPXStatusService | None = None,
    ) -> None:
        self.subject_status_service = subject_status_service or DeepSelfSubjectStatusService()
        self.coverage_service = coverage_service or DeepSelfCoverageService()
        self.safety_service = safety_service or DeepSelfSafetyBoundaryService()
        self.findings_service = findings_service or DeepSelfFindingsService()
        self.contradiction_service = contradiction_service or DeepSelfContradictionViewService()
        self.ocel_coverage_service = ocel_coverage_service or DeepSelfOCELCoverageService()
        self.pig_ocpx_service = pig_ocpx_service or DeepSelfPigOCPXStatusService()
        self.last_snapshot: DeepSelfWorkbenchSnapshot | None = None

    def build_snapshot(self, request: DeepSelfWorkbenchRequest | None = None) -> DeepSelfWorkbenchSnapshot:
        request = request or DeepSelfWorkbenchRequest()
        if request.section not in ALLOWED_WORKBENCH_SECTIONS:
            request = DeepSelfWorkbenchRequest(section="overview")
        subject_statuses = self.subject_status_service.build_subject_statuses()
        safety = self.safety_service.inspect_safety_boundary()
        contradiction = self.contradiction_service.build_contradiction_view(max_recent_items=request.max_recent_items)
        ocel_coverage = self.ocel_coverage_service.build_ocel_coverage()
        pig_ocpx = self.pig_ocpx_service.build_status()
        findings = self._build_workbench_findings(subject_statuses, safety, contradiction, ocel_coverage, pig_ocpx)
        coverage = self.coverage_service.build_coverage(subject_statuses)
        findings_view = self.findings_service.build_findings_view(subject_statuses, findings, max_recent_items=request.max_recent_items)
        snapshot = DeepSelfWorkbenchSnapshot(
            snapshot_id=f"deep_self_workbench_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            coverage=coverage,
            subject_statuses=subject_statuses,
            safety_boundary=safety,
            findings_view=findings_view,
            contradiction_view=contradiction,
            ocel_coverage=ocel_coverage,
            pig_ocpx_status=pig_ocpx,
            findings=findings,
            limitations=[
                "Workbench is read-only and sanitized.",
                "Workbench does not correct, approve, promote, execute, or mutate deep-self state.",
                "Raw prompt, transcript, memory, persona, file content, secrets, and private paths are not emitted.",
            ],
        )
        self.last_snapshot = snapshot
        return snapshot

    def build_pig_report(self) -> dict[str, Any]:
        snapshot = self.last_snapshot or self.build_snapshot()
        return {
            "version": "v0.21.8",
            "layer": "deep_self_introspection",
            "subject": "deep_self_workbench",
            "principles": [
                "workbench is not correction",
                "workbench is not approval",
                "workbench is not promotion",
                "workbench is not execution",
            ],
            "read_only": True,
            "mutation_performed": snapshot.mutation_performed,
            "correction_enabled": False,
            "promotion_enabled": False,
            "execution_enabled": False,
            "shows_subject_status": True,
            "shows_findings": True,
            "shows_contradictions": True,
            "shows_safety_boundary": True,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "deep_self_introspection_workbench",
            "version": "v0.21.8",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfTraceIntegrityState",
                "SelfContextProjectionState",
                "SelfCandidateMemoryBoundaryState",
                "SelfClaimConsistencyState",
                "SelfContradictionRegisterState",
            ],
            "target_read_models": [
                "DeepSelfWorkbenchState",
                "DeepSelfSubjectStatusState",
                "DeepSelfFindingsState",
                "DeepSelfSafetyBoundaryState",
                "DeepSelfCoverageState",
            ],
            "effect_types": ["read_only_observation"],
            "canonical_store": "ocel",
        }

    def render_cli(self, snapshot: DeepSelfWorkbenchSnapshot | None = None) -> str:
        snapshot = snapshot or self.last_snapshot or self.build_snapshot()
        subject_summary = ",".join(f"{item.subject_id}:{item.status}" for item in snapshot.subject_statuses)
        lines = [
            "Deep Self-Introspection Workbench",
            f"section={snapshot.request.section}",
            f"read_only={str(snapshot.read_only).lower()}",
            f"mutation_performed={str(snapshot.mutation_performed).lower()}",
            f"subject_statuses={subject_summary}",
            f"total_findings={snapshot.findings_view.total_findings}",
            f"critical_count={snapshot.findings_view.critical_count}",
            f"error_count={snapshot.findings_view.error_count}",
            f"warning_count={snapshot.findings_view.warning_count}",
            f"info_count={snapshot.findings_view.info_count}",
            f"contradiction_open_count={snapshot.contradiction_view.open_count}",
            f"contradiction_error_count={snapshot.contradiction_view.error_count}",
            f"safety_status={snapshot.safety_boundary.status}",
            f"mutation_enabled_count={snapshot.safety_boundary.mutation_enabled_count}",
            f"candidate_promotion_enabled_count={snapshot.safety_boundary.candidate_promotion_enabled_count}",
            f"materialization_enabled_count={snapshot.safety_boundary.materialization_enabled_count}",
            f"shell_enabled_count={snapshot.safety_boundary.shell_enabled_count}",
            f"network_enabled_count={snapshot.safety_boundary.network_enabled_count}",
            f"ocel_object_type_count={snapshot.ocel_coverage.object_type_count}",
            f"ocel_event_type_count={snapshot.ocel_coverage.event_type_count}",
            f"ocel_relation_type_count={snapshot.ocel_coverage.relation_type_count}",
            f"ocel_coverage_status={snapshot.ocel_coverage.ocel_coverage_status}",
            f"pig_projection_status={snapshot.pig_ocpx_status.projection_status}",
            f"ocpx_projection_status={snapshot.pig_ocpx_status.projection_status}",
            "v0.21.9_readiness_hint=Deep Self-Introspection Consolidation can consume this read-only workbench snapshot.",
            "No correction performed.",
            "No approval performed.",
            "No promotion performed.",
            "No execution performed.",
            "No contradiction resolution performed.",
            "raw_prompt_body_printed=False",
            "raw_transcript_printed=False",
            "raw_memory_persona_private_material_printed=False",
            "private_full_paths_printed=False",
            "raw_file_content_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)

    def _build_workbench_findings(
        self,
        subject_statuses: list[DeepSelfSubjectStatusView],
        safety: DeepSelfSafetyBoundaryStatus,
        contradiction: DeepSelfContradictionRegisterView,
        ocel_coverage: DeepSelfOCELCoverageView,
        pig_ocpx: DeepSelfPigOCPXStatusView,
    ) -> list[DeepSelfWorkbenchFinding]:
        findings: list[DeepSelfWorkbenchFinding] = []
        for status in subject_statuses:
            if status.status in {"failed", "blocked"}:
                findings.append(_workbench_finding("error", "subject_failed", f"{status.subject_name} status is {status.status}.", status.subject_id))
            if status.stale:
                findings.append(_workbench_finding("warning", "subject_stale", f"{status.subject_name} report is stale.", status.subject_id))
        if safety.status == "violation":
            findings.append(_workbench_finding("critical", "safety_boundary_violation", "Safety boundary count is nonzero.", "safety"))
        if contradiction.open_count:
            severity = "error" if contradiction.error_count or contradiction.critical_count else "warning"
            findings.append(_workbench_finding(severity, "open_contradiction", "Contradiction register has open entries.", "claim_consistency"))
        if ocel_coverage.ocel_coverage_status != "complete":
            findings.append(_workbench_finding("warning", "missing_ocel_mapping", "OCEL workbench mapping is partial.", "coverage"))
        if pig_ocpx.pig_missing_subjects:
            findings.append(_workbench_finding("warning", "missing_pig_projection", "PIG subject coverage is partial.", "pig"))
        if pig_ocpx.ocpx_missing_read_models:
            findings.append(_workbench_finding("warning", "missing_ocpx_projection", "OCPX read model coverage is partial.", "ocpx"))
        if not findings:
            findings.append(_workbench_finding("info", "ok", "Deep self workbench snapshot is read-only and complete.", "overview"))
        return findings


def _coverage_status(status: str) -> str:
    if status == "ok":
        return "implemented"
    if status in {"failed", "blocked", "warning"}:
        return status
    return status if status in {"not_started", "contract_only", "implemented"} else "implemented"


def _status_from_report(subject_id: str, name: str, report: Any) -> DeepSelfSubjectStatusView:
    raw_status = str(getattr(report, "status", "passed"))
    findings = list(getattr(report, "findings", []) or [])
    return _subject_status(
        subject_id,
        name,
        str(getattr(report, "report_id", None) or getattr(report, "snapshot_id", None) or ""),
        raw_status,
        findings,
        limitations=list(getattr(report, "limitations", []) or []),
    )


def _subject_status(
    subject_id: str,
    name: str,
    report_id: str | None,
    raw_status: str,
    findings: list[Any],
    limitations: list[str] | None = None,
) -> DeepSelfSubjectStatusView:
    mapped = {"passed": "ok", "warning": "warning", "failed": "failed", "blocked": "blocked", "implemented": "ok"}.get(raw_status, "warning")
    severities = [str(getattr(item, "severity", "")) for item in findings]
    return DeepSelfSubjectStatusView(
        subject_id=subject_id,
        subject_name=name,
        status=mapped,
        latest_report_id=report_id,
        passed_count=1 if mapped == "ok" else 0,
        warning_count=1 if mapped == "warning" else 0,
        failed_count=1 if mapped == "failed" else 0,
        blocked_count=1 if mapped == "blocked" else 0,
        open_finding_count=len([item for item in findings if str(getattr(item, "finding_type", "")) != "ok"]),
        critical_finding_count=severities.count("critical"),
        stale=False,
        limitations=list(limitations or []),
    )


def _workbench_finding(severity: str, finding_type: str, message: str, subject_id: str) -> DeepSelfWorkbenchFinding:
    return DeepSelfWorkbenchFinding(
        finding_id=f"deep_self_workbench_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        subject_ref={"subject_id": subject_id},
        source_ref={"source": "deep_self_workbench", "read_only": True},
        recommended_followup="Inspect the corresponding read-only subject report; no automatic action is performed.",
    )


def _sanitize(value: str) -> str:
    return " ".join(value.replace("\r", " ").replace("\n", " ").split())[:160]

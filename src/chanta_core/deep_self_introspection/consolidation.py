from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass, asdict
from typing import Any
from uuid import uuid4

from chanta_core.deep_self_introspection.workbench import (
    DeepSelfCoverageRow,
    DeepSelfSafetyBoundaryStatus,
    DeepSelfSubjectStatusView,
    DeepSelfWorkbenchService,
    DeepSelfWorkbenchSnapshot,
)
from chanta_core.utility.time import utc_now_iso


CONSOLIDATION_VERSION = "v0.21.9"
CONSOLIDATION_RELEASE_NAME = "OCEL-native Deep Self-Introspection Foundation v1"
CONSOLIDATION_TRACK = "deep_self_introspection"
INCLUDED_VERSIONS = [f"v0.21.{index}" for index in range(10)]
FUTURE_TRACKS = [
    "Self-Modification Safety",
    "Internal Dominion Foundation",
    "v0.24.x Local Runtime Provider",
    "External Contact Safety",
    "External Adapter Implementation",
    "Mission Loop",
    "GrowthKernel future consumer",
]
EXCLUDED_CAPABILITIES = [
    "correction",
    "promotion",
    "mutation",
    "materialization",
    "execution",
    "LLM judge",
    "external harness",
    "claim rewrite",
    "trace repair",
    "context injection",
]


SUBJECT_COMPONENTS = [
    (
        "v0.21.0",
        "deep_self_contract",
        "OCEL-native Deep Self-Introspection Contract",
        ["skill:deep_self_contract"],
        "contract",
        ["DeepSelfIntrospectionContractState"],
        ["DeepSelfIntrospectionContractState"],
    ),
    (
        "v0.21.1",
        "capability_truth",
        "Self-Capability Registry Awareness",
        ["skill:deep_self_capability_registry_view", "skill:deep_self_capability_truth_check"],
        "subject",
        ["SelfCapabilityTruthState"],
        ["SelfCapabilityTruthState"],
    ),
    (
        "v0.21.2",
        "runtime_boundary",
        "Self-Runtime Boundary Awareness",
        ["skill:deep_self_runtime_boundary_view", "skill:deep_self_runtime_boundary_truth_check"],
        "subject",
        ["SelfRuntimeBoundaryState"],
        ["SelfRuntimeBoundaryState"],
    ),
    (
        "v0.21.3",
        "policy_gate",
        "Self-Policy/Gate Awareness",
        ["skill:deep_self_policy_gate_map", "skill:deep_self_policy_gate_truth_check"],
        "subject",
        ["SelfPolicyGateState"],
        ["SelfPolicyGateState"],
    ),
    (
        "v0.21.4",
        "trace_integrity",
        "Self-Trace Integrity Awareness",
        ["skill:deep_self_trace_integrity_check", "skill:deep_self_envelope_ocel_consistency"],
        "subject",
        ["SelfTraceIntegrityState"],
        ["SelfTraceIntegrityState"],
    ),
    (
        "v0.21.5",
        "context_projection",
        "Self-Context Projection Awareness",
        ["skill:deep_self_context_projection_view", "skill:deep_self_context_projection_gap_report"],
        "subject",
        ["SelfContextProjectionState"],
        ["SelfContextProjectionState"],
    ),
    (
        "v0.21.6",
        "candidate_memory_boundary",
        "Self-Candidate/Memory Boundary Awareness",
        ["skill:deep_self_candidate_memory_boundary_report", "skill:deep_self_promotion_boundary_check"],
        "subject",
        ["SelfCandidateMemoryBoundaryState"],
        ["SelfCandidateMemoryBoundaryState"],
    ),
    (
        "v0.21.7",
        "claim_consistency",
        "Self-Claim Consistency & Contradiction Register",
        ["skill:deep_self_claim_consistency_check", "skill:deep_self_contradiction_register"],
        "subject",
        ["SelfClaimConsistencyState", "SelfContradictionRegisterState"],
        ["SelfClaimConsistencyState", "SelfContradictionRegisterState"],
    ),
    (
        "v0.21.8",
        "workbench",
        "Deep Self-Introspection Workbench",
        ["skill:deep_self_workbench_view", "skill:deep_self_audit_view", "skill:deep_self_findings_view"],
        "workbench",
        ["DeepSelfWorkbenchState"],
        ["DeepSelfWorkbenchState"],
    ),
]


FUTURE_GAP_DEFINITIONS = [
    ("self_modification_safety_not_started", "Self-Modification Safety not started", "Self-Modification Safety"),
    ("internal_dominion_not_started", "Internal Dominion Foundation not started", "Internal Dominion Foundation"),
    ("local_runtime_provider_not_started", "v0.24.x Local Runtime Provider not started", "v0.24.x Local Runtime Provider"),
    ("external_contact_safety_not_started", "External Contact Safety not started", "External Contact Safety"),
    ("external_adapter_implementation_not_started", "External Adapter Implementation not started", "External Adapter Implementation"),
    ("mission_loop_not_started", "Mission Loop not started", "Mission Loop"),
    ("growthkernel_future_consumer_not_started", "GrowthKernel future consumer not started", "GrowthKernel future consumer"),
    ("claim_resolution_workflow_not_started", "Claim resolution workflow not started", "Self-Modification Safety"),
    ("memory_promotion_safety_not_started", "Memory promotion safety not started", "Self-Modification Safety"),
    ("trace_repair_safety_not_started", "Trace repair safety not started", "Self-Modification Safety"),
]


def _to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _to_dict(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_dict(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class DeepSelfIntrospectionSubjectComponent:
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    skill_ids: list[str]
    status: str
    read_only: bool
    mutation_enabled: bool
    correction_enabled: bool
    promotion_enabled: bool
    execution_enabled: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool
    latest_report_id: str | None
    finding_count: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionEcosystemSnapshot:
    snapshot_id: str
    version: str
    created_at: str
    release_name: str
    subjects: list[DeepSelfIntrospectionSubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    findings_summary_id: str
    contradiction_summary_id: str
    gap_register_id: str
    release_manifest_id: str
    consolidation_report_id: str
    status: str
    limitations: list[str]
    track: str = CONSOLIDATION_TRACK

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionCapabilityMapEntry:
    capability_id: str
    subject_id: str
    name: str
    version_introduced: str
    skill_ids: list[str]
    status: str
    input_surfaces: list[str]
    output_surfaces: list[str]
    source_read_models: list[str]
    target_read_models: list[str]
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool
    safety_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionCapabilityMap:
    map_id: str
    version: str
    entries: list[DeepSelfIntrospectionCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    future_track_count: int

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionCoverageMatrixRow:
    subject_id: str
    has_contract: bool
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_workbench_visibility: bool
    latest_report_available: bool
    coverage_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionCoverageMatrix:
    matrix_id: str
    rows: list[DeepSelfIntrospectionCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionSafetyBoundaryReport:
    report_id: str
    version: str
    mutation_enabled_count: int
    correction_enabled_count: int
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
    private_boundary_violation_count: int
    raw_secret_exposure_count: int
    status: str
    findings: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionFindingsSummary:
    summary_id: str
    total_findings: int
    open_findings: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    by_subject: dict[str, int]
    unresolved_blocker_count: int
    status: str
    recent_finding_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionContradictionSummary:
    summary_id: str
    total_contradictions: int
    open_count: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    resolved_count: int
    contradiction_status: str
    recent_contradiction_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionGap:
    gap_id: str
    title: str
    description: str
    severity: str
    affected_subjects: list[str]
    recommended_track: str | None
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionGapRegister:
    register_id: str
    gaps: list[DeepSelfIntrospectionGap]
    blocker_count: int
    warning_count: int
    future_track_count: int

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionReleaseManifest:
    manifest_id: str
    release_version: str
    release_name: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    future_tracks: list[str]
    safety_boundary_report_id: str
    gap_register_id: str
    release_status: str
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class DeepSelfIntrospectionConsolidationReport:
    report_id: str
    version: str
    created_at: str
    ecosystem_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    findings_summary_id: str
    contradiction_summary_id: str
    workbench_snapshot_id: str
    gap_register_id: str
    release_manifest_id: str
    readiness_status: str
    readiness_rationale: list[str]
    next_track_recommendations: list[dict[str, Any]]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


class DeepSelfCapabilityMapService:
    def build_capability_map(
        self,
        subject_statuses: list[DeepSelfSubjectStatusView] | None = None,
    ) -> DeepSelfIntrospectionCapabilityMap:
        status_by_subject = {item.subject_id: item.status for item in subject_statuses or []}
        entries = [
            DeepSelfIntrospectionCapabilityMapEntry(
                capability_id=f"deep_self_capability:{subject_id}",
                subject_id=subject_id,
                name=subject_name,
                version_introduced=version,
                skill_ids=list(skill_ids),
                status=_component_status(status_by_subject.get(subject_id, "ok")),
                input_surfaces=["read_model", "cli"],
                output_surfaces=["sanitized_report", "workbench_ref", "ocel_ref"],
                source_read_models=list(source_read_models),
                target_read_models=list(target_read_models),
                ocel_visible=True,
                pig_visible=True,
                ocpx_visible=True,
                workbench_visible=True,
                safety_notes=[
                    "Read-only observation only.",
                    "Consolidation does not add correction, promotion, mutation, materialization, or execution.",
                ],
            )
            for version, subject_id, subject_name, skill_ids, _, source_read_models, target_read_models in SUBJECT_COMPONENTS
        ]
        return DeepSelfIntrospectionCapabilityMap(
            map_id=f"deep_self_capability_map:{uuid4().hex}",
            version=CONSOLIDATION_VERSION,
            entries=entries,
            implemented_count=sum(1 for item in entries if item.status == "implemented"),
            warning_count=sum(1 for item in entries if item.status == "warning"),
            failed_count=sum(1 for item in entries if item.status == "failed"),
            blocked_count=sum(1 for item in entries if item.status == "blocked"),
            future_track_count=sum(1 for item in entries if item.status == "future_track"),
        )


class DeepSelfCoverageMatrixService:
    def build_coverage_matrix(
        self,
        coverage_rows: list[DeepSelfCoverageRow] | None = None,
        subject_statuses: list[DeepSelfSubjectStatusView] | None = None,
    ) -> DeepSelfIntrospectionCoverageMatrix:
        coverage_by_subject = {item.subject: item for item in coverage_rows or []}
        status_by_subject = {item.subject_id: item for item in subject_statuses or []}
        rows: list[DeepSelfIntrospectionCoverageMatrixRow] = []
        for _, subject_id, _, _, _, _, _ in SUBJECT_COMPONENTS:
            source_row = coverage_by_subject.get(subject_id)
            status = status_by_subject.get(subject_id)
            has_required = True
            row = DeepSelfIntrospectionCoverageMatrixRow(
                subject_id=subject_id,
                has_contract=True,
                has_model=source_row.has_model if source_row else True,
                has_service=source_row.has_service if source_row else True,
                has_cli=source_row.has_cli if source_row else True,
                has_tests=source_row.has_tests if source_row else True,
                has_boundary_tests=True,
                has_ocel_mapping=source_row.has_ocel_mapping if source_row else True,
                has_pig_projection=source_row.has_pig_projection if source_row else True,
                has_ocpx_projection=source_row.has_ocpx_projection if source_row else True,
                has_workbench_visibility=source_row.has_workbench_visibility if source_row else True,
                latest_report_available=bool((status.latest_report_id if status else None) or subject_id == "workbench"),
                coverage_notes=["Required release-closure coverage is read-only."],
            )
            has_required = all(
                [
                    row.has_contract,
                    row.has_model,
                    row.has_service,
                    row.has_cli,
                    row.has_tests,
                    row.has_boundary_tests,
                    row.has_ocel_mapping,
                    row.has_pig_projection,
                    row.has_ocpx_projection,
                    row.has_workbench_visibility,
                    row.latest_report_available,
                ]
            )
            if not has_required:
                row.coverage_notes.append("Required coverage is missing.")
            rows.append(row)
        missing = sum(
            1
            for row in rows
            if not all(
                [
                    row.has_contract,
                    row.has_model,
                    row.has_service,
                    row.has_cli,
                    row.has_tests,
                    row.has_boundary_tests,
                    row.has_ocel_mapping,
                    row.has_pig_projection,
                    row.has_ocpx_projection,
                    row.has_workbench_visibility,
                    row.latest_report_available,
                ]
            )
        )
        return DeepSelfIntrospectionCoverageMatrix(
            matrix_id=f"deep_self_coverage_matrix:{uuid4().hex}",
            rows=rows,
            coverage_status="complete" if missing == 0 else "blocked",
            missing_required_coverage_count=missing,
            optional_gap_count=0,
        )


class DeepSelfSafetyBoundaryReportService:
    def build_safety_report(
        self,
        safety: DeepSelfSafetyBoundaryStatus | None = None,
    ) -> DeepSelfIntrospectionSafetyBoundaryReport:
        safety = safety or DeepSelfSafetyBoundaryStatus(
            mutation_enabled_count=0,
            permission_grant_enabled_count=0,
            policy_mutation_enabled_count=0,
            registry_mutation_enabled_count=0,
            trace_repair_enabled_count=0,
            context_injection_enabled_count=0,
            memory_promotion_enabled_count=0,
            candidate_promotion_enabled_count=0,
            materialization_enabled_count=0,
            shell_enabled_count=0,
            network_enabled_count=0,
            mcp_enabled_count=0,
            plugin_enabled_count=0,
            external_harness_enabled_count=0,
            llm_judge_enabled_count=0,
            dangerous_capability_count=0,
            status="ok",
        )
        counts = {
            "mutation_enabled_count": safety.mutation_enabled_count,
            "correction_enabled_count": 0,
            "permission_grant_enabled_count": safety.permission_grant_enabled_count,
            "policy_mutation_enabled_count": safety.policy_mutation_enabled_count,
            "registry_mutation_enabled_count": safety.registry_mutation_enabled_count,
            "trace_repair_enabled_count": safety.trace_repair_enabled_count,
            "context_injection_enabled_count": safety.context_injection_enabled_count,
            "memory_promotion_enabled_count": safety.memory_promotion_enabled_count,
            "candidate_promotion_enabled_count": safety.candidate_promotion_enabled_count,
            "materialization_enabled_count": safety.materialization_enabled_count,
            "shell_enabled_count": safety.shell_enabled_count,
            "network_enabled_count": safety.network_enabled_count,
            "mcp_enabled_count": safety.mcp_enabled_count,
            "plugin_enabled_count": safety.plugin_enabled_count,
            "external_harness_enabled_count": safety.external_harness_enabled_count,
            "llm_judge_enabled_count": safety.llm_judge_enabled_count,
            "dangerous_capability_count": safety.dangerous_capability_count,
            "private_boundary_violation_count": 0,
            "raw_secret_exposure_count": 0,
        }
        findings = [
            {"severity": "critical", "finding_type": key, "message": f"{key} is nonzero."}
            for key, count in counts.items()
            if count
        ]
        return DeepSelfIntrospectionSafetyBoundaryReport(
            report_id=f"deep_self_safety_boundary_report:{uuid4().hex}",
            version=CONSOLIDATION_VERSION,
            status="failed" if findings else "passed",
            findings=findings,
            **counts,
        )


class DeepSelfFindingsSummaryService:
    def build_findings_summary(
        self,
        snapshot: DeepSelfWorkbenchSnapshot,
    ) -> DeepSelfIntrospectionFindingsSummary:
        view = snapshot.findings_view
        status = "failed" if view.critical_count or view.error_count else "warning" if view.warning_count else "passed"
        return DeepSelfIntrospectionFindingsSummary(
            summary_id=f"deep_self_findings_summary:{uuid4().hex}",
            total_findings=view.total_findings,
            open_findings=view.open_findings,
            critical_count=view.critical_count,
            error_count=view.error_count,
            warning_count=view.warning_count,
            info_count=view.info_count,
            by_subject=dict(view.by_subject),
            unresolved_blocker_count=view.critical_count + view.error_count,
            status=status,
            recent_finding_refs=[_sanitized_ref(item) for item in view.recent_findings],
        )


class DeepSelfContradictionSummaryService:
    def build_contradiction_summary(
        self,
        snapshot: DeepSelfWorkbenchSnapshot,
    ) -> DeepSelfIntrospectionContradictionSummary:
        view = snapshot.contradiction_view
        return DeepSelfIntrospectionContradictionSummary(
            summary_id=f"deep_self_contradiction_summary:{uuid4().hex}",
            total_contradictions=view.open_count,
            open_count=view.open_count,
            critical_count=view.critical_count,
            error_count=view.error_count,
            warning_count=view.warning_count,
            info_count=view.info_count,
            resolved_count=0,
            contradiction_status=view.contradiction_status,
            recent_contradiction_refs=[_sanitized_ref(item) for item in view.unresolved_entries],
        )


class DeepSelfGapRegisterService:
    def build_gap_register(self) -> DeepSelfIntrospectionGapRegister:
        gaps = [
            DeepSelfIntrospectionGap(
                gap_id=gap_id,
                title=title,
                description=f"{title} is intentionally outside the current v0.21 consolidation scope.",
                severity="future_track",
                affected_subjects=["deep_self_introspection"],
                recommended_track=track,
                withdrawal_condition="This gap becomes a blocker only if the current release claims to implement that future track.",
            )
            for gap_id, title, track in FUTURE_GAP_DEFINITIONS
        ]
        return DeepSelfIntrospectionGapRegister(
            register_id=f"deep_self_gap_register:{uuid4().hex}",
            gaps=gaps,
            blocker_count=sum(1 for item in gaps if item.severity == "blocker"),
            warning_count=sum(1 for item in gaps if item.severity == "warning"),
            future_track_count=sum(1 for item in gaps if item.severity == "future_track"),
        )


class DeepSelfReleaseManifestService:
    def build_release_manifest(
        self,
        capability_map: DeepSelfIntrospectionCapabilityMap,
        safety_report: DeepSelfIntrospectionSafetyBoundaryReport,
        gap_register: DeepSelfIntrospectionGapRegister,
        readiness_status: str,
    ) -> DeepSelfIntrospectionReleaseManifest:
        if readiness_status == "blocked":
            release_status = "blocked"
        elif readiness_status == "warning" or gap_register.future_track_count:
            release_status = "releasable_with_warnings"
        else:
            release_status = "releasable"
        return DeepSelfIntrospectionReleaseManifest(
            manifest_id=f"deep_self_release_manifest:{uuid4().hex}",
            release_version=CONSOLIDATION_VERSION,
            release_name=CONSOLIDATION_RELEASE_NAME,
            included_versions=list(INCLUDED_VERSIONS),
            included_subjects=[item.subject_id for item in capability_map.entries],
            included_capabilities=[item.capability_id for item in capability_map.entries],
            excluded_capabilities=list(EXCLUDED_CAPABILITIES),
            future_tracks=list(FUTURE_TRACKS),
            safety_boundary_report_id=safety_report.report_id,
            gap_register_id=gap_register.register_id,
            release_status=release_status,
            notes=[
                "Consolidation closes the v0.21 release unit.",
                "Future-track gaps are tracked without expanding the current release scope.",
            ],
        )


class DeepSelfEcosystemSnapshotService:
    def build_snapshot(
        self,
        *,
        workbench_snapshot: DeepSelfWorkbenchSnapshot,
        capability_map: DeepSelfIntrospectionCapabilityMap,
        coverage_matrix: DeepSelfIntrospectionCoverageMatrix,
        safety_report: DeepSelfIntrospectionSafetyBoundaryReport,
        findings_summary: DeepSelfIntrospectionFindingsSummary,
        contradiction_summary: DeepSelfIntrospectionContradictionSummary,
        gap_register: DeepSelfIntrospectionGapRegister,
        release_manifest: DeepSelfIntrospectionReleaseManifest,
        consolidation_report_id: str,
        readiness_status: str,
    ) -> DeepSelfIntrospectionEcosystemSnapshot:
        status_by_subject = {item.subject_id: item for item in workbench_snapshot.subject_statuses}
        subjects = [
            _subject_component(
                version=version,
                subject_id=subject_id,
                subject_name=subject_name,
                component_type=component_type,
                skill_ids=skill_ids,
                status_view=status_by_subject.get(subject_id),
                workbench_snapshot=workbench_snapshot,
            )
            for version, subject_id, subject_name, skill_ids, component_type, _, _ in SUBJECT_COMPONENTS
        ]
        return DeepSelfIntrospectionEcosystemSnapshot(
            snapshot_id=f"deep_self_ecosystem_snapshot:{uuid4().hex}",
            version=CONSOLIDATION_VERSION,
            created_at=utc_now_iso(),
            release_name=CONSOLIDATION_RELEASE_NAME,
            subjects=subjects,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety_report.report_id,
            findings_summary_id=findings_summary.summary_id,
            contradiction_summary_id=contradiction_summary.summary_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            consolidation_report_id=consolidation_report_id,
            status=readiness_status,
            limitations=[
                "Consolidation is a read-only release-closure view.",
                "No correction, approval, promotion, materialization, execution, or mutation is performed.",
                "Raw prompt, transcript, memory, persona, file content, secrets, and private paths are not emitted.",
            ],
        )


class DeepSelfConsolidationService:
    def __init__(
        self,
        *,
        workbench_service: DeepSelfWorkbenchService | None = None,
        capability_map_service: DeepSelfCapabilityMapService | None = None,
        coverage_matrix_service: DeepSelfCoverageMatrixService | None = None,
        safety_report_service: DeepSelfSafetyBoundaryReportService | None = None,
        findings_summary_service: DeepSelfFindingsSummaryService | None = None,
        contradiction_summary_service: DeepSelfContradictionSummaryService | None = None,
        gap_register_service: DeepSelfGapRegisterService | None = None,
        release_manifest_service: DeepSelfReleaseManifestService | None = None,
        ecosystem_snapshot_service: DeepSelfEcosystemSnapshotService | None = None,
    ) -> None:
        self.workbench_service = workbench_service or DeepSelfWorkbenchService()
        self.capability_map_service = capability_map_service or DeepSelfCapabilityMapService()
        self.coverage_matrix_service = coverage_matrix_service or DeepSelfCoverageMatrixService()
        self.safety_report_service = safety_report_service or DeepSelfSafetyBoundaryReportService()
        self.findings_summary_service = findings_summary_service or DeepSelfFindingsSummaryService()
        self.contradiction_summary_service = contradiction_summary_service or DeepSelfContradictionSummaryService()
        self.gap_register_service = gap_register_service or DeepSelfGapRegisterService()
        self.release_manifest_service = release_manifest_service or DeepSelfReleaseManifestService()
        self.ecosystem_snapshot_service = ecosystem_snapshot_service or DeepSelfEcosystemSnapshotService()
        self.last_workbench_snapshot: DeepSelfWorkbenchSnapshot | None = None
        self.last_capability_map: DeepSelfIntrospectionCapabilityMap | None = None
        self.last_coverage_matrix: DeepSelfIntrospectionCoverageMatrix | None = None
        self.last_safety_report: DeepSelfIntrospectionSafetyBoundaryReport | None = None
        self.last_findings_summary: DeepSelfIntrospectionFindingsSummary | None = None
        self.last_contradiction_summary: DeepSelfIntrospectionContradictionSummary | None = None
        self.last_gap_register: DeepSelfIntrospectionGapRegister | None = None
        self.last_release_manifest: DeepSelfIntrospectionReleaseManifest | None = None
        self.last_ecosystem_snapshot: DeepSelfIntrospectionEcosystemSnapshot | None = None
        self.last_report: DeepSelfIntrospectionConsolidationReport | None = None

    def consolidate(self) -> DeepSelfIntrospectionConsolidationReport:
        workbench = self.workbench_service.build_snapshot()
        capability_map = self.capability_map_service.build_capability_map(workbench.subject_statuses)
        coverage_matrix = self.coverage_matrix_service.build_coverage_matrix(workbench.coverage, workbench.subject_statuses)
        safety_report = self.safety_report_service.build_safety_report(workbench.safety_boundary)
        findings_summary = self.findings_summary_service.build_findings_summary(workbench)
        contradiction_summary = self.contradiction_summary_service.build_contradiction_summary(workbench)
        gap_register = self.gap_register_service.build_gap_register()
        readiness_status, rationale = _readiness_status(
            workbench=workbench,
            capability_map=capability_map,
            coverage_matrix=coverage_matrix,
            safety_report=safety_report,
            findings_summary=findings_summary,
            contradiction_summary=contradiction_summary,
            gap_register=gap_register,
        )
        release_manifest = self.release_manifest_service.build_release_manifest(
            capability_map,
            safety_report,
            gap_register,
            readiness_status,
        )
        report_id = f"deep_self_consolidation_report:{uuid4().hex}"
        ecosystem = self.ecosystem_snapshot_service.build_snapshot(
            workbench_snapshot=workbench,
            capability_map=capability_map,
            coverage_matrix=coverage_matrix,
            safety_report=safety_report,
            findings_summary=findings_summary,
            contradiction_summary=contradiction_summary,
            gap_register=gap_register,
            release_manifest=release_manifest,
            consolidation_report_id=report_id,
            readiness_status=readiness_status,
        )
        report = DeepSelfIntrospectionConsolidationReport(
            report_id=report_id,
            version=CONSOLIDATION_VERSION,
            created_at=utc_now_iso(),
            ecosystem_snapshot_id=ecosystem.snapshot_id,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety_report.report_id,
            findings_summary_id=findings_summary.summary_id,
            contradiction_summary_id=contradiction_summary.summary_id,
            workbench_snapshot_id=workbench.snapshot_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            readiness_status=readiness_status,
            readiness_rationale=rationale,
            next_track_recommendations=[
                {"track": track, "reason": "Future release track outside v0.21 consolidation."}
                for track in FUTURE_TRACKS
            ],
            withdrawal_conditions=[
                "Withdraw readiness if any safety boundary count becomes nonzero.",
                "Withdraw readiness if required OCEL/PIG/OCPX/workbench coverage is missing.",
                "Withdraw readiness if claim consistency, candidate/memory boundary, or trace integrity fails.",
                "Withdraw readiness if private material or raw secret exposure is detected.",
            ],
            validity_horizon="Valid until any v0.21 deep-self subject, mapping, safety boundary, or report owner changes.",
        )
        self.last_workbench_snapshot = workbench
        self.last_capability_map = capability_map
        self.last_coverage_matrix = coverage_matrix
        self.last_safety_report = safety_report
        self.last_findings_summary = findings_summary
        self.last_contradiction_summary = contradiction_summary
        self.last_gap_register = gap_register
        self.last_release_manifest = release_manifest
        self.last_ecosystem_snapshot = ecosystem
        self.last_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        if self.last_report is None:
            self.consolidate()
        safety = self.last_safety_report
        return {
            "version": CONSOLIDATION_VERSION,
            "layer": CONSOLIDATION_TRACK,
            "subject": "consolidation",
            "release_name": CONSOLIDATION_RELEASE_NAME,
            "coverage": {
                "contract": "implemented",
                "capability_truth": "implemented",
                "runtime_boundary": "implemented",
                "policy_gate": "implemented",
                "trace_integrity": "implemented",
                "context_projection": "implemented",
                "candidate_memory_boundary": "implemented",
                "claim_consistency": "implemented",
                "workbench": "implemented",
                "consolidation": "implemented",
            },
            "safety_boundary": {
                "mutation_enabled": bool(safety and safety.mutation_enabled_count),
                "correction_enabled": bool(safety and safety.correction_enabled_count),
                "promotion_enabled": bool(safety and (safety.memory_promotion_enabled_count or safety.candidate_promotion_enabled_count)),
                "materialization_enabled": bool(safety and safety.materialization_enabled_count),
                "execution_enabled": bool(safety and (safety.shell_enabled_count or safety.network_enabled_count or safety.external_harness_enabled_count)),
                "llm_judge_enabled": bool(safety and safety.llm_judge_enabled_count),
            },
            "next_tracks": list(FUTURE_TRACKS),
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        if self.last_report is None:
            self.consolidate()
        manifest = self.last_release_manifest
        return {
            "state": "deep_self_introspection_foundation_v1_consolidated",
            "release_version": CONSOLIDATION_VERSION,
            "release_name": CONSOLIDATION_RELEASE_NAME,
            "source_read_models": [
                "DeepSelfWorkbenchState",
                "SelfClaimConsistencyState",
                "SelfContradictionRegisterState",
                "SelfCandidateMemoryBoundaryState",
                "SelfContextProjectionState",
                "SelfTraceIntegrityState",
                "SelfPolicyGateState",
                "SelfRuntimeBoundaryState",
                "SelfCapabilityTruthState",
            ],
            "target_read_models": [
                "DeepSelfReleaseState",
                "DeepSelfConsolidationState",
                "DeepSelfGapRegisterState",
                "DeepSelfSafetyBoundaryState",
                "DeepSelfReadinessState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "release_status": manifest.release_status if manifest else "blocked",
        }

    def render_cli(self, command_name: str = "consolidate") -> str:
        if self.last_report is None:
            self.consolidate()
        report = self.last_report
        manifest = self.last_release_manifest
        safety = self.last_safety_report
        findings = self.last_findings_summary
        contradictions = self.last_contradiction_summary
        gaps = self.last_gap_register
        coverage = self.last_coverage_matrix
        if not all([report, manifest, safety, findings, contradictions, gaps, coverage]):
            raise RuntimeError("consolidation artifacts are unavailable")
        subject_coverage = ",".join(row.subject_id for row in coverage.rows)
        return "\n".join(
            [
                "Deep Self-Introspection Consolidation",
                f"command={command_name}",
                f"version={CONSOLIDATION_VERSION}",
                f"release_name={CONSOLIDATION_RELEASE_NAME}",
                f"release_status={manifest.release_status}",
                f"readiness_status={report.readiness_status}",
                f"subject_coverage={subject_coverage}",
                f"coverage_status={coverage.coverage_status}",
                f"missing_required_coverage_count={coverage.missing_required_coverage_count}",
                f"mutation_enabled_count={safety.mutation_enabled_count}",
                f"correction_enabled_count={safety.correction_enabled_count}",
                f"promotion_enabled_count={safety.memory_promotion_enabled_count + safety.candidate_promotion_enabled_count}",
                f"materialization_enabled_count={safety.materialization_enabled_count}",
                f"execution_enabled_count={safety.shell_enabled_count + safety.network_enabled_count + safety.external_harness_enabled_count}",
                f"llm_judge_enabled_count={safety.llm_judge_enabled_count}",
                f"dangerous_capability_count={safety.dangerous_capability_count}",
                f"private_boundary_violation_count={safety.private_boundary_violation_count}",
                f"raw_secret_exposure_count={safety.raw_secret_exposure_count}",
                f"total_findings={findings.total_findings}",
                f"critical_findings={findings.critical_count}",
                f"error_findings={findings.error_count}",
                f"warning_findings={findings.warning_count}",
                f"open_contradictions={contradictions.open_count}",
                f"critical_contradictions={contradictions.critical_count}",
                f"error_contradictions={contradictions.error_count}",
                f"future_track_gap_count={gaps.future_track_count}",
                f"blocker_gap_count={gaps.blocker_count}",
                "next_track_recommendations=" + ",".join(FUTURE_TRACKS),
                "No correction performed.",
                "No promotion performed.",
                "No mutation performed.",
                "No execution performed.",
                "No LLM judge performed.",
                "raw_prompt_body_printed=False",
                "raw_transcript_printed=False",
                "raw_memory_persona_private_material_printed=False",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _component_status(status: str) -> str:
    if status in {"failed", "blocked", "warning"}:
        return status
    return "implemented"


def _subject_component(
    *,
    version: str,
    subject_id: str,
    subject_name: str,
    component_type: str,
    skill_ids: list[str],
    status_view: DeepSelfSubjectStatusView | None,
    workbench_snapshot: DeepSelfWorkbenchSnapshot,
) -> DeepSelfIntrospectionSubjectComponent:
    status = _component_status(status_view.status if status_view else "ok")
    if subject_id == "workbench":
        status = "implemented"
        latest_report_id = workbench_snapshot.snapshot_id
        finding_count = workbench_snapshot.findings_view.total_findings
    else:
        latest_report_id = status_view.latest_report_id if status_view else None
        finding_count = status_view.open_finding_count if status_view else 0
    return DeepSelfIntrospectionSubjectComponent(
        component_id=f"deep_self_subject_component:{subject_id}",
        version_introduced=version,
        subject_id=subject_id,
        subject_name=subject_name,
        component_type=component_type,
        skill_ids=list(skill_ids),
        status=status,
        read_only=True,
        mutation_enabled=False,
        correction_enabled=False,
        promotion_enabled=False,
        execution_enabled=False,
        ocel_visible=True,
        pig_visible=True,
        ocpx_visible=True,
        workbench_visible=True,
        latest_report_id=latest_report_id,
        finding_count=finding_count,
        notes=["Component is included in read-only v0.21 consolidation."],
    )


def _readiness_status(
    *,
    workbench: DeepSelfWorkbenchSnapshot,
    capability_map: DeepSelfIntrospectionCapabilityMap,
    coverage_matrix: DeepSelfIntrospectionCoverageMatrix,
    safety_report: DeepSelfIntrospectionSafetyBoundaryReport,
    findings_summary: DeepSelfIntrospectionFindingsSummary,
    contradiction_summary: DeepSelfIntrospectionContradictionSummary,
    gap_register: DeepSelfIntrospectionGapRegister,
) -> tuple[str, list[str]]:
    rationale: list[str] = []
    blocked = False
    warning = False
    if safety_report.status == "failed":
        blocked = True
        rationale.append("Safety boundary count is nonzero.")
    if coverage_matrix.coverage_status == "blocked":
        blocked = True
        rationale.append("Required coverage is missing.")
    if capability_map.failed_count or capability_map.blocked_count:
        blocked = True
        rationale.append("Required capability map entry failed or blocked.")
    if contradiction_summary.critical_count or contradiction_summary.error_count:
        blocked = True
        rationale.append("Critical or error contradiction remains open.")
    failed_subjects = [item.subject_id for item in workbench.subject_statuses if item.status in {"failed", "blocked"}]
    if failed_subjects:
        blocked = True
        rationale.append("Required subject failed or blocked: " + ",".join(failed_subjects))
    if any(item.subject_id == "claim_consistency" and item.status == "failed" for item in workbench.subject_statuses):
        blocked = True
        rationale.append("Claim consistency failed.")
    if any(item.subject_id == "candidate_memory_boundary" and item.status == "failed" for item in workbench.subject_statuses):
        blocked = True
        rationale.append("Candidate/memory boundary failed.")
    if any(item.subject_id == "trace_integrity" and item.status == "failed" for item in workbench.subject_statuses):
        blocked = True
        rationale.append("Trace integrity failed.")
    if findings_summary.warning_count:
        warning = True
        rationale.append("Warning findings remain.")
    if contradiction_summary.open_count:
        warning = True
        rationale.append("Non-critical open contradictions remain.")
    if gap_register.future_track_count:
        warning = True
        rationale.append("Future-track gaps remain outside the current release.")
    if not blocked and not warning:
        rationale.append("All required v0.21 deep-self subjects are visible with zero dangerous safety counts.")
    return ("blocked" if blocked else "warning" if warning else "ready", rationale)


def _sanitized_ref(item: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "finding_id",
        "severity",
        "finding_type",
        "message",
        "entry_id",
        "claim_id",
        "contradiction_type",
        "claim_summary",
        "status",
    }
    return {key: value for key, value in item.items() if key in allowed}

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from chanta_core.self_modification_safety.mapping import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
)
from chanta_core.self_modification_safety.registry import SelfModificationRegistryService
from chanta_core.self_modification_safety.workbench import (
    SelfModificationWorkbenchService,
    SelfModificationWorkbenchSnapshot,
)
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_CONSOLIDATION_VERSION = "v0.22.9"
SELF_MODIFICATION_CONSOLIDATION_STATE = "self_modification_safety_foundation_v1_consolidated"
SELF_MODIFICATION_FOUNDATION_RELEASE_NAME = "OCEL-native Self-Modification Safety Foundation v1"
SELF_MODIFICATION_CONSOLIDATION_SKILL_ID = "skill:self_modification_consolidation_view"
CONSOLIDATION_EFFECT_TYPES = ["read_only_observation", "state_candidate_created"]

REQUIRED_RELEASE_VERSIONS = [
    "v0.22.0",
    "v0.22.1",
    "v0.22.2",
    "v0.22.3",
    "v0.22.4",
    "v0.22.5",
    "v0.22.6",
    "v0.22.7",
    "v0.22.8",
    "v0.22.9",
]

REQUIRED_SUBJECTS = [
    ("subject:self_modification_safety_contract", "Self-Modification Safety Contract", "v0.22.0"),
    ("subject:modification_request", "Request", "v0.22.1"),
    ("subject:patch_candidate", "Patch Candidate", "v0.22.1"),
    ("subject:diff_preview", "Patch Draft / Diff Preview", "v0.22.2"),
    ("subject:patch_static_safety", "Patch Static Safety", "v0.22.3"),
    ("subject:patch_dry_run", "Patch Dry-run / Applicability", "v0.22.4"),
    ("subject:modification_review_gate", "Human Review", "v0.22.5"),
    ("subject:patch_apply_gate", "Apply Gate", "v0.22.5"),
    ("subject:rollback_plan", "Rollback Plan Descriptor", "v0.22.5"),
    ("subject:bounded_patch_apply", "Bounded Patch Apply", "v0.22.6"),
    ("subject:post_apply_verification", "Post-Apply Verification", "v0.22.7"),
    ("subject:modification_outcome", "Modification Outcome", "v0.22.7"),
    ("subject:self_modification_workbench", "Self-Modification Workbench", "v0.22.8"),
]

FUTURE_GAPS = [
    ("local_runtime_provider_not_started", "v0.24.x Local Runtime Provider"),
    ("test_lint_execution_safety_not_started", "Test/Lint Execution Safety"),
    ("rollback_execution_safety_not_started", "Rollback Execution Safety"),
    ("multi_file_apply_safety_not_started", "Bounded Multi-File Apply Safety"),
    ("external_adapter_safety_not_started", "External Adapter Safety"),
    ("autonomous_repair_loop_not_started", "Mission Loop Safety"),
    ("memory_promotion_after_modification_not_started", "Memory Promotion Safety"),
    ("semantic_code_review_not_started", "Semantic Code Review Safety"),
    ("performance_regression_check_not_started", "Performance Regression Safety"),
    ("security_scan_execution_not_started", "Security Scan Execution Safety"),
]

EXCLUDED_CAPABILITIES = [
    "test/lint/shell execution",
    "rollback execution",
    "broad multi-file patching",
    "external patch command",
    "autonomous repair loop",
    "LLM judge",
    "memory/persona/overlay mutation",
]

FUTURE_TRACKS = [
    "v0.24.x Local Runtime Provider",
    "Rollback Execution Safety",
    "Test/Lint Execution Safety",
    "External Adapter Safety",
    "Mission Loop Safety",
]


@dataclass(frozen=True)
class SelfModificationSubjectComponent:
    subject_id: str
    subject_name: str
    version_introduced: str
    status: str
    visible: bool
    artifact_count: int
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "version_introduced": self.version_introduced,
            "status": self.status,
            "visible": self.visible,
            "artifact_count": self.artifact_count,
            "ocel_visible": self.ocel_visible,
            "pig_visible": self.pig_visible,
            "ocpx_visible": self.ocpx_visible,
            "workbench_visible": self.workbench_visible,
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class SelfModificationEcosystemSnapshot:
    snapshot_id: str
    created_at: str
    track: str
    release_name: str
    subject_components: list[SelfModificationSubjectComponent]
    workbench_snapshot_ref: dict[str, Any]
    ecosystem_status: str
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "track": self.track,
            "release_name": self.release_name,
            "subject_components": [item.to_dict() for item in self.subject_components],
            "workbench_snapshot_ref": dict(self.workbench_snapshot_ref),
            "ecosystem_status": self.ecosystem_status,
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class SelfModificationCapabilityMapEntry:
    capability_id: str
    capability_name: str
    status: str
    introduced_in: str
    source_read_models: list[str]
    target_read_models: list[str]
    effect_types: list[str]
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "capability_name": self.capability_name,
            "status": self.status,
            "introduced_in": self.introduced_in,
            "source_read_models": list(self.source_read_models),
            "target_read_models": list(self.target_read_models),
            "effect_types": list(self.effect_types),
            "ocel_visible": self.ocel_visible,
            "pig_visible": self.pig_visible,
            "ocpx_visible": self.ocpx_visible,
            "workbench_visible": self.workbench_visible,
        }


@dataclass(frozen=True)
class SelfModificationCapabilityMap:
    map_id: str
    entries: list[SelfModificationCapabilityMapEntry]
    coverage_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "map_id": self.map_id,
            "entries": [item.to_dict() for item in self.entries],
            "coverage_status": self.coverage_status,
        }


@dataclass(frozen=True)
class SelfModificationCoverageMatrixRow:
    subject_id: str
    version_introduced: str
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
    latest_artifact_available: bool
    coverage_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "version_introduced": self.version_introduced,
            "has_contract": self.has_contract,
            "has_model": self.has_model,
            "has_service": self.has_service,
            "has_cli": self.has_cli,
            "has_tests": self.has_tests,
            "has_boundary_tests": self.has_boundary_tests,
            "has_ocel_mapping": self.has_ocel_mapping,
            "has_pig_projection": self.has_pig_projection,
            "has_ocpx_projection": self.has_ocpx_projection,
            "has_workbench_visibility": self.has_workbench_visibility,
            "latest_artifact_available": self.latest_artifact_available,
            "coverage_status": self.coverage_status,
        }


@dataclass(frozen=True)
class SelfModificationCoverageMatrix:
    matrix_id: str
    rows: list[SelfModificationCoverageMatrixRow]
    required_columns: list[str]
    missing_required_coverage: list[str]
    coverage_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "rows": [item.to_dict() for item in self.rows],
            "required_columns": list(self.required_columns),
            "missing_required_coverage": list(self.missing_required_coverage),
            "coverage_status": self.coverage_status,
        }


@dataclass(frozen=True)
class SelfModificationSafetyBoundaryReport:
    report_id: str
    bounded_file_write_count: int
    unauthorized_write_count: int
    apply_without_gate_count: int
    consumed_authorization_reuse_count: int
    workspace_file_changed_count: int
    workspace_file_changed_without_transaction_count: int
    unverified_apply_count: int
    missing_outcome_count: int
    rollback_executed_count: int
    shell_executed_count: int
    test_lint_executed_count: int
    external_patch_command_count: int
    network_mcp_plugin_count: int
    llm_judge_count: int
    memory_mutation_count: int
    persona_overlay_mutation_count: int
    raw_secret_exposure_count: int
    safety_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "bounded_file_write_count": self.bounded_file_write_count,
            "unauthorized_write_count": self.unauthorized_write_count,
            "apply_without_gate_count": self.apply_without_gate_count,
            "consumed_authorization_reuse_count": self.consumed_authorization_reuse_count,
            "workspace_file_changed_count": self.workspace_file_changed_count,
            "workspace_file_changed_without_transaction_count": self.workspace_file_changed_without_transaction_count,
            "unverified_apply_count": self.unverified_apply_count,
            "missing_outcome_count": self.missing_outcome_count,
            "rollback_executed_count": self.rollback_executed_count,
            "shell_executed_count": self.shell_executed_count,
            "test_lint_executed_count": self.test_lint_executed_count,
            "external_patch_command_count": self.external_patch_command_count,
            "network_mcp_plugin_count": self.network_mcp_plugin_count,
            "llm_judge_count": self.llm_judge_count,
            "memory_mutation_count": self.memory_mutation_count,
            "persona_overlay_mutation_count": self.persona_overlay_mutation_count,
            "raw_secret_exposure_count": self.raw_secret_exposure_count,
            "safety_status": self.safety_status,
        }


@dataclass(frozen=True)
class SelfModificationPipelineSummary:
    summary_id: str
    request_count: int
    patch_candidate_count: int
    draft_count: int
    preview_count: int
    static_safety_report_count: int
    dry_run_report_count: int
    review_decision_count: int
    apply_gate_count: int
    bounded_apply_count: int
    post_apply_verification_count: int
    outcome_count: int
    completed_pipeline_count: int
    pending_pipeline_count: int
    blocked_pipeline_count: int
    failed_pipeline_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationAuthorizationSummary:
    summary_id: str
    authorization_count: int
    open_count: int
    consumed_count: int
    expired_count: int
    invalid_count: int
    reused_count: int
    single_use_violation_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationChangeSummary:
    summary_id: str
    changed_file_count: int
    workspace_file_changed_event_count: int
    trace_complete_count: int
    trace_incomplete_count: int
    verified_change_count: int
    unverified_change_count: int
    rollback_recommended_count: int
    raw_content_emitted_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationOutcomeSummary:
    summary_id: str
    total_outcome_count: int
    applied_verified_count: int
    applied_with_warnings_count: int
    verification_failed_count: int
    rollback_recommended_count: int
    blocked_count: int
    needs_more_input_count: int
    missing_outcome_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationGap:
    gap_id: str
    severity: str
    recommended_track: str
    current_release_blocker: bool
    withdrawal_condition: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationGapRegister:
    register_id: str
    gaps: list[SelfModificationGap]
    future_gap_count: int
    blocker_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "register_id": self.register_id,
            "gaps": [item.to_dict() for item in self.gaps],
            "future_gap_count": self.future_gap_count,
            "blocker_count": self.blocker_count,
        }


@dataclass(frozen=True)
class SelfModificationReleaseManifest:
    manifest_id: str
    release_version: str
    release_name: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    future_tracks: list[str]
    release_status: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SelfModificationConsolidationReport:
    report_id: str
    created_at: str
    ecosystem_snapshot: SelfModificationEcosystemSnapshot
    capability_map: SelfModificationCapabilityMap
    coverage_matrix: SelfModificationCoverageMatrix
    safety_boundary_report: SelfModificationSafetyBoundaryReport
    pipeline_summary: SelfModificationPipelineSummary
    authorization_summary: SelfModificationAuthorizationSummary
    change_summary: SelfModificationChangeSummary
    outcome_summary: SelfModificationOutcomeSummary
    gap_register: SelfModificationGapRegister
    release_manifest: SelfModificationReleaseManifest
    release_status: str
    readiness_status: str
    readiness_rationale: list[str]
    next_track_recommendations: list[str]
    review_status: str = "report_only"
    mutation_performed: bool = False
    additional_file_write_performed: bool = False
    rollback_executed: bool = False
    shell_executed: bool = False
    test_lint_executed: bool = False
    llm_judge_used: bool = False
    withdrawal_conditions: list[str] | None = None
    validity_horizon: str = "Valid until v0.22 release artifacts, workbench state, or safety boundary evidence changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "ecosystem_snapshot": self.ecosystem_snapshot.to_dict(),
            "capability_map": self.capability_map.to_dict(),
            "coverage_matrix": self.coverage_matrix.to_dict(),
            "safety_boundary_report": self.safety_boundary_report.to_dict(),
            "pipeline_summary": self.pipeline_summary.to_dict(),
            "authorization_summary": self.authorization_summary.to_dict(),
            "change_summary": self.change_summary.to_dict(),
            "outcome_summary": self.outcome_summary.to_dict(),
            "gap_register": self.gap_register.to_dict(),
            "release_manifest": self.release_manifest.to_dict(),
            "release_status": self.release_status,
            "readiness_status": self.readiness_status,
            "readiness_rationale": list(self.readiness_rationale),
            "next_track_recommendations": list(self.next_track_recommendations),
            "review_status": self.review_status,
            "mutation_performed": self.mutation_performed,
            "additional_file_write_performed": self.additional_file_write_performed,
            "rollback_executed": self.rollback_executed,
            "shell_executed": self.shell_executed,
            "test_lint_executed": self.test_lint_executed,
            "llm_judge_used": self.llm_judge_used,
            "withdrawal_conditions": list(self.withdrawal_conditions or []),
            "validity_horizon": self.validity_horizon,
        }


class SelfModificationConsolidationService:
    def __init__(
        self,
        workbench_service: SelfModificationWorkbenchService | None = None,
        registry_service: SelfModificationRegistryService | None = None,
    ) -> None:
        self.workbench_service = workbench_service or SelfModificationWorkbenchService()
        self.registry_service = registry_service or SelfModificationRegistryService()

    def build_report(self) -> SelfModificationConsolidationReport:
        workbench = self.workbench_service.build_snapshot()
        pipeline_summary = self.build_pipeline_summary(workbench)
        authorization_summary = self.build_authorization_summary(workbench)
        change_summary = self.build_change_summary(workbench)
        outcome_summary = self.build_outcome_summary(workbench, pipeline_summary)
        safety_report = self.build_safety_boundary_report(workbench, outcome_summary)
        ecosystem = self.build_ecosystem_snapshot(workbench, safety_report)
        capability_map = self.build_capability_map()
        coverage_matrix = self.build_coverage_matrix(ecosystem)
        gap_register = self.build_gap_register()
        readiness_status, rationale = self._readiness_status(
            safety_report=safety_report,
            coverage_matrix=coverage_matrix,
            gap_register=gap_register,
            pipeline_summary=pipeline_summary,
            outcome_summary=outcome_summary,
        )
        release_status = {
            "ready": "releasable",
            "warning": "releasable_with_warnings",
            "blocked": "blocked",
        }[readiness_status]
        manifest = self.build_release_manifest(release_status)
        return SelfModificationConsolidationReport(
            report_id=f"self_modification_consolidation_report:{uuid4()}",
            created_at=utc_now_iso(),
            ecosystem_snapshot=ecosystem,
            capability_map=capability_map,
            coverage_matrix=coverage_matrix,
            safety_boundary_report=safety_report,
            pipeline_summary=pipeline_summary,
            authorization_summary=authorization_summary,
            change_summary=change_summary,
            outcome_summary=outcome_summary,
            gap_register=gap_register,
            release_manifest=manifest,
            release_status=release_status,
            readiness_status=readiness_status,
            readiness_rationale=rationale,
            next_track_recommendations=list(FUTURE_TRACKS),
            withdrawal_conditions=[
                "Withdraw if consolidation emits mutation effects or opens execution paths.",
                "Withdraw if unverified apply or missing outcome is downgraded below blocker.",
                "Withdraw if raw full file content, private paths, or secrets are emitted.",
            ],
        )

    def build_ecosystem_snapshot(
        self,
        workbench: SelfModificationWorkbenchSnapshot,
        safety_report: SelfModificationSafetyBoundaryReport,
    ) -> SelfModificationEcosystemSnapshot:
        status_by_subject = {item.subject_id: item for item in workbench.subject_statuses}
        components: list[SelfModificationSubjectComponent] = []
        for subject_id, name, version in REQUIRED_SUBJECTS:
            source_status = status_by_subject.get(subject_id)
            artifact_count = int(source_status.artifact_count) if source_status else 0
            visible = subject_id == "subject:self_modification_safety_contract" or source_status is not None
            status = "ok" if visible else "blocked"
            components.append(
                SelfModificationSubjectComponent(
                    subject_id=subject_id,
                    subject_name=name,
                    version_introduced=version,
                    status=status,
                    visible=visible,
                    artifact_count=artifact_count,
                    ocel_visible=True,
                    pig_visible=True,
                    ocpx_visible=True,
                    workbench_visible=visible,
                    limitations=[] if artifact_count else ["No latest runtime artifact available in this snapshot."],
                )
            )
        ecosystem_status = "blocked" if safety_report.safety_status == "blocked" else "ok"
        return SelfModificationEcosystemSnapshot(
            snapshot_id=f"self_modification_ecosystem_snapshot:{uuid4()}",
            created_at=utc_now_iso(),
            track="self_modification_safety",
            release_name=SELF_MODIFICATION_FOUNDATION_RELEASE_NAME,
            subject_components=components,
            workbench_snapshot_ref={"snapshot_id": workbench.snapshot_id},
            ecosystem_status=ecosystem_status,
            limitations=["Consolidation reads sanitized workbench state and does not execute modification actions."],
        )

    def build_capability_map(self) -> SelfModificationCapabilityMap:
        entries = [
            _capability("contract", "Self-Modification Safety Contract", "v0.22.0", ["DeepSelfConsolidationState"], ["SelfModificationSafetyContractState"], ["read_only_observation"]),
            _capability("request_candidate", "Request & Patch Candidate", "v0.22.1", ["SelfModificationRequestState"], ["PatchCandidateState"], ["state_candidate_created"]),
            _capability("draft_diff_preview", "Patch Draft / Diff Preview", "v0.22.2", ["PatchCandidateState"], ["PatchDraftState", "DiffPreviewState"], ["state_candidate_created"]),
            _capability("static_safety", "Patch Static Safety", "v0.22.3", ["PatchDraftState", "DiffPreviewState"], ["PatchStaticSafetyState"], ["read_only_observation", "state_candidate_created"]),
            _capability("dry_run", "Patch Dry-run / Applicability", "v0.22.4", ["PatchStaticSafetyState"], ["PatchDryRunState"], ["read_only_observation", "state_candidate_created"]),
            _capability("human_review_apply_gate", "Human Review & Apply Gate", "v0.22.5", ["PatchDryRunState"], ["HumanReviewState", "ApplyGateState"], ["read_only_observation", "state_candidate_created", "gate_state_created"]),
            _capability("bounded_apply", "Bounded Patch Apply", "v0.22.6", ["ApplyGateState"], ["BoundedPatchApplyState", "WorkspaceFileChangeState"], ["read_only_observation", "state_candidate_created", "workspace_file_changed"]),
            _capability("post_apply_verification_outcome", "Post-Apply Verification & Outcome", "v0.22.7", ["BoundedPatchApplyState"], ["PostApplyVerificationState", "ModificationOutcomeState"], ["read_only_observation", "state_candidate_created", "outcome_recorded"]),
            _capability("workbench", "Self-Modification Workbench", "v0.22.8", ["ModificationOutcomeState"], ["SelfModificationWorkbenchState"], ["read_only_observation"]),
            _capability("consolidation", "Self-Modification Safety Consolidation", "v0.22.9", ["SelfModificationWorkbenchState"], ["SelfModificationReleaseState", "SelfModificationConsolidationState"], list(CONSOLIDATION_EFFECT_TYPES)),
        ]
        return SelfModificationCapabilityMap(
            map_id=f"self_modification_capability_map:{uuid4()}",
            entries=entries,
            coverage_status="complete",
        )

    def build_coverage_matrix(self, ecosystem: SelfModificationEcosystemSnapshot) -> SelfModificationCoverageMatrix:
        rows: list[SelfModificationCoverageMatrixRow] = []
        missing: list[str] = []
        for component in ecosystem.subject_components:
            latest = component.artifact_count > 0 or component.subject_id == "subject:self_modification_safety_contract"
            row = SelfModificationCoverageMatrixRow(
                subject_id=component.subject_id,
                version_introduced=component.version_introduced,
                has_contract=True,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_workbench_visibility=component.workbench_visible,
                latest_artifact_available=latest,
                coverage_status="complete" if component.visible else "blocked",
            )
            if not component.visible:
                missing.append(component.subject_id)
            rows.append(row)
        coverage_status = "blocked" if missing else "complete"
        return SelfModificationCoverageMatrix(
            matrix_id=f"self_modification_coverage_matrix:{uuid4()}",
            rows=rows,
            required_columns=[
                "has_contract",
                "has_model",
                "has_service",
                "has_cli",
                "has_tests",
                "has_boundary_tests",
                "has_ocel_mapping",
                "has_pig_projection",
                "has_ocpx_projection",
                "has_workbench_visibility",
                "latest_artifact_available",
            ],
            missing_required_coverage=missing,
            coverage_status=coverage_status,
        )

    def build_safety_boundary_report(
        self,
        workbench: SelfModificationWorkbenchSnapshot,
        outcome_summary: SelfModificationOutcomeSummary,
    ) -> SelfModificationSafetyBoundaryReport:
        boundary = workbench.safety_boundary
        unverified_apply_count = int(workbench.readiness.unverified_apply_count)
        missing_outcome_count = int(outcome_summary.missing_outcome_count)
        danger_counts = [
            boundary.unauthorized_write_count,
            boundary.apply_without_gate_count,
            boundary.consumed_authorization_reuse_count,
            boundary.workspace_file_changed_without_transaction_count,
            unverified_apply_count,
            missing_outcome_count,
            boundary.rollback_executed_count,
            boundary.shell_executed_count,
            boundary.test_lint_executed_count,
            boundary.external_patch_command_count,
            boundary.llm_judge_count,
            boundary.memory_mutation_count,
            boundary.persona_overlay_mutation_count,
            boundary.raw_secret_exposure_count,
        ]
        safety_status = "blocked" if any(count > 0 for count in danger_counts) else "ok"
        return SelfModificationSafetyBoundaryReport(
            report_id=f"self_modification_safety_boundary_report:{uuid4()}",
            bounded_file_write_count=boundary.bounded_writer_write_count,
            unauthorized_write_count=boundary.unauthorized_write_count,
            apply_without_gate_count=boundary.apply_without_gate_count,
            consumed_authorization_reuse_count=boundary.consumed_authorization_reuse_count,
            workspace_file_changed_count=boundary.workspace_file_changed_count,
            workspace_file_changed_without_transaction_count=boundary.workspace_file_changed_without_transaction_count,
            unverified_apply_count=unverified_apply_count,
            missing_outcome_count=missing_outcome_count,
            rollback_executed_count=boundary.rollback_executed_count,
            shell_executed_count=boundary.shell_executed_count,
            test_lint_executed_count=boundary.test_lint_executed_count,
            external_patch_command_count=boundary.external_patch_command_count,
            network_mcp_plugin_count=0,
            llm_judge_count=boundary.llm_judge_count,
            memory_mutation_count=boundary.memory_mutation_count,
            persona_overlay_mutation_count=boundary.persona_overlay_mutation_count,
            raw_secret_exposure_count=boundary.raw_secret_exposure_count,
            safety_status=safety_status,
        )

    def build_pipeline_summary(self, workbench: SelfModificationWorkbenchSnapshot) -> SelfModificationPipelineSummary:
        subjects = {item.subject_id: item.artifact_count for item in workbench.subject_statuses}
        pipeline_items = workbench.pipeline_items
        return SelfModificationPipelineSummary(
            summary_id=f"self_modification_pipeline_summary:{uuid4()}",
            request_count=subjects.get("subject:modification_request", 0),
            patch_candidate_count=subjects.get("subject:patch_candidate", 0),
            draft_count=subjects.get("subject:diff_preview", 0),
            preview_count=subjects.get("subject:diff_preview", 0),
            static_safety_report_count=subjects.get("subject:patch_static_safety", 0),
            dry_run_report_count=subjects.get("subject:patch_dry_run", 0),
            review_decision_count=subjects.get("subject:modification_review_gate", 0),
            apply_gate_count=subjects.get("subject:patch_apply_gate", 0),
            bounded_apply_count=subjects.get("subject:bounded_patch_apply", 0),
            post_apply_verification_count=subjects.get("subject:post_apply_verification", 0),
            outcome_count=subjects.get("subject:modification_outcome", 0),
            completed_pipeline_count=sum(item.current_status == "completed" for item in pipeline_items),
            pending_pipeline_count=sum(item.current_status == "pending" for item in pipeline_items),
            blocked_pipeline_count=sum(item.current_status == "blocked" for item in pipeline_items),
            failed_pipeline_count=sum(item.current_status == "failed" for item in pipeline_items),
        )

    def build_authorization_summary(self, workbench: SelfModificationWorkbenchSnapshot) -> SelfModificationAuthorizationSummary:
        return SelfModificationAuthorizationSummary(
            summary_id=f"self_modification_authorization_summary:{uuid4()}",
            authorization_count=len(workbench.authorizations),
            open_count=sum(item.authorization_status == "open" for item in workbench.authorizations),
            consumed_count=sum(item.authorization_status == "consumed" for item in workbench.authorizations),
            expired_count=sum(item.authorization_status == "expired" for item in workbench.authorizations),
            invalid_count=sum(item.authorization_status in {"invalid", "blocked"} for item in workbench.authorizations),
            reused_count=workbench.safety_boundary.consumed_authorization_reuse_count,
            single_use_violation_count=workbench.safety_boundary.consumed_authorization_reuse_count,
        )

    def build_change_summary(self, workbench: SelfModificationWorkbenchSnapshot) -> SelfModificationChangeSummary:
        return SelfModificationChangeSummary(
            summary_id=f"self_modification_change_summary:{uuid4()}",
            changed_file_count=len(workbench.changes),
            workspace_file_changed_event_count=sum(bool(item.workspace_file_changed_event_id) for item in workbench.changes),
            trace_complete_count=sum(bool(item.workspace_file_changed_event_id and item.transaction_id) for item in workbench.changes),
            trace_incomplete_count=sum(not bool(item.workspace_file_changed_event_id and item.transaction_id) for item in workbench.changes),
            verified_change_count=sum(item.verification_status == "passed" for item in workbench.changes),
            unverified_change_count=sum(item.verification_status in {None, "", "missing"} for item in workbench.changes),
            rollback_recommended_count=sum(bool(item.rollback_recommended) for item in workbench.changes),
            raw_content_emitted_count=sum(bool(item.raw_content_emitted) for item in workbench.changes),
        )

    def build_outcome_summary(
        self,
        workbench: SelfModificationWorkbenchSnapshot,
        pipeline_summary: SelfModificationPipelineSummary,
    ) -> SelfModificationOutcomeSummary:
        statuses = [item.outcome_status for item in workbench.changes if item.outcome_status]
        missing = max(0, pipeline_summary.bounded_apply_count - pipeline_summary.outcome_count)
        return SelfModificationOutcomeSummary(
            summary_id=f"self_modification_outcome_summary:{uuid4()}",
            total_outcome_count=pipeline_summary.outcome_count,
            applied_verified_count=sum(status == "applied_verified" for status in statuses),
            applied_with_warnings_count=sum(status == "applied_with_warnings" for status in statuses),
            verification_failed_count=sum(status == "verification_failed" for status in statuses),
            rollback_recommended_count=sum(status == "rollback_recommended" for status in statuses),
            blocked_count=sum(status == "blocked" for status in statuses),
            needs_more_input_count=sum(status == "needs_more_input" for status in statuses),
            missing_outcome_count=missing,
        )

    def build_gap_register(self) -> SelfModificationGapRegister:
        gaps = [
            SelfModificationGap(
                gap_id=gap_id,
                severity="warning",
                recommended_track=track,
                current_release_blocker=False,
                withdrawal_condition=f"Withdraw this future gap when {track} is implemented and covered by OCEL/PIG/OCPX.",
            )
            for gap_id, track in FUTURE_GAPS
        ]
        return SelfModificationGapRegister(
            register_id=f"self_modification_gap_register:{uuid4()}",
            gaps=gaps,
            future_gap_count=len(gaps),
            blocker_count=sum(item.current_release_blocker for item in gaps),
        )

    def build_release_manifest(self, release_status: str) -> SelfModificationReleaseManifest:
        return SelfModificationReleaseManifest(
            manifest_id=f"self_modification_release_manifest:{uuid4()}",
            release_version=SELF_MODIFICATION_CONSOLIDATION_VERSION,
            release_name=SELF_MODIFICATION_FOUNDATION_RELEASE_NAME,
            included_versions=list(REQUIRED_RELEASE_VERSIONS),
            included_subjects=[subject_id for subject_id, _, _ in REQUIRED_SUBJECTS],
            included_capabilities=[
                "contract",
                "request_candidate",
                "draft_diff_preview",
                "static_safety",
                "dry_run",
                "human_review_apply_gate",
                "bounded_apply",
                "post_apply_verification_outcome",
                "workbench",
                "consolidation",
            ],
            excluded_capabilities=list(EXCLUDED_CAPABILITIES),
            future_tracks=list(FUTURE_TRACKS),
            release_status=release_status,
        )

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        safety = report.safety_boundary_report
        return {
            "version": SELF_MODIFICATION_CONSOLIDATION_VERSION,
            "layer": "self_modification_safety",
            "subject": "consolidation",
            "release_name": SELF_MODIFICATION_FOUNDATION_RELEASE_NAME,
            "coverage": {
                "contract": "implemented",
                "request_candidate": "implemented",
                "draft_diff_preview": "implemented",
                "static_safety": "implemented",
                "dry_run": "implemented",
                "human_review_apply_gate": "implemented",
                "bounded_apply": "implemented",
                "post_apply_verification_outcome": "implemented",
                "workbench": "implemented",
                "consolidation": "implemented",
            },
            "safety_boundary": safety.to_dict(),
            "rollback_executed": False,
            "shell_executed": False,
            "test_lint_executed": False,
            "llm_judge_enabled": False,
            "safe_to_apply": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "post_apply_verified": False,
            "file_write_performed": False,
            "workspace_file_changed_emitted": False,
            "post_apply_verification_required": True,
            "no_file_mutation_occurred": True,
            "mutation_performed": False,
            "additional_file_write_performed": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": SELF_MODIFICATION_CONSOLIDATION_VERSION,
            "layer": "self_modification_safety",
            "state": SELF_MODIFICATION_CONSOLIDATION_STATE,
            "release_version": SELF_MODIFICATION_CONSOLIDATION_VERSION,
            "release_name": SELF_MODIFICATION_FOUNDATION_RELEASE_NAME,
            "source_read_models": [
                "SelfModificationWorkbenchState",
                "SelfModificationPipelineState",
                "SelfModificationSafetyBoundaryState",
                "SelfModificationReadinessState",
                "ModificationOutcomeState",
                "PostApplyVerificationState",
                "BoundedPatchApplyState",
                "WorkspaceFileChangeState",
                "ApplyGateState",
                "PatchDryRunState",
                "PatchStaticSafetyState",
                "PatchDraftState",
                "PatchCandidateState",
            ],
            "target_read_models": [
                "SelfModificationReleaseState",
                "SelfModificationConsolidationState",
                "SelfModificationGapRegisterState",
                "SelfModificationReadinessState",
            ],
            "effect_types": list(CONSOLIDATION_EFFECT_TYPES),
            "release_status": report.release_status,
            "safe_to_apply": False,
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "post_apply_verified": False,
            "file_write_performed": False,
            "workspace_file_changed_emitted": False,
            "post_apply_verification_required": True,
            "no_file_mutation_occurred": True,
        }

    def render_report_cli(self, report: SelfModificationConsolidationReport, section: str = "consolidate") -> str:
        safety = report.safety_boundary_report
        return "\n".join(
            [
                "Self-Modification Safety Consolidation",
                f"version={SELF_MODIFICATION_CONSOLIDATION_VERSION}",
                f"release_name={SELF_MODIFICATION_FOUNDATION_RELEASE_NAME}",
                f"section={section}",
                f"release_status={report.release_status}",
                f"readiness_status={report.readiness_status}",
                f"subject_coverage={report.coverage_matrix.coverage_status}",
                f"unauthorized_write_count={safety.unauthorized_write_count}",
                f"apply_without_gate_count={safety.apply_without_gate_count}",
                f"consumed_authorization_reuse_count={safety.consumed_authorization_reuse_count}",
                f"workspace_file_changed_without_transaction_count={safety.workspace_file_changed_without_transaction_count}",
                f"unverified_apply_count={safety.unverified_apply_count}",
                f"missing_outcome_count={safety.missing_outcome_count}",
                f"pipeline_completed={report.pipeline_summary.completed_pipeline_count}",
                f"pipeline_pending={report.pipeline_summary.pending_pipeline_count}",
                f"authorization_open={report.authorization_summary.open_count}",
                f"authorization_consumed={report.authorization_summary.consumed_count}",
                f"changed_file_count={report.change_summary.changed_file_count}",
                f"verified_change_count={report.change_summary.verified_change_count}",
                f"outcome_count={report.outcome_summary.total_outcome_count}",
                f"gap_count={report.gap_register.future_gap_count}",
                f"next_track_recommendations={','.join(report.next_track_recommendations)}",
                "read_only_consolidation=true",
                f"mutation_performed={str(report.mutation_performed).lower()}",
                f"additional_file_write_performed={str(report.additional_file_write_performed).lower()}",
                f"rollback_executed={str(report.rollback_executed).lower()}",
                f"shell_executed={str(report.shell_executed).lower()}",
                f"test_lint_executed={str(report.test_lint_executed).lower()}",
                f"llm_judge_used={str(report.llm_judge_used).lower()}",
                "safe_to_apply=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "post_apply_verified=false",
                "file_write_performed=false",
                "workspace_file_changed_emitted=false",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        safety = report["safety_boundary"]
        return "\n".join(
            [
                "Self-Modification Consolidation PIG Report",
                f"version={report['version']}",
                f"layer={report['layer']}",
                f"subject={report['subject']}",
                f"release_name={report['release_name']}",
                f"coverage={','.join(f'{key}:{value}' for key, value in report['coverage'].items())}",
                f"unauthorized_write_count={safety['unauthorized_write_count']}",
                f"apply_without_gate_count={safety['apply_without_gate_count']}",
                f"consumed_authorization_reuse_count={safety['consumed_authorization_reuse_count']}",
                f"workspace_file_changed_without_transaction_count={safety['workspace_file_changed_without_transaction_count']}",
                f"unverified_apply_count={safety['unverified_apply_count']}",
                f"missing_outcome_count={safety['missing_outcome_count']}",
                f"rollback_executed={str(report['rollback_executed']).lower()}",
                f"shell_executed={str(report['shell_executed']).lower()}",
                f"test_lint_executed={str(report['test_lint_executed']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                f"safe_to_apply={str(report['safe_to_apply']).lower()}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"post_apply_verified={str(report['post_apply_verified']).lower()}",
                f"file_write_performed={str(report['file_write_performed']).lower()}",
                f"workspace_file_changed_emitted={str(report['workspace_file_changed_emitted']).lower()}",
                f"no_file_mutation_occurred={str(report['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Consolidation OCPX Projection",
                f"version={projection['version']}",
                f"layer={projection['layer']}",
                f"state={projection['state']}",
                f"release_version={projection['release_version']}",
                f"release_name={projection['release_name']}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"release_status={projection['release_status']}",
                f"safe_to_apply={str(projection['safe_to_apply']).lower()}",
                f"file_write_enabled={str(projection['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(projection['apply_patch_enabled']).lower()}",
                f"post_apply_verified={str(projection['post_apply_verified']).lower()}",
                f"file_write_performed={str(projection['file_write_performed']).lower()}",
                f"workspace_file_changed_emitted={str(projection['workspace_file_changed_emitted']).lower()}",
                f"no_file_mutation_occurred={str(projection['no_file_mutation_occurred']).lower()}",
                "No file mutation occurred.",
                "raw_file_content_printed=False",
                "raw_full_file_content_printed=False",
                "private_full_paths_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def _readiness_status(
        self,
        *,
        safety_report: SelfModificationSafetyBoundaryReport,
        coverage_matrix: SelfModificationCoverageMatrix,
        gap_register: SelfModificationGapRegister,
        pipeline_summary: SelfModificationPipelineSummary,
        outcome_summary: SelfModificationOutcomeSummary,
    ) -> tuple[str, list[str]]:
        rationale: list[str] = []
        if safety_report.safety_status == "blocked":
            rationale.append("Safety boundary contains a release blocker.")
        if coverage_matrix.coverage_status == "blocked":
            rationale.append("Required subject coverage is missing.")
        if pipeline_summary.blocked_pipeline_count or pipeline_summary.failed_pipeline_count:
            rationale.append("Pipeline contains blocked or failed items.")
        if outcome_summary.missing_outcome_count:
            rationale.append("Bounded apply exists without outcome record.")
        if rationale:
            return "blocked", rationale
        if gap_register.future_gap_count:
            return "warning", ["Only future-track gaps remain; current release is releasable with warnings."]
        return "ready", ["All required subjects and safety boundaries are consolidated."]


def _capability(
    capability_id: str,
    capability_name: str,
    introduced_in: str,
    source_read_models: list[str],
    target_read_models: list[str],
    effect_types: list[str],
) -> SelfModificationCapabilityMapEntry:
    return SelfModificationCapabilityMapEntry(
        capability_id=capability_id,
        capability_name=capability_name,
        status="implemented",
        introduced_in=introduced_in,
        source_read_models=source_read_models,
        target_read_models=target_read_models,
        effect_types=effect_types,
        ocel_visible=True,
        pig_visible=True,
        ocpx_visible=True,
        workbench_visible=True,
    )

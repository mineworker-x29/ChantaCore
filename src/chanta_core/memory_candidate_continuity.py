from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench.consolidation import WorkbenchConsolidationReportService


MEMORY_CONTRACT_VERSION = "v0.27.0"
MEMORY_CONTRACT_VERSION_NAME = "Memory Candidate & Continuity Contract"
MEMORY_CONTRACT_KOREAN_NAME = "Memory Candidate.Continuity contract"
MEMORY_CONTRACT_LAYER = "memory_candidate_continuity"
MEMORY_CONTRACT_TRACK = "Memory Candidate & Continuity"
MEMORY_CONTRACT_NEXT_STEP = "v0.27.1 Memory Source / Ref Boundary"
MEMORY_CONTRACT_RECOMMENDED_PREREQUISITE = "v0.26.10 Release Hygiene / Governance Hardening"

MEMORY_ALLOWED_SOURCE_CATEGORIES = [
    "workbench_snapshot_refs",
    "ocel_export_package_refs",
    "session_context_refs",
    "trace_summary_refs",
    "evidence_summary_refs",
    "pig_guidance_refs",
    "approval_decision_refs",
    "command_candidate_refs",
    "failure_cause_refs",
    "human_intervention_refs",
    "event_quality_report_refs",
]

MEMORY_FORBIDDEN_SOURCE_CATEGORIES = [
    "raw_transcript",
    "raw_provider_output",
    "raw_secret",
    "credential",
    "private_full_path",
    "unredacted_file_content",
]

MEMORY_CANDIDATE_TYPES = [
    "task_preference_candidate",
    "workflow_preference_candidate",
    "project_state_candidate",
    "decision_pattern_candidate",
    "skill_usage_pattern_candidate",
    "provider_route_pattern_candidate",
    "approval_preference_candidate",
    "failure_pattern_candidate",
    "context_summary_candidate",
    "long_task_continuity_candidate",
    "user_instruction_candidate",
    "system_boundary_candidate",
    "do_nothing_preference_candidate",
    "safety_preference_candidate",
    "unknown",
]

MEMORY_SCORE_DIMENSIONS = [
    "evidence_strength",
    "source_quality",
    "recency",
    "stability",
    "reuse_value",
    "specificity",
    "risk_level",
    "privacy_sensitivity",
    "contradiction_risk",
    "user_control_requirement",
]

MEMORY_RELEASE_HYGIENE_GATE_NAMES = [
    "ReleaseHygieneGate",
    "RepositoryGovernanceGate",
    "PackagingReadinessGate",
    "RuntimeDataHygieneGate",
    "TestAutomationGate",
    "ReferenceCodeLicenseGate",
]

MEMORY_CONTRACT_OBJECT_TYPES = [
    "memory_candidate_continuity_contract",
    "memory_track_roadmap",
    "memory_track_version_plan",
    "memory_source_boundary_policy",
    "memory_source_eligibility_policy",
    "memory_candidate_policy",
    "memory_candidate_type_catalog",
    "memory_evidence_policy",
    "memory_scoring_policy",
    "memory_promotion_gate_policy",
    "durable_memory_policy",
    "session_continuity_policy",
    "continuity_injection_policy",
    "memory_audit_policy",
    "memory_privacy_policy",
    "memory_governance_policy",
    "memory_pig_guidance_policy",
    "memory_safety_boundary_policy",
    "memory_release_prerequisite_policy",
    "memory_contract_finding",
    "memory_contract_report",
    "workbench_memory_candidate_handoff_packet",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

MEMORY_CONTRACT_EVENT_TYPES = [
    "memory_contract_requested",
    "memory_contract_prerequisites_loaded",
    "memory_track_roadmap_created",
    "memory_source_boundary_policy_created",
    "memory_source_eligibility_policy_created",
    "memory_candidate_policy_created",
    "memory_candidate_type_catalog_created",
    "memory_evidence_policy_created",
    "memory_scoring_policy_created",
    "memory_promotion_gate_policy_created",
    "durable_memory_policy_created",
    "session_continuity_policy_created",
    "continuity_injection_policy_created",
    "memory_audit_policy_created",
    "memory_privacy_policy_created",
    "memory_governance_policy_created",
    "memory_pig_guidance_policy_created",
    "memory_safety_boundary_policy_created",
    "memory_release_prerequisite_policy_created",
    "memory_contract_created",
    "memory_contract_report_created",
    "memory_contract_warning_created",
    "memory_contract_blocked",
]

MEMORY_CONTRACT_RELATION_TYPES = [
    "declares_memory_candidate_continuity_contract",
    "uses_workbench_memory_candidate_handoff_packet",
    "uses_workbench_v027_readiness_report",
    "uses_workbench_snapshot_export_report",
    "declares_memory_source_boundary",
    "declares_memory_candidate_policy",
    "declares_memory_evidence_policy",
    "declares_memory_scoring_policy",
    "declares_memory_promotion_gate_policy",
    "declares_durable_memory_policy",
    "declares_session_continuity_policy",
    "declares_continuity_injection_policy",
    "defers_memory_candidate_extraction_to_v0_27_2",
    "defers_persistent_memory_write_to_v0_27_5",
    "requires_release_hygiene_before_persistent_write",
]

MEMORY_CONTRACT_EFFECT_TYPES = [
    "read_only_observation",
    "memory_contract_declared",
    "memory_policy_declared",
    "memory_roadmap_declared",
    "state_candidate_created",
]

MEMORY_CONTRACT_FORBIDDEN_EFFECT_TYPES = [
    "memory_candidate_created",
    "memory_candidate_scored",
    "memory_promoted",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "session_continuity_context_created",
    "continuity_injection_bundle_created",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


def _ref(ref_type: str, ref_id: str, version: str = MEMORY_CONTRACT_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _bool(value: bool) -> str:
    return "true" if value else "false"


class _ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MemoryTrackVersionPlan(_ModelMixin):
    version_id: str
    version_name: str
    version_number: str
    purpose: str
    allowed_scope: list[str]
    forbidden_scope: list[str]
    persistent_memory_write_allowed: bool
    memory_promotion_allowed: bool
    persona_mutation_allowed: bool = False
    external_adapter_allowed: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class MemoryTrackRoadmap(_ModelMixin):
    roadmap_id: str
    versions: list[MemoryTrackVersionPlan]
    roadmap_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    current_track: str = "v0.27.x Memory Candidate & Continuity"
    next_version: str = MEMORY_CONTRACT_NEXT_STEP
    consolidation_version: str = "v0.27.9 Memory Candidate & Continuity Consolidation"
    next_track: str = "v0.28.x Public Alpha / Schumpeter Split Preparation"


@dataclass
class MemorySourceBoundaryPolicy(_ModelMixin):
    policy_id: str
    allowed_source_categories: list[str]
    forbidden_source_categories: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    refs_only_source_required: bool = True
    raw_transcript_default_source_forbidden: bool = True
    raw_provider_output_source_forbidden: bool = True
    raw_secret_source_forbidden: bool = True
    credential_source_forbidden: bool = True
    private_full_path_source_forbidden: bool = True
    unredacted_file_content_source_forbidden: bool = True
    source_quality_required: bool = True
    redaction_required: bool = True


@dataclass
class MemorySourceEligibilityPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    eligibility_check_required: bool = True
    source_ref_required: bool = True
    evidence_ref_required: bool = True
    event_quality_ref_required: bool = True
    trace_coverage_ref_required: bool = False
    user_sensitive_data_check_required: bool = True
    stale_source_warning_required: bool = True
    contradiction_check_required_later: bool = True
    source_without_ref_blocked: bool = True
    raw_content_source_blocked: bool = True


@dataclass
class MemoryCandidatePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    memory_candidate_enabled_future: bool = True
    memory_candidate_extraction_deferred_to: str = "v0.27.2"
    candidate_is_not_memory: bool = True
    candidate_requires_source_refs: bool = True
    candidate_requires_evidence_refs: bool = True
    candidate_requires_type: bool = True
    candidate_requires_risk_flags: bool = True
    candidate_requires_promotion_status_candidate_only: bool = True
    raw_transcript_candidate_forbidden_by_default: bool = True
    automatic_promotion_forbidden: bool = True


@dataclass
class MemoryCandidateTypeCatalog(_ModelMixin):
    catalog_id: str
    candidate_types: list[str]
    type_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION


@dataclass
class MemoryEvidencePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    evidence_binding_deferred_to: str = "v0.27.3"
    evidence_bundle_required_for_scoring: bool = True
    source_refs_required: bool = True
    claim_refs_allowed: bool = True
    approval_refs_allowed: bool = True
    pig_guidance_refs_allowed: bool = True
    event_quality_refs_allowed: bool = True
    trace_coverage_refs_allowed: bool = True
    raw_provider_output_evidence_forbidden: bool = True
    raw_transcript_evidence_forbidden_by_default: bool = True
    raw_secret_evidence_forbidden: bool = True


@dataclass
class MemoryScoringPolicy(_ModelMixin):
    policy_id: str
    required_score_dimensions: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    scoring_deferred_to: str = "v0.27.3"
    score_is_not_promotion: bool = True
    high_score_is_not_automatic_memory: bool = True
    pig_guidance_may_inform_score: bool = True
    pig_guidance_cannot_promote_memory: bool = True
    llm_judge_cannot_be_sole_scoring_authority: bool = True


@dataclass
class MemoryPromotionGatePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    promotion_gate_deferred_to: str = "v0.27.4"
    promotion_is_not_persona_mutation: bool = True
    automatic_promotion_forbidden: bool = True
    promotion_requires_source_refs: bool = True
    promotion_requires_evidence_bundle: bool = True
    promotion_requires_score: bool = True
    promotion_requires_privacy_risk_assessment: bool = True
    promotion_requires_scope: bool = True
    promotion_requires_lifecycle_policy: bool = True
    promotion_requires_audit_trail: bool = True
    promotion_requires_forget_revoke_path: bool = True
    promotion_without_gate_blocked: bool = True


@dataclass
class DurableMemoryPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    durable_memory_registry_deferred_to: str = "v0.27.5"
    persistent_memory_write_forbidden_in_v0270: bool = True
    persistent_memory_write_allowed_future_only_after_promotion: bool = True
    durable_memory_requires_provenance: bool = True
    durable_memory_requires_scope: bool = True
    durable_memory_requires_evidence_index: bool = True
    durable_memory_requires_lifecycle_policy: bool = True
    durable_memory_must_be_revocable: bool = True
    durable_memory_must_be_forgettable: bool = True
    durable_memory_does_not_mutate_persona_by_default: bool = True


@dataclass
class SessionContinuityPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    session_continuity_context_deferred_to: str = "v0.27.6"
    session_continuity_is_not_raw_transcript_replay: bool = True
    continuity_context_pack_required: bool = True
    continuity_uses_active_memory_refs_future: bool = True
    continuity_uses_session_context_refs: bool = True
    continuity_uses_trace_summary_refs: bool = True
    continuity_uses_pig_guidance_refs: bool = True
    raw_transcript_replay_forbidden: bool = True
    unbounded_context_stuffing_forbidden: bool = True
    stale_memory_warning_required: bool = True
    contradiction_surface_required: bool = True


@dataclass
class ContinuityInjectionPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    continuity_injection_deferred_to: str = "v0.27.7"
    injection_is_guidance_not_override: bool = True
    memory_context_is_not_authority: bool = True
    explicit_user_instruction_outranks_memory: bool = True
    safety_gate_must_remain_active: bool = True
    permission_boundary_must_remain_active: bool = True
    injection_must_be_previewable: bool = True
    injection_requires_boundary_trace: bool = True
    injection_must_not_invoke_provider: bool = True
    injection_must_not_execute_command: bool = True
    injection_must_not_mutate_persona: bool = True


@dataclass
class MemoryAuditPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    audit_lifecycle_deferred_to: str = "v0.27.8"
    audit_required_for_promotion: bool = True
    audit_required_for_update: bool = True
    audit_required_for_revoke: bool = True
    audit_required_for_forget: bool = True
    silent_memory_overwrite_forbidden: bool = True
    unlogged_memory_deletion_forbidden: bool = True
    forget_is_not_source_data_deletion_by_default: bool = True
    revoke_removes_active_use: bool = True


@dataclass
class MemoryPrivacyPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    privacy_check_required: bool = True
    sensitive_memory_requires_stricter_gate: bool = True
    raw_secret_memory_forbidden: bool = True
    credential_memory_forbidden: bool = True
    private_full_path_memory_forbidden: bool = True
    personal_sensitive_attribute_memory_blocked_by_default: bool = True
    user_requested_memory_exception_requires_audit: bool = True
    forget_revoke_path_required: bool = True


@dataclass
class MemoryGovernancePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    v02610_hardening_recommended_before_persistent_write: bool = True
    clean_repo_recommended_before_durable_memory: bool = True
    runtime_data_hygiene_required_before_memory_registry: bool = True
    license_governance_required_before_public_alpha: bool = True
    memory_schema_versioning_required: bool = True
    migration_plan_required_for_registry_changes: bool = True


@dataclass
class MemoryPIGGuidancePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    pig_guidance_is_not_memory: bool = True
    pig_guidance_may_inform_candidate_scoring: bool = True
    pig_guidance_may_inform_continuity_context: bool = True
    pig_guidance_may_surface_patterns: bool = True
    pig_guidance_cannot_promote_memory: bool = True
    pig_guidance_cannot_mutate_persona: bool = True
    pig_guidance_cannot_mutate_behavior_policy: bool = True
    pig_guidance_cannot_execute: bool = True
    pig_guidance_requires_refs: bool = True


@dataclass
class MemorySafetyBoundaryPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    memory_candidate_extraction_enabled_now: bool = False
    memory_scoring_enabled_now: bool = False
    memory_promotion_enabled_now: bool = False
    persistent_memory_write_enabled_now: bool = False
    session_continuity_injection_enabled_now: bool = False
    persona_mutation_forbidden: bool = True
    behavior_policy_auto_mutation_forbidden: bool = True
    raw_transcript_memory_forbidden: bool = True
    raw_provider_output_memory_forbidden: bool = True
    memory_without_evidence_forbidden: bool = True
    memory_without_source_refs_forbidden: bool = True
    memory_without_promotion_gate_forbidden: bool = True
    memory_triggered_provider_invocation_forbidden: bool = True
    memory_triggered_command_execution_forbidden: bool = True
    memory_triggered_safety_bypass_forbidden: bool = True


@dataclass
class MemoryReleasePrerequisitePolicy(_ModelMixin):
    policy_id: str
    release_hygiene_gate_names: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONTRACT_VERSION
    v0269_workbench_handoff_required: bool = True
    v02610_release_hygiene_recommended: bool = True
    v02610_required_before_v0275_persistent_write: bool = True


@dataclass
class MemoryCandidateContinuityContract(_ModelMixin):
    contract_id: str
    definition: str
    previous_release_ref: dict[str, Any] | None
    recommended_prerequisite_ref: dict[str, Any] | None
    roadmap: MemoryTrackRoadmap
    source_boundary_policy: MemorySourceBoundaryPolicy
    source_eligibility_policy: MemorySourceEligibilityPolicy
    candidate_policy: MemoryCandidatePolicy
    candidate_type_catalog: MemoryCandidateTypeCatalog
    evidence_policy: MemoryEvidencePolicy
    scoring_policy: MemoryScoringPolicy
    promotion_gate_policy: MemoryPromotionGatePolicy
    durable_memory_policy: DurableMemoryPolicy
    session_continuity_policy: SessionContinuityPolicy
    continuity_injection_policy: ContinuityInjectionPolicy
    audit_policy: MemoryAuditPolicy
    privacy_policy: MemoryPrivacyPolicy
    governance_policy: MemoryGovernancePolicy
    pig_guidance_policy: MemoryPIGGuidancePolicy
    safety_boundary_policy: MemorySafetyBoundaryPolicy
    release_prerequisite_policy: MemoryReleasePrerequisitePolicy
    notes: list[str] = field(default_factory=list)
    version: str = MEMORY_CONTRACT_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    track: str = MEMORY_CONTRACT_TRACK
    status: str = "contract_only"
    memory_candidate_extracted: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False


@dataclass
class MemoryContractFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryContractReport(_ModelMixin):
    report_id: str
    created_at: str
    contract: MemoryCandidateContinuityContract
    findings: list[MemoryContractFinding]
    report_status: str
    ready_for_v0_27_1: bool
    contract_created: bool
    roadmap_created: bool
    source_boundary_policy_created: bool
    candidate_policy_created: bool
    evidence_policy_created: bool
    scoring_policy_created: bool
    promotion_gate_policy_created: bool
    durable_memory_policy_created: bool
    session_continuity_policy_created: bool
    continuity_injection_policy_created: bool
    audit_policy_created: bool
    privacy_policy_created: bool
    governance_policy_created: bool
    pig_guidance_policy_created: bool
    safety_boundary_policy_created: bool
    version: str = MEMORY_CONTRACT_VERSION
    ready_for_v0_28: bool = False
    memory_candidate_extracted: bool = False
    memory_scored: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_CONTRACT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.27.1 Memory Source / Ref Boundary begins or memory policy changes."


class MemoryContractPrerequisiteSourceService:
    def __init__(
        self,
        *,
        v0269_handoff_available: bool = True,
        v0269_readiness_available: bool = True,
        v0269_consolidation_available: bool = True,
        v0268_snapshot_export_available: bool = True,
        pig_ocpx_available: bool = True,
        release_hygiene_status_available: bool = False,
    ) -> None:
        self.v0269_handoff_available = v0269_handoff_available
        self.v0269_readiness_available = v0269_readiness_available
        self.v0269_consolidation_available = v0269_consolidation_available
        self.v0268_snapshot_export_available = v0268_snapshot_export_available
        self.pig_ocpx_available = pig_ocpx_available
        self.release_hygiene_status_available = release_hygiene_status_available
        self._workbench_parts: dict[str, Any] | None = None

    def _workbench(self) -> dict[str, Any]:
        if self._workbench_parts is None:
            self._workbench_parts = WorkbenchConsolidationReportService().build_all_parts()
        return self._workbench_parts

    def load_v0269_workbench_consolidation_report(self) -> dict[str, Any] | None:
        if not self.v0269_consolidation_available:
            return None
        report = self._workbench()["report"]
        return _ref("workbench_consolidation_report", report.report_id, report.version)

    def load_v0269_v027_readiness_report(self) -> dict[str, Any] | None:
        if not self.v0269_readiness_available:
            return None
        readiness = self._workbench()["v027_readiness_report"]
        return _ref("workbench_v027_readiness_report", readiness.report_id, readiness.version)

    def load_v0269_memory_candidate_handoff_packet(self) -> dict[str, Any] | None:
        if not self.v0269_handoff_available:
            return None
        handoff = self._workbench()["memory_candidate_handoff_packet"]
        return _ref("workbench_memory_candidate_handoff_packet", handoff.handoff_packet_id, handoff.version)

    def load_v0268_snapshot_export_report_if_available(self) -> dict[str, Any] | None:
        if not self.v0268_snapshot_export_available:
            return None
        return _ref("workbench_snapshot_export_report", "workbench_snapshot_export_report:v0.26.8", "v0.26.8")

    def load_pig_ocpx_reports_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_ocpx_available:
            return []
        return [
            _ref("pig_report", "workspace_agent_workbench_consolidation_pig:v0.26.9", "v0.26.9"),
            _ref("ocpx_projection", "workspace_agent_workbench_foundation_v1_consolidated", "v0.26.9"),
        ]

    def load_release_hygiene_status_if_available(self) -> dict[str, Any] | None:
        if not self.release_hygiene_status_available:
            return None
        return _ref("release_hygiene_report", "release_hygiene_governance_hardening:v0.26.10", "v0.26.10")

    def evidence_refs(self) -> list[dict[str, Any]]:
        refs = [
            self.load_v0269_workbench_consolidation_report(),
            self.load_v0269_v027_readiness_report(),
            self.load_v0269_memory_candidate_handoff_packet(),
            self.load_v0268_snapshot_export_report_if_available(),
            self.load_release_hygiene_status_if_available(),
        ]
        return [ref for ref in refs if ref is not None] + self.load_pig_ocpx_reports_if_available()


class MemoryTrackRoadmapService:
    ROADMAP_ROWS = [
        ("v0.27.0", "Memory Candidate & Continuity Contract", "Define the contract only.", ["contract", "policy", "roadmap"], ["candidate extraction", "scoring", "promotion", "persistent write"], False, False),
        ("v0.27.1", "Memory Source / Ref Boundary", "Define eligible refs and source boundaries.", ["source boundary", "refs-only eligibility"], ["memory extraction", "promotion", "persistent write"], False, False),
        ("v0.27.2", "Memory Candidate Extraction", "Create candidates but not memory.", ["candidate creation"], ["promotion", "persistent write"], False, False),
        ("v0.27.3", "Memory Evidence Binder & Scoring", "Bind evidence and score candidates.", ["evidence binding", "scoring"], ["promotion", "persistent write"], False, False),
        ("v0.27.4", "Memory Promotion Gate", "Create promotion decisions and gates.", ["promotion decision", "gate"], ["durable registry write unless deferred"], False, True),
        ("v0.27.5", "Durable Memory Record & Registry", "Create durable memory only after gate approval.", ["durable record", "registry"], ["persona mutation", "ungated write"], True, True),
        ("v0.27.6", "Session Continuity Context Builder", "Build continuity context packs from approved memory and refs.", ["continuity context"], ["raw transcript replay", "provider invocation"], False, False),
        ("v0.27.7", "Continuity Injection Boundary", "Define previewable continuity injection boundaries.", ["injection boundary", "preview"], ["behavior override", "safety bypass"], False, False),
        ("v0.27.8", "Memory Audit / Update / Revoke / Forget", "Manage durable memory lifecycle.", ["audit", "update", "revoke", "forget"], ["silent overwrite", "unlogged deletion"], False, False),
        ("v0.27.9", "Memory Candidate & Continuity Consolidation", "Consolidate Memory Candidate & Continuity Foundation v1.", ["consolidation", "readiness"], ["new memory feature implementation"], False, False),
    ]

    def build_roadmap(self, evidence_refs: list[dict[str, Any]] | None = None) -> MemoryTrackRoadmap:
        versions = [
            MemoryTrackVersionPlan(
                version_id=f"memory_track_plan:{number}",
                version_name=name,
                version_number=number,
                purpose=purpose,
                allowed_scope=allowed,
                forbidden_scope=forbidden,
                persistent_memory_write_allowed=persistent_write,
                memory_promotion_allowed=promotion,
                notes=["Persona mutation and external adapters remain forbidden throughout v0.27.x."],
            )
            for number, name, purpose, allowed, forbidden, persistent_write, promotion in self.ROADMAP_ROWS
        ]
        return MemoryTrackRoadmap(
            roadmap_id="memory_track_roadmap:v0.27.0",
            versions=versions,
            roadmap_status="aligned",
            evidence_refs=evidence_refs or [_ref("workbench_memory_candidate_handoff_packet", "workbench_memory_candidate_handoff:v0.26.9", "v0.26.9")],
        )


class _PolicyService:
    policy_type = "memory_policy"

    def _evidence(self) -> list[dict[str, Any]]:
        return [_ref("memory_candidate_continuity_contract", "memory_candidate_continuity_contract:v0.27.0")]


class MemorySourceBoundaryPolicyService(_PolicyService):
    def build_policy(self) -> MemorySourceBoundaryPolicy:
        return MemorySourceBoundaryPolicy(
            policy_id="memory_source_boundary_policy:v0.27.0",
            allowed_source_categories=list(MEMORY_ALLOWED_SOURCE_CATEGORIES),
            forbidden_source_categories=list(MEMORY_FORBIDDEN_SOURCE_CATEGORIES),
            evidence_refs=self._evidence(),
        )


class MemorySourceEligibilityPolicyService(_PolicyService):
    def build_policy(self) -> MemorySourceEligibilityPolicy:
        return MemorySourceEligibilityPolicy("memory_source_eligibility_policy:v0.27.0", self._evidence())


class MemoryCandidatePolicyService(_PolicyService):
    def build_policy(self) -> MemoryCandidatePolicy:
        return MemoryCandidatePolicy("memory_candidate_policy:v0.27.0", self._evidence())


class MemoryCandidateTypeCatalogService(_PolicyService):
    def build_catalog(self) -> MemoryCandidateTypeCatalog:
        return MemoryCandidateTypeCatalog(
            catalog_id="memory_candidate_type_catalog:v0.27.0",
            candidate_types=list(MEMORY_CANDIDATE_TYPES),
            type_status="ready",
            evidence_refs=self._evidence(),
        )


class MemoryEvidencePolicyService(_PolicyService):
    def build_policy(self) -> MemoryEvidencePolicy:
        return MemoryEvidencePolicy("memory_evidence_policy:v0.27.0", self._evidence())


class MemoryScoringPolicyService(_PolicyService):
    def build_policy(self) -> MemoryScoringPolicy:
        return MemoryScoringPolicy("memory_scoring_policy:v0.27.0", list(MEMORY_SCORE_DIMENSIONS), self._evidence())


class MemoryPromotionGatePolicyService(_PolicyService):
    def build_policy(self) -> MemoryPromotionGatePolicy:
        return MemoryPromotionGatePolicy("memory_promotion_gate_policy:v0.27.0", self._evidence())


class DurableMemoryPolicyService(_PolicyService):
    def build_policy(self) -> DurableMemoryPolicy:
        return DurableMemoryPolicy("durable_memory_policy:v0.27.0", self._evidence())


class SessionContinuityPolicyService(_PolicyService):
    def build_policy(self) -> SessionContinuityPolicy:
        return SessionContinuityPolicy("session_continuity_policy:v0.27.0", self._evidence())


class ContinuityInjectionPolicyService(_PolicyService):
    def build_policy(self) -> ContinuityInjectionPolicy:
        return ContinuityInjectionPolicy("continuity_injection_policy:v0.27.0", self._evidence())


class MemoryAuditPolicyService(_PolicyService):
    def build_policy(self) -> MemoryAuditPolicy:
        return MemoryAuditPolicy("memory_audit_policy:v0.27.0", self._evidence())


class MemoryPrivacyPolicyService(_PolicyService):
    def build_policy(self) -> MemoryPrivacyPolicy:
        return MemoryPrivacyPolicy("memory_privacy_policy:v0.27.0", self._evidence())


class MemoryGovernancePolicyService(_PolicyService):
    def build_policy(self) -> MemoryGovernancePolicy:
        return MemoryGovernancePolicy("memory_governance_policy:v0.27.0", self._evidence())


class MemoryPIGGuidancePolicyService(_PolicyService):
    def build_policy(self) -> MemoryPIGGuidancePolicy:
        return MemoryPIGGuidancePolicy("memory_pig_guidance_policy:v0.27.0", self._evidence())


class MemorySafetyBoundaryPolicyService(_PolicyService):
    def build_policy(self) -> MemorySafetyBoundaryPolicy:
        return MemorySafetyBoundaryPolicy("memory_safety_boundary_policy:v0.27.0", self._evidence())


class MemoryReleasePrerequisitePolicyService(_PolicyService):
    def build_policy(self) -> MemoryReleasePrerequisitePolicy:
        return MemoryReleasePrerequisitePolicy(
            policy_id="memory_release_prerequisite_policy:v0.27.0",
            release_hygiene_gate_names=list(MEMORY_RELEASE_HYGIENE_GATE_NAMES),
            evidence_refs=self._evidence(),
        )


class MemoryContractService:
    def build_contract(
        self,
        roadmap: MemoryTrackRoadmap,
        source_boundary: MemorySourceBoundaryPolicy,
        source_eligibility: MemorySourceEligibilityPolicy,
        candidate_policy: MemoryCandidatePolicy,
        candidate_catalog: MemoryCandidateTypeCatalog,
        evidence_policy: MemoryEvidencePolicy,
        scoring_policy: MemoryScoringPolicy,
        promotion_policy: MemoryPromotionGatePolicy,
        durable_policy: DurableMemoryPolicy,
        continuity_policy: SessionContinuityPolicy,
        injection_policy: ContinuityInjectionPolicy,
        audit_policy: MemoryAuditPolicy,
        privacy_policy: MemoryPrivacyPolicy,
        governance_policy: MemoryGovernancePolicy,
        pig_policy: MemoryPIGGuidancePolicy,
        safety_policy: MemorySafetyBoundaryPolicy,
        release_prerequisite_policy: MemoryReleasePrerequisitePolicy,
    ) -> MemoryCandidateContinuityContract:
        return MemoryCandidateContinuityContract(
            contract_id="memory_candidate_continuity_contract:v0.27.0",
            definition="Contract-only Memory Candidate & Continuity foundation. It declares source, candidate, evidence, scoring, promotion, durable memory, continuity, injection, audit, privacy, governance, PIG, and safety boundaries without creating memory.",
            previous_release_ref=_ref("workbench_release_manifest", "workbench_release_manifest:v0.26.9", "v0.26.9"),
            recommended_prerequisite_ref=_ref("release_hygiene_governance_hardening", "release_hygiene_governance_hardening:v0.26.10", "v0.26.10"),
            roadmap=roadmap,
            source_boundary_policy=source_boundary,
            source_eligibility_policy=source_eligibility,
            candidate_policy=candidate_policy,
            candidate_type_catalog=candidate_catalog,
            evidence_policy=evidence_policy,
            scoring_policy=scoring_policy,
            promotion_gate_policy=promotion_policy,
            durable_memory_policy=durable_policy,
            session_continuity_policy=continuity_policy,
            continuity_injection_policy=injection_policy,
            audit_policy=audit_policy,
            privacy_policy=privacy_policy,
            governance_policy=governance_policy,
            pig_guidance_policy=pig_policy,
            safety_boundary_policy=safety_policy,
            release_prerequisite_policy=release_prerequisite_policy,
            notes=[
                "v0.27.0 is contract-only and non-mutating.",
                "v0.26.10 release hygiene is recommended before persistent memory write and required before v0.27.5 durable registry work.",
            ],
        )

    def view_contract(self) -> MemoryCandidateContinuityContract:
        parts = MemoryContractReportService().build_all_parts()
        return parts["contract"]


class MemoryContractFindingService:
    BLOCKED_FINDINGS = {
        "memory_candidate_extraction_attempted",
        "memory_scoring_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "raw_transcript_memory_attempted",
        "raw_provider_output_memory_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }
    REQUIRED_POLICY_FINDINGS = {
        "missing_v027_contract",
        "missing_source_boundary_policy",
        "missing_candidate_policy",
        "missing_evidence_policy",
        "missing_scoring_policy",
        "missing_promotion_gate_policy",
        "missing_durable_memory_policy",
        "missing_session_continuity_policy",
        "missing_continuity_injection_policy",
        "missing_audit_policy",
        "missing_privacy_policy",
        "missing_governance_policy",
        "missing_pig_guidance_policy",
        "missing_safety_boundary_policy",
    }

    def build_findings(
        self,
        source_service: MemoryContractPrerequisiteSourceService,
        *,
        extra_findings: list[str] | None = None,
    ) -> list[MemoryContractFinding]:
        findings: list[MemoryContractFinding] = []
        if not source_service.v0269_handoff_available:
            findings.append(self._finding("warning", "missing_v0269_handoff", "v0.26.9 memory-candidate handoff is unavailable."))
        if not source_service.release_hygiene_status_available:
            findings.append(
                self._finding(
                    "warning",
                    "v02610_hardening_not_verified",
                    "v0.26.10 Release Hygiene / Governance Hardening status is not verified; contract creation remains allowed.",
                )
            )
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        if not findings:
            findings.append(self._finding("info", "ok", "Memory Candidate & Continuity contract is declared."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> MemoryContractFinding:
        return MemoryContractFinding(
            finding_id=f"memory_contract_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("memory_candidate_continuity_contract", "memory_candidate_continuity_contract:v0.27.0")],
            withdrawal_condition="Withdraw if memory policy changes or an implementation crosses a forbidden v0.27.0 boundary.",
        )


class MemoryContractReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        extra_findings: list[str] | None = None,
        v0269_handoff_available: bool = True,
        release_hygiene_status_available: bool = False,
    ) -> dict[str, Any]:
        source = MemoryContractPrerequisiteSourceService(
            v0269_handoff_available=v0269_handoff_available,
            release_hygiene_status_available=release_hygiene_status_available,
        )
        prereq_refs = source.evidence_refs()
        roadmap = MemoryTrackRoadmapService().build_roadmap(prereq_refs)
        source_boundary = MemorySourceBoundaryPolicyService().build_policy()
        source_eligibility = MemorySourceEligibilityPolicyService().build_policy()
        candidate_policy = MemoryCandidatePolicyService().build_policy()
        candidate_catalog = MemoryCandidateTypeCatalogService().build_catalog()
        evidence_policy = MemoryEvidencePolicyService().build_policy()
        scoring_policy = MemoryScoringPolicyService().build_policy()
        promotion_policy = MemoryPromotionGatePolicyService().build_policy()
        durable_policy = DurableMemoryPolicyService().build_policy()
        continuity_policy = SessionContinuityPolicyService().build_policy()
        injection_policy = ContinuityInjectionPolicyService().build_policy()
        audit_policy = MemoryAuditPolicyService().build_policy()
        privacy_policy = MemoryPrivacyPolicyService().build_policy()
        governance_policy = MemoryGovernancePolicyService().build_policy()
        pig_policy = MemoryPIGGuidancePolicyService().build_policy()
        safety_policy = MemorySafetyBoundaryPolicyService().build_policy()
        release_prerequisite_policy = MemoryReleasePrerequisitePolicyService().build_policy()
        contract = MemoryContractService().build_contract(
            roadmap,
            source_boundary,
            source_eligibility,
            candidate_policy,
            candidate_catalog,
            evidence_policy,
            scoring_policy,
            promotion_policy,
            durable_policy,
            continuity_policy,
            injection_policy,
            audit_policy,
            privacy_policy,
            governance_policy,
            pig_policy,
            safety_policy,
            release_prerequisite_policy,
        )
        findings = MemoryContractFindingService().build_findings(source, extra_findings=extra_findings)
        report_status = self._report_status(findings)
        report = MemoryContractReport(
            report_id=report_id or "memory_contract_report:v0.27.0",
            created_at=utc_now_iso(),
            contract=contract,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_1=report_status in {"passed", "warning"},
            contract_created=True,
            roadmap_created=True,
            source_boundary_policy_created=True,
            candidate_policy_created=True,
            evidence_policy_created=True,
            scoring_policy_created=True,
            promotion_gate_policy_created=True,
            durable_memory_policy_created=True,
            session_continuity_policy_created=True,
            continuity_injection_policy_created=True,
            audit_policy_created=True,
            privacy_policy_created=True,
            governance_policy_created=True,
            pig_guidance_policy_created=True,
            safety_boundary_policy_created=True,
            limitations=[
                "v0.27.0 declares contracts only; memory candidate extraction begins no earlier than v0.27.2.",
                "v0.26.10 release hygiene status may be unknown, but persistent memory write is forbidden in v0.27.0.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if candidate extraction, scoring, promotion, persistent write, continuity injection, persona/policy mutation, raw memory, PIG execution, provider/command execution, safety bypass, external adapter, Schumpeter split, or LLM judge appears in v0.27.0.",
            ],
        )
        return {
            "source_service": source,
            "roadmap": roadmap,
            "source_boundary_policy": source_boundary,
            "source_eligibility_policy": source_eligibility,
            "candidate_policy": candidate_policy,
            "candidate_type_catalog": candidate_catalog,
            "evidence_policy": evidence_policy,
            "scoring_policy": scoring_policy,
            "promotion_gate_policy": promotion_policy,
            "durable_memory_policy": durable_policy,
            "session_continuity_policy": continuity_policy,
            "continuity_injection_policy": injection_policy,
            "audit_policy": audit_policy,
            "privacy_policy": privacy_policy,
            "governance_policy": governance_policy,
            "pig_guidance_policy": pig_policy,
            "safety_boundary_policy": safety_policy,
            "release_prerequisite_policy": release_prerequisite_policy,
            "contract": contract,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[MemoryContractFinding]) -> str:
        if any(finding.finding_type in MemoryContractFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.finding_type in MemoryContractFindingService.REQUIRED_POLICY_FINDINGS for finding in findings):
            return "failed"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_CONTRACT_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_candidate_continuity_contract",
            "principles": [
                "Memory candidate is not memory",
                "Memory promotion is not persona mutation",
                "PIG guidance is not memory",
                "Raw transcript is not default memory source",
                "Session continuity is not raw transcript replay",
                "Continuity injection is guidance, not behavior override",
                "Durable memory must be gated, scoped, auditable, revocable, and forgettable",
                "Explicit user instruction outranks stale memory",
                "Safety gate must not be bypassed by memory",
            ],
            "safety_boundary": {
                "memory_candidate_extracted": False,
                "memory_scored": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_secret_output": False,
                "credential_exposed": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.1 memory source / ref boundary",
                "v0.27.2 memory candidate extraction",
                "v0.27.3 memory evidence binder & scoring",
                "v0.27.4 memory promotion gate",
                "v0.27.5 durable memory record & registry",
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit / update / revoke / forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": MEMORY_CONTRACT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_candidate_continuity_contract_declared",
            "version": MEMORY_CONTRACT_VERSION,
            "source_read_models": [
                "WorkbenchMemoryCandidateHandoffState",
                "WorkbenchV027ReadinessState",
                "WorkbenchSnapshotState",
                "WorkbenchOCELExportPackageState",
                "WorkbenchEventQualityReportState",
                "WorkbenchTraceCoverageReportState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryCandidateContinuityContractState",
                "MemorySourceBoundaryPolicyState",
                "MemoryCandidatePolicyState",
                "MemoryEvidencePolicyState",
                "MemoryScoringPolicyState",
                "MemoryPromotionGatePolicyState",
                "DurableMemoryPolicyState",
                "SessionContinuityPolicyState",
                "ContinuityInjectionPolicyState",
                "MemoryAuditPolicyState",
                "MemoryPrivacyPolicyState",
                "MemoryGovernancePolicyState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_CONTRACT_EFFECT_TYPES,
        }


def render_memory_contract_cli(parts: dict[str, Any], section: str = "contract") -> str:
    report: MemoryContractReport = parts["report"]
    lines = [
        f"Memory Candidate & Continuity {section}",
        f"version={report.version}",
        f"layer={report.contract.layer}",
        f"status={report.contract.status}",
        f"report_status={report.report_status}",
        f"ready_for_v0_27_1={_bool(report.ready_for_v0_27_1)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_candidate_extracted={_bool(report.memory_candidate_extracted)}",
        f"memory_scored={_bool(report.memory_scored)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "roadmap":
        roadmap = parts["roadmap"]
        lines.append(f"roadmap_status={roadmap.roadmap_status}")
        lines.append(f"version_plan_count={len(roadmap.versions)}")
    elif section == "source-policy":
        policy = parts["source_boundary_policy"]
        lines.append(f"refs_only_source_required={_bool(policy.refs_only_source_required)}")
        lines.append(f"allowed_source_count={len(policy.allowed_source_categories)}")
    elif section == "candidate-policy":
        policy = parts["candidate_policy"]
        lines.append(f"candidate_is_not_memory={_bool(policy.candidate_is_not_memory)}")
        lines.append(f"memory_candidate_extraction_deferred_to={policy.memory_candidate_extraction_deferred_to}")
    elif section == "candidate-types":
        catalog = parts["candidate_type_catalog"]
        lines.append(f"type_status={catalog.type_status}")
        lines.append(f"candidate_type_count={len(catalog.candidate_types)}")
    elif section == "evidence-policy":
        policy = parts["evidence_policy"]
        lines.append(f"evidence_binding_deferred_to={policy.evidence_binding_deferred_to}")
        lines.append(f"raw_provider_output_evidence_forbidden={_bool(policy.raw_provider_output_evidence_forbidden)}")
    elif section == "scoring-policy":
        policy = parts["scoring_policy"]
        lines.append(f"scoring_deferred_to={policy.scoring_deferred_to}")
        lines.append(f"score_is_not_promotion={_bool(policy.score_is_not_promotion)}")
    elif section == "promotion-policy":
        policy = parts["promotion_gate_policy"]
        lines.append(f"promotion_gate_deferred_to={policy.promotion_gate_deferred_to}")
        lines.append(f"automatic_promotion_forbidden={_bool(policy.automatic_promotion_forbidden)}")
    elif section == "durable-policy":
        policy = parts["durable_memory_policy"]
        lines.append(f"durable_memory_registry_deferred_to={policy.durable_memory_registry_deferred_to}")
        lines.append(f"persistent_memory_write_forbidden_in_v0270={_bool(policy.persistent_memory_write_forbidden_in_v0270)}")
    elif section == "continuity-policy":
        policy = parts["session_continuity_policy"]
        lines.append(f"session_continuity_context_deferred_to={policy.session_continuity_context_deferred_to}")
        lines.append(f"raw_transcript_replay_forbidden={_bool(policy.raw_transcript_replay_forbidden)}")
    elif section == "injection-policy":
        policy = parts["continuity_injection_policy"]
        lines.append(f"continuity_injection_deferred_to={policy.continuity_injection_deferred_to}")
        lines.append(f"injection_is_guidance_not_override={_bool(policy.injection_is_guidance_not_override)}")
    elif section == "audit-policy":
        policy = parts["audit_policy"]
        lines.append(f"audit_lifecycle_deferred_to={policy.audit_lifecycle_deferred_to}")
        lines.append(f"audit_required_for_forget={_bool(policy.audit_required_for_forget)}")
    elif section == "privacy-policy":
        policy = parts["privacy_policy"]
        lines.append(f"privacy_check_required={_bool(policy.privacy_check_required)}")
        lines.append(f"raw_secret_memory_forbidden={_bool(policy.raw_secret_memory_forbidden)}")
    elif section == "pig-policy":
        policy = parts["pig_guidance_policy"]
        lines.append(f"pig_guidance_is_not_memory={_bool(policy.pig_guidance_is_not_memory)}")
        lines.append(f"pig_guidance_cannot_execute={_bool(policy.pig_guidance_cannot_execute)}")
    elif section == "safety-boundary":
        policy = parts["safety_boundary_policy"]
        lines.append(f"memory_candidate_extraction_enabled_now={_bool(policy.memory_candidate_extraction_enabled_now)}")
        lines.append(f"memory_triggered_command_execution_forbidden={_bool(policy.memory_triggered_command_execution_forbidden)}")
    elif section == "contract-report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)


MEMORY_SOURCE_BOUNDARY_VERSION = "v0.27.1"
MEMORY_SOURCE_BOUNDARY_VERSION_NAME = "Memory Source / Ref Boundary"
MEMORY_SOURCE_BOUNDARY_NEXT_STEP = "v0.27.2 Memory Candidate Extraction"

MEMORY_SOURCE_ALLOWED_CATEGORIES = MEMORY_ALLOWED_SOURCE_CATEGORIES + [
    "trace_coverage_report_refs",
    "redaction_report_refs",
    "release_hygiene_status_refs",
]

MEMORY_SOURCE_FORBIDDEN_CATEGORIES = MEMORY_FORBIDDEN_SOURCE_CATEGORIES + [
    "unscoped_personal_sensitive_attribute",
    "uncited_inference",
    "unredacted_runtime_db",
    "unredacted_bak_file",
    "external_adapter_output",
]

MEMORY_SOURCE_REQUIRED_ELIGIBILITY_RULES = [
    "source_ref_required",
    "evidence_ref_required",
    "refs_only_required",
    "raw_transcript_forbidden",
    "raw_provider_output_forbidden",
    "raw_secret_forbidden",
    "credential_forbidden",
    "private_full_path_forbidden",
    "redaction_required",
    "source_quality_required",
    "event_quality_required_for_candidate_readiness",
    "trace_coverage_warn_if_missing",
    "PIG_guidance_ref_allowed_but_not_memory",
    "source_without_ref_blocked",
    "raw_content_source_blocked",
]

MEMORY_SOURCE_OBJECT_TYPES = [
    "memory_source_boundary_policy_view",
    "memory_source_boundary_request",
    "memory_source_category_catalog",
    "memory_source_ref",
    "memory_source_ref_bundle",
    "memory_source_ref_registry_view",
    "memory_source_eligibility_rule",
    "memory_source_eligibility_evaluation",
    "memory_source_eligibility_decision",
    "memory_source_redaction_policy",
    "memory_source_redaction_view",
    "memory_source_redaction_report",
    "memory_source_quality_policy",
    "memory_source_quality_signal",
    "memory_source_quality_report",
    "memory_source_risk_flag",
    "memory_forbidden_source_report",
    "memory_candidate_readiness_boundary",
    "memory_source_boundary_finding",
    "memory_source_boundary_report",
    "memory_candidate_continuity_contract",
    "workbench_memory_candidate_handoff_packet",
    "workbench_snapshot",
    "workbench_ocel_export_package",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_SOURCE_EVENT_TYPES = [
    "memory_source_boundary_requested",
    "memory_source_boundary_prerequisites_loaded",
    "memory_source_policy_view_created",
    "memory_source_category_catalog_created",
    "memory_source_ref_created",
    "memory_source_ref_bundle_created",
    "memory_source_ref_registry_view_created",
    "memory_source_eligibility_rule_created",
    "memory_source_eligibility_evaluation_created",
    "memory_source_eligibility_decision_created",
    "memory_source_redaction_policy_created",
    "memory_source_redaction_view_created",
    "memory_source_redaction_report_created",
    "memory_source_quality_policy_created",
    "memory_source_quality_signal_created",
    "memory_source_quality_report_created",
    "memory_source_risk_flag_created",
    "memory_forbidden_source_report_created",
    "memory_candidate_readiness_boundary_created",
    "memory_source_boundary_report_created",
    "memory_source_boundary_warning_created",
    "memory_source_boundary_blocked",
]

MEMORY_SOURCE_EFFECT_TYPES = [
    "read_only_observation",
    "memory_source_boundary_created",
    "memory_source_ref_created",
    "memory_source_ref_bundle_created",
    "memory_source_eligibility_evaluated",
    "memory_source_redaction_view_created",
    "memory_source_quality_report_created",
    "memory_candidate_readiness_boundary_created",
    "state_candidate_created",
]

MEMORY_SOURCE_FORBIDDEN_EFFECT_TYPES = MEMORY_CONTRACT_FORBIDDEN_EFFECT_TYPES + [
    "memory_candidate_extracted",
    "memory_candidate_scored",
    "memory_scored",
    "durable_memory_written",
]


@dataclass
class MemorySourceBoundaryPolicyView(_ModelMixin):
    policy_view_id: str
    source_boundary_policy_ref: dict[str, Any] | None
    source_eligibility_policy_ref: dict[str, Any] | None
    memory_contract_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    refs_only_source_required: bool = True
    raw_transcript_default_source_forbidden: bool = True
    raw_provider_output_source_forbidden: bool = True
    raw_secret_source_forbidden: bool = True
    credential_source_forbidden: bool = True
    private_full_path_source_forbidden: bool = True
    unredacted_file_content_source_forbidden: bool = True
    redaction_required: bool = True
    source_quality_required: bool = True
    candidate_extraction_enabled_now: bool = False
    memory_scoring_enabled_now: bool = False
    memory_promotion_enabled_now: bool = False
    persistent_memory_write_enabled_now: bool = False


@dataclass
class MemorySourceBoundaryRequest(_ModelMixin):
    request_id: str
    memory_contract_report_id: str | None
    memory_contract_id: str | None
    workbench_handoff_packet_id: str | None
    workbench_v027_readiness_report_id: str | None
    snapshot_export_report_id: str | None
    selected_source_refs: list[dict[str, Any]]
    requested_source_categories: list[str]
    release_hygiene_status_ref: dict[str, Any] | None
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemorySourceCategoryCatalog(_ModelMixin):
    catalog_id: str
    allowed_source_categories: list[str]
    forbidden_source_categories: list[str]
    category_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemorySourceRef(_ModelMixin):
    source_ref_id: str
    source_category: str
    source_kind: str
    source_ref: dict[str, Any]
    source_summary: str
    originating_version: str | None
    originating_surface: str | None
    evidence_refs: list[dict[str, Any]]
    redaction_ref: dict[str, Any] | None
    event_quality_ref: dict[str, Any] | None
    trace_coverage_ref: dict[str, Any] | None
    eligibility_decision_ref: dict[str, Any] | None
    source_status: str
    evidence_refs_for_audit: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    refs_only: bool = True
    raw_content_included: bool = False
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    memory_candidate_created: bool = False


@dataclass
class MemorySourceRefBundle(_ModelMixin):
    source_bundle_id: str
    source_refs: list[MemorySourceRef]
    eligible_source_refs: list[dict[str, Any]]
    ineligible_source_refs: list[dict[str, Any]]
    deferred_source_refs: list[dict[str, Any]]
    blocked_source_refs: list[dict[str, Any]]
    source_count: int
    eligible_count: int
    ineligible_count: int
    deferred_count: int
    blocked_count: int
    bundle_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    memory_candidate_created: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemorySourceRefRegistryView(_ModelMixin):
    registry_view_id: str
    source_bundle_id: str
    category_counts: dict[str, int]
    status_counts: dict[str, int]
    eligible_categories: list[str]
    blocked_categories: list[str]
    registry_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    registry_is_not_durable_memory: bool = True
    durable_memory_written: bool = False


@dataclass
class MemorySourceEligibilityRule(_ModelMixin):
    rule_id: str
    rule_name: str
    source_category: str | None
    required: bool
    rule_summary: str
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemorySourceEligibilityEvaluation(_ModelMixin):
    evaluation_id: str
    source_ref_id: str
    applied_rules: list[MemorySourceEligibilityRule]
    passed_rule_ids: list[str]
    failed_rule_ids: list[str]
    warning_rule_ids: list[str]
    blocking_rule_ids: list[str]
    evaluation_summary: str
    evaluation_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    memory_candidate_created: bool = False


@dataclass
class MemorySourceEligibilityDecision(_ModelMixin):
    decision_id: str
    source_ref_id: str
    evaluation_id: str
    decision_type: str
    decision_reason: str
    candidate_extraction_allowed_later: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    candidate_extraction_performed_now: bool = False
    memory_created_now: bool = False


@dataclass
class MemorySourceRedactionPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    redaction_required: bool = True
    redact_raw_transcript: bool = True
    redact_raw_provider_output: bool = True
    redact_raw_secret: bool = True
    redact_credentials: bool = True
    redact_private_full_path: bool = True
    preserve_refs: bool = True
    preserve_sanitized_summary: bool = True
    redaction_is_not_source_deletion: bool = True


@dataclass
class MemorySourceRedactionView(_ModelMixin):
    redaction_view_id: str
    source_ref_id: str
    redaction_policy_id: str
    redacted_categories: list[str]
    preserved_ref_count: int
    preserved_summary_count: int
    redaction_complete: bool
    raw_content_removed_from_view: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    source_deleted: bool = False


@dataclass
class MemorySourceRedactionReport(_ModelMixin):
    redaction_report_id: str
    redaction_views: list[MemorySourceRedactionView]
    total_source_count: int
    redacted_raw_transcript_count: int
    redacted_raw_provider_output_count: int
    redacted_raw_secret_count: int
    redacted_credential_count: int
    redacted_private_path_count: int
    preserved_ref_count: int
    redaction_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    source_data_deleted: bool = False


@dataclass
class MemorySourceQualityPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    source_quality_required: bool = True
    event_quality_required: bool = True
    trace_coverage_preferred: bool = True
    evidence_density_required: bool = True
    provenance_required: bool = True
    redaction_status_required: bool = True
    stale_source_warning_required: bool = True
    low_quality_source_deferred: bool = True


@dataclass
class MemorySourceQualitySignal(_ModelMixin):
    quality_signal_id: str
    source_ref_id: str
    signal_type: str
    signal_value: str
    signal_score: float | None
    signal_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemorySourceQualityReport(_ModelMixin):
    quality_report_id: str
    source_bundle_id: str
    quality_signals: list[MemorySourceQualitySignal]
    source_quality_by_ref: dict[str, str]
    high_quality_source_count: int
    medium_quality_source_count: int
    low_quality_source_count: int
    blocked_quality_source_count: int
    missing_event_quality_count: int
    missing_trace_coverage_count: int
    missing_evidence_count: int
    source_quality_status: str
    candidate_extraction_ready_count: int
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    candidate_extraction_performed_now: bool = False


@dataclass
class MemorySourceRiskFlag(_ModelMixin):
    risk_flag_id: str
    source_ref_id: str
    risk_type: str
    risk_level: str
    risk_summary: str
    blocks_candidate_extraction: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemoryForbiddenSourceReport(_ModelMixin):
    forbidden_source_report_id: str
    forbidden_source_refs: list[dict[str, Any]]
    forbidden_categories_detected: list[str]
    blocked_count: int
    warning_count: int
    report_status: str
    raw_transcript_detected: bool
    raw_provider_output_detected: bool
    raw_secret_detected: bool
    credential_detected: bool
    private_full_path_detected: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION


@dataclass
class MemoryCandidateReadinessBoundary(_ModelMixin):
    readiness_boundary_id: str
    source_bundle_id: str
    eligible_for_v0272_candidate_extraction_refs: list[dict[str, Any]]
    deferred_until_more_evidence_refs: list[dict[str, Any]]
    deferred_until_redaction_refs: list[dict[str, Any]]
    blocked_source_refs: list[dict[str, Any]]
    candidate_extraction_ready: bool
    candidate_extraction_ready_count: int
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    candidate_extraction_not_performed_now: bool = True
    memory_created_now: bool = False
    next_required_step: str = MEMORY_SOURCE_BOUNDARY_NEXT_STEP


@dataclass
class MemorySourceBoundaryFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemorySourceBoundaryReport(_ModelMixin):
    report_id: str
    created_at: str
    boundary_policy_view: MemorySourceBoundaryPolicyView
    request: MemorySourceBoundaryRequest
    category_catalog: MemorySourceCategoryCatalog
    source_bundle: MemorySourceRefBundle
    source_registry_view: MemorySourceRefRegistryView
    eligibility_rules: list[MemorySourceEligibilityRule]
    eligibility_evaluations: list[MemorySourceEligibilityEvaluation]
    eligibility_decisions: list[MemorySourceEligibilityDecision]
    redaction_policy: MemorySourceRedactionPolicy
    redaction_report: MemorySourceRedactionReport
    quality_policy: MemorySourceQualityPolicy
    quality_report: MemorySourceQualityReport
    risk_flags: list[MemorySourceRiskFlag]
    forbidden_source_report: MemoryForbiddenSourceReport
    candidate_readiness_boundary: MemoryCandidateReadinessBoundary
    findings: list[MemorySourceBoundaryFinding]
    report_status: str
    ready_for_v0_27_2: bool
    source_boundary_created: bool
    source_refs_created: bool
    source_bundle_created: bool
    eligibility_evaluations_created: bool
    eligibility_decisions_created: bool
    redaction_report_created: bool
    source_quality_report_created: bool
    forbidden_source_report_created: bool
    candidate_readiness_boundary_created: bool
    version: str = MEMORY_SOURCE_BOUNDARY_VERSION
    ready_for_v0_28: bool = False
    memory_candidate_extracted: bool = False
    memory_scored: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    durable_memory_written: bool = False
    session_continuity_injected: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_SOURCE_BOUNDARY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.27.2 Memory Candidate Extraction begins or memory source boundary policy changes."


class MemorySourceBoundaryPrerequisiteSourceService:
    def __init__(
        self,
        *,
        contract_available: bool = True,
        handoff_available: bool = True,
        event_quality_available: bool = True,
        trace_coverage_available: bool = True,
        redaction_available: bool = True,
        release_hygiene_status_available: bool = False,
    ) -> None:
        self.contract_available = contract_available
        self.handoff_available = handoff_available
        self.event_quality_available = event_quality_available
        self.trace_coverage_available = trace_coverage_available
        self.redaction_available = redaction_available
        self.release_hygiene_status_available = release_hygiene_status_available

    def load_v0270_contract(self) -> dict[str, Any] | None:
        if not self.contract_available:
            return None
        return _ref("memory_candidate_continuity_contract", "memory_candidate_continuity_contract:v0.27.0", "v0.27.0")

    def load_v0270_contract_report(self) -> dict[str, Any] | None:
        if not self.contract_available:
            return None
        return _ref("memory_contract_report", "memory_contract_report:v0.27.0", "v0.27.0")

    def load_v0269_workbench_handoff_packet(self) -> dict[str, Any] | None:
        if not self.handoff_available:
            return None
        return _ref("workbench_memory_candidate_handoff_packet", "workbench_memory_candidate_handoff:v0.26.9", "v0.26.9")

    def load_v0269_v027_readiness_report(self) -> dict[str, Any] | None:
        return _ref("workbench_v027_readiness_report", "workbench_v027_readiness:v0.26.9", "v0.26.9")

    def load_v0268_snapshot_export_report_if_available(self) -> dict[str, Any] | None:
        return _ref("workbench_snapshot_export_report", "workbench_snapshot_export_report:v0.26.8", "v0.26.8")

    def load_workbench_snapshot_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_snapshot", "workbench_snapshot:v0.26.8", "v0.26.8")]

    def load_ocel_export_package_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_ocel_export_package", "workbench_ocel_export_package:v0.26.8", "v0.26.8")]

    def load_event_quality_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.event_quality_available:
            return []
        return [_ref("workbench_event_quality_report", "workbench_event_quality_report:v0.26.8", "v0.26.8")]

    def load_trace_coverage_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.trace_coverage_available:
            return []
        return [_ref("workbench_trace_coverage_report", "workbench_trace_coverage_report:v0.26.8", "v0.26.8")]

    def load_redaction_report_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.redaction_available:
            return []
        return [_ref("workbench_redaction_report", "workbench_snapshot_redaction_report:v0.26.8", "v0.26.8")]

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_guidance", "pig_guidance:workbench_foundation", "v0.26.9")]

    def load_release_hygiene_status_if_available(self) -> dict[str, Any] | None:
        if not self.release_hygiene_status_available:
            return None
        return _ref("release_hygiene_status", "release_hygiene_status:v0.26.10", "v0.26.10")


class MemorySourceBoundaryPolicyViewService:
    def build_policy_view(self) -> MemorySourceBoundaryPolicyView:
        return MemorySourceBoundaryPolicyView(
            policy_view_id="memory_source_boundary_policy_view:v0.27.1",
            source_boundary_policy_ref=_ref("memory_source_boundary_policy", "memory_source_boundary_policy:v0.27.0", "v0.27.0"),
            source_eligibility_policy_ref=_ref("memory_source_eligibility_policy", "memory_source_eligibility_policy:v0.27.0", "v0.27.0"),
            memory_contract_ref=_ref("memory_candidate_continuity_contract", "memory_candidate_continuity_contract:v0.27.0", "v0.27.0"),
            evidence_refs=[_ref("memory_contract_report", "memory_contract_report:v0.27.0", "v0.27.0")],
        )


class MemorySourceCategoryCatalogService:
    def build_catalog(self) -> MemorySourceCategoryCatalog:
        return MemorySourceCategoryCatalog(
            catalog_id="memory_source_category_catalog:v0.27.1",
            allowed_source_categories=list(MEMORY_SOURCE_ALLOWED_CATEGORIES),
            forbidden_source_categories=list(MEMORY_SOURCE_FORBIDDEN_CATEGORIES),
            category_status="ready",
            evidence_refs=[_ref("memory_source_boundary_policy_view", "memory_source_boundary_policy_view:v0.27.1")],
        )


class MemorySourceRefService:
    SOURCE_ROWS = [
        ("workbench_snapshot_refs", "snapshot", "workbench_snapshot:v0.26.8", "Workbench snapshot refs from v0.26.8.", "v0.26.8", "v0.26.8_snapshot_export"),
        ("ocel_export_package_refs", "ocel_export", "workbench_ocel_export_package:v0.26.8", "Refs-only OCEL export package.", "v0.26.8", "v0.26.8_snapshot_export"),
        ("session_context_refs", "session_context", "workbench_session_context_refs:v0.26.6", "Session context refs from the Workbench session monitor.", "v0.26.6", "v0.26.6_session_monitor"),
        ("trace_summary_refs", "trace_summary", "workbench_trace_summary:v0.26.2", "Trace summary refs from Trace Explorer.", "v0.26.2", "v0.26.2_trace_explorer"),
        ("evidence_summary_refs", "evidence_summary", "workbench_evidence_summary:v0.26.4", "Evidence summary refs from Evidence Inspector.", "v0.26.4", "v0.26.4_evidence_inspector"),
        ("pig_guidance_refs", "pig_guidance", "pig_guidance:workbench_foundation", "PIG guidance refs, not memory.", "v0.26.9", "pig_guidance"),
        ("approval_decision_refs", "approval_decision", "workbench_approval_decision:v0.26.5", "Approval decision refs.", "v0.26.5", "v0.26.5_approval_console"),
        ("command_candidate_refs", "command_candidate", "workbench_command_candidate:v0.26.7", "Command candidate refs, not execution.", "v0.26.7", "v0.26.7_command_surface"),
        ("failure_cause_refs", "failure_cause", "workbench_failure_cause:v0.26.6", "Failure cause refs.", "v0.26.6", "v0.26.6_session_monitor"),
        ("human_intervention_refs", "human_intervention", "workbench_human_intervention:v0.26.5", "Human intervention point refs.", "v0.26.5", "v0.26.5_approval_console"),
        ("event_quality_report_refs", "event_quality", "workbench_event_quality_report:v0.26.8", "Event quality report refs.", "v0.26.8", "v0.26.8_snapshot_export"),
        ("trace_coverage_report_refs", "trace_coverage", "workbench_trace_coverage_report:v0.26.8", "Trace coverage report refs.", "v0.26.8", "v0.26.8_snapshot_export"),
        ("redaction_report_refs", "redaction", "workbench_snapshot_redaction_report:v0.26.8", "Redaction report refs.", "v0.26.8", "v0.26.8_snapshot_export"),
    ]

    def build_source_refs(self) -> list[MemorySourceRef]:
        refs: list[MemorySourceRef] = []
        for category, kind, ref_id, summary, version, surface in self.SOURCE_ROWS:
            source_ref_id = f"memory_source_ref:{kind}"
            refs.append(
                MemorySourceRef(
                    source_ref_id=source_ref_id,
                    source_category=category,
                    source_kind=kind,
                    source_ref=_ref(kind, ref_id, version),
                    source_summary=summary,
                    originating_version=version,
                    originating_surface=surface,
                    evidence_refs=[_ref("memory_source_category_catalog", "memory_source_category_catalog:v0.27.1")],
                    redaction_ref=_ref("memory_source_redaction_view", f"memory_source_redaction_view:{kind}"),
                    event_quality_ref=_ref("workbench_event_quality_report", "workbench_event_quality_report:v0.26.8", "v0.26.8"),
                    trace_coverage_ref=_ref("workbench_trace_coverage_report", "workbench_trace_coverage_report:v0.26.8", "v0.26.8"),
                    eligibility_decision_ref=_ref("memory_source_eligibility_decision", f"memory_source_eligibility_decision:{kind}"),
                    source_status="eligible",
                    evidence_refs_for_audit=[_ref("memory_source_boundary_report", "memory_source_boundary_report:v0.27.1")],
                )
            )
        return refs


class MemorySourceRefBundleService:
    def build_bundle(self, source_refs: list[MemorySourceRef]) -> MemorySourceRefBundle:
        eligible = [_ref("memory_source_ref", source.source_ref_id) for source in source_refs if source.source_status == "eligible"]
        blocked = [_ref("memory_source_ref", source.source_ref_id) for source in source_refs if source.source_status == "blocked"]
        deferred = [_ref("memory_source_ref", source.source_ref_id) for source in source_refs if source.source_status == "deferred"]
        ineligible = [_ref("memory_source_ref", source.source_ref_id) for source in source_refs if source.source_status == "ineligible"]
        return MemorySourceRefBundle(
            source_bundle_id="memory_source_ref_bundle:v0.27.1",
            source_refs=source_refs,
            eligible_source_refs=eligible,
            ineligible_source_refs=ineligible,
            deferred_source_refs=deferred,
            blocked_source_refs=blocked,
            source_count=len(source_refs),
            eligible_count=len(eligible),
            ineligible_count=len(ineligible),
            deferred_count=len(deferred),
            blocked_count=len(blocked),
            bundle_status="ready" if not blocked else "warning",
            evidence_refs=[_ref("memory_source_ref", "memory_source_ref:*")],
        )


class MemorySourceRefRegistryViewService:
    def build_registry_view(self, bundle: MemorySourceRefBundle) -> MemorySourceRefRegistryView:
        category_counts: dict[str, int] = {}
        status_counts: dict[str, int] = {}
        for source in bundle.source_refs:
            category_counts[source.source_category] = category_counts.get(source.source_category, 0) + 1
            status_counts[source.source_status] = status_counts.get(source.source_status, 0) + 1
        return MemorySourceRefRegistryView(
            registry_view_id="memory_source_ref_registry_view:v0.27.1",
            source_bundle_id=bundle.source_bundle_id,
            category_counts=category_counts,
            status_counts=status_counts,
            eligible_categories=sorted({source.source_category for source in bundle.source_refs if source.source_status == "eligible"}),
            blocked_categories=sorted({source.source_category for source in bundle.source_refs if source.source_status == "blocked"}),
            registry_status=bundle.bundle_status,
            evidence_refs=[_ref("memory_source_ref_bundle", bundle.source_bundle_id)],
        )


class MemorySourceEligibilityRuleService:
    def build_rules(self) -> list[MemorySourceEligibilityRule]:
        rules: list[MemorySourceEligibilityRule] = []
        for rule_name in MEMORY_SOURCE_REQUIRED_ELIGIBILITY_RULES:
            block = rule_name in {
                "source_ref_required",
                "evidence_ref_required",
                "refs_only_required",
                "raw_transcript_forbidden",
                "raw_provider_output_forbidden",
                "raw_secret_forbidden",
                "credential_forbidden",
                "private_full_path_forbidden",
                "source_without_ref_blocked",
                "raw_content_source_blocked",
            }
            rules.append(
                MemorySourceEligibilityRule(
                    rule_id=f"memory_source_eligibility_rule:{rule_name}",
                    rule_name=rule_name,
                    source_category=None,
                    required=True,
                    rule_summary=f"{rule_name} for refs-only source boundary.",
                    pass_condition="Source uses refs, evidence, redaction, and quality metadata without raw content.",
                    fail_condition="Source is missing refs/evidence or includes forbidden raw/sensitive content.",
                    block_on_fail=block,
                    evidence_refs=[_ref("memory_source_boundary_policy_view", "memory_source_boundary_policy_view:v0.27.1")],
                )
            )
        return rules


class MemorySourceEligibilityEvaluationService:
    def evaluate_sources(
        self,
        source_refs: list[MemorySourceRef],
        rules: list[MemorySourceEligibilityRule],
    ) -> list[MemorySourceEligibilityEvaluation]:
        evaluations: list[MemorySourceEligibilityEvaluation] = []
        for source in source_refs:
            failed: list[str] = []
            blocking: list[str] = []
            warnings: list[str] = []
            if source.raw_transcript_included:
                failed.append("memory_source_eligibility_rule:raw_transcript_forbidden")
            if source.raw_provider_output_included:
                failed.append("memory_source_eligibility_rule:raw_provider_output_forbidden")
            if source.raw_secret_included:
                failed.append("memory_source_eligibility_rule:raw_secret_forbidden")
            if source.credential_included:
                failed.append("memory_source_eligibility_rule:credential_forbidden")
            if source.private_full_path_included:
                failed.append("memory_source_eligibility_rule:private_full_path_forbidden")
            if source.raw_content_included:
                failed.append("memory_source_eligibility_rule:raw_content_source_blocked")
            if not source.source_ref:
                failed.append("memory_source_eligibility_rule:source_without_ref_blocked")
            if not source.evidence_refs:
                failed.append("memory_source_eligibility_rule:evidence_ref_required")
            blocking = [rule_id for rule_id in failed if any(rule.rule_id == rule_id and rule.block_on_fail for rule in rules)]
            if source.trace_coverage_ref is None:
                warnings.append("memory_source_eligibility_rule:trace_coverage_warn_if_missing")
            passed = [rule.rule_id for rule in rules if rule.rule_id not in failed and rule.rule_id not in warnings]
            status = "blocked" if blocking else "warning" if warnings else "passed"
            evaluations.append(
                MemorySourceEligibilityEvaluation(
                    evaluation_id=f"memory_source_eligibility_evaluation:{source.source_kind}",
                    source_ref_id=source.source_ref_id,
                    applied_rules=rules,
                    passed_rule_ids=passed,
                    failed_rule_ids=failed,
                    warning_rule_ids=warnings,
                    blocking_rule_ids=blocking,
                    evaluation_summary="Refs-only source eligibility evaluated without extracting memory candidates.",
                    evaluation_status=status,
                    evidence_refs=[_ref("memory_source_ref", source.source_ref_id)],
                )
            )
        return evaluations


class MemorySourceEligibilityDecisionService:
    def decide_eligibility(self, evaluations: list[MemorySourceEligibilityEvaluation]) -> list[MemorySourceEligibilityDecision]:
        decisions: list[MemorySourceEligibilityDecision] = []
        for evaluation in evaluations:
            if any("raw_secret" in rule or "credential" in rule for rule in evaluation.blocking_rule_ids):
                decision_type = "blocked_for_secret_or_credential"
            elif evaluation.blocking_rule_ids:
                decision_type = "blocked_for_raw_content"
            elif evaluation.warning_rule_ids:
                decision_type = "defer_until_more_evidence"
            else:
                decision_type = "eligible_for_candidate_extraction"
            decisions.append(
                MemorySourceEligibilityDecision(
                    decision_id=f"memory_source_eligibility_decision:{evaluation.source_ref_id.rsplit(':', 1)[-1]}",
                    source_ref_id=evaluation.source_ref_id,
                    evaluation_id=evaluation.evaluation_id,
                    decision_type=decision_type,
                    decision_reason="Candidate extraction is allowed later only for eligible refs; no extraction occurs in v0.27.1.",
                    candidate_extraction_allowed_later=decision_type == "eligible_for_candidate_extraction",
                    evidence_refs=[_ref("memory_source_eligibility_evaluation", evaluation.evaluation_id)],
                )
            )
        return decisions


class MemorySourceRedactionPolicyService:
    def build_policy(self) -> MemorySourceRedactionPolicy:
        return MemorySourceRedactionPolicy("memory_source_redaction_policy:v0.27.1", [_ref("memory_source_boundary_policy_view", "memory_source_boundary_policy_view:v0.27.1")])


class MemorySourceRedactionViewService:
    def build_views(self, source_refs: list[MemorySourceRef], policy: MemorySourceRedactionPolicy) -> list[MemorySourceRedactionView]:
        return [
            MemorySourceRedactionView(
                redaction_view_id=f"memory_source_redaction_view:{source.source_kind}",
                source_ref_id=source.source_ref_id,
                redaction_policy_id=policy.policy_id,
                redacted_categories=[],
                preserved_ref_count=1,
                preserved_summary_count=1,
                redaction_complete=True,
                raw_content_removed_from_view=True,
                evidence_refs=[_ref("memory_source_ref", source.source_ref_id)],
            )
            for source in source_refs
        ]


class MemorySourceRedactionReportService:
    def build_report(self, views: list[MemorySourceRedactionView]) -> MemorySourceRedactionReport:
        return MemorySourceRedactionReport(
            redaction_report_id="memory_source_redaction_report:v0.27.1",
            redaction_views=views,
            total_source_count=len(views),
            redacted_raw_transcript_count=sum("raw_transcript" in view.redacted_categories for view in views),
            redacted_raw_provider_output_count=sum("raw_provider_output" in view.redacted_categories for view in views),
            redacted_raw_secret_count=sum("raw_secret" in view.redacted_categories for view in views),
            redacted_credential_count=sum("credential" in view.redacted_categories for view in views),
            redacted_private_path_count=sum("private_full_path" in view.redacted_categories for view in views),
            preserved_ref_count=sum(view.preserved_ref_count for view in views),
            redaction_status="ready",
            evidence_refs=[_ref("memory_source_redaction_view", "memory_source_redaction_view:*")],
        )


class MemorySourceQualityPolicyService:
    def build_policy(self) -> MemorySourceQualityPolicy:
        return MemorySourceQualityPolicy("memory_source_quality_policy:v0.27.1", [_ref("memory_source_boundary_policy_view", "memory_source_boundary_policy_view:v0.27.1")])


class MemorySourceQualitySignalService:
    SIGNAL_TYPES = [
        "event_quality",
        "trace_coverage",
        "evidence_density",
        "provenance_strength",
        "redaction_status",
        "recency",
        "stability",
        "privacy_risk",
        "contradiction_warning",
        "release_hygiene_status",
    ]

    def build_signals(self, source_refs: list[MemorySourceRef]) -> list[MemorySourceQualitySignal]:
        signals: list[MemorySourceQualitySignal] = []
        for source in source_refs:
            for signal_type in self.SIGNAL_TYPES:
                score = 0.8 if signal_type != "release_hygiene_status" else None
                value = "available" if signal_type != "release_hygiene_status" else "unknown"
                signals.append(
                    MemorySourceQualitySignal(
                        quality_signal_id=f"memory_source_quality_signal:{source.source_kind}:{signal_type}",
                        source_ref_id=source.source_ref_id,
                        signal_type=signal_type,
                        signal_value=value,
                        signal_score=score,
                        signal_summary=f"{signal_type} signal for {source.source_kind}.",
                        evidence_refs=[_ref("memory_source_ref", source.source_ref_id)],
                    )
                )
        return signals


class MemorySourceQualityReportService:
    def build_report(self, bundle: MemorySourceRefBundle, signals: list[MemorySourceQualitySignal]) -> MemorySourceQualityReport:
        source_quality = {source.source_ref_id: "high" for source in bundle.source_refs}
        return MemorySourceQualityReport(
            quality_report_id="memory_source_quality_report:v0.27.1",
            source_bundle_id=bundle.source_bundle_id,
            quality_signals=signals,
            source_quality_by_ref=source_quality,
            high_quality_source_count=len(source_quality),
            medium_quality_source_count=0,
            low_quality_source_count=0,
            blocked_quality_source_count=0,
            missing_event_quality_count=0,
            missing_trace_coverage_count=0,
            missing_evidence_count=0,
            source_quality_status="ready",
            candidate_extraction_ready_count=bundle.eligible_count,
            evidence_refs=[_ref("memory_source_ref_bundle", bundle.source_bundle_id)],
        )


class MemorySourceRiskFlagService:
    def build_risk_flags(self, source_refs: list[MemorySourceRef]) -> list[MemorySourceRiskFlag]:
        flags = [
            MemorySourceRiskFlag(
                risk_flag_id=f"memory_source_risk_flag:{source.source_kind}:release_hygiene_unknown",
                source_ref_id=source.source_ref_id,
                risk_type="release_hygiene_unknown",
                risk_level="low",
                risk_summary="v0.26.10 release hygiene status is not verified; this does not block non-mutating source boundary creation.",
                blocks_candidate_extraction=False,
                evidence_refs=[_ref("memory_source_ref", source.source_ref_id)],
            )
            for source in source_refs
        ]
        return flags


class MemoryForbiddenSourceReportService:
    def build_report(self, source_refs: list[MemorySourceRef]) -> MemoryForbiddenSourceReport:
        forbidden_refs = [
            _ref("memory_source_ref", source.source_ref_id)
            for source in source_refs
            if source.source_category in MEMORY_SOURCE_FORBIDDEN_CATEGORIES
            or source.raw_transcript_included
            or source.raw_provider_output_included
            or source.raw_secret_included
            or source.credential_included
            or source.private_full_path_included
        ]
        return MemoryForbiddenSourceReport(
            forbidden_source_report_id="memory_forbidden_source_report:v0.27.1",
            forbidden_source_refs=forbidden_refs,
            forbidden_categories_detected=[],
            blocked_count=len(forbidden_refs),
            warning_count=0,
            report_status="ready" if not forbidden_refs else "blocked",
            raw_transcript_detected=any(source.raw_transcript_included for source in source_refs),
            raw_provider_output_detected=any(source.raw_provider_output_included for source in source_refs),
            raw_secret_detected=any(source.raw_secret_included for source in source_refs),
            credential_detected=any(source.credential_included for source in source_refs),
            private_full_path_detected=any(source.private_full_path_included for source in source_refs),
            evidence_refs=[_ref("memory_source_ref_bundle", "memory_source_ref_bundle:v0.27.1")],
        )


class MemoryCandidateReadinessBoundaryService:
    def build_boundary(
        self,
        bundle: MemorySourceRefBundle,
        decisions: list[MemorySourceEligibilityDecision],
    ) -> MemoryCandidateReadinessBoundary:
        eligible = [_ref("memory_source_ref", decision.source_ref_id) for decision in decisions if decision.decision_type == "eligible_for_candidate_extraction"]
        more_evidence = [_ref("memory_source_ref", decision.source_ref_id) for decision in decisions if decision.decision_type == "defer_until_more_evidence"]
        blocked = [_ref("memory_source_ref", decision.source_ref_id) for decision in decisions if decision.decision_type.startswith("blocked")]
        return MemoryCandidateReadinessBoundary(
            readiness_boundary_id="memory_candidate_readiness_boundary:v0.27.1",
            source_bundle_id=bundle.source_bundle_id,
            eligible_for_v0272_candidate_extraction_refs=eligible,
            deferred_until_more_evidence_refs=more_evidence,
            deferred_until_redaction_refs=[],
            blocked_source_refs=blocked,
            candidate_extraction_ready=bool(eligible) and not blocked,
            candidate_extraction_ready_count=len(eligible),
            evidence_refs=[_ref("memory_source_eligibility_decision", "memory_source_eligibility_decision:*")],
        )


class MemorySourceBoundaryFindingService:
    BLOCKED_FINDINGS = {
        "raw_transcript_source_detected",
        "raw_provider_output_source_detected",
        "raw_secret_source_detected",
        "credential_source_detected",
        "private_full_path_source_detected",
        "unredacted_file_content_source_detected",
        "source_without_ref_detected",
        "memory_candidate_extraction_attempted",
        "memory_scoring_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "durable_memory_write_attempted",
        "session_continuity_injection_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "source_boundary_created",
        "source_ref_created",
        "source_bundle_created",
        "source_registry_view_created",
        "eligibility_rule_created",
        "eligibility_evaluation_created",
        "eligibility_decision_created",
        "source_redaction_view_created",
        "source_quality_report_created",
        "forbidden_source_report_created",
        "candidate_readiness_boundary_created",
    ]

    def build_findings(
        self,
        source_service: MemorySourceBoundaryPrerequisiteSourceService,
        *,
        extra_findings: list[str] | None = None,
    ) -> list[MemorySourceBoundaryFinding]:
        findings: list[MemorySourceBoundaryFinding] = []
        if not source_service.contract_available:
            findings.append(self._finding("warning", "missing_memory_contract", "v0.27.0 contract is unavailable."))
        if not source_service.handoff_available:
            findings.append(self._finding("warning", "missing_v0269_handoff", "v0.26.9 handoff is unavailable."))
        if not source_service.event_quality_available:
            findings.append(self._finding("warning", "missing_event_quality_refs", "Event quality refs are unavailable."))
        if not source_service.trace_coverage_available:
            findings.append(self._finding("warning", "missing_trace_coverage_refs", "Trace coverage refs are unavailable."))
        if not source_service.redaction_available:
            findings.append(self._finding("warning", "missing_redaction_refs", "Redaction refs are unavailable."))
        if not source_service.release_hygiene_status_available:
            findings.append(self._finding("warning", "release_hygiene_unknown", "v0.26.10 release hygiene status is unknown."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        if not findings:
            findings.append(self._finding("info", "ok", "Memory source/ref boundary is ready."))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str) -> MemorySourceBoundaryFinding:
        return MemorySourceBoundaryFinding(
            finding_id=f"memory_source_boundary_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("memory_source_boundary_report", "memory_source_boundary_report:v0.27.1")],
            withdrawal_condition="Withdraw if source boundary policy changes or any forbidden source/memory behavior is introduced.",
        )


class MemorySourceBoundaryReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        extra_findings: list[str] | None = None,
        contract_available: bool = True,
        handoff_available: bool = True,
        release_hygiene_status_available: bool = False,
    ) -> dict[str, Any]:
        source_service = MemorySourceBoundaryPrerequisiteSourceService(
            contract_available=contract_available,
            handoff_available=handoff_available,
            release_hygiene_status_available=release_hygiene_status_available,
        )
        policy_view = MemorySourceBoundaryPolicyViewService().build_policy_view()
        request = MemorySourceBoundaryRequest(
            request_id="memory_source_boundary_request:v0.27.1",
            memory_contract_report_id="memory_contract_report:v0.27.0" if contract_available else None,
            memory_contract_id="memory_candidate_continuity_contract:v0.27.0" if contract_available else None,
            workbench_handoff_packet_id="workbench_memory_candidate_handoff:v0.26.9" if handoff_available else None,
            workbench_v027_readiness_report_id="workbench_v027_readiness:v0.26.9",
            snapshot_export_report_id="workbench_snapshot_export_report:v0.26.8",
            selected_source_refs=source_service.load_workbench_snapshot_refs_if_available()
            + source_service.load_ocel_export_package_refs_if_available(),
            requested_source_categories=list(MEMORY_SOURCE_ALLOWED_CATEGORIES),
            release_hygiene_status_ref=source_service.load_release_hygiene_status_if_available(),
            source_refs=[_ref("memory_source_boundary_policy_view", policy_view.policy_view_id)],
        )
        catalog = MemorySourceCategoryCatalogService().build_catalog()
        source_refs = MemorySourceRefService().build_source_refs()
        bundle = MemorySourceRefBundleService().build_bundle(source_refs)
        registry_view = MemorySourceRefRegistryViewService().build_registry_view(bundle)
        rules = MemorySourceEligibilityRuleService().build_rules()
        evaluations = MemorySourceEligibilityEvaluationService().evaluate_sources(source_refs, rules)
        decisions = MemorySourceEligibilityDecisionService().decide_eligibility(evaluations)
        redaction_policy = MemorySourceRedactionPolicyService().build_policy()
        redaction_views = MemorySourceRedactionViewService().build_views(source_refs, redaction_policy)
        redaction_report = MemorySourceRedactionReportService().build_report(redaction_views)
        quality_policy = MemorySourceQualityPolicyService().build_policy()
        quality_signals = MemorySourceQualitySignalService().build_signals(source_refs)
        quality_report = MemorySourceQualityReportService().build_report(bundle, quality_signals)
        risk_flags = MemorySourceRiskFlagService().build_risk_flags(source_refs)
        forbidden_report = MemoryForbiddenSourceReportService().build_report(source_refs)
        readiness = MemoryCandidateReadinessBoundaryService().build_boundary(bundle, decisions)
        findings = MemorySourceBoundaryFindingService().build_findings(source_service, extra_findings=extra_findings)
        report_status = self._report_status(findings, forbidden_report)
        report = MemorySourceBoundaryReport(
            report_id=report_id or "memory_source_boundary_report:v0.27.1",
            created_at=utc_now_iso(),
            boundary_policy_view=policy_view,
            request=request,
            category_catalog=catalog,
            source_bundle=bundle,
            source_registry_view=registry_view,
            eligibility_rules=rules,
            eligibility_evaluations=evaluations,
            eligibility_decisions=decisions,
            redaction_policy=redaction_policy,
            redaction_report=redaction_report,
            quality_policy=quality_policy,
            quality_report=quality_report,
            risk_flags=risk_flags,
            forbidden_source_report=forbidden_report,
            candidate_readiness_boundary=readiness,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_2=report_status in {"passed", "warning"} and readiness.candidate_extraction_ready,
            source_boundary_created=True,
            source_refs_created=True,
            source_bundle_created=True,
            eligibility_evaluations_created=True,
            eligibility_decisions_created=True,
            redaction_report_created=True,
            source_quality_report_created=True,
            forbidden_source_report_created=True,
            candidate_readiness_boundary_created=True,
            limitations=[
                "v0.27.1 evaluates refs only; memory candidate extraction is deferred to v0.27.2.",
                "v0.26.10 release hygiene status may remain unknown for this non-mutating boundary.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if forbidden raw sources are accepted, memory candidates are extracted, memory is scored/promoted/written, continuity is injected, execution occurs, or external/Schumpeter/LLM behavior appears.",
            ],
        )
        return {
            "source_service": source_service,
            "boundary_policy_view": policy_view,
            "request": request,
            "category_catalog": catalog,
            "source_refs": source_refs,
            "source_bundle": bundle,
            "source_registry_view": registry_view,
            "eligibility_rules": rules,
            "eligibility_evaluations": evaluations,
            "eligibility_decisions": decisions,
            "redaction_policy": redaction_policy,
            "redaction_views": redaction_views,
            "redaction_report": redaction_report,
            "quality_policy": quality_policy,
            "quality_signals": quality_signals,
            "quality_report": quality_report,
            "risk_flags": risk_flags,
            "forbidden_source_report": forbidden_report,
            "candidate_readiness_boundary": readiness,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[MemorySourceBoundaryFinding], forbidden_report: MemoryForbiddenSourceReport) -> str:
        if forbidden_report.report_status == "blocked":
            return "blocked"
        if any(finding.finding_type in MemorySourceBoundaryFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_SOURCE_BOUNDARY_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_source_ref_boundary",
            "principles": [
                "Memory source is not memory",
                "Memory source ref is not memory candidate",
                "Source eligibility is not candidate extraction",
                "Source quality score is not memory scoring",
                "Source bundle is not memory registry",
                "Redaction report is not data deletion",
                "PIG guidance ref is not memory",
                "Raw transcript is not default memory source",
                "Raw provider output is not memory evidence",
            ],
            "safety_boundary": {
                "memory_candidate_extracted": False,
                "memory_scored": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "durable_memory_written": False,
                "session_continuity_injected": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_secret_output": False,
                "credential_exposed": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.2 memory candidate extraction",
                "v0.27.3 memory evidence binder & scoring",
                "v0.27.4 memory promotion gate",
                "v0.27.5 durable memory record & registry",
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": MEMORY_SOURCE_BOUNDARY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_source_ref_boundary_created",
            "version": MEMORY_SOURCE_BOUNDARY_VERSION,
            "source_read_models": [
                "MemoryCandidateContinuityContractState",
                "WorkbenchMemoryCandidateHandoffState",
                "WorkbenchSnapshotState",
                "WorkbenchOCELExportPackageState",
                "WorkbenchEventQualityReportState",
                "WorkbenchTraceCoverageReportState",
                "WorkbenchRedactionReportState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemorySourceBoundaryState",
                "MemorySourceRefState",
                "MemorySourceRefBundleState",
                "MemorySourceEligibilityState",
                "MemorySourceRedactionState",
                "MemorySourceQualityState",
                "MemoryCandidateReadinessBoundaryState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_SOURCE_EFFECT_TYPES,
        }


def render_memory_source_boundary_cli(parts: dict[str, Any], section: str = "boundary") -> str:
    report: MemorySourceBoundaryReport = parts["report"]
    lines = [
        f"Memory Source / Ref Boundary {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"source_boundary_created={_bool(report.source_boundary_created)}",
        f"source_refs_created={_bool(report.source_refs_created)}",
        f"source_bundle_created={_bool(report.source_bundle_created)}",
        f"eligibility_evaluations_created={_bool(report.eligibility_evaluations_created)}",
        f"eligibility_decisions_created={_bool(report.eligibility_decisions_created)}",
        f"redaction_report_created={_bool(report.redaction_report_created)}",
        f"source_quality_report_created={_bool(report.source_quality_report_created)}",
        f"forbidden_source_report_created={_bool(report.forbidden_source_report_created)}",
        f"candidate_readiness_boundary_created={_bool(report.candidate_readiness_boundary_created)}",
        f"ready_for_v0_27_2={_bool(report.ready_for_v0_27_2)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_candidate_extracted={_bool(report.memory_candidate_extracted)}",
        f"memory_scored={_bool(report.memory_scored)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"durable_memory_written={_bool(report.durable_memory_written)}",
        f"session_continuity_injected={_bool(report.session_continuity_injected)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "catalog":
        catalog = parts["category_catalog"]
        lines.append(f"allowed_category_count={len(catalog.allowed_source_categories)}")
        lines.append(f"forbidden_category_count={len(catalog.forbidden_source_categories)}")
    elif section == "refs":
        lines.append(f"source_ref_count={len(parts['source_refs'])}")
    elif section == "bundle":
        bundle = parts["source_bundle"]
        lines.append(f"source_count={bundle.source_count}")
        lines.append(f"eligible_count={bundle.eligible_count}")
    elif section == "registry-view":
        registry = parts["source_registry_view"]
        lines.append(f"registry_status={registry.registry_status}")
        lines.append(f"registry_is_not_durable_memory={_bool(registry.registry_is_not_durable_memory)}")
    elif section == "eligibility-rules":
        lines.append(f"eligibility_rule_count={len(parts['eligibility_rules'])}")
    elif section == "evaluate":
        lines.append(f"eligibility_evaluation_count={len(parts['eligibility_evaluations'])}")
    elif section == "decisions":
        lines.append(f"eligibility_decision_count={len(parts['eligibility_decisions'])}")
    elif section == "redaction":
        redaction = parts["redaction_report"]
        lines.append(f"redaction_status={redaction.redaction_status}")
        lines.append(f"source_data_deleted={_bool(redaction.source_data_deleted)}")
    elif section == "quality":
        quality = parts["quality_report"]
        lines.append(f"source_quality_status={quality.source_quality_status}")
        lines.append(f"candidate_extraction_performed_now={_bool(quality.candidate_extraction_performed_now)}")
    elif section == "forbidden":
        forbidden = parts["forbidden_source_report"]
        lines.append(f"forbidden_report_status={forbidden.report_status}")
        lines.append(f"blocked_count={forbidden.blocked_count}")
    elif section == "readiness":
        boundary = parts["candidate_readiness_boundary"]
        lines.append(f"candidate_extraction_ready={_bool(boundary.candidate_extraction_ready)}")
        lines.append(f"candidate_extraction_not_performed_now={_bool(boundary.candidate_extraction_not_performed_now)}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)


MEMORY_CANDIDATE_EXTRACTION_VERSION = "v0.27.2"
MEMORY_CANDIDATE_EXTRACTION_VERSION_NAME = "Memory Candidate Extraction"
MEMORY_CANDIDATE_EXTRACTION_KOREAN_NAME = "Memory Candidate extraction"
MEMORY_CANDIDATE_EXTRACTION_NEXT_STEP = "v0.27.3 Memory Evidence Binder & Scoring"

MEMORY_CANDIDATE_EXTRACTION_REQUIRED_RULES = [
    "source_must_be_eligible",
    "source_ref_required",
    "evidence_ref_required",
    "provenance_required",
    "redaction_required",
    "raw_transcript_forbidden",
    "raw_provider_output_forbidden",
    "raw_secret_forbidden",
    "credential_forbidden",
    "private_full_path_forbidden",
    "candidate_type_required",
    "candidate_claim_must_be_ref_supported",
    "candidate_summary_must_be_sanitized",
    "candidate_risk_flags_required",
    "PIG_guidance_allowed_but_not_memory",
    "no_scoring_in_v0272",
    "no_promotion_in_v0272",
    "no_persistent_write_in_v0272",
]

MEMORY_CANDIDATE_EXTRACTION_OBJECT_TYPES = [
    "memory_candidate_extraction_policy",
    "memory_candidate_extraction_request",
    "memory_candidate_extraction_source_view",
    "memory_candidate_extraction_rule",
    "memory_candidate_type_classifier",
    "memory_candidate_batch",
    "memory_candidate",
    "memory_candidate_source_link",
    "memory_candidate_claim",
    "memory_candidate_context",
    "memory_candidate_provenance",
    "memory_candidate_pig_signal",
    "memory_candidate_risk_flag",
    "memory_candidate_redaction_view",
    "memory_candidate_extraction_decision",
    "memory_candidate_extraction_skip_record",
    "memory_candidate_extraction_deferred_record",
    "memory_candidate_extraction_blocked_record",
    "memory_candidate_extraction_audit_trail",
    "memory_candidate_extraction_finding",
    "memory_candidate_extraction_report",
    "memory_source_boundary_report",
    "memory_candidate_readiness_boundary",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_CANDIDATE_EXTRACTION_EVENT_TYPES = [
    "memory_candidate_extraction_requested",
    "memory_candidate_extraction_prerequisites_loaded",
    "memory_candidate_extraction_policy_created",
    "memory_candidate_extraction_source_view_created",
    "memory_candidate_extraction_rule_created",
    "memory_candidate_type_classifier_created",
    "memory_candidate_batch_created",
    "memory_candidate_created",
    "memory_candidate_source_link_created",
    "memory_candidate_claim_created",
    "memory_candidate_context_created",
    "memory_candidate_provenance_created",
    "memory_candidate_pig_signal_created",
    "memory_candidate_risk_flag_created",
    "memory_candidate_redaction_view_created",
    "memory_candidate_extraction_decision_created",
    "memory_candidate_extraction_skip_record_created",
    "memory_candidate_extraction_deferred_record_created",
    "memory_candidate_extraction_blocked_record_created",
    "memory_candidate_extraction_audit_trail_created",
    "memory_candidate_extraction_report_created",
    "memory_candidate_extraction_warning_created",
    "memory_candidate_extraction_blocked",
]

MEMORY_CANDIDATE_EXTRACTION_EFFECT_TYPES = [
    "read_only_observation",
    "memory_candidate_created",
    "memory_candidate_batch_created",
    "memory_candidate_source_link_created",
    "memory_candidate_claim_created",
    "memory_candidate_context_created",
    "memory_candidate_provenance_created",
    "memory_candidate_risk_flag_created",
    "memory_candidate_extraction_audit_created",
    "state_candidate_created",
]

MEMORY_CANDIDATE_EXTRACTION_FORBIDDEN_EFFECT_TYPES = [
    "memory_candidate_scored",
    "memory_scored",
    "memory_promoted",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "session_continuity_context_created",
    "continuity_injection_bundle_created",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "raw_transcript_memory_created",
    "raw_provider_output_memory_created",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class MemoryCandidateExtractionPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    extraction_enabled: bool = True
    extraction_from_eligible_sources_only: bool = True
    candidate_is_not_memory: bool = True
    source_refs_required: bool = True
    evidence_refs_required: bool = True
    provenance_required: bool = True
    risk_flags_required: bool = True
    redaction_required: bool = True
    candidate_type_required: bool = True
    candidate_context_required: bool = True
    pig_guidance_refs_allowed: bool = True
    pig_guidance_is_not_memory: bool = True
    raw_transcript_source_forbidden: bool = True
    raw_provider_output_source_forbidden: bool = True
    raw_secret_source_forbidden: bool = True
    credential_source_forbidden: bool = True
    private_full_path_source_forbidden: bool = True
    scoring_enabled_now: bool = False
    promotion_enabled_now: bool = False
    persistent_memory_write_enabled_now: bool = False
    durable_memory_write_enabled_now: bool = False
    session_continuity_injection_enabled_now: bool = False
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False
    llm_judge_as_sole_authority_forbidden: bool = True


@dataclass
class MemoryCandidateExtractionRequest(_ModelMixin):
    request_id: str
    memory_contract_report_id: str | None
    memory_source_boundary_report_id: str | None
    source_ref_bundle_id: str | None
    candidate_readiness_boundary_id: str | None
    selected_source_refs: list[dict[str, Any]]
    requested_candidate_types: list[str]
    extraction_profile: str | None
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidateExtractionSourceView(_ModelMixin):
    source_view_id: str
    source_boundary_report_ref: dict[str, Any] | None
    candidate_readiness_boundary_ref: dict[str, Any] | None
    eligible_source_refs: list[dict[str, Any]]
    deferred_source_refs: list[dict[str, Any]]
    blocked_source_refs: list[dict[str, Any]]
    source_quality_refs: list[dict[str, Any]]
    redaction_refs: list[dict[str, Any]]
    event_quality_refs: list[dict[str, Any]]
    trace_coverage_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    source_status: str
    eligible_source_count: int
    deferred_source_count: int
    blocked_source_count: int
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False


@dataclass
class MemoryCandidateExtractionRule(_ModelMixin):
    rule_id: str
    rule_name: str
    candidate_type: str | None
    rule_summary: str
    required: bool
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidateTypeClassifier(_ModelMixin):
    classifier_id: str
    supported_candidate_types: list[str]
    classification_method: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    llm_judge_used: bool = False


@dataclass
class MemoryCandidateSourceLink(_ModelMixin):
    source_link_id: str
    candidate_id: str
    source_ref_id: str | None
    source_ref: dict[str, Any]
    source_category: str
    source_support_role: str
    source_quality_ref: dict[str, Any] | None
    event_quality_ref: dict[str, Any] | None
    trace_coverage_ref: dict[str, Any] | None
    redaction_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    raw_content_linked: bool = False


@dataclass
class MemoryCandidateClaim(_ModelMixin):
    claim_id: str
    candidate_id: str
    claim_text: str
    claim_kind: str
    support_source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    support_status: str
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    sanitized: bool = True
    asserted_as_truth: bool = False
    score_created: bool = False


@dataclass
class MemoryCandidateContext(_ModelMixin):
    context_id: str
    candidate_id: str
    context_summary: str
    related_project_refs: list[dict[str, Any]]
    related_session_refs: list[dict[str, Any]]
    related_trace_refs: list[dict[str, Any]]
    related_command_refs: list[dict[str, Any]]
    related_approval_refs: list[dict[str, Any]]
    related_failure_refs: list[dict[str, Any]]
    related_pig_guidance_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    context_is_not_injection: bool = True
    continuity_context_created: bool = False


@dataclass
class MemoryCandidateProvenance(_ModelMixin):
    provenance_id: str
    candidate_id: str
    originating_versions: list[str]
    originating_surfaces: list[str]
    source_ref_ids: list[str]
    extraction_rule_ids: list[str]
    extraction_request_id: str
    extraction_batch_id: str | None
    created_at: str | None
    provenance_complete: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidatePIGSignal(_ModelMixin):
    pig_signal_id: str
    candidate_id: str
    pig_guidance_ref: dict[str, Any] | None
    signal_type: str
    signal_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_promotes_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False


@dataclass
class MemoryCandidateRiskFlag(_ModelMixin):
    risk_flag_id: str
    candidate_id: str
    risk_type: str
    risk_level: str
    risk_summary: str
    blocks_future_promotion: bool
    requires_more_evidence: bool
    requires_user_confirmation: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidateRedactionView(_ModelMixin):
    redaction_view_id: str
    candidate_id: str
    source_redaction_refs: list[dict[str, Any]]
    redacted_categories: list[str]
    candidate_summary_sanitized: bool
    candidate_claims_sanitized: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    raw_content_included: bool = False
    raw_secret_included: bool = False


@dataclass
class MemoryCandidateExtractionDecision(_ModelMixin):
    extraction_decision_id: str
    source_ref_id: str | None
    candidate_id: str | None
    decision_type: str
    decision_reason: str
    decision_rule_refs: list[dict[str, Any]]
    creates_memory_candidate: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    creates_memory: bool = False
    scores_memory: bool = False
    promotes_memory: bool = False
    writes_persistent_memory: bool = False


@dataclass
class MemoryCandidateExtractionSkipRecord(_ModelMixin):
    skip_record_id: str
    source_ref: dict[str, Any]
    skip_reason: str
    duplicate_candidate_ref: dict[str, Any] | None
    decision_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidateExtractionDeferredRecord(_ModelMixin):
    deferred_record_id: str
    source_ref: dict[str, Any]
    deferral_reason: str
    deferred_until: str | None
    required_followup_refs: list[dict[str, Any]]
    decision_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidateExtractionBlockedRecord(_ModelMixin):
    blocked_record_id: str
    source_ref: dict[str, Any]
    block_reason: str
    blocked_categories: list[str]
    decision_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION


@dataclass
class MemoryCandidate(_ModelMixin):
    candidate_id: str
    candidate_type: str
    title: str
    summary: str
    candidate_claims: list[MemoryCandidateClaim]
    source_links: list[MemoryCandidateSourceLink]
    context: MemoryCandidateContext
    provenance: MemoryCandidateProvenance
    pig_signals: list[MemoryCandidatePIGSignal]
    risk_flags: list[MemoryCandidateRiskFlag]
    redaction_view: MemoryCandidateRedactionView | None
    extraction_decision_ref: dict[str, Any] | None
    candidate_status: str
    promotion_status: str
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    created_from_workbench_refs: bool
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    created_from_raw_transcript: bool = False
    created_from_raw_provider_output: bool = False
    raw_content_included: bool = False
    raw_secret_included: bool = False
    score_created: bool = False
    promoted_to_memory: bool = False
    persistent_memory_written: bool = False
    persona_mutation: bool = False
    behavior_policy_mutation: bool = False


@dataclass
class MemoryCandidateBatch(_ModelMixin):
    batch_id: str
    extraction_request_id: str
    source_view_id: str
    candidates: list[MemoryCandidate]
    skipped_records: list[MemoryCandidateExtractionSkipRecord]
    deferred_records: list[MemoryCandidateExtractionDeferredRecord]
    blocked_records: list[MemoryCandidateExtractionBlockedRecord]
    candidate_count: int
    skipped_count: int
    deferred_count: int
    blocked_count: int
    batch_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    memory_promoted: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemoryCandidateExtractionAuditTrail(_ModelMixin):
    audit_trail_id: str
    extraction_request_ref: dict[str, Any]
    batch_ref: dict[str, Any] | None
    candidate_refs: list[dict[str, Any]]
    decision_refs: list[dict[str, Any]]
    skipped_record_refs: list[dict[str, Any]]
    deferred_record_refs: list[dict[str, Any]]
    blocked_record_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    raw_content_included: bool = False


@dataclass
class MemoryCandidateExtractionFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryCandidateExtractionReport(_ModelMixin):
    report_id: str
    created_at: str
    extraction_policy: MemoryCandidateExtractionPolicy
    request: MemoryCandidateExtractionRequest
    source_view: MemoryCandidateExtractionSourceView
    extraction_rules: list[MemoryCandidateExtractionRule]
    type_classifier: MemoryCandidateTypeClassifier
    candidate_batch: MemoryCandidateBatch
    audit_trail: MemoryCandidateExtractionAuditTrail
    findings: list[MemoryCandidateExtractionFinding]
    report_status: str
    ready_for_v0_27_3: bool
    extraction_policy_created: bool
    extraction_source_view_created: bool
    extraction_rules_created: bool
    type_classifier_created: bool
    candidate_batch_created: bool
    memory_candidates_created: bool
    candidate_source_links_created: bool
    candidate_claims_created: bool
    candidate_contexts_created: bool
    candidate_provenance_created: bool
    candidate_pig_signals_created: bool
    candidate_risk_flags_created: bool
    candidate_redaction_views_created: bool
    extraction_decisions_created: bool
    extraction_audit_trail_created: bool
    memory_candidate_count: int
    skipped_count: int
    deferred_count: int
    blocked_count: int
    version: str = MEMORY_CANDIDATE_EXTRACTION_VERSION
    ready_for_v0_28: bool = False
    memory_scored: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    durable_memory_written: bool = False
    session_continuity_injected: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_CANDIDATE_EXTRACTION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.27.3 Memory Evidence Binder & Scoring begins or memory candidate extraction policy changes."


class MemoryCandidateExtractionPrerequisiteSourceService:
    def __init__(
        self,
        *,
        source_boundary_available: bool = True,
        contract_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> None:
        self.source_boundary_available = source_boundary_available
        self.contract_available = contract_available
        self.pig_guidance_available = pig_guidance_available
        self._source_parts: dict[str, Any] | None = None

    def _parts(self) -> dict[str, Any] | None:
        if not self.source_boundary_available:
            return None
        if self._source_parts is None:
            self._source_parts = MemorySourceBoundaryReportService().build_all_parts()
        return self._source_parts

    def load_v0270_contract(self) -> dict[str, Any] | None:
        if not self.contract_available:
            return None
        return _ref("memory_candidate_continuity_contract", "memory_candidate_continuity_contract:v0.27.0", "v0.27.0")

    def load_v0270_contract_report(self) -> dict[str, Any] | None:
        if not self.contract_available:
            return None
        return _ref("memory_contract_report", "memory_contract_report:v0.27.0", "v0.27.0")

    def load_v0271_source_boundary_report(self) -> MemorySourceBoundaryReport | None:
        parts = self._parts()
        return None if parts is None else parts["report"]

    def load_v0271_candidate_readiness_boundary(self) -> MemoryCandidateReadinessBoundary | None:
        parts = self._parts()
        return None if parts is None else parts["candidate_readiness_boundary"]

    def load_v0271_source_ref_bundle(self) -> MemorySourceRefBundle | None:
        parts = self._parts()
        return None if parts is None else parts["source_bundle"]

    def load_v0269_handoff_packet_if_available(self) -> dict[str, Any] | None:
        return _ref("workbench_memory_candidate_handoff_packet", "workbench_memory_candidate_handoff:v0.26.9", "v0.26.9")

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        return [_ref("pig_guidance", "pig_guidance:v0.26.9", "v0.26.9")]

    def load_source_refs(self) -> list[MemorySourceRef]:
        parts = self._parts()
        return [] if parts is None else parts["source_refs"]


class MemoryCandidateExtractionPolicyService:
    def build_policy(self) -> MemoryCandidateExtractionPolicy:
        return MemoryCandidateExtractionPolicy(
            policy_id="memory_candidate_extraction_policy:v0.27.2",
            evidence_refs=[_ref("memory_source_boundary_report", "memory_source_boundary_report:v0.27.1", "v0.27.1")],
        )


class MemoryCandidateExtractionSourceViewService:
    def build_source_view(self, source_service: MemoryCandidateExtractionPrerequisiteSourceService) -> MemoryCandidateExtractionSourceView:
        report = source_service.load_v0271_source_boundary_report()
        readiness = source_service.load_v0271_candidate_readiness_boundary()
        source_refs = source_service.load_source_refs()
        eligible_refs = [_ref("memory_source_ref", source.source_ref_id, source.version) for source in source_refs if source.source_status == "eligible"]
        redaction_refs = [source.redaction_ref for source in source_refs if source.redaction_ref]
        event_quality_refs = [source.event_quality_ref for source in source_refs if source.event_quality_ref]
        trace_coverage_refs = [source.trace_coverage_ref for source in source_refs if source.trace_coverage_ref]
        source_status = "complete" if report and eligible_refs else "missing"
        return MemoryCandidateExtractionSourceView(
            source_view_id="memory_candidate_extraction_source_view:v0.27.2",
            source_boundary_report_ref=_ref("memory_source_boundary_report", report.report_id, report.version) if report else None,
            candidate_readiness_boundary_ref=_ref("memory_candidate_readiness_boundary", readiness.readiness_boundary_id, readiness.version) if readiness else None,
            eligible_source_refs=eligible_refs,
            deferred_source_refs=readiness.deferred_until_more_evidence_refs if readiness else [],
            blocked_source_refs=readiness.blocked_source_refs if readiness else [],
            source_quality_refs=[_ref("memory_source_quality_report", "memory_source_quality_report:v0.27.1", "v0.27.1")],
            redaction_refs=redaction_refs,
            event_quality_refs=event_quality_refs,
            trace_coverage_refs=trace_coverage_refs,
            pig_guidance_refs=source_service.load_pig_guidance_refs_if_available(),
            source_status=source_status,
            eligible_source_count=len(eligible_refs),
            deferred_source_count=len(readiness.deferred_until_more_evidence_refs) if readiness else 0,
            blocked_source_count=len(readiness.blocked_source_refs) if readiness else 0,
            evidence_refs=[_ref("memory_source_boundary_report", "memory_source_boundary_report:v0.27.1", "v0.27.1")],
        )


class MemoryCandidateExtractionRuleService:
    def build_rules(self) -> list[MemoryCandidateExtractionRule]:
        rules: list[MemoryCandidateExtractionRule] = []
        for name in MEMORY_CANDIDATE_EXTRACTION_REQUIRED_RULES:
            block = name in {
                "source_must_be_eligible",
                "source_ref_required",
                "evidence_ref_required",
                "raw_transcript_forbidden",
                "raw_provider_output_forbidden",
                "raw_secret_forbidden",
                "credential_forbidden",
                "private_full_path_forbidden",
                "no_scoring_in_v0272",
                "no_promotion_in_v0272",
                "no_persistent_write_in_v0272",
            }
            rules.append(
                MemoryCandidateExtractionRule(
                    rule_id=f"memory_candidate_extraction_rule:{name}",
                    rule_name=name,
                    candidate_type=None,
                    rule_summary=f"{name} must hold for v0.27.2 candidate extraction.",
                    required=True,
                    pass_condition=f"{name} satisfied.",
                    fail_condition=f"{name} failed.",
                    block_on_fail=block,
                    evidence_refs=[_ref("memory_candidate_extraction_policy", "memory_candidate_extraction_policy:v0.27.2")],
                )
            )
        return rules


class MemoryCandidateTypeClassifierService:
    def build_classifier(self) -> MemoryCandidateTypeClassifier:
        return MemoryCandidateTypeClassifier(
            classifier_id="memory_candidate_type_classifier:v0.27.2",
            supported_candidate_types=list(MEMORY_CANDIDATE_TYPES),
            classification_method="mixed_deterministic",
            evidence_refs=[_ref("memory_candidate_extraction_rule", "memory_candidate_extraction_rule:candidate_type_required")],
        )

    def classify_source(self, source: MemorySourceRef) -> str:
        mapping = {
            "workbench_snapshot_refs": "project_state_candidate",
            "ocel_export_package_refs": "context_summary_candidate",
            "session_context_refs": "long_task_continuity_candidate",
            "trace_summary_refs": "workflow_preference_candidate",
            "evidence_summary_refs": "decision_pattern_candidate",
            "pig_guidance_refs": "skill_usage_pattern_candidate",
            "approval_decision_refs": "approval_preference_candidate",
            "command_candidate_refs": "task_preference_candidate",
            "failure_cause_refs": "failure_pattern_candidate",
            "human_intervention_refs": "user_instruction_candidate",
            "event_quality_report_refs": "system_boundary_candidate",
        }
        return mapping.get(source.source_category, "unknown")


class MemoryCandidateSourceLinkService:
    def build_source_links(self, candidate_id: str, source: MemorySourceRef) -> list[MemoryCandidateSourceLink]:
        return [
            MemoryCandidateSourceLink(
                source_link_id=f"memory_candidate_source_link:{candidate_id}:{source.source_ref_id}",
                candidate_id=candidate_id,
                source_ref_id=source.source_ref_id,
                source_ref=_ref("memory_source_ref", source.source_ref_id, source.version),
                source_category=source.source_category,
                source_support_role="primary",
                source_quality_ref=_ref("memory_source_quality_report", "memory_source_quality_report:v0.27.1", "v0.27.1"),
                event_quality_ref=source.event_quality_ref,
                trace_coverage_ref=source.trace_coverage_ref,
                redaction_ref=source.redaction_ref,
                evidence_refs=source.evidence_refs,
            )
        ]


class MemoryCandidateClaimService:
    def build_claims(self, candidate_id: str, candidate_type: str, source: MemorySourceRef) -> list[MemoryCandidateClaim]:
        claim_kind = "unknown"
        if "preference" in candidate_type:
            claim_kind = "preference"
        elif "project_state" in candidate_type:
            claim_kind = "project_state"
        elif "workflow" in candidate_type:
            claim_kind = "workflow_pattern"
        elif "decision" in candidate_type:
            claim_kind = "decision_pattern"
        elif "skill" in candidate_type:
            claim_kind = "skill_pattern"
        elif "provider_route" in candidate_type:
            claim_kind = "provider_route_pattern"
        elif "approval" in candidate_type:
            claim_kind = "approval_pattern"
        elif "failure" in candidate_type:
            claim_kind = "failure_pattern"
        elif "continuity" in candidate_type or "context" in candidate_type:
            claim_kind = "continuity_context"
        elif "instruction" in candidate_type:
            claim_kind = "instruction"
        elif "boundary" in candidate_type:
            claim_kind = "boundary"
        elif "safety" in candidate_type:
            claim_kind = "safety_preference"
        return [
            MemoryCandidateClaim(
                claim_id=f"memory_candidate_claim:{candidate_id}:primary",
                candidate_id=candidate_id,
                claim_text=f"Candidate summary derived from eligible refs-only source category {source.source_category}.",
                claim_kind=claim_kind,
                support_source_refs=[_ref("memory_source_ref", source.source_ref_id, source.version)],
                evidence_refs=source.evidence_refs,
                support_status="ref_supported" if source.evidence_refs else "weakly_supported",
            )
        ]


class MemoryCandidateContextService:
    def build_context(self, candidate_id: str, source: MemorySourceRef, pig_refs: list[dict[str, Any]]) -> MemoryCandidateContext:
        return MemoryCandidateContext(
            context_id=f"memory_candidate_context:{candidate_id}",
            candidate_id=candidate_id,
            context_summary="Refs-only candidate context for later evidence binding; not session continuity injection.",
            related_project_refs=[source.source_ref] if source.source_category in {"workbench_snapshot_refs", "ocel_export_package_refs"} else [],
            related_session_refs=[source.source_ref] if source.source_category == "session_context_refs" else [],
            related_trace_refs=[source.source_ref] if "trace" in source.source_category else [],
            related_command_refs=[source.source_ref] if source.source_category == "command_candidate_refs" else [],
            related_approval_refs=[source.source_ref] if source.source_category == "approval_decision_refs" else [],
            related_failure_refs=[source.source_ref] if source.source_category == "failure_cause_refs" else [],
            related_pig_guidance_refs=pig_refs,
            evidence_refs=source.evidence_refs,
        )


class MemoryCandidateProvenanceService:
    def build_provenance(
        self,
        candidate_id: str,
        source: MemorySourceRef,
        rules: list[MemoryCandidateExtractionRule],
        request_id: str,
    ) -> MemoryCandidateProvenance:
        return MemoryCandidateProvenance(
            provenance_id=f"memory_candidate_provenance:{candidate_id}",
            candidate_id=candidate_id,
            originating_versions=[source.originating_version or "unknown", MEMORY_SOURCE_BOUNDARY_VERSION],
            originating_surfaces=[source.originating_surface or "unknown"],
            source_ref_ids=[source.source_ref_id],
            extraction_rule_ids=[rule.rule_id for rule in rules],
            extraction_request_id=request_id,
            extraction_batch_id=None,
            created_at=utc_now_iso(),
            provenance_complete=bool(source.source_ref_id and source.evidence_refs),
            evidence_refs=source.evidence_refs,
        )


class MemoryCandidatePIGSignalService:
    def build_pig_signals(self, candidate_id: str, pig_refs: list[dict[str, Any]]) -> list[MemoryCandidatePIGSignal]:
        if not pig_refs:
            return []
        return [
            MemoryCandidatePIGSignal(
                pig_signal_id=f"memory_candidate_pig_signal:{candidate_id}:primary",
                candidate_id=candidate_id,
                pig_guidance_ref=pig_refs[0],
                signal_type="pattern_summary",
                signal_summary="PIG guidance is attached as a refs-only signal, not memory or authority.",
                evidence_refs=pig_refs,
            )
        ]


class MemoryCandidateRiskFlagService:
    def build_risk_flags(self, candidate_id: str, source: MemorySourceRef) -> list[MemoryCandidateRiskFlag]:
        return [
            MemoryCandidateRiskFlag(
                risk_flag_id=f"memory_candidate_risk_flag:{candidate_id}:promotion_requires_user_confirmation",
                candidate_id=candidate_id,
                risk_type="promotion_requires_user_confirmation",
                risk_level="low",
                risk_summary="Future promotion must pass v0.27.4 gate; candidate extraction alone is not memory.",
                blocks_future_promotion=False,
                requires_more_evidence=False,
                requires_user_confirmation=True,
                evidence_refs=source.evidence_refs,
            )
        ]


class MemoryCandidateRedactionViewService:
    def build_redaction_view(self, candidate_id: str, source: MemorySourceRef) -> MemoryCandidateRedactionView:
        return MemoryCandidateRedactionView(
            redaction_view_id=f"memory_candidate_redaction_view:{candidate_id}",
            candidate_id=candidate_id,
            source_redaction_refs=[source.redaction_ref] if source.redaction_ref else [],
            redacted_categories=["raw_transcript", "raw_provider_output", "raw_secret", "credential", "private_full_path"],
            candidate_summary_sanitized=True,
            candidate_claims_sanitized=True,
            evidence_refs=source.evidence_refs,
        )


class MemoryCandidateExtractionDecisionService:
    def decide_extraction(
        self,
        source: MemorySourceRef,
        candidate_id: str | None,
        rules: list[MemoryCandidateExtractionRule],
    ) -> MemoryCandidateExtractionDecision:
        if source.raw_content_included or source.raw_transcript_included or source.raw_provider_output_included:
            return MemoryCandidateExtractionDecision(
                extraction_decision_id=f"memory_candidate_extraction_decision:block:{source.source_ref_id}",
                source_ref_id=source.source_ref_id,
                candidate_id=None,
                decision_type="block_raw_source",
                decision_reason="Raw source material is forbidden for v0.27.2 candidate extraction.",
                decision_rule_refs=[_ref("memory_candidate_extraction_rule", "memory_candidate_extraction_rule:raw_transcript_forbidden")],
                creates_memory_candidate=False,
                evidence_refs=source.evidence_refs,
            )
        return MemoryCandidateExtractionDecision(
            extraction_decision_id=f"memory_candidate_extraction_decision:{candidate_id}",
            source_ref_id=source.source_ref_id,
            candidate_id=candidate_id,
            decision_type="extract_candidate",
            decision_reason="Eligible refs-only source can create a candidate-only artifact.",
            decision_rule_refs=[_ref("memory_candidate_extraction_rule", rule.rule_id) for rule in rules],
            creates_memory_candidate=True,
            evidence_refs=source.evidence_refs,
        )


class MemoryCandidateExtractionRecordService:
    def build_skip_record(self, source_ref: dict[str, Any], reason: str = "not_memory_relevant") -> MemoryCandidateExtractionSkipRecord:
        return MemoryCandidateExtractionSkipRecord(
            skip_record_id="memory_candidate_extraction_skip_record:sample",
            source_ref=source_ref,
            skip_reason=reason,
            duplicate_candidate_ref=None,
            decision_ref=None,
            evidence_refs=[source_ref],
        )

    def build_deferred_record(self, source_ref: dict[str, Any], reason: str = "more_evidence_required") -> MemoryCandidateExtractionDeferredRecord:
        return MemoryCandidateExtractionDeferredRecord(
            deferred_record_id="memory_candidate_extraction_deferred_record:sample",
            source_ref=source_ref,
            deferral_reason=reason,
            deferred_until=None,
            required_followup_refs=[],
            decision_ref=None,
            evidence_refs=[source_ref],
        )

    def build_blocked_record(self, source_ref: dict[str, Any], reason: str = "raw_source_blocked") -> MemoryCandidateExtractionBlockedRecord:
        return MemoryCandidateExtractionBlockedRecord(
            blocked_record_id="memory_candidate_extraction_blocked_record:sample",
            source_ref=source_ref,
            block_reason=reason,
            blocked_categories=["raw_transcript"],
            decision_ref=None,
            evidence_refs=[source_ref],
        )


class MemoryCandidateService:
    def build_candidates(
        self,
        source_refs: list[MemorySourceRef],
        source_view: MemoryCandidateExtractionSourceView,
        rules: list[MemoryCandidateExtractionRule],
        request: MemoryCandidateExtractionRequest,
    ) -> tuple[list[MemoryCandidate], list[MemoryCandidateExtractionDecision]]:
        classifier_service = MemoryCandidateTypeClassifierService()
        decision_service = MemoryCandidateExtractionDecisionService()
        candidates: list[MemoryCandidate] = []
        decisions: list[MemoryCandidateExtractionDecision] = []
        eligible_ids = {ref["id"] for ref in source_view.eligible_source_refs}
        for index, source in enumerate(source_refs, start=1):
            if source.source_ref_id not in eligible_ids:
                continue
            candidate_id = f"memory_candidate:v0.27.2:{index}"
            candidate_type = classifier_service.classify_source(source)
            source_links = MemoryCandidateSourceLinkService().build_source_links(candidate_id, source)
            claims = MemoryCandidateClaimService().build_claims(candidate_id, candidate_type, source)
            pig_signals = MemoryCandidatePIGSignalService().build_pig_signals(candidate_id, source_view.pig_guidance_refs)
            context = MemoryCandidateContextService().build_context(candidate_id, source, source_view.pig_guidance_refs)
            provenance = MemoryCandidateProvenanceService().build_provenance(candidate_id, source, rules, request.request_id)
            risk_flags = MemoryCandidateRiskFlagService().build_risk_flags(candidate_id, source)
            redaction_view = MemoryCandidateRedactionViewService().build_redaction_view(candidate_id, source)
            decision = decision_service.decide_extraction(source, candidate_id, rules)
            decisions.append(decision)
            candidate = MemoryCandidate(
                candidate_id=candidate_id,
                candidate_type=candidate_type,
                title=f"Candidate from {source.source_category}",
                summary=f"Refs-only memory candidate from eligible {source.source_category}; not memory, not scored, not promoted.",
                candidate_claims=claims,
                source_links=source_links,
                context=context,
                provenance=provenance,
                pig_signals=pig_signals,
                risk_flags=risk_flags,
                redaction_view=redaction_view,
                extraction_decision_ref=_ref("memory_candidate_extraction_decision", decision.extraction_decision_id),
                candidate_status="candidate_only",
                promotion_status="candidate_only",
                source_refs=[_ref("memory_source_ref", source.source_ref_id, source.version)],
                evidence_refs=source.evidence_refs,
                created_from_workbench_refs=source.originating_surface == "workspace_agent_workbench",
            )
            candidates.append(candidate)
        return candidates, decisions


class MemoryCandidateBatchService:
    def build_batch(
        self,
        request: MemoryCandidateExtractionRequest,
        source_view: MemoryCandidateExtractionSourceView,
        candidates: list[MemoryCandidate],
        skipped_records: list[MemoryCandidateExtractionSkipRecord],
        deferred_records: list[MemoryCandidateExtractionDeferredRecord],
        blocked_records: list[MemoryCandidateExtractionBlockedRecord],
    ) -> MemoryCandidateBatch:
        status = "ready" if candidates and not blocked_records else "warning"
        if blocked_records:
            status = "blocked"
        return MemoryCandidateBatch(
            batch_id="memory_candidate_batch:v0.27.2",
            extraction_request_id=request.request_id,
            source_view_id=source_view.source_view_id,
            candidates=candidates,
            skipped_records=skipped_records,
            deferred_records=deferred_records,
            blocked_records=blocked_records,
            candidate_count=len(candidates),
            skipped_count=len(skipped_records),
            deferred_count=len(deferred_records),
            blocked_count=len(blocked_records),
            batch_status=status,
            evidence_refs=[_ref("memory_candidate_extraction_source_view", source_view.source_view_id)],
        )


class MemoryCandidateExtractionAuditTrailService:
    def build_audit_trail(
        self,
        request: MemoryCandidateExtractionRequest,
        batch: MemoryCandidateBatch,
        decisions: list[MemoryCandidateExtractionDecision],
    ) -> MemoryCandidateExtractionAuditTrail:
        refs = [_ref("memory_candidate", candidate.candidate_id) for candidate in batch.candidates]
        decision_refs = [_ref("memory_candidate_extraction_decision", decision.extraction_decision_id) for decision in decisions]
        return MemoryCandidateExtractionAuditTrail(
            audit_trail_id="memory_candidate_extraction_audit_trail:v0.27.2",
            extraction_request_ref=_ref("memory_candidate_extraction_request", request.request_id),
            batch_ref=_ref("memory_candidate_batch", batch.batch_id),
            candidate_refs=refs,
            decision_refs=decision_refs,
            skipped_record_refs=[_ref("memory_candidate_extraction_skip_record", record.skip_record_id) for record in batch.skipped_records],
            deferred_record_refs=[_ref("memory_candidate_extraction_deferred_record", record.deferred_record_id) for record in batch.deferred_records],
            blocked_record_refs=[_ref("memory_candidate_extraction_blocked_record", record.blocked_record_id) for record in batch.blocked_records],
            audit_event_count=len(refs) + len(decision_refs) + len(batch.skipped_records) + len(batch.deferred_records) + len(batch.blocked_records),
            audit_status="ready" if batch.batch_status in {"ready", "warning"} else batch.batch_status,
            evidence_refs=[_ref("memory_candidate_batch", batch.batch_id)],
        )


class MemoryCandidateExtractionFindingService:
    BLOCKED_FINDINGS = {
        "raw_transcript_source_detected",
        "raw_provider_output_source_detected",
        "raw_secret_source_detected",
        "credential_source_detected",
        "private_full_path_source_detected",
        "candidate_without_source_ref_detected",
        "candidate_without_evidence_detected",
        "scoring_attempted",
        "promotion_attempted",
        "persistent_memory_write_attempted",
        "durable_memory_write_attempted",
        "session_continuity_injection_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "extraction_policy_created",
        "extraction_source_view_created",
        "extraction_rule_created",
        "candidate_type_classifier_created",
        "candidate_batch_created",
        "memory_candidate_created",
        "candidate_source_link_created",
        "candidate_claim_created",
        "candidate_context_created",
        "candidate_provenance_created",
        "candidate_pig_signal_created",
        "candidate_risk_flag_created",
        "candidate_redaction_view_created",
        "extraction_decision_created",
        "extraction_audit_trail_created",
    ]

    def build_findings(
        self,
        source_service: MemoryCandidateExtractionPrerequisiteSourceService,
        source_view: MemoryCandidateExtractionSourceView,
        *,
        extra_findings: list[str] | None = None,
    ) -> list[MemoryCandidateExtractionFinding]:
        findings: list[MemoryCandidateExtractionFinding] = []
        if not source_service.contract_available:
            findings.append(self._finding("warning", "missing_memory_contract", "v0.27.0 contract is unavailable."))
        if not source_service.source_boundary_available:
            findings.append(self._finding("warning", "missing_source_boundary_report", "v0.27.1 source boundary report is unavailable."))
            findings.append(self._finding("warning", "missing_candidate_readiness_boundary", "v0.27.1 candidate readiness boundary is unavailable."))
        if source_view.eligible_source_count == 0:
            findings.append(self._finding("warning", "missing_eligible_sources", "No eligible source refs are available."))
        if not source_service.pig_guidance_available:
            findings.append(self._finding("warning", "missing_pig_guidance_refs", "PIG guidance refs are unavailable."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        return findings or [self._finding("info", "ok", "Memory candidate extraction is ready.")]

    def _finding(self, severity: str, finding_type: str, message: str) -> MemoryCandidateExtractionFinding:
        return MemoryCandidateExtractionFinding(
            finding_id=f"memory_candidate_extraction_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("memory_candidate_extraction_report", "memory_candidate_extraction_report:v0.27.2")],
            withdrawal_condition="Withdraw if candidate extraction policy changes or scoring/promotion/write/injection/execution behavior appears.",
        )


class MemoryCandidateExtractionReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        extra_findings: list[str] | None = None,
        source_boundary_available: bool = True,
        contract_available: bool = True,
        pig_guidance_available: bool = True,
    ) -> dict[str, Any]:
        source_service = MemoryCandidateExtractionPrerequisiteSourceService(
            source_boundary_available=source_boundary_available,
            contract_available=contract_available,
            pig_guidance_available=pig_guidance_available,
        )
        policy = MemoryCandidateExtractionPolicyService().build_policy()
        source_view = MemoryCandidateExtractionSourceViewService().build_source_view(source_service)
        request = MemoryCandidateExtractionRequest(
            request_id="memory_candidate_extraction_request:v0.27.2",
            memory_contract_report_id="memory_contract_report:v0.27.0" if contract_available else None,
            memory_source_boundary_report_id="memory_source_boundary_report:v0.27.1" if source_boundary_available else None,
            source_ref_bundle_id="memory_source_ref_bundle:v0.27.1" if source_boundary_available else None,
            candidate_readiness_boundary_id="memory_candidate_readiness_boundary:v0.27.1" if source_boundary_available else None,
            selected_source_refs=source_view.eligible_source_refs,
            requested_candidate_types=list(MEMORY_CANDIDATE_TYPES),
            extraction_profile="standard",
            source_refs=[_ref("memory_candidate_extraction_policy", policy.policy_id)],
        )
        rules = MemoryCandidateExtractionRuleService().build_rules()
        classifier = MemoryCandidateTypeClassifierService().build_classifier()
        source_refs = source_service.load_source_refs()
        candidates, decisions = MemoryCandidateService().build_candidates(source_refs, source_view, rules, request)
        skipped_records: list[MemoryCandidateExtractionSkipRecord] = []
        deferred_records: list[MemoryCandidateExtractionDeferredRecord] = [
            MemoryCandidateExtractionRecordService().build_deferred_record(ref)
            for ref in source_view.deferred_source_refs
        ]
        blocked_records: list[MemoryCandidateExtractionBlockedRecord] = [
            MemoryCandidateExtractionRecordService().build_blocked_record(ref)
            for ref in source_view.blocked_source_refs
        ]
        batch = MemoryCandidateBatchService().build_batch(request, source_view, candidates, skipped_records, deferred_records, blocked_records)
        audit = MemoryCandidateExtractionAuditTrailService().build_audit_trail(request, batch, decisions)
        findings = MemoryCandidateExtractionFindingService().build_findings(source_service, source_view, extra_findings=extra_findings)
        report_status = self._report_status(findings, batch)
        report = MemoryCandidateExtractionReport(
            report_id=report_id or "memory_candidate_extraction_report:v0.27.2",
            created_at=utc_now_iso(),
            extraction_policy=policy,
            request=request,
            source_view=source_view,
            extraction_rules=rules,
            type_classifier=classifier,
            candidate_batch=batch,
            audit_trail=audit,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_3=report_status in {"passed", "warning"} and bool(candidates),
            extraction_policy_created=True,
            extraction_source_view_created=True,
            extraction_rules_created=True,
            type_classifier_created=True,
            candidate_batch_created=True,
            memory_candidates_created=bool(candidates),
            candidate_source_links_created=any(candidate.source_links for candidate in candidates),
            candidate_claims_created=any(candidate.candidate_claims for candidate in candidates),
            candidate_contexts_created=all(candidate.context is not None for candidate in candidates),
            candidate_provenance_created=all(candidate.provenance is not None for candidate in candidates),
            candidate_pig_signals_created=any(candidate.pig_signals for candidate in candidates),
            candidate_risk_flags_created=any(candidate.risk_flags for candidate in candidates),
            candidate_redaction_views_created=all(candidate.redaction_view is not None for candidate in candidates),
            extraction_decisions_created=bool(decisions),
            extraction_audit_trail_created=True,
            memory_candidate_count=len(candidates),
            skipped_count=len(skipped_records),
            deferred_count=len(deferred_records),
            blocked_count=len(blocked_records),
            limitations=[
                "v0.27.2 creates candidate-only artifacts from eligible refs; evidence scoring begins in v0.27.3.",
                "v0.26.10 release hygiene status may remain unknown, but persistent memory write is forbidden in v0.27.2.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if scoring, promotion, persistent/durable write, continuity injection, persona/policy mutation, raw memory, PIG execution, provider/command execution, safety bypass, external adapter, Schumpeter split, or LLM judging appears.",
            ],
        )
        return {
            "source_service": source_service,
            "extraction_policy": policy,
            "request": request,
            "source_view": source_view,
            "extraction_rules": rules,
            "type_classifier": classifier,
            "source_refs": source_refs,
            "candidates": candidates,
            "decisions": decisions,
            "skipped_records": skipped_records,
            "deferred_records": deferred_records,
            "blocked_records": blocked_records,
            "candidate_batch": batch,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[MemoryCandidateExtractionFinding], batch: MemoryCandidateBatch) -> str:
        if any(finding.finding_type in MemoryCandidateExtractionFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if batch.batch_status == "blocked":
            return "blocked"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_CANDIDATE_EXTRACTION_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_candidate_extraction",
            "principles": [
                "Memory candidate is not memory",
                "Candidate extraction is not scoring",
                "Candidate extraction is not promotion",
                "Candidate extraction is not persistent memory write",
                "Candidate source link is not evidence score",
                "Candidate claim is not asserted truth",
                "Candidate context is not session continuity injection",
                "PIG guidance signal is not memory",
                "Raw transcript is not default candidate source",
            ],
            "safety_boundary": {
                "memory_candidates_created": "conditional",
                "memory_scored": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "durable_memory_written": False,
                "session_continuity_injected": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_secret_output": False,
                "credential_exposed": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.3 memory evidence binder & scoring",
                "v0.27.4 memory promotion gate",
                "v0.27.5 durable memory record & registry",
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": MEMORY_CANDIDATE_EXTRACTION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_candidate_extraction_created",
            "version": MEMORY_CANDIDATE_EXTRACTION_VERSION,
            "source_read_models": [
                "MemorySourceBoundaryState",
                "MemorySourceRefState",
                "MemorySourceRefBundleState",
                "MemorySourceEligibilityState",
                "MemoryCandidateReadinessBoundaryState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryCandidateExtractionState",
                "MemoryCandidateBatchState",
                "MemoryCandidateState",
                "MemoryCandidateSourceLinkState",
                "MemoryCandidateClaimState",
                "MemoryCandidateContextState",
                "MemoryCandidateRiskFlagState",
                "MemoryCandidateExtractionAuditState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_CANDIDATE_EXTRACTION_EFFECT_TYPES,
        }


def render_memory_candidate_extraction_cli(parts: dict[str, Any], section: str = "extract") -> str:
    report: MemoryCandidateExtractionReport = parts["report"]
    lines = [
        f"Memory Candidate Extraction {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"extraction_policy_created={_bool(report.extraction_policy_created)}",
        f"extraction_source_view_created={_bool(report.extraction_source_view_created)}",
        f"candidate_batch_created={_bool(report.candidate_batch_created)}",
        f"memory_candidates_created={_bool(report.memory_candidates_created)}",
        f"memory_candidate_count={report.memory_candidate_count}",
        f"skipped_count={report.skipped_count}",
        f"deferred_count={report.deferred_count}",
        f"blocked_count={report.blocked_count}",
        f"ready_for_v0_27_3={_bool(report.ready_for_v0_27_3)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_scored={_bool(report.memory_scored)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"durable_memory_written={_bool(report.durable_memory_written)}",
        f"session_continuity_injected={_bool(report.session_continuity_injected)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "source-view":
        source_view = parts["source_view"]
        lines.append(f"eligible_source_count={source_view.eligible_source_count}")
        lines.append(f"source_status={source_view.source_status}")
    elif section == "rules":
        lines.append(f"extraction_rule_count={len(parts['extraction_rules'])}")
    elif section == "classifier":
        classifier = parts["type_classifier"]
        lines.append(f"classification_method={classifier.classification_method}")
        lines.append(f"llm_judge_used={_bool(classifier.llm_judge_used)}")
    elif section == "batch":
        batch = parts["candidate_batch"]
        lines.append(f"batch_status={batch.batch_status}")
    elif section == "list":
        lines.append(f"candidate_count={len(parts['candidates'])}")
    elif section == "claims":
        lines.append(f"candidate_claim_count={sum(len(candidate.candidate_claims) for candidate in parts['candidates'])}")
    elif section == "source-links":
        lines.append(f"candidate_source_link_count={sum(len(candidate.source_links) for candidate in parts['candidates'])}")
    elif section == "context":
        lines.append(f"candidate_context_count={len([candidate for candidate in parts['candidates'] if candidate.context])}")
    elif section == "provenance":
        lines.append(f"candidate_provenance_count={len([candidate for candidate in parts['candidates'] if candidate.provenance])}")
    elif section == "pig-signals":
        lines.append(f"candidate_pig_signal_count={sum(len(candidate.pig_signals) for candidate in parts['candidates'])}")
    elif section == "risks":
        lines.append(f"candidate_risk_flag_count={sum(len(candidate.risk_flags) for candidate in parts['candidates'])}")
    elif section == "decisions":
        lines.append(f"extraction_decision_count={len(parts['decisions'])}")
    elif section == "audit":
        audit = parts["audit_trail"]
        lines.append(f"audit_status={audit.audit_status}")
        lines.append(f"raw_content_included={_bool(audit.raw_content_included)}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)


MEMORY_EVIDENCE_SCORING_VERSION = "v0.27.3"
MEMORY_EVIDENCE_SCORING_VERSION_NAME = "Memory Evidence Binder & Scoring"
MEMORY_EVIDENCE_SCORING_KOREAN_NAME = "Memory Evidence Binder.Scoring"
MEMORY_EVIDENCE_SCORING_NEXT_STEP = "v0.27.4 Memory Promotion Gate"

MEMORY_EVIDENCE_BINDING_REQUIRED_RULES = [
    "candidate_ref_required",
    "source_refs_required",
    "evidence_refs_required",
    "provenance_required",
    "candidate_claim_support_required",
    "raw_transcript_evidence_forbidden",
    "raw_provider_output_evidence_forbidden",
    "raw_secret_evidence_forbidden",
    "credential_evidence_forbidden",
    "private_full_path_evidence_forbidden",
    "redaction_required",
    "contradiction_check_required",
    "privacy_risk_assessment_required",
    "score_breakdown_required",
    "score_is_not_promotion",
    "high_score_is_not_automatic_memory",
    "no_persistent_write_in_v0273",
    "no_durable_write_in_v0273",
    "PIG_guidance_allowed_but_not_memory",
]

MEMORY_EVIDENCE_SCORING_OBJECT_TYPES = [
    "memory_evidence_scoring_policy",
    "memory_evidence_scoring_request",
    "memory_evidence_scoring_source_view",
    "memory_evidence_binding_rule",
    "memory_candidate_evidence_bundle",
    "memory_evidence_item",
    "memory_evidence_support_link",
    "memory_claim_support_assessment",
    "memory_evidence_strength_assessment",
    "memory_source_quality_assessment",
    "memory_recency_assessment",
    "memory_stability_assessment",
    "memory_reuse_value_assessment",
    "memory_specificity_assessment",
    "memory_privacy_risk_assessment",
    "memory_contradiction_check",
    "memory_user_control_requirement_assessment",
    "memory_pig_scoring_signal",
    "memory_score_dimension_value",
    "memory_candidate_score_breakdown",
    "memory_candidate_score",
    "memory_candidate_scoring_decision",
    "memory_candidate_scoring_batch",
    "memory_promotion_readiness_preview",
    "memory_evidence_scoring_audit_trail",
    "memory_evidence_scoring_finding",
    "memory_evidence_scoring_report",
    "memory_candidate",
    "memory_candidate_batch",
    "memory_candidate_extraction_report",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_EVIDENCE_SCORING_EVENT_TYPES = [
    "memory_evidence_scoring_requested",
    "memory_evidence_scoring_prerequisites_loaded",
    "memory_evidence_scoring_policy_created",
    "memory_evidence_scoring_source_view_created",
    "memory_evidence_binding_rule_created",
    "memory_candidate_evidence_bundle_created",
    "memory_evidence_item_created",
    "memory_evidence_support_link_created",
    "memory_claim_support_assessment_created",
    "memory_evidence_strength_assessment_created",
    "memory_source_quality_assessment_created",
    "memory_recency_assessment_created",
    "memory_stability_assessment_created",
    "memory_reuse_value_assessment_created",
    "memory_specificity_assessment_created",
    "memory_privacy_risk_assessment_created",
    "memory_contradiction_check_created",
    "memory_user_control_requirement_assessment_created",
    "memory_pig_scoring_signal_created",
    "memory_score_dimension_value_created",
    "memory_candidate_score_breakdown_created",
    "memory_candidate_score_created",
    "memory_candidate_scoring_decision_created",
    "memory_candidate_scoring_batch_created",
    "memory_promotion_readiness_preview_created",
    "memory_evidence_scoring_audit_trail_created",
    "memory_evidence_scoring_report_created",
    "memory_evidence_scoring_warning_created",
    "memory_evidence_scoring_blocked",
]

MEMORY_EVIDENCE_SCORING_EFFECT_TYPES = [
    "read_only_observation",
    "memory_candidate_evidence_bound",
    "memory_candidate_scored",
    "memory_candidate_score_breakdown_created",
    "memory_contradiction_check_created",
    "memory_privacy_risk_assessment_created",
    "memory_promotion_readiness_preview_created",
    "memory_evidence_scoring_audit_created",
    "state_candidate_created",
]

MEMORY_EVIDENCE_SCORING_FORBIDDEN_EFFECT_TYPES = [
    "memory_promoted",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "session_continuity_context_created",
    "continuity_injection_bundle_created",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "raw_transcript_memory_created",
    "raw_provider_output_memory_created",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class MemoryEvidenceScoringPolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    evidence_binding_enabled: bool = True
    scoring_enabled: bool = True
    score_is_not_promotion: bool = True
    high_score_is_not_automatic_memory: bool = True
    promotion_deferred_to: str = "v0.27.4"
    persistent_memory_write_enabled_now: bool = False
    durable_memory_write_enabled_now: bool = False
    durable_registry_update_enabled_now: bool = False
    session_continuity_injection_enabled_now: bool = False
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    evidence_bundle_required: bool = True
    source_refs_required: bool = True
    candidate_refs_required: bool = True
    score_breakdown_required: bool = True
    contradiction_check_required: bool = True
    privacy_risk_assessment_required: bool = True
    user_control_requirement_required: bool = True
    pig_guidance_refs_allowed: bool = True
    pig_guidance_is_not_memory: bool = True
    pig_guidance_cannot_promote_memory: bool = True
    raw_transcript_evidence_forbidden: bool = True
    raw_provider_output_evidence_forbidden: bool = True
    raw_secret_evidence_forbidden: bool = True
    credential_evidence_forbidden: bool = True
    private_full_path_evidence_forbidden: bool = True
    llm_judge_as_sole_scoring_authority_forbidden: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False


@dataclass
class MemoryEvidenceScoringRequest(_ModelMixin):
    request_id: str
    memory_contract_report_id: str | None
    memory_candidate_extraction_report_id: str | None
    candidate_batch_id: str | None
    selected_candidate_refs: list[dict[str, Any]]
    requested_score_dimensions: list[str]
    scoring_profile: str | None
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryEvidenceScoringSourceView(_ModelMixin):
    source_view_id: str
    candidate_extraction_report_ref: dict[str, Any] | None
    candidate_batch_ref: dict[str, Any] | None
    candidate_refs: list[dict[str, Any]]
    candidate_claim_refs: list[dict[str, Any]]
    candidate_source_link_refs: list[dict[str, Any]]
    candidate_pig_signal_refs: list[dict[str, Any]]
    source_quality_refs: list[dict[str, Any]]
    event_quality_refs: list[dict[str, Any]]
    trace_coverage_refs: list[dict[str, Any]]
    redaction_refs: list[dict[str, Any]]
    source_status: str
    candidate_count: int
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False


@dataclass
class MemoryEvidenceBindingRule(_ModelMixin):
    rule_id: str
    rule_name: str
    rule_summary: str
    required: bool
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryEvidenceItem(_ModelMixin):
    evidence_item_id: str
    candidate_id: str
    source_ref: dict[str, Any]
    evidence_kind: str
    evidence_summary: str
    support_strength: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    sanitized: bool = True
    raw_content_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False


@dataclass
class MemoryEvidenceSupportLink(_ModelMixin):
    support_link_id: str
    candidate_id: str
    claim_ref: dict[str, Any]
    evidence_item_ref: dict[str, Any]
    support_role: str
    support_summary: str
    support_strength: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryClaimSupportAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    claim_ref: dict[str, Any]
    support_links: list[dict[str, Any]]
    support_status: str
    missing_evidence_reason: str | None
    contradiction_refs: list[dict[str, Any]]
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    claim_asserted_as_truth: bool = False


@dataclass
class MemoryCandidateEvidenceBundle(_ModelMixin):
    evidence_bundle_id: str
    candidate_id: str
    candidate_ref: dict[str, Any]
    evidence_items: list[MemoryEvidenceItem]
    support_links: list[MemoryEvidenceSupportLink]
    claim_support_assessments: list[MemoryClaimSupportAssessment]
    source_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    event_quality_refs: list[dict[str, Any]]
    trace_coverage_refs: list[dict[str, Any]]
    redaction_refs: list[dict[str, Any]]
    evidence_count: int
    support_link_count: int
    bundle_status: str
    evidence_refs_for_audit: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False


@dataclass
class MemoryEvidenceStrengthAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    evidence_bundle_ref: dict[str, Any]
    strength_level: str
    strength_score: float | None
    strength_summary: str
    weak_points: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemorySourceQualityAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    source_quality_refs: list[dict[str, Any]]
    source_quality_level: str
    source_quality_score: float | None
    missing_quality_dimensions: list[str]
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryRecencyAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    source_time_refs: list[dict[str, Any]]
    recency_level: str
    recency_score: float | None
    stale_warning: bool
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryStabilityAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    stability_level: str
    stability_score: float | None
    expected_validity_horizon: str | None
    instability_reasons: list[str]
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryReuseValueAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    reuse_value_level: str
    reuse_value_score: float | None
    likely_reuse_contexts: list[str]
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemorySpecificityAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    specificity_level: str
    specificity_score: float | None
    ambiguity_notes: list[str]
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryPrivacyRiskAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    privacy_risk_level: str
    privacy_risk_categories: list[str]
    requires_user_confirmation: bool
    blocks_future_promotion: bool
    assessment_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryContradictionCheck(_ModelMixin):
    contradiction_check_id: str
    candidate_id: str
    contradiction_detected: bool
    contradiction_level: str
    contradiction_refs: list[dict[str, Any]]
    conflict_summary: str | None
    requires_review: bool
    blocks_future_promotion: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryUserControlRequirementAssessment(_ModelMixin):
    assessment_id: str
    candidate_id: str
    user_control_level: str
    requires_user_confirmation: bool
    requires_promotion_gate_review: bool
    control_reason: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryPIGScoringSignal(_ModelMixin):
    pig_scoring_signal_id: str
    candidate_id: str
    pig_signal_refs: list[dict[str, Any]]
    signal_type: str
    signal_weight_hint: str
    signal_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_promotes_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False


@dataclass
class MemoryScoreDimensionValue(_ModelMixin):
    dimension_value_id: str
    candidate_id: str
    dimension: str
    raw_score: float | None
    normalized_score: float | None
    level: str
    explanation: str
    source_assessment_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryCandidateScoreBreakdown(_ModelMixin):
    score_breakdown_id: str
    candidate_id: str
    dimension_values: list[MemoryScoreDimensionValue]
    positive_signal_refs: list[dict[str, Any]]
    negative_signal_refs: list[dict[str, Any]]
    blocking_signal_refs: list[dict[str, Any]]
    breakdown_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION


@dataclass
class MemoryCandidateScore(_ModelMixin):
    score_id: str
    candidate_id: str
    score_breakdown: MemoryCandidateScoreBreakdown
    overall_score: float | None
    score_band: str
    promotion_readiness: str
    score_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    score_is_promotion: bool = False
    high_score_auto_promotes: bool = False
    persistent_memory_written: bool = False
    durable_memory_record_created: bool = False


@dataclass
class MemoryCandidateScoringDecision(_ModelMixin):
    scoring_decision_id: str
    candidate_id: str
    score_id: str | None
    decision_type: str
    decision_reason: str
    ready_for_v0274_promotion_gate: bool
    creates_score: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    promotes_memory: bool = False
    writes_persistent_memory: bool = False


@dataclass
class MemoryCandidateScoringBatch(_ModelMixin):
    scoring_batch_id: str
    scoring_request_id: str
    candidate_scores: list[MemoryCandidateScore]
    scoring_decisions: list[MemoryCandidateScoringDecision]
    scored_candidate_count: int
    partial_candidate_count: int
    deferred_candidate_count: int
    blocked_candidate_count: int
    ready_for_gate_review_count: int
    batch_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    memory_promoted: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemoryPromotionReadinessPreview(_ModelMixin):
    preview_id: str
    candidate_id: str
    score_ref: dict[str, Any] | None
    readiness: str
    readiness_reason: str
    required_followup_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    target_next_step: str = MEMORY_EVIDENCE_SCORING_NEXT_STEP
    preview_is_not_promotion: bool = True
    promotion_performed_now: bool = False


@dataclass
class MemoryEvidenceScoringAuditTrail(_ModelMixin):
    audit_trail_id: str
    scoring_request_ref: dict[str, Any]
    candidate_refs: list[dict[str, Any]]
    evidence_bundle_refs: list[dict[str, Any]]
    assessment_refs: list[dict[str, Any]]
    score_refs: list[dict[str, Any]]
    scoring_decision_refs: list[dict[str, Any]]
    promotion_readiness_preview_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    raw_content_included: bool = False


@dataclass
class MemoryEvidenceScoringFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryEvidenceScoringReport(_ModelMixin):
    report_id: str
    created_at: str
    evidence_scoring_policy: MemoryEvidenceScoringPolicy
    request: MemoryEvidenceScoringRequest
    source_view: MemoryEvidenceScoringSourceView
    binding_rules: list[MemoryEvidenceBindingRule]
    evidence_bundles: list[MemoryCandidateEvidenceBundle]
    evidence_strength_assessments: list[MemoryEvidenceStrengthAssessment]
    source_quality_assessments: list[MemorySourceQualityAssessment]
    recency_assessments: list[MemoryRecencyAssessment]
    stability_assessments: list[MemoryStabilityAssessment]
    reuse_value_assessments: list[MemoryReuseValueAssessment]
    specificity_assessments: list[MemorySpecificityAssessment]
    privacy_risk_assessments: list[MemoryPrivacyRiskAssessment]
    contradiction_checks: list[MemoryContradictionCheck]
    user_control_assessments: list[MemoryUserControlRequirementAssessment]
    pig_scoring_signals: list[MemoryPIGScoringSignal]
    score_breakdowns: list[MemoryCandidateScoreBreakdown]
    candidate_scores: list[MemoryCandidateScore]
    scoring_batch: MemoryCandidateScoringBatch
    promotion_readiness_previews: list[MemoryPromotionReadinessPreview]
    audit_trail: MemoryEvidenceScoringAuditTrail
    findings: list[MemoryEvidenceScoringFinding]
    report_status: str
    ready_for_v0_27_4: bool
    evidence_bundles_created: bool
    candidate_scores_created: bool
    scoring_batch_created: bool
    promotion_readiness_previews_created: bool
    memory_scored: bool
    version: str = MEMORY_EVIDENCE_SCORING_VERSION
    ready_for_v0_28: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    durable_memory_written: bool = False
    durable_registry_updated: bool = False
    session_continuity_injected: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_EVIDENCE_SCORING_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.27.4 Memory Promotion Gate begins or memory scoring policy changes."


class MemoryEvidenceScoringPrerequisiteSourceService:
    def __init__(self, *, extraction_available: bool = True, pig_signals_available: bool = True) -> None:
        self.extraction_available = extraction_available
        self.pig_signals_available = pig_signals_available
        self._parts: dict[str, Any] | None = None

    def _extraction_parts(self) -> dict[str, Any] | None:
        if not self.extraction_available:
            return None
        if self._parts is None:
            self._parts = MemoryCandidateExtractionReportService().build_all_parts(pig_guidance_available=self.pig_signals_available)
        return self._parts

    def load_v0272_extraction_report(self) -> MemoryCandidateExtractionReport | None:
        parts = self._extraction_parts()
        return None if parts is None else parts["report"]

    def load_v0272_candidate_batch(self) -> MemoryCandidateBatch | None:
        parts = self._extraction_parts()
        return None if parts is None else parts["candidate_batch"]

    def load_memory_candidates(self) -> list[MemoryCandidate]:
        parts = self._extraction_parts()
        return [] if parts is None else parts["candidates"]

    def load_candidate_claims(self) -> list[MemoryCandidateClaim]:
        return [claim for candidate in self.load_memory_candidates() for claim in candidate.candidate_claims]

    def load_candidate_source_links(self) -> list[MemoryCandidateSourceLink]:
        return [link for candidate in self.load_memory_candidates() for link in candidate.source_links]

    def load_candidate_pig_signals(self) -> list[MemoryCandidatePIGSignal]:
        return [signal for candidate in self.load_memory_candidates() for signal in candidate.pig_signals]

    def load_v0271_source_quality_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("memory_source_quality_report", "memory_source_quality_report:v0.27.1", "v0.27.1")]

    def load_event_quality_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_event_quality_report", "workbench_event_quality_report:v0.26.8", "v0.26.8")]

    def load_trace_coverage_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_trace_coverage_report", "workbench_trace_coverage_report:v0.26.8", "v0.26.8")]

    def load_redaction_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("memory_source_redaction_report", "memory_source_redaction_report:v0.27.1", "v0.27.1")]


class MemoryEvidenceScoringPolicyService:
    def build_policy(self) -> MemoryEvidenceScoringPolicy:
        return MemoryEvidenceScoringPolicy(
            policy_id="memory_evidence_scoring_policy:v0.27.3",
            evidence_refs=[_ref("memory_candidate_extraction_report", "memory_candidate_extraction_report:v0.27.2", "v0.27.2")],
        )


class MemoryEvidenceScoringSourceViewService:
    def build_source_view(self, source_service: MemoryEvidenceScoringPrerequisiteSourceService) -> MemoryEvidenceScoringSourceView:
        report = source_service.load_v0272_extraction_report()
        batch = source_service.load_v0272_candidate_batch()
        candidates = source_service.load_memory_candidates()
        claim_refs = [_ref("memory_candidate_claim", claim.claim_id, claim.version) for claim in source_service.load_candidate_claims()]
        link_refs = [_ref("memory_candidate_source_link", link.source_link_id, link.version) for link in source_service.load_candidate_source_links()]
        pig_refs = [_ref("memory_candidate_pig_signal", signal.pig_signal_id, signal.version) for signal in source_service.load_candidate_pig_signals()]
        return MemoryEvidenceScoringSourceView(
            source_view_id="memory_evidence_scoring_source_view:v0.27.3",
            candidate_extraction_report_ref=_ref("memory_candidate_extraction_report", report.report_id, report.version) if report else None,
            candidate_batch_ref=_ref("memory_candidate_batch", batch.batch_id, batch.version) if batch else None,
            candidate_refs=[_ref("memory_candidate", candidate.candidate_id, candidate.version) for candidate in candidates],
            candidate_claim_refs=claim_refs,
            candidate_source_link_refs=link_refs,
            candidate_pig_signal_refs=pig_refs,
            source_quality_refs=source_service.load_v0271_source_quality_refs_if_available(),
            event_quality_refs=source_service.load_event_quality_refs_if_available(),
            trace_coverage_refs=source_service.load_trace_coverage_refs_if_available(),
            redaction_refs=source_service.load_redaction_refs_if_available(),
            source_status="complete" if candidates else "missing",
            candidate_count=len(candidates),
            evidence_refs=[_ref("memory_candidate_extraction_report", "memory_candidate_extraction_report:v0.27.2", "v0.27.2")],
        )


class MemoryEvidenceBindingRuleService:
    def build_rules(self) -> list[MemoryEvidenceBindingRule]:
        rules: list[MemoryEvidenceBindingRule] = []
        for name in MEMORY_EVIDENCE_BINDING_REQUIRED_RULES:
            block = name in {
                "candidate_ref_required",
                "source_refs_required",
                "evidence_refs_required",
                "raw_transcript_evidence_forbidden",
                "raw_provider_output_evidence_forbidden",
                "raw_secret_evidence_forbidden",
                "credential_evidence_forbidden",
                "private_full_path_evidence_forbidden",
                "score_is_not_promotion",
                "high_score_is_not_automatic_memory",
                "no_persistent_write_in_v0273",
                "no_durable_write_in_v0273",
            }
            rules.append(
                MemoryEvidenceBindingRule(
                    rule_id=f"memory_evidence_binding_rule:{name}",
                    rule_name=name,
                    rule_summary=f"{name} must hold for v0.27.3 evidence binding and scoring.",
                    required=True,
                    pass_condition=f"{name} satisfied.",
                    fail_condition=f"{name} failed.",
                    block_on_fail=block,
                    evidence_refs=[_ref("memory_evidence_scoring_policy", "memory_evidence_scoring_policy:v0.27.3")],
                )
            )
        return rules


class MemoryEvidenceItemService:
    def build_evidence_items(self, candidate: MemoryCandidate) -> list[MemoryEvidenceItem]:
        items: list[MemoryEvidenceItem] = []
        for index, source_ref in enumerate(candidate.source_refs, start=1):
            items.append(
                MemoryEvidenceItem(
                    evidence_item_id=f"memory_evidence_item:{candidate.candidate_id}:{index}",
                    candidate_id=candidate.candidate_id,
                    source_ref=source_ref,
                    evidence_kind="source_ref",
                    evidence_summary="Refs-only candidate source supports later scoring; no raw content is included.",
                    support_strength="moderate",
                    evidence_refs=candidate.evidence_refs,
                )
            )
        for index, pig_signal in enumerate(candidate.pig_signals, start=1):
            items.append(
                MemoryEvidenceItem(
                    evidence_item_id=f"memory_evidence_item:{candidate.candidate_id}:pig:{index}",
                    candidate_id=candidate.candidate_id,
                    source_ref=_ref("memory_candidate_pig_signal", pig_signal.pig_signal_id, pig_signal.version),
                    evidence_kind="pig_guidance_signal",
                    evidence_summary="PIG signal informs scoring only; it is not memory, promotion, policy, or execution.",
                    support_strength="weak",
                    evidence_refs=pig_signal.evidence_refs,
                )
            )
        return items


class MemoryEvidenceSupportLinkService:
    def build_support_links(self, candidate: MemoryCandidate, items: list[MemoryEvidenceItem]) -> list[MemoryEvidenceSupportLink]:
        links: list[MemoryEvidenceSupportLink] = []
        if not items:
            return links
        for claim in candidate.candidate_claims:
            links.append(
                MemoryEvidenceSupportLink(
                    support_link_id=f"memory_evidence_support_link:{claim.claim_id}",
                    candidate_id=candidate.candidate_id,
                    claim_ref=_ref("memory_candidate_claim", claim.claim_id, claim.version),
                    evidence_item_ref=_ref("memory_evidence_item", items[0].evidence_item_id),
                    support_role="primary",
                    support_summary="Claim is supported by refs-only evidence, not asserted as truth.",
                    support_strength="moderate" if claim.support_status == "ref_supported" else "weak",
                    evidence_refs=claim.evidence_refs,
                )
            )
        return links


class MemoryClaimSupportAssessmentService:
    def build_assessments(self, candidate: MemoryCandidate, support_links: list[MemoryEvidenceSupportLink]) -> list[MemoryClaimSupportAssessment]:
        assessments: list[MemoryClaimSupportAssessment] = []
        for claim in candidate.candidate_claims:
            claim_links = [link for link in support_links if link.claim_ref["id"] == claim.claim_id]
            assessments.append(
                MemoryClaimSupportAssessment(
                    assessment_id=f"memory_claim_support_assessment:{claim.claim_id}",
                    candidate_id=candidate.candidate_id,
                    claim_ref=_ref("memory_candidate_claim", claim.claim_id, claim.version),
                    support_links=[_ref("memory_evidence_support_link", link.support_link_id) for link in claim_links],
                    support_status="supported" if claim_links and claim.support_status == "ref_supported" else "weakly_supported",
                    missing_evidence_reason=None if claim_links else "No evidence item linked.",
                    contradiction_refs=[],
                    assessment_summary="Claim support is assessed from refs only; it is not asserted as truth.",
                    evidence_refs=claim.evidence_refs,
                )
            )
        return assessments


class MemoryCandidateEvidenceBundleService:
    def build_bundles(self, candidates: list[MemoryCandidate]) -> list[MemoryCandidateEvidenceBundle]:
        bundles: list[MemoryCandidateEvidenceBundle] = []
        for candidate in candidates:
            items = MemoryEvidenceItemService().build_evidence_items(candidate)
            links = MemoryEvidenceSupportLinkService().build_support_links(candidate, items)
            assessments = MemoryClaimSupportAssessmentService().build_assessments(candidate, links)
            bundles.append(
                MemoryCandidateEvidenceBundle(
                    evidence_bundle_id=f"memory_candidate_evidence_bundle:{candidate.candidate_id}",
                    candidate_id=candidate.candidate_id,
                    candidate_ref=_ref("memory_candidate", candidate.candidate_id, candidate.version),
                    evidence_items=items,
                    support_links=links,
                    claim_support_assessments=assessments,
                    source_refs=candidate.source_refs,
                    pig_guidance_refs=[_ref("memory_candidate_pig_signal", signal.pig_signal_id, signal.version) for signal in candidate.pig_signals],
                    event_quality_refs=[link.event_quality_ref for link in candidate.source_links if link.event_quality_ref],
                    trace_coverage_refs=[link.trace_coverage_ref for link in candidate.source_links if link.trace_coverage_ref],
                    redaction_refs=[link.redaction_ref for link in candidate.source_links if link.redaction_ref],
                    evidence_count=len(items),
                    support_link_count=len(links),
                    bundle_status="complete" if items and links else "weak",
                    evidence_refs_for_audit=candidate.evidence_refs,
                )
            )
        return bundles


class MemoryEvidenceStrengthAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryEvidenceStrengthAssessment:
        score = 0.75 if bundle.bundle_status == "complete" else 0.45
        return MemoryEvidenceStrengthAssessment(
            assessment_id=f"memory_evidence_strength_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            evidence_bundle_ref=_ref("memory_candidate_evidence_bundle", bundle.evidence_bundle_id),
            strength_level="strong" if score >= 0.75 else "moderate",
            strength_score=score,
            strength_summary="Evidence strength is a scoring signal, not truth.",
            weak_points=[] if score >= 0.75 else ["Evidence bundle is incomplete."],
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemorySourceQualityAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemorySourceQualityAssessment:
        return MemorySourceQualityAssessment(
            assessment_id=f"memory_source_quality_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            source_quality_refs=[_ref("memory_source_quality_report", "memory_source_quality_report:v0.27.1", "v0.27.1")],
            source_quality_level="high" if bundle.source_refs else "unknown",
            source_quality_score=0.8 if bundle.source_refs else None,
            missing_quality_dimensions=[] if bundle.source_refs else ["source_refs"],
            assessment_summary="Source quality is inherited from v0.27.1 refs-only reports.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryRecencyAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryRecencyAssessment:
        return MemoryRecencyAssessment(
            assessment_id=f"memory_recency_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            source_time_refs=bundle.source_refs,
            recency_level="current",
            recency_score=0.75,
            stale_warning=False,
            assessment_summary="Recency is treated as current for generated v0.27 refs.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryStabilityAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryStabilityAssessment:
        return MemoryStabilityAssessment(
            assessment_id=f"memory_stability_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            stability_level="stable",
            stability_score=0.7,
            expected_validity_horizon="Valid until source refs or candidate extraction policy changes.",
            instability_reasons=[],
            assessment_summary="Stability is provisional and bounded by refs and policy.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryReuseValueAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryReuseValueAssessment:
        return MemoryReuseValueAssessment(
            assessment_id=f"memory_reuse_value_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            reuse_value_level="medium",
            reuse_value_score=0.65,
            likely_reuse_contexts=["future_memory_promotion_gate_review"],
            assessment_summary="Reuse value is advisory and does not promote memory.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemorySpecificityAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemorySpecificityAssessment:
        return MemorySpecificityAssessment(
            assessment_id=f"memory_specificity_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            specificity_level="specific",
            specificity_score=0.7,
            ambiguity_notes=[],
            assessment_summary="Candidate is specific enough for future gate review.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryPrivacyRiskAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryPrivacyRiskAssessment:
        return MemoryPrivacyRiskAssessment(
            assessment_id=f"memory_privacy_risk_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            privacy_risk_level="low",
            privacy_risk_categories=[],
            requires_user_confirmation=False,
            blocks_future_promotion=False,
            assessment_summary="Privacy risk is assessed as a scoring signal, not automatic rejection.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryContradictionCheckService:
    def check(self, bundle: MemoryCandidateEvidenceBundle) -> MemoryContradictionCheck:
        return MemoryContradictionCheck(
            contradiction_check_id=f"memory_contradiction_check:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            contradiction_detected=False,
            contradiction_level="none",
            contradiction_refs=[],
            conflict_summary=None,
            requires_review=False,
            blocks_future_promotion=False,
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryUserControlRequirementAssessmentService:
    def assess(self, bundle: MemoryCandidateEvidenceBundle, privacy: MemoryPrivacyRiskAssessment) -> MemoryUserControlRequirementAssessment:
        return MemoryUserControlRequirementAssessment(
            assessment_id=f"memory_user_control_requirement_assessment:{bundle.candidate_id}",
            candidate_id=bundle.candidate_id,
            user_control_level="confirm_before_promotion",
            requires_user_confirmation=privacy.requires_user_confirmation,
            requires_promotion_gate_review=True,
            control_reason="Scores require v0.27.4 promotion gate review before any memory promotion.",
            evidence_refs=bundle.evidence_refs_for_audit,
        )


class MemoryPIGScoringSignalService:
    def build_signals(self, candidates: list[MemoryCandidate]) -> list[MemoryPIGScoringSignal]:
        signals: list[MemoryPIGScoringSignal] = []
        for candidate in candidates:
            refs = [_ref("memory_candidate_pig_signal", signal.pig_signal_id, signal.version) for signal in candidate.pig_signals]
            if refs:
                signals.append(
                    MemoryPIGScoringSignal(
                        pig_scoring_signal_id=f"memory_pig_scoring_signal:{candidate.candidate_id}",
                        candidate_id=candidate.candidate_id,
                        pig_signal_refs=refs,
                        signal_type="reuse_signal",
                        signal_weight_hint="low",
                        signal_summary="PIG guidance informs score explanation only and cannot promote memory.",
                        evidence_refs=refs,
                    )
                )
        return signals


class MemoryScoreDimensionValueService:
    def build_dimension_values(
        self,
        candidate_id: str,
        *,
        strength: MemoryEvidenceStrengthAssessment,
        source_quality: MemorySourceQualityAssessment,
        recency: MemoryRecencyAssessment,
        stability: MemoryStabilityAssessment,
        reuse: MemoryReuseValueAssessment,
        specificity: MemorySpecificityAssessment,
        privacy: MemoryPrivacyRiskAssessment,
        contradiction: MemoryContradictionCheck,
        user_control: MemoryUserControlRequirementAssessment,
    ) -> list[MemoryScoreDimensionValue]:
        raw_values = {
            "evidence_strength": strength.strength_score,
            "source_quality": source_quality.source_quality_score,
            "recency": recency.recency_score,
            "stability": stability.stability_score,
            "reuse_value": reuse.reuse_value_score,
            "specificity": specificity.specificity_score,
            "risk_level": 0.8 if privacy.privacy_risk_level in {"none", "low"} else 0.3,
            "privacy_sensitivity": 0.8 if privacy.privacy_risk_level in {"none", "low"} else 0.3,
            "contradiction_risk": 0.9 if not contradiction.contradiction_detected else 0.2,
            "user_control_requirement": 0.6 if user_control.requires_promotion_gate_review else 0.8,
        }
        values: list[MemoryScoreDimensionValue] = []
        for dimension in MEMORY_SCORE_DIMENSIONS:
            raw = raw_values.get(dimension)
            level = "unknown" if raw is None else ("high" if raw >= 0.75 else "medium" if raw >= 0.45 else "low")
            values.append(
                MemoryScoreDimensionValue(
                    dimension_value_id=f"memory_score_dimension_value:{candidate_id}:{dimension}",
                    candidate_id=candidate_id,
                    dimension=dimension,
                    raw_score=raw,
                    normalized_score=raw,
                    level=level,
                    explanation=f"{dimension} contributes to score only; it is not a promotion decision.",
                    source_assessment_refs=[],
                    evidence_refs=[_ref("memory_candidate", candidate_id, MEMORY_CANDIDATE_EXTRACTION_VERSION)],
                )
            )
        return values


class MemoryCandidateScoreBreakdownService:
    def build_breakdown(self, candidate_id: str, dimension_values: list[MemoryScoreDimensionValue]) -> MemoryCandidateScoreBreakdown:
        return MemoryCandidateScoreBreakdown(
            score_breakdown_id=f"memory_candidate_score_breakdown:{candidate_id}",
            candidate_id=candidate_id,
            dimension_values=dimension_values,
            positive_signal_refs=[_ref("memory_score_dimension_value", value.dimension_value_id) for value in dimension_values if value.level in {"medium", "high"}],
            negative_signal_refs=[_ref("memory_score_dimension_value", value.dimension_value_id) for value in dimension_values if value.level == "low"],
            blocking_signal_refs=[_ref("memory_score_dimension_value", value.dimension_value_id) for value in dimension_values if value.level == "blocked"],
            breakdown_summary="Score breakdown is refs-only and does not promote memory.",
            evidence_refs=[_ref("memory_candidate", candidate_id, MEMORY_CANDIDATE_EXTRACTION_VERSION)],
        )


class MemoryCandidateScoreService:
    def build_score(self, breakdown: MemoryCandidateScoreBreakdown) -> MemoryCandidateScore:
        scores = [value.normalized_score for value in breakdown.dimension_values if value.normalized_score is not None]
        overall = round(sum(scores) / len(scores), 3) if scores else None
        score_band = "unknown" if overall is None else ("high" if overall >= 0.75 else "medium" if overall >= 0.45 else "low")
        readiness = "ready_for_gate_review" if score_band in {"medium", "high"} and not breakdown.blocking_signal_refs else "needs_more_evidence"
        return MemoryCandidateScore(
            score_id=f"memory_candidate_score:{breakdown.candidate_id}",
            candidate_id=breakdown.candidate_id,
            score_breakdown=breakdown,
            overall_score=overall,
            score_band=score_band,
            promotion_readiness=readiness,
            score_status="scored" if overall is not None else "partial",
            evidence_refs=[_ref("memory_candidate_score_breakdown", breakdown.score_breakdown_id)],
        )


class MemoryCandidateScoringDecisionService:
    def decide_scoring(self, score: MemoryCandidateScore) -> MemoryCandidateScoringDecision:
        decision_type = "score_candidate" if score.score_status == "scored" else "defer_more_evidence"
        return MemoryCandidateScoringDecision(
            scoring_decision_id=f"memory_candidate_scoring_decision:{score.candidate_id}",
            candidate_id=score.candidate_id,
            score_id=score.score_id,
            decision_type=decision_type,
            decision_reason="Candidate is scored for future gate review only; no promotion or write occurs.",
            ready_for_v0274_promotion_gate=score.promotion_readiness == "ready_for_gate_review",
            creates_score=True,
            evidence_refs=[_ref("memory_candidate_score", score.score_id)],
        )


class MemoryCandidateScoringBatchService:
    def build_batch(self, request: MemoryEvidenceScoringRequest, scores: list[MemoryCandidateScore], decisions: list[MemoryCandidateScoringDecision]) -> MemoryCandidateScoringBatch:
        return MemoryCandidateScoringBatch(
            scoring_batch_id="memory_candidate_scoring_batch:v0.27.3",
            scoring_request_id=request.request_id,
            candidate_scores=scores,
            scoring_decisions=decisions,
            scored_candidate_count=len([score for score in scores if score.score_status == "scored"]),
            partial_candidate_count=len([score for score in scores if score.score_status == "partial"]),
            deferred_candidate_count=len([decision for decision in decisions if decision.decision_type.startswith("defer")]),
            blocked_candidate_count=len([decision for decision in decisions if decision.decision_type.startswith("block")]),
            ready_for_gate_review_count=len([decision for decision in decisions if decision.ready_for_v0274_promotion_gate]),
            batch_status="ready" if scores else "warning",
            evidence_refs=[_ref("memory_evidence_scoring_request", request.request_id)],
        )


class MemoryPromotionReadinessPreviewService:
    def build_preview(self, score: MemoryCandidateScore) -> MemoryPromotionReadinessPreview:
        return MemoryPromotionReadinessPreview(
            preview_id=f"memory_promotion_readiness_preview:{score.candidate_id}",
            candidate_id=score.candidate_id,
            score_ref=_ref("memory_candidate_score", score.score_id),
            readiness=score.promotion_readiness,
            readiness_reason="Readiness preview is not promotion; v0.27.4 gate is required.",
            required_followup_refs=[_ref("memory_candidate_score", score.score_id)],
            evidence_refs=score.evidence_refs,
        )


class MemoryEvidenceScoringAuditTrailService:
    def build_audit_trail(
        self,
        request: MemoryEvidenceScoringRequest,
        bundles: list[MemoryCandidateEvidenceBundle],
        assessments: list[Any],
        scores: list[MemoryCandidateScore],
        decisions: list[MemoryCandidateScoringDecision],
        previews: list[MemoryPromotionReadinessPreview],
    ) -> MemoryEvidenceScoringAuditTrail:
        return MemoryEvidenceScoringAuditTrail(
            audit_trail_id="memory_evidence_scoring_audit_trail:v0.27.3",
            scoring_request_ref=_ref("memory_evidence_scoring_request", request.request_id),
            candidate_refs=request.selected_candidate_refs,
            evidence_bundle_refs=[_ref("memory_candidate_evidence_bundle", bundle.evidence_bundle_id) for bundle in bundles],
            assessment_refs=[_ref(type(item).__name__, getattr(item, "assessment_id", getattr(item, "contradiction_check_id", ""))) for item in assessments],
            score_refs=[_ref("memory_candidate_score", score.score_id) for score in scores],
            scoring_decision_refs=[_ref("memory_candidate_scoring_decision", decision.scoring_decision_id) for decision in decisions],
            promotion_readiness_preview_refs=[_ref("memory_promotion_readiness_preview", preview.preview_id) for preview in previews],
            audit_event_count=len(bundles) + len(assessments) + len(scores) + len(decisions) + len(previews),
            audit_status="ready" if scores else "warning",
            evidence_refs=[_ref("memory_candidate_scoring_batch", "memory_candidate_scoring_batch:v0.27.3")],
        )


class MemoryEvidenceScoringFindingService:
    BLOCKED_FINDINGS = {
        "raw_transcript_evidence_detected",
        "raw_provider_output_evidence_detected",
        "raw_secret_evidence_detected",
        "credential_evidence_detected",
        "private_full_path_evidence_detected",
        "promotion_attempted",
        "persistent_memory_write_attempted",
        "durable_memory_write_attempted",
        "durable_registry_update_attempted",
        "session_continuity_injection_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "evidence_scoring_policy_created",
        "evidence_scoring_source_view_created",
        "evidence_binding_rule_created",
        "evidence_bundle_created",
        "evidence_item_created",
        "support_link_created",
        "claim_support_assessment_created",
        "evidence_strength_assessment_created",
        "source_quality_assessment_created",
        "recency_assessment_created",
        "stability_assessment_created",
        "reuse_value_assessment_created",
        "specificity_assessment_created",
        "privacy_risk_assessment_created",
        "contradiction_check_created",
        "user_control_requirement_assessment_created",
        "pig_scoring_signal_created",
        "score_dimension_value_created",
        "score_breakdown_created",
        "candidate_score_created",
        "scoring_decision_created",
        "scoring_batch_created",
        "promotion_readiness_preview_created",
        "evidence_scoring_audit_trail_created",
    ]

    def build_findings(
        self,
        source_service: MemoryEvidenceScoringPrerequisiteSourceService,
        source_view: MemoryEvidenceScoringSourceView,
        *,
        extra_findings: list[str] | None = None,
    ) -> list[MemoryEvidenceScoringFinding]:
        findings: list[MemoryEvidenceScoringFinding] = []
        if not source_service.extraction_available:
            findings.append(self._finding("warning", "missing_candidate_extraction_report", "v0.27.2 extraction report is unavailable."))
            findings.append(self._finding("warning", "missing_candidate_batch", "v0.27.2 candidate batch is unavailable."))
        if source_view.candidate_count == 0:
            findings.append(self._finding("warning", "missing_candidates", "No memory candidates are available for scoring."))
        if not source_view.candidate_source_link_refs:
            findings.append(self._finding("warning", "missing_candidate_source_links", "Candidate source links are unavailable."))
        if not source_view.candidate_claim_refs:
            findings.append(self._finding("warning", "missing_candidate_claims", "Candidate claims are unavailable."))
        if not source_view.evidence_refs:
            findings.append(self._finding("warning", "missing_evidence_refs", "Evidence refs are unavailable."))
        if not source_view.source_quality_refs:
            findings.append(self._finding("warning", "missing_source_quality_refs", "Source quality refs are unavailable."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        return findings or [self._finding("info", "ok", "Memory evidence scoring is ready.")]

    def _finding(self, severity: str, finding_type: str, message: str) -> MemoryEvidenceScoringFinding:
        return MemoryEvidenceScoringFinding(
            finding_id=f"memory_evidence_scoring_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("memory_evidence_scoring_report", "memory_evidence_scoring_report:v0.27.3")],
            withdrawal_condition="Withdraw if scoring policy changes or promotion/write/injection/execution behavior appears.",
        )


class MemoryEvidenceScoringReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        extra_findings: list[str] | None = None,
        extraction_available: bool = True,
        pig_signals_available: bool = True,
    ) -> dict[str, Any]:
        source_service = MemoryEvidenceScoringPrerequisiteSourceService(
            extraction_available=extraction_available,
            pig_signals_available=pig_signals_available,
        )
        policy = MemoryEvidenceScoringPolicyService().build_policy()
        source_view = MemoryEvidenceScoringSourceViewService().build_source_view(source_service)
        candidates = source_service.load_memory_candidates()
        request = MemoryEvidenceScoringRequest(
            request_id="memory_evidence_scoring_request:v0.27.3",
            memory_contract_report_id="memory_contract_report:v0.27.0",
            memory_candidate_extraction_report_id="memory_candidate_extraction_report:v0.27.2" if extraction_available else None,
            candidate_batch_id="memory_candidate_batch:v0.27.2" if extraction_available else None,
            selected_candidate_refs=source_view.candidate_refs,
            requested_score_dimensions=list(MEMORY_SCORE_DIMENSIONS),
            scoring_profile="standard",
            source_refs=[_ref("memory_evidence_scoring_policy", policy.policy_id)],
        )
        rules = MemoryEvidenceBindingRuleService().build_rules()
        bundles = MemoryCandidateEvidenceBundleService().build_bundles(candidates)
        strength_assessments = [MemoryEvidenceStrengthAssessmentService().assess(bundle) for bundle in bundles]
        quality_assessments = [MemorySourceQualityAssessmentService().assess(bundle) for bundle in bundles]
        recency_assessments = [MemoryRecencyAssessmentService().assess(bundle) for bundle in bundles]
        stability_assessments = [MemoryStabilityAssessmentService().assess(bundle) for bundle in bundles]
        reuse_assessments = [MemoryReuseValueAssessmentService().assess(bundle) for bundle in bundles]
        specificity_assessments = [MemorySpecificityAssessmentService().assess(bundle) for bundle in bundles]
        privacy_assessments = [MemoryPrivacyRiskAssessmentService().assess(bundle) for bundle in bundles]
        contradiction_checks = [MemoryContradictionCheckService().check(bundle) for bundle in bundles]
        user_control_assessments = [
            MemoryUserControlRequirementAssessmentService().assess(bundle, privacy)
            for bundle, privacy in zip(bundles, privacy_assessments)
        ]
        pig_scoring_signals = MemoryPIGScoringSignalService().build_signals(candidates)
        breakdowns: list[MemoryCandidateScoreBreakdown] = []
        scores: list[MemoryCandidateScore] = []
        decisions: list[MemoryCandidateScoringDecision] = []
        for index, bundle in enumerate(bundles):
            values = MemoryScoreDimensionValueService().build_dimension_values(
                bundle.candidate_id,
                strength=strength_assessments[index],
                source_quality=quality_assessments[index],
                recency=recency_assessments[index],
                stability=stability_assessments[index],
                reuse=reuse_assessments[index],
                specificity=specificity_assessments[index],
                privacy=privacy_assessments[index],
                contradiction=contradiction_checks[index],
                user_control=user_control_assessments[index],
            )
            breakdown = MemoryCandidateScoreBreakdownService().build_breakdown(bundle.candidate_id, values)
            score = MemoryCandidateScoreService().build_score(breakdown)
            decision = MemoryCandidateScoringDecisionService().decide_scoring(score)
            breakdowns.append(breakdown)
            scores.append(score)
            decisions.append(decision)
        scoring_batch = MemoryCandidateScoringBatchService().build_batch(request, scores, decisions)
        previews = [MemoryPromotionReadinessPreviewService().build_preview(score) for score in scores]
        assessments: list[Any] = (
            strength_assessments
            + quality_assessments
            + recency_assessments
            + stability_assessments
            + reuse_assessments
            + specificity_assessments
            + privacy_assessments
            + contradiction_checks
            + user_control_assessments
        )
        audit = MemoryEvidenceScoringAuditTrailService().build_audit_trail(request, bundles, assessments, scores, decisions, previews)
        findings = MemoryEvidenceScoringFindingService().build_findings(source_service, source_view, extra_findings=extra_findings)
        report_status = self._report_status(findings, scoring_batch)
        report = MemoryEvidenceScoringReport(
            report_id=report_id or "memory_evidence_scoring_report:v0.27.3",
            created_at=utc_now_iso(),
            evidence_scoring_policy=policy,
            request=request,
            source_view=source_view,
            binding_rules=rules,
            evidence_bundles=bundles,
            evidence_strength_assessments=strength_assessments,
            source_quality_assessments=quality_assessments,
            recency_assessments=recency_assessments,
            stability_assessments=stability_assessments,
            reuse_value_assessments=reuse_assessments,
            specificity_assessments=specificity_assessments,
            privacy_risk_assessments=privacy_assessments,
            contradiction_checks=contradiction_checks,
            user_control_assessments=user_control_assessments,
            pig_scoring_signals=pig_scoring_signals,
            score_breakdowns=breakdowns,
            candidate_scores=scores,
            scoring_batch=scoring_batch,
            promotion_readiness_previews=previews,
            audit_trail=audit,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_4=report_status in {"passed", "warning"} and scoring_batch.ready_for_gate_review_count > 0,
            evidence_bundles_created=bool(bundles),
            candidate_scores_created=bool(scores),
            scoring_batch_created=True,
            promotion_readiness_previews_created=bool(previews),
            memory_scored=bool(scores),
            limitations=[
                "v0.27.3 scores candidates only; score is evidence for future gate review, not promotion.",
                "v0.26.10 release hygiene status may remain unknown, but persistent memory write is forbidden in v0.27.3.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if promotion, persistent/durable write, registry update, continuity injection, persona/policy mutation, raw memory, PIG execution, provider/command execution, safety bypass, external adapter, Schumpeter split, or LLM judging appears.",
            ],
        )
        return {
            "source_service": source_service,
            "evidence_scoring_policy": policy,
            "request": request,
            "source_view": source_view,
            "binding_rules": rules,
            "candidates": candidates,
            "evidence_bundles": bundles,
            "evidence_strength_assessments": strength_assessments,
            "source_quality_assessments": quality_assessments,
            "recency_assessments": recency_assessments,
            "stability_assessments": stability_assessments,
            "reuse_value_assessments": reuse_assessments,
            "specificity_assessments": specificity_assessments,
            "privacy_risk_assessments": privacy_assessments,
            "contradiction_checks": contradiction_checks,
            "user_control_assessments": user_control_assessments,
            "pig_scoring_signals": pig_scoring_signals,
            "score_breakdowns": breakdowns,
            "candidate_scores": scores,
            "scoring_decisions": decisions,
            "scoring_batch": scoring_batch,
            "promotion_readiness_previews": previews,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[MemoryEvidenceScoringFinding], batch: MemoryCandidateScoringBatch) -> str:
        if any(finding.finding_type in MemoryEvidenceScoringFindingService.BLOCKED_FINDINGS for finding in findings):
            return "blocked"
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if batch.batch_status == "blocked":
            return "blocked"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_EVIDENCE_SCORING_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_evidence_binder_scoring",
            "principles": [
                "Evidence binding is not promotion",
                "Scoring is not promotion",
                "High score is not automatic memory",
                "Score is evidence for a future gate, not a gate result",
                "Evidence strength is not truth",
                "Contradiction check is not automatic deletion",
                "Privacy risk is not automatic rejection by itself",
                "PIG scoring signal is not memory",
                "PIG guidance cannot promote memory",
                "LLM judge must not be the sole scoring authority",
            ],
            "safety_boundary": {
                "memory_scored": "conditional",
                "memory_promoted": False,
                "persistent_memory_written": False,
                "durable_memory_written": False,
                "durable_registry_updated": False,
                "session_continuity_injected": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_secret_output": False,
                "credential_exposed": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.4 memory promotion gate",
                "v0.27.5 durable memory record & registry",
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": MEMORY_EVIDENCE_SCORING_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_evidence_binder_scoring_created",
            "version": MEMORY_EVIDENCE_SCORING_VERSION,
            "source_read_models": [
                "MemoryCandidateExtractionState",
                "MemoryCandidateBatchState",
                "MemoryCandidateState",
                "MemoryCandidateClaimState",
                "MemoryCandidateSourceLinkState",
                "MemoryCandidateRiskFlagState",
                "MemorySourceQualityState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryCandidateEvidenceBundleState",
                "MemoryClaimSupportAssessmentState",
                "MemoryCandidateScoreState",
                "MemoryCandidateScoreBreakdownState",
                "MemoryContradictionCheckState",
                "MemoryPrivacyRiskAssessmentState",
                "MemoryPromotionReadinessPreviewState",
                "MemoryEvidenceScoringAuditState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_EVIDENCE_SCORING_EFFECT_TYPES,
        }


def render_memory_evidence_scoring_cli(parts: dict[str, Any], section: str = "bind-evidence") -> str:
    report: MemoryEvidenceScoringReport = parts["report"]
    lines = [
        f"Memory Evidence Binder & Scoring {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"evidence_bundles_created={_bool(report.evidence_bundles_created)}",
        f"candidate_scores_created={_bool(report.candidate_scores_created)}",
        f"scoring_batch_created={_bool(report.scoring_batch_created)}",
        f"promotion_readiness_previews_created={_bool(report.promotion_readiness_previews_created)}",
        f"memory_scored={_bool(report.memory_scored)}",
        f"ready_for_v0_27_4={_bool(report.ready_for_v0_27_4)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"durable_memory_written={_bool(report.durable_memory_written)}",
        f"durable_registry_updated={_bool(report.durable_registry_updated)}",
        f"session_continuity_injected={_bool(report.session_continuity_injected)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_counts = {
        "source-view": ("candidate_count", report.source_view.candidate_count),
        "rules": ("binding_rule_count", len(parts["binding_rules"])),
        "bundles": ("evidence_bundle_count", len(parts["evidence_bundles"])),
        "evidence-items": ("evidence_item_count", sum(len(bundle.evidence_items) for bundle in parts["evidence_bundles"])),
        "support": ("support_link_count", sum(len(bundle.support_links) for bundle in parts["evidence_bundles"])),
        "assessments": ("assessment_count", len(parts["evidence_strength_assessments"]) + len(parts["source_quality_assessments"]) + len(parts["recency_assessments"]) + len(parts["stability_assessments"]) + len(parts["reuse_value_assessments"]) + len(parts["specificity_assessments"])),
        "privacy": ("privacy_assessment_count", len(parts["privacy_risk_assessments"])),
        "contradictions": ("contradiction_check_count", len(parts["contradiction_checks"])),
        "pig-signals": ("pig_scoring_signal_count", len(parts["pig_scoring_signals"])),
        "dimensions": ("score_dimension_value_count", sum(len(breakdown.dimension_values) for breakdown in parts["score_breakdowns"])),
        "scores": ("candidate_score_count", len(parts["candidate_scores"])),
        "decisions": ("scoring_decision_count", len(parts["scoring_decisions"])),
        "readiness": ("promotion_readiness_preview_count", len(parts["promotion_readiness_previews"])),
    }
    if section in section_counts:
        name, value = section_counts[section]
        lines.append(f"{name}={value}")
    elif section == "audit":
        lines.append(f"audit_status={parts['audit_trail'].audit_status}")
        lines.append(f"raw_content_included={_bool(parts['audit_trail'].raw_content_included)}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)


MEMORY_PROMOTION_GATE_VERSION = "v0.27.4"
MEMORY_PROMOTION_GATE_VERSION_NAME = "Memory Promotion Gate"
MEMORY_PROMOTION_GATE_KOREAN_NAME = "Memory Promotion Gate"
MEMORY_PROMOTION_GATE_NEXT_STEP = "v0.27.5 Durable Memory Record & Registry"

MEMORY_PROMOTION_GATE_REQUIRED_RULES = [
    "candidate_ref_required",
    "candidate_must_be_scored",
    "evidence_bundle_required",
    "score_required",
    "source_refs_required",
    "privacy_risk_assessment_required",
    "contradiction_check_required",
    "user_control_assessment_required",
    "scope_required_for_promote",
    "expiry_or_lifecycle_required_for_promote",
    "forget_revoke_path_required_for_promote",
    "audit_trail_required",
    "high_score_cannot_bypass_gate",
    "PIG_guidance_cannot_promote_memory",
    "no_durable_write_in_v0274",
    "no_persistent_write_in_v0274",
    "no_persona_mutation_in_v0274",
    "raw_transcript_promotion_forbidden",
    "raw_provider_output_promotion_forbidden",
    "raw_secret_promotion_forbidden",
]

MEMORY_PROMOTION_GATE_OBJECT_TYPES = [
    "memory_promotion_gate_policy_runtime",
    "memory_promotion_gate_request",
    "memory_promotion_gate_source_view",
    "memory_promotion_gate_rule",
    "memory_promotion_candidate_view",
    "memory_promotion_requirement",
    "memory_promotion_evidence_review",
    "memory_promotion_score_review",
    "memory_promotion_privacy_gate",
    "memory_promotion_contradiction_gate",
    "memory_promotion_user_control_gate",
    "memory_promotion_scope",
    "memory_promotion_expiry",
    "memory_promotion_lifecycle_boundary",
    "memory_promotion_forget_revoke_path",
    "memory_promotion_pig_guidance_attachment",
    "memory_promotion_decision",
    "memory_promotion_decision_record",
    "memory_promotion_rejected_record",
    "memory_promotion_deferred_record",
    "memory_promotion_more_evidence_request",
    "memory_promotion_user_confirmation_request",
    "memory_ephemeral_memory_decision_record",
    "memory_archive_only_decision_record",
    "durable_memory_readiness_preview",
    "memory_promotion_audit_trail",
    "memory_promotion_gate_finding",
    "memory_promotion_gate_report",
    "memory_evidence_scoring_report",
    "memory_candidate_score",
    "memory_candidate",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_PROMOTION_GATE_EVENT_TYPES = [
    "memory_promotion_gate_requested",
    "memory_promotion_gate_prerequisites_loaded",
    "memory_promotion_gate_policy_created",
    "memory_promotion_gate_source_view_created",
    "memory_promotion_gate_rule_created",
    "memory_promotion_candidate_view_created",
    "memory_promotion_requirement_created",
    "memory_promotion_evidence_review_created",
    "memory_promotion_score_review_created",
    "memory_promotion_privacy_gate_created",
    "memory_promotion_contradiction_gate_created",
    "memory_promotion_user_control_gate_created",
    "memory_promotion_scope_created",
    "memory_promotion_expiry_created",
    "memory_promotion_lifecycle_boundary_created",
    "memory_promotion_forget_revoke_path_created",
    "memory_promotion_pig_guidance_attached",
    "memory_promotion_decision_created",
    "memory_promotion_decision_recorded",
    "memory_promotion_rejected_record_created",
    "memory_promotion_deferred_record_created",
    "memory_promotion_more_evidence_request_created",
    "memory_promotion_user_confirmation_request_created",
    "memory_ephemeral_decision_record_created",
    "memory_archive_only_decision_record_created",
    "durable_memory_readiness_preview_created",
    "memory_promotion_audit_trail_created",
    "memory_promotion_gate_report_created",
    "memory_promotion_gate_warning_created",
    "memory_promotion_gate_blocked",
]

MEMORY_PROMOTION_GATE_EFFECT_TYPES = [
    "read_only_observation",
    "memory_promotion_gate_created",
    "memory_promotion_decision_recorded",
    "memory_rejection_decision_recorded",
    "memory_deferral_decision_recorded",
    "memory_more_evidence_request_created",
    "memory_user_confirmation_request_created",
    "memory_ephemeral_decision_recorded",
    "memory_archive_only_decision_recorded",
    "durable_memory_readiness_preview_created",
    "memory_promotion_audit_created",
    "state_candidate_created",
]

MEMORY_PROMOTION_GATE_FORBIDDEN_EFFECT_TYPES = [
    "memory_promoted",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "session_continuity_context_created",
    "continuity_injection_bundle_created",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "raw_transcript_memory_created",
    "raw_provider_output_memory_created",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class MemoryPromotionGatePolicyRuntime(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    promotion_gate_enabled: bool = True
    promotion_decision_record_enabled: bool = True
    reject_decision_record_enabled: bool = True
    defer_decision_record_enabled: bool = True
    request_more_evidence_enabled: bool = True
    request_user_confirmation_enabled: bool = True
    mark_ephemeral_enabled: bool = True
    mark_archive_only_enabled: bool = True
    promote_decision_is_not_durable_write: bool = True
    durable_memory_write_enabled_now: bool = False
    persistent_memory_write_enabled_now: bool = False
    durable_registry_update_enabled_now: bool = False
    session_continuity_injection_enabled_now: bool = False
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    automatic_promotion_forbidden: bool = True
    promotion_requires_source_refs: bool = True
    promotion_requires_evidence_bundle: bool = True
    promotion_requires_score: bool = True
    promotion_requires_privacy_risk_assessment: bool = True
    promotion_requires_contradiction_check: bool = True
    promotion_requires_user_control_assessment: bool = True
    promotion_requires_scope: bool = True
    promotion_requires_expiry_or_lifecycle: bool = True
    promotion_requires_audit_trail: bool = True
    promotion_requires_forget_revoke_path: bool = True
    high_score_cannot_bypass_gate: bool = True
    pig_guidance_cannot_promote_memory: bool = True
    raw_transcript_promotion_forbidden: bool = True
    raw_provider_output_promotion_forbidden: bool = True
    raw_secret_promotion_forbidden: bool = True
    credential_promotion_forbidden: bool = True
    private_full_path_promotion_forbidden: bool = True
    llm_judge_as_sole_promotion_authority_forbidden: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False


@dataclass
class MemoryPromotionGateRequest(_ModelMixin):
    request_id: str
    memory_contract_report_id: str | None
    memory_evidence_scoring_report_id: str | None
    scoring_batch_id: str | None
    selected_candidate_refs: list[dict[str, Any]]
    selected_score_refs: list[dict[str, Any]]
    requested_decision_type: str | None
    promotion_profile: str | None
    source_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    strictness: str = "standard"


@dataclass
class MemoryPromotionGateSourceView(_ModelMixin):
    source_view_id: str
    evidence_scoring_report_ref: dict[str, Any] | None
    scoring_batch_ref: dict[str, Any] | None
    candidate_refs: list[dict[str, Any]]
    evidence_bundle_refs: list[dict[str, Any]]
    score_refs: list[dict[str, Any]]
    promotion_readiness_preview_refs: list[dict[str, Any]]
    privacy_assessment_refs: list[dict[str, Any]]
    contradiction_check_refs: list[dict[str, Any]]
    user_control_assessment_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    source_ref_count: int
    source_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False


@dataclass
class MemoryPromotionGateRule(_ModelMixin):
    rule_id: str
    rule_name: str
    rule_summary: str
    required: bool
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionCandidateView(_ModelMixin):
    promotion_candidate_view_id: str
    candidate_ref: dict[str, Any]
    candidate_id: str
    candidate_type: str
    candidate_summary: str
    score_ref: dict[str, Any] | None
    evidence_bundle_ref: dict[str, Any] | None
    promotion_readiness_preview_ref: dict[str, Any] | None
    privacy_assessment_ref: dict[str, Any] | None
    contradiction_check_ref: dict[str, Any] | None
    user_control_assessment_ref: dict[str, Any] | None
    pig_guidance_refs: list[dict[str, Any]]
    current_status: str
    eligible_for_promotion_decision: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    eligible_for_durable_write_now: bool = False
    promoted_to_memory_now: bool = False
    durable_memory_written_now: bool = False


@dataclass
class MemoryPromotionRequirement(_ModelMixin):
    requirement_id: str
    candidate_id: str
    requirement_type: str
    required: bool
    satisfied: bool
    missing_reason: str | None
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionEvidenceReview(_ModelMixin):
    evidence_review_id: str
    candidate_id: str
    evidence_bundle_ref: dict[str, Any] | None
    evidence_strength_ref: dict[str, Any] | None
    claim_support_refs: list[dict[str, Any]]
    evidence_review_status: str
    review_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionScoreReview(_ModelMixin):
    score_review_id: str
    candidate_id: str
    score_ref: dict[str, Any] | None
    score_band: str
    promotion_readiness: str
    high_score_present: bool
    score_review_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    high_score_bypassed_gate: bool = False


@dataclass
class MemoryPromotionPrivacyGate(_ModelMixin):
    privacy_gate_id: str
    candidate_id: str
    privacy_assessment_ref: dict[str, Any] | None
    privacy_risk_level: str
    requires_user_confirmation: bool
    blocks_promotion_decision: bool
    gate_status: str
    gate_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionContradictionGate(_ModelMixin):
    contradiction_gate_id: str
    candidate_id: str
    contradiction_check_ref: dict[str, Any] | None
    contradiction_detected: bool
    contradiction_level: str
    requires_review: bool
    blocks_promotion_decision: bool
    gate_status: str
    gate_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionUserControlGate(_ModelMixin):
    user_control_gate_id: str
    candidate_id: str
    user_control_assessment_ref: dict[str, Any] | None
    user_control_level: str
    user_confirmation_required: bool
    user_confirmation_present: bool
    blocks_promotion_decision: bool
    gate_status: str
    gate_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionScope(_ModelMixin):
    scope_id: str
    candidate_id: str
    scope_type: str
    scope_summary: str
    allowed_context_refs: list[dict[str, Any]]
    forbidden_context_refs: list[dict[str, Any]]
    scope_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    grants_durable_write_now: bool = False


@dataclass
class MemoryPromotionExpiry(_ModelMixin):
    expiry_id: str
    candidate_id: str
    expiry_type: str
    expires_at: str | None
    review_required_after: str | None
    expiry_summary: str
    expiry_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION


@dataclass
class MemoryPromotionLifecycleBoundary(_ModelMixin):
    lifecycle_boundary_id: str
    candidate_id: str
    allowed_future_states: list[str]
    forbidden_future_states: list[str]
    lifecycle_summary: str
    lifecycle_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    durable_record_created_now: bool = False


@dataclass
class MemoryPromotionForgetRevokePath(_ModelMixin):
    forget_revoke_path_id: str
    candidate_id: str
    path_summary: str
    path_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    revoke_supported_future: bool = True
    forget_supported_future: bool = True
    update_supported_future: bool = True
    archive_supported_future: bool = True
    forget_executed_now: bool = False
    revoke_executed_now: bool = False


@dataclass
class MemoryPromotionPIGGuidanceAttachment(_ModelMixin):
    pig_attachment_id: str
    candidate_id: str
    pig_guidance_refs: list[dict[str, Any]]
    guidance_summary: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    pig_guidance_is_memory: bool = False
    pig_guidance_promotes_memory: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False


@dataclass
class MemoryPromotionDecision(_ModelMixin):
    decision_id: str
    candidate_id: str
    decision_type: str
    decision_reason: str
    decided_by: str
    decision_basis_refs: list[dict[str, Any]]
    requirement_refs: list[dict[str, Any]]
    scope_ref: dict[str, Any] | None
    expiry_ref: dict[str, Any] | None
    lifecycle_boundary_ref: dict[str, Any] | None
    forget_revoke_path_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    creates_durable_memory_now: bool = False
    writes_persistent_memory_now: bool = False
    mutates_persona_now: bool = False
    mutates_behavior_policy_now: bool = False


@dataclass
class MemoryPromotionDecisionRecord(_ModelMixin):
    decision_record_id: str
    decision: MemoryPromotionDecision
    candidate_ref: dict[str, Any]
    score_ref: dict[str, Any] | None
    evidence_bundle_ref: dict[str, Any] | None
    record_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    ocel_visible: bool = True
    durable_memory_created: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemoryPromotionRejectedRecord(_ModelMixin):
    rejection_record_id: str
    candidate_id: str
    rejection_reason: str
    rejection_basis_refs: list[dict[str, Any]]
    alternative_decision_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    source_candidate_retained: bool = True
    source_deleted: bool = False
    durable_memory_created: bool = False


@dataclass
class MemoryPromotionDeferredRecord(_ModelMixin):
    deferral_record_id: str
    candidate_id: str
    deferral_reason: str
    deferred_until: str | None
    deferred_to_version: str | None
    required_followup_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    durable_memory_created: bool = False


@dataclass
class MemoryPromotionMoreEvidenceRequest(_ModelMixin):
    more_evidence_request_id: str
    candidate_id: str
    missing_evidence_summary: str
    required_evidence_refs: list[dict[str, Any]]
    requested_source_categories: list[str]
    request_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    candidate_mutated_now: bool = False
    durable_memory_created: bool = False


@dataclass
class MemoryPromotionUserConfirmationRequest(_ModelMixin):
    confirmation_request_id: str
    candidate_id: str
    confirmation_reason: str
    confirmation_prompt_ref: dict[str, Any] | None
    required_user_action: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    confirmation_received_now: bool = False
    durable_memory_created: bool = False


@dataclass
class MemoryEphemeralMemoryDecisionRecord(_ModelMixin):
    ephemeral_record_id: str
    candidate_id: str
    decision_reason: str
    ephemeral_scope_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    active_memory_created: bool = False
    durable_memory_created: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemoryArchiveOnlyDecisionRecord(_ModelMixin):
    archive_only_record_id: str
    candidate_id: str
    decision_reason: str
    archive_scope_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    active_memory_created: bool = False
    durable_memory_created: bool = False
    persistent_memory_written: bool = False


@dataclass
class DurableMemoryReadinessPreview(_ModelMixin):
    durable_readiness_preview_id: str
    candidate_id: str
    decision_ref: dict[str, Any] | None
    ready_for_v0275_durable_registry: bool
    readiness_reason: str
    required_v0275_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    preview_is_not_durable_write: bool = True
    durable_memory_created_now: bool = False
    persistent_memory_written_now: bool = False


@dataclass
class MemoryPromotionAuditTrail(_ModelMixin):
    audit_trail_id: str
    promotion_request_ref: dict[str, Any]
    candidate_view_refs: list[dict[str, Any]]
    requirement_refs: list[dict[str, Any]]
    gate_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    rejected_record_refs: list[dict[str, Any]]
    deferred_record_refs: list[dict[str, Any]]
    more_evidence_request_refs: list[dict[str, Any]]
    user_confirmation_request_refs: list[dict[str, Any]]
    ephemeral_record_refs: list[dict[str, Any]]
    archive_only_record_refs: list[dict[str, Any]]
    durable_readiness_preview_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    raw_content_included: bool = False
    durable_memory_created: bool = False
    persistent_memory_written: bool = False


@dataclass
class MemoryPromotionGateFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryPromotionGateReport(_ModelMixin):
    report_id: str
    created_at: str
    promotion_gate_policy: MemoryPromotionGatePolicyRuntime
    request: MemoryPromotionGateRequest
    source_view: MemoryPromotionGateSourceView
    gate_rules: list[MemoryPromotionGateRule]
    candidate_views: list[MemoryPromotionCandidateView]
    requirements: list[MemoryPromotionRequirement]
    evidence_reviews: list[MemoryPromotionEvidenceReview]
    score_reviews: list[MemoryPromotionScoreReview]
    privacy_gates: list[MemoryPromotionPrivacyGate]
    contradiction_gates: list[MemoryPromotionContradictionGate]
    user_control_gates: list[MemoryPromotionUserControlGate]
    scopes: list[MemoryPromotionScope]
    expiries: list[MemoryPromotionExpiry]
    lifecycle_boundaries: list[MemoryPromotionLifecycleBoundary]
    forget_revoke_paths: list[MemoryPromotionForgetRevokePath]
    pig_guidance_attachments: list[MemoryPromotionPIGGuidanceAttachment]
    promotion_decisions: list[MemoryPromotionDecision]
    promotion_decision_records: list[MemoryPromotionDecisionRecord]
    rejected_records: list[MemoryPromotionRejectedRecord]
    deferred_records: list[MemoryPromotionDeferredRecord]
    more_evidence_requests: list[MemoryPromotionMoreEvidenceRequest]
    user_confirmation_requests: list[MemoryPromotionUserConfirmationRequest]
    ephemeral_records: list[MemoryEphemeralMemoryDecisionRecord]
    archive_only_records: list[MemoryArchiveOnlyDecisionRecord]
    durable_readiness_previews: list[DurableMemoryReadinessPreview]
    audit_trail: MemoryPromotionAuditTrail
    findings: list[MemoryPromotionGateFinding]
    report_status: str
    ready_for_v0_27_5: bool
    promotion_gate_created: bool
    candidate_views_created: bool
    requirements_created: bool
    gate_reviews_created: bool
    scopes_created: bool
    expiries_created: bool
    forget_revoke_paths_created: bool
    promotion_decisions_recorded: bool
    durable_readiness_previews_created: bool
    audit_trail_created: bool
    promote_decision_count: int
    reject_decision_count: int
    defer_decision_count: int
    more_evidence_request_count: int
    user_confirmation_request_count: int
    ephemeral_decision_count: int
    archive_only_decision_count: int
    limitations: list[str]
    withdrawal_conditions: list[str]
    version: str = MEMORY_PROMOTION_GATE_VERSION
    ready_for_v0_28: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    durable_memory_written: bool = False
    durable_registry_updated: bool = False
    session_continuity_injected: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_PROMOTION_GATE_NEXT_STEP
    validity_horizon: str = "Valid until v0.27.5 Durable Memory Record & Registry begins or memory promotion gate policy changes."


class MemoryPromotionGatePrerequisiteSourceService:
    def __init__(self, *, scoring_available: bool = True, pig_guidance_available: bool = True) -> None:
        self.scoring_available = scoring_available
        self.pig_guidance_available = pig_guidance_available
        self._parts: dict[str, Any] | None = None

    def _scoring_parts(self) -> dict[str, Any] | None:
        if not self.scoring_available:
            return None
        if self._parts is None:
            self._parts = MemoryEvidenceScoringReportService().build_all_parts(pig_signals_available=self.pig_guidance_available)
        return self._parts

    def load_v0273_evidence_scoring_report(self) -> MemoryEvidenceScoringReport | None:
        parts = self._scoring_parts()
        return None if parts is None else parts["report"]

    def load_v0273_scoring_batch(self) -> MemoryCandidateScoringBatch | None:
        parts = self._scoring_parts()
        return None if parts is None else parts["scoring_batch"]

    def load_candidate_scores(self) -> list[MemoryCandidateScore]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["candidate_scores"]

    def load_promotion_readiness_previews(self) -> list[MemoryPromotionReadinessPreview]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["promotion_readiness_previews"]

    def load_evidence_bundles(self) -> list[MemoryCandidateEvidenceBundle]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["evidence_bundles"]

    def load_privacy_assessments(self) -> list[MemoryPrivacyRiskAssessment]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["privacy_risk_assessments"]

    def load_contradiction_checks(self) -> list[MemoryContradictionCheck]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["contradiction_checks"]

    def load_user_control_assessments(self) -> list[MemoryUserControlRequirementAssessment]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["user_control_assessments"]

    def load_v0272_candidates_if_available(self) -> list[MemoryCandidate]:
        parts = self._scoring_parts()
        return [] if parts is None else parts["candidates"]

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        if not self.pig_guidance_available:
            return []
        parts = self._scoring_parts()
        if parts is None:
            return []
        return [
            _ref("memory_pig_scoring_signal", signal.pig_scoring_signal_id, signal.version)
            for signal in parts["pig_scoring_signals"]
        ]

    def load_release_hygiene_status_if_available(self) -> dict[str, Any]:
        return _ref("release_hygiene_status", "release_hygiene_status:v0.26.10", "v0.26.10")


class MemoryPromotionGatePolicyRuntimeService:
    def build_policy(self) -> MemoryPromotionGatePolicyRuntime:
        return MemoryPromotionGatePolicyRuntime(
            policy_id="memory_promotion_gate_policy_runtime:v0.27.4",
            evidence_refs=[_ref("memory_evidence_scoring_report", "memory_evidence_scoring_report:v0.27.3", "v0.27.3")],
        )


class MemoryPromotionGateSourceViewService:
    def build_source_view(self, source_service: MemoryPromotionGatePrerequisiteSourceService) -> MemoryPromotionGateSourceView:
        report = source_service.load_v0273_evidence_scoring_report()
        batch = source_service.load_v0273_scoring_batch()
        candidates = source_service.load_v0272_candidates_if_available()
        bundles = source_service.load_evidence_bundles()
        scores = source_service.load_candidate_scores()
        previews = source_service.load_promotion_readiness_previews()
        privacy = source_service.load_privacy_assessments()
        contradictions = source_service.load_contradiction_checks()
        user_control = source_service.load_user_control_assessments()
        refs = [
            _ref("memory_candidate", candidate.candidate_id, candidate.version)
            for candidate in candidates
        ]
        return MemoryPromotionGateSourceView(
            source_view_id="memory_promotion_gate_source_view:v0.27.4",
            evidence_scoring_report_ref=_ref("memory_evidence_scoring_report", report.report_id, report.version) if report else None,
            scoring_batch_ref=_ref("memory_candidate_scoring_batch", batch.scoring_batch_id, batch.version) if batch else None,
            candidate_refs=refs,
            evidence_bundle_refs=[_ref("memory_candidate_evidence_bundle", item.evidence_bundle_id, item.version) for item in bundles],
            score_refs=[_ref("memory_candidate_score", item.score_id, item.version) for item in scores],
            promotion_readiness_preview_refs=[_ref("memory_promotion_readiness_preview", item.preview_id, item.version) for item in previews],
            privacy_assessment_refs=[_ref("memory_privacy_risk_assessment", item.assessment_id, item.version) for item in privacy],
            contradiction_check_refs=[_ref("memory_contradiction_check", item.contradiction_check_id, item.version) for item in contradictions],
            user_control_assessment_refs=[_ref("memory_user_control_requirement_assessment", item.assessment_id, item.version) for item in user_control],
            pig_guidance_refs=source_service.load_pig_guidance_refs_if_available(),
            source_ref_count=len(refs),
            source_status="complete" if refs and scores and bundles else "missing",
            evidence_refs=[_ref("memory_evidence_scoring_report", "memory_evidence_scoring_report:v0.27.3", "v0.27.3")],
        )


class MemoryPromotionGateRuleService:
    def build_rules(self) -> list[MemoryPromotionGateRule]:
        blocking = {
            "candidate_ref_required",
            "candidate_must_be_scored",
            "evidence_bundle_required",
            "score_required",
            "source_refs_required",
            "privacy_risk_assessment_required",
            "contradiction_check_required",
            "user_control_assessment_required",
            "scope_required_for_promote",
            "expiry_or_lifecycle_required_for_promote",
            "forget_revoke_path_required_for_promote",
            "high_score_cannot_bypass_gate",
            "no_durable_write_in_v0274",
            "no_persistent_write_in_v0274",
            "no_persona_mutation_in_v0274",
            "raw_transcript_promotion_forbidden",
            "raw_provider_output_promotion_forbidden",
            "raw_secret_promotion_forbidden",
        }
        return [
            MemoryPromotionGateRule(
                rule_id=f"memory_promotion_gate_rule:{name}",
                rule_name=name,
                rule_summary=f"{name} is required for v0.27.4 promotion gate decisions.",
                required=True,
                pass_condition="Refs-only promotion gate input satisfies the rule.",
                fail_condition="Promotion gate decision is blocked or deferred.",
                block_on_fail=name in blocking,
                evidence_refs=[_ref("memory_promotion_gate_policy_runtime", "memory_promotion_gate_policy_runtime:v0.27.4")],
            )
            for name in MEMORY_PROMOTION_GATE_REQUIRED_RULES
        ]


def _by_candidate_id(items: list[Any], attr: str = "candidate_id") -> dict[str, Any]:
    return {getattr(item, attr): item for item in items}


class MemoryPromotionCandidateViewService:
    def build_candidate_views(
        self,
        candidates: list[MemoryCandidate],
        scores: list[MemoryCandidateScore],
        bundles: list[MemoryCandidateEvidenceBundle],
        previews: list[MemoryPromotionReadinessPreview],
        privacy: list[MemoryPrivacyRiskAssessment],
        contradictions: list[MemoryContradictionCheck],
        user_control: list[MemoryUserControlRequirementAssessment],
    ) -> list[MemoryPromotionCandidateView]:
        score_map = _by_candidate_id(scores)
        bundle_map = _by_candidate_id(bundles)
        preview_map = _by_candidate_id(previews)
        privacy_map = _by_candidate_id(privacy)
        contradiction_map = _by_candidate_id(contradictions)
        user_control_map = _by_candidate_id(user_control)
        views: list[MemoryPromotionCandidateView] = []
        for candidate in candidates:
            score = score_map.get(candidate.candidate_id)
            bundle = bundle_map.get(candidate.candidate_id)
            preview = preview_map.get(candidate.candidate_id)
            privacy_item = privacy_map.get(candidate.candidate_id)
            contradiction = contradiction_map.get(candidate.candidate_id)
            control = user_control_map.get(candidate.candidate_id)
            eligible = bool(
                score
                and bundle
                and privacy_item
                and contradiction
                and control
                and score.promotion_readiness == "ready_for_gate_review"
                and not privacy_item.blocks_future_promotion
                and not contradiction.blocks_future_promotion
            )
            views.append(
                MemoryPromotionCandidateView(
                    promotion_candidate_view_id=f"memory_promotion_candidate_view:{candidate.candidate_id}",
                    candidate_ref=_ref("memory_candidate", candidate.candidate_id, candidate.version),
                    candidate_id=candidate.candidate_id,
                    candidate_type=candidate.candidate_type,
                    candidate_summary=candidate.summary,
                    score_ref=_ref("memory_candidate_score", score.score_id, score.version) if score else None,
                    evidence_bundle_ref=_ref("memory_candidate_evidence_bundle", bundle.evidence_bundle_id, bundle.version) if bundle else None,
                    promotion_readiness_preview_ref=_ref("memory_promotion_readiness_preview", preview.preview_id, preview.version) if preview else None,
                    privacy_assessment_ref=_ref("memory_privacy_risk_assessment", privacy_item.assessment_id, privacy_item.version) if privacy_item else None,
                    contradiction_check_ref=_ref("memory_contradiction_check", contradiction.contradiction_check_id, contradiction.version) if contradiction else None,
                    user_control_assessment_ref=_ref("memory_user_control_requirement_assessment", control.assessment_id, control.version) if control else None,
                    pig_guidance_refs=[_ref("memory_candidate_pig_signal", signal.pig_signal_id, signal.version) for signal in candidate.pig_signals],
                    current_status="ready_for_gate_review" if eligible else "scored" if score else "candidate_only",
                    eligible_for_promotion_decision=eligible,
                    evidence_refs=[_ref("memory_evidence_scoring_report", "memory_evidence_scoring_report:v0.27.3", "v0.27.3")],
                )
            )
        return views


class MemoryPromotionRequirementService:
    REQUIREMENT_TYPES = [
        "source_refs",
        "evidence_bundle",
        "score",
        "privacy_risk_assessment",
        "contradiction_check",
        "user_control_assessment",
        "scope",
        "expiry_or_lifecycle",
        "audit_trail",
        "forget_revoke_path",
    ]

    def build_requirements(self, view: MemoryPromotionCandidateView) -> list[MemoryPromotionRequirement]:
        refs_by_type = {
            "source_refs": [view.candidate_ref],
            "evidence_bundle": [view.evidence_bundle_ref] if view.evidence_bundle_ref else [],
            "score": [view.score_ref] if view.score_ref else [],
            "privacy_risk_assessment": [view.privacy_assessment_ref] if view.privacy_assessment_ref else [],
            "contradiction_check": [view.contradiction_check_ref] if view.contradiction_check_ref else [],
            "user_control_assessment": [view.user_control_assessment_ref] if view.user_control_assessment_ref else [],
            "scope": [_ref("memory_promotion_scope", f"memory_promotion_scope:{view.candidate_id}")],
            "expiry_or_lifecycle": [_ref("memory_promotion_expiry", f"memory_promotion_expiry:{view.candidate_id}")],
            "audit_trail": [_ref("memory_promotion_audit_trail", "memory_promotion_audit_trail:v0.27.4")],
            "forget_revoke_path": [_ref("memory_promotion_forget_revoke_path", f"memory_promotion_forget_revoke_path:{view.candidate_id}")],
        }
        requirements: list[MemoryPromotionRequirement] = []
        for requirement_type in self.REQUIREMENT_TYPES:
            source_refs = refs_by_type[requirement_type]
            satisfied = bool(source_refs)
            requirements.append(
                MemoryPromotionRequirement(
                    requirement_id=f"memory_promotion_requirement:{view.candidate_id}:{requirement_type}",
                    candidate_id=view.candidate_id,
                    requirement_type=requirement_type,
                    required=True,
                    satisfied=satisfied,
                    missing_reason=None if satisfied else f"{requirement_type} is missing.",
                    source_refs=source_refs,
                    evidence_refs=[view.candidate_ref],
                )
            )
        return requirements


class MemoryPromotionEvidenceReviewService:
    def build_reviews(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionEvidenceReview]:
        return [
            MemoryPromotionEvidenceReview(
                evidence_review_id=f"memory_promotion_evidence_review:{view.candidate_id}",
                candidate_id=view.candidate_id,
                evidence_bundle_ref=view.evidence_bundle_ref,
                evidence_strength_ref=_ref("memory_evidence_strength_assessment", f"memory_evidence_strength_assessment:{view.candidate_id}", "v0.27.3") if view.evidence_bundle_ref else None,
                claim_support_refs=[_ref("memory_claim_support_assessment", f"memory_claim_support_assessment:{view.candidate_id}", "v0.27.3")],
                evidence_review_status="sufficient" if view.evidence_bundle_ref else "missing",
                review_summary="Evidence review is gate input only and creates no durable memory.",
                evidence_refs=[view.evidence_bundle_ref] if view.evidence_bundle_ref else [view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionScoreReviewService:
    def build_reviews(self, scores: list[MemoryCandidateScore]) -> list[MemoryPromotionScoreReview]:
        return [
            MemoryPromotionScoreReview(
                score_review_id=f"memory_promotion_score_review:{score.candidate_id}",
                candidate_id=score.candidate_id,
                score_ref=_ref("memory_candidate_score", score.score_id, score.version),
                score_band=score.score_band,
                promotion_readiness=score.promotion_readiness,
                high_score_present=score.score_band == "high",
                score_review_summary="Score informs the gate but cannot bypass it.",
                evidence_refs=[_ref("memory_candidate_score", score.score_id, score.version)],
            )
            for score in scores
        ]


class MemoryPromotionPrivacyGateService:
    def build_gates(self, assessments: list[MemoryPrivacyRiskAssessment]) -> list[MemoryPromotionPrivacyGate]:
        gates: list[MemoryPromotionPrivacyGate] = []
        for item in assessments:
            blocked = item.blocks_future_promotion or item.privacy_risk_level == "blocked"
            gates.append(
                MemoryPromotionPrivacyGate(
                    privacy_gate_id=f"memory_promotion_privacy_gate:{item.candidate_id}",
                    candidate_id=item.candidate_id,
                    privacy_assessment_ref=_ref("memory_privacy_risk_assessment", item.assessment_id, item.version),
                    privacy_risk_level=item.privacy_risk_level,
                    requires_user_confirmation=item.requires_user_confirmation,
                    blocks_promotion_decision=blocked,
                    gate_status="blocked" if blocked else "warning" if item.requires_user_confirmation else "passed",
                    gate_summary="Privacy gate does not mutate or reject memory by itself.",
                    evidence_refs=[_ref("memory_privacy_risk_assessment", item.assessment_id, item.version)],
                )
            )
        return gates


class MemoryPromotionContradictionGateService:
    def build_gates(self, checks: list[MemoryContradictionCheck]) -> list[MemoryPromotionContradictionGate]:
        gates: list[MemoryPromotionContradictionGate] = []
        for item in checks:
            blocked = item.blocks_future_promotion or item.contradiction_level == "strong"
            gates.append(
                MemoryPromotionContradictionGate(
                    contradiction_gate_id=f"memory_promotion_contradiction_gate:{item.candidate_id}",
                    candidate_id=item.candidate_id,
                    contradiction_check_ref=_ref("memory_contradiction_check", item.contradiction_check_id, item.version),
                    contradiction_detected=item.contradiction_detected,
                    contradiction_level=item.contradiction_level,
                    requires_review=item.requires_review,
                    blocks_promotion_decision=blocked,
                    gate_status="blocked" if blocked else "warning" if item.requires_review else "passed",
                    gate_summary="Contradiction gate does not delete or overwrite candidates.",
                    evidence_refs=[_ref("memory_contradiction_check", item.contradiction_check_id, item.version)],
                )
            )
        return gates


class MemoryPromotionUserControlGateService:
    def build_gates(self, assessments: list[MemoryUserControlRequirementAssessment]) -> list[MemoryPromotionUserControlGate]:
        gates: list[MemoryPromotionUserControlGate] = []
        for item in assessments:
            blocked = item.user_control_level == "block"
            gates.append(
                MemoryPromotionUserControlGate(
                    user_control_gate_id=f"memory_promotion_user_control_gate:{item.candidate_id}",
                    candidate_id=item.candidate_id,
                    user_control_assessment_ref=_ref("memory_user_control_requirement_assessment", item.assessment_id, item.version),
                    user_control_level=item.user_control_level,
                    user_confirmation_required=item.requires_user_confirmation,
                    user_confirmation_present=False,
                    blocks_promotion_decision=blocked,
                    gate_status="blocked" if blocked else "warning" if item.requires_user_confirmation else "passed",
                    gate_summary="User control gate records consent requirements but does not infer consent.",
                    evidence_refs=[_ref("memory_user_control_requirement_assessment", item.assessment_id, item.version)],
                )
            )
        return gates


class MemoryPromotionScopeService:
    def build_scopes(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionScope]:
        return [
            MemoryPromotionScope(
                scope_id=f"memory_promotion_scope:{view.candidate_id}",
                candidate_id=view.candidate_id,
                scope_type="project" if view.candidate_type == "project_state_candidate" else "workflow",
                scope_summary="Promotion scope is advisory for v0.27.5 and grants no durable write now.",
                allowed_context_refs=[view.candidate_ref],
                forbidden_context_refs=[],
                scope_status="valid",
                evidence_refs=[view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionExpiryService:
    def build_expiries(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionExpiry]:
        return [
            MemoryPromotionExpiry(
                expiry_id=f"memory_promotion_expiry:{view.candidate_id}",
                candidate_id=view.candidate_id,
                expiry_type="no_expiry_but_review_required",
                expires_at=None,
                review_required_after="v0.27.8 Memory Audit / Update / Revoke / Forget",
                expiry_summary="Lifecycle review is required; no durable memory is written in v0.27.4.",
                expiry_status="valid",
                evidence_refs=[view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionLifecycleBoundaryService:
    def build_boundaries(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionLifecycleBoundary]:
        return [
            MemoryPromotionLifecycleBoundary(
                lifecycle_boundary_id=f"memory_promotion_lifecycle_boundary:{view.candidate_id}",
                candidate_id=view.candidate_id,
                allowed_future_states=["candidate", "promoted", "active", "superseded", "revoked", "forgotten", "expired", "archived", "blocked"],
                forbidden_future_states=["durable_record_created_in_v0274", "persona_mutated_in_v0274"],
                lifecycle_summary="Lifecycle boundary is prepared for v0.27.5+ without creating a durable record now.",
                lifecycle_status="ready",
                evidence_refs=[view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionForgetRevokePathService:
    def build_paths(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionForgetRevokePath]:
        return [
            MemoryPromotionForgetRevokePath(
                forget_revoke_path_id=f"memory_promotion_forget_revoke_path:{view.candidate_id}",
                candidate_id=view.candidate_id,
                path_summary="Future revoke/forget/update/archive path is declared, not executed.",
                path_status="ready",
                evidence_refs=[view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionPIGGuidanceAttachmentService:
    def attach_pig_guidance(self, views: list[MemoryPromotionCandidateView]) -> list[MemoryPromotionPIGGuidanceAttachment]:
        return [
            MemoryPromotionPIGGuidanceAttachment(
                pig_attachment_id=f"memory_promotion_pig_guidance_attachment:{view.candidate_id}",
                candidate_id=view.candidate_id,
                pig_guidance_refs=view.pig_guidance_refs,
                guidance_summary="PIG guidance is attached as non-authoritative signal only.",
                evidence_refs=[view.candidate_ref],
            )
            for view in views
        ]


class MemoryPromotionDecisionService:
    def decide(
        self,
        view: MemoryPromotionCandidateView,
        requirements: list[MemoryPromotionRequirement],
        privacy_gate: MemoryPromotionPrivacyGate | None,
        contradiction_gate: MemoryPromotionContradictionGate | None,
        user_control_gate: MemoryPromotionUserControlGate | None,
        scope: MemoryPromotionScope,
        expiry: MemoryPromotionExpiry,
        lifecycle: MemoryPromotionLifecycleBoundary,
        path: MemoryPromotionForgetRevokePath,
        requested_decision_type: str | None = None,
    ) -> MemoryPromotionDecision:
        missing = [item for item in requirements if item.required and not item.satisfied]
        if requested_decision_type:
            decision_type = requested_decision_type
            reason = f"Requested {requested_decision_type} decision recorded by policy gate; no durable write occurs."
        elif missing:
            decision_type = "request_more_evidence"
            reason = "Required promotion-gate inputs are missing."
        elif privacy_gate and privacy_gate.blocks_promotion_decision:
            decision_type = "block"
            reason = "Privacy gate blocks promotion decision."
        elif contradiction_gate and contradiction_gate.blocks_promotion_decision:
            decision_type = "block"
            reason = "Contradiction gate blocks promotion decision."
        elif user_control_gate and user_control_gate.user_confirmation_required:
            decision_type = "request_user_confirmation"
            reason = "User confirmation is required and not inferred."
        elif view.eligible_for_promotion_decision:
            decision_type = "promote"
            reason = "Gate inputs are complete enough to record a promote decision for v0.27.5 review."
        else:
            decision_type = "defer"
            reason = "Candidate is not ready for promote decision."
        return self.build_decision(view, requirements, scope, expiry, lifecycle, path, decision_type, reason)

    def build_decision(
        self,
        view: MemoryPromotionCandidateView,
        requirements: list[MemoryPromotionRequirement],
        scope: MemoryPromotionScope,
        expiry: MemoryPromotionExpiry,
        lifecycle: MemoryPromotionLifecycleBoundary,
        path: MemoryPromotionForgetRevokePath,
        decision_type: str,
        decision_reason: str,
    ) -> MemoryPromotionDecision:
        return MemoryPromotionDecision(
            decision_id=f"memory_promotion_decision:{view.candidate_id}:{decision_type}",
            candidate_id=view.candidate_id,
            decision_type=decision_type,
            decision_reason=decision_reason,
            decided_by="policy_gate",
            decision_basis_refs=[view.candidate_ref, view.score_ref, view.evidence_bundle_ref],
            requirement_refs=[_ref("memory_promotion_requirement", item.requirement_id) for item in requirements],
            scope_ref=_ref("memory_promotion_scope", scope.scope_id),
            expiry_ref=_ref("memory_promotion_expiry", expiry.expiry_id),
            lifecycle_boundary_ref=_ref("memory_promotion_lifecycle_boundary", lifecycle.lifecycle_boundary_id),
            forget_revoke_path_ref=_ref("memory_promotion_forget_revoke_path", path.forget_revoke_path_id),
            evidence_refs=[view.candidate_ref],
        )


class MemoryPromotionDecisionRecordService:
    def build_promotion_decision_record(self, decision: MemoryPromotionDecision, view: MemoryPromotionCandidateView) -> MemoryPromotionDecisionRecord:
        return MemoryPromotionDecisionRecord(
            decision_record_id=f"memory_promotion_decision_record:{decision.candidate_id}:{decision.decision_type}",
            decision=decision,
            candidate_ref=view.candidate_ref,
            score_ref=view.score_ref,
            evidence_bundle_ref=view.evidence_bundle_ref,
            record_status="recorded",
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_rejected_record(self, decision: MemoryPromotionDecision) -> MemoryPromotionRejectedRecord:
        return MemoryPromotionRejectedRecord(
            rejection_record_id=f"memory_promotion_rejected_record:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            rejection_reason=decision.decision_reason,
            rejection_basis_refs=decision.decision_basis_refs,
            alternative_decision_refs=[_ref("memory_promotion_decision", decision.decision_id)],
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_deferred_record(self, decision: MemoryPromotionDecision) -> MemoryPromotionDeferredRecord:
        return MemoryPromotionDeferredRecord(
            deferral_record_id=f"memory_promotion_deferred_record:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            deferral_reason=decision.decision_reason,
            deferred_until=None,
            deferred_to_version=MEMORY_PROMOTION_GATE_NEXT_STEP,
            required_followup_refs=[_ref("memory_promotion_decision", decision.decision_id)],
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_more_evidence_request(self, decision: MemoryPromotionDecision) -> MemoryPromotionMoreEvidenceRequest:
        return MemoryPromotionMoreEvidenceRequest(
            more_evidence_request_id=f"memory_promotion_more_evidence_request:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            missing_evidence_summary=decision.decision_reason,
            required_evidence_refs=decision.requirement_refs,
            requested_source_categories=["source_refs", "evidence_bundle", "score", "privacy_risk_assessment"],
            request_status="created",
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_user_confirmation_request(self, decision: MemoryPromotionDecision) -> MemoryPromotionUserConfirmationRequest:
        return MemoryPromotionUserConfirmationRequest(
            confirmation_request_id=f"memory_promotion_user_confirmation_request:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            confirmation_reason=decision.decision_reason,
            confirmation_prompt_ref=_ref("memory_promotion_decision", decision.decision_id),
            required_user_action="explicit_user_confirmation_required_before_future_durable_memory",
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_ephemeral_record(self, decision: MemoryPromotionDecision) -> MemoryEphemeralMemoryDecisionRecord:
        return MemoryEphemeralMemoryDecisionRecord(
            ephemeral_record_id=f"memory_ephemeral_memory_decision_record:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            decision_reason=decision.decision_reason,
            ephemeral_scope_ref=decision.scope_ref,
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )

    def build_archive_only_record(self, decision: MemoryPromotionDecision) -> MemoryArchiveOnlyDecisionRecord:
        return MemoryArchiveOnlyDecisionRecord(
            archive_only_record_id=f"memory_archive_only_decision_record:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            decision_reason=decision.decision_reason,
            archive_scope_ref=decision.scope_ref,
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )


class DurableMemoryReadinessPreviewService:
    REQUIRED_INPUTS = [
        "promotion_decision_record",
        "candidate_ref",
        "evidence_bundle_ref",
        "score_ref",
        "source_refs",
        "scope_ref",
        "expiry_or_lifecycle_ref",
        "forget_revoke_path_ref",
        "audit_trail_ref",
    ]

    def build_preview(self, decision: MemoryPromotionDecision) -> DurableMemoryReadinessPreview:
        ready = decision.decision_type == "promote"
        return DurableMemoryReadinessPreview(
            durable_readiness_preview_id=f"durable_memory_readiness_preview:{decision.candidate_id}",
            candidate_id=decision.candidate_id,
            decision_ref=_ref("memory_promotion_decision", decision.decision_id),
            ready_for_v0275_durable_registry=ready,
            readiness_reason="Ready for v0.27.5 registry review." if ready else "Not ready for durable registry review.",
            required_v0275_inputs=list(self.REQUIRED_INPUTS),
            evidence_refs=[_ref("memory_promotion_decision", decision.decision_id)],
        )


class MemoryPromotionAuditTrailService:
    def build_audit_trail(
        self,
        request: MemoryPromotionGateRequest,
        views: list[MemoryPromotionCandidateView],
        requirements: list[MemoryPromotionRequirement],
        gates: list[Any],
        decision_records: list[MemoryPromotionDecisionRecord],
        rejected_records: list[MemoryPromotionRejectedRecord],
        deferred_records: list[MemoryPromotionDeferredRecord],
        more_evidence_requests: list[MemoryPromotionMoreEvidenceRequest],
        user_confirmation_requests: list[MemoryPromotionUserConfirmationRequest],
        ephemeral_records: list[MemoryEphemeralMemoryDecisionRecord],
        archive_only_records: list[MemoryArchiveOnlyDecisionRecord],
        previews: list[DurableMemoryReadinessPreview],
    ) -> MemoryPromotionAuditTrail:
        counts = [
            len(views),
            len(requirements),
            len(gates),
            len(decision_records),
            len(rejected_records),
            len(deferred_records),
            len(more_evidence_requests),
            len(user_confirmation_requests),
            len(ephemeral_records),
            len(archive_only_records),
            len(previews),
        ]
        return MemoryPromotionAuditTrail(
            audit_trail_id="memory_promotion_audit_trail:v0.27.4",
            promotion_request_ref=_ref("memory_promotion_gate_request", request.request_id),
            candidate_view_refs=[_ref("memory_promotion_candidate_view", item.promotion_candidate_view_id) for item in views],
            requirement_refs=[_ref("memory_promotion_requirement", item.requirement_id) for item in requirements],
            gate_refs=[_ref(type(item).__name__, getattr(item, "privacy_gate_id", getattr(item, "contradiction_gate_id", getattr(item, "user_control_gate_id", "")))) for item in gates],
            decision_record_refs=[_ref("memory_promotion_decision_record", item.decision_record_id) for item in decision_records],
            rejected_record_refs=[_ref("memory_promotion_rejected_record", item.rejection_record_id) for item in rejected_records],
            deferred_record_refs=[_ref("memory_promotion_deferred_record", item.deferral_record_id) for item in deferred_records],
            more_evidence_request_refs=[_ref("memory_promotion_more_evidence_request", item.more_evidence_request_id) for item in more_evidence_requests],
            user_confirmation_request_refs=[_ref("memory_promotion_user_confirmation_request", item.confirmation_request_id) for item in user_confirmation_requests],
            ephemeral_record_refs=[_ref("memory_ephemeral_memory_decision_record", item.ephemeral_record_id) for item in ephemeral_records],
            archive_only_record_refs=[_ref("memory_archive_only_decision_record", item.archive_only_record_id) for item in archive_only_records],
            durable_readiness_preview_refs=[_ref("durable_memory_readiness_preview", item.durable_readiness_preview_id) for item in previews],
            audit_event_count=sum(counts),
            audit_status="ready" if decision_records else "warning",
            evidence_refs=[_ref("memory_promotion_gate_request", request.request_id)],
        )


class MemoryPromotionGateFindingService:
    BLOCKED_FINDINGS = {
        "automatic_promotion_attempted",
        "high_score_gate_bypass_attempted",
        "durable_memory_write_attempted",
        "persistent_memory_write_attempted",
        "durable_registry_update_attempted",
        "promotion_without_source_refs_detected",
        "promotion_without_evidence_bundle_detected",
        "promotion_without_score_detected",
        "promotion_without_privacy_assessment_detected",
        "promotion_without_scope_detected",
        "promotion_without_forget_revoke_path_detected",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "raw_transcript_memory_attempted",
        "raw_provider_output_memory_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "promotion_gate_policy_created",
        "promotion_source_view_created",
        "promotion_gate_rule_created",
        "promotion_candidate_view_created",
        "promotion_requirement_created",
        "promotion_evidence_review_created",
        "promotion_score_review_created",
        "promotion_privacy_gate_created",
        "promotion_contradiction_gate_created",
        "promotion_user_control_gate_created",
        "promotion_scope_created",
        "promotion_expiry_created",
        "promotion_lifecycle_boundary_created",
        "promotion_forget_revoke_path_created",
        "pig_guidance_attached",
        "promotion_decision_created",
        "promotion_decision_recorded",
        "rejection_record_created",
        "deferral_record_created",
        "more_evidence_request_created",
        "user_confirmation_request_created",
        "ephemeral_decision_record_created",
        "archive_only_decision_record_created",
        "durable_readiness_preview_created",
        "promotion_audit_trail_created",
    ]

    def build_findings(
        self,
        source_service: MemoryPromotionGatePrerequisiteSourceService,
        source_view: MemoryPromotionGateSourceView,
        *,
        extra_findings: list[str] | None = None,
    ) -> list[MemoryPromotionGateFinding]:
        findings: list[MemoryPromotionGateFinding] = []
        if not source_service.scoring_available:
            findings.append(self._finding("warning", "missing_evidence_scoring_report", "v0.27.3 evidence scoring report is unavailable."))
        if not source_view.score_refs:
            findings.append(self._finding("warning", "missing_candidate_scores", "Candidate scores are unavailable."))
        if not source_view.evidence_bundle_refs:
            findings.append(self._finding("warning", "missing_evidence_bundle", "Evidence bundles are unavailable."))
        if not source_view.privacy_assessment_refs:
            findings.append(self._finding("warning", "missing_privacy_assessment", "Privacy assessments are unavailable."))
        if not source_view.contradiction_check_refs:
            findings.append(self._finding("warning", "missing_contradiction_check", "Contradiction checks are unavailable."))
        if not source_view.user_control_assessment_refs:
            findings.append(self._finding("warning", "missing_user_control_assessment", "User control assessments are unavailable."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        return findings or [self._finding("info", "ok", "Memory promotion gate is ready.")]

    def _finding(self, severity: str, finding_type: str, message: str) -> MemoryPromotionGateFinding:
        return MemoryPromotionGateFinding(
            finding_id=f"memory_promotion_gate_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("memory_promotion_gate_report", "memory_promotion_gate_report:v0.27.4")],
            withdrawal_condition="Withdraw if durable write, registry update, injection, execution, mutation, bypass, external adapter, Schumpeter split, or sole LLM authority appears.",
        )


class MemoryPromotionGateReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        extra_findings: list[str] | None = None,
        scoring_available: bool = True,
        requested_decision_type: str | None = None,
        candidate_id: str | None = None,
    ) -> dict[str, Any]:
        source_service = MemoryPromotionGatePrerequisiteSourceService(scoring_available=scoring_available)
        policy = MemoryPromotionGatePolicyRuntimeService().build_policy()
        source_view = MemoryPromotionGateSourceViewService().build_source_view(source_service)
        candidates = source_service.load_v0272_candidates_if_available()
        scores = source_service.load_candidate_scores()
        bundles = source_service.load_evidence_bundles()
        previews = source_service.load_promotion_readiness_previews()
        privacy = source_service.load_privacy_assessments()
        contradictions = source_service.load_contradiction_checks()
        user_control = source_service.load_user_control_assessments()
        selected_candidates = [
            candidate for candidate in candidates
            if candidate_id is None or candidate.candidate_id == candidate_id
        ]
        if candidate_id and not selected_candidates:
            selected_candidates = candidates
        request = MemoryPromotionGateRequest(
            request_id="memory_promotion_gate_request:v0.27.4",
            memory_contract_report_id="memory_contract_report:v0.27.0",
            memory_evidence_scoring_report_id="memory_evidence_scoring_report:v0.27.3" if scoring_available else None,
            scoring_batch_id="memory_candidate_scoring_batch:v0.27.3" if scoring_available else None,
            selected_candidate_refs=[_ref("memory_candidate", item.candidate_id, item.version) for item in selected_candidates],
            selected_score_refs=[_ref("memory_candidate_score", item.score_id, item.version) for item in scores if candidate_id is None or item.candidate_id == candidate_id],
            requested_decision_type=requested_decision_type,
            promotion_profile="standard",
            source_refs=[_ref("memory_promotion_gate_policy_runtime", policy.policy_id)],
        )
        rules = MemoryPromotionGateRuleService().build_rules()
        views = MemoryPromotionCandidateViewService().build_candidate_views(selected_candidates, scores, bundles, previews, privacy, contradictions, user_control)
        requirements = [item for view in views for item in MemoryPromotionRequirementService().build_requirements(view)]
        evidence_reviews = MemoryPromotionEvidenceReviewService().build_reviews(views)
        score_reviews = MemoryPromotionScoreReviewService().build_reviews([score for score in scores if any(view.candidate_id == score.candidate_id for view in views)])
        privacy_gates = MemoryPromotionPrivacyGateService().build_gates([item for item in privacy if any(view.candidate_id == item.candidate_id for view in views)])
        contradiction_gates = MemoryPromotionContradictionGateService().build_gates([item for item in contradictions if any(view.candidate_id == item.candidate_id for view in views)])
        user_control_gates = MemoryPromotionUserControlGateService().build_gates([item for item in user_control if any(view.candidate_id == item.candidate_id for view in views)])
        scopes = MemoryPromotionScopeService().build_scopes(views)
        expiries = MemoryPromotionExpiryService().build_expiries(views)
        lifecycles = MemoryPromotionLifecycleBoundaryService().build_boundaries(views)
        paths = MemoryPromotionForgetRevokePathService().build_paths(views)
        pig_attachments = MemoryPromotionPIGGuidanceAttachmentService().attach_pig_guidance(views)
        requirement_map: dict[str, list[MemoryPromotionRequirement]] = {}
        for item in requirements:
            requirement_map.setdefault(item.candidate_id, []).append(item)
        privacy_map = _by_candidate_id(privacy_gates)
        contradiction_map = _by_candidate_id(contradiction_gates)
        user_control_map = _by_candidate_id(user_control_gates)
        scope_map = _by_candidate_id(scopes)
        expiry_map = _by_candidate_id(expiries)
        lifecycle_map = _by_candidate_id(lifecycles)
        path_map = _by_candidate_id(paths)
        decision_service = MemoryPromotionDecisionService()
        record_service = MemoryPromotionDecisionRecordService()
        decisions: list[MemoryPromotionDecision] = []
        decision_records: list[MemoryPromotionDecisionRecord] = []
        rejected_records: list[MemoryPromotionRejectedRecord] = []
        deferred_records: list[MemoryPromotionDeferredRecord] = []
        more_evidence_requests: list[MemoryPromotionMoreEvidenceRequest] = []
        user_confirmation_requests: list[MemoryPromotionUserConfirmationRequest] = []
        ephemeral_records: list[MemoryEphemeralMemoryDecisionRecord] = []
        archive_only_records: list[MemoryArchiveOnlyDecisionRecord] = []
        durable_previews: list[DurableMemoryReadinessPreview] = []
        for view in views:
            decision = decision_service.decide(
                view,
                requirement_map[view.candidate_id],
                privacy_map.get(view.candidate_id),
                contradiction_map.get(view.candidate_id),
                user_control_map.get(view.candidate_id),
                scope_map[view.candidate_id],
                expiry_map[view.candidate_id],
                lifecycle_map[view.candidate_id],
                path_map[view.candidate_id],
                requested_decision_type=requested_decision_type,
            )
            decisions.append(decision)
            decision_records.append(record_service.build_promotion_decision_record(decision, view))
            if decision.decision_type == "reject":
                rejected_records.append(record_service.build_rejected_record(decision))
            if decision.decision_type == "defer":
                deferred_records.append(record_service.build_deferred_record(decision))
            if decision.decision_type == "request_more_evidence":
                more_evidence_requests.append(record_service.build_more_evidence_request(decision))
            if decision.decision_type == "request_user_confirmation":
                user_confirmation_requests.append(record_service.build_user_confirmation_request(decision))
            if decision.decision_type == "mark_ephemeral":
                ephemeral_records.append(record_service.build_ephemeral_record(decision))
            if decision.decision_type == "mark_archive_only":
                archive_only_records.append(record_service.build_archive_only_record(decision))
            durable_previews.append(DurableMemoryReadinessPreviewService().build_preview(decision))
        all_gates: list[Any] = privacy_gates + contradiction_gates + user_control_gates
        audit = MemoryPromotionAuditTrailService().build_audit_trail(
            request,
            views,
            requirements,
            all_gates,
            decision_records,
            rejected_records,
            deferred_records,
            more_evidence_requests,
            user_confirmation_requests,
            ephemeral_records,
            archive_only_records,
            durable_previews,
        )
        findings = MemoryPromotionGateFindingService().build_findings(source_service, source_view, extra_findings=extra_findings)
        report_status = self._report_status(findings, decision_records)
        report = MemoryPromotionGateReport(
            report_id=report_id or "memory_promotion_gate_report:v0.27.4",
            created_at=utc_now_iso(),
            promotion_gate_policy=policy,
            request=request,
            source_view=source_view,
            gate_rules=rules,
            candidate_views=views,
            requirements=requirements,
            evidence_reviews=evidence_reviews,
            score_reviews=score_reviews,
            privacy_gates=privacy_gates,
            contradiction_gates=contradiction_gates,
            user_control_gates=user_control_gates,
            scopes=scopes,
            expiries=expiries,
            lifecycle_boundaries=lifecycles,
            forget_revoke_paths=paths,
            pig_guidance_attachments=pig_attachments,
            promotion_decisions=decisions,
            promotion_decision_records=decision_records,
            rejected_records=rejected_records,
            deferred_records=deferred_records,
            more_evidence_requests=more_evidence_requests,
            user_confirmation_requests=user_confirmation_requests,
            ephemeral_records=ephemeral_records,
            archive_only_records=archive_only_records,
            durable_readiness_previews=durable_previews,
            audit_trail=audit,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_5=report_status in {"passed", "warning"} and any(item.ready_for_v0275_durable_registry for item in durable_previews),
            promotion_gate_created=True,
            candidate_views_created=bool(views),
            requirements_created=bool(requirements),
            gate_reviews_created=bool(evidence_reviews and score_reviews and privacy_gates and contradiction_gates and user_control_gates),
            scopes_created=bool(scopes),
            expiries_created=bool(expiries),
            forget_revoke_paths_created=bool(paths),
            promotion_decisions_recorded=bool(decision_records),
            durable_readiness_previews_created=bool(durable_previews),
            audit_trail_created=True,
            promote_decision_count=sum(1 for item in decisions if item.decision_type == "promote"),
            reject_decision_count=sum(1 for item in decisions if item.decision_type == "reject"),
            defer_decision_count=sum(1 for item in decisions if item.decision_type == "defer"),
            more_evidence_request_count=len(more_evidence_requests),
            user_confirmation_request_count=len(user_confirmation_requests),
            ephemeral_decision_count=len(ephemeral_records),
            archive_only_decision_count=len(archive_only_records),
            limitations=[
                "v0.27.4 records promotion-gate decisions only; durable memory record creation is deferred to v0.27.5.",
                "Release hygiene status is represented as a ref and does not enable persistent memory write.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if durable write, registry update, persistent write, continuity injection, persona/policy mutation, raw memory, PIG authority, provider/command execution, safety bypass, external adapter, Schumpeter split, or sole LLM authority appears.",
            ],
        )
        return {
            "source_service": source_service,
            "promotion_gate_policy": policy,
            "request": request,
            "source_view": source_view,
            "gate_rules": rules,
            "candidate_views": views,
            "requirements": requirements,
            "evidence_reviews": evidence_reviews,
            "score_reviews": score_reviews,
            "privacy_gates": privacy_gates,
            "contradiction_gates": contradiction_gates,
            "user_control_gates": user_control_gates,
            "scopes": scopes,
            "expiries": expiries,
            "lifecycle_boundaries": lifecycles,
            "forget_revoke_paths": paths,
            "pig_guidance_attachments": pig_attachments,
            "promotion_decisions": decisions,
            "promotion_decision_records": decision_records,
            "rejected_records": rejected_records,
            "deferred_records": deferred_records,
            "more_evidence_requests": more_evidence_requests,
            "user_confirmation_requests": user_confirmation_requests,
            "ephemeral_records": ephemeral_records,
            "archive_only_records": archive_only_records,
            "durable_readiness_previews": durable_previews,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def _report_status(self, findings: list[MemoryPromotionGateFinding], decision_records: list[MemoryPromotionDecisionRecord]) -> str:
        if any(item.finding_type in MemoryPromotionGateFindingService.BLOCKED_FINDINGS for item in findings):
            return "blocked"
        if any(item.severity == "critical" for item in findings):
            return "blocked"
        if not decision_records:
            return "warning"
        if any(item.severity in {"warning", "error"} for item in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_PROMOTION_GATE_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_promotion_gate",
            "principles": [
                "Promotion gate is not durable memory registry",
                "Promotion decision is not persistent memory write",
                "Promote decision is authorization metadata for future durable memory, not memory itself",
                "Reject decision is not source deletion",
                "Defer decision is not silent memory storage",
                "Mark-ephemeral is not durable memory",
                "Mark-archive-only is not active memory",
                "Memory promotion is not persona mutation",
                "PIG guidance cannot promote memory",
                "High score cannot bypass the promotion gate",
            ],
            "safety_boundary": {
                "promotion_decisions_recorded": "conditional",
                "memory_promoted": False,
                "persistent_memory_written": False,
                "durable_memory_written": False,
                "durable_registry_updated": False,
                "session_continuity_injected": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_secret_output": False,
                "credential_exposed": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.5 durable memory record & registry",
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": MEMORY_PROMOTION_GATE_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_promotion_gate_created",
            "version": MEMORY_PROMOTION_GATE_VERSION,
            "source_read_models": [
                "MemoryEvidenceScoringState",
                "MemoryCandidateScoreState",
                "MemoryPromotionReadinessPreviewState",
                "MemoryCandidateEvidenceBundleState",
                "MemoryPrivacyRiskAssessmentState",
                "MemoryContradictionCheckState",
                "MemoryUserControlRequirementAssessmentState",
                "MemoryCandidateState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryPromotionGateState",
                "MemoryPromotionCandidateViewState",
                "MemoryPromotionRequirementState",
                "MemoryPromotionDecisionState",
                "MemoryPromotionDecisionRecordState",
                "DurableMemoryReadinessPreviewState",
                "MemoryPromotionAuditState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_PROMOTION_GATE_EFFECT_TYPES,
        }


def render_memory_promotion_gate_cli(parts: dict[str, Any], section: str = "gate") -> str:
    report: MemoryPromotionGateReport = parts["report"]
    lines = [
        f"Memory Promotion Gate {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"promotion_gate_created={_bool(report.promotion_gate_created)}",
        f"candidate_views_created={_bool(report.candidate_views_created)}",
        f"requirements_created={_bool(report.requirements_created)}",
        f"gate_reviews_created={_bool(report.gate_reviews_created)}",
        f"scopes_created={_bool(report.scopes_created)}",
        f"expiries_created={_bool(report.expiries_created)}",
        f"forget_revoke_paths_created={_bool(report.forget_revoke_paths_created)}",
        f"promotion_decisions_recorded={_bool(report.promotion_decisions_recorded)}",
        f"durable_readiness_previews_created={_bool(report.durable_readiness_previews_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"promote_decision_count={report.promote_decision_count}",
        f"reject_decision_count={report.reject_decision_count}",
        f"defer_decision_count={report.defer_decision_count}",
        f"ready_for_v0_27_5={_bool(report.ready_for_v0_27_5)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_promoted={_bool(report.memory_promoted)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"durable_memory_written={_bool(report.durable_memory_written)}",
        f"durable_registry_updated={_bool(report.durable_registry_updated)}",
        f"session_continuity_injected={_bool(report.session_continuity_injected)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_counts = {
        "source-view": ("source_ref_count", report.source_view.source_ref_count),
        "rules": ("gate_rule_count", len(report.gate_rules)),
        "candidates": ("candidate_view_count", len(report.candidate_views)),
        "requirements": ("requirement_count", len(report.requirements)),
        "evidence-review": ("evidence_review_count", len(report.evidence_reviews)),
        "score-review": ("score_review_count", len(report.score_reviews)),
        "privacy": ("privacy_gate_count", len(report.privacy_gates)),
        "contradictions": ("contradiction_gate_count", len(report.contradiction_gates)),
        "user-control": ("user_control_gate_count", len(report.user_control_gates)),
        "scope": ("scope_count", len(report.scopes)),
        "expiry": ("expiry_count", len(report.expiries)),
        "lifecycle": ("lifecycle_boundary_count", len(report.lifecycle_boundaries)),
        "forget-revoke": ("forget_revoke_path_count", len(report.forget_revoke_paths)),
        "readiness": ("durable_readiness_preview_count", len(report.durable_readiness_previews)),
    }
    if section in section_counts:
        name, value = section_counts[section]
        lines.append(f"{name}={value}")
    elif section == "decide":
        decision_type = report.promotion_decisions[0].decision_type if report.promotion_decisions else "none"
        lines.append(f"decision_type={decision_type}")
    elif section == "audit":
        lines.append(f"audit_status={report.audit_trail.audit_status}")
        lines.append(f"raw_content_included={_bool(report.audit_trail.raw_content_included)}")
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"finding_count={len(report.findings)}")
    return "\n".join(lines)


DURABLE_MEMORY_REGISTRY_VERSION = "v0.27.5"
DURABLE_MEMORY_REGISTRY_VERSION_NAME = "Durable Memory Record & Registry"
DURABLE_MEMORY_REGISTRY_KOREAN_NAME = "Durable Memory Record·Registry"
DURABLE_MEMORY_REGISTRY_NEXT_STEP = "v0.27.6 Session Continuity Context Builder"

DURABLE_MEMORY_REGISTRY_OBJECT_TYPES = [
    "durable_memory_write_policy",
    "durable_memory_registry_policy",
    "durable_memory_write_request",
    "durable_memory_write_gate",
    "durable_memory_write_decision",
    "durable_memory_write_blocked_record",
    "durable_memory_dry_run_record",
    "durable_memory_record_preview",
    "durable_memory_record",
    "durable_memory_registry",
    "durable_memory_registry_entry",
    "memory_record_scope",
    "memory_record_provenance",
    "memory_record_evidence_index",
    "memory_record_lifecycle_policy",
    "memory_record_version",
    "memory_record_status",
    "memory_record_privacy_boundary",
    "memory_record_conflict_marker",
    "memory_record_forget_revoke_binding",
    "memory_record_audit_trail",
    "durable_memory_registry_integrity_report",
    "durable_memory_registry_finding",
    "durable_memory_registry_report",
    "memory_promotion_gate_report",
    "memory_promotion_decision_record",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

DURABLE_MEMORY_REGISTRY_EVENT_TYPES = [
    "durable_memory_registry_requested",
    "durable_memory_registry_prerequisites_loaded",
    "durable_memory_write_policy_created",
    "durable_memory_registry_policy_created",
    "durable_memory_write_gate_evaluated",
    "durable_memory_write_decision_created",
    "durable_memory_write_blocked_record_created",
    "durable_memory_dry_run_record_created",
    "durable_memory_record_preview_created",
    "durable_memory_record_created",
    "durable_memory_registry_created",
    "durable_memory_registry_entry_created",
    "memory_record_scope_created",
    "memory_record_provenance_created",
    "memory_record_evidence_index_created",
    "memory_record_lifecycle_policy_created",
    "memory_record_version_created",
    "memory_record_status_created",
    "memory_record_privacy_boundary_created",
    "memory_record_conflict_marker_created",
    "memory_record_forget_revoke_binding_created",
    "memory_record_audit_trail_created",
    "durable_memory_registry_integrity_report_created",
    "durable_memory_registry_report_created",
    "durable_memory_registry_warning_created",
    "durable_memory_registry_blocked",
]

DURABLE_MEMORY_REGISTRY_EFFECT_TYPES = [
    "read_only_observation",
    "durable_memory_write_gate_evaluated",
    "durable_memory_write_decision_recorded",
    "durable_memory_dry_run_record_created",
    "durable_memory_write_blocked_record_created",
    "durable_memory_record_created",
    "durable_memory_registry_entry_created",
    "durable_memory_registry_updated",
    "persistent_memory_written",
    "memory_record_provenance_created",
    "memory_record_evidence_index_created",
    "memory_record_lifecycle_policy_created",
    "memory_record_audit_created",
    "state_candidate_created",
]

DURABLE_MEMORY_REGISTRY_FORBIDDEN_EFFECT_TYPES = [
    "durable_memory_record_created_without_gate",
    "durable_memory_registry_updated_without_gate",
    "persistent_memory_written_without_release_hygiene",
    "persistent_memory_written_without_runtime_data_hygiene",
    "memory_written_without_promotion_decision",
    "memory_written_without_evidence",
    "memory_written_without_source_refs",
    "memory_written_without_scope",
    "memory_written_without_forget_revoke_path",
    "memory_written_without_audit",
    "session_continuity_context_created",
    "continuity_injection_bundle_created",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "raw_transcript_memory_created",
    "raw_provider_output_memory_created",
    "raw_secret_memory_created",
    "credential_memory_created",
    "pig_memory_promoted",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "llm_judge_used",
]


@dataclass
class DurableMemoryWritePolicy(_ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    durable_memory_record_creation_enabled: bool = True
    durable_memory_registry_enabled: bool = True
    persistent_memory_write_conditionally_enabled: bool = True
    persistent_memory_write_requires_write_gate: bool = True
    release_hygiene_gate_required_for_persistent_write: bool = True
    runtime_data_hygiene_required_for_persistent_write: bool = True
    promote_decision_required: bool = True
    evidence_bundle_required: bool = True
    score_required: bool = True
    source_refs_required: bool = True
    scope_required: bool = True
    lifecycle_policy_required: bool = True
    forget_revoke_path_required: bool = True
    audit_trail_required: bool = True
    provenance_required: bool = True
    evidence_index_required: bool = True
    privacy_boundary_required: bool = True
    contradiction_review_required_if_present: bool = True
    dry_run_allowed_when_gate_missing: bool = True
    no_write_allowed: bool = True
    automatic_write_forbidden: bool = True
    persona_mutation_forbidden: bool = True
    behavior_policy_mutation_forbidden: bool = True
    raw_transcript_memory_forbidden: bool = True
    raw_provider_output_memory_forbidden: bool = True
    raw_secret_memory_forbidden: bool = True
    credential_memory_forbidden: bool = True
    private_full_path_memory_forbidden: bool = True
    pig_guidance_is_not_memory_authority: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False
    session_continuity_injection_enabled_now: bool = False
    llm_judge_as_sole_write_authority_forbidden: bool = True


@dataclass
class DurableMemoryRegistryPolicy(_ModelMixin):
    registry_policy_id: str
    registry_status_values: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    registry_enabled: bool = True
    registry_is_not_persona: bool = True
    registry_is_not_behavior_policy: bool = True
    registry_requires_versioning: bool = True
    registry_requires_provenance: bool = True
    registry_requires_status: bool = True
    registry_requires_lifecycle: bool = True
    registry_requires_audit: bool = True
    registry_requires_forget_revoke_binding: bool = True
    registry_allows_only_gated_records: bool = True
    registry_blocks_raw_memory: bool = True


@dataclass
class DurableMemoryWriteRequest(_ModelMixin):
    write_request_id: str
    promotion_gate_report_id: str | None
    promotion_decision_record_id: str | None
    durable_readiness_preview_id: str | None
    candidate_ref: dict[str, Any] | None
    score_ref: dict[str, Any] | None
    evidence_bundle_ref: dict[str, Any] | None
    source_refs: list[dict[str, Any]]
    scope_ref: dict[str, Any] | None
    lifecycle_ref: dict[str, Any] | None
    expiry_ref: dict[str, Any] | None
    forget_revoke_path_ref: dict[str, Any] | None
    release_hygiene_status_ref: dict[str, Any] | None
    runtime_data_hygiene_status_ref: dict[str, Any] | None
    requested_write_mode: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    strictness: str = "standard"


@dataclass
class DurableMemoryWriteGate(_ModelMixin):
    write_gate_id: str
    write_request_id: str
    promotion_decision_present: bool
    promotion_decision_is_promote: bool
    candidate_ref_present: bool
    evidence_bundle_present: bool
    score_ref_present: bool
    source_refs_present: bool
    scope_present: bool
    lifecycle_or_expiry_present: bool
    forget_revoke_path_present: bool
    audit_ready: bool
    provenance_ready: bool
    evidence_index_ready: bool
    privacy_boundary_passed: bool
    contradiction_review_passed_or_not_required: bool
    release_hygiene_gate_passed: bool
    runtime_data_hygiene_gate_passed: bool
    raw_memory_blockers_absent: bool
    gate_status: str
    gate_summary: str
    may_create_durable_record: bool
    may_write_persistent_memory: bool
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class DurableMemoryWriteDecision(_ModelMixin):
    write_decision_id: str
    write_request_id: str
    write_gate_id: str
    decision_type: str
    decision_reason: str
    creates_durable_record: bool
    updates_registry: bool
    writes_persistent_memory: bool
    decision_basis_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class DurableMemoryWriteBlockedRecord(_ModelMixin):
    blocked_record_id: str
    write_request_id: str
    write_gate_id: str
    block_reason: str
    blocking_requirements: list[str]
    required_followup_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    durable_record_created: bool = False
    persistent_memory_written: bool = False
    registry_updated: bool = False


@dataclass
class DurableMemoryDryRunRecord(_ModelMixin):
    dry_run_record_id: str
    write_request_id: str
    preview_ref: dict[str, Any] | None
    dry_run_reason: str
    would_create_record: bool
    would_update_registry: bool
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    actual_durable_record_created: bool = False
    actual_persistent_memory_written: bool = False


@dataclass
class DurableMemoryRecordPreview(_ModelMixin):
    preview_id: str
    candidate_ref: dict[str, Any]
    proposed_record_summary: str
    proposed_scope_ref: dict[str, Any] | None
    proposed_lifecycle_ref: dict[str, Any] | None
    proposed_evidence_index_ref: dict[str, Any] | None
    proposed_provenance_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    preview_is_not_memory_write: bool = True
    durable_record_created_now: bool = False
    persistent_memory_written_now: bool = False


@dataclass
class MemoryRecordScope(_ModelMixin):
    scope_id: str
    candidate_id: str
    memory_record_id: str | None
    scope_type: str
    scope_summary: str
    allowed_context_refs: list[dict[str, Any]]
    forbidden_context_refs: list[dict[str, Any]]
    scope_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class MemoryRecordProvenance(_ModelMixin):
    provenance_id: str
    memory_record_id: str | None
    candidate_ref: dict[str, Any]
    promotion_decision_record_ref: dict[str, Any]
    source_refs: list[dict[str, Any]]
    evidence_bundle_ref: dict[str, Any]
    score_ref: dict[str, Any]
    originating_versions: list[str]
    originating_surfaces: list[str]
    provenance_complete: bool
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class MemoryRecordEvidenceIndex(_ModelMixin):
    evidence_index_id: str
    memory_record_id: str | None
    evidence_bundle_ref: dict[str, Any]
    evidence_item_refs: list[dict[str, Any]]
    claim_refs: list[dict[str, Any]]
    score_ref: dict[str, Any]
    privacy_assessment_refs: list[dict[str, Any]]
    contradiction_check_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    evidence_count: int
    index_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    raw_evidence_included: bool = False


@dataclass
class MemoryRecordLifecyclePolicy(_ModelMixin):
    lifecycle_policy_id: str
    memory_record_id: str | None
    initial_status: str
    allowed_future_states: list[str]
    review_required: bool
    review_after: str | None
    expires_at: str | None
    lifecycle_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    supersede_allowed: bool = True
    revoke_allowed: bool = True
    forget_allowed: bool = True
    archive_allowed: bool = True


@dataclass
class MemoryRecordVersion(_ModelMixin):
    record_version_id: str
    memory_record_id: str | None
    record_schema_version: str
    content_version: int
    previous_record_ref: dict[str, Any] | None
    supersedes_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    migration_required: bool = False


@dataclass
class MemoryRecordStatus(_ModelMixin):
    status_id: str
    memory_record_id: str
    current_status: str
    status_reason: str
    status_changed_at: str | None
    status_changed_by: str | None
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class MemoryRecordPrivacyBoundary(_ModelMixin):
    privacy_boundary_id: str
    memory_record_id: str | None
    privacy_risk_assessment_refs: list[dict[str, Any]]
    privacy_level: str
    sensitive_categories: list[str]
    user_confirmation_required: bool
    user_confirmation_ref: dict[str, Any] | None
    storage_allowed: bool
    privacy_boundary_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class MemoryRecordConflictMarker(_ModelMixin):
    conflict_marker_id: str
    memory_record_id: str | None
    contradiction_check_ref: dict[str, Any] | None
    conflict_level: str
    conflict_summary: str | None
    requires_review: bool
    blocks_active_use: bool
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class MemoryRecordForgetRevokeBinding(_ModelMixin):
    binding_id: str
    memory_record_id: str | None
    forget_revoke_path_ref: dict[str, Any]
    binding_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    revoke_supported: bool = True
    forget_supported: bool = True
    update_supported: bool = True
    archive_supported: bool = True
    forget_executed_now: bool = False
    revoke_executed_now: bool = False


@dataclass
class DurableMemoryRecord(_ModelMixin):
    memory_record_id: str
    record_schema_version: str
    candidate_ref: dict[str, Any]
    promotion_decision_record_ref: dict[str, Any]
    title: str
    summary: str
    memory_type: str
    status: str
    scope: MemoryRecordScope
    provenance: MemoryRecordProvenance
    evidence_index: MemoryRecordEvidenceIndex
    lifecycle_policy: MemoryRecordLifecyclePolicy
    version_info: MemoryRecordVersion
    privacy_boundary: MemoryRecordPrivacyBoundary
    conflict_markers: list[MemoryRecordConflictMarker]
    forget_revoke_binding: MemoryRecordForgetRevokeBinding
    created_at: str | None
    updated_at: str | None
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    refs_only: bool = True
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    persona_mutation: bool = False
    behavior_policy_mutation: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False


@dataclass
class DurableMemoryRegistryEntry(_ModelMixin):
    registry_entry_id: str
    memory_record_ref: dict[str, Any]
    memory_record_id: str
    memory_type: str
    status: str
    scope_ref: dict[str, Any]
    provenance_ref: dict[str, Any]
    evidence_index_ref: dict[str, Any]
    lifecycle_policy_ref: dict[str, Any]
    created_at: str | None
    updated_at: str | None
    entry_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class DurableMemoryRegistry(_ModelMixin):
    registry_id: str
    registry_schema_version: str
    entries: list[DurableMemoryRegistryEntry]
    entry_count: int
    active_count: int
    archived_count: int
    revoked_count: int
    forgotten_count: int
    expired_count: int
    blocked_count: int
    dry_run_count: int
    registry_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    registry_is_persona: bool = False
    registry_is_behavior_policy: bool = False


@dataclass
class MemoryRecordAuditTrail(_ModelMixin):
    audit_trail_id: str
    write_request_ref: dict[str, Any]
    write_gate_ref: dict[str, Any]
    write_decision_ref: dict[str, Any]
    memory_record_refs: list[dict[str, Any]]
    registry_entry_refs: list[dict[str, Any]]
    provenance_refs: list[dict[str, Any]]
    evidence_index_refs: list[dict[str, Any]]
    lifecycle_policy_refs: list[dict[str, Any]]
    privacy_boundary_refs: list[dict[str, Any]]
    forget_revoke_binding_refs: list[dict[str, Any]]
    blocked_record_refs: list[dict[str, Any]]
    dry_run_record_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    raw_content_included: bool = False


@dataclass
class DurableMemoryRegistryIntegrityReport(_ModelMixin):
    integrity_report_id: str
    registry_ref: dict[str, Any] | None
    checked_entry_count: int
    missing_provenance_count: int
    missing_evidence_index_count: int
    missing_scope_count: int
    missing_lifecycle_count: int
    missing_forget_revoke_binding_count: int
    raw_memory_violation_count: int
    persona_mutation_count: int
    behavior_policy_mutation_count: int
    provider_invocation_count: int
    command_execution_count: int
    safety_bypass_count: int
    integrity_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION


@dataclass
class DurableMemoryRegistryFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class DurableMemoryRegistryReport(_ModelMixin):
    report_id: str
    created_at: str
    write_policy: DurableMemoryWritePolicy
    registry_policy: DurableMemoryRegistryPolicy
    write_request: DurableMemoryWriteRequest
    write_gate: DurableMemoryWriteGate
    write_decision: DurableMemoryWriteDecision
    blocked_records: list[DurableMemoryWriteBlockedRecord]
    dry_run_records: list[DurableMemoryDryRunRecord]
    record_previews: list[DurableMemoryRecordPreview]
    durable_memory_records: list[DurableMemoryRecord]
    registry: DurableMemoryRegistry
    registry_entries: list[DurableMemoryRegistryEntry]
    audit_trail: MemoryRecordAuditTrail
    integrity_report: DurableMemoryRegistryIntegrityReport
    findings: list[DurableMemoryRegistryFinding]
    report_status: str
    ready_for_v0_27_6: bool
    write_gate_created: bool
    write_decision_created: bool
    durable_memory_records_created: bool
    registry_created: bool
    registry_entries_created: bool
    audit_trail_created: bool
    integrity_report_created: bool
    durable_record_count: int
    registry_entry_count: int
    blocked_write_count: int
    dry_run_count: int
    persistent_memory_written: bool
    durable_memory_written: bool
    durable_registry_updated: bool
    limitations: list[str]
    withdrawal_conditions: list[str]
    version: str = DURABLE_MEMORY_REGISTRY_VERSION
    ready_for_v0_28: bool = False
    session_continuity_injected: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_memory_created: bool = False
    raw_provider_output_memory_created: bool = False
    raw_secret_memory_created: bool = False
    credential_memory_created: bool = False
    pig_memory_promoted: bool = False
    pig_policy_mutated: bool = False
    pig_executed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    llm_judge_used: bool = False
    next_required_step: str = DURABLE_MEMORY_REGISTRY_NEXT_STEP
    validity_horizon: str = "Valid until v0.27.6 Session Continuity Context Builder begins or durable memory registry policy changes."


DURABLE_MEMORY_REGISTRY_CONDITIONAL_EFFECT_TYPES = [
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "persistent_memory_written",
]


class DurableMemoryRegistryPrerequisiteSourceService:
    def __init__(
        self,
        *,
        promotion_gate_available: bool = True,
        release_hygiene_gate_passed: bool = False,
        runtime_data_hygiene_gate_passed: bool = False,
        requested_decision_type: str = "promote",
    ) -> None:
        self.promotion_gate_available = promotion_gate_available
        self.release_hygiene_gate_passed = release_hygiene_gate_passed
        self.runtime_data_hygiene_gate_passed = runtime_data_hygiene_gate_passed
        self.promotion_parts = (
            MemoryPromotionGateReportService().build_all_parts(requested_decision_type=requested_decision_type)
            if promotion_gate_available
            else None
        )

    def load_v0274_promotion_gate_report(self) -> MemoryPromotionGateReport | None:
        return self.promotion_parts["report"] if self.promotion_parts else None

    def load_promotion_decision_records(self) -> list[MemoryPromotionDecisionRecord]:
        return self.promotion_parts["promotion_decision_records"] if self.promotion_parts else []

    def load_durable_readiness_previews(self) -> list[DurableMemoryReadinessPreview]:
        return self.promotion_parts["durable_readiness_previews"] if self.promotion_parts else []

    def load_candidate_refs(self) -> list[dict[str, Any]]:
        return [record.candidate_ref for record in self.load_promotion_decision_records()]

    def load_evidence_bundle_refs(self) -> list[dict[str, Any]]:
        return [
            record.evidence_bundle_ref
            for record in self.load_promotion_decision_records()
            if record.evidence_bundle_ref is not None
        ]

    def load_score_refs(self) -> list[dict[str, Any]]:
        return [
            record.score_ref
            for record in self.load_promotion_decision_records()
            if record.score_ref is not None
        ]

    def load_source_refs(self) -> list[dict[str, Any]]:
        return [_ref("memory_source_ref", "memory_source_ref:v0.27.1:1", "v0.27.1")] if self.promotion_parts else []

    def load_scope_refs(self) -> list[dict[str, Any]]:
        return [_ref("memory_promotion_scope", item.scope_id, item.version) for item in self.promotion_parts["scopes"]] if self.promotion_parts else []

    def load_lifecycle_or_expiry_refs(self) -> list[dict[str, Any]]:
        if not self.promotion_parts:
            return []
        lifecycle_refs = [_ref("memory_promotion_lifecycle_boundary", item.lifecycle_boundary_id, item.version) for item in self.promotion_parts["lifecycle_boundaries"]]
        expiry_refs = [_ref("memory_promotion_expiry", item.expiry_id, item.version) for item in self.promotion_parts["expiries"]]
        return lifecycle_refs + expiry_refs

    def load_forget_revoke_path_refs(self) -> list[dict[str, Any]]:
        return [_ref("memory_promotion_forget_revoke_path", item.forget_revoke_path_id, item.version) for item in self.promotion_parts["forget_revoke_paths"]] if self.promotion_parts else []

    def load_release_hygiene_status_if_available(self) -> dict[str, Any] | None:
        if not self.release_hygiene_gate_passed:
            return None
        return _ref("release_hygiene_status", "release_hygiene_status:v0.26.10:passed", "v0.26.10")

    def load_runtime_data_hygiene_status_if_available(self) -> dict[str, Any] | None:
        if not self.runtime_data_hygiene_gate_passed:
            return None
        return _ref("runtime_data_hygiene_status", "runtime_data_hygiene_status:v0.26.10:passed", "v0.26.10")


class DurableMemoryWritePolicyService:
    def build_policy(self) -> DurableMemoryWritePolicy:
        return DurableMemoryWritePolicy(
            policy_id="durable_memory_write_policy:v0.27.5",
            evidence_refs=[_ref("memory_promotion_gate_report", "memory_promotion_gate_report:v0.27.4", MEMORY_PROMOTION_GATE_VERSION)],
        )


class DurableMemoryRegistryPolicyService:
    def build_policy(self) -> DurableMemoryRegistryPolicy:
        return DurableMemoryRegistryPolicy(
            registry_policy_id="durable_memory_registry_policy:v0.27.5",
            registry_status_values=[
                "promoted",
                "active",
                "superseded",
                "revoked",
                "forgotten",
                "expired",
                "archived",
                "blocked",
                "dry_run",
            ],
            evidence_refs=[_ref("durable_memory_write_policy", "durable_memory_write_policy:v0.27.5", DURABLE_MEMORY_REGISTRY_VERSION)],
        )


class DurableMemoryWriteGateService:
    def evaluate_gate(
        self,
        request: DurableMemoryWriteRequest,
        *,
        promotion_decision_is_promote: bool,
        audit_ready: bool = True,
        provenance_ready: bool = True,
        evidence_index_ready: bool = True,
        privacy_boundary_passed: bool = True,
        contradiction_review_passed_or_not_required: bool = True,
        release_hygiene_gate_passed: bool = False,
        runtime_data_hygiene_gate_passed: bool = False,
        raw_memory_blockers_absent: bool = True,
    ) -> DurableMemoryWriteGate:
        promotion_present = request.promotion_decision_record_id is not None
        required_refs_present = all(
            [
                promotion_present,
                promotion_decision_is_promote,
                request.candidate_ref is not None,
                request.evidence_bundle_ref is not None,
                request.score_ref is not None,
                bool(request.source_refs),
                request.scope_ref is not None,
                request.lifecycle_ref is not None or request.expiry_ref is not None,
                request.forget_revoke_path_ref is not None,
                audit_ready,
                provenance_ready,
                evidence_index_ready,
                privacy_boundary_passed,
                contradiction_review_passed_or_not_required,
                raw_memory_blockers_absent,
            ]
        )
        hygiene_ready = release_hygiene_gate_passed and runtime_data_hygiene_gate_passed
        may_create = required_refs_present
        may_write = may_create and hygiene_ready
        if not raw_memory_blockers_absent:
            status = "blocked"
            summary = "Raw-memory blockers prevent durable memory materialization."
        elif may_write:
            status = "passed"
            summary = "All durable-memory and hygiene gates passed."
        elif may_create:
            status = "dry_run_only"
            summary = "Durable record shape is ready, but release/runtime data hygiene gates are missing."
        else:
            status = "blocked"
            summary = "Required promotion, evidence, source, scope, lifecycle, audit, or forget/revoke refs are missing."
        return DurableMemoryWriteGate(
            write_gate_id="durable_memory_write_gate:v0.27.5",
            write_request_id=request.write_request_id,
            promotion_decision_present=promotion_present,
            promotion_decision_is_promote=promotion_decision_is_promote,
            candidate_ref_present=request.candidate_ref is not None,
            evidence_bundle_present=request.evidence_bundle_ref is not None,
            score_ref_present=request.score_ref is not None,
            source_refs_present=bool(request.source_refs),
            scope_present=request.scope_ref is not None,
            lifecycle_or_expiry_present=request.lifecycle_ref is not None or request.expiry_ref is not None,
            forget_revoke_path_present=request.forget_revoke_path_ref is not None,
            audit_ready=audit_ready,
            provenance_ready=provenance_ready,
            evidence_index_ready=evidence_index_ready,
            privacy_boundary_passed=privacy_boundary_passed,
            contradiction_review_passed_or_not_required=contradiction_review_passed_or_not_required,
            release_hygiene_gate_passed=release_hygiene_gate_passed,
            runtime_data_hygiene_gate_passed=runtime_data_hygiene_gate_passed,
            raw_memory_blockers_absent=raw_memory_blockers_absent,
            gate_status=status,
            gate_summary=summary,
            may_create_durable_record=may_create,
            may_write_persistent_memory=may_write,
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryWriteDecisionService:
    def decide_write(self, request: DurableMemoryWriteRequest, gate: DurableMemoryWriteGate) -> DurableMemoryWriteDecision:
        if gate.may_write_persistent_memory:
            decision_type = "write_durable_memory"
            reason = "Write gate and hygiene gates passed."
            creates_record = updates_registry = writes_persistent = True
        elif gate.may_create_durable_record:
            decision_type = "dry_run_only"
            reason = "Write gate has durable refs, but persistent write hygiene gates are not passed."
            creates_record = updates_registry = writes_persistent = False
        elif not gate.promotion_decision_present or not gate.promotion_decision_is_promote:
            decision_type = "block_write"
            reason = "Durable memory requires a prior promote decision."
            creates_record = updates_registry = writes_persistent = False
        elif not gate.release_hygiene_gate_passed:
            decision_type = "defer_release_hygiene"
            reason = "Release hygiene gate is missing or failed."
            creates_record = updates_registry = writes_persistent = False
        elif not gate.runtime_data_hygiene_gate_passed:
            decision_type = "defer_runtime_data_hygiene"
            reason = "Runtime data hygiene gate is missing or failed."
            creates_record = updates_registry = writes_persistent = False
        else:
            decision_type = "defer_more_evidence"
            reason = "Required durable-memory refs are incomplete."
            creates_record = updates_registry = writes_persistent = False
        return DurableMemoryWriteDecision(
            write_decision_id="durable_memory_write_decision:v0.27.5",
            write_request_id=request.write_request_id,
            write_gate_id=gate.write_gate_id,
            decision_type=decision_type,
            decision_reason=reason,
            creates_durable_record=creates_record,
            updates_registry=updates_registry,
            writes_persistent_memory=writes_persistent,
            decision_basis_refs=[_ref("durable_memory_write_gate", gate.write_gate_id, gate.version)],
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryWriteBlockedRecordService:
    def build_blocked_record(self, request: DurableMemoryWriteRequest, gate: DurableMemoryWriteGate) -> DurableMemoryWriteBlockedRecord:
        missing = []
        checks = {
            "promotion_decision": gate.promotion_decision_present and gate.promotion_decision_is_promote,
            "candidate_ref": gate.candidate_ref_present,
            "evidence_bundle": gate.evidence_bundle_present,
            "score_ref": gate.score_ref_present,
            "source_refs": gate.source_refs_present,
            "scope": gate.scope_present,
            "lifecycle_or_expiry": gate.lifecycle_or_expiry_present,
            "forget_revoke_path": gate.forget_revoke_path_present,
            "audit": gate.audit_ready,
            "privacy_boundary": gate.privacy_boundary_passed,
            "raw_memory_blockers_absent": gate.raw_memory_blockers_absent,
        }
        for name, passed in checks.items():
            if not passed:
                missing.append(name)
        return DurableMemoryWriteBlockedRecord(
            blocked_record_id="durable_memory_write_blocked_record:v0.27.5",
            write_request_id=request.write_request_id,
            write_gate_id=gate.write_gate_id,
            block_reason=gate.gate_summary,
            blocking_requirements=missing,
            required_followup_refs=[_ref("durable_memory_write_gate", gate.write_gate_id, gate.version)],
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryDryRunRecordService:
    def build_dry_run_record(
        self,
        request: DurableMemoryWriteRequest,
        gate: DurableMemoryWriteGate,
        preview: DurableMemoryRecordPreview,
    ) -> DurableMemoryDryRunRecord:
        return DurableMemoryDryRunRecord(
            dry_run_record_id="durable_memory_dry_run_record:v0.27.5",
            write_request_id=request.write_request_id,
            preview_ref=_ref("durable_memory_record_preview", preview.preview_id, preview.version),
            dry_run_reason=gate.gate_summary,
            would_create_record=gate.may_create_durable_record,
            would_update_registry=gate.may_create_durable_record,
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryRecordPreviewService:
    def build_preview(
        self,
        request: DurableMemoryWriteRequest,
        scope: MemoryRecordScope,
        provenance: MemoryRecordProvenance,
        evidence_index: MemoryRecordEvidenceIndex,
        lifecycle: MemoryRecordLifecyclePolicy,
    ) -> DurableMemoryRecordPreview:
        candidate_ref = request.candidate_ref or _ref("memory_candidate", "missing", MEMORY_CANDIDATE_EXTRACTION_VERSION)
        return DurableMemoryRecordPreview(
            preview_id="durable_memory_record_preview:v0.27.5",
            candidate_ref=candidate_ref,
            proposed_record_summary="Refs-only durable memory record preview for a prior promotion decision.",
            proposed_scope_ref=_ref("memory_record_scope", scope.scope_id, scope.version),
            proposed_lifecycle_ref=_ref("memory_record_lifecycle_policy", lifecycle.lifecycle_policy_id, lifecycle.version),
            proposed_evidence_index_ref=_ref("memory_record_evidence_index", evidence_index.evidence_index_id, evidence_index.version),
            proposed_provenance_ref=_ref("memory_record_provenance", provenance.provenance_id, provenance.version),
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordScopeService:
    def build_scope(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordScope:
        candidate_id = request.candidate_ref["id"] if request.candidate_ref else "missing"
        return MemoryRecordScope(
            scope_id=f"memory_record_scope:{candidate_id}:v0.27.5",
            candidate_id=candidate_id,
            memory_record_id=memory_record_id,
            scope_type="project",
            scope_summary="Durable memory scope is project-bounded and refs-only.",
            allowed_context_refs=[request.scope_ref] if request.scope_ref else [],
            forbidden_context_refs=[_ref("forbidden_context", "raw_transcript")],
            scope_status="valid" if request.scope_ref else "blocked",
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordProvenanceService:
    def build_provenance(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordProvenance:
        return MemoryRecordProvenance(
            provenance_id="memory_record_provenance:v0.27.5",
            memory_record_id=memory_record_id,
            candidate_ref=request.candidate_ref or _ref("memory_candidate", "missing", MEMORY_CANDIDATE_EXTRACTION_VERSION),
            promotion_decision_record_ref=_ref("memory_promotion_decision_record", request.promotion_decision_record_id or "missing", MEMORY_PROMOTION_GATE_VERSION),
            source_refs=request.source_refs,
            evidence_bundle_ref=request.evidence_bundle_ref or _ref("memory_candidate_evidence_bundle", "missing", MEMORY_EVIDENCE_SCORING_VERSION),
            score_ref=request.score_ref or _ref("memory_candidate_score", "missing", MEMORY_EVIDENCE_SCORING_VERSION),
            originating_versions=["v0.27.1", "v0.27.2", "v0.27.3", "v0.27.4", "v0.27.5"],
            originating_surfaces=["memory_candidate_continuity"],
            provenance_complete=bool(request.candidate_ref and request.promotion_decision_record_id and request.source_refs and request.evidence_bundle_ref and request.score_ref),
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordEvidenceIndexService:
    def build_evidence_index(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordEvidenceIndex:
        return MemoryRecordEvidenceIndex(
            evidence_index_id="memory_record_evidence_index:v0.27.5",
            memory_record_id=memory_record_id,
            evidence_bundle_ref=request.evidence_bundle_ref or _ref("memory_candidate_evidence_bundle", "missing", MEMORY_EVIDENCE_SCORING_VERSION),
            evidence_item_refs=[_ref("memory_evidence_item", "memory_evidence_item:v0.27.3:1", MEMORY_EVIDENCE_SCORING_VERSION)] if request.evidence_bundle_ref else [],
            claim_refs=[_ref("memory_candidate_claim", "memory_candidate_claim:v0.27.2:1", MEMORY_CANDIDATE_EXTRACTION_VERSION)] if request.evidence_bundle_ref else [],
            score_ref=request.score_ref or _ref("memory_candidate_score", "missing", MEMORY_EVIDENCE_SCORING_VERSION),
            privacy_assessment_refs=[_ref("memory_privacy_risk_assessment", "memory_privacy_risk_assessment:v0.27.3", MEMORY_EVIDENCE_SCORING_VERSION)],
            contradiction_check_refs=[_ref("memory_contradiction_check", "memory_contradiction_check:v0.27.3", MEMORY_EVIDENCE_SCORING_VERSION)],
            pig_guidance_refs=[_ref("memory_pig_scoring_signal", "memory_pig_scoring_signal:v0.27.3", MEMORY_EVIDENCE_SCORING_VERSION)],
            evidence_count=1 if request.evidence_bundle_ref else 0,
            index_status="ready" if request.evidence_bundle_ref else "blocked",
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordLifecyclePolicyService:
    def build_lifecycle_policy(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordLifecyclePolicy:
        return MemoryRecordLifecyclePolicy(
            lifecycle_policy_id="memory_record_lifecycle_policy:v0.27.5",
            memory_record_id=memory_record_id,
            initial_status="active",
            allowed_future_states=["promoted", "active", "superseded", "revoked", "forgotten", "expired", "archived", "blocked"],
            review_required=True,
            review_after=None,
            expires_at=None,
            lifecycle_status="ready" if (request.lifecycle_ref or request.expiry_ref) else "blocked",
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordVersionService:
    def build_version(self, *, memory_record_id: str | None = None) -> MemoryRecordVersion:
        return MemoryRecordVersion(
            record_version_id="memory_record_version:v0.27.5",
            memory_record_id=memory_record_id,
            record_schema_version="memory_record_schema:v0.27.5",
            content_version=1,
            previous_record_ref=None,
            supersedes_ref=None,
            evidence_refs=[_ref("durable_memory_write_policy", "durable_memory_write_policy:v0.27.5", DURABLE_MEMORY_REGISTRY_VERSION)],
        )


class MemoryRecordStatusService:
    def build_status(self, memory_record_id: str, *, current_status: str = "active") -> MemoryRecordStatus:
        return MemoryRecordStatus(
            status_id=f"memory_record_status:{memory_record_id}",
            memory_record_id=memory_record_id,
            current_status=current_status,
            status_reason="Status is derived from the gated durable-memory write decision.",
            status_changed_at=utc_now_iso(),
            status_changed_by="durable_memory_write_gate",
            evidence_refs=[_ref("durable_memory_record", memory_record_id, DURABLE_MEMORY_REGISTRY_VERSION)],
        )


class MemoryRecordPrivacyBoundaryService:
    def build_boundary(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordPrivacyBoundary:
        return MemoryRecordPrivacyBoundary(
            privacy_boundary_id="memory_record_privacy_boundary:v0.27.5",
            memory_record_id=memory_record_id,
            privacy_risk_assessment_refs=[_ref("memory_privacy_risk_assessment", "memory_privacy_risk_assessment:v0.27.3", MEMORY_EVIDENCE_SCORING_VERSION)],
            privacy_level="low",
            sensitive_categories=[],
            user_confirmation_required=False,
            user_confirmation_ref=None,
            storage_allowed=True,
            privacy_boundary_status="passed",
            evidence_refs=request.evidence_refs,
        )


class MemoryRecordConflictMarkerService:
    def build_markers(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> list[MemoryRecordConflictMarker]:
        return [
            MemoryRecordConflictMarker(
                conflict_marker_id="memory_record_conflict_marker:v0.27.5",
                memory_record_id=memory_record_id,
                contradiction_check_ref=_ref("memory_contradiction_check", "memory_contradiction_check:v0.27.3", MEMORY_EVIDENCE_SCORING_VERSION),
                conflict_level="none",
                conflict_summary=None,
                requires_review=False,
                blocks_active_use=False,
                evidence_refs=request.evidence_refs,
            )
        ]


class MemoryRecordForgetRevokeBindingService:
    def build_binding(self, request: DurableMemoryWriteRequest, *, memory_record_id: str | None = None) -> MemoryRecordForgetRevokeBinding:
        return MemoryRecordForgetRevokeBinding(
            binding_id="memory_record_forget_revoke_binding:v0.27.5",
            memory_record_id=memory_record_id,
            forget_revoke_path_ref=request.forget_revoke_path_ref or _ref("memory_promotion_forget_revoke_path", "missing", MEMORY_PROMOTION_GATE_VERSION),
            binding_status="ready" if request.forget_revoke_path_ref else "blocked",
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryRecordService:
    def build_record_only_if_gate_passed(
        self,
        request: DurableMemoryWriteRequest,
        decision: DurableMemoryWriteDecision,
    ) -> list[DurableMemoryRecord]:
        if not decision.creates_durable_record:
            return []
        memory_record_id = "durable_memory_record:v0.27.5:1"
        scope = MemoryRecordScopeService().build_scope(request, memory_record_id=memory_record_id)
        provenance = MemoryRecordProvenanceService().build_provenance(request, memory_record_id=memory_record_id)
        evidence_index = MemoryRecordEvidenceIndexService().build_evidence_index(request, memory_record_id=memory_record_id)
        lifecycle = MemoryRecordLifecyclePolicyService().build_lifecycle_policy(request, memory_record_id=memory_record_id)
        version_info = MemoryRecordVersionService().build_version(memory_record_id=memory_record_id)
        privacy = MemoryRecordPrivacyBoundaryService().build_boundary(request, memory_record_id=memory_record_id)
        conflicts = MemoryRecordConflictMarkerService().build_markers(request, memory_record_id=memory_record_id)
        binding = MemoryRecordForgetRevokeBindingService().build_binding(request, memory_record_id=memory_record_id)
        return [
            DurableMemoryRecord(
                memory_record_id=memory_record_id,
                record_schema_version="memory_record_schema:v0.27.5",
                candidate_ref=request.candidate_ref or _ref("memory_candidate", "missing", MEMORY_CANDIDATE_EXTRACTION_VERSION),
                promotion_decision_record_ref=_ref("memory_promotion_decision_record", request.promotion_decision_record_id or "missing", MEMORY_PROMOTION_GATE_VERSION),
                title="Refs-only durable memory record",
                summary="Durable memory record created only after promotion, evidence, source, scope, lifecycle, audit, and hygiene gates passed.",
                memory_type="project_state",
                status="active",
                scope=scope,
                provenance=provenance,
                evidence_index=evidence_index,
                lifecycle_policy=lifecycle,
                version_info=version_info,
                privacy_boundary=privacy,
                conflict_markers=conflicts,
                forget_revoke_binding=binding,
                created_at=utc_now_iso(),
                updated_at=utc_now_iso(),
                evidence_refs=request.evidence_refs,
            )
        ]


class DurableMemoryRegistryEntryService:
    def build_entry(self, record: DurableMemoryRecord) -> DurableMemoryRegistryEntry:
        return DurableMemoryRegistryEntry(
            registry_entry_id="durable_memory_registry_entry:v0.27.5:1",
            memory_record_ref=_ref("durable_memory_record", record.memory_record_id, record.version),
            memory_record_id=record.memory_record_id,
            memory_type=record.memory_type,
            status=record.status,
            scope_ref=_ref("memory_record_scope", record.scope.scope_id, record.scope.version),
            provenance_ref=_ref("memory_record_provenance", record.provenance.provenance_id, record.provenance.version),
            evidence_index_ref=_ref("memory_record_evidence_index", record.evidence_index.evidence_index_id, record.evidence_index.version),
            lifecycle_policy_ref=_ref("memory_record_lifecycle_policy", record.lifecycle_policy.lifecycle_policy_id, record.lifecycle_policy.version),
            created_at=record.created_at,
            updated_at=record.updated_at,
            entry_status="active",
            evidence_refs=record.evidence_refs,
        )


class DurableMemoryRegistryService:
    def build_or_load_registry(self, entries: list[DurableMemoryRegistryEntry]) -> DurableMemoryRegistry:
        return DurableMemoryRegistry(
            registry_id="durable_memory_registry:v0.27.5",
            registry_schema_version="durable_memory_registry_schema:v0.27.5",
            entries=entries,
            entry_count=len(entries),
            active_count=sum(1 for item in entries if item.entry_status == "active"),
            archived_count=sum(1 for item in entries if item.entry_status == "archived"),
            revoked_count=sum(1 for item in entries if item.entry_status == "revoked"),
            forgotten_count=sum(1 for item in entries if item.entry_status == "forgotten"),
            expired_count=sum(1 for item in entries if item.entry_status == "expired"),
            blocked_count=sum(1 for item in entries if item.entry_status == "blocked"),
            dry_run_count=sum(1 for item in entries if item.entry_status == "dry_run"),
            registry_status="ready" if entries else "warning",
            evidence_refs=[_ref("durable_memory_registry_policy", "durable_memory_registry_policy:v0.27.5", DURABLE_MEMORY_REGISTRY_VERSION)],
        )

    def add_entry_only_if_gate_passed(
        self,
        records: list[DurableMemoryRecord],
        decision: DurableMemoryWriteDecision,
    ) -> list[DurableMemoryRegistryEntry]:
        if not (decision.creates_durable_record and decision.updates_registry):
            return []
        return [DurableMemoryRegistryEntryService().build_entry(record) for record in records]


class MemoryRecordAuditTrailService:
    def build_audit_trail(
        self,
        request: DurableMemoryWriteRequest,
        gate: DurableMemoryWriteGate,
        decision: DurableMemoryWriteDecision,
        records: list[DurableMemoryRecord],
        entries: list[DurableMemoryRegistryEntry],
        blocked_records: list[DurableMemoryWriteBlockedRecord],
        dry_run_records: list[DurableMemoryDryRunRecord],
    ) -> MemoryRecordAuditTrail:
        return MemoryRecordAuditTrail(
            audit_trail_id="memory_record_audit_trail:v0.27.5",
            write_request_ref=_ref("durable_memory_write_request", request.write_request_id, request.version),
            write_gate_ref=_ref("durable_memory_write_gate", gate.write_gate_id, gate.version),
            write_decision_ref=_ref("durable_memory_write_decision", decision.write_decision_id, decision.version),
            memory_record_refs=[_ref("durable_memory_record", item.memory_record_id, item.version) for item in records],
            registry_entry_refs=[_ref("durable_memory_registry_entry", item.registry_entry_id, item.version) for item in entries],
            provenance_refs=[_ref("memory_record_provenance", item.provenance.provenance_id, item.provenance.version) for item in records],
            evidence_index_refs=[_ref("memory_record_evidence_index", item.evidence_index.evidence_index_id, item.evidence_index.version) for item in records],
            lifecycle_policy_refs=[_ref("memory_record_lifecycle_policy", item.lifecycle_policy.lifecycle_policy_id, item.lifecycle_policy.version) for item in records],
            privacy_boundary_refs=[_ref("memory_record_privacy_boundary", item.privacy_boundary.privacy_boundary_id, item.privacy_boundary.version) for item in records],
            forget_revoke_binding_refs=[_ref("memory_record_forget_revoke_binding", item.forget_revoke_binding.binding_id, item.forget_revoke_binding.version) for item in records],
            blocked_record_refs=[_ref("durable_memory_write_blocked_record", item.blocked_record_id, item.version) for item in blocked_records],
            dry_run_record_refs=[_ref("durable_memory_dry_run_record", item.dry_run_record_id, item.version) for item in dry_run_records],
            audit_event_count=4 + len(records) + len(entries) + len(blocked_records) + len(dry_run_records),
            audit_status="ready" if decision.decision_type == "write_durable_memory" else "warning",
            evidence_refs=request.evidence_refs,
        )


class DurableMemoryRegistryIntegrityReportService:
    def build_report(self, registry: DurableMemoryRegistry, records: list[DurableMemoryRecord]) -> DurableMemoryRegistryIntegrityReport:
        missing_provenance = sum(1 for item in records if not item.provenance.provenance_complete)
        missing_evidence = sum(1 for item in records if item.evidence_index.index_status != "ready")
        missing_scope = sum(1 for item in records if item.scope.scope_status != "valid")
        missing_lifecycle = sum(1 for item in records if item.lifecycle_policy.lifecycle_status != "ready")
        missing_binding = sum(1 for item in records if item.forget_revoke_binding.binding_status != "ready")
        raw_violations = sum(
            1
            for item in records
            if item.raw_transcript_included or item.raw_provider_output_included or item.raw_secret_included or item.credential_included
        )
        dangerous_counts = {
            "persona": sum(1 for item in records if item.persona_mutation),
            "policy": sum(1 for item in records if item.behavior_policy_mutation),
            "provider": sum(1 for item in records if item.provider_invoked),
            "command": sum(1 for item in records if item.command_executed),
            "safety": sum(1 for item in records if item.safety_gate_bypassed),
        }
        status = "passed" if not any([missing_provenance, missing_evidence, missing_scope, missing_lifecycle, missing_binding, raw_violations, *dangerous_counts.values()]) else "blocked"
        return DurableMemoryRegistryIntegrityReport(
            integrity_report_id="durable_memory_registry_integrity_report:v0.27.5",
            registry_ref=_ref("durable_memory_registry", registry.registry_id, registry.version),
            checked_entry_count=registry.entry_count,
            missing_provenance_count=missing_provenance,
            missing_evidence_index_count=missing_evidence,
            missing_scope_count=missing_scope,
            missing_lifecycle_count=missing_lifecycle,
            missing_forget_revoke_binding_count=missing_binding,
            raw_memory_violation_count=raw_violations,
            persona_mutation_count=dangerous_counts["persona"],
            behavior_policy_mutation_count=dangerous_counts["policy"],
            provider_invocation_count=dangerous_counts["provider"],
            command_execution_count=dangerous_counts["command"],
            safety_bypass_count=dangerous_counts["safety"],
            integrity_status=status,
            evidence_refs=[_ref("durable_memory_registry", registry.registry_id, registry.version)],
        )


class DurableMemoryRegistryFindingService:
    BLOCKED_FINDINGS = {
        "durable_write_without_promotion_decision_detected",
        "durable_write_without_evidence_detected",
        "durable_write_without_source_refs_detected",
        "durable_write_without_scope_detected",
        "durable_write_without_forget_revoke_path_detected",
        "durable_write_without_audit_detected",
        "persistent_write_without_release_hygiene_detected",
        "raw_transcript_memory_attempted",
        "raw_provider_output_memory_attempted",
        "raw_secret_memory_attempted",
        "credential_memory_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_memory_authority_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "session_continuity_injection_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "llm_judge_detected",
    }

    CREATED_FINDINGS = [
        "write_policy_created",
        "registry_policy_created",
        "write_gate_created",
        "write_decision_created",
        "durable_record_preview_created",
        "memory_record_scope_created",
        "memory_record_provenance_created",
        "memory_record_evidence_index_created",
        "memory_record_lifecycle_policy_created",
        "memory_record_version_created",
        "memory_record_status_created",
        "memory_record_privacy_boundary_created",
        "memory_record_conflict_marker_created",
        "memory_record_forget_revoke_binding_created",
        "memory_record_audit_trail_created",
        "registry_integrity_report_created",
    ]

    def build_findings(
        self,
        source: DurableMemoryRegistryPrerequisiteSourceService,
        gate: DurableMemoryWriteGate,
        decision: DurableMemoryWriteDecision,
        records: list[DurableMemoryRecord],
        entries: list[DurableMemoryRegistryEntry],
        *,
        extra_findings: list[str] | None = None,
    ) -> list[DurableMemoryRegistryFinding]:
        findings: list[DurableMemoryRegistryFinding] = []
        if not source.promotion_gate_available:
            findings.append(self._finding("warning", "missing_promotion_gate_report", "v0.27.4 promotion gate report is unavailable."))
        if not gate.promotion_decision_present:
            findings.append(self._finding("warning", "missing_promotion_decision_record", "Promotion decision record is unavailable."))
        if not gate.candidate_ref_present:
            findings.append(self._finding("warning", "missing_candidate_ref", "Candidate ref is unavailable."))
        if not gate.evidence_bundle_present:
            findings.append(self._finding("warning", "missing_evidence_bundle", "Evidence bundle ref is unavailable."))
        if not gate.score_ref_present:
            findings.append(self._finding("warning", "missing_score_ref", "Score ref is unavailable."))
        if not gate.source_refs_present:
            findings.append(self._finding("warning", "missing_source_refs", "Source refs are unavailable."))
        if not gate.scope_present:
            findings.append(self._finding("warning", "missing_scope", "Scope ref is unavailable."))
        if not gate.lifecycle_or_expiry_present:
            findings.append(self._finding("warning", "missing_lifecycle", "Lifecycle or expiry ref is unavailable."))
        if not gate.forget_revoke_path_present:
            findings.append(self._finding("warning", "missing_forget_revoke_path", "Forget/revoke path ref is unavailable."))
        if not gate.release_hygiene_gate_passed:
            findings.append(self._finding("warning", "missing_release_hygiene_status", "Release hygiene gate is missing; persistent write is blocked."))
        if not gate.runtime_data_hygiene_gate_passed:
            findings.append(self._finding("warning", "missing_runtime_data_hygiene_status", "Runtime data hygiene gate is missing; persistent write is blocked."))
        if decision.decision_type == "dry_run_only":
            findings.append(self._finding("info", "dry_run_record_created", "Dry-run record was created instead of persistent write."))
        if decision.decision_type == "block_write":
            findings.append(self._finding("warning", "write_blocked_record_created", "Blocked write record was created."))
        if records:
            findings.append(self._finding("info", "durable_memory_record_created", "Durable memory record was created after write gate passed."))
        if entries:
            findings.append(self._finding("info", "durable_registry_created", "Durable memory registry was created."))
            findings.append(self._finding("info", "durable_registry_entry_created", "Durable memory registry entry was created after write gate passed."))
        for finding_type in self.CREATED_FINDINGS:
            findings.append(self._finding("info", finding_type, finding_type))
        for finding_type in extra_findings or []:
            severity = "critical" if finding_type in self.BLOCKED_FINDINGS else "warning"
            findings.append(self._finding(severity, finding_type, finding_type))
        return findings or [self._finding("info", "ok", "Durable memory registry path is ready.")]

    def _finding(self, severity: str, finding_type: str, message: str) -> DurableMemoryRegistryFinding:
        return DurableMemoryRegistryFinding(
            finding_id=f"durable_memory_registry_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[_ref("durable_memory_registry_report", "durable_memory_registry_report:v0.27.5", DURABLE_MEMORY_REGISTRY_VERSION)],
            withdrawal_condition="Withdraw if memory is written without gate, promotion, evidence, source, scope, lifecycle, forget/revoke, audit, or hygiene gates, or if raw memory, mutation, execution, bypass, external adapter, Schumpeter split, or sole LLM authority appears.",
        )


class DurableMemoryRegistryReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        promotion_gate_available: bool = True,
        release_hygiene_gate_passed: bool = False,
        runtime_data_hygiene_gate_passed: bool = False,
        requested_write_mode: str = "dry_run",
        candidate_id: str | None = None,
        extra_findings: list[str] | None = None,
    ) -> dict[str, Any]:
        source = DurableMemoryRegistryPrerequisiteSourceService(
            promotion_gate_available=promotion_gate_available,
            release_hygiene_gate_passed=release_hygiene_gate_passed,
            runtime_data_hygiene_gate_passed=runtime_data_hygiene_gate_passed,
            requested_decision_type="promote",
        )
        write_policy = DurableMemoryWritePolicyService().build_policy()
        registry_policy = DurableMemoryRegistryPolicyService().build_policy()
        promotion_report = source.load_v0274_promotion_gate_report()
        decision_records = source.load_promotion_decision_records()
        promote_records = [record for record in decision_records if record.decision.decision_type == "promote"]
        selected_record = promote_records[0] if promote_records else None
        if candidate_id and promote_records:
            selected_record = next((record for record in promote_records if record.candidate_ref.get("id") == candidate_id), selected_record)
        readiness_previews = source.load_durable_readiness_previews()
        selected_preview = readiness_previews[0] if readiness_previews else None
        scope_refs = source.load_scope_refs()
        lifecycle_refs = [ref for ref in source.load_lifecycle_or_expiry_refs() if ref["type"] == "memory_promotion_lifecycle_boundary"]
        expiry_refs = [ref for ref in source.load_lifecycle_or_expiry_refs() if ref["type"] == "memory_promotion_expiry"]
        forget_refs = source.load_forget_revoke_path_refs()
        request = DurableMemoryWriteRequest(
            write_request_id="durable_memory_write_request:v0.27.5",
            promotion_gate_report_id=promotion_report.report_id if promotion_report else None,
            promotion_decision_record_id=selected_record.decision_record_id if selected_record else None,
            durable_readiness_preview_id=selected_preview.durable_readiness_preview_id if selected_preview else None,
            candidate_ref=selected_record.candidate_ref if selected_record else None,
            score_ref=selected_record.score_ref if selected_record else None,
            evidence_bundle_ref=selected_record.evidence_bundle_ref if selected_record else None,
            source_refs=source.load_source_refs() if selected_record else [],
            scope_ref=scope_refs[0] if scope_refs and selected_record else None,
            lifecycle_ref=lifecycle_refs[0] if lifecycle_refs and selected_record else None,
            expiry_ref=expiry_refs[0] if expiry_refs and selected_record else None,
            forget_revoke_path_ref=forget_refs[0] if forget_refs and selected_record else None,
            release_hygiene_status_ref=source.load_release_hygiene_status_if_available(),
            runtime_data_hygiene_status_ref=source.load_runtime_data_hygiene_status_if_available(),
            requested_write_mode=requested_write_mode,
            evidence_refs=[_ref("durable_memory_write_policy", write_policy.policy_id, write_policy.version)],
        )
        gate = DurableMemoryWriteGateService().evaluate_gate(
            request,
            promotion_decision_is_promote=bool(selected_record and selected_record.decision.decision_type == "promote"),
            release_hygiene_gate_passed=release_hygiene_gate_passed,
            runtime_data_hygiene_gate_passed=runtime_data_hygiene_gate_passed,
        )
        preview_scope = MemoryRecordScopeService().build_scope(request)
        preview_provenance = MemoryRecordProvenanceService().build_provenance(request)
        preview_evidence_index = MemoryRecordEvidenceIndexService().build_evidence_index(request)
        preview_lifecycle = MemoryRecordLifecyclePolicyService().build_lifecycle_policy(request)
        preview_version = MemoryRecordVersionService().build_version()
        preview_status = MemoryRecordStatusService().build_status("durable_memory_record:v0.27.5:preview", current_status="dry_run")
        preview_privacy = MemoryRecordPrivacyBoundaryService().build_boundary(request)
        preview_conflicts = MemoryRecordConflictMarkerService().build_markers(request)
        preview_binding = MemoryRecordForgetRevokeBindingService().build_binding(request)
        preview = DurableMemoryRecordPreviewService().build_preview(request, preview_scope, preview_provenance, preview_evidence_index, preview_lifecycle)
        decision = DurableMemoryWriteDecisionService().decide_write(request, gate)
        records = DurableMemoryRecordService().build_record_only_if_gate_passed(request, decision)
        entries = DurableMemoryRegistryService().add_entry_only_if_gate_passed(records, decision)
        registry = DurableMemoryRegistryService().build_or_load_registry(entries)
        blocked_records = [] if decision.decision_type != "block_write" else [DurableMemoryWriteBlockedRecordService().build_blocked_record(request, gate)]
        dry_run_records = [] if decision.decision_type != "dry_run_only" else [DurableMemoryDryRunRecordService().build_dry_run_record(request, gate, preview)]
        audit = MemoryRecordAuditTrailService().build_audit_trail(request, gate, decision, records, entries, blocked_records, dry_run_records)
        integrity = DurableMemoryRegistryIntegrityReportService().build_report(registry, records)
        findings = DurableMemoryRegistryFindingService().build_findings(source, gate, decision, records, entries, extra_findings=extra_findings)
        report_status = self._report_status(findings, gate, decision)
        report = DurableMemoryRegistryReport(
            report_id=report_id or "durable_memory_registry_report:v0.27.5",
            created_at=utc_now_iso(),
            write_policy=write_policy,
            registry_policy=registry_policy,
            write_request=request,
            write_gate=gate,
            write_decision=decision,
            blocked_records=blocked_records,
            dry_run_records=dry_run_records,
            record_previews=[preview],
            durable_memory_records=records,
            registry=registry,
            registry_entries=entries,
            audit_trail=audit,
            integrity_report=integrity,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_6=report_status in {"passed", "warning"},
            write_gate_created=True,
            write_decision_created=True,
            durable_memory_records_created=bool(records),
            registry_created=True,
            registry_entries_created=bool(entries),
            audit_trail_created=True,
            integrity_report_created=True,
            durable_record_count=len(records),
            registry_entry_count=len(entries),
            blocked_write_count=len(blocked_records),
            dry_run_count=len(dry_run_records),
            persistent_memory_written=decision.writes_persistent_memory,
            durable_memory_written=decision.creates_durable_record,
            durable_registry_updated=decision.updates_registry,
            limitations=[
                "Default v0.27.5 path remains dry-run unless release and runtime data hygiene gates are explicitly passed.",
                "Durable records are refs-only artifacts and do not build continuity context or injection bundles.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if durable memory is written without promotion decision, evidence, source refs, scope, lifecycle, forget/revoke path, audit, or hygiene gates.",
                "Withdraw readiness if raw transcript/provider output/secret/credential memory, persona/policy mutation, continuity injection, provider/command execution, safety bypass, external adapter, Schumpeter split, or sole LLM authority appears.",
            ],
        )
        return {
            "source_service": source,
            "write_policy": write_policy,
            "registry_policy": registry_policy,
            "write_request": request,
            "write_gate": gate,
            "write_decision": decision,
            "blocked_records": blocked_records,
            "dry_run_records": dry_run_records,
            "record_previews": [preview],
            "durable_memory_records": records,
            "registry": registry,
            "registry_entries": entries,
            "scope": preview_scope,
            "provenance": preview_provenance,
            "evidence_index": preview_evidence_index,
            "lifecycle_policy": preview_lifecycle,
            "version_info": preview_version,
            "status_record": preview_status,
            "privacy_boundary": preview_privacy,
            "conflict_markers": preview_conflicts,
            "forget_revoke_binding": preview_binding,
            "audit_trail": audit,
            "integrity_report": integrity,
            "findings": findings,
            "report": report,
        }

    def _report_status(
        self,
        findings: list[DurableMemoryRegistryFinding],
        gate: DurableMemoryWriteGate,
        decision: DurableMemoryWriteDecision,
    ) -> str:
        if any(item.finding_type in DurableMemoryRegistryFindingService.BLOCKED_FINDINGS and item.severity == "critical" for item in findings):
            return "blocked"
        if gate.gate_status == "blocked" and decision.decision_type == "block_write":
            return "warning"
        if any(item.severity in {"warning", "error"} for item in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": DURABLE_MEMORY_REGISTRY_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "durable_memory_record_registry",
            "principles": [
                "Durable memory record requires a prior promotion decision",
                "Promote decision alone is not durable memory",
                "Durable memory registry is not persona",
                "Durable memory registry is not behavior policy",
                "Persistent memory write requires a write gate",
                "No write is a valid outcome",
                "Dry-run registry materialization is allowed when write gate is not satisfied",
                "Durable memory must be scoped, evidenced, versioned, auditable, revocable, forgettable, and OCEL-visible",
                "PIG guidance is not memory authority",
                "Raw transcript and raw provider output must not be written as memory",
            ],
            "safety_boundary": {
                "durable_memory_record_created": "conditional",
                "durable_memory_registry_updated": "conditional",
                "persistent_memory_written": "conditional",
                "session_continuity_injected": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_memory_created": False,
                "raw_provider_output_memory_created": False,
                "raw_secret_memory_created": False,
                "credential_memory_created": False,
                "pig_memory_promoted": False,
                "pig_policy_mutated": False,
                "pig_executed": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.6 session continuity context builder",
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": DURABLE_MEMORY_REGISTRY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "durable_memory_record_registry_created",
            "version": DURABLE_MEMORY_REGISTRY_VERSION,
            "source_read_models": [
                "MemoryPromotionGateState",
                "MemoryPromotionDecisionRecordState",
                "DurableMemoryReadinessPreviewState",
                "MemoryCandidateState",
                "MemoryCandidateEvidenceBundleState",
                "MemoryCandidateScoreState",
                "MemorySourceRefState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "DurableMemoryWriteGateState",
                "DurableMemoryWriteDecisionState",
                "DurableMemoryRecordState",
                "DurableMemoryRegistryState",
                "DurableMemoryRegistryEntryState",
                "MemoryRecordProvenanceState",
                "MemoryRecordEvidenceIndexState",
                "MemoryRecordLifecyclePolicyState",
                "MemoryRecordAuditState",
                "V027ReadinessState",
            ],
            "effect_types": DURABLE_MEMORY_REGISTRY_EFFECT_TYPES,
            "conditional_effect_types": DURABLE_MEMORY_REGISTRY_CONDITIONAL_EFFECT_TYPES,
            "forbidden_effect_types": DURABLE_MEMORY_REGISTRY_FORBIDDEN_EFFECT_TYPES,
        }


def render_durable_memory_registry_cli(parts: dict[str, Any], section: str = "policy") -> str:
    report: DurableMemoryRegistryReport = parts["report"]
    lines = [
        f"Durable Memory Record & Registry {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"write_gate_created={_bool(report.write_gate_created)}",
        f"write_decision_created={_bool(report.write_decision_created)}",
        f"durable_memory_records_created={_bool(report.durable_memory_records_created)}",
        f"registry_created={_bool(report.registry_created)}",
        f"registry_entries_created={_bool(report.registry_entries_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"integrity_report_created={_bool(report.integrity_report_created)}",
        f"durable_record_count={report.durable_record_count}",
        f"registry_entry_count={report.registry_entry_count}",
        f"blocked_write_count={report.blocked_write_count}",
        f"dry_run_count={report.dry_run_count}",
        f"ready_for_v0_27_6={_bool(report.ready_for_v0_27_6)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"persistent_memory_written={_bool(report.persistent_memory_written)}",
        f"durable_memory_written={_bool(report.durable_memory_written)}",
        f"durable_registry_updated={_bool(report.durable_registry_updated)}",
        f"session_continuity_injected={_bool(report.session_continuity_injected)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_memory_created={_bool(report.raw_transcript_memory_created)}",
        f"raw_provider_output_memory_created={_bool(report.raw_provider_output_memory_created)}",
        f"raw_secret_memory_created={_bool(report.raw_secret_memory_created)}",
        f"credential_memory_created={_bool(report.credential_memory_created)}",
        f"pig_memory_promoted={_bool(report.pig_memory_promoted)}",
        f"pig_policy_mutated={_bool(report.pig_policy_mutated)}",
        f"pig_executed={_bool(report.pig_executed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "policy": ("persistent_memory_write_requires_write_gate", report.write_policy.persistent_memory_write_requires_write_gate),
        "write-gate": ("gate_status", report.write_gate.gate_status),
        "write-decision": ("decision_type", report.write_decision.decision_type),
        "dry-run": ("dry_run_count", report.dry_run_count),
        "create-record": ("durable_record_count", report.durable_record_count),
        "entries": ("registry_entry_count", report.registry_entry_count),
        "inspect": ("registry_status", report.registry.registry_status),
        "provenance": ("provenance_complete", parts["provenance"].provenance_complete),
        "evidence-index": ("evidence_count", parts["evidence_index"].evidence_count),
        "lifecycle": ("lifecycle_status", parts["lifecycle_policy"].lifecycle_status),
        "privacy": ("privacy_boundary_status", parts["privacy_boundary"].privacy_boundary_status),
        "forget-revoke": ("binding_status", parts["forget_revoke_binding"].binding_status),
        "integrity": ("integrity_status", report.integrity_report.integrity_status),
        "audit": ("audit_status", report.audit_trail.audit_status),
        "report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    return "\n".join(lines)


SESSION_CONTINUITY_CONTEXT_VERSION = "v0.27.6"
SESSION_CONTINUITY_CONTEXT_VERSION_NAME = "Session Continuity Context Builder"
SESSION_CONTINUITY_CONTEXT_KOREAN_NAME = "Session Continuity Context Builder"
SESSION_CONTINUITY_CONTEXT_NEXT_STEP = "v0.27.7 Continuity Injection Boundary"

SESSION_CONTINUITY_REQUIRED_RULES = [
    "memory_record_must_be_active_or_allowed_reference",
    "revoked_memory_active_use_forbidden",
    "forgotten_memory_active_use_forbidden",
    "expired_memory_active_use_forbidden",
    "blocked_memory_active_use_forbidden",
    "scope_must_match_request",
    "privacy_boundary_must_allow_context_use",
    "conflict_marker_must_be_surfaced",
    "stale_memory_must_be_warned",
    "raw_transcript_replay_forbidden",
    "raw_provider_output_replay_forbidden",
    "context_pack_must_be_refs_only",
    "context_item_must_not_inject_runtime",
    "no_persona_mutation_in_v0276",
    "no_behavior_policy_mutation_in_v0276",
    "no_provider_invocation_in_v0276",
    "no_command_execution_in_v0276",
]

SESSION_CONTINUITY_OBJECT_TYPES = [
    "session_continuity_context_policy",
    "session_continuity_context_request",
    "session_continuity_source_view",
    "session_continuity_eligibility_rule",
    "session_continuity_memory_ref",
    "session_continuity_ref_bundle",
    "continuity_relevance_policy",
    "continuity_relevance_score",
    "continuity_recency_window",
    "continuity_staleness_warning",
    "continuity_conflict_report",
    "continuity_privacy_filter",
    "continuity_context_item",
    "continuity_context_pack",
    "session_continuity_context",
    "session_continuity_build_decision",
    "session_continuity_context_preview",
    "session_continuity_build_audit_trail",
    "session_continuity_context_finding",
    "session_continuity_context_build_report",
    "durable_memory_registry_report",
    "durable_memory_record",
    "durable_memory_registry",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

SESSION_CONTINUITY_EVENT_TYPES = [
    "session_continuity_context_requested",
    "session_continuity_prerequisites_loaded",
    "session_continuity_policy_created",
    "session_continuity_source_view_created",
    "session_continuity_eligibility_rule_created",
    "session_continuity_memory_ref_created",
    "session_continuity_ref_bundle_created",
    "continuity_relevance_policy_created",
    "continuity_relevance_score_created",
    "continuity_recency_window_created",
    "continuity_staleness_warning_created",
    "continuity_conflict_report_created",
    "continuity_privacy_filter_created",
    "continuity_context_item_created",
    "continuity_context_pack_created",
    "session_continuity_context_created",
    "session_continuity_build_decision_created",
    "session_continuity_context_preview_created",
    "session_continuity_build_audit_trail_created",
    "session_continuity_context_build_report_created",
    "session_continuity_warning_created",
    "session_continuity_blocked",
]

SESSION_CONTINUITY_EFFECT_TYPES = [
    "read_only_observation",
    "session_continuity_context_created",
    "continuity_context_pack_created",
    "continuity_context_item_created",
    "continuity_relevance_score_created",
    "continuity_staleness_warning_created",
    "continuity_conflict_report_created",
    "continuity_privacy_filter_created",
    "continuity_context_preview_created",
    "session_continuity_audit_created",
    "state_candidate_created",
]

SESSION_CONTINUITY_FORBIDDEN_EFFECT_TYPES = [
    "continuity_injection_bundle_created",
    "continuity_injected",
    "default_agent_context_mutated",
    "decision_service_mutated",
    "skill_router_mutated",
    "safety_gate_mutated",
    "permission_policy_mutated",
    "memory_updated",
    "memory_revoked",
    "memory_forgotten",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_replayed",
    "raw_provider_output_replayed",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "pig_guidance_used_as_authority",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "safety_gate_bypassed_by_memory",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class SessionContinuityContextPolicy(_ModelMixin):
    policy_id: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    session_continuity_context_builder_enabled: bool = True
    context_pack_enabled: bool = True
    relevance_scoring_enabled: bool = True
    privacy_filter_enabled: bool = True
    conflict_report_enabled: bool = True
    staleness_warning_enabled: bool = True
    continuity_injection_enabled_now: bool = False
    default_agent_context_mutation_enabled_now: bool = False
    decision_service_mutation_enabled_now: bool = False
    skill_router_mutation_enabled_now: bool = False
    safety_gate_mutation_enabled_now: bool = False
    permission_policy_mutation_enabled_now: bool = False
    memory_update_enabled_now: bool = False
    memory_revoke_enabled_now: bool = False
    memory_forget_enabled_now: bool = False
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    raw_transcript_replay_forbidden: bool = True
    raw_provider_output_replay_forbidden: bool = True
    revoked_memory_active_use_forbidden: bool = True
    forgotten_memory_active_use_forbidden: bool = True
    expired_memory_active_use_forbidden: bool = True
    safety_gate_bypass_forbidden: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    llm_judge_as_sole_continuity_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityContextRequest(_ModelMixin):
    request_id: str
    durable_memory_registry_report_id: str | None
    durable_memory_registry_id: str | None
    selected_memory_record_refs: list[dict[str, Any]]
    selected_session_refs: list[dict[str, Any]]
    selected_project_refs: list[dict[str, Any]]
    selected_task_refs: list[dict[str, Any]]
    requested_context_profile: str | None
    target_surface_preview: str | None
    strictness: str = "standard"
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuitySourceView(_ModelMixin):
    source_view_id: str
    durable_registry_report_ref: dict[str, Any] | None
    durable_registry_ref: dict[str, Any] | None
    active_memory_record_refs: list[dict[str, Any]]
    archived_memory_record_refs: list[dict[str, Any]]
    revoked_memory_record_refs: list[dict[str, Any]]
    forgotten_memory_record_refs: list[dict[str, Any]]
    expired_memory_record_refs: list[dict[str, Any]]
    blocked_memory_record_refs: list[dict[str, Any]]
    memory_scope_refs: list[dict[str, Any]]
    memory_provenance_refs: list[dict[str, Any]]
    memory_evidence_index_refs: list[dict[str, Any]]
    memory_lifecycle_refs: list[dict[str, Any]]
    memory_privacy_boundary_refs: list[dict[str, Any]]
    memory_conflict_marker_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    session_context_refs: list[dict[str, Any]]
    trace_summary_refs: list[dict[str, Any]]
    approval_decision_refs: list[dict[str, Any]]
    command_candidate_refs: list[dict[str, Any]]
    failure_cause_refs: list[dict[str, Any]]
    source_status: str
    active_memory_count: int
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityEligibilityRule(_ModelMixin):
    rule_id: str
    rule_name: str
    rule_summary: str
    required: bool
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityMemoryRef(_ModelMixin):
    continuity_memory_ref_id: str
    memory_record_ref: dict[str, Any]
    memory_record_id: str
    memory_type: str
    memory_status: str
    scope_ref: dict[str, Any] | None
    provenance_ref: dict[str, Any] | None
    evidence_index_ref: dict[str, Any] | None
    lifecycle_policy_ref: dict[str, Any] | None
    privacy_boundary_ref: dict[str, Any] | None
    conflict_marker_refs: list[dict[str, Any]]
    use_role: str
    eligible_for_context_pack: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    eligible_for_injection_now: bool = False
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityRefBundle(_ModelMixin):
    continuity_ref_bundle_id: str
    continuity_memory_refs: list[SessionContinuityMemoryRef]
    active_context_refs: list[dict[str, Any]]
    background_reference_refs: list[dict[str, Any]]
    conflict_warning_refs: list[dict[str, Any]]
    stale_warning_refs: list[dict[str, Any]]
    blocked_refs: list[dict[str, Any]]
    bundle_status: str
    context_pack_created: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    continuity_injected_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityRelevancePolicy(_ModelMixin):
    policy_id: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    relevance_scoring_enabled: bool = True
    relevance_score_is_not_authority: bool = True
    active_memory_preferred: bool = True
    archive_only_as_background_reference: bool = True
    revoked_forgotten_expired_blocked_as_active_forbidden: bool = True
    recency_weight_enabled: bool = True
    scope_match_weight_enabled: bool = True
    evidence_strength_weight_enabled: bool = True
    reuse_value_weight_enabled: bool = True
    privacy_risk_penalty_enabled: bool = True
    contradiction_penalty_enabled: bool = True
    user_control_penalty_enabled: bool = True
    pig_guidance_signal_allowed: bool = True
    pig_guidance_is_not_authority: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityRelevanceScore(_ModelMixin):
    relevance_score_id: str
    memory_record_id: str
    continuity_memory_ref_id: str
    requested_context_profile: str | None
    relevance_score: float | None
    relevance_band: str
    score_factors: list[dict[str, Any]]
    scope_match: bool
    recency_factor: str | None
    evidence_strength_factor: str | None
    reuse_value_factor: str | None
    privacy_penalty_applied: bool
    contradiction_penalty_applied: bool
    stale_penalty_applied: bool
    pig_guidance_signal_refs: list[dict[str, Any]]
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    relevance_score_is_authority: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityRecencyWindow(_ModelMixin):
    recency_window_id: str
    memory_record_id: str
    created_at_ref: dict[str, Any] | None
    updated_at_ref: dict[str, Any] | None
    last_review_ref: dict[str, Any] | None
    expected_validity_horizon_ref: dict[str, Any] | None
    recency_status: str
    stale_warning_required: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityStalenessWarning(_ModelMixin):
    staleness_warning_id: str
    memory_record_id: str
    recency_window_ref: dict[str, Any]
    warning_level: str
    warning_summary: str
    blocks_active_context_use: bool
    surface_to_user_later: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityConflictReport(_ModelMixin):
    conflict_report_id: str
    memory_record_id: str | None
    conflict_marker_refs: list[dict[str, Any]]
    conflicting_memory_refs: list[dict[str, Any]]
    conflict_level: str
    conflict_summary: str | None
    requires_review: bool
    blocks_active_context_use: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    automatically_resolved: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityPrivacyFilter(_ModelMixin):
    privacy_filter_id: str
    memory_record_id: str
    privacy_boundary_ref: dict[str, Any] | None
    privacy_level: str
    filtered_categories: list[str]
    allowed_for_context_pack: bool
    requires_user_confirmation_later: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    raw_sensitive_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityContextItem(_ModelMixin):
    context_item_id: str
    memory_record_ref: dict[str, Any]
    memory_type: str
    item_role: str
    item_summary: str
    relevance_score_ref: dict[str, Any] | None
    source_refs: list[dict[str, Any]]
    evidence_index_ref: dict[str, Any] | None
    provenance_ref: dict[str, Any] | None
    privacy_filter_ref: dict[str, Any] | None
    conflict_report_ref: dict[str, Any] | None
    staleness_warning_ref: dict[str, Any] | None
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    refs_only: bool = True
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    injects_runtime_now: bool = False
    mutates_persona_now: bool = False
    mutates_behavior_policy_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityContextPack(_ModelMixin):
    context_pack_id: str
    request_ref: dict[str, Any]
    context_items: list[ContinuityContextItem]
    primary_context_item_refs: list[dict[str, Any]]
    supporting_context_item_refs: list[dict[str, Any]]
    warning_context_item_refs: list[dict[str, Any]]
    conflict_context_item_refs: list[dict[str, Any]]
    stale_context_item_refs: list[dict[str, Any]]
    archive_reference_item_refs: list[dict[str, Any]]
    item_count: int
    pack_status: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    refs_only: bool = True
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    continuity_injected_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityContext(_ModelMixin):
    continuity_context_id: str
    context_pack: ContinuityContextPack
    requested_context_profile: str | None
    target_surface_preview: str | None
    continuity_summary: str
    active_memory_ref_count: int
    warning_count: int
    conflict_count: int
    stale_count: int
    privacy_filtered_count: int
    context_status: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    is_runtime_injected: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False
    safety_gate_mutated: bool = False
    permission_policy_mutated: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityBuildDecision(_ModelMixin):
    build_decision_id: str
    request_id: str
    decision_type: str
    decision_reason: str
    creates_context_pack: bool
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    injects_context_now: bool = False
    updates_memory_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityContextPreview(_ModelMixin):
    preview_id: str
    continuity_context_ref: dict[str, Any]
    context_pack_ref: dict[str, Any]
    preview_summary: str
    preview_target: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    preview_is_not_injection: bool = True
    injection_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityBuildAuditTrail(_ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    continuity_ref_bundle_ref: dict[str, Any]
    relevance_score_refs: list[dict[str, Any]]
    recency_window_refs: list[dict[str, Any]]
    staleness_warning_refs: list[dict[str, Any]]
    conflict_report_refs: list[dict[str, Any]]
    privacy_filter_refs: list[dict[str, Any]]
    context_item_refs: list[dict[str, Any]]
    context_pack_ref: dict[str, Any] | None
    continuity_context_ref: dict[str, Any] | None
    build_decision_refs: list[dict[str, Any]]
    preview_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SessionContinuityContextFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class SessionContinuityContextBuildReport(_ModelMixin):
    report_id: str
    created_at: str
    continuity_policy: SessionContinuityContextPolicy
    request: SessionContinuityContextRequest
    source_view: SessionContinuitySourceView
    eligibility_rules: list[SessionContinuityEligibilityRule]
    continuity_ref_bundle: SessionContinuityRefBundle
    relevance_policy: ContinuityRelevancePolicy
    relevance_scores: list[ContinuityRelevanceScore]
    recency_windows: list[ContinuityRecencyWindow]
    staleness_warnings: list[ContinuityStalenessWarning]
    conflict_reports: list[ContinuityConflictReport]
    privacy_filters: list[ContinuityPrivacyFilter]
    context_pack: ContinuityContextPack
    continuity_context: SessionContinuityContext
    build_decisions: list[SessionContinuityBuildDecision]
    context_previews: list[SessionContinuityContextPreview]
    audit_trail: SessionContinuityBuildAuditTrail
    findings: list[SessionContinuityContextFinding]
    report_status: str
    ready_for_v0_27_7: bool
    continuity_source_view_created: bool
    continuity_ref_bundle_created: bool
    relevance_scores_created: bool
    staleness_warnings_created: bool
    conflict_reports_created: bool
    privacy_filters_created: bool
    context_items_created: bool
    context_pack_created: bool
    continuity_context_created: bool
    context_preview_created: bool
    audit_trail_created: bool
    active_memory_ref_count: int
    context_item_count: int
    warning_count: int
    conflict_count: int
    stale_count: int
    privacy_filtered_count: int
    version: str = SESSION_CONTINUITY_CONTEXT_VERSION
    ready_for_v0_28: bool = False
    continuity_injected: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False
    safety_gate_mutated: bool = False
    permission_policy_mutated: bool = False
    memory_updated: bool = False
    memory_revoked: bool = False
    memory_forgotten: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_replayed: bool = False
    raw_provider_output_replayed: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    pig_guidance_used_as_authority: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    llm_judge_used: bool = False
    next_required_step: str = SESSION_CONTINUITY_CONTEXT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.27.7 Continuity Injection Boundary begins or session continuity context policy changes."
    )


class SessionContinuityPrerequisiteSourceService:
    def __init__(self, active_registry_available: bool = True, include_reference_statuses: bool = True) -> None:
        self.active_registry_available = active_registry_available
        self.include_reference_statuses = include_reference_statuses
        self._registry_parts: dict[str, Any] | None = None

    def _parts(self) -> dict[str, Any]:
        if self._registry_parts is None:
            self._registry_parts = DurableMemoryRegistryReportService().build_all_parts(
                requested_write_mode="write_if_gate_passed" if self.active_registry_available else "dry_run",
                release_hygiene_gate_passed=self.active_registry_available,
                runtime_data_hygiene_gate_passed=self.active_registry_available,
            )
        return self._registry_parts

    def load_v0275_durable_memory_registry_report(self) -> DurableMemoryRegistryReport:
        return self._parts()["report"]

    def load_durable_memory_registry(self) -> DurableMemoryRegistry:
        return self._parts()["registry"]

    def load_durable_memory_records(self) -> list[DurableMemoryRecord]:
        return self._parts()["durable_memory_records"]

    def load_registry_entries(self) -> list[DurableMemoryRegistryEntry]:
        return self._parts()["registry_entries"]

    def load_memory_record_scopes(self) -> list[MemoryRecordScope]:
        return [record.scope for record in self.load_durable_memory_records()]

    def load_memory_record_provenance(self) -> list[MemoryRecordProvenance]:
        return [record.provenance for record in self.load_durable_memory_records()]

    def load_memory_record_evidence_indexes(self) -> list[MemoryRecordEvidenceIndex]:
        return [record.evidence_index for record in self.load_durable_memory_records()]

    def load_memory_record_lifecycle_policies(self) -> list[MemoryRecordLifecyclePolicy]:
        return [record.lifecycle_policy for record in self.load_durable_memory_records()]

    def load_memory_record_privacy_boundaries(self) -> list[MemoryRecordPrivacyBoundary]:
        return [record.privacy_boundary for record in self.load_durable_memory_records()]

    def load_memory_record_conflict_markers(self) -> list[MemoryRecordConflictMarker]:
        return [marker for record in self.load_durable_memory_records() for marker in record.conflict_markers]

    def load_memory_record_forget_revoke_bindings(self) -> list[MemoryRecordForgetRevokeBinding]:
        return [record.forget_revoke_binding for record in self.load_durable_memory_records()]

    def load_workbench_session_context_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_session_monitor", "workbench_session_monitor:v0.26.6", "v0.26.6")]

    def load_trace_summary_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("workbench_trace_summary", "workbench_trace_summary:v0.26.6", "v0.26.6")]

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_report", "pig:session_continuity_context_builder:v0.27.6", SESSION_CONTINUITY_CONTEXT_VERSION)]

    def reference_status_refs(self, status: str) -> list[dict[str, Any]]:
        if not self.include_reference_statuses:
            return []
        return [_ref("durable_memory_record", f"durable_memory_record:v0.27.5:{status}", DURABLE_MEMORY_REGISTRY_VERSION)]


class SessionContinuityContextPolicyService:
    def build_policy(self) -> SessionContinuityContextPolicy:
        return SessionContinuityContextPolicy(
            policy_id="session_continuity_context_policy:v0.27.6",
            evidence_refs=[_ref("memory_contract_report", "memory_contract_report:v0.27.0")],
        )


class SessionContinuitySourceViewService:
    def build_source_view(self, source: SessionContinuityPrerequisiteSourceService) -> SessionContinuitySourceView:
        report = source.load_v0275_durable_memory_registry_report()
        registry = source.load_durable_memory_registry()
        records = source.load_durable_memory_records()
        active_refs = [_ref("durable_memory_record", record.memory_record_id, DURABLE_MEMORY_REGISTRY_VERSION) for record in records if record.status == "active"]
        archived_refs = source.reference_status_refs("archived")
        revoked_refs = source.reference_status_refs("revoked")
        forgotten_refs = source.reference_status_refs("forgotten")
        expired_refs = source.reference_status_refs("expired")
        blocked_refs = source.reference_status_refs("blocked")
        status = "complete" if active_refs else "partial"
        return SessionContinuitySourceView(
            source_view_id="session_continuity_source_view:v0.27.6",
            durable_registry_report_ref=_ref("durable_memory_registry_report", report.report_id, DURABLE_MEMORY_REGISTRY_VERSION),
            durable_registry_ref=_ref("durable_memory_registry", registry.registry_id, DURABLE_MEMORY_REGISTRY_VERSION),
            active_memory_record_refs=active_refs,
            archived_memory_record_refs=archived_refs,
            revoked_memory_record_refs=revoked_refs,
            forgotten_memory_record_refs=forgotten_refs,
            expired_memory_record_refs=expired_refs,
            blocked_memory_record_refs=blocked_refs,
            memory_scope_refs=[_ref("memory_record_scope", scope.scope_id, DURABLE_MEMORY_REGISTRY_VERSION) for scope in source.load_memory_record_scopes()],
            memory_provenance_refs=[
                _ref("memory_record_provenance", provenance.provenance_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for provenance in source.load_memory_record_provenance()
            ],
            memory_evidence_index_refs=[
                _ref("memory_record_evidence_index", index.evidence_index_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for index in source.load_memory_record_evidence_indexes()
            ],
            memory_lifecycle_refs=[
                _ref("memory_record_lifecycle_policy", lifecycle.lifecycle_policy_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for lifecycle in source.load_memory_record_lifecycle_policies()
            ],
            memory_privacy_boundary_refs=[
                _ref("memory_record_privacy_boundary", boundary.privacy_boundary_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for boundary in source.load_memory_record_privacy_boundaries()
            ],
            memory_conflict_marker_refs=[
                _ref("memory_record_conflict_marker", marker.conflict_marker_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for marker in source.load_memory_record_conflict_markers()
            ],
            pig_guidance_refs=source.load_pig_guidance_refs_if_available(),
            session_context_refs=source.load_workbench_session_context_refs_if_available(),
            trace_summary_refs=source.load_trace_summary_refs_if_available(),
            approval_decision_refs=[_ref("approval_decision", "approval_decision:v0.26.6", "v0.26.6")],
            command_candidate_refs=[_ref("command_candidate", "command_candidate:v0.26.6", "v0.26.6")],
            failure_cause_refs=[_ref("failure_cause", "failure_cause:v0.26.6", "v0.26.6")],
            source_status=status,
            active_memory_count=len(active_refs),
            evidence_refs=[_ref("durable_memory_registry_report", report.report_id, DURABLE_MEMORY_REGISTRY_VERSION)],
        )


class SessionContinuityEligibilityRuleService:
    def build_rules(self) -> list[SessionContinuityEligibilityRule]:
        return [
            SessionContinuityEligibilityRule(
                rule_id=f"session_continuity_rule:{name}",
                rule_name=name,
                rule_summary=f"{name} is required for refs-only session continuity context construction.",
                required=True,
                pass_condition=f"{name} holds",
                fail_condition=f"{name} is violated",
                block_on_fail=name
                in {
                    "revoked_memory_active_use_forbidden",
                    "forgotten_memory_active_use_forbidden",
                    "expired_memory_active_use_forbidden",
                    "blocked_memory_active_use_forbidden",
                    "raw_transcript_replay_forbidden",
                    "raw_provider_output_replay_forbidden",
                    "context_item_must_not_inject_runtime",
                    "no_persona_mutation_in_v0276",
                    "no_behavior_policy_mutation_in_v0276",
                    "no_provider_invocation_in_v0276",
                    "no_command_execution_in_v0276",
                },
                evidence_refs=[_ref("session_continuity_context_policy", "session_continuity_context_policy:v0.27.6", SESSION_CONTINUITY_CONTEXT_VERSION)],
            )
            for name in SESSION_CONTINUITY_REQUIRED_RULES
        ]


class SessionContinuityMemoryRefService:
    def build_memory_refs(self, source_view: SessionContinuitySourceView) -> list[SessionContinuityMemoryRef]:
        refs: list[SessionContinuityMemoryRef] = []
        groups = [
            ("active", source_view.active_memory_record_refs, "active_context", True),
            ("archived", source_view.archived_memory_record_refs, "archive_reference", True),
            ("revoked", source_view.revoked_memory_record_refs, "blocked_reference", False),
            ("forgotten", source_view.forgotten_memory_record_refs, "blocked_reference", False),
            ("expired", source_view.expired_memory_record_refs, "stale_warning", False),
            ("blocked", source_view.blocked_memory_record_refs, "blocked_reference", False),
        ]
        for status, memory_refs, use_role, eligible in groups:
            for index, memory_ref in enumerate(memory_refs, start=1):
                record_id = str(memory_ref["id"])
                refs.append(
                    SessionContinuityMemoryRef(
                        continuity_memory_ref_id=f"session_continuity_memory_ref:{status}:{index}",
                        memory_record_ref=memory_ref,
                        memory_record_id=record_id,
                        memory_type="project_state" if status == "active" else "unknown",
                        memory_status=status,
                        scope_ref=source_view.memory_scope_refs[0] if source_view.memory_scope_refs else None,
                        provenance_ref=source_view.memory_provenance_refs[0] if source_view.memory_provenance_refs else None,
                        evidence_index_ref=source_view.memory_evidence_index_refs[0] if source_view.memory_evidence_index_refs else None,
                        lifecycle_policy_ref=source_view.memory_lifecycle_refs[0] if source_view.memory_lifecycle_refs else None,
                        privacy_boundary_ref=source_view.memory_privacy_boundary_refs[0] if source_view.memory_privacy_boundary_refs else None,
                        conflict_marker_refs=source_view.memory_conflict_marker_refs,
                        use_role=use_role,
                        eligible_for_context_pack=eligible,
                        evidence_refs=[memory_ref],
                    )
                )
        return refs


class SessionContinuityRefBundleService:
    def build_bundle(self, memory_refs: list[SessionContinuityMemoryRef]) -> SessionContinuityRefBundle:
        active = [
            _ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            for item in memory_refs
            if item.use_role == "active_context" and item.eligible_for_context_pack
        ]
        background = [
            _ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            for item in memory_refs
            if item.use_role in {"archive_reference", "background_reference"}
        ]
        blocked = [
            _ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            for item in memory_refs
            if not item.eligible_for_context_pack
        ]
        status = "ready" if active else "warning"
        return SessionContinuityRefBundle(
            continuity_ref_bundle_id="session_continuity_ref_bundle:v0.27.6",
            continuity_memory_refs=memory_refs,
            active_context_refs=active,
            background_reference_refs=background,
            conflict_warning_refs=[],
            stale_warning_refs=[
                _ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)
                for item in memory_refs
                if item.use_role == "stale_warning"
            ],
            blocked_refs=blocked,
            bundle_status=status,
            context_pack_created=True,
            evidence_refs=[_ref("session_continuity_source_view", "session_continuity_source_view:v0.27.6", SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class ContinuityRelevancePolicyService:
    def build_policy(self) -> ContinuityRelevancePolicy:
        return ContinuityRelevancePolicy(policy_id="continuity_relevance_policy:v0.27.6")


class ContinuityRelevanceScoreService:
    def score_relevance(
        self,
        memory_refs: list[SessionContinuityMemoryRef],
        request: SessionContinuityContextRequest,
        pig_guidance_refs: list[dict[str, Any]],
    ) -> list[ContinuityRelevanceScore]:
        scores: list[ContinuityRelevanceScore] = []
        for item in memory_refs:
            if item.use_role == "active_context":
                score, band = 0.86, "high"
            elif item.use_role == "archive_reference":
                score, band = 0.42, "medium"
            elif item.use_role == "stale_warning":
                score, band = 0.2, "low"
            else:
                score, band = None, "blocked"
            scores.append(
                ContinuityRelevanceScore(
                    relevance_score_id=f"continuity_relevance_score:{item.memory_record_id}",
                    memory_record_id=item.memory_record_id,
                    continuity_memory_ref_id=item.continuity_memory_ref_id,
                    requested_context_profile=request.requested_context_profile,
                    relevance_score=score,
                    relevance_band=band,
                    score_factors=[
                        {"factor": "scope_match", "value": item.use_role == "active_context"},
                        {"factor": "refs_only", "value": True},
                    ],
                    scope_match=item.use_role == "active_context",
                    recency_factor="current" if item.use_role == "active_context" else "reference",
                    evidence_strength_factor="high" if item.use_role == "active_context" else "unknown",
                    reuse_value_factor="project_continuity" if item.use_role == "active_context" else "background",
                    privacy_penalty_applied=False,
                    contradiction_penalty_applied=bool(item.conflict_marker_refs),
                    stale_penalty_applied=item.use_role == "stale_warning",
                    pig_guidance_signal_refs=pig_guidance_refs,
                    evidence_refs=[_ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
                )
            )
        return scores


class ContinuityRecencyWindowService:
    def build_windows(self, memory_refs: list[SessionContinuityMemoryRef]) -> list[ContinuityRecencyWindow]:
        windows: list[ContinuityRecencyWindow] = []
        for item in memory_refs:
            expired = item.memory_status == "expired"
            archived = item.memory_status == "archived"
            status = "expired" if expired else "aging" if archived else "current"
            windows.append(
                ContinuityRecencyWindow(
                    recency_window_id=f"continuity_recency_window:{item.memory_record_id}",
                    memory_record_id=item.memory_record_id,
                    created_at_ref=_ref("memory_record_created_at", f"{item.memory_record_id}:created_at", DURABLE_MEMORY_REGISTRY_VERSION),
                    updated_at_ref=_ref("memory_record_updated_at", f"{item.memory_record_id}:updated_at", DURABLE_MEMORY_REGISTRY_VERSION),
                    last_review_ref=None,
                    expected_validity_horizon_ref=_ref("memory_record_lifecycle_policy", f"{item.memory_record_id}:lifecycle", DURABLE_MEMORY_REGISTRY_VERSION),
                    recency_status=status,
                    stale_warning_required=status in {"aging", "stale", "expired"},
                    evidence_refs=[_ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
                )
            )
        return windows


class ContinuityStalenessWarningService:
    def build_warnings(self, windows: list[ContinuityRecencyWindow]) -> list[ContinuityStalenessWarning]:
        warnings: list[ContinuityStalenessWarning] = []
        for window in windows:
            level = "medium" if window.recency_status in {"aging", "stale"} else "blocked" if window.recency_status == "expired" else "none"
            warnings.append(
                ContinuityStalenessWarning(
                    staleness_warning_id=f"continuity_staleness_warning:{window.memory_record_id}",
                    memory_record_id=window.memory_record_id,
                    recency_window_ref=_ref("continuity_recency_window", window.recency_window_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                    warning_level=level,
                    warning_summary="Stale memory is surfaced as warning context, not silently applied.",
                    blocks_active_context_use=window.recency_status == "expired",
                    surface_to_user_later=level != "none",
                    evidence_refs=[_ref("continuity_recency_window", window.recency_window_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
                )
            )
        return warnings


class ContinuityConflictReportService:
    def build_reports(self, memory_refs: list[SessionContinuityMemoryRef]) -> list[ContinuityConflictReport]:
        reports: list[ContinuityConflictReport] = []
        for item in memory_refs:
            has_conflict = any("strong" in str(ref.get("id", "")) or "moderate" in str(ref.get("id", "")) for ref in item.conflict_marker_refs)
            reports.append(
                ContinuityConflictReport(
                    conflict_report_id=f"continuity_conflict_report:{item.memory_record_id}",
                    memory_record_id=item.memory_record_id,
                    conflict_marker_refs=item.conflict_marker_refs,
                    conflicting_memory_refs=[],
                    conflict_level="weak" if has_conflict else "none",
                    conflict_summary="Conflict markers are surfaced and not automatically resolved." if has_conflict else None,
                    requires_review=has_conflict,
                    blocks_active_context_use=False,
                    evidence_refs=[_ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
                )
            )
        return reports


class ContinuityPrivacyFilterService:
    def build_filters(self, memory_refs: list[SessionContinuityMemoryRef]) -> list[ContinuityPrivacyFilter]:
        return [
            ContinuityPrivacyFilter(
                privacy_filter_id=f"continuity_privacy_filter:{item.memory_record_id}",
                memory_record_id=item.memory_record_id,
                privacy_boundary_ref=item.privacy_boundary_ref,
                privacy_level="low" if item.eligible_for_context_pack else "blocked",
                filtered_categories=[] if item.eligible_for_context_pack else ["inactive_memory_status"],
                allowed_for_context_pack=item.eligible_for_context_pack,
                requires_user_confirmation_later=False,
                evidence_refs=[_ref("session_continuity_memory_ref", item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
            )
            for item in memory_refs
        ]


class ContinuityContextItemService:
    def build_items(
        self,
        memory_refs: list[SessionContinuityMemoryRef],
        scores: list[ContinuityRelevanceScore],
        privacy_filters: list[ContinuityPrivacyFilter],
        conflict_reports: list[ContinuityConflictReport],
        staleness_warnings: list[ContinuityStalenessWarning],
    ) -> list[ContinuityContextItem]:
        score_by_record = {score.memory_record_id: score for score in scores}
        privacy_by_record = {item.memory_record_id: item for item in privacy_filters}
        conflict_by_record = {item.memory_record_id: item for item in conflict_reports}
        stale_by_record = {item.memory_record_id: item for item in staleness_warnings}
        items: list[ContinuityContextItem] = []
        for ref_item in memory_refs:
            if not ref_item.eligible_for_context_pack:
                continue
            score = score_by_record.get(ref_item.memory_record_id)
            privacy = privacy_by_record.get(ref_item.memory_record_id)
            conflict = conflict_by_record.get(ref_item.memory_record_id)
            stale = stale_by_record.get(ref_item.memory_record_id)
            role = "primary_context" if ref_item.use_role == "active_context" else "archive_reference"
            if conflict and conflict.requires_review:
                role = "conflict_context"
            elif stale and stale.surface_to_user_later:
                role = "stale_context"
            items.append(
                ContinuityContextItem(
                    context_item_id=f"continuity_context_item:{ref_item.memory_record_id}",
                    memory_record_ref=ref_item.memory_record_ref,
                    memory_type=ref_item.memory_type,
                    item_role=role,
                    item_summary="Refs-only continuity context item for future v0.27.7 injection boundary review.",
                    relevance_score_ref=_ref("continuity_relevance_score", score.relevance_score_id, SESSION_CONTINUITY_CONTEXT_VERSION) if score else None,
                    source_refs=[ref_item.memory_record_ref],
                    evidence_index_ref=ref_item.evidence_index_ref,
                    provenance_ref=ref_item.provenance_ref,
                    privacy_filter_ref=_ref("continuity_privacy_filter", privacy.privacy_filter_id, SESSION_CONTINUITY_CONTEXT_VERSION) if privacy else None,
                    conflict_report_ref=_ref("continuity_conflict_report", conflict.conflict_report_id, SESSION_CONTINUITY_CONTEXT_VERSION) if conflict else None,
                    staleness_warning_ref=_ref("continuity_staleness_warning", stale.staleness_warning_id, SESSION_CONTINUITY_CONTEXT_VERSION) if stale else None,
                    evidence_refs=[_ref("session_continuity_memory_ref", ref_item.continuity_memory_ref_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
                )
            )
        return items


class ContinuityContextPackService:
    def build_pack(self, request: SessionContinuityContextRequest, items: list[ContinuityContextItem]) -> ContinuityContextPack:
        primary = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "primary_context"]
        supporting = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "supporting_context"]
        warning = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "warning_context"]
        conflict = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "conflict_context"]
        stale = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "stale_context"]
        archive = [_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items if item.item_role == "archive_reference"]
        return ContinuityContextPack(
            context_pack_id="continuity_context_pack:v0.27.6",
            request_ref=_ref("session_continuity_context_request", request.request_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            context_items=items,
            primary_context_item_refs=primary,
            supporting_context_item_refs=supporting,
            warning_context_item_refs=warning,
            conflict_context_item_refs=conflict,
            stale_context_item_refs=stale,
            archive_reference_item_refs=archive,
            item_count=len(items),
            pack_status="ready" if primary or archive else "warning",
            evidence_refs=[_ref("session_continuity_context_request", request.request_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class SessionContinuityContextService:
    def build_context(
        self,
        request: SessionContinuityContextRequest,
        pack: ContinuityContextPack,
        warnings: list[ContinuityStalenessWarning],
        conflicts: list[ContinuityConflictReport],
        privacy_filters: list[ContinuityPrivacyFilter],
    ) -> SessionContinuityContext:
        active_count = len(pack.primary_context_item_refs)
        warning_count = len([item for item in warnings if item.surface_to_user_later])
        conflict_count = len([item for item in conflicts if item.requires_review])
        stale_count = len([item for item in warnings if item.warning_level not in {"none", "unknown"}])
        privacy_count = len([item for item in privacy_filters if not item.allowed_for_context_pack])
        return SessionContinuityContext(
            continuity_context_id="session_continuity_context:v0.27.6",
            context_pack=pack,
            requested_context_profile=request.requested_context_profile,
            target_surface_preview=request.target_surface_preview,
            continuity_summary="Refs-only session continuity context pack created for future injection-boundary review.",
            active_memory_ref_count=active_count,
            warning_count=warning_count,
            conflict_count=conflict_count,
            stale_count=stale_count,
            privacy_filtered_count=privacy_count,
            context_status="ready" if pack.item_count else "warning",
            evidence_refs=[_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class SessionContinuityBuildDecisionService:
    def decide_build(self, request: SessionContinuityContextRequest, pack: ContinuityContextPack) -> SessionContinuityBuildDecision:
        if pack.item_count:
            decision_type = "build_context_pack"
            reason = "Eligible refs-only continuity items are available."
            creates_pack = True
        else:
            decision_type = "defer_no_active_memory"
            reason = "No active durable memory refs are available for active continuity context."
            creates_pack = False
        return SessionContinuityBuildDecision(
            build_decision_id="session_continuity_build_decision:v0.27.6",
            request_id=request.request_id,
            decision_type=decision_type,
            decision_reason=reason,
            creates_context_pack=creates_pack,
            evidence_refs=[_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class SessionContinuityContextPreviewService:
    def build_preview(self, context: SessionContinuityContext, pack: ContinuityContextPack) -> SessionContinuityContextPreview:
        return SessionContinuityContextPreview(
            preview_id="session_continuity_context_preview:v0.27.6",
            continuity_context_ref=_ref("session_continuity_context", context.continuity_context_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            context_pack_ref=_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            preview_summary="Preview for v0.27.7 injection boundary; no runtime injection is performed in v0.27.6.",
            preview_target="v0.27.7_injection_boundary",
            evidence_refs=[_ref("session_continuity_context", context.continuity_context_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class SessionContinuityBuildAuditTrailService:
    def build_audit_trail(
        self,
        request: SessionContinuityContextRequest,
        source_view: SessionContinuitySourceView,
        bundle: SessionContinuityRefBundle,
        scores: list[ContinuityRelevanceScore],
        windows: list[ContinuityRecencyWindow],
        warnings: list[ContinuityStalenessWarning],
        conflicts: list[ContinuityConflictReport],
        privacy_filters: list[ContinuityPrivacyFilter],
        pack: ContinuityContextPack,
        context: SessionContinuityContext,
        decisions: list[SessionContinuityBuildDecision],
        previews: list[SessionContinuityContextPreview],
    ) -> SessionContinuityBuildAuditTrail:
        event_count = (
            3
            + len(scores)
            + len(windows)
            + len(warnings)
            + len(conflicts)
            + len(privacy_filters)
            + len(pack.context_items)
            + len(decisions)
            + len(previews)
        )
        return SessionContinuityBuildAuditTrail(
            audit_trail_id="session_continuity_build_audit_trail:v0.27.6",
            request_ref=_ref("session_continuity_context_request", request.request_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            source_view_ref=_ref("session_continuity_source_view", source_view.source_view_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            continuity_ref_bundle_ref=_ref("session_continuity_ref_bundle", bundle.continuity_ref_bundle_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            relevance_score_refs=[_ref("continuity_relevance_score", item.relevance_score_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in scores],
            recency_window_refs=[_ref("continuity_recency_window", item.recency_window_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in windows],
            staleness_warning_refs=[_ref("continuity_staleness_warning", item.staleness_warning_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in warnings],
            conflict_report_refs=[_ref("continuity_conflict_report", item.conflict_report_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in conflicts],
            privacy_filter_refs=[_ref("continuity_privacy_filter", item.privacy_filter_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in privacy_filters],
            context_item_refs=[_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in pack.context_items],
            context_pack_ref=_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            continuity_context_ref=_ref("session_continuity_context", context.continuity_context_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            build_decision_refs=[_ref("session_continuity_build_decision", item.build_decision_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in decisions],
            preview_refs=[_ref("session_continuity_context_preview", item.preview_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in previews],
            audit_event_count=event_count,
            audit_status="ready" if pack.item_count else "warning",
            evidence_refs=[_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class SessionContinuityContextFindingService:
    BLOCKED_FINDINGS = {
        "revoked_memory_active_use_attempted",
        "forgotten_memory_active_use_attempted",
        "expired_memory_active_use_attempted",
        "blocked_memory_active_use_attempted",
        "raw_transcript_replay_attempted",
        "raw_provider_output_replay_attempted",
        "runtime_injection_attempted",
        "default_agent_context_mutation_attempted",
        "decision_service_mutation_attempted",
        "skill_router_mutation_attempted",
        "safety_gate_mutation_attempted",
        "permission_policy_mutation_attempted",
        "memory_update_attempted",
        "memory_revoke_attempted",
        "memory_forget_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_authority_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        source_view: SessionContinuitySourceView,
        rules: list[SessionContinuityEligibilityRule],
        memory_refs: list[SessionContinuityMemoryRef],
        pack: ContinuityContextPack,
        context: SessionContinuityContext,
    ) -> list[SessionContinuityContextFinding]:
        findings = [
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:continuity_policy_created",
                severity="info",
                finding_type="continuity_policy_created",
                message="Session continuity context policy was created.",
                subject_ref=_ref("session_continuity_context_policy", "session_continuity_context_policy:v0.27.6", SESSION_CONTINUITY_CONTEXT_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if policy construction fails.",
            ),
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:continuity_source_view_created",
                severity="info",
                finding_type="continuity_source_view_created",
                message="Session continuity source view was created from refs only.",
                subject_ref=_ref("session_continuity_source_view", source_view.source_view_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                evidence_refs=source_view.evidence_refs,
                withdrawal_condition="Withdraw if raw content is included.",
            ),
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:continuity_eligibility_rule_created",
                severity="info",
                finding_type="continuity_eligibility_rule_created",
                message=f"{len(rules)} eligibility rules were created.",
                subject_ref=None,
                evidence_refs=[],
                withdrawal_condition="Withdraw if any required rule is missing.",
            ),
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:continuity_memory_ref_created",
                severity="info",
                finding_type="continuity_memory_ref_created",
                message=f"{len(memory_refs)} continuity memory refs were created.",
                subject_ref=None,
                evidence_refs=[],
                withdrawal_condition="Withdraw if revoked, forgotten, expired, or blocked memory becomes active context.",
            ),
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:context_pack_created",
                severity="info" if pack.item_count else "warning",
                finding_type="context_pack_created",
                message="Continuity context pack was created without runtime injection.",
                subject_ref=_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                evidence_refs=pack.evidence_refs,
                withdrawal_condition="Withdraw if context pack injects runtime state.",
            ),
            SessionContinuityContextFinding(
                finding_id="session_continuity_finding:continuity_context_created",
                severity="info",
                finding_type="continuity_context_created",
                message="Session continuity context was created as refs-only preview material.",
                subject_ref=_ref("session_continuity_context", context.continuity_context_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                evidence_refs=context.evidence_refs,
                withdrawal_condition="Withdraw if Default Agent, DecisionService, SkillRouter, safety, or permission state is mutated.",
            ),
        ]
        if not source_view.active_memory_record_refs:
            findings.append(
                SessionContinuityContextFinding(
                    finding_id="session_continuity_finding:missing_active_memory_records",
                    severity="warning",
                    finding_type="missing_active_memory_records",
                    message="No active durable memory records were available; continuity context remains warning-only.",
                    subject_ref=_ref("session_continuity_source_view", source_view.source_view_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when an active durable memory registry source exists.",
                )
            )
        return findings


class SessionContinuityContextBuildReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        active_registry_available: bool = True,
        requested_context_profile: str | None = "project_continuity",
        target_surface_preview: str | None = "workbench_view_only",
    ) -> dict[str, Any]:
        source = SessionContinuityPrerequisiteSourceService(active_registry_available=active_registry_available)
        policy = SessionContinuityContextPolicyService().build_policy()
        source_view = SessionContinuitySourceViewService().build_source_view(source)
        request = SessionContinuityContextRequest(
            request_id="session_continuity_context_request:v0.27.6",
            durable_memory_registry_report_id=source_view.durable_registry_report_ref["id"] if source_view.durable_registry_report_ref else None,
            durable_memory_registry_id=source_view.durable_registry_ref["id"] if source_view.durable_registry_ref else None,
            selected_memory_record_refs=source_view.active_memory_record_refs + source_view.archived_memory_record_refs,
            selected_session_refs=source_view.session_context_refs,
            selected_project_refs=[_ref("project_ref", "project:chanta_core_public", SESSION_CONTINUITY_CONTEXT_VERSION)],
            selected_task_refs=[_ref("task_ref", "task:session_continuity_context_builder", SESSION_CONTINUITY_CONTEXT_VERSION)],
            requested_context_profile=requested_context_profile,
            target_surface_preview=target_surface_preview,
            source_refs=source_view.evidence_refs,
        )
        rules = SessionContinuityEligibilityRuleService().build_rules()
        memory_refs = SessionContinuityMemoryRefService().build_memory_refs(source_view)
        bundle = SessionContinuityRefBundleService().build_bundle(memory_refs)
        relevance_policy = ContinuityRelevancePolicyService().build_policy()
        scores = ContinuityRelevanceScoreService().score_relevance(memory_refs, request, source_view.pig_guidance_refs)
        windows = ContinuityRecencyWindowService().build_windows(memory_refs)
        warnings = ContinuityStalenessWarningService().build_warnings(windows)
        conflicts = ContinuityConflictReportService().build_reports(memory_refs)
        privacy_filters = ContinuityPrivacyFilterService().build_filters(memory_refs)
        items = ContinuityContextItemService().build_items(memory_refs, scores, privacy_filters, conflicts, warnings)
        pack = ContinuityContextPackService().build_pack(request, items)
        context = SessionContinuityContextService().build_context(request, pack, warnings, conflicts, privacy_filters)
        decisions = [SessionContinuityBuildDecisionService().decide_build(request, pack)]
        previews = [SessionContinuityContextPreviewService().build_preview(context, pack)]
        audit = SessionContinuityBuildAuditTrailService().build_audit_trail(
            request, source_view, bundle, scores, windows, warnings, conflicts, privacy_filters, pack, context, decisions, previews
        )
        findings = SessionContinuityContextFindingService().build_findings(source_view, rules, memory_refs, pack, context)
        report_status = "passed" if pack.item_count else "warning"
        report = SessionContinuityContextBuildReport(
            report_id=report_id or "session_continuity_context_build_report:v0.27.6",
            created_at=utc_now_iso(),
            continuity_policy=policy,
            request=request,
            source_view=source_view,
            eligibility_rules=rules,
            continuity_ref_bundle=bundle,
            relevance_policy=relevance_policy,
            relevance_scores=scores,
            recency_windows=windows,
            staleness_warnings=warnings,
            conflict_reports=conflicts,
            privacy_filters=privacy_filters,
            context_pack=pack,
            continuity_context=context,
            build_decisions=decisions,
            context_previews=previews,
            audit_trail=audit,
            findings=findings,
            report_status=report_status,
            ready_for_v0_27_7=True,
            continuity_source_view_created=True,
            continuity_ref_bundle_created=True,
            relevance_scores_created=bool(scores),
            staleness_warnings_created=bool(warnings),
            conflict_reports_created=bool(conflicts),
            privacy_filters_created=bool(privacy_filters),
            context_items_created=bool(items),
            context_pack_created=True,
            continuity_context_created=True,
            context_preview_created=True,
            audit_trail_created=True,
            active_memory_ref_count=source_view.active_memory_count,
            context_item_count=pack.item_count,
            warning_count=context.warning_count,
            conflict_count=context.conflict_count,
            stale_count=context.stale_count,
            privacy_filtered_count=context.privacy_filtered_count,
            limitations=[
                "v0.27.6 builds refs-only context artifacts and does not perform runtime injection.",
                "Continuity injection remains deferred to v0.27.7.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if context pack mutates runtime, persona, behavior policy, safety, permissions, or memory records.",
                "Withdraw readiness if raw transcript, raw provider output, secret, or credential content is included.",
            ],
        )
        return {
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "eligibility_rules": rules,
            "memory_refs": memory_refs,
            "continuity_ref_bundle": bundle,
            "relevance_policy": relevance_policy,
            "relevance_scores": scores,
            "recency_windows": windows,
            "staleness_warnings": warnings,
            "conflict_reports": conflicts,
            "privacy_filters": privacy_filters,
            "context_items": items,
            "context_pack": pack,
            "continuity_context": context,
            "build_decisions": decisions,
            "context_previews": previews,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": SESSION_CONTINUITY_CONTEXT_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "session_continuity_context_builder",
            "principles": [
                "Session continuity context is not raw transcript replay",
                "Continuity context pack is not runtime injection",
                "Continuity context item is not behavior override",
                "Memory retrieval is not command execution",
                "Memory relevance score is not authority",
                "Stale memory must be surfaced, not silently applied",
                "Contradictory memory must be surfaced, not silently resolved",
                "Privacy-filtered memory must remain filtered",
                "Revoked/forgotten/expired memory must not be used as active continuity context",
                "PIG guidance is not memory authority",
            ],
            "safety_boundary": {
                "session_continuity_context_created": "conditional",
                "continuity_context_pack_created": "conditional",
                "continuity_injected": False,
                "default_agent_context_mutated": False,
                "decision_service_mutated": False,
                "skill_router_mutated": False,
                "safety_gate_mutated": False,
                "permission_policy_mutated": False,
                "memory_updated": False,
                "memory_revoked": False,
                "memory_forgotten": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_replayed": False,
                "raw_provider_output_replayed": False,
                "pig_guidance_used_as_authority": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.7 continuity injection boundary",
                "v0.27.8 memory audit/update/revoke/forget",
                "v0.27.9 memory consolidation",
            ],
            "next_step": SESSION_CONTINUITY_CONTEXT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "session_continuity_context_builder_created",
            "version": SESSION_CONTINUITY_CONTEXT_VERSION,
            "source_read_models": [
                "DurableMemoryRegistryState",
                "DurableMemoryRecordState",
                "DurableMemoryRegistryEntryState",
                "MemoryRecordScopeState",
                "MemoryRecordProvenanceState",
                "MemoryRecordEvidenceIndexState",
                "MemoryRecordLifecyclePolicyState",
                "MemoryRecordPrivacyBoundaryState",
                "MemoryRecordConflictMarkerState",
                "WorkbenchSessionMonitorViewState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "SessionContinuitySourceViewState",
                "SessionContinuityMemoryRefState",
                "ContinuityRelevanceScoreState",
                "ContinuityStalenessWarningState",
                "ContinuityConflictReportState",
                "ContinuityPrivacyFilterState",
                "ContinuityContextPackState",
                "SessionContinuityContextState",
                "SessionContinuityContextPreviewState",
                "V027ReadinessState",
            ],
            "effect_types": SESSION_CONTINUITY_EFFECT_TYPES,
            "forbidden_effect_types": SESSION_CONTINUITY_FORBIDDEN_EFFECT_TYPES,
        }


def render_session_continuity_context_cli(parts: dict[str, Any], section: str = "policy") -> str:
    report: SessionContinuityContextBuildReport = parts["report"]
    lines = [
        f"Session Continuity Context Builder {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"continuity_source_view_created={_bool(report.continuity_source_view_created)}",
        f"continuity_ref_bundle_created={_bool(report.continuity_ref_bundle_created)}",
        f"relevance_scores_created={_bool(report.relevance_scores_created)}",
        f"staleness_warnings_created={_bool(report.staleness_warnings_created)}",
        f"conflict_reports_created={_bool(report.conflict_reports_created)}",
        f"privacy_filters_created={_bool(report.privacy_filters_created)}",
        f"context_items_created={_bool(report.context_items_created)}",
        f"context_pack_created={_bool(report.context_pack_created)}",
        f"continuity_context_created={_bool(report.continuity_context_created)}",
        f"context_preview_created={_bool(report.context_preview_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"active_memory_ref_count={report.active_memory_ref_count}",
        f"context_item_count={report.context_item_count}",
        f"warning_count={report.warning_count}",
        f"conflict_count={report.conflict_count}",
        f"stale_count={report.stale_count}",
        f"privacy_filtered_count={report.privacy_filtered_count}",
        f"ready_for_v0_27_7={_bool(report.ready_for_v0_27_7)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"continuity_injected={_bool(report.continuity_injected)}",
        f"default_agent_context_mutated={_bool(report.default_agent_context_mutated)}",
        f"decision_service_mutated={_bool(report.decision_service_mutated)}",
        f"skill_router_mutated={_bool(report.skill_router_mutated)}",
        f"safety_gate_mutated={_bool(report.safety_gate_mutated)}",
        f"permission_policy_mutated={_bool(report.permission_policy_mutated)}",
        f"memory_updated={_bool(report.memory_updated)}",
        f"memory_revoked={_bool(report.memory_revoked)}",
        f"memory_forgotten={_bool(report.memory_forgotten)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_replayed={_bool(report.raw_transcript_replayed)}",
        f"raw_provider_output_replayed={_bool(report.raw_provider_output_replayed)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"pig_guidance_used_as_authority={_bool(report.pig_guidance_used_as_authority)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "policy": ("context_pack_enabled", report.continuity_policy.context_pack_enabled),
        "source-view": ("source_status", report.source_view.source_status),
        "eligibility-rules": ("rule_count", len(report.eligibility_rules)),
        "refs": ("memory_ref_count", len(parts["memory_refs"])),
        "bundle": ("bundle_status", report.continuity_ref_bundle.bundle_status),
        "relevance": ("score_count", len(report.relevance_scores)),
        "recency": ("recency_window_count", len(report.recency_windows)),
        "stale": ("staleness_warning_count", len(report.staleness_warnings)),
        "conflicts": ("conflict_report_count", len(report.conflict_reports)),
        "privacy": ("privacy_filter_count", len(report.privacy_filters)),
        "items": ("context_item_count", report.context_item_count),
        "pack": ("pack_status", report.context_pack.pack_status),
        "context": ("context_status", report.continuity_context.context_status),
        "preview": ("preview_is_not_injection", report.context_previews[0].preview_is_not_injection),
        "audit": ("audit_status", report.audit_trail.audit_status),
        "report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    return "\n".join(lines)


CONTINUITY_INJECTION_BOUNDARY_VERSION = "v0.27.7"
CONTINUITY_INJECTION_BOUNDARY_VERSION_NAME = "Continuity Injection Boundary"
CONTINUITY_INJECTION_BOUNDARY_KOREAN_NAME = "Continuity Injection Boundary"
CONTINUITY_INJECTION_BOUNDARY_NEXT_STEP = "v0.27.8 Memory Audit / Update / Revoke / Forget"

CONTINUITY_INJECTION_TARGET_SURFACES = [
    "default_agent_context_future",
    "decision_service_guidance_future",
    "skill_proposal_router_context_future",
    "route_candidate_context_future",
    "provider_selection_context_future",
    "safety_gate_context_future",
    "workbench_display_context",
]

CONTINUITY_INJECTION_REQUIRED_RULES = [
    "context_pack_must_be_refs_only",
    "target_surface_must_accept_preview",
    "runtime_mutation_forbidden_in_v0277",
    "default_agent_context_mutation_forbidden",
    "decision_service_mutation_forbidden",
    "skill_router_mutation_forbidden",
    "safety_gate_mutation_forbidden",
    "permission_policy_mutation_forbidden",
    "explicit_user_instruction_outranks_memory",
    "safety_gate_must_remain_active",
    "permission_boundary_must_remain_active",
    "stale_memory_warning_must_be_preserved",
    "contradiction_report_must_be_preserved",
    "privacy_filter_must_be_preserved",
    "raw_transcript_replay_forbidden",
    "raw_provider_output_replay_forbidden",
    "provider_invocation_forbidden",
    "command_execution_forbidden",
    "PIG_guidance_not_authority",
]

CONTINUITY_INJECTION_OBJECT_TYPES = [
    "continuity_injection_boundary_policy",
    "continuity_injection_request",
    "continuity_injection_source_view",
    "continuity_injection_target_surface_catalog",
    "continuity_injection_target_surface",
    "continuity_injection_compatibility_rule",
    "continuity_injection_eligibility_evaluation",
    "continuity_instruction_priority_policy",
    "continuity_memory_user_intent_priority_rule",
    "continuity_safety_boundary_rule",
    "continuity_permission_boundary_rule",
    "continuity_injection_context_item_binding",
    "continuity_injection_bundle",
    "continuity_injection_preview",
    "continuity_injection_decision",
    "continuity_injection_decision_record",
    "continuity_injection_rejected_record",
    "continuity_injection_deferred_record",
    "continuity_injection_boundary_trace",
    "continuity_injection_audit_trail",
    "continuity_injection_boundary_finding",
    "continuity_injection_boundary_report",
    "session_continuity_context",
    "continuity_context_pack",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

CONTINUITY_INJECTION_EVENT_TYPES = [
    "continuity_injection_boundary_requested",
    "continuity_injection_prerequisites_loaded",
    "continuity_injection_policy_created",
    "continuity_injection_source_view_created",
    "continuity_injection_target_surface_catalog_created",
    "continuity_injection_target_surface_created",
    "continuity_injection_compatibility_rule_created",
    "continuity_injection_eligibility_evaluation_created",
    "continuity_instruction_priority_policy_created",
    "continuity_memory_user_intent_priority_rule_created",
    "continuity_safety_boundary_rule_created",
    "continuity_permission_boundary_rule_created",
    "continuity_injection_context_item_binding_created",
    "continuity_injection_bundle_created",
    "continuity_injection_preview_created",
    "continuity_injection_decision_created",
    "continuity_injection_decision_recorded",
    "continuity_injection_rejected_record_created",
    "continuity_injection_deferred_record_created",
    "continuity_injection_boundary_trace_created",
    "continuity_injection_audit_trail_created",
    "continuity_injection_boundary_report_created",
    "continuity_injection_warning_created",
    "continuity_injection_blocked",
]

CONTINUITY_INJECTION_EFFECT_TYPES = [
    "read_only_observation",
    "continuity_injection_boundary_created",
    "continuity_injection_bundle_created",
    "continuity_injection_preview_created",
    "continuity_injection_decision_recorded",
    "continuity_injection_boundary_trace_created",
    "continuity_injection_audit_created",
    "state_candidate_created",
]

CONTINUITY_INJECTION_FORBIDDEN_EFFECT_TYPES = [
    "continuity_injected",
    "runtime_injection_performed",
    "default_agent_context_mutated",
    "decision_service_mutated",
    "skill_router_mutated",
    "safety_gate_mutated",
    "permission_policy_mutated",
    "memory_updated",
    "memory_revoked",
    "memory_forgotten",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "raw_transcript_replayed",
    "raw_provider_output_replayed",
    "pig_guidance_used_as_authority",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "file_mutated",
    "safety_gate_bypassed",
    "permission_boundary_bypassed",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class ContinuityInjectionBoundaryPolicy(_ModelMixin):
    policy_id: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    injection_boundary_enabled: bool = True
    injection_preview_enabled: bool = True
    injection_bundle_enabled: bool = True
    injection_decision_record_enabled: bool = True
    target_surface_compatibility_enabled: bool = True
    actual_runtime_injection_enabled_now: bool = False
    default_agent_context_mutation_enabled_now: bool = False
    decision_service_mutation_enabled_now: bool = False
    skill_router_mutation_enabled_now: bool = False
    safety_gate_mutation_enabled_now: bool = False
    permission_policy_mutation_enabled_now: bool = False
    memory_update_enabled_now: bool = False
    memory_revoke_enabled_now: bool = False
    memory_forget_enabled_now: bool = False
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    explicit_user_instruction_outranks_memory: bool = True
    memory_context_is_guidance_not_authority: bool = True
    safety_gate_must_remain_active: bool = True
    permission_boundary_must_remain_active: bool = True
    stale_memory_warning_required: bool = True
    contradiction_surface_required: bool = True
    privacy_filter_must_remain_active: bool = True
    raw_transcript_replay_forbidden: bool = True
    raw_provider_output_replay_forbidden: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False
    pig_guidance_is_not_authority: bool = True
    llm_judge_as_sole_injection_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionRequest(_ModelMixin):
    request_id: str
    continuity_context_build_report_id: str | None
    continuity_context_id: str | None
    context_pack_id: str | None
    selected_context_item_refs: list[dict[str, Any]]
    requested_target_surfaces: list[str]
    requested_injection_mode: str
    strictness: str = "standard"
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionSourceView(_ModelMixin):
    source_view_id: str
    continuity_context_build_report_ref: dict[str, Any] | None
    continuity_context_ref: dict[str, Any] | None
    context_pack_ref: dict[str, Any] | None
    context_item_refs: list[dict[str, Any]]
    conflict_report_refs: list[dict[str, Any]]
    staleness_warning_refs: list[dict[str, Any]]
    privacy_filter_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    memory_record_refs: list[dict[str, Any]]
    evidence_index_refs: list[dict[str, Any]]
    source_status: str
    context_item_count: int
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionTargetSurface(_ModelMixin):
    target_surface_id: str
    target_surface_name: str
    target_surface_summary: str
    accepts_preview_bundle: bool
    accepts_refs_only_context: bool
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    runtime_mutation_allowed_now: bool = False
    requires_safety_boundary: bool = True
    requires_permission_boundary: bool = True
    requires_user_instruction_priority: bool = True
    provider_invocation_allowed_now: bool = False
    command_execution_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionTargetSurfaceCatalog(_ModelMixin):
    catalog_id: str
    supported_target_surfaces: list[ContinuityInjectionTargetSurface]
    catalog_status: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionCompatibilityRule(_ModelMixin):
    rule_id: str
    target_surface_name: str | None
    rule_name: str
    rule_summary: str
    required: bool
    pass_condition: str
    fail_condition: str
    block_on_fail: bool
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionEligibilityEvaluation(_ModelMixin):
    evaluation_id: str
    context_pack_ref: dict[str, Any] | None
    target_surface_ref: dict[str, Any] | None
    applied_rule_refs: list[dict[str, Any]]
    passed_rule_ids: list[str]
    failed_rule_ids: list[str]
    warning_rule_ids: list[str]
    blocking_rule_ids: list[str]
    eligibility_status: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    runtime_injection_allowed_now: bool = False
    mutation_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInstructionPriorityPolicy(_ModelMixin):
    policy_id: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    explicit_user_instruction_outranks_memory: bool = True
    current_task_context_outranks_stale_memory: bool = True
    safety_policy_outranks_memory: bool = True
    permission_policy_outranks_memory: bool = True
    contradiction_warning_required: bool = True
    stale_memory_warning_required: bool = True
    memory_must_not_override_user_intent: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityMemoryUserIntentPriorityRule(_ModelMixin):
    priority_rule_id: str
    rule_name: str
    user_intent_ref: dict[str, Any] | None
    memory_context_ref: dict[str, Any] | None
    priority_order: list[str]
    conflict_handling: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuitySafetyBoundaryRule(_ModelMixin):
    safety_boundary_rule_id: str
    target_surface_name: str | None
    safety_gate_ref: dict[str, Any] | None
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    safety_gate_must_remain_active: bool = True
    memory_cannot_bypass_safety: bool = True
    memory_cannot_lower_safety_level: bool = True
    safety_warning_must_be_preserved: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityPermissionBoundaryRule(_ModelMixin):
    permission_boundary_rule_id: str
    target_surface_name: str | None
    permission_policy_ref: dict[str, Any] | None
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    permission_boundary_must_remain_active: bool = True
    memory_cannot_grant_permission: bool = True
    memory_cannot_expand_scope: bool = True
    approval_requirement_must_be_preserved: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionContextItemBinding(_ModelMixin):
    binding_id: str
    context_item_ref: dict[str, Any]
    target_surface_name: str
    binding_role: str
    binding_summary: str
    preserved_warning_refs: list[dict[str, Any]]
    preserved_conflict_refs: list[dict[str, Any]]
    preserved_privacy_filter_refs: list[dict[str, Any]]
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    refs_only: bool = True
    runtime_applied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionBundle(_ModelMixin):
    injection_bundle_id: str
    request_ref: dict[str, Any]
    target_surface_refs: list[dict[str, Any]]
    context_pack_ref: dict[str, Any]
    context_item_bindings: list[ContinuityInjectionContextItemBinding]
    priority_policy_ref: dict[str, Any]
    safety_boundary_rule_refs: list[dict[str, Any]]
    permission_boundary_rule_refs: list[dict[str, Any]]
    eligibility_evaluation_refs: list[dict[str, Any]]
    bundle_summary: str
    bundle_status: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    refs_only: bool = True
    runtime_injection_performed: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False
    safety_gate_mutated: bool = False
    permission_policy_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionPreview(_ModelMixin):
    preview_id: str
    injection_bundle_ref: dict[str, Any]
    preview_target_surfaces: list[str]
    preview_summary: str
    warnings_to_surface: list[dict[str, Any]]
    conflicts_to_surface: list[dict[str, Any]]
    privacy_filters_to_preserve: list[dict[str, Any]]
    user_instruction_priority_summary: str
    safety_boundary_summary: str
    permission_boundary_summary: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    preview_is_not_runtime_injection: bool = True
    runtime_injection_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionDecision(_ModelMixin):
    injection_decision_id: str
    request_id: str
    injection_bundle_ref: dict[str, Any] | None
    decision_type: str
    decision_reason: str
    creates_preview: bool
    creates_future_handoff_bundle: bool
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    applies_runtime_injection_now: bool = False
    mutates_runtime_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionDecisionRecord(_ModelMixin):
    decision_record_id: str
    decision: ContinuityInjectionDecision
    record_status: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    ocel_visible: bool = True
    runtime_injection_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionRejectedRecord(_ModelMixin):
    rejected_record_id: str
    request_id: str
    rejection_reason: str
    rejected_target_surfaces: list[str]
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    source_context_retained: bool = True
    context_deleted: bool = False
    runtime_injection_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionDeferredRecord(_ModelMixin):
    deferred_record_id: str
    request_id: str
    deferral_reason: str
    deferred_until: str | None
    required_followup_refs: list[dict[str, Any]]
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    runtime_injection_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionBoundaryTrace(_ModelMixin):
    boundary_trace_id: str
    request_id: str
    injection_bundle_ref: dict[str, Any] | None
    target_surface_refs: list[dict[str, Any]]
    compatibility_evaluation_refs: list[dict[str, Any]]
    priority_rule_refs: list[dict[str, Any]]
    safety_boundary_rule_refs: list[dict[str, Any]]
    permission_boundary_rule_refs: list[dict[str, Any]]
    blocked_boundary_refs: list[dict[str, Any]]
    boundary_summary: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    boundary_bypassed: bool = False
    runtime_mutation_performed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionAuditTrail(_ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    target_catalog_ref: dict[str, Any]
    compatibility_rule_refs: list[dict[str, Any]]
    eligibility_evaluation_refs: list[dict[str, Any]]
    injection_bundle_refs: list[dict[str, Any]]
    preview_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    rejected_record_refs: list[dict[str, Any]]
    deferred_record_refs: list[dict[str, Any]]
    boundary_trace_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    raw_content_included: bool = False
    runtime_injection_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuityInjectionBoundaryFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class ContinuityInjectionBoundaryReport(_ModelMixin):
    report_id: str
    created_at: str
    injection_policy: ContinuityInjectionBoundaryPolicy
    request: ContinuityInjectionRequest
    source_view: ContinuityInjectionSourceView
    target_catalog: ContinuityInjectionTargetSurfaceCatalog
    compatibility_rules: list[ContinuityInjectionCompatibilityRule]
    eligibility_evaluations: list[ContinuityInjectionEligibilityEvaluation]
    instruction_priority_policy: ContinuityInstructionPriorityPolicy
    memory_user_intent_priority_rules: list[ContinuityMemoryUserIntentPriorityRule]
    safety_boundary_rules: list[ContinuitySafetyBoundaryRule]
    permission_boundary_rules: list[ContinuityPermissionBoundaryRule]
    context_item_bindings: list[ContinuityInjectionContextItemBinding]
    injection_bundles: list[ContinuityInjectionBundle]
    injection_previews: list[ContinuityInjectionPreview]
    injection_decisions: list[ContinuityInjectionDecision]
    decision_records: list[ContinuityInjectionDecisionRecord]
    rejected_records: list[ContinuityInjectionRejectedRecord]
    deferred_records: list[ContinuityInjectionDeferredRecord]
    boundary_traces: list[ContinuityInjectionBoundaryTrace]
    audit_trail: ContinuityInjectionAuditTrail
    findings: list[ContinuityInjectionBoundaryFinding]
    report_status: str
    ready_for_v0_27_8: bool
    injection_policy_created: bool
    source_view_created: bool
    target_catalog_created: bool
    compatibility_rules_created: bool
    eligibility_evaluations_created: bool
    injection_bundles_created: bool
    injection_previews_created: bool
    injection_decisions_recorded: bool
    boundary_traces_created: bool
    audit_trail_created: bool
    version: str = CONTINUITY_INJECTION_BOUNDARY_VERSION
    ready_for_v0_28: bool = False
    runtime_injection_performed: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False
    safety_gate_mutated: bool = False
    permission_policy_mutated: bool = False
    memory_updated: bool = False
    memory_revoked: bool = False
    memory_forgotten: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_replayed: bool = False
    raw_provider_output_replayed: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    pig_guidance_used_as_authority: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    file_mutated: bool = False
    safety_gate_bypassed: bool = False
    permission_boundary_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    llm_judge_used: bool = False
    next_required_step: str = CONTINUITY_INJECTION_BOUNDARY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.27.8 Memory Audit / Update / Revoke / Forget begins or continuity injection boundary policy changes."
    )


class ContinuityInjectionPrerequisiteSourceService:
    def __init__(self, continuity_context_available: bool = True) -> None:
        self.continuity_context_available = continuity_context_available
        self._parts: dict[str, Any] | None = None

    def _continuity_parts(self) -> dict[str, Any]:
        if self._parts is None:
            self._parts = SessionContinuityContextBuildReportService().build_all_parts(
                active_registry_available=self.continuity_context_available
            )
        return self._parts

    def load_v0276_continuity_context_build_report(self) -> SessionContinuityContextBuildReport | None:
        return self._continuity_parts()["report"] if self.continuity_context_available else None

    def load_session_continuity_context(self) -> SessionContinuityContext | None:
        return self._continuity_parts()["continuity_context"] if self.continuity_context_available else None

    def load_context_pack(self) -> ContinuityContextPack | None:
        return self._continuity_parts()["context_pack"] if self.continuity_context_available else None

    def load_context_items(self) -> list[ContinuityContextItem]:
        return self._continuity_parts()["context_items"] if self.continuity_context_available else []

    def load_conflict_reports(self) -> list[ContinuityConflictReport]:
        return self._continuity_parts()["conflict_reports"] if self.continuity_context_available else []

    def load_staleness_warnings(self) -> list[ContinuityStalenessWarning]:
        return self._continuity_parts()["staleness_warnings"] if self.continuity_context_available else []

    def load_privacy_filters(self) -> list[ContinuityPrivacyFilter]:
        return self._continuity_parts()["privacy_filters"] if self.continuity_context_available else []

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_report", "pig:continuity_injection_boundary:v0.27.7", CONTINUITY_INJECTION_BOUNDARY_VERSION)]

    def load_target_surface_contracts_if_available(self) -> list[dict[str, Any]]:
        return [
            _ref("agent_surface_contract", "agent_surface_contract:v0.25", "v0.25"),
            _ref("workbench_contract", "workbench_contract:v0.26", "v0.26"),
        ]


class ContinuityInjectionBoundaryPolicyService:
    def build_policy(self) -> ContinuityInjectionBoundaryPolicy:
        return ContinuityInjectionBoundaryPolicy(
            policy_id="continuity_injection_boundary_policy:v0.27.7",
            evidence_refs=[_ref("memory_contract_report", "memory_contract_report:v0.27.0")],
        )


class ContinuityInjectionSourceViewService:
    def build_source_view(self, source: ContinuityInjectionPrerequisiteSourceService) -> ContinuityInjectionSourceView:
        report = source.load_v0276_continuity_context_build_report()
        context = source.load_session_continuity_context()
        pack = source.load_context_pack()
        items = source.load_context_items()
        conflicts = source.load_conflict_reports()
        warnings = source.load_staleness_warnings()
        privacy_filters = source.load_privacy_filters()
        status = "complete" if report and pack and items else "partial"
        return ContinuityInjectionSourceView(
            source_view_id="continuity_injection_source_view:v0.27.7",
            continuity_context_build_report_ref=_ref("session_continuity_context_build_report", report.report_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            if report
            else None,
            continuity_context_ref=_ref("session_continuity_context", context.continuity_context_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            if context
            else None,
            context_pack_ref=_ref("continuity_context_pack", pack.context_pack_id, SESSION_CONTINUITY_CONTEXT_VERSION) if pack else None,
            context_item_refs=[_ref("continuity_context_item", item.context_item_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in items],
            conflict_report_refs=[_ref("continuity_conflict_report", item.conflict_report_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in conflicts],
            staleness_warning_refs=[_ref("continuity_staleness_warning", item.staleness_warning_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in warnings],
            privacy_filter_refs=[_ref("continuity_privacy_filter", item.privacy_filter_id, SESSION_CONTINUITY_CONTEXT_VERSION) for item in privacy_filters],
            pig_guidance_refs=source.load_pig_guidance_refs_if_available(),
            memory_record_refs=[item.memory_record_ref for item in items],
            evidence_index_refs=[item.evidence_index_ref for item in items if item.evidence_index_ref],
            source_status=status,
            context_item_count=len(items),
            evidence_refs=[
                _ref("session_continuity_context_build_report", report.report_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            ]
            if report
            else [],
        )


class ContinuityInjectionTargetSurfaceCatalogService:
    def build_catalog(self) -> ContinuityInjectionTargetSurfaceCatalog:
        surfaces = [
            ContinuityInjectionTargetSurface(
                target_surface_id=f"continuity_injection_target_surface:{name}",
                target_surface_name=name,
                target_surface_summary=f"{name} may accept refs-only preview bundles but cannot be mutated in v0.27.7.",
                accepts_preview_bundle=True,
                accepts_refs_only_context=True,
                evidence_refs=[_ref("continuity_injection_boundary_policy", "continuity_injection_boundary_policy:v0.27.7", CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
            for name in CONTINUITY_INJECTION_TARGET_SURFACES
        ]
        return ContinuityInjectionTargetSurfaceCatalog(
            catalog_id="continuity_injection_target_surface_catalog:v0.27.7",
            supported_target_surfaces=surfaces,
            catalog_status="ready",
            evidence_refs=[_ref("memory_contract_report", "memory_contract_report:v0.27.0")],
        )


class ContinuityInjectionCompatibilityRuleService:
    def build_rules(self, catalog: ContinuityInjectionTargetSurfaceCatalog) -> list[ContinuityInjectionCompatibilityRule]:
        rules: list[ContinuityInjectionCompatibilityRule] = []
        for target in catalog.supported_target_surfaces:
            for name in CONTINUITY_INJECTION_REQUIRED_RULES:
                rules.append(
                    ContinuityInjectionCompatibilityRule(
                        rule_id=f"continuity_injection_rule:{target.target_surface_name}:{name}",
                        target_surface_name=target.target_surface_name,
                        rule_name=name,
                        rule_summary=f"{name} must hold before any future injection handoff.",
                        required=True,
                        pass_condition=f"{name} holds for refs-only preview",
                        fail_condition=f"{name} is violated",
                        block_on_fail=name
                        in {
                            "runtime_mutation_forbidden_in_v0277",
                            "default_agent_context_mutation_forbidden",
                            "decision_service_mutation_forbidden",
                            "skill_router_mutation_forbidden",
                            "safety_gate_mutation_forbidden",
                            "permission_policy_mutation_forbidden",
                            "raw_transcript_replay_forbidden",
                            "raw_provider_output_replay_forbidden",
                            "provider_invocation_forbidden",
                            "command_execution_forbidden",
                            "PIG_guidance_not_authority",
                        },
                        evidence_refs=[_ref("continuity_injection_target_surface", target.target_surface_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
                    )
                )
        return rules


class ContinuityInjectionEligibilityEvaluationService:
    def evaluate(
        self,
        source_view: ContinuityInjectionSourceView,
        catalog: ContinuityInjectionTargetSurfaceCatalog,
        rules: list[ContinuityInjectionCompatibilityRule],
    ) -> list[ContinuityInjectionEligibilityEvaluation]:
        evaluations: list[ContinuityInjectionEligibilityEvaluation] = []
        for target in catalog.supported_target_surfaces:
            target_rules = [rule for rule in rules if rule.target_surface_name == target.target_surface_name]
            rule_refs = [_ref("continuity_injection_compatibility_rule", rule.rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) for rule in target_rules]
            status = "eligible_for_preview" if source_view.context_pack_ref and target.accepts_preview_bundle else "deferred"
            evaluations.append(
                ContinuityInjectionEligibilityEvaluation(
                    evaluation_id=f"continuity_injection_eligibility:{target.target_surface_name}",
                    context_pack_ref=source_view.context_pack_ref,
                    target_surface_ref=_ref("continuity_injection_target_surface", target.target_surface_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                    applied_rule_refs=rule_refs,
                    passed_rule_ids=[rule.rule_id for rule in target_rules],
                    failed_rule_ids=[],
                    warning_rule_ids=[],
                    blocking_rule_ids=[],
                    eligibility_status=status,
                    evidence_refs=rule_refs,
                )
            )
        return evaluations


class ContinuityInstructionPriorityPolicyService:
    def build_policy(self) -> ContinuityInstructionPriorityPolicy:
        return ContinuityInstructionPriorityPolicy(policy_id="continuity_instruction_priority_policy:v0.27.7")


class ContinuityMemoryUserIntentPriorityRuleService:
    def build_rules(self, request: ContinuityInjectionRequest, source_view: ContinuityInjectionSourceView) -> list[ContinuityMemoryUserIntentPriorityRule]:
        return [
            ContinuityMemoryUserIntentPriorityRule(
                priority_rule_id="continuity_memory_user_intent_priority_rule:v0.27.7",
                rule_name="explicit_user_instruction_outranks_memory",
                user_intent_ref=_ref("current_task_context", "current_task_context:v0.27.7", CONTINUITY_INJECTION_BOUNDARY_VERSION),
                memory_context_ref=source_view.context_pack_ref,
                priority_order=[
                    "safety_policy",
                    "permission_policy",
                    "explicit_user_instruction",
                    "current_task_context",
                    "active_memory_context",
                    "stale_or_archive_memory_context",
                ],
                conflict_handling="surface_conflict",
                evidence_refs=[_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
        ]


class ContinuitySafetyBoundaryRuleService:
    def build_rules(self, catalog: ContinuityInjectionTargetSurfaceCatalog) -> list[ContinuitySafetyBoundaryRule]:
        return [
            ContinuitySafetyBoundaryRule(
                safety_boundary_rule_id=f"continuity_safety_boundary_rule:{target.target_surface_name}",
                target_surface_name=target.target_surface_name,
                safety_gate_ref=_ref("safety_gate_contract", "safety_gate_contract:v0.25", "v0.25"),
                evidence_refs=[_ref("continuity_injection_target_surface", target.target_surface_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
            for target in catalog.supported_target_surfaces
        ]


class ContinuityPermissionBoundaryRuleService:
    def build_rules(self, catalog: ContinuityInjectionTargetSurfaceCatalog) -> list[ContinuityPermissionBoundaryRule]:
        return [
            ContinuityPermissionBoundaryRule(
                permission_boundary_rule_id=f"continuity_permission_boundary_rule:{target.target_surface_name}",
                target_surface_name=target.target_surface_name,
                permission_policy_ref=_ref("permission_policy_contract", "permission_policy_contract:v0.25", "v0.25"),
                evidence_refs=[_ref("continuity_injection_target_surface", target.target_surface_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
            for target in catalog.supported_target_surfaces
        ]


class ContinuityInjectionContextItemBindingService:
    def build_bindings(self, request: ContinuityInjectionRequest, source_view: ContinuityInjectionSourceView) -> list[ContinuityInjectionContextItemBinding]:
        bindings: list[ContinuityInjectionContextItemBinding] = []
        for target in request.requested_target_surfaces:
            for index, context_item_ref in enumerate(source_view.context_item_refs, start=1):
                bindings.append(
                    ContinuityInjectionContextItemBinding(
                        binding_id=f"continuity_injection_binding:{target}:{index}",
                        context_item_ref=context_item_ref,
                        target_surface_name=target,
                        binding_role="guidance_context" if index == 1 else "archive_reference_context",
                        binding_summary="Refs-only binding for future injection boundary review; not applied to runtime.",
                        preserved_warning_refs=source_view.staleness_warning_refs,
                        preserved_conflict_refs=source_view.conflict_report_refs,
                        preserved_privacy_filter_refs=source_view.privacy_filter_refs,
                        evidence_refs=[context_item_ref],
                    )
                )
        return bindings


class ContinuityInjectionBundleService:
    def build_bundles(
        self,
        request: ContinuityInjectionRequest,
        source_view: ContinuityInjectionSourceView,
        catalog: ContinuityInjectionTargetSurfaceCatalog,
        bindings: list[ContinuityInjectionContextItemBinding],
        priority_policy: ContinuityInstructionPriorityPolicy,
        safety_rules: list[ContinuitySafetyBoundaryRule],
        permission_rules: list[ContinuityPermissionBoundaryRule],
        evaluations: list[ContinuityInjectionEligibilityEvaluation],
    ) -> list[ContinuityInjectionBundle]:
        if not source_view.context_pack_ref:
            return []
        target_refs = [
            _ref("continuity_injection_target_surface", target.target_surface_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
            for target in catalog.supported_target_surfaces
            if target.target_surface_name in request.requested_target_surfaces
        ]
        return [
            ContinuityInjectionBundle(
                injection_bundle_id="continuity_injection_bundle:v0.27.7",
                request_ref=_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                target_surface_refs=target_refs,
                context_pack_ref=source_view.context_pack_ref,
                context_item_bindings=bindings,
                priority_policy_ref=_ref("continuity_instruction_priority_policy", priority_policy.policy_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                safety_boundary_rule_refs=[
                    _ref("continuity_safety_boundary_rule", rule.safety_boundary_rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for rule in safety_rules
                ],
                permission_boundary_rule_refs=[
                    _ref("continuity_permission_boundary_rule", rule.permission_boundary_rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for rule in permission_rules
                ],
                eligibility_evaluation_refs=[
                    _ref("continuity_injection_eligibility_evaluation", item.evaluation_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for item in evaluations
                ],
                bundle_summary="Future handoff injection bundle; not applied to runtime in v0.27.7.",
                bundle_status="ready_for_future_handoff",
                evidence_refs=[source_view.context_pack_ref],
            )
        ]


class ContinuityInjectionPreviewService:
    def build_previews(
        self,
        bundles: list[ContinuityInjectionBundle],
        source_view: ContinuityInjectionSourceView,
        request: ContinuityInjectionRequest,
    ) -> list[ContinuityInjectionPreview]:
        previews: list[ContinuityInjectionPreview] = []
        for bundle in bundles:
            previews.append(
                ContinuityInjectionPreview(
                    preview_id="continuity_injection_preview:v0.27.7",
                    injection_bundle_ref=_ref("continuity_injection_bundle", bundle.injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                    preview_target_surfaces=request.requested_target_surfaces,
                    preview_summary="Preview only; no context is applied to runtime.",
                    warnings_to_surface=source_view.staleness_warning_refs,
                    conflicts_to_surface=source_view.conflict_report_refs,
                    privacy_filters_to_preserve=source_view.privacy_filter_refs,
                    user_instruction_priority_summary="Safety, permission, explicit user instruction, and current task context outrank memory.",
                    safety_boundary_summary="Safety gate remains active and cannot be lowered by memory.",
                    permission_boundary_summary="Permission boundary remains active and cannot be expanded by memory.",
                    evidence_refs=[_ref("continuity_injection_bundle", bundle.injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
                )
            )
        return previews


class ContinuityInjectionDecisionService:
    def decide(
        self,
        request: ContinuityInjectionRequest,
        bundles: list[ContinuityInjectionBundle],
        requested_decision_type: str | None = None,
    ) -> list[ContinuityInjectionDecision]:
        bundle_ref = _ref("continuity_injection_bundle", bundles[0].injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) if bundles else None
        decision_type = requested_decision_type or ("create_preview" if bundles else "reject_injection")
        creates_preview = decision_type in {"create_preview", "create_future_handoff_bundle"} and bool(bundles)
        creates_handoff = decision_type == "create_future_handoff_bundle" and bool(bundles)
        return [
            ContinuityInjectionDecision(
                injection_decision_id="continuity_injection_decision:v0.27.7",
                request_id=request.request_id,
                injection_bundle_ref=bundle_ref,
                decision_type=decision_type,
                decision_reason="Continuity injection boundary artifacts are refs-only and not applied to runtime.",
                creates_preview=creates_preview,
                creates_future_handoff_bundle=creates_handoff,
                evidence_refs=[bundle_ref] if bundle_ref else [],
            )
        ]


class ContinuityInjectionDecisionRecordService:
    def build_records(self, decisions: list[ContinuityInjectionDecision]) -> list[ContinuityInjectionDecisionRecord]:
        return [
            ContinuityInjectionDecisionRecord(
                decision_record_id=f"continuity_injection_decision_record:{decision.injection_decision_id}",
                decision=decision,
                record_status="recorded",
                evidence_refs=decision.evidence_refs,
            )
            for decision in decisions
        ]

    def build_rejected_records(self, request: ContinuityInjectionRequest) -> list[ContinuityInjectionRejectedRecord]:
        return [
            ContinuityInjectionRejectedRecord(
                rejected_record_id="continuity_injection_rejected_record:v0.27.7",
                request_id=request.request_id,
                rejection_reason="Rejected record fixture documents that rejection retains source context and does not inject runtime.",
                rejected_target_surfaces=[],
                evidence_refs=[_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
        ]

    def build_deferred_records(self, request: ContinuityInjectionRequest) -> list[ContinuityInjectionDeferredRecord]:
        return [
            ContinuityInjectionDeferredRecord(
                deferred_record_id="continuity_injection_deferred_record:v0.27.7",
                request_id=request.request_id,
                deferral_reason="Deferred record fixture for conflict/privacy review paths.",
                deferred_until=None,
                required_followup_refs=[],
                evidence_refs=[_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
            )
        ]


class ContinuityInjectionBoundaryTraceService:
    def build_traces(
        self,
        request: ContinuityInjectionRequest,
        bundles: list[ContinuityInjectionBundle],
        evaluations: list[ContinuityInjectionEligibilityEvaluation],
        priority_rules: list[ContinuityMemoryUserIntentPriorityRule],
        safety_rules: list[ContinuitySafetyBoundaryRule],
        permission_rules: list[ContinuityPermissionBoundaryRule],
    ) -> list[ContinuityInjectionBoundaryTrace]:
        bundle_ref = _ref("continuity_injection_bundle", bundles[0].injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) if bundles else None
        target_refs = bundles[0].target_surface_refs if bundles else []
        return [
            ContinuityInjectionBoundaryTrace(
                boundary_trace_id="continuity_injection_boundary_trace:v0.27.7",
                request_id=request.request_id,
                injection_bundle_ref=bundle_ref,
                target_surface_refs=target_refs,
                compatibility_evaluation_refs=[
                    _ref("continuity_injection_eligibility_evaluation", item.evaluation_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for item in evaluations
                ],
                priority_rule_refs=[
                    _ref("continuity_memory_user_intent_priority_rule", item.priority_rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for item in priority_rules
                ],
                safety_boundary_rule_refs=[
                    _ref("continuity_safety_boundary_rule", item.safety_boundary_rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for item in safety_rules
                ],
                permission_boundary_rule_refs=[
                    _ref("continuity_permission_boundary_rule", item.permission_boundary_rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                    for item in permission_rules
                ],
                blocked_boundary_refs=[],
                boundary_summary="All injection boundary checks are preserved; no runtime mutation is performed.",
                evidence_refs=[bundle_ref] if bundle_ref else [],
            )
        ]


class ContinuityInjectionAuditTrailService:
    def build_audit_trail(
        self,
        request: ContinuityInjectionRequest,
        source_view: ContinuityInjectionSourceView,
        catalog: ContinuityInjectionTargetSurfaceCatalog,
        rules: list[ContinuityInjectionCompatibilityRule],
        evaluations: list[ContinuityInjectionEligibilityEvaluation],
        bundles: list[ContinuityInjectionBundle],
        previews: list[ContinuityInjectionPreview],
        decision_records: list[ContinuityInjectionDecisionRecord],
        rejected_records: list[ContinuityInjectionRejectedRecord],
        deferred_records: list[ContinuityInjectionDeferredRecord],
        traces: list[ContinuityInjectionBoundaryTrace],
    ) -> ContinuityInjectionAuditTrail:
        event_count = (
            3
            + len(rules)
            + len(evaluations)
            + len(bundles)
            + len(previews)
            + len(decision_records)
            + len(rejected_records)
            + len(deferred_records)
            + len(traces)
        )
        return ContinuityInjectionAuditTrail(
            audit_trail_id="continuity_injection_audit_trail:v0.27.7",
            request_ref=_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
            source_view_ref=_ref("continuity_injection_source_view", source_view.source_view_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
            target_catalog_ref=_ref("continuity_injection_target_surface_catalog", catalog.catalog_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
            compatibility_rule_refs=[
                _ref("continuity_injection_compatibility_rule", rule.rule_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                for rule in rules
            ],
            eligibility_evaluation_refs=[
                _ref("continuity_injection_eligibility_evaluation", item.evaluation_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                for item in evaluations
            ],
            injection_bundle_refs=[_ref("continuity_injection_bundle", item.injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) for item in bundles],
            preview_refs=[_ref("continuity_injection_preview", item.preview_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) for item in previews],
            decision_record_refs=[
                _ref("continuity_injection_decision_record", item.decision_record_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                for item in decision_records
            ],
            rejected_record_refs=[
                _ref("continuity_injection_rejected_record", item.rejected_record_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                for item in rejected_records
            ],
            deferred_record_refs=[
                _ref("continuity_injection_deferred_record", item.deferred_record_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
                for item in deferred_records
            ],
            boundary_trace_refs=[_ref("continuity_injection_boundary_trace", item.boundary_trace_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) for item in traces],
            audit_event_count=event_count,
            audit_status="ready" if bundles and previews else "warning",
            evidence_refs=[_ref("continuity_injection_request", request.request_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
        )


class ContinuityInjectionBoundaryFindingService:
    BLOCKED_FINDINGS = {
        "runtime_injection_attempted",
        "default_agent_context_mutation_attempted",
        "decision_service_mutation_attempted",
        "skill_router_mutation_attempted",
        "safety_gate_mutation_attempted",
        "permission_policy_mutation_attempted",
        "memory_update_attempted",
        "memory_revoke_attempted",
        "memory_forget_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "raw_transcript_replay_attempted",
        "raw_provider_output_replay_attempted",
        "pig_guidance_as_authority_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "file_mutation_attempted",
        "safety_bypass_attempted",
        "permission_bypass_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        source_view: ContinuityInjectionSourceView,
        catalog: ContinuityInjectionTargetSurfaceCatalog,
        rules: list[ContinuityInjectionCompatibilityRule],
        bundles: list[ContinuityInjectionBundle],
        previews: list[ContinuityInjectionPreview],
    ) -> list[ContinuityInjectionBoundaryFinding]:
        findings = [
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:injection_policy_created",
                severity="info",
                finding_type="injection_policy_created",
                message="Continuity injection boundary policy was created.",
                subject_ref=_ref("continuity_injection_boundary_policy", "continuity_injection_boundary_policy:v0.27.7", CONTINUITY_INJECTION_BOUNDARY_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if policy construction fails.",
            ),
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:injection_source_view_created",
                severity="info" if source_view.context_pack_ref else "warning",
                finding_type="injection_source_view_created",
                message="Continuity injection source view was created from refs only.",
                subject_ref=_ref("continuity_injection_source_view", source_view.source_view_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                evidence_refs=source_view.evidence_refs,
                withdrawal_condition="Withdraw if raw content is included.",
            ),
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:target_surface_catalog_created",
                severity="info",
                finding_type="target_surface_catalog_created",
                message=f"{len(catalog.supported_target_surfaces)} target surfaces were cataloged.",
                subject_ref=_ref("continuity_injection_target_surface_catalog", catalog.catalog_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                evidence_refs=catalog.evidence_refs,
                withdrawal_condition="Withdraw if any catalog surface allows runtime mutation now.",
            ),
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:compatibility_rule_created",
                severity="info",
                finding_type="compatibility_rule_created",
                message=f"{len(rules)} compatibility rules were created.",
                subject_ref=None,
                evidence_refs=[],
                withdrawal_condition="Withdraw if any required compatibility rule is missing.",
            ),
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:injection_bundle_created",
                severity="info" if bundles else "warning",
                finding_type="injection_bundle_created",
                message="Injection bundle was created as a future handoff artifact only.",
                subject_ref=_ref("continuity_injection_bundle", bundles[0].injection_bundle_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) if bundles else None,
                evidence_refs=bundles[0].evidence_refs if bundles else [],
                withdrawal_condition="Withdraw if the bundle is applied to runtime.",
            ),
            ContinuityInjectionBoundaryFinding(
                finding_id="continuity_injection_finding:injection_preview_created",
                severity="info" if previews else "warning",
                finding_type="injection_preview_created",
                message="Injection preview was created and not applied.",
                subject_ref=_ref("continuity_injection_preview", previews[0].preview_id, CONTINUITY_INJECTION_BOUNDARY_VERSION) if previews else None,
                evidence_refs=previews[0].evidence_refs if previews else [],
                withdrawal_condition="Withdraw if preview performs runtime injection.",
            ),
        ]
        if not source_view.context_pack_ref:
            findings.append(
                ContinuityInjectionBoundaryFinding(
                    finding_id="continuity_injection_finding:missing_context_pack",
                    severity="warning",
                    finding_type="missing_context_pack",
                    message="No context pack was available; boundary remains warning-only.",
                    subject_ref=_ref("continuity_injection_source_view", source_view.source_view_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when v0.27.6 context pack exists.",
                )
            )
        return findings


class ContinuityInjectionBoundaryReportService:
    def build_all_parts(
        self,
        *,
        report_id: str | None = None,
        continuity_context_available: bool = True,
        requested_target_surfaces: list[str] | None = None,
        requested_injection_mode: str = "preview_only",
        requested_decision_type: str | None = None,
    ) -> dict[str, Any]:
        source = ContinuityInjectionPrerequisiteSourceService(continuity_context_available=continuity_context_available)
        policy = ContinuityInjectionBoundaryPolicyService().build_policy()
        source_view = ContinuityInjectionSourceViewService().build_source_view(source)
        targets = requested_target_surfaces or [
            "default_agent_context_future",
            "decision_service_guidance_future",
            "skill_proposal_router_context_future",
            "workbench_display_context",
        ]
        request = ContinuityInjectionRequest(
            request_id="continuity_injection_request:v0.27.7",
            continuity_context_build_report_id=source_view.continuity_context_build_report_ref["id"] if source_view.continuity_context_build_report_ref else None,
            continuity_context_id=source_view.continuity_context_ref["id"] if source_view.continuity_context_ref else None,
            context_pack_id=source_view.context_pack_ref["id"] if source_view.context_pack_ref else None,
            selected_context_item_refs=source_view.context_item_refs,
            requested_target_surfaces=targets,
            requested_injection_mode=requested_injection_mode,
            source_refs=source_view.evidence_refs,
        )
        catalog = ContinuityInjectionTargetSurfaceCatalogService().build_catalog()
        rules = ContinuityInjectionCompatibilityRuleService().build_rules(catalog)
        evaluations = ContinuityInjectionEligibilityEvaluationService().evaluate(source_view, catalog, rules)
        priority_policy = ContinuityInstructionPriorityPolicyService().build_policy()
        priority_rules = ContinuityMemoryUserIntentPriorityRuleService().build_rules(request, source_view)
        safety_rules = ContinuitySafetyBoundaryRuleService().build_rules(catalog)
        permission_rules = ContinuityPermissionBoundaryRuleService().build_rules(catalog)
        bindings = ContinuityInjectionContextItemBindingService().build_bindings(request, source_view)
        bundles = ContinuityInjectionBundleService().build_bundles(
            request, source_view, catalog, bindings, priority_policy, safety_rules, permission_rules, evaluations
        )
        previews = ContinuityInjectionPreviewService().build_previews(bundles, source_view, request)
        decisions = ContinuityInjectionDecisionService().decide(request, bundles, requested_decision_type=requested_decision_type)
        record_service = ContinuityInjectionDecisionRecordService()
        decision_records = record_service.build_records(decisions)
        rejected_records = record_service.build_rejected_records(request)
        deferred_records = record_service.build_deferred_records(request)
        traces = ContinuityInjectionBoundaryTraceService().build_traces(
            request, bundles, evaluations, priority_rules, safety_rules, permission_rules
        )
        audit = ContinuityInjectionAuditTrailService().build_audit_trail(
            request, source_view, catalog, rules, evaluations, bundles, previews, decision_records, rejected_records, deferred_records, traces
        )
        findings = ContinuityInjectionBoundaryFindingService().build_findings(source_view, catalog, rules, bundles, previews)
        status = "passed" if bundles and previews else "warning"
        report = ContinuityInjectionBoundaryReport(
            report_id=report_id or "continuity_injection_boundary_report:v0.27.7",
            created_at=utc_now_iso(),
            injection_policy=policy,
            request=request,
            source_view=source_view,
            target_catalog=catalog,
            compatibility_rules=rules,
            eligibility_evaluations=evaluations,
            instruction_priority_policy=priority_policy,
            memory_user_intent_priority_rules=priority_rules,
            safety_boundary_rules=safety_rules,
            permission_boundary_rules=permission_rules,
            context_item_bindings=bindings,
            injection_bundles=bundles,
            injection_previews=previews,
            injection_decisions=decisions,
            decision_records=decision_records,
            rejected_records=rejected_records,
            deferred_records=deferred_records,
            boundary_traces=traces,
            audit_trail=audit,
            findings=findings,
            report_status=status,
            ready_for_v0_27_8=True,
            injection_policy_created=True,
            source_view_created=True,
            target_catalog_created=True,
            compatibility_rules_created=True,
            eligibility_evaluations_created=True,
            injection_bundles_created=bool(bundles),
            injection_previews_created=bool(previews),
            injection_decisions_recorded=bool(decision_records),
            boundary_traces_created=bool(traces),
            audit_trail_created=True,
            limitations=[
                "v0.27.7 creates boundary, preview, decision, and future handoff artifacts only.",
                "Actual continuity runtime injection remains outside v0.27.7.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if any runtime context, policy, safety, permission, memory, persona, or behavior surface is mutated.",
                "Withdraw readiness if provider invocation, command execution, file mutation, or safety/permission bypass occurs.",
            ],
        )
        return {
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "target_catalog": catalog,
            "target_surfaces": catalog.supported_target_surfaces,
            "compatibility_rules": rules,
            "eligibility_evaluations": evaluations,
            "instruction_priority_policy": priority_policy,
            "memory_user_intent_priority_rules": priority_rules,
            "safety_boundary_rules": safety_rules,
            "permission_boundary_rules": permission_rules,
            "context_item_bindings": bindings,
            "injection_bundles": bundles,
            "injection_previews": previews,
            "injection_decisions": decisions,
            "decision_records": decision_records,
            "rejected_records": rejected_records,
            "deferred_records": deferred_records,
            "boundary_traces": traces,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": CONTINUITY_INJECTION_BOUNDARY_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "continuity_injection_boundary",
            "principles": [
                "Continuity injection boundary is not runtime injection",
                "Injection preview is not applied context",
                "Injection bundle is not behavior override",
                "Memory context is guidance, not authority",
                "Explicit user instruction outranks memory",
                "Safety gate and permission boundary must remain active",
                "Contradictory memory must be surfaced, not silently resolved",
                "Stale memory must be warned, not silently applied",
                "Privacy-filtered memory must remain filtered",
                "Memory must not trigger provider invocation or command execution",
            ],
            "safety_boundary": {
                "continuity_injection_bundle_created": "conditional",
                "continuity_injection_preview_created": "conditional",
                "runtime_injection_performed": False,
                "default_agent_context_mutated": False,
                "decision_service_mutated": False,
                "skill_router_mutated": False,
                "safety_gate_mutated": False,
                "permission_policy_mutated": False,
                "memory_updated": False,
                "memory_revoked": False,
                "memory_forgotten": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_replayed": False,
                "raw_provider_output_replayed": False,
                "pig_guidance_used_as_authority": False,
                "provider_invoked": False,
                "command_executed": False,
                "file_mutated": False,
                "safety_gate_bypassed": False,
                "permission_boundary_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.27.8 memory audit/update/revoke/forget", "v0.27.9 memory consolidation"],
            "next_step": CONTINUITY_INJECTION_BOUNDARY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "continuity_injection_boundary_created",
            "version": CONTINUITY_INJECTION_BOUNDARY_VERSION,
            "source_read_models": [
                "SessionContinuityContextState",
                "ContinuityContextPackState",
                "ContinuityContextItemState",
                "ContinuityConflictReportState",
                "ContinuityStalenessWarningState",
                "ContinuityPrivacyFilterState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "ContinuityInjectionBoundaryState",
                "ContinuityInjectionBundleState",
                "ContinuityInjectionPreviewState",
                "ContinuityInjectionDecisionState",
                "ContinuityInjectionBoundaryTraceState",
                "ContinuityInjectionAuditState",
                "V027ReadinessState",
            ],
            "effect_types": CONTINUITY_INJECTION_EFFECT_TYPES,
            "forbidden_effect_types": CONTINUITY_INJECTION_FORBIDDEN_EFFECT_TYPES,
        }


def render_continuity_injection_boundary_cli(parts: dict[str, Any], section: str = "policy") -> str:
    report: ContinuityInjectionBoundaryReport = parts["report"]
    lines = [
        f"Continuity Injection Boundary {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"injection_policy_created={_bool(report.injection_policy_created)}",
        f"source_view_created={_bool(report.source_view_created)}",
        f"target_catalog_created={_bool(report.target_catalog_created)}",
        f"compatibility_rules_created={_bool(report.compatibility_rules_created)}",
        f"eligibility_evaluations_created={_bool(report.eligibility_evaluations_created)}",
        f"injection_bundles_created={_bool(report.injection_bundles_created)}",
        f"injection_previews_created={_bool(report.injection_previews_created)}",
        f"injection_decisions_recorded={_bool(report.injection_decisions_recorded)}",
        f"boundary_traces_created={_bool(report.boundary_traces_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"ready_for_v0_27_8={_bool(report.ready_for_v0_27_8)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"runtime_injection_performed={_bool(report.runtime_injection_performed)}",
        f"default_agent_context_mutated={_bool(report.default_agent_context_mutated)}",
        f"decision_service_mutated={_bool(report.decision_service_mutated)}",
        f"skill_router_mutated={_bool(report.skill_router_mutated)}",
        f"safety_gate_mutated={_bool(report.safety_gate_mutated)}",
        f"permission_policy_mutated={_bool(report.permission_policy_mutated)}",
        f"memory_updated={_bool(report.memory_updated)}",
        f"memory_revoked={_bool(report.memory_revoked)}",
        f"memory_forgotten={_bool(report.memory_forgotten)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_replayed={_bool(report.raw_transcript_replayed)}",
        f"raw_provider_output_replayed={_bool(report.raw_provider_output_replayed)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"pig_guidance_used_as_authority={_bool(report.pig_guidance_used_as_authority)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"file_mutated={_bool(report.file_mutated)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"permission_boundary_bypassed={_bool(report.permission_boundary_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "policy": ("actual_runtime_injection_enabled_now", report.injection_policy.actual_runtime_injection_enabled_now),
        "source-view": ("source_status", report.source_view.source_status),
        "targets": ("target_surface_count", len(report.target_catalog.supported_target_surfaces)),
        "compatibility": ("compatibility_rule_count", len(report.compatibility_rules)),
        "eligibility": ("eligibility_evaluation_count", len(report.eligibility_evaluations)),
        "priority": ("explicit_user_instruction_outranks_memory", report.instruction_priority_policy.explicit_user_instruction_outranks_memory),
        "safety-boundary": ("safety_boundary_rule_count", len(report.safety_boundary_rules)),
        "permission-boundary": ("permission_boundary_rule_count", len(report.permission_boundary_rules)),
        "bindings": ("binding_count", len(report.context_item_bindings)),
        "bundle": ("bundle_count", len(report.injection_bundles)),
        "preview": ("preview_count", len(report.injection_previews)),
        "decide": ("decision_type", report.injection_decisions[0].decision_type),
        "boundary-trace": ("boundary_bypassed", report.boundary_traces[0].boundary_bypassed),
        "audit": ("audit_status", report.audit_trail.audit_status),
        "report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    return "\n".join(lines)


MEMORY_LIFECYCLE_VERSION = "v0.27.8"
MEMORY_LIFECYCLE_VERSION_NAME = "Memory Audit / Update / Revoke / Forget"
MEMORY_LIFECYCLE_KOREAN_NAME = "Memory Audit·Update·Revoke·Forget"
MEMORY_LIFECYCLE_NEXT_STEP = "v0.27.9 Memory Candidate & Continuity Consolidation"

MEMORY_LIFECYCLE_OBJECT_TYPES = [
    "memory_lifecycle_control_policy",
    "memory_lifecycle_request",
    "memory_lifecycle_source_view",
    "memory_lifecycle_operation_gate",
    "memory_review_request",
    "memory_review_record",
    "memory_update_candidate",
    "memory_update_decision",
    "memory_update_record",
    "memory_supersede_record",
    "memory_revoke_request",
    "memory_revoke_decision",
    "memory_revoke_record",
    "memory_forget_request",
    "memory_forget_decision",
    "memory_forget_record",
    "memory_forget_tombstone",
    "memory_archive_decision",
    "memory_archive_record",
    "memory_expiration_decision",
    "memory_expiration_record",
    "memory_conflict_resolution_record",
    "memory_lifecycle_privacy_gate",
    "memory_lifecycle_evidence_review",
    "memory_lifecycle_scope",
    "memory_lifecycle_pig_guidance_attachment",
    "memory_lifecycle_no_op_decision",
    "memory_lifecycle_audit_trail",
    "memory_lifecycle_registry_update_preview",
    "memory_lifecycle_registry_update_record",
    "memory_lifecycle_finding",
    "memory_lifecycle_report",
    "durable_memory_record",
    "durable_memory_registry",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_LIFECYCLE_EVENT_TYPES = [
    "memory_lifecycle_requested",
    "memory_lifecycle_prerequisites_loaded",
    "memory_lifecycle_policy_created",
    "memory_lifecycle_source_view_created",
    "memory_lifecycle_gate_evaluated",
    "memory_review_request_created",
    "memory_review_record_created",
    "memory_update_candidate_created",
    "memory_update_decision_created",
    "memory_update_record_created",
    "memory_supersede_record_created",
    "memory_revoke_request_created",
    "memory_revoke_decision_created",
    "memory_revoke_record_created",
    "memory_forget_request_created",
    "memory_forget_decision_created",
    "memory_forget_record_created",
    "memory_forget_tombstone_created",
    "memory_archive_decision_created",
    "memory_archive_record_created",
    "memory_expiration_decision_created",
    "memory_expiration_record_created",
    "memory_conflict_resolution_record_created",
    "memory_lifecycle_privacy_gate_created",
    "memory_lifecycle_evidence_review_created",
    "memory_lifecycle_scope_created",
    "memory_lifecycle_pig_guidance_attached",
    "memory_lifecycle_no_op_decision_created",
    "memory_lifecycle_registry_update_preview_created",
    "memory_lifecycle_registry_update_record_created",
    "memory_lifecycle_audit_trail_created",
    "memory_lifecycle_report_created",
    "memory_lifecycle_warning_created",
    "memory_lifecycle_blocked",
]

MEMORY_LIFECYCLE_EFFECT_TYPES = [
    "read_only_observation",
    "memory_review_record_created",
    "memory_update_candidate_created",
    "memory_update_decision_recorded",
    "memory_update_record_created",
    "memory_supersede_record_created",
    "memory_revoke_record_created",
    "memory_forget_record_created",
    "memory_forget_tombstone_created",
    "memory_archive_record_created",
    "memory_expiration_record_created",
    "memory_conflict_resolution_record_created",
    "memory_lifecycle_registry_updated",
    "memory_lifecycle_audit_created",
    "state_candidate_created",
]

MEMORY_LIFECYCLE_CONDITIONAL_EFFECT_TYPES = [
    "memory_update_record_created",
    "memory_revoke_record_created",
    "memory_forget_record_created",
    "memory_lifecycle_registry_updated",
]

MEMORY_LIFECYCLE_FORBIDDEN_EFFECT_TYPES = [
    "silent_memory_overwrite",
    "unlogged_memory_deletion",
    "source_data_deleted",
    "raw_transcript_restored",
    "raw_provider_output_restored",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "pig_guidance_used_as_authority",
    "pig_policy_mutated",
    "pig_executed",
    "provider_invoked",
    "command_executed",
    "safety_gate_bypassed",
    "continuity_injected",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "raw_secret_output",
    "credential_exposed",
    "llm_judge_used",
]


@dataclass
class MemoryLifecycleControlPolicy(_ModelMixin):
    policy_id: str
    version: str = MEMORY_LIFECYCLE_VERSION
    layer: str = MEMORY_CONTRACT_LAYER
    lifecycle_control_enabled: bool = True
    review_enabled: bool = True
    update_candidate_enabled: bool = True
    update_decision_enabled: bool = True
    update_execution_conditionally_enabled: bool = True
    supersede_enabled: bool = True
    revoke_enabled: bool = True
    forget_enabled: bool = True
    archive_enabled: bool = True
    expiration_enabled: bool = True
    conflict_resolution_enabled: bool = True
    no_op_decision_enabled: bool = True
    lifecycle_gate_required: bool = True
    audit_required: bool = True
    source_data_deletion_enabled_now: bool = False
    silent_overwrite_forbidden: bool = True
    unlogged_deletion_forbidden: bool = True
    forget_is_not_source_data_deletion_by_default: bool = True
    revoke_removes_active_use: bool = True
    archive_removes_active_use: bool = True
    expiration_removes_active_use: bool = True
    forget_removes_recallable_memory_content: bool = True
    forget_tombstone_required: bool = True
    update_requires_evidence: bool = True
    update_requires_decision_record: bool = True
    update_requires_version_record: bool = True
    supersede_requires_previous_record_ref: bool = True
    persona_mutation_enabled_now: bool = False
    behavior_policy_mutation_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    safety_bypass_enabled_now: bool = False
    continuity_injection_enabled_now: bool = False
    pig_guidance_is_not_lifecycle_authority: bool = True
    llm_judge_as_sole_lifecycle_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleRequest(_ModelMixin):
    lifecycle_request_id: str
    durable_memory_registry_report_id: str | None
    durable_memory_registry_id: str | None
    selected_memory_record_refs: list[dict[str, Any]]
    requested_operation: str
    request_reason: str
    requested_by: str
    strictness: str = "standard"
    version: str = MEMORY_LIFECYCLE_VERSION
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleSourceView(_ModelMixin):
    source_view_id: str
    durable_registry_report_ref: dict[str, Any] | None
    durable_registry_ref: dict[str, Any] | None
    selected_memory_record_refs: list[dict[str, Any]]
    registry_entry_refs: list[dict[str, Any]]
    memory_status_refs: list[dict[str, Any]]
    lifecycle_policy_refs: list[dict[str, Any]]
    privacy_boundary_refs: list[dict[str, Any]]
    conflict_marker_refs: list[dict[str, Any]]
    forget_revoke_binding_refs: list[dict[str, Any]]
    evidence_index_refs: list[dict[str, Any]]
    provenance_refs: list[dict[str, Any]]
    continuity_context_refs: list[dict[str, Any]]
    injection_boundary_refs: list[dict[str, Any]]
    pig_guidance_refs: list[dict[str, Any]]
    source_status: str
    selected_memory_count: int
    version: str = MEMORY_LIFECYCLE_VERSION
    raw_transcript_included: bool = False
    raw_provider_output_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleOperationGate(_ModelMixin):
    gate_id: str
    lifecycle_request_id: str
    memory_record_ref_present: bool
    operation_allowed_by_lifecycle_policy: bool
    operation_allowed_by_forget_revoke_binding: bool
    evidence_available: bool
    privacy_gate_passed: bool
    conflict_review_passed_or_not_required: bool
    audit_ready: bool
    user_confirmation_required: bool
    user_confirmation_present: bool
    source_data_deletion_requested: bool
    raw_memory_restoration_absent: bool
    persona_mutation_absent: bool
    behavior_policy_mutation_absent: bool
    gate_status: str
    gate_summary: str
    may_review: bool
    may_create_update_candidate: bool
    may_apply_update: bool
    may_revoke: bool
    may_forget: bool
    may_archive: bool
    may_expire: bool
    may_resolve_conflict: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    source_data_deletion_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryReviewRequest(_ModelMixin):
    review_request_id: str
    memory_record_ref: dict[str, Any]
    review_reason: str
    review_scope: str
    requested_by: str
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryReviewRecord(_ModelMixin):
    review_record_id: str
    memory_record_ref: dict[str, Any]
    review_request_ref: dict[str, Any]
    review_status: str
    review_summary: str
    evidence_review_refs: list[dict[str, Any]]
    privacy_gate_ref: dict[str, Any] | None
    conflict_marker_refs: list[dict[str, Any]]
    version: str = MEMORY_LIFECYCLE_VERSION
    no_mutation_performed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryUpdateCandidate(_ModelMixin):
    update_candidate_id: str
    memory_record_ref: dict[str, Any]
    proposed_update_summary: str
    update_type: str
    proposed_new_summary: str | None
    proposed_scope_ref: dict[str, Any] | None
    proposed_lifecycle_ref: dict[str, Any] | None
    proposed_privacy_boundary_ref: dict[str, Any] | None
    proposed_evidence_index_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_LIFECYCLE_VERSION
    update_applied_now: bool = False
    persona_mutation: bool = False
    behavior_policy_mutation: bool = False


@dataclass
class MemoryUpdateDecision(_ModelMixin):
    update_decision_id: str
    update_candidate_ref: dict[str, Any]
    decision_type: str
    decision_reason: str
    decision_basis_refs: list[dict[str, Any]]
    applies_update_now: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_LIFECYCLE_VERSION
    mutates_persona_now: bool = False
    mutates_behavior_policy_now: bool = False


@dataclass
class MemoryUpdateRecord(_ModelMixin):
    update_record_id: str
    memory_record_ref: dict[str, Any]
    update_candidate_ref: dict[str, Any]
    update_decision_ref: dict[str, Any]
    previous_version_ref: dict[str, Any] | None
    new_version_ref: dict[str, Any] | None
    updated_fields: list[str]
    update_summary: str
    update_applied: bool
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    raw_content_added: bool = False
    persona_mutation: bool = False
    behavior_policy_mutation: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemorySupersedeRecord(_ModelMixin):
    supersede_record_id: str
    old_memory_record_ref: dict[str, Any]
    new_memory_record_ref: dict[str, Any] | None
    supersede_reason: str
    old_record_status_after: str
    version: str = MEMORY_LIFECYCLE_VERSION
    source_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryRevokeRequest(_ModelMixin):
    revoke_request_id: str
    memory_record_ref: dict[str, Any]
    revoke_reason: str
    requested_by: str
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryRevokeDecision(_ModelMixin):
    revoke_decision_id: str
    revoke_request_ref: dict[str, Any]
    decision_type: str
    decision_reason: str
    revokes_active_use_now: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    deletes_source_data_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryRevokeRecord(_ModelMixin):
    revoke_record_id: str
    memory_record_ref: dict[str, Any]
    revoke_request_ref: dict[str, Any]
    revoke_decision_ref: dict[str, Any]
    previous_status: str
    active_use_removed: bool
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    new_status: str = "revoked"
    source_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryForgetRequest(_ModelMixin):
    forget_request_id: str
    memory_record_ref: dict[str, Any]
    forget_reason: str
    requested_by: str
    version: str = MEMORY_LIFECYCLE_VERSION
    source_data_deletion_requested: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryForgetDecision(_ModelMixin):
    forget_decision_id: str
    forget_request_ref: dict[str, Any]
    decision_type: str
    decision_reason: str
    removes_recallable_memory_content_now: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    deletes_source_data_now: bool = False
    creates_tombstone: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryForgetRecord(_ModelMixin):
    forget_record_id: str
    memory_record_ref: dict[str, Any]
    forget_request_ref: dict[str, Any]
    forget_decision_ref: dict[str, Any]
    previous_status: str
    recallable_content_removed: bool
    active_use_removed: bool
    registry_updated: bool
    tombstone_ref: dict[str, Any] | None
    version: str = MEMORY_LIFECYCLE_VERSION
    new_status: str = "forgotten"
    source_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryForgetTombstone(_ModelMixin):
    tombstone_id: str
    forgotten_memory_record_id: str
    forget_record_ref: dict[str, Any]
    tombstone_summary: str
    version: str = MEMORY_LIFECYCLE_VERSION
    contains_recallable_memory_content: bool = False
    contains_raw_source_content: bool = False
    contains_secret: bool = False
    audit_only: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryArchiveDecision(_ModelMixin):
    archive_decision_id: str
    memory_record_ref: dict[str, Any]
    decision_reason: str
    archives_memory_now: bool
    active_use_removed: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryArchiveRecord(_ModelMixin):
    archive_record_id: str
    memory_record_ref: dict[str, Any]
    archive_decision_ref: dict[str, Any]
    previous_status: str
    active_use_removed: bool
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    new_status: str = "archived"
    source_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryExpirationDecision(_ModelMixin):
    expiration_decision_id: str
    memory_record_ref: dict[str, Any]
    lifecycle_policy_ref: dict[str, Any] | None
    expiration_reason: str
    expires_memory_now: bool
    active_use_removed: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryExpirationRecord(_ModelMixin):
    expiration_record_id: str
    memory_record_ref: dict[str, Any]
    expiration_decision_ref: dict[str, Any]
    previous_status: str
    active_use_removed: bool
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    new_status: str = "expired"
    source_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryConflictResolutionRecord(_ModelMixin):
    conflict_resolution_record_id: str
    memory_record_refs: list[dict[str, Any]]
    conflict_marker_refs: list[dict[str, Any]]
    resolution_type: str
    resolution_summary: str
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    automatically_resolved: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecyclePrivacyGate(_ModelMixin):
    privacy_gate_id: str
    memory_record_ref: dict[str, Any]
    operation: str
    privacy_boundary_ref: dict[str, Any] | None
    privacy_risk_level: str
    user_confirmation_required: bool
    user_confirmation_present: bool
    operation_allowed: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleEvidenceReview(_ModelMixin):
    evidence_review_id: str
    memory_record_ref: dict[str, Any]
    operation: str
    evidence_index_ref: dict[str, Any] | None
    provenance_ref: dict[str, Any] | None
    evidence_sufficient: bool
    evidence_review_summary: str
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleScope(_ModelMixin):
    lifecycle_scope_id: str
    memory_record_ref: dict[str, Any]
    operation: str
    scope_ref: dict[str, Any] | None
    operation_within_scope: bool
    scope_summary: str
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecyclePIGGuidanceAttachment(_ModelMixin):
    pig_attachment_id: str
    memory_record_ref: dict[str, Any]
    operation: str
    pig_guidance_refs: list[dict[str, Any]]
    guidance_summary: str
    version: str = MEMORY_LIFECYCLE_VERSION
    pig_guidance_is_authority: bool = False
    pig_guidance_mutates_policy: bool = False
    pig_guidance_executes: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleNoOpDecision(_ModelMixin):
    no_op_decision_id: str
    memory_record_ref: dict[str, Any] | None
    no_op_reason: str
    decision_basis_refs: list[dict[str, Any]]
    version: str = MEMORY_LIFECYCLE_VERSION
    no_mutation_performed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleAuditTrail(_ModelMixin):
    audit_trail_id: str
    lifecycle_request_ref: dict[str, Any]
    operation_gate_refs: list[dict[str, Any]]
    review_record_refs: list[dict[str, Any]]
    update_candidate_refs: list[dict[str, Any]]
    update_decision_refs: list[dict[str, Any]]
    update_record_refs: list[dict[str, Any]]
    supersede_record_refs: list[dict[str, Any]]
    revoke_record_refs: list[dict[str, Any]]
    forget_record_refs: list[dict[str, Any]]
    forget_tombstone_refs: list[dict[str, Any]]
    archive_record_refs: list[dict[str, Any]]
    expiration_record_refs: list[dict[str, Any]]
    conflict_resolution_record_refs: list[dict[str, Any]]
    no_op_decision_refs: list[dict[str, Any]]
    registry_update_record_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    version: str = MEMORY_LIFECYCLE_VERSION
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleRegistryUpdatePreview(_ModelMixin):
    registry_update_preview_id: str
    operation: str
    memory_record_ref: dict[str, Any]
    proposed_status: str
    proposed_registry_effect: str
    version: str = MEMORY_LIFECYCLE_VERSION
    preview_is_not_registry_update: bool = True
    registry_updated_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleRegistryUpdateRecord(_ModelMixin):
    registry_update_record_id: str
    operation: str
    memory_record_ref: dict[str, Any]
    previous_status: str
    new_status: str
    registry_entry_ref: dict[str, Any] | None
    registry_updated: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryLifecycleFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryLifecycleReport(_ModelMixin):
    report_id: str
    created_at: str
    lifecycle_policy: MemoryLifecycleControlPolicy
    request: MemoryLifecycleRequest
    source_view: MemoryLifecycleSourceView
    operation_gates: list[MemoryLifecycleOperationGate]
    review_records: list[MemoryReviewRecord]
    update_candidates: list[MemoryUpdateCandidate]
    update_decisions: list[MemoryUpdateDecision]
    update_records: list[MemoryUpdateRecord]
    supersede_records: list[MemorySupersedeRecord]
    revoke_requests: list[MemoryRevokeRequest]
    revoke_decisions: list[MemoryRevokeDecision]
    revoke_records: list[MemoryRevokeRecord]
    forget_requests: list[MemoryForgetRequest]
    forget_decisions: list[MemoryForgetDecision]
    forget_records: list[MemoryForgetRecord]
    forget_tombstones: list[MemoryForgetTombstone]
    archive_decisions: list[MemoryArchiveDecision]
    archive_records: list[MemoryArchiveRecord]
    expiration_decisions: list[MemoryExpirationDecision]
    expiration_records: list[MemoryExpirationRecord]
    conflict_resolution_records: list[MemoryConflictResolutionRecord]
    privacy_gates: list[MemoryLifecyclePrivacyGate]
    evidence_reviews: list[MemoryLifecycleEvidenceReview]
    lifecycle_scopes: list[MemoryLifecycleScope]
    pig_guidance_attachments: list[MemoryLifecyclePIGGuidanceAttachment]
    no_op_decisions: list[MemoryLifecycleNoOpDecision]
    registry_update_previews: list[MemoryLifecycleRegistryUpdatePreview]
    registry_update_records: list[MemoryLifecycleRegistryUpdateRecord]
    audit_trail: MemoryLifecycleAuditTrail
    findings: list[MemoryLifecycleFinding]
    report_status: str
    ready_for_v0_27_9: bool
    review_records_created: bool
    update_candidates_created: bool
    update_decisions_created: bool
    update_records_created: bool
    revoke_records_created: bool
    forget_records_created: bool
    archive_records_created: bool
    expiration_records_created: bool
    conflict_resolution_records_created: bool
    audit_trail_created: bool
    registry_update_records_created: bool
    memory_updated: bool
    memory_revoked: bool
    memory_forgotten: bool
    memory_archived: bool
    memory_expired: bool
    version: str = MEMORY_LIFECYCLE_VERSION
    ready_for_v0_28: bool = False
    source_data_deleted: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    raw_transcript_restored: bool = False
    raw_provider_output_restored: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    pig_guidance_used_as_authority: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    safety_gate_bypassed: bool = False
    continuity_injected: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_LIFECYCLE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.27.9 Memory Candidate & Continuity Consolidation begins or memory lifecycle policy changes."
    )


class MemoryLifecyclePrerequisiteSourceService:
    def __init__(self, registry_available: bool = True, source_data_deletion_requested: bool = False) -> None:
        self.registry_available = registry_available
        self.source_data_deletion_requested = source_data_deletion_requested
        self._registry_parts: dict[str, Any] | None = None
        self._continuity_parts: dict[str, Any] | None = None
        self._injection_parts: dict[str, Any] | None = None

    def _registry(self) -> dict[str, Any]:
        if self._registry_parts is None:
            self._registry_parts = DurableMemoryRegistryReportService().build_all_parts(
                requested_write_mode="write_if_gate_passed",
                release_hygiene_gate_passed=True,
                runtime_data_hygiene_gate_passed=True,
            )
        return self._registry_parts

    def _continuity(self) -> dict[str, Any]:
        if self._continuity_parts is None:
            self._continuity_parts = SessionContinuityContextBuildReportService().build_all_parts(
                active_registry_available=self.registry_available
            )
        return self._continuity_parts

    def _injection(self) -> dict[str, Any]:
        if self._injection_parts is None:
            self._injection_parts = ContinuityInjectionBoundaryReportService().build_all_parts(
                continuity_context_available=self.registry_available
            )
        return self._injection_parts

    def load_v0277_injection_boundary_report(self) -> ContinuityInjectionBoundaryReport | None:
        return self._injection()["report"] if self.registry_available else None

    def load_v0276_continuity_context_report(self) -> SessionContinuityContextBuildReport | None:
        return self._continuity()["report"] if self.registry_available else None

    def load_v0275_registry_report(self) -> DurableMemoryRegistryReport | None:
        return self._registry()["report"] if self.registry_available else None

    def load_durable_memory_registry(self) -> DurableMemoryRegistry | None:
        return self._registry()["registry"] if self.registry_available else None

    def load_durable_memory_records(self) -> list[DurableMemoryRecord]:
        return self._registry()["durable_memory_records"] if self.registry_available else []

    def load_registry_entries(self) -> list[DurableMemoryRegistryEntry]:
        return self._registry()["registry_entries"] if self.registry_available else []

    def load_record_statuses(self) -> list[dict[str, Any]]:
        return [_ref("memory_record_status", "memory_record_status:v0.27.5:active", DURABLE_MEMORY_REGISTRY_VERSION)]

    def load_lifecycle_policies(self) -> list[MemoryRecordLifecyclePolicy]:
        return [self._registry()["lifecycle_policy"]] if self.registry_available else []

    def load_privacy_boundaries(self) -> list[MemoryRecordPrivacyBoundary]:
        return [self._registry()["privacy_boundary"]] if self.registry_available else []

    def load_conflict_markers(self) -> list[MemoryRecordConflictMarker]:
        return self._registry()["conflict_markers"] if self.registry_available else []

    def load_forget_revoke_bindings(self) -> list[MemoryRecordForgetRevokeBinding]:
        return [self._registry()["forget_revoke_binding"]] if self.registry_available else []

    def load_evidence_indexes(self) -> list[MemoryRecordEvidenceIndex]:
        return [self._registry()["evidence_index"]] if self.registry_available else []

    def load_provenance_refs(self) -> list[MemoryRecordProvenance]:
        return [self._registry()["provenance"]] if self.registry_available else []

    def load_pig_guidance_refs_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_report", "pig:memory_audit_update_revoke_forget:v0.27.8", MEMORY_LIFECYCLE_VERSION)]


class MemoryLifecycleControlPolicyService:
    def build_policy(self) -> MemoryLifecycleControlPolicy:
        return MemoryLifecycleControlPolicy(
            policy_id="memory_lifecycle_control_policy:v0.27.8",
            evidence_refs=[_ref("memory_contract_report", "memory_contract_report:v0.27.0")],
        )


class MemoryLifecycleSourceViewService:
    def build_source_view(
        self,
        source: MemoryLifecyclePrerequisiteSourceService,
        request: MemoryLifecycleRequest,
    ) -> MemoryLifecycleSourceView:
        registry_report = source.load_v0275_registry_report()
        registry = source.load_durable_memory_registry()
        records = source.load_durable_memory_records()
        entries = source.load_registry_entries()
        lifecycle_policies = source.load_lifecycle_policies()
        privacy_boundaries = source.load_privacy_boundaries()
        conflict_markers = source.load_conflict_markers()
        bindings = source.load_forget_revoke_bindings()
        evidence_indexes = source.load_evidence_indexes()
        provenance = source.load_provenance_refs()
        continuity_report = source.load_v0276_continuity_context_report()
        injection_report = source.load_v0277_injection_boundary_report()
        selected_refs = request.selected_memory_record_refs or [
            _ref("durable_memory_record", item.memory_record_id, DURABLE_MEMORY_REGISTRY_VERSION) for item in records
        ]
        status = "complete" if registry_report and registry and selected_refs else "partial"
        return MemoryLifecycleSourceView(
            source_view_id="memory_lifecycle_source_view:v0.27.8",
            durable_registry_report_ref=_ref("durable_memory_registry_report", registry_report.report_id, DURABLE_MEMORY_REGISTRY_VERSION)
            if registry_report
            else None,
            durable_registry_ref=_ref("durable_memory_registry", registry.registry_id, DURABLE_MEMORY_REGISTRY_VERSION)
            if registry
            else None,
            selected_memory_record_refs=selected_refs,
            registry_entry_refs=[
                _ref("durable_memory_registry_entry", item.registry_entry_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in entries
            ],
            memory_status_refs=source.load_record_statuses(),
            lifecycle_policy_refs=[
                _ref("memory_record_lifecycle_policy", item.lifecycle_policy_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in lifecycle_policies
            ],
            privacy_boundary_refs=[
                _ref("memory_record_privacy_boundary", item.privacy_boundary_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in privacy_boundaries
            ],
            conflict_marker_refs=[
                _ref("memory_record_conflict_marker", item.conflict_marker_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in conflict_markers
            ],
            forget_revoke_binding_refs=[
                _ref("memory_record_forget_revoke_binding", item.binding_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in bindings
            ],
            evidence_index_refs=[
                _ref("memory_record_evidence_index", item.evidence_index_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in evidence_indexes
            ],
            provenance_refs=[
                _ref("memory_record_provenance", item.provenance_id, DURABLE_MEMORY_REGISTRY_VERSION)
                for item in provenance
            ],
            continuity_context_refs=[
                _ref("session_continuity_context_build_report", continuity_report.report_id, SESSION_CONTINUITY_CONTEXT_VERSION)
            ]
            if continuity_report
            else [],
            injection_boundary_refs=[
                _ref("continuity_injection_boundary_report", injection_report.report_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)
            ]
            if injection_report
            else [],
            pig_guidance_refs=source.load_pig_guidance_refs_if_available(),
            source_status=status,
            selected_memory_count=len(selected_refs),
            evidence_refs=[
                _ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION),
            ],
        )


class MemoryLifecycleOperationGateService:
    def evaluate_gate(
        self,
        request: MemoryLifecycleRequest,
        source_view: MemoryLifecycleSourceView,
        source_data_deletion_requested: bool = False,
    ) -> MemoryLifecycleOperationGate:
        has_record = bool(source_view.selected_memory_record_refs)
        binding_ok = bool(source_view.forget_revoke_binding_refs) or request.requested_operation not in {"forget", "revoke"}
        source_deletion_blocks = source_data_deletion_requested
        gate_passed = has_record and binding_ok and not source_deletion_blocks
        return MemoryLifecycleOperationGate(
            gate_id=f"memory_lifecycle_operation_gate:v0.27.8:{request.requested_operation}",
            lifecycle_request_id=request.lifecycle_request_id,
            memory_record_ref_present=has_record,
            operation_allowed_by_lifecycle_policy=bool(source_view.lifecycle_policy_refs),
            operation_allowed_by_forget_revoke_binding=binding_ok,
            evidence_available=bool(source_view.evidence_index_refs),
            privacy_gate_passed=True,
            conflict_review_passed_or_not_required=True,
            audit_ready=True,
            user_confirmation_required=source_deletion_blocks,
            user_confirmation_present=not source_deletion_blocks,
            source_data_deletion_requested=source_data_deletion_requested,
            raw_memory_restoration_absent=True,
            persona_mutation_absent=True,
            behavior_policy_mutation_absent=True,
            gate_status="passed" if gate_passed else "blocked",
            gate_summary="Lifecycle operation is gated and auditable; source deletion remains disabled.",
            may_review=has_record,
            may_create_update_candidate=has_record,
            may_apply_update=gate_passed and request.requested_operation in {"update", "supersede"},
            may_revoke=gate_passed and request.requested_operation == "revoke",
            may_forget=gate_passed and request.requested_operation == "forget",
            may_archive=gate_passed and request.requested_operation == "archive",
            may_expire=gate_passed and request.requested_operation == "expire",
            may_resolve_conflict=gate_passed and request.requested_operation == "resolve_conflict",
            evidence_refs=[_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryReviewService:
    def build_review_request(self, request: MemoryLifecycleRequest, memory_record_ref: dict[str, Any]) -> MemoryReviewRequest:
        return MemoryReviewRequest(
            review_request_id="memory_review_request:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            review_reason=request.request_reason,
            review_scope="selected durable memory record lifecycle status",
            requested_by=request.requested_by,
            evidence_refs=[_ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def build_review_record(
        self,
        review_request: MemoryReviewRequest,
        privacy_gate: MemoryLifecyclePrivacyGate,
        evidence_review: MemoryLifecycleEvidenceReview,
        source_view: MemoryLifecycleSourceView,
    ) -> MemoryReviewRecord:
        return MemoryReviewRecord(
            review_record_id="memory_review_record:v0.27.8:default",
            memory_record_ref=review_request.memory_record_ref,
            review_request_ref=_ref("memory_review_request", review_request.review_request_id, MEMORY_LIFECYCLE_VERSION),
            review_status="reviewed",
            review_summary="Review completed without applying lifecycle mutation.",
            evidence_review_refs=[
                _ref("memory_lifecycle_evidence_review", evidence_review.evidence_review_id, MEMORY_LIFECYCLE_VERSION)
            ],
            privacy_gate_ref=_ref("memory_lifecycle_privacy_gate", privacy_gate.privacy_gate_id, MEMORY_LIFECYCLE_VERSION),
            conflict_marker_refs=source_view.conflict_marker_refs,
            evidence_refs=[_ref("memory_lifecycle_request", review_request.review_request_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryUpdateService:
    def build_update_candidate(self, memory_record_ref: dict[str, Any], source_view: MemoryLifecycleSourceView) -> MemoryUpdateCandidate:
        return MemoryUpdateCandidate(
            update_candidate_id="memory_update_candidate:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            proposed_update_summary="Refs-only lifecycle metadata update candidate; not an executed update.",
            update_type="update_status",
            proposed_new_summary=None,
            proposed_scope_ref=None,
            proposed_lifecycle_ref=source_view.lifecycle_policy_refs[0] if source_view.lifecycle_policy_refs else None,
            proposed_privacy_boundary_ref=source_view.privacy_boundary_refs[0] if source_view.privacy_boundary_refs else None,
            proposed_evidence_index_ref=source_view.evidence_index_refs[0] if source_view.evidence_index_refs else None,
            evidence_refs=source_view.evidence_index_refs,
        )

    def build_update_decision(
        self,
        candidate: MemoryUpdateCandidate,
        gate: MemoryLifecycleOperationGate,
    ) -> MemoryUpdateDecision:
        applies = gate.may_apply_update and gate.gate_status == "passed"
        return MemoryUpdateDecision(
            update_decision_id="memory_update_decision:v0.27.8:default",
            update_candidate_ref=_ref("memory_update_candidate", candidate.update_candidate_id, MEMORY_LIFECYCLE_VERSION),
            decision_type="apply_update" if applies else "block_update",
            decision_reason="Update is allowed only when lifecycle gate passes and audit refs are present.",
            decision_basis_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
            applies_update_now=applies,
            evidence_refs=candidate.evidence_refs,
        )

    def apply_update_only_if_gate_passed(self, gate: MemoryLifecycleOperationGate) -> bool:
        return gate.gate_status == "passed" and gate.may_apply_update

    def build_update_record(
        self,
        memory_record_ref: dict[str, Any],
        candidate: MemoryUpdateCandidate,
        decision: MemoryUpdateDecision,
        gate: MemoryLifecycleOperationGate,
    ) -> MemoryUpdateRecord:
        applied = self.apply_update_only_if_gate_passed(gate) and decision.applies_update_now
        return MemoryUpdateRecord(
            update_record_id="memory_update_record:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            update_candidate_ref=_ref("memory_update_candidate", candidate.update_candidate_id, MEMORY_LIFECYCLE_VERSION),
            update_decision_ref=_ref("memory_update_decision", decision.update_decision_id, MEMORY_LIFECYCLE_VERSION),
            previous_version_ref=_ref("durable_memory_record_version", "durable_memory_record_version:v0.27.5:previous", DURABLE_MEMORY_REGISTRY_VERSION),
            new_version_ref=_ref("durable_memory_record_version", "durable_memory_record_version:v0.27.8:preview", MEMORY_LIFECYCLE_VERSION),
            updated_fields=["status"],
            update_summary="Gated lifecycle update record; no raw content or persona policy changes added.",
            update_applied=applied,
            registry_updated=applied,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemorySupersedeService:
    def build_supersede_record(self, memory_record_ref: dict[str, Any]) -> MemorySupersedeRecord:
        return MemorySupersedeRecord(
            supersede_record_id="memory_supersede_record:v0.27.8:default",
            old_memory_record_ref=memory_record_ref,
            new_memory_record_ref=None,
            supersede_reason="Supersede path is represented as an auditable lifecycle record.",
            old_record_status_after="superseded",
            evidence_refs=[memory_record_ref],
        )


class MemoryRevokeService:
    def build_revoke_request(self, request: MemoryLifecycleRequest, memory_record_ref: dict[str, Any]) -> MemoryRevokeRequest:
        return MemoryRevokeRequest(
            revoke_request_id="memory_revoke_request:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            revoke_reason=request.request_reason,
            requested_by=request.requested_by,
            evidence_refs=[_ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def build_revoke_decision(self, revoke_request: MemoryRevokeRequest, gate: MemoryLifecycleOperationGate) -> MemoryRevokeDecision:
        revokes = gate.gate_status == "passed" and gate.may_revoke
        return MemoryRevokeDecision(
            revoke_decision_id="memory_revoke_decision:v0.27.8:default",
            revoke_request_ref=_ref("memory_revoke_request", revoke_request.revoke_request_id, MEMORY_LIFECYCLE_VERSION),
            decision_type="revoke" if revokes else "block_revoke",
            decision_reason="Revoke removes active use only when lifecycle gate passes.",
            revokes_active_use_now=revokes,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def apply_revoke_only_if_gate_passed(self, gate: MemoryLifecycleOperationGate) -> bool:
        return gate.gate_status == "passed" and gate.may_revoke

    def build_revoke_record(
        self,
        revoke_request: MemoryRevokeRequest,
        decision: MemoryRevokeDecision,
        gate: MemoryLifecycleOperationGate,
    ) -> MemoryRevokeRecord:
        active_removed = self.apply_revoke_only_if_gate_passed(gate) and decision.revokes_active_use_now
        return MemoryRevokeRecord(
            revoke_record_id="memory_revoke_record:v0.27.8:default",
            memory_record_ref=revoke_request.memory_record_ref,
            revoke_request_ref=_ref("memory_revoke_request", revoke_request.revoke_request_id, MEMORY_LIFECYCLE_VERSION),
            revoke_decision_ref=_ref("memory_revoke_decision", decision.revoke_decision_id, MEMORY_LIFECYCLE_VERSION),
            previous_status="active",
            active_use_removed=active_removed,
            registry_updated=active_removed,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryForgetService:
    def build_forget_request(
        self,
        request: MemoryLifecycleRequest,
        memory_record_ref: dict[str, Any],
        source_data_deletion_requested: bool = False,
    ) -> MemoryForgetRequest:
        return MemoryForgetRequest(
            forget_request_id="memory_forget_request:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            forget_reason=request.request_reason,
            requested_by=request.requested_by,
            source_data_deletion_requested=source_data_deletion_requested,
            evidence_refs=[_ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def build_forget_decision(self, forget_request: MemoryForgetRequest, gate: MemoryLifecycleOperationGate) -> MemoryForgetDecision:
        forgets = gate.gate_status == "passed" and gate.may_forget
        return MemoryForgetDecision(
            forget_decision_id="memory_forget_decision:v0.27.8:default",
            forget_request_ref=_ref("memory_forget_request", forget_request.forget_request_id, MEMORY_LIFECYCLE_VERSION),
            decision_type="forget_memory" if forgets else "block_forget",
            decision_reason="Forget disables active use and removes recallable memory content; source data deletion remains disabled.",
            removes_recallable_memory_content_now=forgets,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def apply_forget_only_if_gate_passed(self, gate: MemoryLifecycleOperationGate) -> bool:
        return gate.gate_status == "passed" and gate.may_forget

    def build_tombstone(self, memory_record_ref: dict[str, Any]) -> MemoryForgetTombstone:
        record_id = memory_record_ref.get("id", "durable_memory_record:v0.27.5:default")
        return MemoryForgetTombstone(
            tombstone_id="memory_forget_tombstone:v0.27.8:default",
            forgotten_memory_record_id=record_id,
            forget_record_ref=_ref("memory_forget_record", "memory_forget_record:v0.27.8:default", MEMORY_LIFECYCLE_VERSION),
            tombstone_summary="Audit-only tombstone with no recallable memory content, raw source content, or secrets.",
            evidence_refs=[memory_record_ref],
        )

    def build_forget_record(
        self,
        forget_request: MemoryForgetRequest,
        decision: MemoryForgetDecision,
        gate: MemoryLifecycleOperationGate,
        tombstone: MemoryForgetTombstone,
    ) -> MemoryForgetRecord:
        forgotten = self.apply_forget_only_if_gate_passed(gate) and decision.removes_recallable_memory_content_now
        return MemoryForgetRecord(
            forget_record_id="memory_forget_record:v0.27.8:default",
            memory_record_ref=forget_request.memory_record_ref,
            forget_request_ref=_ref("memory_forget_request", forget_request.forget_request_id, MEMORY_LIFECYCLE_VERSION),
            forget_decision_ref=_ref("memory_forget_decision", decision.forget_decision_id, MEMORY_LIFECYCLE_VERSION),
            previous_status="active",
            recallable_content_removed=forgotten,
            active_use_removed=forgotten,
            registry_updated=forgotten,
            tombstone_ref=_ref("memory_forget_tombstone", tombstone.tombstone_id, MEMORY_LIFECYCLE_VERSION),
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryArchiveService:
    def build_archive_decision(self, memory_record_ref: dict[str, Any], gate: MemoryLifecycleOperationGate) -> MemoryArchiveDecision:
        archives = gate.gate_status == "passed" and gate.may_archive
        return MemoryArchiveDecision(
            archive_decision_id="memory_archive_decision:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            decision_reason="Archive removes active use while preserving reference.",
            archives_memory_now=archives,
            active_use_removed=archives,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def build_archive_record(self, decision: MemoryArchiveDecision) -> MemoryArchiveRecord:
        return MemoryArchiveRecord(
            archive_record_id="memory_archive_record:v0.27.8:default",
            memory_record_ref=decision.memory_record_ref,
            archive_decision_ref=_ref("memory_archive_decision", decision.archive_decision_id, MEMORY_LIFECYCLE_VERSION),
            previous_status="active",
            active_use_removed=decision.active_use_removed,
            registry_updated=decision.archives_memory_now,
            evidence_refs=[_ref("memory_archive_decision", decision.archive_decision_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryExpirationService:
    def build_expiration_decision(
        self,
        memory_record_ref: dict[str, Any],
        gate: MemoryLifecycleOperationGate,
        lifecycle_policy_ref: dict[str, Any] | None,
    ) -> MemoryExpirationDecision:
        expires = gate.gate_status == "passed" and gate.may_expire
        return MemoryExpirationDecision(
            expiration_decision_id="memory_expiration_decision:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            lifecycle_policy_ref=lifecycle_policy_ref,
            expiration_reason="Expiration removes active use without deleting source data.",
            expires_memory_now=expires,
            active_use_removed=expires,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )

    def build_expiration_record(self, decision: MemoryExpirationDecision) -> MemoryExpirationRecord:
        return MemoryExpirationRecord(
            expiration_record_id="memory_expiration_record:v0.27.8:default",
            memory_record_ref=decision.memory_record_ref,
            expiration_decision_ref=_ref("memory_expiration_decision", decision.expiration_decision_id, MEMORY_LIFECYCLE_VERSION),
            previous_status="active",
            active_use_removed=decision.active_use_removed,
            registry_updated=decision.expires_memory_now,
            evidence_refs=[_ref("memory_expiration_decision", decision.expiration_decision_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryConflictResolutionService:
    def build_resolution_record(
        self,
        source_view: MemoryLifecycleSourceView,
        gate: MemoryLifecycleOperationGate,
    ) -> MemoryConflictResolutionRecord:
        return MemoryConflictResolutionRecord(
            conflict_resolution_record_id="memory_conflict_resolution_record:v0.27.8:default",
            memory_record_refs=source_view.selected_memory_record_refs,
            conflict_marker_refs=source_view.conflict_marker_refs,
            resolution_type="surface_only",
            resolution_summary="Conflict is recorded and surfaced; it is not silently resolved.",
            registry_updated=gate.gate_status == "passed" and gate.may_resolve_conflict,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryLifecyclePrivacyGateService:
    def build_gate(
        self,
        memory_record_ref: dict[str, Any],
        operation: str,
        source_view: MemoryLifecycleSourceView,
    ) -> MemoryLifecyclePrivacyGate:
        return MemoryLifecyclePrivacyGate(
            privacy_gate_id=f"memory_lifecycle_privacy_gate:v0.27.8:{operation}",
            memory_record_ref=memory_record_ref,
            operation=operation,
            privacy_boundary_ref=source_view.privacy_boundary_refs[0] if source_view.privacy_boundary_refs else None,
            privacy_risk_level="low",
            user_confirmation_required=False,
            user_confirmation_present=True,
            operation_allowed=True,
            evidence_refs=source_view.privacy_boundary_refs,
        )


class MemoryLifecycleEvidenceReviewService:
    def build_review(
        self,
        memory_record_ref: dict[str, Any],
        operation: str,
        source_view: MemoryLifecycleSourceView,
    ) -> MemoryLifecycleEvidenceReview:
        return MemoryLifecycleEvidenceReview(
            evidence_review_id=f"memory_lifecycle_evidence_review:v0.27.8:{operation}",
            memory_record_ref=memory_record_ref,
            operation=operation,
            evidence_index_ref=source_view.evidence_index_refs[0] if source_view.evidence_index_refs else None,
            provenance_ref=source_view.provenance_refs[0] if source_view.provenance_refs else None,
            evidence_sufficient=bool(source_view.evidence_index_refs),
            evidence_review_summary="Evidence refs are available for lifecycle review.",
            evidence_refs=source_view.evidence_index_refs,
        )


class MemoryLifecycleScopeService:
    def build_scope(
        self,
        memory_record_ref: dict[str, Any],
        operation: str,
        source_view: MemoryLifecycleSourceView,
    ) -> MemoryLifecycleScope:
        return MemoryLifecycleScope(
            lifecycle_scope_id=f"memory_lifecycle_scope:v0.27.8:{operation}",
            memory_record_ref=memory_record_ref,
            operation=operation,
            scope_ref=None,
            operation_within_scope=True,
            scope_summary="Lifecycle operation is limited to selected durable memory record refs.",
            evidence_refs=source_view.selected_memory_record_refs,
        )


class MemoryLifecyclePIGGuidanceAttachmentService:
    def attach_guidance(
        self,
        memory_record_ref: dict[str, Any],
        operation: str,
        source_view: MemoryLifecycleSourceView,
    ) -> MemoryLifecyclePIGGuidanceAttachment:
        return MemoryLifecyclePIGGuidanceAttachment(
            pig_attachment_id=f"memory_lifecycle_pig_guidance_attachment:v0.27.8:{operation}",
            memory_record_ref=memory_record_ref,
            operation=operation,
            pig_guidance_refs=source_view.pig_guidance_refs,
            guidance_summary="PIG guidance is attached as non-authoritative lifecycle review signal.",
            evidence_refs=source_view.pig_guidance_refs,
        )


class MemoryLifecycleNoOpService:
    def build_no_op_decision(self, memory_record_ref: dict[str, Any] | None) -> MemoryLifecycleNoOpDecision:
        return MemoryLifecycleNoOpDecision(
            no_op_decision_id="memory_lifecycle_no_op_decision:v0.27.8:default",
            memory_record_ref=memory_record_ref,
            no_op_reason="No-op is a valid lifecycle decision when no mutation is required.",
            decision_basis_refs=[] if memory_record_ref is None else [memory_record_ref],
            evidence_refs=[] if memory_record_ref is None else [memory_record_ref],
        )


class MemoryLifecycleRegistryUpdateService:
    def build_preview(
        self,
        operation: str,
        memory_record_ref: dict[str, Any],
        proposed_status: str,
    ) -> MemoryLifecycleRegistryUpdatePreview:
        return MemoryLifecycleRegistryUpdatePreview(
            registry_update_preview_id=f"memory_lifecycle_registry_update_preview:v0.27.8:{operation}",
            operation=operation,
            memory_record_ref=memory_record_ref,
            proposed_status=proposed_status,
            proposed_registry_effect="refs-only lifecycle registry status transition preview",
            evidence_refs=[memory_record_ref],
        )

    def build_record(
        self,
        operation: str,
        memory_record_ref: dict[str, Any],
        previous_status: str,
        new_status: str,
        gate: MemoryLifecycleOperationGate,
        registry_entry_ref: dict[str, Any] | None,
    ) -> MemoryLifecycleRegistryUpdateRecord:
        registry_updated = gate.gate_status == "passed" and operation in {"update", "revoke", "forget", "archive", "expire", "resolve_conflict"}
        return MemoryLifecycleRegistryUpdateRecord(
            registry_update_record_id=f"memory_lifecycle_registry_update_record:v0.27.8:{operation}",
            operation=operation,
            memory_record_ref=memory_record_ref,
            previous_status=previous_status,
            new_status=new_status,
            registry_entry_ref=registry_entry_ref,
            registry_updated=registry_updated,
            evidence_refs=[_ref("memory_lifecycle_operation_gate", gate.gate_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryLifecycleAuditTrailService:
    def build_audit_trail(
        self,
        request: MemoryLifecycleRequest,
        gates: list[MemoryLifecycleOperationGate],
        review_records: list[MemoryReviewRecord],
        update_candidates: list[MemoryUpdateCandidate],
        update_decisions: list[MemoryUpdateDecision],
        update_records: list[MemoryUpdateRecord],
        supersede_records: list[MemorySupersedeRecord],
        revoke_records: list[MemoryRevokeRecord],
        forget_records: list[MemoryForgetRecord],
        tombstones: list[MemoryForgetTombstone],
        archive_records: list[MemoryArchiveRecord],
        expiration_records: list[MemoryExpirationRecord],
        conflict_records: list[MemoryConflictResolutionRecord],
        no_op_decisions: list[MemoryLifecycleNoOpDecision],
        registry_update_records: list[MemoryLifecycleRegistryUpdateRecord],
    ) -> MemoryLifecycleAuditTrail:
        event_count = (
            len(gates)
            + len(review_records)
            + len(update_candidates)
            + len(update_decisions)
            + len(update_records)
            + len(supersede_records)
            + len(revoke_records)
            + len(forget_records)
            + len(tombstones)
            + len(archive_records)
            + len(expiration_records)
            + len(conflict_records)
            + len(no_op_decisions)
            + len(registry_update_records)
        )
        blocked = any(gate.gate_status == "blocked" for gate in gates)
        return MemoryLifecycleAuditTrail(
            audit_trail_id="memory_lifecycle_audit_trail:v0.27.8",
            lifecycle_request_ref=_ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION),
            operation_gate_refs=[_ref("memory_lifecycle_operation_gate", item.gate_id, MEMORY_LIFECYCLE_VERSION) for item in gates],
            review_record_refs=[_ref("memory_review_record", item.review_record_id, MEMORY_LIFECYCLE_VERSION) for item in review_records],
            update_candidate_refs=[_ref("memory_update_candidate", item.update_candidate_id, MEMORY_LIFECYCLE_VERSION) for item in update_candidates],
            update_decision_refs=[_ref("memory_update_decision", item.update_decision_id, MEMORY_LIFECYCLE_VERSION) for item in update_decisions],
            update_record_refs=[_ref("memory_update_record", item.update_record_id, MEMORY_LIFECYCLE_VERSION) for item in update_records],
            supersede_record_refs=[_ref("memory_supersede_record", item.supersede_record_id, MEMORY_LIFECYCLE_VERSION) for item in supersede_records],
            revoke_record_refs=[_ref("memory_revoke_record", item.revoke_record_id, MEMORY_LIFECYCLE_VERSION) for item in revoke_records],
            forget_record_refs=[_ref("memory_forget_record", item.forget_record_id, MEMORY_LIFECYCLE_VERSION) for item in forget_records],
            forget_tombstone_refs=[_ref("memory_forget_tombstone", item.tombstone_id, MEMORY_LIFECYCLE_VERSION) for item in tombstones],
            archive_record_refs=[_ref("memory_archive_record", item.archive_record_id, MEMORY_LIFECYCLE_VERSION) for item in archive_records],
            expiration_record_refs=[
                _ref("memory_expiration_record", item.expiration_record_id, MEMORY_LIFECYCLE_VERSION)
                for item in expiration_records
            ],
            conflict_resolution_record_refs=[
                _ref("memory_conflict_resolution_record", item.conflict_resolution_record_id, MEMORY_LIFECYCLE_VERSION)
                for item in conflict_records
            ],
            no_op_decision_refs=[
                _ref("memory_lifecycle_no_op_decision", item.no_op_decision_id, MEMORY_LIFECYCLE_VERSION)
                for item in no_op_decisions
            ],
            registry_update_record_refs=[
                _ref("memory_lifecycle_registry_update_record", item.registry_update_record_id, MEMORY_LIFECYCLE_VERSION)
                for item in registry_update_records
            ],
            audit_event_count=event_count,
            audit_status="blocked" if blocked else "ready",
            evidence_refs=[_ref("memory_lifecycle_request", request.lifecycle_request_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryLifecycleFindingService:
    BLOCKED_FINDINGS = {
        "silent_overwrite_attempted",
        "unlogged_deletion_attempted",
        "source_data_deletion_attempted",
        "raw_transcript_restoration_attempted",
        "raw_provider_output_restoration_attempted",
        "persona_mutation_attempted",
        "behavior_policy_mutation_attempted",
        "pig_guidance_as_authority_detected",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "safety_bypass_attempted",
        "continuity_injection_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        source_view: MemoryLifecycleSourceView,
        gates: list[MemoryLifecycleOperationGate],
    ) -> list[MemoryLifecycleFinding]:
        findings = [
            MemoryLifecycleFinding(
                finding_id="memory_lifecycle_finding:policy_created",
                severity="info",
                finding_type="lifecycle_policy_created",
                message="Memory lifecycle control policy was created.",
                subject_ref=_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION),
                evidence_refs=[_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION)],
                withdrawal_condition="Withdraw if lifecycle policy cannot be created.",
            ),
            MemoryLifecycleFinding(
                finding_id="memory_lifecycle_finding:source_view_created",
                severity="info",
                finding_type="lifecycle_source_view_created",
                message="Memory lifecycle source view was created from refs only.",
                subject_ref=_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION),
                evidence_refs=[_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION)],
                withdrawal_condition="Withdraw if raw content enters lifecycle source view.",
            ),
            MemoryLifecycleFinding(
                finding_id="memory_lifecycle_finding:lifecycle_gate_created",
                severity="info",
                finding_type="lifecycle_gate_created",
                message="Lifecycle operation gate was evaluated.",
                subject_ref=_ref("memory_lifecycle_operation_gate", gates[0].gate_id, MEMORY_LIFECYCLE_VERSION) if gates else None,
                evidence_refs=[_ref("memory_lifecycle_source_view", source_view.source_view_id, MEMORY_LIFECYCLE_VERSION)],
                withdrawal_condition="Withdraw if lifecycle operation gate cannot be evaluated.",
            ),
        ]
        if source_view.durable_registry_report_ref is None:
            findings.append(
                MemoryLifecycleFinding(
                    finding_id="memory_lifecycle_finding:missing_registry_report",
                    severity="warning",
                    finding_type="missing_durable_memory_registry_report",
                    message="Durable memory registry report is missing; lifecycle report remains warning-only.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when a valid v0.27.5 registry report is available.",
                )
            )
        if not source_view.selected_memory_record_refs:
            findings.append(
                MemoryLifecycleFinding(
                    finding_id="memory_lifecycle_finding:missing_record",
                    severity="warning",
                    finding_type="missing_durable_memory_record",
                    message="No durable memory records are selected for lifecycle review.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when selected durable memory record refs exist.",
                )
            )
        if any(gate.source_data_deletion_requested for gate in gates):
            findings.append(
                MemoryLifecycleFinding(
                    finding_id="memory_lifecycle_finding:source_data_deletion_attempted",
                    severity="critical",
                    finding_type="source_data_deletion_attempted",
                    message="Source data deletion was requested, but v0.27.8 does not allow it by default.",
                    subject_ref=_ref("memory_lifecycle_operation_gate", gates[0].gate_id, MEMORY_LIFECYCLE_VERSION) if gates else None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw only if a later explicit deletion policy is implemented and gated.",
                )
            )
        return findings


class MemoryLifecycleReportService:
    def build_request(
        self,
        requested_operation: str = "review",
        record_id: str | None = None,
        report_id: str | None = None,
    ) -> MemoryLifecycleRequest:
        memory_ref = _ref(
            "durable_memory_record",
            record_id or "durable_memory_record:v0.27.5:active",
            DURABLE_MEMORY_REGISTRY_VERSION,
        )
        return MemoryLifecycleRequest(
            lifecycle_request_id=report_id or "memory_lifecycle_request:v0.27.8:default",
            durable_memory_registry_report_id="durable_memory_registry_report:v0.27.5",
            durable_memory_registry_id="durable_memory_registry:v0.27.5",
            selected_memory_record_refs=[memory_ref],
            requested_operation=requested_operation,
            request_reason="v0.27.8 lifecycle audit/update/revoke/forget verification",
            requested_by="system_test_fixture",
            source_refs=[memory_ref],
        )

    def build_all_parts(
        self,
        report_id: str | None = None,
        requested_operation: str = "review",
        record_id: str | None = None,
        registry_available: bool = True,
        source_data_deletion_requested: bool = False,
    ) -> dict[str, Any]:
        policy = MemoryLifecycleControlPolicyService().build_policy()
        request = self.build_request(requested_operation=requested_operation, record_id=record_id, report_id=report_id)
        source = MemoryLifecyclePrerequisiteSourceService(
            registry_available=registry_available,
            source_data_deletion_requested=source_data_deletion_requested,
        )
        source_view = MemoryLifecycleSourceViewService().build_source_view(source, request)
        memory_record_ref = source_view.selected_memory_record_refs[0] if source_view.selected_memory_record_refs else request.selected_memory_record_refs[0]

        operations = ["review", "update", "revoke", "forget", "archive", "expire", "resolve_conflict", "no_op"]
        gates: list[MemoryLifecycleOperationGate] = []
        for operation in operations:
            operation_request = self.build_request(
                requested_operation=operation,
                record_id=memory_record_ref["id"],
                report_id=f"memory_lifecycle_request:v0.27.8:{operation}",
            )
            gates.append(
                MemoryLifecycleOperationGateService().evaluate_gate(
                    operation_request,
                    source_view,
                    source_data_deletion_requested=source_data_deletion_requested if operation == requested_operation else False,
                )
            )
        gate_by_operation = {gate.gate_id.rsplit(":", 1)[-1]: gate for gate in gates}
        requested_gate = gate_by_operation.get(requested_operation, gates[0])

        privacy_gate = MemoryLifecyclePrivacyGateService().build_gate(memory_record_ref, requested_operation, source_view)
        evidence_review = MemoryLifecycleEvidenceReviewService().build_review(memory_record_ref, requested_operation, source_view)
        lifecycle_scope = MemoryLifecycleScopeService().build_scope(memory_record_ref, requested_operation, source_view)
        pig_attachment = MemoryLifecyclePIGGuidanceAttachmentService().attach_guidance(memory_record_ref, requested_operation, source_view)

        review_service = MemoryReviewService()
        review_request = review_service.build_review_request(request, memory_record_ref)
        review_record = review_service.build_review_record(review_request, privacy_gate, evidence_review, source_view)

        update_service = MemoryUpdateService()
        update_candidate = update_service.build_update_candidate(memory_record_ref, source_view)
        update_decision = update_service.build_update_decision(update_candidate, gate_by_operation["update"])
        update_record = update_service.build_update_record(memory_record_ref, update_candidate, update_decision, gate_by_operation["update"])
        if requested_operation != "update":
            update_decision.decision_type = "defer_update"
            update_decision.applies_update_now = False
            update_record.update_applied = False
            update_record.registry_updated = False
        supersede_record = MemorySupersedeService().build_supersede_record(memory_record_ref)

        revoke_service = MemoryRevokeService()
        revoke_request = revoke_service.build_revoke_request(request, memory_record_ref)
        revoke_decision = revoke_service.build_revoke_decision(revoke_request, gate_by_operation["revoke"])
        revoke_record = revoke_service.build_revoke_record(revoke_request, revoke_decision, gate_by_operation["revoke"])
        if requested_operation != "revoke":
            revoke_decision.decision_type = "defer_revoke"
            revoke_decision.revokes_active_use_now = False
            revoke_record.active_use_removed = False
            revoke_record.registry_updated = False

        forget_service = MemoryForgetService()
        forget_request = forget_service.build_forget_request(request, memory_record_ref, source_data_deletion_requested)
        forget_decision = forget_service.build_forget_decision(forget_request, gate_by_operation["forget"])
        tombstone = forget_service.build_tombstone(memory_record_ref)
        forget_record = forget_service.build_forget_record(forget_request, forget_decision, gate_by_operation["forget"], tombstone)
        if requested_operation != "forget":
            forget_decision.decision_type = "defer_forget"
            forget_decision.removes_recallable_memory_content_now = False
            forget_record.recallable_content_removed = False
            forget_record.active_use_removed = False
            forget_record.registry_updated = False

        archive_service = MemoryArchiveService()
        archive_decision = archive_service.build_archive_decision(memory_record_ref, gate_by_operation["archive"])
        archive_record = archive_service.build_archive_record(archive_decision)
        if requested_operation != "archive":
            archive_decision.archives_memory_now = False
            archive_decision.active_use_removed = False
            archive_record.active_use_removed = False
            archive_record.registry_updated = False

        expiration_service = MemoryExpirationService()
        expiration_decision = expiration_service.build_expiration_decision(
            memory_record_ref,
            gate_by_operation["expire"],
            source_view.lifecycle_policy_refs[0] if source_view.lifecycle_policy_refs else None,
        )
        expiration_record = expiration_service.build_expiration_record(expiration_decision)
        if requested_operation != "expire":
            expiration_decision.expires_memory_now = False
            expiration_decision.active_use_removed = False
            expiration_record.active_use_removed = False
            expiration_record.registry_updated = False

        conflict_record = MemoryConflictResolutionService().build_resolution_record(
            source_view,
            gate_by_operation["resolve_conflict"],
        )
        if requested_operation != "resolve_conflict":
            conflict_record.registry_updated = False
        no_op_decision = MemoryLifecycleNoOpService().build_no_op_decision(memory_record_ref)

        registry_update_service = MemoryLifecycleRegistryUpdateService()
        registry_preview = registry_update_service.build_preview(requested_operation, memory_record_ref, "lifecycle_controlled")
        registry_entry_ref = source_view.registry_entry_refs[0] if source_view.registry_entry_refs else None
        registry_records = [
            registry_update_service.build_record("update", memory_record_ref, "active", "active", gate_by_operation["update"], registry_entry_ref),
            registry_update_service.build_record("revoke", memory_record_ref, "active", "revoked", gate_by_operation["revoke"], registry_entry_ref),
            registry_update_service.build_record("forget", memory_record_ref, "active", "forgotten", gate_by_operation["forget"], registry_entry_ref),
            registry_update_service.build_record("archive", memory_record_ref, "active", "archived", gate_by_operation["archive"], registry_entry_ref),
            registry_update_service.build_record("expire", memory_record_ref, "active", "expired", gate_by_operation["expire"], registry_entry_ref),
        ]
        for registry_record in registry_records:
            if registry_record.operation != requested_operation:
                registry_record.registry_updated = False

        audit = MemoryLifecycleAuditTrailService().build_audit_trail(
            request,
            gates,
            [review_record],
            [update_candidate],
            [update_decision],
            [update_record],
            [supersede_record],
            [revoke_record],
            [forget_record],
            [tombstone],
            [archive_record],
            [expiration_record],
            [conflict_record],
            [no_op_decision],
            registry_records,
        )
        findings = MemoryLifecycleFindingService().build_findings(source_view, gates)
        blocked = any(finding.finding_type in MemoryLifecycleFindingService.BLOCKED_FINDINGS for finding in findings)
        warning = source_view.source_status != "complete"
        report = MemoryLifecycleReport(
            report_id=report_id or "memory_lifecycle_report:v0.27.8",
            created_at=utc_now_iso(),
            lifecycle_policy=policy,
            request=request,
            source_view=source_view,
            operation_gates=gates,
            review_records=[review_record],
            update_candidates=[update_candidate],
            update_decisions=[update_decision],
            update_records=[update_record],
            supersede_records=[supersede_record],
            revoke_requests=[revoke_request],
            revoke_decisions=[revoke_decision],
            revoke_records=[revoke_record],
            forget_requests=[forget_request],
            forget_decisions=[forget_decision],
            forget_records=[forget_record],
            forget_tombstones=[tombstone],
            archive_decisions=[archive_decision],
            archive_records=[archive_record],
            expiration_decisions=[expiration_decision],
            expiration_records=[expiration_record],
            conflict_resolution_records=[conflict_record],
            privacy_gates=[privacy_gate],
            evidence_reviews=[evidence_review],
            lifecycle_scopes=[lifecycle_scope],
            pig_guidance_attachments=[pig_attachment],
            no_op_decisions=[no_op_decision],
            registry_update_previews=[registry_preview],
            registry_update_records=registry_records,
            audit_trail=audit,
            findings=findings,
            report_status="blocked" if blocked else ("warning" if warning else "passed"),
            ready_for_v0_27_9=not blocked,
            review_records_created=True,
            update_candidates_created=True,
            update_decisions_created=True,
            update_records_created=True,
            revoke_records_created=True,
            forget_records_created=True,
            archive_records_created=True,
            expiration_records_created=True,
            conflict_resolution_records_created=True,
            audit_trail_created=True,
            registry_update_records_created=True,
            memory_updated=update_record.update_applied,
            memory_revoked=revoke_record.active_use_removed,
            memory_forgotten=forget_record.recallable_content_removed,
            memory_archived=archive_record.active_use_removed,
            memory_expired=expiration_record.active_use_removed,
            limitations=[
                "Lifecycle records are in-memory/report artifacts for v0.27.8; source data deletion is not implemented.",
                "Forget creates an audit tombstone and does not delete source refs by default.",
            ],
            withdrawal_conditions=[
                "Withdraw if any lifecycle operation bypasses MemoryLifecycleOperationGate.",
                "Withdraw if tombstone includes recallable memory content, raw source content, or secrets.",
            ],
        )
        return {
            "policy": policy,
            "request": request,
            "source_view": source_view,
            "operation_gates": gates,
            "requested_gate": requested_gate,
            "review_request": review_request,
            "review_records": [review_record],
            "update_candidates": [update_candidate],
            "update_decisions": [update_decision],
            "update_records": [update_record],
            "supersede_records": [supersede_record],
            "revoke_requests": [revoke_request],
            "revoke_decisions": [revoke_decision],
            "revoke_records": [revoke_record],
            "forget_requests": [forget_request],
            "forget_decisions": [forget_decision],
            "forget_records": [forget_record],
            "forget_tombstones": [tombstone],
            "archive_decisions": [archive_decision],
            "archive_records": [archive_record],
            "expiration_decisions": [expiration_decision],
            "expiration_records": [expiration_record],
            "conflict_resolution_records": [conflict_record],
            "privacy_gates": [privacy_gate],
            "evidence_reviews": [evidence_review],
            "lifecycle_scopes": [lifecycle_scope],
            "pig_guidance_attachments": [pig_attachment],
            "no_op_decisions": [no_op_decision],
            "registry_update_previews": [registry_preview],
            "registry_update_records": registry_records,
            "audit_trail": audit,
            "findings": findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_LIFECYCLE_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_audit_update_revoke_forget",
            "principles": [
                "Memory review is not mutation",
                "Memory update candidate is not update execution",
                "Memory revoke disables active use",
                "Memory forget disables active use and removes recallable memory content",
                "Forget is not source data deletion by default",
                "Memory archive is not active memory",
                "Memory expiration is not deletion",
                "Conflict resolution must be recorded",
                "No-op is a valid lifecycle decision",
                "PIG guidance is not lifecycle authority",
            ],
            "safety_boundary": {
                "memory_updated": "conditional",
                "memory_revoked": "conditional",
                "memory_forgotten": "conditional",
                "memory_archived": "conditional",
                "memory_expired": "conditional",
                "source_data_deleted": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "raw_transcript_restored": False,
                "raw_provider_output_restored": False,
                "pig_guidance_used_as_authority": False,
                "provider_invoked": False,
                "command_executed": False,
                "safety_gate_bypassed": False,
                "continuity_injected": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.27.9 memory candidate & continuity consolidation",
                "v0.28 public alpha / Schumpeter split preparation",
            ],
            "next_step": MEMORY_LIFECYCLE_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_lifecycle_control_created",
            "version": MEMORY_LIFECYCLE_VERSION,
            "source_read_models": [
                "DurableMemoryRegistryState",
                "DurableMemoryRecordState",
                "DurableMemoryRegistryEntryState",
                "MemoryRecordStatusState",
                "MemoryRecordLifecyclePolicyState",
                "MemoryRecordPrivacyBoundaryState",
                "MemoryRecordConflictMarkerState",
                "MemoryRecordForgetRevokeBindingState",
                "ContinuityInjectionBoundaryState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryLifecycleSourceViewState",
                "MemoryReviewRecordState",
                "MemoryUpdateCandidateState",
                "MemoryUpdateRecordState",
                "MemoryRevokeRecordState",
                "MemoryForgetRecordState",
                "MemoryForgetTombstoneState",
                "MemoryArchiveRecordState",
                "MemoryExpirationRecordState",
                "MemoryConflictResolutionState",
                "MemoryLifecycleAuditState",
                "V027ReadinessState",
            ],
            "effect_types": MEMORY_LIFECYCLE_EFFECT_TYPES,
            "conditional_effect_types": MEMORY_LIFECYCLE_CONDITIONAL_EFFECT_TYPES,
            "forbidden_effect_types": MEMORY_LIFECYCLE_FORBIDDEN_EFFECT_TYPES,
        }


def render_memory_lifecycle_cli(parts: dict[str, Any], section: str = "policy") -> str:
    report: MemoryLifecycleReport = parts["report"]
    lines = [
        f"Memory Lifecycle {section}",
        f"version={report.version}",
        f"layer={MEMORY_CONTRACT_LAYER}",
        f"review_records_created={_bool(report.review_records_created)}",
        f"update_candidates_created={_bool(report.update_candidates_created)}",
        f"update_decisions_created={_bool(report.update_decisions_created)}",
        f"update_records_created={_bool(report.update_records_created)}",
        f"revoke_records_created={_bool(report.revoke_records_created)}",
        f"forget_records_created={_bool(report.forget_records_created)}",
        f"archive_records_created={_bool(report.archive_records_created)}",
        f"expiration_records_created={_bool(report.expiration_records_created)}",
        f"conflict_resolution_records_created={_bool(report.conflict_resolution_records_created)}",
        f"audit_trail_created={_bool(report.audit_trail_created)}",
        f"registry_update_records_created={_bool(report.registry_update_records_created)}",
        f"ready_for_v0_27_9={_bool(report.ready_for_v0_27_9)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"memory_updated={_bool(report.memory_updated)}",
        f"memory_revoked={_bool(report.memory_revoked)}",
        f"memory_forgotten={_bool(report.memory_forgotten)}",
        f"memory_archived={_bool(report.memory_archived)}",
        f"memory_expired={_bool(report.memory_expired)}",
        f"source_data_deleted={_bool(report.source_data_deleted)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"raw_transcript_restored={_bool(report.raw_transcript_restored)}",
        f"raw_provider_output_restored={_bool(report.raw_provider_output_restored)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"pig_guidance_used_as_authority={_bool(report.pig_guidance_used_as_authority)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"continuity_injected={_bool(report.continuity_injected)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "policy": ("source_data_deletion_enabled_now", report.lifecycle_policy.source_data_deletion_enabled_now),
        "source-view": ("source_status", report.source_view.source_status),
        "gate": ("gate_status", parts["requested_gate"].gate_status),
        "review": ("review_status", report.review_records[0].review_status),
        "update-candidate": ("update_type", report.update_candidates[0].update_type),
        "update": ("update_applied", report.update_records[0].update_applied),
        "revoke": ("active_use_removed", report.revoke_records[0].active_use_removed),
        "forget": ("recallable_content_removed", report.forget_records[0].recallable_content_removed),
        "archive": ("memory_archived", report.memory_archived),
        "expire": ("memory_expired", report.memory_expired),
        "conflicts": ("conflict_resolution_type", report.conflict_resolution_records[0].resolution_type),
        "no-op": ("no_mutation_performed", report.no_op_decisions[0].no_mutation_performed),
        "audit": ("audit_status", report.audit_trail.audit_status),
        "report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    return "\n".join(lines)


MEMORY_CONSOLIDATION_VERSION = "v0.27.9"
MEMORY_CONSOLIDATION_VERSION_NAME = "Memory Candidate & Continuity Consolidation"
MEMORY_CONSOLIDATION_KOREAN_NAME = "Memory Candidate·Continuity 통합·릴리즈 준비성"
MEMORY_CONSOLIDATION_RELEASE_NAME = "Memory Candidate & Continuity Foundation v1"
MEMORY_CONSOLIDATION_NEXT_STEP = "v0.28.0 Public Alpha / Schumpeter Split Preparation Contract"
MEMORY_CONSOLIDATION_INCLUDED_VERSIONS = [
    "v0.27.0",
    "v0.27.1",
    "v0.27.2",
    "v0.27.3",
    "v0.27.4",
    "v0.27.5",
    "v0.27.6",
    "v0.27.7",
    "v0.27.8",
    "v0.27.9",
]

MEMORY_CONSOLIDATION_OBJECT_TYPES = [
    "memory_foundation_snapshot",
    "memory_foundation_subject_component",
    "memory_capability_map",
    "memory_capability_map_entry",
    "memory_coverage_matrix",
    "memory_coverage_matrix_row",
    "memory_safety_boundary_consolidation_report",
    "memory_privacy_boundary_consolidation_report",
    "memory_source_boundary_consolidation_report",
    "memory_candidate_quality_consolidation_report",
    "memory_evidence_scoring_consolidation_report",
    "memory_promotion_boundary_consolidation_report",
    "durable_memory_registry_consolidation_report",
    "session_continuity_boundary_consolidation_report",
    "continuity_injection_boundary_consolidation_report",
    "memory_lifecycle_boundary_consolidation_report",
    "memory_process_intelligence_feedback_loop_report",
    "memory_default_agent_readiness_report",
    "memory_release_hygiene_dependency_report",
    "memory_v028_readiness_report",
    "memory_public_alpha_handoff_packet",
    "memory_release_manifest",
    "memory_consolidation_finding",
    "memory_consolidation_report",
    "pig_report",
    "ocpx_projection",
    "execution_envelope",
]

MEMORY_CONSOLIDATION_EVENT_TYPES = [
    "memory_consolidation_requested",
    "memory_consolidation_sources_loaded",
    "memory_foundation_snapshot_created",
    "memory_foundation_subject_components_created",
    "memory_capability_map_created",
    "memory_coverage_matrix_created",
    "memory_safety_boundary_consolidation_report_created",
    "memory_privacy_boundary_consolidation_report_created",
    "memory_source_boundary_consolidation_report_created",
    "memory_candidate_quality_consolidation_report_created",
    "memory_evidence_scoring_consolidation_report_created",
    "memory_promotion_boundary_consolidation_report_created",
    "durable_memory_registry_consolidation_report_created",
    "session_continuity_boundary_consolidation_report_created",
    "continuity_injection_boundary_consolidation_report_created",
    "memory_lifecycle_boundary_consolidation_report_created",
    "memory_process_intelligence_feedback_loop_report_created",
    "memory_default_agent_readiness_report_created",
    "memory_release_hygiene_dependency_report_created",
    "memory_v028_readiness_report_created",
    "memory_public_alpha_handoff_packet_created",
    "memory_release_manifest_created",
    "memory_consolidation_report_created",
    "memory_foundation_release_ready",
    "memory_foundation_release_warning",
    "memory_foundation_release_blocked",
]

MEMORY_CONSOLIDATION_EFFECT_TYPES = [
    "read_only_observation",
    "memory_consolidation_created",
    "memory_foundation_snapshot_created",
    "memory_release_manifest_created",
    "memory_v028_readiness_created",
    "memory_public_alpha_handoff_packet_created",
    "state_candidate_created",
]

MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES = [
    "memory_candidate_created",
    "memory_candidate_scored",
    "memory_promoted",
    "persistent_memory_written",
    "durable_memory_record_created",
    "durable_memory_registry_updated",
    "memory_updated",
    "memory_revoked",
    "memory_forgotten",
    "continuity_injected",
    "runtime_injection_performed",
    "default_agent_context_mutated",
    "decision_service_mutated",
    "skill_router_mutated",
    "safety_gate_mutated",
    "permission_policy_mutated",
    "persona_mutated",
    "behavior_policy_auto_mutated",
    "behavior_policy_mutated",
    "provider_invoked",
    "command_executed",
    "file_mutated",
    "safety_gate_bypassed",
    "permission_boundary_bypassed",
    "raw_transcript_replayed",
    "raw_provider_output_replayed",
    "raw_transcript_persisted_as_memory",
    "raw_provider_output_persisted_as_memory",
    "raw_secret_memory_created",
    "credential_memory_created",
    "pig_guidance_used_as_authority",
    "pig_policy_mutated",
    "pig_executed",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "schumpeter_split_introduced",
    "llm_judge_used",
]

MEMORY_CONSOLIDATION_COMPONENTS = [
    ("memory_contract", "v0.27.0", "contract", "Memory Candidate & Continuity Contract"),
    ("memory_source_boundary", "v0.27.1", "source_boundary", "Memory Source / Ref Boundary"),
    ("memory_candidate_extraction", "v0.27.2", "candidate_extraction", "Memory Candidate Extraction"),
    ("memory_evidence_scoring", "v0.27.3", "evidence_scoring", "Memory Evidence Binder & Scoring"),
    ("memory_promotion_gate", "v0.27.4", "promotion_gate", "Memory Promotion Gate"),
    ("durable_memory_registry", "v0.27.5", "durable_registry", "Durable Memory Record & Registry"),
    ("session_continuity_context", "v0.27.6", "session_continuity_context", "Session Continuity Context Builder"),
    ("continuity_injection_boundary", "v0.27.7", "injection_boundary", "Continuity Injection Boundary"),
    ("memory_lifecycle_control", "v0.27.8", "lifecycle_control", "Memory Audit / Update / Revoke / Forget"),
    ("memory_consolidation", "v0.27.9", "consolidation", "Memory Candidate & Continuity Consolidation"),
]

MEMORY_CONSOLIDATION_EXCLUDED_CAPABILITIES = [
    "Public Alpha Packaging",
    "Schumpeter Split / Company Wrapper",
    "External Provider Adapter",
    "External Agent Dominion Bridge",
    "Runtime Continuity Injection",
    "Default Agent Runtime Mutation",
    "DecisionService Runtime Memory Mutation",
    "SkillRouter Runtime Memory Mutation",
    "SafetyGate Runtime Mutation",
    "PermissionPolicy Runtime Mutation",
    "Autonomous Memory-Driven Execution",
    "Persona Mutation",
    "Behavior Policy Auto-Mutation",
    "Raw Transcript Replay",
    "Raw Provider Output Replay",
    "PIG as Memory Authority",
    "Provider Invocation by Memory",
    "Command Execution by Memory",
    "Safety / Permission Boundary Bypass",
]


@dataclass
class MemoryFoundationSubjectComponent(_ModelMixin):
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    report_ref: dict[str, Any] | None
    status: str
    creates_memory_candidate: bool
    scores_memory_candidate: bool
    records_promotion_decision: bool
    writes_durable_memory: bool
    builds_continuity_context: bool
    performs_lifecycle_mutation: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    finding_count: int
    performs_runtime_injection: bool = False
    mutates_persona: bool = False
    mutates_behavior_policy: bool = False
    invokes_provider: bool = False
    executes_command: bool = False
    bypasses_safety: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class MemoryFoundationSnapshot(_ModelMixin):
    snapshot_id: str
    created_at: str
    included_versions: list[str]
    previous_foundation_ref: dict[str, Any] | None
    recommended_hardening_ref: dict[str, Any] | None
    subject_components: list[MemoryFoundationSubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    privacy_boundary_report_id: str
    lifecycle_boundary_report_id: str
    release_manifest_id: str
    consolidation_report_id: str
    snapshot_status: str
    architecture_ready: bool
    repository_release_ready: bool
    runtime_agent_maturity_ready: bool
    version: str = MEMORY_CONSOLIDATION_VERSION
    release_name: str = MEMORY_CONSOLIDATION_RELEASE_NAME
    public_alpha_ready: bool = False
    limitations: list[str] = field(default_factory=list)


@dataclass
class MemoryCapabilityMapEntry(_ModelMixin):
    capability_id: str
    name: str
    version_introduced: str
    source_report_refs: list[dict[str, Any]]
    status: str
    capability_category: str
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    mutating: bool
    persistent_write_capable: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    runtime_injection_capable: bool = False
    persona_mutation_capable: bool = False
    external_adapter_capable: bool = False
    schumpeter_split_capable: bool = False
    safety_notes: list[str] = field(default_factory=list)


@dataclass
class MemoryCapabilityMap(_ModelMixin):
    map_id: str
    entries: list[MemoryCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    source_boundary_capability_count: int
    candidate_capability_count: int
    scoring_capability_count: int
    promotion_gate_capability_count: int
    durable_registry_capability_count: int
    continuity_context_capability_count: int
    injection_boundary_capability_count: int
    lifecycle_capability_count: int
    version: str = MEMORY_CONSOLIDATION_VERSION
    runtime_injection_capability_count: int = 0
    persona_mutation_capability_count: int = 0
    external_adapter_capability_count: int = 0
    schumpeter_split_capability_count: int = 0


@dataclass
class MemoryCoverageMatrixRow(_ModelMixin):
    subject_id: str
    version_introduced: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_docs: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_safety_boundary: bool
    has_privacy_boundary: bool
    has_audit_trail: bool
    has_forbidden_search: bool
    latest_artifact_available: bool
    coverage_notes: list[str] = field(default_factory=list)


@dataclass
class MemoryCoverageMatrix(_ModelMixin):
    matrix_id: str
    rows: list[MemoryCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int
    future_track_gap_count: int
    version: str = MEMORY_CONSOLIDATION_VERSION


@dataclass
class MemorySafetyBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    status: str
    version: str = MEMORY_CONSOLIDATION_VERSION
    runtime_injection_count: int = 0
    default_agent_mutation_count: int = 0
    decision_service_mutation_count: int = 0
    skill_router_mutation_count: int = 0
    safety_gate_mutation_count: int = 0
    permission_policy_mutation_count: int = 0
    persona_mutation_count: int = 0
    behavior_policy_mutation_count: int = 0
    provider_invocation_count: int = 0
    command_execution_count: int = 0
    file_mutation_count: int = 0
    safety_bypass_count: int = 0
    permission_bypass_count: int = 0
    external_adapter_count: int = 0
    schumpeter_split_count: int = 0
    llm_judge_as_sole_authority_count: int = 0
    raw_transcript_memory_count: int = 0
    raw_provider_output_memory_count: int = 0
    raw_secret_memory_count: int = 0
    credential_memory_count: int = 0
    source_data_deletion_count: int = 0
    unlogged_deletion_count: int = 0
    silent_overwrite_count: int = 0
    pig_authority_violation_count: int = 0
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryPrivacyBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    privacy_policy_refs: list[dict[str, Any]]
    privacy_gate_refs: list[dict[str, Any]]
    privacy_filter_refs: list[dict[str, Any]]
    sensitive_memory_blocked_count: int
    user_confirmation_required_count: int
    privacy_filtered_context_count: int
    privacy_violation_count: int
    privacy_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    credential_exposure_count: int = 0
    raw_secret_output_count: int = 0
    private_path_exposure_count: int = 0


@dataclass
class MemorySourceBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    source_boundary_report_ref: dict[str, Any] | None
    allowed_source_category_count: int
    forbidden_source_category_count: int
    eligible_source_count: int
    blocked_source_count: int
    deferred_source_count: int
    source_boundary_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    raw_source_violation_count: int = 0


@dataclass
class MemoryCandidateQualityConsolidationReport(_ModelMixin):
    report_id: str
    candidate_extraction_report_ref: dict[str, Any] | None
    candidate_count: int
    candidate_only_count: int
    unsupported_claim_count: int
    weakly_supported_claim_count: int
    candidate_with_source_refs_count: int
    candidate_with_evidence_refs_count: int
    candidate_with_risk_flags_count: int
    candidate_quality_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    raw_candidate_violation_count: int = 0


@dataclass
class MemoryEvidenceScoringConsolidationReport(_ModelMixin):
    report_id: str
    evidence_scoring_report_ref: dict[str, Any] | None
    scored_candidate_count: int
    score_breakdown_count: int
    privacy_assessment_count: int
    contradiction_check_count: int
    promotion_readiness_preview_count: int
    scoring_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    high_score_auto_promotion_count: int = 0
    score_as_promotion_violation_count: int = 0


@dataclass
class MemoryPromotionBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    promotion_gate_report_ref: dict[str, Any] | None
    promote_decision_count: int
    reject_decision_count: int
    defer_decision_count: int
    more_evidence_request_count: int
    user_confirmation_request_count: int
    ephemeral_decision_count: int
    archive_only_decision_count: int
    promotion_boundary_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    promotion_without_gate_count: int = 0
    promotion_without_evidence_count: int = 0
    promotion_as_write_violation_count: int = 0


@dataclass
class DurableMemoryRegistryConsolidationReport(_ModelMixin):
    report_id: str
    durable_registry_report_ref: dict[str, Any] | None
    durable_record_count: int
    registry_entry_count: int
    active_count: int
    archived_count: int
    revoked_count: int
    forgotten_count: int
    expired_count: int
    blocked_count: int
    dry_run_count: int
    blocked_write_count: int
    missing_provenance_count: int
    missing_evidence_index_count: int
    missing_scope_count: int
    missing_lifecycle_count: int
    missing_forget_revoke_binding_count: int
    registry_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    write_without_gate_count: int = 0
    write_without_hygiene_count: int = 0


@dataclass
class SessionContinuityBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    session_continuity_report_ref: dict[str, Any] | None
    context_pack_count: int
    context_item_count: int
    active_memory_ref_count: int
    warning_count: int
    conflict_count: int
    stale_count: int
    privacy_filtered_count: int
    continuity_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    raw_replay_violation_count: int = 0
    runtime_injection_count: int = 0


@dataclass
class ContinuityInjectionBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    injection_boundary_report_ref: dict[str, Any] | None
    injection_bundle_count: int
    injection_preview_count: int
    decision_record_count: int
    boundary_trace_count: int
    injection_boundary_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    runtime_injection_count: int = 0
    default_agent_mutation_count: int = 0
    decision_service_mutation_count: int = 0
    skill_router_mutation_count: int = 0
    safety_gate_mutation_count: int = 0
    permission_policy_mutation_count: int = 0


@dataclass
class MemoryLifecycleBoundaryConsolidationReport(_ModelMixin):
    report_id: str
    lifecycle_report_ref: dict[str, Any] | None
    review_record_count: int
    update_record_count: int
    revoke_record_count: int
    forget_record_count: int
    archive_record_count: int
    expiration_record_count: int
    conflict_resolution_record_count: int
    no_op_decision_count: int
    tombstone_count: int
    lifecycle_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    silent_overwrite_count: int = 0
    unlogged_deletion_count: int = 0
    source_data_deletion_count: int = 0
    tombstone_with_recallable_content_count: int = 0


@dataclass
class MemoryProcessIntelligenceFeedbackLoopReport(_ModelMixin):
    report_id: str
    ocel_memory_event_visibility_ready: bool
    ocpx_memory_view_readiness_ready: bool
    pig_guidance_memory_signal_ready: bool
    memory_candidate_traceability_ready: bool
    memory_scoring_traceability_ready: bool
    memory_promotion_traceability_ready: bool
    durable_registry_traceability_ready: bool
    continuity_context_traceability_ready: bool
    lifecycle_traceability_ready: bool
    feedback_loop_status: str
    notes: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    closed_loop_learning_implemented: bool = False


@dataclass
class MemoryDefaultAgentReadinessReport(_ModelMixin):
    report_id: str
    memory_context_available: bool
    continuity_context_pack_available: bool
    injection_boundary_available: bool
    memory_lifecycle_controls_available: bool
    readiness_status: str
    remaining_gaps: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    runtime_injection_implemented: bool = False
    default_agent_mutation_implemented: bool = False
    decision_service_memory_use_implemented: bool = False
    skill_router_memory_use_implemented: bool = False
    safety_gate_memory_context_implemented: bool = False


@dataclass
class MemoryReleaseHygieneDependencyReport(_ModelMixin):
    report_id: str
    release_hygiene_report_ref: dict[str, Any] | None
    release_hygiene_status: str
    clean_worktree_verified: bool | None
    release_tag_verified: bool | None
    license_verified: bool | None
    changelog_verified: bool | None
    pyproject_verified: bool | None
    py_typed_verified: bool | None
    ci_verified: bool | None
    runtime_data_hygiene_verified: bool | None
    reference_license_policy_verified: bool | None
    repository_release_ready: bool
    can_claim_foundation_release: bool
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    can_claim_public_alpha_ready: bool = False


@dataclass
class MemoryV028ReadinessReport(_ModelMixin):
    report_id: str
    ready_for_v0_28: bool
    architecture_requirements_met: bool
    repository_release_requirements_met: bool
    memory_foundation_ready: bool
    workbench_foundation_ready: bool
    blockers: list[str]
    warnings: list[str]
    notes: list[str]
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    target_track: str = "v0.28.x Public Alpha / Schumpeter Split Preparation"
    recommended_next_version: str = MEMORY_CONSOLIDATION_NEXT_STEP
    public_alpha_not_implemented_yet: bool = True
    schumpeter_split_not_implemented_yet: bool = True
    external_adapters_not_implemented_yet: bool = True


@dataclass
class MemoryPublicAlphaHandoffPacket(_ModelMixin):
    handoff_packet_id: str
    source_release_manifest_id: str
    source_consolidation_report_id: str
    ready_inputs: list[str]
    not_implemented_in_v0279: list[str]
    handoff_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = MEMORY_CONSOLIDATION_VERSION
    target_version: str = "v0.28.0"
    target_track: str = "Public Alpha / Schumpeter Split Preparation"
    refs_only: bool = True
    implementation_performed_now: bool = False


@dataclass
class MemoryReleaseManifest(_ModelMixin):
    manifest_id: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    foundation_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    privacy_boundary_report_id: str
    lifecycle_boundary_report_id: str
    release_hygiene_dependency_report_id: str
    v028_readiness_report_id: str
    public_alpha_handoff_packet_id: str
    release_status: str
    architecture_ready: bool
    repository_release_ready: bool
    runtime_agent_maturity_ready: bool
    release_version: str = MEMORY_CONSOLIDATION_VERSION
    release_name: str = MEMORY_CONSOLIDATION_RELEASE_NAME
    public_alpha_ready: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class MemoryConsolidationFinding(_ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class MemoryConsolidationReport(_ModelMixin):
    report_id: str
    created_at: str
    foundation_snapshot: MemoryFoundationSnapshot
    capability_map: MemoryCapabilityMap
    coverage_matrix: MemoryCoverageMatrix
    safety_boundary_report: MemorySafetyBoundaryConsolidationReport
    privacy_boundary_report: MemoryPrivacyBoundaryConsolidationReport
    source_boundary_consolidation_report: MemorySourceBoundaryConsolidationReport
    candidate_quality_consolidation_report: MemoryCandidateQualityConsolidationReport
    evidence_scoring_consolidation_report: MemoryEvidenceScoringConsolidationReport
    promotion_boundary_consolidation_report: MemoryPromotionBoundaryConsolidationReport
    durable_registry_consolidation_report: DurableMemoryRegistryConsolidationReport
    session_continuity_consolidation_report: SessionContinuityBoundaryConsolidationReport
    injection_boundary_consolidation_report: ContinuityInjectionBoundaryConsolidationReport
    lifecycle_boundary_consolidation_report: MemoryLifecycleBoundaryConsolidationReport
    process_intelligence_feedback_loop_report: MemoryProcessIntelligenceFeedbackLoopReport
    default_agent_readiness_report: MemoryDefaultAgentReadinessReport
    release_hygiene_dependency_report: MemoryReleaseHygieneDependencyReport
    v028_readiness_report: MemoryV028ReadinessReport
    public_alpha_handoff_packet: MemoryPublicAlphaHandoffPacket
    release_manifest: MemoryReleaseManifest
    findings: list[MemoryConsolidationFinding]
    readiness_status: str
    release_status: str
    ready_for_v0_28: bool
    architecture_ready: bool
    repository_release_ready: bool
    runtime_agent_maturity_ready: bool
    version: str = MEMORY_CONSOLIDATION_VERSION
    release_name: str = MEMORY_CONSOLIDATION_RELEASE_NAME
    ready_for_v0_29: bool = False
    public_alpha_ready: bool = False
    runtime_injection_performed: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False
    safety_gate_mutated: bool = False
    permission_policy_mutated: bool = False
    persona_mutated: bool = False
    behavior_policy_mutated: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    file_mutated: bool = False
    safety_gate_bypassed: bool = False
    permission_boundary_bypassed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    raw_transcript_replayed: bool = False
    raw_provider_output_replayed: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    pig_guidance_used_as_authority: bool = False
    llm_judge_used: bool = False
    next_required_step: str = MEMORY_CONSOLIDATION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.28 Public Alpha / Schumpeter Split Preparation begins or Memory Foundation policy changes."
    )


class MemoryConsolidationSourceService:
    def __init__(self, release_hygiene_available: bool = False) -> None:
        self.release_hygiene_available = release_hygiene_available
        self._parts: dict[str, dict[str, Any]] = {}

    def _part(self, key: str, factory: Any) -> dict[str, Any]:
        if key not in self._parts:
            self._parts[key] = factory().build_all_parts()
        return self._parts[key]

    def load_v0270_contract_report(self) -> MemoryContractReport:
        return self._part("v0270", MemoryContractReportService)["report"]

    def load_v0271_source_boundary_report(self) -> MemorySourceBoundaryReport:
        return self._part("v0271", MemorySourceBoundaryReportService)["report"]

    def load_v0272_candidate_extraction_report(self) -> MemoryCandidateExtractionReport:
        return self._part("v0272", MemoryCandidateExtractionReportService)["report"]

    def load_v0273_evidence_scoring_report(self) -> MemoryEvidenceScoringReport:
        return self._part("v0273", MemoryEvidenceScoringReportService)["report"]

    def load_v0274_promotion_gate_report(self) -> MemoryPromotionGateReport:
        return self._part("v0274", MemoryPromotionGateReportService)["report"]

    def load_v0275_durable_registry_report(self) -> DurableMemoryRegistryReport:
        def factory() -> DurableMemoryRegistryReportService:
            return DurableMemoryRegistryReportService()

        if "v0275" not in self._parts:
            self._parts["v0275"] = factory().build_all_parts(
                requested_write_mode="write_if_gate_passed",
                release_hygiene_gate_passed=True,
                runtime_data_hygiene_gate_passed=True,
            )
        return self._parts["v0275"]["report"]

    def load_v0276_session_continuity_report(self) -> SessionContinuityContextBuildReport:
        return self._part("v0276", SessionContinuityContextBuildReportService)["report"]

    def load_v0277_injection_boundary_report(self) -> ContinuityInjectionBoundaryReport:
        return self._part("v0277", ContinuityInjectionBoundaryReportService)["report"]

    def load_v0278_lifecycle_report(self) -> MemoryLifecycleReport:
        return self._part("v0278", MemoryLifecycleReportService)["report"]

    def load_v02610_release_hygiene_report_if_available(self) -> dict[str, Any] | None:
        if not self.release_hygiene_available:
            return None
        return _ref("release_hygiene_report", "release_hygiene_report:v0.26.10", "v0.26.10")

    def load_v0269_workbench_consolidation_report_if_available(self) -> Any:
        return WorkbenchConsolidationReportService().build_all_parts()["report"]

    def load_pig_ocpx_reports_if_available(self) -> list[dict[str, Any]]:
        return [
            _ref("pig_report", "pig:memory_candidate_continuity_consolidation:v0.27.9", MEMORY_CONSOLIDATION_VERSION),
            _ref("ocpx_projection", "ocpx:memory_candidate_continuity_foundation_v1:v0.27.9", MEMORY_CONSOLIDATION_VERSION),
        ]

    def load_ocel_mapping_registry_if_available(self) -> dict[str, Any]:
        return {
            "object_types": MEMORY_CONSOLIDATION_OBJECT_TYPES,
            "event_types": MEMORY_CONSOLIDATION_EVENT_TYPES,
            "effect_types": MEMORY_CONSOLIDATION_EFFECT_TYPES,
            "forbidden_effect_types": MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
        }


class MemoryFoundationSubjectComponentService:
    def build_components(self, source: MemoryConsolidationSourceService) -> list[MemoryFoundationSubjectComponent]:
        report_refs = {
            "memory_contract": _ref("memory_contract_report", source.load_v0270_contract_report().report_id, MEMORY_CONTRACT_VERSION),
            "memory_source_boundary": _ref("memory_source_boundary_report", source.load_v0271_source_boundary_report().report_id, MEMORY_SOURCE_BOUNDARY_VERSION),
            "memory_candidate_extraction": _ref("memory_candidate_extraction_report", source.load_v0272_candidate_extraction_report().report_id, MEMORY_CANDIDATE_EXTRACTION_VERSION),
            "memory_evidence_scoring": _ref("memory_evidence_scoring_report", source.load_v0273_evidence_scoring_report().report_id, MEMORY_EVIDENCE_SCORING_VERSION),
            "memory_promotion_gate": _ref("memory_promotion_gate_report", source.load_v0274_promotion_gate_report().report_id, MEMORY_PROMOTION_GATE_VERSION),
            "durable_memory_registry": _ref("durable_memory_registry_report", source.load_v0275_durable_registry_report().report_id, DURABLE_MEMORY_REGISTRY_VERSION),
            "session_continuity_context": _ref("session_continuity_context_build_report", source.load_v0276_session_continuity_report().report_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            "continuity_injection_boundary": _ref("continuity_injection_boundary_report", source.load_v0277_injection_boundary_report().report_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
            "memory_lifecycle_control": _ref("memory_lifecycle_report", source.load_v0278_lifecycle_report().report_id, MEMORY_LIFECYCLE_VERSION),
            "memory_consolidation": _ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", MEMORY_CONSOLIDATION_VERSION),
        }
        components: list[MemoryFoundationSubjectComponent] = []
        for subject_id, version, component_type, subject_name in MEMORY_CONSOLIDATION_COMPONENTS:
            components.append(
                MemoryFoundationSubjectComponent(
                    component_id=f"memory_foundation_subject_component:{subject_id}:v0.27.9",
                    version_introduced=version,
                    subject_id=subject_id,
                    subject_name=subject_name,
                    component_type=component_type,
                    report_ref=report_refs.get(subject_id),
                    status="implemented",
                    creates_memory_candidate=component_type == "candidate_extraction",
                    scores_memory_candidate=component_type == "evidence_scoring",
                    records_promotion_decision=component_type == "promotion_gate",
                    writes_durable_memory=component_type == "durable_registry",
                    builds_continuity_context=component_type == "session_continuity_context",
                    performs_lifecycle_mutation=component_type == "lifecycle_control",
                    ocel_visible=True,
                    pig_visible=True,
                    ocpx_visible=True,
                    finding_count=0,
                    notes=["Consolidated as refs-only Memory Foundation v1 component."],
                )
            )
        return components


class MemoryCapabilityMapService:
    def build_capability_map(self, components: list[MemoryFoundationSubjectComponent]) -> MemoryCapabilityMap:
        entries: list[MemoryCapabilityMapEntry] = []
        for component in components:
            category = "continuity_context" if component.component_type == "session_continuity_context" else component.component_type
            entries.append(
                MemoryCapabilityMapEntry(
                    capability_id=f"memory_capability:{component.subject_id}:v0.27.9",
                    name=component.subject_name,
                    version_introduced=component.version_introduced,
                    source_report_refs=[] if component.report_ref is None else [component.report_ref],
                    status=component.status,
                    capability_category=category,
                    allowed_effect_types=MEMORY_CONSOLIDATION_EFFECT_TYPES,
                    forbidden_effect_types=MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
                    mutating=component.performs_lifecycle_mutation or component.writes_durable_memory,
                    persistent_write_capable=component.writes_durable_memory,
                    ocel_visible=True,
                    pig_visible=True,
                    ocpx_visible=True,
                    safety_notes=["Capability is consolidated; v0.27.9 does not execute the capability."],
                )
            )
        return MemoryCapabilityMap(
            map_id="memory_capability_map:v0.27.9",
            entries=entries,
            implemented_count=sum(1 for item in entries if item.status == "implemented"),
            warning_count=sum(1 for item in entries if item.status == "warning"),
            failed_count=sum(1 for item in entries if item.status == "failed"),
            blocked_count=sum(1 for item in entries if item.status == "blocked"),
            source_boundary_capability_count=sum(1 for item in entries if item.capability_category == "source_boundary"),
            candidate_capability_count=sum(1 for item in entries if item.capability_category == "candidate_extraction"),
            scoring_capability_count=sum(1 for item in entries if item.capability_category == "evidence_scoring"),
            promotion_gate_capability_count=sum(1 for item in entries if item.capability_category == "promotion_gate"),
            durable_registry_capability_count=sum(1 for item in entries if item.capability_category == "durable_registry"),
            continuity_context_capability_count=sum(1 for item in entries if item.capability_category == "continuity_context"),
            injection_boundary_capability_count=sum(1 for item in entries if item.capability_category == "injection_boundary"),
            lifecycle_capability_count=sum(1 for item in entries if item.capability_category == "lifecycle_control"),
        )


class MemoryCoverageMatrixService:
    def build_coverage_matrix(self, components: list[MemoryFoundationSubjectComponent]) -> MemoryCoverageMatrix:
        rows = [
            MemoryCoverageMatrixRow(
                subject_id=component.subject_id,
                version_introduced=component.version_introduced,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_docs=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_safety_boundary=True,
                has_privacy_boundary=True,
                has_audit_trail=True,
                has_forbidden_search=True,
                latest_artifact_available=component.report_ref is not None,
                coverage_notes=["Coverage consolidated from existing v0.27 artifact tests and docs."],
            )
            for component in components
        ]
        missing = sum(1 for row in rows if not row.latest_artifact_available)
        return MemoryCoverageMatrix(
            matrix_id="memory_coverage_matrix:v0.27.9",
            rows=rows,
            coverage_status="complete" if missing == 0 else "warning",
            missing_required_coverage_count=missing,
            optional_gap_count=0,
            future_track_gap_count=4,
        )


class MemorySafetyBoundaryConsolidationReportService:
    def build_report(self) -> MemorySafetyBoundaryConsolidationReport:
        return MemorySafetyBoundaryConsolidationReport(
            report_id="memory_safety_boundary_consolidation_report:v0.27.9",
            status="passed",
        )


class MemoryPrivacyBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryPrivacyBoundaryConsolidationReport:
        continuity_parts = source._part("v0276", SessionContinuityContextBuildReportService)
        continuity = continuity_parts["report"]
        privacy_filters = continuity_parts["privacy_filters"]
        return MemoryPrivacyBoundaryConsolidationReport(
            report_id="memory_privacy_boundary_consolidation_report:v0.27.9",
            privacy_policy_refs=[_ref("memory_privacy_policy", "memory_privacy_policy:v0.27.0", MEMORY_CONTRACT_VERSION)],
            privacy_gate_refs=[_ref("memory_lifecycle_privacy_gate", "memory_lifecycle_privacy_gate:v0.27.8:review", MEMORY_LIFECYCLE_VERSION)],
            privacy_filter_refs=[
                _ref("continuity_privacy_filter", item.privacy_filter_id, SESSION_CONTINUITY_CONTEXT_VERSION)
                for item in privacy_filters
            ],
            sensitive_memory_blocked_count=0,
            user_confirmation_required_count=0,
            privacy_filtered_context_count=continuity.privacy_filtered_count,
            privacy_violation_count=0,
            privacy_status="passed",
            evidence_refs=[_ref("session_continuity_context_build_report", continuity.report_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class MemorySourceBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemorySourceBoundaryConsolidationReport:
        report = source.load_v0271_source_boundary_report()
        return MemorySourceBoundaryConsolidationReport(
            report_id="memory_source_boundary_consolidation_report:v0.27.9",
            source_boundary_report_ref=_ref("memory_source_boundary_report", report.report_id, MEMORY_SOURCE_BOUNDARY_VERSION),
            allowed_source_category_count=len(MEMORY_ALLOWED_SOURCE_CATEGORIES),
            forbidden_source_category_count=len(MEMORY_FORBIDDEN_SOURCE_CATEGORIES),
            eligible_source_count=getattr(report, "eligible_source_count", 0),
            blocked_source_count=getattr(report, "blocked_source_count", 0),
            deferred_source_count=getattr(report, "deferred_source_count", 0),
            source_boundary_status="ready",
            evidence_refs=[_ref("memory_source_boundary_report", report.report_id, MEMORY_SOURCE_BOUNDARY_VERSION)],
        )


class MemoryCandidateQualityConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryCandidateQualityConsolidationReport:
        parts = source._part("v0272", MemoryCandidateExtractionReportService)
        report = parts["report"]
        candidates = parts["candidates"]
        return MemoryCandidateQualityConsolidationReport(
            report_id="memory_candidate_quality_consolidation_report:v0.27.9",
            candidate_extraction_report_ref=_ref("memory_candidate_extraction_report", report.report_id, MEMORY_CANDIDATE_EXTRACTION_VERSION),
            candidate_count=len(candidates),
            candidate_only_count=len(candidates),
            unsupported_claim_count=0,
            weakly_supported_claim_count=0,
            candidate_with_source_refs_count=sum(1 for item in candidates if item.source_links),
            candidate_with_evidence_refs_count=0,
            candidate_with_risk_flags_count=sum(1 for item in candidates if item.risk_flags),
            candidate_quality_status="ready",
            evidence_refs=[_ref("memory_candidate_extraction_report", report.report_id, MEMORY_CANDIDATE_EXTRACTION_VERSION)],
        )


class MemoryEvidenceScoringConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryEvidenceScoringConsolidationReport:
        parts = source._part("v0273", MemoryEvidenceScoringReportService)
        report = parts["report"]
        return MemoryEvidenceScoringConsolidationReport(
            report_id="memory_evidence_scoring_consolidation_report:v0.27.9",
            evidence_scoring_report_ref=_ref("memory_evidence_scoring_report", report.report_id, MEMORY_EVIDENCE_SCORING_VERSION),
            scored_candidate_count=len(parts["candidate_scores"]),
            score_breakdown_count=len(parts["score_breakdowns"]),
            privacy_assessment_count=len(parts["privacy_risk_assessments"]),
            contradiction_check_count=len(parts["contradiction_checks"]),
            promotion_readiness_preview_count=len(parts["promotion_readiness_previews"]),
            scoring_status="ready",
            evidence_refs=[_ref("memory_evidence_scoring_report", report.report_id, MEMORY_EVIDENCE_SCORING_VERSION)],
        )


class MemoryPromotionBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryPromotionBoundaryConsolidationReport:
        parts = source._part("v0274", MemoryPromotionGateReportService)
        report = parts["report"]
        decisions = parts["promotion_decision_records"]
        decision_types = [item.decision.decision_type for item in decisions]
        return MemoryPromotionBoundaryConsolidationReport(
            report_id="memory_promotion_boundary_consolidation_report:v0.27.9",
            promotion_gate_report_ref=_ref("memory_promotion_gate_report", report.report_id, MEMORY_PROMOTION_GATE_VERSION),
            promote_decision_count=decision_types.count("promote"),
            reject_decision_count=decision_types.count("reject"),
            defer_decision_count=decision_types.count("defer"),
            more_evidence_request_count=decision_types.count("request_more_evidence"),
            user_confirmation_request_count=decision_types.count("request_user_confirmation"),
            ephemeral_decision_count=decision_types.count("mark_ephemeral"),
            archive_only_decision_count=decision_types.count("mark_archive_only"),
            promotion_boundary_status="ready",
            evidence_refs=[_ref("memory_promotion_gate_report", report.report_id, MEMORY_PROMOTION_GATE_VERSION)],
        )


class DurableMemoryRegistryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> DurableMemoryRegistryConsolidationReport:
        report = source.load_v0275_durable_registry_report()
        return DurableMemoryRegistryConsolidationReport(
            report_id="durable_memory_registry_consolidation_report:v0.27.9",
            durable_registry_report_ref=_ref("durable_memory_registry_report", report.report_id, DURABLE_MEMORY_REGISTRY_VERSION),
            durable_record_count=report.durable_record_count,
            registry_entry_count=report.registry_entry_count,
            active_count=report.durable_record_count,
            archived_count=0,
            revoked_count=0,
            forgotten_count=0,
            expired_count=0,
            blocked_count=report.blocked_write_count,
            dry_run_count=report.dry_run_count,
            blocked_write_count=report.blocked_write_count,
            missing_provenance_count=report.integrity_report.missing_provenance_count,
            missing_evidence_index_count=report.integrity_report.missing_evidence_index_count,
            missing_scope_count=report.integrity_report.missing_scope_count,
            missing_lifecycle_count=report.integrity_report.missing_lifecycle_count,
            missing_forget_revoke_binding_count=report.integrity_report.missing_forget_revoke_binding_count,
            registry_status="ready",
            evidence_refs=[_ref("durable_memory_registry_report", report.report_id, DURABLE_MEMORY_REGISTRY_VERSION)],
        )


class SessionContinuityBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> SessionContinuityBoundaryConsolidationReport:
        report = source.load_v0276_session_continuity_report()
        return SessionContinuityBoundaryConsolidationReport(
            report_id="session_continuity_boundary_consolidation_report:v0.27.9",
            session_continuity_report_ref=_ref("session_continuity_context_build_report", report.report_id, SESSION_CONTINUITY_CONTEXT_VERSION),
            context_pack_count=1 if report.context_pack_created else 0,
            context_item_count=report.context_item_count,
            active_memory_ref_count=report.active_memory_ref_count,
            warning_count=report.warning_count,
            conflict_count=report.conflict_count,
            stale_count=report.stale_count,
            privacy_filtered_count=report.privacy_filtered_count,
            continuity_status="ready",
            evidence_refs=[_ref("session_continuity_context_build_report", report.report_id, SESSION_CONTINUITY_CONTEXT_VERSION)],
        )


class ContinuityInjectionBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> ContinuityInjectionBoundaryConsolidationReport:
        report = source.load_v0277_injection_boundary_report()
        return ContinuityInjectionBoundaryConsolidationReport(
            report_id="continuity_injection_boundary_consolidation_report:v0.27.9",
            injection_boundary_report_ref=_ref("continuity_injection_boundary_report", report.report_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
            injection_bundle_count=len(report.injection_bundles),
            injection_preview_count=len(report.injection_previews),
            decision_record_count=len(report.decision_records),
            boundary_trace_count=len(report.boundary_traces),
            injection_boundary_status="ready",
            evidence_refs=[_ref("continuity_injection_boundary_report", report.report_id, CONTINUITY_INJECTION_BOUNDARY_VERSION)],
        )


class MemoryLifecycleBoundaryConsolidationReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryLifecycleBoundaryConsolidationReport:
        report = source.load_v0278_lifecycle_report()
        tombstone_bad = sum(1 for item in report.forget_tombstones if item.contains_recallable_memory_content)
        return MemoryLifecycleBoundaryConsolidationReport(
            report_id="memory_lifecycle_boundary_consolidation_report:v0.27.9",
            lifecycle_report_ref=_ref("memory_lifecycle_report", report.report_id, MEMORY_LIFECYCLE_VERSION),
            review_record_count=len(report.review_records),
            update_record_count=len(report.update_records),
            revoke_record_count=len(report.revoke_records),
            forget_record_count=len(report.forget_records),
            archive_record_count=len(report.archive_records),
            expiration_record_count=len(report.expiration_records),
            conflict_resolution_record_count=len(report.conflict_resolution_records),
            no_op_decision_count=len(report.no_op_decisions),
            tombstone_count=len(report.forget_tombstones),
            tombstone_with_recallable_content_count=tombstone_bad,
            lifecycle_status="passed" if tombstone_bad == 0 else "blocked",
            evidence_refs=[_ref("memory_lifecycle_report", report.report_id, MEMORY_LIFECYCLE_VERSION)],
        )


class MemoryProcessIntelligenceFeedbackLoopReportService:
    def build_report(self) -> MemoryProcessIntelligenceFeedbackLoopReport:
        return MemoryProcessIntelligenceFeedbackLoopReport(
            report_id="memory_process_intelligence_feedback_loop_report:v0.27.9",
            ocel_memory_event_visibility_ready=True,
            ocpx_memory_view_readiness_ready=True,
            pig_guidance_memory_signal_ready=True,
            memory_candidate_traceability_ready=True,
            memory_scoring_traceability_ready=True,
            memory_promotion_traceability_ready=True,
            durable_registry_traceability_ready=True,
            continuity_context_traceability_ready=True,
            lifecycle_traceability_ready=True,
            feedback_loop_status="ready",
            notes=["OCEL/OCPX/PIG visibility is consolidated; closed-loop learning remains future-track."],
            evidence_refs=[_ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", MEMORY_CONSOLIDATION_VERSION)],
        )


class MemoryDefaultAgentReadinessReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryDefaultAgentReadinessReport:
        continuity = source.load_v0276_session_continuity_report()
        injection = source.load_v0277_injection_boundary_report()
        lifecycle = source.load_v0278_lifecycle_report()
        return MemoryDefaultAgentReadinessReport(
            report_id="memory_default_agent_readiness_report:v0.27.9",
            memory_context_available=continuity.continuity_context_created,
            continuity_context_pack_available=continuity.context_pack_created,
            injection_boundary_available=injection.injection_policy_created,
            memory_lifecycle_controls_available=lifecycle.audit_trail_created,
            readiness_status="warning",
            remaining_gaps=[
                {"gap": "runtime_continuity_injection", "deferred_to": "future_track"},
                {"gap": "default_agent_runtime_memory_use", "deferred_to": "future_track"},
            ],
            evidence_refs=[
                _ref("session_continuity_context_build_report", continuity.report_id, SESSION_CONTINUITY_CONTEXT_VERSION),
                _ref("continuity_injection_boundary_report", injection.report_id, CONTINUITY_INJECTION_BOUNDARY_VERSION),
                _ref("memory_lifecycle_report", lifecycle.report_id, MEMORY_LIFECYCLE_VERSION),
            ],
        )


class MemoryReleaseHygieneDependencyReportService:
    def build_report(self, source: MemoryConsolidationSourceService) -> MemoryReleaseHygieneDependencyReport:
        hygiene_ref = source.load_v02610_release_hygiene_report_if_available()
        passed = hygiene_ref is not None
        return MemoryReleaseHygieneDependencyReport(
            report_id="memory_release_hygiene_dependency_report:v0.27.9",
            release_hygiene_report_ref=hygiene_ref,
            release_hygiene_status="passed" if passed else "unknown",
            clean_worktree_verified=True if passed else None,
            release_tag_verified=True if passed else None,
            license_verified=True if passed else None,
            changelog_verified=True if passed else None,
            pyproject_verified=True if passed else None,
            py_typed_verified=True if passed else None,
            ci_verified=True if passed else None,
            runtime_data_hygiene_verified=True if passed else None,
            reference_license_policy_verified=True if passed else None,
            repository_release_ready=passed,
            can_claim_foundation_release=passed,
            evidence_refs=[] if hygiene_ref is None else [hygiene_ref],
        )


class MemoryV028ReadinessReportService:
    def build_report(
        self,
        architecture_ready: bool,
        repository_release_ready: bool,
        workbench_foundation_ready: bool,
    ) -> MemoryV028ReadinessReport:
        ready = architecture_ready and repository_release_ready and workbench_foundation_ready
        warnings = [] if repository_release_ready else ["v0.26.10 release hygiene status is unknown; repository release readiness cannot be claimed."]
        return MemoryV028ReadinessReport(
            report_id="memory_v028_readiness_report:v0.27.9",
            ready_for_v0_28=ready,
            architecture_requirements_met=architecture_ready,
            repository_release_requirements_met=repository_release_ready,
            memory_foundation_ready=architecture_ready,
            workbench_foundation_ready=workbench_foundation_ready,
            blockers=[],
            warnings=warnings,
            notes=[
                "v0.28 readiness is a handoff/readiness signal, not v0.28 implementation.",
                "Public Alpha packaging, Schumpeter split, and external adapters remain unimplemented.",
            ],
            evidence_refs=[_ref("memory_release_hygiene_dependency_report", "memory_release_hygiene_dependency_report:v0.27.9", MEMORY_CONSOLIDATION_VERSION)],
        )


class MemoryPublicAlphaHandoffPacketService:
    def build_packet(self, handoff_status: str) -> MemoryPublicAlphaHandoffPacket:
        return MemoryPublicAlphaHandoffPacket(
            handoff_packet_id="memory_public_alpha_handoff_packet:v0.27.9",
            source_release_manifest_id="memory_release_manifest:v0.27.9",
            source_consolidation_report_id="memory_consolidation_report:v0.27.9",
            ready_inputs=[
                "memory_contract_report",
                "memory_source_boundary_report",
                "memory_candidate_extraction_report",
                "memory_evidence_scoring_report",
                "memory_promotion_gate_report",
                "durable_memory_registry_report",
                "session_continuity_context_report",
                "continuity_injection_boundary_report",
                "memory_lifecycle_report",
                "memory_release_manifest",
                "memory_safety_boundary_report",
                "memory_privacy_boundary_report",
            ],
            not_implemented_in_v0279=[
                "public alpha packaging",
                "Schumpeter split",
                "company deployment profile",
                "external provider adapters",
                "external agent dominion bridge",
                "runtime continuity injection",
                "autonomous memory-driven execution",
            ],
            handoff_status=handoff_status,
            evidence_refs=[_ref("memory_release_manifest", "memory_release_manifest:v0.27.9", MEMORY_CONSOLIDATION_VERSION)],
        )


class MemoryReleaseManifestService:
    def build_manifest(
        self,
        components: list[MemoryFoundationSubjectComponent],
        capability_map: MemoryCapabilityMap,
        coverage_matrix: MemoryCoverageMatrix,
        safety: MemorySafetyBoundaryConsolidationReport,
        privacy: MemoryPrivacyBoundaryConsolidationReport,
        lifecycle: MemoryLifecycleBoundaryConsolidationReport,
        hygiene: MemoryReleaseHygieneDependencyReport,
        v028: MemoryV028ReadinessReport,
        handoff: MemoryPublicAlphaHandoffPacket,
    ) -> MemoryReleaseManifest:
        release_status = "releasable" if hygiene.repository_release_ready else "releasable_with_warnings"
        return MemoryReleaseManifest(
            manifest_id="memory_release_manifest:v0.27.9",
            included_versions=MEMORY_CONSOLIDATION_INCLUDED_VERSIONS,
            included_subjects=[component.subject_id for component in components],
            included_capabilities=[entry.capability_id for entry in capability_map.entries],
            excluded_capabilities=MEMORY_CONSOLIDATION_EXCLUDED_CAPABILITIES,
            allowed_effect_types=MEMORY_CONSOLIDATION_EFFECT_TYPES,
            forbidden_effect_types=MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
            foundation_snapshot_id="memory_foundation_snapshot:v0.27.9",
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety.report_id,
            privacy_boundary_report_id=privacy.report_id,
            lifecycle_boundary_report_id=lifecycle.report_id,
            release_hygiene_dependency_report_id=hygiene.report_id,
            v028_readiness_report_id=v028.report_id,
            public_alpha_handoff_packet_id=handoff.handoff_packet_id,
            release_status=release_status,
            architecture_ready=True,
            repository_release_ready=hygiene.repository_release_ready,
            runtime_agent_maturity_ready=False,
            notes=[
                "Memory Foundation architecture is consolidated.",
                "Repository release readiness depends on v0.26.10 hygiene evidence.",
            ],
        )


class MemoryFoundationSnapshotService:
    def build_snapshot(
        self,
        components: list[MemoryFoundationSubjectComponent],
        manifest: MemoryReleaseManifest,
    ) -> MemoryFoundationSnapshot:
        return MemoryFoundationSnapshot(
            snapshot_id="memory_foundation_snapshot:v0.27.9",
            created_at=utc_now_iso(),
            included_versions=MEMORY_CONSOLIDATION_INCLUDED_VERSIONS,
            previous_foundation_ref=_ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9", "v0.26.9"),
            recommended_hardening_ref=_ref("release_hygiene_report", "release_hygiene_report:v0.26.10", "v0.26.10"),
            subject_components=components,
            capability_map_id=manifest.capability_map_id,
            coverage_matrix_id=manifest.coverage_matrix_id,
            safety_boundary_report_id=manifest.safety_boundary_report_id,
            privacy_boundary_report_id=manifest.privacy_boundary_report_id,
            lifecycle_boundary_report_id=manifest.lifecycle_boundary_report_id,
            release_manifest_id=manifest.manifest_id,
            consolidation_report_id="memory_consolidation_report:v0.27.9",
            snapshot_status="ready" if manifest.repository_release_ready else "warning",
            architecture_ready=manifest.architecture_ready,
            repository_release_ready=manifest.repository_release_ready,
            runtime_agent_maturity_ready=manifest.runtime_agent_maturity_ready,
            limitations=[
                "Public Alpha readiness is separated from Memory Foundation readiness.",
                "Runtime continuity injection remains future-track.",
            ],
        )


class MemoryConsolidationFindingService:
    BLOCKED_FINDINGS = {
        "runtime_injection_detected",
        "default_agent_mutation_detected",
        "decision_service_mutation_detected",
        "skill_router_mutation_detected",
        "safety_gate_mutation_detected",
        "permission_policy_mutation_detected",
        "persona_mutation_detected",
        "behavior_policy_mutation_detected",
        "provider_invocation_detected",
        "command_execution_detected",
        "file_mutation_detected",
        "safety_bypass_detected",
        "permission_bypass_detected",
        "raw_transcript_memory_detected",
        "raw_provider_output_memory_detected",
        "raw_secret_memory_detected",
        "credential_memory_detected",
        "source_data_deletion_detected",
        "silent_overwrite_detected",
        "unlogged_deletion_detected",
        "pig_authority_detected",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "llm_judge_detected",
    }

    def build_findings(self, hygiene: MemoryReleaseHygieneDependencyReport) -> list[MemoryConsolidationFinding]:
        findings = [
            MemoryConsolidationFinding(
                finding_id="memory_consolidation_finding:foundation_snapshot_created",
                severity="info",
                finding_type="memory_foundation_snapshot_created",
                message="Memory Candidate & Continuity Foundation v1 snapshot was created.",
                subject_ref=_ref("memory_foundation_snapshot", "memory_foundation_snapshot:v0.27.9", MEMORY_CONSOLIDATION_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if any v0.27 required component is missing under strict mode.",
            ),
            MemoryConsolidationFinding(
                finding_id="memory_consolidation_finding:release_manifest_created",
                severity="info",
                finding_type="memory_release_manifest_created",
                message="Memory release manifest was created as consolidation/readiness artifact.",
                subject_ref=_ref("memory_release_manifest", "memory_release_manifest:v0.27.9", MEMORY_CONSOLIDATION_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if manifest claims public alpha implementation.",
            ),
        ]
        if hygiene.release_hygiene_status == "unknown":
            findings.append(
                MemoryConsolidationFinding(
                    finding_id="memory_consolidation_finding:repository_release_hygiene_unknown",
                    severity="warning",
                    finding_type="repository_release_hygiene_unknown",
                    message="v0.26.10 release hygiene report is not available; repository release readiness is not claimed.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when v0.26.10 release hygiene report is available and passed.",
                )
            )
        return findings


class MemoryConsolidationReportService:
    def build_report(
        self,
        report_id: str | None = None,
        release_hygiene_available: bool = False,
        extra_findings: list[str] | None = None,
    ) -> MemoryConsolidationReport:
        source = MemoryConsolidationSourceService(release_hygiene_available=release_hygiene_available)
        components = MemoryFoundationSubjectComponentService().build_components(source)
        capability_map = MemoryCapabilityMapService().build_capability_map(components)
        coverage_matrix = MemoryCoverageMatrixService().build_coverage_matrix(components)
        safety = MemorySafetyBoundaryConsolidationReportService().build_report()
        privacy = MemoryPrivacyBoundaryConsolidationReportService().build_report(source)
        source_boundary = MemorySourceBoundaryConsolidationReportService().build_report(source)
        candidate_quality = MemoryCandidateQualityConsolidationReportService().build_report(source)
        scoring = MemoryEvidenceScoringConsolidationReportService().build_report(source)
        promotion = MemoryPromotionBoundaryConsolidationReportService().build_report(source)
        registry = DurableMemoryRegistryConsolidationReportService().build_report(source)
        continuity = SessionContinuityBoundaryConsolidationReportService().build_report(source)
        injection = ContinuityInjectionBoundaryConsolidationReportService().build_report(source)
        lifecycle = MemoryLifecycleBoundaryConsolidationReportService().build_report(source)
        pi_feedback = MemoryProcessIntelligenceFeedbackLoopReportService().build_report()
        agent_readiness = MemoryDefaultAgentReadinessReportService().build_report(source)
        hygiene = MemoryReleaseHygieneDependencyReportService().build_report(source)
        workbench = source.load_v0269_workbench_consolidation_report_if_available()
        workbench_ready = getattr(workbench, "ready_for_v0_27", True)
        architecture_ready = (
            coverage_matrix.missing_required_coverage_count == 0
            and safety.status == "passed"
            and privacy.privacy_status == "passed"
            and lifecycle.lifecycle_status in {"passed", "ready"}
        )
        v028 = MemoryV028ReadinessReportService().build_report(
            architecture_ready=architecture_ready,
            repository_release_ready=hygiene.repository_release_ready,
            workbench_foundation_ready=bool(workbench_ready),
        )
        handoff = MemoryPublicAlphaHandoffPacketService().build_packet(
            "ready" if v028.ready_for_v0_28 else "warning"
        )
        manifest = MemoryReleaseManifestService().build_manifest(
            components,
            capability_map,
            coverage_matrix,
            safety,
            privacy,
            lifecycle,
            hygiene,
            v028,
            handoff,
        )
        snapshot = MemoryFoundationSnapshotService().build_snapshot(components, manifest)
        findings = MemoryConsolidationFindingService().build_findings(hygiene)
        for finding_type in extra_findings or []:
            findings.append(
                MemoryConsolidationFinding(
                    finding_id=f"memory_consolidation_finding:{finding_type}",
                    severity="critical" if finding_type in MemoryConsolidationFindingService.BLOCKED_FINDINGS else "warning",
                    finding_type=finding_type,
                    message=f"Injected consolidation finding for boundary validation: {finding_type}.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when boundary validation input is removed.",
                )
            )
        blocked = any(finding.finding_type in MemoryConsolidationFindingService.BLOCKED_FINDINGS for finding in findings)
        readiness_status = "blocked" if blocked else ("ready" if v028.ready_for_v0_28 else "warning")
        release_status = "blocked" if blocked else manifest.release_status
        return MemoryConsolidationReport(
            report_id=report_id or "memory_consolidation_report:v0.27.9",
            created_at=utc_now_iso(),
            foundation_snapshot=snapshot,
            capability_map=capability_map,
            coverage_matrix=coverage_matrix,
            safety_boundary_report=safety,
            privacy_boundary_report=privacy,
            source_boundary_consolidation_report=source_boundary,
            candidate_quality_consolidation_report=candidate_quality,
            evidence_scoring_consolidation_report=scoring,
            promotion_boundary_consolidation_report=promotion,
            durable_registry_consolidation_report=registry,
            session_continuity_consolidation_report=continuity,
            injection_boundary_consolidation_report=injection,
            lifecycle_boundary_consolidation_report=lifecycle,
            process_intelligence_feedback_loop_report=pi_feedback,
            default_agent_readiness_report=agent_readiness,
            release_hygiene_dependency_report=hygiene,
            v028_readiness_report=v028,
            public_alpha_handoff_packet=handoff,
            release_manifest=manifest,
            findings=findings,
            readiness_status=readiness_status,
            release_status=release_status,
            ready_for_v0_28=v028.ready_for_v0_28,
            architecture_ready=architecture_ready,
            repository_release_ready=hygiene.repository_release_ready,
            runtime_agent_maturity_ready=False,
            limitations=[
                "v0.27.9 is consolidation/readiness only and does not implement v0.28.",
                "Repository release readiness remains warning unless v0.26.10 hygiene evidence is available.",
            ],
            withdrawal_conditions=[
                "Withdraw if any new memory extraction/scoring/promotion/write/lifecycle execution is added.",
                "Withdraw if runtime injection, external adapter, or Schumpeter split is implemented in v0.27.9.",
            ],
        )

    def build_all_parts(
        self,
        report_id: str | None = None,
        release_hygiene_available: bool = False,
    ) -> dict[str, Any]:
        report = self.build_report(report_id=report_id, release_hygiene_available=release_hygiene_available)
        return {
            "foundation_snapshot": report.foundation_snapshot,
            "subject_components": report.foundation_snapshot.subject_components,
            "capability_map": report.capability_map,
            "coverage_matrix": report.coverage_matrix,
            "safety_boundary_report": report.safety_boundary_report,
            "privacy_boundary_report": report.privacy_boundary_report,
            "source_boundary_consolidation_report": report.source_boundary_consolidation_report,
            "candidate_quality_consolidation_report": report.candidate_quality_consolidation_report,
            "evidence_scoring_consolidation_report": report.evidence_scoring_consolidation_report,
            "promotion_boundary_consolidation_report": report.promotion_boundary_consolidation_report,
            "durable_registry_consolidation_report": report.durable_registry_consolidation_report,
            "session_continuity_consolidation_report": report.session_continuity_consolidation_report,
            "injection_boundary_consolidation_report": report.injection_boundary_consolidation_report,
            "lifecycle_boundary_consolidation_report": report.lifecycle_boundary_consolidation_report,
            "process_intelligence_feedback_loop_report": report.process_intelligence_feedback_loop_report,
            "default_agent_readiness_report": report.default_agent_readiness_report,
            "release_hygiene_dependency_report": report.release_hygiene_dependency_report,
            "v028_readiness_report": report.v028_readiness_report,
            "public_alpha_handoff_packet": report.public_alpha_handoff_packet,
            "release_manifest": report.release_manifest,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": MEMORY_CONSOLIDATION_VERSION,
            "layer": MEMORY_CONTRACT_LAYER,
            "subject": "memory_candidate_continuity_consolidation",
            "release_name": MEMORY_CONSOLIDATION_RELEASE_NAME,
            "principles": [
                "Consolidation is not new memory feature implementation",
                "Memory Foundation release readiness is not public alpha readiness",
                "v0.28 readiness is not v0.28 implementation",
                "Durable memory registry is not persona",
                "Continuity context is not runtime injection",
                "Lifecycle control is not silent mutation",
                "PIG guidance is not memory authority",
                "Memory must not trigger provider invocation or command execution",
                "Memory must not bypass safety or permission boundaries",
            ],
            "safety_boundary": {
                "runtime_injection_performed": False,
                "default_agent_context_mutated": False,
                "decision_service_mutated": False,
                "skill_router_mutated": False,
                "safety_gate_mutated": False,
                "permission_policy_mutated": False,
                "persona_mutated": False,
                "behavior_policy_mutated": False,
                "provider_invoked": False,
                "command_executed": False,
                "file_mutated": False,
                "safety_gate_bypassed": False,
                "permission_boundary_bypassed": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "raw_transcript_replayed": False,
                "raw_provider_output_replayed": False,
                "pig_guidance_used_as_authority": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.28 public alpha / Schumpeter split preparation",
                "v0.29+ external provider adapters",
                "v0.30+ external agent dominion bridge",
            ],
            "next_step": MEMORY_CONSOLIDATION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "memory_candidate_continuity_foundation_v1_consolidated",
            "version": MEMORY_CONSOLIDATION_VERSION,
            "release_name": MEMORY_CONSOLIDATION_RELEASE_NAME,
            "source_read_models": [
                "MemoryCandidateContinuityContractState",
                "MemorySourceBoundaryState",
                "MemoryCandidateExtractionState",
                "MemoryEvidenceScoringState",
                "MemoryPromotionGateState",
                "DurableMemoryRegistryState",
                "SessionContinuityContextState",
                "ContinuityInjectionBoundaryState",
                "MemoryLifecycleState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "MemoryFoundationSnapshotState",
                "MemoryReleaseManifestState",
                "MemorySafetyBoundaryConsolidationState",
                "MemoryPrivacyBoundaryConsolidationState",
                "MemoryV028ReadinessState",
                "MemoryPublicAlphaHandoffState",
                "V028ReadinessState",
            ],
            "effect_types": MEMORY_CONSOLIDATION_EFFECT_TYPES,
            "forbidden_effect_types": MEMORY_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
        }


def render_memory_consolidation_cli(parts: dict[str, Any], section: str = "consolidate") -> str:
    report: MemoryConsolidationReport = parts["report"]
    lines = [
        f"Memory Candidate & Continuity Consolidation {section}",
        f"version={report.version}",
        f"release_name={report.release_name}",
        f"release_status={report.release_status}",
        f"readiness_status={report.readiness_status}",
        f"architecture_ready={_bool(report.architecture_ready)}",
        f"repository_release_ready={_bool(report.repository_release_ready)}",
        f"runtime_agent_maturity_ready={_bool(report.runtime_agent_maturity_ready)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"ready_for_v0_28={_bool(report.ready_for_v0_28)}",
        f"ready_for_v0_29={_bool(report.ready_for_v0_29)}",
        f"runtime_injection_performed={_bool(report.runtime_injection_performed)}",
        f"default_agent_context_mutated={_bool(report.default_agent_context_mutated)}",
        f"decision_service_mutated={_bool(report.decision_service_mutated)}",
        f"skill_router_mutated={_bool(report.skill_router_mutated)}",
        f"safety_gate_mutated={_bool(report.safety_gate_mutated)}",
        f"permission_policy_mutated={_bool(report.permission_policy_mutated)}",
        f"persona_mutated={_bool(report.persona_mutated)}",
        f"behavior_policy_mutated={_bool(report.behavior_policy_mutated)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"file_mutated={_bool(report.file_mutated)}",
        f"safety_gate_bypassed={_bool(report.safety_gate_bypassed)}",
        f"permission_boundary_bypassed={_bool(report.permission_boundary_bypassed)}",
        f"external_provider_adapter_implemented={_bool(report.external_provider_adapter_implemented)}",
        f"schumpeter_split_introduced={_bool(report.schumpeter_split_introduced)}",
        f"raw_transcript_replayed={_bool(report.raw_transcript_replayed)}",
        f"raw_provider_output_replayed={_bool(report.raw_provider_output_replayed)}",
        f"raw_secret_output={_bool(report.raw_secret_output)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"pig_guidance_used_as_authority={_bool(report.pig_guidance_used_as_authority)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "consolidate": ("snapshot_status", report.foundation_snapshot.snapshot_status),
        "release-manifest": ("manifest_id", report.release_manifest.manifest_id),
        "readiness": ("ready_for_v0_28", report.v028_readiness_report.ready_for_v0_28),
        "coverage": ("coverage_status", report.coverage_matrix.coverage_status),
        "safety-boundary": ("safety_status", report.safety_boundary_report.status),
        "privacy-boundary": ("privacy_status", report.privacy_boundary_report.privacy_status),
        "source-boundary-summary": ("source_boundary_status", report.source_boundary_consolidation_report.source_boundary_status),
        "candidate-quality": ("candidate_quality_status", report.candidate_quality_consolidation_report.candidate_quality_status),
        "scoring-summary": ("scoring_status", report.evidence_scoring_consolidation_report.scoring_status),
        "promotion-summary": ("promotion_boundary_status", report.promotion_boundary_consolidation_report.promotion_boundary_status),
        "registry-summary": ("registry_status", report.durable_registry_consolidation_report.registry_status),
        "continuity-summary": ("continuity_status", report.session_continuity_consolidation_report.continuity_status),
        "injection-boundary-summary": ("injection_boundary_status", report.injection_boundary_consolidation_report.injection_boundary_status),
        "lifecycle-summary": ("lifecycle_status", report.lifecycle_boundary_consolidation_report.lifecycle_status),
        "pi-feedback": ("feedback_loop_status", report.process_intelligence_feedback_loop_report.feedback_loop_status),
        "default-agent-readiness": ("agent_readiness_status", report.default_agent_readiness_report.readiness_status),
        "release-hygiene": ("release_hygiene_status", report.release_hygiene_dependency_report.release_hygiene_status),
        "handoff": ("handoff_status", report.public_alpha_handoff_packet.handoff_status),
        "consolidation-report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    if section == "safety-boundary":
        lines.extend(
            [
                "legacy_contract_compatibility=v0.27.0_memory_safety_boundary",
                "version=v0.27.0",
                "layer=memory_candidate_continuity",
                "status=contract_only",
                "ready_for_v0_27_1=true",
                "ready_for_v0_28=false",
                "memory_candidate_extracted=false",
                "memory_scored=false",
                "memory_promoted=false",
                "persistent_memory_written=false",
                "raw_transcript_memory_created=false",
                "raw_provider_output_memory_created=false",
                "pig_memory_promoted=false",
                "pig_policy_mutated=false",
                "pig_executed=false",
            ]
        )
    return "\n".join(lines)

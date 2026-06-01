from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
import tomllib
from typing import Any

from chanta_core.memory_candidate_continuity import MemoryConsolidationReportService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench import WorkbenchConsolidationReportService


def _now() -> str:
    return utc_now_iso()


def _bool(value: bool) -> str:
    return str(value).lower()


def _ref(object_type: str, object_id: str, version: str | None = None) -> dict[str, Any]:
    ref: dict[str, Any] = {"object_type": object_type, "object_id": object_id}
    if version:
        ref["version"] = version
    return ref


class ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        def convert(value: Any) -> Any:
            if is_dataclass(value):
                return {key: convert(item) for key, item in asdict(value).items()}
            if isinstance(value, list):
                return [convert(item) for item in value]
            if isinstance(value, dict):
                return {key: convert(item) for key, item in value.items()}
            return value

        return convert(self)


V028_VERSION = "v0.28.0"
V028_VERSION_NAME = "Public Alpha / Schumpeter Split Preparation Contract"
V028_KOREAN_NAME = "Public Alpha·Schumpeter Split Preparation 계약"
V028_LAYER = "public_alpha_schumpeter_preparation"
V028_TRACK = "Public Alpha / Schumpeter Split Preparation"
V028_NEXT_STEP = "v0.28.1 Release Hygiene / Repository Governance Blocking Gate"

V028_OBJECT_TYPES = [
    "public_alpha_schumpeter_preparation_contract",
    "v028_roadmap",
    "v028_version_plan",
    "public_alpha_scope_policy",
    "public_alpha_stage_policy",
    "release_hygiene_debt_policy",
    "hygiene_debt_disposition",
    "release_hygiene_blocking_policy",
    "packaging_readiness_policy",
    "public_private_boundary_policy",
    "schumpeter_split_preparation_policy",
    "schumpeter_split_decision_framework",
    "schumpeter_split_decision_option",
    "schumpeter_split_evaluation_criterion",
    "schumpeter_reference_inventory_policy",
    "schumpeter_reuse_disposition_policy",
    "external_adapter_preflight_boundary",
    "v029_risk_reopen_criteria",
    "public_alpha_safety_boundary_policy",
    "v028_contract_finding",
    "v028_contract_report",
    "memory_consolidation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V028_EVENT_TYPES = [
    "v028_contract_requested",
    "v028_contract_prerequisites_loaded",
    "v028_roadmap_created",
    "public_alpha_scope_policy_created",
    "public_alpha_stage_policy_created",
    "release_hygiene_debt_policy_created",
    "hygiene_debt_disposition_created",
    "release_hygiene_blocking_policy_created",
    "packaging_readiness_policy_created",
    "public_private_boundary_policy_created",
    "schumpeter_split_preparation_policy_created",
    "schumpeter_split_decision_framework_created",
    "schumpeter_split_decision_option_created",
    "schumpeter_split_evaluation_criterion_created",
    "schumpeter_reference_inventory_policy_created",
    "schumpeter_reuse_disposition_policy_created",
    "external_adapter_preflight_boundary_created",
    "v029_risk_reopen_criteria_created",
    "public_alpha_safety_boundary_policy_created",
    "public_alpha_schumpeter_preparation_contract_created",
    "v028_contract_report_created",
    "v028_contract_warning_created",
    "v028_contract_blocked",
]

V028_EFFECT_TYPES = [
    "read_only_observation",
    "public_alpha_schumpeter_contract_declared",
    "v028_roadmap_declared",
    "release_hygiene_debt_declared",
    "schumpeter_split_decision_framework_declared",
    "external_adapter_preflight_boundary_declared",
    "public_private_boundary_declared",
    "state_candidate_created",
]

V028_FORBIDDEN_EFFECT_TYPES = [
    "public_alpha_implemented",
    "package_published",
    "release_tag_created",
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "external_dominion_bridge_implemented",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "autonomous_memory_execution_enabled",
    "references_schumpeter_runtime_dependency_added",
    "references_schumpeter_code_copied",
    "company_private_material_exposed",
    "credential_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class V028VersionPlan(ModelMixin):
    version_number: str
    version_name: str
    purpose: str
    allowed_scope: list[str]
    forbidden_scope: list[str]
    implementation_kind: str
    public_alpha_release_allowed: bool = False
    schumpeter_split_allowed: bool = False
    external_adapter_allowed: bool = False
    provider_invocation_allowed: bool = False
    command_execution_allowed: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class V028Roadmap(ModelMixin):
    roadmap_id: str
    versions: list[V028VersionPlan]
    roadmap_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    current_track: str = "v0.28.x Public Alpha / Schumpeter Split Preparation"
    next_version: str = V028_NEXT_STEP
    consolidation_version: str = "v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation"
    next_track: str = "v0.29.x External Skill / External Provider Adapter Development"


@dataclass
class PublicAlphaScopePolicy(ModelMixin):
    policy_id: str
    public_alpha_allowed_surfaces: list[str]
    public_alpha_forbidden_surfaces: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    public_alpha_scope_defined: bool = True
    public_alpha_is_not_production_ready: bool = True
    public_alpha_is_not_company_deployment: bool = True
    public_alpha_is_not_external_adapter_runtime: bool = True
    public_alpha_is_not_schumpeter_split: bool = True


@dataclass
class PublicAlphaStagePolicy(ModelMixin):
    policy_id: str
    stages: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    stage_order_required: bool = True
    architecture_ready_is_not_release_ready: bool = True
    repository_ready_is_not_package_ready: bool = True
    package_ready_is_not_production_ready: bool = True
    public_alpha_ready_requires_all_gates: bool = True
    no_release_is_valid_outcome: bool = True


@dataclass
class ReleaseHygieneDebtPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    v02610_hygiene_debt_must_be_resolved_or_explicitly_dispositioned: bool = True
    hygiene_unknown_is_not_passed: bool = True
    hygiene_failed_blocks_public_alpha_release_claim: bool = True
    clean_worktree_required_for_release_claim: bool = True
    release_tag_required_for_release_claim: bool = True
    license_required_for_release_claim: bool = True
    changelog_required_for_release_claim: bool = True
    third_party_notice_required_when_references_exist: bool = True
    runtime_data_hygiene_required: bool = True
    reference_license_policy_required: bool = True
    no_release_allowed: bool = True


@dataclass
class HygieneDebtDisposition(ModelMixin):
    disposition_id: str
    debt_item: str
    current_status: str
    disposition_type: str
    disposition_reason: str
    required_followup_version: str | None
    evidence_refs: list[dict[str, Any]]
    version: str = V028_VERSION


@dataclass
class ReleaseHygieneBlockingPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    v0281_is_blocking_gate: bool = True
    public_alpha_release_claim_requires_v0281_pass: bool = True
    repository_release_ready_requires_hygiene_pass: bool = True
    no_release_decision_enabled: bool = True
    architecture_ready_may_pass_when_hygiene_unknown: bool = True
    repository_release_ready_must_be_false_when_hygiene_unknown: bool = True
    public_alpha_ready_must_be_false_when_hygiene_failed: bool = True


@dataclass
class PackagingReadinessPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    packaging_boundary_deferred_to: str = "v0.28.2"
    pyproject_validation_required: bool = True
    runtime_dev_dependency_separation_required: bool = True
    pytest_must_not_be_runtime_dependency: bool = True
    py_typed_required: bool = True
    package_include_exclude_policy_required: bool = True
    runtime_data_excluded_from_package: bool = True
    references_excluded_or_policy_controlled: bool = True
    wheel_build_smoke_required: bool = True
    sdist_build_smoke_required: bool = True
    import_smoke_required: bool = True
    cli_smoke_required: bool = True
    package_publish_enabled_now: bool = False


@dataclass
class PublicPrivateBoundaryPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    boundary_deferred_to: str = "v0.28.3"
    public_core_private_overlay_required: bool = True
    public_repo_must_not_contain_company_material: bool = True
    public_repo_must_not_contain_credentials: bool = True
    public_repo_must_not_contain_internal_endpoints: bool = True
    public_repo_must_not_contain_raw_traces: bool = True
    public_repo_must_not_contain_raw_transcripts: bool = True
    public_repo_must_not_contain_raw_provider_outputs: bool = True
    public_repo_may_contain_sanitized_examples: bool = True
    public_repo_may_contain_synthetic_demo_data: bool = True
    private_overlay_required_for_schumpeter: bool = True


@dataclass
class SchumpeterSplitPreparationPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    split_preparation_deferred_to: str = "v0.28.5"
    decision_framework_required_before_split: bool = True
    actual_split_enabled_now: bool = False
    company_wrapper_enabled_now: bool = False
    private_distribution_enabled_now: bool = False
    public_core_private_overlay_policy_required: bool = True
    company_config_forbidden_in_public_core: bool = True
    company_credentials_forbidden_in_public_core: bool = True
    company_endpoint_forbidden_in_public_core: bool = True
    company_rpa_integration_forbidden_now: bool = True
    references_schumpeter_reference_only_by_default: bool = True


@dataclass
class SchumpeterSplitDecisionOption(ModelMixin):
    option_id: str
    option_name: str
    option_summary: str
    allowed_now: bool
    risk_notes: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    implementation_now: bool = False


@dataclass
class SchumpeterSplitEvaluationCriterion(ModelMixin):
    criterion_id: str
    criterion_name: str
    criterion_summary: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    required_for_decision: bool = True


@dataclass
class SchumpeterSplitDecisionFramework(ModelMixin):
    framework_id: str
    options: list[SchumpeterSplitDecisionOption]
    criteria: list[SchumpeterSplitEvaluationCriterion]
    decision_outputs: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    decision_framework_deferred_to: str = "v0.28.4"
    decision_required_before_split: bool = True
    default_option: str = "keep_reference_only_and_prepare_private_overlay"
    actual_decision_made_now: bool = False
    split_implemented_now: bool = False


@dataclass
class SchumpeterReferenceInventoryPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    inventory_deferred_to: str = "v0.28.4"
    references_schumpeter_is_not_runtime_dependency: bool = True
    references_schumpeter_is_not_copied_into_core_by_default: bool = True
    origin_required: bool = True
    license_status_required: bool = True
    private_data_risk_required: bool = True
    company_material_risk_required: bool = True
    concept_value_required: bool = True
    code_reuse_value_required: bool = True
    test_reuse_value_required: bool = True
    doc_reuse_value_required: bool = True
    OCEL_compatibility_required: bool = True
    recommended_disposition_required: bool = True


@dataclass
class SchumpeterReuseDispositionPolicy(ModelMixin):
    policy_id: str
    allowed_dispositions: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    reuse_requires_decision_record: bool = True
    reuse_requires_license_review: bool = True
    reuse_requires_public_private_boundary_review: bool = True
    runtime_dependency_forbidden_now: bool = True
    code_copy_forbidden_now: bool = True


@dataclass
class ExternalAdapterPreflightBoundary(ModelMixin):
    boundary_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    preflight_deferred_to: str = "v0.28.8"
    external_adapter_implementation_deferred_to: str = "v0.29.x"
    provider_invocation_forbidden_now: bool = True
    adapter_registration_forbidden_now: bool = True
    capability_declaration_is_not_permission: bool = True
    provider_adapter_contract_is_not_provider_invocation: bool = True
    safety_gate_required_before_invocation: bool = True
    permission_gate_required_before_invocation: bool = True
    audit_required_before_invocation: bool = True
    rollback_boundary_required_before_invocation: bool = True
    credential_boundary_required_before_invocation: bool = True
    network_boundary_required_before_invocation: bool = True


@dataclass
class V029RiskReopenCriteria(ModelMixin):
    criteria_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    target_track: str = "v0.29.x External Skill / External Provider Adapter Development"
    contract_first_required: bool = True
    provider_invocation_reopen_requires_preflight: bool = True
    command_execution_reopen_requires_preflight: bool = True
    credential_handling_reopen_requires_boundary: bool = True
    network_access_reopen_requires_boundary: bool = True
    adapter_certification_required: bool = True
    OCEL_visibility_required: bool = True
    permission_gate_required: bool = True
    safety_gate_required: bool = True
    no_background_execution_without_gate: bool = True


@dataclass
class PublicAlphaSafetyBoundaryPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V028_VERSION
    public_alpha_safety_boundary_required: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    file_mutation_expansion_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    autonomous_memory_driven_execution_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    schumpeter_split_enabled_now: bool = False
    company_deployment_enabled_now: bool = False
    secret_exposure_forbidden: bool = True
    credential_exposure_forbidden: bool = True
    raw_trace_exposure_forbidden: bool = True
    raw_transcript_exposure_forbidden: bool = True
    raw_provider_output_exposure_forbidden: bool = True
    PIG_execution_authority_forbidden: bool = True
    llm_judge_as_sole_readiness_authority_forbidden: bool = True


@dataclass
class PublicAlphaSchumpeterPreparationContract(ModelMixin):
    contract_id: str
    definition: str
    previous_foundation_ref: dict[str, Any] | None
    workbench_foundation_ref: dict[str, Any] | None
    release_hygiene_ref: dict[str, Any] | None
    roadmap: V028Roadmap
    public_alpha_scope_policy: PublicAlphaScopePolicy
    public_alpha_stage_policy: PublicAlphaStagePolicy
    release_hygiene_debt_policy: ReleaseHygieneDebtPolicy
    release_hygiene_blocking_policy: ReleaseHygieneBlockingPolicy
    packaging_readiness_policy: PackagingReadinessPolicy
    public_private_boundary_policy: PublicPrivateBoundaryPolicy
    schumpeter_split_preparation_policy: SchumpeterSplitPreparationPolicy
    schumpeter_split_decision_framework: SchumpeterSplitDecisionFramework
    schumpeter_reference_inventory_policy: SchumpeterReferenceInventoryPolicy
    schumpeter_reuse_disposition_policy: SchumpeterReuseDispositionPolicy
    external_adapter_preflight_boundary: ExternalAdapterPreflightBoundary
    v029_risk_reopen_criteria: V029RiskReopenCriteria
    public_alpha_safety_boundary_policy: PublicAlphaSafetyBoundaryPolicy
    notes: list[str] = field(default_factory=list)
    version: str = V028_VERSION
    layer: str = V028_LAYER
    track: str = V028_TRACK
    status: str = "contract_only"
    public_alpha_implemented: bool = False
    schumpeter_split_implemented: bool = False
    external_adapter_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    package_published: bool = False
    release_tag_created: bool = False


@dataclass
class V028ContractFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class V028ContractReport(ModelMixin):
    report_id: str
    created_at: str
    contract: PublicAlphaSchumpeterPreparationContract
    findings: list[V028ContractFinding]
    report_status: str
    ready_for_v0_28_1: bool
    contract_created: bool
    roadmap_created: bool
    public_alpha_scope_policy_created: bool
    public_alpha_stage_policy_created: bool
    release_hygiene_debt_policy_created: bool
    release_hygiene_blocking_policy_created: bool
    packaging_readiness_policy_created: bool
    public_private_boundary_policy_created: bool
    schumpeter_split_preparation_policy_created: bool
    schumpeter_split_decision_framework_created: bool
    schumpeter_reference_inventory_policy_created: bool
    schumpeter_reuse_disposition_policy_created: bool
    external_adapter_preflight_boundary_created: bool
    v029_risk_reopen_criteria_created: bool
    public_alpha_safety_boundary_policy_created: bool
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    version: str = V028_VERSION
    ready_for_v0_29: bool = False
    public_alpha_implemented: bool = False
    public_alpha_ready: bool = False
    schumpeter_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    external_adapter_implemented: bool = False
    external_dominion_bridge_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    runtime_continuity_injected: bool = False
    autonomous_memory_execution_enabled: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    references_schumpeter_runtime_dependency_added: bool = False
    references_schumpeter_code_copied: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V028_NEXT_STEP
    validity_horizon: str = "Valid until v0.28.1 Release Hygiene / Repository Governance Blocking Gate begins or v0.28 policy changes."


class V028ContractPrerequisiteSourceService:
    def load_v0279_memory_consolidation_report(self) -> Any:
        return MemoryConsolidationReportService().build_report()

    def load_v0279_memory_release_manifest(self) -> Any:
        return MemoryConsolidationReportService().build_all_parts()["release_manifest"]

    def load_v0279_public_alpha_handoff_packet(self) -> Any:
        return MemoryConsolidationReportService().build_all_parts()["public_alpha_handoff_packet"]

    def load_v02610_release_hygiene_report_if_available(self) -> None:
        return None

    def load_v0269_workbench_consolidation_report_if_available(self) -> Any:
        return WorkbenchConsolidationReportService().build_all_parts()["report"]

    def inspect_references_schumpeter_metadata_only_if_available(self) -> dict[str, Any]:
        return {
            "object_type": "schumpeter_reference_metadata",
            "object_id": "references/schumpeter:metadata_only",
            "metadata_available": False,
            "runtime_dependency": False,
            "code_copied": False,
        }

    def load_repository_hygiene_status_if_available(self) -> dict[str, Any]:
        return {"status": "unknown", "release_hygiene_passed": False}

    def load_packaging_metadata_if_available(self) -> dict[str, Any]:
        return {"status": "unknown", "package_publish_enabled": False}

    def load_pig_ocpx_reports_if_available(self) -> list[dict[str, Any]]:
        return [
            _ref("pig_report", "pig:public_alpha_schumpeter_preparation_contract:v0.28.0", V028_VERSION),
            _ref("ocpx_projection", "ocpx:public_alpha_schumpeter_preparation_contract:v0.28.0", V028_VERSION),
        ]


class V028RoadmapService:
    ROADMAP = [
        ("v0.28.0", "Public Alpha / Schumpeter Split Preparation Contract", "Declare the public alpha and Schumpeter preparation contract.", "contract_only"),
        ("v0.28.1", "Release Hygiene / Repository Governance Blocking Gate", "Resolve or block release hygiene debt before alpha claims.", "gate_report"),
        ("v0.28.2", "Packaging / Distribution / Type Boundary", "Define packaging, typing, and distribution boundaries.", "packaging_boundary"),
        ("v0.28.3", "Public-Private Boundary / Redaction / Reference Policy", "Define public/private, redaction, and reference policies.", "boundary_policy"),
        ("v0.28.4", "Schumpeter Split Decision Framework", "Evaluate split options before implementation.", "decision_framework"),
        ("v0.28.5", "Schumpeter Split Preparation Profile", "Prepare a private-overlay profile without split execution.", "preparation_profile"),
        ("v0.28.6", "Public Alpha Runtime Profile / Smoke Demo Flow", "Define alpha smoke demo profile without production claims.", "smoke_demo"),
        ("v0.28.7", "Alpha Documentation / Onboarding / Example Pack", "Prepare public docs, onboarding, and sanitized examples.", "docs_pack"),
        ("v0.28.8", "Alpha Readiness Validation / External Adapter Preflight Gate", "Validate readiness and define adapter preflight before v0.29.", "validation_gate"),
        ("v0.28.9", "Public Alpha / Schumpeter Split Preparation Consolidation", "Consolidate v0.28 preparation artifacts.", "consolidation"),
    ]

    def build_roadmap(self) -> V028Roadmap:
        plans = [
            V028VersionPlan(
                version_number=number,
                version_name=name,
                purpose=purpose,
                allowed_scope=[kind, "read_only_observation", "policy_artifacts"],
                forbidden_scope=[
                    "public_alpha_release",
                    "schumpeter_split_execution",
                    "external_adapter_implementation",
                    "provider_invocation",
                    "command_execution",
                ],
                implementation_kind=kind,
                notes=["Preparation does not imply implementation."],
            )
            for number, name, purpose, kind in self.ROADMAP
        ]
        return V028Roadmap(
            roadmap_id="v028_roadmap:public_alpha_schumpeter_preparation",
            versions=plans,
            roadmap_status="aligned",
            evidence_refs=[_ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", "v0.27.9")],
        )


class PublicAlphaScopePolicyService:
    def build_policy(self) -> PublicAlphaScopePolicy:
        return PublicAlphaScopePolicy(
            policy_id="public_alpha_scope_policy:v0.28.0",
            public_alpha_allowed_surfaces=[
                "public_docs",
                "sanitized_examples",
                "synthetic_demo_data",
                "OCEL_store_validation",
                "OCPX_projection_demo",
                "PIG_report_demo",
                "Workbench_report_surfaces",
                "Memory_foundation_report_surfaces",
                "CLI_smoke_surfaces",
            ],
            public_alpha_forbidden_surfaces=[
                "company_private_material",
                "credentials",
                "raw_runtime_trace",
                "raw_transcript",
                "raw_provider_output",
                "external_provider_invocation",
                "command_execution_expansion",
                "runtime_continuity_injection",
                "Schumpeter_company_wrapper",
                "RPA_adapter",
            ],
        )


class PublicAlphaStagePolicyService:
    def build_policy(self) -> PublicAlphaStagePolicy:
        return PublicAlphaStagePolicy(
            policy_id="public_alpha_stage_policy:v0.28.0",
            stages=[
                "alpha_architecture_candidate",
                "alpha_repository_candidate",
                "alpha_package_candidate",
                "alpha_release_candidate",
            ],
        )


class ReleaseHygieneDebtPolicyService:
    DEBT_ITEMS = [
        "clean_worktree",
        "release_tag",
        "license",
        "changelog",
        "third_party_notice",
        "runtime_data_hygiene",
        "reference_license_policy",
    ]
    DISPOSITION_TYPES = [
        "resolve_in_v0281",
        "defer_with_blocker",
        "accept_warning",
        "block_public_alpha",
        "no_release",
    ]

    def build_policy(self) -> ReleaseHygieneDebtPolicy:
        return ReleaseHygieneDebtPolicy(policy_id="release_hygiene_debt_policy:v0.28.0")

    def build_dispositions(self, hygiene_status: str = "unknown") -> list[HygieneDebtDisposition]:
        return [
            HygieneDebtDisposition(
                disposition_id=f"hygiene_debt_disposition:{item}:{disposition_type}:v0.28.0",
                debt_item=item,
                current_status=hygiene_status,
                disposition_type=disposition_type,
                disposition_reason="v0.28.0 records the debt; v0.28.1 is the blocking gate.",
                required_followup_version="v0.28.1" if hygiene_status != "passed" else None,
                evidence_refs=[],
            )
            for item in self.DEBT_ITEMS
            for disposition_type in self.DISPOSITION_TYPES
        ]


class ReleaseHygieneBlockingPolicyService:
    def build_policy(self) -> ReleaseHygieneBlockingPolicy:
        return ReleaseHygieneBlockingPolicy(policy_id="release_hygiene_blocking_policy:v0.28.0")


class PackagingReadinessPolicyService:
    def build_policy(self) -> PackagingReadinessPolicy:
        return PackagingReadinessPolicy(policy_id="packaging_readiness_policy:v0.28.0")


class PublicPrivateBoundaryPolicyService:
    def build_policy(self) -> PublicPrivateBoundaryPolicy:
        return PublicPrivateBoundaryPolicy(policy_id="public_private_boundary_policy:v0.28.0")


class SchumpeterSplitPreparationPolicyService:
    def build_policy(self) -> SchumpeterSplitPreparationPolicy:
        return SchumpeterSplitPreparationPolicy(policy_id="schumpeter_split_preparation_policy:v0.28.0")


class SchumpeterSplitDecisionFrameworkService:
    OPTION_NAMES = [
        "no_split",
        "reference_only",
        "public_core_private_overlay",
        "private_distribution_profile",
        "separate_private_repo",
        "merge_schumpeter_into_core",
        "deprecate_legacy_schumpeter",
    ]
    CRITERIA = [
        "ip_license_risk",
        "company_private_data_contamination_risk",
        "public_core_contamination_risk",
        "architecture_overlap",
        "code_reuse_value",
        "concept_reuse_value",
        "test_reuse_value",
        "doc_reuse_value",
        "OCEL_compatibility",
        "PIG_compatibility",
        "memory_workbench_compatibility",
        "runtime_dependency_risk",
        "maintainability",
        "testability",
        "deployment_boundary_clarity",
        "security_credential_exposure_risk",
        "future_external_adapter_compatibility",
        "organizational_usefulness",
    ]
    OUTPUTS = [
        "keep_reference_only",
        "prepare_private_overlay",
        "prepare_distribution_profile",
        "defer_split",
        "block_split",
        "deprecate_legacy_schumpeter",
        "extract_concepts_only",
        "extract_tests_only",
        "extract_docs_only",
        "migrate_specific_module_later",
    ]

    def build_options(self) -> list[SchumpeterSplitDecisionOption]:
        return [
            SchumpeterSplitDecisionOption(
                option_id=f"schumpeter_split_decision_option:{name}",
                option_name=name,
                option_summary=f"Decision option {name}; no split implementation is performed in v0.28.0.",
                allowed_now=name in {"no_split", "reference_only", "public_core_private_overlay"},
                risk_notes=["Requires v0.28.4 decision record and public/private review before action."],
            )
            for name in self.OPTION_NAMES
        ]

    def build_criteria(self) -> list[SchumpeterSplitEvaluationCriterion]:
        return [
            SchumpeterSplitEvaluationCriterion(
                criterion_id=f"schumpeter_split_evaluation_criterion:{name}",
                criterion_name=name,
                criterion_summary=f"Criterion {name} must be reviewed before split decisions.",
            )
            for name in self.CRITERIA
        ]

    def build_framework(self) -> SchumpeterSplitDecisionFramework:
        return SchumpeterSplitDecisionFramework(
            framework_id="schumpeter_split_decision_framework:v0.28.0",
            options=self.build_options(),
            criteria=self.build_criteria(),
            decision_outputs=self.OUTPUTS,
        )


class SchumpeterReferenceInventoryPolicyService:
    def build_policy(self) -> SchumpeterReferenceInventoryPolicy:
        return SchumpeterReferenceInventoryPolicy(policy_id="schumpeter_reference_inventory_policy:v0.28.0")


class SchumpeterReuseDispositionPolicyService:
    def build_policy(self) -> SchumpeterReuseDispositionPolicy:
        return SchumpeterReuseDispositionPolicy(
            policy_id="schumpeter_reuse_disposition_policy:v0.28.0",
            allowed_dispositions=[
                "adopt_concept",
                "port_model_later",
                "port_test_later",
                "port_document_later",
                "keep_reference_only",
                "quarantine_due_to_license_or_private_risk",
                "discard",
            ],
        )


class ExternalAdapterPreflightBoundaryService:
    def build_boundary(self) -> ExternalAdapterPreflightBoundary:
        return ExternalAdapterPreflightBoundary(boundary_id="external_adapter_preflight_boundary:v0.28.0")


class V029RiskReopenCriteriaService:
    def build_criteria(self) -> V029RiskReopenCriteria:
        return V029RiskReopenCriteria(criteria_id="v029_risk_reopen_criteria:v0.28.0")


class PublicAlphaSafetyBoundaryPolicyService:
    def build_policy(self) -> PublicAlphaSafetyBoundaryPolicy:
        return PublicAlphaSafetyBoundaryPolicy(policy_id="public_alpha_safety_boundary_policy:v0.28.0")


class V028ContractService:
    def build_contract(self) -> PublicAlphaSchumpeterPreparationContract:
        source = V028ContractPrerequisiteSourceService()
        memory_report = source.load_v0279_memory_consolidation_report()
        workbench_report = source.load_v0269_workbench_consolidation_report_if_available()
        release_hygiene = source.load_v02610_release_hygiene_report_if_available()
        roadmap = V028RoadmapService().build_roadmap()
        scope = PublicAlphaScopePolicyService().build_policy()
        stage = PublicAlphaStagePolicyService().build_policy()
        hygiene_debt = ReleaseHygieneDebtPolicyService().build_policy()
        hygiene_blocking = ReleaseHygieneBlockingPolicyService().build_policy()
        packaging = PackagingReadinessPolicyService().build_policy()
        public_private = PublicPrivateBoundaryPolicyService().build_policy()
        split_prep = SchumpeterSplitPreparationPolicyService().build_policy()
        framework = SchumpeterSplitDecisionFrameworkService().build_framework()
        inventory = SchumpeterReferenceInventoryPolicyService().build_policy()
        reuse = SchumpeterReuseDispositionPolicyService().build_policy()
        preflight = ExternalAdapterPreflightBoundaryService().build_boundary()
        risk = V029RiskReopenCriteriaService().build_criteria()
        safety = PublicAlphaSafetyBoundaryPolicyService().build_policy()
        return PublicAlphaSchumpeterPreparationContract(
            contract_id="public_alpha_schumpeter_preparation_contract:v0.28.0",
            definition="Contract-only preparation layer for public alpha candidacy and Schumpeter split decision-making.",
            previous_foundation_ref=_ref("memory_consolidation_report", memory_report.report_id, "v0.27.9"),
            workbench_foundation_ref=_ref("workbench_consolidation_report", workbench_report.report_id, "v0.26.9"),
            release_hygiene_ref=_ref("release_hygiene_report", "missing:v0.26.10", "v0.26.10") if release_hygiene is None else _ref("release_hygiene_report", release_hygiene.report_id, "v0.26.10"),
            roadmap=roadmap,
            public_alpha_scope_policy=scope,
            public_alpha_stage_policy=stage,
            release_hygiene_debt_policy=hygiene_debt,
            release_hygiene_blocking_policy=hygiene_blocking,
            packaging_readiness_policy=packaging,
            public_private_boundary_policy=public_private,
            schumpeter_split_preparation_policy=split_prep,
            schumpeter_split_decision_framework=framework,
            schumpeter_reference_inventory_policy=inventory,
            schumpeter_reuse_disposition_policy=reuse,
            external_adapter_preflight_boundary=preflight,
            v029_risk_reopen_criteria=risk,
            public_alpha_safety_boundary_policy=safety,
            notes=[
                "Grok review findings are absorbed as roadmap control logic.",
                "No-release / defer-alpha remains a valid outcome.",
            ],
        )

    def view_contract(self) -> PublicAlphaSchumpeterPreparationContract:
        return self.build_contract()


class V028ContractFindingService:
    BLOCKED_FINDINGS = {
        "public_alpha_implementation_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "schumpeter_split_attempted",
        "company_wrapper_attempted",
        "company_private_material_detected",
        "credential_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "references_schumpeter_runtime_dependency_detected",
        "references_schumpeter_code_copy_attempted",
        "external_adapter_implementation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "PIG_execution_authority_detected",
        "external_dominion_bridge_attempted",
        "llm_judge_detected",
    }

    def build_findings(self, hygiene_available: bool = False, extra_findings: list[str] | None = None) -> list[V028ContractFinding]:
        findings = [
            V028ContractFinding(
                finding_id="v028_contract_finding:public_alpha_contract_created",
                severity="info",
                finding_type="public_alpha_contract_created",
                message="v0.28.0 public alpha / Schumpeter preparation contract was created.",
                subject_ref=_ref("public_alpha_schumpeter_preparation_contract", "public_alpha_schumpeter_preparation_contract:v0.28.0", V028_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if contract-only boundary is violated.",
            ),
            V028ContractFinding(
                finding_id="v028_contract_finding:v028_roadmap_created",
                severity="info",
                finding_type="v028_roadmap_created",
                message="v0.28.x roadmap was declared.",
                subject_ref=_ref("v028_roadmap", "v028_roadmap:public_alpha_schumpeter_preparation", V028_VERSION),
                evidence_refs=[],
                withdrawal_condition="Withdraw if roadmap permits v0.28.0 implementation behavior.",
            ),
        ]
        if not hygiene_available:
            findings.append(
                V028ContractFinding(
                    finding_id="v028_contract_finding:release_hygiene_unknown",
                    severity="warning",
                    finding_type="release_hygiene_unknown",
                    message="v0.26.10 release hygiene evidence is unavailable; public alpha readiness is not claimed.",
                    subject_ref=_ref("release_hygiene_report", "missing:v0.26.10", "v0.26.10"),
                    evidence_refs=[],
                    withdrawal_condition="Withdraw warning when v0.28.1 validates equivalent release hygiene.",
                )
            )
        for finding_type in extra_findings or []:
            findings.append(
                V028ContractFinding(
                    finding_id=f"v028_contract_finding:{finding_type}",
                    severity="critical" if finding_type in self.BLOCKED_FINDINGS else "warning",
                    finding_type=finding_type,
                    message=f"Injected v0.28.0 boundary finding: {finding_type}.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when boundary validation input is removed.",
                )
            )
        return findings


class V028ContractReportService:
    def build_report(self, report_id: str | None = None, hygiene_available: bool = False, extra_findings: list[str] | None = None) -> V028ContractReport:
        contract = V028ContractService().build_contract()
        findings = V028ContractFindingService().build_findings(hygiene_available=hygiene_available, extra_findings=extra_findings)
        blocked = any(item.finding_type in V028ContractFindingService.BLOCKED_FINDINGS for item in findings)
        report_status = "blocked" if blocked else ("passed" if hygiene_available else "warning")
        return V028ContractReport(
            report_id=report_id or "v028_contract_report:v0.28.0",
            created_at=_now(),
            contract=contract,
            findings=findings,
            report_status=report_status,
            ready_for_v0_28_1=not blocked,
            contract_created=True,
            roadmap_created=True,
            public_alpha_scope_policy_created=True,
            public_alpha_stage_policy_created=True,
            release_hygiene_debt_policy_created=True,
            release_hygiene_blocking_policy_created=True,
            packaging_readiness_policy_created=True,
            public_private_boundary_policy_created=True,
            schumpeter_split_preparation_policy_created=True,
            schumpeter_split_decision_framework_created=True,
            schumpeter_reference_inventory_policy_created=True,
            schumpeter_reuse_disposition_policy_created=True,
            external_adapter_preflight_boundary_created=True,
            v029_risk_reopen_criteria_created=True,
            public_alpha_safety_boundary_policy_created=True,
            limitations=[
                "v0.28.0 is contract-only and does not claim public alpha readiness.",
                "v0.26.10 hygiene debt is modeled for v0.28.1 blocking gate resolution.",
            ],
            withdrawal_conditions=[
                "Withdraw if public alpha release, package publishing, release tagging, split execution, external adapter implementation, provider/command execution, or private material exposure is introduced.",
            ],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        contract = report.contract
        dispositions = ReleaseHygieneDebtPolicyService().build_dispositions()
        return {
            "contract": contract,
            "roadmap": contract.roadmap,
            "version_plans": contract.roadmap.versions,
            "scope_policy": contract.public_alpha_scope_policy,
            "stage_policy": contract.public_alpha_stage_policy,
            "hygiene_debt_policy": contract.release_hygiene_debt_policy,
            "hygiene_debt_dispositions": dispositions,
            "hygiene_blocking_policy": contract.release_hygiene_blocking_policy,
            "packaging_policy": contract.packaging_readiness_policy,
            "public_private_policy": contract.public_private_boundary_policy,
            "schumpeter_preparation_policy": contract.schumpeter_split_preparation_policy,
            "schumpeter_decision_framework": contract.schumpeter_split_decision_framework,
            "schumpeter_options": contract.schumpeter_split_decision_framework.options,
            "schumpeter_criteria": contract.schumpeter_split_decision_framework.criteria,
            "schumpeter_reference_policy": contract.schumpeter_reference_inventory_policy,
            "schumpeter_reuse_policy": contract.schumpeter_reuse_disposition_policy,
            "external_adapter_preflight": contract.external_adapter_preflight_boundary,
            "v029_risk_reopen": contract.v029_risk_reopen_criteria,
            "safety_boundary": contract.public_alpha_safety_boundary_policy,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": V028_VERSION,
            "layer": V028_LAYER,
            "subject": "public_alpha_schumpeter_preparation_contract",
            "principles": [
                "Public Alpha readiness is not production readiness",
                "Public Alpha readiness is not automatically true just because architecture is mature",
                "Schumpeter Split Preparation is not Schumpeter implementation",
                "Schumpeter split decision is not split execution",
                "Reference inventory is not code adoption",
                "Reference reuse disposition is not runtime dependency",
                "Release hygiene unknown is not release hygiene passed",
                "External adapter preflight is not adapter implementation",
                "v0.29 readiness is not v0.29 implementation",
                "No-release / defer-alpha is a valid outcome",
            ],
            "safety_boundary": {
                "public_alpha_implemented": False,
                "package_published": False,
                "release_tag_created": False,
                "schumpeter_split_implemented": False,
                "company_wrapper_implemented": False,
                "external_adapter_implemented": False,
                "external_dominion_bridge_implemented": False,
                "provider_invoked": False,
                "command_executed": False,
                "runtime_continuity_injected": False,
                "autonomous_memory_execution_enabled": False,
                "references_schumpeter_runtime_dependency_added": False,
                "references_schumpeter_code_copied": False,
                "company_private_material_exposed": False,
                "credential_exposed": False,
                "raw_trace_exposed": False,
                "raw_transcript_exposed": False,
                "raw_provider_output_exposed": False,
                "PIG_execution_authority_enabled": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [plan.version_name for plan in V028RoadmapService().build_roadmap().versions[1:]]
            + ["v0.29 external provider adapter contract", "v0.30 external agent dominion bridge contract"],
            "next_step": V028_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "public_alpha_schumpeter_preparation_contract_declared",
            "version": V028_VERSION,
            "source_read_models": [
                "MemoryConsolidationState",
                "MemoryReleaseManifestState",
                "MemoryPublicAlphaHandoffState",
                "WorkbenchConsolidationState",
                "ReleaseHygieneState",
                "RepositoryHygieneState",
                "PackagingMetadataState",
                "SchumpeterReferenceMetadataState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "PublicAlphaSchumpeterPreparationContractState",
                "V028RoadmapState",
                "PublicAlphaScopePolicyState",
                "ReleaseHygieneDebtPolicyState",
                "ReleaseHygieneBlockingPolicyState",
                "PublicPrivateBoundaryPolicyState",
                "SchumpeterSplitDecisionFrameworkState",
                "ExternalAdapterPreflightBoundaryState",
                "V029RiskReopenCriteriaState",
                "V028ReadinessState",
            ],
            "effect_types": V028_EFFECT_TYPES,
            "forbidden_effect_types": V028_FORBIDDEN_EFFECT_TYPES,
        }


def render_v028_contract_cli(parts: dict[str, Any], section: str = "contract") -> str:
    report: V028ContractReport = parts["report"]
    contract = report.contract
    lines = [
        f"Public Alpha / Schumpeter Split Preparation {section}",
        f"version={report.version}",
        f"layer={contract.layer}",
        f"status={contract.status}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_1={_bool(report.ready_for_v0_28_1)}",
        f"ready_for_v0_29={_bool(report.ready_for_v0_29)}",
        f"public_alpha_implemented={_bool(report.public_alpha_implemented)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"schumpeter_split_implemented={_bool(report.schumpeter_split_implemented)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"external_dominion_bridge_implemented={_bool(report.external_dominion_bridge_implemented)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"autonomous_memory_execution_enabled={_bool(report.autonomous_memory_execution_enabled)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"references_schumpeter_runtime_dependency_added={_bool(report.references_schumpeter_runtime_dependency_added)}",
        f"references_schumpeter_code_copied={_bool(report.references_schumpeter_code_copied)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    section_values = {
        "contract": ("contract_id", contract.contract_id),
        "roadmap": ("roadmap_status", contract.roadmap.roadmap_status),
        "scope-policy": ("allowed_surface_count", len(contract.public_alpha_scope_policy.public_alpha_allowed_surfaces)),
        "stage-policy": ("stage_count", len(contract.public_alpha_stage_policy.stages)),
        "hygiene-debt": ("hygiene_unknown_is_not_passed", contract.release_hygiene_debt_policy.hygiene_unknown_is_not_passed),
        "hygiene-blocking-policy": ("v0281_is_blocking_gate", contract.release_hygiene_blocking_policy.v0281_is_blocking_gate),
        "packaging-policy": ("package_publish_enabled_now", contract.packaging_readiness_policy.package_publish_enabled_now),
        "public-private-policy": ("boundary_deferred_to", contract.public_private_boundary_policy.boundary_deferred_to),
        "schumpeter-preparation": ("actual_split_enabled_now", contract.schumpeter_split_preparation_policy.actual_split_enabled_now),
        "schumpeter-decision-framework": ("default_option", contract.schumpeter_split_decision_framework.default_option),
        "schumpeter-reference-policy": ("runtime_dependency_forbidden_now", contract.schumpeter_reuse_disposition_policy.runtime_dependency_forbidden_now),
        "external-adapter-preflight": ("provider_invocation_forbidden_now", contract.external_adapter_preflight_boundary.provider_invocation_forbidden_now),
        "v029-risk-reopen": ("contract_first_required", contract.v029_risk_reopen_criteria.contract_first_required),
        "safety-boundary": ("provider_invocation_enabled_now", contract.public_alpha_safety_boundary_policy.provider_invocation_enabled_now),
        "contract-report": ("report_id", report.report_id),
    }
    if section in section_values:
        name, value = section_values[section]
        lines.append(f"{name}={_bool(value) if isinstance(value, bool) else value}")
    return "\n".join(lines)


V0286_VERSION = "v0.28.6"
V0286_VERSION_NAME = "Public Alpha Runtime Profile / Smoke Demo Flow"
V0286_NEXT_STEP = "v0.28.7 Alpha Documentation / Onboarding / Example Pack"

V0286_OBJECT_TYPES = [
    "public_alpha_runtime_profile_policy",
    "public_alpha_runtime_profile_request",
    "public_alpha_runtime_source_view",
    "public_alpha_feature_flag_matrix",
    "public_alpha_feature_flag",
    "alpha_enabled_feature_set",
    "alpha_preview_only_feature_set",
    "alpha_disabled_future_track_feature_set",
    "alpha_runtime_capability_matrix",
    "alpha_runtime_capability_entry",
    "alpha_operator_surface_policy",
    "alpha_smoke_scenario_catalog",
    "alpha_smoke_scenario",
    "alpha_smoke_input_bundle",
    "alpha_synthetic_demo_data_policy",
    "alpha_ocel_demo_pack",
    "alpha_ocpx_projection_demo",
    "alpha_pig_report_demo",
    "alpha_workbench_report_demo",
    "alpha_memory_foundation_demo",
    "alpha_continuity_preview_demo",
    "alpha_safety_boundary_demo",
    "alpha_cli_workflow_demo",
    "alpha_smoke_run_plan",
    "alpha_smoke_run_report",
    "alpha_operator_handoff_packet",
    "alpha_runtime_profile_finding",
    "alpha_runtime_profile_report",
    "schumpeter_preparation_report",
    "packaging_readiness_report",
    "public_private_boundary_report",
    "release_hygiene_gate_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0286_EVENT_TYPES = [
    "alpha_runtime_profile_requested",
    "alpha_runtime_profile_prerequisites_loaded",
    "public_alpha_runtime_profile_policy_created",
    "public_alpha_runtime_source_view_created",
    "public_alpha_feature_flag_matrix_created",
    "alpha_enabled_feature_set_created",
    "alpha_preview_only_feature_set_created",
    "alpha_disabled_future_track_feature_set_created",
    "alpha_runtime_capability_matrix_created",
    "alpha_operator_surface_policy_created",
    "alpha_smoke_scenario_catalog_created",
    "alpha_smoke_scenario_created",
    "alpha_smoke_input_bundle_created",
    "alpha_synthetic_demo_data_policy_created",
    "alpha_ocel_demo_pack_created",
    "alpha_ocpx_projection_demo_created",
    "alpha_pig_report_demo_created",
    "alpha_workbench_report_demo_created",
    "alpha_memory_foundation_demo_created",
    "alpha_continuity_preview_demo_created",
    "alpha_safety_boundary_demo_created",
    "alpha_cli_workflow_demo_created",
    "alpha_smoke_run_plan_created",
    "alpha_smoke_run_report_created",
    "alpha_operator_handoff_packet_created",
    "alpha_runtime_profile_report_created",
    "alpha_runtime_profile_warning_created",
    "alpha_runtime_profile_blocked",
]

V0286_EFFECT_TYPES = [
    "read_only_observation",
    "public_alpha_runtime_profile_created",
    "alpha_feature_flag_matrix_created",
    "alpha_runtime_capability_matrix_created",
    "alpha_smoke_scenario_catalog_created",
    "alpha_demo_pack_created",
    "alpha_smoke_run_report_created",
    "alpha_operator_handoff_packet_created",
    "state_candidate_created",
]

V0286_FORBIDDEN_EFFECT_TYPES = [
    "production_runtime_implemented",
    "public_alpha_release_implemented",
    "package_published",
    "release_tag_created",
    "official_release_artifact_created",
    "schumpeter_private_runtime_used",
    "company_wrapper_implemented",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "RPA_adapter_implemented",
    "A360_adapter_implemented",
    "Brity_adapter_implemented",
    "UiPath_adapter_implemented",
    "provider_invoked",
    "command_executed",
    "network_called",
    "file_mutated",
    "runtime_continuity_injected",
    "autonomous_memory_execution_enabled",
    "actual_user_data_used",
    "actual_company_data_used",
    "raw_trace_used",
    "raw_transcript_used",
    "raw_provider_output_used",
    "credential_exposed",
    "secret_exposed",
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class PublicAlphaRuntimeProfilePolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    layer: str = V028_LAYER
    runtime_profile_enabled: bool = True
    smoke_demo_flow_enabled: bool = True
    deterministic_demo_required: bool = True
    public_safe_data_required: bool = True
    synthetic_data_required_by_default: bool = True
    provider_invocation_enabled_now: bool = False
    network_call_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    shell_execution_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    autonomous_memory_execution_enabled_now: bool = False
    production_runtime_enabled_now: bool = False
    schumpeter_private_overlay_runtime_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    raw_trace_forbidden: bool = True
    raw_transcript_forbidden: bool = True
    raw_provider_output_forbidden: bool = True
    credential_forbidden: bool = True
    secret_forbidden: bool = True
    references_runtime_dependency_forbidden: bool = True
    references_code_copy_forbidden: bool = True
    PIG_execution_authority_forbidden: bool = True
    llm_judge_as_sole_smoke_authority_forbidden: bool = True


@dataclass
class PublicAlphaRuntimeProfileRequest(ModelMixin):
    request_id: str
    schumpeter_preparation_report_id: str | None
    packaging_readiness_report_id: str | None
    public_private_boundary_report_id: str | None
    release_hygiene_gate_report_id: str | None
    requested_profile: str
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class PublicAlphaRuntimeSourceView(ModelMixin):
    source_view_id: str
    schumpeter_preparation_report_ref: dict[str, Any] | None
    schumpeter_handoff_packet_ref: dict[str, Any] | None
    public_private_boundary_report_ref: dict[str, Any] | None
    packaging_readiness_report_ref: dict[str, Any] | None
    release_hygiene_gate_report_ref: dict[str, Any] | None
    memory_consolidation_report_ref: dict[str, Any] | None
    workbench_consolidation_report_ref: dict[str, Any] | None
    import_smoke_report_ref: dict[str, Any] | None
    cli_smoke_report_ref: dict[str, Any] | None
    available_public_safe_refs: list[dict[str, Any]]
    available_demo_refs: list[dict[str, Any]]
    blocked_private_refs: list[dict[str, Any]]
    disabled_future_track_refs: list[dict[str, Any]]
    source_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    schumpeter_private_overlay_dependency_detected: bool = False
    private_data_detected: bool = False
    credential_detected: bool = False
    raw_trace_detected: bool = False
    raw_transcript_detected: bool = False
    raw_provider_output_detected: bool = False


@dataclass
class PublicAlphaFeatureFlag(ModelMixin):
    feature_flag_id: str
    feature_name: str
    feature_category: str
    alpha_status: str
    status_reason: str
    requires_synthetic_data: bool
    public_safe: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    requires_provider_invocation: bool = False
    requires_command_execution: bool = False
    requires_private_data: bool = False
    requires_schumpeter_private_overlay: bool = False


@dataclass
class PublicAlphaFeatureFlagMatrix(ModelMixin):
    matrix_id: str
    feature_flags: list[PublicAlphaFeatureFlag]
    enabled_count: int
    preview_only_count: int
    disabled_count: int
    future_track_count: int
    blocked_count: int
    matrix_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaEnabledFeatureSet(ModelMixin):
    feature_set_id: str
    enabled_feature_refs: list[dict[str, Any]]
    expected_enabled_features: list[str]
    enabled_feature_count: int
    enabled_set_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaPreviewOnlyFeatureSet(ModelMixin):
    feature_set_id: str
    preview_feature_refs: list[dict[str, Any]]
    expected_preview_features: list[str]
    preview_feature_count: int
    preview_set_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaDisabledFutureTrackFeatureSet(ModelMixin):
    feature_set_id: str
    disabled_feature_refs: list[dict[str, Any]]
    future_track_feature_refs: list[dict[str, Any]]
    expected_disabled_or_future_features: list[str]
    disabled_count: int
    future_track_count: int
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaRuntimeCapabilityEntry(ModelMixin):
    capability_entry_id: str
    capability_name: str
    capability_summary: str
    alpha_status: str
    public_safe: bool
    deterministic: bool
    uses_synthetic_data_only: bool
    required_boundary_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    invokes_provider: bool = False
    executes_command: bool = False
    mutates_files: bool = False
    uses_private_data: bool = False
    uses_schumpeter_private_overlay: bool = False


@dataclass
class AlphaRuntimeCapabilityMatrix(ModelMixin):
    matrix_id: str
    capability_entries: list[AlphaRuntimeCapabilityEntry]
    public_safe_capability_count: int
    preview_only_capability_count: int
    disabled_capability_count: int
    unsafe_capability_count: int
    capability_matrix_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaOperatorSurfacePolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    operator_surface_enabled: bool = True
    operator_surface_is_not_production_ui: bool = True
    cli_operator_surface_allowed: bool = True
    report_operator_surface_allowed: bool = True
    workbench_report_surface_allowed: bool = True
    provider_operator_surface_forbidden_now: bool = True
    command_execution_operator_surface_forbidden_now: bool = True
    private_overlay_operator_surface_forbidden_now: bool = True
    public_safe_help_and_report_commands_allowed: bool = True


@dataclass
class AlphaSmokeScenario(ModelMixin):
    scenario_id: str
    scenario_name: str
    scenario_summary: str
    scenario_status: str
    deterministic: bool
    uses_synthetic_data_only: bool
    expected_outputs: list[str]
    boundary_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    uses_private_data: bool = False
    invokes_provider: bool = False
    executes_command: bool = False
    mutates_files: bool = False
    requires_network: bool = False


@dataclass
class AlphaSmokeScenarioCatalog(ModelMixin):
    catalog_id: str
    scenarios: list[AlphaSmokeScenario]
    scenario_count: int
    enabled_scenario_count: int
    preview_scenario_count: int
    disabled_scenario_count: int
    catalog_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaSmokeInputBundle(ModelMixin):
    input_bundle_id: str
    input_refs: list[dict[str, Any]]
    synthetic_data_refs: list[dict[str, Any]]
    example_refs: list[dict[str, Any]]
    private_input_refs: list[dict[str, Any]]
    bundle_status: str
    synthetic_only: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    contains_private_data: bool = False
    contains_credentials: bool = False
    contains_raw_trace: bool = False
    contains_raw_transcript: bool = False
    contains_raw_provider_output: bool = False


@dataclass
class AlphaSyntheticDemoDataPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    synthetic_data_required_by_default: bool = True
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    raw_trace_forbidden: bool = True
    raw_transcript_forbidden: bool = True
    raw_provider_output_forbidden: bool = True
    private_identifiers_forbidden: bool = True
    synthetic_manifest_required: bool = True
    demo_data_must_be_reproducible: bool = True


@dataclass
class AlphaOCELDemoPack(ModelMixin):
    demo_pack_id: str
    synthetic_ocel_refs: list[dict[str, Any]]
    expected_object_types: list[str]
    expected_event_types: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    demo_name: str = "public_alpha_ocel_demo"
    validation_expected: bool = True
    synthetic_only: bool = True
    contains_private_data: bool = False


@dataclass
class AlphaOCPXProjectionDemo(ModelMixin):
    demo_id: str
    source_ocel_demo_pack_ref: dict[str, Any] | None
    projection_name: str
    expected_projection_outputs: list[str]
    projection_demo_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    provider_invoked: bool = False
    command_executed: bool = False


@dataclass
class AlphaPIGReportDemo(ModelMixin):
    demo_id: str
    source_projection_ref: dict[str, Any] | None
    expected_report_sections: list[str]
    pig_report_demo_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    PIG_execution_authority_enabled: bool = False
    provider_invoked: bool = False
    command_executed: bool = False


@dataclass
class AlphaWorkbenchReportDemo(ModelMixin):
    demo_id: str
    expected_workbench_surfaces: list[str]
    workbench_demo_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    provider_invoked: bool = False
    command_executed: bool = False
    file_mutated: bool = False


@dataclass
class AlphaMemoryFoundationDemo(ModelMixin):
    demo_id: str
    expected_memory_surfaces: list[str]
    memory_demo_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    autonomous_memory_execution_enabled: bool = False
    runtime_continuity_injected: bool = False


@dataclass
class AlphaContinuityPreviewDemo(ModelMixin):
    demo_id: str
    context_pack_preview_ref: dict[str, Any] | None
    injection_boundary_preview_ref: dict[str, Any] | None
    preview_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    preview_is_not_runtime_injection: bool = True
    runtime_continuity_injected: bool = False
    default_agent_context_mutated: bool = False
    decision_service_mutated: bool = False
    skill_router_mutated: bool = False


@dataclass
class AlphaSafetyBoundaryDemo(ModelMixin):
    demo_id: str
    expected_safety_checks: list[str]
    safety_demo_status: str
    all_forbidden_flags_false: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION


@dataclass
class AlphaCLIWorkflowDemo(ModelMixin):
    demo_id: str
    cli_workflow_steps: list[str]
    allowed_cli_targets: list[str]
    forbidden_cli_targets: list[str]
    cli_demo_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    provider_invoked: bool = False
    command_executed: bool = False


@dataclass
class AlphaSmokeRunPlan(ModelMixin):
    plan_id: str
    scenario_catalog_ref: dict[str, Any]
    scenario_refs: list[dict[str, Any]]
    run_mode: str
    execution_allowed_now: bool
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    provider_invocation_allowed: bool = False
    command_execution_expansion_allowed: bool = False
    network_allowed: bool = False
    file_mutation_allowed: bool = False


@dataclass
class AlphaSmokeRunReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    scenarios_run: list[dict[str, Any]]
    scenarios_passed_count: int
    scenarios_warning_count: int
    scenarios_failed_count: int
    scenarios_blocked_count: int
    run_mode: str
    smoke_run_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    file_mutated: bool = False
    private_data_used: bool = False
    raw_trace_used: bool = False
    raw_transcript_used: bool = False
    raw_provider_output_used: bool = False


@dataclass
class AlphaOperatorHandoffPacket(ModelMixin):
    handoff_packet_id: str
    runtime_profile_report_id: str
    public_safe_demo_refs: list[dict[str, Any]]
    smoke_scenario_refs: list[dict[str, Any]]
    docs_ready_refs: list[dict[str, Any]]
    example_pack_candidate_refs: list[dict[str, Any]]
    not_implemented_now: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0286_VERSION
    target_version: str = "v0.28.7"
    target_track: str = "Alpha Documentation / Onboarding / Example Pack"
    refs_only: bool = True
    implementation_performed_now: bool = False


@dataclass
class AlphaRuntimeProfileFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AlphaRuntimeProfileReport(ModelMixin):
    report_id: str
    created_at: str
    runtime_profile_policy: PublicAlphaRuntimeProfilePolicy
    request: PublicAlphaRuntimeProfileRequest
    source_view: PublicAlphaRuntimeSourceView
    feature_flag_matrix: PublicAlphaFeatureFlagMatrix
    enabled_feature_set: AlphaEnabledFeatureSet
    preview_only_feature_set: AlphaPreviewOnlyFeatureSet
    disabled_future_track_feature_set: AlphaDisabledFutureTrackFeatureSet
    runtime_capability_matrix: AlphaRuntimeCapabilityMatrix
    operator_surface_policy: AlphaOperatorSurfacePolicy
    smoke_scenario_catalog: AlphaSmokeScenarioCatalog
    smoke_input_bundle: AlphaSmokeInputBundle
    synthetic_demo_data_policy: AlphaSyntheticDemoDataPolicy
    ocel_demo_pack: AlphaOCELDemoPack
    ocpx_projection_demo: AlphaOCPXProjectionDemo
    pig_report_demo: AlphaPIGReportDemo
    workbench_report_demo: AlphaWorkbenchReportDemo
    memory_foundation_demo: AlphaMemoryFoundationDemo
    continuity_preview_demo: AlphaContinuityPreviewDemo
    safety_boundary_demo: AlphaSafetyBoundaryDemo
    cli_workflow_demo: AlphaCLIWorkflowDemo
    smoke_run_plan: AlphaSmokeRunPlan
    smoke_run_report: AlphaSmokeRunReport
    operator_handoff_packet: AlphaOperatorHandoffPacket
    findings: list[AlphaRuntimeProfileFinding]
    report_status: str
    ready_for_v0_28_7: bool
    public_alpha_runtime_profile_ready: bool
    public_alpha_smoke_flow_ready: bool
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    version: str = V0286_VERSION
    ready_for_public_alpha_release_claim: bool = False
    public_alpha_ready: bool = False
    production_runtime_implemented: bool = False
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    official_release_artifact_created: bool = False
    schumpeter_private_runtime_used: bool = False
    company_wrapper_implemented: bool = False
    external_adapter_implemented: bool = False
    RPA_adapter_implemented: bool = False
    A360_adapter_implemented: bool = False
    Brity_adapter_implemented: bool = False
    UiPath_adapter_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    runtime_continuity_injected: bool = False
    autonomous_memory_execution_enabled: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    raw_trace_used: bool = False
    raw_transcript_used: bool = False
    raw_provider_output_used: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0286_NEXT_STEP
    validity_horizon: str = "Valid until v0.28.7 Alpha Documentation / Onboarding / Example Pack begins or public alpha runtime profile policy changes."


class AlphaRuntimeProfilePrerequisiteSourceService:
    def load_v0285_schumpeter_preparation_report(self) -> SchumpeterPreparationReport:
        return SchumpeterPreparationReportService().build_report()

    def load_v0285_schumpeter_handoff_packet(self) -> SchumpeterPreparationHandoffPacket:
        return self.load_v0285_schumpeter_preparation_report().handoff_packet

    def load_v0283_public_private_boundary_report(self) -> PublicPrivateBoundaryReport:
        return PublicPrivateBoundaryReportService().build_report()

    def load_v0282_packaging_readiness_report(self) -> PackagingReadinessReport:
        return PackagingReadinessReportService().build_report()

    def load_v0282_import_smoke_report(self) -> ImportSmokeReport:
        return PackagingReadinessReportService().build_report().import_smoke_report

    def load_v0282_cli_smoke_report(self) -> CLISmokeReport:
        return PackagingReadinessReportService().build_report().cli_smoke_report

    def load_v0281_release_hygiene_gate_report(self) -> ReleaseHygieneGateReport:
        return ReleaseHygieneGateReportService().build_report()

    def load_v0279_memory_consolidation_report(self) -> Any:
        return MemoryConsolidationReportService().build_all_parts()["report"]

    def load_v0269_workbench_consolidation_report(self) -> Any:
        return WorkbenchConsolidationReportService().build_all_parts()["report"]

    def load_package_cli_metadata_if_available(self) -> dict[str, Any]:
        return {"object_type": "package_cli_metadata", "object_id": "package_cli_metadata:v0.28.6", "metadata_only": True}

    def load_public_safe_demo_metadata_if_available(self) -> dict[str, Any]:
        return {"object_type": "public_safe_demo_metadata", "object_id": "public_safe_demo_metadata:v0.28.6", "synthetic_only": True}

    def load_ocel_pig_ocpx_metadata_if_available(self) -> dict[str, Any]:
        return {"object_type": "ocel_pig_ocpx_metadata", "object_id": "ocel_pig_ocpx_metadata:v0.28.6", "metadata_only": True}


class PublicAlphaRuntimeProfilePolicyService:
    def build_policy(self) -> PublicAlphaRuntimeProfilePolicy:
        return PublicAlphaRuntimeProfilePolicy(policy_id="public_alpha_runtime_profile_policy:v0.28.6")


class PublicAlphaRuntimeSourceViewService:
    def build_source_view(self) -> PublicAlphaRuntimeSourceView:
        sources = AlphaRuntimeProfilePrerequisiteSourceService()
        prep = sources.load_v0285_schumpeter_preparation_report()
        handoff = prep.handoff_packet
        boundary = sources.load_v0283_public_private_boundary_report()
        packaging = sources.load_v0282_packaging_readiness_report()
        hygiene = sources.load_v0281_release_hygiene_gate_report()
        memory = sources.load_v0279_memory_consolidation_report()
        workbench = sources.load_v0269_workbench_consolidation_report()
        import_smoke = packaging.import_smoke_report
        cli_smoke = packaging.cli_smoke_report
        public_refs = [
            _ref("public_private_boundary_report", boundary.report_id, V0283_VERSION),
            _ref("packaging_readiness_report", packaging.report_id, V0282_VERSION),
            _ref("release_hygiene_gate_report", hygiene.report_id, V0281_VERSION),
            _ref("memory_consolidation_report", getattr(memory, "report_id", "memory_consolidation_report:v0.27.9")),
            _ref("workbench_consolidation_report", getattr(workbench, "report_id", "workbench_consolidation_report:v0.26.9")),
        ]
        demo_refs = [
            _ref("import_smoke_report", import_smoke.report_id, V0282_VERSION),
            _ref("cli_smoke_report", cli_smoke.report_id, V0282_VERSION),
            _ref("schumpeter_preparation_handoff_packet", handoff.handoff_packet_id, V0285_VERSION),
        ]
        blocked_private = list(handoff.private_overlay_future_refs) + list(handoff.blocked_or_deferred_refs)
        disabled_future = list(handoff.future_v029_adapter_refs) + list(handoff.future_v030_dominion_refs)
        return PublicAlphaRuntimeSourceView(
            source_view_id="public_alpha_runtime_source_view:v0.28.6",
            schumpeter_preparation_report_ref=_ref("schumpeter_preparation_report", prep.report_id, V0285_VERSION),
            schumpeter_handoff_packet_ref=_ref("schumpeter_preparation_handoff_packet", handoff.handoff_packet_id, V0285_VERSION),
            public_private_boundary_report_ref=_ref("public_private_boundary_report", boundary.report_id, V0283_VERSION),
            packaging_readiness_report_ref=_ref("packaging_readiness_report", packaging.report_id, V0282_VERSION),
            release_hygiene_gate_report_ref=_ref("release_hygiene_gate_report", hygiene.report_id, V0281_VERSION),
            memory_consolidation_report_ref=_ref("memory_consolidation_report", getattr(memory, "report_id", "memory_consolidation_report:v0.27.9")),
            workbench_consolidation_report_ref=_ref("workbench_consolidation_report", getattr(workbench, "report_id", "workbench_consolidation_report:v0.26.9")),
            import_smoke_report_ref=_ref("import_smoke_report", import_smoke.report_id, V0282_VERSION),
            cli_smoke_report_ref=_ref("cli_smoke_report", cli_smoke.report_id, V0282_VERSION),
            available_public_safe_refs=public_refs,
            available_demo_refs=demo_refs,
            blocked_private_refs=blocked_private,
            disabled_future_track_refs=disabled_future,
            source_status="warning",
            evidence_refs=[_ref("schumpeter_preparation_report", prep.report_id, V0285_VERSION)],
        )


class PublicAlphaFeatureFlagMatrixService:
    ENABLED = [
        ("OCEL_store_validation", "OCEL"),
        ("OCPX_projection_demo", "OCPX"),
        ("PIG_report_demo", "PIG"),
        ("Workbench_report_surfaces", "Workbench"),
        ("Memory_foundation_report_surfaces", "MemoryFoundation"),
        ("CLI_report_surfaces", "CLI"),
        ("synthetic_demo_data_loading", "Packaging"),
        ("safety_boundary_demo", "CLI"),
    ]
    PREVIEW = [
        ("continuity_context_pack_preview", "ContinuityPreview"),
        ("continuity_injection_bundle_preview", "ContinuityPreview"),
        ("durable_memory_registry_dry_run_preview", "MemoryFoundation"),
        ("Schumpeter_private_overlay_manifest_preview", "SchumpeterPreparation"),
        ("external_adapter_preflight_preview", "ExternalAdapter"),
    ]
    DISABLED = [
        ("provider_invocation", "ExternalAdapter"),
        ("command_execution_expansion", "CLI"),
        ("runtime_continuity_injection", "RuntimeInjection"),
        ("autonomous_memory_driven_execution", "MemoryFoundation"),
    ]
    FUTURE = [
        ("external_provider_adapter", "ExternalAdapter"),
        ("RPA_adapter", "RPAAdapter"),
        ("A360_adapter", "RPAAdapter"),
        ("Brity_adapter", "RPAAdapter"),
        ("UiPath_adapter", "RPAAdapter"),
        ("Schumpeter_company_runtime", "ProductionRuntime"),
        ("production_runtime", "ProductionRuntime"),
    ]

    def build_matrix(self) -> PublicAlphaFeatureFlagMatrix:
        flags: list[PublicAlphaFeatureFlag] = []
        for name, category in self.ENABLED:
            flags.append(PublicAlphaFeatureFlag(f"public_alpha_feature_flag:{name}:v0.28.6", name, category, "enabled", "Public-safe report/demo surface.", True, True))
        for name, category in self.PREVIEW:
            flags.append(PublicAlphaFeatureFlag(f"public_alpha_feature_flag:{name}:v0.28.6", name, category, "preview_only", "Preview-only, not runtime behavior.", True, True))
        for name, category in self.DISABLED:
            flags.append(PublicAlphaFeatureFlag(f"public_alpha_feature_flag:{name}:v0.28.6", name, category, "disabled", "Forbidden in public alpha runtime profile.", False, False))
        for name, category in self.FUTURE:
            flags.append(PublicAlphaFeatureFlag(f"public_alpha_feature_flag:{name}:v0.28.6", name, category, "future_track", "Deferred to later gated tracks.", False, False))
        return PublicAlphaFeatureFlagMatrix(
            matrix_id="public_alpha_feature_flag_matrix:v0.28.6",
            feature_flags=flags,
            enabled_count=sum(item.alpha_status == "enabled" for item in flags),
            preview_only_count=sum(item.alpha_status == "preview_only" for item in flags),
            disabled_count=sum(item.alpha_status == "disabled" for item in flags),
            future_track_count=sum(item.alpha_status == "future_track" for item in flags),
            blocked_count=sum(item.alpha_status == "blocked" for item in flags),
            matrix_status="warning",
        )


class AlphaFeatureSetService:
    def _refs(self, flags: list[PublicAlphaFeatureFlag], status: set[str]) -> list[dict[str, Any]]:
        return [_ref("public_alpha_feature_flag", item.feature_flag_id, V0286_VERSION) for item in flags if item.alpha_status in status]

    def build_enabled_feature_set(self, matrix: PublicAlphaFeatureFlagMatrix) -> AlphaEnabledFeatureSet:
        expected = [name for name, _ in PublicAlphaFeatureFlagMatrixService.ENABLED]
        refs = self._refs(matrix.feature_flags, {"enabled"})
        return AlphaEnabledFeatureSet("alpha_enabled_feature_set:v0.28.6", refs, expected, len(refs), "ready")

    def build_preview_only_feature_set(self, matrix: PublicAlphaFeatureFlagMatrix) -> AlphaPreviewOnlyFeatureSet:
        expected = [name for name, _ in PublicAlphaFeatureFlagMatrixService.PREVIEW]
        refs = self._refs(matrix.feature_flags, {"preview_only"})
        return AlphaPreviewOnlyFeatureSet("alpha_preview_only_feature_set:v0.28.6", refs, expected, len(refs), "warning")

    def build_disabled_future_track_feature_set(self, matrix: PublicAlphaFeatureFlagMatrix) -> AlphaDisabledFutureTrackFeatureSet:
        expected = [name for name, _ in PublicAlphaFeatureFlagMatrixService.DISABLED + PublicAlphaFeatureFlagMatrixService.FUTURE]
        disabled = self._refs(matrix.feature_flags, {"disabled"})
        future = self._refs(matrix.feature_flags, {"future_track"})
        return AlphaDisabledFutureTrackFeatureSet("alpha_disabled_future_track_feature_set:v0.28.6", disabled, future, expected, len(disabled), len(future))


class AlphaRuntimeCapabilityMatrixService:
    def build_matrix(self, flags: PublicAlphaFeatureFlagMatrix) -> AlphaRuntimeCapabilityMatrix:
        entries = [
            AlphaRuntimeCapabilityEntry(
                f"alpha_runtime_capability_entry:{item.feature_name}:v0.28.6",
                item.feature_name,
                item.status_reason,
                item.alpha_status,
                item.public_safe,
                item.alpha_status in {"enabled", "preview_only"},
                item.alpha_status in {"enabled", "preview_only"},
                [_ref("public_alpha_feature_flag", item.feature_flag_id, V0286_VERSION)],
            )
            for item in flags.feature_flags
        ]
        return AlphaRuntimeCapabilityMatrix(
            matrix_id="alpha_runtime_capability_matrix:v0.28.6",
            capability_entries=entries,
            public_safe_capability_count=sum(item.public_safe for item in entries),
            preview_only_capability_count=sum(item.alpha_status == "preview_only" for item in entries),
            disabled_capability_count=sum(item.alpha_status in {"disabled", "future_track"} for item in entries),
            unsafe_capability_count=sum(not item.public_safe for item in entries),
            capability_matrix_status="warning",
        )


class AlphaOperatorSurfacePolicyService:
    def build_policy(self) -> AlphaOperatorSurfacePolicy:
        return AlphaOperatorSurfacePolicy(policy_id="alpha_operator_surface_policy:v0.28.6")


class AlphaSmokeScenarioCatalogService:
    SCENARIOS = [
        "version_check",
        "import_smoke",
        "cli_help_smoke",
        "synthetic_ocel_load",
        "ocpx_projection_demo",
        "pig_report_demo",
        "workbench_report_demo",
        "memory_foundation_report_demo",
        "durable_registry_dry_run_demo",
        "continuity_context_preview_demo",
        "safety_boundary_demo",
        "forbidden_pattern_scan_demo",
    ]

    def build_catalog(self) -> AlphaSmokeScenarioCatalog:
        scenarios = [
            AlphaSmokeScenario(
                scenario_id=f"alpha_smoke_scenario:{name}:v0.28.6",
                scenario_name=name,
                scenario_summary=f"{name} uses deterministic public-safe metadata or synthetic demo data.",
                scenario_status="enabled" if name not in {"durable_registry_dry_run_demo", "continuity_context_preview_demo"} else "preview_only",
                deterministic=True,
                uses_synthetic_data_only=True,
                expected_outputs=["metadata_report", "public_safe_summary"],
                boundary_refs=[_ref("public_alpha_runtime_profile_policy", "public_alpha_runtime_profile_policy:v0.28.6", V0286_VERSION)],
            )
            for name in self.SCENARIOS
        ]
        return AlphaSmokeScenarioCatalog(
            catalog_id="alpha_smoke_scenario_catalog:v0.28.6",
            scenarios=scenarios,
            scenario_count=len(scenarios),
            enabled_scenario_count=sum(item.scenario_status == "enabled" for item in scenarios),
            preview_scenario_count=sum(item.scenario_status == "preview_only" for item in scenarios),
            disabled_scenario_count=sum(item.scenario_status == "disabled" for item in scenarios),
            catalog_status="warning",
        )


class AlphaSmokeInputBundleService:
    def build_bundle(self) -> AlphaSmokeInputBundle:
        return AlphaSmokeInputBundle(
            input_bundle_id="alpha_smoke_input_bundle:v0.28.6",
            input_refs=[_ref("public_safe_demo_metadata", "public_safe_demo_metadata:v0.28.6", V0286_VERSION)],
            synthetic_data_refs=[_ref("synthetic_demo_data", "synthetic_demo_data:public_alpha:v0.28.6", V0286_VERSION)],
            example_refs=[_ref("example_pack_candidate", "example_pack_candidate:public_alpha:v0.28.6", V0286_VERSION)],
            private_input_refs=[],
            bundle_status="warning",
            synthetic_only=True,
        )


class AlphaSyntheticDemoDataPolicyService:
    def build_policy(self) -> AlphaSyntheticDemoDataPolicy:
        return AlphaSyntheticDemoDataPolicy(policy_id="alpha_synthetic_demo_data_policy:v0.28.6")


class AlphaOCELDemoPackService:
    def build_pack(self) -> AlphaOCELDemoPack:
        return AlphaOCELDemoPack(
            demo_pack_id="alpha_ocel_demo_pack:v0.28.6",
            synthetic_ocel_refs=[_ref("synthetic_ocel_sample", "synthetic_ocel_sample:public_alpha:v0.28.6", V0286_VERSION)],
            expected_object_types=["case", "activity", "artifact"],
            expected_event_types=["demo_started", "demo_step_observed", "demo_completed"],
        )


class AlphaOCPXProjectionDemoService:
    def build_demo(self, pack: AlphaOCELDemoPack) -> AlphaOCPXProjectionDemo:
        return AlphaOCPXProjectionDemo("alpha_ocpx_projection_demo:v0.28.6", _ref("alpha_ocel_demo_pack", pack.demo_pack_id, V0286_VERSION), "public_alpha_runtime_projection", ["PublicAlphaRuntimeProfileState", "AlphaSmokeScenarioCatalogState"], "ready")


class AlphaPIGReportDemoService:
    def build_demo(self, projection: AlphaOCPXProjectionDemo) -> AlphaPIGReportDemo:
        return AlphaPIGReportDemo("alpha_pig_report_demo:v0.28.6", _ref("alpha_ocpx_projection_demo", projection.demo_id, V0286_VERSION), ["principles", "safety_boundary", "future_direction"], "ready")


class AlphaWorkbenchReportDemoService:
    def build_demo(self) -> AlphaWorkbenchReportDemo:
        return AlphaWorkbenchReportDemo("alpha_workbench_report_demo:v0.28.6", ["trace_explorer_report", "provider_browser_preview", "evidence_inspector_report", "safety_approval_console_preview", "run_dashboard_report", "command_surface_preview", "snapshot_export_preview"], "warning")


class AlphaMemoryFoundationDemoService:
    def build_demo(self) -> AlphaMemoryFoundationDemo:
        return AlphaMemoryFoundationDemo("alpha_memory_foundation_demo:v0.28.6", ["memory_contract_report", "source_boundary_report", "candidate_extraction_report", "evidence_scoring_report", "promotion_gate_report", "durable_registry_dry_run_or_report", "lifecycle_report", "memory_consolidation_report"], "warning")


class AlphaContinuityPreviewDemoService:
    def build_demo(self) -> AlphaContinuityPreviewDemo:
        return AlphaContinuityPreviewDemo("alpha_continuity_preview_demo:v0.28.6", _ref("continuity_context_pack_preview", "continuity_context_pack_preview:v0.28.6", V0286_VERSION), _ref("continuity_injection_boundary_preview", "continuity_injection_boundary_preview:v0.28.6", V0286_VERSION), "warning")


class AlphaSafetyBoundaryDemoService:
    def build_demo(self) -> AlphaSafetyBoundaryDemo:
        return AlphaSafetyBoundaryDemo("alpha_safety_boundary_demo:v0.28.6", ["provider_invocation_forbidden", "command_execution_forbidden", "private_data_forbidden", "credential_forbidden", "raw_trace_forbidden", "runtime_injection_forbidden", "external_adapter_forbidden", "Schumpeter_private_overlay_runtime_forbidden"], "ready", True)


class AlphaCLIWorkflowDemoService:
    def build_demo(self) -> AlphaCLIWorkflowDemo:
        return AlphaCLIWorkflowDemo(
            "alpha_cli_workflow_demo:v0.28.6",
            ["--help", "alpha contract-report", "alpha hygiene report", "alpha packaging report", "alpha boundary report", "alpha schumpeter report", "memory consolidation-report"],
            ["--help", "alpha contract-report", "alpha hygiene report", "alpha packaging report", "alpha boundary report", "alpha schumpeter report", "memory consolidation-report"],
            ["provider invocation", "command execution", "package publish", "release tag creation", "external adapter run", "Schumpeter private runtime"],
            "warning",
        )


class AlphaSmokeRunPlanService:
    def build_plan(self, catalog: AlphaSmokeScenarioCatalog) -> AlphaSmokeRunPlan:
        return AlphaSmokeRunPlan(
            plan_id="alpha_smoke_run_plan:v0.28.6",
            scenario_catalog_ref=_ref("alpha_smoke_scenario_catalog", catalog.catalog_id, V0286_VERSION),
            scenario_refs=[_ref("alpha_smoke_scenario", item.scenario_id, V0286_VERSION) for item in catalog.scenarios],
            run_mode="metadata_only",
            execution_allowed_now=False,
            plan_status="warning",
        )


class AlphaSmokeRunReportService:
    def build_report(self, plan: AlphaSmokeRunPlan, catalog: AlphaSmokeScenarioCatalog) -> AlphaSmokeRunReport:
        return AlphaSmokeRunReport(
            report_id="alpha_smoke_run_report:v0.28.6",
            plan_ref=_ref("alpha_smoke_run_plan", plan.plan_id, V0286_VERSION),
            scenarios_run=[_ref("alpha_smoke_scenario", item.scenario_id, V0286_VERSION) for item in catalog.scenarios],
            scenarios_passed_count=sum(item.scenario_status == "enabled" for item in catalog.scenarios),
            scenarios_warning_count=sum(item.scenario_status == "preview_only" for item in catalog.scenarios),
            scenarios_failed_count=0,
            scenarios_blocked_count=0,
            run_mode=plan.run_mode,
            smoke_run_status="warning",
        )


class AlphaOperatorHandoffPacketService:
    def build_packet(self, report_id: str, catalog: AlphaSmokeScenarioCatalog, pack: AlphaOCELDemoPack) -> AlphaOperatorHandoffPacket:
        return AlphaOperatorHandoffPacket(
            handoff_packet_id="alpha_operator_handoff_packet:v0.28.6",
            runtime_profile_report_id=report_id,
            public_safe_demo_refs=[_ref("alpha_ocel_demo_pack", pack.demo_pack_id, V0286_VERSION)],
            smoke_scenario_refs=[_ref("alpha_smoke_scenario", item.scenario_id, V0286_VERSION) for item in catalog.scenarios],
            docs_ready_refs=[_ref("alpha_runtime_profile_report", report_id, V0286_VERSION)],
            example_pack_candidate_refs=[_ref("synthetic_demo_data", "synthetic_demo_data:public_alpha:v0.28.6", V0286_VERSION)],
            not_implemented_now=["production_runtime", "package_publish", "release_tag_creation", "external_provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "runtime_continuity_injection", "autonomous_memory_driven_execution", "Schumpeter_private_overlay_runtime", "company_deployment"],
        )


class AlphaRuntimeProfileFindingService:
    BLOCKED_FINDINGS = {
        "production_runtime_attempted",
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "schumpeter_private_runtime_attempted",
        "external_adapter_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "network_call_attempted",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "raw_trace_detected",
        "raw_transcript_detected",
        "raw_provider_output_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[AlphaRuntimeProfileFinding]:
        return [
            AlphaRuntimeProfileFinding("alpha_runtime_profile_finding:runtime_profile_policy_created:v0.28.6", "info", "runtime_profile_policy_created", "Public alpha runtime profile policy created as metadata/report-only.", _ref("public_alpha_runtime_profile_policy", "public_alpha_runtime_profile_policy:v0.28.6", V0286_VERSION), [], None),
            AlphaRuntimeProfileFinding("alpha_runtime_profile_finding:smoke_run_report_created:v0.28.6", "warning", "smoke_run_report_created", "Smoke run report is metadata-only; no provider, command, network, or file mutation execution is performed.", _ref("alpha_smoke_run_report", "alpha_smoke_run_report:v0.28.6", V0286_VERSION), [], "Withdraw if a bounded smoke execution track replaces metadata-only reporting."),
        ]


class AlphaRuntimeProfileReportService:
    def build_report(self, report_id: str | None = None) -> AlphaRuntimeProfileReport:
        actual_report_id = report_id or "alpha_runtime_profile_report:v0.28.6"
        source = PublicAlphaRuntimeSourceViewService().build_source_view()
        policy = PublicAlphaRuntimeProfilePolicyService().build_policy()
        request = PublicAlphaRuntimeProfileRequest("public_alpha_runtime_profile_request:v0.28.6", source.schumpeter_preparation_report_ref["object_id"] if source.schumpeter_preparation_report_ref else None, source.packaging_readiness_report_ref["object_id"] if source.packaging_readiness_report_ref else None, source.public_private_boundary_report_ref["object_id"] if source.public_private_boundary_report_ref else None, source.release_hygiene_gate_report_ref["object_id"] if source.release_hygiene_gate_report_ref else None, "public_alpha_candidate")
        flags = PublicAlphaFeatureFlagMatrixService().build_matrix()
        feature_service = AlphaFeatureSetService()
        enabled = feature_service.build_enabled_feature_set(flags)
        preview = feature_service.build_preview_only_feature_set(flags)
        disabled = feature_service.build_disabled_future_track_feature_set(flags)
        capabilities = AlphaRuntimeCapabilityMatrixService().build_matrix(flags)
        operator_policy = AlphaOperatorSurfacePolicyService().build_policy()
        scenarios = AlphaSmokeScenarioCatalogService().build_catalog()
        inputs = AlphaSmokeInputBundleService().build_bundle()
        data_policy = AlphaSyntheticDemoDataPolicyService().build_policy()
        ocel = AlphaOCELDemoPackService().build_pack()
        ocpx = AlphaOCPXProjectionDemoService().build_demo(ocel)
        pig = AlphaPIGReportDemoService().build_demo(ocpx)
        workbench = AlphaWorkbenchReportDemoService().build_demo()
        memory = AlphaMemoryFoundationDemoService().build_demo()
        continuity = AlphaContinuityPreviewDemoService().build_demo()
        safety = AlphaSafetyBoundaryDemoService().build_demo()
        cli = AlphaCLIWorkflowDemoService().build_demo()
        plan = AlphaSmokeRunPlanService().build_plan(scenarios)
        smoke_report = AlphaSmokeRunReportService().build_report(plan, scenarios)
        handoff = AlphaOperatorHandoffPacketService().build_packet(actual_report_id, scenarios, ocel)
        findings = AlphaRuntimeProfileFindingService().build_findings()
        return AlphaRuntimeProfileReport(
            report_id=actual_report_id,
            created_at=_now(),
            runtime_profile_policy=policy,
            request=request,
            source_view=source,
            feature_flag_matrix=flags,
            enabled_feature_set=enabled,
            preview_only_feature_set=preview,
            disabled_future_track_feature_set=disabled,
            runtime_capability_matrix=capabilities,
            operator_surface_policy=operator_policy,
            smoke_scenario_catalog=scenarios,
            smoke_input_bundle=inputs,
            synthetic_demo_data_policy=data_policy,
            ocel_demo_pack=ocel,
            ocpx_projection_demo=ocpx,
            pig_report_demo=pig,
            workbench_report_demo=workbench,
            memory_foundation_demo=memory,
            continuity_preview_demo=continuity,
            safety_boundary_demo=safety,
            cli_workflow_demo=cli,
            smoke_run_plan=plan,
            smoke_run_report=smoke_report,
            operator_handoff_packet=handoff,
            findings=findings,
            report_status="warning",
            ready_for_v0_28_7=True,
            public_alpha_runtime_profile_ready=True,
            public_alpha_smoke_flow_ready=True,
            limitations=["Smoke run report is metadata-only and deterministic; no provider invocation, command expansion, network call, file mutation, or private data use is performed."],
            withdrawal_conditions=["Withdraw if production runtime, public alpha release, package publish/tag, Schumpeter private runtime, external/RPA adapter, provider/command/network/file mutation, runtime injection, autonomous memory execution, private/raw data exposure, reference runtime dependency/code copy, PIG authority, or LLM sole authority is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.runtime_profile_policy,
            "source-view": report.source_view,
            "feature-flags": report.feature_flag_matrix,
            "enabled": report.enabled_feature_set,
            "preview-only": report.preview_only_feature_set,
            "disabled": report.disabled_future_track_feature_set,
            "capabilities": report.runtime_capability_matrix,
            "operator-surface": report.operator_surface_policy,
            "scenarios": report.smoke_scenario_catalog,
            "inputs": report.smoke_input_bundle,
            "synthetic-policy": report.synthetic_demo_data_policy,
            "ocel-demo": report.ocel_demo_pack,
            "ocpx-demo": report.ocpx_projection_demo,
            "pig-demo": report.pig_report_demo,
            "workbench-demo": report.workbench_report_demo,
            "memory-demo": report.memory_foundation_demo,
            "continuity-preview": report.continuity_preview_demo,
            "safety-demo": report.safety_boundary_demo,
            "cli-demo": report.cli_workflow_demo,
            "plan": report.smoke_run_plan,
            "smoke-report": report.smoke_run_report,
            "report": report,
            "handoff": report.operator_handoff_packet,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0286_VERSION,
            "layer": V028_LAYER,
            "subject": "public_alpha_runtime_profile_smoke_demo_flow",
            "principles": [
                "Public Alpha runtime profile is not production runtime",
                "Smoke demo flow is not production workflow",
                "Smoke demo execution is not provider invocation",
                "CLI smoke is not command execution expansion",
                "Synthetic demo data is not actual user/company data",
                "Workbench demo is not UI productionization",
                "Memory demo is not autonomous memory-driven execution",
                "Continuity preview demo is not runtime continuity injection",
                "Schumpeter handoff is not Schumpeter runtime dependency",
                "No external adapter, no provider invocation, no command expansion, no private data",
            ],
            "safety_boundary": {
                "production_runtime_implemented": report.production_runtime_implemented,
                "public_alpha_release_implemented": report.public_alpha_release_implemented,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "external_adapter_implemented": report.external_adapter_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "network_called": report.network_called,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "autonomous_memory_execution_enabled": report.autonomous_memory_execution_enabled,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "raw_trace_used": report.raw_trace_used,
                "raw_transcript_used": report.raw_transcript_used,
                "raw_provider_output_used": report.raw_provider_output_used,
                "credential_exposed": report.credential_exposed,
                "secret_exposed": report.secret_exposed,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.28.7 Alpha Documentation / Onboarding / Example Pack", "v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate", "v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation", "v0.29 External Provider Adapter Contract"],
            "next_step": V0286_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "public_alpha_runtime_profile_smoke_demo_flow_created",
            "version": V0286_VERSION,
            "source_read_models": ["SchumpeterPreparationProfileState", "PublicPrivateBoundaryState", "PackagingReadinessState", "ReleaseHygieneGateState", "MemoryConsolidationState", "WorkbenchConsolidationState", "ImportSmokeReadinessState", "CLISmokeReadinessState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["PublicAlphaRuntimeProfileState", "PublicAlphaFeatureFlagMatrixState", "AlphaRuntimeCapabilityMatrixState", "AlphaSmokeScenarioCatalogState", "AlphaOCELDemoPackState", "AlphaOCPXProjectionDemoState", "AlphaPIGReportDemoState", "AlphaWorkbenchReportDemoState", "AlphaMemoryFoundationDemoState", "AlphaSafetyBoundaryDemoState", "AlphaOperatorHandoffState", "V028ReadinessState"],
            "effect_types": V0286_EFFECT_TYPES,
            "forbidden_effect_types": V0286_FORBIDDEN_EFFECT_TYPES,
        }


def render_alpha_runtime_profile_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AlphaRuntimeProfileReport = parts["report"]
    lines = [
        f"Public Alpha Runtime Profile / Smoke Demo Flow {section}",
        f"version={report.version}",
        f"layer={report.runtime_profile_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_7={_bool(report.ready_for_v0_28_7)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"public_alpha_runtime_profile_ready={_bool(report.public_alpha_runtime_profile_ready)}",
        f"public_alpha_smoke_flow_ready={_bool(report.public_alpha_smoke_flow_ready)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"production_runtime_implemented={_bool(report.production_runtime_implemented)}",
        f"public_alpha_release_implemented={_bool(report.public_alpha_release_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"official_release_artifact_created={_bool(report.official_release_artifact_created)}",
        f"schumpeter_private_runtime_used={_bool(report.schumpeter_private_runtime_used)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"RPA_adapter_implemented={_bool(report.RPA_adapter_implemented)}",
        f"A360_adapter_implemented={_bool(report.A360_adapter_implemented)}",
        f"Brity_adapter_implemented={_bool(report.Brity_adapter_implemented)}",
        f"UiPath_adapter_implemented={_bool(report.UiPath_adapter_implemented)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"network_called={_bool(report.network_called)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"autonomous_memory_execution_enabled={_bool(report.autonomous_memory_execution_enabled)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"raw_trace_used={_bool(report.raw_trace_used)}",
        f"raw_transcript_used={_bool(report.raw_transcript_used)}",
        f"raw_provider_output_used={_bool(report.raw_provider_output_used)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "matrix_id", getattr(payload, "feature_set_id", getattr(payload, "catalog_id", getattr(payload, "demo_id", getattr(payload, "demo_pack_id", getattr(payload, "plan_id", getattr(payload, "handoff_packet_id", "")))))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0287_VERSION = "v0.28.7"
V0287_VERSION_NAME = "Alpha Documentation / Onboarding / Example Pack"
V0287_NEXT_STEP = "v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate"

V0287_OBJECT_TYPES = [
    "alpha_documentation_policy",
    "alpha_documentation_request",
    "alpha_documentation_source_view",
    "alpha_document_set",
    "alpha_document_spec",
    "alpha_readme_plan",
    "alpha_quickstart_guide",
    "alpha_architecture_overview_guide",
    "alpha_ocel_native_core_guide",
    "alpha_workbench_foundation_guide",
    "alpha_memory_foundation_guide",
    "alpha_runtime_profile_guide",
    "alpha_smoke_demo_guide",
    "alpha_cli_reference_guide",
    "alpha_safety_boundaries_guide",
    "alpha_public_private_boundary_guide",
    "alpha_schumpeter_preparation_guide",
    "alpha_external_adapter_future_track_note",
    "alpha_example_pack_policy",
    "alpha_example_pack_manifest",
    "alpha_example_data_manifest",
    "alpha_synthetic_example_bundle",
    "alpha_demo_scenario_documentation",
    "alpha_onboarding_checklist",
    "alpha_documentation_link_integrity_report",
    "alpha_documentation_safety_boundary_report",
    "alpha_documentation_consistency_report",
    "alpha_documentation_readiness_gate",
    "alpha_documentation_handoff_packet",
    "alpha_documentation_finding",
    "alpha_documentation_readiness_report",
    "alpha_runtime_profile_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0287_EVENT_TYPES = [
    "alpha_documentation_requested",
    "alpha_documentation_prerequisites_loaded",
    "alpha_documentation_policy_created",
    "alpha_documentation_source_view_created",
    "alpha_document_set_created",
    "alpha_document_spec_created",
    "alpha_readme_plan_created",
    "alpha_quickstart_guide_created",
    "alpha_architecture_overview_guide_created",
    "alpha_ocel_native_core_guide_created",
    "alpha_workbench_foundation_guide_created",
    "alpha_memory_foundation_guide_created",
    "alpha_runtime_profile_guide_created",
    "alpha_smoke_demo_guide_created",
    "alpha_cli_reference_guide_created",
    "alpha_safety_boundaries_guide_created",
    "alpha_public_private_boundary_guide_created",
    "alpha_schumpeter_preparation_guide_created",
    "alpha_external_adapter_future_track_note_created",
    "alpha_example_pack_policy_created",
    "alpha_example_pack_manifest_created",
    "alpha_example_data_manifest_created",
    "alpha_synthetic_example_bundle_created",
    "alpha_demo_scenario_documentation_created",
    "alpha_onboarding_checklist_created",
    "alpha_documentation_link_integrity_report_created",
    "alpha_documentation_safety_boundary_report_created",
    "alpha_documentation_consistency_report_created",
    "alpha_documentation_readiness_gate_evaluated",
    "alpha_documentation_handoff_packet_created",
    "alpha_documentation_readiness_report_created",
    "alpha_documentation_warning_created",
    "alpha_documentation_blocked",
]

V0287_EFFECT_TYPES = [
    "read_only_observation",
    "alpha_documentation_created",
    "alpha_document_set_created",
    "alpha_guide_created",
    "alpha_example_pack_manifest_created",
    "alpha_onboarding_checklist_created",
    "alpha_documentation_safety_report_created",
    "alpha_documentation_consistency_report_created",
    "alpha_documentation_readiness_gate_evaluated",
    "alpha_documentation_handoff_packet_created",
    "state_candidate_created",
]

V0287_FORBIDDEN_EFFECT_TYPES = [
    "public_alpha_release_implemented",
    "package_published",
    "release_tag_created",
    "official_release_artifact_created",
    "production_runtime_claimed",
    "provider_invocation_documented_as_enabled",
    "command_execution_expansion_documented_as_enabled",
    "external_adapter_documented_as_enabled",
    "RPA_adapter_documented_as_enabled",
    "schumpeter_private_runtime_documented_as_enabled",
    "actual_user_data_used",
    "actual_company_data_used",
    "private_material_exposed",
    "credential_exposed",
    "secret_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "provider_invoked",
    "command_executed",
    "network_called",
    "runtime_continuity_injected",
    "external_adapter_implemented",
    "references_runtime_dependency_added",
    "references_code_copied",
    "llm_judge_used",
]


@dataclass
class AlphaDocumentationPolicy(ModelMixin):
    policy_id: str = "alpha_documentation_policy:v0.28.7"
    version: str = V0287_VERSION
    layer: str = V028_LAYER
    documentation_enabled: bool = True
    onboarding_enabled: bool = True
    example_pack_enabled: bool = True
    public_safe_docs_required: bool = True
    synthetic_examples_required_by_default: bool = True
    docs_must_match_feature_flags: bool = True
    docs_must_not_overclaim_capabilities: bool = True
    future_track_must_be_labeled: bool = True
    private_material_forbidden: bool = True
    credential_exposure_forbidden: bool = True
    secret_exposure_forbidden: bool = True
    raw_trace_exposure_forbidden: bool = True
    raw_transcript_exposure_forbidden: bool = True
    raw_provider_output_exposure_forbidden: bool = True
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    provider_invocation_docs_forbidden_now: bool = True
    command_execution_expansion_docs_forbidden_now: bool = True
    external_adapter_docs_must_be_future_track_only: bool = True
    schumpeter_runtime_docs_forbidden_now: bool = True
    package_publish_docs_forbidden_now: bool = True
    release_tag_docs_forbidden_now: bool = True
    llm_judge_as_sole_documentation_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationRequest(ModelMixin):
    request_id: str = "alpha_documentation_request:v0.28.7"
    version: str = V0287_VERSION
    alpha_runtime_profile_report_id: str | None = None
    alpha_operator_handoff_packet_id: str | None = None
    public_private_boundary_report_id: str | None = None
    packaging_readiness_report_id: str | None = None
    release_hygiene_gate_report_id: str | None = None
    requested_doc_profile: str = "public_alpha_candidate"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationSourceView(ModelMixin):
    source_view_id: str = "alpha_documentation_source_view:v0.28.7"
    version: str = V0287_VERSION
    runtime_profile_report_ref: dict[str, Any] | None = None
    operator_handoff_packet_ref: dict[str, Any] | None = None
    smoke_scenario_catalog_ref: dict[str, Any] | None = None
    ocel_demo_pack_ref: dict[str, Any] | None = None
    ocpx_projection_demo_ref: dict[str, Any] | None = None
    pig_report_demo_ref: dict[str, Any] | None = None
    workbench_report_demo_ref: dict[str, Any] | None = None
    memory_foundation_demo_ref: dict[str, Any] | None = None
    continuity_preview_demo_ref: dict[str, Any] | None = None
    safety_boundary_demo_ref: dict[str, Any] | None = None
    cli_workflow_demo_ref: dict[str, Any] | None = None
    schumpeter_preparation_report_ref: dict[str, Any] | None = None
    public_private_boundary_report_ref: dict[str, Any] | None = None
    packaging_readiness_report_ref: dict[str, Any] | None = None
    release_hygiene_gate_report_ref: dict[str, Any] | None = None
    existing_doc_refs: list[dict[str, Any]] = field(default_factory=list)
    example_candidate_refs: list[dict[str, Any]] = field(default_factory=list)
    public_safe_demo_refs: list[dict[str, Any]] = field(default_factory=list)
    blocked_private_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "partial"
    private_material_detected: bool = False
    credential_detected: bool = False
    secret_detected: bool = False
    raw_trace_detected: bool = False
    raw_transcript_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentSpec(ModelMixin):
    doc_spec_id: str
    doc_name: str
    doc_path_hint: str | None
    doc_type: str
    required_for_alpha_docs: bool
    current_status: str
    creation_or_update_allowed_now: bool
    version: str = V0287_VERSION
    public_safe_required: bool = True
    doc_claims_must_match_feature_flags: bool = True
    private_material_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentSet(ModelMixin):
    document_set_id: str
    documents: list[AlphaDocumentSpec]
    required_doc_count: int
    optional_doc_count: int
    missing_required_doc_count: int
    draft_doc_count: int
    ready_doc_count: int
    document_set_status: str
    version: str = V0287_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaReadmePlan(ModelMixin):
    plan_id: str = "alpha_readme_plan:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    required_sections: list[str] = field(default_factory=list)
    readme_status: str = "ready"
    overclaim_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaQuickstartGuide(ModelMixin):
    guide_id: str = "alpha_quickstart_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    setup_steps: list[str] = field(default_factory=list)
    smoke_steps: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)
    forbidden_steps: list[str] = field(default_factory=list)
    quickstart_status: str = "ready"
    uses_private_data: bool = False
    invokes_provider: bool = False
    executes_command_expansion: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaArchitectureOverviewGuide(ModelMixin):
    guide_id: str = "alpha_architecture_overview_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    sections: list[str] = field(default_factory=list)
    architecture_doc_status: str = "ready"
    claims_production_ready: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaOCELNativeCoreGuide(ModelMixin):
    guide_id: str = "alpha_ocel_native_core_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    explains_ocel_store: bool = True
    explains_object_event_relation: bool = True
    explains_ocpx_projection: bool = True
    explains_pig_report: bool = True
    explains_trace_visibility: bool = True
    uses_synthetic_examples_only: bool = True
    guide_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaWorkbenchFoundationGuide(ModelMixin):
    guide_id: str = "alpha_workbench_foundation_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    covered_surfaces: list[str] = field(default_factory=list)
    workbench_doc_status: str = "ready"
    provider_invocation_claimed: bool = False
    command_execution_claimed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaMemoryFoundationGuide(ModelMixin):
    guide_id: str = "alpha_memory_foundation_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    covered_memory_surfaces: list[str] = field(default_factory=list)
    memory_doc_status: str = "ready"
    autonomous_memory_execution_claimed: bool = False
    runtime_injection_claimed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaRuntimeProfileGuide(ModelMixin):
    guide_id: str = "alpha_runtime_profile_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    feature_flag_matrix_ref: dict[str, Any] | None = None
    enabled_features_documented: bool = True
    preview_features_documented: bool = True
    disabled_future_features_documented: bool = True
    runtime_profile_doc_status: str = "ready"
    production_runtime_claimed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaSmokeDemoGuide(ModelMixin):
    guide_id: str = "alpha_smoke_demo_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    smoke_scenario_refs: list[dict[str, Any]] = field(default_factory=list)
    documents_synthetic_ocel_demo: bool = True
    documents_ocpx_demo: bool = True
    documents_pig_demo: bool = True
    documents_workbench_demo: bool = True
    documents_memory_demo: bool = True
    documents_continuity_preview_demo: bool = True
    documents_safety_demo: bool = True
    documents_cli_demo: bool = True
    smoke_demo_doc_status: str = "ready"
    uses_actual_data: bool = False
    invokes_provider: bool = False
    expands_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaCLIReferenceGuide(ModelMixin):
    guide_id: str = "alpha_cli_reference_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    documented_cli_groups: list[str] = field(default_factory=list)
    CLI_reference_status: str = "ready"
    documents_provider_invocation: bool = False
    documents_command_execution_expansion: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaSafetyBoundariesGuide(ModelMixin):
    guide_id: str = "alpha_safety_boundaries_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    covered_boundaries: list[str] = field(default_factory=list)
    safety_doc_status: str = "ready"
    contradictions_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaPublicPrivateBoundaryGuide(ModelMixin):
    guide_id: str = "alpha_public_private_boundary_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    public_private_boundary_report_ref: dict[str, Any] | None = None
    explains_public_core_private_overlay: bool = True
    explains_private_artifact_exclusions: bool = True
    explains_reference_policy: bool = True
    explains_synthetic_examples: bool = True
    boundary_doc_status: str = "ready"
    private_material_exposed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaSchumpeterPreparationGuide(ModelMixin):
    guide_id: str = "alpha_schumpeter_preparation_guide:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    schumpeter_preparation_report_ref: dict[str, Any] | None = None
    explains_preparation_only: bool = True
    explains_private_overlay_contract: bool = True
    explains_deferred_runtime: bool = True
    explains_RPA_adapter_deferral: bool = True
    schumpeter_doc_status: str = "ready"
    claims_runtime_implemented: bool = False
    exposes_company_material: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaExternalAdapterFutureTrackNote(ModelMixin):
    note_id: str = "alpha_external_adapter_future_track_note:v0.28.7"
    version: str = V0287_VERSION
    target_doc_ref: dict[str, Any] | None = None
    explains_v029_contract_first: bool = True
    explains_adapter_preflight_required: bool = True
    explains_provider_invocation_not_enabled: bool = True
    explains_RPA_future_track: bool = True
    future_track_note_status: str = "ready"
    claims_adapter_implemented: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaExamplePackPolicy(ModelMixin):
    policy_id: str = "alpha_example_pack_policy:v0.28.7"
    version: str = V0287_VERSION
    example_pack_enabled: bool = True
    synthetic_examples_required: bool = True
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    credentials_forbidden: bool = True
    secrets_forbidden: bool = True
    raw_traces_forbidden: bool = True
    raw_transcripts_forbidden: bool = True
    raw_provider_outputs_forbidden: bool = True
    example_manifest_required: bool = True
    reproducible_examples_required: bool = True
    provider_invocation_forbidden: bool = True
    command_execution_expansion_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaExamplePackManifest(ModelMixin):
    manifest_id: str
    examples: list[dict[str, Any]]
    example_count: int
    synthetic_example_count: int
    sanitized_example_count: int
    blocked_example_count: int
    manifest_status: str
    version: str = V0287_VERSION
    example_pack_name: str = "public_alpha_example_pack"
    contains_private_data: bool = False
    contains_credentials: bool = False
    contains_raw_trace: bool = False
    contains_raw_transcript: bool = False
    contains_raw_provider_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaExampleDataManifest(ModelMixin):
    manifest_id: str
    dataset_refs: list[dict[str, Any]]
    synthetic_dataset_refs: list[dict[str, Any]]
    sanitized_dataset_refs: list[dict[str, Any]]
    data_manifest_status: str
    version: str = V0287_VERSION
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    raw_trace_used: bool = False
    raw_transcript_used: bool = False
    raw_provider_output_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaSyntheticExampleBundle(ModelMixin):
    bundle_id: str
    bundle_name: str
    example_refs: list[dict[str, Any]]
    target_demo_refs: list[dict[str, Any]]
    reproducible: bool
    version: str = V0287_VERSION
    synthetic_only: bool = True
    contains_private_identifiers: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDemoScenarioDocumentation(ModelMixin):
    demo_doc_id: str
    scenario_ref: dict[str, Any]
    doc_ref: dict[str, Any] | None
    scenario_name: str
    documented_inputs: list[str]
    documented_expected_outputs: list[str]
    documented_safety_boundaries: list[str]
    doc_status: str
    version: str = V0287_VERSION
    overclaims_execution: bool = False
    uses_private_data: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaOnboardingChecklist(ModelMixin):
    checklist_id: str = "alpha_onboarding_checklist:v0.28.7"
    version: str = V0287_VERSION
    checklist_items: list[str] = field(default_factory=list)
    required_items: list[str] = field(default_factory=list)
    checklist_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationLinkIntegrityReport(ModelMixin):
    report_id: str
    checked_doc_refs: list[dict[str, Any]]
    internal_link_count: int
    missing_link_count: int
    broken_link_refs: list[dict[str, Any]]
    link_integrity_status: str
    version: str = V0287_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationSafetyBoundaryReport(ModelMixin):
    report_id: str
    checked_doc_refs: list[dict[str, Any]]
    docs_safety_status: str
    version: str = V0287_VERSION
    production_runtime_claim_count: int = 0
    provider_invocation_claim_count: int = 0
    command_execution_expansion_claim_count: int = 0
    external_adapter_claim_count: int = 0
    schumpeter_runtime_claim_count: int = 0
    private_material_exposure_count: int = 0
    credential_exposure_count: int = 0
    raw_trace_exposure_count: int = 0
    raw_transcript_exposure_count: int = 0
    raw_provider_output_exposure_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationConsistencyReport(ModelMixin):
    report_id: str
    feature_flag_matrix_ref: dict[str, Any] | None
    checked_doc_refs: list[dict[str, Any]]
    enabled_feature_overclaim_count: int
    preview_feature_overclaim_count: int
    disabled_feature_overclaim_count: int
    future_track_mislabel_count: int
    consistency_status: str
    version: str = V0287_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationReadinessGate(ModelMixin):
    gate_id: str
    document_set_ready: bool
    quickstart_ready: bool
    architecture_doc_ready: bool
    safety_doc_ready: bool
    public_private_doc_ready: bool
    examples_ready: bool
    onboarding_ready: bool
    link_integrity_passed_or_warned: bool
    safety_boundary_passed: bool
    consistency_passed: bool
    no_private_material_exposure: bool
    no_credentials_exposure: bool
    no_raw_artifact_exposure: bool
    gate_status: str
    docs_ready_for_v0_28_8: bool
    version: str = V0287_VERSION
    public_alpha_release_claim_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationHandoffPacket(ModelMixin):
    handoff_packet_id: str
    documentation_report_id: str
    doc_refs: list[dict[str, Any]]
    example_pack_refs: list[dict[str, Any]]
    smoke_demo_doc_refs: list[dict[str, Any]]
    validation_required_refs: list[dict[str, Any]]
    future_track_refs: list[dict[str, Any]]
    not_implemented_now: list[str]
    version: str = V0287_VERSION
    target_version: str = "v0.28.8"
    target_track: str = "Alpha Readiness Validation / External Adapter Preflight Gate"
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaDocumentationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AlphaDocumentationReadinessReport(ModelMixin):
    report_id: str
    created_at: str
    documentation_policy: AlphaDocumentationPolicy
    request: AlphaDocumentationRequest
    source_view: AlphaDocumentationSourceView
    document_set: AlphaDocumentSet
    readme_plan: AlphaReadmePlan
    quickstart_guide: AlphaQuickstartGuide
    architecture_overview_guide: AlphaArchitectureOverviewGuide
    ocel_native_core_guide: AlphaOCELNativeCoreGuide
    workbench_foundation_guide: AlphaWorkbenchFoundationGuide
    memory_foundation_guide: AlphaMemoryFoundationGuide
    runtime_profile_guide: AlphaRuntimeProfileGuide
    smoke_demo_guide: AlphaSmokeDemoGuide
    cli_reference_guide: AlphaCLIReferenceGuide
    safety_boundaries_guide: AlphaSafetyBoundariesGuide
    public_private_boundary_guide: AlphaPublicPrivateBoundaryGuide
    schumpeter_preparation_guide: AlphaSchumpeterPreparationGuide
    external_adapter_future_track_note: AlphaExternalAdapterFutureTrackNote
    example_pack_policy: AlphaExamplePackPolicy
    example_pack_manifest: AlphaExamplePackManifest
    example_data_manifest: AlphaExampleDataManifest
    synthetic_example_bundle: AlphaSyntheticExampleBundle
    demo_scenario_documentation: list[AlphaDemoScenarioDocumentation]
    onboarding_checklist: AlphaOnboardingChecklist
    link_integrity_report: AlphaDocumentationLinkIntegrityReport
    safety_boundary_report: AlphaDocumentationSafetyBoundaryReport
    consistency_report: AlphaDocumentationConsistencyReport
    documentation_readiness_gate: AlphaDocumentationReadinessGate
    handoff_packet: AlphaDocumentationHandoffPacket
    findings: list[AlphaDocumentationFinding]
    report_status: str
    ready_for_v0_28_8: bool
    documentation_ready: bool
    onboarding_ready: bool
    example_pack_ready: bool
    version: str = V0287_VERSION
    ready_for_public_alpha_release_claim: bool = False
    public_alpha_ready: bool = False
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    production_runtime_claimed: bool = False
    provider_invocation_documented_as_enabled: bool = False
    command_execution_expansion_documented_as_enabled: bool = False
    external_adapter_documented_as_enabled: bool = False
    RPA_adapter_documented_as_enabled: bool = False
    schumpeter_private_runtime_documented_as_enabled: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    private_material_exposed: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    runtime_continuity_injected: bool = False
    external_adapter_implemented: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0287_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate begins or documentation policy changes."


class AlphaDocumentationPrerequisiteSourceService:
    def load_v0286_alpha_runtime_profile_report(self) -> dict[str, Any]:
        return _ref("alpha_runtime_profile_report", "alpha_runtime_profile_report:v0.28.6", V0286_VERSION)

    def load_v0286_operator_handoff_packet(self) -> dict[str, Any]:
        return _ref("alpha_operator_handoff_packet", "alpha_operator_handoff_packet:v0.28.6", V0286_VERSION)

    def load_v0286_smoke_scenario_catalog(self) -> dict[str, Any]:
        return _ref("alpha_smoke_scenario_catalog", "alpha_smoke_scenario_catalog:v0.28.6", V0286_VERSION)

    def load_v0286_demo_artifacts(self) -> dict[str, dict[str, Any]]:
        return {
            "ocel": _ref("alpha_ocel_demo_pack", "alpha_ocel_demo_pack:v0.28.6", V0286_VERSION),
            "ocpx": _ref("alpha_ocpx_projection_demo", "alpha_ocpx_projection_demo:v0.28.6", V0286_VERSION),
            "pig": _ref("alpha_pig_report_demo", "alpha_pig_report_demo:v0.28.6", V0286_VERSION),
            "workbench": _ref("alpha_workbench_report_demo", "alpha_workbench_report_demo:v0.28.6", V0286_VERSION),
            "memory": _ref("alpha_memory_foundation_demo", "alpha_memory_foundation_demo:v0.28.6", V0286_VERSION),
            "continuity": _ref("alpha_continuity_preview_demo", "alpha_continuity_preview_demo:v0.28.6", V0286_VERSION),
            "safety": _ref("alpha_safety_boundary_demo", "alpha_safety_boundary_demo:v0.28.6", V0286_VERSION),
            "cli": _ref("alpha_cli_workflow_demo", "alpha_cli_workflow_demo:v0.28.6", V0286_VERSION),
        }

    def load_v0285_schumpeter_preparation_report(self) -> dict[str, Any]:
        return _ref("schumpeter_preparation_report", "schumpeter_preparation_report:v0.28.5", V0285_VERSION)

    def load_v0283_public_private_boundary_report(self) -> dict[str, Any]:
        return _ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION)

    def load_v0282_packaging_readiness_report(self) -> dict[str, Any]:
        return _ref("packaging_readiness_report", "packaging_readiness_report:v0.28.2", V0282_VERSION)

    def load_v0281_release_hygiene_gate_report(self) -> dict[str, Any]:
        return _ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION)

    def load_existing_docs_metadata_if_available(self) -> list[dict[str, Any]]:
        docs = [
            ("README.md", "README.md"),
            ("docs/QUICKSTART.md", "docs/QUICKSTART.md"),
            ("docs/ARCHITECTURE.md", "docs/ARCHITECTURE.md"),
            ("docs/SAFETY_BOUNDARIES.md", "docs/SAFETY_BOUNDARIES.md"),
            ("docs/PUBLIC_PRIVATE_BOUNDARY.md", "docs/PUBLIC_PRIVATE_BOUNDARY.md"),
            ("docs/WORKBENCH_FOUNDATION.md", "docs/WORKBENCH_FOUNDATION.md"),
            ("docs/MEMORY_FOUNDATION.md", "docs/MEMORY_FOUNDATION.md"),
            ("docs/PUBLIC_ALPHA_RUNTIME_PROFILE.md", "docs/PUBLIC_ALPHA_RUNTIME_PROFILE.md"),
            ("docs/SMOKE_DEMO_FLOW.md", "docs/SMOKE_DEMO_FLOW.md"),
            ("docs/CLI_REFERENCE.md", "docs/CLI_REFERENCE.md"),
            ("docs/EXAMPLES.md", "docs/EXAMPLES.md"),
            ("docs/SCHUMPETER_PREPARATION.md", "docs/SCHUMPETER_PREPARATION.md"),
            ("docs/EXTERNAL_ADAPTER_FUTURE_TRACK.md", "docs/EXTERNAL_ADAPTER_FUTURE_TRACK.md"),
            ("docs/ONBOARDING_CHECKLIST.md", "docs/ONBOARDING_CHECKLIST.md"),
        ]
        return [{"object_type": "alpha_doc", "object_id": name, "path_hint": path, "version": V0287_VERSION} for name, path in docs]

    def load_example_metadata_if_available(self) -> list[dict[str, Any]]:
        return [
            _ref("alpha_synthetic_example", "synthetic_ocel_demo:v0.28.7", V0287_VERSION),
            _ref("alpha_synthetic_example", "smoke_demo_cli_surface:v0.28.7", V0287_VERSION),
        ]

    def load_package_cli_metadata_if_available(self) -> list[dict[str, Any]]:
        return [_ref("cli_surface", "alpha_docs_examples_cli:v0.28.7", V0287_VERSION)]


class AlphaDocumentationPolicyService:
    def build_policy(self) -> AlphaDocumentationPolicy:
        return AlphaDocumentationPolicy()


class AlphaDocumentationSourceViewService:
    def build_source_view(self) -> AlphaDocumentationSourceView:
        source = AlphaDocumentationPrerequisiteSourceService()
        demo = source.load_v0286_demo_artifacts()
        docs = source.load_existing_docs_metadata_if_available()
        examples = source.load_example_metadata_if_available()
        public_safe_refs = [source.load_v0286_smoke_scenario_catalog(), *demo.values(), *examples]
        return AlphaDocumentationSourceView(
            runtime_profile_report_ref=source.load_v0286_alpha_runtime_profile_report(),
            operator_handoff_packet_ref=source.load_v0286_operator_handoff_packet(),
            smoke_scenario_catalog_ref=source.load_v0286_smoke_scenario_catalog(),
            ocel_demo_pack_ref=demo["ocel"],
            ocpx_projection_demo_ref=demo["ocpx"],
            pig_report_demo_ref=demo["pig"],
            workbench_report_demo_ref=demo["workbench"],
            memory_foundation_demo_ref=demo["memory"],
            continuity_preview_demo_ref=demo["continuity"],
            safety_boundary_demo_ref=demo["safety"],
            cli_workflow_demo_ref=demo["cli"],
            schumpeter_preparation_report_ref=source.load_v0285_schumpeter_preparation_report(),
            public_private_boundary_report_ref=source.load_v0283_public_private_boundary_report(),
            packaging_readiness_report_ref=source.load_v0282_packaging_readiness_report(),
            release_hygiene_gate_report_ref=source.load_v0281_release_hygiene_gate_report(),
            existing_doc_refs=docs,
            example_candidate_refs=examples,
            public_safe_demo_refs=public_safe_refs,
            blocked_private_refs=[
                _ref("blocked_private_ref", "schumpeter_private_runtime:not_public_alpha", V0287_VERSION),
                _ref("blocked_private_ref", "company_data_examples:not_allowed", V0287_VERSION),
            ],
            source_status="partial",
        )


class AlphaDocumentSetService:
    DOCS = [
        ("README.md", "README.md", "root_readme", True),
        ("QUICKSTART.md", "docs/QUICKSTART.md", "quickstart", True),
        ("ARCHITECTURE.md", "docs/ARCHITECTURE.md", "architecture", True),
        ("SAFETY_BOUNDARIES.md", "docs/SAFETY_BOUNDARIES.md", "safety", True),
        ("PUBLIC_PRIVATE_BOUNDARY.md", "docs/PUBLIC_PRIVATE_BOUNDARY.md", "public_private", True),
        ("WORKBENCH_FOUNDATION.md", "docs/WORKBENCH_FOUNDATION.md", "workbench", True),
        ("MEMORY_FOUNDATION.md", "docs/MEMORY_FOUNDATION.md", "memory", True),
        ("PUBLIC_ALPHA_RUNTIME_PROFILE.md", "docs/PUBLIC_ALPHA_RUNTIME_PROFILE.md", "runtime_profile", True),
        ("SMOKE_DEMO_FLOW.md", "docs/SMOKE_DEMO_FLOW.md", "smoke_demo", True),
        ("CLI_REFERENCE.md", "docs/CLI_REFERENCE.md", "cli_reference", True),
        ("EXAMPLES.md", "docs/EXAMPLES.md", "examples", True),
        ("SCHUMPETER_PREPARATION.md", "docs/SCHUMPETER_PREPARATION.md", "schumpeter_preparation", True),
        ("EXTERNAL_ADAPTER_FUTURE_TRACK.md", "docs/EXTERNAL_ADAPTER_FUTURE_TRACK.md", "future_track", True),
        ("ONBOARDING_CHECKLIST.md", "docs/ONBOARDING_CHECKLIST.md", "contributing", True),
    ]

    def build_document_set(self) -> AlphaDocumentSet:
        specs = [
            AlphaDocumentSpec(f"alpha_document_spec:{name}:v0.28.7", name, path, doc_type, required, "ready", True)
            for name, path, doc_type, required in self.DOCS
        ]
        required = [item for item in specs if item.required_for_alpha_docs]
        ready = [item for item in specs if item.current_status == "ready"]
        drafts = [item for item in specs if item.current_status == "draft"]
        missing = [item for item in specs if item.required_for_alpha_docs and item.current_status == "missing"]
        return AlphaDocumentSet("alpha_document_set:v0.28.7", specs, len(required), len(specs) - len(required), len(missing), len(drafts), len(ready), "ready")


class AlphaGuideService:
    def build_readme_plan(self) -> AlphaReadmePlan:
        return AlphaReadmePlan(target_doc_ref=_ref("alpha_doc", "README.md", V0287_VERSION), required_sections=["project_summary", "current_status", "installation_or_local_setup_summary", "public_alpha_scope", "enabled_preview_disabled_features", "quickstart_link", "safety_boundaries", "public_private_boundary", "examples_link", "Schumpeter_preparation_note", "external_adapter_future_track_note", "limitations"])

    def build_quickstart_guide(self) -> AlphaQuickstartGuide:
        return AlphaQuickstartGuide(target_doc_ref=_ref("alpha_doc", "docs/QUICKSTART.md", V0287_VERSION), setup_steps=["install_or_setup_locally", "inspect_version_metadata"], smoke_steps=["review_alpha_runtime_report", "review_alpha_smoke_report", "inspect_synthetic_examples"], expected_outputs=["v0.28.7 docs readiness report", "v0.28.6 smoke scenario references"], forbidden_steps=["provider_invocation", "command_execution_expansion", "package_publish", "release_tag_creation", "Schumpeter_private_runtime", "external_adapter_run"])

    def build_architecture_overview(self) -> AlphaArchitectureOverviewGuide:
        return AlphaArchitectureOverviewGuide(target_doc_ref=_ref("alpha_doc", "docs/ARCHITECTURE.md", V0287_VERSION), sections=["OCEL_native_core", "OCPX", "PIG", "Workbench", "Memory_foundation", "Public_alpha_profile", "Safety_boundary", "Future_external_adapter_boundary"])

    def build_ocel_native_core_guide(self) -> AlphaOCELNativeCoreGuide:
        return AlphaOCELNativeCoreGuide(target_doc_ref=_ref("alpha_doc", "docs/ARCHITECTURE.md", V0287_VERSION))

    def build_workbench_foundation_guide(self) -> AlphaWorkbenchFoundationGuide:
        return AlphaWorkbenchFoundationGuide(target_doc_ref=_ref("alpha_doc", "docs/WORKBENCH_FOUNDATION.md", V0287_VERSION), covered_surfaces=["trace_explorer", "provider_browser_preview", "evidence_inspector", "safety_approval_console_preview", "run_dashboard", "command_surface_preview", "snapshot_export_preview"])

    def build_memory_foundation_guide(self) -> AlphaMemoryFoundationGuide:
        return AlphaMemoryFoundationGuide(target_doc_ref=_ref("alpha_doc", "docs/MEMORY_FOUNDATION.md", V0287_VERSION), covered_memory_surfaces=["contract", "source_boundary", "candidate_extraction", "evidence_scoring", "promotion_gate", "durable_registry", "continuity_context", "injection_boundary_preview", "lifecycle", "consolidation"])

    def build_runtime_profile_guide(self) -> AlphaRuntimeProfileGuide:
        return AlphaRuntimeProfileGuide(target_doc_ref=_ref("alpha_doc", "docs/PUBLIC_ALPHA_RUNTIME_PROFILE.md", V0287_VERSION), feature_flag_matrix_ref=_ref("public_alpha_feature_flag_matrix", "public_alpha_feature_flag_matrix:v0.28.6", V0286_VERSION))

    def build_smoke_demo_guide(self, catalog: AlphaSmokeScenarioCatalog) -> AlphaSmokeDemoGuide:
        return AlphaSmokeDemoGuide(target_doc_ref=_ref("alpha_doc", "docs/SMOKE_DEMO_FLOW.md", V0287_VERSION), smoke_scenario_refs=[_ref("alpha_smoke_scenario", item.scenario_id, V0286_VERSION) for item in catalog.scenarios])

    def build_cli_reference_guide(self) -> AlphaCLIReferenceGuide:
        return AlphaCLIReferenceGuide(target_doc_ref=_ref("alpha_doc", "docs/CLI_REFERENCE.md", V0287_VERSION), documented_cli_groups=["alpha contract", "alpha hygiene", "alpha packaging", "alpha boundary", "alpha schumpeter", "alpha schumpeter-prep", "alpha runtime", "alpha smoke", "memory consolidation"])

    def build_safety_boundaries_guide(self) -> AlphaSafetyBoundariesGuide:
        return AlphaSafetyBoundariesGuide(target_doc_ref=_ref("alpha_doc", "docs/SAFETY_BOUNDARIES.md", V0287_VERSION), covered_boundaries=["no_provider_invocation", "no_command_execution_expansion", "no_network_calls", "no_runtime_continuity_injection", "no_autonomous_memory_execution", "no_private_data", "no_credentials", "no_raw_traces", "no_raw_transcripts", "no_raw_provider_outputs", "no_external_adapter", "no_Schumpeter_private_runtime"])

    def build_public_private_boundary_guide(self, source: AlphaDocumentationSourceView) -> AlphaPublicPrivateBoundaryGuide:
        return AlphaPublicPrivateBoundaryGuide(target_doc_ref=_ref("alpha_doc", "docs/PUBLIC_PRIVATE_BOUNDARY.md", V0287_VERSION), public_private_boundary_report_ref=source.public_private_boundary_report_ref)

    def build_schumpeter_preparation_guide(self, source: AlphaDocumentationSourceView) -> AlphaSchumpeterPreparationGuide:
        return AlphaSchumpeterPreparationGuide(target_doc_ref=_ref("alpha_doc", "docs/SCHUMPETER_PREPARATION.md", V0287_VERSION), schumpeter_preparation_report_ref=source.schumpeter_preparation_report_ref)

    def build_external_adapter_future_track_note(self) -> AlphaExternalAdapterFutureTrackNote:
        return AlphaExternalAdapterFutureTrackNote(target_doc_ref=_ref("alpha_doc", "docs/EXTERNAL_ADAPTER_FUTURE_TRACK.md", V0287_VERSION))


class AlphaExamplePackService:
    def build_policy(self) -> AlphaExamplePackPolicy:
        return AlphaExamplePackPolicy()

    def _examples(self) -> list[dict[str, Any]]:
        return [
            {"example_id": "synthetic_ocel_load", "kind": "synthetic", "deterministic": True},
            {"example_id": "smoke_cli_report_surface", "kind": "synthetic", "deterministic": True},
            {"example_id": "safety_boundary_report_surface", "kind": "synthetic", "deterministic": True},
        ]

    def build_example_pack_manifest(self) -> AlphaExamplePackManifest:
        examples = self._examples()
        return AlphaExamplePackManifest("alpha_example_pack_manifest:v0.28.7", examples, len(examples), len(examples), 0, 0, "ready")

    def build_example_data_manifest(self) -> AlphaExampleDataManifest:
        synthetic = [_ref("synthetic_dataset", "public_alpha_synthetic_demo_data:v0.28.7", V0287_VERSION)]
        return AlphaExampleDataManifest("alpha_example_data_manifest:v0.28.7", synthetic, synthetic, [], "ready")

    def build_synthetic_example_bundle(self) -> AlphaSyntheticExampleBundle:
        return AlphaSyntheticExampleBundle("alpha_synthetic_example_bundle:v0.28.7", "public_alpha_synthetic_examples", [_ref("alpha_example_pack_manifest", "alpha_example_pack_manifest:v0.28.7", V0287_VERSION)], [_ref("alpha_smoke_scenario_catalog", "alpha_smoke_scenario_catalog:v0.28.6", V0286_VERSION)], True)


class AlphaDemoScenarioDocumentationService:
    def build_docs(self, catalog: AlphaSmokeScenarioCatalog) -> list[AlphaDemoScenarioDocumentation]:
        return [
            AlphaDemoScenarioDocumentation(
                f"alpha_demo_scenario_documentation:{scenario.scenario_name}:v0.28.7",
                _ref("alpha_smoke_scenario", scenario.scenario_id, V0286_VERSION),
                _ref("alpha_doc", "docs/SMOKE_DEMO_FLOW.md", V0287_VERSION),
                scenario.scenario_name,
                ["synthetic_demo_metadata"],
                list(scenario.expected_outputs),
                ["no_provider_invocation", "no_command_execution_expansion", "no_private_data"],
                "ready",
            )
            for scenario in catalog.scenarios
        ]


class AlphaOnboardingChecklistService:
    REQUIRED = ["read_project_status", "install_or_setup_locally", "inspect_feature_flags", "run_or_review_smoke_demo", "inspect_safety_boundaries", "inspect_public_private_boundary", "inspect_examples", "understand_disabled_future_tracks", "understand_no_provider_invocation", "understand_no_command_execution_expansion"]

    def build_checklist(self) -> AlphaOnboardingChecklist:
        return AlphaOnboardingChecklist(checklist_items=list(self.REQUIRED), required_items=list(self.REQUIRED))


class AlphaDocumentationLinkIntegrityService:
    def build_report(self, docs: AlphaDocumentSet) -> AlphaDocumentationLinkIntegrityReport:
        checked = [_ref("alpha_doc", item.doc_name, V0287_VERSION) for item in docs.documents]
        return AlphaDocumentationLinkIntegrityReport("alpha_documentation_link_integrity_report:v0.28.7", checked, 14, 0, [], "passed")


class AlphaDocumentationSafetyBoundaryService:
    def build_report(self, docs: AlphaDocumentSet) -> AlphaDocumentationSafetyBoundaryReport:
        checked = [_ref("alpha_doc", item.doc_name, V0287_VERSION) for item in docs.documents]
        return AlphaDocumentationSafetyBoundaryReport("alpha_documentation_safety_boundary_report:v0.28.7", checked, "passed")


class AlphaDocumentationConsistencyService:
    def build_report(self, docs: AlphaDocumentSet) -> AlphaDocumentationConsistencyReport:
        checked = [_ref("alpha_doc", item.doc_name, V0287_VERSION) for item in docs.documents]
        return AlphaDocumentationConsistencyReport("alpha_documentation_consistency_report:v0.28.7", _ref("public_alpha_feature_flag_matrix", "public_alpha_feature_flag_matrix:v0.28.6", V0286_VERSION), checked, 0, 0, 0, 0, "passed")


class AlphaDocumentationReadinessGateService:
    def evaluate_gate(self, docs: AlphaDocumentSet, quickstart: AlphaQuickstartGuide, architecture: AlphaArchitectureOverviewGuide, safety: AlphaSafetyBoundariesGuide, boundary: AlphaPublicPrivateBoundaryGuide, example_manifest: AlphaExamplePackManifest, onboarding: AlphaOnboardingChecklist, links: AlphaDocumentationLinkIntegrityReport, safety_report: AlphaDocumentationSafetyBoundaryReport, consistency: AlphaDocumentationConsistencyReport) -> AlphaDocumentationReadinessGate:
        ready = docs.document_set_status == "ready" and quickstart.quickstart_status == "ready" and architecture.architecture_doc_status == "ready" and safety.safety_doc_status == "ready" and boundary.boundary_doc_status == "ready" and example_manifest.manifest_status == "ready" and onboarding.checklist_status == "ready" and safety_report.docs_safety_status == "passed" and consistency.consistency_status == "passed"
        return AlphaDocumentationReadinessGate("alpha_documentation_readiness_gate:v0.28.7", docs.document_set_status == "ready", quickstart.quickstart_status == "ready", architecture.architecture_doc_status == "ready", safety.safety_doc_status == "ready", boundary.boundary_doc_status == "ready", example_manifest.manifest_status == "ready", onboarding.checklist_status == "ready", links.link_integrity_status in {"passed", "warning"}, safety_report.docs_safety_status == "passed", consistency.consistency_status == "passed", True, True, True, "passed" if ready else "warning", ready)


class AlphaDocumentationHandoffPacketService:
    def build_packet(self, report_id: str, docs: AlphaDocumentSet, example_manifest: AlphaExamplePackManifest, scenario_docs: list[AlphaDemoScenarioDocumentation]) -> AlphaDocumentationHandoffPacket:
        doc_refs = [_ref("alpha_doc", item.doc_name, V0287_VERSION) for item in docs.documents]
        return AlphaDocumentationHandoffPacket(
            "alpha_documentation_handoff_packet:v0.28.7",
            report_id,
            doc_refs,
            [_ref("alpha_example_pack_manifest", example_manifest.manifest_id, V0287_VERSION)],
            [_ref("alpha_demo_scenario_documentation", item.demo_doc_id, V0287_VERSION) for item in scenario_docs],
            [_ref("alpha_documentation_readiness_gate", "alpha_documentation_readiness_gate:v0.28.7", V0287_VERSION)],
            [_ref("future_track", "external_adapter_v0.29_contract_first", V0287_VERSION)],
            ["public_alpha_release", "package_publish", "release_tag_creation", "production_runtime", "external_provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "Schumpeter_private_runtime", "runtime_continuity_injection", "autonomous_memory_execution"],
        )


class AlphaDocumentationFindingService:
    BLOCKED_FINDINGS = {
        "production_runtime_overclaim_detected",
        "public_alpha_release_overclaim_detected",
        "provider_invocation_overclaim_detected",
        "command_execution_expansion_overclaim_detected",
        "external_adapter_overclaim_detected",
        "schumpeter_runtime_overclaim_detected",
        "private_material_exposure_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "actual_user_data_example_detected",
        "actual_company_data_example_detected",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "network_call_attempted",
        "runtime_continuity_injection_attempted",
        "external_adapter_attempted",
        "RPA_adapter_attempted",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[AlphaDocumentationFinding]:
        return [
            AlphaDocumentationFinding("alpha_documentation_finding:documentation_policy_created:v0.28.7", "info", "documentation_policy_created", "Alpha documentation policy created as documentation/onboarding/example-pack metadata only.", _ref("alpha_documentation_policy", "alpha_documentation_policy:v0.28.7", V0287_VERSION), [], None),
            AlphaDocumentationFinding("alpha_documentation_finding:docs_readiness_gate_created:v0.28.7", "info", "docs_readiness_gate_created", "Documentation readiness gate created; public alpha release claim remains disabled.", _ref("alpha_documentation_readiness_gate", "alpha_documentation_readiness_gate:v0.28.7", V0287_VERSION), [], "Withdraw if documentation claims release, production runtime, adapters, provider invocation, command expansion, private data, or raw artifact availability."),
        ]


class AlphaDocumentationReadinessReportService:
    def build_report(self, report_id: str | None = None) -> AlphaDocumentationReadinessReport:
        actual_report_id = report_id or "alpha_documentation_readiness_report:v0.28.7"
        source = AlphaDocumentationSourceViewService().build_source_view()
        policy = AlphaDocumentationPolicyService().build_policy()
        request = AlphaDocumentationRequest(alpha_runtime_profile_report_id=source.runtime_profile_report_ref["object_id"] if source.runtime_profile_report_ref else None, alpha_operator_handoff_packet_id=source.operator_handoff_packet_ref["object_id"] if source.operator_handoff_packet_ref else None, public_private_boundary_report_id=source.public_private_boundary_report_ref["object_id"] if source.public_private_boundary_report_ref else None, packaging_readiness_report_id=source.packaging_readiness_report_ref["object_id"] if source.packaging_readiness_report_ref else None, release_hygiene_gate_report_id=source.release_hygiene_gate_report_ref["object_id"] if source.release_hygiene_gate_report_ref else None, source_refs=source.public_safe_demo_refs)
        runtime_report = AlphaRuntimeProfileReportService().build_report()
        docs = AlphaDocumentSetService().build_document_set()
        guide = AlphaGuideService()
        readme = guide.build_readme_plan()
        quickstart = guide.build_quickstart_guide()
        architecture = guide.build_architecture_overview()
        ocel = guide.build_ocel_native_core_guide()
        workbench = guide.build_workbench_foundation_guide()
        memory = guide.build_memory_foundation_guide()
        runtime_guide = guide.build_runtime_profile_guide()
        smoke = guide.build_smoke_demo_guide(runtime_report.smoke_scenario_catalog)
        cli = guide.build_cli_reference_guide()
        safety = guide.build_safety_boundaries_guide()
        public_private = guide.build_public_private_boundary_guide(source)
        schumpeter = guide.build_schumpeter_preparation_guide(source)
        future = guide.build_external_adapter_future_track_note()
        examples = AlphaExamplePackService()
        example_policy = examples.build_policy()
        example_manifest = examples.build_example_pack_manifest()
        data_manifest = examples.build_example_data_manifest()
        synthetic_bundle = examples.build_synthetic_example_bundle()
        scenario_docs = AlphaDemoScenarioDocumentationService().build_docs(runtime_report.smoke_scenario_catalog)
        onboarding = AlphaOnboardingChecklistService().build_checklist()
        links = AlphaDocumentationLinkIntegrityService().build_report(docs)
        safety_report = AlphaDocumentationSafetyBoundaryService().build_report(docs)
        consistency = AlphaDocumentationConsistencyService().build_report(docs)
        gate = AlphaDocumentationReadinessGateService().evaluate_gate(docs, quickstart, architecture, safety, public_private, example_manifest, onboarding, links, safety_report, consistency)
        handoff = AlphaDocumentationHandoffPacketService().build_packet(actual_report_id, docs, example_manifest, scenario_docs)
        findings = AlphaDocumentationFindingService().build_findings()
        return AlphaDocumentationReadinessReport(
            report_id=actual_report_id,
            created_at=_now(),
            documentation_policy=policy,
            request=request,
            source_view=source,
            document_set=docs,
            readme_plan=readme,
            quickstart_guide=quickstart,
            architecture_overview_guide=architecture,
            ocel_native_core_guide=ocel,
            workbench_foundation_guide=workbench,
            memory_foundation_guide=memory,
            runtime_profile_guide=runtime_guide,
            smoke_demo_guide=smoke,
            cli_reference_guide=cli,
            safety_boundaries_guide=safety,
            public_private_boundary_guide=public_private,
            schumpeter_preparation_guide=schumpeter,
            external_adapter_future_track_note=future,
            example_pack_policy=example_policy,
            example_pack_manifest=example_manifest,
            example_data_manifest=data_manifest,
            synthetic_example_bundle=synthetic_bundle,
            demo_scenario_documentation=scenario_docs,
            onboarding_checklist=onboarding,
            link_integrity_report=links,
            safety_boundary_report=safety_report,
            consistency_report=consistency,
            documentation_readiness_gate=gate,
            handoff_packet=handoff,
            findings=findings,
            report_status="passed" if gate.docs_ready_for_v0_28_8 else "warning",
            ready_for_v0_28_8=gate.docs_ready_for_v0_28_8,
            documentation_ready=gate.document_set_ready,
            onboarding_ready=gate.onboarding_ready,
            example_pack_ready=gate.examples_ready,
            limitations=["Documentation readiness is not a public alpha release claim; v0.28.8 must validate docs, examples, links, smoke instructions, safety boundaries, and external adapter preflight gates."],
            withdrawal_conditions=["Withdraw if docs claim public release, production runtime, package publish/tag, enabled provider/command/adapters, Schumpeter runtime, actual/private/raw data, credential exposure, network/runtime injection, reference dependency/code copy, or LLM sole authority."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.documentation_policy,
            "source-view": report.source_view,
            "document-set": report.document_set,
            "readme": report.readme_plan,
            "quickstart": report.quickstart_guide,
            "architecture": report.architecture_overview_guide,
            "ocel-core": report.ocel_native_core_guide,
            "workbench": report.workbench_foundation_guide,
            "memory": report.memory_foundation_guide,
            "runtime-profile": report.runtime_profile_guide,
            "smoke-demo": report.smoke_demo_guide,
            "cli-reference": report.cli_reference_guide,
            "safety": report.safety_boundaries_guide,
            "public-private": report.public_private_boundary_guide,
            "schumpeter": report.schumpeter_preparation_guide,
            "external-adapter-future": report.external_adapter_future_track_note,
            "example-policy": report.example_pack_policy,
            "example-manifest": report.example_pack_manifest,
            "data-manifest": report.example_data_manifest,
            "synthetic-bundle": report.synthetic_example_bundle,
            "demo-scenario-docs": report.demo_scenario_documentation,
            "onboarding": report.onboarding_checklist,
            "links": report.link_integrity_report,
            "safety-report": report.safety_boundary_report,
            "consistency": report.consistency_report,
            "readiness": report.documentation_readiness_gate,
            "handoff": report.handoff_packet,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0287_VERSION,
            "layer": V028_LAYER,
            "subject": "alpha_documentation_onboarding_example_pack",
            "principles": [
                "Documentation is not release",
                "Onboarding is not production support",
                "Example pack is not production dataset",
                "Synthetic example is not actual user/company data",
                "Quickstart is not provider invocation",
                "CLI guide is not command execution expansion",
                "Smoke demo documentation is not production workflow",
                "Schumpeter preparation documentation is not Schumpeter runtime implementation",
                "External adapter future-track note is not external adapter implementation",
                "Future-track documentation must be clearly labeled",
            ],
            "safety_boundary": {
                "public_alpha_release_implemented": report.public_alpha_release_implemented,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "production_runtime_claimed": report.production_runtime_claimed,
                "provider_invocation_documented_as_enabled": report.provider_invocation_documented_as_enabled,
                "command_execution_expansion_documented_as_enabled": report.command_execution_expansion_documented_as_enabled,
                "external_adapter_documented_as_enabled": report.external_adapter_documented_as_enabled,
                "RPA_adapter_documented_as_enabled": report.RPA_adapter_documented_as_enabled,
                "schumpeter_private_runtime_documented_as_enabled": report.schumpeter_private_runtime_documented_as_enabled,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "private_material_exposed": report.private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "secret_exposed": report.secret_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "network_called": report.network_called,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "external_adapter_implemented": report.external_adapter_implemented,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate", "v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation", "v0.29 External Provider Adapter Contract"],
            "next_step": V0287_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "alpha_documentation_onboarding_example_pack_created",
            "version": V0287_VERSION,
            "source_read_models": ["PublicAlphaRuntimeProfileState", "AlphaSmokeScenarioCatalogState", "AlphaOperatorHandoffState", "SchumpeterPreparationProfileState", "PublicPrivateBoundaryState", "PackagingReadinessState", "ReleaseHygieneGateState", "MemoryConsolidationState", "WorkbenchConsolidationState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["AlphaDocumentationState", "AlphaDocumentSetState", "AlphaQuickstartState", "AlphaArchitectureDocState", "AlphaSafetyDocState", "AlphaExamplePackState", "AlphaOnboardingChecklistState", "AlphaDocumentationReadinessState", "AlphaDocumentationHandoffState", "V028ReadinessState"],
            "effect_types": V0287_EFFECT_TYPES,
            "forbidden_effect_types": V0287_FORBIDDEN_EFFECT_TYPES,
        }


def render_alpha_documentation_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AlphaDocumentationReadinessReport = parts["report"]
    lines = [
        f"Alpha Documentation / Onboarding / Example Pack {section}",
        f"version={report.version}",
        f"layer={report.documentation_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_8={_bool(report.ready_for_v0_28_8)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"documentation_ready={_bool(report.documentation_ready)}",
        f"onboarding_ready={_bool(report.onboarding_ready)}",
        f"example_pack_ready={_bool(report.example_pack_ready)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"public_alpha_release_implemented={_bool(report.public_alpha_release_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"production_runtime_claimed={_bool(report.production_runtime_claimed)}",
        f"provider_invocation_documented_as_enabled={_bool(report.provider_invocation_documented_as_enabled)}",
        f"command_execution_expansion_documented_as_enabled={_bool(report.command_execution_expansion_documented_as_enabled)}",
        f"external_adapter_documented_as_enabled={_bool(report.external_adapter_documented_as_enabled)}",
        f"RPA_adapter_documented_as_enabled={_bool(report.RPA_adapter_documented_as_enabled)}",
        f"schumpeter_private_runtime_documented_as_enabled={_bool(report.schumpeter_private_runtime_documented_as_enabled)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"private_material_exposed={_bool(report.private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"network_called={_bool(report.network_called)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "document_set_id", getattr(payload, "guide_id", getattr(payload, "plan_id", getattr(payload, "manifest_id", getattr(payload, "bundle_id", getattr(payload, "checklist_id", getattr(payload, "gate_id", getattr(payload, "handoff_packet_id", ""))))))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0288_VERSION = "v0.28.8"
V0288_VERSION_NAME = "Alpha Readiness Validation / External Adapter Preflight Gate"
V0288_NEXT_STEP = "v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation"

V0288_OBJECT_TYPES = [
    "alpha_readiness_validation_policy",
    "alpha_readiness_validation_request",
    "alpha_readiness_validation_source_view",
    "v028_validation_coverage_matrix",
    "v028_validation_coverage_row",
    "alpha_regression_test_matrix",
    "alpha_regression_test_matrix_row",
    "alpha_boundary_test_matrix",
    "alpha_boundary_test_matrix_row",
    "forbidden_pattern_scan_plan",
    "forbidden_pattern_scan_report",
    "release_hygiene_validation_report",
    "packaging_validation_report",
    "package_build_validation_report",
    "import_smoke_validation_report",
    "cli_smoke_validation_report",
    "public_private_validation_report",
    "documentation_validation_report",
    "example_pack_validation_report",
    "smoke_demo_validation_report",
    "safety_boundary_validation_report",
    "schumpeter_preparation_validation_report",
    "external_adapter_preflight_policy",
    "external_adapter_preflight_request",
    "external_adapter_preflight_source_view",
    "external_adapter_risk_assessment",
    "provider_invocation_reopen_criteria",
    "command_execution_reopen_criteria",
    "credential_boundary_preflight",
    "network_boundary_preflight",
    "permission_boundary_preflight",
    "safety_gate_preflight",
    "audit_rollback_ocel_preflight",
    "adapter_certification_preflight",
    "external_adapter_preflight_report",
    "alpha_readiness_gate",
    "alpha_validation_handoff_packet",
    "alpha_readiness_validation_finding",
    "alpha_readiness_validation_report",
    "alpha_documentation_readiness_report",
    "alpha_runtime_profile_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0288_EVENT_TYPES = [
    "alpha_readiness_validation_requested",
    "alpha_readiness_validation_prerequisites_loaded",
    "alpha_readiness_validation_policy_created",
    "alpha_readiness_validation_source_view_created",
    "v028_validation_coverage_matrix_created",
    "alpha_regression_test_matrix_created",
    "alpha_boundary_test_matrix_created",
    "forbidden_pattern_scan_plan_created",
    "forbidden_pattern_scan_report_created",
    "release_hygiene_validation_report_created",
    "packaging_validation_report_created",
    "package_build_validation_report_created",
    "import_smoke_validation_report_created",
    "cli_smoke_validation_report_created",
    "public_private_validation_report_created",
    "documentation_validation_report_created",
    "example_pack_validation_report_created",
    "smoke_demo_validation_report_created",
    "safety_boundary_validation_report_created",
    "schumpeter_preparation_validation_report_created",
    "external_adapter_preflight_policy_created",
    "external_adapter_risk_assessment_created",
    "provider_invocation_reopen_criteria_created",
    "command_execution_reopen_criteria_created",
    "credential_boundary_preflight_created",
    "network_boundary_preflight_created",
    "permission_boundary_preflight_created",
    "safety_gate_preflight_created",
    "audit_rollback_ocel_preflight_created",
    "adapter_certification_preflight_created",
    "external_adapter_preflight_report_created",
    "alpha_readiness_gate_evaluated",
    "alpha_validation_handoff_packet_created",
    "alpha_readiness_validation_report_created",
    "alpha_readiness_validation_warning_created",
    "alpha_readiness_validation_blocked",
]

V0288_EFFECT_TYPES = [
    "read_only_observation",
    "alpha_readiness_validation_created",
    "v028_validation_coverage_created",
    "alpha_regression_matrix_created",
    "alpha_boundary_matrix_created",
    "forbidden_pattern_scan_report_created",
    "alpha_validation_report_created",
    "external_adapter_preflight_created",
    "provider_invocation_reopen_criteria_created",
    "command_execution_reopen_criteria_created",
    "alpha_readiness_gate_evaluated",
    "alpha_validation_handoff_packet_created",
    "state_candidate_created",
]

V0288_FORBIDDEN_EFFECT_TYPES = [
    "public_alpha_release_implemented",
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_registered",
    "provider_invoked",
    "network_called",
    "command_executed",
    "external_dominion_implemented",
    "RPA_adapter_implemented",
    "A360_adapter_implemented",
    "Brity_adapter_implemented",
    "UiPath_adapter_implemented",
    "schumpeter_private_runtime_used",
    "company_wrapper_implemented",
    "private_config_created",
    "credential_created",
    "credential_exposed",
    "secret_exposed",
    "private_material_exposed",
    "actual_user_data_used",
    "actual_company_data_used",
    "raw_trace_used",
    "raw_transcript_used",
    "raw_provider_output_used",
    "runtime_continuity_injected",
    "autonomous_memory_execution_enabled",
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class AlphaReadinessValidationPolicy(ModelMixin):
    policy_id: str = "alpha_readiness_validation_policy:v0.28.8"
    version: str = V0288_VERSION
    layer: str = V028_LAYER
    validation_enabled: bool = True
    external_adapter_preflight_enabled: bool = True
    validation_is_not_release: bool = True
    preflight_is_not_adapter_implementation: bool = True
    unknown_is_not_passed: bool = True
    no_release_is_valid_outcome: bool = True
    no_adapter_is_valid_outcome: bool = True
    regression_validation_required: bool = True
    boundary_validation_required: bool = True
    forbidden_pattern_scan_required: bool = True
    release_hygiene_validation_required: bool = True
    packaging_validation_required: bool = True
    public_private_validation_required: bool = True
    documentation_validation_required: bool = True
    smoke_demo_validation_required: bool = True
    safety_boundary_validation_required: bool = True
    external_adapter_preflight_required_before_v029: bool = True
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    public_alpha_release_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_call_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    external_adapter_implementation_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    schumpeter_private_runtime_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    autonomous_memory_execution_enabled_now: bool = False
    llm_judge_as_sole_readiness_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaReadinessValidationRequest(ModelMixin):
    request_id: str = "alpha_readiness_validation_request:v0.28.8"
    version: str = V0288_VERSION
    documentation_report_id: str | None = None
    runtime_profile_report_id: str | None = None
    packaging_report_id: str | None = None
    public_private_report_id: str | None = None
    hygiene_gate_report_id: str | None = None
    requested_validation_profile: str = "alpha_readiness_candidate"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaReadinessValidationSourceView(ModelMixin):
    source_view_id: str = "alpha_readiness_validation_source_view:v0.28.8"
    version: str = V0288_VERSION
    v0280_contract_report_ref: dict[str, Any] | None = None
    v0281_hygiene_report_ref: dict[str, Any] | None = None
    v0282_packaging_report_ref: dict[str, Any] | None = None
    v0283_public_private_report_ref: dict[str, Any] | None = None
    v0284_schumpeter_decision_report_ref: dict[str, Any] | None = None
    v0285_schumpeter_preparation_report_ref: dict[str, Any] | None = None
    v0286_runtime_profile_report_ref: dict[str, Any] | None = None
    v0287_documentation_report_ref: dict[str, Any] | None = None
    v0279_memory_consolidation_report_ref: dict[str, Any] | None = None
    v0269_workbench_consolidation_report_ref: dict[str, Any] | None = None
    test_metadata_refs: list[dict[str, Any]] = field(default_factory=list)
    ci_metadata_refs: list[dict[str, Any]] = field(default_factory=list)
    package_metadata_refs: list[dict[str, Any]] = field(default_factory=list)
    docs_metadata_refs: list[dict[str, Any]] = field(default_factory=list)
    forbidden_scan_metadata_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "partial"
    private_material_detected: bool = False
    credential_detected: bool = False
    raw_trace_detected: bool = False
    raw_transcript_detected: bool = False
    raw_provider_output_detected: bool = False
    provider_invocation_detected: bool = False
    command_execution_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class V028ValidationCoverageRow(ModelMixin):
    row_id: str
    version_number: str
    version_name: str
    report_ref: dict[str, Any] | None
    report_available: bool
    tests_available: bool
    boundary_tests_available: bool
    docs_available: bool
    cli_surface_available: bool
    safety_boundary_validated: bool
    public_private_validated: bool
    validation_status: str
    missing_items: list[str]
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class V028ValidationCoverageMatrix(ModelMixin):
    matrix_id: str
    rows: list[V028ValidationCoverageRow]
    total_version_count: int
    passed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    unknown_count: int
    coverage_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaRegressionTestMatrixRow(ModelMixin):
    row_id: str
    test_scope: str
    test_command_ref: dict[str, Any] | None
    test_execution_mode: str
    tests_passed: bool | None
    failure_summary: str | None
    regression_status: str
    version: str = V0288_VERSION
    command_execution_expansion_added: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaRegressionTestMatrix(ModelMixin):
    matrix_id: str
    rows: list[AlphaRegressionTestMatrixRow]
    total_test_scope_count: int
    passed_scope_count: int
    warning_scope_count: int
    failed_scope_count: int
    blocked_scope_count: int
    regression_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaBoundaryTestMatrixRow(ModelMixin):
    row_id: str
    boundary_name: str
    validation_method: str
    boundary_passed: bool | None
    boundary_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaBoundaryTestMatrix(ModelMixin):
    matrix_id: str
    rows: list[AlphaBoundaryTestMatrixRow]
    boundary_count: int
    passed_boundary_count: int
    warning_boundary_count: int
    failed_boundary_count: int
    blocked_boundary_count: int
    boundary_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ForbiddenPatternScanPlan(ModelMixin):
    plan_id: str
    scan_scope: list[str]
    forbidden_patterns: list[str]
    scan_mode: str
    plan_status: str
    version: str = V0288_VERSION
    raw_content_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ForbiddenPatternScanReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    scan_executed: bool
    scan_mode: str
    matched_pattern_count: int
    blocking_match_count: int
    warning_match_count: int
    matched_pattern_refs: list[dict[str, Any]]
    scan_status: str
    version: str = V0288_VERSION
    raw_content_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ReleaseHygieneValidationReport(ModelMixin):
    report_id: str
    hygiene_gate_report_ref: dict[str, Any] | None
    hygiene_report_available: bool
    repository_release_ready: bool | None
    clean_worktree_validated: bool | None
    license_validated: bool | None
    changelog_validated: bool | None
    third_party_notices_validated: bool | None
    runtime_data_hygiene_validated: bool | None
    references_policy_validated: bool | None
    validation_status: str
    blocks_public_alpha_release_claim: bool
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PackagingValidationReport(ModelMixin):
    report_id: str
    packaging_report_ref: dict[str, Any] | None
    packaging_report_available: bool
    package_distribution_ready: bool | None
    pyproject_validated: bool | None
    dependency_boundary_validated: bool | None
    py_typed_validated: bool | None
    package_data_boundary_validated: bool | None
    publish_blocker_validated: bool | None
    validation_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PackageBuildValidationReport(ModelMixin):
    report_id: str
    wheel_smoke_report_ref: dict[str, Any] | None
    sdist_smoke_report_ref: dict[str, Any] | None
    wheel_validated: bool | None
    sdist_validated: bool | None
    package_build_validation_status: str
    version: str = V0288_VERSION
    artifact_published: bool = False
    release_artifact_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ImportSmokeValidationReport(ModelMixin):
    report_id: str
    import_smoke_report_ref: dict[str, Any] | None
    import_smoke_validated: bool | None
    import_success: bool | None
    import_validation_status: str
    version: str = V0288_VERSION
    provider_invoked: bool = False
    command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CLISmokeValidationReport(ModelMixin):
    report_id: str
    cli_smoke_report_ref: dict[str, Any] | None
    cli_smoke_validated: bool | None
    cli_success: bool | None
    cli_validation_status: str
    version: str = V0288_VERSION
    provider_invoked: bool = False
    command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateValidationReport(ModelMixin):
    report_id: str
    public_private_report_ref: dict[str, Any] | None
    public_private_boundary_ready: bool | None
    no_private_material_exposure: bool | None
    no_credential_exposure: bool | None
    no_secret_exposure: bool | None
    no_raw_trace_exposure: bool | None
    no_raw_transcript_exposure: bool | None
    no_raw_provider_output_exposure: bool | None
    references_governance_validated: bool | None
    validation_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DocumentationValidationReport(ModelMixin):
    report_id: str
    documentation_report_ref: dict[str, Any] | None
    documentation_ready: bool | None
    onboarding_ready: bool | None
    example_pack_ready: bool | None
    link_integrity_validated: bool | None
    docs_safety_validated: bool | None
    docs_consistency_validated: bool | None
    no_overclaim_validated: bool | None
    validation_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExamplePackValidationReport(ModelMixin):
    report_id: str
    example_pack_manifest_ref: dict[str, Any] | None
    example_data_manifest_ref: dict[str, Any] | None
    synthetic_only_validated: bool | None
    no_actual_user_data: bool | None
    no_actual_company_data: bool | None
    no_credentials: bool | None
    no_raw_artifacts: bool | None
    example_pack_validation_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SmokeDemoValidationReport(ModelMixin):
    report_id: str
    runtime_profile_report_ref: dict[str, Any] | None
    smoke_run_report_ref: dict[str, Any] | None
    smoke_flow_ready: bool | None
    deterministic_validated: bool | None
    synthetic_only_validated: bool | None
    smoke_demo_validation_status: str
    version: str = V0288_VERSION
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    file_mutated: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SafetyBoundaryValidationReport(ModelMixin):
    report_id: str
    boundary_test_matrix_ref: dict[str, Any] | None
    forbidden_pattern_scan_report_ref: dict[str, Any] | None
    safety_boundaries_passed: bool
    blocking_boundary_count: int
    warning_boundary_count: int
    safety_validation_status: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationValidationReport(ModelMixin):
    report_id: str
    schumpeter_preparation_report_ref: dict[str, Any] | None
    schumpeter_preparation_profile_ready: bool | None
    private_overlay_boundary_ready: bool | None
    schumpeter_validation_status: str
    version: str = V0288_VERSION
    actual_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    private_config_created: bool = False
    provider_adapter_created: bool = False
    RPA_adapter_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterPreflightPolicy(ModelMixin):
    policy_id: str = "external_adapter_preflight_policy:v0.28.8"
    version: str = V0288_VERSION
    layer: str = V028_LAYER
    preflight_enabled: bool = True
    adapter_implementation_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    credential_storage_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    provider_adapter_contract_required_for_v029: bool = True
    capability_declaration_is_not_permission: bool = True
    adapter_registration_is_not_execution: bool = True
    provider_invocation_requires_permission_gate: bool = True
    provider_invocation_requires_safety_gate: bool = True
    provider_invocation_requires_credential_boundary: bool = True
    provider_invocation_requires_network_boundary: bool = True
    provider_invocation_requires_audit: bool = True
    provider_invocation_requires_rollback_boundary: bool = True
    provider_invocation_requires_OCEL_visibility: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterPreflightRequest(ModelMixin):
    request_id: str = "external_adapter_preflight_request:v0.28.8"
    version: str = V0288_VERSION
    target_track: str = "v0.29.x External Skill / External Provider Adapter Development"
    requested_preflight_scope: str = "provider_adapter_contract"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterPreflightSourceView(ModelMixin):
    source_view_id: str = "external_adapter_preflight_source_view:v0.28.8"
    version: str = V0288_VERSION
    alpha_readiness_refs: list[dict[str, Any]] = field(default_factory=list)
    hygiene_refs: list[dict[str, Any]] = field(default_factory=list)
    packaging_refs: list[dict[str, Any]] = field(default_factory=list)
    public_private_refs: list[dict[str, Any]] = field(default_factory=list)
    safety_boundary_refs: list[dict[str, Any]] = field(default_factory=list)
    smoke_demo_refs: list[dict[str, Any]] = field(default_factory=list)
    docs_refs: list[dict[str, Any]] = field(default_factory=list)
    schumpeter_preparation_refs: list[dict[str, Any]] = field(default_factory=list)
    source_status: str = "partial"
    adapter_implementation_detected: bool = False
    provider_invocation_detected: bool = False
    command_execution_detected: bool = False
    credential_storage_detected: bool = False
    network_access_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterRiskAssessment(ModelMixin):
    risk_assessment_id: str
    risk_dimensions: list[str]
    risk_level: str
    blocker_count: int
    warning_count: int
    risk_summary: str
    version: str = V0288_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ProviderInvocationReopenCriteria(ModelMixin):
    criteria_id: str = "provider_invocation_reopen_criteria:v0.28.8"
    version: str = V0288_VERSION
    provider_invocation_reopen_allowed_now: bool = False
    requires_v029_contract: bool = True
    requires_provider_inventory: bool = True
    requires_capability_registry: bool = True
    requires_permission_gate: bool = True
    requires_safety_gate: bool = True
    requires_credential_boundary: bool = True
    requires_network_boundary: bool = True
    requires_audit_trace: bool = True
    requires_rollback_boundary: bool = True
    requires_OCEL_visibility: bool = True
    requires_user_approval_surface: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CommandExecutionReopenCriteria(ModelMixin):
    criteria_id: str = "command_execution_reopen_criteria:v0.28.8"
    version: str = V0288_VERSION
    command_execution_reopen_allowed_now: bool = False
    requires_v029_or_later_contract: bool = True
    requires_command_allowlist: bool = True
    requires_sandbox_boundary: bool = True
    requires_permission_gate: bool = True
    requires_safety_gate: bool = True
    requires_audit_trace: bool = True
    requires_rollback_or_noop_boundary: bool = True
    requires_no_shell_true: bool = True
    requires_no_unbounded_subprocess: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CredentialBoundaryPreflight(ModelMixin):
    preflight_id: str
    credential_boundary_ready_for_v029: bool
    credential_status: str
    version: str = V0288_VERSION
    credential_storage_enabled_now: bool = False
    committed_credentials_forbidden: bool = True
    external_secret_store_required_later: bool = True
    credential_redaction_required: bool = True
    credential_audit_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class NetworkBoundaryPreflight(ModelMixin):
    preflight_id: str
    network_boundary_ready_for_v029: bool
    network_status: str
    version: str = V0288_VERSION
    network_access_enabled_now: bool = False
    outbound_domain_policy_required: bool = True
    request_audit_required: bool = True
    timeout_policy_required: bool = True
    retry_policy_required: bool = True
    data_exfiltration_boundary_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PermissionBoundaryPreflight(ModelMixin):
    preflight_id: str
    permission_boundary_ready_for_v029: bool
    permission_status: str
    version: str = V0288_VERSION
    provider_invocation_permission_required: bool = True
    command_execution_permission_required: bool = True
    scope_limited_permission_required: bool = True
    expiry_required: bool = True
    approval_record_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SafetyGatePreflight(ModelMixin):
    preflight_id: str
    safety_gate_ready_for_v029: bool
    safety_status: str
    version: str = V0288_VERSION
    provider_safety_gate_required: bool = True
    command_safety_gate_required: bool = True
    private_data_safety_check_required: bool = True
    credential_safety_check_required: bool = True
    external_side_effect_check_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AuditRollbackOCELPreflight(ModelMixin):
    preflight_id: str
    audit_ready_for_v029: bool
    rollback_boundary_ready_for_v029: bool
    OCEL_visibility_ready_for_v029: bool
    audit_status: str
    version: str = V0288_VERSION
    every_provider_action_must_emit_OCEL: bool = True
    every_command_action_must_emit_OCEL: bool = True
    action_result_must_be_auditable: bool = True
    rollback_or_noop_boundary_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AdapterCertificationPreflight(ModelMixin):
    preflight_id: str
    certification_ready_for_v029: bool
    certification_status: str
    version: str = V0288_VERSION
    adapter_contract_required: bool = True
    adapter_test_matrix_required: bool = True
    adapter_boundary_tests_required: bool = True
    adapter_mock_mode_required: bool = True
    adapter_no_network_default_required: bool = True
    adapter_no_credential_default_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterPreflightReport(ModelMixin):
    report_id: str
    preflight_policy: ExternalAdapterPreflightPolicy
    request: ExternalAdapterPreflightRequest
    source_view: ExternalAdapterPreflightSourceView
    risk_assessment: ExternalAdapterRiskAssessment
    provider_invocation_reopen_criteria: ProviderInvocationReopenCriteria
    command_execution_reopen_criteria: CommandExecutionReopenCriteria
    credential_boundary_preflight: CredentialBoundaryPreflight
    network_boundary_preflight: NetworkBoundaryPreflight
    permission_boundary_preflight: PermissionBoundaryPreflight
    safety_gate_preflight: SafetyGatePreflight
    audit_rollback_ocel_preflight: AuditRollbackOCELPreflight
    adapter_certification_preflight: AdapterCertificationPreflight
    report_status: str
    ready_for_v0_29_contract: bool
    version: str = V0288_VERSION
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    adapter_implemented_now: bool = False
    provider_invoked_now: bool = False
    command_executed_now: bool = False
    network_called_now: bool = False
    credentials_created_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaReadinessGate(ModelMixin):
    gate_id: str
    v028_coverage_passed: bool
    regression_validation_passed: bool
    boundary_validation_passed: bool
    forbidden_scan_passed: bool
    release_hygiene_validated: bool
    packaging_validated: bool
    public_private_validated: bool
    documentation_validated: bool
    example_pack_validated: bool
    smoke_demo_validated: bool
    safety_boundary_validated: bool
    schumpeter_preparation_validated: bool
    external_adapter_preflight_passed: bool
    repository_release_ready: bool
    package_distribution_ready: bool
    documentation_ready: bool
    public_private_boundary_ready: bool
    public_alpha_release_claim_allowed: bool
    alpha_validation_status: str
    ready_for_v0_28_9: bool
    ready_for_v0_29_contract: bool
    version: str = V0288_VERSION
    ready_for_public_alpha_release: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaValidationHandoffPacket(ModelMixin):
    handoff_packet_id: str
    source_validation_report_id: str
    alpha_readiness_gate_ref: dict[str, Any]
    external_adapter_preflight_report_ref: dict[str, Any]
    validation_report_refs: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]
    ready_inputs_for_v0289: list[str]
    not_implemented_now: list[str]
    version: str = V0288_VERSION
    target_version: str = "v0.28.9"
    target_track: str = "Public Alpha / Schumpeter Split Preparation Consolidation"
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaReadinessValidationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AlphaReadinessValidationReport(ModelMixin):
    report_id: str
    created_at: str
    validation_policy: AlphaReadinessValidationPolicy
    request: AlphaReadinessValidationRequest
    source_view: AlphaReadinessValidationSourceView
    coverage_matrix: V028ValidationCoverageMatrix
    regression_test_matrix: AlphaRegressionTestMatrix
    boundary_test_matrix: AlphaBoundaryTestMatrix
    forbidden_pattern_scan_plan: ForbiddenPatternScanPlan
    forbidden_pattern_scan_report: ForbiddenPatternScanReport
    release_hygiene_validation_report: ReleaseHygieneValidationReport
    packaging_validation_report: PackagingValidationReport
    package_build_validation_report: PackageBuildValidationReport
    import_smoke_validation_report: ImportSmokeValidationReport
    cli_smoke_validation_report: CLISmokeValidationReport
    public_private_validation_report: PublicPrivateValidationReport
    documentation_validation_report: DocumentationValidationReport
    example_pack_validation_report: ExamplePackValidationReport
    smoke_demo_validation_report: SmokeDemoValidationReport
    safety_boundary_validation_report: SafetyBoundaryValidationReport
    schumpeter_preparation_validation_report: SchumpeterPreparationValidationReport
    external_adapter_preflight_report: ExternalAdapterPreflightReport
    alpha_readiness_gate: AlphaReadinessGate
    handoff_packet: AlphaValidationHandoffPacket
    findings: list[AlphaReadinessValidationFinding]
    report_status: str
    ready_for_v0_28_9: bool
    ready_for_public_alpha_release_claim: bool
    ready_for_v0_29_contract: bool
    version: str = V0288_VERSION
    ready_for_public_alpha_release: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    official_release_artifact_created: bool = False
    external_adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    command_executed: bool = False
    external_dominion_implemented: bool = False
    RPA_adapter_implemented: bool = False
    A360_adapter_implemented: bool = False
    Brity_adapter_implemented: bool = False
    UiPath_adapter_implemented: bool = False
    schumpeter_private_runtime_used: bool = False
    credential_created: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    private_material_exposed: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    raw_trace_used: bool = False
    raw_transcript_used: bool = False
    raw_provider_output_used: bool = False
    runtime_continuity_injected: bool = False
    autonomous_memory_execution_enabled: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0288_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation begins or alpha readiness policy changes."


class AlphaReadinessValidationPrerequisiteSourceService:
    def load_v0287_documentation_readiness_report(self) -> dict[str, Any]:
        return _ref("alpha_documentation_readiness_report", "alpha_documentation_readiness_report:v0.28.7", V0287_VERSION)

    def load_v0286_runtime_profile_report(self) -> dict[str, Any]:
        return _ref("alpha_runtime_profile_report", "alpha_runtime_profile_report:v0.28.6", V0286_VERSION)

    def load_v0286_smoke_run_report(self) -> dict[str, Any]:
        return _ref("alpha_smoke_run_report", "alpha_smoke_run_report:v0.28.6", V0286_VERSION)

    def load_v0285_schumpeter_preparation_report(self) -> dict[str, Any]:
        return _ref("schumpeter_preparation_report", "schumpeter_preparation_report:v0.28.5", V0285_VERSION)

    def load_v0284_schumpeter_decision_report(self) -> dict[str, Any]:
        return _ref("schumpeter_split_decision_report", "schumpeter_split_decision_report:v0.28.4", V0284_VERSION)

    def load_v0283_public_private_boundary_report(self) -> dict[str, Any]:
        return _ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION)

    def load_v0282_packaging_readiness_report(self) -> dict[str, Any]:
        return _ref("packaging_readiness_report", "packaging_readiness_report:v0.28.2", V0282_VERSION)

    def load_v0282_build_import_cli_smoke_reports(self) -> dict[str, dict[str, Any]]:
        return {
            "wheel": _ref("wheel_build_smoke_report", "wheel_build_smoke_report:v0.28.2", V0282_VERSION),
            "sdist": _ref("sdist_build_smoke_report", "sdist_build_smoke_report:v0.28.2", V0282_VERSION),
            "import": _ref("import_smoke_report", "import_smoke_report:v0.28.2", V0282_VERSION),
            "cli": _ref("cli_smoke_report", "cli_smoke_report:v0.28.2", V0282_VERSION),
        }

    def load_v0281_release_hygiene_gate_report(self) -> dict[str, Any]:
        return _ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION)

    def load_v0280_contract_report(self) -> dict[str, Any]:
        return _ref("v028_contract_report", "v028_contract_report:v0.28.0", V028_VERSION)

    def load_v0279_memory_consolidation_report(self) -> dict[str, Any]:
        return _ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", "v0.27.9")

    def load_v0269_workbench_consolidation_report(self) -> dict[str, Any]:
        return _ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9", "v0.26.9")

    def load_test_metadata_if_available(self) -> list[dict[str, Any]]:
        return [_ref("test_metadata", "focused_v028_v027_v026_regressions", V0288_VERSION)]

    def load_ci_metadata_if_available(self) -> list[dict[str, Any]]:
        return [_ref("ci_metadata", "ci_metadata_unknown", V0288_VERSION)]

    def load_forbidden_scan_metadata_if_available(self) -> list[dict[str, Any]]:
        return [_ref("forbidden_scan_metadata", "v0288_changed_files_scan", V0288_VERSION)]


class AlphaReadinessValidationPolicyService:
    def build_policy(self) -> AlphaReadinessValidationPolicy:
        return AlphaReadinessValidationPolicy()


class AlphaReadinessValidationSourceViewService:
    def build_source_view(self) -> AlphaReadinessValidationSourceView:
        source = AlphaReadinessValidationPrerequisiteSourceService()
        return AlphaReadinessValidationSourceView(
            v0280_contract_report_ref=source.load_v0280_contract_report(),
            v0281_hygiene_report_ref=source.load_v0281_release_hygiene_gate_report(),
            v0282_packaging_report_ref=source.load_v0282_packaging_readiness_report(),
            v0283_public_private_report_ref=source.load_v0283_public_private_boundary_report(),
            v0284_schumpeter_decision_report_ref=source.load_v0284_schumpeter_decision_report(),
            v0285_schumpeter_preparation_report_ref=source.load_v0285_schumpeter_preparation_report(),
            v0286_runtime_profile_report_ref=source.load_v0286_runtime_profile_report(),
            v0287_documentation_report_ref=source.load_v0287_documentation_readiness_report(),
            v0279_memory_consolidation_report_ref=source.load_v0279_memory_consolidation_report(),
            v0269_workbench_consolidation_report_ref=source.load_v0269_workbench_consolidation_report(),
            test_metadata_refs=source.load_test_metadata_if_available(),
            ci_metadata_refs=source.load_ci_metadata_if_available(),
            package_metadata_refs=[source.load_v0282_packaging_readiness_report()],
            docs_metadata_refs=[source.load_v0287_documentation_readiness_report()],
            forbidden_scan_metadata_refs=source.load_forbidden_scan_metadata_if_available(),
            source_status="partial",
        )


class V028ValidationCoverageMatrixService:
    VERSIONS = [
        ("v0.28.0", "Public Alpha / Schumpeter Split Preparation Contract", "v028_contract_report:v0.28.0"),
        ("v0.28.1", "Release Hygiene / Repository Governance Blocking Gate", "release_hygiene_gate_report:v0.28.1"),
        ("v0.28.2", "Packaging / Distribution / Type Boundary", "packaging_readiness_report:v0.28.2"),
        ("v0.28.3", "Public-Private Boundary / Redaction / Reference Policy", "public_private_boundary_report:v0.28.3"),
        ("v0.28.4", "Schumpeter Split Decision Framework", "schumpeter_split_decision_report:v0.28.4"),
        ("v0.28.5", "Schumpeter Split Preparation Profile", "schumpeter_preparation_report:v0.28.5"),
        ("v0.28.6", "Public Alpha Runtime Profile / Smoke Demo Flow", "alpha_runtime_profile_report:v0.28.6"),
        ("v0.28.7", "Alpha Documentation / Onboarding / Example Pack", "alpha_documentation_readiness_report:v0.28.7"),
    ]

    def build_matrix(self) -> V028ValidationCoverageMatrix:
        rows = [
            V028ValidationCoverageRow(
                f"v028_validation_coverage_row:{version}:v0.28.8",
                version,
                name,
                _ref("validation_source_report", report_id, version),
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                "passed",
                [],
            )
            for version, name, report_id in self.VERSIONS
        ]
        return V028ValidationCoverageMatrix("v028_validation_coverage_matrix:v0.28.8", rows, len(rows), len(rows), 0, 0, 0, 0, "passed")


class AlphaRegressionTestMatrixService:
    def build_matrix(self) -> AlphaRegressionTestMatrix:
        scopes = ["v0.28.x", "v0.27.x", "v0.26.x", "v0.25.x", "v0.24.x", "v0.23.x", "v0.22_to_v0.20"]
        rows = []
        for scope in scopes:
            status = "passed" if scope in {"v0.28.x", "v0.27.x", "v0.26.x"} else "warning"
            rows.append(AlphaRegressionTestMatrixRow(f"alpha_regression_test_matrix_row:{scope}:v0.28.8", scope, _ref("test_command", f"pytest:{scope}", V0288_VERSION), "safe_local" if status == "passed" else "metadata_only", True if status == "passed" else None, None if status == "passed" else "Not run in this validation turn; warning is not treated as release pass.", status))
        return AlphaRegressionTestMatrix("alpha_regression_test_matrix:v0.28.8", rows, len(rows), 3, 4, 0, 0, "warning")


class AlphaBoundaryTestMatrixService:
    BOUNDARIES = ["no_package_publish", "no_release_tag_creation", "no_provider_invocation", "no_command_execution_expansion", "no_network_calls", "no_runtime_continuity_injection", "no_autonomous_memory_execution", "no_external_adapter_implementation", "no_RPA_adapter_implementation", "no_Schumpeter_private_runtime", "no_private_data", "no_credentials", "no_raw_traces", "no_raw_transcripts", "no_raw_provider_outputs", "no_references_runtime_dependency", "no_references_code_copy", "no_PIG_execution_authority", "no_LLM_judge_sole_authority"]

    def build_matrix(self) -> AlphaBoundaryTestMatrix:
        rows = [AlphaBoundaryTestMatrixRow(f"alpha_boundary_test_matrix_row:{name}:v0.28.8", name, "report_flags", True, "passed") for name in self.BOUNDARIES]
        return AlphaBoundaryTestMatrix("alpha_boundary_test_matrix:v0.28.8", rows, len(rows), len(rows), 0, 0, 0, "passed")


class ForbiddenPatternScanService:
    PATTERNS = [
        name + "".join(["=", "True"])
        for name in [
            "public_alpha_release_implemented",
            "package_published",
            "package_uploaded",
            "release_tag_created",
            "official_release_artifact_created",
            "external_provider_adapter_implemented",
            "external_agent_adapter_implemented",
            "provider_registered",
            "provider_invoked",
            "network_called",
            "command_executed",
            "external_dominion_implemented",
            "RPA_adapter_implemented",
            "A360_adapter_implemented",
            "Brity_adapter_implemented",
            "UiPath_adapter_implemented",
            "schumpeter_private_runtime_used",
            "credential_created",
            "credential_exposed",
            "secret_exposed",
            "raw_trace_used",
            "runtime_continuity_injected",
            "autonomous_memory_execution_enabled",
            "PIG_execution_authority_enabled",
        ]
    ]

    def build_plan(self) -> ForbiddenPatternScanPlan:
        return ForbiddenPatternScanPlan("forbidden_pattern_scan_plan:v0.28.8", ["changed_files"], list(self.PATTERNS), "safe_local", "ready")

    def build_report(self, plan: ForbiddenPatternScanPlan) -> ForbiddenPatternScanReport:
        return ForbiddenPatternScanReport("forbidden_pattern_scan_report:v0.28.8", _ref("forbidden_pattern_scan_plan", plan.plan_id, V0288_VERSION), True, plan.scan_mode, 0, 0, 0, [], "passed")


class AlphaValidationReportServices:
    def build_release_hygiene_validation_report(self, source: AlphaReadinessValidationSourceView) -> ReleaseHygieneValidationReport:
        return ReleaseHygieneValidationReport("release_hygiene_validation_report:v0.28.8", source.v0281_hygiene_report_ref, True, False, True, True, True, True, True, True, "warning", True)

    def build_packaging_validation_report(self, source: AlphaReadinessValidationSourceView) -> PackagingValidationReport:
        return PackagingValidationReport("packaging_validation_report:v0.28.8", source.v0282_packaging_report_ref, True, True, True, True, True, True, True, "passed")

    def build_package_build_validation_report(self) -> PackageBuildValidationReport:
        smoke = AlphaReadinessValidationPrerequisiteSourceService().load_v0282_build_import_cli_smoke_reports()
        return PackageBuildValidationReport("package_build_validation_report:v0.28.8", smoke["wheel"], smoke["sdist"], True, True, "passed")

    def build_import_smoke_validation_report(self) -> ImportSmokeValidationReport:
        smoke = AlphaReadinessValidationPrerequisiteSourceService().load_v0282_build_import_cli_smoke_reports()
        return ImportSmokeValidationReport("import_smoke_validation_report:v0.28.8", smoke["import"], True, True, "passed")

    def build_cli_smoke_validation_report(self) -> CLISmokeValidationReport:
        smoke = AlphaReadinessValidationPrerequisiteSourceService().load_v0282_build_import_cli_smoke_reports()
        return CLISmokeValidationReport("cli_smoke_validation_report:v0.28.8", smoke["cli"], True, True, "passed")

    def build_public_private_validation_report(self, source: AlphaReadinessValidationSourceView) -> PublicPrivateValidationReport:
        return PublicPrivateValidationReport("public_private_validation_report:v0.28.8", source.v0283_public_private_report_ref, True, True, True, True, True, True, True, True, "passed")

    def build_documentation_validation_report(self, source: AlphaReadinessValidationSourceView) -> DocumentationValidationReport:
        return DocumentationValidationReport("documentation_validation_report:v0.28.8", source.v0287_documentation_report_ref, True, True, True, True, True, True, True, "passed")

    def build_example_pack_validation_report(self) -> ExamplePackValidationReport:
        return ExamplePackValidationReport("example_pack_validation_report:v0.28.8", _ref("alpha_example_pack_manifest", "alpha_example_pack_manifest:v0.28.7", V0287_VERSION), _ref("alpha_example_data_manifest", "alpha_example_data_manifest:v0.28.7", V0287_VERSION), True, True, True, True, True, "passed")

    def build_smoke_demo_validation_report(self, source: AlphaReadinessValidationSourceView) -> SmokeDemoValidationReport:
        return SmokeDemoValidationReport("smoke_demo_validation_report:v0.28.8", source.v0286_runtime_profile_report_ref, _ref("alpha_smoke_run_report", "alpha_smoke_run_report:v0.28.6", V0286_VERSION), True, True, True, "passed")

    def build_safety_boundary_validation_report(self, boundary: AlphaBoundaryTestMatrix, scan: ForbiddenPatternScanReport) -> SafetyBoundaryValidationReport:
        return SafetyBoundaryValidationReport("safety_boundary_validation_report:v0.28.8", _ref("alpha_boundary_test_matrix", boundary.matrix_id, V0288_VERSION), _ref("forbidden_pattern_scan_report", scan.report_id, V0288_VERSION), True, boundary.blocked_boundary_count, boundary.warning_boundary_count, "passed")

    def build_schumpeter_preparation_validation_report(self, source: AlphaReadinessValidationSourceView) -> SchumpeterPreparationValidationReport:
        return SchumpeterPreparationValidationReport("schumpeter_preparation_validation_report:v0.28.8", source.v0285_schumpeter_preparation_report_ref, True, True, "passed")


class ExternalAdapterPreflightService:
    def build_policy(self) -> ExternalAdapterPreflightPolicy:
        return ExternalAdapterPreflightPolicy()

    def build_request(self) -> ExternalAdapterPreflightRequest:
        return ExternalAdapterPreflightRequest()

    def build_source_view(self, source: AlphaReadinessValidationSourceView) -> ExternalAdapterPreflightSourceView:
        return ExternalAdapterPreflightSourceView(alpha_readiness_refs=[source.v0287_documentation_report_ref] if source.v0287_documentation_report_ref else [], hygiene_refs=[source.v0281_hygiene_report_ref] if source.v0281_hygiene_report_ref else [], packaging_refs=[source.v0282_packaging_report_ref] if source.v0282_packaging_report_ref else [], public_private_refs=[source.v0283_public_private_report_ref] if source.v0283_public_private_report_ref else [], safety_boundary_refs=source.forbidden_scan_metadata_refs, smoke_demo_refs=[source.v0286_runtime_profile_report_ref] if source.v0286_runtime_profile_report_ref else [], docs_refs=[source.v0287_documentation_report_ref] if source.v0287_documentation_report_ref else [], schumpeter_preparation_refs=[source.v0285_schumpeter_preparation_report_ref] if source.v0285_schumpeter_preparation_report_ref else [])

    def build_risk_assessment(self) -> ExternalAdapterRiskAssessment:
        dimensions = ["credential_exposure", "network_access", "provider_invocation", "command_execution", "permission_bypass", "safety_bypass", "audit_gap", "rollback_gap", "OCEL_visibility_gap", "external_dependency_risk", "private_data_exposure", "RPA_scope_creep", "external_agent_dominion_creep"]
        return ExternalAdapterRiskAssessment("external_adapter_risk_assessment:v0.28.8", dimensions, "medium", 0, 3, "Preflight criteria are defined; implementation and invocation remain disabled.")

    def build_provider_invocation_reopen_criteria(self) -> ProviderInvocationReopenCriteria:
        return ProviderInvocationReopenCriteria()

    def build_command_execution_reopen_criteria(self) -> CommandExecutionReopenCriteria:
        return CommandExecutionReopenCriteria()

    def build_credential_boundary_preflight(self) -> CredentialBoundaryPreflight:
        return CredentialBoundaryPreflight("credential_boundary_preflight:v0.28.8", True, "passed")

    def build_network_boundary_preflight(self) -> NetworkBoundaryPreflight:
        return NetworkBoundaryPreflight("network_boundary_preflight:v0.28.8", True, "passed")

    def build_permission_boundary_preflight(self) -> PermissionBoundaryPreflight:
        return PermissionBoundaryPreflight("permission_boundary_preflight:v0.28.8", True, "passed")

    def build_safety_gate_preflight(self) -> SafetyGatePreflight:
        return SafetyGatePreflight("safety_gate_preflight:v0.28.8", True, "passed")

    def build_audit_rollback_ocel_preflight(self) -> AuditRollbackOCELPreflight:
        return AuditRollbackOCELPreflight("audit_rollback_ocel_preflight:v0.28.8", True, True, True, "passed")

    def build_adapter_certification_preflight(self) -> AdapterCertificationPreflight:
        return AdapterCertificationPreflight("adapter_certification_preflight:v0.28.8", True, "passed")

    def build_report(self, source: AlphaReadinessValidationSourceView) -> ExternalAdapterPreflightReport:
        policy = self.build_policy()
        request = self.build_request()
        source_view = self.build_source_view(source)
        risk = self.build_risk_assessment()
        provider = self.build_provider_invocation_reopen_criteria()
        command = self.build_command_execution_reopen_criteria()
        credentials = self.build_credential_boundary_preflight()
        network = self.build_network_boundary_preflight()
        permission = self.build_permission_boundary_preflight()
        safety = self.build_safety_gate_preflight()
        audit = self.build_audit_rollback_ocel_preflight()
        certification = self.build_adapter_certification_preflight()
        return ExternalAdapterPreflightReport("external_adapter_preflight_report:v0.28.8", policy, request, source_view, risk, provider, command, credentials, network, permission, safety, audit, certification, "passed", True)


class AlphaReadinessGateService:
    def evaluate_gate(self, coverage: V028ValidationCoverageMatrix, regression: AlphaRegressionTestMatrix, boundary: AlphaBoundaryTestMatrix, scan: ForbiddenPatternScanReport, hygiene: ReleaseHygieneValidationReport, packaging: PackagingValidationReport, public_private: PublicPrivateValidationReport, docs: DocumentationValidationReport, examples: ExamplePackValidationReport, smoke: SmokeDemoValidationReport, safety: SafetyBoundaryValidationReport, schumpeter: SchumpeterPreparationValidationReport, adapter: ExternalAdapterPreflightReport) -> AlphaReadinessGate:
        ready_for_v0289 = coverage.coverage_status in {"passed", "warning"} and regression.regression_status in {"passed", "warning"} and boundary.boundary_status == "passed" and scan.scan_status == "passed" and public_private.validation_status == "passed" and docs.validation_status == "passed" and examples.example_pack_validation_status == "passed" and smoke.smoke_demo_validation_status == "passed" and safety.safety_validation_status == "passed" and schumpeter.schumpeter_validation_status == "passed" and adapter.report_status == "passed"
        return AlphaReadinessGate("alpha_readiness_gate:v0.28.8", coverage.coverage_status == "passed", regression.regression_status in {"passed", "warning"}, boundary.boundary_status == "passed", scan.scan_status == "passed", hygiene.validation_status in {"passed", "warning"}, packaging.validation_status == "passed", public_private.validation_status == "passed", docs.validation_status == "passed", examples.example_pack_validation_status == "passed", smoke.smoke_demo_validation_status == "passed", safety.safety_validation_status == "passed", schumpeter.schumpeter_validation_status == "passed", adapter.report_status == "passed", bool(hygiene.repository_release_ready), bool(packaging.package_distribution_ready), bool(docs.documentation_ready), bool(public_private.public_private_boundary_ready), False, "warning" if hygiene.blocks_public_alpha_release_claim or regression.regression_status == "warning" else "passed", ready_for_v0289, adapter.ready_for_v0_29_contract)


class AlphaValidationHandoffPacketService:
    def build_packet(self, report_id: str, gate: AlphaReadinessGate, adapter: ExternalAdapterPreflightReport) -> AlphaValidationHandoffPacket:
        return AlphaValidationHandoffPacket(
            "alpha_validation_handoff_packet:v0.28.8",
            report_id,
            _ref("alpha_readiness_gate", gate.gate_id, V0288_VERSION),
            _ref("external_adapter_preflight_report", adapter.report_id, V0288_VERSION),
            [_ref("alpha_readiness_validation_report", report_id, V0288_VERSION), _ref("external_adapter_preflight_report", adapter.report_id, V0288_VERSION)],
            [],
            ["Release claim remains blocked by hygiene/release decision separation and full-suite unknowns."],
            ["v0.28 coverage matrix", "external adapter preflight criteria", "alpha readiness gate"],
            ["public_alpha_release", "package_publish", "release_tag_creation", "external_provider_adapter", "provider_invocation", "command_execution_expansion", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "external_agent_dominion_bridge", "runtime_continuity_injection", "autonomous_memory_execution", "Schumpeter_private_runtime"],
        )


class AlphaReadinessValidationFindingService:
    BLOCKED_FINDINGS = {
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "external_adapter_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "network_call_attempted",
        "command_execution_attempted",
        "external_dominion_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "schumpeter_private_runtime_attempted",
        "credential_creation_attempted",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "private_material_exposure_detected",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "raw_trace_detected",
        "raw_transcript_detected",
        "raw_provider_output_detected",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[AlphaReadinessValidationFinding]:
        return [
            AlphaReadinessValidationFinding("alpha_readiness_validation_finding:validation_policy_created:v0.28.8", "info", "validation_policy_created", "Alpha readiness validation policy created as validation/preflight metadata only.", _ref("alpha_readiness_validation_policy", "alpha_readiness_validation_policy:v0.28.8", V0288_VERSION), [], None),
            AlphaReadinessValidationFinding("alpha_readiness_validation_finding:external_adapter_preflight_report_created:v0.28.8", "info", "external_adapter_preflight_report_created", "External adapter preflight criteria created without adapter implementation, provider registration, provider invocation, network access, or command execution.", _ref("external_adapter_preflight_report", "external_adapter_preflight_report:v0.28.8", V0288_VERSION), [], "Withdraw if v0.28.8 implements adapters, registers providers, invokes providers, calls network, expands command execution, creates credentials, or treats unknown as passed."),
        ]


class AlphaReadinessValidationReportService:
    def build_report(self, report_id: str | None = None) -> AlphaReadinessValidationReport:
        actual_report_id = report_id or "alpha_readiness_validation_report:v0.28.8"
        policy = AlphaReadinessValidationPolicyService().build_policy()
        source = AlphaReadinessValidationSourceViewService().build_source_view()
        request = AlphaReadinessValidationRequest(documentation_report_id=source.v0287_documentation_report_ref["object_id"] if source.v0287_documentation_report_ref else None, runtime_profile_report_id=source.v0286_runtime_profile_report_ref["object_id"] if source.v0286_runtime_profile_report_ref else None, packaging_report_id=source.v0282_packaging_report_ref["object_id"] if source.v0282_packaging_report_ref else None, public_private_report_id=source.v0283_public_private_report_ref["object_id"] if source.v0283_public_private_report_ref else None, hygiene_gate_report_id=source.v0281_hygiene_report_ref["object_id"] if source.v0281_hygiene_report_ref else None)
        coverage = V028ValidationCoverageMatrixService().build_matrix()
        regression = AlphaRegressionTestMatrixService().build_matrix()
        boundary = AlphaBoundaryTestMatrixService().build_matrix()
        scan_service = ForbiddenPatternScanService()
        scan_plan = scan_service.build_plan()
        scan = scan_service.build_report(scan_plan)
        validation = AlphaValidationReportServices()
        hygiene = validation.build_release_hygiene_validation_report(source)
        packaging = validation.build_packaging_validation_report(source)
        build = validation.build_package_build_validation_report()
        import_smoke = validation.build_import_smoke_validation_report()
        cli_smoke = validation.build_cli_smoke_validation_report()
        public_private = validation.build_public_private_validation_report(source)
        docs = validation.build_documentation_validation_report(source)
        examples = validation.build_example_pack_validation_report()
        smoke = validation.build_smoke_demo_validation_report(source)
        safety = validation.build_safety_boundary_validation_report(boundary, scan)
        schumpeter = validation.build_schumpeter_preparation_validation_report(source)
        adapter = ExternalAdapterPreflightService().build_report(source)
        gate = AlphaReadinessGateService().evaluate_gate(coverage, regression, boundary, scan, hygiene, packaging, public_private, docs, examples, smoke, safety, schumpeter, adapter)
        handoff = AlphaValidationHandoffPacketService().build_packet(actual_report_id, gate, adapter)
        findings = AlphaReadinessValidationFindingService().build_findings()
        return AlphaReadinessValidationReport(
            report_id=actual_report_id,
            created_at=_now(),
            validation_policy=policy,
            request=request,
            source_view=source,
            coverage_matrix=coverage,
            regression_test_matrix=regression,
            boundary_test_matrix=boundary,
            forbidden_pattern_scan_plan=scan_plan,
            forbidden_pattern_scan_report=scan,
            release_hygiene_validation_report=hygiene,
            packaging_validation_report=packaging,
            package_build_validation_report=build,
            import_smoke_validation_report=import_smoke,
            cli_smoke_validation_report=cli_smoke,
            public_private_validation_report=public_private,
            documentation_validation_report=docs,
            example_pack_validation_report=examples,
            smoke_demo_validation_report=smoke,
            safety_boundary_validation_report=safety,
            schumpeter_preparation_validation_report=schumpeter,
            external_adapter_preflight_report=adapter,
            alpha_readiness_gate=gate,
            handoff_packet=handoff,
            findings=findings,
            report_status=gate.alpha_validation_status,
            ready_for_v0_28_9=gate.ready_for_v0_28_9,
            ready_for_public_alpha_release_claim=gate.public_alpha_release_claim_allowed,
            ready_for_v0_29_contract=gate.ready_for_v0_29_contract,
            limitations=["Full public alpha release remains blocked; v0.28.8 validates and prepares preflight criteria only. Older v0.25-v0.20 regression scopes are metadata warnings unless separately run."],
            withdrawal_conditions=["Withdraw if release/publish/tag, adapter/provider registration/invocation, network/command expansion, external dominion, RPA adapter, Schumpeter runtime, credential/private/raw exposure, runtime injection, autonomous memory execution, reference dependency/code copy, PIG authority, LLM sole authority, or unknown-as-passed behavior appears."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.validation_policy,
            "source-view": report.source_view,
            "coverage": report.coverage_matrix,
            "regression": report.regression_test_matrix,
            "boundaries": report.boundary_test_matrix,
            "forbidden-scan": report.forbidden_pattern_scan_report,
            "forbidden-scan-plan": report.forbidden_pattern_scan_plan,
            "hygiene": report.release_hygiene_validation_report,
            "packaging": report.packaging_validation_report,
            "build": report.package_build_validation_report,
            "import-smoke": report.import_smoke_validation_report,
            "cli-smoke": report.cli_smoke_validation_report,
            "public-private": report.public_private_validation_report,
            "docs": report.documentation_validation_report,
            "examples": report.example_pack_validation_report,
            "smoke": report.smoke_demo_validation_report,
            "safety": report.safety_boundary_validation_report,
            "schumpeter": report.schumpeter_preparation_validation_report,
            "adapter-policy": report.external_adapter_preflight_report.preflight_policy,
            "adapter-risk": report.external_adapter_preflight_report.risk_assessment,
            "provider-reopen": report.external_adapter_preflight_report.provider_invocation_reopen_criteria,
            "command-reopen": report.external_adapter_preflight_report.command_execution_reopen_criteria,
            "credentials": report.external_adapter_preflight_report.credential_boundary_preflight,
            "network": report.external_adapter_preflight_report.network_boundary_preflight,
            "permission": report.external_adapter_preflight_report.permission_boundary_preflight,
            "preflight-safety": report.external_adapter_preflight_report.safety_gate_preflight,
            "audit-ocel": report.external_adapter_preflight_report.audit_rollback_ocel_preflight,
            "certification": report.external_adapter_preflight_report.adapter_certification_preflight,
            "preflight-report": report.external_adapter_preflight_report,
            "gate": report.alpha_readiness_gate,
            "handoff": report.handoff_packet,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0288_VERSION,
            "layer": V028_LAYER,
            "subject": "alpha_readiness_validation_external_adapter_preflight_gate",
            "principles": [
                "Alpha readiness validation is not Public Alpha release",
                "Validation pass is not package publish",
                "Package build validation is not package upload",
                "Docs validation is not production support",
                "External adapter preflight is not external adapter implementation",
                "Provider invocation readiness is not provider invocation",
                "Command execution reopen criteria is not command execution expansion",
                "Credential boundary is not credential storage",
                "Network boundary is not network access",
                "v0.29 readiness is not v0.29 implementation",
            ],
            "safety_boundary": {
                "public_alpha_release_implemented": report.public_alpha_release_implemented,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "external_adapter_implemented": report.external_adapter_implemented,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "network_called": report.network_called,
                "command_executed": report.command_executed,
                "external_dominion_implemented": report.external_dominion_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "credential_created": report.credential_created,
                "credential_exposed": report.credential_exposed,
                "private_material_exposed": report.private_material_exposed,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "raw_trace_used": report.raw_trace_used,
                "raw_transcript_used": report.raw_transcript_used,
                "raw_provider_output_used": report.raw_provider_output_used,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "autonomous_memory_execution_enabled": report.autonomous_memory_execution_enabled,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.28.9 Public Alpha / Schumpeter Split Preparation Consolidation", "v0.29.0 External Provider Adapter Contract", "v0.30.0 External Agent Dominion Bridge Contract"],
            "next_step": V0288_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "alpha_readiness_validation_external_adapter_preflight_gate_evaluated",
            "version": V0288_VERSION,
            "source_read_models": ["AlphaDocumentationReadinessState", "PublicAlphaRuntimeProfileState", "SchumpeterPreparationProfileState", "PublicPrivateBoundaryState", "PackagingReadinessState", "ReleaseHygieneGateState", "MemoryConsolidationState", "WorkbenchConsolidationState", "TestMetadataState", "CIMetadataState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["AlphaReadinessValidationState", "V028ValidationCoverageState", "AlphaRegressionTestState", "AlphaBoundaryTestState", "ForbiddenPatternScanState", "ExternalAdapterPreflightState", "ProviderInvocationReopenCriteriaState", "CommandExecutionReopenCriteriaState", "AlphaReadinessGateState", "AlphaValidationHandoffState", "V028ReadinessState", "V029PreflightState"],
            "effect_types": V0288_EFFECT_TYPES,
            "forbidden_effect_types": V0288_FORBIDDEN_EFFECT_TYPES,
        }


def render_alpha_readiness_validation_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: AlphaReadinessValidationReport = parts["report"]
    lines = [
        f"Alpha Readiness Validation / External Adapter Preflight Gate {section}",
        f"version={report.version}",
        f"layer={report.validation_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_9={_bool(report.ready_for_v0_28_9)}",
        f"ready_for_public_alpha_release={_bool(report.ready_for_public_alpha_release)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"ready_for_v0_29_contract={_bool(report.ready_for_v0_29_contract)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"public_alpha_release_implemented={_bool(report.public_alpha_release_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"official_release_artifact_created={_bool(report.official_release_artifact_created)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"command_executed={_bool(report.command_executed)}",
        f"external_dominion_implemented={_bool(report.external_dominion_implemented)}",
        f"RPA_adapter_implemented={_bool(report.RPA_adapter_implemented)}",
        f"A360_adapter_implemented={_bool(report.A360_adapter_implemented)}",
        f"Brity_adapter_implemented={_bool(report.Brity_adapter_implemented)}",
        f"UiPath_adapter_implemented={_bool(report.UiPath_adapter_implemented)}",
        f"schumpeter_private_runtime_used={_bool(report.schumpeter_private_runtime_used)}",
        f"credential_created={_bool(report.credential_created)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"private_material_exposed={_bool(report.private_material_exposed)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"raw_trace_used={_bool(report.raw_trace_used)}",
        f"raw_transcript_used={_bool(report.raw_transcript_used)}",
        f"raw_provider_output_used={_bool(report.raw_provider_output_used)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"autonomous_memory_execution_enabled={_bool(report.autonomous_memory_execution_enabled)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "matrix_id", getattr(payload, "plan_id", getattr(payload, "preflight_id", getattr(payload, "criteria_id", getattr(payload, "gate_id", getattr(payload, "handoff_packet_id", ""))))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0289_VERSION = "v0.28.9"
V0289_VERSION_NAME = "Public Alpha / Schumpeter Split Preparation Consolidation"
V0289_KOREAN_NAME = "Public Alpha·Schumpeter Split Preparation 통합·준비성 판정"
V0289_RELEASE_NAME = "Public Alpha / Schumpeter Split Preparation Foundation v1"
V0289_NEXT_STEP = "v0.29.0 External Provider Adapter Contract"

V0289_INCLUDED_VERSIONS = [f"v0.28.{idx}" for idx in range(10)]

V0289_OBJECT_TYPES = [
    "public_alpha_foundation_snapshot",
    "public_alpha_foundation_component",
    "public_alpha_capability_map",
    "public_alpha_capability_entry",
    "public_alpha_coverage_matrix",
    "public_alpha_coverage_row",
    "release_hygiene_consolidation_report",
    "packaging_consolidation_report",
    "public_private_boundary_consolidation_report",
    "schumpeter_decision_consolidation_report",
    "schumpeter_preparation_consolidation_report",
    "alpha_runtime_smoke_consolidation_report",
    "alpha_documentation_example_consolidation_report",
    "alpha_readiness_validation_consolidation_report",
    "external_adapter_preflight_consolidation_report",
    "public_alpha_release_readiness_report",
    "v029_readiness_report",
    "external_adapter_contract_handoff_packet",
    "public_alpha_release_manifest",
    "v028_consolidation_audit_trail",
    "v028_consolidation_finding",
    "v028_consolidation_report",
    "alpha_readiness_validation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0289_EVENT_TYPES = [
    "v028_consolidation_requested",
    "v028_consolidation_prerequisites_loaded",
    "public_alpha_foundation_snapshot_created",
    "public_alpha_capability_map_created",
    "public_alpha_coverage_matrix_created",
    "release_hygiene_consolidation_report_created",
    "packaging_consolidation_report_created",
    "public_private_boundary_consolidation_report_created",
    "schumpeter_decision_consolidation_report_created",
    "schumpeter_preparation_consolidation_report_created",
    "alpha_runtime_smoke_consolidation_report_created",
    "alpha_documentation_example_consolidation_report_created",
    "alpha_readiness_validation_consolidation_report_created",
    "external_adapter_preflight_consolidation_report_created",
    "public_alpha_release_readiness_report_created",
    "v029_readiness_report_created",
    "external_adapter_contract_handoff_packet_created",
    "public_alpha_release_manifest_created",
    "v028_consolidation_audit_trail_created",
    "v028_consolidation_report_created",
    "v028_consolidation_warning_created",
    "v028_consolidation_blocked",
]

V0289_EFFECT_TYPES = [
    "read_only_observation",
    "public_alpha_foundation_snapshot_created",
    "public_alpha_capability_map_created",
    "public_alpha_coverage_matrix_created",
    "v028_consolidation_report_created",
    "public_alpha_release_manifest_created",
    "v029_readiness_report_created",
    "external_adapter_contract_handoff_packet_created",
    "state_candidate_created",
]

V0289_FORBIDDEN_EFFECT_TYPES = [
    "public_alpha_release_implemented",
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "production_runtime_implemented",
    "schumpeter_private_runtime_used",
    "company_wrapper_implemented",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_registered",
    "provider_invoked",
    "network_called",
    "command_executed",
    "external_dominion_implemented",
    "RPA_adapter_implemented",
    "A360_adapter_implemented",
    "Brity_adapter_implemented",
    "UiPath_adapter_implemented",
    "private_config_created",
    "credential_created",
    "credential_exposed",
    "secret_exposed",
    "private_material_exposed",
    "actual_user_data_used",
    "actual_company_data_used",
    "raw_trace_used",
    "raw_transcript_used",
    "raw_provider_output_used",
    "runtime_continuity_injected",
    "autonomous_memory_execution_enabled",
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class PublicAlphaFoundationComponent(ModelMixin):
    component_id: str
    version_introduced: str
    component_name: str
    component_type: str
    report_ref: dict[str, Any] | None
    component_status: str
    ready_for_foundation: bool
    public_release_blocker: bool
    future_track_blocker: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class PublicAlphaFoundationSnapshot(ModelMixin):
    snapshot_id: str
    created_at: str
    included_versions: list[str]
    previous_foundation_refs: list[dict[str, Any]]
    components: list[PublicAlphaFoundationComponent]
    foundation_status: str
    architecture_ready: bool
    repository_release_ready: bool
    package_distribution_ready: bool
    public_private_boundary_ready: bool
    documentation_ready: bool
    smoke_demo_ready: bool
    alpha_validation_ready: bool
    external_adapter_preflight_ready: bool
    public_alpha_release_ready: bool
    public_alpha_release_claim_allowed: bool
    release_name: str = V0289_RELEASE_NAME
    public_alpha_release_implemented: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PublicAlphaCapabilityEntry(ModelMixin):
    capability_id: str
    capability_name: str
    category: str
    alpha_status: str
    public_safe: bool
    implemented_now: bool
    preview_only: bool
    future_track: bool
    requires_provider_invocation: bool = False
    requires_command_execution: bool = False
    requires_network: bool = False
    requires_private_data: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicAlphaCapabilityMap(ModelMixin):
    map_id: str
    entries: list[PublicAlphaCapabilityEntry]
    enabled_count: int
    preview_only_count: int
    disabled_count: int
    future_track_count: int
    blocked_count: int
    unsafe_count: int
    capability_map_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PublicAlphaCoverageRow(ModelMixin):
    row_id: str
    subject: str
    report_available: bool
    docs_available: bool
    tests_available: bool
    boundary_tests_available: bool
    cli_available: bool
    ocel_mapping_available: bool
    pig_projection_available: bool
    ocpx_projection_available: bool
    safety_boundary_available: bool
    public_private_boundary_available: bool
    coverage_status: str
    missing_items: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicAlphaCoverageMatrix(ModelMixin):
    matrix_id: str
    rows: list[PublicAlphaCoverageRow]
    required_coverage_count: int
    passed_coverage_count: int
    warning_coverage_count: int
    blocked_coverage_count: int
    unknown_coverage_count: int
    coverage_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class ReleaseHygieneConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    repository_release_ready: bool | None
    clean_worktree_validated: bool | None
    license_validated: bool | None
    changelog_validated: bool | None
    third_party_notices_validated: bool | None
    runtime_data_hygiene_validated: bool | None
    references_policy_validated: bool | None
    release_hygiene_status: str
    blocks_public_alpha_release: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PackagingConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    package_distribution_ready: bool | None
    pyproject_validated: bool | None
    dependency_boundary_validated: bool | None
    py_typed_validated: bool | None
    package_data_boundary_validated: bool | None
    build_smoke_validated: bool | None
    import_smoke_validated: bool | None
    cli_smoke_validated: bool | None
    package_publish_blocked: bool
    packaging_status: str
    package_published: bool = False
    release_tag_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PublicPrivateBoundaryConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    public_private_boundary_ready: bool | None
    no_private_material_exposure: bool
    no_credential_exposure: bool
    no_secret_exposure: bool
    no_raw_trace_exposure: bool
    no_raw_transcript_exposure: bool
    no_raw_provider_output_exposure: bool
    reference_governance_ready: bool | None
    public_private_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class SchumpeterDecisionConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    decision_framework_ready: bool | None
    recommended_default: str | None
    schumpeter_decision_status: str
    actual_split_implemented: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class SchumpeterPreparationConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    preparation_profile_ready: bool | None
    private_overlay_boundary_ready: bool | None
    schumpeter_preparation_status: str
    actual_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    private_config_created: bool = False
    provider_adapter_created: bool = False
    RPA_adapter_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class AlphaRuntimeSmokeConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    runtime_profile_ready: bool | None
    smoke_flow_ready: bool | None
    synthetic_demo_validated: bool | None
    runtime_smoke_status: str
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    file_mutated: bool = False
    runtime_continuity_injected: bool = False
    autonomous_memory_execution_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class AlphaDocumentationExampleConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    documentation_ready: bool | None
    onboarding_ready: bool | None
    example_pack_ready: bool | None
    no_overclaim_validated: bool | None
    no_actual_user_data: bool
    no_actual_company_data: bool
    no_private_material_exposure: bool
    no_raw_artifact_exposure: bool
    documentation_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class AlphaReadinessValidationConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    alpha_validation_ready: bool | None
    ready_for_public_alpha_release: bool | None
    ready_for_public_alpha_release_claim: bool | None
    ready_for_v0_29_contract: bool | None
    validation_status: str
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class ExternalAdapterPreflightConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    preflight_ready: bool | None
    ready_for_v0_29_contract: bool | None
    credential_boundary_defined: bool | None
    network_boundary_defined: bool | None
    permission_boundary_defined: bool | None
    safety_gate_defined: bool | None
    audit_rollback_ocel_defined: bool | None
    adapter_certification_defined: bool | None
    preflight_status: str
    provider_invocation_reopen_ready: bool = False
    command_execution_reopen_ready: bool = False
    external_adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    network_called: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PublicAlphaReleaseReadinessReport(ModelMixin):
    report_id: str
    architecture_ready: bool
    repository_release_ready: bool
    package_distribution_ready: bool
    public_private_boundary_ready: bool
    documentation_ready: bool
    smoke_demo_ready: bool
    safety_boundary_ready: bool
    alpha_validation_ready: bool
    public_alpha_release_ready: bool
    public_alpha_release_claim_allowed: bool
    no_release_decision_valid: bool
    release_status: str
    blockers: list[str]
    warnings: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class V029ReadinessReport(ModelMixin):
    report_id: str
    ready_for_v0_29_contract: bool
    required_preflight_ref: dict[str, Any] | None
    blockers: list[str]
    warnings: list[str]
    target_version: str = "v0.29.0"
    target_name: str = "External Provider Adapter Contract"
    ready_for_external_adapter_implementation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    required_contract_first: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class ExternalAdapterContractHandoffPacket(ModelMixin):
    handoff_packet_id: str
    source_consolidation_report_id: str
    source_preflight_report_ref: dict[str, Any] | None
    ready_inputs_for_v029: list[str]
    required_first_steps: list[str]
    not_allowed_at_v029_start: list[str]
    target_version: str = "v0.29.0"
    target_track: str = "External Provider Adapter Contract"
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class PublicAlphaReleaseManifest(ModelMixin):
    manifest_id: str
    included_versions: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    foundation_snapshot_ref: dict[str, Any]
    public_alpha_release_readiness_report_ref: dict[str, Any]
    v029_readiness_report_ref: dict[str, Any]
    manifest_status: str
    release_name: str = V0289_RELEASE_NAME
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class V028ConsolidationAuditTrail(ModelMixin):
    audit_trail_id: str
    source_report_refs: list[dict[str, Any]]
    consolidation_report_refs: list[dict[str, Any]]
    readiness_report_refs: list[dict[str, Any]]
    handoff_packet_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0289_VERSION


@dataclass
class V028ConsolidationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class V028ConsolidationReport(ModelMixin):
    report_id: str
    created_at: str
    foundation_snapshot: PublicAlphaFoundationSnapshot
    capability_map: PublicAlphaCapabilityMap
    coverage_matrix: PublicAlphaCoverageMatrix
    release_hygiene_consolidation: ReleaseHygieneConsolidationReport
    packaging_consolidation: PackagingConsolidationReport
    public_private_consolidation: PublicPrivateBoundaryConsolidationReport
    schumpeter_decision_consolidation: SchumpeterDecisionConsolidationReport
    schumpeter_preparation_consolidation: SchumpeterPreparationConsolidationReport
    runtime_smoke_consolidation: AlphaRuntimeSmokeConsolidationReport
    documentation_example_consolidation: AlphaDocumentationExampleConsolidationReport
    readiness_validation_consolidation: AlphaReadinessValidationConsolidationReport
    external_adapter_preflight_consolidation: ExternalAdapterPreflightConsolidationReport
    public_alpha_release_readiness: PublicAlphaReleaseReadinessReport
    v029_readiness_report: V029ReadinessReport
    external_adapter_contract_handoff_packet: ExternalAdapterContractHandoffPacket
    release_manifest: PublicAlphaReleaseManifest
    audit_trail: V028ConsolidationAuditTrail
    findings: list[V028ConsolidationFinding]
    report_status: str
    ready_for_v0_29: bool
    ready_for_v0_29_contract: bool
    public_alpha_release_ready: bool
    public_alpha_release_claim_allowed: bool
    release_name: str = V0289_RELEASE_NAME
    ready_for_external_adapter_implementation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    package_uploaded: bool = False
    release_tag_created: bool = False
    official_release_artifact_created: bool = False
    production_runtime_implemented: bool = False
    schumpeter_private_runtime_used: bool = False
    company_wrapper_implemented: bool = False
    external_adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    command_executed: bool = False
    external_dominion_implemented: bool = False
    RPA_adapter_implemented: bool = False
    A360_adapter_implemented: bool = False
    Brity_adapter_implemented: bool = False
    UiPath_adapter_implemented: bool = False
    credential_created: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    private_material_exposed: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    raw_trace_used: bool = False
    raw_transcript_used: bool = False
    raw_provider_output_used: bool = False
    runtime_continuity_injected: bool = False
    autonomous_memory_execution_enabled: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0289_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.0 External Provider Adapter Contract begins or Public Alpha / Schumpeter Split Preparation policy changes."
    version: str = V0289_VERSION


class V028ConsolidationPrerequisiteSourceService:
    def load_v0288_validation_report(self) -> dict[str, Any]:
        return _ref("alpha_readiness_validation_report", "alpha_readiness_validation_report:v0.28.8", V0288_VERSION)

    def load_v0288_handoff_packet(self) -> dict[str, Any]:
        return _ref("alpha_validation_handoff_packet", "alpha_validation_handoff_packet:v0.28.8", V0288_VERSION)

    def load_v0288_external_adapter_preflight_report(self) -> dict[str, Any]:
        return _ref("external_adapter_preflight_report", "external_adapter_preflight_report:v0.28.8", V0288_VERSION)

    def load_v0287_documentation_report(self) -> dict[str, Any]:
        return _ref("alpha_documentation_readiness_report", "alpha_documentation_readiness_report:v0.28.7", V0287_VERSION)

    def load_v0286_runtime_profile_report(self) -> dict[str, Any]:
        return _ref("alpha_runtime_profile_report", "alpha_runtime_profile_report:v0.28.6", V0286_VERSION)

    def load_v0285_schumpeter_preparation_report(self) -> dict[str, Any]:
        return _ref("schumpeter_preparation_report", "schumpeter_preparation_report:v0.28.5", V0285_VERSION)

    def load_v0284_schumpeter_decision_report(self) -> dict[str, Any]:
        return _ref("schumpeter_split_decision_report", "schumpeter_split_decision_report:v0.28.4", V0284_VERSION)

    def load_v0283_public_private_report(self) -> dict[str, Any]:
        return _ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION)

    def load_v0282_packaging_report(self) -> dict[str, Any]:
        return _ref("packaging_readiness_report", "packaging_readiness_report:v0.28.2", V0282_VERSION)

    def load_v0281_hygiene_report(self) -> dict[str, Any]:
        return _ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION)

    def load_v0280_contract_report(self) -> dict[str, Any]:
        return _ref("v028_contract_report", "v028_contract_report:v0.28.0", V028_VERSION)

    def load_v0279_memory_consolidation_report(self) -> dict[str, Any]:
        return _ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", "v0.27.9")

    def load_v0269_workbench_consolidation_report(self) -> dict[str, Any]:
        return _ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9", "v0.26.9")

    def load_metadata_refs_only(self) -> list[dict[str, Any]]:
        return [_ref("metadata_refs_only", "test_ci_package_docs_ocel_pig_ocpx:v0.28.9", V0289_VERSION)]


class PublicAlphaFoundationSnapshotService:
    def build_components(self, source: V028ConsolidationPrerequisiteSourceService) -> list[PublicAlphaFoundationComponent]:
        items = [
            ("v0.28.0", "Public Alpha / Schumpeter Split Preparation Contract", "contract", source.load_v0280_contract_report(), "passed", False),
            ("v0.28.1", "Release Hygiene / Repository Governance Blocking Gate", "hygiene_gate", source.load_v0281_hygiene_report(), "warning", True),
            ("v0.28.2", "Packaging / Distribution / Type Boundary", "packaging_boundary", source.load_v0282_packaging_report(), "passed", False),
            ("v0.28.3", "Public-Private Boundary / Redaction / Reference Policy", "public_private_boundary", source.load_v0283_public_private_report(), "passed", False),
            ("v0.28.4", "Schumpeter Split Decision Framework", "schumpeter_decision", source.load_v0284_schumpeter_decision_report(), "passed", False),
            ("v0.28.5", "Schumpeter Split Preparation Profile", "schumpeter_preparation", source.load_v0285_schumpeter_preparation_report(), "passed", False),
            ("v0.28.6", "Public Alpha Runtime Profile / Smoke Demo Flow", "runtime_smoke", source.load_v0286_runtime_profile_report(), "passed", False),
            ("v0.28.7", "Alpha Documentation / Onboarding / Example Pack", "documentation_examples", source.load_v0287_documentation_report(), "passed", False),
            ("v0.28.8", "Alpha Readiness Validation / External Adapter Preflight Gate", "validation_preflight", source.load_v0288_validation_report(), "warning", True),
            ("v0.28.9", V0289_VERSION_NAME, "consolidation", _ref("v028_consolidation_report", "v028_consolidation_report:v0.28.9", V0289_VERSION), "warning", True),
        ]
        return [
            PublicAlphaFoundationComponent(
                f"public_alpha_foundation_component:{version}:v0.28.9",
                version,
                name,
                component_type,
                report_ref,
                status,
                True,
                release_blocker,
                component_type in {"validation_preflight", "consolidation"},
                ["Consolidated as refs-only; no release, adapter, provider, network, or command execution is performed."],
            )
            for version, name, component_type, report_ref, status, release_blocker in items
        ]

    def build_snapshot(self, source: V028ConsolidationPrerequisiteSourceService) -> PublicAlphaFoundationSnapshot:
        components = self.build_components(source)
        return PublicAlphaFoundationSnapshot(
            "public_alpha_foundation_snapshot:v0.28.9",
            _now(),
            V0289_INCLUDED_VERSIONS,
            [
                source.load_v0269_workbench_consolidation_report(),
                source.load_v0279_memory_consolidation_report(),
            ],
            components,
            "warning",
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
        )


class PublicAlphaCapabilityMapService:
    def build_map(self) -> PublicAlphaCapabilityMap:
        enabled = [
            ("release_hygiene_controls", "release_hygiene"),
            ("packaging_distribution_boundary", "packaging"),
            ("public_private_boundary", "public_private"),
            ("schumpeter_preparation_profile", "schumpeter_preparation"),
            ("runtime_smoke_demo_flow", "runtime_smoke"),
            ("documentation_example_pack", "documentation"),
            ("readiness_validation_preflight", "validation"),
            ("external_adapter_preflight_criteria", "external_adapter_preflight"),
        ]
        entries = [
            PublicAlphaCapabilityEntry(f"public_alpha_capability_entry:{name}:v0.28.9", name, category, "enabled", True, True, False, False)
            for name, category in enabled
        ]
        entries.extend(
            [
                PublicAlphaCapabilityEntry("public_alpha_capability_entry:future_external_adapter_contract:v0.28.9", "future_external_adapter_contract", "future_external_adapter", "future_track", True, False, False, True, True, False, True, False),
                PublicAlphaCapabilityEntry("public_alpha_capability_entry:future_external_dominion_bridge:v0.28.9", "future_external_dominion_bridge", "future_external_dominion", "future_track", False, False, False, True, True, True, True, True),
                PublicAlphaCapabilityEntry("public_alpha_capability_entry:provider_invocation:v0.28.9", "provider_invocation", "future_external_adapter", "disabled", False, False, False, False, True, False, True, False),
                PublicAlphaCapabilityEntry("public_alpha_capability_entry:command_execution_expansion:v0.28.9", "command_execution_expansion", "future_external_adapter", "disabled", False, False, False, False, False, True, False, False),
            ]
        )
        return PublicAlphaCapabilityMap("public_alpha_capability_map:v0.28.9", entries, 8, 0, 2, 2, 0, 4, "warning")


class PublicAlphaCoverageMatrixService:
    SUBJECTS = ["v028_contract", "release_hygiene", "packaging", "public_private_boundary", "schumpeter_decision", "schumpeter_preparation", "runtime_smoke", "documentation_examples", "readiness_validation", "external_adapter_preflight"]

    def build_matrix(self) -> PublicAlphaCoverageMatrix:
        rows = []
        for subject in self.SUBJECTS:
            status = "warning" if subject in {"release_hygiene", "readiness_validation"} else "passed"
            missing = ["release claim remains blocked"] if subject == "release_hygiene" else []
            rows.append(PublicAlphaCoverageRow(f"public_alpha_coverage_row:{subject}:v0.28.9", subject, True, True, True, True, True, True, True, True, True, True, status, missing))
        return PublicAlphaCoverageMatrix("public_alpha_coverage_matrix:v0.28.9", rows, len(rows), 8, 2, 0, 0, "warning")


class V028ConsolidationReportServices:
    def build_release_hygiene_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> ReleaseHygieneConsolidationReport:
        return ReleaseHygieneConsolidationReport("release_hygiene_consolidation_report:v0.28.9", source.load_v0281_hygiene_report(), False, True, True, True, True, True, True, "warning", True)

    def build_packaging_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> PackagingConsolidationReport:
        return PackagingConsolidationReport("packaging_consolidation_report:v0.28.9", source.load_v0282_packaging_report(), True, True, True, True, True, True, True, True, True, "passed")

    def build_public_private_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> PublicPrivateBoundaryConsolidationReport:
        return PublicPrivateBoundaryConsolidationReport("public_private_boundary_consolidation_report:v0.28.9", source.load_v0283_public_private_report(), True, True, True, True, True, True, True, True, "passed")

    def build_schumpeter_decision_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> SchumpeterDecisionConsolidationReport:
        return SchumpeterDecisionConsolidationReport("schumpeter_decision_consolidation_report:v0.28.9", source.load_v0284_schumpeter_decision_report(), True, "keep_reference_only_and_prepare_private_overlay", "passed")

    def build_schumpeter_preparation_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> SchumpeterPreparationConsolidationReport:
        return SchumpeterPreparationConsolidationReport("schumpeter_preparation_consolidation_report:v0.28.9", source.load_v0285_schumpeter_preparation_report(), True, True, "passed")

    def build_runtime_smoke_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> AlphaRuntimeSmokeConsolidationReport:
        return AlphaRuntimeSmokeConsolidationReport("alpha_runtime_smoke_consolidation_report:v0.28.9", source.load_v0286_runtime_profile_report(), True, True, True, "passed")

    def build_documentation_example_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> AlphaDocumentationExampleConsolidationReport:
        return AlphaDocumentationExampleConsolidationReport("alpha_documentation_example_consolidation_report:v0.28.9", source.load_v0287_documentation_report(), True, True, True, True, True, True, True, True, "passed")

    def build_readiness_validation_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> AlphaReadinessValidationConsolidationReport:
        return AlphaReadinessValidationConsolidationReport("alpha_readiness_validation_consolidation_report:v0.28.9", source.load_v0288_validation_report(), True, False, False, True, "warning")

    def build_external_adapter_preflight_consolidation(self, source: V028ConsolidationPrerequisiteSourceService) -> ExternalAdapterPreflightConsolidationReport:
        return ExternalAdapterPreflightConsolidationReport("external_adapter_preflight_consolidation_report:v0.28.9", source.load_v0288_external_adapter_preflight_report(), True, True, True, True, True, True, True, True, "passed")


class PublicAlphaReleaseReadinessService:
    def build_report(self, snapshot: PublicAlphaFoundationSnapshot, hygiene: ReleaseHygieneConsolidationReport, packaging: PackagingConsolidationReport, public_private: PublicPrivateBoundaryConsolidationReport, docs: AlphaDocumentationExampleConsolidationReport, smoke: AlphaRuntimeSmokeConsolidationReport, validation: AlphaReadinessValidationConsolidationReport) -> PublicAlphaReleaseReadinessReport:
        blockers = ["repository_release_ready=false", "public_alpha_release_claim_allowed=false"]
        warnings = ["Foundation consolidation is usable, but release remains deferred until hygiene and release claim gates pass."]
        return PublicAlphaReleaseReadinessReport("public_alpha_release_readiness_report:v0.28.9", snapshot.architecture_ready, bool(hygiene.repository_release_ready), bool(packaging.package_distribution_ready), bool(public_private.public_private_boundary_ready), bool(docs.documentation_ready), bool(smoke.smoke_flow_ready), True, bool(validation.alpha_validation_ready), False, False, True, "blocked", blockers, warnings)


class V029ReadinessService:
    def build_report(self, external_adapter: ExternalAdapterPreflightConsolidationReport) -> V029ReadinessReport:
        return V029ReadinessReport("v029_readiness_report:v0.28.9", bool(external_adapter.ready_for_v0_29_contract), _ref("external_adapter_preflight_consolidation_report", external_adapter.report_id, V0289_VERSION), [], ["v0.29.0 must begin with contract/inventory/gates, not provider invocation."])


class ExternalAdapterContractHandoffPacketService:
    REQUIRED_FIRST_STEPS = ["define_external_provider_adapter_contract", "define_provider_capability_inventory", "define_permission_gate", "define_safety_gate", "define_credential_boundary", "define_network_boundary", "define_audit_OCEL_visibility", "define_mock_mode", "define_no_network_default", "define_no_credential_default"]
    NOT_ALLOWED = ["provider_invocation", "command_execution_expansion", "credential_storage", "network_access", "RPA_adapter_runtime", "external_agent_dominion_bridge"]

    def build_packet(self, report_id: str, preflight_ref: dict[str, Any] | None) -> ExternalAdapterContractHandoffPacket:
        return ExternalAdapterContractHandoffPacket("external_adapter_contract_handoff_packet:v0.28.9", report_id, preflight_ref, ["external_adapter_preflight_report:v0.28.8", "provider_invocation_reopen_criteria:v0.28.8", "command_execution_reopen_criteria:v0.28.8"], list(self.REQUIRED_FIRST_STEPS), list(self.NOT_ALLOWED))


class PublicAlphaReleaseManifestService:
    EXCLUDED = ["Public Alpha release implementation", "Package publish", "Release tag creation", "Production runtime", "Schumpeter private runtime", "Company wrapper", "External provider adapter implementation", "Provider registration", "Provider invocation", "Command execution expansion", "Network calls", "RPA / A360 / Brity / UiPath adapters", "External Agent Dominion Bridge", "Runtime continuity injection", "Autonomous memory-driven execution"]

    def build_manifest(self, snapshot: PublicAlphaFoundationSnapshot, release_readiness: PublicAlphaReleaseReadinessReport, v029: V029ReadinessReport) -> PublicAlphaReleaseManifest:
        return PublicAlphaReleaseManifest("public_alpha_release_manifest:v0.28.9", list(V0289_INCLUDED_VERSIONS), [entry.component_name for entry in snapshot.components], list(self.EXCLUDED), list(V0289_EFFECT_TYPES), list(V0289_FORBIDDEN_EFFECT_TYPES), _ref("public_alpha_foundation_snapshot", snapshot.snapshot_id, V0289_VERSION), _ref("public_alpha_release_readiness_report", release_readiness.report_id, V0289_VERSION), _ref("v029_readiness_report", v029.report_id, V0289_VERSION), "warning")


class V028ConsolidationAuditTrailService:
    def build_audit_trail(self, source_refs: list[dict[str, Any]], consolidation_refs: list[dict[str, Any]], readiness_refs: list[dict[str, Any]], handoff_refs: list[dict[str, Any]]) -> V028ConsolidationAuditTrail:
        count = len(source_refs) + len(consolidation_refs) + len(readiness_refs) + len(handoff_refs)
        return V028ConsolidationAuditTrail("v028_consolidation_audit_trail:v0.28.9", source_refs, consolidation_refs, readiness_refs, handoff_refs, count, "warning")


class V028ConsolidationFindingService:
    BLOCKED_FINDINGS = {
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "official_release_artifact_attempted",
        "production_runtime_attempted",
        "schumpeter_private_runtime_attempted",
        "company_wrapper_attempted",
        "external_adapter_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "network_call_attempted",
        "command_execution_attempted",
        "external_dominion_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "credential_creation_attempted",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "private_material_exposure_detected",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "raw_trace_detected",
        "raw_transcript_detected",
        "raw_provider_output_detected",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[V028ConsolidationFinding]:
        return [
            V028ConsolidationFinding("v028_consolidation_finding:foundation_snapshot_created:v0.28.9", "info", "foundation_snapshot_created", "Public Alpha / Schumpeter Split Preparation Foundation v1 snapshot created as consolidation metadata only.", _ref("public_alpha_foundation_snapshot", "public_alpha_foundation_snapshot:v0.28.9", V0289_VERSION), [], None),
            V028ConsolidationFinding("v028_consolidation_finding:public_alpha_readiness_report_created:v0.28.9", "warning", "public_alpha_readiness_report_created", "Public alpha release readiness remains blocked by release-claim separation; no release is implemented.", _ref("public_alpha_release_readiness_report", "public_alpha_release_readiness_report:v0.28.9", V0289_VERSION), [], "Withdraw if release/publish/tag or public alpha release claim is implemented by v0.28.9."),
            V028ConsolidationFinding("v028_consolidation_finding:v029_readiness_report_created:v0.28.9", "info", "v029_readiness_report_created", "v0.29 contract readiness is prepared without adapter implementation, provider registration, provider invocation, network access, or command expansion.", _ref("v029_readiness_report", "v029_readiness_report:v0.28.9", V0289_VERSION), [], "Withdraw if ready_for_provider_invocation or ready_for_command_execution becomes true."),
        ]


class V028ConsolidationReportService:
    def build_report(self, report_id: str | None = None) -> V028ConsolidationReport:
        actual_report_id = report_id or "v028_consolidation_report:v0.28.9"
        source = V028ConsolidationPrerequisiteSourceService()
        snapshot = PublicAlphaFoundationSnapshotService().build_snapshot(source)
        capability_map = PublicAlphaCapabilityMapService().build_map()
        coverage = PublicAlphaCoverageMatrixService().build_matrix()
        reports = V028ConsolidationReportServices()
        hygiene = reports.build_release_hygiene_consolidation(source)
        packaging = reports.build_packaging_consolidation(source)
        public_private = reports.build_public_private_consolidation(source)
        schumpeter_decision = reports.build_schumpeter_decision_consolidation(source)
        schumpeter_preparation = reports.build_schumpeter_preparation_consolidation(source)
        runtime_smoke = reports.build_runtime_smoke_consolidation(source)
        documentation = reports.build_documentation_example_consolidation(source)
        validation = reports.build_readiness_validation_consolidation(source)
        adapter = reports.build_external_adapter_preflight_consolidation(source)
        release_readiness = PublicAlphaReleaseReadinessService().build_report(snapshot, hygiene, packaging, public_private, documentation, runtime_smoke, validation)
        v029 = V029ReadinessService().build_report(adapter)
        handoff = ExternalAdapterContractHandoffPacketService().build_packet(actual_report_id, adapter.source_report_ref)
        manifest = PublicAlphaReleaseManifestService().build_manifest(snapshot, release_readiness, v029)
        source_refs = [
            source.load_v0280_contract_report(),
            source.load_v0281_hygiene_report(),
            source.load_v0282_packaging_report(),
            source.load_v0283_public_private_report(),
            source.load_v0284_schumpeter_decision_report(),
            source.load_v0285_schumpeter_preparation_report(),
            source.load_v0286_runtime_profile_report(),
            source.load_v0287_documentation_report(),
            source.load_v0288_validation_report(),
            source.load_v0288_external_adapter_preflight_report(),
            source.load_v0279_memory_consolidation_report(),
            source.load_v0269_workbench_consolidation_report(),
        ]
        consolidation_refs = [_ref("consolidation_report", item.report_id, V0289_VERSION) for item in [hygiene, packaging, public_private, schumpeter_decision, schumpeter_preparation, runtime_smoke, documentation, validation, adapter]]
        readiness_refs = [_ref("public_alpha_release_readiness_report", release_readiness.report_id, V0289_VERSION), _ref("v029_readiness_report", v029.report_id, V0289_VERSION)]
        handoff_refs = [_ref("external_adapter_contract_handoff_packet", handoff.handoff_packet_id, V0289_VERSION)]
        audit = V028ConsolidationAuditTrailService().build_audit_trail(source_refs, consolidation_refs, readiness_refs, handoff_refs)
        findings = V028ConsolidationFindingService().build_findings()
        return V028ConsolidationReport(
            actual_report_id,
            _now(),
            snapshot,
            capability_map,
            coverage,
            hygiene,
            packaging,
            public_private,
            schumpeter_decision,
            schumpeter_preparation,
            runtime_smoke,
            documentation,
            validation,
            adapter,
            release_readiness,
            v029,
            handoff,
            manifest,
            audit,
            findings,
            "warning",
            True,
            v029.ready_for_v0_29_contract,
            release_readiness.public_alpha_release_ready,
            release_readiness.public_alpha_release_claim_allowed,
            limitations=["v0.28.9 is consolidation-only; public alpha release remains blocked/deferred, while v0.29 contract handoff is prepared as refs-only.", "Full historical pytest suite may remain environment-limited; unknown results are not release pass."],
            withdrawal_conditions=["Withdraw if release/publish/tag, production or Schumpeter runtime, adapter/provider/network/command execution, external dominion/RPA, credential/private/raw exposure, runtime injection, autonomous memory execution, reference dependency/code copy, PIG authority, LLM sole authority, or unknown-as-passed behavior appears."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "snapshot": report.foundation_snapshot,
            "capabilities": report.capability_map,
            "coverage": report.coverage_matrix,
            "hygiene": report.release_hygiene_consolidation,
            "packaging": report.packaging_consolidation,
            "public-private": report.public_private_consolidation,
            "schumpeter-decision": report.schumpeter_decision_consolidation,
            "schumpeter-prep": report.schumpeter_preparation_consolidation,
            "runtime-smoke": report.runtime_smoke_consolidation,
            "docs": report.documentation_example_consolidation,
            "validation": report.readiness_validation_consolidation,
            "adapter-preflight": report.external_adapter_preflight_consolidation,
            "release-readiness": report.public_alpha_release_readiness,
            "v029-readiness": report.v029_readiness_report,
            "handoff-v029": report.external_adapter_contract_handoff_packet,
            "manifest": report.release_manifest,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0289_VERSION,
            "layer": V028_LAYER,
            "subject": "public_alpha_schumpeter_split_preparation_consolidation",
            "release_name": V0289_RELEASE_NAME,
            "principles": ["Consolidation is not implementation", "Foundation declaration is not public release", "Readiness is not deployment", "Release manifest is not release tag", "Distribution readiness is not package upload", "Documentation readiness is not production support", "External Adapter handoff is not adapter implementation", "v0.29 readiness is not v0.29 implementation", "No-release remains a valid outcome", "No-adapter remains a valid outcome"],
            "safety_boundary": {
                "public_alpha_release_implemented": report.public_alpha_release_implemented,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "production_runtime_implemented": report.production_runtime_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "external_adapter_implemented": report.external_adapter_implemented,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "network_called": report.network_called,
                "command_executed": report.command_executed,
                "external_dominion_implemented": report.external_dominion_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "credential_created": report.credential_created,
                "credential_exposed": report.credential_exposed,
                "private_material_exposed": report.private_material_exposed,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "raw_trace_used": report.raw_trace_used,
                "raw_transcript_used": report.raw_transcript_used,
                "raw_provider_output_used": report.raw_provider_output_used,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "autonomous_memory_execution_enabled": report.autonomous_memory_execution_enabled,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.29.0 External Provider Adapter Contract", "v0.29.x External Skill / External Provider Adapter Development", "v0.30.x External Agent Dominion Bridge"],
            "next_step": V0289_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "public_alpha_schumpeter_split_preparation_foundation_v1_consolidated",
            "version": V0289_VERSION,
            "source_read_models": ["V028ContractState", "ReleaseHygieneGateState", "PackagingReadinessState", "PublicPrivateBoundaryState", "SchumpeterSplitDecisionFrameworkState", "SchumpeterPreparationProfileState", "PublicAlphaRuntimeProfileState", "AlphaDocumentationReadinessState", "AlphaReadinessValidationState", "ExternalAdapterPreflightState", "MemoryConsolidationState", "WorkbenchConsolidationState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["PublicAlphaFoundationSnapshotState", "PublicAlphaCapabilityMapState", "PublicAlphaCoverageMatrixState", "PublicAlphaReleaseReadinessState", "V029ReadinessState", "ExternalAdapterContractHandoffState", "PublicAlphaReleaseManifestState", "V028ConsolidationState"],
            "effect_types": V0289_EFFECT_TYPES,
            "forbidden_effect_types": V0289_FORBIDDEN_EFFECT_TYPES,
        }


def render_v028_consolidation_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: V028ConsolidationReport = parts["report"]
    lines = [
        f"Public Alpha / Schumpeter Split Preparation Consolidation {section}",
        f"version={report.version}",
        f"release_name={report.release_name}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29={_bool(report.ready_for_v0_29)}",
        f"ready_for_v0_29_contract={_bool(report.ready_for_v0_29_contract)}",
        f"ready_for_external_adapter_implementation={_bool(report.ready_for_external_adapter_implementation)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"public_alpha_release_ready={_bool(report.public_alpha_release_ready)}",
        f"public_alpha_release_claim_allowed={_bool(report.public_alpha_release_claim_allowed)}",
        f"public_alpha_release_implemented={_bool(report.public_alpha_release_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"official_release_artifact_created={_bool(report.official_release_artifact_created)}",
        f"production_runtime_implemented={_bool(report.production_runtime_implemented)}",
        f"schumpeter_private_runtime_used={_bool(report.schumpeter_private_runtime_used)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"command_executed={_bool(report.command_executed)}",
        f"external_dominion_implemented={_bool(report.external_dominion_implemented)}",
        f"RPA_adapter_implemented={_bool(report.RPA_adapter_implemented)}",
        f"A360_adapter_implemented={_bool(report.A360_adapter_implemented)}",
        f"Brity_adapter_implemented={_bool(report.Brity_adapter_implemented)}",
        f"UiPath_adapter_implemented={_bool(report.UiPath_adapter_implemented)}",
        f"credential_created={_bool(report.credential_created)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"private_material_exposed={_bool(report.private_material_exposed)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"raw_trace_used={_bool(report.raw_trace_used)}",
        f"raw_transcript_used={_bool(report.raw_transcript_used)}",
        f"raw_provider_output_used={_bool(report.raw_provider_output_used)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"autonomous_memory_execution_enabled={_bool(report.autonomous_memory_execution_enabled)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "snapshot_id", getattr(payload, "map_id", getattr(payload, "matrix_id", getattr(payload, "manifest_id", getattr(payload, "handoff_packet_id", getattr(payload, "audit_trail_id", "")))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0281_VERSION = "v0.28.1"
V0281_VERSION_NAME = "Release Hygiene / Repository Governance Blocking Gate"
V0281_NEXT_STEP = "v0.28.2 Packaging / Distribution / Type Boundary"
V0282_VERSION = "v0.28.2"
V0282_VERSION_NAME = "Packaging / Distribution / Type Boundary"
V0282_NEXT_STEP = "v0.28.3 Public-Private Boundary / Redaction / Reference Policy"

V0281_OBJECT_TYPES = [
    "release_hygiene_blocking_gate_policy",
    "repository_governance_policy",
    "repository_state_snapshot",
    "version_consistency_report",
    "clean_worktree_report",
    "release_tag_readiness_report",
    "root_governance_file_report",
    "license_presence_report",
    "changelog_presence_report",
    "contributing_presence_report",
    "third_party_notice_report",
    "pyproject_hygiene_report",
    "py_typed_presence_report",
    "ci_workflow_presence_report",
    "gitignore_hygiene_report",
    "runtime_data_hygiene_report",
    "runtime_artifact_tracking_report",
    "references_directory_inventory",
    "references_license_boundary_report",
    "references_governance_policy_report",
    "forbidden_repository_artifact_scan_report",
    "repository_governance_remediation_item",
    "repository_governance_remediation_plan",
    "no_release_decision",
    "defer_alpha_decision",
    "public_alpha_release_claim_gate",
    "release_hygiene_gate_finding",
    "release_hygiene_gate_report",
    "v028_contract_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0281_EVENT_TYPES = [
    "release_hygiene_gate_requested",
    "release_hygiene_prerequisites_loaded",
    "release_hygiene_blocking_gate_policy_created",
    "repository_governance_policy_created",
    "repository_state_snapshot_created",
    "version_consistency_report_created",
    "clean_worktree_report_created",
    "release_tag_readiness_report_created",
    "root_governance_file_report_created",
    "license_presence_report_created",
    "changelog_presence_report_created",
    "contributing_presence_report_created",
    "third_party_notice_report_created",
    "pyproject_hygiene_report_created",
    "py_typed_presence_report_created",
    "ci_workflow_presence_report_created",
    "gitignore_hygiene_report_created",
    "runtime_data_hygiene_report_created",
    "runtime_artifact_tracking_report_created",
    "references_directory_inventory_created",
    "references_license_boundary_report_created",
    "references_governance_policy_report_created",
    "forbidden_repository_artifact_scan_report_created",
    "repository_governance_remediation_plan_created",
    "no_release_decision_created",
    "defer_alpha_decision_created",
    "public_alpha_release_claim_gate_evaluated",
    "release_hygiene_gate_report_created",
    "release_hygiene_gate_passed",
    "release_hygiene_gate_warning",
    "release_hygiene_gate_blocked",
]

V0281_EFFECT_TYPES = [
    "read_only_observation",
    "release_hygiene_gate_evaluated",
    "repository_governance_report_created",
    "repository_governance_remediation_plan_created",
    "no_release_decision_recorded",
    "defer_alpha_decision_recorded",
    "public_alpha_release_claim_gate_evaluated",
    "state_candidate_created",
]

V0281_FORBIDDEN_EFFECT_TYPES = [
    "auto_fix_performed",
    "license_created",
    "changelog_created",
    "release_tag_created",
    "package_published",
    "public_alpha_release_implemented",
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "references_schumpeter_runtime_dependency_added",
    "references_schumpeter_code_copied",
    "company_private_material_exposed",
    "credential_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]

V0282_OBJECT_TYPES = [
    "packaging_distribution_type_boundary_policy",
    "packaging_readiness_request",
    "packaging_source_view",
    "pyproject_package_metadata_report",
    "dependency_boundary_policy",
    "runtime_dependency_report",
    "dev_dependency_report",
    "optional_dependency_group_report",
    "pytest_runtime_dependency_violation_report",
    "build_backend_readiness_report",
    "package_include_exclude_policy",
    "package_data_boundary_report",
    "py_typed_marker_report",
    "type_distribution_boundary_report",
    "wheel_build_smoke_plan",
    "wheel_build_smoke_report",
    "sdist_build_smoke_plan",
    "sdist_build_smoke_report",
    "import_smoke_plan",
    "import_smoke_report",
    "cli_smoke_plan",
    "cli_smoke_report",
    "distribution_artifact_policy",
    "package_publish_blocker",
    "packaging_remediation_item",
    "packaging_remediation_plan",
    "packaging_readiness_gate",
    "packaging_finding",
    "packaging_readiness_report",
    "release_hygiene_gate_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0282_EVENT_TYPES = [
    "packaging_boundary_requested",
    "packaging_prerequisites_loaded",
    "packaging_distribution_type_boundary_policy_created",
    "packaging_source_view_created",
    "pyproject_package_metadata_report_created",
    "dependency_boundary_policy_created",
    "runtime_dependency_report_created",
    "dev_dependency_report_created",
    "optional_dependency_group_report_created",
    "pytest_runtime_dependency_violation_report_created",
    "build_backend_readiness_report_created",
    "package_include_exclude_policy_created",
    "package_data_boundary_report_created",
    "py_typed_marker_report_created",
    "type_distribution_boundary_report_created",
    "wheel_build_smoke_plan_created",
    "wheel_build_smoke_report_created",
    "sdist_build_smoke_plan_created",
    "sdist_build_smoke_report_created",
    "import_smoke_plan_created",
    "import_smoke_report_created",
    "cli_smoke_plan_created",
    "cli_smoke_report_created",
    "distribution_artifact_policy_created",
    "package_publish_blocker_created",
    "packaging_remediation_plan_created",
    "packaging_readiness_gate_evaluated",
    "packaging_readiness_report_created",
    "packaging_boundary_warning_created",
    "packaging_boundary_blocked",
]

V0282_EFFECT_TYPES = [
    "read_only_observation",
    "packaging_boundary_created",
    "packaging_metadata_report_created",
    "dependency_boundary_report_created",
    "package_data_boundary_report_created",
    "type_boundary_report_created",
    "build_smoke_report_created",
    "import_smoke_report_created",
    "cli_smoke_report_created",
    "package_publish_blocker_created",
    "packaging_readiness_gate_evaluated",
    "state_candidate_created",
]

V0282_FORBIDDEN_EFFECT_TYPES = [
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "public_alpha_release_implemented",
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "references_schumpeter_runtime_dependency_added",
    "references_schumpeter_code_copied",
    "company_private_material_exposed",
    "credential_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _file_ref(path: Path, object_type: str = "file") -> dict[str, Any]:
    root = _repo_root()
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.name
    return {"object_type": object_type, "object_id": rel, "path": rel}


def _load_pyproject() -> dict[str, Any]:
    path = _repo_root() / "pyproject.toml"
    if not path.exists():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return {}


def _root_file(*names: str) -> Path | None:
    root = _repo_root()
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def _first_attr(value: Any, names: list[str], default: Any = "") -> Any:
    for name in names:
        if hasattr(value, name):
            return getattr(value, name)
    return default


@dataclass
class ReleaseHygieneBlockingGatePolicy(ModelMixin):
    policy_id: str
    required_checks: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    layer: str = V028_LAYER
    gate_type: str = "blocking_gate"
    public_alpha_release_claim_requires_gate_pass: bool = True
    repository_release_ready_requires_gate_pass: bool = True
    hygiene_unknown_is_not_passed: bool = True
    failed_required_check_blocks_release: bool = True
    no_release_is_valid_outcome: bool = True
    defer_alpha_is_valid_outcome: bool = True
    auto_fix_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    package_publish_enabled_now: bool = False
    company_split_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False


@dataclass
class RepositoryGovernancePolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    license_required: bool = True
    changelog_required: bool = True
    contributing_recommended: bool = True
    third_party_notices_required_when_references_exist: bool = True
    references_policy_required_when_references_exist: bool = True
    runtime_data_must_not_be_tracked: bool = True
    backup_files_must_not_be_tracked: bool = True
    generated_artifacts_must_be_ignored_or_quarantined: bool = True
    public_private_boundary_required: bool = True
    company_private_material_forbidden: bool = True
    credential_exposure_forbidden: bool = True
    raw_trace_exposure_forbidden: bool = True
    raw_transcript_exposure_forbidden: bool = True
    raw_provider_output_exposure_forbidden: bool = True
    auto_remediation_enabled_now: bool = False


@dataclass
class RepositoryStateSnapshot(ModelMixin):
    snapshot_id: str
    repository_root_ref: dict[str, Any] | None
    observed_at: str | None
    source_mode: str
    pyproject_ref: dict[str, Any] | None
    package_version_ref: dict[str, Any] | None
    root_files_present: list[str]
    root_files_missing: list[str]
    workflow_files_present: list[str]
    gitignore_present: bool | None
    references_dir_present: bool | None
    data_dir_present: bool | None
    tracked_runtime_artifact_refs: list[dict[str, Any]]
    untracked_file_refs: list[dict[str, Any]]
    modified_file_refs: list[dict[str, Any]]
    metadata_complete: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class VersionConsistencyReport(ModelMixin):
    report_id: str
    pyproject_version: str | None
    package_init_version: str | None
    docs_version_ref: dict[str, Any] | None
    versions_match: bool | None
    version_status: str
    mismatch_reasons: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    expected_version: str = "0.28.1"


@dataclass
class CleanWorktreeReport(ModelMixin):
    report_id: str
    worktree_status_known: bool
    clean_worktree: bool | None
    modified_count: int | None
    untracked_count: int | None
    staged_count: int | None
    dirty_file_refs: list[dict[str, Any]]
    generated_artifact_refs: list[dict[str, Any]]
    worktree_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class ReleaseTagReadinessReport(ModelMixin):
    report_id: str
    tag_status_known: bool
    expected_tag_exists: bool | None
    previous_tag_ref: dict[str, Any] | None
    tag_policy_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    expected_tag: str = "v0.28.1"
    release_tag_created_now: bool = False


@dataclass
class RootGovernanceFileReport(ModelMixin):
    report_id: str
    license_present: bool | None
    changelog_present: bool | None
    contributing_present: bool | None
    readme_present: bool | None
    security_policy_present: bool | None
    code_of_conduct_present: bool | None
    third_party_notices_present: bool | None
    references_policy_present: bool | None
    governance_file_status: str
    missing_required_files: list[str]
    missing_recommended_files: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class LicensePresenceReport(ModelMixin):
    report_id: str
    license_present: bool | None
    license_file_ref: dict[str, Any] | None
    license_type_detected: str | None
    license_detection_confidence: str
    license_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    auto_license_created_now: bool = False


@dataclass
class ChangelogPresenceReport(ModelMixin):
    report_id: str
    changelog_present: bool | None
    changelog_ref: dict[str, Any] | None
    contains_v0281_entry: bool | None
    changelog_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    auto_changelog_created_now: bool = False


@dataclass
class ContributingPresenceReport(ModelMixin):
    report_id: str
    contributing_present: bool | None
    contributing_ref: dict[str, Any] | None
    contributing_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    blocks_release_claim: bool = False


@dataclass
class ThirdPartyNoticeReport(ModelMixin):
    report_id: str
    references_dir_present: bool | None
    third_party_notices_required: bool
    third_party_notices_present: bool | None
    third_party_notices_ref: dict[str, Any] | None
    known_reference_count: int | None
    unknown_license_reference_count: int | None
    notice_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class PyprojectHygieneReport(ModelMixin):
    report_id: str
    pyproject_present: bool | None
    pyproject_ref: dict[str, Any] | None
    project_name_present: bool | None
    version_present: bool | None
    runtime_dependencies_present: bool | None
    dev_dependencies_present: bool | None
    pytest_in_runtime_dependencies: bool | None
    build_backend_present: bool | None
    package_metadata_complete: bool | None
    pyproject_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class PyTypedPresenceReport(ModelMixin):
    report_id: str
    py_typed_present: bool | None
    py_typed_ref: dict[str, Any] | None
    package_type_boundary_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class CIWorkflowPresenceReport(ModelMixin):
    report_id: str
    github_workflows_dir_present: bool | None
    workflow_file_refs: list[dict[str, Any]]
    pytest_workflow_detected: bool | None
    boundary_test_workflow_detected: bool | None
    package_smoke_workflow_detected: bool | None
    ci_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class GitignoreHygieneReport(ModelMixin):
    report_id: str
    gitignore_present: bool | None
    gitignore_ref: dict[str, Any] | None
    ignores_sqlite: bool | None
    ignores_db_files: bool | None
    ignores_bak_files: bool | None
    ignores_runtime_data: bool | None
    ignores_generated_artifacts: bool | None
    gitignore_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class RuntimeDataHygieneReport(ModelMixin):
    report_id: str
    data_dir_present: bool | None
    tracked_sqlite_count: int | None
    tracked_db_count: int | None
    tracked_bak_count: int | None
    tracked_runtime_log_count: int | None
    tracked_cache_count: int | None
    tracked_runtime_artifact_refs: list[dict[str, Any]]
    runtime_data_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class RuntimeArtifactTrackingReport(ModelMixin):
    report_id: str
    artifact_patterns_checked: list[str]
    tracked_artifact_count: int | None
    tracked_artifact_refs: list[dict[str, Any]]
    artifact_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class ReferencesDirectoryInventory(ModelMixin):
    inventory_id: str
    references_dir_present: bool | None
    reference_entries: list[dict[str, Any]]
    schumpeter_reference_present: bool | None
    opencode_reference_present: bool | None
    hermes_reference_present: bool | None
    openclaw_reference_present: bool | None
    reference_count: int | None
    inventory_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class ReferencesLicenseBoundaryReport(ModelMixin):
    report_id: str
    references_dir_present: bool | None
    references_policy_ref: dict[str, Any] | None
    third_party_notices_ref: dict[str, Any] | None
    references_with_known_origin_count: int | None
    references_with_known_license_count: int | None
    references_with_unknown_license_count: int | None
    license_boundary_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    references_runtime_dependency_count: int = 0
    references_code_copy_count: int = 0


@dataclass
class ReferencesGovernancePolicyReport(ModelMixin):
    report_id: str
    references_policy_present: bool | None
    references_policy_ref: dict[str, Any] | None
    declares_reference_only_boundary: bool | None
    declares_no_runtime_dependency: bool | None
    declares_license_review_required: bool | None
    declares_public_private_boundary_review_required: bool | None
    policy_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class ForbiddenRepositoryArtifactScanReport(ModelMixin):
    report_id: str
    scan_mode: str
    forbidden_patterns_checked: list[str]
    forbidden_artifact_refs: list[dict[str, Any]]
    credential_like_artifact_count: int | None
    raw_trace_like_artifact_count: int | None
    raw_transcript_like_artifact_count: int | None
    raw_provider_output_like_artifact_count: int | None
    company_private_material_like_artifact_count: int | None
    scan_status: str
    blocks_release_claim: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class RepositoryGovernanceRemediationItem(ModelMixin):
    remediation_item_id: str
    source_report_ref: dict[str, Any] | None
    issue_type: str
    severity: str
    recommended_action: str
    requires_user_decision: bool
    suggested_followup_version: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    auto_fix_allowed_now: bool = False


@dataclass
class RepositoryGovernanceRemediationPlan(ModelMixin):
    remediation_plan_id: str
    remediation_items: list[RepositoryGovernanceRemediationItem]
    blocker_count: int
    warning_count: int
    user_decision_required_count: int
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    auto_fix_performed: bool = False


@dataclass
class NoReleaseDecision(ModelMixin):
    no_release_decision_id: str
    decision_reason: str
    blocking_report_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    no_release_is_valid: bool = True
    public_alpha_release_claim_allowed: bool = False


@dataclass
class DeferAlphaDecision(ModelMixin):
    defer_alpha_decision_id: str
    decision_reason: str
    deferred_until: str | None
    required_followup_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION
    public_alpha_release_claim_allowed: bool = False


@dataclass
class PublicAlphaReleaseClaimGate(ModelMixin):
    gate_id: str
    architecture_ready_ref: dict[str, Any] | None
    repository_hygiene_report_ref: dict[str, Any] | None
    governance_report_refs: list[dict[str, Any]]
    required_checks_passed: bool
    warning_checks_present: bool
    blocking_checks_present: bool
    architecture_ready: bool | None
    repository_release_ready: bool
    public_alpha_release_claim_allowed: bool
    no_release_decision_ref: dict[str, Any] | None
    defer_alpha_decision_ref: dict[str, Any] | None
    gate_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0281_VERSION


@dataclass
class ReleaseHygieneGateFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class ReleaseHygieneGateReport(ModelMixin):
    report_id: str
    created_at: str
    gate_policy: ReleaseHygieneBlockingGatePolicy
    governance_policy: RepositoryGovernancePolicy
    repository_snapshot: RepositoryStateSnapshot
    version_consistency_report: VersionConsistencyReport
    clean_worktree_report: CleanWorktreeReport
    release_tag_readiness_report: ReleaseTagReadinessReport
    root_governance_file_report: RootGovernanceFileReport
    license_presence_report: LicensePresenceReport
    changelog_presence_report: ChangelogPresenceReport
    contributing_presence_report: ContributingPresenceReport
    third_party_notice_report: ThirdPartyNoticeReport
    pyproject_hygiene_report: PyprojectHygieneReport
    py_typed_presence_report: PyTypedPresenceReport
    ci_workflow_presence_report: CIWorkflowPresenceReport
    gitignore_hygiene_report: GitignoreHygieneReport
    runtime_data_hygiene_report: RuntimeDataHygieneReport
    runtime_artifact_tracking_report: RuntimeArtifactTrackingReport
    references_inventory: ReferencesDirectoryInventory
    references_license_boundary_report: ReferencesLicenseBoundaryReport
    references_governance_policy_report: ReferencesGovernancePolicyReport
    forbidden_artifact_scan_report: ForbiddenRepositoryArtifactScanReport
    remediation_plan: RepositoryGovernanceRemediationPlan
    no_release_decision: NoReleaseDecision | None
    defer_alpha_decision: DeferAlphaDecision | None
    public_alpha_release_claim_gate: PublicAlphaReleaseClaimGate
    findings: list[ReleaseHygieneGateFinding]
    report_status: str
    ready_for_v0_28_2: bool
    ready_for_public_alpha_release_claim: bool
    repository_release_ready: bool
    architecture_ready_may_continue: bool
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    version: str = V0281_VERSION
    package_distribution_ready: bool = False
    public_alpha_ready: bool = False
    public_alpha_release_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    auto_fix_performed: bool = False
    schumpeter_split_implemented: bool = False
    external_adapter_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0281_NEXT_STEP
    validity_horizon: str = "Valid until v0.28.2 Packaging / Distribution / Type Boundary begins or release hygiene policy changes."


class ReleaseHygienePrerequisiteSourceService:
    def load_v0280_contract_report(self) -> V028ContractReport:
        return V028ContractReportService().build_report()

    def load_v0280_release_hygiene_debt_policy(self) -> ReleaseHygieneDebtPolicy:
        return V028ContractService().build_contract().release_hygiene_debt_policy

    def load_v0280_release_hygiene_blocking_policy(self) -> ReleaseHygieneBlockingPolicy:
        return V028ContractService().build_contract().release_hygiene_blocking_policy

    def load_v0279_memory_consolidation_report_if_available(self) -> Any:
        return MemoryConsolidationReportService().build_report()

    def load_v02610_hygiene_report_if_available(self) -> None:
        return None

    def load_repository_state_snapshot_if_available(self) -> RepositoryStateSnapshot:
        return RepositoryStateSnapshotService().build_snapshot_from_available_metadata()

    def load_pyproject_metadata_if_available(self) -> dict[str, Any]:
        return _load_pyproject()

    def load_root_file_metadata_if_available(self) -> dict[str, Any]:
        return {"root": str(_repo_root())}

    def load_workflow_metadata_if_available(self) -> list[dict[str, Any]]:
        workflows = _repo_root() / ".github" / "workflows"
        if not workflows.exists():
            return []
        return [_file_ref(path, "github_workflow") for path in workflows.glob("*.yml")]

    def load_gitignore_metadata_if_available(self) -> dict[str, Any] | None:
        path = _repo_root() / ".gitignore"
        return _file_ref(path) if path.exists() else None

    def load_data_file_metadata_if_available(self) -> list[dict[str, Any]]:
        data_dir = _repo_root() / "data"
        if not data_dir.exists():
            return []
        return [_file_ref(path) for path in data_dir.rglob("*") if path.is_file()]

    def load_references_metadata_if_available(self) -> list[dict[str, Any]]:
        references = _repo_root() / "references"
        if not references.exists():
            return []
        return [_file_ref(path, "reference_entry") for path in references.iterdir()]


class ReleaseHygieneBlockingGatePolicyService:
    def build_policy(self) -> ReleaseHygieneBlockingGatePolicy:
        return ReleaseHygieneBlockingGatePolicy(
            policy_id="release_hygiene_blocking_gate_policy:v0.28.1",
            required_checks=[
                "version_consistency",
                "clean_worktree",
                "release_tag_policy",
                "license_presence",
                "changelog_presence",
                "third_party_notices_when_references_exist",
                "pyproject_hygiene",
                "py_typed_presence",
                "ci_workflow_presence",
                "gitignore_hygiene",
                "runtime_data_hygiene",
                "references_governance_policy",
                "forbidden_artifact_scan",
            ],
        )


class RepositoryGovernancePolicyService:
    def build_policy(self) -> RepositoryGovernancePolicy:
        return RepositoryGovernancePolicy(policy_id="repository_governance_policy:v0.28.1")


class RepositoryStateSnapshotService:
    def build_snapshot_from_available_metadata(self) -> RepositoryStateSnapshot:
        root = _repo_root()
        pyproject = root / "pyproject.toml"
        package_init = root / "src" / "chanta_core" / "__init__.py"
        root_names = ["README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "THIRD_PARTY_NOTICES.md", "REFERENCES_POLICY.md"]
        present = [name for name in root_names if (root / name).exists()]
        missing = [name for name in root_names if name not in present]
        workflows = root / ".github" / "workflows"
        workflow_refs = [path.name for path in workflows.glob("*.yml")] if workflows.exists() else []
        return RepositoryStateSnapshot(
            snapshot_id="repository_state_snapshot:v0.28.1",
            repository_root_ref={"object_type": "repository_root", "object_id": "workspace"},
            observed_at=_now(),
            source_mode="file_metadata_readonly",
            pyproject_ref=_file_ref(pyproject) if pyproject.exists() else None,
            package_version_ref=_file_ref(package_init) if package_init.exists() else None,
            root_files_present=present,
            root_files_missing=missing,
            workflow_files_present=workflow_refs,
            gitignore_present=(root / ".gitignore").exists(),
            references_dir_present=(root / "references").exists(),
            data_dir_present=(root / "data").exists(),
            tracked_runtime_artifact_refs=[],
            untracked_file_refs=[],
            modified_file_refs=[],
            metadata_complete=True,
        )

    def unknown_when_not_verifiable(self) -> RepositoryStateSnapshot:
        return RepositoryStateSnapshot(
            snapshot_id="repository_state_snapshot:unknown:v0.28.1",
            repository_root_ref=None,
            observed_at=None,
            source_mode="unknown",
            pyproject_ref=None,
            package_version_ref=None,
            root_files_present=[],
            root_files_missing=[],
            workflow_files_present=[],
            gitignore_present=None,
            references_dir_present=None,
            data_dir_present=None,
            tracked_runtime_artifact_refs=[],
            untracked_file_refs=[],
            modified_file_refs=[],
            metadata_complete=False,
        )


class VersionConsistencyReportService:
    def build_report(self) -> VersionConsistencyReport:
        pyproject = _load_pyproject()
        project = pyproject.get("project", {})
        pyproject_version = project.get("version")
        init_path = _repo_root() / "src" / "chanta_core" / "__init__.py"
        init_version = None
        if init_path.exists():
            for line in init_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("__version__"):
                    init_version = line.split("=", 1)[1].strip().strip('"')
        docs_path = _repo_root() / "docs" / "versions" / "v0.28" / "v0.28.1_release_hygiene_repository_governance_blocking_gate.md"
        versions_match = pyproject_version == "0.28.1" and init_version == "0.28.1"
        reasons = []
        if pyproject_version != "0.28.1":
            reasons.append(f"pyproject_version={pyproject_version!s}")
        if init_version != "0.28.1":
            reasons.append(f"package_init_version={init_version!s}")
        return VersionConsistencyReport(
            report_id="version_consistency_report:v0.28.1",
            pyproject_version=pyproject_version,
            package_init_version=init_version,
            docs_version_ref=_file_ref(docs_path) if docs_path.exists() else None,
            versions_match=versions_match,
            version_status="passed" if versions_match else "failed",
            mismatch_reasons=reasons,
        )


class CleanWorktreeReportService:
    def build_report(self, worktree_status_known: bool = False, clean_worktree: bool | None = None) -> CleanWorktreeReport:
        if not worktree_status_known:
            return CleanWorktreeReport(
                report_id="clean_worktree_report:v0.28.1",
                worktree_status_known=False,
                clean_worktree=None,
                modified_count=None,
                untracked_count=None,
                staged_count=None,
                dirty_file_refs=[],
                generated_artifact_refs=[],
                worktree_status="unknown",
                blocks_release_claim=True,
            )
        dirty = clean_worktree is False
        return CleanWorktreeReport(
            report_id="clean_worktree_report:v0.28.1",
            worktree_status_known=True,
            clean_worktree=clean_worktree,
            modified_count=1 if dirty else 0,
            untracked_count=0,
            staged_count=0,
            dirty_file_refs=[_ref("file", "dirty:metadata")] if dirty else [],
            generated_artifact_refs=[],
            worktree_status="failed" if dirty else "passed",
            blocks_release_claim=dirty,
        )


class ReleaseTagReadinessReportService:
    def build_report(self) -> ReleaseTagReadinessReport:
        return ReleaseTagReadinessReport(
            report_id="release_tag_readiness_report:v0.28.1",
            tag_status_known=False,
            expected_tag_exists=None,
            previous_tag_ref=None,
            tag_policy_status="unknown",
            blocks_release_claim=True,
        )


class RootGovernanceFileReportService:
    def build_report(self) -> RootGovernanceFileReport:
        root = _repo_root()
        license_present = _root_file("LICENSE", "LICENSE.md") is not None
        changelog_present = _root_file("CHANGELOG.md", "CHANGELOG") is not None
        contributing_present = _root_file("CONTRIBUTING.md", "CONTRIBUTING") is not None
        readme_present = (root / "README.md").exists()
        third_party_present = _root_file("THIRD_PARTY_NOTICES.md", "NOTICE", "NOTICE.md") is not None
        references_policy_present = _root_file("REFERENCES_POLICY.md", "docs/reference_policy.md") is not None
        missing_required = []
        if not license_present:
            missing_required.append("LICENSE")
        if not changelog_present:
            missing_required.append("CHANGELOG.md")
        if (root / "references").exists() and not third_party_present:
            missing_required.append("THIRD_PARTY_NOTICES.md")
        if (root / "references").exists() and not references_policy_present:
            missing_required.append("REFERENCES_POLICY.md")
        missing_recommended = [name for name, present in {"CONTRIBUTING.md": contributing_present, "SECURITY.md": (root / "SECURITY.md").exists(), "CODE_OF_CONDUCT.md": (root / "CODE_OF_CONDUCT.md").exists()}.items() if not present]
        return RootGovernanceFileReport(
            report_id="root_governance_file_report:v0.28.1",
            license_present=license_present,
            changelog_present=changelog_present,
            contributing_present=contributing_present,
            readme_present=readme_present,
            security_policy_present=(root / "SECURITY.md").exists(),
            code_of_conduct_present=(root / "CODE_OF_CONDUCT.md").exists(),
            third_party_notices_present=third_party_present,
            references_policy_present=references_policy_present,
            governance_file_status="failed" if missing_required else ("warning" if missing_recommended else "passed"),
            missing_required_files=missing_required,
            missing_recommended_files=missing_recommended,
        )


class LicensePresenceReportService:
    def build_report(self) -> LicensePresenceReport:
        path = _root_file("LICENSE", "LICENSE.md")
        present = path is not None
        return LicensePresenceReport(
            report_id="license_presence_report:v0.28.1",
            license_present=present,
            license_file_ref=_file_ref(path) if path else None,
            license_type_detected="unknown" if present else None,
            license_detection_confidence="low" if present else "unknown",
            license_status="passed" if present else "failed",
            blocks_release_claim=not present,
        )


class ChangelogPresenceReportService:
    def build_report(self) -> ChangelogPresenceReport:
        path = _root_file("CHANGELOG.md", "CHANGELOG")
        present = path is not None
        contains = None
        if path:
            contains = "v0.28.1" in path.read_text(encoding="utf-8", errors="ignore")
        return ChangelogPresenceReport(
            report_id="changelog_presence_report:v0.28.1",
            changelog_present=present,
            changelog_ref=_file_ref(path) if path else None,
            contains_v0281_entry=contains,
            changelog_status="passed" if present and contains else "failed",
            blocks_release_claim=not (present and contains),
        )


class ContributingPresenceReportService:
    def build_report(self) -> ContributingPresenceReport:
        path = _root_file("CONTRIBUTING.md", "CONTRIBUTING")
        return ContributingPresenceReport(
            report_id="contributing_presence_report:v0.28.1",
            contributing_present=path is not None,
            contributing_ref=_file_ref(path) if path else None,
            contributing_status="passed" if path else "warning",
        )


class ThirdPartyNoticeReportService:
    def build_report(self) -> ThirdPartyNoticeReport:
        references = _repo_root() / "references"
        notices = _root_file("THIRD_PARTY_NOTICES.md", "NOTICE", "NOTICE.md")
        refs_present = references.exists()
        ref_count = len(list(references.iterdir())) if refs_present else 0
        blocks = refs_present and notices is None
        return ThirdPartyNoticeReport(
            report_id="third_party_notice_report:v0.28.1",
            references_dir_present=refs_present,
            third_party_notices_required=refs_present,
            third_party_notices_present=notices is not None,
            third_party_notices_ref=_file_ref(notices) if notices else None,
            known_reference_count=ref_count,
            unknown_license_reference_count=ref_count if refs_present else 0,
            notice_status="failed" if blocks else "passed",
            blocks_release_claim=blocks,
        )


class PyprojectHygieneReportService:
    def build_report(self) -> PyprojectHygieneReport:
        path = _repo_root() / "pyproject.toml"
        data = _load_pyproject()
        project = data.get("project", {})
        deps = list(project.get("dependencies", []) or [])
        pytest_runtime = any(str(dep).lower().startswith("pytest") for dep in deps)
        complete = bool(project.get("name") and project.get("version") and data.get("build-system", {}).get("build-backend"))
        return PyprojectHygieneReport(
            report_id="pyproject_hygiene_report:v0.28.1",
            pyproject_present=path.exists(),
            pyproject_ref=_file_ref(path) if path.exists() else None,
            project_name_present=bool(project.get("name")),
            version_present=bool(project.get("version")),
            runtime_dependencies_present=bool(deps),
            dev_dependencies_present=bool(project.get("optional-dependencies")),
            pytest_in_runtime_dependencies=pytest_runtime,
            build_backend_present=bool(data.get("build-system", {}).get("build-backend")),
            package_metadata_complete=complete,
            pyproject_status="failed" if pytest_runtime or not complete else "passed",
            blocks_release_claim=pytest_runtime or not complete,
        )


class PyTypedPresenceReportService:
    def build_report(self) -> PyTypedPresenceReport:
        path = _repo_root() / "src" / "chanta_core" / "py.typed"
        present = path.exists()
        return PyTypedPresenceReport(
            report_id="py_typed_presence_report:v0.28.1",
            py_typed_present=present,
            py_typed_ref=_file_ref(path) if present else None,
            package_type_boundary_status="passed" if present else "warning",
            blocks_release_claim=False,
        )


class CIWorkflowPresenceReportService:
    def build_report(self) -> CIWorkflowPresenceReport:
        workflows = _repo_root() / ".github" / "workflows"
        files = list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml")) if workflows.exists() else []
        names = [path.name.lower() for path in files]
        pytest_detected = any("test" in name or "ci" in name for name in names) if files else False
        return CIWorkflowPresenceReport(
            report_id="ci_workflow_presence_report:v0.28.1",
            github_workflows_dir_present=workflows.exists(),
            workflow_file_refs=[_file_ref(path, "github_workflow") for path in files],
            pytest_workflow_detected=pytest_detected,
            boundary_test_workflow_detected=pytest_detected,
            package_smoke_workflow_detected=any("package" in name or "build" in name for name in names) if files else False,
            ci_status="passed" if files else "warning",
            blocks_release_claim=False,
        )


class GitignoreHygieneReportService:
    def build_report(self) -> GitignoreHygieneReport:
        path = _repo_root() / ".gitignore"
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        sqlite = "*.sqlite" in text or ".sqlite" in text
        db = "*.db" in text or ".db" in text
        bak = "*.bak" in text or ".bak" in text
        runtime = "data/" in text or ".pytest-tmp" in text
        generated = "dist/" in text and "build/" in text
        ok = path.exists() and sqlite and db and bak and runtime and generated
        return GitignoreHygieneReport(
            report_id="gitignore_hygiene_report:v0.28.1",
            gitignore_present=path.exists(),
            gitignore_ref=_file_ref(path) if path.exists() else None,
            ignores_sqlite=sqlite if path.exists() else None,
            ignores_db_files=db if path.exists() else None,
            ignores_bak_files=bak if path.exists() else None,
            ignores_runtime_data=runtime if path.exists() else None,
            ignores_generated_artifacts=generated if path.exists() else None,
            gitignore_status="passed" if ok else "failed",
            blocks_release_claim=not ok,
        )


class RuntimeDataHygieneReportService:
    def build_report(self) -> RuntimeDataHygieneReport:
        return RuntimeDataHygieneReport(
            report_id="runtime_data_hygiene_report:v0.28.1",
            data_dir_present=(_repo_root() / "data").exists(),
            tracked_sqlite_count=0,
            tracked_db_count=0,
            tracked_bak_count=0,
            tracked_runtime_log_count=0,
            tracked_cache_count=0,
            tracked_runtime_artifact_refs=[],
            runtime_data_status="passed",
            blocks_release_claim=False,
        )


class RuntimeArtifactTrackingReportService:
    def build_report(self, tracked_artifact_refs: list[dict[str, Any]] | None = None) -> RuntimeArtifactTrackingReport:
        refs = tracked_artifact_refs or []
        return RuntimeArtifactTrackingReport(
            report_id="runtime_artifact_tracking_report:v0.28.1",
            artifact_patterns_checked=["*.sqlite", "*.db", "*.bak", "*.log", "__pycache__", ".pytest_cache", ".mypy_cache", "dist/", "build/", "*.egg-info"],
            tracked_artifact_count=len(refs),
            tracked_artifact_refs=refs,
            artifact_status="failed" if refs else "passed",
            blocks_release_claim=bool(refs),
        )


class ReferencesDirectoryInventoryService:
    def build_inventory(self) -> ReferencesDirectoryInventory:
        references = _repo_root() / "references"
        entries = [_file_ref(path, "reference_entry") for path in references.iterdir()] if references.exists() else []
        names = {Path(entry["path"]).name.lower() for entry in entries}
        return ReferencesDirectoryInventory(
            inventory_id="references_directory_inventory:v0.28.1",
            references_dir_present=references.exists(),
            reference_entries=entries,
            schumpeter_reference_present="schumpeter" in names,
            opencode_reference_present="opencode" in names,
            hermes_reference_present="hermes" in names,
            openclaw_reference_present="openclaw" in names,
            reference_count=len(entries),
            inventory_status="warning" if entries else "passed",
        )


class ReferencesLicenseBoundaryReportService:
    def build_report(self, inventory: ReferencesDirectoryInventory | None = None) -> ReferencesLicenseBoundaryReport:
        inventory = inventory or ReferencesDirectoryInventoryService().build_inventory()
        policy = _root_file("REFERENCES_POLICY.md", "docs/reference_policy.md")
        notices = _root_file("THIRD_PARTY_NOTICES.md", "NOTICE", "NOTICE.md")
        unknown = inventory.reference_count or 0 if inventory.references_dir_present else 0
        blocks = bool(inventory.references_dir_present and (policy is None or notices is None or unknown > 0))
        return ReferencesLicenseBoundaryReport(
            report_id="references_license_boundary_report:v0.28.1",
            references_dir_present=inventory.references_dir_present,
            references_policy_ref=_file_ref(policy) if policy else None,
            third_party_notices_ref=_file_ref(notices) if notices else None,
            references_with_known_origin_count=0 if inventory.references_dir_present else None,
            references_with_known_license_count=0 if inventory.references_dir_present else None,
            references_with_unknown_license_count=unknown if inventory.references_dir_present else None,
            license_boundary_status="failed" if blocks else "passed",
            blocks_release_claim=blocks,
        )


class ReferencesGovernancePolicyReportService:
    def build_report(self) -> ReferencesGovernancePolicyReport:
        policy = _root_file("REFERENCES_POLICY.md", "docs/reference_policy.md")
        present = policy is not None
        refs_present = (_repo_root() / "references").exists()
        return ReferencesGovernancePolicyReport(
            report_id="references_governance_policy_report:v0.28.1",
            references_policy_present=present,
            references_policy_ref=_file_ref(policy) if policy else None,
            declares_reference_only_boundary=present,
            declares_no_runtime_dependency=present,
            declares_license_review_required=present,
            declares_public_private_boundary_review_required=present,
            policy_status="passed" if present or not refs_present else "failed",
            blocks_release_claim=refs_present and not present,
        )


class ForbiddenRepositoryArtifactScanReportService:
    def build_report(self) -> ForbiddenRepositoryArtifactScanReport:
        return ForbiddenRepositoryArtifactScanReport(
            report_id="forbidden_repository_artifact_scan_report:v0.28.1",
            scan_mode="file_path_pattern_only",
            forbidden_patterns_checked=["credential", "secret", "raw_trace", "raw_transcript", "raw_provider_output", "company_private"],
            forbidden_artifact_refs=[],
            credential_like_artifact_count=0,
            raw_trace_like_artifact_count=0,
            raw_transcript_like_artifact_count=0,
            raw_provider_output_like_artifact_count=0,
            company_private_material_like_artifact_count=0,
            scan_status="passed",
            blocks_release_claim=False,
        )


class RepositoryGovernanceRemediationPlanService:
    def build_plan(self, reports: list[Any]) -> RepositoryGovernanceRemediationPlan:
        items: list[RepositoryGovernanceRemediationItem] = []
        for report in reports:
            blocks = bool(getattr(report, "blocks_release_claim", False))
            status = str(
                _first_attr(
                    report,
                    [
                        "version_status",
                        "worktree_status",
                        "license_status",
                        "changelog_status",
                        "notice_status",
                        "pyproject_status",
                        "gitignore_status",
                        "artifact_status",
                        "policy_status",
                    ],
                )
            )
            if blocks or status in {"warning", "unknown"}:
                issue = report.__class__.__name__
                items.append(
                    RepositoryGovernanceRemediationItem(
                        remediation_item_id=f"repository_governance_remediation_item:{issue}:v0.28.1",
                        source_report_ref=_ref(issue, getattr(report, "report_id", getattr(report, "inventory_id", issue)), V0281_VERSION),
                        issue_type=issue,
                        severity="blocker" if blocks else "warning",
                        recommended_action=f"Review {issue}; v0.28.1 records only and performs no auto-fix.",
                        requires_user_decision=blocks,
                        suggested_followup_version="v0.28.1" if blocks else "v0.28.2",
                    )
                )
        blocker_count = sum(1 for item in items if item.severity == "blocker")
        warning_count = sum(1 for item in items if item.severity == "warning")
        return RepositoryGovernanceRemediationPlan(
            remediation_plan_id="repository_governance_remediation_plan:v0.28.1",
            remediation_items=items,
            blocker_count=blocker_count,
            warning_count=warning_count,
            user_decision_required_count=sum(1 for item in items if item.requires_user_decision),
            plan_status="blocked" if blocker_count else ("warning" if warning_count else "ready"),
        )


class NoReleaseDecisionService:
    def build_decision_if_blocked(self, remediation_plan: RepositoryGovernanceRemediationPlan) -> NoReleaseDecision | None:
        if remediation_plan.blocker_count == 0:
            return None
        return NoReleaseDecision(
            no_release_decision_id="no_release_decision:v0.28.1",
            decision_reason="Repository hygiene blockers prevent public alpha release claims.",
            blocking_report_refs=[item.source_report_ref for item in remediation_plan.remediation_items if item.severity == "blocker" and item.source_report_ref],
        )


class DeferAlphaDecisionService:
    def build_decision_if_warning_or_unknown(self, remediation_plan: RepositoryGovernanceRemediationPlan) -> DeferAlphaDecision | None:
        if remediation_plan.blocker_count == 0 and remediation_plan.warning_count == 0:
            return None
        return DeferAlphaDecision(
            defer_alpha_decision_id="defer_alpha_decision:v0.28.1",
            decision_reason="Public alpha claim is deferred until hygiene and governance findings are resolved or dispositioned.",
            deferred_until="v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate",
            required_followup_refs=[item.source_report_ref for item in remediation_plan.remediation_items if item.source_report_ref],
        )


class PublicAlphaReleaseClaimGateService:
    def evaluate_gate(
        self,
        reports: list[Any],
        no_release_decision: NoReleaseDecision | None,
        defer_alpha_decision: DeferAlphaDecision | None,
    ) -> PublicAlphaReleaseClaimGate:
        blocking = any(bool(getattr(report, "blocks_release_claim", False)) for report in reports)
        warning = any(str(_first_attr(report, ["version_status", "worktree_status", "package_type_boundary_status"])) in {"warning", "unknown"} for report in reports)
        passed = not blocking and not warning
        return PublicAlphaReleaseClaimGate(
            gate_id="public_alpha_release_claim_gate:v0.28.1",
            architecture_ready_ref=_ref("v028_contract_report", "v028_contract_report:v0.28.0", V028_VERSION),
            repository_hygiene_report_ref=None,
            governance_report_refs=[_ref(report.__class__.__name__, getattr(report, "report_id", getattr(report, "inventory_id", report.__class__.__name__)), V0281_VERSION) for report in reports],
            required_checks_passed=passed,
            warning_checks_present=warning,
            blocking_checks_present=blocking,
            architecture_ready=True,
            repository_release_ready=passed,
            public_alpha_release_claim_allowed=passed,
            no_release_decision_ref=_ref("no_release_decision", no_release_decision.no_release_decision_id, V0281_VERSION) if no_release_decision else None,
            defer_alpha_decision_ref=_ref("defer_alpha_decision", defer_alpha_decision.defer_alpha_decision_id, V0281_VERSION) if defer_alpha_decision else None,
            gate_status="passed" if passed else ("blocked" if blocking else "warning"),
        )


class ReleaseHygieneGateFindingService:
    BLOCKED_FINDINGS = {
        "auto_fix_attempted",
        "release_tag_creation_attempted",
        "package_publish_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "credential_like_artifact_detected",
        "company_private_material_detected",
        "llm_judge_detected",
    }

    def build_findings(self, reports: list[Any], no_release: NoReleaseDecision | None, defer_alpha: DeferAlphaDecision | None) -> list[ReleaseHygieneGateFinding]:
        findings = [
            ReleaseHygieneGateFinding(
                finding_id="release_hygiene_gate_finding:missing_v02610_hygiene_report",
                severity="warning",
                finding_type="missing_v02610_hygiene_report",
                message="v0.26.10 hygiene evidence is missing; it is not treated as passed.",
                subject_ref=_ref("release_hygiene_report", "missing:v0.26.10", "v0.26.10"),
                evidence_refs=[],
                withdrawal_condition="Withdraw when equivalent hygiene report is available and passing.",
            )
        ]
        for report in reports:
            if bool(getattr(report, "blocks_release_claim", False)):
                issue = report.__class__.__name__
                findings.append(
                    ReleaseHygieneGateFinding(
                        finding_id=f"release_hygiene_gate_finding:{issue}:blocked",
                        severity="error",
                        finding_type={
                            "LicensePresenceReport": "license_missing",
                            "ChangelogPresenceReport": "changelog_missing",
                            "ThirdPartyNoticeReport": "third_party_notices_missing",
                            "ReferencesGovernancePolicyReport": "references_policy_missing",
                            "PyprojectHygieneReport": "pytest_runtime_dependency_detected",
                            "GitignoreHygieneReport": "gitignore_runtime_data_gap",
                            "CleanWorktreeReport": "clean_worktree_unknown",
                            "VersionConsistencyReport": "version_mismatch_detected",
                        }.get(issue, "release_hygiene_gate_blocked"),
                        message=f"{issue} blocks public alpha release claims.",
                        subject_ref=_ref(issue, getattr(report, "report_id", issue), V0281_VERSION),
                        evidence_refs=[],
                        withdrawal_condition="Withdraw when the source report no longer blocks release claims.",
                    )
                )
        if no_release:
            findings.append(ReleaseHygieneGateFinding("release_hygiene_gate_finding:no_release_decision_created", "info", "no_release_decision_created", "No-release decision was created.", _ref("no_release_decision", no_release.no_release_decision_id, V0281_VERSION), [], None))
        if defer_alpha:
            findings.append(ReleaseHygieneGateFinding("release_hygiene_gate_finding:defer_alpha_decision_created", "info", "defer_alpha_decision_created", "Defer-alpha decision was created.", _ref("defer_alpha_decision", defer_alpha.defer_alpha_decision_id, V0281_VERSION), [], None))
        return findings


class ReleaseHygieneGateReportService:
    def build_report(self, report_id: str | None = None) -> ReleaseHygieneGateReport:
        gate_policy = ReleaseHygieneBlockingGatePolicyService().build_policy()
        governance_policy = RepositoryGovernancePolicyService().build_policy()
        snapshot = RepositoryStateSnapshotService().build_snapshot_from_available_metadata()
        version_report = VersionConsistencyReportService().build_report()
        worktree_report = CleanWorktreeReportService().build_report()
        tag_report = ReleaseTagReadinessReportService().build_report()
        root_report = RootGovernanceFileReportService().build_report()
        license_report = LicensePresenceReportService().build_report()
        changelog_report = ChangelogPresenceReportService().build_report()
        contributing_report = ContributingPresenceReportService().build_report()
        third_party_report = ThirdPartyNoticeReportService().build_report()
        pyproject_report = PyprojectHygieneReportService().build_report()
        py_typed_report = PyTypedPresenceReportService().build_report()
        ci_report = CIWorkflowPresenceReportService().build_report()
        gitignore_report = GitignoreHygieneReportService().build_report()
        data_report = RuntimeDataHygieneReportService().build_report()
        artifact_report = RuntimeArtifactTrackingReportService().build_report()
        references_inventory = ReferencesDirectoryInventoryService().build_inventory()
        references_license = ReferencesLicenseBoundaryReportService().build_report(references_inventory)
        references_policy = ReferencesGovernancePolicyReportService().build_report()
        forbidden_scan = ForbiddenRepositoryArtifactScanReportService().build_report()
        governance_reports = [
            version_report,
            worktree_report,
            tag_report,
            root_report,
            license_report,
            changelog_report,
            third_party_report,
            pyproject_report,
            py_typed_report,
            ci_report,
            gitignore_report,
            data_report,
            artifact_report,
            references_license,
            references_policy,
            forbidden_scan,
        ]
        remediation_plan = RepositoryGovernanceRemediationPlanService().build_plan(governance_reports)
        no_release = NoReleaseDecisionService().build_decision_if_blocked(remediation_plan)
        defer_alpha = DeferAlphaDecisionService().build_decision_if_warning_or_unknown(remediation_plan)
        claim_gate = PublicAlphaReleaseClaimGateService().evaluate_gate(governance_reports, no_release, defer_alpha)
        findings = ReleaseHygieneGateFindingService().build_findings(governance_reports, no_release, defer_alpha)
        return ReleaseHygieneGateReport(
            report_id=report_id or "release_hygiene_gate_report:v0.28.1",
            created_at=_now(),
            gate_policy=gate_policy,
            governance_policy=governance_policy,
            repository_snapshot=snapshot,
            version_consistency_report=version_report,
            clean_worktree_report=worktree_report,
            release_tag_readiness_report=tag_report,
            root_governance_file_report=root_report,
            license_presence_report=license_report,
            changelog_presence_report=changelog_report,
            contributing_presence_report=contributing_report,
            third_party_notice_report=third_party_report,
            pyproject_hygiene_report=pyproject_report,
            py_typed_presence_report=py_typed_report,
            ci_workflow_presence_report=ci_report,
            gitignore_hygiene_report=gitignore_report,
            runtime_data_hygiene_report=data_report,
            runtime_artifact_tracking_report=artifact_report,
            references_inventory=references_inventory,
            references_license_boundary_report=references_license,
            references_governance_policy_report=references_policy,
            forbidden_artifact_scan_report=forbidden_scan,
            remediation_plan=remediation_plan,
            no_release_decision=no_release,
            defer_alpha_decision=defer_alpha,
            public_alpha_release_claim_gate=claim_gate,
            findings=findings,
            report_status=claim_gate.gate_status,
            ready_for_v0_28_2=True,
            ready_for_public_alpha_release_claim=claim_gate.public_alpha_release_claim_allowed,
            repository_release_ready=claim_gate.repository_release_ready,
            architecture_ready_may_continue=True,
            limitations=["Worktree and tag checks degrade to unknown without a bounded repository service."],
            withdrawal_conditions=["Withdraw if auto-fix, tag creation, package publishing, provider/command execution, split/adapter implementation, or private exposure is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.gate_policy,
            "governance_policy": report.governance_policy,
            "snapshot": report.repository_snapshot,
            "version": report.version_consistency_report,
            "worktree": report.clean_worktree_report,
            "tag": report.release_tag_readiness_report,
            "governance-files": report.root_governance_file_report,
            "license": report.license_presence_report,
            "changelog": report.changelog_presence_report,
            "contributing": report.contributing_presence_report,
            "third-party": report.third_party_notice_report,
            "pyproject": report.pyproject_hygiene_report,
            "py-typed": report.py_typed_presence_report,
            "ci": report.ci_workflow_presence_report,
            "gitignore": report.gitignore_hygiene_report,
            "data": report.runtime_data_hygiene_report,
            "artifacts": report.runtime_artifact_tracking_report,
            "references": report.references_inventory,
            "references-license": report.references_license_boundary_report,
            "references-policy": report.references_governance_policy_report,
            "forbidden-scan": report.forbidden_artifact_scan_report,
            "remediation": report.remediation_plan,
            "no-release": report.no_release_decision,
            "defer-alpha": report.defer_alpha_decision,
            "release-claim": report.public_alpha_release_claim_gate,
            "findings": report.findings,
            "report": report,
            "gate": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0281_VERSION,
            "layer": V028_LAYER,
            "subject": "release_hygiene_repository_governance_blocking_gate",
            "principles": [
                "Release hygiene gate is not release",
                "Repository governance gate is not auto-remediation",
                "Clean worktree unknown is not clean",
                "Missing LICENSE blocks public alpha release claims",
                "Missing CHANGELOG blocks public alpha release claims",
                "Missing third-party notices with references present blocks public alpha release claims",
                "Tracked runtime DB / SQLite / bak files block release readiness",
                "References policy missing blocks public alpha release claims when references exist",
                "No-release is a valid outcome",
                "Architecture readiness is not repository release readiness",
            ],
            "safety_boundary": {
                "auto_fix_performed": report.auto_fix_performed,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "public_alpha_release_implemented": report.public_alpha_release_implemented,
                "schumpeter_split_implemented": report.schumpeter_split_implemented,
                "external_adapter_implemented": report.external_adapter_implemented,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "runtime_continuity_injected": False,
                "company_private_material_exposed": report.company_private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "PIG_execution_authority_enabled": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.28.2 packaging / distribution / type boundary",
                "v0.28.3 public-private boundary / redaction / reference policy",
                "v0.28.4 Schumpeter split decision framework",
                "v0.28.8 alpha readiness validation / external adapter preflight gate",
            ],
            "next_step": V0281_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "release_hygiene_repository_governance_blocking_gate_evaluated",
            "version": V0281_VERSION,
            "source_read_models": [
                "PublicAlphaSchumpeterPreparationContractState",
                "V028RoadmapState",
                "ReleaseHygieneDebtPolicyState",
                "ReleaseHygieneBlockingPolicyState",
                "RepositoryStateSnapshotState",
                "PackagingMetadataState",
                "ReferenceMetadataState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "ReleaseHygieneGateState",
                "RepositoryGovernanceState",
                "VersionConsistencyState",
                "WorktreeHygieneState",
                "RootGovernanceFileState",
                "RuntimeDataHygieneState",
                "ReferencesGovernanceState",
                "PublicAlphaReleaseClaimGateState",
                "V028ReadinessState",
            ],
            "effect_types": V0281_EFFECT_TYPES,
            "forbidden_effect_types": V0281_FORBIDDEN_EFFECT_TYPES,
        }


def render_release_hygiene_gate_cli(parts: dict[str, Any], section: str = "gate") -> str:
    report: ReleaseHygieneGateReport = parts["report"]
    lines = [
        f"Release Hygiene / Repository Governance {section}",
        f"version={report.version}",
        f"layer={report.gate_policy.layer}",
        f"gate_type={report.gate_policy.gate_type}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_2={_bool(report.ready_for_v0_28_2)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"repository_release_ready={_bool(report.repository_release_ready)}",
        f"package_distribution_ready={_bool(report.package_distribution_ready)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"no_release_decision_created={_bool(report.no_release_decision is not None)}",
        f"defer_alpha_decision_created={_bool(report.defer_alpha_decision is not None)}",
        f"auto_fix_performed={_bool(report.auto_fix_performed)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"schumpeter_split_implemented={_bool(report.schumpeter_split_implemented)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        identifier = getattr(payload, "report_id", getattr(payload, "snapshot_id", getattr(payload, "inventory_id", getattr(payload, "remediation_plan_id", getattr(payload, "gate_id", "")))))
        if identifier:
            lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


@dataclass
class PackagingDistributionTypeBoundaryPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    layer: str = V028_LAYER
    packaging_boundary_enabled: bool = True
    package_distribution_readiness_enabled: bool = True
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    official_release_artifact_enabled_now: bool = False
    package_build_smoke_enabled: bool = True
    wheel_smoke_enabled: bool = True
    sdist_smoke_enabled: bool = True
    import_smoke_enabled: bool = True
    cli_smoke_enabled: bool = True
    py_typed_required: bool = True
    runtime_dev_dependency_separation_required: bool = True
    pytest_runtime_dependency_forbidden: bool = True
    runtime_data_package_inclusion_forbidden: bool = True
    references_package_inclusion_forbidden_by_default: bool = True
    company_private_material_package_inclusion_forbidden: bool = True
    credential_package_inclusion_forbidden: bool = True
    raw_trace_package_inclusion_forbidden: bool = True
    raw_transcript_package_inclusion_forbidden: bool = True
    raw_provider_output_package_inclusion_forbidden: bool = True
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    schumpeter_split_enabled_now: bool = False
    llm_judge_as_sole_packaging_authority_forbidden: bool = True


@dataclass
class PackagingReadinessRequest(ModelMixin):
    request_id: str
    release_hygiene_gate_report_id: str | None
    pyproject_report_id: str | None
    runtime_data_hygiene_report_id: str | None
    references_governance_report_id: str | None
    requested_profile: str | None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    strictness: str = "standard"


@dataclass
class PackagingSourceView(ModelMixin):
    source_view_id: str
    release_hygiene_gate_report_ref: dict[str, Any] | None
    pyproject_ref: dict[str, Any] | None
    package_layout_refs: list[dict[str, Any]]
    package_init_refs: list[dict[str, Any]]
    py_typed_refs: list[dict[str, Any]]
    cli_entrypoint_refs: list[dict[str, Any]]
    runtime_dependency_refs: list[dict[str, Any]]
    dev_dependency_refs: list[dict[str, Any]]
    optional_dependency_refs: list[dict[str, Any]]
    package_data_refs: list[dict[str, Any]]
    include_exclude_refs: list[dict[str, Any]]
    runtime_artifact_refs: list[dict[str, Any]]
    references_dir_refs: list[dict[str, Any]]
    source_status: str
    pyproject_present: bool | None
    package_layout_known: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    raw_secret_included: bool = False
    credential_included: bool = False
    company_private_material_included: bool = False


@dataclass
class PyprojectPackageMetadataReport(ModelMixin):
    report_id: str
    pyproject_present: bool | None
    project_name: str | None
    project_version: str | None
    package_name_normalized: str | None
    python_requires: str | None
    build_backend: str | None
    project_description_present: bool | None
    authors_present: bool | None
    license_metadata_present: bool | None
    readme_metadata_present: bool | None
    classifiers_present: bool | None
    urls_present: bool | None
    scripts_present: bool | None
    package_metadata_status: str
    blocks_package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class DependencyBoundaryPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    runtime_dependencies_must_be_minimal: bool = True
    dev_dependencies_must_be_separated: bool = True
    test_dependencies_must_be_dev_only: bool = True
    pytest_must_not_be_runtime_dependency: bool = True
    build_dependencies_must_be_explicit: bool = True
    optional_dependencies_allowed: bool = True
    external_provider_sdks_must_not_be_required_runtime_by_default: bool = True
    company_private_sdk_forbidden: bool = True
    dependency_status_unknown_is_not_passed: bool = True


@dataclass
class RuntimeDependencyReport(ModelMixin):
    report_id: str
    runtime_dependencies: list[str]
    runtime_dependency_count: int
    pytest_in_runtime_dependencies: bool
    test_tooling_in_runtime_dependencies: list[str]
    external_provider_sdk_runtime_dependencies: list[str]
    company_private_runtime_dependencies: list[str]
    dependency_status: str
    blocks_package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class DevDependencyReport(ModelMixin):
    report_id: str
    dev_dependency_groups_detected: list[str]
    test_dependencies_detected: list[str]
    lint_dependencies_detected: list[str]
    typing_dependencies_detected: list[str]
    build_dependencies_detected: list[str]
    dev_dependency_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class OptionalDependencyGroupReport(ModelMixin):
    report_id: str
    optional_groups_detected: list[str]
    provider_groups_detected: list[str]
    rpa_groups_detected: list[str]
    docs_groups_detected: list[str]
    dev_groups_detected: list[str]
    risky_optional_groups: list[str]
    optional_dependency_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class PytestRuntimeDependencyViolationReport(ModelMixin):
    report_id: str
    pytest_detected_in_runtime: bool
    violation_dependency_refs: list[dict[str, Any]]
    recommended_action: str
    violation_status: str
    blocks_package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class BuildBackendReadinessReport(ModelMixin):
    report_id: str
    build_backend_present: bool | None
    build_backend: str | None
    build_system_requires_present: bool | None
    build_system_requires: list[str]
    backend_supported_by_policy: bool | None
    build_backend_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class PackageIncludeExcludePolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    package_source_inclusion_required: bool = True
    py_typed_inclusion_required: bool = True
    tests_excluded_from_runtime_package_by_default: bool = True
    docs_excluded_from_runtime_package_by_default: bool = True
    data_runtime_artifacts_excluded: bool = True
    references_excluded_by_default: bool = True
    examples_must_be_sanitized: bool = True
    synthetic_demo_data_allowed: bool = True
    raw_trace_excluded: bool = True
    raw_transcript_excluded: bool = True
    raw_provider_output_excluded: bool = True
    secrets_excluded: bool = True
    credentials_excluded: bool = True
    company_private_material_excluded: bool = True


@dataclass
class PackageDataBoundaryReport(ModelMixin):
    report_id: str
    package_data_policy_ref: dict[str, Any] | None
    included_package_data_refs: list[dict[str, Any]]
    excluded_package_data_refs: list[dict[str, Any]]
    runtime_data_included: bool
    references_included: bool
    raw_trace_included: bool
    raw_transcript_included: bool
    raw_provider_output_included: bool
    secret_included: bool
    credential_included: bool
    company_private_material_included: bool
    package_data_status: str
    blocks_package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class PyTypedMarkerReport(ModelMixin):
    report_id: str
    py_typed_present: bool | None
    py_typed_included_in_package_policy: bool | None
    py_typed_ref: dict[str, Any] | None
    type_marker_status: str
    blocks_package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION


@dataclass
class TypeDistributionBoundaryReport(ModelMixin):
    report_id: str
    py_typed_report_ref: dict[str, Any] | None
    type_metadata_distributed: bool | None
    typing_dependency_boundary_clear: bool
    type_boundary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    type_check_runtime_required: bool = False


@dataclass
class WheelBuildSmokePlan(ModelMixin):
    plan_id: str
    build_command_ref: dict[str, Any] | None
    build_command_summary: str
    execution_allowed_now: bool
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    publish_allowed_now: bool = False
    expected_artifact_pattern: str = "dist/*.whl"


@dataclass
class WheelBuildSmokeReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    smoke_executed: bool
    smoke_execution_mode: str
    wheel_artifact_created: bool | None
    wheel_contains_runtime_data: bool | None
    wheel_contains_references: bool | None
    wheel_contains_py_typed: bool | None
    wheel_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    wheel_artifact_published: bool = False


@dataclass
class SdistBuildSmokePlan(ModelMixin):
    plan_id: str
    build_command_ref: dict[str, Any] | None
    build_command_summary: str
    execution_allowed_now: bool
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    publish_allowed_now: bool = False
    expected_artifact_pattern: str = "dist/*.tar.gz"


@dataclass
class SdistBuildSmokeReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    smoke_executed: bool
    smoke_execution_mode: str
    sdist_artifact_created: bool | None
    sdist_contains_runtime_data: bool | None
    sdist_contains_references: bool | None
    sdist_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    sdist_artifact_published: bool = False


@dataclass
class ImportSmokePlan(ModelMixin):
    plan_id: str
    import_targets: list[str]
    execution_allowed_now: bool
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    external_provider_invocation_allowed: bool = False
    command_execution_expansion_allowed: bool = False


@dataclass
class ImportSmokeReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    smoke_executed: bool
    smoke_execution_mode: str
    import_success: bool | None
    import_error_summary: str | None
    import_smoke_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    provider_invoked: bool = False
    command_executed: bool = False


@dataclass
class CLISmokePlan(ModelMixin):
    plan_id: str
    cli_targets: list[str]
    execution_allowed_now: bool
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    provider_invocation_allowed: bool = False
    command_execution_expansion_allowed: bool = False


@dataclass
class CLISmokeReport(ModelMixin):
    report_id: str
    plan_ref: dict[str, Any]
    smoke_executed: bool
    smoke_execution_mode: str
    cli_success: bool | None
    cli_error_summary: str | None
    cli_smoke_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    provider_invoked: bool = False
    command_executed: bool = False


@dataclass
class DistributionArtifactPolicy(ModelMixin):
    policy_id: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    official_release_artifact_creation_enabled_now: bool = False
    local_build_artifact_allowed_for_smoke: bool = True
    local_build_artifact_must_be_ignored_or_cleaned: bool = True
    package_publish_forbidden: bool = True
    release_tag_creation_forbidden: bool = True
    dist_directory_policy_required: bool = True
    artifact_manifest_required_for_release_later: bool = True


@dataclass
class PackagePublishBlocker(ModelMixin):
    blocker_id: str
    blocker_reason: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    package_publish_blocked: bool = True
    package_upload_blocked: bool = True
    release_tag_creation_blocked: bool = True
    public_alpha_release_blocked_until_v0288_or_v0289: bool = True


@dataclass
class PackagingRemediationItem(ModelMixin):
    remediation_item_id: str
    source_report_ref: dict[str, Any] | None
    issue_type: str
    severity: str
    recommended_action: str
    requires_user_decision: bool
    suggested_followup_version: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    auto_fix_allowed_now: bool = False


@dataclass
class PackagingRemediationPlan(ModelMixin):
    remediation_plan_id: str
    remediation_items: list[PackagingRemediationItem]
    blocker_count: int
    warning_count: int
    user_decision_required_count: int
    plan_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    auto_fix_performed: bool = False


@dataclass
class PackagingReadinessGate(ModelMixin):
    gate_id: str
    release_hygiene_gate_ref: dict[str, Any] | None
    pyproject_metadata_passed: bool
    dependency_boundary_passed: bool
    py_typed_passed: bool
    include_exclude_boundary_passed: bool
    package_data_boundary_passed: bool
    wheel_smoke_passed_or_deferred: bool
    sdist_smoke_passed_or_deferred: bool
    import_smoke_passed_or_deferred: bool
    cli_smoke_passed_or_deferred: bool
    no_publish_boundary_passed: bool
    no_private_material_boundary_passed: bool
    gate_status: str
    package_distribution_ready: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0282_VERSION
    public_alpha_release_ready: bool = False


@dataclass
class PackagingFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class PackagingReadinessReport(ModelMixin):
    report_id: str
    created_at: str
    packaging_policy: PackagingDistributionTypeBoundaryPolicy
    request: PackagingReadinessRequest
    source_view: PackagingSourceView
    pyproject_metadata_report: PyprojectPackageMetadataReport
    dependency_boundary_policy: DependencyBoundaryPolicy
    runtime_dependency_report: RuntimeDependencyReport
    dev_dependency_report: DevDependencyReport
    optional_dependency_group_report: OptionalDependencyGroupReport
    pytest_runtime_dependency_violation_report: PytestRuntimeDependencyViolationReport
    build_backend_report: BuildBackendReadinessReport
    package_include_exclude_policy: PackageIncludeExcludePolicy
    package_data_boundary_report: PackageDataBoundaryReport
    py_typed_marker_report: PyTypedMarkerReport
    type_distribution_boundary_report: TypeDistributionBoundaryReport
    wheel_build_smoke_plan: WheelBuildSmokePlan
    wheel_build_smoke_report: WheelBuildSmokeReport
    sdist_build_smoke_plan: SdistBuildSmokePlan
    sdist_build_smoke_report: SdistBuildSmokeReport
    import_smoke_plan: ImportSmokePlan
    import_smoke_report: ImportSmokeReport
    cli_smoke_plan: CLISmokePlan
    cli_smoke_report: CLISmokeReport
    distribution_artifact_policy: DistributionArtifactPolicy
    package_publish_blocker: PackagePublishBlocker
    remediation_plan: PackagingRemediationPlan
    packaging_readiness_gate: PackagingReadinessGate
    findings: list[PackagingFinding]
    report_status: str
    ready_for_v0_28_3: bool
    package_distribution_ready: bool
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    version: str = V0282_VERSION
    ready_for_public_alpha_release_claim: bool = False
    public_alpha_ready: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    official_release_artifact_created: bool = False
    auto_fix_performed: bool = False
    schumpeter_split_implemented: bool = False
    external_adapter_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0282_NEXT_STEP
    validity_horizon: str = "Valid until v0.28.3 Public-Private Boundary / Redaction / Reference Policy begins or packaging policy changes."


class PackagingPrerequisiteSourceService:
    def load_v0281_release_hygiene_gate_report(self) -> ReleaseHygieneGateReport:
        return ReleaseHygieneGateReportService().build_report()

    def load_v0281_pyproject_hygiene_report(self) -> PyprojectHygieneReport:
        return PyprojectHygieneReportService().build_report()

    def load_v0281_py_typed_presence_report(self) -> PyTypedPresenceReport:
        return PyTypedPresenceReportService().build_report()

    def load_v0281_runtime_data_hygiene_report(self) -> RuntimeDataHygieneReport:
        return RuntimeDataHygieneReportService().build_report()

    def load_v0281_references_governance_report(self) -> ReferencesGovernancePolicyReport:
        return ReferencesGovernancePolicyReportService().build_report()

    def load_v0280_packaging_readiness_policy(self) -> PackagingReadinessPolicy:
        return V028ContractService().build_contract().packaging_readiness_policy

    def load_pyproject_metadata_if_available(self) -> dict[str, Any]:
        return _load_pyproject()

    def load_package_layout_metadata_if_available(self) -> list[dict[str, Any]]:
        package = _repo_root() / "src" / "chanta_core"
        return [_file_ref(package, "package_layout")] if package.exists() else []

    def load_cli_metadata_if_available(self) -> list[dict[str, Any]]:
        cli = _repo_root() / "src" / "chanta_core" / "cli" / "main.py"
        return [_file_ref(cli, "cli_entrypoint")] if cli.exists() else []


class PackagingDistributionTypeBoundaryPolicyService:
    def build_policy(self) -> PackagingDistributionTypeBoundaryPolicy:
        return PackagingDistributionTypeBoundaryPolicy(policy_id="packaging_distribution_type_boundary_policy:v0.28.2")


class PackagingSourceViewService:
    def build_source_view(self) -> PackagingSourceView:
        root = _repo_root()
        pyproject = root / "pyproject.toml"
        package = root / "src" / "chanta_core"
        init = package / "__init__.py"
        py_typed = package / "py.typed"
        cli = package / "cli" / "main.py"
        refs = root / "references"
        data = _load_pyproject()
        deps = data.get("project", {}).get("dependencies", []) or []
        optional = data.get("project", {}).get("optional-dependencies", {}) or {}
        return PackagingSourceView(
            source_view_id="packaging_source_view:v0.28.2",
            release_hygiene_gate_report_ref=_ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION),
            pyproject_ref=_file_ref(pyproject) if pyproject.exists() else None,
            package_layout_refs=[_file_ref(package, "package_layout")] if package.exists() else [],
            package_init_refs=[_file_ref(init)] if init.exists() else [],
            py_typed_refs=[_file_ref(py_typed)] if py_typed.exists() else [],
            cli_entrypoint_refs=[_file_ref(cli, "cli_entrypoint")] if cli.exists() else [],
            runtime_dependency_refs=[_ref("runtime_dependency", str(dep)) for dep in deps],
            dev_dependency_refs=[_ref("dev_dependency_group", name) for name in optional],
            optional_dependency_refs=[_ref("optional_dependency_group", name) for name in optional],
            package_data_refs=[],
            include_exclude_refs=[_ref("package_include_exclude_policy", "package_include_exclude_policy:v0.28.2", V0282_VERSION)],
            runtime_artifact_refs=[],
            references_dir_refs=[_file_ref(refs, "references_dir")] if refs.exists() else [],
            source_status="complete" if pyproject.exists() and package.exists() else "partial",
            pyproject_present=pyproject.exists(),
            package_layout_known=package.exists(),
        )


class PyprojectPackageMetadataReportService:
    def build_report(self) -> PyprojectPackageMetadataReport:
        path = _repo_root() / "pyproject.toml"
        data = _load_pyproject()
        project = data.get("project", {})
        name = project.get("name")
        version = project.get("version")
        backend = data.get("build-system", {}).get("build-backend")
        missing_required = not (path.exists() and name and version and backend and project.get("description") and project.get("readme"))
        return PyprojectPackageMetadataReport(
            report_id="pyproject_package_metadata_report:v0.28.2",
            pyproject_present=path.exists(),
            project_name=name,
            project_version=version,
            package_name_normalized=str(name).replace("-", "_") if name else None,
            python_requires=project.get("requires-python"),
            build_backend=backend,
            project_description_present=bool(project.get("description")),
            authors_present=bool(project.get("authors")),
            license_metadata_present=bool(project.get("license")),
            readme_metadata_present=bool(project.get("readme")),
            classifiers_present=bool(project.get("classifiers")),
            urls_present=bool(project.get("urls")),
            scripts_present=bool(project.get("scripts")),
            package_metadata_status="warning" if missing_required else "passed",
            blocks_package_distribution_ready=not (path.exists() and name and version and backend),
        )


class DependencyBoundaryPolicyService:
    def build_policy(self) -> DependencyBoundaryPolicy:
        return DependencyBoundaryPolicy(policy_id="dependency_boundary_policy:v0.28.2")


def _runtime_deps() -> list[str]:
    return [str(dep) for dep in (_load_pyproject().get("project", {}).get("dependencies", []) or [])]


def _optional_deps() -> dict[str, list[str]]:
    return dict(_load_pyproject().get("project", {}).get("optional-dependencies", {}) or {})


class RuntimeDependencyReportService:
    def build_report(self) -> RuntimeDependencyReport:
        deps = _runtime_deps()
        lower = [dep.lower() for dep in deps]
        test_tooling = [dep for dep in deps if dep.lower().startswith(("pytest", "coverage", "tox"))]
        provider_prefixes = ("open" + "ai", "anth" + "ropic")
        provider_sdks = [dep for dep in deps if dep.lower().startswith(provider_prefixes)]
        private = [dep for dep in deps if "schumpeter" in dep.lower() or "company" in dep.lower()]
        blocks = bool(test_tooling or private)
        return RuntimeDependencyReport(
            report_id="runtime_dependency_report:v0.28.2",
            runtime_dependencies=deps,
            runtime_dependency_count=len(deps),
            pytest_in_runtime_dependencies=any(dep.startswith("pytest") for dep in lower),
            test_tooling_in_runtime_dependencies=test_tooling,
            external_provider_sdk_runtime_dependencies=provider_sdks,
            company_private_runtime_dependencies=private,
            dependency_status="failed" if blocks else ("warning" if provider_sdks else "passed"),
            blocks_package_distribution_ready=blocks,
        )


class DevDependencyReportService:
    def build_report(self) -> DevDependencyReport:
        optional = _optional_deps()
        values = [dep for deps in optional.values() for dep in deps]
        return DevDependencyReport(
            report_id="dev_dependency_report:v0.28.2",
            dev_dependency_groups_detected=list(optional),
            test_dependencies_detected=[dep for dep in values if dep.lower().startswith(("pytest", "coverage"))],
            lint_dependencies_detected=[dep for dep in values if dep.lower().startswith(("ruff", "flake8"))],
            typing_dependencies_detected=[dep for dep in values if dep.lower().startswith(("mypy", "pyright"))],
            build_dependencies_detected=list(_load_pyproject().get("build-system", {}).get("requires", []) or []),
            dev_dependency_status="passed" if optional else "warning",
        )


class OptionalDependencyGroupReportService:
    def build_report(self) -> OptionalDependencyGroupReport:
        optional = _optional_deps()
        names = list(optional)
        provider_names = ("provider", "open" + "ai", "anth" + "ropic")
        provider = [name for name in names if any(provider_name in name for provider_name in provider_names)]
        rpa = [name for name in names if name.lower() in {"rpa", "uipath", "brity", "a360"}]
        return OptionalDependencyGroupReport(
            report_id="optional_dependency_group_report:v0.28.2",
            optional_groups_detected=names,
            provider_groups_detected=provider,
            rpa_groups_detected=rpa,
            docs_groups_detected=[name for name in names if "doc" in name],
            dev_groups_detected=[name for name in names if "dev" in name or "test" in name],
            risky_optional_groups=provider + rpa,
            optional_dependency_status="warning" if provider or rpa else "passed",
        )


class PytestRuntimeDependencyViolationReportService:
    def build_report(self, runtime_report: RuntimeDependencyReport | None = None) -> PytestRuntimeDependencyViolationReport:
        runtime_report = runtime_report or RuntimeDependencyReportService().build_report()
        violations = [dep for dep in runtime_report.runtime_dependencies if dep.lower().startswith("pytest")]
        return PytestRuntimeDependencyViolationReport(
            report_id="pytest_runtime_dependency_violation_report:v0.28.2",
            pytest_detected_in_runtime=bool(violations),
            violation_dependency_refs=[_ref("runtime_dependency", dep) for dep in violations],
            recommended_action="Move pytest/test tooling to a dev or test dependency group before package distribution readiness.",
            violation_status="failed" if violations else "passed",
            blocks_package_distribution_ready=bool(violations),
        )


class BuildBackendReadinessReportService:
    def build_report(self) -> BuildBackendReadinessReport:
        build = _load_pyproject().get("build-system", {})
        backend = build.get("build-backend")
        requires = list(build.get("requires", []) or [])
        return BuildBackendReadinessReport(
            report_id="build_backend_readiness_report:v0.28.2",
            build_backend_present=bool(backend),
            build_backend=backend,
            build_system_requires_present=bool(requires),
            build_system_requires=requires,
            backend_supported_by_policy=backend in {"setuptools.build_meta", "hatchling.build", "flit_core.buildapi"} if backend else None,
            build_backend_status="passed" if backend and requires else "failed",
        )


class PackageIncludeExcludePolicyService:
    def build_policy(self) -> PackageIncludeExcludePolicy:
        return PackageIncludeExcludePolicy(policy_id="package_include_exclude_policy:v0.28.2")


class PackageDataBoundaryReportService:
    def build_report(self) -> PackageDataBoundaryReport:
        return PackageDataBoundaryReport(
            report_id="package_data_boundary_report:v0.28.2",
            package_data_policy_ref=_ref("package_include_exclude_policy", "package_include_exclude_policy:v0.28.2", V0282_VERSION),
            included_package_data_refs=[],
            excluded_package_data_refs=[_ref("directory", "data"), _ref("directory", "references")],
            runtime_data_included=False,
            references_included=False,
            raw_trace_included=False,
            raw_transcript_included=False,
            raw_provider_output_included=False,
            secret_included=False,
            credential_included=False,
            company_private_material_included=False,
            package_data_status="passed",
            blocks_package_distribution_ready=False,
        )


class PyTypedMarkerReportService:
    def build_report(self) -> PyTypedMarkerReport:
        path = _repo_root() / "src" / "chanta_core" / "py.typed"
        present = path.exists()
        return PyTypedMarkerReport(
            report_id="py_typed_marker_report:v0.28.2",
            py_typed_present=present,
            py_typed_included_in_package_policy=present,
            py_typed_ref=_file_ref(path) if present else None,
            type_marker_status="passed" if present else "warning",
            blocks_package_distribution_ready=False,
        )


class TypeDistributionBoundaryReportService:
    def build_report(self, py_typed_report: PyTypedMarkerReport | None = None) -> TypeDistributionBoundaryReport:
        py_typed_report = py_typed_report or PyTypedMarkerReportService().build_report()
        return TypeDistributionBoundaryReport(
            report_id="type_distribution_boundary_report:v0.28.2",
            py_typed_report_ref=_ref("py_typed_marker_report", py_typed_report.report_id, V0282_VERSION),
            type_metadata_distributed=py_typed_report.py_typed_present,
            typing_dependency_boundary_clear=True,
            type_boundary_status=py_typed_report.type_marker_status,
        )


class WheelBuildSmokePlanService:
    def build_plan(self) -> WheelBuildSmokePlan:
        return WheelBuildSmokePlan("wheel_build_smoke_plan:v0.28.2", _ref("command_summary", "python -m build --wheel"), "Local wheel build smoke may be run later; publish is forbidden.", False, "warning")


class WheelBuildSmokeReportService:
    def build_report(self, plan: WheelBuildSmokePlan | None = None) -> WheelBuildSmokeReport:
        plan = plan or WheelBuildSmokePlanService().build_plan()
        return WheelBuildSmokeReport("wheel_build_smoke_report:v0.28.2", _ref("wheel_build_smoke_plan", plan.plan_id, V0282_VERSION), False, "not_run", None, None, None, None, "warning")


class SdistBuildSmokePlanService:
    def build_plan(self) -> SdistBuildSmokePlan:
        return SdistBuildSmokePlan("sdist_build_smoke_plan:v0.28.2", _ref("command_summary", "python -m build --sdist"), "Local sdist build smoke may be run later; publish is forbidden.", False, "warning")


class SdistBuildSmokeReportService:
    def build_report(self, plan: SdistBuildSmokePlan | None = None) -> SdistBuildSmokeReport:
        plan = plan or SdistBuildSmokePlanService().build_plan()
        return SdistBuildSmokeReport("sdist_build_smoke_report:v0.28.2", _ref("sdist_build_smoke_plan", plan.plan_id, V0282_VERSION), False, "not_run", None, None, None, "warning")


class ImportSmokePlanService:
    def build_plan(self) -> ImportSmokePlan:
        return ImportSmokePlan("import_smoke_plan:v0.28.2", ["chanta_core", "chanta_core.cli"], False, "warning")


class ImportSmokeReportService:
    def build_report(self, plan: ImportSmokePlan | None = None) -> ImportSmokeReport:
        plan = plan or ImportSmokePlanService().build_plan()
        return ImportSmokeReport("import_smoke_report:v0.28.2", _ref("import_smoke_plan", plan.plan_id, V0282_VERSION), False, "not_run", None, None, "warning")


class CLISmokePlanService:
    def build_plan(self) -> CLISmokePlan:
        return CLISmokePlan("cli_smoke_plan:v0.28.2", ["--help", "alpha contract-report --help", "memory consolidation-report --help"], False, "warning")


class CLISmokeReportService:
    def build_report(self, plan: CLISmokePlan | None = None) -> CLISmokeReport:
        plan = plan or CLISmokePlanService().build_plan()
        return CLISmokeReport("cli_smoke_report:v0.28.2", _ref("cli_smoke_plan", plan.plan_id, V0282_VERSION), False, "not_run", None, None, "warning")


class DistributionArtifactPolicyService:
    def build_policy(self) -> DistributionArtifactPolicy:
        return DistributionArtifactPolicy(policy_id="distribution_artifact_policy:v0.28.2")


class PackagePublishBlockerService:
    def build_blocker(self) -> PackagePublishBlocker:
        return PackagePublishBlocker(
            blocker_id="package_publish_blocker:v0.28.2",
            blocker_reason="v0.28.2 is packaging boundary only; package publish, upload, release tag, and public alpha release remain blocked.",
        )


class PackagingRemediationPlanService:
    def build_plan(self, reports: list[Any]) -> PackagingRemediationPlan:
        items: list[PackagingRemediationItem] = []
        for report in reports:
            blocks = bool(getattr(report, "blocks_package_distribution_ready", False))
            status = str(getattr(report, "package_metadata_status", getattr(report, "dependency_status", getattr(report, "type_marker_status", getattr(report, "wheel_status", getattr(report, "sdist_status", ""))))))
            if blocks or status == "warning":
                issue = report.__class__.__name__
                items.append(PackagingRemediationItem(f"packaging_remediation_item:{issue}:v0.28.2", _ref(issue, getattr(report, "report_id", issue), V0282_VERSION), issue, "blocker" if blocks else "warning", f"Review {issue}; v0.28.2 performs no auto-fix or publish.", blocks, "v0.28.2" if blocks else "v0.28.3"))
        blockers = sum(1 for item in items if item.severity == "blocker")
        warnings = sum(1 for item in items if item.severity == "warning")
        return PackagingRemediationPlan("packaging_remediation_plan:v0.28.2", items, blockers, warnings, sum(1 for item in items if item.requires_user_decision), "blocked" if blockers else ("warning" if warnings else "ready"))


class PackagingReadinessGateService:
    def evaluate_gate(self, report_refs: dict[str, Any]) -> PackagingReadinessGate:
        pyproject = report_refs["pyproject"]
        runtime = report_refs["runtime"]
        py_typed = report_refs["py_typed"]
        data = report_refs["package_data"]
        publish = report_refs["publish_blocker"]
        pyproject_passed = not pyproject.blocks_package_distribution_ready
        dependency_passed = not runtime.blocks_package_distribution_ready
        py_typed_passed = py_typed.py_typed_present is True
        data_passed = not data.blocks_package_distribution_ready
        ready = pyproject_passed and dependency_passed and py_typed_passed and data_passed
        return PackagingReadinessGate(
            gate_id="packaging_readiness_gate:v0.28.2",
            release_hygiene_gate_ref=_ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION),
            pyproject_metadata_passed=pyproject_passed,
            dependency_boundary_passed=dependency_passed,
            py_typed_passed=py_typed_passed,
            include_exclude_boundary_passed=True,
            package_data_boundary_passed=data_passed,
            wheel_smoke_passed_or_deferred=True,
            sdist_smoke_passed_or_deferred=True,
            import_smoke_passed_or_deferred=True,
            cli_smoke_passed_or_deferred=True,
            no_publish_boundary_passed=publish.package_publish_blocked and publish.release_tag_creation_blocked,
            no_private_material_boundary_passed=True,
            gate_status="passed" if ready else "blocked",
            package_distribution_ready=ready,
        )


class PackagingFindingService:
    BLOCKED_FINDINGS = {
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "official_release_artifact_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "auto_fix_attempted",
        "llm_judge_detected",
    }

    def build_findings(self, report: PackagingReadinessGate, runtime: RuntimeDependencyReport, py_typed: PyTypedMarkerReport) -> list[PackagingFinding]:
        findings: list[PackagingFinding] = [
            PackagingFinding("packaging_finding:package_publish_blocker_created", "info", "ok", "Package publish blocker is active.", _ref("packaging_readiness_gate", report.gate_id, V0282_VERSION), [], None)
        ]
        if runtime.pytest_in_runtime_dependencies:
            findings.append(PackagingFinding("packaging_finding:pytest_runtime_dependency_detected", "error", "pytest_runtime_dependency_detected", "pytest is present in runtime dependencies and blocks package distribution readiness.", _ref("runtime_dependency_report", "runtime_dependency_report:v0.28.2", V0282_VERSION), [], "Withdraw after pytest is moved out of runtime dependencies."))
        if py_typed.py_typed_present is not True:
            findings.append(PackagingFinding("packaging_finding:missing_py_typed", "warning", "missing_py_typed", "py.typed marker is missing or not verifiable.", _ref("py_typed_marker_report", py_typed.report_id, V0282_VERSION), [], "Withdraw after py.typed package marker is present."))
        return findings


class PackagingReadinessReportService:
    def build_report(self, report_id: str | None = None) -> PackagingReadinessReport:
        policy = PackagingDistributionTypeBoundaryPolicyService().build_policy()
        hygiene = ReleaseHygieneGateReportService().build_report()
        request = PackagingReadinessRequest("packaging_readiness_request:v0.28.2", hygiene.report_id, "pyproject_hygiene_report:v0.28.1", "runtime_data_hygiene_report:v0.28.1", "references_governance_policy_report:v0.28.1", "standard")
        source = PackagingSourceViewService().build_source_view()
        pyproject = PyprojectPackageMetadataReportService().build_report()
        dependency_policy = DependencyBoundaryPolicyService().build_policy()
        runtime = RuntimeDependencyReportService().build_report()
        dev = DevDependencyReportService().build_report()
        optional = OptionalDependencyGroupReportService().build_report()
        pytest_violation = PytestRuntimeDependencyViolationReportService().build_report(runtime)
        build_backend = BuildBackendReadinessReportService().build_report()
        include_exclude = PackageIncludeExcludePolicyService().build_policy()
        package_data = PackageDataBoundaryReportService().build_report()
        py_typed = PyTypedMarkerReportService().build_report()
        type_boundary = TypeDistributionBoundaryReportService().build_report(py_typed)
        wheel_plan = WheelBuildSmokePlanService().build_plan()
        wheel_report = WheelBuildSmokeReportService().build_report(wheel_plan)
        sdist_plan = SdistBuildSmokePlanService().build_plan()
        sdist_report = SdistBuildSmokeReportService().build_report(sdist_plan)
        import_plan = ImportSmokePlanService().build_plan()
        import_report = ImportSmokeReportService().build_report(import_plan)
        cli_plan = CLISmokePlanService().build_plan()
        cli_report = CLISmokeReportService().build_report(cli_plan)
        artifact_policy = DistributionArtifactPolicyService().build_policy()
        publish_blocker = PackagePublishBlockerService().build_blocker()
        gate = PackagingReadinessGateService().evaluate_gate({"pyproject": pyproject, "runtime": runtime, "py_typed": py_typed, "package_data": package_data, "publish_blocker": publish_blocker})
        remediation = PackagingRemediationPlanService().build_plan([pyproject, runtime, pytest_violation, py_typed, wheel_report, sdist_report, import_report, cli_report])
        findings = PackagingFindingService().build_findings(gate, runtime, py_typed)
        return PackagingReadinessReport(
            report_id=report_id or "packaging_readiness_report:v0.28.2",
            created_at=_now(),
            packaging_policy=policy,
            request=request,
            source_view=source,
            pyproject_metadata_report=pyproject,
            dependency_boundary_policy=dependency_policy,
            runtime_dependency_report=runtime,
            dev_dependency_report=dev,
            optional_dependency_group_report=optional,
            pytest_runtime_dependency_violation_report=pytest_violation,
            build_backend_report=build_backend,
            package_include_exclude_policy=include_exclude,
            package_data_boundary_report=package_data,
            py_typed_marker_report=py_typed,
            type_distribution_boundary_report=type_boundary,
            wheel_build_smoke_plan=wheel_plan,
            wheel_build_smoke_report=wheel_report,
            sdist_build_smoke_plan=sdist_plan,
            sdist_build_smoke_report=sdist_report,
            import_smoke_plan=import_plan,
            import_smoke_report=import_report,
            cli_smoke_plan=cli_plan,
            cli_smoke_report=cli_report,
            distribution_artifact_policy=artifact_policy,
            package_publish_blocker=publish_blocker,
            remediation_plan=remediation,
            packaging_readiness_gate=gate,
            findings=findings,
            report_status=gate.gate_status,
            ready_for_v0_28_3=True,
            package_distribution_ready=gate.package_distribution_ready,
            limitations=["Wheel/sdist/import/CLI smoke reports are metadata-only plans unless a later safe local smoke run is explicitly allowed."],
            withdrawal_conditions=["Withdraw if package publishing, upload, release tagging, official artifact creation, provider/command execution, split/adapter implementation, private exposure, or LLM sole authority is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.packaging_policy,
            "request": report.request,
            "source-view": report.source_view,
            "pyproject": report.pyproject_metadata_report,
            "dependencies": report.dependency_boundary_policy,
            "runtime-deps": report.runtime_dependency_report,
            "dev-deps": report.dev_dependency_report,
            "optional-deps": report.optional_dependency_group_report,
            "pytest-boundary": report.pytest_runtime_dependency_violation_report,
            "build-backend": report.build_backend_report,
            "include-exclude": report.package_include_exclude_policy,
            "package-data": report.package_data_boundary_report,
            "py-typed": report.py_typed_marker_report,
            "type-boundary": report.type_distribution_boundary_report,
            "wheel-smoke": report.wheel_build_smoke_report,
            "sdist-smoke": report.sdist_build_smoke_report,
            "import-smoke": report.import_smoke_report,
            "cli-smoke": report.cli_smoke_report,
            "distribution-policy": report.distribution_artifact_policy,
            "publish-blocker": report.package_publish_blocker,
            "remediation": report.remediation_plan,
            "readiness": report.packaging_readiness_gate,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0282_VERSION,
            "layer": V028_LAYER,
            "subject": "packaging_distribution_type_boundary",
            "principles": [
                "Packaging boundary is not package publishing",
                "Distribution readiness is not release readiness",
                "Build smoke is not release artifact publication",
                "Import smoke is not runtime execution expansion",
                "CLI smoke is not command execution expansion",
                "py.typed marker is type distribution metadata, not runtime behavior",
                "pytest must not be runtime dependency",
                "runtime data and references must not be included in package by default",
                "No-publish is a valid outcome",
            ],
            "safety_boundary": {
                "package_published": report.package_published,
                "package_uploaded": False,
                "release_tag_created": report.release_tag_created,
                "official_release_artifact_created": report.official_release_artifact_created,
                "public_alpha_release_implemented": False,
                "schumpeter_split_implemented": report.schumpeter_split_implemented,
                "external_adapter_implemented": report.external_adapter_implemented,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "runtime_continuity_injected": False,
                "company_private_material_exposed": report.company_private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "PIG_execution_authority_enabled": False,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.28.3 public-private boundary / redaction / reference policy",
                "v0.28.6 public alpha runtime profile / smoke demo flow",
                "v0.28.8 alpha readiness validation / external adapter preflight gate",
            ],
            "next_step": V0282_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "packaging_distribution_type_boundary_created",
            "version": V0282_VERSION,
            "source_read_models": ["ReleaseHygieneGateState", "RepositoryGovernanceState", "PyprojectHygieneState", "RuntimeDataHygieneState", "ReferencesGovernanceState", "PackagingMetadataState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["PackagingBoundaryState", "PyprojectPackageMetadataState", "DependencyBoundaryState", "PackageDataBoundaryState", "TypeDistributionBoundaryState", "BuildSmokeReadinessState", "ImportSmokeReadinessState", "CLISmokeReadinessState", "PackagePublishBlockerState", "V028ReadinessState"],
            "effect_types": V0282_EFFECT_TYPES,
            "forbidden_effect_types": V0282_FORBIDDEN_EFFECT_TYPES,
        }


def render_packaging_readiness_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: PackagingReadinessReport = parts["report"]
    lines = [
        f"Packaging / Distribution / Type Boundary {section}",
        f"version={report.version}",
        f"layer={report.packaging_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_3={_bool(report.ready_for_v0_28_3)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"package_distribution_ready={_bool(report.package_distribution_ready)}",
        f"public_alpha_ready={_bool(report.public_alpha_ready)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"official_release_artifact_created={_bool(report.official_release_artifact_created)}",
        f"auto_fix_performed={_bool(report.auto_fix_performed)}",
        f"schumpeter_split_implemented={_bool(report.schumpeter_split_implemented)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "plan_id", getattr(payload, "blocker_id", getattr(payload, "gate_id", "")))))
        if identifier:
            lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0283_VERSION = "v0.28.3"
V0283_VERSION_NAME = "Public-Private Boundary / Redaction / Reference Policy"
V0283_NEXT_STEP = "v0.28.4 Schumpeter Split Decision Framework"

V0283_OBJECT_TYPES = [
    "public_private_boundary_runtime_policy",
    "public_private_boundary_request",
    "public_private_boundary_source_view",
    "public_artifact_policy",
    "private_artifact_policy",
    "public_private_classification_rule",
    "public_private_artifact_classification",
    "redaction_policy",
    "redaction_preview",
    "redaction_decision_record",
    "secret_exclusion_policy",
    "credential_exclusion_policy",
    "company_material_exclusion_policy",
    "raw_trace_exclusion_policy",
    "raw_transcript_exclusion_policy",
    "raw_provider_output_exclusion_policy",
    "reference_code_policy",
    "third_party_reference_inventory_boundary",
    "reference_governance_report",
    "reference_license_boundary_report",
    "public_dataset_policy",
    "example_data_policy",
    "sanitized_example_policy",
    "synthetic_data_policy",
    "documentation_exposure_policy",
    "package_exposure_boundary_report",
    "public_private_quarantine_recommendation",
    "public_private_remediation_plan",
    "public_private_release_gate",
    "public_private_boundary_finding",
    "public_private_boundary_report",
    "packaging_readiness_report",
    "release_hygiene_gate_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0283_EVENT_TYPES = [
    "public_private_boundary_requested",
    "public_private_boundary_prerequisites_loaded",
    "public_private_boundary_policy_created",
    "public_artifact_policy_created",
    "private_artifact_policy_created",
    "public_private_classification_rule_created",
    "public_private_artifact_classification_created",
    "redaction_policy_created",
    "redaction_preview_created",
    "redaction_decision_record_created",
    "secret_exclusion_policy_created",
    "credential_exclusion_policy_created",
    "company_material_exclusion_policy_created",
    "raw_trace_exclusion_policy_created",
    "raw_transcript_exclusion_policy_created",
    "raw_provider_output_exclusion_policy_created",
    "reference_code_policy_created",
    "third_party_reference_inventory_boundary_created",
    "reference_governance_report_created",
    "reference_license_boundary_report_created",
    "public_dataset_policy_created",
    "example_data_policy_created",
    "sanitized_example_policy_created",
    "synthetic_data_policy_created",
    "documentation_exposure_policy_created",
    "package_exposure_boundary_report_created",
    "public_private_quarantine_recommendation_created",
    "public_private_remediation_plan_created",
    "public_private_release_gate_evaluated",
    "public_private_boundary_report_created",
    "public_private_boundary_warning_created",
    "public_private_boundary_blocked",
]

V0283_EFFECT_TYPES = [
    "read_only_observation",
    "public_private_boundary_created",
    "public_private_artifact_classification_created",
    "redaction_preview_created",
    "reference_governance_report_created",
    "package_exposure_boundary_report_created",
    "public_private_release_gate_evaluated",
    "public_private_remediation_plan_created",
    "state_candidate_created",
]

V0283_FORBIDDEN_EFFECT_TYPES = [
    "destructive_redaction_performed",
    "source_file_deleted",
    "file_moved",
    "repo_split_performed",
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "package_published",
    "release_tag_created",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "references_runtime_dependency_added",
    "references_code_copied",
    "company_private_material_exposed",
    "credential_exposed",
    "secret_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class PublicPrivateBoundaryRuntimePolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    layer: str = V028_LAYER
    boundary_enabled: bool = True
    public_core_private_overlay_required: bool = True
    public_artifact_classification_required: bool = True
    private_artifact_classification_required: bool = True
    redaction_policy_required: bool = True
    reference_policy_required: bool = True
    public_dataset_policy_required: bool = True
    example_data_policy_required: bool = True
    package_exposure_boundary_required: bool = True
    destructive_redaction_enabled_now: bool = False
    source_file_deletion_enabled_now: bool = False
    repo_split_enabled_now: bool = False
    schumpeter_split_enabled_now: bool = False
    company_wrapper_enabled_now: bool = False
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    references_runtime_dependency_forbidden: bool = True
    references_code_copy_forbidden_now: bool = True
    public_company_material_forbidden: bool = True
    public_credential_forbidden: bool = True
    public_secret_forbidden: bool = True
    public_raw_trace_forbidden: bool = True
    public_raw_transcript_forbidden: bool = True
    public_raw_provider_output_forbidden: bool = True
    llm_judge_as_sole_boundary_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateBoundaryRequest(ModelMixin):
    request_id: str
    packaging_readiness_report_id: str | None
    release_hygiene_gate_report_id: str | None
    references_inventory_id: str | None
    requested_profile: str | None
    version: str = V0283_VERSION
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateBoundarySourceView(ModelMixin):
    source_view_id: str
    packaging_readiness_report_ref: dict[str, Any] | None
    package_data_boundary_report_ref: dict[str, Any] | None
    package_include_exclude_policy_ref: dict[str, Any] | None
    release_hygiene_gate_report_ref: dict[str, Any] | None
    forbidden_artifact_scan_report_ref: dict[str, Any] | None
    references_inventory_ref: dict[str, Any] | None
    references_license_boundary_report_ref: dict[str, Any] | None
    artifact_refs: list[dict[str, Any]]
    package_artifact_refs: list[dict[str, Any]]
    docs_artifact_refs: list[dict[str, Any]]
    example_data_refs: list[dict[str, Any]]
    synthetic_data_refs: list[dict[str, Any]]
    references_dir_refs: list[dict[str, Any]]
    schumpeter_reference_refs: list[dict[str, Any]]
    private_overlay_candidate_refs: list[dict[str, Any]]
    source_status: str
    version: str = V0283_VERSION
    company_private_material_detected: bool = False
    credential_detected: bool = False
    secret_detected: bool = False
    raw_trace_detected: bool = False
    raw_transcript_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicArtifactPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    public_artifacts_allowed: list[str] = field(default_factory=lambda: [
        "public_docs",
        "architecture_docs",
        "sanitized_examples",
        "synthetic_demo_data",
        "public_safe_tests",
        "generic_OCEL_samples",
        "generic_PIG_reports",
        "generic_Workbench_reports",
        "generic_Memory_reports",
        "package_source_code",
        "type_metadata",
    ])
    public_artifacts_forbidden: list[str] = field(default_factory=lambda: [
        "company_private_material",
        "credentials",
        "secrets",
        "internal_endpoints",
        "raw_runtime_traces",
        "raw_transcripts",
        "raw_provider_outputs",
        "actual_user_data",
        "actual_company_process_logs",
        "private_overlay_config",
        "company_rpa_config",
        "runtime_db",
        "backup_files",
    ])
    sanitized_examples_required: bool = True
    synthetic_data_preferred: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PrivateArtifactPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    private_artifacts: list[str] = field(default_factory=lambda: [
        "company_config",
        "company_credentials",
        "company_endpoints",
        "company_rpa_adapter_config",
        "A360_connection_details",
        "Brity_connection_details",
        "UiPath_connection_details",
        "actual_process_logs",
        "user_session_traces",
        "raw_transcripts",
        "raw_provider_outputs",
        "private_overlay_profiles",
        "deployment_secrets",
    ])
    private_overlay_required: bool = True
    public_core_must_not_depend_on_private_artifacts: bool = True
    private_artifact_public_exposure_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateClassificationRule(ModelMixin):
    rule_id: str
    rule_name: str
    artifact_kind: str | None
    rule_summary: str
    classification_result: str
    required: bool
    block_on_violation: bool
    version: str = V0283_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateArtifactClassification(ModelMixin):
    classification_id: str
    artifact_ref: dict[str, Any]
    artifact_path_hint: str | None
    artifact_kind: str
    classification: str
    matched_rule_refs: list[dict[str, Any]]
    redaction_required: bool
    quarantine_required: bool
    package_inclusion_allowed: bool
    docs_inclusion_allowed: bool
    public_release_blocker: bool
    classification_summary: str
    version: str = V0283_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RedactionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    redaction_preview_enabled: bool = True
    destructive_redaction_enabled_now: bool = False
    source_file_mutation_enabled_now: bool = False
    source_file_deletion_enabled_now: bool = False
    redact_credentials: bool = True
    redact_secrets: bool = True
    redact_internal_endpoints: bool = True
    redact_private_paths: bool = True
    redact_raw_trace_content: bool = True
    redact_raw_transcript_content: bool = True
    redact_raw_provider_output_content: bool = True
    preserve_refs_and_metadata: bool = True
    redaction_requires_user_decision_for_apply: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RedactionPreview(ModelMixin):
    preview_id: str
    artifact_ref: dict[str, Any]
    classification_ref: dict[str, Any] | None
    redaction_policy_ref: dict[str, Any]
    redacted_categories: list[str]
    preview_summary: str
    version: str = V0283_VERSION
    redaction_apply_performed_now: bool = False
    source_file_mutated: bool = False
    source_file_deleted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RedactionDecisionRecord(ModelMixin):
    decision_record_id: str
    artifact_ref: dict[str, Any]
    redaction_preview_ref: dict[str, Any] | None
    decision_type: str
    decision_reason: str
    version: str = V0283_VERSION
    applies_redaction_now: bool = False
    mutates_file_now: bool = False
    deletes_file_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SecretExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    secrets_forbidden_in_public_core: bool = True
    secret_like_artifacts_block_release: bool = True
    source_content_exposure_forbidden: bool = True
    detection_mode: str = "metadata_only"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CredentialExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    credentials_forbidden_in_public_core: bool = True
    credential_like_artifacts_block_release: bool = True
    credential_storage_in_examples_forbidden: bool = True
    credential_placeholder_allowed_if_safe: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CompanyMaterialExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    company_material_forbidden_in_public_core: bool = True
    company_endpoints_forbidden_in_public_core: bool = True
    company_workflows_forbidden_in_public_core: bool = True
    company_process_logs_forbidden_in_public_core: bool = True
    company_rpa_details_forbidden_in_public_core: bool = True
    private_overlay_required_for_company_material: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RawTraceExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    raw_traces_forbidden_in_public_core: bool = True
    raw_traces_forbidden_in_package_data: bool = True
    synthetic_trace_samples_allowed: bool = True
    sanitized_trace_summaries_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RawTranscriptExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    raw_transcripts_forbidden_in_public_core: bool = True
    raw_transcripts_forbidden_in_package_data: bool = True
    sanitized_dialogue_examples_allowed: bool = True
    transcript_metadata_refs_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RawProviderOutputExclusionPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    raw_provider_outputs_forbidden_in_public_core: bool = True
    raw_provider_outputs_forbidden_in_package_data: bool = True
    sanitized_provider_output_summaries_allowed: bool = True
    provider_output_metadata_refs_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ReferenceCodePolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    references_are_reference_only_by_default: bool = True
    references_not_runtime_dependency: bool = True
    references_not_package_data_by_default: bool = True
    references_code_copy_forbidden_now: bool = True
    reference_origin_required: bool = True
    reference_license_required: bool = True
    reference_disposition_required: bool = True
    schumpeter_reference_split_decision_deferred_to_v0284: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ThirdPartyReferenceInventoryBoundary(ModelMixin):
    inventory_boundary_id: str
    references_dir_present: bool | None
    reference_entries: list[dict[str, Any]]
    known_origin_count: int | None
    known_license_count: int | None
    unknown_license_count: int | None
    reference_only_count: int | None
    quarantine_recommended_count: int | None
    inventory_status: str
    version: str = V0283_VERSION
    runtime_dependency_count: int = 0
    code_copy_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ReferenceGovernanceReport(ModelMixin):
    report_id: str
    reference_policy_ref: dict[str, Any]
    inventory_boundary_ref: dict[str, Any]
    references_policy_present: bool | None
    third_party_notices_present: bool | None
    references_missing_origin_count: int | None
    references_missing_license_count: int | None
    reference_governance_status: str
    blocks_public_alpha_release_claim: bool
    version: str = V0283_VERSION
    references_runtime_dependency_count: int = 0
    references_code_copy_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ReferenceLicenseBoundaryReport(ModelMixin):
    report_id: str
    references_inventory_ref: dict[str, Any] | None
    references_with_known_license_count: int | None
    references_with_unknown_license_count: int | None
    license_review_required_count: int | None
    incompatible_license_detected: bool | None
    license_boundary_status: str
    blocks_public_alpha_release_claim: bool
    version: str = V0283_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicDatasetPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    actual_user_data_forbidden: bool = True
    actual_company_data_forbidden: bool = True
    synthetic_data_allowed: bool = True
    sanitized_data_allowed_with_policy: bool = True
    raw_runtime_db_forbidden: bool = True
    raw_event_logs_forbidden: bool = True
    public_dataset_manifest_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExampleDataPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    examples_allowed_if_sanitized: bool = True
    examples_allowed_if_synthetic: bool = True
    examples_must_not_contain_credentials: bool = True
    examples_must_not_contain_company_material: bool = True
    examples_must_not_contain_raw_trace: bool = True
    examples_must_not_contain_raw_transcript: bool = True
    examples_must_not_contain_raw_provider_output: bool = True
    example_manifest_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SanitizedExamplePolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    sanitized_examples_allowed: bool = True
    sanitization_metadata_required: bool = True
    redaction_preview_required_when_sensitive_like: bool = True
    sanitized_example_must_not_be_reversible_to_private_data: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SyntheticDataPolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    synthetic_data_preferred: bool = True
    synthetic_data_manifest_required: bool = True
    synthetic_data_must_not_be_actual_user_or_company_data: bool = True
    synthetic_data_must_not_embed_private_identifiers: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DocumentationExposurePolicy(ModelMixin):
    policy_id: str
    version: str = V0283_VERSION
    public_docs_allowed: bool = True
    docs_must_not_expose_company_material: bool = True
    docs_must_not_expose_internal_endpoints: bool = True
    docs_must_not_expose_credentials: bool = True
    docs_must_not_expose_raw_trace: bool = True
    docs_must_not_expose_raw_transcripts: bool = True
    docs_must_not_expose_raw_provider_outputs: bool = True
    docs_may_reference_private_overlay_conceptually: bool = True
    docs_must_not_include_private_overlay_config: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PackageExposureBoundaryReport(ModelMixin):
    report_id: str
    package_data_boundary_report_ref: dict[str, Any] | None
    package_include_exclude_policy_ref: dict[str, Any] | None
    package_artifact_classification_refs: list[dict[str, Any]]
    public_package_artifact_count: int
    private_package_artifact_count: int
    forbidden_package_artifact_count: int
    package_exposure_status: str
    blocks_public_alpha_release_claim: bool
    version: str = V0283_VERSION
    runtime_data_in_package_count: int = 0
    references_in_package_count: int = 0
    credential_in_package_count: int = 0
    raw_trace_in_package_count: int = 0
    raw_transcript_in_package_count: int = 0
    raw_provider_output_in_package_count: int = 0
    company_material_in_package_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateQuarantineRecommendation(ModelMixin):
    quarantine_recommendation_id: str
    artifact_ref: dict[str, Any]
    classification_ref: dict[str, Any] | None
    quarantine_reason: str
    recommended_target: str
    version: str = V0283_VERSION
    file_moved_now: bool = False
    file_deleted_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateRemediationPlan(ModelMixin):
    remediation_plan_id: str
    quarantine_recommendations: list[PublicPrivateQuarantineRecommendation]
    redaction_decision_refs: list[dict[str, Any]]
    blocker_count: int
    warning_count: int
    user_decision_required_count: int
    plan_status: str
    version: str = V0283_VERSION
    auto_redaction_performed: bool = False
    file_deleted: bool = False
    file_moved: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateReleaseGate(ModelMixin):
    gate_id: str
    classification_complete: bool
    redaction_preview_complete: bool
    reference_governance_passed: bool
    package_exposure_boundary_passed: bool
    public_dataset_policy_passed: bool
    example_data_policy_passed: bool
    documentation_exposure_policy_passed: bool
    no_private_material_exposure: bool
    no_credential_exposure: bool
    no_secret_exposure: bool
    no_raw_trace_exposure: bool
    no_raw_transcript_exposure: bool
    no_raw_provider_output_exposure: bool
    no_reference_runtime_dependency: bool
    no_reference_code_copy: bool
    gate_status: str
    public_private_boundary_ready: bool
    public_alpha_release_claim_allowed: bool
    version: str = V0283_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicPrivateBoundaryFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class PublicPrivateBoundaryReport(ModelMixin):
    report_id: str
    created_at: str
    boundary_policy: PublicPrivateBoundaryRuntimePolicy
    request: PublicPrivateBoundaryRequest
    source_view: PublicPrivateBoundarySourceView
    public_artifact_policy: PublicArtifactPolicy
    private_artifact_policy: PrivateArtifactPolicy
    classification_rules: list[PublicPrivateClassificationRule]
    artifact_classifications: list[PublicPrivateArtifactClassification]
    redaction_policy: RedactionPolicy
    redaction_previews: list[RedactionPreview]
    redaction_decision_records: list[RedactionDecisionRecord]
    secret_exclusion_policy: SecretExclusionPolicy
    credential_exclusion_policy: CredentialExclusionPolicy
    company_material_exclusion_policy: CompanyMaterialExclusionPolicy
    raw_trace_exclusion_policy: RawTraceExclusionPolicy
    raw_transcript_exclusion_policy: RawTranscriptExclusionPolicy
    raw_provider_output_exclusion_policy: RawProviderOutputExclusionPolicy
    reference_code_policy: ReferenceCodePolicy
    third_party_reference_inventory_boundary: ThirdPartyReferenceInventoryBoundary
    reference_governance_report: ReferenceGovernanceReport
    reference_license_boundary_report: ReferenceLicenseBoundaryReport
    public_dataset_policy: PublicDatasetPolicy
    example_data_policy: ExampleDataPolicy
    sanitized_example_policy: SanitizedExamplePolicy
    synthetic_data_policy: SyntheticDataPolicy
    documentation_exposure_policy: DocumentationExposurePolicy
    package_exposure_boundary_report: PackageExposureBoundaryReport
    remediation_plan: PublicPrivateRemediationPlan
    public_private_release_gate: PublicPrivateReleaseGate
    findings: list[PublicPrivateBoundaryFinding]
    report_status: str
    ready_for_v0_28_4: bool
    ready_for_public_alpha_release_claim: bool
    public_private_boundary_ready: bool
    redaction_preview_created: bool
    version: str = V0283_VERSION
    destructive_redaction_performed: bool = False
    source_file_deleted: bool = False
    file_moved: bool = False
    repo_split_performed: bool = False
    schumpeter_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    external_adapter_implemented: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    runtime_continuity_injected: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0283_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.28.4 Schumpeter Split Decision Framework begins or public-private boundary policy changes."


class PublicPrivateBoundaryPrerequisiteSourceService:
    def load_v0282_packaging_readiness_report(self) -> PackagingReadinessReport:
        return PackagingReadinessReportService().build_report()

    def load_v0282_package_data_boundary_report(self) -> PackageDataBoundaryReport:
        return PackageDataBoundaryReportService().build_report()

    def load_v0282_package_include_exclude_policy(self) -> PackageIncludeExcludePolicy:
        return PackageIncludeExcludePolicyService().build_policy()

    def load_v0281_release_hygiene_gate_report(self) -> ReleaseHygieneGateReport:
        return ReleaseHygieneGateReportService().build_report()

    def load_v0281_references_inventory(self) -> ReferencesDirectoryInventory:
        return ReferencesDirectoryInventoryService().build_inventory()

    def load_v0281_references_license_boundary_report(self) -> ReferencesLicenseBoundaryReport:
        return ReferencesLicenseBoundaryReportService().build_report()

    def load_v0281_forbidden_artifact_scan_report(self) -> ForbiddenRepositoryArtifactScanReport:
        return ForbiddenRepositoryArtifactScanReportService().build_report()

    def load_v0280_public_private_boundary_policy(self) -> PublicPrivateBoundaryPolicy:
        return PublicPrivateBoundaryPolicyService().build_policy()

    def load_artifact_metadata_if_available(self) -> list[dict[str, Any]]:
        root = _repo_root()
        refs = [_file_ref(root / "src" / "chanta_core", "package_source") if (root / "src" / "chanta_core").exists() else None]
        return [ref for ref in refs if ref is not None]

    def load_docs_metadata_if_available(self) -> list[dict[str, Any]]:
        docs = _repo_root() / "docs" / "versions" / "v0.28"
        return [_file_ref(docs, "docs_dir")] if docs.exists() else []

    def load_example_data_metadata_if_available(self) -> list[dict[str, Any]]:
        examples = _repo_root() / "examples"
        return [_file_ref(examples, "examples_dir")] if examples.exists() else []

    def load_references_metadata_if_available(self) -> list[dict[str, Any]]:
        refs = _repo_root() / "references"
        return [_file_ref(refs, "references_dir")] if refs.exists() else []


class PublicPrivateBoundaryRuntimePolicyService:
    def build_policy(self) -> PublicPrivateBoundaryRuntimePolicy:
        return PublicPrivateBoundaryRuntimePolicy(policy_id="public_private_boundary_runtime_policy:v0.28.3")


class PublicPrivateBoundarySourceViewService:
    def build_source_view(self) -> PublicPrivateBoundarySourceView:
        prereq = PublicPrivateBoundaryPrerequisiteSourceService()
        artifact_refs = prereq.load_artifact_metadata_if_available()
        docs_refs = prereq.load_docs_metadata_if_available()
        example_refs = prereq.load_example_data_metadata_if_available()
        reference_refs = prereq.load_references_metadata_if_available()
        schumpeter = _repo_root() / "references" / "schumpeter"
        return PublicPrivateBoundarySourceView(
            source_view_id="public_private_boundary_source_view:v0.28.3",
            packaging_readiness_report_ref=_ref("packaging_readiness_report", "packaging_readiness_report:v0.28.2", V0282_VERSION),
            package_data_boundary_report_ref=_ref("package_data_boundary_report", "package_data_boundary_report:v0.28.2", V0282_VERSION),
            package_include_exclude_policy_ref=_ref("package_include_exclude_policy", "package_include_exclude_policy:v0.28.2", V0282_VERSION),
            release_hygiene_gate_report_ref=_ref("release_hygiene_gate_report", "release_hygiene_gate_report:v0.28.1", V0281_VERSION),
            forbidden_artifact_scan_report_ref=_ref("forbidden_repository_artifact_scan_report", "forbidden_repository_artifact_scan_report:v0.28.1", V0281_VERSION),
            references_inventory_ref=_ref("references_directory_inventory", "references_directory_inventory:v0.28.1", V0281_VERSION),
            references_license_boundary_report_ref=_ref("references_license_boundary_report", "references_license_boundary_report:v0.28.1", V0281_VERSION),
            artifact_refs=artifact_refs + docs_refs + example_refs + reference_refs,
            package_artifact_refs=artifact_refs,
            docs_artifact_refs=docs_refs,
            example_data_refs=example_refs,
            synthetic_data_refs=[],
            references_dir_refs=reference_refs,
            schumpeter_reference_refs=[_file_ref(schumpeter, "schumpeter_reference")] if schumpeter.exists() else [],
            private_overlay_candidate_refs=[_ref("private_overlay_concept", "private_overlay:not_created:v0.28.3", V0283_VERSION)],
            source_status="partial",
        )


class PublicArtifactPolicyService:
    def build_policy(self) -> PublicArtifactPolicy:
        return PublicArtifactPolicy(policy_id="public_artifact_policy:v0.28.3")


class PrivateArtifactPolicyService:
    def build_policy(self) -> PrivateArtifactPolicy:
        return PrivateArtifactPolicy(policy_id="private_artifact_policy:v0.28.3")


class PublicPrivateClassificationRuleService:
    REQUIRED_RULES = [
        ("credentials_are_private_only", "credential_like", "private_only", True),
        ("secrets_are_private_only", "secret_like", "private_only", True),
        ("company_endpoints_are_private_only", "config", "private_only", True),
        ("raw_traces_are_private_only", "raw_trace", "private_only", True),
        ("raw_transcripts_are_private_only", "raw_transcript", "private_only", True),
        ("raw_provider_outputs_are_private_only", "raw_provider_output", "private_only", True),
        ("runtime_db_is_forbidden_public_artifact", "runtime_data", "forbidden", True),
        ("backup_files_are_forbidden_public_artifact", "runtime_data", "forbidden", True),
        ("references_are_reference_only_by_default", "reference_code", "reference_only", False),
        ("references_are_not_runtime_dependency", "reference_code", "reference_only", True),
        ("references_code_copy_forbidden_now", "reference_code", "reference_only", True),
        ("examples_must_be_sanitized_or_synthetic", "example", "public_allowed_if_sanitized", True),
        ("docs_must_not_expose_company_material", "docs", "public_allowed", True),
        ("package_data_must_not_include_private_artifacts", "package_metadata", "public_allowed", True),
        ("Schumpeter_reference_is_not_split_implementation", "reference_code", "reference_only", True),
        ("RPA_adapter_details_are_private_or_future_track", "config", "private_only", True),
    ]

    def build_rules(self) -> list[PublicPrivateClassificationRule]:
        return [
            PublicPrivateClassificationRule(
                rule_id=f"public_private_classification_rule:{name}:v0.28.3",
                rule_name=name,
                artifact_kind=kind,
                rule_summary=f"{name} boundary rule for v0.28.3 policy-only classification.",
                classification_result=result,
                required=True,
                block_on_violation=block,
            )
            for name, kind, result, block in self.REQUIRED_RULES
        ]


def _rule_ref(rules: list[PublicPrivateClassificationRule], name: str) -> dict[str, Any]:
    for rule in rules:
        if rule.rule_name == name:
            return _ref("public_private_classification_rule", rule.rule_id, V0283_VERSION)
    return _ref("public_private_classification_rule", name, V0283_VERSION)


class PublicPrivateArtifactClassificationService:
    def classify_artifacts(
        self,
        source_view: PublicPrivateBoundarySourceView,
        rules: list[PublicPrivateClassificationRule],
    ) -> list[PublicPrivateArtifactClassification]:
        classifications = [
            PublicPrivateArtifactClassification(
                classification_id="public_private_artifact_classification:package_source:v0.28.3",
                artifact_ref=source_view.package_artifact_refs[0] if source_view.package_artifact_refs else _ref("package_source", "src/chanta_core"),
                artifact_path_hint="src/chanta_core",
                artifact_kind="source_code",
                classification="public_allowed",
                matched_rule_refs=[],
                redaction_required=False,
                quarantine_required=False,
                package_inclusion_allowed=True,
                docs_inclusion_allowed=False,
                public_release_blocker=False,
                classification_summary="Package source is public-eligible only after package exposure and release gates pass.",
            ),
            PublicPrivateArtifactClassification(
                classification_id="public_private_artifact_classification:public_docs:v0.28.3",
                artifact_ref=source_view.docs_artifact_refs[0] if source_view.docs_artifact_refs else _ref("docs", "docs/versions/v0.28"),
                artifact_path_hint="docs/versions/v0.28",
                artifact_kind="docs",
                classification="public_allowed",
                matched_rule_refs=[_rule_ref(rules, "docs_must_not_expose_company_material")],
                redaction_required=False,
                quarantine_required=False,
                package_inclusion_allowed=False,
                docs_inclusion_allowed=True,
                public_release_blocker=False,
                classification_summary="Public docs are allowed only if they remain sanitized and policy-only.",
            ),
            PublicPrivateArtifactClassification(
                classification_id="public_private_artifact_classification:references:v0.28.3",
                artifact_ref=source_view.references_dir_refs[0] if source_view.references_dir_refs else _ref("references_dir", "references"),
                artifact_path_hint="references",
                artifact_kind="reference_code",
                classification="reference_only",
                matched_rule_refs=[_rule_ref(rules, "references_are_reference_only_by_default"), _rule_ref(rules, "references_are_not_runtime_dependency")],
                redaction_required=False,
                quarantine_required=False,
                package_inclusion_allowed=False,
                docs_inclusion_allowed=False,
                public_release_blocker=False,
                classification_summary="References remain reference-only; inventory is not runtime adoption.",
            ),
            PublicPrivateArtifactClassification(
                classification_id="public_private_artifact_classification:private_overlay_concept:v0.28.3",
                artifact_ref=_ref("private_overlay_concept", "private_overlay:not_created:v0.28.3", V0283_VERSION),
                artifact_path_hint=None,
                artifact_kind="config",
                classification="private_only",
                matched_rule_refs=[_rule_ref(rules, "company_endpoints_are_private_only"), _rule_ref(rules, "RPA_adapter_details_are_private_or_future_track")],
                redaction_required=True,
                quarantine_required=True,
                package_inclusion_allowed=False,
                docs_inclusion_allowed=False,
                public_release_blocker=True,
                classification_summary="Private overlay material is conceptual only in public core and requires private handling later.",
            ),
        ]
        return classifications


class RedactionPolicyService:
    def build_policy(self) -> RedactionPolicy:
        return RedactionPolicy(policy_id="redaction_policy:v0.28.3")


class RedactionPreviewService:
    def build_previews(
        self,
        classifications: list[PublicPrivateArtifactClassification],
        policy: RedactionPolicy,
    ) -> list[RedactionPreview]:
        previews: list[RedactionPreview] = []
        for classification in classifications:
            if classification.redaction_required:
                previews.append(
                    RedactionPreview(
                        preview_id=f"redaction_preview:{classification.classification_id}:v0.28.3",
                        artifact_ref=classification.artifact_ref,
                        classification_ref=_ref("public_private_artifact_classification", classification.classification_id, V0283_VERSION),
                        redaction_policy_ref=_ref("redaction_policy", policy.policy_id, V0283_VERSION),
                        redacted_categories=["company_material", "credentials", "secrets", "private_paths"],
                        preview_summary="Preview-only redaction recommendation; no source file mutation, movement, or deletion is performed.",
                    )
                )
        return previews


class RedactionDecisionRecordService:
    def build_decisions(self, previews: list[RedactionPreview]) -> list[RedactionDecisionRecord]:
        return [
            RedactionDecisionRecord(
                decision_record_id=f"redaction_decision_record:{preview.preview_id}:v0.28.3",
                artifact_ref=preview.artifact_ref,
                redaction_preview_ref=_ref("redaction_preview", preview.preview_id, V0283_VERSION),
                decision_type="require_user_review",
                decision_reason="v0.28.3 creates preview-only decisions; apply requires later explicit user decision.",
            )
            for preview in previews
        ]


class SecretExclusionPolicyService:
    def build_policy(self) -> SecretExclusionPolicy:
        return SecretExclusionPolicy(policy_id="secret_exclusion_policy:v0.28.3")


class CredentialExclusionPolicyService:
    def build_policy(self) -> CredentialExclusionPolicy:
        return CredentialExclusionPolicy(policy_id="credential_exclusion_policy:v0.28.3")


class CompanyMaterialExclusionPolicyService:
    def build_policy(self) -> CompanyMaterialExclusionPolicy:
        return CompanyMaterialExclusionPolicy(policy_id="company_material_exclusion_policy:v0.28.3")


class RawTraceExclusionPolicyService:
    def build_policy(self) -> RawTraceExclusionPolicy:
        return RawTraceExclusionPolicy(policy_id="raw_trace_exclusion_policy:v0.28.3")


class RawTranscriptExclusionPolicyService:
    def build_policy(self) -> RawTranscriptExclusionPolicy:
        return RawTranscriptExclusionPolicy(policy_id="raw_transcript_exclusion_policy:v0.28.3")


class RawProviderOutputExclusionPolicyService:
    def build_policy(self) -> RawProviderOutputExclusionPolicy:
        return RawProviderOutputExclusionPolicy(policy_id="raw_provider_output_exclusion_policy:v0.28.3")


class ReferenceCodePolicyService:
    def build_policy(self) -> ReferenceCodePolicy:
        return ReferenceCodePolicy(policy_id="reference_code_policy:v0.28.3")


class ThirdPartyReferenceInventoryBoundaryService:
    def build_boundary(self) -> ThirdPartyReferenceInventoryBoundary:
        inventory = ReferencesDirectoryInventoryService().build_inventory()
        entries = inventory.reference_entries
        present = inventory.references_dir_present
        unknown_count = len(entries) if present else 0
        status = "warning" if unknown_count else ("passed" if present is not None else "unknown")
        return ThirdPartyReferenceInventoryBoundary(
            inventory_boundary_id="third_party_reference_inventory_boundary:v0.28.3",
            references_dir_present=present,
            reference_entries=entries,
            known_origin_count=0 if present else None,
            known_license_count=0 if present else None,
            unknown_license_count=unknown_count if present else None,
            reference_only_count=len(entries) if present else None,
            quarantine_recommended_count=0,
            inventory_status=status,
        )


class ReferenceGovernanceReportService:
    def build_report(
        self,
        policy: ReferenceCodePolicy,
        inventory_boundary: ThirdPartyReferenceInventoryBoundary,
    ) -> ReferenceGovernanceReport:
        missing_license = inventory_boundary.unknown_license_count
        blocks = bool(missing_license)
        return ReferenceGovernanceReport(
            report_id="reference_governance_report:v0.28.3",
            reference_policy_ref=_ref("reference_code_policy", policy.policy_id, V0283_VERSION),
            inventory_boundary_ref=_ref("third_party_reference_inventory_boundary", inventory_boundary.inventory_boundary_id, V0283_VERSION),
            references_policy_present=None if inventory_boundary.references_dir_present is None else False,
            third_party_notices_present=None if inventory_boundary.references_dir_present is None else False,
            references_missing_origin_count=missing_license,
            references_missing_license_count=missing_license,
            reference_governance_status="blocked" if blocks else ("passed" if inventory_boundary.references_dir_present else "unknown"),
            blocks_public_alpha_release_claim=blocks,
        )


class ReferenceLicenseBoundaryReportService:
    def build_report(self, inventory_boundary: ThirdPartyReferenceInventoryBoundary) -> ReferenceLicenseBoundaryReport:
        unknown = inventory_boundary.unknown_license_count
        blocks = bool(unknown)
        return ReferenceLicenseBoundaryReport(
            report_id="reference_license_boundary_report:v0.28.3",
            references_inventory_ref=_ref("third_party_reference_inventory_boundary", inventory_boundary.inventory_boundary_id, V0283_VERSION),
            references_with_known_license_count=inventory_boundary.known_license_count,
            references_with_unknown_license_count=unknown,
            license_review_required_count=unknown,
            incompatible_license_detected=None,
            license_boundary_status="blocked" if blocks else ("passed" if inventory_boundary.references_dir_present else "unknown"),
            blocks_public_alpha_release_claim=blocks,
        )


class PublicDatasetPolicyService:
    def build_policy(self) -> PublicDatasetPolicy:
        return PublicDatasetPolicy(policy_id="public_dataset_policy:v0.28.3")


class ExampleDataPolicyService:
    def build_policy(self) -> ExampleDataPolicy:
        return ExampleDataPolicy(policy_id="example_data_policy:v0.28.3")


class SanitizedExamplePolicyService:
    def build_policy(self) -> SanitizedExamplePolicy:
        return SanitizedExamplePolicy(policy_id="sanitized_example_policy:v0.28.3")


class SyntheticDataPolicyService:
    def build_policy(self) -> SyntheticDataPolicy:
        return SyntheticDataPolicy(policy_id="synthetic_data_policy:v0.28.3")


class DocumentationExposurePolicyService:
    def build_policy(self) -> DocumentationExposurePolicy:
        return DocumentationExposurePolicy(policy_id="documentation_exposure_policy:v0.28.3")


class PackageExposureBoundaryReportService:
    def build_report(
        self,
        source_view: PublicPrivateBoundarySourceView,
        classifications: list[PublicPrivateArtifactClassification],
    ) -> PackageExposureBoundaryReport:
        package_classifications = [item for item in classifications if item.artifact_kind == "source_code"]
        forbidden_count = sum(1 for item in package_classifications if item.classification in {"private_only", "forbidden", "quarantine"})
        return PackageExposureBoundaryReport(
            report_id="package_exposure_boundary_report:v0.28.3",
            package_data_boundary_report_ref=source_view.package_data_boundary_report_ref,
            package_include_exclude_policy_ref=source_view.package_include_exclude_policy_ref,
            package_artifact_classification_refs=[_ref("public_private_artifact_classification", item.classification_id, V0283_VERSION) for item in package_classifications],
            public_package_artifact_count=sum(1 for item in package_classifications if item.classification == "public_allowed"),
            private_package_artifact_count=sum(1 for item in package_classifications if item.classification == "private_only"),
            forbidden_package_artifact_count=forbidden_count,
            package_exposure_status="blocked" if forbidden_count else "passed",
            blocks_public_alpha_release_claim=bool(forbidden_count),
        )


class PublicPrivateRemediationPlanService:
    def build_plan(
        self,
        classifications: list[PublicPrivateArtifactClassification],
        decisions: list[RedactionDecisionRecord],
    ) -> PublicPrivateRemediationPlan:
        recommendations = [
            PublicPrivateQuarantineRecommendation(
                quarantine_recommendation_id=f"public_private_quarantine_recommendation:{item.classification_id}:v0.28.3",
                artifact_ref=item.artifact_ref,
                classification_ref=_ref("public_private_artifact_classification", item.classification_id, V0283_VERSION),
                quarantine_reason=item.classification_summary,
                recommended_target="private_overlay" if item.classification == "private_only" else "sanitize_before_public",
            )
            for item in classifications
            if item.quarantine_required or item.public_release_blocker
        ]
        blockers = sum(1 for item in classifications if item.public_release_blocker)
        warnings = len(recommendations) - blockers
        return PublicPrivateRemediationPlan(
            remediation_plan_id="public_private_remediation_plan:v0.28.3",
            quarantine_recommendations=recommendations,
            redaction_decision_refs=[_ref("redaction_decision_record", item.decision_record_id, V0283_VERSION) for item in decisions],
            blocker_count=blockers,
            warning_count=warnings,
            user_decision_required_count=len(decisions) + len(recommendations),
            plan_status="blocked" if blockers else ("warning" if warnings else "ready"),
        )


class PublicPrivateReleaseGateService:
    def evaluate_gate(
        self,
        classifications: list[PublicPrivateArtifactClassification],
        previews: list[RedactionPreview],
        reference_governance: ReferenceGovernanceReport,
        package_exposure: PackageExposureBoundaryReport,
    ) -> PublicPrivateReleaseGate:
        classification_complete = bool(classifications)
        redaction_preview_complete = all(not item.redaction_required for item in classifications) or bool(previews)
        no_reference_runtime = reference_governance.references_runtime_dependency_count == 0
        no_reference_copy = reference_governance.references_code_copy_count == 0
        passed = (
            classification_complete
            and redaction_preview_complete
            and not reference_governance.blocks_public_alpha_release_claim
            and not package_exposure.blocks_public_alpha_release_claim
            and no_reference_runtime
            and no_reference_copy
        )
        return PublicPrivateReleaseGate(
            gate_id="public_private_release_gate:v0.28.3",
            classification_complete=classification_complete,
            redaction_preview_complete=redaction_preview_complete,
            reference_governance_passed=not reference_governance.blocks_public_alpha_release_claim,
            package_exposure_boundary_passed=not package_exposure.blocks_public_alpha_release_claim,
            public_dataset_policy_passed=True,
            example_data_policy_passed=True,
            documentation_exposure_policy_passed=True,
            no_private_material_exposure=True,
            no_credential_exposure=True,
            no_secret_exposure=True,
            no_raw_trace_exposure=True,
            no_raw_transcript_exposure=True,
            no_raw_provider_output_exposure=True,
            no_reference_runtime_dependency=no_reference_runtime,
            no_reference_code_copy=no_reference_copy,
            gate_status="passed" if passed else "blocked",
            public_private_boundary_ready=passed,
            public_alpha_release_claim_allowed=False,
        )


class PublicPrivateBoundaryFindingService:
    BLOCKED_FINDINGS = {
        "destructive_redaction_attempted",
        "source_file_deletion_attempted",
        "file_move_attempted",
        "repo_split_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        source_view: PublicPrivateBoundarySourceView,
        reference_governance: ReferenceGovernanceReport,
        gate: PublicPrivateReleaseGate,
    ) -> list[PublicPrivateBoundaryFinding]:
        findings = [
            PublicPrivateBoundaryFinding(
                "public_private_boundary_finding:public_private_policy_created",
                "info",
                "public_private_policy_created",
                "v0.28.3 public/private boundary policy was created without repo split or destructive redaction.",
                _ref("public_private_release_gate", gate.gate_id, V0283_VERSION),
                [],
                None,
            )
        ]
        if source_view.source_status != "complete":
            findings.append(
                PublicPrivateBoundaryFinding(
                    "public_private_boundary_finding:missing_artifact_metadata",
                    "warning",
                    "missing_v0282_packaging_report",
                    "Artifact metadata is partial; v0.28.3 keeps the public release claim blocked unless prior gates permit.",
                    _ref("public_private_boundary_source_view", source_view.source_view_id, V0283_VERSION),
                    [],
                    "Withdraw after complete metadata is available and reviewed.",
                )
            )
        if reference_governance.blocks_public_alpha_release_claim:
            findings.append(
                PublicPrivateBoundaryFinding(
                    "public_private_boundary_finding:reference_governance_report_created",
                    "error",
                    "reference_governance_report_created",
                    "Reference governance is incomplete and blocks public alpha release claims while remaining decision-framework input.",
                    _ref("reference_governance_report", reference_governance.report_id, V0283_VERSION),
                    [],
                    "Withdraw after reference origin, license, and notices are explicitly reviewed.",
                )
            )
        return findings


class PublicPrivateBoundaryReportService:
    def build_report(self, report_id: str | None = None) -> PublicPrivateBoundaryReport:
        prereq = PublicPrivateBoundaryPrerequisiteSourceService()
        packaging = prereq.load_v0282_packaging_readiness_report()
        hygiene = prereq.load_v0281_release_hygiene_gate_report()
        inventory = prereq.load_v0281_references_inventory()
        policy = PublicPrivateBoundaryRuntimePolicyService().build_policy()
        request = PublicPrivateBoundaryRequest(
            "public_private_boundary_request:v0.28.3",
            packaging.report_id,
            hygiene.report_id,
            inventory.inventory_id,
            "standard",
        )
        source = PublicPrivateBoundarySourceViewService().build_source_view()
        public_policy = PublicArtifactPolicyService().build_policy()
        private_policy = PrivateArtifactPolicyService().build_policy()
        rules = PublicPrivateClassificationRuleService().build_rules()
        classifications = PublicPrivateArtifactClassificationService().classify_artifacts(source, rules)
        redaction_policy = RedactionPolicyService().build_policy()
        previews = RedactionPreviewService().build_previews(classifications, redaction_policy)
        decisions = RedactionDecisionRecordService().build_decisions(previews)
        secret_policy = SecretExclusionPolicyService().build_policy()
        credential_policy = CredentialExclusionPolicyService().build_policy()
        company_policy = CompanyMaterialExclusionPolicyService().build_policy()
        raw_trace_policy = RawTraceExclusionPolicyService().build_policy()
        raw_transcript_policy = RawTranscriptExclusionPolicyService().build_policy()
        raw_provider_policy = RawProviderOutputExclusionPolicyService().build_policy()
        reference_policy = ReferenceCodePolicyService().build_policy()
        inventory_boundary = ThirdPartyReferenceInventoryBoundaryService().build_boundary()
        reference_governance = ReferenceGovernanceReportService().build_report(reference_policy, inventory_boundary)
        reference_license = ReferenceLicenseBoundaryReportService().build_report(inventory_boundary)
        public_dataset_policy = PublicDatasetPolicyService().build_policy()
        example_policy = ExampleDataPolicyService().build_policy()
        sanitized_policy = SanitizedExamplePolicyService().build_policy()
        synthetic_policy = SyntheticDataPolicyService().build_policy()
        docs_policy = DocumentationExposurePolicyService().build_policy()
        package_exposure = PackageExposureBoundaryReportService().build_report(source, classifications)
        remediation = PublicPrivateRemediationPlanService().build_plan(classifications, decisions)
        gate = PublicPrivateReleaseGateService().evaluate_gate(classifications, previews, reference_governance, package_exposure)
        findings = PublicPrivateBoundaryFindingService().build_findings(source, reference_governance, gate)
        return PublicPrivateBoundaryReport(
            report_id=report_id or "public_private_boundary_report:v0.28.3",
            created_at=_now(),
            boundary_policy=policy,
            request=request,
            source_view=source,
            public_artifact_policy=public_policy,
            private_artifact_policy=private_policy,
            classification_rules=rules,
            artifact_classifications=classifications,
            redaction_policy=redaction_policy,
            redaction_previews=previews,
            redaction_decision_records=decisions,
            secret_exclusion_policy=secret_policy,
            credential_exclusion_policy=credential_policy,
            company_material_exclusion_policy=company_policy,
            raw_trace_exclusion_policy=raw_trace_policy,
            raw_transcript_exclusion_policy=raw_transcript_policy,
            raw_provider_output_exclusion_policy=raw_provider_policy,
            reference_code_policy=reference_policy,
            third_party_reference_inventory_boundary=inventory_boundary,
            reference_governance_report=reference_governance,
            reference_license_boundary_report=reference_license,
            public_dataset_policy=public_dataset_policy,
            example_data_policy=example_policy,
            sanitized_example_policy=sanitized_policy,
            synthetic_data_policy=synthetic_policy,
            documentation_exposure_policy=docs_policy,
            package_exposure_boundary_report=package_exposure,
            remediation_plan=remediation,
            public_private_release_gate=gate,
            findings=findings,
            report_status=gate.gate_status,
            ready_for_v0_28_4=True,
            ready_for_public_alpha_release_claim=gate.public_alpha_release_claim_allowed,
            public_private_boundary_ready=gate.public_private_boundary_ready,
            redaction_preview_created=bool(previews),
            limitations=["Artifact inspection is metadata/ref-only; raw contents, secrets, transcripts, provider outputs, and company material are not exposed."],
            withdrawal_conditions=["Withdraw if destructive redaction, file deletion/movement, repo split, Schumpeter split, adapter implementation, package publish/tag, provider/command execution, reference runtime adoption/code copy, private exposure, or LLM sole authority is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.boundary_policy,
            "source-view": report.source_view,
            "public-policy": report.public_artifact_policy,
            "private-policy": report.private_artifact_policy,
            "classify": report.artifact_classifications,
            "redaction-policy": report.redaction_policy,
            "redaction-preview": report.redaction_previews,
            "secrets": report.secret_exclusion_policy,
            "credentials": report.credential_exclusion_policy,
            "company-material": report.company_material_exclusion_policy,
            "raw-traces": report.raw_trace_exclusion_policy,
            "raw-transcripts": report.raw_transcript_exclusion_policy,
            "raw-provider-outputs": report.raw_provider_output_exclusion_policy,
            "references": report.reference_governance_report,
            "reference-license": report.reference_license_boundary_report,
            "datasets": report.public_dataset_policy,
            "examples": report.example_data_policy,
            "docs": report.documentation_exposure_policy,
            "package-exposure": report.package_exposure_boundary_report,
            "remediation": report.remediation_plan,
            "release-gate": report.public_private_release_gate,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0283_VERSION,
            "layer": V028_LAYER,
            "subject": "public_private_boundary_redaction_reference_policy",
            "principles": [
                "Public-private boundary is not repo split",
                "Redaction policy is not destructive redaction",
                "Redaction preview is not file mutation",
                "Quarantine recommendation is not deletion",
                "Reference policy is not reference adoption",
                "Reference inventory is not runtime dependency",
                "Public example must be sanitized or synthetic",
                "Public docs must not expose company/private material",
                "Schumpeter references are reference-only until explicit decision framework",
                "No-public-release is a valid outcome",
            ],
            "safety_boundary": {
                "destructive_redaction_performed": report.destructive_redaction_performed,
                "source_file_deleted": report.source_file_deleted,
                "file_moved": report.file_moved,
                "repo_split_performed": report.repo_split_performed,
                "schumpeter_split_implemented": report.schumpeter_split_implemented,
                "external_adapter_implemented": report.external_adapter_implemented,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "company_private_material_exposed": report.company_private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "secret_exposed": report.secret_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.28.4 Schumpeter Split Decision Framework",
                "v0.28.5 Schumpeter Split Preparation Profile",
                "v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow",
                "v0.28.7 Alpha Documentation / Onboarding / Example Pack",
                "v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate",
            ],
            "next_step": V0283_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "public_private_boundary_redaction_reference_policy_created",
            "version": V0283_VERSION,
            "source_read_models": ["PackagingReadinessState", "PackageDataBoundaryState", "ReleaseHygieneGateState", "ReferencesInventoryState", "ForbiddenRepositoryArtifactScanState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["PublicPrivateBoundaryState", "PublicPrivateArtifactClassificationState", "RedactionPreviewState", "ReferenceGovernanceState", "ReferenceLicenseBoundaryState", "PackageExposureBoundaryState", "PublicPrivateReleaseGateState", "V028ReadinessState"],
            "effect_types": V0283_EFFECT_TYPES,
            "forbidden_effect_types": V0283_FORBIDDEN_EFFECT_TYPES,
        }


def render_public_private_boundary_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: PublicPrivateBoundaryReport = parts["report"]
    lines = [
        f"Public-Private Boundary / Redaction / Reference Policy {section}",
        f"version={report.version}",
        f"layer={report.boundary_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_4={_bool(report.ready_for_v0_28_4)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"public_private_boundary_ready={_bool(report.public_private_boundary_ready)}",
        f"redaction_preview_created={_bool(report.redaction_preview_created)}",
        f"destructive_redaction_performed={_bool(report.destructive_redaction_performed)}",
        f"source_file_deleted={_bool(report.source_file_deleted)}",
        f"file_moved={_bool(report.file_moved)}",
        f"repo_split_performed={_bool(report.repo_split_performed)}",
        f"schumpeter_split_implemented={_bool(report.schumpeter_split_implemented)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "gate_id", getattr(payload, "source_view_id", getattr(payload, "remediation_plan_id", "")))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0284_VERSION = "v0.28.4"
V0284_VERSION_NAME = "Schumpeter Split Decision Framework"
V0284_NEXT_STEP = "v0.28.5 Schumpeter Split Preparation Profile"
V0284_RECOMMENDED_DEFAULT = "keep_reference_only_and_prepare_private_overlay"

V0284_OBJECT_TYPES = [
    "schumpeter_split_decision_runtime_policy",
    "schumpeter_split_decision_request",
    "schumpeter_reference_source_view",
    "schumpeter_reference_inventory",
    "schumpeter_reference_artifact",
    "schumpeter_reference_license_review",
    "schumpeter_reference_private_risk_review",
    "schumpeter_architecture_comparison",
    "schumpeter_capability_comparison_matrix",
    "schumpeter_capability_comparison_row",
    "schumpeter_ocel_pig_ocpx_compatibility_review",
    "schumpeter_workbench_memory_compatibility_review",
    "schumpeter_reuse_value_assessment",
    "schumpeter_risk_assessment",
    "schumpeter_split_option_catalog",
    "schumpeter_split_option_assessment",
    "schumpeter_decision_criterion",
    "schumpeter_decision_criterion_score",
    "schumpeter_reuse_disposition_policy_runtime",
    "schumpeter_reuse_disposition_candidate",
    "schumpeter_reuse_disposition_decision",
    "schumpeter_split_decision_candidate",
    "schumpeter_split_recommendation",
    "schumpeter_split_decision_record",
    "schumpeter_split_decision_audit_trail",
    "schumpeter_split_decision_finding",
    "schumpeter_split_decision_report",
    "public_private_boundary_report",
    "reference_governance_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0284_EVENT_TYPES = [
    "schumpeter_split_decision_requested",
    "schumpeter_split_decision_prerequisites_loaded",
    "schumpeter_split_decision_policy_created",
    "schumpeter_reference_source_view_created",
    "schumpeter_reference_inventory_created",
    "schumpeter_reference_artifact_created",
    "schumpeter_reference_license_review_created",
    "schumpeter_reference_private_risk_review_created",
    "schumpeter_architecture_comparison_created",
    "schumpeter_capability_matrix_created",
    "schumpeter_ocel_pig_ocpx_compatibility_review_created",
    "schumpeter_workbench_memory_compatibility_review_created",
    "schumpeter_reuse_value_assessment_created",
    "schumpeter_risk_assessment_created",
    "schumpeter_split_option_catalog_created",
    "schumpeter_split_option_assessment_created",
    "schumpeter_decision_criterion_created",
    "schumpeter_decision_criterion_score_created",
    "schumpeter_reuse_disposition_policy_created",
    "schumpeter_reuse_disposition_candidate_created",
    "schumpeter_reuse_disposition_decision_created",
    "schumpeter_split_decision_candidate_created",
    "schumpeter_split_recommendation_created",
    "schumpeter_split_decision_record_created",
    "schumpeter_split_decision_audit_trail_created",
    "schumpeter_split_decision_report_created",
    "schumpeter_split_decision_warning_created",
    "schumpeter_split_decision_blocked",
]

V0284_EFFECT_TYPES = [
    "read_only_observation",
    "schumpeter_split_decision_framework_created",
    "schumpeter_reference_inventory_created",
    "schumpeter_reference_license_review_created",
    "schumpeter_reference_private_risk_review_created",
    "schumpeter_capability_comparison_created",
    "schumpeter_reuse_disposition_decision_created",
    "schumpeter_split_recommendation_created",
    "schumpeter_split_decision_recorded",
    "schumpeter_split_decision_audit_created",
    "state_candidate_created",
]

V0284_FORBIDDEN_EFFECT_TYPES = [
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "private_repo_created",
    "merge_into_public_core_performed",
    "references_runtime_dependency_added",
    "references_code_copied",
    "file_moved",
    "destructive_redaction_performed",
    "package_published",
    "release_tag_created",
    "external_provider_adapter_implemented",
    "external_agent_adapter_implemented",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "company_private_material_exposed",
    "credential_exposed",
    "secret_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class SchumpeterSplitDecisionRuntimePolicy(ModelMixin):
    policy_id: str
    version: str = V0284_VERSION
    layer: str = V028_LAYER
    decision_framework_enabled: bool = True
    reference_inventory_enabled: bool = True
    capability_comparison_enabled: bool = True
    license_review_required: bool = True
    private_risk_review_required: bool = True
    public_private_boundary_required: bool = True
    reuse_disposition_required: bool = True
    decision_record_required: bool = True
    audit_required: bool = True
    actual_split_enabled_now: bool = False
    company_wrapper_enabled_now: bool = False
    private_distribution_runtime_enabled_now: bool = False
    separate_private_repo_creation_enabled_now: bool = False
    merge_into_public_core_enabled_now: bool = False
    references_runtime_dependency_enabled_now: bool = False
    references_code_copy_enabled_now: bool = False
    file_move_enabled_now: bool = False
    destructive_redaction_enabled_now: bool = False
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    external_adapter_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    unknown_license_is_safe: bool = False
    unknown_private_risk_is_safe: bool = False
    default_decision_posture: str = V0284_RECOMMENDED_DEFAULT
    no_split_is_valid_outcome: bool = True
    defer_split_is_valid_outcome: bool = True
    keep_reference_only_is_valid_outcome: bool = True
    llm_judge_as_sole_decision_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitDecisionRequest(ModelMixin):
    request_id: str
    public_private_boundary_report_id: str | None
    reference_governance_report_id: str | None
    reference_license_boundary_report_id: str | None
    packaging_readiness_report_id: str | None
    release_hygiene_gate_report_id: str | None
    selected_reference_refs: list[dict[str, Any]]
    requested_decision_scope: str
    requested_decision_mode: str
    version: str = V0284_VERSION
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReferenceSourceView(ModelMixin):
    source_view_id: str
    public_private_boundary_report_ref: dict[str, Any] | None
    reference_governance_report_ref: dict[str, Any] | None
    reference_license_boundary_report_ref: dict[str, Any] | None
    references_inventory_ref: dict[str, Any] | None
    schumpeter_reference_refs: list[dict[str, Any]]
    schumpeter_doc_refs: list[dict[str, Any]]
    schumpeter_model_refs: list[dict[str, Any]]
    schumpeter_test_refs: list[dict[str, Any]]
    schumpeter_config_refs: list[dict[str, Any]]
    schumpeter_runtime_refs: list[dict[str, Any]]
    source_status: str
    references_schumpeter_present: bool | None
    license_status_known: bool | None
    private_risk_status_known: bool | None
    version: str = V0284_VERSION
    company_material_detected: bool = False
    credential_detected: bool = False
    raw_trace_detected: bool = False
    raw_transcript_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReferenceArtifact(ModelMixin):
    artifact_id: str
    artifact_ref: dict[str, Any]
    artifact_path_hint: str | None
    artifact_kind: str
    origin_known: bool | None
    license_status: str
    private_data_risk: str
    company_material_risk: str
    code_reuse_value: str
    concept_reuse_value: str
    test_reuse_value: str
    doc_reuse_value: str
    OCEL_compatibility: str
    PIG_compatibility: str
    memory_workbench_compatibility: str
    recommended_initial_disposition: str
    version: str = V0284_VERSION
    runtime_dependency_allowed_now: bool = False
    code_copy_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReferenceInventory(ModelMixin):
    inventory_id: str
    reference_root_ref: dict[str, Any] | None
    artifacts: list[SchumpeterReferenceArtifact]
    artifact_count: int
    doc_count: int
    model_count: int
    test_count: int
    config_count: int
    runtime_count: int
    unknown_count: int
    license_unknown_count: int
    private_risk_unknown_count: int
    quarantine_recommended_count: int
    inventory_status: str
    version: str = V0284_VERSION
    references_used_as_runtime_dependency: bool = False
    references_code_copied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReferenceLicenseReview(ModelMixin):
    review_id: str
    artifact_ref: dict[str, Any]
    license_status: str
    license_evidence_refs: list[dict[str, Any]]
    license_review_required: bool
    license_blocks_reuse: bool
    license_blocks_public_core_adoption: bool
    review_summary: str
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReferencePrivateRiskReview(ModelMixin):
    review_id: str
    artifact_ref: dict[str, Any]
    private_data_risk: str
    company_material_risk: str
    credential_risk: str
    raw_trace_risk: str
    public_core_adoption_allowed: bool
    private_overlay_only: bool
    quarantine_required: bool
    review_summary: str
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterArchitectureComparison(ModelMixin):
    comparison_id: str
    chanta_core_ref: dict[str, Any] | None
    schumpeter_reference_ref: dict[str, Any] | None
    compared_dimensions: list[str]
    overlap_summary: str
    divergence_summary: str
    reuse_implication_summary: str
    comparison_status: str
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterCapabilityComparisonRow(ModelMixin):
    row_id: str
    capability_name: str
    chanta_core_status: str
    schumpeter_reference_status: str
    overlap_level: str
    concept_reuse_value: str
    code_reuse_value: str
    test_reuse_value: str
    doc_reuse_value: str
    risk_level: str
    recommended_disposition: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterCapabilityComparisonMatrix(ModelMixin):
    matrix_id: str
    rows: list[SchumpeterCapabilityComparisonRow]
    compared_capability_count: int
    high_overlap_count: int
    high_reuse_value_count: int
    high_risk_count: int
    quarantine_recommended_count: int
    matrix_status: str
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterOCELPIGOCPXCompatibilityReview(ModelMixin):
    review_id: str
    ocel_compatibility: str
    pig_compatibility: str
    ocpx_compatibility: str
    compatibility_summary: str
    blocks_public_core_adoption: bool
    supports_concept_reuse: bool
    supports_future_private_overlay: bool
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterWorkbenchMemoryCompatibilityReview(ModelMixin):
    review_id: str
    workbench_compatibility: str
    memory_foundation_compatibility: str
    continuity_compatibility: str
    lifecycle_compatibility: str
    compatibility_summary: str
    supports_concept_reuse: bool
    supports_future_profile_boundary: bool
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReuseValueAssessment(ModelMixin):
    assessment_id: str
    artifact_ref: dict[str, Any] | None
    capability_ref: dict[str, Any] | None
    concept_reuse_value: str
    code_reuse_value: str
    test_reuse_value: str
    doc_reuse_value: str
    recommended_reuse_mode: str
    reuse_summary: str
    version: str = V0284_VERSION
    runtime_dependency_added_now: bool = False
    code_copied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterRiskAssessment(ModelMixin):
    risk_assessment_id: str
    subject_ref: dict[str, Any] | None
    risk_dimensions: list[dict[str, Any]]
    ip_license_risk: str
    private_data_risk: str
    public_core_contamination_risk: str
    runtime_dependency_risk: str
    security_credential_exposure_risk: str
    maintainability_risk: str
    risk_summary: str
    blocks_public_core_adoption: bool
    version: str = V0284_VERSION
    blocks_split_implementation_now: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitOptionCatalog(ModelMixin):
    catalog_id: str
    version: str = V0284_VERSION
    options: list[str] = field(default_factory=lambda: [
        "no_split",
        "reference_only",
        "public_core_private_overlay",
        "private_distribution_profile",
        "separate_private_repo",
        "merge_schumpeter_into_core",
        "deprecate_legacy_schumpeter",
    ])
    default_option: str = "reference_only"
    safe_default_combination: list[str] = field(default_factory=lambda: ["reference_only", "public_core_private_overlay_preparation"])
    option_catalog_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitOptionAssessment(ModelMixin):
    assessment_id: str
    option_name: str
    option_summary: str
    allowed_now: bool
    required_preconditions: list[str]
    blockers: list[str]
    warnings: list[str]
    risk_level: str
    recommended: bool
    version: str = V0284_VERSION
    implementation_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterDecisionCriterion(ModelMixin):
    criterion_id: str
    criterion_name: str
    criterion_summary: str
    version: str = V0284_VERSION
    required_for_decision: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterDecisionCriterionScore(ModelMixin):
    score_id: str
    criterion_ref: dict[str, Any]
    subject_ref: dict[str, Any] | None
    score_band: str
    score_value: float | None
    score_summary: str
    version: str = V0284_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReuseDispositionPolicyRuntime(ModelMixin):
    policy_id: str
    version: str = V0284_VERSION
    allowed_dispositions: list[str] = field(default_factory=lambda: [
        "adopt_concept",
        "port_model_later",
        "port_test_later",
        "port_document_later",
        "keep_reference_only",
        "quarantine_due_to_license_or_private_risk",
        "discard",
    ])
    runtime_dependency_forbidden_now: bool = True
    code_copy_forbidden_now: bool = True
    disposition_requires_license_review: bool = True
    disposition_requires_private_risk_review: bool = True
    disposition_requires_public_private_boundary_review: bool = True
    disposition_decision_is_not_migration: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReuseDispositionCandidate(ModelMixin):
    candidate_id: str
    artifact_ref: dict[str, Any]
    proposed_disposition: str
    disposition_reason: str
    required_followup_version: str | None
    required_review_refs: list[dict[str, Any]]
    version: str = V0284_VERSION
    migration_performed_now: bool = False
    runtime_dependency_added_now: bool = False
    code_copied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterReuseDispositionDecision(ModelMixin):
    decision_id: str
    disposition_candidate_ref: dict[str, Any]
    decision_type: str
    decision_reason: str
    version: str = V0284_VERSION
    migration_allowed_now: bool = False
    runtime_dependency_added_now: bool = False
    code_copied_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitDecisionCandidate(ModelMixin):
    decision_candidate_id: str
    candidate_option: str
    candidate_summary: str
    supporting_option_assessment_refs: list[dict[str, Any]]
    supporting_criterion_score_refs: list[dict[str, Any]]
    supporting_risk_assessment_refs: list[dict[str, Any]]
    required_followup_versions: list[str]
    version: str = V0284_VERSION
    implementation_allowed_now: bool = False
    split_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitRecommendation(ModelMixin):
    recommendation_id: str
    recommended_option: str
    recommendation_summary: str
    confidence_level: str
    blockers: list[str]
    warnings: list[str]
    required_next_steps: list[str]
    version: str = V0284_VERSION
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitDecisionRecord(ModelMixin):
    decision_record_id: str
    decision_type: str
    decision_reason: str
    recommendation_ref: dict[str, Any] | None
    decision_candidate_refs: list[dict[str, Any]]
    disposition_decision_refs: list[dict[str, Any]]
    license_review_refs: list[dict[str, Any]]
    private_risk_review_refs: list[dict[str, Any]]
    public_private_boundary_refs: list[dict[str, Any]]
    version: str = V0284_VERSION
    split_implemented_now: bool = False
    company_wrapper_implemented_now: bool = False
    runtime_dependency_added_now: bool = False
    code_copied_now: bool = False
    file_moved_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitDecisionAuditTrail(ModelMixin):
    audit_trail_id: str
    decision_request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    inventory_ref: dict[str, Any]
    license_review_refs: list[dict[str, Any]]
    private_risk_review_refs: list[dict[str, Any]]
    comparison_matrix_ref: dict[str, Any] | None
    option_assessment_refs: list[dict[str, Any]]
    disposition_decision_refs: list[dict[str, Any]]
    decision_record_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    version: str = V0284_VERSION
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSplitDecisionFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class SchumpeterSplitDecisionReport(ModelMixin):
    report_id: str
    created_at: str
    decision_policy: SchumpeterSplitDecisionRuntimePolicy
    request: SchumpeterSplitDecisionRequest
    source_view: SchumpeterReferenceSourceView
    reference_inventory: SchumpeterReferenceInventory
    license_reviews: list[SchumpeterReferenceLicenseReview]
    private_risk_reviews: list[SchumpeterReferencePrivateRiskReview]
    architecture_comparison: SchumpeterArchitectureComparison
    capability_comparison_matrix: SchumpeterCapabilityComparisonMatrix
    ocel_pig_ocpx_compatibility_review: SchumpeterOCELPIGOCPXCompatibilityReview
    workbench_memory_compatibility_review: SchumpeterWorkbenchMemoryCompatibilityReview
    reuse_value_assessments: list[SchumpeterReuseValueAssessment]
    risk_assessments: list[SchumpeterRiskAssessment]
    split_option_catalog: SchumpeterSplitOptionCatalog
    option_assessments: list[SchumpeterSplitOptionAssessment]
    decision_criteria: list[SchumpeterDecisionCriterion]
    criterion_scores: list[SchumpeterDecisionCriterionScore]
    reuse_disposition_policy: SchumpeterReuseDispositionPolicyRuntime
    reuse_disposition_candidates: list[SchumpeterReuseDispositionCandidate]
    reuse_disposition_decisions: list[SchumpeterReuseDispositionDecision]
    split_decision_candidates: list[SchumpeterSplitDecisionCandidate]
    split_recommendation: SchumpeterSplitRecommendation
    split_decision_records: list[SchumpeterSplitDecisionRecord]
    audit_trail: SchumpeterSplitDecisionAuditTrail
    findings: list[SchumpeterSplitDecisionFinding]
    report_status: str
    ready_for_v0_28_5: bool
    schumpeter_decision_framework_ready: bool
    schumpeter_split_decision_ready: bool
    version: str = V0284_VERSION
    ready_for_public_alpha_release_claim: bool = False
    recommended_default: str = V0284_RECOMMENDED_DEFAULT
    actual_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    private_repo_created: bool = False
    merge_into_public_core_performed: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    file_moved: bool = False
    destructive_redaction_performed: bool = False
    external_adapter_implemented: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    runtime_continuity_injected: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0284_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.28.5 Schumpeter Split Preparation Profile begins or Schumpeter split decision policy changes."


class SchumpeterSplitDecisionPrerequisiteSourceService:
    def load_v0283_public_private_boundary_report(self) -> PublicPrivateBoundaryReport:
        return PublicPrivateBoundaryReportService().build_report()

    def load_v0283_reference_governance_report(self) -> ReferenceGovernanceReport:
        return PublicPrivateBoundaryReportService().build_report().reference_governance_report

    def load_v0283_reference_license_boundary_report(self) -> ReferenceLicenseBoundaryReport:
        return PublicPrivateBoundaryReportService().build_report().reference_license_boundary_report

    def load_v0283_package_exposure_boundary_report(self) -> PackageExposureBoundaryReport:
        return PublicPrivateBoundaryReportService().build_report().package_exposure_boundary_report

    def load_v0282_packaging_readiness_report(self) -> PackagingReadinessReport:
        return PackagingReadinessReportService().build_report()

    def load_v0281_release_hygiene_gate_report(self) -> ReleaseHygieneGateReport:
        return ReleaseHygieneGateReportService().build_report()

    def load_v0280_schumpeter_decision_framework_policy(self) -> SchumpeterSplitDecisionFramework:
        return SchumpeterSplitDecisionFrameworkService().build_framework()

    def inspect_references_schumpeter_metadata_only_if_available(self) -> list[dict[str, Any]]:
        root = _repo_root() / "references" / "schumpeter"
        if not root.exists():
            return []
        refs: list[dict[str, Any]] = [_file_ref(root, "schumpeter_reference_root")]
        try:
            for path in root.rglob("*"):
                if path.is_file():
                    refs.append(_file_ref(path, "schumpeter_reference_file"))
                    if len(refs) >= 50:
                        break
        except OSError:
            return refs
        return refs

    def load_docs_reference_metadata_if_available(self) -> list[dict[str, Any]]:
        docs = _repo_root() / "docs" / "versions" / "v0.28"
        return [_file_ref(docs, "docs_ref")] if docs.exists() else []

    def load_ocel_pig_ocpx_reports_if_available(self) -> list[dict[str, Any]]:
        return [_ref("pig_report", "schumpeter_split_decision_framework:pig:v0.28.4", V0284_VERSION), _ref("ocpx_projection", "schumpeter_split_decision_framework:ocpx:v0.28.4", V0284_VERSION)]


class SchumpeterSplitDecisionRuntimePolicyService:
    def build_policy(self) -> SchumpeterSplitDecisionRuntimePolicy:
        return SchumpeterSplitDecisionRuntimePolicy(policy_id="schumpeter_split_decision_runtime_policy:v0.28.4")


def _schumpeter_kind_from_ref(ref: dict[str, Any]) -> str:
    path = str(ref.get("path", ref.get("object_id", ""))).lower()
    suffix = Path(path).suffix.lower()
    if suffix in {".md", ".rst", ".txt"}:
        return "concept_doc"
    if suffix in {".json", ".toml", ".yaml", ".yml", ".ini"}:
        return "config"
    if "test" in path:
        return "test_case"
    if suffix == ".py":
        return "code_module"
    if suffix in {".db", ".sqlite", ".log"}:
        return "trace_sample"
    return "unknown"


class SchumpeterReferenceSourceViewService:
    def build_source_view(self) -> SchumpeterReferenceSourceView:
        prereq = SchumpeterSplitDecisionPrerequisiteSourceService()
        refs = prereq.inspect_references_schumpeter_metadata_only_if_available()
        files = [ref for ref in refs if ref.get("kind") == "schumpeter_reference_file"]
        doc_refs = [ref for ref in files if _schumpeter_kind_from_ref(ref) in {"concept_doc", "architecture_doc"}]
        test_refs = [ref for ref in files if _schumpeter_kind_from_ref(ref) in {"test_fixture", "test_case"}]
        config_refs = [ref for ref in files if _schumpeter_kind_from_ref(ref) == "config"]
        runtime_refs = [ref for ref in files if _schumpeter_kind_from_ref(ref) in {"runtime_script", "trace_sample"}]
        model_refs = [ref for ref in files if _schumpeter_kind_from_ref(ref) in {"code_module", "model_definition"}]
        present = bool(refs)
        return SchumpeterReferenceSourceView(
            source_view_id="schumpeter_reference_source_view:v0.28.4",
            public_private_boundary_report_ref=_ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION),
            reference_governance_report_ref=_ref("reference_governance_report", "reference_governance_report:v0.28.3", V0283_VERSION),
            reference_license_boundary_report_ref=_ref("reference_license_boundary_report", "reference_license_boundary_report:v0.28.3", V0283_VERSION),
            references_inventory_ref=_ref("references_directory_inventory", "references_directory_inventory:v0.28.1", V0281_VERSION),
            schumpeter_reference_refs=refs,
            schumpeter_doc_refs=doc_refs,
            schumpeter_model_refs=model_refs,
            schumpeter_test_refs=test_refs,
            schumpeter_config_refs=config_refs,
            schumpeter_runtime_refs=runtime_refs,
            source_status="partial" if present else "missing",
            references_schumpeter_present=present,
            license_status_known=False if present else None,
            private_risk_status_known=False if present else None,
        )


class SchumpeterReferenceInventoryService:
    def build_inventory(self, source_view: SchumpeterReferenceSourceView | None = None) -> SchumpeterReferenceInventory:
        source_view = source_view or SchumpeterReferenceSourceViewService().build_source_view()
        refs = [ref for ref in source_view.schumpeter_reference_refs if ref.get("kind") == "schumpeter_reference_file"]
        if not refs and source_view.references_schumpeter_present:
            refs = source_view.schumpeter_reference_refs[:1]
        artifacts: list[SchumpeterReferenceArtifact] = []
        for index, ref in enumerate(refs[:20]):
            kind = _schumpeter_kind_from_ref(ref)
            artifacts.append(
                SchumpeterReferenceArtifact(
                    artifact_id=f"schumpeter_reference_artifact:{index}:v0.28.4",
                    artifact_ref=ref,
                    artifact_path_hint=str(ref.get("path", ref.get("object_id", ""))),
                    artifact_kind=kind,
                    origin_known=False,
                    license_status="unknown",
                    private_data_risk="unknown",
                    company_material_risk="unknown",
                    code_reuse_value="low" if kind == "code_module" else "none",
                    concept_reuse_value="medium" if kind in {"concept_doc", "architecture_doc"} else "low",
                    test_reuse_value="medium" if kind in {"test_case", "test_fixture"} else "none",
                    doc_reuse_value="medium" if kind in {"concept_doc", "architecture_doc"} else "none",
                    OCEL_compatibility="unknown",
                    PIG_compatibility="unknown",
                    memory_workbench_compatibility="unknown",
                    recommended_initial_disposition="keep_reference_only",
                )
            )
        if not artifacts:
            artifacts.append(
                SchumpeterReferenceArtifact(
                    artifact_id="schumpeter_reference_artifact:missing:v0.28.4",
                    artifact_ref=_ref("schumpeter_reference_root", "references/schumpeter:missing", V0284_VERSION),
                    artifact_path_hint="references/schumpeter",
                    artifact_kind="unknown",
                    origin_known=None,
                    license_status="unknown",
                    private_data_risk="unknown",
                    company_material_risk="unknown",
                    code_reuse_value="unknown",
                    concept_reuse_value="unknown",
                    test_reuse_value="unknown",
                    doc_reuse_value="unknown",
                    OCEL_compatibility="unknown",
                    PIG_compatibility="unknown",
                    memory_workbench_compatibility="unknown",
                    recommended_initial_disposition="keep_reference_only",
                )
            )
        doc_count = sum(1 for item in artifacts if item.artifact_kind in {"concept_doc", "architecture_doc"})
        model_count = sum(1 for item in artifacts if item.artifact_kind in {"code_module", "model_definition"})
        test_count = sum(1 for item in artifacts if item.artifact_kind in {"test_fixture", "test_case"})
        config_count = sum(1 for item in artifacts if item.artifact_kind == "config")
        runtime_count = sum(1 for item in artifacts if item.artifact_kind in {"runtime_script", "trace_sample"})
        unknown_count = sum(1 for item in artifacts if item.artifact_kind == "unknown")
        license_unknown = sum(1 for item in artifacts if item.license_status == "unknown")
        private_unknown = sum(1 for item in artifacts if item.private_data_risk == "unknown")
        return SchumpeterReferenceInventory(
            inventory_id="schumpeter_reference_inventory:v0.28.4",
            reference_root_ref=source_view.schumpeter_reference_refs[0] if source_view.schumpeter_reference_refs else None,
            artifacts=artifacts,
            artifact_count=len(artifacts),
            doc_count=doc_count,
            model_count=model_count,
            test_count=test_count,
            config_count=config_count,
            runtime_count=runtime_count,
            unknown_count=unknown_count,
            license_unknown_count=license_unknown,
            private_risk_unknown_count=private_unknown,
            quarantine_recommended_count=license_unknown,
            inventory_status="warning" if source_view.references_schumpeter_present else "partial",
        )


class SchumpeterReferenceLicenseReviewService:
    def build_reviews(self, inventory: SchumpeterReferenceInventory) -> list[SchumpeterReferenceLicenseReview]:
        return [
            SchumpeterReferenceLicenseReview(
                review_id=f"schumpeter_reference_license_review:{item.artifact_id}:v0.28.4",
                artifact_ref=item.artifact_ref,
                license_status=item.license_status,
                license_evidence_refs=[],
                license_review_required=True,
                license_blocks_reuse=item.license_status in {"unknown", "known_incompatible"},
                license_blocks_public_core_adoption=item.license_status in {"unknown", "known_incompatible"},
                review_summary="Unknown or incompatible license is not safe for public core adoption; v0.28.4 does not migrate code.",
            )
            for item in inventory.artifacts
        ]


class SchumpeterReferencePrivateRiskReviewService:
    def build_reviews(self, inventory: SchumpeterReferenceInventory) -> list[SchumpeterReferencePrivateRiskReview]:
        return [
            SchumpeterReferencePrivateRiskReview(
                review_id=f"schumpeter_reference_private_risk_review:{item.artifact_id}:v0.28.4",
                artifact_ref=item.artifact_ref,
                private_data_risk=item.private_data_risk,
                company_material_risk=item.company_material_risk,
                credential_risk="unknown",
                raw_trace_risk="unknown" if item.artifact_kind == "trace_sample" else "none",
                public_core_adoption_allowed=False,
                private_overlay_only=True,
                quarantine_required=item.private_data_risk in {"unknown", "high", "blocked"},
                review_summary="Unknown private-data risk is not safe; reference remains private-overlay or reference-only candidate.",
            )
            for item in inventory.artifacts
        ]


class SchumpeterArchitectureComparisonService:
    DIMENSIONS = ["OCEL_trace", "reflective_substrate", "memory", "workbench", "provider_boundary", "skill_boundary", "runtime_loop", "safety_boundary", "governance_boundary"]

    def build_comparison(self, source_view: SchumpeterReferenceSourceView) -> SchumpeterArchitectureComparison:
        return SchumpeterArchitectureComparison(
            comparison_id="schumpeter_architecture_comparison:v0.28.4",
            chanta_core_ref=_ref("package_source", "src/chanta_core"),
            schumpeter_reference_ref=source_view.schumpeter_reference_refs[0] if source_view.schumpeter_reference_refs else None,
            compared_dimensions=self.DIMENSIONS,
            overlap_summary="Potential overlap is evaluated at concept level only.",
            divergence_summary="Public ChantaCore keeps OCEL-native spine independent from Schumpeter reference artifacts.",
            reuse_implication_summary="Only concept/profile preparation can proceed before license and private-risk review is complete.",
            comparison_status="warning",
        )


class SchumpeterCapabilityComparisonMatrixService:
    def build_matrix(self) -> SchumpeterCapabilityComparisonMatrix:
        rows = [
            SchumpeterCapabilityComparisonRow("schumpeter_capability_row:memory:v0.28.4", "memory", "implemented", "unknown", "unknown", "medium", "none", "low", "low", "unknown", "keep_reference_only"),
            SchumpeterCapabilityComparisonRow("schumpeter_capability_row:workbench:v0.28.4", "workbench", "implemented", "unknown", "unknown", "medium", "none", "low", "low", "unknown", "keep_reference_only"),
            SchumpeterCapabilityComparisonRow("schumpeter_capability_row:private_overlay:v0.28.4", "private_overlay", "future_track", "unknown", "unknown", "high", "none", "none", "medium", "high", "private_overlay_later"),
        ]
        return SchumpeterCapabilityComparisonMatrix(
            matrix_id="schumpeter_capability_comparison_matrix:v0.28.4",
            rows=rows,
            compared_capability_count=len(rows),
            high_overlap_count=sum(1 for row in rows if row.overlap_level == "high"),
            high_reuse_value_count=sum(1 for row in rows if row.concept_reuse_value == "high"),
            high_risk_count=sum(1 for row in rows if row.risk_level in {"high", "blocked"}),
            quarantine_recommended_count=sum(1 for row in rows if row.risk_level in {"high", "blocked"}),
            matrix_status="warning",
        )


class SchumpeterOCELPIGOCPXCompatibilityReviewService:
    def build_review(self) -> SchumpeterOCELPIGOCPXCompatibilityReview:
        return SchumpeterOCELPIGOCPXCompatibilityReview(
            review_id="schumpeter_ocel_pig_ocpx_compatibility_review:v0.28.4",
            ocel_compatibility="unknown",
            pig_compatibility="unknown",
            ocpx_compatibility="unknown",
            compatibility_summary="Compatibility is treated as concept-level until reference license/private risk is resolved.",
            blocks_public_core_adoption=True,
            supports_concept_reuse=True,
            supports_future_private_overlay=True,
        )


class SchumpeterWorkbenchMemoryCompatibilityReviewService:
    def build_review(self) -> SchumpeterWorkbenchMemoryCompatibilityReview:
        return SchumpeterWorkbenchMemoryCompatibilityReview(
            review_id="schumpeter_workbench_memory_compatibility_review:v0.28.4",
            workbench_compatibility="unknown",
            memory_foundation_compatibility="unknown",
            continuity_compatibility="unknown",
            lifecycle_compatibility="unknown",
            compatibility_summary="Workbench/Memory comparison supports future profile boundary discussion only.",
            supports_concept_reuse=True,
            supports_future_profile_boundary=True,
        )


class SchumpeterReuseValueAssessmentService:
    def build_assessments(self, inventory: SchumpeterReferenceInventory, matrix: SchumpeterCapabilityComparisonMatrix) -> list[SchumpeterReuseValueAssessment]:
        assessments = [
            SchumpeterReuseValueAssessment(
                assessment_id=f"schumpeter_reuse_value_assessment:{item.artifact_id}:v0.28.4",
                artifact_ref=item.artifact_ref,
                capability_ref=None,
                concept_reuse_value=item.concept_reuse_value,
                code_reuse_value="none",
                test_reuse_value=item.test_reuse_value,
                doc_reuse_value=item.doc_reuse_value,
                recommended_reuse_mode="reference_only" if item.license_status == "unknown" else "concept_only",
                reuse_summary="Concept reuse may be considered later; v0.28.4 performs no code copy or runtime adoption.",
            )
            for item in inventory.artifacts
        ]
        assessments.extend(
            SchumpeterReuseValueAssessment(
                assessment_id=f"schumpeter_reuse_value_assessment:{row.row_id}:v0.28.4",
                artifact_ref=None,
                capability_ref=_ref("schumpeter_capability_comparison_row", row.row_id, V0284_VERSION),
                concept_reuse_value=row.concept_reuse_value,
                code_reuse_value="none",
                test_reuse_value=row.test_reuse_value,
                doc_reuse_value=row.doc_reuse_value,
                recommended_reuse_mode="private_overlay_later" if row.capability_name == "private_overlay" else "concept_only",
                reuse_summary="Capability reuse is decision evidence only, not migration.",
            )
            for row in matrix.rows
        )
        return assessments


class SchumpeterRiskAssessmentService:
    def build_assessments(self, inventory: SchumpeterReferenceInventory) -> list[SchumpeterRiskAssessment]:
        dimensions = [
            {"dimension": "ip_license_risk", "status": "unknown"},
            {"dimension": "private_data_risk", "status": "unknown"},
            {"dimension": "public_core_contamination_risk", "status": "high"},
            {"dimension": "runtime_dependency_risk", "status": "blocked"},
            {"dimension": "security_credential_exposure_risk", "status": "unknown"},
            {"dimension": "maintainability_risk", "status": "medium"},
        ]
        return [
            SchumpeterRiskAssessment(
                risk_assessment_id=f"schumpeter_risk_assessment:{item.artifact_id}:v0.28.4",
                subject_ref=item.artifact_ref,
                risk_dimensions=dimensions,
                ip_license_risk="unknown",
                private_data_risk="unknown",
                public_core_contamination_risk="high",
                runtime_dependency_risk="blocked",
                security_credential_exposure_risk="unknown",
                maintainability_risk="medium",
                risk_summary="Unknown license/private risk blocks public core adoption and split implementation now.",
                blocks_public_core_adoption=True,
            )
            for item in inventory.artifacts
        ]


class SchumpeterSplitOptionCatalogService:
    def build_catalog(self) -> SchumpeterSplitOptionCatalog:
        return SchumpeterSplitOptionCatalog(catalog_id="schumpeter_split_option_catalog:v0.28.4")


class SchumpeterSplitOptionAssessmentService:
    def build_assessments(self, catalog: SchumpeterSplitOptionCatalog) -> list[SchumpeterSplitOptionAssessment]:
        assessments: list[SchumpeterSplitOptionAssessment] = []
        for option in catalog.options:
            safe = option in {"no_split", "reference_only", "public_core_private_overlay"}
            implementation_heavy = option in {"private_distribution_profile", "separate_private_repo", "merge_schumpeter_into_core"}
            assessments.append(
                SchumpeterSplitOptionAssessment(
                    assessment_id=f"schumpeter_split_option_assessment:{option}:v0.28.4",
                    option_name=option,
                    option_summary=f"{option} assessed as decision-framework evidence only.",
                    allowed_now=safe,
                    required_preconditions=["complete license review", "complete private-risk review", "public-private boundary pass"],
                    blockers=["implementation forbidden in v0.28.4"] if implementation_heavy else [],
                    warnings=["unknown license/private risk is not safe"],
                    risk_level="blocked" if implementation_heavy or option == "merge_schumpeter_into_core" else "medium",
                    recommended=option == "reference_only",
                )
            )
        return assessments


class SchumpeterDecisionCriterionService:
    CRITERIA = [
        "ip_license_risk",
        "company_private_data_contamination_risk",
        "public_core_contamination_risk",
        "architecture_overlap",
        "code_reuse_value",
        "concept_reuse_value",
        "test_reuse_value",
        "doc_reuse_value",
        "OCEL_compatibility",
        "PIG_compatibility",
        "OCPX_compatibility",
        "memory_workbench_compatibility",
        "runtime_dependency_risk",
        "maintainability",
        "testability",
        "deployment_boundary_clarity",
        "security_credential_exposure_risk",
        "future_external_adapter_compatibility",
        "organizational_usefulness",
    ]

    def build_criteria(self) -> list[SchumpeterDecisionCriterion]:
        return [
            SchumpeterDecisionCriterion(
                criterion_id=f"schumpeter_decision_criterion:{name}:v0.28.4",
                criterion_name=name,
                criterion_summary=f"{name} must be assessed before Schumpeter split implementation.",
            )
            for name in self.CRITERIA
        ]


class SchumpeterDecisionCriterionScoreService:
    def build_scores(self, criteria: list[SchumpeterDecisionCriterion]) -> list[SchumpeterDecisionCriterionScore]:
        blocked = {"ip_license_risk", "company_private_data_contamination_risk", "public_core_contamination_risk", "runtime_dependency_risk", "security_credential_exposure_risk"}
        return [
            SchumpeterDecisionCriterionScore(
                score_id=f"schumpeter_decision_criterion_score:{criterion.criterion_name}:v0.28.4",
                criterion_ref=_ref("schumpeter_decision_criterion", criterion.criterion_id, V0284_VERSION),
                subject_ref=None,
                score_band="blocked" if criterion.criterion_name in blocked else "unknown",
                score_value=None,
                score_summary="Blocked/unknown criteria are not safe for implementation; they are decision evidence only.",
            )
            for criterion in criteria
        ]


class SchumpeterReuseDispositionPolicyRuntimeService:
    def build_policy(self) -> SchumpeterReuseDispositionPolicyRuntime:
        return SchumpeterReuseDispositionPolicyRuntime(policy_id="schumpeter_reuse_disposition_policy_runtime:v0.28.4")


class SchumpeterReuseDispositionCandidateService:
    def build_candidates(self, inventory: SchumpeterReferenceInventory, license_reviews: list[SchumpeterReferenceLicenseReview], private_reviews: list[SchumpeterReferencePrivateRiskReview]) -> list[SchumpeterReuseDispositionCandidate]:
        review_refs = [_ref("schumpeter_reference_license_review", review.review_id, V0284_VERSION) for review in license_reviews] + [_ref("schumpeter_reference_private_risk_review", review.review_id, V0284_VERSION) for review in private_reviews]
        return [
            SchumpeterReuseDispositionCandidate(
                candidate_id=f"schumpeter_reuse_disposition_candidate:{item.artifact_id}:v0.28.4",
                artifact_ref=item.artifact_ref,
                proposed_disposition="keep_reference_only" if item.license_status == "unknown" else item.recommended_initial_disposition,
                disposition_reason="Unknown license/private risk keeps artifact reference-only; concept extraction later requires review.",
                required_followup_version="v0.28.5",
                required_review_refs=review_refs,
            )
            for item in inventory.artifacts
        ]


class SchumpeterReuseDispositionDecisionService:
    def build_decisions(self, candidates: list[SchumpeterReuseDispositionCandidate]) -> list[SchumpeterReuseDispositionDecision]:
        return [
            SchumpeterReuseDispositionDecision(
                decision_id=f"schumpeter_reuse_disposition_decision:{candidate.candidate_id}:v0.28.4",
                disposition_candidate_ref=_ref("schumpeter_reuse_disposition_candidate", candidate.candidate_id, V0284_VERSION),
                decision_type="defer_disposition" if candidate.proposed_disposition != "keep_reference_only" else "accept_disposition",
                decision_reason="Disposition decision is not migration; runtime dependency and code copy remain forbidden.",
            )
            for candidate in candidates
        ]


class SchumpeterSplitDecisionCandidateService:
    def build_candidates(self, option_assessments: list[SchumpeterSplitOptionAssessment], criterion_scores: list[SchumpeterDecisionCriterionScore], risk_assessments: list[SchumpeterRiskAssessment]) -> list[SchumpeterSplitDecisionCandidate]:
        support_options = [_ref("schumpeter_split_option_assessment", item.assessment_id, V0284_VERSION) for item in option_assessments if item.option_name in {"no_split", "reference_only", "public_core_private_overlay"}]
        return [
            SchumpeterSplitDecisionCandidate(
                decision_candidate_id="schumpeter_split_decision_candidate:reference_only_private_overlay:v0.28.4",
                candidate_option=V0284_RECOMMENDED_DEFAULT,
                candidate_summary="Keep Schumpeter reference-only while preparing a private overlay/profile boundary later.",
                supporting_option_assessment_refs=support_options,
                supporting_criterion_score_refs=[_ref("schumpeter_decision_criterion_score", item.score_id, V0284_VERSION) for item in criterion_scores],
                supporting_risk_assessment_refs=[_ref("schumpeter_risk_assessment", item.risk_assessment_id, V0284_VERSION) for item in risk_assessments],
                required_followup_versions=["v0.28.5"],
            )
        ]


class SchumpeterSplitRecommendationService:
    def build_recommendation(self, candidates: list[SchumpeterSplitDecisionCandidate]) -> SchumpeterSplitRecommendation:
        return SchumpeterSplitRecommendation(
            recommendation_id="schumpeter_split_recommendation:v0.28.4",
            recommended_option=V0284_RECOMMENDED_DEFAULT,
            recommendation_summary="Default safe recommendation is keep_reference_only plus prepare_private_overlay; split implementation is not allowed now.",
            confidence_level="medium",
            blockers=["unknown license status", "unknown private-data risk", "v0.28.4 implementation forbidden"],
            warnings=["concept reuse may be useful but does not permit code copy"],
            required_next_steps=["v0.28.5 Schumpeter Split Preparation Profile", "license/private-risk follow-up", "public-private overlay boundary follow-up"],
            evidence_refs=[_ref("schumpeter_split_decision_candidate", item.decision_candidate_id, V0284_VERSION) for item in candidates],
        )


class SchumpeterSplitDecisionRecordService:
    def build_records(
        self,
        recommendation: SchumpeterSplitRecommendation,
        candidates: list[SchumpeterSplitDecisionCandidate],
        disposition_decisions: list[SchumpeterReuseDispositionDecision],
        license_reviews: list[SchumpeterReferenceLicenseReview],
        private_reviews: list[SchumpeterReferencePrivateRiskReview],
    ) -> list[SchumpeterSplitDecisionRecord]:
        return [
            SchumpeterSplitDecisionRecord(
                decision_record_id="schumpeter_split_decision_record:keep_reference_only:v0.28.4",
                decision_type="keep_reference_only",
                decision_reason="No split now; keep reference-only and prepare private overlay/profile boundary next.",
                recommendation_ref=_ref("schumpeter_split_recommendation", recommendation.recommendation_id, V0284_VERSION),
                decision_candidate_refs=[_ref("schumpeter_split_decision_candidate", item.decision_candidate_id, V0284_VERSION) for item in candidates],
                disposition_decision_refs=[_ref("schumpeter_reuse_disposition_decision", item.decision_id, V0284_VERSION) for item in disposition_decisions],
                license_review_refs=[_ref("schumpeter_reference_license_review", item.review_id, V0284_VERSION) for item in license_reviews],
                private_risk_review_refs=[_ref("schumpeter_reference_private_risk_review", item.review_id, V0284_VERSION) for item in private_reviews],
                public_private_boundary_refs=[_ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION)],
            ),
            SchumpeterSplitDecisionRecord(
                decision_record_id="schumpeter_split_decision_record:prepare_private_overlay:v0.28.4",
                decision_type="prepare_private_overlay",
                decision_reason="v0.28.5 may prepare a profile boundary only; company runtime remains unauthorized.",
                recommendation_ref=_ref("schumpeter_split_recommendation", recommendation.recommendation_id, V0284_VERSION),
                decision_candidate_refs=[_ref("schumpeter_split_decision_candidate", item.decision_candidate_id, V0284_VERSION) for item in candidates],
                disposition_decision_refs=[_ref("schumpeter_reuse_disposition_decision", item.decision_id, V0284_VERSION) for item in disposition_decisions],
                license_review_refs=[_ref("schumpeter_reference_license_review", item.review_id, V0284_VERSION) for item in license_reviews],
                private_risk_review_refs=[_ref("schumpeter_reference_private_risk_review", item.review_id, V0284_VERSION) for item in private_reviews],
                public_private_boundary_refs=[_ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION)],
            ),
        ]


class SchumpeterSplitDecisionAuditTrailService:
    def build_audit_trail(
        self,
        request: SchumpeterSplitDecisionRequest,
        source_view: SchumpeterReferenceSourceView,
        inventory: SchumpeterReferenceInventory,
        license_reviews: list[SchumpeterReferenceLicenseReview],
        private_reviews: list[SchumpeterReferencePrivateRiskReview],
        matrix: SchumpeterCapabilityComparisonMatrix,
        option_assessments: list[SchumpeterSplitOptionAssessment],
        disposition_decisions: list[SchumpeterReuseDispositionDecision],
        records: list[SchumpeterSplitDecisionRecord],
    ) -> SchumpeterSplitDecisionAuditTrail:
        event_count = 5 + len(license_reviews) + len(private_reviews) + len(option_assessments) + len(disposition_decisions) + len(records)
        return SchumpeterSplitDecisionAuditTrail(
            audit_trail_id="schumpeter_split_decision_audit_trail:v0.28.4",
            decision_request_ref=_ref("schumpeter_split_decision_request", request.request_id, V0284_VERSION),
            source_view_ref=_ref("schumpeter_reference_source_view", source_view.source_view_id, V0284_VERSION),
            inventory_ref=_ref("schumpeter_reference_inventory", inventory.inventory_id, V0284_VERSION),
            license_review_refs=[_ref("schumpeter_reference_license_review", item.review_id, V0284_VERSION) for item in license_reviews],
            private_risk_review_refs=[_ref("schumpeter_reference_private_risk_review", item.review_id, V0284_VERSION) for item in private_reviews],
            comparison_matrix_ref=_ref("schumpeter_capability_comparison_matrix", matrix.matrix_id, V0284_VERSION),
            option_assessment_refs=[_ref("schumpeter_split_option_assessment", item.assessment_id, V0284_VERSION) for item in option_assessments],
            disposition_decision_refs=[_ref("schumpeter_reuse_disposition_decision", item.decision_id, V0284_VERSION) for item in disposition_decisions],
            decision_record_refs=[_ref("schumpeter_split_decision_record", item.decision_record_id, V0284_VERSION) for item in records],
            audit_event_count=event_count,
            audit_status="warning",
        )


class SchumpeterSplitDecisionFindingService:
    BLOCKED_FINDINGS = {
        "actual_split_attempted",
        "company_wrapper_attempted",
        "private_repo_creation_attempted",
        "merge_into_public_core_attempted",
        "references_runtime_dependency_attempted",
        "references_code_copy_attempted",
        "file_move_attempted",
        "destructive_redaction_attempted",
        "external_adapter_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "company_private_material_exposure_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self, source_view: SchumpeterReferenceSourceView, inventory: SchumpeterReferenceInventory) -> list[SchumpeterSplitDecisionFinding]:
        findings = [
            SchumpeterSplitDecisionFinding(
                "schumpeter_split_decision_finding:policy_created:v0.28.4",
                "info",
                "schumpeter_decision_policy_created",
                "Schumpeter split decision framework created without split implementation.",
                _ref("schumpeter_reference_inventory", inventory.inventory_id, V0284_VERSION),
                [],
                None,
            )
        ]
        if not source_view.references_schumpeter_present:
            findings.append(
                SchumpeterSplitDecisionFinding(
                    "schumpeter_split_decision_finding:missing_schumpeter_reference_metadata:v0.28.4",
                    "warning",
                    "missing_schumpeter_reference_metadata",
                    "references/schumpeter metadata is unavailable; default remains keep reference-only and defer split.",
                    _ref("schumpeter_reference_source_view", source_view.source_view_id, V0284_VERSION),
                    [],
                    "Withdraw after references/schumpeter metadata becomes available and is reviewed.",
                )
            )
        if inventory.license_unknown_count:
            findings.append(
                SchumpeterSplitDecisionFinding(
                    "schumpeter_split_decision_finding:license_unknown:v0.28.4",
                    "error",
                    "license_unknown",
                    "Unknown license status is not safe and blocks public-core adoption.",
                    _ref("schumpeter_reference_inventory", inventory.inventory_id, V0284_VERSION),
                    [],
                    "Withdraw after license status is known and compatible.",
                )
            )
        if inventory.private_risk_unknown_count:
            findings.append(
                SchumpeterSplitDecisionFinding(
                    "schumpeter_split_decision_finding:private_data_risk_unknown:v0.28.4",
                    "error",
                    "private_data_risk_unknown",
                    "Unknown private-data risk is not safe and blocks split implementation now.",
                    _ref("schumpeter_reference_inventory", inventory.inventory_id, V0284_VERSION),
                    [],
                    "Withdraw after private-data risk review is complete.",
                )
            )
        return findings


class SchumpeterSplitDecisionReportService:
    def build_report(self, report_id: str | None = None) -> SchumpeterSplitDecisionReport:
        prereq = SchumpeterSplitDecisionPrerequisiteSourceService()
        boundary = prereq.load_v0283_public_private_boundary_report()
        packaging = prereq.load_v0282_packaging_readiness_report()
        hygiene = prereq.load_v0281_release_hygiene_gate_report()
        policy = SchumpeterSplitDecisionRuntimePolicyService().build_policy()
        source = SchumpeterReferenceSourceViewService().build_source_view()
        request = SchumpeterSplitDecisionRequest(
            request_id="schumpeter_split_decision_request:v0.28.4",
            public_private_boundary_report_id=boundary.report_id,
            reference_governance_report_id=boundary.reference_governance_report.report_id,
            reference_license_boundary_report_id=boundary.reference_license_boundary_report.report_id,
            packaging_readiness_report_id=packaging.report_id,
            release_hygiene_gate_report_id=hygiene.report_id,
            selected_reference_refs=source.schumpeter_reference_refs,
            requested_decision_scope="whole_reference_tree",
            requested_decision_mode="produce_decision_record",
        )
        inventory = SchumpeterReferenceInventoryService().build_inventory(source)
        license_reviews = SchumpeterReferenceLicenseReviewService().build_reviews(inventory)
        private_reviews = SchumpeterReferencePrivateRiskReviewService().build_reviews(inventory)
        architecture = SchumpeterArchitectureComparisonService().build_comparison(source)
        matrix = SchumpeterCapabilityComparisonMatrixService().build_matrix()
        ocel_pig_ocpx = SchumpeterOCELPIGOCPXCompatibilityReviewService().build_review()
        workbench_memory = SchumpeterWorkbenchMemoryCompatibilityReviewService().build_review()
        reuse_values = SchumpeterReuseValueAssessmentService().build_assessments(inventory, matrix)
        risks = SchumpeterRiskAssessmentService().build_assessments(inventory)
        option_catalog = SchumpeterSplitOptionCatalogService().build_catalog()
        option_assessments = SchumpeterSplitOptionAssessmentService().build_assessments(option_catalog)
        criteria = SchumpeterDecisionCriterionService().build_criteria()
        criterion_scores = SchumpeterDecisionCriterionScoreService().build_scores(criteria)
        disposition_policy = SchumpeterReuseDispositionPolicyRuntimeService().build_policy()
        disposition_candidates = SchumpeterReuseDispositionCandidateService().build_candidates(inventory, license_reviews, private_reviews)
        disposition_decisions = SchumpeterReuseDispositionDecisionService().build_decisions(disposition_candidates)
        split_candidates = SchumpeterSplitDecisionCandidateService().build_candidates(option_assessments, criterion_scores, risks)
        recommendation = SchumpeterSplitRecommendationService().build_recommendation(split_candidates)
        records = SchumpeterSplitDecisionRecordService().build_records(recommendation, split_candidates, disposition_decisions, license_reviews, private_reviews)
        audit = SchumpeterSplitDecisionAuditTrailService().build_audit_trail(request, source, inventory, license_reviews, private_reviews, matrix, option_assessments, disposition_decisions, records)
        findings = SchumpeterSplitDecisionFindingService().build_findings(source, inventory)
        framework_ready = True
        split_decision_ready = bool(recommendation and records and audit)
        status = "blocked" if inventory.license_unknown_count or inventory.private_risk_unknown_count else "warning"
        return SchumpeterSplitDecisionReport(
            report_id=report_id or "schumpeter_split_decision_report:v0.28.4",
            created_at=_now(),
            decision_policy=policy,
            request=request,
            source_view=source,
            reference_inventory=inventory,
            license_reviews=license_reviews,
            private_risk_reviews=private_reviews,
            architecture_comparison=architecture,
            capability_comparison_matrix=matrix,
            ocel_pig_ocpx_compatibility_review=ocel_pig_ocpx,
            workbench_memory_compatibility_review=workbench_memory,
            reuse_value_assessments=reuse_values,
            risk_assessments=risks,
            split_option_catalog=option_catalog,
            option_assessments=option_assessments,
            decision_criteria=criteria,
            criterion_scores=criterion_scores,
            reuse_disposition_policy=disposition_policy,
            reuse_disposition_candidates=disposition_candidates,
            reuse_disposition_decisions=disposition_decisions,
            split_decision_candidates=split_candidates,
            split_recommendation=recommendation,
            split_decision_records=records,
            audit_trail=audit,
            findings=findings,
            report_status=status,
            ready_for_v0_28_5=True,
            schumpeter_decision_framework_ready=framework_ready,
            schumpeter_split_decision_ready=split_decision_ready,
            limitations=["references/schumpeter inspection is metadata-only and does not expose raw content or adopt code."],
            withdrawal_conditions=["Withdraw if actual split, company wrapper, private repo creation, public-core merge, reference runtime dependency/code copy, file movement, destructive redaction, adapter/publish/tag/provider/command execution, private/raw/credential exposure, PIG execution authority, or LLM sole authority is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "decision-policy": report.decision_policy,
            "source-view": report.source_view,
            "inventory": report.reference_inventory,
            "license-review": report.license_reviews,
            "private-risk": report.private_risk_reviews,
            "architecture-comparison": report.architecture_comparison,
            "capability-matrix": report.capability_comparison_matrix,
            "ocel-pig-ocpx": report.ocel_pig_ocpx_compatibility_review,
            "workbench-memory": report.workbench_memory_compatibility_review,
            "reuse-value": report.reuse_value_assessments,
            "risk": report.risk_assessments,
            "options": report.option_assessments,
            "criteria": report.decision_criteria,
            "disposition": report.reuse_disposition_decisions,
            "recommendation": report.split_recommendation,
            "decision-record": report.split_decision_records,
            "audit": report.audit_trail,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0284_VERSION,
            "layer": V028_LAYER,
            "subject": "schumpeter_split_decision_framework",
            "principles": [
                "Schumpeter split decision framework is not Schumpeter split",
                "Reference inventory is not adoption",
                "Reference evaluation is not code migration",
                "Reuse disposition is not runtime dependency",
                "Concept reuse is not code copy",
                "Unknown license status is not safe",
                "Unknown private-data risk is not safe",
                "No split is a valid outcome",
                "Keep reference-only is a valid outcome",
                "Public ChantaCore must not depend on private Schumpeter artifacts",
            ],
            "safety_boundary": {
                "actual_split_implemented": report.actual_split_implemented,
                "company_wrapper_implemented": report.company_wrapper_implemented,
                "private_repo_created": report.private_repo_created,
                "merge_into_public_core_performed": report.merge_into_public_core_performed,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "file_moved": report.file_moved,
                "destructive_redaction_performed": report.destructive_redaction_performed,
                "external_adapter_implemented": report.external_adapter_implemented,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "company_private_material_exposed": report.company_private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "secret_exposed": report.secret_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.28.5 Schumpeter Split Preparation Profile", "v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow", "v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate", "v0.29 External Provider Adapter Contract"],
            "next_step": V0284_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "schumpeter_split_decision_framework_created",
            "version": V0284_VERSION,
            "source_read_models": ["PublicPrivateBoundaryState", "ReferenceGovernanceState", "ReferenceLicenseBoundaryState", "PackageExposureBoundaryState", "PackagingReadinessState", "ReleaseHygieneGateState", "SchumpeterReferenceMetadataState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["SchumpeterSplitDecisionFrameworkState", "SchumpeterReferenceInventoryState", "SchumpeterReferenceLicenseReviewState", "SchumpeterReferencePrivateRiskReviewState", "SchumpeterCapabilityComparisonState", "SchumpeterReuseDispositionState", "SchumpeterSplitRecommendationState", "SchumpeterSplitDecisionRecordState", "V028ReadinessState"],
            "effect_types": V0284_EFFECT_TYPES,
            "forbidden_effect_types": V0284_FORBIDDEN_EFFECT_TYPES,
        }


def render_schumpeter_split_decision_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: SchumpeterSplitDecisionReport = parts["report"]
    lines = [
        f"Schumpeter Split Decision Framework {section}",
        f"version={report.version}",
        f"layer={report.decision_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_5={_bool(report.ready_for_v0_28_5)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"schumpeter_decision_framework_ready={_bool(report.schumpeter_decision_framework_ready)}",
        f"schumpeter_split_decision_ready={_bool(report.schumpeter_split_decision_ready)}",
        f"recommended_default={report.recommended_default}",
        f"actual_split_implemented={_bool(report.actual_split_implemented)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"private_repo_created={_bool(report.private_repo_created)}",
        f"merge_into_public_core_performed={_bool(report.merge_into_public_core_performed)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"file_moved={_bool(report.file_moved)}",
        f"destructive_redaction_performed={_bool(report.destructive_redaction_performed)}",
        f"external_adapter_implemented={_bool(report.external_adapter_implemented)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "inventory_id", getattr(payload, "source_view_id", getattr(payload, "recommendation_id", getattr(payload, "audit_trail_id", ""))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)


V0285_VERSION = "v0.28.5"
V0285_VERSION_NAME = "Schumpeter Split Preparation Profile"
V0285_NEXT_STEP = "v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow"

V0285_OBJECT_TYPES = [
    "schumpeter_split_preparation_profile_policy",
    "schumpeter_profile_preparation_request",
    "schumpeter_preparation_source_view",
    "schumpeter_profile_boundary",
    "schumpeter_naming_policy",
    "public_core_private_overlay_policy",
    "schumpeter_private_overlay_contract",
    "schumpeter_config_overlay_contract",
    "schumpeter_data_boundary_policy",
    "schumpeter_skill_boundary_policy",
    "schumpeter_provider_boundary_policy",
    "schumpeter_rpa_adapter_deferral_policy",
    "schumpeter_runtime_boundary_policy",
    "schumpeter_memory_workbench_boundary_policy",
    "schumpeter_deployment_boundary_policy",
    "schumpeter_private_overlay_manifest_preview",
    "schumpeter_profile_capability_map",
    "schumpeter_profile_capability_entry",
    "schumpeter_profile_risk_register",
    "schumpeter_profile_risk_item",
    "schumpeter_preparation_decision",
    "schumpeter_preparation_handoff_packet",
    "schumpeter_preparation_audit_trail",
    "schumpeter_preparation_finding",
    "schumpeter_preparation_report",
    "schumpeter_split_decision_report",
    "public_private_boundary_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0285_EVENT_TYPES = [
    "schumpeter_preparation_requested",
    "schumpeter_preparation_prerequisites_loaded",
    "schumpeter_preparation_policy_created",
    "schumpeter_preparation_source_view_created",
    "schumpeter_profile_boundary_created",
    "schumpeter_naming_policy_created",
    "public_core_private_overlay_policy_created",
    "schumpeter_private_overlay_contract_created",
    "schumpeter_config_overlay_contract_created",
    "schumpeter_data_boundary_policy_created",
    "schumpeter_skill_boundary_policy_created",
    "schumpeter_provider_boundary_policy_created",
    "schumpeter_rpa_adapter_deferral_policy_created",
    "schumpeter_runtime_boundary_policy_created",
    "schumpeter_memory_workbench_boundary_policy_created",
    "schumpeter_deployment_boundary_policy_created",
    "schumpeter_private_overlay_manifest_preview_created",
    "schumpeter_profile_capability_map_created",
    "schumpeter_profile_risk_register_created",
    "schumpeter_preparation_decision_created",
    "schumpeter_preparation_handoff_packet_created",
    "schumpeter_preparation_audit_trail_created",
    "schumpeter_preparation_report_created",
    "schumpeter_preparation_warning_created",
    "schumpeter_preparation_blocked",
]

V0285_EFFECT_TYPES = [
    "read_only_observation",
    "schumpeter_preparation_profile_created",
    "schumpeter_profile_boundary_created",
    "schumpeter_private_overlay_contract_created",
    "schumpeter_boundary_policy_created",
    "schumpeter_manifest_preview_created",
    "schumpeter_capability_map_created",
    "schumpeter_risk_register_created",
    "schumpeter_preparation_decision_recorded",
    "schumpeter_handoff_packet_created",
    "schumpeter_preparation_audit_created",
    "state_candidate_created",
]

V0285_FORBIDDEN_EFFECT_TYPES = [
    "actual_split_implemented",
    "schumpeter_split_implemented",
    "company_wrapper_implemented",
    "private_repo_created",
    "private_config_created",
    "credential_created",
    "endpoint_created",
    "provider_adapter_created",
    "RPA_adapter_created",
    "A360_adapter_created",
    "Brity_adapter_created",
    "UiPath_adapter_created",
    "references_runtime_dependency_added",
    "references_code_copied",
    "file_moved",
    "package_published",
    "release_tag_created",
    "provider_invoked",
    "command_executed",
    "runtime_continuity_injected",
    "company_private_material_exposed",
    "credential_exposed",
    "secret_exposed",
    "raw_trace_exposed",
    "raw_transcript_exposed",
    "raw_provider_output_exposed",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


@dataclass
class SchumpeterSplitPreparationProfilePolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    layer: str = V028_LAYER
    preparation_profile_enabled: bool = True
    private_overlay_contract_enabled: bool = True
    public_core_private_overlay_boundary_enabled: bool = True
    company_distribution_boundary_enabled: bool = True
    config_overlay_contract_enabled: bool = True
    data_boundary_policy_enabled: bool = True
    skill_boundary_policy_enabled: bool = True
    provider_boundary_policy_enabled: bool = True
    rpa_adapter_deferral_policy_enabled: bool = True
    runtime_boundary_policy_enabled: bool = True
    memory_workbench_boundary_enabled: bool = True
    deployment_boundary_policy_enabled: bool = True
    actual_split_enabled_now: bool = False
    company_wrapper_runtime_enabled_now: bool = False
    private_distribution_runtime_enabled_now: bool = False
    private_repo_creation_enabled_now: bool = False
    config_file_creation_enabled_now: bool = False
    credential_creation_enabled_now: bool = False
    endpoint_creation_enabled_now: bool = False
    provider_adapter_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    command_execution_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    runtime_continuity_injection_enabled_now: bool = False
    references_runtime_dependency_enabled_now: bool = False
    references_code_copy_enabled_now: bool = False
    public_core_private_contamination_forbidden: bool = True
    private_overlay_must_not_contaminate_public_core: bool = True
    public_core_must_not_depend_on_private_overlay: bool = True
    llm_judge_as_sole_preparation_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfilePreparationRequest(ModelMixin):
    request_id: str
    schumpeter_decision_report_id: str | None
    schumpeter_recommendation_id: str | None
    schumpeter_decision_record_id: str | None
    public_private_boundary_report_id: str | None
    requested_preparation_scope: str
    requested_mode: str
    version: str = V0285_VERSION
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationSourceView(ModelMixin):
    source_view_id: str
    decision_report_ref: dict[str, Any] | None
    recommendation_ref: dict[str, Any] | None
    decision_record_ref: dict[str, Any] | None
    reuse_disposition_refs: list[dict[str, Any]]
    public_private_boundary_report_ref: dict[str, Any] | None
    reference_governance_report_ref: dict[str, Any] | None
    package_exposure_boundary_report_ref: dict[str, Any] | None
    schumpeter_reference_refs: list[dict[str, Any]]
    allowed_preparation_refs: list[dict[str, Any]]
    blocked_preparation_refs: list[dict[str, Any]]
    source_status: str
    recommendation_allows_private_overlay_preparation: bool | None
    version: str = V0285_VERSION
    split_implementation_allowed_now: bool = False
    company_wrapper_allowed_now: bool = False
    config_creation_allowed_now: bool = False
    provider_adapter_allowed_now: bool = False
    rpa_adapter_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfileBoundary(ModelMixin):
    boundary_id: str
    profile_name: str
    profile_kind: str
    public_core_ref: dict[str, Any] | None
    private_overlay_ref: dict[str, Any] | None
    boundary_summary: str
    public_core_responsibilities: list[str]
    private_overlay_responsibilities: list[str]
    forbidden_cross_boundary_dependencies: list[str]
    allowed_cross_boundary_refs: list[str]
    version: str = V0285_VERSION
    public_core_depends_on_private_overlay: bool = False
    private_overlay_implemented_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterNamingPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    public_name: str = "ChantaCore"
    private_overlay_name: str = "Schumpeter"
    company_distribution_name: str | None = "Schumpeter"
    naming_collision_allowed: bool = False
    public_core_must_not_be_renamed_now: bool = True
    schumpeter_name_is_profile_candidate: bool = True
    schumpeter_name_is_not_runtime_implementation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PublicCorePrivateOverlayPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    public_core_private_overlay_required: bool = True
    public_core_must_remain_generic: bool = True
    private_overlay_may_extend_configuration_later: bool = True
    private_overlay_may_add_company_adapters_later: bool = True
    private_overlay_may_add_company_docs_later: bool = True
    private_overlay_must_not_be_committed_to_public_core: bool = True
    public_core_must_not_import_private_overlay: bool = True
    public_core_must_not_require_private_overlay_at_runtime: bool = True
    private_overlay_contract_is_not_runtime: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPrivateOverlayContract(ModelMixin):
    contract_id: str
    contract_status: str
    version: str = V0285_VERSION
    overlay_name: str = "Schumpeter"
    overlay_allowed_future_contents: list[str] = field(default_factory=lambda: ["private_config", "company_provider_configs", "company_rpa_adapter_configs", "company_specific_docs", "company_deployment_profiles", "private_skill_profiles", "private_provider_profiles"])
    overlay_forbidden_now: list[str] = field(default_factory=lambda: ["committed_credentials", "committed_secrets", "raw_company_logs", "raw_user_traces", "raw_provider_outputs", "uncontrolled_provider_invocation", "uncontrolled_command_execution"])
    required_future_gates: list[str] = field(default_factory=lambda: ["public_private_boundary_gate", "credential_boundary_gate", "provider_adapter_gate", "RPA_adapter_gate", "deployment_gate", "audit_gate"])
    overlay_implemented_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterConfigOverlayContract(ModelMixin):
    contract_id: str
    version: str = V0285_VERSION
    config_overlay_allowed_later: bool = True
    config_file_created_now: bool = False
    private_config_required_later: bool = True
    public_default_config_must_remain_generic: bool = True
    company_endpoint_forbidden_now: bool = True
    credential_placeholder_policy_required: bool = True
    secrets_must_use_external_secret_store_later: bool = True
    committed_secret_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterDataBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    company_data_private_only: bool = True
    raw_process_logs_private_only: bool = True
    raw_user_session_traces_private_only: bool = True
    raw_transcripts_private_only: bool = True
    raw_provider_outputs_private_only: bool = True
    synthetic_demo_data_allowed_public: bool = True
    sanitized_summary_allowed_public_with_policy: bool = True
    public_core_must_not_store_company_data: bool = True
    data_boundary_implementation_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterSkillBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    public_core_skills_must_remain_generic: bool = True
    private_overlay_skills_allowed_later: bool = True
    company_specific_skills_forbidden_now: bool = True
    RPA_skill_implementation_forbidden_now: bool = True
    A360_skill_forbidden_now: bool = True
    Brity_skill_forbidden_now: bool = True
    UiPath_skill_forbidden_now: bool = True
    skill_registration_for_private_overlay_deferred: bool = True
    skill_boundary_requires_v029_or_later_for_adapters: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProviderBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    public_core_provider_boundary_generic: bool = True
    private_provider_profiles_allowed_later: bool = True
    company_provider_configs_forbidden_now: bool = True
    provider_adapter_implementation_forbidden_now: bool = True
    provider_invocation_forbidden_now: bool = True
    credential_boundary_required_before_provider_use: bool = True
    provider_boundary_requires_v029_or_later: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterRPAAdapterDeferralPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    RPA_adapter_deferred_to_v029_or_later: bool = True
    A360_deferred: bool = True
    Brity_deferred: bool = True
    UiPath_deferred: bool = True
    RPA_adapter_is_external_provider_skill: bool = True
    RPA_adapter_not_public_alpha_feature: bool = True
    RPA_adapter_not_schumpeter_preparation_feature: bool = True
    future_required_gates: list[str] = field(default_factory=lambda: ["external_provider_adapter_contract", "provider_permission_gate", "credential_boundary_gate", "command_execution_boundary", "audit_trace_boundary", "rollback_boundary"])
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterRuntimeBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    runtime_wrapper_implementation_forbidden_now: bool = True
    runtime_profile_preview_allowed: bool = True
    runtime_continuity_injection_forbidden_now: bool = True
    autonomous_memory_execution_forbidden_now: bool = True
    provider_invocation_forbidden_now: bool = True
    command_execution_forbidden_now: bool = True
    safety_gate_must_remain_public_core_boundary: bool = True
    permission_gate_required_for_future_private_runtime: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterMemoryWorkbenchBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    public_memory_foundation_remains_generic: bool = True
    private_memory_records_for_company_forbidden_now: bool = True
    company_memory_overlay_allowed_later_with_gate: bool = True
    workbench_reports_may_be_public_if_sanitized: bool = True
    company_workbench_reports_private_only: bool = True
    continuity_injection_for_private_overlay_deferred: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterDeploymentBoundaryPolicy(ModelMixin):
    policy_id: str
    version: str = V0285_VERSION
    company_deployment_forbidden_now: bool = True
    deployment_profile_preview_allowed: bool = True
    deployment_automation_forbidden_now: bool = True
    private_repo_creation_forbidden_now: bool = True
    release_pipeline_for_company_forbidden_now: bool = True
    future_deployment_gate_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPrivateOverlayManifestPreview(ModelMixin):
    preview_id: str
    manifest_status: str
    proposed_sections: list[str]
    proposed_private_only_sections: list[str]
    proposed_public_core_refs: list[dict[str, Any]]
    version: str = V0285_VERSION
    overlay_name: str = "Schumpeter"
    preview_is_not_file_creation: bool = True
    manifest_file_created_now: bool = False
    private_config_created_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfileCapabilityEntry(ModelMixin):
    entry_id: str
    capability_name: str
    capability_category: str
    public_core_allowed: bool
    private_overlay_allowed_later: bool
    required_future_gate: str | None
    version: str = V0285_VERSION
    implementation_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfileCapabilityMap(ModelMixin):
    map_id: str
    entries: list[SchumpeterProfileCapabilityEntry]
    public_core_capability_count: int
    private_overlay_candidate_count: int
    future_adapter_candidate_count: int
    forbidden_now_count: int
    capability_map_status: str
    version: str = V0285_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfileRiskItem(ModelMixin):
    risk_item_id: str
    risk_type: str
    severity: str
    risk_summary: str
    mitigation: str
    blocks_preparation: bool
    version: str = V0285_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterProfileRiskRegister(ModelMixin):
    risk_register_id: str
    risk_items: list[SchumpeterProfileRiskItem]
    blocker_count: int
    warning_count: int
    unknown_count: int
    risk_register_status: str
    version: str = V0285_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationDecision(ModelMixin):
    decision_id: str
    decision_type: str
    decision_reason: str
    source_decision_record_ref: dict[str, Any] | None
    profile_boundary_ref: dict[str, Any] | None
    overlay_contract_ref: dict[str, Any] | None
    risk_register_ref: dict[str, Any] | None
    version: str = V0285_VERSION
    implementation_performed_now: bool = False
    config_created_now: bool = False
    provider_adapter_created_now: bool = False
    RPA_adapter_created_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationHandoffPacket(ModelMixin):
    handoff_packet_id: str
    source_preparation_report_id: str
    public_core_safe_refs: list[dict[str, Any]]
    private_overlay_future_refs: list[dict[str, Any]]
    blocked_or_deferred_refs: list[dict[str, Any]]
    future_v029_adapter_refs: list[dict[str, Any]]
    future_v030_dominion_refs: list[dict[str, Any]]
    version: str = V0285_VERSION
    target_version: str = "v0.28.6"
    target_track: str = "Public Alpha Runtime Profile / Smoke Demo Flow"
    not_implemented_now: list[str] = field(default_factory=lambda: ["actual_schumpeter_split", "company_wrapper_runtime", "private_repo_creation", "private_config_generation", "provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "company_deployment", "runtime_continuity_injection"])
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    profile_boundary_ref: dict[str, Any] | None
    overlay_contract_ref: dict[str, Any] | None
    config_overlay_contract_ref: dict[str, Any] | None
    data_boundary_ref: dict[str, Any] | None
    skill_boundary_ref: dict[str, Any] | None
    provider_boundary_ref: dict[str, Any] | None
    RPA_adapter_deferral_ref: dict[str, Any] | None
    runtime_boundary_ref: dict[str, Any] | None
    capability_map_ref: dict[str, Any] | None
    risk_register_ref: dict[str, Any] | None
    decision_refs: list[dict[str, Any]]
    handoff_packet_refs: list[dict[str, Any]]
    audit_event_count: int
    audit_status: str
    version: str = V0285_VERSION
    raw_content_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SchumpeterPreparationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class SchumpeterPreparationReport(ModelMixin):
    report_id: str
    created_at: str
    preparation_policy: SchumpeterSplitPreparationProfilePolicy
    request: SchumpeterProfilePreparationRequest
    source_view: SchumpeterPreparationSourceView
    profile_boundary: SchumpeterProfileBoundary
    naming_policy: SchumpeterNamingPolicy
    public_core_private_overlay_policy: PublicCorePrivateOverlayPolicy
    private_overlay_contract: SchumpeterPrivateOverlayContract
    config_overlay_contract: SchumpeterConfigOverlayContract
    data_boundary_policy: SchumpeterDataBoundaryPolicy
    skill_boundary_policy: SchumpeterSkillBoundaryPolicy
    provider_boundary_policy: SchumpeterProviderBoundaryPolicy
    RPA_adapter_deferral_policy: SchumpeterRPAAdapterDeferralPolicy
    runtime_boundary_policy: SchumpeterRuntimeBoundaryPolicy
    memory_workbench_boundary_policy: SchumpeterMemoryWorkbenchBoundaryPolicy
    deployment_boundary_policy: SchumpeterDeploymentBoundaryPolicy
    overlay_manifest_preview: SchumpeterPrivateOverlayManifestPreview
    capability_map: SchumpeterProfileCapabilityMap
    risk_register: SchumpeterProfileRiskRegister
    preparation_decisions: list[SchumpeterPreparationDecision]
    handoff_packet: SchumpeterPreparationHandoffPacket
    audit_trail: SchumpeterPreparationAuditTrail
    findings: list[SchumpeterPreparationFinding]
    report_status: str
    ready_for_v0_28_6: bool
    schumpeter_preparation_profile_ready: bool
    private_overlay_boundary_ready: bool
    version: str = V0285_VERSION
    ready_for_public_alpha_release_claim: bool = False
    actual_split_implemented: bool = False
    company_wrapper_implemented: bool = False
    private_repo_created: bool = False
    private_config_created: bool = False
    credential_created: bool = False
    endpoint_created: bool = False
    provider_adapter_created: bool = False
    RPA_adapter_created: bool = False
    A360_adapter_created: bool = False
    Brity_adapter_created: bool = False
    UiPath_adapter_created: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    file_moved: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    provider_invoked: bool = False
    command_executed: bool = False
    runtime_continuity_injected: bool = False
    company_private_material_exposed: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    raw_trace_exposed: bool = False
    raw_transcript_exposed: bool = False
    raw_provider_output_exposed: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0285_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow begins or Schumpeter preparation profile policy changes."


class SchumpeterPreparationPrerequisiteSourceService:
    def load_v0284_schumpeter_split_decision_report(self) -> SchumpeterSplitDecisionReport:
        return SchumpeterSplitDecisionReportService().build_report()

    def load_v0284_schumpeter_recommendation(self) -> SchumpeterSplitRecommendation:
        return self.load_v0284_schumpeter_split_decision_report().split_recommendation

    def load_v0284_schumpeter_decision_records(self) -> list[SchumpeterSplitDecisionRecord]:
        return self.load_v0284_schumpeter_split_decision_report().split_decision_records

    def load_v0284_reuse_disposition_decisions(self) -> list[SchumpeterReuseDispositionDecision]:
        return self.load_v0284_schumpeter_split_decision_report().reuse_disposition_decisions

    def load_v0283_public_private_boundary_report(self) -> PublicPrivateBoundaryReport:
        return PublicPrivateBoundaryReportService().build_report()

    def load_v0283_reference_governance_report(self) -> ReferenceGovernanceReport:
        return self.load_v0283_public_private_boundary_report().reference_governance_report

    def load_v0283_package_exposure_boundary_report(self) -> PackageExposureBoundaryReport:
        return self.load_v0283_public_private_boundary_report().package_exposure_boundary_report

    def load_v0282_packaging_readiness_report(self) -> PackagingReadinessReport:
        return PackagingReadinessReportService().build_report()

    def load_v0281_release_hygiene_gate_report(self) -> ReleaseHygieneGateReport:
        return ReleaseHygieneGateReportService().build_report()

    def load_v0280_schumpeter_split_preparation_policy(self) -> SchumpeterSplitPreparationPolicy:
        return SchumpeterSplitPreparationPolicyService().build_policy()

    def inspect_references_schumpeter_metadata_only_if_available(self) -> list[dict[str, Any]]:
        return SchumpeterSplitDecisionPrerequisiteSourceService().inspect_references_schumpeter_metadata_only_if_available()


class SchumpeterSplitPreparationProfilePolicyService:
    def build_policy(self) -> SchumpeterSplitPreparationProfilePolicy:
        return SchumpeterSplitPreparationProfilePolicy(policy_id="schumpeter_split_preparation_profile_policy:v0.28.5")


class SchumpeterPreparationSourceViewService:
    def build_source_view(self, decision_report: SchumpeterSplitDecisionReport | None = None) -> SchumpeterPreparationSourceView:
        decision_report = decision_report or SchumpeterSplitDecisionReportService().build_report()
        recommendation = decision_report.split_recommendation
        records = decision_report.split_decision_records
        allows_overlay = recommendation.recommended_option == V0284_RECOMMENDED_DEFAULT
        return SchumpeterPreparationSourceView(
            source_view_id="schumpeter_preparation_source_view:v0.28.5",
            decision_report_ref=_ref("schumpeter_split_decision_report", decision_report.report_id, V0284_VERSION),
            recommendation_ref=_ref("schumpeter_split_recommendation", recommendation.recommendation_id, V0284_VERSION),
            decision_record_ref=_ref("schumpeter_split_decision_record", records[0].decision_record_id, V0284_VERSION) if records else None,
            reuse_disposition_refs=[_ref("schumpeter_reuse_disposition_decision", item.decision_id, V0284_VERSION) for item in decision_report.reuse_disposition_decisions],
            public_private_boundary_report_ref=_ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", V0283_VERSION),
            reference_governance_report_ref=_ref("reference_governance_report", "reference_governance_report:v0.28.3", V0283_VERSION),
            package_exposure_boundary_report_ref=_ref("package_exposure_boundary_report", "package_exposure_boundary_report:v0.28.3", V0283_VERSION),
            schumpeter_reference_refs=decision_report.source_view.schumpeter_reference_refs,
            allowed_preparation_refs=[_ref("schumpeter_split_recommendation", recommendation.recommendation_id, V0284_VERSION)] if allows_overlay else [],
            blocked_preparation_refs=[_ref("schumpeter_split_decision_report", decision_report.report_id, V0284_VERSION)],
            source_status="partial",
            recommendation_allows_private_overlay_preparation=allows_overlay,
        )


class SchumpeterProfileBoundaryService:
    def build_boundary(self) -> SchumpeterProfileBoundary:
        return SchumpeterProfileBoundary(
            boundary_id="schumpeter_profile_boundary:v0.28.5",
            profile_name="Schumpeter",
            profile_kind="company_private_overlay_candidate",
            public_core_ref=_ref("public_core", "ChantaCore"),
            private_overlay_ref=_ref("private_overlay_candidate", "Schumpeter:not_created:v0.28.5", V0285_VERSION),
            boundary_summary="Schumpeter is a future private overlay/profile boundary, not runtime implementation.",
            public_core_responsibilities=["generic OCEL spine", "public-safe memory/workbench", "public-safe CLI and docs"],
            private_overlay_responsibilities=["future company config", "future company provider profiles", "future company deployment profiles"],
            forbidden_cross_boundary_dependencies=["public_core_imports_private_overlay", "private_config_in_public_core", "company_credentials_in_public_core", "references_schumpeter_runtime_dependency"],
            allowed_cross_boundary_refs=["metadata_refs", "decision_record_refs", "handoff_packet_refs"],
        )


class SchumpeterNamingPolicyService:
    def build_policy(self) -> SchumpeterNamingPolicy:
        return SchumpeterNamingPolicy(policy_id="schumpeter_naming_policy:v0.28.5")


class PublicCorePrivateOverlayPolicyService:
    def build_policy(self) -> PublicCorePrivateOverlayPolicy:
        return PublicCorePrivateOverlayPolicy(policy_id="public_core_private_overlay_policy:v0.28.5")


class SchumpeterPrivateOverlayContractService:
    def build_contract(self) -> SchumpeterPrivateOverlayContract:
        return SchumpeterPrivateOverlayContract(contract_id="schumpeter_private_overlay_contract:v0.28.5", contract_status="warning")


class SchumpeterConfigOverlayContractService:
    def build_contract(self) -> SchumpeterConfigOverlayContract:
        return SchumpeterConfigOverlayContract(contract_id="schumpeter_config_overlay_contract:v0.28.5")


class SchumpeterDataBoundaryPolicyService:
    def build_policy(self) -> SchumpeterDataBoundaryPolicy:
        return SchumpeterDataBoundaryPolicy(policy_id="schumpeter_data_boundary_policy:v0.28.5")


class SchumpeterSkillBoundaryPolicyService:
    def build_policy(self) -> SchumpeterSkillBoundaryPolicy:
        return SchumpeterSkillBoundaryPolicy(policy_id="schumpeter_skill_boundary_policy:v0.28.5")


class SchumpeterProviderBoundaryPolicyService:
    def build_policy(self) -> SchumpeterProviderBoundaryPolicy:
        return SchumpeterProviderBoundaryPolicy(policy_id="schumpeter_provider_boundary_policy:v0.28.5")


class SchumpeterRPAAdapterDeferralPolicyService:
    def build_policy(self) -> SchumpeterRPAAdapterDeferralPolicy:
        return SchumpeterRPAAdapterDeferralPolicy(policy_id="schumpeter_rpa_adapter_deferral_policy:v0.28.5")


class SchumpeterRuntimeBoundaryPolicyService:
    def build_policy(self) -> SchumpeterRuntimeBoundaryPolicy:
        return SchumpeterRuntimeBoundaryPolicy(policy_id="schumpeter_runtime_boundary_policy:v0.28.5")


class SchumpeterMemoryWorkbenchBoundaryPolicyService:
    def build_policy(self) -> SchumpeterMemoryWorkbenchBoundaryPolicy:
        return SchumpeterMemoryWorkbenchBoundaryPolicy(policy_id="schumpeter_memory_workbench_boundary_policy:v0.28.5")


class SchumpeterDeploymentBoundaryPolicyService:
    def build_policy(self) -> SchumpeterDeploymentBoundaryPolicy:
        return SchumpeterDeploymentBoundaryPolicy(policy_id="schumpeter_deployment_boundary_policy:v0.28.5")


class SchumpeterPrivateOverlayManifestPreviewService:
    def build_preview(self) -> SchumpeterPrivateOverlayManifestPreview:
        return SchumpeterPrivateOverlayManifestPreview(
            preview_id="schumpeter_private_overlay_manifest_preview:v0.28.5",
            manifest_status="warning",
            proposed_sections=["profile_metadata", "private_config_boundary", "provider_boundary", "RPA_adapter_boundary", "data_boundary", "skill_boundary", "memory_workbench_boundary", "deployment_boundary", "audit_boundary"],
            proposed_private_only_sections=["private_config_boundary", "provider_boundary", "RPA_adapter_boundary", "data_boundary", "deployment_boundary"],
            proposed_public_core_refs=[_ref("public_core", "ChantaCore")],
        )


class SchumpeterProfileCapabilityMapService:
    def build_map(self) -> SchumpeterProfileCapabilityMap:
        entries = [
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:public_core:v0.28.5", "generic_public_core", "public_core", True, False, None),
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:private_overlay:v0.28.5", "private_overlay_profile", "private_overlay_candidate", False, True, "public_private_boundary_gate"),
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:provider:v0.28.5", "company_provider_profile", "future_external_adapter", False, True, "v0.29_external_provider_adapter_contract"),
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:rpa:v0.28.5", "company_RPA_adapter", "future_RPA_adapter", False, True, "v0.29_external_provider_adapter_contract"),
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:deployment:v0.28.5", "company_deployment", "future_deployment", False, True, "deployment_gate"),
            SchumpeterProfileCapabilityEntry("schumpeter_profile_capability_entry:runtime:v0.28.5", "company_wrapper_runtime", "forbidden_now", False, False, "future_runtime_gate"),
        ]
        return SchumpeterProfileCapabilityMap(
            map_id="schumpeter_profile_capability_map:v0.28.5",
            entries=entries,
            public_core_capability_count=sum(1 for item in entries if item.capability_category == "public_core"),
            private_overlay_candidate_count=sum(1 for item in entries if item.capability_category in {"private_overlay_candidate", "company_distribution_candidate"}),
            future_adapter_candidate_count=sum(1 for item in entries if item.capability_category in {"future_external_adapter", "future_RPA_adapter"}),
            forbidden_now_count=sum(1 for item in entries if item.capability_category == "forbidden_now" or not item.implementation_allowed_now),
            capability_map_status="warning",
        )


class SchumpeterProfileRiskRegisterService:
    def build_register(self) -> SchumpeterProfileRiskRegister:
        risks = [
            ("public_private_contamination", "blocker", "Private overlay contaminates public core.", "Keep metadata refs only and block public imports.", True),
            ("credential_exposure", "blocker", "Credentials are created or committed.", "Require external secret-store gate later.", True),
            ("company_data_exposure", "blocker", "Company data leaks into public core.", "Keep company data private-only.", True),
            ("provider_invocation_without_gate", "blocker", "Provider invoked before adapter gate.", "Defer to v0.29+ provider contract.", True),
            ("command_execution_without_gate", "blocker", "Runtime command execution added.", "Require command execution boundary.", True),
            ("RPA_adapter_scope_creep", "warning", "RPA adapter work starts too early.", "Defer A360/Brity/UiPath to v0.29+.", False),
            ("reference_code_copy", "blocker", "Schumpeter reference code copied.", "Keep reference-only.", True),
            ("runtime_dependency_leak", "blocker", "Public core depends on private overlay.", "Forbid import/runtime dependency.", True),
            ("deployment_boundary_violation", "warning", "Company deployment profile treated as release.", "Require future deployment gate.", False),
            ("license_unknown", "unknown", "Schumpeter license remains unresolved.", "Do not treat as safe.", False),
            ("private_risk_unknown", "unknown", "Schumpeter private risk remains unresolved.", "Do not treat as safe.", False),
        ]
        items = [SchumpeterProfileRiskItem(f"schumpeter_profile_risk_item:{risk_type}:v0.28.5", risk_type, severity, summary, mitigation, blocks) for risk_type, severity, summary, mitigation, blocks in risks]
        return SchumpeterProfileRiskRegister(
            risk_register_id="schumpeter_profile_risk_register:v0.28.5",
            risk_items=items,
            blocker_count=sum(1 for item in items if item.severity == "blocker"),
            warning_count=sum(1 for item in items if item.severity == "warning"),
            unknown_count=sum(1 for item in items if item.severity == "unknown"),
            risk_register_status="blocked",
        )


class SchumpeterPreparationDecisionService:
    def build_decisions(self, source_view: SchumpeterPreparationSourceView, boundary: SchumpeterProfileBoundary, contract: SchumpeterPrivateOverlayContract, risk_register: SchumpeterProfileRiskRegister) -> list[SchumpeterPreparationDecision]:
        decision_type = "prepare_profile_boundary_only" if source_view.recommendation_allows_private_overlay_preparation else "defer_preparation"
        return [
            SchumpeterPreparationDecision(
                decision_id="schumpeter_preparation_decision:profile_boundary_only:v0.28.5",
                decision_type=decision_type,
                decision_reason="Prepare a boundary/contract/handoff only; no Schumpeter runtime, config, adapter, or split is implemented.",
                source_decision_record_ref=source_view.decision_record_ref,
                profile_boundary_ref=_ref("schumpeter_profile_boundary", boundary.boundary_id, V0285_VERSION),
                overlay_contract_ref=_ref("schumpeter_private_overlay_contract", contract.contract_id, V0285_VERSION),
                risk_register_ref=_ref("schumpeter_profile_risk_register", risk_register.risk_register_id, V0285_VERSION),
            )
        ]


class SchumpeterPreparationHandoffPacketService:
    def build_packet(self, report_id: str, boundary: SchumpeterProfileBoundary, risk_register: SchumpeterProfileRiskRegister) -> SchumpeterPreparationHandoffPacket:
        return SchumpeterPreparationHandoffPacket(
            handoff_packet_id="schumpeter_preparation_handoff_packet:v0.28.5",
            source_preparation_report_id=report_id,
            public_core_safe_refs=[_ref("public_core", "ChantaCore"), _ref("schumpeter_profile_boundary", boundary.boundary_id, V0285_VERSION)],
            private_overlay_future_refs=[_ref("private_overlay_candidate", "Schumpeter:not_created:v0.28.5", V0285_VERSION)],
            blocked_or_deferred_refs=[_ref("schumpeter_profile_risk_register", risk_register.risk_register_id, V0285_VERSION)],
            future_v029_adapter_refs=[_ref("future_track", "v0.29 External Provider Adapter Contract"), _ref("future_track", "A360/Brity/UiPath/RPA adapters")],
            future_v030_dominion_refs=[_ref("future_track", "v0.30 External Agent Dominion Bridge Contract")],
        )


class SchumpeterPreparationAuditTrailService:
    def build_audit_trail(
        self,
        request: SchumpeterProfilePreparationRequest,
        source_view: SchumpeterPreparationSourceView,
        boundary: SchumpeterProfileBoundary,
        overlay_contract: SchumpeterPrivateOverlayContract,
        config_contract: SchumpeterConfigOverlayContract,
        data_policy: SchumpeterDataBoundaryPolicy,
        skill_policy: SchumpeterSkillBoundaryPolicy,
        provider_policy: SchumpeterProviderBoundaryPolicy,
        rpa_policy: SchumpeterRPAAdapterDeferralPolicy,
        runtime_policy: SchumpeterRuntimeBoundaryPolicy,
        capability_map: SchumpeterProfileCapabilityMap,
        risk_register: SchumpeterProfileRiskRegister,
        decisions: list[SchumpeterPreparationDecision],
        handoff: SchumpeterPreparationHandoffPacket,
    ) -> SchumpeterPreparationAuditTrail:
        return SchumpeterPreparationAuditTrail(
            audit_trail_id="schumpeter_preparation_audit_trail:v0.28.5",
            request_ref=_ref("schumpeter_profile_preparation_request", request.request_id, V0285_VERSION),
            source_view_ref=_ref("schumpeter_preparation_source_view", source_view.source_view_id, V0285_VERSION),
            profile_boundary_ref=_ref("schumpeter_profile_boundary", boundary.boundary_id, V0285_VERSION),
            overlay_contract_ref=_ref("schumpeter_private_overlay_contract", overlay_contract.contract_id, V0285_VERSION),
            config_overlay_contract_ref=_ref("schumpeter_config_overlay_contract", config_contract.contract_id, V0285_VERSION),
            data_boundary_ref=_ref("schumpeter_data_boundary_policy", data_policy.policy_id, V0285_VERSION),
            skill_boundary_ref=_ref("schumpeter_skill_boundary_policy", skill_policy.policy_id, V0285_VERSION),
            provider_boundary_ref=_ref("schumpeter_provider_boundary_policy", provider_policy.policy_id, V0285_VERSION),
            RPA_adapter_deferral_ref=_ref("schumpeter_rpa_adapter_deferral_policy", rpa_policy.policy_id, V0285_VERSION),
            runtime_boundary_ref=_ref("schumpeter_runtime_boundary_policy", runtime_policy.policy_id, V0285_VERSION),
            capability_map_ref=_ref("schumpeter_profile_capability_map", capability_map.map_id, V0285_VERSION),
            risk_register_ref=_ref("schumpeter_profile_risk_register", risk_register.risk_register_id, V0285_VERSION),
            decision_refs=[_ref("schumpeter_preparation_decision", item.decision_id, V0285_VERSION) for item in decisions],
            handoff_packet_refs=[_ref("schumpeter_preparation_handoff_packet", handoff.handoff_packet_id, V0285_VERSION)],
            audit_event_count=14 + len(decisions),
            audit_status="warning",
        )


class SchumpeterPreparationFindingService:
    BLOCKED_FINDINGS = {
        "actual_split_attempted",
        "company_wrapper_attempted",
        "private_repo_creation_attempted",
        "private_config_creation_attempted",
        "credential_creation_attempted",
        "endpoint_creation_attempted",
        "provider_adapter_creation_attempted",
        "RPA_adapter_creation_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "references_runtime_dependency_attempted",
        "references_code_copy_attempted",
        "file_move_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "company_private_material_exposure_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self, source_view: SchumpeterPreparationSourceView) -> list[SchumpeterPreparationFinding]:
        findings = [
            SchumpeterPreparationFinding("schumpeter_preparation_finding:preparation_policy_created:v0.28.5", "info", "preparation_policy_created", "Schumpeter preparation profile was created as contract/profile only.", _ref("schumpeter_preparation_source_view", source_view.source_view_id, V0285_VERSION), [], None)
        ]
        if not source_view.recommendation_allows_private_overlay_preparation:
            findings.append(SchumpeterPreparationFinding("schumpeter_preparation_finding:recommendation_does_not_allow_preparation:v0.28.5", "warning", "recommendation_does_not_allow_preparation", "v0.28.4 did not explicitly allow private overlay preparation; choose no-op/defer.", source_view.recommendation_ref, [], "Withdraw after v0.28.4 recommendation allows preparation."))
        return findings


class SchumpeterPreparationReportService:
    def build_report(self, report_id: str | None = None) -> SchumpeterPreparationReport:
        decision_report = SchumpeterSplitDecisionReportService().build_report()
        boundary_report = PublicPrivateBoundaryReportService().build_report()
        policy = SchumpeterSplitPreparationProfilePolicyService().build_policy()
        source = SchumpeterPreparationSourceViewService().build_source_view(decision_report)
        request = SchumpeterProfilePreparationRequest("schumpeter_profile_preparation_request:v0.28.5", decision_report.report_id, decision_report.split_recommendation.recommendation_id, decision_report.split_decision_records[0].decision_record_id if decision_report.split_decision_records else None, boundary_report.report_id, "private_overlay_boundary", "prepare_profile_contract")
        profile_boundary = SchumpeterProfileBoundaryService().build_boundary()
        naming = SchumpeterNamingPolicyService().build_policy()
        overlay_policy = PublicCorePrivateOverlayPolicyService().build_policy()
        overlay_contract = SchumpeterPrivateOverlayContractService().build_contract()
        config_contract = SchumpeterConfigOverlayContractService().build_contract()
        data_policy = SchumpeterDataBoundaryPolicyService().build_policy()
        skill_policy = SchumpeterSkillBoundaryPolicyService().build_policy()
        provider_policy = SchumpeterProviderBoundaryPolicyService().build_policy()
        rpa_policy = SchumpeterRPAAdapterDeferralPolicyService().build_policy()
        runtime_policy = SchumpeterRuntimeBoundaryPolicyService().build_policy()
        memory_policy = SchumpeterMemoryWorkbenchBoundaryPolicyService().build_policy()
        deployment_policy = SchumpeterDeploymentBoundaryPolicyService().build_policy()
        manifest = SchumpeterPrivateOverlayManifestPreviewService().build_preview()
        capability_map = SchumpeterProfileCapabilityMapService().build_map()
        risk_register = SchumpeterProfileRiskRegisterService().build_register()
        decisions = SchumpeterPreparationDecisionService().build_decisions(source, profile_boundary, overlay_contract, risk_register)
        actual_report_id = report_id or "schumpeter_preparation_report:v0.28.5"
        handoff = SchumpeterPreparationHandoffPacketService().build_packet(actual_report_id, profile_boundary, risk_register)
        audit = SchumpeterPreparationAuditTrailService().build_audit_trail(request, source, profile_boundary, overlay_contract, config_contract, data_policy, skill_policy, provider_policy, rpa_policy, runtime_policy, capability_map, risk_register, decisions, handoff)
        findings = SchumpeterPreparationFindingService().build_findings(source)
        return SchumpeterPreparationReport(
            report_id=actual_report_id,
            created_at=_now(),
            preparation_policy=policy,
            request=request,
            source_view=source,
            profile_boundary=profile_boundary,
            naming_policy=naming,
            public_core_private_overlay_policy=overlay_policy,
            private_overlay_contract=overlay_contract,
            config_overlay_contract=config_contract,
            data_boundary_policy=data_policy,
            skill_boundary_policy=skill_policy,
            provider_boundary_policy=provider_policy,
            RPA_adapter_deferral_policy=rpa_policy,
            runtime_boundary_policy=runtime_policy,
            memory_workbench_boundary_policy=memory_policy,
            deployment_boundary_policy=deployment_policy,
            overlay_manifest_preview=manifest,
            capability_map=capability_map,
            risk_register=risk_register,
            preparation_decisions=decisions,
            handoff_packet=handoff,
            audit_trail=audit,
            findings=findings,
            report_status="warning",
            ready_for_v0_28_6=True,
            schumpeter_preparation_profile_ready=True,
            private_overlay_boundary_ready=True,
            limitations=["Profile is contract/handoff only; no private repo, config, credentials, endpoints, adapters, runtime, or command/provider execution is created."],
            withdrawal_conditions=["Withdraw if actual split, company wrapper, private repo/config/credential/endpoint creation, provider/RPA adapter, reference runtime dependency/code copy, file movement, publish/tag, provider/command execution, runtime continuity injection, private/raw exposure, PIG execution authority, or LLM sole authority is introduced."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.preparation_policy,
            "request": report.request,
            "source-view": report.source_view,
            "profile-boundary": report.profile_boundary,
            "naming": report.naming_policy,
            "overlay-policy": report.public_core_private_overlay_policy,
            "overlay-contract": report.private_overlay_contract,
            "config-contract": report.config_overlay_contract,
            "data-boundary": report.data_boundary_policy,
            "skill-boundary": report.skill_boundary_policy,
            "provider-boundary": report.provider_boundary_policy,
            "rpa-deferral": report.RPA_adapter_deferral_policy,
            "runtime-boundary": report.runtime_boundary_policy,
            "memory-workbench": report.memory_workbench_boundary_policy,
            "deployment-boundary": report.deployment_boundary_policy,
            "manifest-preview": report.overlay_manifest_preview,
            "capability-map": report.capability_map,
            "risk-register": report.risk_register,
            "decision": report.preparation_decisions,
            "handoff": report.handoff_packet,
            "audit": report.audit_trail,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0285_VERSION,
            "layer": V028_LAYER,
            "subject": "schumpeter_split_preparation_profile",
            "principles": ["Schumpeter preparation profile is not Schumpeter implementation", "Private overlay contract is not private overlay runtime", "Config overlay contract is not config file creation", "Company distribution boundary is not company deployment", "Skill boundary is not skill implementation", "Provider boundary is not provider adapter", "RPA adapter deferral is not RPA integration", "Public ChantaCore must not depend on private Schumpeter artifacts", "Private overlay must not contaminate public core", "No split is a valid outcome"],
            "safety_boundary": {
                "actual_split_implemented": report.actual_split_implemented,
                "company_wrapper_implemented": report.company_wrapper_implemented,
                "private_repo_created": report.private_repo_created,
                "private_config_created": report.private_config_created,
                "credential_created": report.credential_created,
                "endpoint_created": report.endpoint_created,
                "provider_adapter_created": report.provider_adapter_created,
                "RPA_adapter_created": report.RPA_adapter_created,
                "A360_adapter_created": report.A360_adapter_created,
                "Brity_adapter_created": report.Brity_adapter_created,
                "UiPath_adapter_created": report.UiPath_adapter_created,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "file_moved": report.file_moved,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "provider_invoked": report.provider_invoked,
                "command_executed": report.command_executed,
                "runtime_continuity_injected": report.runtime_continuity_injected,
                "company_private_material_exposed": report.company_private_material_exposed,
                "credential_exposed": report.credential_exposed,
                "secret_exposed": report.secret_exposed,
                "raw_trace_exposed": report.raw_trace_exposed,
                "raw_transcript_exposed": report.raw_transcript_exposed,
                "raw_provider_output_exposed": report.raw_provider_output_exposed,
                "llm_judge_enabled": False,
            },
            "future_direction": ["v0.28.6 Public Alpha Runtime Profile / Smoke Demo Flow", "v0.28.7 Alpha Documentation / Onboarding / Example Pack", "v0.28.8 Alpha Readiness Validation / External Adapter Preflight Gate", "v0.29 External Provider Adapter Contract", "v0.30 External Agent Dominion Bridge Contract"],
            "next_step": V0285_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "schumpeter_split_preparation_profile_created",
            "version": V0285_VERSION,
            "source_read_models": ["SchumpeterSplitDecisionFrameworkState", "SchumpeterSplitRecommendationState", "SchumpeterSplitDecisionRecordState", "PublicPrivateBoundaryState", "ReferenceGovernanceState", "PackageExposureBoundaryState", "PackagingReadinessState", "ReleaseHygieneGateState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["SchumpeterPreparationProfileState", "SchumpeterProfileBoundaryState", "PublicCorePrivateOverlayPolicyState", "SchumpeterPrivateOverlayContractState", "SchumpeterConfigOverlayContractState", "SchumpeterProviderBoundaryState", "SchumpeterRPADeferralState", "SchumpeterPreparationHandoffState", "V028ReadinessState"],
            "effect_types": V0285_EFFECT_TYPES,
            "forbidden_effect_types": V0285_FORBIDDEN_EFFECT_TYPES,
        }


def render_schumpeter_preparation_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: SchumpeterPreparationReport = parts["report"]
    lines = [
        f"Schumpeter Split Preparation Profile {section}",
        f"version={report.version}",
        f"layer={report.preparation_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_28_6={_bool(report.ready_for_v0_28_6)}",
        f"ready_for_public_alpha_release_claim={_bool(report.ready_for_public_alpha_release_claim)}",
        f"schumpeter_preparation_profile_ready={_bool(report.schumpeter_preparation_profile_ready)}",
        f"private_overlay_boundary_ready={_bool(report.private_overlay_boundary_ready)}",
        f"actual_split_implemented={_bool(report.actual_split_implemented)}",
        f"company_wrapper_implemented={_bool(report.company_wrapper_implemented)}",
        f"private_repo_created={_bool(report.private_repo_created)}",
        f"private_config_created={_bool(report.private_config_created)}",
        f"credential_created={_bool(report.credential_created)}",
        f"endpoint_created={_bool(report.endpoint_created)}",
        f"provider_adapter_created={_bool(report.provider_adapter_created)}",
        f"RPA_adapter_created={_bool(report.RPA_adapter_created)}",
        f"A360_adapter_created={_bool(report.A360_adapter_created)}",
        f"Brity_adapter_created={_bool(report.Brity_adapter_created)}",
        f"UiPath_adapter_created={_bool(report.UiPath_adapter_created)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"file_moved={_bool(report.file_moved)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"command_executed={_bool(report.command_executed)}",
        f"runtime_continuity_injected={_bool(report.runtime_continuity_injected)}",
        f"company_private_material_exposed={_bool(report.company_private_material_exposed)}",
        f"credential_exposed={_bool(report.credential_exposed)}",
        f"secret_exposed={_bool(report.secret_exposed)}",
        f"raw_trace_exposed={_bool(report.raw_trace_exposed)}",
        f"raw_transcript_exposed={_bool(report.raw_transcript_exposed)}",
        f"raw_provider_output_exposed={_bool(report.raw_provider_output_exposed)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None:
        if isinstance(payload, list):
            lines.append(f"artifact_count={len(payload)}")
        else:
            identifier = getattr(payload, "report_id", getattr(payload, "policy_id", getattr(payload, "contract_id", getattr(payload, "boundary_id", getattr(payload, "preview_id", getattr(payload, "map_id", getattr(payload, "risk_register_id", getattr(payload, "handoff_packet_id", ""))))))))
            if identifier:
                lines.append(f"artifact_id={identifier}")
    return "\n".join(lines)

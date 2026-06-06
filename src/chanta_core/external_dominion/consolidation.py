from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, FUTURE_TRACK_LEVELS, normalize_dominion_level
from chanta_core.external_dominion.preview_gate import ExternalDominionV0309ConsolidationHandoff


V0309_VERSION = "v0.30.9"
FOUNDATION_RELEASE_NAME = "External Dominion Control Plane Foundation v1"
REQUIRED_V030_VERSIONS = [f"v0.30.{index}" for index in range(0, 9)]
PROHIBITED_RUNTIME_SURFACES = [
    "external_execution",
    "limited_preview_execution",
    "network",
    "credential",
    "command",
    "provider",
    "browser",
    "rpa",
    "gateway",
    "delegation",
    "packet_send",
    "rollback_execution",
    "retry_execution",
]


class ExternalDominionConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDominionReleaseReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    FOUNDATION_READY = "foundation_ready"
    HANDOFF_READY_FOR_V031 = "handoff_ready_for_v031"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _normalize_status(value: ExternalDominionConsolidationStatus | str) -> ExternalDominionConsolidationStatus:
    if isinstance(value, ExternalDominionConsolidationStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("consolidation status must not be blank")
        return ExternalDominionConsolidationStatus(stripped)
    raise TypeError(f"unsupported consolidation status: {value!r}")


def _normalize_readiness(value: ExternalDominionReleaseReadinessLevel | str) -> ExternalDominionReleaseReadinessLevel:
    if isinstance(value, ExternalDominionReleaseReadinessLevel):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("readiness level must not be blank")
        return ExternalDominionReleaseReadinessLevel(stripped)
    raise TypeError(f"unsupported readiness level: {value!r}")


def _version_includes_v0309(version: str) -> bool:
    return "v0.30.9" in version


def _contains_required_versions(versions: list[str]) -> bool:
    return all(version in versions for version in REQUIRED_V030_VERSIONS)


def _future_track_values(levels: list[DominionLevel | int | str]) -> set[DominionLevel]:
    return {normalize_dominion_level(level) for level in levels}


@dataclass(frozen=True)
class ExternalDominionReleaseFlagSet:
    flag_set_id: str
    version: str
    external_dominion_control_plane_foundation_ready: bool
    ready_for_v031_internal_triad_skill_foundation: bool
    ready_for_external_execution: bool = False
    ready_for_limited_preview_execution: bool = False
    limited_preview_execution_ready_now: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_rpa_runtime_control: bool = False
    ready_for_browser_runtime_control: bool = False
    ready_for_gateway_control: bool = False
    ready_for_external_agent_delegation_runtime: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    max_grantable_level: DominionLevel | int | str = DominionLevel.D3_SIMULATE
    future_track_levels: list[DominionLevel | int | str] = field(default_factory=lambda: list(FUTURE_TRACK_LEVELS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _require_non_blank("version", self.version)
        if not _version_includes_v0309(self.version):
            raise ValueError("version must include v0.30.9")
        for name in (
            "ready_for_external_execution",
            "ready_for_limited_preview_execution",
            "limited_preview_execution_ready_now",
            "ready_for_provider_invocation",
            "ready_for_network_access",
            "ready_for_credential_access",
            "ready_for_command_execution",
            "ready_for_rpa_runtime_control",
            "ready_for_browser_runtime_control",
            "ready_for_gateway_control",
            "ready_for_external_agent_delegation_runtime",
            "production_certified",
            "live_adapter_certified",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.30.9")
        if normalize_dominion_level(self.max_grantable_level) > DominionLevel.D3_SIMULATE:
            raise ValueError("max_grantable_level must not exceed D3_SIMULATE")
        if not FUTURE_TRACK_LEVELS.issubset(_future_track_values(self.future_track_levels)):
            raise ValueError("D4-D9 must be present in future_track_levels")


def release_flags_preserve_runtime_false(flags: ExternalDominionReleaseFlagSet) -> bool:
    return (
        flags.ready_for_external_execution is False
        and flags.ready_for_limited_preview_execution is False
        and flags.limited_preview_execution_ready_now is False
        and flags.ready_for_provider_invocation is False
        and flags.ready_for_network_access is False
        and flags.ready_for_credential_access is False
        and flags.ready_for_command_execution is False
        and flags.ready_for_rpa_runtime_control is False
        and flags.ready_for_browser_runtime_control is False
        and flags.ready_for_gateway_control is False
        and flags.ready_for_external_agent_delegation_runtime is False
        and flags.production_certified is False
        and flags.live_adapter_certified is False
        and normalize_dominion_level(flags.max_grantable_level) <= DominionLevel.D3_SIMULATE
    )


@dataclass(frozen=True)
class ExternalDominionFoundationSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_artifact_groups: list[str]
    release_flags: ExternalDominionReleaseFlagSet
    consolidation_status: ExternalDominionConsolidationStatus | str
    readiness_level: ExternalDominionReleaseReadinessLevel | str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("version", self.version)
        if not _version_includes_v0309(self.version):
            raise ValueError("version must include v0.30.9")
        _require_non_blank("release_name", self.release_name)
        _validate_string_list("included_versions", self.included_versions)
        _validate_string_list("included_artifact_groups", self.included_artifact_groups)
        if not _contains_required_versions(self.included_versions):
            raise ValueError("included_versions must include v0.30.0 through v0.30.8")
        if not release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-execution runtime flags")
        _normalize_status(self.consolidation_status)
        _normalize_readiness(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("known_gaps", self.known_gaps)
        _validate_string_list("known_risks", self.known_risks)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)

    @property
    def runtime_enablement(self) -> bool:
        return False


@dataclass(frozen=True)
class CoverageMatrixBase:
    coverage_id: str
    target_id: str | None = None
    candidate_id: str | None = None
    covered_artifact_refs: list[str] = field(default_factory=list)
    missing_artifact_refs: list[str] = field(default_factory=list)
    coverage_notes: list[str] = field(default_factory=list)
    coverage_complete: bool = False
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("coverage_id", self.coverage_id)
        _validate_string_list("covered_artifact_refs", self.covered_artifact_refs)
        _validate_string_list("missing_artifact_refs", self.missing_artifact_refs)
        _validate_string_list("coverage_notes", self.coverage_notes)
        _validate_string_list("blocking_gaps", self.blocking_gaps)
        _validate_string_list("non_blocking_gaps", self.non_blocking_gaps)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be true when blocking_gaps is non-empty")

    @property
    def runtime_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalTargetCoverageMatrix(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class ExternalCapabilityObservationCoverage(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class DigestionCandidateCoverageMatrix(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class DominionTargetCoverageMatrix(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class DominionAuthorityCoverageMatrix(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class ExternalDelegationDryRunCoverage(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class ApprovalAuditRollbackCoverage(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class CertificationMatrixCoverage(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class LimitedPreviewGateCoverage(CoverageMatrixBase):
    pass


@dataclass(frozen=True)
class ExternalDominionGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str] = field(default_factory=list)
    non_blocking_gaps: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=lambda: ["D4-D9 future-track", *PROHIBITED_RUNTIME_SURFACES])
    recommended_v031_items: list[str] = field(default_factory=list)
    recommended_later_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _require_non_blank("version", self.version)
        _validate_string_list("blocking_gaps", self.blocking_gaps)
        _validate_string_list("non_blocking_gaps", self.non_blocking_gaps)
        _validate_string_list("future_track_items", self.future_track_items)
        _validate_string_list("recommended_v031_items", self.recommended_v031_items)
        _validate_string_list("recommended_later_items", self.recommended_later_items)
        _validate_string_list("evidence_refs", self.evidence_refs)
        lower = " ".join(self.future_track_items).lower()
        if "d4" not in lower or "d9" not in lower:
            raise ValueError("future_track_items must preserve D4-D9")

    @property
    def blocks_handoff(self) -> bool:
        return bool(self.blocking_gaps)


@dataclass(frozen=True)
class ExternalDominionRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[str] = field(default_factory=list)
    high_risk_surfaces: list[str] = field(default_factory=list)
    prohibited_runtime_surfaces: list[str] = field(default_factory=lambda: list(PROHIBITED_RUNTIME_SURFACES))
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _require_non_blank("version", self.version)
        _validate_string_list("known_risks", self.known_risks)
        _validate_string_list("high_risk_surfaces", self.high_risk_surfaces)
        _validate_string_list("prohibited_runtime_surfaces", self.prohibited_runtime_surfaces)
        _validate_string_list("mitigations", self.mitigations)
        _validate_string_list("unresolved_risks", self.unresolved_risks)
        _validate_string_list("evidence_refs", self.evidence_refs)
        missing = set(PROHIBITED_RUNTIME_SURFACES) - set(self.prohibited_runtime_surfaces)
        if missing:
            raise ValueError("prohibited_runtime_surfaces must include all runtime surfaces")

    @property
    def proves_exploitability(self) -> bool:
        return False

    @property
    def grants_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionV031HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    internal_triad_focus: list[str]
    observation_skill_handoff_items: list[str] = field(default_factory=list)
    digestion_skill_handoff_items: list[str] = field(default_factory=list)
    dominion_skill_handoff_items: list[str] = field(default_factory=list)
    reusable_contract_refs: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(PROHIBITED_RUNTIME_SURFACES))
    future_track_items: list[str] = field(default_factory=lambda: ["D4-D9 future-track", *PROHIBITED_RUNTIME_SURFACES])
    evidence_refs: list[str] = field(default_factory=list)
    readiness_level: ExternalDominionReleaseReadinessLevel | str = ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031
    ready_for_v031: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        if not _version_includes_v0309(self.source_version):
            raise ValueError("source_version must include v0.30.9")
        if "v0.31" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.31")
        _require_non_blank("source_snapshot_id", self.source_snapshot_id)
        _require_non_blank("recommended_next_track", self.recommended_next_track)
        _require_non_blank("recommended_next_release", self.recommended_next_release)
        _validate_string_list("internal_triad_focus", self.internal_triad_focus)
        focus_text = " ".join(self.internal_triad_focus).lower()
        if not all(term in focus_text for term in ("observation", "digestion", "dominion")):
            raise ValueError("internal_triad_focus must mention observation/digestion/dominion")
        for name in (
            "observation_skill_handoff_items",
            "digestion_skill_handoff_items",
            "dominion_skill_handoff_items",
            "reusable_contract_refs",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if set(PROHIBITED_RUNTIME_SURFACES) - set(self.prohibited_until_later_gate):
            raise ValueError("prohibited_until_later_gate must include external execution/runtime surfaces")
        readiness = _normalize_readiness(self.readiness_level)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if self.ready_for_v031 and readiness not in {
            ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031,
            ExternalDominionReleaseReadinessLevel.FOUNDATION_READY,
        }:
            raise ValueError("ready_for_v031 requires foundation or handoff readiness")

    @property
    def is_implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionReleaseManifest:
    release_manifest_id: str
    version: str
    release_name: str
    snapshot_id: str
    included_versions: list[str]
    included_docs: list[str]
    included_modules: list[str]
    included_tests: list[str]
    release_flags: ExternalDominionReleaseFlagSet
    test_command: str
    known_gaps: list[str] = field(default_factory=list)
    known_risks: list[str] = field(default_factory=list)
    next_handoff_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        if not _version_includes_v0309(self.version):
            raise ValueError("version must include v0.30.9")
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        for name in ("included_versions", "included_docs", "included_modules", "included_tests"):
            _validate_string_list(name, getattr(self, name))
        if not _contains_required_versions(self.included_versions):
            raise ValueError("included_versions must include v0.30.0 through v0.30.8")
        if not release_flags_preserve_runtime_false(self.release_flags):
            raise ValueError("release_flags must preserve no-execution")
        _require_non_blank("test_command", self.test_command)
        _validate_string_list("known_gaps", self.known_gaps)
        _validate_string_list("known_risks", self.known_risks)

    @property
    def is_production_release(self) -> bool:
        return False

    @property
    def runtime_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class V030ConsolidationAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    negative_runtime_checks: list[str]
    no_execution_confirmed: bool
    runtime_readiness_flags_false_confirmed: bool
    d4_d9_future_track_confirmed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _require_non_blank("version", self.version)
        for name in (
            "reviewed_artifact_refs",
            "reviewed_test_refs",
            "reviewed_doc_refs",
            "boundary_checks",
            "negative_runtime_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.no_execution_confirmed is not True:
            raise ValueError("no_execution_confirmed must be True for successful consolidation")
        if self.runtime_readiness_flags_false_confirmed is not True:
            raise ValueError("runtime_readiness_flags_false_confirmed must be True")
        if self.d4_d9_future_track_confirmed is not True:
            raise ValueError("d4_d9_future_track_confirmed must be True")

    @property
    def executes_audit(self) -> bool:
        return False


@dataclass(frozen=True)
class V030ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: ExternalDominionConsolidationStatus | str
    readiness_level: ExternalDominionReleaseReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    runtime_not_ready_items: list[str] = field(default_factory=lambda: list(PROHIBITED_RUNTIME_SURFACES))
    v031_handoff_summary: str = "v0.31 Internal Triad Skill Foundation handoff only."
    ready_for_v031: bool = True
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        if not _version_includes_v0309(self.version):
            raise ValueError("version must include v0.30.9")
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("release_manifest_id", self.release_manifest_id)
        status = _normalize_status(self.consolidation_status)
        readiness = _normalize_readiness(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "runtime_not_ready_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("v031_handoff_summary", self.v031_handoff_summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if self.ready_for_v031 and (self.blocked_items or status is ExternalDominionConsolidationStatus.BLOCKED or readiness is ExternalDominionReleaseReadinessLevel.BLOCKED):
            raise ValueError("ready_for_v031 requires no blocking gaps")

    @property
    def runtime_enablement(self) -> bool:
        return False

    @property
    def production_certification(self) -> bool:
        return False


def build_v0309_release_flags(
    foundation_ready: bool = True,
    ready_for_v031: bool = True,
) -> ExternalDominionReleaseFlagSet:
    return ExternalDominionReleaseFlagSet(
        flag_set_id="external_dominion_release_flags:v0.30.9",
        version=V0309_VERSION,
        external_dominion_control_plane_foundation_ready=foundation_ready,
        ready_for_v031_internal_triad_skill_foundation=ready_for_v031,
        metadata={"control_plane_only": True},
    )


def build_foundation_snapshot(
    release_flags: ExternalDominionReleaseFlagSet | None = None,
    known_gaps: list[str] | None = None,
    known_risks: list[str] | None = None,
    consolidation_handoff: ExternalDominionV0309ConsolidationHandoff | None = None,
) -> ExternalDominionFoundationSnapshot:
    flags = release_flags or build_v0309_release_flags()
    gaps = list(known_gaps or [])
    evidence_refs = []
    metadata: dict[str, Any] = {"v0309_contract_only": True}
    if consolidation_handoff is not None:
        gaps.extend(getattr(consolidation_handoff, "unresolved_requirements", []))
        evidence_refs.extend(getattr(consolidation_handoff, "evidence_refs", []))
        metadata["source_v0308_handoff_id"] = consolidation_handoff.handoff_id
        metadata["source_v0308_approved_for_consolidation"] = consolidation_handoff.approved_for_v0309_consolidation
    return ExternalDominionFoundationSnapshot(
        snapshot_id="external_dominion_foundation_snapshot:v0.30.9",
        version=V0309_VERSION,
        release_name=FOUNDATION_RELEASE_NAME,
        included_versions=list(REQUIRED_V030_VERSIONS),
        included_artifact_groups=[
            "target_inventory",
            "capability_observation",
            "digestion",
            "authority",
            "delegation_dry_run",
            "approval_audit_rollback",
            "certification_matrix",
            "limited_preview_gate",
        ],
        release_flags=flags,
        consolidation_status=ExternalDominionConsolidationStatus.CONSOLIDATED_WITH_GAPS
        if gaps
        else ExternalDominionConsolidationStatus.CONSOLIDATED,
        readiness_level=ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031,
        summary="External Dominion Control Plane Foundation v1 consolidation; not runtime enablement.",
        evidence_refs=evidence_refs,
        known_gaps=gaps,
        known_risks=list(known_risks or []),
        withdrawal_conditions=[
            "consolidation is treated as runtime enablement",
            "runtime readiness flag becomes true",
        ],
        metadata=metadata,
    )


def build_coverage_matrix(
    cls: type[CoverageMatrixBase],
    coverage_id: str,
    covered_artifact_refs: list[str] | None = None,
    missing_artifact_refs: list[str] | None = None,
    blocking_gaps: list[str] | None = None,
    non_blocking_gaps: list[str] | None = None,
    target_id: str | None = None,
    candidate_id: str | None = None,
) -> CoverageMatrixBase:
    gaps = list(blocking_gaps or [])
    return cls(
        coverage_id=coverage_id,
        target_id=target_id,
        candidate_id=candidate_id,
        covered_artifact_refs=list(covered_artifact_refs or []),
        missing_artifact_refs=list(missing_artifact_refs or []),
        coverage_notes=["coverage matrix is not certification or runtime readiness"],
        coverage_complete=not gaps and not missing_artifact_refs,
        blocking_gaps=gaps,
        non_blocking_gaps=list(non_blocking_gaps or []),
        evidence_refs=[],
        metadata={"v0309_contract_only": True},
    )


def build_gap_register(
    blocking_gaps: list[str] | None = None,
    non_blocking_gaps: list[str] | None = None,
) -> ExternalDominionGapRegister:
    return ExternalDominionGapRegister(
        gap_register_id="external_dominion_gap_register:v0.30.9",
        version=V0309_VERSION,
        blocking_gaps=list(blocking_gaps or []),
        non_blocking_gaps=list(non_blocking_gaps or []),
        recommended_v031_items=["internal observation skill foundation", "internal digestion skill foundation", "internal dominion skill foundation"],
        recommended_later_items=list(PROHIBITED_RUNTIME_SURFACES),
        metadata={"v0309_contract_only": True},
    )


def build_risk_register(
    unresolved_risks: list[str] | None = None,
) -> ExternalDominionRiskRegister:
    return ExternalDominionRiskRegister(
        risk_register_id="external_dominion_risk_register:v0.30.9",
        version=V0309_VERSION,
        known_risks=["external runtime surfaces remain prohibited"],
        high_risk_surfaces=list(PROHIBITED_RUNTIME_SURFACES),
        mitigations=["keep D4-D9 future-track", "keep runtime readiness flags false"],
        unresolved_risks=list(unresolved_risks or []),
        metadata={"v0309_contract_only": True},
    )


def build_v031_handoff_packet(
    snapshot: ExternalDominionFoundationSnapshot,
    manifest_id: str | None = None,
    blocking_gaps: list[str] | None = None,
) -> ExternalDominionV031HandoffPacket:
    gaps = list(blocking_gaps or [])
    readiness = (
        ExternalDominionReleaseReadinessLevel.NOT_READY
        if gaps
        else ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031
    )
    return ExternalDominionV031HandoffPacket(
        handoff_id="external_dominion_v031_handoff_packet:v0.30.9",
        source_version=V0309_VERSION,
        target_version_track="v0.31 Internal Triad Skill Foundation",
        source_snapshot_id=snapshot.snapshot_id,
        release_manifest_id=manifest_id,
        recommended_next_track="v0.31 Internal Triad Skill Foundation",
        recommended_next_release="v0.31.0",
        internal_triad_focus=["observation", "digestion", "dominion"],
        observation_skill_handoff_items=["consume capability observation contracts"],
        digestion_skill_handoff_items=["consume digestion candidate contracts"],
        dominion_skill_handoff_items=["consume authority and preview gate contracts"],
        reusable_contract_refs=list(snapshot.included_artifact_groups),
        readiness_level=readiness,
        ready_for_v031=not gaps,
        ready_for_execution=False,
        metadata={"v0309_contract_only": True},
    )


def build_release_manifest(
    snapshot: ExternalDominionFoundationSnapshot,
    handoff_id: str | None = None,
) -> ExternalDominionReleaseManifest:
    return ExternalDominionReleaseManifest(
        release_manifest_id="external_dominion_release_manifest:v0.30.9",
        version=V0309_VERSION,
        release_name=FOUNDATION_RELEASE_NAME,
        snapshot_id=snapshot.snapshot_id,
        included_versions=list(REQUIRED_V030_VERSIONS),
        included_docs=[
            f"docs/versions/v0.30/v0.30.{index}_external_dominion.md" for index in range(0, 9)
        ],
        included_modules=[
            "contracts",
            "inventory",
            "observation",
            "digestion",
            "authority",
            "delegation",
            "approval_audit",
            "certification",
            "preview_gate",
            "consolidation",
        ],
        included_tests=[
            f"tests/test_v030{index}_external_dominion_contract.py" if index == 0 else f"tests/test_v030{index}_*.py"
            for index in range(0, 10)
        ],
        release_flags=snapshot.release_flags,
        test_command="py -m pytest tests/test_v0300_external_dominion_contract.py ... tests/test_v0309_external_dominion_control_plane_consolidation.py",
        known_gaps=list(snapshot.known_gaps),
        known_risks=list(snapshot.known_risks),
        next_handoff_id=handoff_id,
        metadata={"v0309_contract_only": True},
    )


def build_consolidation_audit_trail() -> V030ConsolidationAuditTrail:
    return V030ConsolidationAuditTrail(
        audit_trail_id="v030_consolidation_audit_trail:v0.30.9",
        version=V0309_VERSION,
        reviewed_artifact_refs=list(REQUIRED_V030_VERSIONS),
        reviewed_test_refs=[f"test_v030{index}" for index in range(0, 10)],
        reviewed_doc_refs=[f"v0.30.{index} docs" for index in range(0, 10)],
        boundary_checks=["no execution", "runtime flags false", "D4-D9 future-track"],
        negative_runtime_checks=list(PROHIBITED_RUNTIME_SURFACES),
        no_execution_confirmed=True,
        runtime_readiness_flags_false_confirmed=True,
        d4_d9_future_track_confirmed=True,
        evidence_refs=[],
        metadata={"v0309_contract_only": True},
    )


def build_v030_consolidation_report(
    snapshot: ExternalDominionFoundationSnapshot,
    manifest: ExternalDominionReleaseManifest,
    handoff: ExternalDominionV031HandoffPacket | None = None,
    blocking_gaps: list[str] | None = None,
) -> V030ConsolidationReport:
    gaps = list(blocking_gaps or [])
    return V030ConsolidationReport(
        report_id="v030_consolidation_report:v0.30.9",
        version=V0309_VERSION,
        release_name=FOUNDATION_RELEASE_NAME,
        snapshot_id=snapshot.snapshot_id,
        release_manifest_id=manifest.release_manifest_id,
        handoff_id=handoff.handoff_id if handoff else None,
        consolidation_status=ExternalDominionConsolidationStatus.BLOCKED
        if gaps
        else ExternalDominionConsolidationStatus.CONSOLIDATED,
        readiness_level=ExternalDominionReleaseReadinessLevel.BLOCKED
        if gaps
        else ExternalDominionReleaseReadinessLevel.HANDOFF_READY_FOR_V031,
        summary="v0.30.x consolidated as External Dominion Control Plane Foundation v1; not runtime-ready.",
        completed_items=list(REQUIRED_V030_VERSIONS),
        blocked_items=gaps,
        future_track_items=["D4-D9 future-track", *PROHIBITED_RUNTIME_SURFACES],
        runtime_not_ready_items=list(PROHIBITED_RUNTIME_SURFACES),
        ready_for_v031=not gaps,
        ready_for_execution=False,
        evidence_refs=[],
        withdrawal_conditions=[
            "consolidation report is treated as runtime enablement",
            "ready_for_execution becomes true",
        ],
        metadata={"v0309_contract_only": True},
    )


def consolidation_preserves_no_execution(obj: Any) -> bool:
    return getattr(obj, "ready_for_execution", False) is False and not bool(getattr(obj, "runtime_enablement", False))


def handoff_packet_is_v031_only(packet: ExternalDominionV031HandoffPacket) -> bool:
    return packet.ready_for_execution is False and "v0.31" in packet.target_version_track and packet.is_implementation is False


def consolidation_report_is_not_runtime_ready(report: V030ConsolidationReport) -> bool:
    return report.ready_for_execution is False and report.runtime_enablement is False and report.production_certification is False

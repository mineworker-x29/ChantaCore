from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.internal_triad.boundaries import _require_non_blank, _validate_string_list
from chanta_core.internal_triad.skill_kinds import V0310_TRACK


V0318_VERSION = "v0.31.8"
V0318_RELEASE_NAME = "v0.31.8 Triad Skill Workbench Surface"
V0318_TRACK = V0310_TRACK

V0318_PROHIBITED_UNTIL_LATER_GATE = [
    "ui_runtime",
    "action_execution",
    "approval_execution",
    "ocel_emission",
    "runtime_trace_persistence",
    "log_write",
    "database_write",
    "registry_mutation",
    "memory_mutation",
    "external_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "rollback",
    "retry",
]


class TriadWorkbenchSurfaceKind(StrEnum):
    TRIAD_OVERVIEW = "triad_overview"
    OBSERVATION_SURFACE = "observation_surface"
    CAPABILITY_MAP_SURFACE = "capability_map_surface"
    DIGESTION_SURFACE = "digestion_surface"
    INTERNALIZATION_SURFACE = "internalization_surface"
    DOMINION_SURFACE = "dominion_surface"
    OCEL_TRACE_SURFACE = "ocel_trace_surface"
    GAP_RISK_EVIDENCE_SURFACE = "gap_risk_evidence_surface"
    READINESS_SURFACE = "readiness_surface"
    FUTURE_GATE_SURFACE = "future_gate_surface"
    NO_OP_SURFACE = "no_op_surface"
    UNKNOWN = "unknown"


class TriadWorkbenchPanelKind(StrEnum):
    OVERVIEW_PANEL = "overview_panel"
    OBSERVATION_REPORT_PANEL = "observation_report_panel"
    CAPABILITY_MAP_PANEL = "capability_map_panel"
    DIGESTION_SIGNAL_PANEL = "digestion_signal_panel"
    INTERNAL_CANDIDATE_PANEL = "internal_candidate_panel"
    INTERNALIZATION_PLAN_PANEL = "internalization_plan_panel"
    DOMINION_TARGET_PANEL = "dominion_target_panel"
    DOMINION_DECISION_PANEL = "dominion_decision_panel"
    OCEL_TRACE_PLAN_PANEL = "ocel_trace_plan_panel"
    OCEL_TRACE_COVERAGE_PANEL = "ocel_trace_coverage_panel"
    GAP_REGISTER_PANEL = "gap_register_panel"
    RISK_MAP_PANEL = "risk_map_panel"
    EVIDENCE_TABLE_PANEL = "evidence_table_panel"
    FUTURE_GATE_PANEL = "future_gate_panel"
    NO_OP_PANEL = "no_op_panel"
    READINESS_PANEL = "readiness_panel"
    UNKNOWN = "unknown"


class TriadWorkbenchCardKind(StrEnum):
    ARTIFACT_CARD = "artifact_card"
    REPORT_CARD = "report_card"
    CANDIDATE_CARD = "candidate_card"
    DECISION_CARD = "decision_card"
    TRACE_CARD = "trace_card"
    RISK_CARD = "risk_card"
    GAP_CARD = "gap_card"
    EVIDENCE_CARD = "evidence_card"
    FUTURE_GATE_CARD = "future_gate_card"
    NO_OP_CARD = "no_op_card"
    READINESS_CARD = "readiness_card"
    UNKNOWN = "unknown"


class TriadWorkbenchActionKind(StrEnum):
    VIEW_ONLY = "view_only"
    INSPECT_ARTIFACT = "inspect_artifact"
    INSPECT_TRACE_PLAN = "inspect_trace_plan"
    INSPECT_GAP = "inspect_gap"
    INSPECT_RISK = "inspect_risk"
    INSPECT_EVIDENCE = "inspect_evidence"
    INSPECT_READINESS = "inspect_readiness"
    EXPORT_PREVIEW = "export_preview"
    APPROVAL_PREVIEW = "approval_preview"
    NO_OP_PREVIEW = "no_op_preview"
    FUTURE_TRACK_PREVIEW = "future_track_preview"
    UNKNOWN = "unknown"


class TriadWorkbenchDataSourceKind(StrEnum):
    TRIAD_CONTRACT = "triad_contract"
    OBSERVATION_REPORT = "observation_report"
    CAPABILITY_MAP = "capability_map"
    DIGESTION_OUTPUT = "digestion_output"
    INTERNAL_CANDIDATE_SET = "internal_candidate_set"
    INTERNALIZATION_PLAN = "internalization_plan"
    DOMINION_TARGET_DECISION_SET = "dominion_target_decision_set"
    OCEL_TRACE_PLAN = "ocel_trace_plan"
    OCEL_TRACE_COVERAGE = "ocel_trace_coverage"
    READINESS_REPORT = "readiness_report"
    GAP_REGISTER = "gap_register"
    RISK_MAP = "risk_map"
    EVIDENCE_TABLE = "evidence_table"
    MANUAL_REF = "manual_ref"
    UNKNOWN = "unknown"


class TriadWorkbenchStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    SURFACE_READY = "surface_ready"
    SURFACE_READY_WITH_GAPS = "surface_ready_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class TriadWorkbenchSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return isinstance(metadata, dict) and any(metadata.get(name) is True for name in names)


def _validate_version_includes_v0318(version: str) -> None:
    _require_non_blank("version", version)
    if V0318_VERSION not in version:
        raise ValueError("version must include v0.31.8")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], normalizer: Any) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        normalizer(value)


def normalize_triad_workbench_surface_kind(value: TriadWorkbenchSurfaceKind | str) -> TriadWorkbenchSurfaceKind:
    if isinstance(value, TriadWorkbenchSurfaceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench surface kind must not be blank")
        return TriadWorkbenchSurfaceKind(stripped)
    raise TypeError(f"unsupported triad workbench surface kind: {value!r}")


def normalize_triad_workbench_panel_kind(value: TriadWorkbenchPanelKind | str) -> TriadWorkbenchPanelKind:
    if isinstance(value, TriadWorkbenchPanelKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench panel kind must not be blank")
        return TriadWorkbenchPanelKind(stripped)
    raise TypeError(f"unsupported triad workbench panel kind: {value!r}")


def normalize_triad_workbench_card_kind(value: TriadWorkbenchCardKind | str) -> TriadWorkbenchCardKind:
    if isinstance(value, TriadWorkbenchCardKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench card kind must not be blank")
        return TriadWorkbenchCardKind(stripped)
    raise TypeError(f"unsupported triad workbench card kind: {value!r}")


def normalize_triad_workbench_action_kind(value: TriadWorkbenchActionKind | str) -> TriadWorkbenchActionKind:
    if isinstance(value, TriadWorkbenchActionKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench action kind must not be blank")
        return TriadWorkbenchActionKind(stripped)
    raise TypeError(f"unsupported triad workbench action kind: {value!r}")


def normalize_triad_workbench_data_source_kind(value: TriadWorkbenchDataSourceKind | str) -> TriadWorkbenchDataSourceKind:
    if isinstance(value, TriadWorkbenchDataSourceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench data source kind must not be blank")
        return TriadWorkbenchDataSourceKind(stripped)
    raise TypeError(f"unsupported triad workbench data source kind: {value!r}")


def normalize_triad_workbench_status(value: TriadWorkbenchStatus | str) -> TriadWorkbenchStatus:
    if isinstance(value, TriadWorkbenchStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench status must not be blank")
        return TriadWorkbenchStatus(stripped)
    raise TypeError(f"unsupported triad workbench status: {value!r}")


def normalize_triad_workbench_severity(value: TriadWorkbenchSeverity | str) -> TriadWorkbenchSeverity:
    if isinstance(value, TriadWorkbenchSeverity):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad workbench severity must not be blank")
        return TriadWorkbenchSeverity(stripped)
    raise TypeError(f"unsupported triad workbench severity: {value!r}")


def triad_workbench_surface_kind_creates_ui_runtime(_: TriadWorkbenchSurfaceKind | str) -> bool:
    normalize_triad_workbench_surface_kind(_)
    return False


def triad_workbench_action_kind_executes(_: TriadWorkbenchActionKind | str) -> bool:
    normalize_triad_workbench_action_kind(_)
    return False


@dataclass(frozen=True)
class TriadWorkbenchArtifactRef:
    artifact_ref_id: str
    artifact_kind: TriadWorkbenchDataSourceKind | str
    artifact_id: str
    source_version: str | None = None
    display_name: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("artifact_ref_id", self.artifact_ref_id)
        normalize_triad_workbench_data_source_kind(self.artifact_kind)
        _require_non_blank("artifact_id", self.artifact_id)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "source_ref_fetch", "active_object"}):
            raise ValueError("TriadWorkbenchArtifactRef must not imply fetch or active object")

    @property
    def fetches_data(self) -> bool:
        return False

    @property
    def active_object(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchDisplayFilter:
    filter_id: str
    name: str
    target_surface_kinds: list[TriadWorkbenchSurfaceKind | str] = field(default_factory=list)
    target_panel_kinds: list[TriadWorkbenchPanelKind | str] = field(default_factory=list)
    target_card_kinds: list[TriadWorkbenchCardKind | str] = field(default_factory=list)
    include_statuses: list[TriadWorkbenchStatus | str] = field(default_factory=list)
    include_severities: list[TriadWorkbenchSeverity | str] = field(default_factory=list)
    include_artifact_kinds: list[TriadWorkbenchDataSourceKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("filter_id", self.filter_id)
        _require_non_blank("name", self.name)
        _validate_enum_list("target_surface_kinds", self.target_surface_kinds, normalize_triad_workbench_surface_kind)
        _validate_enum_list("target_panel_kinds", self.target_panel_kinds, normalize_triad_workbench_panel_kind)
        _validate_enum_list("target_card_kinds", self.target_card_kinds, normalize_triad_workbench_card_kind)
        _validate_enum_list("include_statuses", self.include_statuses, normalize_triad_workbench_status)
        _validate_enum_list("include_severities", self.include_severities, normalize_triad_workbench_severity)
        _validate_enum_list("include_artifact_kinds", self.include_artifact_kinds, normalize_triad_workbench_data_source_kind)
        if _metadata_flag_true(self.metadata, {"query_execution", "fetch"}):
            raise ValueError("TriadWorkbenchDisplayFilter must not imply query execution")

    @property
    def executes_query(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchActionSpec:
    action_spec_id: str
    action_kind: TriadWorkbenchActionKind | str
    label: str
    description: str
    target_artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    requires_confirmation: bool = False
    execution_enabled: bool = False
    approval_enabled: bool = False
    mutation_enabled: bool = False
    export_enabled: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("action_spec_id", self.action_spec_id)
        normalize_triad_workbench_action_kind(self.action_kind)
        _require_non_blank("label", self.label)
        _require_non_blank("description", self.description)
        _validate_object_list("target_artifact_refs", self.target_artifact_refs, TriadWorkbenchArtifactRef)
        for name in ("execution_enabled", "approval_enabled", "mutation_enabled", "export_enabled"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.8")
        if _metadata_flag_true(self.metadata, {"action_execution", "approval_granted", "mutation", "export_execution"}):
            raise ValueError("TriadWorkbenchActionSpec must not imply action execution")

    @property
    def executes_action(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchPanelSpec:
    panel_id: str
    panel_kind: TriadWorkbenchPanelKind | str
    title: str
    description: str
    artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    action_specs: list[TriadWorkbenchActionSpec] = field(default_factory=list)
    filters: list[TriadWorkbenchDisplayFilter] = field(default_factory=list)
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.DRAFT
    severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO
    gaps: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("panel_id", self.panel_id)
        normalize_triad_workbench_panel_kind(self.panel_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("description", self.description)
        _validate_object_list("artifact_refs", self.artifact_refs, TriadWorkbenchArtifactRef)
        _validate_object_list("action_specs", self.action_specs, TriadWorkbenchActionSpec)
        _validate_object_list("filters", self.filters, TriadWorkbenchDisplayFilter)
        normalize_triad_workbench_status(self.status)
        normalize_triad_workbench_severity(self.severity)
        _validate_string_list("gaps", self.gaps)
        if not all(workbench_action_spec_preserves_no_execution(action) for action in self.action_specs):
            raise ValueError("panel action_specs must preserve no execution")
        if _metadata_flag_true(self.metadata, {"rendered_ui", "ui_runtime"}):
            raise ValueError("TriadWorkbenchPanelSpec must not imply rendered UI")

    @property
    def rendered_ui(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchArtifactCard:
    card_id: str
    card_kind: TriadWorkbenchCardKind | str
    title: str
    summary: str
    artifact_ref: TriadWorkbenchArtifactRef
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.DRAFT
    severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO
    tags: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    action_specs: list[TriadWorkbenchActionSpec] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("card_id", self.card_id)
        normalize_triad_workbench_card_kind(self.card_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        if not isinstance(self.artifact_ref, TriadWorkbenchArtifactRef):
            raise TypeError("artifact_ref must be TriadWorkbenchArtifactRef")
        normalize_triad_workbench_status(self.status)
        normalize_triad_workbench_severity(self.severity)
        _validate_string_list("tags", self.tags)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_object_list("action_specs", self.action_specs, TriadWorkbenchActionSpec)
        if not all(workbench_action_spec_preserves_no_execution(action) for action in self.action_specs):
            raise ValueError("card action_specs must preserve no execution")
        if _metadata_flag_true(self.metadata, {"active_artifact", "artifact_mutation"}):
            raise ValueError("TriadWorkbenchArtifactCard must not imply active artifact")

    @property
    def active_artifact(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchTracePreview:
    trace_preview_id: str
    source_trace_plan_id: str | None = None
    source_trace_coverage_id: str | None = None
    planned_event_type_names: list[str] = field(default_factory=list)
    planned_object_type_names: list[str] = field(default_factory=list)
    planned_relation_type_names: list[str] = field(default_factory=list)
    coverage_summary: str = "Trace preview is display-only and does not emit OCEL events."
    gaps: list[str] = field(default_factory=list)
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_preview_id", self.trace_preview_id)
        _validate_string_list("planned_event_type_names", self.planned_event_type_names)
        _validate_string_list("planned_object_type_names", self.planned_object_type_names)
        _validate_string_list("planned_relation_type_names", self.planned_relation_type_names)
        _require_non_blank("coverage_summary", self.coverage_summary)
        _validate_string_list("gaps", self.gaps)
        if self.ready_for_ocel_emission is not False:
            raise ValueError("ready_for_ocel_emission must always be False in v0.31.8")
        if self.ready_for_runtime_trace_persistence is not False:
            raise ValueError("ready_for_runtime_trace_persistence must always be False in v0.31.8")
        if _metadata_flag_true(self.metadata, {"ocel_emission", "runtime_trace_persistence"}):
            raise ValueError("TriadWorkbenchTracePreview must not imply OCEL emission")

    @property
    def emits_ocel_events(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchGapRiskEvidenceView:
    view_id: str
    gap_artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    risk_artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    evidence_artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    highest_severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO
    summary: str = "Gap, risk, and evidence view is display-only."
    recommended_followups: list[str] = field(default_factory=list)
    remediation_enabled: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _validate_object_list("gap_artifact_refs", self.gap_artifact_refs, TriadWorkbenchArtifactRef)
        _validate_object_list("risk_artifact_refs", self.risk_artifact_refs, TriadWorkbenchArtifactRef)
        _validate_object_list("evidence_artifact_refs", self.evidence_artifact_refs, TriadWorkbenchArtifactRef)
        normalize_triad_workbench_severity(self.highest_severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("recommended_followups", self.recommended_followups)
        if self.remediation_enabled is not False:
            raise ValueError("remediation_enabled must always be False in v0.31.8")
        if _metadata_flag_true(self.metadata, {"remediation", "action_execution"}):
            raise ValueError("TriadWorkbenchGapRiskEvidenceView must not imply remediation")

    @property
    def remediates(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchReadinessView:
    readiness_view_id: str
    readiness_report_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    ready_for_v0319_consolidation: bool = True
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_action_execution: bool = False
    summary: str = "Readiness view supports v0.31.9 consolidation handoff only."
    blockers: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_view_id", self.readiness_view_id)
        _validate_object_list("readiness_report_refs", self.readiness_report_refs, TriadWorkbenchArtifactRef)
        _require_non_blank("summary", self.summary)
        for name in ("ready_for_execution", "ready_for_skill_activation", "ready_for_ui_runtime", "ready_for_action_execution"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.8")
        _validate_string_list("blockers", self.blockers)
        _validate_string_list("future_track_items", self.future_track_items)
        if self.ready_for_v0319_consolidation and self.blockers:
            raise ValueError("ready_for_v0319_consolidation requires no blockers")
        if _metadata_flag_true(self.metadata, {"runtime_readiness", "ui_runtime", "action_execution"}):
            raise ValueError("TriadWorkbenchReadinessView must not imply runtime readiness")

    @property
    def runtime_readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchSurface:
    surface_id: str
    surface_kind: TriadWorkbenchSurfaceKind | str
    title: str
    description: str
    panels: list[TriadWorkbenchPanelSpec] = field(default_factory=list)
    cards: list[TriadWorkbenchArtifactCard] = field(default_factory=list)
    trace_preview: TriadWorkbenchTracePreview | None = None
    gap_risk_evidence_view: TriadWorkbenchGapRiskEvidenceView | None = None
    readiness_view: TriadWorkbenchReadinessView | None = None
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.DRAFT
    ready_for_v0319_consolidation: bool = True
    ready_for_ui_runtime: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("surface_id", self.surface_id)
        normalize_triad_workbench_surface_kind(self.surface_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("description", self.description)
        _validate_object_list("panels", self.panels, TriadWorkbenchPanelSpec)
        _validate_object_list("cards", self.cards, TriadWorkbenchArtifactCard)
        if self.trace_preview is not None and not isinstance(self.trace_preview, TriadWorkbenchTracePreview):
            raise TypeError("trace_preview must be TriadWorkbenchTracePreview")
        if self.gap_risk_evidence_view is not None and not isinstance(self.gap_risk_evidence_view, TriadWorkbenchGapRiskEvidenceView):
            raise TypeError("gap_risk_evidence_view must be TriadWorkbenchGapRiskEvidenceView")
        if self.readiness_view is not None and not isinstance(self.readiness_view, TriadWorkbenchReadinessView):
            raise TypeError("readiness_view must be TriadWorkbenchReadinessView")
        status = normalize_triad_workbench_status(self.status)
        if self.ready_for_ui_runtime is not False:
            raise ValueError("ready_for_ui_runtime must always be False in v0.31.8")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.8")
        if self.ready_for_v0319_consolidation and status is TriadWorkbenchStatus.BLOCKED:
            raise ValueError("ready_for_v0319_consolidation requires unblocked surface")
        if _metadata_flag_true(self.metadata, {"ui_runtime", "execution", "dashboard_runtime"}):
            raise ValueError("TriadWorkbenchSurface must not imply UI runtime")

    @property
    def ui_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchSnapshot:
    snapshot_id: str
    version: str
    surfaces: list[TriadWorkbenchSurface] = field(default_factory=list)
    artifact_refs: list[TriadWorkbenchArtifactRef] = field(default_factory=list)
    action_specs: list[TriadWorkbenchActionSpec] = field(default_factory=list)
    filters: list[TriadWorkbenchDisplayFilter] = field(default_factory=list)
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.DRAFT
    summary: str = "Workbench snapshot is a display contract, not persistence."
    gaps: list[str] = field(default_factory=list)
    ready_for_v0319_consolidation: bool = True
    ready_for_ui_runtime: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0318(self.version)
        _validate_object_list("surfaces", self.surfaces, TriadWorkbenchSurface)
        _validate_object_list("artifact_refs", self.artifact_refs, TriadWorkbenchArtifactRef)
        _validate_object_list("action_specs", self.action_specs, TriadWorkbenchActionSpec)
        _validate_object_list("filters", self.filters, TriadWorkbenchDisplayFilter)
        normalize_triad_workbench_status(self.status)
        _require_non_blank("summary", self.summary)
        _validate_string_list("gaps", self.gaps)
        if self.ready_for_ui_runtime is not False:
            raise ValueError("ready_for_ui_runtime must always be False in v0.31.8")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.8")
        if _metadata_flag_true(self.metadata, {"persistence", "ui_runtime", "execution"}):
            raise ValueError("TriadWorkbenchSnapshot must not imply persistence or runtime")

    @property
    def persists_runtime_state(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchReport:
    report_id: str
    snapshot_id: str
    version: str
    summary: str
    surface_count: int
    panel_count: int
    card_count: int
    action_spec_count: int
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    ready_for_v0319_consolidation: bool = True
    ready_for_ui_runtime: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0318(self.version)
        _require_non_blank("summary", self.summary)
        for name in ("surface_count", "panel_count", "card_count", "action_spec_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        for name in ("ready_for_ui_runtime", "ready_for_action_execution", "ready_for_execution"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.8")
        if self.ready_for_v0319_consolidation and self.blocked_items:
            raise ValueError("ready_for_v0319_consolidation requires no blocked items")
        if _metadata_flag_true(self.metadata, {"runtime_result", "ui_runtime", "action_execution"}):
            raise ValueError("TriadWorkbenchReport must not imply runtime result")

    @property
    def runtime_result(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadWorkbenchRunPreview:
    run_preview_id: str
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_ui_runtime_guarantee: bool = True
    no_action_execution_guarantee: bool = True
    no_approval_execution_guarantee: bool = True
    no_ocel_emission_guarantee: bool = True
    no_runtime_persistence_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        for name in (
            "no_ui_runtime_guarantee",
            "no_action_execution_guarantee",
            "no_approval_execution_guarantee",
            "no_ocel_emission_guarantee",
            "no_runtime_persistence_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.8")
        if _metadata_flag_true(self.metadata, {"execution", "ui_runtime", "action_execution"}):
            raise ValueError("TriadWorkbenchRunPreview must not imply execution")

    @property
    def executes_run(self) -> bool:
        return False


@dataclass(frozen=True)
class V0318ReadinessReport:
    report_id: str
    version: str
    workbench_report_id: str | None
    summary: str
    ready_for_v0319_internal_triad_consolidation: bool
    ready_for_ui_runtime: bool = False
    ready_for_action_execution: bool = False
    ready_for_approval_execution: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0318_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0318(self.version)
        _require_non_blank("summary", self.summary)
        for name in (
            "ready_for_ui_runtime",
            "ready_for_action_execution",
            "ready_for_approval_execution",
            "ready_for_ocel_emission",
            "ready_for_runtime_trace_persistence",
            "ready_for_execution",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.31.8")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "prohibited_until_later_gate",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0318_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing v0.31.8 prohibitions: {sorted(missing)}")
        if self.ready_for_v0319_internal_triad_consolidation and self.blocked_items:
            raise ValueError("ready_for_v0319_internal_triad_consolidation requires no blocked items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "ui_runtime", "action_execution"}):
            raise ValueError("V0318ReadinessReport must not imply runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_triad_workbench_artifact_ref(
    artifact_ref_id: str,
    artifact_kind: TriadWorkbenchDataSourceKind | str,
    artifact_id: str,
    source_version: str | None = None,
    display_name: str | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchArtifactRef:
    return TriadWorkbenchArtifactRef(
        artifact_ref_id=artifact_ref_id,
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        source_version=source_version,
        display_name=display_name,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_display_filter(
    filter_id: str,
    name: str,
    target_surface_kinds: list[TriadWorkbenchSurfaceKind | str] | None = None,
    target_panel_kinds: list[TriadWorkbenchPanelKind | str] | None = None,
    target_card_kinds: list[TriadWorkbenchCardKind | str] | None = None,
    include_statuses: list[TriadWorkbenchStatus | str] | None = None,
    include_severities: list[TriadWorkbenchSeverity | str] | None = None,
    include_artifact_kinds: list[TriadWorkbenchDataSourceKind | str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchDisplayFilter:
    return TriadWorkbenchDisplayFilter(
        filter_id=filter_id,
        name=name,
        target_surface_kinds=list(target_surface_kinds or []),
        target_panel_kinds=list(target_panel_kinds or []),
        target_card_kinds=list(target_card_kinds or []),
        include_statuses=list(include_statuses or []),
        include_severities=list(include_severities or []),
        include_artifact_kinds=list(include_artifact_kinds or []),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_action_spec(
    action_spec_id: str,
    action_kind: TriadWorkbenchActionKind | str,
    label: str,
    description: str,
    target_artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    requires_confirmation: bool = False,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchActionSpec:
    return TriadWorkbenchActionSpec(
        action_spec_id=action_spec_id,
        action_kind=action_kind,
        label=label,
        description=description,
        target_artifact_refs=list(target_artifact_refs or []),
        requires_confirmation=requires_confirmation,
        execution_enabled=False,
        approval_enabled=False,
        mutation_enabled=False,
        export_enabled=False,
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_panel_spec(
    panel_id: str,
    panel_kind: TriadWorkbenchPanelKind | str,
    title: str,
    description: str,
    artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    action_specs: list[TriadWorkbenchActionSpec] | None = None,
    filters: list[TriadWorkbenchDisplayFilter] | None = None,
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.SURFACE_READY,
    severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO,
    gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchPanelSpec:
    return TriadWorkbenchPanelSpec(
        panel_id=panel_id,
        panel_kind=panel_kind,
        title=title,
        description=description,
        artifact_refs=list(artifact_refs or []),
        action_specs=list(action_specs or []),
        filters=list(filters or []),
        status=status,
        severity=severity,
        gaps=list(gaps or []),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_artifact_card(
    card_id: str,
    card_kind: TriadWorkbenchCardKind | str,
    title: str,
    summary: str,
    artifact_ref: TriadWorkbenchArtifactRef,
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.SURFACE_READY,
    severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO,
    tags: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    action_specs: list[TriadWorkbenchActionSpec] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchArtifactCard:
    return TriadWorkbenchArtifactCard(
        card_id=card_id,
        card_kind=card_kind,
        title=title,
        summary=summary,
        artifact_ref=artifact_ref,
        status=status,
        severity=severity,
        tags=list(tags or []),
        evidence_refs=list(evidence_refs or []),
        action_specs=list(action_specs or []),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_trace_preview(
    trace_preview_id: str,
    source_trace_plan_id: str | None = None,
    source_trace_coverage_id: str | None = None,
    planned_event_type_names: list[str] | None = None,
    planned_object_type_names: list[str] | None = None,
    planned_relation_type_names: list[str] | None = None,
    coverage_summary: str = "Trace preview is display-only and does not emit OCEL events.",
    gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchTracePreview:
    return TriadWorkbenchTracePreview(
        trace_preview_id=trace_preview_id,
        source_trace_plan_id=source_trace_plan_id,
        source_trace_coverage_id=source_trace_coverage_id,
        planned_event_type_names=list(planned_event_type_names or []),
        planned_object_type_names=list(planned_object_type_names or []),
        planned_relation_type_names=list(planned_relation_type_names or []),
        coverage_summary=coverage_summary,
        gaps=list(gaps or []),
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_gap_risk_evidence_view(
    view_id: str,
    gap_artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    risk_artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    evidence_artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    highest_severity: TriadWorkbenchSeverity | str = TriadWorkbenchSeverity.INFO,
    summary: str = "Gap, risk, and evidence view is display-only.",
    recommended_followups: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchGapRiskEvidenceView:
    return TriadWorkbenchGapRiskEvidenceView(
        view_id=view_id,
        gap_artifact_refs=list(gap_artifact_refs or []),
        risk_artifact_refs=list(risk_artifact_refs or []),
        evidence_artifact_refs=list(evidence_artifact_refs or []),
        highest_severity=highest_severity,
        summary=summary,
        recommended_followups=list(recommended_followups or []),
        remediation_enabled=False,
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_readiness_view(
    readiness_view_id: str,
    readiness_report_refs: list[TriadWorkbenchArtifactRef] | None = None,
    summary: str = "Readiness view supports v0.31.9 consolidation handoff only.",
    blockers: list[str] | None = None,
    future_track_items: list[str] | None = None,
    ready_for_v0319_consolidation: bool = True,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchReadinessView:
    return TriadWorkbenchReadinessView(
        readiness_view_id=readiness_view_id,
        readiness_report_refs=list(readiness_report_refs or []),
        ready_for_v0319_consolidation=ready_for_v0319_consolidation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        ready_for_ui_runtime=False,
        ready_for_action_execution=False,
        summary=summary,
        blockers=list(blockers or []),
        future_track_items=list(future_track_items or []),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_surface(
    surface_id: str,
    surface_kind: TriadWorkbenchSurfaceKind | str,
    title: str,
    description: str,
    panels: list[TriadWorkbenchPanelSpec] | None = None,
    cards: list[TriadWorkbenchArtifactCard] | None = None,
    trace_preview: TriadWorkbenchTracePreview | None = None,
    gap_risk_evidence_view: TriadWorkbenchGapRiskEvidenceView | None = None,
    readiness_view: TriadWorkbenchReadinessView | None = None,
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.SURFACE_READY,
    ready_for_v0319_consolidation: bool = True,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchSurface:
    return TriadWorkbenchSurface(
        surface_id=surface_id,
        surface_kind=surface_kind,
        title=title,
        description=description,
        panels=list(panels or []),
        cards=list(cards or []),
        trace_preview=trace_preview,
        gap_risk_evidence_view=gap_risk_evidence_view,
        readiness_view=readiness_view,
        status=status,
        ready_for_v0319_consolidation=ready_for_v0319_consolidation,
        ready_for_ui_runtime=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_snapshot(
    snapshot_id: str,
    surfaces: list[TriadWorkbenchSurface] | None = None,
    artifact_refs: list[TriadWorkbenchArtifactRef] | None = None,
    action_specs: list[TriadWorkbenchActionSpec] | None = None,
    filters: list[TriadWorkbenchDisplayFilter] | None = None,
    status: TriadWorkbenchStatus | str = TriadWorkbenchStatus.SURFACE_READY,
    summary: str = "Workbench snapshot is a display contract, not persistence.",
    gaps: list[str] | None = None,
    ready_for_v0319_consolidation: bool = True,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchSnapshot:
    return TriadWorkbenchSnapshot(
        snapshot_id=snapshot_id,
        version=V0318_VERSION,
        surfaces=list(surfaces or []),
        artifact_refs=list(artifact_refs or []),
        action_specs=list(action_specs or []),
        filters=list(filters or []),
        status=status,
        summary=summary,
        gaps=list(gaps or []),
        ready_for_v0319_consolidation=ready_for_v0319_consolidation,
        ready_for_ui_runtime=False,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_report(
    report_id: str,
    snapshot: TriadWorkbenchSnapshot,
    evidence_refs: list[str] | None = None,
    withdrawal_conditions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchReport:
    if not isinstance(snapshot, TriadWorkbenchSnapshot):
        raise TypeError("snapshot must be TriadWorkbenchSnapshot")
    panel_count = sum(len(surface.panels) for surface in snapshot.surfaces)
    card_count = sum(len(surface.cards) for surface in snapshot.surfaces)
    return TriadWorkbenchReport(
        report_id=report_id,
        snapshot_id=snapshot.snapshot_id,
        version=V0318_VERSION,
        summary="v0.31.8 defines Workbench surface contracts only; no UI runtime or action execution.",
        surface_count=len(snapshot.surfaces),
        panel_count=panel_count,
        card_count=card_count,
        action_spec_count=len(snapshot.action_specs),
        blocked_items=[],
        future_track_items=["UI runtime", "action execution", "approval execution"],
        ready_for_v0319_consolidation=snapshot.ready_for_v0319_consolidation,
        ready_for_ui_runtime=False,
        ready_for_action_execution=False,
        ready_for_execution=False,
        evidence_refs=list(evidence_refs or []),
        withdrawal_conditions=list(
            withdrawal_conditions
            or [
                "UI runtime is introduced",
                "action or approval execution is introduced",
                "ready_for_ui_runtime, ready_for_action_execution, or ready_for_execution becomes true",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_triad_workbench_run_preview(
    run_preview_id: str,
    planned_steps: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    explicitly_not_performed: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadWorkbenchRunPreview:
    return TriadWorkbenchRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=list(planned_steps or ["create surface specs", "create card specs", "create snapshot/report"]),
        expected_artifacts=list(
            expected_artifacts
            or [
                "TriadWorkbenchSurface",
                "TriadWorkbenchPanelSpec",
                "TriadWorkbenchArtifactCard",
                "TriadWorkbenchSnapshot",
                "TriadWorkbenchReport",
            ]
        ),
        explicitly_not_performed=list(
            explicitly_not_performed
            or [
                "UI runtime",
                "action execution",
                "approval execution",
                "OCEL event emission",
                "runtime persistence",
                "registry mutation",
                "memory mutation",
            ]
        ),
        metadata=dict(metadata or {}),
    )


def build_v0318_readiness_report(
    workbench_report: TriadWorkbenchReport | None = None,
    metadata: dict[str, Any] | None = None,
) -> V0318ReadinessReport:
    return V0318ReadinessReport(
        report_id="v0318_readiness_report:triad_skill_workbench_surface",
        version=V0318_VERSION,
        workbench_report_id=workbench_report.report_id if workbench_report is not None else None,
        summary="v0.31.8 is ready for v0.31.9 Internal Triad Foundation Consolidation handoff only; not UI runtime.",
        ready_for_v0319_internal_triad_consolidation=workbench_report.ready_for_v0319_consolidation if workbench_report else True,
        ready_for_ui_runtime=False,
        ready_for_action_execution=False,
        ready_for_approval_execution=False,
        ready_for_ocel_emission=False,
        ready_for_runtime_trace_persistence=False,
        ready_for_execution=False,
        completed_items=[
            "Workbench surface taxonomy",
            "panel and card contracts",
            "display-only action specs",
            "trace preview and readiness views",
            "snapshot/report contracts",
        ],
        blocked_items=[],
        future_track_items=["UI runtime", "action execution", "approval execution", "OCEL emission"],
        evidence_refs=list(workbench_report.evidence_refs if workbench_report is not None else []),
        withdrawal_conditions=list(workbench_report.withdrawal_conditions if workbench_report is not None else []),
        metadata=dict(metadata or {}),
    )


def workbench_action_spec_preserves_no_execution(action: TriadWorkbenchActionSpec) -> bool:
    return (
        action.execution_enabled is False
        and action.approval_enabled is False
        and action.mutation_enabled is False
        and action.export_enabled is False
        and action.executes_action is False
    )


def workbench_surface_is_not_ui_runtime(surface: TriadWorkbenchSurface) -> bool:
    return surface.ready_for_ui_runtime is False and surface.ready_for_execution is False and surface.ui_runtime is False


def workbench_snapshot_preserves_no_runtime(snapshot: TriadWorkbenchSnapshot) -> bool:
    return (
        snapshot.ready_for_ui_runtime is False
        and snapshot.ready_for_execution is False
        and snapshot.persists_runtime_state is False
        and all(workbench_surface_is_not_ui_runtime(surface) for surface in snapshot.surfaces)
        and all(workbench_action_spec_preserves_no_execution(action) for action in snapshot.action_specs)
    )


def workbench_report_is_not_runtime_ready(report: TriadWorkbenchReport) -> bool:
    return (
        report.ready_for_ui_runtime is False
        and report.ready_for_action_execution is False
        and report.ready_for_execution is False
        and report.runtime_result is False
    )


def workbench_readiness_report_is_not_runtime_ready(report: V0318ReadinessReport) -> bool:
    return (
        report.ready_for_ui_runtime is False
        and report.ready_for_action_execution is False
        and report.ready_for_approval_execution is False
        and report.ready_for_ocel_emission is False
        and report.ready_for_runtime_trace_persistence is False
        and report.ready_for_execution is False
        and report.runtime_enablement is False
    )

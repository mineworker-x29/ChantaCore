from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list
from .reference_corpus import ReferenceFileInventoryEntry


V0322_VERSION = "v0.32.2"
V0322_RELEASE_NAME = "v0.32.2 OpenClaw-style Gateway Observation Profile"

DEFAULT_OPENCLAW_PROHIBITED_RUNTIME_ACTIONS = [
    "OpenClaw execution",
    "reference code execution",
    "install",
    "import runtime",
    "gateway connection",
    "gateway control",
    "channel access",
    "message receive",
    "message send",
    "email access",
    "email send",
    "calendar access",
    "calendar write",
    "contact access",
    "notification send",
    "attachment access",
    "private data access",
    "credential access",
    "webhook call",
    "network",
    "command",
    "provider invocation",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
]

HIGH_RISK_CAPABILITIES = {
    "send_message",
    "invoke_app_action",
    "call_webhook",
    "read_email",
    "send_email",
    "read_calendar",
    "modify_calendar",
    "read_contacts",
    "send_notification",
    "read_attachment",
    "access_private_data",
    "use_credential",
    "access_network",
}


class OpenClawHarnessSurfaceKind(StrEnum):
    GATEWAY_SURFACE = "gateway_surface"
    CHANNEL_SURFACE = "channel_surface"
    MESSAGE_RECEIVE_SURFACE = "message_receive_surface"
    MESSAGE_SEND_SURFACE = "message_send_surface"
    APP_CONTROL_SURFACE = "app_control_surface"
    EXTERNAL_ACTION_SURFACE = "external_action_surface"
    WEBHOOK_SURFACE = "webhook_surface"
    EMAIL_SURFACE = "email_surface"
    CALENDAR_SURFACE = "calendar_surface"
    CONTACT_SURFACE = "contact_surface"
    NOTIFICATION_SURFACE = "notification_surface"
    FILE_ATTACHMENT_SURFACE = "file_attachment_surface"
    PRIVATE_DATA_SURFACE = "private_data_surface"
    CREDENTIAL_SURFACE = "credential_surface"
    NETWORK_SURFACE = "network_surface"
    APPROVAL_BOUNDARY_SURFACE = "approval_boundary_surface"
    AUDIT_BOUNDARY_SURFACE = "audit_boundary_surface"
    ACTION_MANIFEST_SURFACE = "action_manifest_surface"
    AUTOMATION_TRIGGER_SURFACE = "automation_trigger_surface"
    RESULT_ENVELOPE_SURFACE = "result_envelope_surface"
    OCEL_TRACE_SURFACE = "ocel_trace_surface"
    UNKNOWN = "unknown"


class OpenClawObservationFocusKind(StrEnum):
    GATEWAY_MODEL = "gateway_model"
    CHANNEL_MODEL = "channel_model"
    MESSAGE_FLOW_MODEL = "message_flow_model"
    ACTION_MODEL = "action_model"
    WEBHOOK_MODEL = "webhook_model"
    EMAIL_BOUNDARY = "email_boundary"
    CALENDAR_BOUNDARY = "calendar_boundary"
    CONTACT_BOUNDARY = "contact_boundary"
    NOTIFICATION_BOUNDARY = "notification_boundary"
    FILE_ATTACHMENT_BOUNDARY = "file_attachment_boundary"
    PRIVATE_DATA_BOUNDARY = "private_data_boundary"
    CREDENTIAL_BOUNDARY = "credential_boundary"
    NETWORK_BOUNDARY = "network_boundary"
    APPROVAL_BOUNDARY = "approval_boundary"
    AUDIT_BOUNDARY = "audit_boundary"
    AUTOMATION_TRIGGER_BOUNDARY = "automation_trigger_boundary"
    RESULT_ENVELOPE = "result_envelope"
    OCEL_TRACE_RELEVANCE = "ocel_trace_relevance"
    DIGESTION_RELEVANCE = "digestion_relevance"
    DOMINION_RELEVANCE = "dominion_relevance"
    UNKNOWN = "unknown"


class OpenClawCapabilityKind(StrEnum):
    OBSERVE_GATEWAY = "observe_gateway"
    OBSERVE_CHANNEL = "observe_channel"
    RECEIVE_MESSAGE = "receive_message"
    SEND_MESSAGE = "send_message"
    INVOKE_APP_ACTION = "invoke_app_action"
    CALL_WEBHOOK = "call_webhook"
    READ_EMAIL = "read_email"
    SEND_EMAIL = "send_email"
    READ_CALENDAR = "read_calendar"
    MODIFY_CALENDAR = "modify_calendar"
    READ_CONTACTS = "read_contacts"
    SEND_NOTIFICATION = "send_notification"
    READ_ATTACHMENT = "read_attachment"
    ACCESS_PRIVATE_DATA = "access_private_data"
    USE_CREDENTIAL = "use_credential"
    ACCESS_NETWORK = "access_network"
    REQUEST_APPROVAL = "request_approval"
    RECORD_AUDIT = "record_audit"
    EMIT_RESULT_ENVELOPE = "emit_result_envelope"
    UNKNOWN = "unknown"


class OpenClawRiskSignalKind(StrEnum):
    GATEWAY_CONTROL_RISK = "gateway_control_risk"
    CHANNEL_ACCESS_RISK = "channel_access_risk"
    MESSAGE_SEND_RISK = "message_send_risk"
    EMAIL_SEND_RISK = "email_send_risk"
    CALENDAR_WRITE_RISK = "calendar_write_risk"
    CONTACT_ACCESS_RISK = "contact_access_risk"
    NOTIFICATION_SEND_RISK = "notification_send_risk"
    ATTACHMENT_ACCESS_RISK = "attachment_access_risk"
    PRIVATE_DATA_EXPOSURE_RISK = "private_data_exposure_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    WEBHOOK_CALL_RISK = "webhook_call_risk"
    APP_CONTROL_RISK = "app_control_risk"
    EXTERNAL_SIDE_EFFECT_RISK = "external_side_effect_risk"
    APPROVAL_BYPASS_RISK = "approval_bypass_risk"
    AUDIT_GAP_RISK = "audit_gap_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    MEMORY_MUTATION_RISK = "memory_mutation_risk"
    REGISTRY_MUTATION_RISK = "registry_mutation_risk"
    OCEL_EMISSION_RISK = "ocel_emission_risk"
    UNKNOWN = "unknown"


class OpenClawObservationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    OBSERVED = "observed"
    OBSERVED_WITH_GAPS = "observed_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class OpenClawEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_STATIC_OBSERVATION = "sufficient_for_static_observation"
    SUFFICIENT_FOR_PROFILE = "sufficient_for_profile"
    SUFFICIENT_FOR_MANIFEST_EXTRACTION_REVIEW = "sufficient_for_manifest_extraction_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


def _validate_version_includes_v0322(version: str) -> None:
    _require_non_blank("version", version)
    if V0322_VERSION not in version:
        raise ValueError("version must include v0.32.2")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_OPENCLAW_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.2 prohibitions: {sorted(missing)}")


def _capability_is_high_risk(value: OpenClawCapabilityKind | str) -> bool:
    return OpenClawCapabilityKind(value).value in HIGH_RISK_CAPABILITIES


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.2")


@dataclass(frozen=True)
class OpenClawReferenceSourceRef:
    source_ref_id: str
    reference_source_id: str | None = None
    reference_inventory_id: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    local_path_ref: str | None = None
    source_label: str = "OpenClaw-style static reference"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_label", self.source_label)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution"}):
            raise ValueError("OpenClawReferenceSourceRef is not source fetch or execution")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawSurfaceObservation:
    observation_id: str
    surface_kind: OpenClawHarnessSurfaceKind | str
    focus_kind: OpenClawObservationFocusKind | str
    capability_kind: OpenClawCapabilityKind | str
    title: str
    summary: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    evidence_quality: OpenClawEvidenceQuality | str = OpenClawEvidenceQuality.UNKNOWN
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("observation_id", self.observation_id)
        OpenClawHarnessSurfaceKind(self.surface_kind)
        OpenClawObservationFocusKind(self.focus_kind)
        capability = OpenClawCapabilityKind(self.capability_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("summary", self.summary)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        OpenClawEvidenceQuality(self.evidence_quality)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        for name in ("boundary_notes", "prohibited_runtime_actions", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        if capability.value in HIGH_RISK_CAPABILITIES and not self.prohibited_runtime_actions:
            raise ValueError("high-risk capabilities require prohibited_runtime_actions")
        if _metadata_flag_true(self.metadata, {"permission", "runtime_surface"}):
            raise ValueError("OpenClawSurfaceObservation is not permission")

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawGatewaySurfaceObservation:
    gateway_observation_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_gateway_manifest_paths: list[str] = field(default_factory=list)
    possible_gateway_runtime_paths: list[str] = field(default_factory=list)
    possible_gateway_config_paths: list[str] = field(default_factory=list)
    declared_gateway_names: list[str] = field(default_factory=list)
    gateway_control_risk_detected: bool = False
    network_risk_detected: bool = False
    credential_risk_detected: bool = False
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_gateway_connection: bool = False
    ready_for_gateway_control: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gateway_observation_id", self.gateway_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_gateway_manifest_paths", "possible_gateway_runtime_paths", "possible_gateway_config_paths", "declared_gateway_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_gateway_connection", "ready_for_gateway_control", "ready_for_network_access", "ready_for_credential_access", "ready_for_execution"))

    @property
    def gateway_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawChannelSurfaceObservation:
    channel_observation_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_channel_manifest_paths: list[str] = field(default_factory=list)
    possible_channel_runtime_paths: list[str] = field(default_factory=list)
    declared_channel_names: list[str] = field(default_factory=list)
    message_receive_surface_detected: bool = False
    message_send_surface_detected: bool = False
    private_data_risk_detected: bool = False
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_channel_access: bool = False
    ready_for_message_receive: bool = False
    ready_for_message_send: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("channel_observation_id", self.channel_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_channel_manifest_paths", "possible_channel_runtime_paths", "declared_channel_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_channel_access", "ready_for_message_receive", "ready_for_message_send", "ready_for_execution"))

    @property
    def channel_access(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawActionSurfaceObservation:
    action_observation_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_action_manifest_paths: list[str] = field(default_factory=list)
    possible_action_runtime_paths: list[str] = field(default_factory=list)
    possible_trigger_paths: list[str] = field(default_factory=list)
    declared_action_names: list[str] = field(default_factory=list)
    external_side_effect_risk_detected: bool = False
    approval_boundary_detected: bool = False
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_action_execution: bool = False
    ready_for_external_action: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("action_observation_id", self.action_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_action_manifest_paths", "possible_action_runtime_paths", "possible_trigger_paths", "declared_action_names"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_action_execution", "ready_for_external_action", "ready_for_execution"))

    @property
    def action_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawMessageSurfaceBoundary:
    message_boundary_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_message_paths: list[str] = field(default_factory=list)
    possible_send_paths: list[str] = field(default_factory=list)
    possible_receive_paths: list[str] = field(default_factory=list)
    message_keywords_detected: list[str] = field(default_factory=list)
    send_keywords_detected: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    required_boundaries: list[str] = field(default_factory=list)
    ready_for_message_send: bool = False
    ready_for_message_receive: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("message_boundary_id", self.message_boundary_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_message_paths", "possible_send_paths", "possible_receive_paths", "message_keywords_detected", "send_keywords_detected", "required_boundaries"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_message_send", "ready_for_message_receive", "ready_for_execution"))

    @property
    def message_operation(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawPrivateDataBoundaryObservation:
    private_data_boundary_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_private_data_paths: list[str] = field(default_factory=list)
    possible_attachment_paths: list[str] = field(default_factory=list)
    possible_email_calendar_contact_paths: list[str] = field(default_factory=list)
    private_data_keywords_detected: list[str] = field(default_factory=list)
    pii_sensitive_surface_detected: bool = False
    attachment_surface_detected: bool = False
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_private_data_access: bool = False
    ready_for_attachment_access: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("private_data_boundary_id", self.private_data_boundary_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_private_data_paths", "possible_attachment_paths", "possible_email_calendar_contact_paths", "private_data_keywords_detected"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_private_data_access", "ready_for_attachment_access", "ready_for_execution"))

    @property
    def private_data_access(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawCredentialNetworkBoundaryObservation:
    credential_network_boundary_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_credential_paths: list[str] = field(default_factory=list)
    possible_network_paths: list[str] = field(default_factory=list)
    possible_webhook_paths: list[str] = field(default_factory=list)
    credential_keywords_detected: list[str] = field(default_factory=list)
    network_keywords_detected: list[str] = field(default_factory=list)
    webhook_keywords_detected: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_credential_access: bool = False
    ready_for_network_access: bool = False
    ready_for_webhook_call: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("credential_network_boundary_id", self.credential_network_boundary_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_credential_paths", "possible_network_paths", "possible_webhook_paths", "credential_keywords_detected", "network_keywords_detected", "webhook_keywords_detected"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_credential_access", "ready_for_network_access", "ready_for_webhook_call", "ready_for_execution"))

    @property
    def credential_or_network_access(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawApprovalBoundaryRequirement:
    approval_boundary_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_approval_paths: list[str] = field(default_factory=list)
    possible_audit_paths: list[str] = field(default_factory=list)
    approval_required_for_surfaces: list[OpenClawHarnessSurfaceKind | str] = field(default_factory=list)
    audit_required_for_surfaces: list[OpenClawHarnessSurfaceKind | str] = field(default_factory=list)
    approval_gap_detected: bool = False
    audit_gap_detected: bool = False
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    approval_granted: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_boundary_id", self.approval_boundary_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        _validate_string_list("possible_approval_paths", self.possible_approval_paths)
        _validate_string_list("possible_audit_paths", self.possible_audit_paths)
        _validate_kind_list("approval_required_for_surfaces", self.approval_required_for_surfaces, OpenClawHarnessSurfaceKind)
        _validate_kind_list("audit_required_for_surfaces", self.audit_required_for_surfaces, OpenClawHarnessSurfaceKind)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("approval_granted", "ready_for_action_execution", "ready_for_execution"))

    @property
    def approval_is_granted(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawConfigManifestObservation:
    config_manifest_observation_id: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    possible_package_manifest_paths: list[str] = field(default_factory=list)
    possible_config_paths: list[str] = field(default_factory=list)
    possible_action_manifest_paths: list[str] = field(default_factory=list)
    possible_channel_manifest_paths: list[str] = field(default_factory=list)
    possible_gateway_manifest_paths: list[str] = field(default_factory=list)
    possible_script_entries: list[str] = field(default_factory=list)
    possible_dependency_entries: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    ready_for_dependency_install: bool = False
    ready_for_script_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("config_manifest_observation_id", self.config_manifest_observation_id)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        for name in ("possible_package_manifest_paths", "possible_config_paths", "possible_action_manifest_paths", "possible_channel_manifest_paths", "possible_gateway_manifest_paths", "possible_script_entries", "possible_dependency_entries"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        _validate_false(self, ("ready_for_dependency_install", "ready_for_script_execution", "ready_for_execution"))

    @property
    def dependency_install(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawStaticObservationInput:
    openclaw_input_id: str
    external_harness_profile_id: str | None = None
    reference_corpus_snapshot_id: str | None = None
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    requested_focus: list[OpenClawObservationFocusKind | str] = field(default_factory=list)
    task_summary: str = "OpenClaw-style static observation contract input."
    source_version: str = V0322_VERSION
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_OPENCLAW_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("openclaw_input_id", self.openclaw_input_id)
        _validate_string_list("reference_inventory_ids", self.reference_inventory_ids)
        _validate_object_list("reference_source_refs", self.reference_source_refs, OpenClawReferenceSourceRef)
        _validate_kind_list("requested_focus", self.requested_focus, OpenClawObservationFocusKind)
        _require_non_blank("task_summary", self.task_summary)
        _require_non_blank("source_version", self.source_version)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "runtime_input"}):
            raise ValueError("OpenClawStaticObservationInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawObservationFinding:
    finding_id: str
    openclaw_input_id: str
    surface_kind: OpenClawHarnessSurfaceKind | str
    capability_kind: OpenClawCapabilityKind | str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    risk_signal_kinds: list[OpenClawRiskSignalKind | str] = field(default_factory=list)
    evidence_quality: OpenClawEvidenceQuality | str = OpenClawEvidenceQuality.UNKNOWN
    digestion_relevance: bool = False
    dominion_relevance: bool = False
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("openclaw_input_id", self.openclaw_input_id)
        OpenClawHarnessSurfaceKind(self.surface_kind)
        OpenClawCapabilityKind(self.capability_kind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_kind_list("risk_signal_kinds", self.risk_signal_kinds, OpenClawRiskSignalKind)
        OpenClawEvidenceQuality(self.evidence_quality)
        _validate_string_list("assumptions", self.assumptions)
        _validate_string_list("limitations", self.limitations)
        if _metadata_flag_true(self.metadata, {"permission", "internal_skill_candidate", "dominion_target"}):
            raise ValueError("OpenClawObservationFinding is not permission, InternalSkillCandidate, or DominionTarget")

    @property
    def digestion_candidate(self) -> bool:
        return False

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawRiskSignal:
    risk_signal_id: str
    finding_id: str | None
    signal_kind: OpenClawRiskSignalKind | str
    severity: str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    recommended_boundary: str | None = None
    routes_to_dominion_hint: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        OpenClawRiskSignalKind(self.signal_kind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.severity.lower() in {"high", "critical"} and not self.recommended_boundary and not self.routes_to_dominion_hint:
            raise ValueError("high or critical severity requires recommended_boundary or routes_to_dominion_hint")
        if _metadata_flag_true(self.metadata, {"authority_grant", "permission"}):
            raise ValueError("OpenClawRiskSignal does not grant authority")

    @property
    def authority_grant(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawDigestionHint:
    digestion_hint_id: str
    finding_ids: list[str]
    candidate_focus: OpenClawObservationFocusKind | str
    suggested_internal_candidate_kind: str | None
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0326_digestion_candidate_generation: bool = True
    ready_for_internal_candidate_creation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_hint_id", self.digestion_hint_id)
        _validate_string_list("finding_ids", self.finding_ids)
        OpenClawObservationFocusKind(self.candidate_focus)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_internal_candidate_creation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"internal_skill_candidate", "execution_ready"}):
            raise ValueError("OpenClawDigestionHint is not InternalSkillCandidate")

    @property
    def internal_skill_candidate(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawDominionHint:
    dominion_hint_id: str
    finding_ids: list[str]
    risk_signal_ids: list[str]
    suggested_boundary: str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0328_dominion_candidate_emitter: bool = True
    ready_for_dominion_target_creation: bool = False
    ready_for_external_control: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dominion_hint_id", self.dominion_hint_id)
        _validate_string_list("finding_ids", self.finding_ids)
        _validate_string_list("risk_signal_ids", self.risk_signal_ids)
        _require_non_blank("suggested_boundary", self.suggested_boundary)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_dominion_target_creation", "ready_for_external_control", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"dominion_target", "external_control"}):
            raise ValueError("OpenClawDominionHint is not DominionTarget")

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawStyleObservationProfile:
    openclaw_profile_id: str
    base_harness_profile_id: str | None
    display_name: str
    description: str
    source_refs: list[OpenClawReferenceSourceRef] = field(default_factory=list)
    observed_surfaces: list[OpenClawSurfaceObservation] = field(default_factory=list)
    gateway_surface: OpenClawGatewaySurfaceObservation | None = None
    channel_surface: OpenClawChannelSurfaceObservation | None = None
    action_surface: OpenClawActionSurfaceObservation | None = None
    message_boundary: OpenClawMessageSurfaceBoundary | None = None
    private_data_boundary: OpenClawPrivateDataBoundaryObservation | None = None
    credential_network_boundary: OpenClawCredentialNetworkBoundaryObservation | None = None
    approval_boundary: OpenClawApprovalBoundaryRequirement | None = None
    config_manifest_observation: OpenClawConfigManifestObservation | None = None
    status: OpenClawObservationStatus | str = OpenClawObservationStatus.OBSERVED_WITH_GAPS
    gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_execution: bool = False
    ready_for_openclaw_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_channel_access: bool = False
    ready_for_message_send: bool = False
    ready_for_private_data_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_network_access: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("openclaw_profile_id", self.openclaw_profile_id)
        _require_non_blank("display_name", self.display_name)
        _require_non_blank("description", self.description)
        _validate_object_list("source_refs", self.source_refs, OpenClawReferenceSourceRef)
        _validate_object_list("observed_surfaces", self.observed_surfaces, OpenClawSurfaceObservation)
        OpenClawObservationStatus(self.status)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_execution", "ready_for_openclaw_execution", "ready_for_reference_code_execution", "ready_for_gateway_connection", "ready_for_channel_access", "ready_for_message_send", "ready_for_private_data_access", "ready_for_credential_access", "ready_for_network_access"))
        if _metadata_flag_true(self.metadata, {"openclaw_runtime", "execution_ready"}):
            raise ValueError("OpenClawStyleObservationProfile is not OpenClaw runtime")

    @property
    def openclaw_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class OpenClawObservationOutput:
    openclaw_output_id: str
    openclaw_input_id: str
    openclaw_profile: OpenClawStyleObservationProfile
    findings: list[OpenClawObservationFinding] = field(default_factory=list)
    risk_signals: list[OpenClawRiskSignal] = field(default_factory=list)
    digestion_hints: list[OpenClawDigestionHint] = field(default_factory=list)
    dominion_hints: list[OpenClawDominionHint] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_openclaw_execution: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_message_send: bool = False
    ready_for_private_data_access: bool = False
    ready_for_credential_access: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("openclaw_output_id", self.openclaw_output_id)
        _require_non_blank("openclaw_input_id", self.openclaw_input_id)
        if not isinstance(self.openclaw_profile, OpenClawStyleObservationProfile):
            raise TypeError("openclaw_profile must be OpenClawStyleObservationProfile")
        _validate_object_list("findings", self.findings, OpenClawObservationFinding)
        _validate_object_list("risk_signals", self.risk_signals, OpenClawRiskSignal)
        _validate_object_list("digestion_hints", self.digestion_hints, OpenClawDigestionHint)
        _validate_object_list("dominion_hints", self.dominion_hints, OpenClawDominionHint)
        _validate_string_list("gaps", self.gaps)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_false(self, ("ready_for_execution", "ready_for_openclaw_execution", "ready_for_gateway_connection", "ready_for_message_send", "ready_for_private_data_access", "ready_for_credential_access"))
        if _metadata_flag_true(self.metadata, {"manifest_extraction_execution", "digestion_candidate", "dominion_target"}):
            raise ValueError("OpenClawObservationOutput is not runtime, digestion candidate, or dominion target")


@dataclass(frozen=True)
class OpenClawObservationRunPreview:
    run_preview_id: str
    openclaw_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_openclaw_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_gateway_connection_guarantee: bool = True
    no_channel_access_guarantee: bool = True
    no_message_send_guarantee: bool = True
    no_email_access_guarantee: bool = True
    no_calendar_access_guarantee: bool = True
    no_contact_access_guarantee: bool = True
    no_private_data_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_webhook_call_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "no_openclaw_execution_guarantee",
            "no_reference_code_execution_guarantee",
            "no_install_guarantee",
            "no_import_runtime_guarantee",
            "no_gateway_connection_guarantee",
            "no_channel_access_guarantee",
            "no_message_send_guarantee",
            "no_email_access_guarantee",
            "no_calendar_access_guarantee",
            "no_contact_access_guarantee",
            "no_private_data_access_guarantee",
            "no_credential_access_guarantee",
            "no_webhook_call_guarantee",
            "no_network_access_guarantee",
            "no_command_execution_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.2")


@dataclass(frozen=True)
class OpenClawNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_openclaw_execution: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_gateway_connection: bool = True
    no_gateway_control: bool = True
    no_channel_access: bool = True
    no_message_receive: bool = True
    no_message_send: bool = True
    no_email_access: bool = True
    no_email_send: bool = True
    no_calendar_access: bool = True
    no_calendar_write: bool = True
    no_contact_access: bool = True
    no_notification_send: bool = True
    no_attachment_access: bool = True
    no_private_data_access: bool = True
    no_credential_access: bool = True
    no_webhook_call: bool = True
    no_network_access: bool = True
    no_command_execution: bool = True
    no_provider_invocation: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0322(self.version)
        for name in (
            "no_openclaw_execution",
            "no_reference_code_execution",
            "no_dependency_install",
            "no_import_runtime",
            "no_gateway_connection",
            "no_gateway_control",
            "no_channel_access",
            "no_message_receive",
            "no_message_send",
            "no_email_access",
            "no_email_send",
            "no_calendar_access",
            "no_calendar_write",
            "no_contact_access",
            "no_notification_send",
            "no_attachment_access",
            "no_private_data_access",
            "no_credential_access",
            "no_webhook_call",
            "no_network_access",
            "no_command_execution",
            "no_provider_invocation",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_ocel_emission",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.2")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0322ReadinessReport:
    report_id: str
    version: str
    openclaw_profile_id: str | None
    openclaw_output_id: str | None
    summary: str
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_v0325_risk_classification: bool = True
    ready_for_execution: bool = False
    ready_for_openclaw_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_channel_access: bool = False
    ready_for_message_send: bool = False
    ready_for_private_data_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_network_access: bool = False
    ready_for_webhook_call: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_OPENCLAW_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0322(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_execution", "ready_for_openclaw_execution", "ready_for_reference_code_execution", "ready_for_gateway_connection", "ready_for_channel_access", "ready_for_message_send", "ready_for_private_data_access", "ready_for_credential_access", "ready_for_network_access", "ready_for_webhook_call"))
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_ready"}):
            raise ValueError("V0322ReadinessReport is not runtime enablement")


def build_openclaw_reference_source_ref(source_ref_id: str, reference_source_id: str | None = None, reference_inventory_id: str | None = None, reference_entry_ids: list[str] | None = None, local_path_ref: str | None = None, source_label: str = "OpenClaw-style static reference", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> OpenClawReferenceSourceRef:
    return OpenClawReferenceSourceRef(source_ref_id, reference_source_id, reference_inventory_id, list(reference_entry_ids or []), local_path_ref, source_label, list(evidence_refs or []), dict(metadata or {}))


def build_openclaw_surface_observation(observation_id: str, surface_kind: OpenClawHarnessSurfaceKind | str, focus_kind: OpenClawObservationFocusKind | str, capability_kind: OpenClawCapabilityKind | str, title: str, summary: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, evidence_quality: OpenClawEvidenceQuality | str = OpenClawEvidenceQuality.UNKNOWN, risk_signal_kinds: list[OpenClawRiskSignalKind | str] | None = None, boundary_notes: list[str] | None = None, prohibited_runtime_actions: list[str] | None = None, assumptions: list[str] | None = None, limitations: list[str] | None = None, metadata: dict[str, Any] | None = None) -> OpenClawSurfaceObservation:
    return OpenClawSurfaceObservation(
        observation_id=observation_id,
        surface_kind=surface_kind,
        focus_kind=focus_kind,
        capability_kind=capability_kind,
        title=title,
        summary=summary,
        source_refs=list(source_refs or []),
        evidence_quality=evidence_quality,
        risk_signal_kinds=list(risk_signal_kinds or []),
        boundary_notes=list(boundary_notes or []),
        prohibited_runtime_actions=list(prohibited_runtime_actions or (DEFAULT_OPENCLAW_PROHIBITED_RUNTIME_ACTIONS if _capability_is_high_risk(capability_kind) else [])),
        assumptions=list(assumptions or []),
        limitations=list(limitations or []),
        metadata=dict(metadata or {}),
    )


def build_openclaw_gateway_surface_observation(gateway_observation_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawGatewaySurfaceObservation:
    return OpenClawGatewaySurfaceObservation(gateway_observation_id=gateway_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_channel_surface_observation(channel_observation_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawChannelSurfaceObservation:
    return OpenClawChannelSurfaceObservation(channel_observation_id=channel_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_action_surface_observation(action_observation_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawActionSurfaceObservation:
    return OpenClawActionSurfaceObservation(action_observation_id=action_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_message_surface_boundary(message_boundary_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawMessageSurfaceBoundary:
    return OpenClawMessageSurfaceBoundary(message_boundary_id=message_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_private_data_boundary_observation(private_data_boundary_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawPrivateDataBoundaryObservation:
    return OpenClawPrivateDataBoundaryObservation(private_data_boundary_id=private_data_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_credential_network_boundary_observation(credential_network_boundary_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawCredentialNetworkBoundaryObservation:
    return OpenClawCredentialNetworkBoundaryObservation(credential_network_boundary_id=credential_network_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_approval_boundary_requirement(approval_boundary_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawApprovalBoundaryRequirement:
    return OpenClawApprovalBoundaryRequirement(approval_boundary_id=approval_boundary_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_config_manifest_observation(config_manifest_observation_id: str, source_refs: list[OpenClawReferenceSourceRef] | None = None, **kwargs: Any) -> OpenClawConfigManifestObservation:
    return OpenClawConfigManifestObservation(config_manifest_observation_id=config_manifest_observation_id, source_refs=list(source_refs or []), **kwargs)


def build_openclaw_static_observation_input(openclaw_input_id: str, **kwargs: Any) -> OpenClawStaticObservationInput:
    return OpenClawStaticObservationInput(openclaw_input_id=openclaw_input_id, **kwargs)


def build_openclaw_observation_finding(finding_id: str, openclaw_input_id: str, surface_kind: OpenClawHarnessSurfaceKind | str, capability_kind: OpenClawCapabilityKind | str, summary: str, **kwargs: Any) -> OpenClawObservationFinding:
    return OpenClawObservationFinding(finding_id=finding_id, openclaw_input_id=openclaw_input_id, surface_kind=surface_kind, capability_kind=capability_kind, summary=summary, **kwargs)


def build_openclaw_risk_signal(risk_signal_id: str, signal_kind: OpenClawRiskSignalKind | str, severity: str, summary: str, finding_id: str | None = None, **kwargs: Any) -> OpenClawRiskSignal:
    return OpenClawRiskSignal(risk_signal_id=risk_signal_id, finding_id=finding_id, signal_kind=signal_kind, severity=severity, summary=summary, **kwargs)


def build_openclaw_digestion_hint(digestion_hint_id: str, finding_ids: list[str], candidate_focus: OpenClawObservationFocusKind | str, summary: str, suggested_internal_candidate_kind: str | None = None, **kwargs: Any) -> OpenClawDigestionHint:
    return OpenClawDigestionHint(digestion_hint_id=digestion_hint_id, finding_ids=list(finding_ids), candidate_focus=candidate_focus, suggested_internal_candidate_kind=suggested_internal_candidate_kind, summary=summary, **kwargs)


def build_openclaw_dominion_hint(dominion_hint_id: str, finding_ids: list[str], risk_signal_ids: list[str], suggested_boundary: str, summary: str, **kwargs: Any) -> OpenClawDominionHint:
    return OpenClawDominionHint(dominion_hint_id=dominion_hint_id, finding_ids=list(finding_ids), risk_signal_ids=list(risk_signal_ids), suggested_boundary=suggested_boundary, summary=summary, **kwargs)


def build_openclaw_style_observation_profile(openclaw_profile_id: str, display_name: str, description: str, base_harness_profile_id: str | None = None, **kwargs: Any) -> OpenClawStyleObservationProfile:
    return OpenClawStyleObservationProfile(openclaw_profile_id=openclaw_profile_id, base_harness_profile_id=base_harness_profile_id, display_name=display_name, description=description, **kwargs)


def build_openclaw_observation_output(openclaw_output_id: str, openclaw_input_id: str, openclaw_profile: OpenClawStyleObservationProfile, **kwargs: Any) -> OpenClawObservationOutput:
    return OpenClawObservationOutput(openclaw_output_id=openclaw_output_id, openclaw_input_id=openclaw_input_id, openclaw_profile=openclaw_profile, **kwargs)


def build_openclaw_observation_run_preview(run_preview_id: str = "openclaw_observation_run_preview:v0.32.2", **kwargs: Any) -> OpenClawObservationRunPreview:
    return OpenClawObservationRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_openclaw_no_execution_guarantee(guarantee_id: str = "openclaw_no_execution_guarantee:v0.32.2", evidence_refs: list[str] | None = None, metadata: dict[str, Any] | None = None) -> OpenClawNoExecutionGuarantee:
    return OpenClawNoExecutionGuarantee(guarantee_id=guarantee_id, version=V0322_VERSION, evidence_refs=list(evidence_refs or []), metadata=dict(metadata or {}))


def build_v0322_readiness_report(report_id: str = "v0322_readiness_report", openclaw_profile_id: str | None = None, openclaw_output_id: str | None = None, summary: str = "v0.32.2 is ready for manifest extraction and risk classification design-stage handoff only, not execution.", **kwargs: Any) -> V0322ReadinessReport:
    return V0322ReadinessReport(report_id=report_id, version=V0322_VERSION, openclaw_profile_id=openclaw_profile_id, openclaw_output_id=openclaw_output_id, summary=summary, **kwargs)


def classify_inventory_entry_as_openclaw_surface(entry: ReferenceFileInventoryEntry) -> OpenClawHarnessSurfaceKind:
    name = entry.file_name.lower()
    path = entry.relative_path.lower()
    detected = (entry.detected_kind or "").lower()
    if "webhook" in path or "webhook" in name:
        return OpenClawHarnessSurfaceKind.WEBHOOK_SURFACE
    if "gateway" in path or "gateway" in name:
        return OpenClawHarnessSurfaceKind.GATEWAY_SURFACE
    if "channel" in path or "channel" in name:
        return OpenClawHarnessSurfaceKind.CHANNEL_SURFACE
    if "message" in path or "send" in path:
        return OpenClawHarnessSurfaceKind.MESSAGE_SEND_SURFACE
    if "email" in path:
        return OpenClawHarnessSurfaceKind.EMAIL_SURFACE
    if "calendar" in path:
        return OpenClawHarnessSurfaceKind.CALENDAR_SURFACE
    if "contact" in path:
        return OpenClawHarnessSurfaceKind.CONTACT_SURFACE
    if "attachment" in path or "file" in path:
        return OpenClawHarnessSurfaceKind.FILE_ATTACHMENT_SURFACE
    if "credential" in path or "secret" in path or "token" in path:
        return OpenClawHarnessSurfaceKind.CREDENTIAL_SURFACE
    if "private" in path or "pii" in path:
        return OpenClawHarnessSurfaceKind.PRIVATE_DATA_SURFACE
    if "action" in path or "action" in detected:
        return OpenClawHarnessSurfaceKind.ACTION_MANIFEST_SURFACE
    if "package" in name or "config" in path or entry.file_extension in {".json", ".toml", ".yaml", ".yml"}:
        return OpenClawHarnessSurfaceKind.ACTION_MANIFEST_SURFACE
    return OpenClawHarnessSurfaceKind.UNKNOWN


def infer_openclaw_capability_from_surface(surface_kind: OpenClawHarnessSurfaceKind | str) -> OpenClawCapabilityKind:
    surface = OpenClawHarnessSurfaceKind(surface_kind)
    return {
        OpenClawHarnessSurfaceKind.GATEWAY_SURFACE: OpenClawCapabilityKind.OBSERVE_GATEWAY,
        OpenClawHarnessSurfaceKind.CHANNEL_SURFACE: OpenClawCapabilityKind.OBSERVE_CHANNEL,
        OpenClawHarnessSurfaceKind.MESSAGE_RECEIVE_SURFACE: OpenClawCapabilityKind.RECEIVE_MESSAGE,
        OpenClawHarnessSurfaceKind.MESSAGE_SEND_SURFACE: OpenClawCapabilityKind.SEND_MESSAGE,
        OpenClawHarnessSurfaceKind.APP_CONTROL_SURFACE: OpenClawCapabilityKind.INVOKE_APP_ACTION,
        OpenClawHarnessSurfaceKind.EXTERNAL_ACTION_SURFACE: OpenClawCapabilityKind.INVOKE_APP_ACTION,
        OpenClawHarnessSurfaceKind.WEBHOOK_SURFACE: OpenClawCapabilityKind.CALL_WEBHOOK,
        OpenClawHarnessSurfaceKind.EMAIL_SURFACE: OpenClawCapabilityKind.READ_EMAIL,
        OpenClawHarnessSurfaceKind.CALENDAR_SURFACE: OpenClawCapabilityKind.READ_CALENDAR,
        OpenClawHarnessSurfaceKind.CONTACT_SURFACE: OpenClawCapabilityKind.READ_CONTACTS,
        OpenClawHarnessSurfaceKind.NOTIFICATION_SURFACE: OpenClawCapabilityKind.SEND_NOTIFICATION,
        OpenClawHarnessSurfaceKind.FILE_ATTACHMENT_SURFACE: OpenClawCapabilityKind.READ_ATTACHMENT,
        OpenClawHarnessSurfaceKind.PRIVATE_DATA_SURFACE: OpenClawCapabilityKind.ACCESS_PRIVATE_DATA,
        OpenClawHarnessSurfaceKind.CREDENTIAL_SURFACE: OpenClawCapabilityKind.USE_CREDENTIAL,
        OpenClawHarnessSurfaceKind.NETWORK_SURFACE: OpenClawCapabilityKind.ACCESS_NETWORK,
        OpenClawHarnessSurfaceKind.APPROVAL_BOUNDARY_SURFACE: OpenClawCapabilityKind.REQUEST_APPROVAL,
        OpenClawHarnessSurfaceKind.AUDIT_BOUNDARY_SURFACE: OpenClawCapabilityKind.RECORD_AUDIT,
        OpenClawHarnessSurfaceKind.RESULT_ENVELOPE_SURFACE: OpenClawCapabilityKind.EMIT_RESULT_ENVELOPE,
    }.get(surface, OpenClawCapabilityKind.UNKNOWN)


def infer_openclaw_risk_signals_from_inventory_entry(entry: ReferenceFileInventoryEntry) -> list[OpenClawRiskSignalKind]:
    surface = classify_inventory_entry_as_openclaw_surface(entry)
    capability = infer_openclaw_capability_from_surface(surface)
    risks: list[OpenClawRiskSignalKind] = []
    if capability == OpenClawCapabilityKind.OBSERVE_GATEWAY:
        risks.append(OpenClawRiskSignalKind.GATEWAY_CONTROL_RISK)
    if capability == OpenClawCapabilityKind.OBSERVE_CHANNEL:
        risks.append(OpenClawRiskSignalKind.CHANNEL_ACCESS_RISK)
    if capability == OpenClawCapabilityKind.SEND_MESSAGE:
        risks.append(OpenClawRiskSignalKind.MESSAGE_SEND_RISK)
    if capability == OpenClawCapabilityKind.CALL_WEBHOOK:
        risks.extend([OpenClawRiskSignalKind.WEBHOOK_CALL_RISK, OpenClawRiskSignalKind.NETWORK_ACCESS_RISK])
    if capability == OpenClawCapabilityKind.READ_EMAIL:
        risks.append(OpenClawRiskSignalKind.PRIVATE_DATA_EXPOSURE_RISK)
    if capability == OpenClawCapabilityKind.READ_CALENDAR:
        risks.append(OpenClawRiskSignalKind.CALENDAR_WRITE_RISK)
    if capability == OpenClawCapabilityKind.READ_CONTACTS:
        risks.append(OpenClawRiskSignalKind.CONTACT_ACCESS_RISK)
    if capability == OpenClawCapabilityKind.READ_ATTACHMENT:
        risks.append(OpenClawRiskSignalKind.ATTACHMENT_ACCESS_RISK)
    if capability == OpenClawCapabilityKind.ACCESS_PRIVATE_DATA:
        risks.append(OpenClawRiskSignalKind.PRIVATE_DATA_EXPOSURE_RISK)
    if capability == OpenClawCapabilityKind.USE_CREDENTIAL:
        risks.append(OpenClawRiskSignalKind.CREDENTIAL_ACCESS_RISK)
    if capability == OpenClawCapabilityKind.ACCESS_NETWORK:
        risks.append(OpenClawRiskSignalKind.NETWORK_ACCESS_RISK)
    if capability == OpenClawCapabilityKind.INVOKE_APP_ACTION:
        risks.extend([OpenClawRiskSignalKind.APP_CONTROL_RISK, OpenClawRiskSignalKind.EXTERNAL_SIDE_EFFECT_RISK])
    return risks or [OpenClawRiskSignalKind.UNKNOWN]


def openclaw_profile_preserves_no_execution(profile: OpenClawStyleObservationProfile) -> bool:
    return (
        profile.ready_for_execution is False
        and profile.ready_for_openclaw_execution is False
        and profile.ready_for_reference_code_execution is False
        and profile.ready_for_gateway_connection is False
        and profile.ready_for_channel_access is False
        and profile.ready_for_message_send is False
        and profile.ready_for_private_data_access is False
        and profile.ready_for_credential_access is False
        and profile.ready_for_network_access is False
        and profile.openclaw_runtime is False
    )


def openclaw_output_is_not_manifest_or_digestive_runtime(output: OpenClawObservationOutput) -> bool:
    return (
        output.ready_for_execution is False
        and output.ready_for_openclaw_execution is False
        and output.ready_for_gateway_connection is False
        and output.ready_for_message_send is False
        and output.ready_for_private_data_access is False
        and output.ready_for_credential_access is False
    )


def openclaw_run_preview_preserves_no_execution(preview: OpenClawObservationRunPreview) -> bool:
    return (
        preview.no_openclaw_execution_guarantee
        and preview.no_reference_code_execution_guarantee
        and preview.no_gateway_connection_guarantee
        and preview.no_channel_access_guarantee
        and preview.no_message_send_guarantee
        and preview.no_private_data_access_guarantee
        and preview.no_credential_access_guarantee
        and preview.no_network_access_guarantee
    )


def v0322_readiness_report_is_not_runtime_ready(report: V0322ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_openclaw_execution is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_channel_access is False
        and report.ready_for_message_send is False
        and report.ready_for_private_data_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_network_access is False
        and report.ready_for_webhook_call is False
    )

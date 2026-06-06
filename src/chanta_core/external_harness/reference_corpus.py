from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .profiles import (
    DEFAULT_PROHIBITED_FILE_PATTERNS,
    ExternalHarnessProfileKind,
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
    _validate_version_includes_v0320,
    normalize_external_harness_profile_kind,
    V0320_VERSION,
)


DEFAULT_REFERENCE_PROHIBITED_RUNTIME_ACTIONS = [
    "harness execution",
    "reference code execution",
    "source_ref fetch",
    "live scan",
    "install",
    "import runtime",
    "dependency resolution",
    "network",
    "credential",
    "secret file read",
    "command",
    "provider invocation",
    "browser",
    "rpa",
    "gateway",
    "packet send",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
    "UI runtime",
]


class ReferenceHarnessSourceKind(StrEnum):
    LOCAL_REFERENCE_DIRECTORY = "local_reference_directory"
    LOCAL_REFERENCE_FILE = "local_reference_file"
    LOCAL_REFERENCE_MANIFEST = "local_reference_manifest"
    LOCAL_REFERENCE_DOCUMENTATION = "local_reference_documentation"
    LOCAL_REFERENCE_CONFIG = "local_reference_config"
    SANITIZED_MANIFEST = "sanitized_manifest"
    MANUAL_REFERENCE = "manual_reference"
    UNKNOWN = "unknown"


def normalize_reference_harness_source_kind(value: ReferenceHarnessSourceKind | str) -> ReferenceHarnessSourceKind:
    if isinstance(value, ReferenceHarnessSourceKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("reference harness source kind must not be blank")
        return ReferenceHarnessSourceKind(stripped)
    raise TypeError(f"unsupported reference harness source kind: {value!r}")


def reference_harness_source_kind_executes(_: ReferenceHarnessSourceKind | str) -> bool:
    normalize_reference_harness_source_kind(_)
    return False


def _validate_static_policy_patterns(patterns: list[str]) -> None:
    _validate_string_list("prohibited_file_patterns", patterns)
    for pattern in DEFAULT_PROHIBITED_FILE_PATTERNS:
        if pattern not in patterns:
            raise ValueError("prohibited_file_patterns must include secret-like defaults")


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_REFERENCE_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.0 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class ReferenceHarnessCorpusPolicy:
    policy_id: str
    read_only: bool = True
    allow_file_tree_inventory: bool = True
    allow_text_file_read: bool = True
    allow_manifest_parse: bool = True
    allow_hashing: bool = True
    prohibit_execution: bool = True
    prohibit_install: bool = True
    prohibit_import_runtime: bool = True
    prohibit_network: bool = True
    prohibit_credentials: bool = True
    prohibit_command_execution: bool = True
    prohibit_provider_invocation: bool = True
    prohibit_browser_automation: bool = True
    prohibit_rpa_control: bool = True
    prohibit_gateway_control: bool = True
    prohibit_packet_send: bool = True
    prohibit_secret_file_read: bool = True
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        if self.read_only is not True:
            raise ValueError("read_only must be True in v0.32.0")
        for name in (
            "prohibit_execution",
            "prohibit_install",
            "prohibit_import_runtime",
            "prohibit_network",
            "prohibit_credentials",
            "prohibit_command_execution",
            "prohibit_provider_invocation",
            "prohibit_browser_automation",
            "prohibit_rpa_control",
            "prohibit_gateway_control",
            "prohibit_packet_send",
            "prohibit_secret_file_read",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.0")
        for name in ("allow_file_tree_inventory", "allow_text_file_read", "allow_manifest_parse", "allow_hashing"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        _validate_static_policy_patterns(self.prohibited_file_patterns)
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "execution_policy"}):
            raise ValueError("ReferenceHarnessCorpusPolicy is not runtime enforcement by itself")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceHarnessSource:
    source_id: str
    source_kind: ReferenceHarnessSourceKind | str
    harness_kind: ExternalHarnessProfileKind | str
    local_path_ref: str | None
    display_name: str
    description: str
    corpus_policy_id: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_id", self.source_id)
        normalize_reference_harness_source_kind(self.source_kind)
        normalize_external_harness_profile_kind(self.harness_kind)
        _require_non_blank("display_name", self.display_name)
        _require_non_blank("description", self.description)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"executable_source", "runtime_import"}):
            raise ValueError("ReferenceHarnessSource must not imply executable source")

    @property
    def executable_source(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceHarnessCorpus:
    corpus_id: str
    version: str
    sources: list[ReferenceHarnessSource]
    corpus_policy: ReferenceHarnessCorpusPolicy
    root_path_ref: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_static_observation: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("corpus_id", self.corpus_id)
        _validate_version_includes_v0320(self.version)
        _validate_object_list("sources", self.sources, ReferenceHarnessSource)
        if not isinstance(self.corpus_policy, ReferenceHarnessCorpusPolicy):
            raise TypeError("corpus_policy must be ReferenceHarnessCorpusPolicy")
        if not reference_corpus_policy_preserves_read_only(self.corpus_policy):
            raise ValueError("corpus_policy must preserve read-only/no-execution")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("gaps", self.gaps)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_corpus", "active_source"}):
            raise ValueError("ReferenceHarnessCorpus must not imply runtime")

    @property
    def runtime_corpus(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceFileInventoryPolicy:
    inventory_policy_id: str
    allow_file_tree_inventory: bool = True
    allow_file_size: bool = True
    allow_extension_capture: bool = True
    allow_hash_capture: bool = False
    allow_text_preview: bool = False
    max_text_preview_chars: int = 0
    prohibit_binary_read: bool = True
    prohibit_secret_file_read: bool = True
    prohibit_execution: bool = True
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_FILE_PATTERNS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("inventory_policy_id", self.inventory_policy_id)
        for name in (
            "allow_file_tree_inventory",
            "allow_file_size",
            "allow_extension_capture",
            "allow_hash_capture",
            "allow_text_preview",
            "prohibit_binary_read",
            "prohibit_secret_file_read",
            "prohibit_execution",
        ):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")
        if self.max_text_preview_chars < 0:
            raise ValueError("max_text_preview_chars must be >= 0")
        if self.prohibit_secret_file_read is not True:
            raise ValueError("prohibit_secret_file_read must be True in v0.32.0")
        if self.prohibit_execution is not True:
            raise ValueError("prohibit_execution must be True in v0.32.0")
        _validate_static_policy_patterns(self.prohibited_file_patterns)
        if _metadata_flag_true(self.metadata, {"runtime_file_access", "execution_policy"}):
            raise ValueError("ReferenceFileInventoryPolicy is read-only contract metadata")

    @property
    def read_only_policy(self) -> bool:
        return True


@dataclass(frozen=True)
class ReferenceFileInventoryEntry:
    entry_id: str
    source_id: str
    relative_path: str
    file_name: str
    file_extension: str | None = None
    file_size_bytes: int | None = None
    file_hash: str | None = None
    detected_kind: str | None = None
    text_preview: str | None = None
    skipped_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("entry_id", self.entry_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("relative_path", self.relative_path)
        _require_non_blank("file_name", self.file_name)
        if self.file_size_bytes is not None and self.file_size_bytes < 0:
            raise ValueError("file_size_bytes must be None or >= 0")
        if self.text_preview is not None and self.skipped_reason:
            raise ValueError("skipped files must be represented with skipped_reason, not text_preview")
        if _metadata_flag_true(self.metadata, {"file_execution", "runtime_file_access"}):
            raise ValueError("ReferenceFileInventoryEntry must not imply file execution")

    @property
    def file_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceFileInventory:
    inventory_id: str
    source_id: str
    inventory_policy_id: str
    entries: list[ReferenceFileInventoryEntry]
    skipped_paths: list[str] = field(default_factory=list)
    manifest_candidate_paths: list[str] = field(default_factory=list)
    documentation_candidate_paths: list[str] = field(default_factory=list)
    config_candidate_paths: list[str] = field(default_factory=list)
    risk_surface_candidate_paths: list[str] = field(default_factory=list)
    summary: str = "Reference file inventory contract only; no runtime file access."
    ready_for_manifest_extraction: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("inventory_id", self.inventory_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("inventory_policy_id", self.inventory_policy_id)
        _validate_object_list("entries", self.entries, ReferenceFileInventoryEntry)
        for name in (
            "skipped_paths",
            "manifest_candidate_paths",
            "documentation_candidate_paths",
            "config_candidate_paths",
            "risk_surface_candidate_paths",
        ):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_file_access", "execution"}):
            raise ValueError("ReferenceFileInventory must not imply runtime file access")

    @property
    def runtime_file_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceCorpusSnapshot:
    snapshot_id: str
    corpus_id: str
    version: str
    source_ids: list[str]
    inventory_ids: list[str]
    profile_seed_ids: list[str]
    summary: str
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_v0321_opencode_profile: bool = True
    ready_for_v0322_openclaw_profile: bool = True
    ready_for_v0323_hermes_profile: bool = True
    ready_for_manifest_extraction: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _require_non_blank("corpus_id", self.corpus_id)
        _validate_version_includes_v0320(self.version)
        for name in ("source_ids", "inventory_ids", "profile_seed_ids", "gaps", "blocked_reasons"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.32.0")
        if _metadata_flag_true(self.metadata, {"runtime_state", "persistence"}):
            raise ValueError("ReferenceCorpusSnapshot must not imply persistence")

    @property
    def runtime_state(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceCorpusNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_reference_code_execution: bool = True
    no_import_runtime: bool = True
    no_install: bool = True
    no_dependency_resolution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_command_execution: bool = True
    no_provider_invocation: bool = True
    no_browser_automation: bool = True
    no_rpa_control: bool = True
    no_gateway_control: bool = True
    no_packet_send: bool = True
    no_workspace_write: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0320(self.version)
        for name in (
            "no_reference_code_execution",
            "no_import_runtime",
            "no_install",
            "no_dependency_resolution",
            "no_network_access",
            "no_credential_access",
            "no_secret_file_read",
            "no_command_execution",
            "no_provider_invocation",
            "no_browser_automation",
            "no_rpa_control",
            "no_gateway_control",
            "no_packet_send",
            "no_workspace_write",
            "no_registry_mutation",
            "no_memory_mutation",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.32.0")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0320ReadinessReport:
    report_id: str
    version: str
    profile_set_id: str | None
    reference_corpus_snapshot_id: str | None
    summary: str
    ready_for_v0321_opencode_profile: bool = True
    ready_for_v0322_openclaw_profile: bool = True
    ready_for_v0323_hermes_profile: bool = True
    ready_for_v0324_manifest_extraction: bool = True
    ready_for_execution: bool = False
    ready_for_external_harness_execution: bool = False
    ready_for_reference_code_execution: bool = False
    ready_for_live_scan: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_REFERENCE_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0320(self.version)
        _require_non_blank("summary", self.summary)
        for name in (
            "ready_for_execution",
            "ready_for_external_harness_execution",
            "ready_for_reference_code_execution",
            "ready_for_live_scan",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.32.0")
        for name in (
            "completed_items",
            "blocked_items",
            "future_track_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "execution_ready"}):
            raise ValueError("V0320ReadinessReport is not runtime enablement")


def build_reference_corpus_policy(
    policy_id: str = "reference_harness_corpus_policy:v0.32.0",
    prohibited_file_patterns: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceHarnessCorpusPolicy:
    return ReferenceHarnessCorpusPolicy(
        policy_id=policy_id,
        prohibited_file_patterns=list(prohibited_file_patterns or DEFAULT_PROHIBITED_FILE_PATTERNS),
        metadata=dict(metadata or {}),
    )


def build_reference_harness_source(
    source_id: str,
    source_kind: ReferenceHarnessSourceKind | str,
    harness_kind: ExternalHarnessProfileKind | str,
    display_name: str,
    description: str,
    local_path_ref: str | None = None,
    corpus_policy_id: str | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceHarnessSource:
    return ReferenceHarnessSource(
        source_id=source_id,
        source_kind=source_kind,
        harness_kind=harness_kind,
        local_path_ref=local_path_ref,
        display_name=display_name,
        description=description,
        corpus_policy_id=corpus_policy_id,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_reference_harness_corpus(
    corpus_id: str,
    sources: list[ReferenceHarnessSource] | None = None,
    corpus_policy: ReferenceHarnessCorpusPolicy | None = None,
    root_path_ref: str | None = None,
    evidence_refs: list[str] | None = None,
    gaps: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceHarnessCorpus:
    return ReferenceHarnessCorpus(
        corpus_id=corpus_id,
        version=V0320_VERSION,
        sources=list(sources or []),
        corpus_policy=corpus_policy or build_reference_corpus_policy(),
        root_path_ref=root_path_ref,
        evidence_refs=list(evidence_refs or []),
        gaps=list(gaps or []),
        ready_for_static_observation=True,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_reference_file_inventory_policy(
    inventory_policy_id: str = "reference_file_inventory_policy:v0.32.0",
    allow_hash_capture: bool = False,
    allow_text_preview: bool = False,
    max_text_preview_chars: int = 0,
    prohibited_file_patterns: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceFileInventoryPolicy:
    return ReferenceFileInventoryPolicy(
        inventory_policy_id=inventory_policy_id,
        allow_hash_capture=allow_hash_capture,
        allow_text_preview=allow_text_preview,
        max_text_preview_chars=max_text_preview_chars,
        prohibited_file_patterns=list(prohibited_file_patterns or DEFAULT_PROHIBITED_FILE_PATTERNS),
        metadata=dict(metadata or {}),
    )


def build_reference_file_inventory_entry(
    entry_id: str,
    source_id: str,
    relative_path: str,
    file_name: str,
    file_extension: str | None = None,
    file_size_bytes: int | None = None,
    file_hash: str | None = None,
    detected_kind: str | None = None,
    text_preview: str | None = None,
    skipped_reason: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceFileInventoryEntry:
    return ReferenceFileInventoryEntry(
        entry_id=entry_id,
        source_id=source_id,
        relative_path=relative_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size_bytes=file_size_bytes,
        file_hash=file_hash,
        detected_kind=detected_kind,
        text_preview=text_preview,
        skipped_reason=skipped_reason,
        metadata=dict(metadata or {}),
    )


def build_reference_file_inventory(
    inventory_id: str,
    source_id: str,
    inventory_policy_id: str,
    entries: list[ReferenceFileInventoryEntry] | None = None,
    skipped_paths: list[str] | None = None,
    manifest_candidate_paths: list[str] | None = None,
    documentation_candidate_paths: list[str] | None = None,
    config_candidate_paths: list[str] | None = None,
    risk_surface_candidate_paths: list[str] | None = None,
    summary: str = "Reference file inventory contract only; no runtime file access.",
    ready_for_manifest_extraction: bool = True,
    metadata: dict[str, Any] | None = None,
) -> ReferenceFileInventory:
    return ReferenceFileInventory(
        inventory_id=inventory_id,
        source_id=source_id,
        inventory_policy_id=inventory_policy_id,
        entries=list(entries or []),
        skipped_paths=list(skipped_paths or []),
        manifest_candidate_paths=list(manifest_candidate_paths or []),
        documentation_candidate_paths=list(documentation_candidate_paths or []),
        config_candidate_paths=list(config_candidate_paths or []),
        risk_surface_candidate_paths=list(risk_surface_candidate_paths or []),
        summary=summary,
        ready_for_manifest_extraction=ready_for_manifest_extraction,
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_reference_corpus_snapshot(
    snapshot_id: str,
    corpus_id: str,
    source_ids: list[str] | None = None,
    inventory_ids: list[str] | None = None,
    profile_seed_ids: list[str] | None = None,
    summary: str = "Reference corpus snapshot contract only; no persistence or execution.",
    gaps: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceCorpusSnapshot:
    return ReferenceCorpusSnapshot(
        snapshot_id=snapshot_id,
        corpus_id=corpus_id,
        version=V0320_VERSION,
        source_ids=list(source_ids or []),
        inventory_ids=list(inventory_ids or []),
        profile_seed_ids=list(profile_seed_ids or []),
        summary=summary,
        gaps=list(gaps or []),
        blocked_reasons=list(blocked_reasons or []),
        ready_for_execution=False,
        metadata=dict(metadata or {}),
    )


def build_reference_corpus_no_execution_guarantee(
    guarantee_id: str = "reference_corpus_no_execution_guarantee:v0.32.0",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ReferenceCorpusNoExecutionGuarantee:
    return ReferenceCorpusNoExecutionGuarantee(
        guarantee_id=guarantee_id,
        version=V0320_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_v0320_readiness_report(
    report_id: str = "v0320_readiness_report",
    profile_set_id: str | None = None,
    reference_corpus_snapshot_id: str | None = None,
    summary: str = "v0.32.0 is ready for design-stage external harness profile handoff only, not execution.",
    completed_items: list[str] | None = None,
    blocked_items: list[str] | None = None,
    future_track_items: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    withdrawal_conditions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> V0320ReadinessReport:
    return V0320ReadinessReport(
        report_id=report_id,
        version=V0320_VERSION,
        profile_set_id=profile_set_id,
        reference_corpus_snapshot_id=reference_corpus_snapshot_id,
        summary=summary,
        ready_for_execution=False,
        ready_for_external_harness_execution=False,
        ready_for_reference_code_execution=False,
        ready_for_live_scan=False,
        completed_items=list(completed_items or []),
        blocked_items=list(blocked_items or []),
        future_track_items=list(future_track_items or []),
        prohibited_until_later_gate=list(DEFAULT_REFERENCE_PROHIBITED_RUNTIME_ACTIONS),
        evidence_refs=list(evidence_refs or []),
        withdrawal_conditions=list(withdrawal_conditions or []),
        metadata=dict(metadata or {}),
    )


def reference_corpus_policy_preserves_read_only(policy: ReferenceHarnessCorpusPolicy) -> bool:
    return (
        policy.read_only is True
        and policy.prohibit_execution is True
        and policy.prohibit_install is True
        and policy.prohibit_import_runtime is True
        and policy.prohibit_network is True
        and policy.prohibit_credentials is True
        and policy.prohibit_command_execution is True
        and policy.prohibit_provider_invocation is True
        and policy.prohibit_browser_automation is True
        and policy.prohibit_rpa_control is True
        and policy.prohibit_gateway_control is True
        and policy.prohibit_packet_send is True
        and policy.prohibit_secret_file_read is True
        and policy.runtime_enforcement is False
    )


def reference_inventory_preserves_no_execution(inventory: ReferenceFileInventory) -> bool:
    return inventory.ready_for_execution is False and inventory.runtime_file_access is False


def reference_snapshot_is_not_runtime(snapshot: ReferenceCorpusSnapshot) -> bool:
    return snapshot.ready_for_execution is False and snapshot.runtime_state is False


def v0320_readiness_report_is_not_runtime_ready(report: V0320ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_external_harness_execution is False
        and report.ready_for_reference_code_execution is False
        and report.ready_for_live_scan is False
    )

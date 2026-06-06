from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .profile_runtime import AgentRuntimeLoadout, AgentRuntimeProfile


V0332_VERSION = "v0.33.2"
V0332_RELEASE_NAME = "v0.33.2 Prompt Assembly Pipeline"

DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS = [
    "model_invocation",
    "model invocation",
    "provider_invocation",
    "provider invocation",
    "agent_step_execution",
    "agent step execution",
    "session_runtime_execution",
    "session runtime execution",
    "read_only_tool_execution",
    "read-only tool execution",
    "tool_execution",
    "tool execution",
    "workspace_inspection_execution",
    "workspace inspection execution",
    "network_access",
    "network access",
    "credential_access",
    "credential access",
    "command_execution",
    "command execution",
    "workspace_write",
    "workspace write",
    "code_edit",
    "code edit",
    "patch_application",
    "patch application",
    "reference_file_access",
    "reference file access",
    "reference_code_execution",
    "reference code execution",
    "reference_import",
    "reference import",
    "dependency_install",
    "dependency install",
    "secret_file_read",
    "secret file read",
    "registry_mutation",
    "registry mutation",
    "memory_mutation",
    "memory mutation",
    "ocel_emission",
    "OCEL emission",
    "ui_runtime",
    "UI runtime",
    "external_control",
    "external control",
    "authority_grant",
    "authority grant",
]


class PromptAssemblyBlockKind(StrEnum):
    RUNTIME_BOUNDARY = "runtime_boundary"
    PERMISSION_BOUNDARY = "permission_boundary"
    PROFILE = "profile"
    PERSONA_PROJECTION = "persona_projection"
    MODE_BINDING = "mode_binding"
    POLICY_OVERLAY = "policy_overlay"
    TASK = "task"
    USER_REQUEST = "user_request"
    TOOL_AVAILABILITY = "tool_availability"
    REFERENCE_CONTEXT = "reference_context"
    EVIDENCE = "evidence"
    OCEL_TRACE_SUMMARY = "ocel_trace_summary"
    PROHIBITED_ACTIONS = "prohibited_actions"
    OUTPUT_CONTRACT = "output_contract"
    SAFETY_INSTRUCTION = "safety_instruction"
    DEVELOPER_NOTE = "developer_note"
    INTERNAL_NOTE = "internal_note"
    UNKNOWN = "unknown"


class PromptAssemblyBlockTrustLevel(StrEnum):
    TRUSTED_RUNTIME_BOUNDARY = "trusted_runtime_boundary"
    TRUSTED_POLICY = "trusted_policy"
    TRUSTED_PROFILE = "trusted_profile"
    TRUSTED_INTERNAL = "trusted_internal"
    USER_SUPPLIED = "user_supplied"
    REFERENCE_CONTEXT = "reference_context"
    UNTRUSTED_EXTERNAL_REFERENCE = "untrusted_external_reference"
    EVIDENCE_REFERENCE = "evidence_reference"
    TOOL_METADATA = "tool_metadata"
    UNKNOWN = "unknown"


class PromptAssemblyBlockPlacement(StrEnum):
    SYSTEM_BOUNDARY_SECTION = "system_boundary_section"
    RUNTIME_POLICY_SECTION = "runtime_policy_section"
    PROFILE_SECTION = "profile_section"
    TASK_SECTION = "task_section"
    TOOL_AVAILABILITY_SECTION = "tool_availability_section"
    EVIDENCE_SECTION = "evidence_section"
    REFERENCE_CONTEXT_SECTION = "reference_context_section"
    OUTPUT_CONTRACT_SECTION = "output_contract_section"
    PROHIBITED_ACTION_SECTION = "prohibited_action_section"
    APPENDIX_SECTION = "appendix_section"
    EXCLUDED = "excluded"
    UNKNOWN = "unknown"


class PromptAssemblySourceKind(StrEnum):
    INTERNAL_RUNTIME_BOUNDARY = "internal_runtime_boundary"
    AGENT_RUNTIME_PROFILE = "agent_runtime_profile"
    AGENT_RUNTIME_LOADOUT = "agent_runtime_loadout"
    POLICY_OVERLAY = "policy_overlay"
    TOOL_AVAILABILITY_VIEW = "tool_availability_view"
    REFERENCE_CONTEXT = "reference_context"
    OPENCODE_REFERENCE_CONTEXT = "opencode_reference_context"
    HERMES_REFERENCE_CONTEXT = "hermes_reference_context"
    OPENCLAW_REFERENCE_CONTEXT = "openclaw_reference_context"
    USER_TASK = "user_task"
    EVIDENCE_REF = "evidence_ref"
    OCEL_SUMMARY_REF = "ocel_summary_ref"
    MANUAL_PROMPT_SPEC = "manual_prompt_spec"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PromptAssemblyStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    ASSEMBLED = "assembled"
    ASSEMBLED_WITH_GAPS = "assembled_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class PromptAssemblyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    ASSEMBLY_CONTRACT_READY = "assembly_contract_ready"
    PROMPT_PAYLOAD_READY = "prompt_payload_ready"
    DESIGN_HANDOFF_READY_FOR_V0333 = "design_handoff_ready_for_v0333"
    DESIGN_HANDOFF_READY_FOR_V0336 = "design_handoff_ready_for_v0336"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PromptAssemblyRiskKind(StrEnum):
    PROMPT_INJECTION_RISK = "prompt_injection_risk"
    BOUNDARY_OVERRIDE_RISK = "boundary_override_risk"
    UNTRUSTED_REFERENCE_INSTRUCTION_RISK = "untrusted_reference_instruction_risk"
    USER_INSTRUCTION_CONFLICT_RISK = "user_instruction_conflict_risk"
    SECRET_LEAK_RISK = "secret_leak_risk"
    TOOL_AUTHORITY_CONFUSION_RISK = "tool_authority_confusion_risk"
    PROVIDER_INVOCATION_CONFUSION_RISK = "provider_invocation_confusion_risk"
    WORKSPACE_WRITE_CONFUSION_RISK = "workspace_write_confusion_risk"
    COMMAND_EXECUTION_CONFUSION_RISK = "command_execution_confusion_risk"
    EXTERNAL_CONTROL_CONFUSION_RISK = "external_control_confusion_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    TOKEN_BUDGET_OVERFLOW_RISK = "token_budget_overflow_risk"
    UNKNOWN = "unknown"


class PromptAssemblyOutputFormat(StrEnum):
    STRUCTURED_BLOCKS = "structured_blocks"
    MESSAGE_LIST = "message_list"
    PLAIN_TEXT_PROMPT = "plain_text_prompt"
    DEBUG_SUMMARY = "debug_summary"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_agent_step_execution",
    "ready_for_session_runtime_execution",
    "ready_for_read_only_tool_execution",
    "ready_for_workspace_inspection_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ocel_emission",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

UNTRUSTED_TRUST_LEVELS = {
    PromptAssemblyBlockTrustLevel.USER_SUPPLIED,
    PromptAssemblyBlockTrustLevel.REFERENCE_CONTEXT,
    PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE,
    PromptAssemblyBlockTrustLevel.UNKNOWN,
}

TRUSTED_BOUNDARY_PLACEMENTS = {
    PromptAssemblyBlockPlacement.SYSTEM_BOUNDARY_SECTION,
    PromptAssemblyBlockPlacement.RUNTIME_POLICY_SECTION,
}


def _validate_version_includes_v0332(version: str) -> None:
    _require_non_blank("version", version)
    if V0332_VERSION not in version:
        raise ValueError("version must include v0.33.2")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.2")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.33.2")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_source_ref_list(values: list["PromptAssemblySourceRef"]) -> None:
    _validate_object_list("source_refs", values, PromptAssemblySourceRef)


def _validate_context_block_list(values: list["PromptContextBlock"]) -> None:
    _validate_object_list("ordered_blocks", values, PromptContextBlock)


def _validate_non_negative_int(name: str, value: int | None) -> None:
    if value is not None and (not isinstance(value, int) or value < 0):
        raise ValueError(f"{name} must be None or >= 0")


def _validate_positive_int(name: str, value: int | None) -> None:
    if value is not None and (not isinstance(value, int) or value <= 0):
        raise ValueError(f"{name} must be None or > 0")


def _validate_prohibited_runtime_actions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.33.2 prohibitions: {sorted(missing)}")


def _is_untrusted(trust_level: PromptAssemblyBlockTrustLevel | str) -> bool:
    return PromptAssemblyBlockTrustLevel(trust_level) in UNTRUSTED_TRUST_LEVELS


def _validate_message_list(values: list[dict[str, str]]) -> None:
    if not isinstance(values, list):
        raise TypeError("assembled_messages must be list[dict[str, str]]")
    for item in values:
        if not isinstance(item, dict):
            raise TypeError("assembled_messages must be list[dict[str, str]]")
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in item.items()):
            raise TypeError("assembled_messages must be list[dict[str, str]]")


@dataclass(frozen=True)
class PromptAssemblyFlagSet:
    flag_set_id: str
    version: str = V0332_VERSION
    prompt_payload_constructed: bool = False
    ready_for_v0333_session_runtime: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_session_runtime_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0332(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "model_invocation", "provider_invocation"}):
            raise ValueError("PromptAssemblyFlagSet is not runtime or provider enablement")


@dataclass(frozen=True)
class PromptAssemblySourceRef:
    source_ref_id: str
    source_kind: PromptAssemblySourceKind | str
    source_id: str
    source_summary: str
    trust_level: PromptAssemblyBlockTrustLevel | str = PromptAssemblyBlockTrustLevel.TRUSTED_INTERNAL
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PromptAssemblySourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        PromptAssemblyBlockTrustLevel(self.trust_level)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "file_read", "execution"}):
            raise ValueError("PromptAssemblySourceRef is not fetch, file read, or execution")

    @property
    def fetch(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptContextBlock:
    block_id: str
    block_kind: PromptAssemblyBlockKind | str
    trust_level: PromptAssemblyBlockTrustLevel | str
    placement: PromptAssemblyBlockPlacement | str
    title: str
    content: str
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    token_budget_estimate: int | None = None
    risk_kinds: list[PromptAssemblyRiskKind | str] = field(default_factory=list)
    is_instructional: bool = False
    is_untrusted: bool = False
    excluded: bool = False
    exclusion_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("block_id", "title", "content"):
            _require_non_blank(name, getattr(self, name))
        block_kind = PromptAssemblyBlockKind(self.block_kind)
        trust_level = PromptAssemblyBlockTrustLevel(self.trust_level)
        placement = PromptAssemblyBlockPlacement(self.placement)
        _validate_source_ref_list(self.source_refs)
        _validate_non_negative_int("token_budget_estimate", self.token_budget_estimate)
        _validate_enum_list("risk_kinds", self.risk_kinds, PromptAssemblyRiskKind)
        if _is_untrusted(trust_level) and self.is_instructional:
            raise ValueError("untrusted external/reference/user blocks must not be instructional")
        if _is_untrusted(trust_level) and placement in TRUSTED_BOUNDARY_PLACEMENTS:
            raise ValueError("untrusted external/reference/user blocks cannot be boundary or policy instructions")
        if block_kind in {PromptAssemblyBlockKind.RUNTIME_BOUNDARY, PromptAssemblyBlockKind.PERMISSION_BOUNDARY} and trust_level != PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY:
            raise ValueError("boundary blocks must use trusted_runtime_boundary trust level")
        if block_kind == PromptAssemblyBlockKind.POLICY_OVERLAY and trust_level != PromptAssemblyBlockTrustLevel.TRUSTED_POLICY:
            raise ValueError("policy blocks must use trusted_policy trust level")
        if self.excluded and not self.exclusion_reason:
            raise ValueError("excluded blocks must have exclusion_reason")
        if _metadata_flag_true(self.metadata, {"execution", "model_invocation", "tool_execution"}):
            raise ValueError("PromptContextBlock is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptBoundaryBlock:
    boundary_block_id: str
    runtime_boundary_summary: str
    permission_gate_summary: str
    non_negotiable_rules: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS))
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_block_id", "runtime_boundary_summary", "permission_gate_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("non_negotiable_rules", self.non_negotiable_rules)
        _validate_prohibited_runtime_actions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "execution"}):
            raise ValueError("PromptBoundaryBlock is not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptProfileBlock:
    profile_block_id: str
    profile_name: str
    mode_summary: str
    persona_summary: str
    constraints_summary: str
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("profile_block_id", "profile_name", "mode_summary", "persona_summary", "constraints_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"active_session", "execution"}):
            raise ValueError("PromptProfileBlock is not active session")

    @property
    def active_session(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptPolicyBlock:
    policy_block_id: str
    policy_summary: str
    policy_rules: list[str] = field(default_factory=list)
    safe_fail_rules: list[str] = field(default_factory=list)
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_block_id", self.policy_block_id)
        _require_non_blank("policy_summary", self.policy_summary)
        _validate_string_list("policy_rules", self.policy_rules)
        _validate_string_list("safe_fail_rules", self.safe_fail_rules)
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"active_policy_enforcement", "policy_execution"}):
            raise ValueError("PromptPolicyBlock is not active policy enforcement")

    @property
    def active_policy_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptTaskBlock:
    task_block_id: str
    task_summary: str
    user_request_summary: str
    explicit_user_constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("task_block_id", "task_summary", "user_request_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("explicit_user_constraints", self.explicit_user_constraints)
        _validate_string_list("assumptions", self.assumptions)
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"command_execution", "execution"}):
            raise ValueError("PromptTaskBlock is not command execution")

    @property
    def command_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptReferenceContextBlock:
    reference_context_block_id: str
    reference_summary: str
    opencode_reference_note: str | None = "references/OpenCode is read-only design/reference context only."
    hermes_reference_note: str | None = "references/Hermes is read-only design/reference context only."
    openclaw_reference_note: str | None = "references/OpenClaw is optional read-only design/reference context only."
    reference_path_refs: list[str] = field(default_factory=lambda: ["references/OpenCode", "references/Hermes"])
    allowed_reference_uses: list[str] = field(default_factory=lambda: ["path refs", "design/reference context notes"])
    prohibited_reference_uses: list[str] = field(default_factory=lambda: ["file access", "execute", "import runtime", "install dependencies", "read secrets"])
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    trust_level: PromptAssemblyBlockTrustLevel | str = PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("reference_context_block_id", self.reference_context_block_id)
        _require_non_blank("reference_summary", self.reference_summary)
        for name in ("reference_path_refs", "allowed_reference_uses", "prohibited_reference_uses"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        trust_level = PromptAssemblyBlockTrustLevel(self.trust_level)
        if trust_level == PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY:
            raise ValueError("reference context block must not be trusted_runtime_boundary")
        if _metadata_flag_true(self.metadata, {"file_access", "reference_execution", "reference_import", "dependency_install"}):
            raise ValueError("PromptReferenceContextBlock is not file access or reference execution")

    @property
    def file_access(self) -> bool:
        return False

    @property
    def reference_execution_permission(self) -> bool:
        return False

    @property
    def path_refs_only(self) -> bool:
        return True


@dataclass(frozen=True)
class PromptToolAvailabilityBlock:
    tool_block_id: str
    summary: str
    available_tool_names: list[str] = field(default_factory=list)
    unavailable_tool_names: list[str] = field(default_factory=list)
    future_tool_names: list[str] = field(default_factory=list)
    prohibited_tool_actions: list[str] = field(default_factory=lambda: ["tool execution", "tool registry access"])
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    ready_for_tool_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("tool_block_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        for name in ("available_tool_names", "unavailable_tool_names", "future_tool_names", "prohibited_tool_actions"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_tool_execution is not False:
            raise ValueError("ready_for_tool_execution must always be False")
        if _metadata_flag_true(self.metadata, {"tool_execution", "tool_registry_access"}):
            raise ValueError("PromptToolAvailabilityBlock is not tool execution")

    @property
    def tool_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptEvidenceBlock:
    evidence_block_id: str
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_block_id", self.evidence_block_id)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_source_ref_list(self.source_refs)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("conflict_notes", self.conflict_notes)
        if _metadata_flag_true(self.metadata, {"runtime_trust", "execution"}):
            raise ValueError("PromptEvidenceBlock is not runtime trust")

    @property
    def runtime_trust(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptOutputContractBlock:
    output_contract_block_id: str
    response_style_summary: str
    required_sections: list[str] = field(default_factory=list)
    prohibited_content: list[str] = field(default_factory=list)
    citation_requirements: list[str] = field(default_factory=list)
    uncertainty_handling_rules: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("output_contract_block_id", self.output_contract_block_id)
        _require_non_blank("response_style_summary", self.response_style_summary)
        for name in ("required_sections", "prohibited_content", "citation_requirements", "uncertainty_handling_rules"):
            _validate_string_list(name, getattr(self, name))
        if _metadata_flag_true(self.metadata, {"implementation", "execution"}):
            raise ValueError("PromptOutputContractBlock is not implementation")

    @property
    def implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptProhibitedActionBlock:
    prohibited_action_block_id: str
    prohibited_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS))
    safe_alternatives: list[str] = field(default_factory=lambda: ["no-op", "defer", "ask user", "design-stage handoff"])
    no_op_conditions: list[str] = field(default_factory=lambda: ["blocked runtime request", "missing safe design evidence"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prohibited_action_block_id", self.prohibited_action_block_id)
        _validate_prohibited_runtime_actions("prohibited_actions", self.prohibited_actions)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("no_op_conditions", self.no_op_conditions)


@dataclass(frozen=True)
class PromptAssemblyInput:
    assembly_input_id: str
    source_version: str
    runtime_profile_id: str | None
    runtime_boundary_id: str | None
    task_summary: str
    source_refs: list[PromptAssemblySourceRef] = field(default_factory=list)
    requested_output_format: PromptAssemblyOutputFormat | str = PromptAssemblyOutputFormat.MESSAGE_LIST
    token_budget_limit: int | None = None
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("assembly_input_id", self.assembly_input_id)
        _require_non_blank("source_version", self.source_version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_source_ref_list(self.source_refs)
        PromptAssemblyOutputFormat(self.requested_output_format)
        _validate_positive_int("token_budget_limit", self.token_budget_limit)
        _validate_prohibited_runtime_actions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"model_invocation_request", "provider_invocation", "execution"}):
            raise ValueError("PromptAssemblyInput is not model invocation request")

    @property
    def model_invocation_request(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptAssemblyPlan:
    plan_id: str
    assembly_input_id: str
    planned_block_order: list[PromptAssemblyBlockKind | str] = field(default_factory=list)
    expected_sections: list[str] = field(default_factory=list)
    excluded_source_refs: list[str] = field(default_factory=list)
    risk_kinds: list[PromptAssemblyRiskKind | str] = field(default_factory=list)
    summary: str = "Prompt assembly plan only; no model invocation."
    ready_for_prompt_payload_construction: bool = False
    ready_for_model_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("assembly_input_id", self.assembly_input_id)
        _validate_enum_list("planned_block_order", self.planned_block_order, PromptAssemblyBlockKind)
        _validate_string_list("expected_sections", self.expected_sections)
        _validate_string_list("excluded_source_refs", self.excluded_source_refs)
        _validate_enum_list("risk_kinds", self.risk_kinds, PromptAssemblyRiskKind)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_model_invocation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"model_invocation", "execution"}):
            raise ValueError("PromptAssemblyPlan is not model invocation")

    @property
    def model_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptInjectionRiskSignal:
    risk_signal_id: str
    risk_kind: PromptAssemblyRiskKind | str
    source_ref_ids: list[str] = field(default_factory=list)
    affected_block_ids: list[str] = field(default_factory=list)
    severity: str = "unknown"
    summary: str = "Prompt assembly risk signal."
    recommended_action: str = "keep as quoted reference context or exclude"
    block_should_be_excluded: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        PromptAssemblyRiskKind(self.risk_kind)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        _validate_string_list("affected_block_ids", self.affected_block_ids)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _require_non_blank("recommended_action", self.recommended_action)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"remediation_execution", "execution"}):
            raise ValueError("PromptInjectionRiskSignal is advisory only")

    @property
    def advisory_only(self) -> bool:
        return True


@dataclass(frozen=True)
class PromptAssemblyValidationReport:
    validation_report_id: str
    assembly_input_id: str
    checked_block_ids: list[str] = field(default_factory=list)
    risk_signals: list[PromptInjectionRiskSignal] = field(default_factory=list)
    blocked_block_ids: list[str] = field(default_factory=list)
    warning_block_ids: list[str] = field(default_factory=list)
    validation_passed: bool = False
    summary: str = "Prompt assembly validation report only."
    ready_for_prompt_output: bool = False
    ready_for_model_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _require_non_blank("assembly_input_id", self.assembly_input_id)
        _validate_string_list("checked_block_ids", self.checked_block_ids)
        _validate_object_list("risk_signals", self.risk_signals, PromptInjectionRiskSignal)
        _validate_string_list("blocked_block_ids", self.blocked_block_ids)
        _validate_string_list("warning_block_ids", self.warning_block_ids)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_model_invocation", "ready_for_execution"))
        if self.validation_passed and self.blocked_block_ids:
            raise ValueError("validation_passed cannot be True if blocked_block_ids is non-empty")
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "model_invocation", "execution"}):
            raise ValueError("PromptAssemblyValidationReport is not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptAssemblyOutput:
    prompt_output_id: str
    assembly_input_id: str
    output_format: PromptAssemblyOutputFormat | str
    ordered_blocks: list[PromptContextBlock] = field(default_factory=list)
    boundary_block: PromptBoundaryBlock | None = None
    profile_block: PromptProfileBlock | None = None
    policy_block: PromptPolicyBlock | None = None
    task_block: PromptTaskBlock | None = None
    reference_context_block: PromptReferenceContextBlock | None = None
    tool_availability_block: PromptToolAvailabilityBlock | None = None
    evidence_block: PromptEvidenceBlock | None = None
    output_contract_block: PromptOutputContractBlock | None = None
    prohibited_action_block: PromptProhibitedActionBlock | None = None
    assembled_prompt_text: str | None = None
    assembled_messages: list[dict[str, str]] = field(default_factory=list)
    validation_report_id: str | None = None
    token_budget_estimate: int | None = None
    ready_for_v0333_session_runtime: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_model_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prompt_output_id", self.prompt_output_id)
        _require_non_blank("assembly_input_id", self.assembly_input_id)
        PromptAssemblyOutputFormat(self.output_format)
        _validate_context_block_list(self.ordered_blocks)
        _validate_message_list(self.assembled_messages)
        _validate_non_negative_int("token_budget_estimate", self.token_budget_estimate)
        _validate_false(self, ("ready_for_model_invocation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"model_call", "agent_step", "execution"}):
            raise ValueError("PromptAssemblyOutput is not model call or agent step")

    @property
    def model_call(self) -> bool:
        return False

    @property
    def agent_step(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptAssemblyReport:
    report_id: str
    version: str
    assembly_input_id: str
    prompt_output_id: str | None
    validation_report_id: str | None
    status: PromptAssemblyStatus | str
    readiness_level: PromptAssemblyReadinessLevel | str
    summary: str
    assembled_block_count: int = 0
    excluded_block_count: int = 0
    risk_signal_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0333_session_runtime: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_model_invocation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "assembly_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0332(self.version)
        PromptAssemblyStatus(self.status)
        PromptAssemblyReadinessLevel(self.readiness_level)
        for name in ("assembled_block_count", "excluded_block_count", "risk_signal_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_model_invocation", "ready_for_execution"))
        if (self.ready_for_v0333_session_runtime or self.ready_for_v0336_agent_step_runner) and self.blocked_items:
            raise ValueError("design-stage report handoff readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"model_invocation", "execution"}):
            raise ValueError("PromptAssemblyReport is not model invocation")

    @property
    def model_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptAssemblyRunPreview:
    run_preview_id: str
    assembly_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["assemble provided in-memory prompt blocks"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["PromptAssemblyOutput", "PromptAssemblyReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: ["model invocation", "agent step execution", "tool execution", "reference file access"])
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_session_runtime_execution_guarantee: bool = True
    no_read_only_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_reference_file_access_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_ocel_emission_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.2")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class PromptAssemblyNoRuntimeGuarantee:
    guarantee_id: str
    version: str = V0332_VERSION
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_agent_step_execution: bool = True
    no_session_runtime_execution: bool = True
    no_read_only_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_reference_file_access: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_file_read: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0332(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.2")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0332ReadinessReport:
    report_id: str
    version: str = V0332_VERSION
    prompt_output_id: str | None = None
    prompt_assembly_report_id: str | None = None
    summary: str = "v0.33.2 constructs prompt assembly artifacts only."
    ready_for_v0333_session_runtime: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_session_runtime_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0332(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_runtime_actions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if (self.ready_for_v0333_session_runtime or self.ready_for_v0336_agent_step_runner) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "model_invocation", "provider_invocation"}):
            raise ValueError("V0332ReadinessReport is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_prompt_assembly_flags(flag_set_id: str = "prompt_assembly_flags:v0.33.2", **kwargs: Any) -> PromptAssemblyFlagSet:
    return PromptAssemblyFlagSet(flag_set_id=flag_set_id, version=V0332_VERSION, **kwargs)


def build_prompt_assembly_source_ref(
    source_ref_id: str,
    source_kind: PromptAssemblySourceKind | str = PromptAssemblySourceKind.MANUAL_PROMPT_SPEC,
    source_id: str = "manual_prompt_spec",
    source_summary: str = "Provided in-memory prompt assembly metadata.",
    **kwargs: Any,
) -> PromptAssemblySourceRef:
    return PromptAssemblySourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_prompt_context_block(block_id: str, block_kind: PromptAssemblyBlockKind | str, title: str, content: str, **kwargs: Any) -> PromptContextBlock:
    return PromptContextBlock(
        block_id=block_id,
        block_kind=block_kind,
        trust_level=kwargs.pop("trust_level", PromptAssemblyBlockTrustLevel.TRUSTED_INTERNAL),
        placement=kwargs.pop("placement", PromptAssemblyBlockPlacement.APPENDIX_SECTION),
        title=title,
        content=content,
        **kwargs,
    )


def build_prompt_boundary_block(boundary_block_id: str, **kwargs: Any) -> PromptBoundaryBlock:
    return PromptBoundaryBlock(
        boundary_block_id=boundary_block_id,
        runtime_boundary_summary=kwargs.pop("runtime_boundary_summary", "Internal runtime boundary remains non-execution."),
        permission_gate_summary=kwargs.pop("permission_gate_summary", "Permission gate metadata is not permission grant."),
        **kwargs,
    )


def build_prompt_profile_block(profile_block_id: str, **kwargs: Any) -> PromptProfileBlock:
    return PromptProfileBlock(
        profile_block_id=profile_block_id,
        profile_name=kwargs.pop("profile_name", "Vera"),
        mode_summary=kwargs.pop("mode_summary", "Agent profile mode context only."),
        persona_summary=kwargs.pop("persona_summary", "Persona projection is not authority."),
        constraints_summary=kwargs.pop("constraints_summary", "Preserve no model/provider/tool/runtime execution."),
        **kwargs,
    )


def build_prompt_policy_block(policy_block_id: str, **kwargs: Any) -> PromptPolicyBlock:
    return PromptPolicyBlock(
        policy_block_id=policy_block_id,
        policy_summary=kwargs.pop("policy_summary", "Policy prompt block is not active policy execution."),
        policy_rules=kwargs.pop("policy_rules", ["no model invocation", "no tool execution", "no reference file access"]),
        safe_fail_rules=kwargs.pop("safe_fail_rules", ["defer", "ask user", "no-op"]),
        **kwargs,
    )


def build_prompt_task_block(task_block_id: str, task_summary: str = "Assemble prompt from in-memory artifacts.", **kwargs: Any) -> PromptTaskBlock:
    return PromptTaskBlock(
        task_block_id=task_block_id,
        task_summary=task_summary,
        user_request_summary=kwargs.pop("user_request_summary", task_summary),
        **kwargs,
    )


def build_prompt_reference_context_block(reference_context_block_id: str, **kwargs: Any) -> PromptReferenceContextBlock:
    return PromptReferenceContextBlock(
        reference_context_block_id=reference_context_block_id,
        reference_summary=kwargs.pop("reference_summary", "Reference paths are read-only design/reference context only."),
        **kwargs,
    )


def build_prompt_tool_availability_block(tool_block_id: str, **kwargs: Any) -> PromptToolAvailabilityBlock:
    return PromptToolAvailabilityBlock(
        tool_block_id=tool_block_id,
        summary=kwargs.pop("summary", "Tool availability metadata only; no tool execution."),
        **kwargs,
    )


def build_prompt_evidence_block(evidence_block_id: str, **kwargs: Any) -> PromptEvidenceBlock:
    return PromptEvidenceBlock(
        evidence_block_id=evidence_block_id,
        summary=kwargs.pop("summary", "Evidence refs are not runtime trust."),
        **kwargs,
    )


def build_prompt_output_contract_block(output_contract_block_id: str, **kwargs: Any) -> PromptOutputContractBlock:
    return PromptOutputContractBlock(
        output_contract_block_id=output_contract_block_id,
        response_style_summary=kwargs.pop("response_style_summary", "Produce concise, evidence-aware output."),
        **kwargs,
    )


def build_prompt_prohibited_action_block(prohibited_action_block_id: str, **kwargs: Any) -> PromptProhibitedActionBlock:
    return PromptProhibitedActionBlock(prohibited_action_block_id=prohibited_action_block_id, **kwargs)


def build_prompt_assembly_input(assembly_input_id: str, task_summary: str, **kwargs: Any) -> PromptAssemblyInput:
    return PromptAssemblyInput(
        assembly_input_id=assembly_input_id,
        source_version=kwargs.pop("source_version", V0332_VERSION),
        runtime_profile_id=kwargs.pop("runtime_profile_id", None),
        runtime_boundary_id=kwargs.pop("runtime_boundary_id", None),
        task_summary=task_summary,
        **kwargs,
    )


def build_prompt_assembly_plan(plan_id: str, assembly_input_id: str, **kwargs: Any) -> PromptAssemblyPlan:
    return PromptAssemblyPlan(
        plan_id=plan_id,
        assembly_input_id=assembly_input_id,
        planned_block_order=kwargs.pop(
            "planned_block_order",
            [
                PromptAssemblyBlockKind.RUNTIME_BOUNDARY,
                PromptAssemblyBlockKind.POLICY_OVERLAY,
                PromptAssemblyBlockKind.PROFILE,
                PromptAssemblyBlockKind.TASK,
                PromptAssemblyBlockKind.TOOL_AVAILABILITY,
                PromptAssemblyBlockKind.EVIDENCE,
                PromptAssemblyBlockKind.REFERENCE_CONTEXT,
                PromptAssemblyBlockKind.OUTPUT_CONTRACT,
            ],
        ),
        ready_for_prompt_payload_construction=kwargs.pop("ready_for_prompt_payload_construction", True),
        **kwargs,
    )


def build_prompt_injection_risk_signal(risk_signal_id: str, risk_kind: PromptAssemblyRiskKind | str = PromptAssemblyRiskKind.PROMPT_INJECTION_RISK, **kwargs: Any) -> PromptInjectionRiskSignal:
    return PromptInjectionRiskSignal(risk_signal_id=risk_signal_id, risk_kind=risk_kind, **kwargs)


def build_prompt_assembly_validation_report(validation_report_id: str, assembly_input_id: str, **kwargs: Any) -> PromptAssemblyValidationReport:
    return PromptAssemblyValidationReport(
        validation_report_id=validation_report_id,
        assembly_input_id=assembly_input_id,
        **kwargs,
    )


def build_prompt_assembly_output(prompt_output_id: str, assembly_input_id: str, **kwargs: Any) -> PromptAssemblyOutput:
    return PromptAssemblyOutput(
        prompt_output_id=prompt_output_id,
        assembly_input_id=assembly_input_id,
        output_format=kwargs.pop("output_format", PromptAssemblyOutputFormat.MESSAGE_LIST),
        **kwargs,
    )


def build_prompt_assembly_report(report_id: str, assembly_input_id: str, **kwargs: Any) -> PromptAssemblyReport:
    return PromptAssemblyReport(
        report_id=report_id,
        version=V0332_VERSION,
        assembly_input_id=assembly_input_id,
        prompt_output_id=kwargs.pop("prompt_output_id", None),
        validation_report_id=kwargs.pop("validation_report_id", None),
        status=kwargs.pop("status", PromptAssemblyStatus.ASSEMBLED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", PromptAssemblyReadinessLevel.PROMPT_PAYLOAD_READY),
        summary=kwargs.pop("summary", "Prompt assembly report is not model invocation."),
        **kwargs,
    )


def build_prompt_assembly_run_preview(run_preview_id: str, **kwargs: Any) -> PromptAssemblyRunPreview:
    return PromptAssemblyRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_prompt_assembly_no_runtime_guarantee(guarantee_id: str = "prompt_assembly_no_runtime:v0.33.2", **kwargs: Any) -> PromptAssemblyNoRuntimeGuarantee:
    return PromptAssemblyNoRuntimeGuarantee(guarantee_id=guarantee_id, version=V0332_VERSION, **kwargs)


def build_v0332_readiness_report(report_id: str = "v0332_readiness_report", **kwargs: Any) -> V0332ReadinessReport:
    return V0332ReadinessReport(report_id=report_id, version=V0332_VERSION, **kwargs)


def validate_prompt_block_order(
    ordered_blocks: list[PromptContextBlock],
    assembly_input_id: str = "prompt_assembly_input",
    validation_report_id: str = "prompt_assembly_validation:v0.33.2",
) -> PromptAssemblyValidationReport:
    _validate_context_block_list(ordered_blocks)
    _require_non_blank("assembly_input_id", assembly_input_id)
    checked_block_ids = [block.block_id for block in ordered_blocks]
    blocked_block_ids: list[str] = []
    warning_block_ids: list[str] = []
    risk_signals: list[PromptInjectionRiskSignal] = []

    trusted_boundary_seen = False
    for block in ordered_blocks:
        trust_level = PromptAssemblyBlockTrustLevel(block.trust_level)
        placement = PromptAssemblyBlockPlacement(block.placement)
        if trust_level == PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY:
            trusted_boundary_seen = True
        if _is_untrusted(trust_level) and placement in TRUSTED_BOUNDARY_PLACEMENTS:
            blocked_block_ids.append(block.block_id)
            risk_signals.append(
                build_prompt_injection_risk_signal(
                    f"{block.block_id}:boundary_override",
                    PromptAssemblyRiskKind.BOUNDARY_OVERRIDE_RISK,
                    affected_block_ids=[block.block_id],
                    severity="blocked",
                    summary="Untrusted block attempted trusted boundary placement.",
                    block_should_be_excluded=True,
                )
            )
        if _is_untrusted(trust_level) and block.is_instructional:
            blocked_block_ids.append(block.block_id)
            risk_signals.append(
                build_prompt_injection_risk_signal(
                    f"{block.block_id}:instructional_reference",
                    PromptAssemblyRiskKind.UNTRUSTED_REFERENCE_INSTRUCTION_RISK,
                    affected_block_ids=[block.block_id],
                    severity="blocked",
                    summary="Untrusted block attempted instructional use.",
                    block_should_be_excluded=True,
                )
            )
        if not trusted_boundary_seen and block.block_kind in {PromptAssemblyBlockKind.TASK, PromptAssemblyBlockKind.USER_REQUEST, PromptAssemblyBlockKind.REFERENCE_CONTEXT}:
            warning_block_ids.append(block.block_id)

    return build_prompt_assembly_validation_report(
        validation_report_id,
        assembly_input_id,
        checked_block_ids=checked_block_ids,
        risk_signals=risk_signals,
        blocked_block_ids=blocked_block_ids,
        warning_block_ids=warning_block_ids,
        validation_passed=not blocked_block_ids,
        ready_for_prompt_output=not blocked_block_ids,
        summary="Prompt block order validation is advisory and does not execute remediation.",
    )


def assemble_prompt_from_blocks(
    assembly_input: PromptAssemblyInput,
    ordered_blocks: list[PromptContextBlock],
    output_format: PromptAssemblyOutputFormat | str | None = None,
    prompt_output_id: str | None = None,
    validation_report_id: str | None = None,
) -> PromptAssemblyOutput:
    if not isinstance(assembly_input, PromptAssemblyInput):
        raise TypeError("assembly_input must be PromptAssemblyInput")
    _validate_context_block_list(ordered_blocks)
    validation = validate_prompt_block_order(ordered_blocks, assembly_input.assembly_input_id, validation_report_id or f"{assembly_input.assembly_input_id}:validation")
    if validation.blocked_block_ids:
        raise ValueError("cannot assemble prompt output with blocked prompt blocks")

    included_blocks = [block for block in ordered_blocks if not block.excluded]
    assembled_prompt_text = "\n\n".join(f"## {block.title}\n{block.content}" for block in included_blocks)
    token_budget_estimate = sum(block.token_budget_estimate or len(block.content.split()) for block in included_blocks)
    messages = [{"role": "system", "content": assembled_prompt_text}] if assembled_prompt_text else []

    return build_prompt_assembly_output(
        prompt_output_id or f"{assembly_input.assembly_input_id}:prompt_output",
        assembly_input.assembly_input_id,
        output_format=output_format or assembly_input.requested_output_format,
        ordered_blocks=list(ordered_blocks),
        assembled_prompt_text=assembled_prompt_text,
        assembled_messages=messages,
        validation_report_id=validation.validation_report_id,
        token_budget_estimate=token_budget_estimate,
        ready_for_v0333_session_runtime=True,
        ready_for_v0336_agent_step_runner=True,
    )


def build_prompt_profile_block_from_runtime_profile(
    profile: AgentRuntimeProfile,
    source_refs: list[PromptAssemblySourceRef] | None = None,
    profile_block_id: str | None = None,
) -> PromptProfileBlock:
    if not isinstance(profile, AgentRuntimeProfile):
        raise TypeError("profile must be AgentRuntimeProfile")
    loadout = profile.loadout
    if not isinstance(loadout, AgentRuntimeLoadout):
        raise TypeError("profile.loadout must be AgentRuntimeLoadout")
    return build_prompt_profile_block(
        profile_block_id or f"{profile.runtime_profile_id}:prompt_profile",
        profile_name=profile.display_name,
        mode_summary=str(profile.mode_kind),
        persona_summary=loadout.persona_projection.role_summary,
        constraints_summary=loadout.persona_projection.constraints_summary,
        source_refs=source_refs or [],
    )


def prompt_assembly_flags_preserve_runtime_false(flags: PromptAssemblyFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)


def prompt_output_is_not_model_invocation(output: PromptAssemblyOutput) -> bool:
    return output.ready_for_model_invocation is False and output.ready_for_execution is False and output.model_call is False and output.agent_step is False


def prompt_reference_block_preserves_no_file_access(block: PromptReferenceContextBlock) -> bool:
    return block.file_access is False and block.reference_execution_permission is False and block.path_refs_only is True


def v0332_readiness_report_is_not_runtime_ready(report: V0332ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in RUNTIME_FLAG_NAMES) and report.runtime_enablement is False

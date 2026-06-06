from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level
from chanta_core.internal_triad.skill_kinds import TriadSkillKind, normalize_triad_skill_kind


V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS = [
    "external_execution",
    "internal_tool_execution",
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
    "active_registry_mutation",
    "active_memory_mutation",
]

V0310_REQUIRED_PROHIBITED_EXTERNAL_SURFACES = [
    "external_agent_harness",
    "external_runtime",
    "provider_sdk",
    "network_endpoint",
    "credential_store",
    "command_runner",
    "browser_runtime",
    "rpa_runtime",
    "gateway_channel",
    "packet_transport",
]

OBSERVATION_OUTPUT_ARTIFACT_KINDS = [
    "observation_report",
    "capability_map",
    "observation_gap_register",
    "observation_risk_map",
    "observation_evidence_table",
]

DIGESTION_OUTPUT_ARTIFACT_KINDS = [
    "internal_skill_candidate",
    "internal_tool_contract_candidate",
    "internal_mission_candidate",
    "internal_policy_candidate",
    "internal_memory_schema_candidate",
    "internalization_plan",
]

DOMINION_OUTPUT_ARTIFACT_KINDS = [
    "dominion_target_candidate",
    "dominion_decision",
    "future_gate_item",
    "no_op_decision",
    "dominion_control_boundary",
]


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _default_output_artifact_kinds(skill_kind: TriadSkillKind) -> list[str]:
    if skill_kind is TriadSkillKind.OBSERVATION:
        return list(OBSERVATION_OUTPUT_ARTIFACT_KINDS)
    if skill_kind is TriadSkillKind.DIGESTION:
        return list(DIGESTION_OUTPUT_ARTIFACT_KINDS)
    if skill_kind is TriadSkillKind.DOMINION:
        return list(DOMINION_OUTPUT_ARTIFACT_KINDS)
    return []


@dataclass(frozen=True)
class TriadSkillBoundaryPolicy:
    boundary_policy_id: str
    skill_kind: TriadSkillKind | str
    allowed_input_artifact_kinds: list[str] = field(default_factory=list)
    allowed_output_artifact_kinds: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    prohibited_external_surfaces: list[str] = field(default_factory=lambda: list(V0310_REQUIRED_PROHIBITED_EXTERNAL_SURFACES))
    max_dominion_level: DominionLevel | int | str | None = DominionLevel.D3_SIMULATE
    requires_evidence_refs: bool = True
    requires_ocel_trace_plan: bool = True
    no_execution_guarantee: bool = True
    no_external_contact_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_policy_id", self.boundary_policy_id)
        normalize_triad_skill_kind(self.skill_kind)
        _validate_string_list("allowed_input_artifact_kinds", self.allowed_input_artifact_kinds)
        _validate_string_list("allowed_output_artifact_kinds", self.allowed_output_artifact_kinds)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("prohibited_external_surfaces", self.prohibited_external_surfaces)
        missing_actions = set(V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(self.prohibited_runtime_actions)
        if missing_actions:
            raise ValueError(f"prohibited_runtime_actions missing required no-execution actions: {sorted(missing_actions)}")
        missing_surfaces = set(V0310_REQUIRED_PROHIBITED_EXTERNAL_SURFACES) - set(self.prohibited_external_surfaces)
        if missing_surfaces:
            raise ValueError(f"prohibited_external_surfaces missing required external surfaces: {sorted(missing_surfaces)}")
        if self.max_dominion_level is not None and normalize_dominion_level(self.max_dominion_level) > DominionLevel.D3_SIMULATE:
            raise ValueError("max_dominion_level must be None or <= D3_SIMULATE in v0.31.0")
        for name in (
            "requires_evidence_refs",
            "requires_ocel_trace_plan",
            "no_execution_guarantee",
            "no_external_contact_guarantee",
            "no_registry_mutation_guarantee",
            "no_memory_mutation_guarantee",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.0")

    @property
    def grants_permission(self) -> bool:
        return False


def build_default_triad_boundary_policy(skill_kind: TriadSkillKind | str) -> TriadSkillBoundaryPolicy:
    kind = normalize_triad_skill_kind(skill_kind)
    extra_actions: list[str] = []
    if kind is TriadSkillKind.OBSERVATION:
        extra_actions = ["live_external_scan", "source_ref_fetch"]
    elif kind is TriadSkillKind.DIGESTION:
        extra_actions = [
            "active_skill_registry_mutation",
            "tool_registration",
            "mission_installation",
            "policy_activation",
            "memory_writer_activation",
        ]
    elif kind is TriadSkillKind.DOMINION:
        extra_actions = ["external_runtime_control"]
    return TriadSkillBoundaryPolicy(
        boundary_policy_id=f"triad_boundary_policy:{kind.value}:v0.31.0",
        skill_kind=kind,
        allowed_input_artifact_kinds=[
            "v0309_handoff_packet",
            "external_dominion_contract_ref",
            "external_observation_report_ref",
            "external_digestion_candidate_ref",
            "external_dominion_decision_ref",
            "ocel_trace_plan_ref",
        ],
        allowed_output_artifact_kinds=_default_output_artifact_kinds(kind),
        prohibited_runtime_actions=list(dict.fromkeys([*V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS, *extra_actions])),
        metadata={"policy_is_permission": False, "v0310_contract_only": True},
    )


def triad_boundary_preserves_no_execution(policy: TriadSkillBoundaryPolicy) -> bool:
    return (
        policy.no_execution_guarantee is True
        and policy.no_external_contact_guarantee is True
        and policy.no_registry_mutation_guarantee is True
        and policy.no_memory_mutation_guarantee is True
        and policy.grants_permission is False
        and not (set(V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(policy.prohibited_runtime_actions))
        and (policy.max_dominion_level is None or normalize_dominion_level(policy.max_dominion_level) <= DominionLevel.D3_SIMULATE)
    )


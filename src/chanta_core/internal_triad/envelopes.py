from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.internal_triad.boundaries import V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS, _require_non_blank, _validate_string_list
from chanta_core.internal_triad.skill_kinds import (
    TriadSkillKind,
    TriadSkillStatus,
    normalize_triad_skill_kind,
    normalize_triad_skill_status,
)


def _metadata_flag_true(metadata: dict[str, Any], names: set[str]) -> bool:
    return any(metadata.get(name) is True for name in names)


@dataclass(frozen=True)
class TriadSkillInputEnvelope:
    input_id: str
    source_version: str
    requested_skill_kind: TriadSkillKind | str
    source_artifact_refs: list[str]
    source_target_refs: list[str]
    source_capability_refs: list[str]
    source_candidate_refs: list[str]
    source_report_refs: list[str]
    task_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("input_id", self.input_id)
        _require_non_blank("source_version", self.source_version)
        normalize_triad_skill_kind(self.requested_skill_kind)
        _require_non_blank("task_summary", self.task_summary)
        for name in (
            "source_artifact_refs",
            "source_target_refs",
            "source_capability_refs",
            "source_candidate_refs",
            "source_report_refs",
            "evidence_refs",
            "prohibited_runtime_actions",
        ):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS) - set(self.prohibited_runtime_actions)
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing required no-execution actions: {sorted(missing)}")
        if _metadata_flag_true(self.metadata, {"execution_request", "runtime_execution", "read_only_tool_execution", "external_scan"}):
            raise ValueError("TriadSkillInputEnvelope must not imply an execution request")

    @property
    def is_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadSkillResultEnvelope:
    result_id: str
    input_id: str
    skill_id: str
    skill_kind: TriadSkillKind | str
    status: TriadSkillStatus | str
    produced_artifact_refs: list[str] = field(default_factory=list)
    produced_candidate_refs: list[str] = field(default_factory=list)
    produced_decision_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    no_op_reason: str | None = None
    ready_for_next_stage: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("result_id", self.result_id)
        _require_non_blank("input_id", self.input_id)
        _require_non_blank("skill_id", self.skill_id)
        normalize_triad_skill_kind(self.skill_kind)
        status = normalize_triad_skill_status(self.status)
        for name in (
            "produced_artifact_refs",
            "produced_candidate_refs",
            "produced_decision_refs",
            "evidence_refs",
            "blocked_reasons",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.0")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.0")
        if self.no_op_reason is not None and not isinstance(self.no_op_reason, str):
            raise TypeError("no_op_reason must be str | None")
        if status is TriadSkillStatus.NO_OP and self.no_op_reason is not None and not self.no_op_reason.strip():
            raise ValueError("no_op_reason must not be blank when supplied")
        if _metadata_flag_true(self.metadata, {"active_artifact_registration", "runtime_completion", "skill_activation", "registry_mutation"}):
            raise ValueError("TriadSkillResultEnvelope must not imply active artifact registration")

    @property
    def active_artifact_registration(self) -> bool:
        return False


def build_triad_input_envelope(
    input_id: str,
    source_version: str,
    requested_skill_kind: TriadSkillKind | str,
    task_summary: str,
    source_artifact_refs: list[str] | None = None,
    source_target_refs: list[str] | None = None,
    source_capability_refs: list[str] | None = None,
    source_candidate_refs: list[str] | None = None,
    source_report_refs: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TriadSkillInputEnvelope:
    return TriadSkillInputEnvelope(
        input_id=input_id,
        source_version=source_version,
        requested_skill_kind=requested_skill_kind,
        source_artifact_refs=list(source_artifact_refs or []),
        source_target_refs=list(source_target_refs or []),
        source_capability_refs=list(source_capability_refs or []),
        source_candidate_refs=list(source_candidate_refs or []),
        source_report_refs=list(source_report_refs or []),
        task_summary=task_summary,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_triad_result_envelope(
    result_id: str,
    input_id: str,
    skill_id: str,
    skill_kind: TriadSkillKind | str,
    status: TriadSkillStatus | str,
    produced_artifact_refs: list[str] | None = None,
    produced_candidate_refs: list[str] | None = None,
    produced_decision_refs: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    blocked_reasons: list[str] | None = None,
    no_op_reason: str | None = None,
    ready_for_next_stage: bool = False,
    metadata: dict[str, Any] | None = None,
) -> TriadSkillResultEnvelope:
    return TriadSkillResultEnvelope(
        result_id=result_id,
        input_id=input_id,
        skill_id=skill_id,
        skill_kind=skill_kind,
        status=status,
        produced_artifact_refs=list(produced_artifact_refs or []),
        produced_candidate_refs=list(produced_candidate_refs or []),
        produced_decision_refs=list(produced_decision_refs or []),
        evidence_refs=list(evidence_refs or []),
        blocked_reasons=list(blocked_reasons or []),
        no_op_reason=no_op_reason,
        ready_for_next_stage=ready_for_next_stage,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        metadata=dict(metadata or {}),
    )


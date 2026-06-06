from __future__ import annotations

from enum import StrEnum


V0310_VERSION = "v0.31.0"
V0310_TRACK = "Internal Triad Skill Foundation"
V0310_RELEASE_NAME = "v0.31.0 Internal Triad Skill Contract"


class TriadSkillKind(StrEnum):
    OBSERVATION = "observation"
    DIGESTION = "digestion"
    DOMINION = "dominion"
    UNKNOWN = "unknown"


class TriadSkillStatus(StrEnum):
    UNKNOWN = "unknown"
    CONTRACT_DEFINED = "contract_defined"
    INPUT_READY = "input_ready"
    RESULT_READY = "result_ready"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class TriadSkillExecutionMode(StrEnum):
    CONTRACT_ONLY = "contract_only"
    PLANNING_ONLY = "planning_only"
    REPORT_ONLY = "report_only"
    CANDIDATE_ONLY = "candidate_only"
    GOVERNANCE_ONLY = "governance_only"
    FUTURE_RUNTIME = "future_runtime"
    UNKNOWN = "unknown"


def normalize_triad_skill_kind(value: TriadSkillKind | str) -> TriadSkillKind:
    if isinstance(value, TriadSkillKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad skill kind must not be blank")
        return TriadSkillKind(stripped)
    raise TypeError(f"unsupported triad skill kind: {value!r}")


def normalize_triad_skill_status(value: TriadSkillStatus | str) -> TriadSkillStatus:
    if isinstance(value, TriadSkillStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad skill status must not be blank")
        return TriadSkillStatus(stripped)
    raise TypeError(f"unsupported triad skill status: {value!r}")


def normalize_triad_execution_mode(value: TriadSkillExecutionMode | str) -> TriadSkillExecutionMode:
    if isinstance(value, TriadSkillExecutionMode):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("triad skill execution mode must not be blank")
        return TriadSkillExecutionMode(stripped)
    raise TypeError(f"unsupported triad skill execution mode: {value!r}")


def triad_skill_kind_implies_execution(_: TriadSkillKind | str) -> bool:
    normalize_triad_skill_kind(_)
    return False


def triad_execution_mode_permits_execution(_: TriadSkillExecutionMode | str) -> bool:
    normalize_triad_execution_mode(_)
    return False


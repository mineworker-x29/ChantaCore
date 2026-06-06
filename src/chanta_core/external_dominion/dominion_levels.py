from __future__ import annotations

from enum import IntEnum


V0300_VERSION = "v0.30.0"
V0300_MAX_GRANTABLE_LEVEL = 3


class DominionLevel(IntEnum):
    D0_OBSERVE = 0
    D1_DESCRIBE = 1
    D2_PLAN = 2
    D3_SIMULATE = 3
    D4_EXECUTE_READ = 4
    D5_EXECUTE_WRITE_PROPOSAL = 5
    D6_EXECUTE_SANDBOX = 6
    D7_EXECUTE_NETWORK_PREVIEW = 7
    D8_DELEGATE_AGENT = 8
    D9_GATEWAY_CONTROL = 9


FUTURE_TRACK_LEVELS = frozenset(
    {
        DominionLevel.D4_EXECUTE_READ,
        DominionLevel.D5_EXECUTE_WRITE_PROPOSAL,
        DominionLevel.D6_EXECUTE_SANDBOX,
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }
)


def normalize_dominion_level(level: DominionLevel | int | str) -> DominionLevel:
    if isinstance(level, DominionLevel):
        return level
    if isinstance(level, int):
        return DominionLevel(level)
    if isinstance(level, str):
        stripped = level.strip()
        if not stripped:
            raise ValueError("dominion level must not be blank")
        if stripped in DominionLevel.__members__:
            return DominionLevel[stripped]
        return DominionLevel(int(stripped))
    raise TypeError(f"unsupported dominion level: {level!r}")


def is_execution_level(level: DominionLevel | int | str) -> bool:
    return normalize_dominion_level(level) >= DominionLevel.D4_EXECUTE_READ


def is_v030_grantable_level(level: DominionLevel | int | str) -> bool:
    return normalize_dominion_level(level) <= DominionLevel.D3_SIMULATE

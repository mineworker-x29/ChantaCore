"""Golden snapshot helpers for v0.43.9 tests."""

from chanta_core.schumpeter_tui.snapshot import create_v0439_snapshot_golden_case, execute_v0439_snapshot_golden_case


def execute_v0439_default_golden_snapshot():
    return execute_v0439_snapshot_golden_case(create_v0439_snapshot_golden_case())


__all__ = ["execute_v0439_default_golden_snapshot"]

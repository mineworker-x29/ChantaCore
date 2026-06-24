"""Fixture factories for v0.43.9 tests."""

from chanta_core.schumpeter_tui.state import create_v0439_ui_state


def create_v0439_fixture_ui_state():
    return create_v0439_ui_state()


__all__ = ["create_v0439_fixture_ui_state"]

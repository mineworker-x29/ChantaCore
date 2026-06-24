"""Status bar component."""

from __future__ import annotations

from chanta_core.schumpeter_tui.components.sidebar import V0439ComponentKind, _result
from chanta_core.schumpeter_tui.state import V0439UIState


def render_v0439_status_bar(state: V0439UIState):
    monitor = state.status_monitor
    text = (
        f"PI {monitor.pi_status} | Provider {monitor.provider_status} | Trace {monitor.trace_status} | "
        f"Evidence {monitor.evidence_status} | Safety {monitor.safety_status} | {state.version_label}"
    )
    return _result(V0439ComponentKind.STATUS_BAR.value, (text,))


__all__ = ["render_v0439_status_bar"]

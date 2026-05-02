from __future__ import annotations

from typing import Any

from chanta_core.runtime.loop.state import ProcessRunState


class ProcessRunEvaluator:
    def evaluate(self, state: ProcessRunState) -> dict[str, Any]:
        result: dict[str, Any] = {
            "success": state.status == "completed",
            "evaluation_mode": "runtime_basic",
            "observation_count": len(state.observations),
        }
        if state.status == "failed":
            result["error"] = state.last_error
            result["exception_type"] = state.state_attrs.get("exception_type")
            result["failure_stage"] = state.state_attrs.get("failure_stage")
        return result

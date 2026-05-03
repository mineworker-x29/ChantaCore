from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from chanta_core.runtime.loop.observation import ProcessObservation
from chanta_core.runtime.loop.state import ProcessRunState


@dataclass(frozen=True)
class ProcessRunPolicy:
    max_iterations: int = 1
    stop_on_text_response: bool = True
    raise_on_failure: bool = True
    include_pig_context: bool = False
    pig_context_scope: Literal["recent", "process_instance", "session"] = "recent"
    use_decision_service: bool = True
    use_pig_guidance: bool = False
    guidance_scope: Literal["recent", "process_instance", "session"] = "recent"

    def should_continue(self, state: ProcessRunState) -> bool:
        return state.status == "running" and state.iteration < state.max_iterations

    def should_stop_after_observation(
        self,
        state: ProcessRunState,
        observation: ProcessObservation,
    ) -> bool:
        if state.iteration >= state.max_iterations:
            return True
        if self.stop_on_text_response and observation.success and observation.output_text:
            return True
        return False

    @property
    def fail_on_exception(self) -> bool:
        return self.raise_on_failure

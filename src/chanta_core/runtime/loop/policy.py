from __future__ import annotations

from dataclasses import dataclass

from chanta_core.runtime.loop.observation import ProcessObservation
from chanta_core.runtime.loop.state import ProcessRunState


@dataclass(frozen=True)
class ProcessRunPolicy:
    max_iterations: int = 1
    stop_on_text_response: bool = True
    fail_on_exception: bool = True

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

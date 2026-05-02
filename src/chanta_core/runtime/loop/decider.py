from __future__ import annotations

from chanta_core.runtime.loop.state import ProcessRunState


class ProcessActivityDecider:
    def decide_next_activity(self, state: ProcessRunState) -> str:
        if state.iteration == 0:
            return "execute_skill"
        return "complete_process_instance"

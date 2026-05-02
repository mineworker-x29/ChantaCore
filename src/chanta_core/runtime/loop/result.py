from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from chanta_core.runtime.loop.observation import ProcessObservation

ProcessRunResultStatus = Literal["completed", "failed"]


@dataclass(frozen=True)
class ProcessRunResult:
    process_instance_id: str
    session_id: str
    agent_id: str
    status: ProcessRunResultStatus
    response_text: str
    observations: list[ProcessObservation]
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "process_instance_id": self.process_instance_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "status": self.status,
            "response_text": self.response_text,
            "observations": [item.to_dict() for item in self.observations],
            "result_attrs": self.result_attrs,
        }

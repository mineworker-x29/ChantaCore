from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ProcessRunStatus = Literal["created", "running", "completed", "failed"]


@dataclass
class ProcessRunState:
    process_instance_id: str
    session_id: str
    agent_id: str
    status: ProcessRunStatus
    iteration: int
    max_iterations: int
    current_activity: str | None
    selected_skill_id: str | None
    observations: list[dict[str, Any]] = field(default_factory=list)
    last_error: str | None = None
    state_attrs: dict[str, Any] = field(default_factory=dict)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def create_session_id() -> str:
    return str(uuid4())


@dataclass(frozen=True)
class ExecutionContext:
    session_id: str
    agent_id: str
    user_input: str
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        agent_id: str,
        user_input: str,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ExecutionContext":
        return cls(
            session_id=session_id or create_session_id(),
            agent_id=agent_id,
            user_input=user_input,
            created_at=utc_now_iso(),
            metadata=metadata or {},
        )

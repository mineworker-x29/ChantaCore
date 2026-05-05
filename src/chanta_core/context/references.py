from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


REFERENCE_TYPES = {
    "context_block",
    "ocel_event",
    "ocel_object",
    "pi_artifact",
    "pig_report",
    "tool_result",
    "workspace_file",
    "repo_match",
    "worker_job",
    "scheduler_schedule",
    "edit_proposal",
    "patch_application",
    "other",
}


def new_context_reference_id() -> str:
    return f"context_ref:{uuid4()}"


@dataclass(frozen=True)
class ContextReference:
    ref_id: str
    ref_type: str
    source: str
    title: str
    block_id: str | None = None
    object_id: str | None = None
    event_id: str | None = None
    artifact_id: str | None = None
    path: str | None = None
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_id": self.ref_id,
            "ref_type": self.ref_type,
            "source": self.source,
            "title": self.title,
            "block_id": self.block_id,
            "object_id": self.object_id,
            "event_id": self.event_id,
            "artifact_id": self.artifact_id,
            "path": self.path,
            "attrs": self.attrs,
        }

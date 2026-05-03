from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def new_patch_application_id() -> str:
    return f"patch_application:{uuid4()}"


@dataclass(frozen=True)
class PatchApplication:
    patch_application_id: str
    proposal_id: str
    approval_id: str
    target_path: str
    status: str
    applied_at: str | None
    backup_path: str | None
    original_size_bytes: int | None
    new_size_bytes: int | None
    diff_preview: str | None
    error: str | None
    patch_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch_application_id": self.patch_application_id,
            "proposal_id": self.proposal_id,
            "approval_id": self.approval_id,
            "target_path": self.target_path,
            "status": self.status,
            "applied_at": self.applied_at,
            "backup_path": self.backup_path,
            "original_size_bytes": self.original_size_bytes,
            "new_size_bytes": self.new_size_bytes,
            "diff_preview": self.diff_preview,
            "error": self.error,
            "patch_attrs": self.patch_attrs,
        }

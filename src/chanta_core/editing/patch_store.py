from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from chanta_core.editing.patch import PatchApplication


class PatchApplicationStore:
    def __init__(self, path: str | Path = "data/editing/patch_applications.jsonl") -> None:
        self.path = Path(path)

    def append(self, application: PatchApplication) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(application.to_dict(), ensure_ascii=False, sort_keys=True))
            handle.write("\n")

    def load_all(self) -> list[PatchApplication]:
        if not self.path.exists():
            return []
        applications: list[PatchApplication] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    loaded = json.loads(raw)
                    if isinstance(loaded, dict):
                        applications.append(_application_from_dict(loaded))
                except Exception as error:
                    warnings.warn(
                        f"Skipping invalid patch application JSONL row {line_number}: {error}",
                        RuntimeWarning,
                        stacklevel=2,
                    )
        return applications

    def recent(self, limit: int = 20) -> list[PatchApplication]:
        return self.load_all()[-limit:]

    def get(self, patch_application_id: str) -> PatchApplication | None:
        for application in self.load_all():
            if application.patch_application_id == patch_application_id:
                return application
        return None

    def find_by_proposal_id(self, proposal_id: str) -> list[PatchApplication]:
        return [
            application
            for application in self.load_all()
            if application.proposal_id == proposal_id
        ]

    def find_by_target_path(self, target_path: str) -> list[PatchApplication]:
        return [
            application
            for application in self.load_all()
            if application.target_path == target_path
        ]


def _application_from_dict(data: dict[str, Any]) -> PatchApplication:
    return PatchApplication(
        patch_application_id=str(data["patch_application_id"]),
        proposal_id=str(data["proposal_id"]),
        approval_id=str(data["approval_id"]),
        target_path=str(data["target_path"]),
        status=str(data["status"]),
        applied_at=data.get("applied_at"),
        backup_path=data.get("backup_path"),
        original_size_bytes=data.get("original_size_bytes"),
        new_size_bytes=data.get("new_size_bytes"),
        diff_preview=data.get("diff_preview"),
        error=data.get("error"),
        patch_attrs=dict(data.get("patch_attrs") or {}),
    )

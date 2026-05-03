from __future__ import annotations

from pathlib import Path

from chanta_core.ocel.factory import short_hash
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import WorkspaceConfig


class PatchBackupService:
    def __init__(self, workspace_config: WorkspaceConfig) -> None:
        self.workspace_config = workspace_config

    def create_backup(
        self,
        target_path: str | Path,
        original_text: str,
        proposal_id: str,
    ) -> str:
        safe_proposal = _safe_component(proposal_id)
        target = Path(target_path)
        timestamp_hash = short_hash(f"{utc_now_iso()}:{target.as_posix()}:{proposal_id}")
        backup_dir = Path("data/editing/backups") / safe_proposal
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_name = f"{_safe_component(target.name or 'target')}.{timestamp_hash}.bak"
        backup_path = backup_dir / backup_name
        backup_path.write_text(original_text, encoding="utf-8")
        return str(backup_path)


def _safe_component(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)

from __future__ import annotations

import shutil
from pathlib import Path

from chanta_core.ocel.store import OCELStore


class OCELImporter:
    """Safe placeholder importer; full OCEL conformance checks are future work."""

    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def import_sqlite(self, source_path: str | Path) -> None:
        source = Path(source_path)
        if not source.is_file():
            raise FileNotFoundError(source)
        self.store.db_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, self.store.db_path)

from __future__ import annotations

import json
from pathlib import Path

from chanta_core.pig.artifacts import PIArtifact


class PIArtifactStore:
    def __init__(
        self,
        path: str | Path = "data/pig/pi_artifacts.jsonl",
    ) -> None:
        self.path = Path(path)
        self.warnings: list[str] = []

    def append(self, artifact: PIArtifact) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(artifact.to_dict(), ensure_ascii=False, sort_keys=True))
            file.write("\n")

    def load_all(self) -> list[PIArtifact]:
        self.warnings = []
        if not self.path.exists():
            return []
        artifacts: list[PIArtifact] = []
        with self.path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                raw_line = line.strip()
                if not raw_line:
                    continue
                try:
                    loaded = json.loads(raw_line)
                    if not isinstance(loaded, dict):
                        raise ValueError("JSONL row is not an object")
                    artifacts.append(PIArtifact.from_dict(loaded))
                except Exception as error:
                    self.warnings.append(f"Skipped invalid JSONL row {line_number}: {error}")
        return artifacts

    def find_by_scope(self, scope_key: str, scope_value: str) -> list[PIArtifact]:
        return [
            artifact
            for artifact in self.load_all()
            if str(artifact.scope.get(scope_key)) == scope_value
        ]

    def recent(self, limit: int = 20) -> list[PIArtifact]:
        if limit <= 0:
            return []
        return self.load_all()[-limit:]

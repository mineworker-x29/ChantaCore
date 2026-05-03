from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.artifacts import PIArtifact
from chanta_core.utility.time import utc_now_iso


class HumanPIAssimilator:
    def __init__(self, store: PIArtifactStore | None = None) -> None:
        self.store = store or PIArtifactStore()

    def assimilate_text(
        self,
        text: str,
        *,
        source_type: str = "human_pi",
        artifact_type: str = "process_note",
        title: str | None = None,
        scope: dict[str, Any] | None = None,
        evidence_refs: list[dict[str, Any]] | None = None,
        object_refs: list[dict[str, Any]] | None = None,
        confidence: float = 0.5,
        artifact_attrs: dict[str, Any] | None = None,
    ) -> PIArtifact:
        content = text.strip()
        if not content:
            raise ValueError("Human PI text must not be empty")
        artifact = PIArtifact(
            artifact_id=f"pi_artifact:{uuid4()}",
            artifact_type=artifact_type,
            source_type=source_type,
            title=title or self._title_from_text(content),
            content=content,
            scope=dict(scope or {}),
            evidence_refs=list(evidence_refs or []),
            object_refs=list(object_refs or []),
            confidence=float(confidence),
            status="active",
            created_at=utc_now_iso(),
            artifact_attrs={
                **dict(artifact_attrs or {}),
                "advisory": True,
                "hard_policy": False,
            },
        )
        self.store.append(artifact)
        return artifact

    def assimilate_many(self, items: list[dict[str, Any]]) -> list[PIArtifact]:
        artifacts: list[PIArtifact] = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("assimilate_many items must be dictionaries")
            text = str(item.get("text") or item.get("content") or "")
            artifacts.append(
                self.assimilate_text(
                    text,
                    source_type=str(item.get("source_type") or "human_pi"),
                    artifact_type=str(item.get("artifact_type") or "process_note"),
                    title=item.get("title"),
                    scope=item.get("scope"),
                    evidence_refs=item.get("evidence_refs"),
                    object_refs=item.get("object_refs"),
                    confidence=float(item.get("confidence", 0.5)),
                    artifact_attrs=item.get("artifact_attrs"),
                )
            )
        return artifacts

    @staticmethod
    def _title_from_text(text: str, max_chars: int = 72) -> str:
        first_line = " ".join(text.split())
        if len(first_line) <= max_chars:
            return first_line
        return f"{first_line[: max_chars - 3].rstrip()}..."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.context.block import ContextBlock, make_context_block
from chanta_core.context.references import ContextReference
from chanta_core.utility.time import utc_now_iso


RAW_PRESERVED_MESSAGE = (
    "Raw content preserved in source stores; not included in prompt context."
)


@dataclass(frozen=True)
class CollapsedContextManifest:
    manifest_id: str
    collapsed_block_count: int
    collapsed_by_type: dict[str, int]
    references: list[ContextReference]
    created_at: str
    manifest_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "collapsed_block_count": self.collapsed_block_count,
            "collapsed_by_type": self.collapsed_by_type,
            "references": [reference.to_dict() for reference in self.references],
            "created_at": self.created_at,
            "manifest_attrs": self.manifest_attrs,
        }

    def to_context_block(self, priority: int | None = None) -> ContextBlock:
        lines = [
            f"Collapsed block count: {self.collapsed_block_count}",
            "Collapsed by type:",
        ]
        for block_type in sorted(self.collapsed_by_type):
            lines.append(f"- {block_type}: {self.collapsed_by_type[block_type]}")
        lines.append("Top references:")
        for reference in self.references[:10]:
            pointer_key = "ref_id"
            pointer = reference.ref_id
            for key, value in [
                ("artifact_id", reference.artifact_id),
                ("event_id", reference.event_id),
                ("object_id", reference.object_id),
                ("path", reference.path),
                ("block_id", reference.block_id),
            ]:
                if value:
                    pointer_key = key
                    pointer = value
                    break
            lines.append(
                f"- {reference.ref_type}: {reference.title}"
                f" (source={reference.source}, ref_id={reference.ref_id}, {pointer_key}={pointer})"
            )
        if len(self.references) > 10:
            lines.append(f"- ... {len(self.references) - 10} more reference(s)")
        lines.append(RAW_PRESERVED_MESSAGE)
        return make_context_block(
            block_type="collapsed_context",
            title="Collapsed Context References",
            content="\n".join(lines),
            priority=priority if priority is not None else 15,
            source="context_collapse",
            refs=[reference.to_dict() for reference in self.references],
            block_attrs={
                "manifest_id": self.manifest_id,
                "collapsed_block_count": self.collapsed_block_count,
                "collapsed_by_type": dict(self.collapsed_by_type),
                "created_at": self.created_at,
            },
        )


def new_collapsed_context_manifest(
    *,
    collapsed_block_count: int,
    collapsed_by_type: dict[str, int],
    references: list[ContextReference],
    manifest_attrs: dict[str, Any] | None = None,
) -> CollapsedContextManifest:
    from uuid import uuid4

    return CollapsedContextManifest(
        manifest_id=f"collapsed_context_manifest:{uuid4()}",
        collapsed_block_count=collapsed_block_count,
        collapsed_by_type=dict(collapsed_by_type),
        references=list(references),
        created_at=utc_now_iso(),
        manifest_attrs=dict(manifest_attrs or {}),
    )

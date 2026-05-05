from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chanta_core.context.block import ContextBlock


@dataclass(frozen=True)
class ContextRenderPolicy:
    include_refs: bool = True
    max_refs_per_block: int = 5
    include_block_metadata: bool = True


class ContextRenderer:
    def __init__(self, policy: ContextRenderPolicy | None = None) -> None:
        self.policy = policy or ContextRenderPolicy()

    def render_block(self, block: ContextBlock) -> str:
        parts = [f"[{block.block_type}] {block.title}"]
        metadata = self._render_metadata(block)
        if metadata:
            parts.append(metadata)
        parts.append(block.content)
        if block.was_truncated:
            parts.append("(content compacted/truncated by context pipeline)")
        refs_text = self._render_refs(block.refs) if self.policy.include_refs else ""
        if refs_text:
            parts.append(refs_text)
        return "\n".join(part for part in parts if part)

    def render_blocks(self, blocks: list[ContextBlock]) -> str:
        return "\n\n".join(self.render_block(block) for block in blocks)

    def _render_refs(self, refs: list[dict[str, Any]]) -> str:
        if not refs:
            return ""
        lines = ["Refs:"]
        max_refs = max(0, self.policy.max_refs_per_block)
        for ref in refs[:max_refs]:
            visible = []
            preferred_keys = ["ref_type", "ref_id", "event_id", "artifact_id", "report_id"]
            keys = preferred_keys + [
                key for key in sorted(ref) if key not in preferred_keys
            ]
            for key in keys:
                if key not in ref:
                    continue
                value = ref[key]
                if value is not None:
                    rendered = str(value)
                    if len(rendered) > 80:
                        rendered = f"{rendered[:77]}..."
                    visible.append(f"{key}={rendered}")
                if len(visible) >= 4:
                    break
            lines.append(f"- {', '.join(visible) if visible else 'none'}")
        if len(refs) > max_refs:
            lines.append(f"- ... {len(refs) - max_refs} more ref(s)")
        return "\n".join(lines)

    def _render_metadata(self, block: ContextBlock) -> str:
        if not self.policy.include_block_metadata:
            return ""
        values = [
            f"source={block.source}",
            f"priority={block.priority}",
            f"truncated={block.was_truncated}",
            f"refs={len(block.refs)}",
        ]
        if block.block_attrs.get("microcompacted"):
            values.append("microcompacted=True")
        return f"metadata: {', '.join(values)}"

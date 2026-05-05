from __future__ import annotations

from typing import Any

from chanta_core.context.block import ContextBlock


class ContextRenderer:
    def render_block(self, block: ContextBlock) -> str:
        parts = [f"[{block.block_type}] {block.title}", block.content]
        if block.was_truncated:
            parts.append("(content truncated by context compaction)")
        refs_text = self._render_refs(block.refs)
        if refs_text:
            parts.append(refs_text)
        return "\n".join(part for part in parts if part)

    def render_blocks(self, blocks: list[ContextBlock]) -> str:
        return "\n\n".join(self.render_block(block) for block in blocks)

    def _render_refs(self, refs: list[dict[str, Any]]) -> str:
        if not refs:
            return ""
        lines = ["Refs:"]
        for ref in refs[:5]:
            visible = []
            for key in sorted(ref):
                value = ref[key]
                if value is not None:
                    visible.append(f"{key}={value}")
                if len(visible) >= 4:
                    break
            lines.append(f"- {', '.join(visible) if visible else 'none'}")
        if len(refs) > 5:
            lines.append(f"- ... {len(refs) - 5} more ref(s)")
        return "\n".join(lines)

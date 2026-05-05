from __future__ import annotations

from chanta_core.context.block import (
    ContextBlock,
    replace_context_block_content,
)
from chanta_core.context.budget import ContextBudget
from chanta_core.context.layers.base import block_char_limit
from chanta_core.context.microcompact import (
    compact_activity_sequence,
    compact_json_like_text,
    compact_lines,
    compact_long_line,
    compact_mapping,
    compact_report_text,
)
from chanta_core.context.microcompact_policy import MicrocompactPolicy
from chanta_core.context.result import ContextCompactionLayerResult


class MicrocompactLayer:
    name = "MicrocompactLayer"

    def __init__(
        self,
        policy: MicrocompactPolicy | None = None,
        *,
        first_lines: int = 20,
        last_lines: int = 5,
    ) -> None:
        self.policy = policy or MicrocompactPolicy()
        self.first_lines = first_lines
        self.last_lines = last_lines

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        self.policy.validate()
        next_blocks: list[ContextBlock] = []
        changed_ids: list[str] = []
        truncated_ids: list[str] = []
        block_type_counts: dict[str, int] = {}
        for block in blocks:
            compacted = self._microcompact_content(block.content, block, budget)
            if compacted != block.content:
                shortened = len(compacted) < len(block.content)
                next_blocks.append(
                    replace_context_block_content(
                        block,
                        compacted,
                        was_truncated=block.was_truncated or shortened,
                        block_attrs={"microcompacted": True},
                    )
                )
                changed_ids.append(block.block_id)
                if shortened:
                    truncated_ids.append(block.block_id)
                block_type_counts[block.block_type] = (
                    block_type_counts.get(block.block_type, 0) + 1
                )
            else:
                next_blocks.append(block)
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=next_blocks,
            changed=bool(changed_ids),
            truncated_block_ids=truncated_ids,
            result_attrs={
                "microcompacted_block_ids": changed_ids,
                "microcompacted_block_count": len(changed_ids),
                "block_type_counts": block_type_counts,
                "policy": self.policy.to_dict(),
            },
        )

    def _microcompact_content(
        self,
        content: str,
        block: ContextBlock,
        budget: ContextBudget,
    ) -> str:
        if block.block_type == "pig_context":
            compacted = self._compact_pig_context(content, block)
        elif block.block_type == "pig_report":
            compacted, _ = compact_report_text(
                content,
                max_chars=self.policy.max_report_chars,
            )
        elif block.block_type == "tool_result":
            compacted = self._compact_tool_result(content)
        elif block.block_type in {"conformance", "decision"}:
            compacted = self._compact_structured_diagnostic(content, block)
        elif block.block_type in {"workspace", "repo", "worker", "scheduler"}:
            compacted = self._compact_listing(content)
        elif block.block_type == "artifact":
            compacted = self._compact_artifact(content, block)
        else:
            compacted = self._compact_default(content)

        limit = block_char_limit(block, budget)
        if len(compacted) > limit:
            compacted, _ = compact_long_line(
                compacted,
                max_chars=limit,
                marker="...[microcompact block char cap]...",
            )
        return compacted

    def _compact_pig_context(self, content: str, block: ContextBlock) -> str:
        parts: list[str] = []
        activity_sequence = block.block_attrs.get("activity_sequence")
        if isinstance(activity_sequence, list) and activity_sequence:
            sequence_text, _ = compact_activity_sequence(
                [str(item) for item in activity_sequence],
                max_items=self.policy.max_activity_items,
            )
            parts.append(f"Activity sequence: {sequence_text}")
        for key in [
            "scope",
            "conformance_status",
            "diagnostic_count",
            "recommendation_count",
            "pi_artifact_count",
        ]:
            if key in block.block_attrs:
                parts.append(f"{key}: {block.block_attrs[key]}")
        compacted, _ = compact_report_text(
            content,
            max_chars=self.policy.max_report_chars,
        )
        parts.append(compacted)
        return "\n".join(part for part in parts if part).strip()

    def _compact_tool_result(self, content: str) -> str:
        stripped = content.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            compacted, _ = compact_json_like_text(
                content,
                max_chars=self.policy.max_json_chars,
            )
            return compacted
        return self._compact_default(content)

    def _compact_structured_diagnostic(
        self,
        content: str,
        block: ContextBlock,
    ) -> str:
        parts: list[str] = []
        for key in [
            "status",
            "issue_count",
            "selected_skill_id",
            "decision_mode",
            "applied_guidance_ids",
        ]:
            if key in block.block_attrs:
                value = block.block_attrs[key]
                if isinstance(value, dict):
                    value, _ = compact_mapping(value, max_items=self.policy.max_mapping_items)
                parts.append(f"{key}: {value}")
        parts.append(self._compact_default(content))
        return "\n".join(part for part in parts if part).strip()

    def _compact_listing(self, content: str) -> str:
        compacted = self._compact_default(content)
        compacted, _ = compact_lines(
            compacted,
            max_lines=self.policy.max_lines,
            head_lines=min(25, self.policy.max_lines),
            tail_lines=min(10, self.policy.max_lines),
        )
        return compacted

    def _compact_artifact(self, content: str, block: ContextBlock) -> str:
        parts: list[str] = []
        for key in ["title", "source", "source_type", "confidence", "artifact_type"]:
            if key in block.block_attrs:
                parts.append(f"{key}: {block.block_attrs[key]}")
        parts.append(self._compact_default(content))
        return "\n".join(part for part in parts if part).strip()

    def _compact_default(self, content: str) -> str:
        lines: list[str] = []
        previous_blank = False
        for line in content.splitlines():
            next_line = line.rstrip()
            next_line, _ = compact_long_line(
                next_line,
                max_chars=self.policy.max_line_chars,
                marker="...[line truncated by MicrocompactLayer]...",
            )
            is_blank = next_line == ""
            if is_blank and previous_blank:
                continue
            lines.append(next_line)
            previous_blank = is_blank
        compacted = "\n".join(lines).strip()
        compacted, _ = compact_lines(
            compacted,
            max_lines=self.policy.max_lines,
            head_lines=self.first_lines,
            tail_lines=self.last_lines,
            marker="...[middle lines omitted by MicrocompactLayer]...",
        )
        return compacted

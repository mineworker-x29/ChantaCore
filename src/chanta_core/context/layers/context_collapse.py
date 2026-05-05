from __future__ import annotations

from typing import Any

from chanta_core.context.block import (
    ContextBlock,
    replace_context_block_content,
    truncate_text,
)
from chanta_core.context.budget import ContextBudget
from chanta_core.context.collapse import (
    CollapsedContextManifest,
    RAW_PRESERVED_MESSAGE,
    new_collapsed_context_manifest,
)
from chanta_core.context.collapse_policy import ContextCollapsePolicy
from chanta_core.context.layers.base import is_protected, total_chars
from chanta_core.context.references import ContextReference, new_context_reference_id
from chanta_core.context.result import ContextCompactionLayerResult


class ContextCollapseLayer:
    name = "ContextCollapseLayer"

    def __init__(self, policy: ContextCollapsePolicy | None = None) -> None:
        self.policy = policy or ContextCollapsePolicy()

    def apply(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
    ) -> ContextCompactionLayerResult:
        return self.apply_with_projected_blocks(
            blocks,
            budget,
            projected_blocks=[],
        )

    def apply_with_projected_blocks(
        self,
        blocks: list[ContextBlock],
        budget: ContextBudget,
        *,
        projected_blocks: list[ContextBlock],
    ) -> ContextCompactionLayerResult:
        self.policy.validate()
        if not self.policy.enabled:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=list(blocks),
                changed=False,
                result_attrs={"disabled": True},
            )

        usable = budget.usable_chars()
        current_blocks = list(blocks)
        projected_blocks = self._deterministic_projected_blocks(projected_blocks)
        if total_chars(current_blocks) <= usable and not projected_blocks:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=current_blocks,
                changed=False,
                result_attrs={"disabled": False},
            )

        collapse_candidates = self._collapse_candidates(current_blocks)
        collapsed: list[ContextBlock] = []
        keep_ids = {block.block_id for block in current_blocks}
        remaining = list(current_blocks)

        if total_chars(remaining) > usable:
            for _, block in collapse_candidates:
                collapsed.append(block)
                keep_ids.remove(block.block_id)
                remaining = [item for item in current_blocks if item.block_id in keep_ids]
                projected_candidate = self._dedupe_blocks(projected_blocks + collapsed)
                projected_manifest = self._make_manifest(projected_candidate)
                projected_block = self._fit_collapse_block(
                    projected_manifest.to_context_block(
                        priority=self.policy.collapse_block_priority
                    )
                )
                if total_chars(remaining) + projected_block.char_length <= usable:
                    break

        all_collapsed = self._dedupe_blocks(projected_blocks + collapsed)
        if len(all_collapsed) < self.policy.min_blocks_to_collapse and not collapsed:
            if total_chars(remaining) <= usable:
                return ContextCompactionLayerResult(
                    layer_name=self.name,
                    blocks=remaining,
                    changed=False,
                    result_attrs={"disabled": False, "collapsed_block_count": 0},
                )

        if not all_collapsed:
            return ContextCompactionLayerResult(
                layer_name=self.name,
                blocks=remaining,
                changed=False,
                warnings=[
                    "ContextCollapseLayer could not collapse context; only protected blocks remain."
                ],
                result_attrs={"disabled": False, "collapsed_block_count": 0},
            )

        manifest = self._make_manifest(all_collapsed)
        collapse_block = manifest.to_context_block(
            priority=self.policy.collapse_block_priority
        )
        collapse_block = self._fit_collapse_block(collapse_block)
        available_chars = max(0, usable - total_chars(remaining))
        collapse_block = self._fit_collapse_block_to_available(
            collapse_block,
            available_chars,
        )
        next_blocks = remaining + [collapse_block]
        warnings = [
            f"ContextCollapseLayer projected {len(all_collapsed)} collapsed block(s)."
        ]
        created = [collapse_block.block_id]
        if total_chars(next_blocks) > usable:
            next_blocks = remaining
            created = []
            warnings.append("Collapsed context manifest did not fit and was dropped.")

        if total_chars(next_blocks) > usable:
            warnings.append(
                "Context remains over budget after ContextCollapseLayer; protected blocks were kept."
            )
        return ContextCompactionLayerResult(
            layer_name=self.name,
            blocks=next_blocks,
            changed=bool(all_collapsed or collapsed),
            dropped_block_ids=[block.block_id for block in all_collapsed],
            created_block_ids=created,
            warnings=warnings,
            result_attrs={
                "collapsed_block_count": len(all_collapsed),
                "collapsed_by_type": dict(manifest.collapsed_by_type),
                "manifest_id": manifest.manifest_id,
                "reference_count": len(manifest.references),
                "disabled": False,
            },
        )

    def _collapse_candidates(
        self,
        blocks: list[ContextBlock],
    ) -> list[tuple[int, ContextBlock]]:
        candidates = [
            (index, block)
            for index, block in enumerate(blocks)
            if not is_protected(block) and block.block_type != "collapsed_context"
        ]
        candidates.sort(key=lambda item: self._candidate_sort_key(item[0], item[1]))
        return candidates

    def _candidate_sort_key(self, index: int, block: ContextBlock) -> tuple[int, int, str, int]:
        return (
            self._collapse_group(block),
            block.priority,
            str(block.block_attrs.get("created_at") or ""),
            index,
        )

    @staticmethod
    def _collapse_group(block: ContextBlock) -> int:
        if block.block_type in {
            "tool_result",
            "pig_report",
            "artifact",
            "workspace",
            "repo",
            "worker",
            "scheduler",
            "edit",
            "patch",
        }:
            return 0
        if block.block_type == "history" or block.block_attrs.get("is_history"):
            return 1
        if block.block_type in {"decision", "conformance"}:
            return 2
        return 3

    def _make_manifest(self, blocks: list[ContextBlock]) -> CollapsedContextManifest:
        collapsed_by_type: dict[str, int] = {}
        for block in blocks:
            collapsed_by_type[block.block_type] = (
                collapsed_by_type.get(block.block_type, 0) + 1
            )
        references = [self._reference_from_block(block) for block in blocks]
        references = references[: self.policy.max_references]
        return new_collapsed_context_manifest(
            collapsed_block_count=len(blocks),
            collapsed_by_type=collapsed_by_type,
            references=references,
            manifest_attrs={"policy": self.policy.to_dict()},
        )

    def _reference_from_block(self, block: ContextBlock) -> ContextReference:
        ref_type = self._reference_type(block)
        attrs: dict[str, Any] = {
            "block_type": block.block_type,
            "priority": block.priority,
            "source": block.source,
            "ref_count": len(block.refs),
        }
        for key in [
            "created_at",
            "session_id",
            "process_instance_id",
            "tool_id",
            "operation",
            "status",
        ]:
            if block.block_attrs.get(key) is not None:
                attrs[key] = block.block_attrs[key]
        for ref in block.refs:
            for key in ["event_id", "object_id", "artifact_id", "path", "report_id"]:
                if ref.get(key) is not None and key not in attrs:
                    attrs[key] = ref[key]
        return ContextReference(
            ref_id=new_context_reference_id(),
            ref_type=ref_type,
            source=block.source,
            title=block.title,
            block_id=block.block_id,
            object_id=self._first_value(block, "object_id"),
            event_id=self._first_value(block, "event_id"),
            artifact_id=self._first_value(block, "artifact_id"),
            path=self._first_value(block, "path"),
            attrs=attrs,
        )

    @staticmethod
    def _reference_type(block: ContextBlock) -> str:
        if block.block_type == "tool_result":
            return "tool_result"
        if block.block_type == "pig_report":
            return "pig_report"
        if block.block_type == "artifact":
            return "pi_artifact"
        if block.block_type == "workspace":
            return "workspace_file"
        if block.block_type == "repo":
            return "repo_match"
        if block.block_type == "worker":
            return "worker_job"
        if block.block_type == "scheduler":
            return "scheduler_schedule"
        if block.block_type == "edit":
            return "edit_proposal"
        if block.block_type == "patch":
            return "patch_application"
        return "context_block"

    @staticmethod
    def _first_value(block: ContextBlock, key: str) -> str | None:
        if block.block_attrs.get(key) is not None:
            return str(block.block_attrs[key])
        for ref in block.refs:
            if ref.get(key) is not None:
                return str(ref[key])
        return None

    @staticmethod
    def _dedupe_blocks(blocks: list[ContextBlock]) -> list[ContextBlock]:
        seen: set[str] = set()
        result: list[ContextBlock] = []
        for block in blocks:
            if block.block_id in seen:
                continue
            seen.add(block.block_id)
            result.append(block)
        return result

    @staticmethod
    def _deterministic_projected_blocks(
        blocks: list[ContextBlock],
    ) -> list[ContextBlock]:
        return sorted(
            blocks,
            key=lambda block: (
                block.block_type,
                block.priority,
                str(block.block_attrs.get("created_at") or ""),
                block.block_id,
            ),
        )

    def _fit_collapse_block(self, block: ContextBlock) -> ContextBlock:
        if block.char_length <= self.policy.max_collapsed_block_chars:
            return block
        content, changed = truncate_text(
            block.content,
            self.policy.max_collapsed_block_chars,
            "\n...[collapsed context manifest truncated]...",
        )
        if not changed:
            return block
        return replace_context_block_content(
            block,
            content,
            was_truncated=True,
            block_attrs={"collapse_manifest_truncated": True},
        )

    @staticmethod
    def _fit_collapse_block_to_available(
        block: ContextBlock,
        available_chars: int,
    ) -> ContextBlock:
        if available_chars <= 0 or block.char_length <= available_chars:
            return block
        marker = "\n...[collapsed context manifest truncated to budget]...\n"
        suffix = RAW_PRESERVED_MESSAGE
        if available_chars > len(marker) + len(suffix):
            head_chars = available_chars - len(marker) - len(suffix)
            content = f"{block.content[:head_chars]}{marker}{suffix}"
            changed = True
        else:
            content, changed = truncate_text(
                block.content,
                available_chars,
                "\n...[collapsed context manifest truncated to budget]...",
            )
        if not changed:
            return block
        return replace_context_block_content(
            block,
            content,
            was_truncated=True,
            block_attrs={"collapse_manifest_truncated": True},
        )

from __future__ import annotations

from typing import Any

from chanta_core.context.block import (
    ContextBlock,
    from_pig_context,
    from_process_report,
    from_tool_result,
    make_context_block,
)


def context_block_from_pig_context(pig_context: Any, priority: int = 70) -> ContextBlock:
    return from_pig_context(pig_context, priority=priority)


def context_block_from_process_report(report: Any, priority: int = 50) -> ContextBlock:
    return from_process_report(report, priority=priority)


def context_block_from_tool_result(tool_result: Any, priority: int = 40) -> ContextBlock:
    return from_tool_result(tool_result, priority=priority)


def context_block_from_pi_artifact(artifact: Any, priority: int = 45) -> ContextBlock:
    refs = [
        {
            "ref_type": "pi_artifact",
            "artifact_id": getattr(artifact, "artifact_id", None),
        }
    ]
    refs.extend(list(getattr(artifact, "evidence_refs", None) or [])[:5])
    return make_context_block(
        block_type="artifact",
        title=str(getattr(artifact, "title", None) or "PI Artifact"),
        content=str(getattr(artifact, "content", "") or ""),
        priority=priority,
        source=str(getattr(artifact, "source_type", None) or "pi_artifact"),
        refs=refs,
        block_attrs={
            "artifact_id": getattr(artifact, "artifact_id", None),
            "artifact_type": getattr(artifact, "artifact_type", None),
            "title": getattr(artifact, "title", None),
            "source_type": getattr(artifact, "source_type", None),
            "confidence": getattr(artifact, "confidence", None),
            "status": getattr(artifact, "status", None),
            "created_at": getattr(artifact, "created_at", None),
        },
    )

KNOWN_LIFECYCLE_STAGES = {
    "session_start",
    "session_close",
    "turn_start",
    "turn_complete",
    "pre_process_run",
    "post_process_run",
    "pre_decision",
    "post_decision",
    "pre_skill_execution",
    "post_skill_execution",
    "pre_tool_dispatch",
    "post_tool_dispatch",
    "pre_context_compaction",
    "post_context_compaction",
    "pre_materialized_view_refresh",
    "post_materialized_view_refresh",
    "on_error",
    "other",
}


def normalize_lifecycle_stage(stage: str | None) -> str:
    normalized = (stage or "").strip().lower()
    if not normalized:
        return "other"
    normalized = normalized.replace("-", "_").replace(" ", "_")
    return normalized if normalized in KNOWN_LIFECYCLE_STAGES else "other"


def is_known_lifecycle_stage(stage: str) -> bool:
    return normalize_lifecycle_stage(stage) == stage.strip().lower().replace("-", "_").replace(" ", "_")


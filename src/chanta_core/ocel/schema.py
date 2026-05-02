from __future__ import annotations

REQUIRED_OBJECT_TYPES = {
    "session",
    "agent",
    "worker",
    "user_request",
    "goal",
    "task_instance",
    "step_instance",
    "message",
    "prompt",
    "llm_call",
    "llm_response",
    "llm_model",
    "provider",
    "skill",
    "tool",
    "mission",
    "delegation",
    "trace",
    "artifact",
    "file",
    "repository",
    "memory_entry",
    "pattern_asset",
    "recommendation",
    "error",
    "outcome",
}

EVENT_OBJECT_QUALIFIERS = {
    "session_context",
    "acting_agent",
    "executing_worker",
    "primary_request",
    "input_message",
    "assembled_prompt",
    "llm_call",
    "used_provider",
    "used_model",
    "generated_response",
    "selected_skill",
    "executed_skill",
    "used_tool",
    "target_file",
    "target_repository",
    "produced_artifact",
    "observed_error",
    "produced_outcome",
    "goal_context",
    "trace_context",
}

OBJECT_OBJECT_QUALIFIERS = {
    "belongs_to_session",
    "created_by_agent",
    "derived_from_request",
    "handled_in_session",
    "executed_by_agent",
    "handled_by_worker",
    "request_to_prompt",
    "prompt_to_llm_call",
    "llm_call_to_response",
    "response_to_outcome",
    "skill_part_of_agent",
    "worker_for_agent",
    "artifact_from_request",
    "error_from_run",
    "outcome_of_run",
}

CANONICAL_EVENT_ACTIVITIES = {
    "receive_user_request",
    "register_goal",
    "start_goal",
    "plan_goal",
    "create_task_instance",
    "start_task",
    "select_skill",
    "execute_skill",
    "complete_task",
    "fail_task",
    "complete_goal",
    "fail_goal",
    "assemble_prompt",
    "call_llm",
    "receive_llm_response",
    "record_outcome",
    "fail_run",
}

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS event(
        ocel_id TEXT PRIMARY KEY,
        ocel_type TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS object(
        ocel_id TEXT PRIMARY KEY,
        ocel_type TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS event_object(
        ocel_event_id TEXT NOT NULL,
        ocel_object_id TEXT NOT NULL,
        ocel_qualifier TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS object_object(
        ocel_source_id TEXT NOT NULL,
        ocel_target_id TEXT NOT NULL,
        ocel_qualifier TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS event_map_type(
        ocel_type TEXT NOT NULL,
        ocel_type_map TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS object_map_type(
        ocel_type TEXT NOT NULL,
        ocel_type_map TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS chanta_event_payload(
        event_id TEXT PRIMARY KEY,
        event_activity TEXT NOT NULL,
        event_timestamp TEXT NOT NULL,
        event_attrs_json TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS chanta_object_state(
        object_id TEXT PRIMARY KEY,
        object_type TEXT NOT NULL,
        object_attrs_json TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS chanta_event_object_relation_ext(
        event_id TEXT NOT NULL,
        object_id TEXT NOT NULL,
        qualifier TEXT NOT NULL,
        relation_attrs_json TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS chanta_object_object_relation_ext(
        source_object_id TEXT NOT NULL,
        target_object_id TEXT NOT NULL,
        qualifier TEXT NOT NULL,
        relation_attrs_json TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS chanta_raw_event_mirror(
        row_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT,
        raw_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
]

UNIQUE_INDEX_STATEMENTS = [
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_event_object_unique
    ON event_object (
        ocel_event_id,
        ocel_object_id,
        ocel_qualifier
    )
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_object_object_unique
    ON object_object (
        ocel_source_id,
        ocel_target_id,
        ocel_qualifier
    )
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_chanta_event_object_relation_ext_unique
    ON chanta_event_object_relation_ext (
        event_id,
        object_id,
        qualifier
    )
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_chanta_object_object_relation_ext_unique
    ON chanta_object_object_relation_ext (
        source_object_id,
        target_object_id,
        qualifier
    )
    """,
]

QUERY_INDEX_STATEMENTS = [
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_event_payload_event_activity
    ON chanta_event_payload(event_activity)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_event_payload_event_timestamp
    ON chanta_event_payload(event_timestamp)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_object_state_object_type
    ON chanta_object_state(object_type)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_event_object_relation_ext_event_id
    ON chanta_event_object_relation_ext(event_id)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_event_object_relation_ext_object_id
    ON chanta_event_object_relation_ext(object_id)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_object_object_relation_ext_source
    ON chanta_object_object_relation_ext(source_object_id)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_chanta_object_object_relation_ext_target
    ON chanta_object_object_relation_ext(target_object_id)
    """,
]

REQUIRED_TABLES = {
    "event",
    "object",
    "event_object",
    "object_object",
    "event_map_type",
    "object_map_type",
    "chanta_event_payload",
    "chanta_object_state",
    "chanta_event_object_relation_ext",
    "chanta_object_object_relation_ext",
    "chanta_raw_event_mirror",
}

REQUIRED_INDEXES = {
    "idx_event_object_unique",
    "idx_object_object_unique",
    "idx_chanta_event_object_relation_ext_unique",
    "idx_chanta_object_object_relation_ext_unique",
    "idx_chanta_event_payload_event_activity",
    "idx_chanta_event_payload_event_timestamp",
    "idx_chanta_object_state_object_type",
    "idx_chanta_event_object_relation_ext_event_id",
    "idx_chanta_event_object_relation_ext_object_id",
    "idx_chanta_object_object_relation_ext_source",
    "idx_chanta_object_object_relation_ext_target",
}

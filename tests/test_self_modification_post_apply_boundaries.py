from __future__ import annotations

import inspect

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
)
import chanta_core.self_modification_safety.post_apply as post_apply


def test_post_apply_ocel_mapping_includes_verification_and_outcome_types() -> None:
    for object_type in [
        "post_apply_verification_request",
        "post_apply_verification_source_bundle",
        "post_apply_target_snapshot",
        "post_apply_hash_verification_result",
        "post_apply_ocel_trace_verification_result",
        "post_apply_authorization_verification_result",
        "post_apply_rollback_readiness_result",
        "post_apply_scope_verification_result",
        "post_apply_safety_regression_check",
        "post_apply_verification_finding",
        "post_apply_verification_report",
        "modification_outcome_record",
        "post_apply_needs_more_input_candidate",
        "post_apply_rollback_recommended_candidate",
        "workspace_file_changed_event",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_post_apply_verification_requested",
        "self_modification_post_apply_sources_collected",
        "self_modification_post_apply_target_snapshot_collected",
        "self_modification_post_apply_hash_verified",
        "self_modification_post_apply_ocel_trace_verified",
        "self_modification_post_apply_authorization_verified",
        "self_modification_post_apply_rollback_readiness_checked",
        "self_modification_post_apply_scope_verified",
        "self_modification_post_apply_safety_regression_checked",
        "self_modification_post_apply_verification_report_created",
        "self_modification_outcome_recorded",
        "self_modification_rollback_recommended",
        "self_modification_post_apply_needs_more_input_created",
        "self_modification_post_apply_verification_failed",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "verifies_bounded_apply",
        "uses_bounded_apply_report",
        "uses_bounded_apply_transaction",
        "uses_workspace_file_change_record",
        "uses_workspace_file_changed_event",
        "verifies_after_hash",
        "verifies_ocel_trace",
        "verifies_apply_authorization_consumed",
        "verifies_rollback_readiness",
        "verifies_apply_scope",
        "checks_post_apply_safety_regression",
        "records_modification_outcome",
        "recommends_rollback",
        "requires_operator_followup",
        "not_rollback_executed",
        "not_memory_promotion",
        "not_post_apply_shell_execution",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert "outcome_recorded" in SELF_MODIFICATION_EFFECT_TYPES


def test_post_apply_runtime_has_no_additional_write_shell_test_lint_or_llm_judge() -> None:
    source = inspect.getsource(post_apply)
    forbidden = [
        "apply_patch(",
        "write_file",
        "Path.write_text",
        "Path.write_bytes",
        "shutil.move",
        "os.remove",
        "chmod",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "additional_patch_applied=True",
        "file_write_performed=True",
        "shell_executed=True",
        "test_lint_executed=True",
        "rollback_executed=True",
        "memory_mutation_enabled=True",
        "persona_mutation_enabled=True",
        "overlay_mutation_enabled=True",
        "exec(",
        "eval(",
    ]
    for token in forbidden:
        assert token not in source
    assert "emit_file_changed" not in source
    assert ".write_text(" not in source
    assert ".write_bytes(" not in source
    assert '.open("w"' not in source
    assert "handle.write(" not in source


def test_post_apply_workspace_file_changed_is_read_only_verification_target() -> None:
    source = inspect.getsource(post_apply)

    assert "workspace_file_changed_event_refs" in source
    assert "workspace_file_changed_event_id" in source
    assert "WorkspaceFileChangedEventService" not in source
    assert "workspace_file_changed_event_refs" in source

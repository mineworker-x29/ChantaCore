from __future__ import annotations

import inspect

from chanta_core.self_modification_safety import (
    BoundedWorkspaceWriter,
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
)
import chanta_core.self_modification_safety.bounded_apply as bounded_apply


def test_bounded_apply_ocel_mapping_includes_workspace_file_changed() -> None:
    for object_type in [
        "bounded_patch_apply_request",
        "apply_authorization_validation_result",
        "pre_apply_revalidation_report",
        "bounded_patch_apply_transaction",
        "workspace_file_change_record",
        "bounded_patch_apply_report",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_bounded_apply_requested",
        "self_modification_apply_authorization_validated",
        "self_modification_pre_apply_revalidation_performed",
        "self_modification_bounded_patch_applied",
        "self_modification_apply_authorization_consumed",
        "workspace_file_changed",
        "self_modification_bounded_apply_report_created",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "requests_bounded_apply",
        "uses_apply_gate_authorization",
        "validates_apply_authorization",
        "revalidates_target_before_apply",
        "revalidates_operation_before_apply",
        "applies_approved_operation",
        "changes_workspace_file",
        "records_before_hash",
        "records_after_hash",
        "consumes_apply_authorization",
        "requires_post_apply_verification",
        "not_post_apply_verified_yet",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert "workspace_file_changed" in SELF_MODIFICATION_EFFECT_TYPES


def test_runtime_does_not_use_shell_test_lint_external_or_llm_judge() -> None:
    source = inspect.getsource(bounded_apply)
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "shell_executed=True",
        "test_lint_executed=True",
        "post_apply_verified=True",
        "outcome_recorded=True",
        "rollback_executed=True",
        "exec(",
        "eval(",
    ]
    for token in forbidden:
        assert token not in source


def test_file_write_calls_are_isolated_to_bounded_workspace_writer() -> None:
    module_source = inspect.getsource(bounded_apply)
    writer_source = inspect.getsource(BoundedWorkspaceWriter)

    assert '.open("w"' in writer_source
    assert "handle.write(" in writer_source
    assert module_source.count('.open("w"') == writer_source.count('.open("w"')
    assert module_source.count("handle.write(") == writer_source.count("handle.write(")
    assert ".write_text(" not in module_source


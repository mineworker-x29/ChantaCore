from __future__ import annotations

import inspect

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    SelfModificationWorkbenchService,
)
import chanta_core.self_modification_safety.workbench as workbench


def test_workbench_ocel_mapping_contains_view_types() -> None:
    for object_type in [
        "self_modification_workbench_snapshot",
        "self_modification_subject_status_view",
        "self_modification_pipeline_item",
        "self_modification_safety_boundary_summary",
        "self_modification_authorization_view",
        "self_modification_change_view",
        "self_modification_finding_view",
        "self_modification_timeline_event",
        "self_modification_ocel_coverage_view",
        "self_modification_readiness_view",
        "bounded_patch_apply_report",
        "post_apply_verification_report",
        "modification_outcome_record",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_workbench_requested",
        "self_modification_workbench_snapshot_created",
        "self_modification_requests_viewed",
        "self_modification_candidates_viewed",
        "self_modification_drafts_viewed",
        "self_modification_static_safety_viewed",
        "self_modification_dry_run_viewed",
        "self_modification_review_gate_viewed",
        "self_modification_bounded_apply_viewed",
        "self_modification_post_apply_viewed",
        "self_modification_outcomes_viewed",
        "self_modification_findings_viewed",
        "self_modification_timeline_viewed",
        "self_modification_safety_boundary_viewed",
        "self_modification_workbench_warning_created",
        "self_modification_workbench_blocker_detected",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "views_self_modification_pipeline",
        "views_modification_request",
        "views_patch_candidate",
        "views_patch_draft",
        "views_diff_preview",
        "views_static_safety_report",
        "views_dry_run_report",
        "views_review_gate",
        "views_apply_gate",
        "views_bounded_apply_report",
        "views_workspace_file_change",
        "views_post_apply_verification",
        "views_modification_outcome",
        "views_authorization_state",
        "views_safety_boundary",
        "views_timeline",
        "views_findings",
        "views_ocel_coverage",
        "computes_self_modification_readiness",
        "detects_self_modification_blocker",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES


def test_workbench_projection_effect_is_read_only_only() -> None:
    projection = SelfModificationWorkbenchService().build_ocpx_projection()

    assert projection["effect_types"] == ["read_only_observation"]
    assert projection["mutation_performed"] is False


def test_workbench_runtime_has_no_mutation_execution_or_llm_judge() -> None:
    source = inspect.getsource(workbench)
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
        "httpx",
        "mcp.connect",
        "plugin.load",
        "outcome_recorded=True",
        "authorization_consumed=True",
        "rollback_executed=True",
        "shell_executed=True",
        "test_lint_executed=True",
        "file_write_performed=True",
        "mutation_performed=True",
        "exec(",
        "eval(",
    ]
    for token in forbidden:
        assert token not in source
    assert "emit_file_changed" not in source
    assert "WorkspaceFileChangedEventService" not in source
    assert "record_review_decision" not in source
    assert "consume(" not in source
    assert "verify_and_record_outcome(" not in source
    assert ".write_text(" not in source
    assert ".write_bytes(" not in source
    assert '.open("w"' not in source
    assert "handle.write(" not in source

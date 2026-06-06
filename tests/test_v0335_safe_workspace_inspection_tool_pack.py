import os

import pytest

from chanta_core.agent_runtime import (
    V0335ReadinessReport,
    WorkspaceInspectionDecisionKind,
    WorkspaceInspectionFlagSet,
    WorkspaceInspectionNoWriteGuarantee,
    WorkspaceInspectionReadinessLevel,
    WorkspaceInspectionRequestKind,
    WorkspaceInspectionResultKind,
    WorkspaceInspectionRiskKind,
    WorkspaceInspectionSkipReasonKind,
    WorkspaceInspectionSourceKind,
    WorkspaceInspectionStatus,
    WorkspaceInspectionToolKind,
    build_v0335_readiness_report,
    build_workspace_inspection_flags,
    build_workspace_inspection_denied_record,
    build_workspace_inspection_no_write_guarantee,
    build_workspace_inspection_report,
    build_workspace_inspection_request,
    build_workspace_inspection_run_preview,
    build_workspace_inspection_tool_pack,
    build_workspace_inspection_validation_report,
    default_workspace_inspection_limits,
    default_workspace_inspection_path_policy,
    inspect_file_metadata_readonly,
    inspect_project_tree_readonly,
    inspect_workspace_path_readonly,
    normalize_and_validate_workspace_path,
    read_text_file_safe,
    search_text_in_workspace_readonly,
    summarize_reference_inventory_readonly,
    v0335_readiness_report_is_not_general_runtime_ready,
    workspace_inspection_decision_is_safe_readonly,
    workspace_inspection_flags_preserve_unsafe_runtime_false,
    workspace_inspection_policy_blocks_secret_paths,
    workspace_inspection_result_has_no_write,
)
from chanta_core.agent_runtime.workspace_inspection import (
    DEFAULT_PROHIBITED_UNTIL_LATER_GATE,
    UNSAFE_RUNTIME_FLAG_NAMES,
    WorkspaceInspectionPathPolicy,
)


def _policy(tmp_path, **limit_overrides):
    limits = default_workspace_inspection_limits()
    if limit_overrides:
        limits = default_workspace_inspection_limits().__class__(
            limits_id="limits:test",
            max_depth=limit_overrides.get("max_depth", limits.max_depth),
            max_entries=limit_overrides.get("max_entries", limits.max_entries),
            max_file_size_bytes=limit_overrides.get("max_file_size_bytes", limits.max_file_size_bytes),
            max_read_chars=limit_overrides.get("max_read_chars", limits.max_read_chars),
            max_search_matches=limit_overrides.get("max_search_matches", limits.max_search_matches),
            max_search_files=limit_overrides.get("max_search_files", limits.max_search_files),
            max_line_length=limit_overrides.get("max_line_length", limits.max_line_length),
            allowed_text_extensions=list(limits.allowed_text_extensions),
        )
    return default_workspace_inspection_path_policy(tmp_path, limits=limits)


def test_workspace_inspection_taxonomies_and_flags():
    assert "inspect_project_tree_readonly" in {item.value for item in WorkspaceInspectionToolKind}
    assert "read_text_file_safe" in {item.value for item in WorkspaceInspectionToolKind}
    assert "inspect_tree" in {item.value for item in WorkspaceInspectionRequestKind}
    assert "allow_safe_text_read" in {item.value for item in WorkspaceInspectionDecisionKind}
    assert "outside_allowed_root" in {item.value for item in WorkspaceInspectionSkipReasonKind}
    assert "secret_file_risk" in {item.value for item in WorkspaceInspectionRiskKind}
    assert "safe_text_read_result" in {item.value for item in WorkspaceInspectionResultKind}
    assert "completed_with_skips" in {item.value for item in WorkspaceInspectionStatus}
    assert "safe_readonly_inspection_ready" in {item.value for item in WorkspaceInspectionReadinessLevel}
    assert "opencode_reference_path" in {item.value for item in WorkspaceInspectionSourceKind}

    flags = build_workspace_inspection_flags(
        safe_workspace_inspection_tool_pack_constructed=True,
        safe_path_policy_available=True,
        safe_metadata_inspection_enabled=True,
        safe_tree_inspection_enabled=True,
        safe_text_read_enabled=True,
        safe_text_search_enabled=True,
        safe_reference_inventory_summary_enabled=True,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
        ready_for_file_read=True,
        ready_for_reference_file_access=True,
    )

    assert flags.safe_workspace_inspection_tool_pack_constructed is True
    assert flags.ready_for_safe_workspace_inspection_execution is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_tool_execution is False
    assert workspace_inspection_flags_preserve_unsafe_runtime_false(flags)

    for flag_name in UNSAFE_RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            WorkspaceInspectionFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.5",
                **{flag_name: True},
            )


def test_path_policy_blocks_secret_binary_write_command_network_and_reference_execution(tmp_path):
    policy = _policy(tmp_path)

    assert workspace_inspection_policy_blocks_secret_paths(policy)
    assert policy.allow_binary_read is False
    assert policy.allow_secret_read is False
    assert policy.allow_workspace_write is False
    assert policy.allow_command_execution is False
    assert policy.allow_network_access is False
    assert policy.allow_credential_access is False
    assert policy.allow_reference_code_execution is False
    assert policy.allow_reference_import is False
    assert policy.allow_dependency_install is False
    assert policy.root_policy.allow_symlink_escape is False

    for flag_name in (
        "allow_binary_read",
        "allow_secret_read",
        "allow_workspace_write",
        "allow_command_execution",
        "allow_network_access",
        "allow_credential_access",
        "allow_reference_code_execution",
        "allow_reference_import",
        "allow_dependency_install",
    ):
        with pytest.raises(ValueError):
            WorkspaceInspectionPathPolicy(
                path_policy_id=f"policy:bad:{flag_name}",
                root_policy=policy.root_policy,
                limits=policy.limits,
                **{flag_name: True},
            )


def test_normalize_path_allows_inside_root_and_denies_outside_traversal_secret_and_symlink(tmp_path):
    policy = _policy(tmp_path)
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("safe", encoding="utf-8")
    secret_file = tmp_path / ".env"
    secret_file.write_text("SECRET=not-read", encoding="utf-8")
    outside = tmp_path.parent / "outside.txt"

    allowed = normalize_and_validate_workspace_path(safe_file, policy)
    outside_decision = normalize_and_validate_workspace_path(outside, policy)
    traversal = normalize_and_validate_workspace_path(tmp_path / ".." / "outside.txt", policy)
    secret = normalize_and_validate_workspace_path(secret_file, policy)

    assert allowed.safe_readonly_allowed is True
    assert workspace_inspection_decision_is_safe_readonly(allowed)
    assert outside_decision.status == WorkspaceInspectionStatus.DENIED
    assert WorkspaceInspectionSkipReasonKind.OUTSIDE_ALLOWED_ROOT in outside_decision.skip_reasons
    assert traversal.status == WorkspaceInspectionStatus.DENIED
    assert secret.status == WorkspaceInspectionStatus.SKIPPED
    assert WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE in secret.skip_reasons

    target_dir = tmp_path.parent
    link = tmp_path / "escape_link"
    try:
        link.symlink_to(target_dir, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable in this environment")
    symlink_decision = normalize_and_validate_workspace_path(link, policy)
    assert symlink_decision.status == WorkspaceInspectionStatus.SKIPPED
    assert WorkspaceInspectionSkipReasonKind.PATH_IS_SYMLINK_OUTSIDE_ROOT in symlink_decision.skip_reasons


def test_tree_and_metadata_inspection_are_bounded_and_content_free(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "one.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "a" / "two.md").write_text("beta", encoding="utf-8")
    (tmp_path / "b").mkdir()
    (tmp_path / "b" / "three.py").write_text("print('metadata only')", encoding="utf-8")
    policy = _policy(tmp_path, max_depth=1, max_entries=3)

    tree_request = build_workspace_inspection_request(
        "request:tree",
        WorkspaceInspectionRequestKind.INSPECT_TREE,
        WorkspaceInspectionToolKind.INSPECT_PROJECT_TREE_READONLY,
        path_ref=str(tmp_path),
    )
    tree_result = inspect_project_tree_readonly(tree_request, policy)
    metadata_request = build_workspace_inspection_request(
        "request:metadata",
        WorkspaceInspectionRequestKind.INSPECT_METADATA,
        WorkspaceInspectionToolKind.INSPECT_FILE_METADATA_READONLY,
        path_ref=str(tmp_path / "a" / "one.txt"),
    )
    metadata_result = inspect_file_metadata_readonly(metadata_request, policy)

    assert tree_result.tree_result is not None
    assert len(tree_result.tree_result.entries) <= policy.limits.max_entries
    assert tree_result.ready_for_execution is False
    assert workspace_inspection_result_has_no_write(tree_result)
    assert all("alpha" not in entry.path_metadata.metadata for entry in tree_result.tree_result.entries)
    assert metadata_result.metadata_result is not None
    assert metadata_result.metadata_result.path_metadata.size_bytes == 5
    assert metadata_result.metadata_result.metadata == {}


def test_safe_text_read_reads_truncates_and_skips_secret_oversized_and_binary(tmp_path):
    safe = tmp_path / "safe.txt"
    safe.write_text("abcdef", encoding="utf-8")
    secret = tmp_path / "token.txt"
    secret.write_text("TOKEN=not-read", encoding="utf-8")
    large = tmp_path / "large.txt"
    large.write_text("x" * 20, encoding="utf-8")
    binary = tmp_path / "binary.txt"
    binary.write_bytes(b"\x00\x01\x02abc")
    policy = _policy(tmp_path, max_read_chars=3, max_file_size_bytes=10)

    safe_result = read_text_file_safe(
        build_workspace_inspection_request(
            "request:read",
            WorkspaceInspectionRequestKind.READ_SAFE_TEXT,
            WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE,
            path_ref=str(safe),
        ),
        policy,
    )
    secret_result = read_text_file_safe(
        build_workspace_inspection_request(
            "request:secret",
            WorkspaceInspectionRequestKind.READ_SAFE_TEXT,
            WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE,
            path_ref=str(secret),
        ),
        policy,
    )
    large_result = read_text_file_safe(
        build_workspace_inspection_request(
            "request:large",
            WorkspaceInspectionRequestKind.READ_SAFE_TEXT,
            WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE,
            path_ref=str(large),
        ),
        policy,
    )
    binary_result = read_text_file_safe(
        build_workspace_inspection_request(
            "request:binary",
            WorkspaceInspectionRequestKind.READ_SAFE_TEXT,
            WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE,
            path_ref=str(binary),
        ),
        policy,
    )

    assert safe_result.text_read_result is not None
    assert safe_result.text_read_result.text_excerpt == "abc"
    assert safe_result.text_read_result.truncated is True
    assert safe_result.ready_for_execution is False
    assert secret_result.text_read_result is not None
    assert secret_result.text_read_result.text_excerpt == ""
    assert WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE in secret_result.text_read_result.skip_reasons
    assert large_result.text_read_result is not None
    assert WorkspaceInspectionSkipReasonKind.FILE_TOO_LARGE in large_result.text_read_result.skip_reasons
    assert binary_result.text_read_result is not None
    assert WorkspaceInspectionSkipReasonKind.PATH_IS_BINARY in binary_result.text_read_result.skip_reasons


def test_safe_text_search_is_bounded_and_skips_unsafe_files(tmp_path):
    (tmp_path / "one.txt").write_text("needle one\nneedle two\n", encoding="utf-8")
    (tmp_path / "two.md").write_text("needle three\n", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("needle secret", encoding="utf-8")
    (tmp_path / "bin.txt").write_bytes(b"\x00needle")
    policy = _policy(tmp_path, max_search_matches=2, max_search_files=3)

    request = build_workspace_inspection_request(
        "request:search",
        WorkspaceInspectionRequestKind.SEARCH_SAFE_TEXT,
        WorkspaceInspectionToolKind.SEARCH_TEXT_IN_WORKSPACE_READONLY,
        path_ref=str(tmp_path),
        query="needle",
    )
    result = search_text_in_workspace_readonly(request, policy)

    assert result.text_search_result is not None
    assert len(result.text_search_result.matches) <= 2
    assert result.text_search_result.searched_file_count <= 3
    assert result.text_search_result.truncated is True
    assert all("secret" not in match.line_excerpt for match in result.text_search_result.matches)
    assert result.ready_for_execution is False


def test_reference_inventory_is_metadata_only_when_reference_root_allowed(tmp_path):
    references = tmp_path / "references"
    opencode = references / "OpenCode"
    opencode.mkdir(parents=True)
    (opencode / "README.md").write_text("reference metadata only", encoding="utf-8")
    (opencode / ".env").write_text("SECRET=not-read", encoding="utf-8")
    policy = default_workspace_inspection_path_policy(
        tmp_path,
        allow_references_root=True,
        references_root=references,
        limits=default_workspace_inspection_limits(),
    )

    request = build_workspace_inspection_request(
        "request:reference",
        WorkspaceInspectionRequestKind.SUMMARIZE_REFERENCE_INVENTORY,
        WorkspaceInspectionToolKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY,
        path_ref=str(references),
    )
    result = summarize_reference_inventory_readonly(request, policy)

    assert result.result_kind == WorkspaceInspectionResultKind.REFERENCE_INVENTORY_SUMMARY
    assert result.tree_result is not None
    assert all("reference metadata only" not in entry.path_metadata.metadata for entry in result.tree_result.entries)
    assert any(
        WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE in record.skip_reasons
        for record in result.denied_records
    )
    assert result.ready_for_execution is False


def test_tool_pack_reports_preview_guarantee_and_readiness_are_not_general_runtime(tmp_path):
    policy = _policy(tmp_path)
    tool_pack = build_workspace_inspection_tool_pack(
        "tool_pack:1",
        policy,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
    )
    denied = normalize_and_validate_workspace_path(tmp_path / ".." / "outside.txt", policy)
    validation = build_workspace_inspection_validation_report(
        "validation:1",
        tool_pack_id=tool_pack.tool_pack_id,
        request_id="request:outside",
        decision_id=denied.decision_id,
        denied_records=[],
        validation_passed=True,
    )
    blocked_validation = build_workspace_inspection_validation_report(
        "validation:blocked",
        denied_records=[
            build_workspace_inspection_denied_record(
                "denied:1",
                reason="Denied path.",
            )
        ],
        validation_passed=False,
    )
    report = build_workspace_inspection_report(
        "report:1",
        tool_pack_id=tool_pack.tool_pack_id,
        result_ids=["result:1"],
        inspected_path_count=1,
        skipped_path_count=0,
        denied_count=0,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
    )
    preview = build_workspace_inspection_run_preview("preview:1", tool_pack_id=tool_pack.tool_pack_id)
    guarantee = build_workspace_inspection_no_write_guarantee("guarantee:1")
    readiness = build_v0335_readiness_report(
        "readiness:1",
        tool_pack_id=tool_pack.tool_pack_id,
        inspection_report_id=report.report_id,
        validation_report_id=validation.validation_report_id,
        ready_for_v0336_agent_step_runner=True,
        ready_for_v0337_runtime_ocel_trace_emitter=True,
        safe_readonly_workspace_inspection_enabled=True,
        ready_for_safe_readonly_tool_execution=True,
        ready_for_safe_workspace_inspection_execution=True,
        ready_for_file_read=True,
        ready_for_reference_file_access=True,
    )

    assert tool_pack.ready_for_execution is False
    assert validation.validation_passed is True
    assert blocked_validation.validation_passed is False
    assert report.ready_for_execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert readiness.safe_readonly_workspace_inspection_enabled is True
    assert readiness.ready_for_safe_workspace_inspection_execution is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_general_tool_execution is False
    assert v0335_readiness_report_is_not_general_runtime_ready(readiness)
    assert set(DEFAULT_PROHIBITED_UNTIL_LATER_GATE).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        build_workspace_inspection_validation_report(
            "validation:bad",
            denied_records=[
                build_workspace_inspection_denied_record(
                    "denied:bad",
                    reason="Denied path.",
                )
            ],
            validation_passed=True,
        )
    with pytest.raises(ValueError):
        WorkspaceInspectionNoWriteGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.5",
            no_workspace_write=False,
        )
    for flag_name in UNSAFE_RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0335ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.5",
                **{flag_name: True},
            )


def test_inspect_workspace_path_routes_safely(tmp_path):
    safe = tmp_path / "safe.txt"
    safe.write_text("route", encoding="utf-8")
    policy = _policy(tmp_path)

    metadata_request = build_workspace_inspection_request(
        "request:route:metadata",
        WorkspaceInspectionRequestKind.INSPECT_PATH,
        WorkspaceInspectionToolKind.INSPECT_WORKSPACE_PATH_READONLY,
        path_ref=str(safe),
    )
    tree_request = build_workspace_inspection_request(
        "request:route:tree",
        WorkspaceInspectionRequestKind.INSPECT_PATH,
        WorkspaceInspectionToolKind.INSPECT_WORKSPACE_PATH_READONLY,
        path_ref=str(tmp_path),
    )

    assert inspect_workspace_path_readonly(metadata_request, policy).metadata_result is not None
    assert inspect_workspace_path_readonly(tree_request, policy).tree_result is not None


def test_implementation_source_has_no_shell_subprocess_network_or_write_patterns():
    source_path = os.path.join("src", "chanta_core", "agent_runtime", "workspace_inspection.py")
    with open(source_path, "r", encoding="utf-8") as handle:
        source = handle.read()

    forbidden_fragments = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "write_text(",
        "write_bytes(",
        "unlink(",
        "rmdir(",
        "mkdir(",
        "rename(",
        "replace(",
        "chmod(",
        "chown(",
        "shutil.",
    ]
    assert not any(fragment in source for fragment in forbidden_fragments)

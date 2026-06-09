import inspect

import pytest

from chanta_core.agent_runtime import (
    PatchContextCollectionMode,
    PatchContextDecisionKind,
    PatchContextEvidenceKind,
    PatchContextFileRole,
    PatchContextReadinessLevel,
    PatchContextReferenceRole,
    PatchContextRiskKind,
    PatchContextSourceKind,
    PatchContextTargetStatus,
    ReferenceCorpusKind,
    build_patch_context_collection_decision,
    build_patch_context_collection_policy,
    build_patch_context_collection_report,
    build_patch_context_evidence_bundle,
    build_patch_context_evidence_item,
    build_patch_context_file_summary,
    build_patch_context_flags,
    build_patch_context_no_write_guarantee,
    build_patch_context_reference_summary,
    build_patch_context_request,
    build_patch_context_request_from_intent_scope_bundle,
    build_patch_context_run_preview,
    build_patch_context_search_finding,
    build_patch_context_snapshot,
    build_patch_context_source_ref,
    build_patch_context_target,
    build_patch_context_validation_report,
    build_patch_intent_scope_bundle,
    build_v0352_readiness_report,
    collect_patch_context_readonly,
    collect_reference_corpus_context_readonly,
    default_patch_context_collection_policy,
    patch_context_collection_policy_blocks_write,
    patch_context_evidence_bundle_is_not_diff_proposal,
    patch_context_flags_preserve_no_write,
    patch_context_snapshot_is_not_patch_plan,
    search_patch_context_readonly,
    summarize_patch_context_file_readonly,
    v0352_readiness_report_is_not_execution_ready,
    validate_patch_context_snapshot,
)
from chanta_core.agent_runtime import patch_context as context_module


def test_v0352_taxonomies_have_required_values() -> None:
    assert PatchContextCollectionMode.READONLY_WORKSPACE_CONTEXT.value == "readonly_workspace_context"
    assert PatchContextCollectionMode.UNKNOWN.value == "unknown"
    assert PatchContextSourceKind.V0351_PATCH_INTENT_SCOPE_BUNDLE.value == "v0351_patch_intent_scope_bundle"
    assert PatchContextSourceKind.REFERENCE_CORPUS_HERMES.value == "reference_corpus_hermes"
    assert PatchContextTargetStatus.COLLECTED_WITH_WARNINGS.value == "collected_with_warnings"
    assert PatchContextReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0353.value == "design_handoff_ready_for_v0353"
    assert PatchContextDecisionKind.ALLOW_BOUNDED_SEARCH.value == "allow_bounded_search"
    assert PatchContextRiskKind.RAW_SOURCE_DUMP_RISK.value == "raw_source_dump_risk"
    assert PatchContextEvidenceKind.BOUNDED_TEXT_EXCERPT.value == "bounded_text_excerpt"
    assert PatchContextFileRole.REFERENCE_SOURCE_SUMMARY.value == "reference_source_summary"
    assert PatchContextReferenceRole.HERMES_PATCH_PATTERN_SOURCE.value == "hermes_patch_pattern_source"


def test_flags_allow_readonly_context_but_block_unsafe_readiness() -> None:
    flags = build_patch_context_flags()
    assert flags.patch_context_collector_constructed is True
    assert flags.readonly_collection_policy_defined is True
    assert flags.context_snapshot_constructed is True
    assert flags.evidence_bundle_constructed is True
    assert flags.reference_digest_consumed is True
    assert flags.reference_corpus_readonly_summary_available is True
    assert flags.ready_for_v0353_reference_informed_patch_plan is True
    assert flags.ready_for_v0354_diff_proposal_envelope is True
    assert flags.ready_for_readonly_patch_context_collection is True
    assert flags.ready_for_patch_context_snapshot is True
    assert flags.ready_for_patch_context_evidence_bundle is True
    assert flags.ready_for_patch_plan is False
    assert flags.ready_for_change_set_graph is False
    assert flags.ready_for_diff_proposal is False
    assert flags.ready_for_patch_proposal is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_reference_execution is False
    assert flags.ready_for_reference_import is False
    assert flags.ready_for_raw_source_dump is False
    assert flags.production_certified is False
    assert patch_context_flags_preserve_no_write(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_patch_plan",
        "ready_for_change_set_graph",
        "ready_for_diff_proposal",
        "ready_for_patch_proposal",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_raw_source_dump",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_patch_context_flags(**{unsafe_flag: True})


def test_collection_policy_blocks_write_apply_secret_binary_outside_and_raw_dump(tmp_path) -> None:
    policy = build_patch_context_collection_policy(allowed_root_refs=[str(tmp_path)])
    assert policy.allow_file_metadata is True
    assert policy.allow_bounded_text_excerpt is True
    assert policy.allow_bounded_search is True
    assert policy.allow_reference_digest_metadata is True
    assert policy.allow_reference_corpus_readonly_summary is True
    assert policy.allow_secret_file_read is False
    assert policy.allow_credential_file_read is False
    assert policy.allow_binary_file_read is False
    assert policy.allow_outside_scope_read is False
    assert policy.allow_shell is False
    assert policy.allow_subprocess is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_patch_application is False
    assert policy.allow_raw_source_dump is False
    assert patch_context_collection_policy_blocks_write(policy)

    for field in [
        "allow_secret_file_read",
        "allow_credential_file_read",
        "allow_binary_file_read",
        "allow_outside_scope_read",
        "allow_shell",
        "allow_subprocess",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_patch_application",
        "allow_raw_source_dump",
    ]:
        with pytest.raises(ValueError):
            build_patch_context_collection_policy(**{field: True})


def test_request_source_ref_target_file_search_reference_and_evidence_models_are_readonly() -> None:
    source = build_patch_context_source_ref()
    assert source.source_kind == PatchContextSourceKind.V0351_PATCH_INTENT_SCOPE_BUNDLE

    request = build_patch_context_request(requested_target_refs=["docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"])
    assert "workspace_write" in request.prohibited_runtime_actions
    assert "reference_execution" in request.prohibited_runtime_actions

    target = build_patch_context_target(collected=True)
    assert target.allowed_readonly is True
    assert target.collected is True
    assert target.blocked is False

    with pytest.raises(ValueError):
        build_patch_context_target(collected=True, allowed_readonly=False)
    with pytest.raises(ValueError):
        build_patch_context_target(skipped=True)

    file_summary = build_patch_context_file_summary(excerpt_preview="bounded", structural_summary="bounded summary")
    assert file_summary.skipped is False
    assert len(file_summary.excerpt_preview) < 1200
    with pytest.raises(ValueError):
        build_patch_context_file_summary(excerpt_preview="x" * 1300)

    finding = build_patch_context_search_finding(query="PatchContext", finding_preview="bounded")
    assert finding.line_number is None
    assert "shell" not in finding.relevance_summary.lower()

    reference = build_patch_context_reference_summary(corpus_kind=ReferenceCorpusKind.HERMES)
    assert reference.executed_reference is False
    assert reference.imported_reference is False
    assert reference.installed_dependency is False
    assert reference.ran_reference_tests is False
    with pytest.raises(ValueError):
        build_patch_context_reference_summary(executed_reference=True)

    item = build_patch_context_evidence_item(evidence_preview="bounded evidence")
    assert len(item.evidence_preview) < 1200
    bundle = build_patch_context_evidence_bundle(evidence_items=[item])
    assert patch_context_evidence_bundle_is_not_diff_proposal(bundle)
    assert bundle.ready_for_patch_plan is False
    assert bundle.ready_for_diff_proposal is False
    assert bundle.ready_for_patch_proposal is False
    assert bundle.ready_for_execution is False


def test_evidence_bundle_snapshot_reports_guarantee_and_readiness_keep_unsafe_false() -> None:
    bundle = build_patch_context_evidence_bundle()
    snapshot = build_patch_context_snapshot(evidence_bundle=bundle)
    assert patch_context_snapshot_is_not_patch_plan(snapshot)
    assert snapshot.ready_for_v0353_reference_informed_patch_plan is True
    assert snapshot.ready_for_v0354_diff_proposal_envelope is True
    assert snapshot.ready_for_patch_plan is False
    assert snapshot.ready_for_diff_proposal is False
    assert snapshot.ready_for_patch_proposal is False
    assert snapshot.ready_for_patch_application is False
    assert snapshot.ready_for_execution is False
    for field in ["ready_for_patch_plan", "ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"]:
        with pytest.raises(ValueError):
            build_patch_context_snapshot(**{field: True})

    decision = build_patch_context_collection_decision()
    assert decision.readonly_collection_allowed is True
    assert decision.workspace_write_allowed is False
    assert decision.code_edit_allowed is False
    assert decision.patch_application_allowed is False
    assert decision.shell_allowed is False
    with pytest.raises(ValueError):
        build_patch_context_collection_decision(workspace_write_allowed=True)

    validation = build_patch_context_validation_report()
    assert validation.no_write_confirmed is True
    assert validation.no_code_edit_confirmed is True
    assert validation.no_patch_application_confirmed is True
    assert validation.no_raw_source_dump_confirmed is True
    assert validation.ready_for_execution is False

    report = build_patch_context_collection_report()
    assert report.ready_for_readonly_patch_context_collection is True
    assert report.ready_for_patch_context_snapshot is True
    assert report.ready_for_patch_context_evidence_bundle is True
    assert report.ready_for_patch_plan is False
    assert report.ready_for_diff_proposal is False
    assert report.ready_for_patch_proposal is False
    assert report.ready_for_execution is False

    preview = build_patch_context_run_preview()
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_patch_context_no_write_guarantee()
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0352_readiness_report()
    assert readiness.ready_for_v0353_reference_informed_patch_plan is True
    assert readiness.ready_for_v0354_diff_proposal_envelope is True
    assert readiness.ready_for_readonly_patch_context_collection is True
    assert readiness.ready_for_patch_context_snapshot is True
    assert readiness.ready_for_patch_context_evidence_bundle is True
    assert readiness.ready_for_patch_plan is False
    assert readiness.ready_for_change_set_graph is False
    assert readiness.ready_for_diff_proposal is False
    assert readiness.ready_for_patch_proposal is False
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_code_edit is False
    assert readiness.ready_for_apply_patch is False
    assert readiness.ready_for_git_apply is False
    assert readiness.ready_for_test_execution is False
    assert readiness.ready_for_shell_execution is False
    assert readiness.ready_for_dependency_install is False
    assert readiness.ready_for_reference_execution is False
    assert readiness.ready_for_reference_import is False
    assert readiness.ready_for_execution is False
    assert readiness.production_certified is False
    assert v0352_readiness_report_is_not_execution_ready(readiness)


def test_tmp_path_safe_source_summary_and_search_are_bounded_readonly(tmp_path) -> None:
    source = tmp_path / "module.py"
    source.write_text("class Demo:\n    pass\n\ndef collect_context():\n    return 'PatchContext'\n", encoding="utf-8")
    policy = build_patch_context_collection_policy(allowed_root_refs=[str(tmp_path)], max_excerpt_chars=40)

    target, summary = summarize_patch_context_file_readonly(source, policy)
    assert target.collected is True
    assert target.allowed_readonly is True
    assert summary.skipped is False
    assert summary.truncated is True
    assert "class Demo" in summary.excerpt_preview
    assert any("class Demo" in item for item in summary.relevant_symbols_or_headings)

    findings = search_patch_context_readonly(source, "PatchContext", policy)
    assert len(findings) == 1
    assert findings[0].line_number == 5
    assert findings[0].truncated is False


def test_secret_binary_oversized_and_outside_root_targets_are_skipped_or_denied(tmp_path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    secret = root / ".env"
    secret.write_text("SECRET=do-not-read", encoding="utf-8")
    binary = root / "image.png"
    binary.write_bytes(b"\x89PNG")
    large = root / "large.py"
    large.write_text("x" * 100, encoding="utf-8")
    outside = tmp_path / "outside.py"
    outside.write_text("print('outside')", encoding="utf-8")
    policy = build_patch_context_collection_policy(allowed_root_refs=[str(root)], max_file_size_bytes=20)

    secret_target, secret_summary = summarize_patch_context_file_readonly(secret, policy)
    assert secret_target.status == PatchContextTargetStatus.SECRET_SKIPPED
    assert secret_summary.skipped is True

    binary_target, _ = summarize_patch_context_file_readonly(binary, policy)
    assert binary_target.status == PatchContextTargetStatus.BINARY_SKIPPED

    large_target, _ = summarize_patch_context_file_readonly(large, policy)
    assert large_target.status == PatchContextTargetStatus.TOO_LARGE

    outside_target, _ = summarize_patch_context_file_readonly(outside, policy)
    assert outside_target.status == PatchContextTargetStatus.OUTSIDE_SCOPE


def test_collect_patch_context_readonly_builds_snapshot_without_plan_or_diff(tmp_path) -> None:
    safe = tmp_path / "safe.md"
    safe.write_text("# Heading\nPatchContext evidence only.\n", encoding="utf-8")
    secret = tmp_path / "token.txt"
    secret.write_text("token should be skipped by name", encoding="utf-8")
    policy = build_patch_context_collection_policy(
        allowed_root_refs=[str(tmp_path)],
    )
    request = build_patch_context_request(
        requested_target_refs=[str(safe), str(secret)],
        requested_reference_corpus=[PatchContextSourceKind.REFERENCE_CORPUS_OPENCLAW],
    )
    snapshot = collect_patch_context_readonly(request, policy)
    assert patch_context_snapshot_is_not_patch_plan(snapshot)
    assert any(target.collected for target in snapshot.targets)
    assert any(target.status == PatchContextTargetStatus.SECRET_SKIPPED for target in snapshot.targets)
    assert snapshot.evidence_bundle.ready_for_diff_proposal is False
    assert any(ref.corpus_kind == ReferenceCorpusKind.OPENCLAW for ref in snapshot.reference_summaries)
    validation = validate_patch_context_snapshot(snapshot)
    assert validation.valid is True
    assert validation.ready_for_execution is False


def test_request_from_intent_scope_bundle_uses_selected_targets_only() -> None:
    bundle = build_patch_intent_scope_bundle()
    request = build_patch_context_request_from_intent_scope_bundle(bundle)
    assert request.intent_id == bundle.intent.intent_id
    assert request.scope_policy_id == bundle.scope_policy.scope_policy_id
    assert request.intent_scope_bundle_id == bundle.bundle_id
    assert isinstance(request.requested_target_refs, list)


def test_fake_reference_corpus_summary_is_readonly_and_blocks_runtime_patterns(tmp_path) -> None:
    opencode = tmp_path / "OpenCode"
    opencode.mkdir()
    (opencode / "README.md").write_text("CLI command surface and patch review pattern.", encoding="utf-8")
    (opencode / "runner.ts").write_text("runtime execution pattern is observed but rejected.", encoding="utf-8")
    (opencode / ".env").write_text("SECRET=not-read", encoding="utf-8")
    policy = build_patch_context_collection_policy(allowed_root_refs=[str(tmp_path)], max_files_per_target=3)
    summary = collect_reference_corpus_context_readonly(opencode, ReferenceCorpusKind.OPENCODE, policy)
    assert summary.inspected_readonly is True
    assert summary.executed_reference is False
    assert summary.imported_reference is False
    assert summary.installed_dependency is False
    assert summary.ran_reference_tests is False
    assert summary.observed_patterns
    assert summary.rejected_notes

    missing = collect_reference_corpus_context_readonly(tmp_path / "OpenClaw", ReferenceCorpusKind.OPENCLAW, policy)
    assert missing.inspected_readonly is False
    assert missing.executed_reference is False
    assert "not found" in missing.summary.lower()


def test_module_source_has_no_runtime_write_apply_shell_or_provider_calls() -> None:
    source = inspect.getsource(context_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "apply_patch(",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

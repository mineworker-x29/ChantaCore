from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairSandboxRootValidationReport,
    RepairSourceContextAssessment,
    RepairSourceContextConfidenceLevel,
    RepairSourceContextDecisionKind,
    RepairSourceContextFlagSet,
    RepairSourceContextMode,
    RepairSourceContextNoMutationGuarantee,
    RepairSourceContextPolicy,
    RepairSourceContextReadinessLevel,
    RepairSourceContextReport,
    RepairSourceContextRequest,
    RepairSourceContextRiskKind,
    RepairSourceContextRunPreview,
    RepairSourceContextSnapshot,
    RepairSourceContextSourceKind,
    RepairSourceContextSourceRef,
    RepairSourceContextStatus,
    RepairSourceContextSufficiencyKind,
    RepairSourceContextValidationFinding,
    RepairSourceContextValidationReport,
    RepairSourceExcerpt,
    RepairSourceExcerptKind,
    RepairSourceFileKind,
    RepairSourceFileSnapshot,
    RepairSourcePathCandidate,
    RepairSourcePathDisposition,
    RepairSourcePathValidationResult,
    RepairSourceReadDecision,
    RepairSymbolContextHint,
    V0382ReadinessReport,
    assess_repair_source_context,
    build_repair_sandbox_root_validation_report,
    build_repair_source_context_assessment,
    build_repair_source_context_flags,
    build_repair_source_context_no_mutation_guarantee,
    build_repair_source_context_policy,
    build_repair_source_context_report,
    build_repair_source_context_request,
    build_repair_source_context_request_from_evidence_bundle,
    build_repair_source_context_run_preview,
    build_repair_source_context_snapshot,
    build_repair_source_context_source_ref,
    build_repair_source_context_validation_finding,
    build_repair_source_context_validation_report,
    build_repair_source_excerpt,
    build_repair_source_file_snapshot,
    build_repair_source_path_candidate,
    build_repair_source_path_validation_result,
    build_repair_source_read_decision,
    build_repair_symbol_context_hint,
    build_v0382_readiness_report,
    classify_repair_source_file_kind,
    create_repair_source_context_snapshot,
    create_repair_source_excerpts,
    create_repair_source_file_snapshot,
    create_repair_symbol_context_hints,
    decide_repair_source_read,
    default_repair_source_context_policy,
    normalize_repair_source_relative_path,
    read_bounded_read_only_sandbox_source_file,
    repair_source_context_flags_preserve_no_mutation,
    repair_source_context_policy_blocks_live_and_unbounded_read,
    repair_source_context_snapshot_is_not_generation,
    repair_source_path_validation_blocks_escape,
    repair_source_snapshot_is_not_proposal,
    v0382_readiness_report_is_not_execution_ready,
    validate_repair_sandbox_root,
    validate_repair_source_context_snapshot,
    validate_repair_source_path_candidate,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0383_repair_scope_planner_change_intent",
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_read_only_sandbox_source_context",
    "ready_for_validated_sandbox_root_context",
    "ready_for_validated_read_only_sandbox_source_read",
    "ready_for_sandbox_source_read",
    "ready_for_source_context_snapshot",
    "ready_for_bounded_source_excerpt",
    "ready_for_source_path_validation",
    "ready_for_source_context_redaction",
    "ready_for_symbol_context_hint",
    "ready_for_source_context_sufficiency_assessment",
    "ready_for_future_repair_scope_planning_input",
    "ready_for_future_change_intent_input",
    "ready_for_future_proposed_diff_metadata_input",
    "ready_for_future_proposed_code_hunk_metadata_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def _root_and_file(tmp_path):
    root = tmp_path / "sandbox"
    package = root / "pkg"
    package.mkdir(parents=True)
    target = package / "module.py"
    target.write_text(
        "API_KEY = 'should-not-leak'\n\nclass Worker:\n    pass\n\ndef target_function():\n    return 1\n",
        encoding="utf-8",
    )
    return root, target


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairSourceContextMode} == {
        "read_only_sandbox_source_context",
        "sandbox_root_validation",
        "source_path_validation",
        "bounded_source_file_snapshot",
        "bounded_source_excerpt",
        "symbol_context_hint",
        "source_context_assessment",
        "future_scope_planning_input",
        "future_patch_metadata_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0381_repair_proposal_evidence_bundle" in {item.value for item in RepairSourceContextSourceKind}
    assert "source_snapshot_created" in {item.value for item in RepairSourceContextStatus}
    assert "bounded_source_snapshot_ready" in {item.value for item in RepairSourceContextReadinessLevel}
    assert "allow_bounded_read_only_sandbox_source_read" in {item.value for item in RepairSourceContextDecisionKind}
    assert "symlink_escape_risk" in {item.value for item in RepairSourceContextRiskKind}
    assert "python_source" in {item.value for item in RepairSourceFileKind}
    assert "denied_secret_path" in {item.value for item in RepairSourcePathDisposition}
    assert "symbol_hint_window" in {item.value for item in RepairSourceExcerptKind}
    assert "sufficient_for_future_patch_metadata" in {item.value for item in RepairSourceContextSufficiencyKind}
    assert "inconclusive" in {item.value for item in RepairSourceContextConfidenceLevel}


def test_required_models_are_exported():
    for model in (
        RepairSourceContextFlagSet,
        RepairSourceContextSourceRef,
        RepairSourceContextPolicy,
        RepairSandboxRootValidationReport,
        RepairSourceContextRequest,
        RepairSourcePathCandidate,
        RepairSourcePathValidationResult,
        RepairSourceReadDecision,
        RepairSourceFileSnapshot,
        RepairSourceExcerpt,
        RepairSymbolContextHint,
        RepairSourceContextAssessment,
        RepairSourceContextSnapshot,
        RepairSourceContextValidationFinding,
        RepairSourceContextValidationReport,
        RepairSourceContextReport,
        RepairSourceContextRunPreview,
        RepairSourceContextNoMutationGuarantee,
        V0382ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_read_only_sandbox_readiness_and_preserve_no_mutation():
    flags = build_repair_source_context_flags()
    assert flags.repair_source_context_layer_constructed
    assert flags.source_context_policy_available
    assert flags.sandbox_root_validation_available
    assert flags.source_path_validation_available
    assert flags.bounded_source_snapshot_available
    assert flags.bounded_source_excerpt_available
    assert flags.symbol_context_hint_available
    assert flags.source_context_assessment_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert repair_source_context_flags_preserve_no_mutation(flags)
    for name in _unsafe_flag_names(RepairSourceContextFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairSourceContextFlagSet) + ["production_certified"])
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_source_context_flags(**{field_name: True})


def test_policy_allows_bounded_read_only_sandbox_source_and_blocks_unsafe():
    policy = default_repair_source_context_policy()
    assert policy.allow_sandbox_root_validation
    assert policy.allow_explicit_relative_path_candidates
    assert policy.allow_bounded_read_only_sandbox_source_read
    assert policy.allow_bounded_source_snapshot
    assert policy.allow_bounded_source_excerpt
    assert policy.allow_symbol_context_hint
    assert policy.allow_future_scope_planning_input
    assert policy.allow_future_patch_metadata_input
    assert repair_source_context_policy_blocks_live_and_unbounded_read(policy)
    for name in (
        "allow_live_workspace_read",
        "allow_unbounded_source_read",
        "allow_reference_source_read",
        "allow_secret_read",
        "allow_source_file_write",
        "allow_sandbox_source_write",
        "allow_repair_proposal_generation",
        "allow_proposed_diff_generation",
        "allow_proposed_code_hunk_generation",
        "allow_proposed_patch_envelope_generation",
        "allow_repair_execution",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_repair_source_context_policy(**{name: True})


def test_valid_and_invalid_sandbox_root_validation(tmp_path):
    root, _target = _root_and_file(tmp_path)
    valid = validate_repair_sandbox_root(root)
    assert valid.valid_for_read_only_context
    assert valid.root_exists
    assert valid.root_is_directory
    missing = validate_repair_sandbox_root(tmp_path / "missing")
    assert missing.valid_for_read_only_context is False
    non_dir = tmp_path / "file.txt"
    non_dir.write_text("x", encoding="utf-8")
    assert validate_repair_sandbox_root(non_dir).valid_for_read_only_context is False
    live = tmp_path / "live"
    (live / ".git").mkdir(parents=True)
    assert validate_repair_sandbox_root(live).valid_for_read_only_context is False
    ref = tmp_path / "references" / "OpenCode"
    ref.mkdir(parents=True)
    assert validate_repair_sandbox_root(ref).valid_for_read_only_context is False


def test_source_context_request_requires_explicit_relative_paths(tmp_path):
    request = build_repair_source_context_request_from_evidence_bundle(
        sandbox_root_ref=str(tmp_path),
        path_candidates=["pkg/module.py"],
    )
    assert request.path_candidates == ["pkg/module.py"]
    required = {
        "live_read",
        "unbounded_read",
        "reference_read",
        "secret_read",
        "file_write",
        "proposal_generation",
        "diff_generation",
        "hunk_generation",
        "patch_apply",
        "repair_execution",
        "test_execution",
        "subprocess",
        "shell",
        "dependency_install",
        "network",
        "model_provider",
        "external_agent",
        "dominion",
    }
    assert required.issubset(set(request.prohibited_runtime_actions))
    with pytest.raises(ValueError):
        build_repair_source_context_request(path_candidates=[str(tmp_path / "absolute.py")])
    with pytest.raises(ValueError):
        build_repair_source_context_request(path_candidates=["../escape.py"])


def test_path_candidate_and_file_kind_classification():
    candidate = build_repair_source_path_candidate(raw_path="pkg/module.py")
    assert candidate.normalized_relative_path == "pkg/module.py"
    assert candidate.file_kind == RepairSourceFileKind.PYTHON_SOURCE
    assert normalize_repair_source_relative_path("../x.py") is None
    assert classify_repair_source_file_kind("test_example.py") == RepairSourceFileKind.TEST_SOURCE
    assert classify_repair_source_file_kind(".env") == RepairSourceFileKind.SECRET_LIKE
    assert classify_repair_source_file_kind("asset.png") == RepairSourceFileKind.BINARY


def test_path_validation_accepts_explicit_relative_path(tmp_path):
    root, _target = _root_and_file(tmp_path)
    root_validation = validate_repair_sandbox_root(root)
    candidate = build_repair_source_path_candidate(raw_path="pkg/module.py")
    result = validate_repair_source_path_candidate(root_validation, candidate)
    assert result.disposition == RepairSourcePathDisposition.ACCEPTED
    assert result.read_allowed
    assert result.is_inside_sandbox_root
    decision = decide_repair_source_read(result)
    assert decision.read_allowed
    assert decision.source_read_performed is False
    for name in (
        "live_workspace_read_allowed",
        "reference_read_allowed",
        "secret_read_allowed",
        "write_allowed",
        "proposal_generation_allowed",
        "diff_generation_allowed",
        "hunk_generation_allowed",
        "repair_execution_allowed",
    ):
        assert getattr(decision, name) is False


@pytest.mark.parametrize(
    ("raw_path", "expected_disposition"),
    [
        (r"C:\outside.py", RepairSourcePathDisposition.DENIED_ABSOLUTE_PATH),
        ("../outside.py", RepairSourcePathDisposition.DENIED_PARENT_TRAVERSAL),
        ("references/OpenCode/file.py", RepairSourcePathDisposition.DENIED_REFERENCE_PATH),
        (".git/config", RepairSourcePathDisposition.DENIED_SECRET_PATH),
        (".env", RepairSourcePathDisposition.DENIED_SECRET_PATH),
        ("secret_token.py", RepairSourcePathDisposition.DENIED_SECRET_PATH),
        ("asset.png", RepairSourcePathDisposition.DENIED_BINARY),
        ("missing.py", RepairSourcePathDisposition.DENIED_MISSING_FILE),
        ("pkg", RepairSourcePathDisposition.DENIED_DIRECTORY),
        ("pkg/module.bin2", RepairSourcePathDisposition.DENIED_UNSUPPORTED_EXTENSION),
    ],
)
def test_path_validation_denies_unsafe_paths(tmp_path, raw_path, expected_disposition):
    root, _target = _root_and_file(tmp_path)
    (root / "references" / "OpenCode").mkdir(parents=True)
    (root / "references" / "OpenCode" / "file.py").write_text("x", encoding="utf-8")
    (root / ".git").mkdir()
    (root / ".git" / "config").write_text("x", encoding="utf-8")
    (root / ".env").write_text("TOKEN=x", encoding="utf-8")
    (root / "secret_token.py").write_text("x", encoding="utf-8")
    (root / "asset.png").write_bytes(b"\x89PNG")
    (root / "pkg" / "module.bin2").write_text("x", encoding="utf-8")
    root_validation = build_repair_sandbox_root_validation_report(sandbox_root_ref=str(root))
    candidate = build_repair_source_path_candidate(raw_path=raw_path)
    result = validate_repair_source_path_candidate(root_validation, candidate)
    assert result.disposition == expected_disposition
    assert result.read_allowed is False
    assert repair_source_path_validation_blocks_escape(result)


def test_path_validation_denies_symlink_escape(tmp_path):
    root, _target = _root_and_file(tmp_path)
    outside = tmp_path / "outside.py"
    outside.write_text("x", encoding="utf-8")
    link = root / "pkg" / "linked.py"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable on this platform")
    root_validation = validate_repair_sandbox_root(root)
    result = validate_repair_source_path_candidate(root_validation, build_repair_source_path_candidate(raw_path="pkg/linked.py"))
    assert result.disposition == RepairSourcePathDisposition.DENIED_SYMLINK
    assert result.read_allowed is False


def test_path_validation_denies_oversized_file(tmp_path):
    root, _target = _root_and_file(tmp_path)
    (root / "pkg" / "big.py").write_text("x" * 50, encoding="utf-8")
    policy = build_repair_source_context_policy(max_file_bytes=10)
    result = validate_repair_source_path_candidate(
        validate_repair_sandbox_root(root),
        build_repair_source_path_candidate(raw_path="pkg/big.py"),
        policy,
    )
    assert result.disposition == RepairSourcePathDisposition.DENIED_OVERSIZED
    assert result.read_allowed is False


def test_bounded_snapshot_excerpt_redaction_and_symbol_hint(tmp_path):
    root, _target = _root_and_file(tmp_path)
    root_validation = validate_repair_sandbox_root(root)
    policy = build_repair_source_context_policy(max_total_snapshot_chars=120, max_excerpt_chars=120)
    validation = validate_repair_source_path_candidate(root_validation, build_repair_source_path_candidate(raw_path="pkg/module.py"), policy)
    preview, redacted, truncated, digest, file_size = read_bounded_read_only_sandbox_source_file(root_validation, validation, policy)
    assert "should-not-leak" not in preview
    assert "[REDACTED]" in preview
    assert redacted
    assert digest
    assert file_size is not None
    snapshot = create_repair_source_file_snapshot(root_validation, validation, policy)
    assert repair_source_snapshot_is_not_proposal(snapshot)
    assert snapshot.source_read_performed
    assert snapshot.write_performed is False
    assert snapshot.redacted
    excerpts = create_repair_source_excerpts(snapshot, policy)
    assert excerpts
    assert all(len(excerpt.excerpt_text) <= policy.max_excerpt_chars for excerpt in excerpts)
    assert excerpts[0].redacted
    assert excerpts[0].secret_like_content_detected
    hints = create_repair_symbol_context_hints(excerpts, ["target_function"])
    assert hints
    assert hints[0].symbol_name == "target_function"
    assert hints[0].imported_or_executed_source is False
    with pytest.raises(ValueError):
        build_repair_symbol_context_hint(imported_or_executed_source=True)


def test_context_assessment_and_snapshot_readiness(tmp_path):
    root, _target = _root_and_file(tmp_path)
    request = build_repair_source_context_request(
        sandbox_root_ref=str(root),
        path_candidates=["pkg/module.py"],
        requested_symbols=["target_function"],
    )
    snapshot = create_repair_source_context_snapshot(request)
    assert snapshot.file_snapshots
    assert snapshot.source_excerpts
    assert snapshot.symbol_context_hints
    assert snapshot.context_assessment.sufficient_for_future_scope_planning
    assert snapshot.context_assessment.do_nothing_remains_valid
    assert snapshot.ready_for_future_scope_planning_input
    assert snapshot.ready_for_future_patch_metadata_input
    assert repair_source_context_snapshot_is_not_generation(snapshot)
    for name in (
        "live_workspace_read_performed",
        "reference_source_read_performed",
        "secret_read_performed",
        "unbounded_read_performed",
        "write_performed",
        "proposal_generated",
        "diff_generated",
        "hunk_generated",
        "patch_envelope_generated",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ):
        assert getattr(snapshot, name) is False
    validation_report = validate_repair_source_context_snapshot(snapshot)
    assert validation_report.sandbox_root_validation_confirmed
    report = build_repair_source_context_report(snapshot=snapshot, validation_report=validation_report)
    assert report.ready_for_execution is False
    assert report.production_certified is False


def test_context_assessment_insufficient_for_missing_or_denied_context():
    assessment = assess_repair_source_context([], [], [], ["denied.py"])
    assert assessment.sufficient_for_future_scope_planning is False
    assert assessment.sufficient_for_future_patch_metadata is False
    assert assessment.do_nothing_remains_valid
    with pytest.raises(ValueError):
        build_repair_source_context_assessment(
            sufficiency_kind=RepairSourceContextSufficiencyKind.INSUFFICIENT_DENIED_PATHS,
            sufficient_for_future_scope_planning=True,
        )
    with pytest.raises(ValueError):
        build_repair_source_context_snapshot(
            context_assessment=assessment,
            ready_for_future_scope_planning_input=True,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "live_workspace_read_performed",
        "reference_source_read_performed",
        "secret_read_performed",
        "unbounded_read_performed",
        "write_performed",
        "proposal_generated",
        "diff_generated",
        "hunk_generated",
        "patch_envelope_generated",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ],
)
def test_snapshot_rejects_unsafe_state_true(field_name):
    with pytest.raises(ValueError):
        build_repair_source_context_snapshot(**{field_name: True})


def test_reports_preview_no_mutation_guarantee_and_readiness():
    finding = build_repair_source_context_validation_finding()
    validation = build_repair_source_context_validation_report(findings=[finding])
    assert validation.no_live_workspace_read_confirmed
    assert validation.no_reference_read_confirmed
    assert validation.no_secret_read_confirmed
    assert validation.no_unbounded_read_confirmed
    assert validation.no_write_confirmed
    assert validation.no_proposal_generation_confirmed
    assert validation.no_diff_generation_confirmed
    assert validation.no_hunk_generation_confirmed
    assert validation.no_patch_envelope_generation_confirmed
    assert validation.no_repair_execution_confirmed
    preview = build_repair_source_context_run_preview()
    assert preview.would_validate_root
    assert preview.would_read_bounded_sandbox_source
    assert preview.would_read_live_workspace is False
    assert preview.would_generate_diff is False
    guarantee = build_repair_source_context_no_mutation_guarantee()
    for field in fields(RepairSourceContextNoMutationGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    report = build_v0382_readiness_report()
    assert report.ready_for_v0383_repair_scope_planner_change_intent
    assert report.ready_for_v0384_proposed_diff_code_hunk_metadata
    assert report.ready_for_read_only_sandbox_source_context
    assert report.ready_for_validated_sandbox_root_context
    assert report.ready_for_validated_read_only_sandbox_source_read
    assert report.ready_for_sandbox_source_read
    assert report.ready_for_source_context_snapshot
    assert report.ready_for_bounded_source_excerpt
    assert report.ready_for_source_path_validation
    assert report.ready_for_source_context_redaction
    assert report.ready_for_symbol_context_hint
    assert report.ready_for_source_context_sufficiency_assessment
    assert report.ready_for_future_repair_scope_planning_input
    assert report.ready_for_future_change_intent_input
    assert report.ready_for_future_proposed_diff_metadata_input
    assert report.ready_for_future_proposed_code_hunk_metadata_input
    assert v0382_readiness_report_is_not_execution_ready(report)
    for name in _unsafe_flag_names(V0382ReadinessReport) + ["production_certified"]:
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0382_readiness_report(**{name: True})


def test_helpers_do_not_contain_forbidden_runtime_patterns():
    import chanta_core.agent_runtime.repair_source_context as module

    source = inspect.getsource(module)
    forbidden = [
        "os.walk",
        ".rglob(",
        ".glob(",
        "write_text",
        "write_bytes",
        "open(",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "apply_patch(",
    ]
    for pattern in forbidden:
        assert pattern not in source

import subprocess
import sys
from dataclasses import replace

from chanta_core.deep_self_introspection import (
    ContextProjectionBudgetService,
    ContextProjectionGapService,
    ContextProjectionItem,
    ContextProjectionItemService,
    ContextProjectionSourceRef,
    ContextProjectionSourceService,
    SelfCapabilityRegistryAwarenessService,
    SelfContextProjectionAwarenessService,
    SelfContextProjectionViewRequest,
)


def _source(source_id: str, source_type: str = "ocpx_read_model", status: str = "included", freshness: str = "fresh"):
    return ContextProjectionSourceRef(
        source_id=source_id,
        source_type=source_type,
        source_ref={"ref_id": source_id.removeprefix("source:"), "updated_at": "2026-05-16T00:00:00Z"},
        source_status=status,
        freshness_status=freshness,
        evidence_refs=[{"source_id": source_id, "read_only": True}],
    )


def _safe_sources():
    return [
        _source("source:capability_truth"),
        _source("source:runtime_boundary"),
        _source("source:policy_gate"),
        _source("source:trace_integrity"),
        _source("source:candidate_memory_boundary", "candidate"),
        _source("source:ocpx_projection"),
        _source("source:pig_diagnostic", "pig_report"),
        _source("source:self_awareness_release", "workbench_snapshot"),
    ]


def _service(sources=None):
    return SelfContextProjectionAwarenessService(source_service=ContextProjectionSourceService(sources=sources or _safe_sources()))


def _finding_types(report):
    return {item.finding_type for item in report.findings}


def _gap_types(snapshot):
    return {item.gap_type for item in snapshot.gaps}


def _bad_item(**overrides):
    base = ContextProjectionItem(
        item_id="context_projection_item:bad",
        item_type="candidate_summary",
        source_id="source:candidate",
        projection_role="primary_context",
        content_kind="structured_state",
        canonical_truth=True,
        candidate_only=True,
        stale=False,
        truncated=False,
        redacted=True,
        evidence_refs=[{"source_id": "source:candidate"}],
        limitations=[],
    )
    return replace(base, **overrides)


def test_context_projection_snapshot_builds_and_default_report_is_read_only() -> None:
    service = SelfContextProjectionAwarenessService()
    snapshot = service.view_context_projection()
    report = service.truth_check()

    assert snapshot.snapshot_id
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.sources
    assert snapshot.projected_items
    assert snapshot.budget.projected_item_count == len(snapshot.projected_items)
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.projection_truth_summary["context_injection_performed"] is False
    assert report.projection_truth_summary["memory_promotion_performed"] is False
    assert report.projection_truth_summary["raw_transcript_is_process_state"] is False


def test_safe_projection_truth_check_passes() -> None:
    report = _service().truth_check()

    assert report.status == "passed"
    assert report.candidate_as_canonical_count == 0
    assert report.raw_transcript_as_state_count == 0
    assert report.private_payload_risk_count == 0


def test_sources_include_ocpx_pig_workbench_and_candidate_refs_without_raw_transcript() -> None:
    snapshot = _service().view_context_projection()
    source_types = {source.source_type for source in snapshot.sources}
    content_kinds = {item.content_kind for item in snapshot.projected_items}

    assert "ocpx_read_model" in source_types
    assert "pig_report" in source_types
    assert "workbench_snapshot" in source_types
    assert "candidate" in source_types
    assert "raw_transcript" not in content_kinds


def test_projected_items_have_required_projection_flags() -> None:
    snapshot = _service().view_context_projection()

    assert snapshot.projected_items
    for item in snapshot.projected_items:
        assert item.source_id
        assert item.projection_role
        assert item.content_kind
        assert isinstance(item.canonical_truth, bool)
        assert isinstance(item.candidate_only, bool)
        assert isinstance(item.stale, bool)
        assert isinstance(item.truncated, bool)
        assert isinstance(item.redacted, bool)
        assert item.evidence_refs
        assert item.limitations
        if item.candidate_only:
            assert item.canonical_truth is False
        if item.projection_role == "summary_context":
            assert item.canonical_truth is False


def test_missing_truth_sources_create_gaps() -> None:
    required_gap_types = {
        "missing_capability_truth",
        "missing_runtime_boundary",
        "missing_policy_gate",
        "missing_trace_integrity",
        "missing_candidate_memory_boundary",
        "missing_ocpx_projection",
        "missing_pig_diagnostic",
    }
    for gap_type in required_gap_types:
        missing_source = ContextProjectionGapService.REQUIRED[gap_type]
        sources = [source for source in _safe_sources() if source.source_id != missing_source]
        snapshot = _service(sources).view_context_projection()
        assert gap_type in _gap_types(snapshot)


def test_freshness_and_budget_descriptors_report_stale_omitted_compacted_and_truncated_state() -> None:
    sources = [
        _source("source:capability_truth", freshness="stale"),
        _source("source:runtime_boundary", status="omitted"),
        _source("source:policy_gate", status="compacted"),
    ]
    service = _service(sources)
    snapshot = service.view_context_projection(SelfContextProjectionViewRequest(max_items=2))
    truncated_items = [replace(snapshot.projected_items[0], truncated=True, limitations=["truncation_marked"])]
    budget = ContextProjectionBudgetService().describe_budget(snapshot.request, truncated_items, sources)

    assert any(item.stale for item in snapshot.freshness)
    assert budget.omitted_item_count == 1
    assert budget.compacted_item_count == 1
    assert budget.truncated_item_count == 1
    assert budget.budget_status in {"near_limit", "exceeded"}


def test_projection_gap_and_truth_failures_cover_candidate_raw_private_and_truncation_risks() -> None:
    bad_items = [
        _bad_item(),
        _bad_item(item_id="context_projection_item:raw", candidate_only=False, canonical_truth=False, content_kind="raw_transcript"),
        _bad_item(item_id="context_projection_item:private", candidate_only=False, canonical_truth=False, content_kind="private_payload"),
        _bad_item(item_id="context_projection_item:truncated", candidate_only=False, canonical_truth=False, truncated=True),
    ]

    class BadItemService(ContextProjectionItemService):
        def build_projected_items(self, sources):
            return bad_items

    service = SelfContextProjectionAwarenessService(
        source_service=ContextProjectionSourceService(sources=_safe_sources()),
        item_service=BadItemService(),
    )
    report = service.truth_check()
    findings = _finding_types(report)

    assert report.status == "failed"
    assert report.candidate_as_canonical_count == 1
    assert report.raw_transcript_as_state_count == 1
    assert report.private_payload_risk_count == 1
    assert "candidate_memory_confusion" in findings
    assert "raw_transcript_as_state" in findings
    assert "private_payload_projection_risk" in findings
    assert "projection_truncation_unmarked" in findings


def test_projection_limitations_detect_runtime_capability_policy_and_trace_contradictions() -> None:
    risky_items = [
        _bad_item(candidate_only=False, canonical_truth=False, limitations=["exceeds_runtime_boundary"]),
        _bad_item(item_id="context_projection_item:capability", candidate_only=False, canonical_truth=False, limitations=["exceeds_capability_truth"]),
        _bad_item(item_id="context_projection_item:policy", candidate_only=False, canonical_truth=False, limitations=["ignores_policy_gate"]),
        _bad_item(item_id="context_projection_item:trace", candidate_only=False, canonical_truth=False, limitations=["ignores_trace_integrity_failure"]),
    ]

    class RiskyItemService(ContextProjectionItemService):
        def build_projected_items(self, sources):
            return risky_items

    report = SelfContextProjectionAwarenessService(
        source_service=ContextProjectionSourceService(sources=_safe_sources()),
        item_service=RiskyItemService(),
    ).truth_check()
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "projection_exceeds_runtime_boundary" in findings
    assert "projection_exceeds_capability_truth" in findings
    assert "projection_ignores_policy_gate" in findings
    assert "projection_ignores_trace_integrity_failure" in findings


def test_optional_source_omission_warns_without_becoming_implicit_allow() -> None:
    report = SelfContextProjectionAwarenessService().truth_check()

    assert report.status == "warning"
    assert "missing_truth_source" in _finding_types(report)


def test_context_projection_skills_are_implemented_and_remaining_seed_skills_are_contract_only() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    records = {record.skill_id: record for record in snapshot.records if record.skill_id}

    assert records["skill:deep_self_context_projection_view"].status == "implemented"
    assert records["skill:deep_self_context_projection_gap_report"].status == "implemented"
    assert records["skill:deep_self_trace_integrity_check"].status == "implemented"
    assert records["skill:deep_self_candidate_memory_boundary_report"].status == "implemented"
    assert records["skill:deep_self_promotion_boundary_check"].status == "implemented"
    assert records["skill:deep_self_claim_consistency_check"].status == "implemented"
    assert records["skill:deep_self_context_projection_view"].read_only is True
    assert records["skill:deep_self_context_projection_gap_report"].execution_enabled is False


def test_pig_and_ocpx_projection_build() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.5"
    assert pig["subject"] == "context_projection"
    assert "context projection awareness is not context injection" in pig["principles"]
    assert "projection view is not canonical truth" in pig["principles"]
    assert "raw transcript is not process-state" in pig["principles"]
    assert "candidate-only must not appear as canonical memory" in pig["principles"]
    assert pig["checks_sources"] is True
    assert pig["checks_freshness"] is True
    assert pig["checks_budget"] is True
    assert pig["checks_candidate_memory_confusion"] is True
    assert pig["uses_raw_transcript_as_state"] is False
    assert pig["mutates_projection"] is False
    assert pig["promotes_memory"] is False
    assert ocpx["state"] == "self_context_projection_awareness"
    assert "SelfContextProjectionState" in ocpx["target_read_models"]
    assert "SelfProjectionRiskState" in ocpx["target_read_models"]


def test_cli_context_projection_views_work() -> None:
    commands = [
        ["deep-self", "context", "projection"],
        ["deep-self", "context", "projection", "--scope", "deep_self"],
        ["deep-self", "context", "projection", "--scope", "self_awareness"],
        ["deep-self", "context", "truth-check"],
        ["deep-self", "context", "sources"],
        ["deep-self", "context", "items"],
        ["deep-self", "context", "gaps"],
        ["deep-self", "context", "freshness"],
        ["deep-self", "context", "budget"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Self-Context Projection Awareness" in result.stdout
        assert "No context injection performed." in result.stdout
        assert "No memory promotion performed." in result.stdout
        assert "raw_prompt_body_printed=False" in result.stdout
        assert "raw_transcript_printed=False" in result.stdout
        assert "private_full_paths_printed=False" in result.stdout

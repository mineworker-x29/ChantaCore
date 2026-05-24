import subprocess
import sys
from dataclasses import replace

from chanta_core.deep_self_introspection import (
    CandidateLineageVerifier,
    EnvelopeOCELConsistencyVerifier,
    EventObjectCoverageVerifier,
    ObjectRelationIntegrityVerifier,
    ProcessChainIntegrityVerifier,
    SelfCapabilityRegistryAwarenessService,
    SelfTraceIntegrityAwarenessService,
    SelfTraceIntegrityRequest,
    TraceIntegritySourceService,
)


def _events():
    return [
        {
            "event_id": "evt:1",
            "event_activity": "self_awareness_ecosystem_snapshot_created",
            "event_attrs": {
                "envelope_id": "env:1",
                "required_object_types": ["execution_envelope"],
            },
        },
        {"event_id": "evt:2", "event_activity": "self_awareness_release_manifest_created", "event_attrs": {}},
        {"event_id": "evt:3", "event_activity": "self_awareness_consolidation_report_created", "event_attrs": {}},
    ]


def _objects():
    return [{"object_id": "obj:envelope", "object_type": "execution_envelope"}]


def _relations():
    return [
        {
            "relation_kind": "event_object",
            "source_id": "evt:1",
            "target_id": "obj:envelope",
            "qualifier": "execution_envelope_object",
        }
    ]


def _envelopes():
    return [
        {
            "envelope_id": "env:1",
            "skill_id": "skill:deep_self_trace_integrity_check",
            "blocked": False,
            "envelope_attrs": {"event_id": "evt:1", "effect_types": ["read_only_observation"]},
        }
    ]


def _candidates():
    return [
        {
            "candidate_id": "candidate:1",
            "candidate_type": "summary_candidate",
            "source_refs": [
                {"ref_type": "event", "ref_id": "evt:1"},
                {"ref_type": "object", "ref_id": "obj:envelope"},
            ],
            "evidence_refs": [{"source": "ocel"}],
            "verification_ref": "verification:1",
        }
    ]


def _service(**overrides):
    source = TraceIntegritySourceService(
        events=overrides.get("events", _events()),
        objects=overrides.get("objects", _objects()),
        relations=overrides.get("relations", _relations()),
        envelopes=overrides.get("envelopes", _envelopes()),
        candidates=overrides.get("candidates", _candidates()),
        source_available=overrides.get("source_available", True),
        uses_jsonl_as_canonical=overrides.get("uses_jsonl_as_canonical", False),
    )
    return SelfTraceIntegrityAwarenessService(source_service=source)


def _finding_types(report):
    return {item.finding_type for item in report.findings}


def test_trace_integrity_report_builds_and_passes_for_clean_trace() -> None:
    report = _service().check_trace_integrity()
    snapshot = _service().build_snapshot(SelfTraceIntegrityRequest())

    assert report.status == "passed"
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False


def test_source_service_reads_owner_shapes_without_jsonl_canonical() -> None:
    source = TraceIntegritySourceService(events=_events(), objects=_objects(), relations=_relations())
    request = SelfTraceIntegrityRequest()

    assert source.load_ocel_events(request)
    assert source.load_ocel_objects(request)
    assert source.load_ocel_relations(request)
    assert source.uses_jsonl_as_canonical is False


def test_envelope_link_checks_detect_missing_and_ambiguous_links() -> None:
    report = _service(envelopes=[{"envelope_id": "env:missing", "envelope_attrs": {"event_id": "evt:missing"}}]).check_trace_integrity()
    assert "missing_ocel_event" in _finding_types(report)

    events = _events() + [{"event_id": "evt:extra", "event_activity": "x", "event_attrs": {"envelope_id": "env:1"}}]
    report = _service(events=events).check_trace_integrity()
    assert "missing_envelope_link" in _finding_types(report)


def test_event_requiring_envelope_and_blocked_attempt_create_findings() -> None:
    events = [{"event_id": "evt:blocked", "event_activity": "blocked", "event_attrs": {"blocked": True, "requires_envelope": True}}]
    report = _service(events=events, objects=[], relations=[], envelopes=[], candidates=[]).check_trace_integrity(
        SelfTraceIntegrityRequest(include_process_chain_checks=False)
    )
    assert "blocked_attempt_not_enveloped" in _finding_types(report)


def test_event_object_coverage_and_relation_integrity_find_gaps() -> None:
    event_report = _service(relations=[]).check_trace_integrity()
    assert "missing_required_object" in _finding_types(event_report)

    relations = _relations() + [
        {"relation_kind": "object_object", "source_id": "obj:envelope", "target_id": "obj:missing", "qualifier": "links_to"},
        {"relation_kind": "object_object", "source_id": "obj:envelope", "target_id": "obj:missing", "qualifier": "links_to"},
    ]
    relation_report = _service(relations=relations).check_trace_integrity()
    findings = _finding_types(relation_report)
    assert "dangling_object_relation" in findings
    assert "duplicate_relation" in findings


def test_candidate_lineage_findings_cover_missing_source_evidence_and_verification() -> None:
    report = _service(candidates=[{"candidate_id": "candidate:bad", "candidate_type": "state_candidate_created"}]).check_trace_integrity()
    findings = _finding_types(report)

    assert "missing_candidate_source" in findings
    assert "missing_candidate_evidence" in findings
    assert "missing_verification_ref" in findings
    assert "state_candidate_without_source" in findings

    no_action = [{"candidate_id": "candidate:no_action", "candidate_type": "no_action", "source_refs": [{"ref_type": "event", "ref_id": "evt:1"}], "evidence_refs": [{"source": "operator"}]}]
    report = _service(candidates=no_action).check_trace_integrity()
    assert "no_action_candidate_without_policy_ref" in _finding_types(report)


def test_process_chain_status_and_unsupported_scope_rules() -> None:
    complete = _service().check_trace_integrity()
    assert complete.status == "passed"

    broken = _service(events=_events()[:1]).check_trace_integrity()
    assert "trace_chain_broken" in _finding_types(broken)

    blocked = _service().check_trace_integrity(SelfTraceIntegrityRequest(scope="unsupported"))
    assert blocked.status == "blocked"


def test_jsonl_canonical_and_effect_type_mismatch_fail_report() -> None:
    jsonl_report = _service(uses_jsonl_as_canonical=True).check_trace_integrity()
    assert "jsonl_canonical_leak" in _finding_types(jsonl_report)

    events = [
        {
            "event_id": "evt:1",
            "event_activity": "self_awareness_ecosystem_snapshot_created",
            "event_attrs": {"required_object_types": ["execution_envelope"], "effect_types": ["mutation"]},
        }
    ]
    report = _service(events=events, relations=[]).check_trace_integrity(SelfTraceIntegrityRequest(include_process_chain_checks=False))
    assert "effect_type_mismatch" in _finding_types(report)


def test_verifier_classes_are_importable_and_read_only() -> None:
    assert EnvelopeOCELConsistencyVerifier()
    assert EventObjectCoverageVerifier()
    assert ObjectRelationIntegrityVerifier()
    assert CandidateLineageVerifier()
    assert ProcessChainIntegrityVerifier()


def test_trace_integrity_skills_are_implemented_and_remaining_seed_skills_are_contract_only() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    by_skill = {item.skill_id: item for item in snapshot.records if item.skill_id}

    assert by_skill["skill:deep_self_trace_integrity_check"].status == "implemented"
    assert by_skill["skill:deep_self_envelope_ocel_consistency"].status == "implemented"
    assert by_skill["skill:deep_self_context_projection_view"].status == "implemented"
    assert by_skill["skill:deep_self_context_projection_gap_report"].status == "implemented"
    assert by_skill["skill:deep_self_candidate_memory_boundary_report"].status == "implemented"
    assert by_skill["skill:deep_self_promotion_boundary_check"].status == "implemented"
    assert by_skill["skill:deep_self_claim_consistency_check"].status == "implemented"
    assert by_skill["skill:deep_self_trace_integrity_check"].execution_enabled is False


def test_pig_and_ocpx_projection_build() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.4"
    assert pig["subject"] == "trace_integrity"
    assert "trace integrity awareness is not trace repair" in pig["principles"]
    assert pig["repairs_trace"] is False
    assert pig["rewrites_events"] is False
    assert pig["uses_jsonl_as_canonical"] is False
    assert ocpx["state"] == "self_trace_integrity_awareness"
    assert "SelfTraceIntegrityState" in ocpx["target_read_models"]
    assert "SelfEnvelopeOCELLinkState" in ocpx["target_read_models"]


def test_cli_trace_integrity_views_work() -> None:
    commands = [
        ["deep-self", "trace", "integrity"],
        ["deep-self", "trace", "integrity", "--scope", "self_awareness"],
        ["deep-self", "trace", "integrity", "--scope", "deep_self"],
        ["deep-self", "trace", "envelope-links"],
        ["deep-self", "trace", "event-object-coverage"],
        ["deep-self", "trace", "candidate-lineage"],
        ["deep-self", "trace", "process-chain"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Self-Trace Integrity Awareness" in result.stdout
        assert "No repair performed." in result.stdout
        assert "raw_file_content_printed=False" in result.stdout
        assert "private_full_paths_printed=False" in result.stdout

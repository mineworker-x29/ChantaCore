from chanta_core.observation_digest.models import (
    AgentObservationBatch,
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
    ObservationDigestionFinding,
    ObservationDigestionResult,
)
from chanta_core.utility.time import utc_now_iso


def test_observation_digest_shared_models_to_dict_and_confidence_clamp():
    batch = AgentObservationBatch(
        batch_id="batch:demo",
        source_id="source:demo",
        input_format="generic_jsonl",
        raw_record_count=2,
        normalized_event_count=2,
        status="completed",
        confidence=3.0,
        created_at=utc_now_iso(),
    )
    finding = ObservationDigestionFinding(
        finding_id="finding:demo",
        subject_ref="batch:demo",
        finding_type="low_confidence",
        status="warning",
        severity="medium",
        message="Demo finding.",
        evidence_ref="evidence:demo",
        created_at=utc_now_iso(),
    )
    result = ObservationDigestionResult(
        result_id="result:demo",
        operation_kind="demo",
        subject_ref="batch:demo",
        status="completed",
        created_object_refs=["batch:demo"],
        finding_ids=["finding:demo"],
        summary="Demo result.",
        created_at=utc_now_iso(),
    )

    assert batch.confidence == 1.0
    assert batch.to_dict()["batch_id"] == "batch:demo"
    assert finding.to_dict()["finding_type"] == "low_confidence"
    assert result.to_dict()["created_object_refs"] == ["batch:demo"]


def test_external_candidate_defaults_are_non_executable():
    candidate = ExternalSkillAssimilationCandidate(
        candidate_id="candidate:demo",
        source_runtime="dummy_runtime",
        source_skill_ref="dummy_skill",
        source_kind="external_skill",
        static_profile_id=None,
        behavior_fingerprint_id=None,
        proposed_chantacore_skill_id="skill:dummy_skill",
        proposed_execution_type="review_only_candidate",
        adapter_candidate_ids=[],
        risk_class="read_only",
        confidence=0.5,
        evidence_refs=[],
        created_at=utc_now_iso(),
    )
    adapter = ExternalSkillAdapterCandidate(
        adapter_candidate_id="adapter:demo",
        source_skill_ref="dummy_skill",
        target_skill_id="skill:dummy_skill",
        mapping_type="static_review_candidate",
        mapping_confidence=0.5,
        required_input_mapping={},
        output_mapping={},
        unsupported_features=["execution"],
        created_at=utc_now_iso(),
    )

    assert candidate.review_status == "pending_review"
    assert candidate.canonical_import_enabled is False
    assert candidate.execution_enabled is False
    assert adapter.requires_review is True
    assert adapter.execution_enabled is False

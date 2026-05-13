from chanta_core.observation_digest.history_adapter import (
    behavior_inferences_to_history_entries,
    external_skill_adapter_candidates_to_history_entries,
    external_skill_assimilation_candidates_to_history_entries,
    observation_digestion_findings_to_history_entries,
    observation_sources_to_history_entries,
)
from chanta_core.observation_digest.models import (
    AgentBehaviorInference,
    AgentObservationSource,
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
    ObservationDigestionFinding,
)
from chanta_core.utility.time import utc_now_iso


def test_observation_digest_history_entries_have_expected_source_and_priority():
    created_at = utc_now_iso()
    source = AgentObservationSource(
        source_id="source:demo",
        source_name="demo",
        source_kind="trace_file",
        source_runtime="dummy_runtime",
        source_version=None,
        source_format="generic_jsonl",
        location_ref="trace.jsonl",
        collection_mode="read_only_file_inspection",
        trusted=False,
        private=False,
        created_at=created_at,
    )
    inference = AgentBehaviorInference(
        inference_id="inference:demo",
        observed_run_id="run:demo",
        inferred_goal="observe_trace",
        inferred_goal_confidence=0.5,
        inferred_task_type="trace_observation",
        inferred_action_sequence=["user_message_observed"],
        inferred_skill_sequence=[],
        inferred_tool_sequence=[],
        touched_object_types=[],
        outcome_inference="observed_without_explicit_failure",
        outcome_confidence=0.5,
        confirmed_observations=["one event"],
        data_based_interpretations=["one event observed"],
        likely_hypotheses=["goal inferred from order"],
        estimates=["event_count_estimate=1"],
        unknown_or_needs_verification=["runtime semantics"],
        failure_signals=[],
        recovery_signals=[],
        evidence_refs=["evidence:demo"],
        uncertainty_notes=["static inference"],
        withdrawal_conditions=["new evidence contradicts sequence"],
        created_at=created_at,
    )
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
        created_at=created_at,
    )
    adapter = ExternalSkillAdapterCandidate(
        adapter_candidate_id="adapter:demo",
        source_skill_ref="dummy_skill",
        target_skill_id="skill:dummy_skill",
        mapping_type="static_review_candidate",
        mapping_confidence=0.5,
        required_input_mapping={},
        output_mapping={},
        unsupported_features=[],
        created_at=created_at,
    )
    finding = ObservationDigestionFinding(
        finding_id="finding:demo",
        subject_ref="source:demo",
        finding_type="private_content_risk",
        status="blocked",
        severity="high",
        message="Private content risk.",
        evidence_ref=None,
        created_at=created_at,
    )

    entries = [
        *observation_sources_to_history_entries([source]),
        *behavior_inferences_to_history_entries([inference]),
        *external_skill_assimilation_candidates_to_history_entries([candidate]),
        *external_skill_adapter_candidates_to_history_entries([adapter]),
        *observation_digestion_findings_to_history_entries([finding]),
    ]

    assert {entry.source for entry in entries} == {"observation_digest"}
    assert any(entry.priority >= 85 for entry in entries)
    assert any(
        any(ref.get("ref_type") == "agent_behavior_inference" for ref in entry.refs)
        for entry in entries
    )

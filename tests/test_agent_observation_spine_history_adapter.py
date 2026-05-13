from chanta_core.observation import AgentObservationSpineService
from chanta_core.observation_digest import ObservedAgentRun
from chanta_core.skills.history_adapter import (
    agent_instances_to_history_entries,
    agent_runtime_descriptors_to_history_entries,
    behavior_inferences_v2_to_history_entries,
    environment_snapshots_to_history_entries,
    export_policies_to_history_entries,
    fleet_snapshots_to_history_entries,
    movement_ontology_terms_to_history_entries,
    normalized_events_v2_to_history_entries,
    observation_corrections_to_history_entries,
    observation_reviews_to_history_entries,
    observation_spine_findings_to_history_entries,
    observation_spine_results_to_history_entries,
    observed_objects_to_history_entries,
    observed_relations_to_history_entries,
    redaction_policies_to_history_entries,
)
from chanta_core.utility.time import utc_now_iso


def test_spine_history_adapters() -> None:
    service = AgentObservationSpineService()
    runtime = service.register_runtime_descriptor()
    agent = service.register_agent_instance()
    env = service.create_environment_snapshot(agent_instance=agent)
    terms = service.register_movement_ontology_terms()[:1]
    event = service.normalize_event_v2({"id": "u1", "role": "user", "content": "hello"})
    objects = service.create_observed_objects(observed_run_id="observed_agent_run:demo")
    relations = service.create_observed_relations(observed_run_id="observed_agent_run:demo", events=[event])
    inference = service.create_behavior_inference_v2(
        observed_run=ObservedAgentRun(
            observed_run_id="observed_agent_run:demo",
            source_id="source:demo",
            batch_id="batch:demo",
            source_agent_id=None,
            source_session_id=None,
            inferred_runtime="generic",
            event_count=1,
            object_count=1,
            relation_count=0,
            observation_confidence=0.5,
            created_at=utc_now_iso(),
        )
    )
    review = service.create_observation_review(observed_run_id="observed_agent_run:demo", inference_id=inference.inference_id)
    correction = service.create_observation_correction(review_id=review.review_id, corrected_field="inferred_goal")
    redaction = service.create_redaction_policy()
    export = service.create_export_policy()
    fleet = service.create_fleet_snapshot(agent_instances=[agent], events=[event], observed_objects=objects)
    finding = service.record_finding(subject_ref="demo", finding_type="low_confidence", status="warning", severity="medium", message="Low confidence.")
    result = service.record_result(operation_kind="demo", status="completed", created_object_refs=[event.normalized_event_id], summary="done")

    entries = [
        *agent_runtime_descriptors_to_history_entries([runtime]),
        *agent_instances_to_history_entries([agent]),
        *environment_snapshots_to_history_entries([env]),
        *movement_ontology_terms_to_history_entries(terms),
        *normalized_events_v2_to_history_entries([event]),
        *observed_objects_to_history_entries(objects),
        *observed_relations_to_history_entries(relations),
        *behavior_inferences_v2_to_history_entries([inference]),
        *observation_reviews_to_history_entries([review]),
        *observation_corrections_to_history_entries([correction]),
        *redaction_policies_to_history_entries([redaction]),
        *export_policies_to_history_entries([export]),
        *fleet_snapshots_to_history_entries([fleet]),
        *observation_spine_findings_to_history_entries([finding]),
        *observation_spine_results_to_history_entries([result]),
    ]
    assert entries
    assert {entry.source for entry in entries} == {"agent_observation_spine"}
    assert any(entry.priority >= 70 for entry in entries)

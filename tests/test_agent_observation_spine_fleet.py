from chanta_core.observation import AgentObservationSpineService
from chanta_core.observation_digest import ObservedAgentRun
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.utility.time import utc_now_iso


def test_fleet_snapshot_aggregates_counts_only() -> None:
    service = AgentObservationSpineService()
    agent = service.register_agent_instance(source_runtime="generic_jsonl")
    event = service.normalize_event_v2({"id": "u1", "role": "user", "content": "hello"})
    objects = service.create_observed_objects(observed_run_id="observed_agent_run:demo", events=[event])
    run = ObservedAgentRun(
        observed_run_id="observed_agent_run:demo",
        source_id="source:demo",
        batch_id="batch:demo",
        source_agent_id=None,
        source_session_id=None,
        inferred_runtime="generic_jsonl",
        event_count=1,
        object_count=1,
        relation_count=0,
        observation_confidence=0.5,
        created_at=utc_now_iso(),
    )

    snapshot = service.create_fleet_snapshot(agent_instances=[agent], observed_runs=[run], events=[event], observed_objects=objects)

    assert snapshot.agent_instance_count == 1
    assert snapshot.observed_run_count == 1
    assert snapshot.source_runtime_counts == {"generic_jsonl": 1}
    assert snapshot.snapshot_attrs["aggregate_only"] is True
    assert "content" not in snapshot.to_dict()


def test_pig_ocpx_spine_counts_visible() -> None:
    view = OCPXProcessView(
        view_id="view:spine",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView("event:v2", "agent_observation_normalized_event_v2", {"canonical_action_type": "observe_context"}),
            OCPXObjectView("object:file", "observed_agent_object", {"object_type": "file"}),
            OCPXObjectView("relation:one", "observed_agent_relation", {"relation_type": "followed_by"}),
            OCPXObjectView("inference:v2", "agent_behavior_inference_v2", {"inference_attrs": {"confidence_class": "behavior_inference"}}),
            OCPXObjectView("adapter:one", "agent_observation_adapter_profile", {"source_runtime": "generic_jsonl"}),
            OCPXObjectView("collector:one", "agent_observation_collector_contract", {"collector_kind": "batch_file"}),
        ],
    )
    summary = PIGReportService._agent_observation_spine_summary(
        {
            "agent_observation_normalized_event_v2": 1,
            "observed_agent_object": 1,
            "observed_agent_relation": 1,
            "agent_behavior_inference_v2": 1,
            "agent_observation_adapter_profile": 1,
            "agent_observation_collector_contract": 1,
        },
        {},
        view,
    )

    assert summary["agent_observation_normalized_event_v2_count"] == 1
    assert summary["observed_event_v2_by_action_type"] == {"observe_context": 1}
    assert summary["observed_object_by_type"] == {"file": 1}
    assert summary["observed_relation_by_type"] == {"followed_by": 1}
    assert summary["behavior_inference_by_confidence_class"] == {"behavior_inference": 1}
    assert summary["adapter_profile_by_runtime"] == {"generic_jsonl": 1}
    assert summary["collector_contract_by_kind"] == {"batch_file": 1}

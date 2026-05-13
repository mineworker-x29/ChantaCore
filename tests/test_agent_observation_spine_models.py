from chanta_core.observation import (
    AgentObservationNormalizedEventV2,
    AgentObservationSpineService,
    ObservedAgentRelation,
)
from chanta_core.skills.ids import (
    new_agent_observation_normalized_event_v2_id,
    new_observed_agent_relation_id,
)
from chanta_core.utility.time import utc_now_iso


def test_normalized_event_v2_and_relation_defaults() -> None:
    now = utc_now_iso()
    event = AgentObservationNormalizedEventV2(
        normalized_event_id=new_agent_observation_normalized_event_v2_id(),
        batch_id="batch:demo",
        source_event_id="event:demo",
        source_runtime="generic_jsonl",
        source_format="jsonl",
        source_schema_version="1",
        adapter_version="0.19.6",
        observed_activity="tool_call_observed",
        canonical_action_type="invoke_tool",
        observed_timestamp=None,
        actor_type="agent",
        actor_ref="assistant",
        object_refs=["tool:search"],
        effect_type="unknown_side_effect",
        input_preview="query",
        output_preview=None,
        confidence=2.0,
        confidence_class="confirmed_observation",
        evidence_ref="event:demo",
        uncertainty_notes=[],
        withdrawal_conditions=["Withdraw on contradiction."],
        created_at=now,
    )
    relation = ObservedAgentRelation(
        observed_relation_id=new_observed_agent_relation_id(),
        observed_run_id="observed_agent_run:demo",
        source_ref=event.normalized_event_id,
        target_ref="agent_observation_normalized_event_v2:next",
        relation_type="followed_by",
        confidence=0.7,
        causal_claim=False,
        evidence_refs=["event:demo"],
        uncertainty_notes=["Temporal relation only."],
        created_at=now,
    )

    assert event.to_dict()["confidence"] == 1.0
    assert event.evidence_ref
    assert event.withdrawal_conditions
    assert relation.to_dict()["causal_claim"] is False
    assert AgentObservationSpineService is not None

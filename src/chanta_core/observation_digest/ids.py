from __future__ import annotations

from uuid import uuid4


def new_agent_observation_source_id() -> str:
    return f"agent_observation_source:{uuid4()}"


def new_agent_observation_batch_id() -> str:
    return f"agent_observation_batch:{uuid4()}"


def new_agent_observation_normalized_event_id() -> str:
    return f"agent_observation_normalized_event:{uuid4()}"


def new_observed_agent_run_id() -> str:
    return f"observed_agent_run:{uuid4()}"


def new_agent_behavior_inference_id() -> str:
    return f"agent_behavior_inference:{uuid4()}"


def new_agent_process_narrative_id() -> str:
    return f"agent_process_narrative:{uuid4()}"


def new_external_skill_source_descriptor_id() -> str:
    return f"external_skill_source_descriptor:{uuid4()}"


def new_external_skill_static_profile_id() -> str:
    return f"external_skill_static_profile:{uuid4()}"


def new_external_skill_behavior_fingerprint_id() -> str:
    return f"external_skill_behavior_fingerprint:{uuid4()}"


def new_external_skill_assimilation_candidate_id() -> str:
    return f"external_skill_assimilation_candidate:{uuid4()}"


def new_external_skill_adapter_candidate_id() -> str:
    return f"external_skill_adapter_candidate:{uuid4()}"


def new_observation_digestion_finding_id() -> str:
    return f"observation_digestion_finding:{uuid4()}"


def new_observation_digestion_result_id() -> str:
    return f"observation_digestion_result:{uuid4()}"

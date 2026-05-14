from chanta_core.digestion import (
    ObservationDigestionAdapterCandidate,
    ObservationToDigestionAdapterBuilderService,
)


def test_policy_defaults_disable_auto_activation_import_execution() -> None:
    service = ObservationToDigestionAdapterBuilderService()
    policy = service.create_default_policy()

    assert policy.allow_auto_adapter_activation is False
    assert policy.allow_canonical_skill_import is False
    assert policy.allow_execution_enablement is False
    assert policy.require_review is True


def test_adapter_candidate_defaults_are_review_only() -> None:
    candidate = ObservationDigestionAdapterCandidate(
        adapter_candidate_id="observation_digestion_adapter_candidate:dummy",
        observed_capability_id="observed_capability_candidate:dummy",
        target_candidate_id="chantacore_target_skill_candidate:dummy",
        source_runtime="generic_runtime",
        source_skill_ref="generic_skill",
        source_tool_ref=None,
        target_skill_id="skill:read_workspace_text_file",
        mapping_type="observed_behavior_to_skill_candidate",
        mapping_confidence=0.8,
        input_mapping_id="adapter_input_mapping_spec:dummy",
        output_mapping_id="adapter_output_mapping_spec:dummy",
        unsupported_feature_ids=[],
        risk_class="low",
    )

    assert candidate.review_status == "pending_review"
    assert candidate.requires_review is True
    assert candidate.canonical_import_enabled is False
    assert candidate.execution_enabled is False
    assert candidate.to_dict()["execution_enabled"] is False


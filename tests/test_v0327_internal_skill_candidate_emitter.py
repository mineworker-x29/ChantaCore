import pytest

from chanta_core.external_harness import (
    InternalCandidateEmissionBlockerKind,
    InternalCandidateEmissionEvidenceQuality,
    InternalCandidateEmissionKind,
    InternalCandidateEmissionReviewRequirementKind,
    InternalCandidateEmissionRoute,
    InternalCandidateEmissionSourceKind,
    InternalCandidateEmissionStatus,
    build_external_digestibility_assessment,
    build_external_digestion_pattern_signal,
    build_external_digestion_source_ref,
    build_external_harness_digestion_candidate,
    build_external_to_internal_pattern_map,
    build_emitted_internal_approval_boundary_candidate,
    build_emitted_internal_memory_schema_candidate,
    build_emitted_internal_mission_candidate,
    build_emitted_internal_policy_candidate,
    build_emitted_internal_profile_pattern_candidate,
    build_emitted_internal_prompt_pattern_candidate,
    build_emitted_internal_result_envelope_candidate,
    build_emitted_internal_skill_candidate,
    build_emitted_internal_tool_contract_candidate,
    build_emitted_internal_trace_event_pattern_candidate,
    build_external_harness_internal_candidate_set,
    build_internal_candidate_emission_blocker,
    build_internal_candidate_emission_evidence_ref,
    build_internal_candidate_emission_finding,
    build_internal_candidate_emission_input,
    build_internal_candidate_emission_no_runtime_guarantee,
    build_internal_candidate_emission_report,
    build_internal_candidate_emission_review_requirement,
    build_internal_candidate_emission_run_preview,
    build_internal_candidate_emission_source_ref,
    build_v0327_readiness_report,
    emission_report_is_not_runtime,
    emitted_candidate_preserves_no_activation,
    external_harness_internal_candidate_set_is_not_registry,
    infer_emission_blockers_from_digestion_candidate,
    infer_emission_kind_from_external_digestion_candidate,
    infer_review_requirements_from_pattern_map,
    v0327_readiness_report_is_not_runtime_ready,
)
from chanta_core.external_harness.digestion_generation import (
    ExternalDigestibilityPosture,
    ExternalDigestionCandidateKind,
    ExternalDigestionEvidenceQuality,
    ExternalDigestionPatternKind,
    ExternalDigestionRoute,
)
from chanta_core.external_harness.internal_candidate_emitter import (
    DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS,
    InternalCandidateEmissionEvidenceRef,
    InternalCandidateEmissionReviewRequirement,
    InternalCandidateEmissionSourceRef,
    V0327ReadinessReport,
)


def test_internal_candidate_emission_taxonomies_include_required_values():
    assert {item.value for item in InternalCandidateEmissionKind} == {
        "emitted_internal_skill_candidate",
        "emitted_internal_tool_contract_candidate",
        "emitted_internal_mission_candidate",
        "emitted_internal_policy_candidate",
        "emitted_internal_memory_schema_candidate",
        "emitted_internal_prompt_pattern_candidate",
        "emitted_internal_trace_event_pattern_candidate",
        "emitted_internal_result_envelope_candidate",
        "emitted_internal_approval_boundary_candidate",
        "emitted_internal_profile_pattern_candidate",
        "no_op_candidate",
        "future_track_candidate",
        "unknown",
    }
    assert {item.value for item in InternalCandidateEmissionStatus} == {
        "unknown",
        "draft",
        "emitted",
        "emitted_with_gaps",
        "requires_review",
        "blocked",
        "deferred",
        "rejected",
        "future_track",
        "no_op",
    }
    assert {item.value for item in InternalCandidateEmissionRoute} == {
        "emit_for_v0329_consolidation",
        "send_to_v0328_dominion_emitter",
        "require_review",
        "defer",
        "reject",
        "block",
        "future_track",
        "no_op",
        "unknown",
    }
    assert "external_harness_digestion_candidate" in {item.value for item in InternalCandidateEmissionSourceKind}
    assert "sufficient_for_candidate_emission" in {item.value for item in InternalCandidateEmissionEvidenceQuality}
    assert "contract_review" in {item.value for item in InternalCandidateEmissionReviewRequirementKind}
    assert "dominion_required_route" in {item.value for item in InternalCandidateEmissionBlockerKind}


def test_source_evidence_blocker_and_review_are_static_only():
    source_ref = build_internal_candidate_emission_source_ref(
        "source:1",
        InternalCandidateEmissionSourceKind.EXTERNAL_HARNESS_DIGESTION_CANDIDATE,
        "digestion:1",
        reference_entry_ids=["ref:1"],
        evidence_refs=["evidence:1"],
    )
    evidence_ref = build_internal_candidate_emission_evidence_ref(
        "evidence:1",
        evidence_kind="pattern_map_summary",
        evidence_summary="Static pattern map evidence only.",
        quality=InternalCandidateEmissionEvidenceQuality.SUFFICIENT_FOR_CANDIDATE_EMISSION,
        limitations=["review pending"],
    )
    blocker = build_internal_candidate_emission_blocker(
        "blocker:1",
        InternalCandidateEmissionBlockerKind.INSUFFICIENT_EVIDENCE,
        source_ref_ids=[source_ref.source_ref_id],
        reason="More static evidence is required.",
    )
    review = build_internal_candidate_emission_review_requirement(
        "review:1",
        InternalCandidateEmissionReviewRequirementKind.CONTRACT_REVIEW,
        target_candidate_ids=["candidate:1"],
        reason="Contract review is required.",
        required_evidence_refs=[evidence_ref.evidence_ref_id],
    )

    assert source_ref.source_fetch is False
    assert source_ref.execution is False
    assert evidence_ref.runtime_trust is False
    assert blocker.remediation_execution is False
    assert review.approval_granted is False
    assert review.blocks_activation is True
    assert review.blocks_registry_mutation is True
    assert review.approval is False

    with pytest.raises(ValueError):
        InternalCandidateEmissionSourceRef(
            source_ref_id="source:bad",
            source_kind=InternalCandidateEmissionSourceKind.UNKNOWN,
            source_id="source",
            metadata={"source_fetch": True},
        )
    with pytest.raises(ValueError):
        InternalCandidateEmissionEvidenceRef(
            evidence_ref_id="evidence:bad",
            evidence_kind="static",
            evidence_summary="Static evidence.",
            metadata={"runtime_trust": True},
        )
    with pytest.raises(ValueError):
        build_internal_candidate_emission_blocker(
            "blocker:bad",
            InternalCandidateEmissionBlockerKind.UNKNOWN,
            metadata={"remediation": True},
        )
    with pytest.raises(ValueError):
        InternalCandidateEmissionReviewRequirement(
            review_requirement_id="review:bad",
            requirement_kind=InternalCandidateEmissionReviewRequirementKind.HUMAN_REVIEW,
            reason="Review only.",
            approval_granted=True,
        )


def _all_candidate_types():
    source_ref = build_internal_candidate_emission_source_ref(
        "source:shared",
        InternalCandidateEmissionSourceKind.EXTERNAL_TO_INTERNAL_PATTERN_MAP,
        "pattern-map:shared",
    )
    evidence_ref = build_internal_candidate_emission_evidence_ref("evidence:shared")
    common = {
        "source_refs": [source_ref],
        "evidence_refs": [evidence_ref],
        "source_pattern_map_ids": ["pattern-map:shared"],
        "required_tests": ["static contract review test"],
    }
    return [
        build_emitted_internal_skill_candidate("candidate:skill", "static_skill", **common),
        build_emitted_internal_tool_contract_candidate("candidate:tool", "static_tool", **common),
        build_emitted_internal_mission_candidate("candidate:mission", "static_mission", **common),
        build_emitted_internal_policy_candidate("candidate:policy", "static_policy", **common),
        build_emitted_internal_memory_schema_candidate("candidate:memory", "static_memory", **common),
        build_emitted_internal_prompt_pattern_candidate("candidate:prompt", "static_prompt", **common),
        build_emitted_internal_trace_event_pattern_candidate("candidate:trace", "static_event", **common),
        build_emitted_internal_result_envelope_candidate("candidate:result", "static_envelope", **common),
        build_emitted_internal_approval_boundary_candidate("candidate:approval", "static_boundary", **common),
        build_emitted_internal_profile_pattern_candidate("candidate:profile", "static_profile", **common),
    ]


def test_each_emitted_candidate_type_is_inactive_design_artifact():
    candidates = _all_candidate_types()

    for candidate in candidates:
        assert emitted_candidate_preserves_no_activation(candidate)
        assert candidate.ready_for_activation is False
        assert candidate.ready_for_skill_activation is False
        assert candidate.ready_for_registry_mutation is False
        assert candidate.ready_for_memory_mutation is False
        assert candidate.ready_for_internalization is False
        assert candidate.ready_for_execution is False
        assert candidate.active_artifact is False

    skill, tool, mission, policy, memory, prompt, trace, result, approval, profile = candidates
    assert skill.active_skill is False
    assert skill.registered_skill is False
    assert tool.registered_tool is False
    assert tool.tool_invocation is False
    assert mission.installed_mission is False
    assert mission.mission_execution is False
    assert policy.active_policy is False
    assert policy.enforcement_execution is False
    assert memory.memory_writer is False
    assert memory.memory_persistence is False
    assert prompt.prompt_injection is False
    assert trace.ocel_event_emission is False
    assert result.result_ingestion is False
    assert result.raw_output_allowed is False
    assert result.memory_persistence_allowed is False
    assert approval.approval_granted is False
    assert approval.approval_execution is False
    assert profile.profile_activation is False
    assert profile.memory_or_private_data_access is False

    with pytest.raises(ValueError):
        build_emitted_internal_skill_candidate(
            "candidate:bad-active",
            "bad_active",
            ready_for_activation=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_skill_candidate(
            "candidate:bad-exec",
            "bad_exec",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_result_envelope_candidate(
            "candidate:bad-result",
            "bad_result",
            raw_output_allowed=True,
        )
    with pytest.raises(ValueError):
        build_emitted_internal_policy_candidate(
            "candidate:bad-impl",
            "bad_impl",
            metadata={"implementation": True},
        )


def test_candidate_set_input_finding_report_preview_guarantee_and_readiness_are_non_runtime():
    skill = build_emitted_internal_skill_candidate("candidate:skill-set", "static_skill_set")
    evidence_ref = build_internal_candidate_emission_evidence_ref("evidence:set")
    candidate_set = build_external_harness_internal_candidate_set(
        "candidate-set:1",
        skill_candidates=[skill],
        emitted_candidate_ids=[skill.emitted_candidate_id],
        evidence_refs=[evidence_ref],
        ready_for_v0329_consolidation=True,
    )
    source_ref = build_internal_candidate_emission_source_ref(
        "source:input",
        InternalCandidateEmissionSourceKind.EXTERNAL_DIGESTION_CANDIDATE_SET,
        "candidate-set:source",
    )
    emission_input = build_internal_candidate_emission_input(
        "input:1",
        external_digestion_candidate_ids=["digestion:1"],
        external_digestion_candidate_set_ids=["digestion-set:1"],
        pattern_map_ids=["pattern-map:1"],
        source_refs=[source_ref],
        requested_emission_kinds=[InternalCandidateEmissionKind.EMITTED_INTERNAL_SKILL_CANDIDATE],
    )
    finding = build_internal_candidate_emission_finding(
        "finding:1",
        emission_input.emission_input_id,
        [source_ref.source_ref_id],
        skill.emitted_candidate_id,
        InternalCandidateEmissionKind.EMITTED_INTERNAL_SKILL_CANDIDATE,
        InternalCandidateEmissionRoute.EMIT_FOR_V0329_CONSOLIDATION,
        InternalCandidateEmissionStatus.EMITTED_WITH_GAPS,
        "Static candidate emission finding.",
    )
    report = build_internal_candidate_emission_report(
        "report:1",
        emission_input.emission_input_id,
        candidate_set_id=candidate_set.candidate_set_id,
        findings=[finding],
        emitted_candidate_count=1,
        ready_for_v0329_consolidation=True,
    )
    run_preview = build_internal_candidate_emission_run_preview(
        "preview:1",
        emission_input_id=emission_input.emission_input_id,
        planned_steps=["read static metadata"],
        expected_artifacts=["emitted candidate design records"],
        explicitly_not_performed=["execution"],
    )
    guarantee = build_internal_candidate_emission_no_runtime_guarantee("guarantee:1")
    readiness = build_v0327_readiness_report(
        "readiness:1",
        emission_report_id=report.report_id,
        candidate_set_id=candidate_set.candidate_set_id,
        ready_for_v0328_external_dominion_candidate_emitter=True,
        ready_for_v0329_external_observation_digestion_consolidation=True,
    )

    assert external_harness_internal_candidate_set_is_not_registry(candidate_set)
    assert emission_input.execution_request is False
    assert finding.active_candidate is False
    assert finding.activation is False
    assert emission_report_is_not_runtime(report)
    assert run_preview.execution is False
    assert all(getattr(run_preview, name) is True for name in run_preview.__dataclass_fields__ if name.startswith("no_"))
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0327_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(emission_input.prohibited_runtime_actions))
    assert set(DEFAULT_EMISSION_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        build_external_harness_internal_candidate_set("candidate-set:bad", metadata={"registry": True})
    with pytest.raises(ValueError):
        build_internal_candidate_emission_report(
            "report:bad",
            emission_input.emission_input_id,
            metadata={"runtime_result": True},
        )
    with pytest.raises(ValueError):
        V0327ReadinessReport(
            report_id="readiness:bad",
            version="v0.32.7",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        V0327ReadinessReport(
            report_id="readiness:bad-plugin",
            version="v0.32.7",
            ready_for_plugin_loading=True,
        )


def test_fake_external_digestion_candidates_emit_design_stage_internal_candidates_without_execution():
    digestion_source = build_external_digestion_source_ref(
        "digestion-source:1",
        "external_manifest_candidate",
        "manifest:1",
    )
    signal = build_external_digestion_pattern_signal(
        "signal:1",
        [digestion_source.source_ref_id],
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        ExternalDigestionPatternKind.CONTRACT_PATTERN,
        "Static skill pattern",
        "A static external skill pattern.",
        "Input, output, validation, and tests can be summarized.",
        evidence_quality=ExternalDigestionEvidenceQuality.SUFFICIENT_FOR_DIGESTION_CANDIDATE,
    )
    pattern_map = build_external_to_internal_pattern_map(
        "pattern-map:1",
        source_pattern_signal_ids=[signal.pattern_signal_id],
        suggested_internal_candidate_kind="skill_candidate",
        evidence_refs=["evidence:pattern-map"],
    )
    assessment = build_external_digestibility_assessment(
        "assessment:1",
        pattern_signal_ids=[signal.pattern_signal_id],
        digestibility_posture=ExternalDigestibilityPosture.DIGESTIBLE,
        route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
        summary="Digestible static pattern.",
        ready_for_v0327_internal_candidate_emitter=True,
    )
    digestion_candidate = build_external_harness_digestion_candidate(
        "digestion:1",
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        [digestion_source],
        [signal],
        assessment,
        external_to_internal_pattern_map=pattern_map,
        source_manifest_candidate_ids=["manifest:1"],
        ready_for_v0327_internal_candidate_emitter=True,
        status=ExternalDigestibilityPosture.DIGESTIBLE,
        route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
    )

    assert infer_emission_kind_from_external_digestion_candidate(digestion_candidate) == InternalCandidateEmissionKind.EMITTED_INTERNAL_SKILL_CANDIDATE
    reviews = infer_review_requirements_from_pattern_map(pattern_map)
    assert InternalCandidateEmissionReviewRequirementKind.CONTRACT_REVIEW in reviews
    assert InternalCandidateEmissionReviewRequirementKind.EVIDENCE_REVIEW in reviews
    assert infer_emission_blockers_from_digestion_candidate(digestion_candidate) == []

    emitted = build_emitted_internal_skill_candidate(
        "emitted:skill:1",
        "static_skill_from_external_pattern",
        source_pattern_map_ids=[pattern_map.pattern_map_id],
        input_contract_summary=pattern_map.suggested_input_contract_summary,
        output_contract_summary=pattern_map.suggested_output_contract_summary,
        validation_summary=pattern_map.suggested_validation_summary,
        required_tests=[pattern_map.suggested_test_summary],
    )

    assert emitted_candidate_preserves_no_activation(emitted)
    assert emitted.active_skill is False
    assert emitted.registered_skill is False

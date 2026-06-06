from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import (
    InternalCandidateEvidenceRef,
    InternalCandidateKind,
    InternalCandidateRiskKind,
    InternalCandidateSet,
    InternalCandidateSourceRef,
    InternalCandidateStatus,
    InternalMemorySchemaCandidate,
    InternalMissionCandidate,
    InternalPolicyCandidate,
    InternalPromptPatternCandidate,
    InternalResultEnvelopeCandidate,
    InternalSkillCandidate,
    InternalToolContractCandidate,
    InternalTraceEventPatternCandidate,
    InternalizationNoOpDecision,
    InternalizationPlan,
    InternalizationPlanStatus,
    InternalizationPlanStep,
    InternalizationPlanStepKind,
    InternalizationReviewRequirement,
    InternalizationReviewRequirementKind,
    InternalizationRunPreview,
    V0314ReadinessReport,
    build_internal_candidate_evidence_ref,
    build_internal_candidate_set,
    build_internal_candidate_source_ref,
    build_internal_memory_schema_candidate,
    build_internal_mission_candidate,
    build_internal_policy_candidate,
    build_internal_prompt_pattern_candidate,
    build_internal_result_envelope_candidate,
    build_internal_skill_candidate,
    build_internal_tool_contract_candidate,
    build_internal_trace_event_pattern_candidate,
    build_internalization_no_op_decision,
    build_internalization_plan,
    build_internalization_plan_step,
    build_internalization_review_requirement,
    build_internalization_run_preview,
    build_v0314_readiness_report,
    candidate_preserves_no_activation,
    candidate_set_preserves_no_registry_mutation,
    internal_candidate_kind_creates_active_artifact,
    internalization_plan_is_not_implementation,
    internalization_plan_preserves_no_execution,
    normalize_internal_candidate_kind,
    normalize_internal_candidate_risk_kind,
    normalize_internal_candidate_status,
    normalize_internalization_plan_status,
    normalize_internalization_plan_step_kind,
    normalize_internalization_review_requirement_kind,
    v0314_readiness_report_is_not_runtime_ready,
)
from chanta_core.internal_triad import internalization


REQUIRED_PROHIBITIONS = {
    "runtime_execution",
    "skill_activation",
    "registry_mutation",
    "tool_registration",
    "mission_installation",
    "policy_activation",
    "memory_mutation",
    "external_scan",
    "source_ref_fetch",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "rollback",
    "retry",
}


def test_internalization_taxonomies_are_complete_and_conservative() -> None:
    assert {kind.value for kind in InternalCandidateKind} == {
        "internal_skill_candidate",
        "internal_tool_contract_candidate",
        "internal_mission_candidate",
        "internal_policy_candidate",
        "internal_memory_schema_candidate",
        "internal_prompt_pattern_candidate",
        "internal_trace_event_pattern_candidate",
        "internal_result_envelope_candidate",
        "internal_profile_pattern_candidate",
        "internal_approval_boundary_candidate",
        "unknown",
    }
    assert normalize_internal_candidate_kind("unknown") is InternalCandidateKind.UNKNOWN
    assert internal_candidate_kind_creates_active_artifact(InternalCandidateKind.INTERNAL_SKILL_CANDIDATE) is False

    assert {status.value for status in InternalCandidateStatus} == {
        "unknown",
        "candidate",
        "requires_review",
        "requires_more_evidence",
        "deferred",
        "rejected",
        "blocked",
        "future_track",
        "no_op",
    }
    assert normalize_internal_candidate_status("candidate") is InternalCandidateStatus.CANDIDATE

    assert {status.value for status in InternalizationPlanStatus} == {
        "unknown",
        "draft",
        "plan_ready",
        "plan_ready_with_gaps",
        "requires_review",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_internalization_plan_status("plan_ready") is InternalizationPlanStatus.PLAN_READY

    assert {kind.value for kind in InternalizationPlanStepKind} == {
        "define_contract",
        "define_schema",
        "define_validation",
        "define_test",
        "define_doc",
        "define_ocel_trace_contract",
        "define_review_gate",
        "define_no_op_path",
        "define_future_gate",
        "unknown",
    }
    assert normalize_internalization_plan_step_kind("define_test") is InternalizationPlanStepKind.DEFINE_TEST

    assert {kind.value for kind in InternalizationReviewRequirementKind} == {
        "evidence_review",
        "boundary_review",
        "safety_review",
        "ocel_trace_review",
        "test_review",
        "documentation_review",
        "human_review",
        "future_gate_review",
        "unknown",
    }
    assert normalize_internalization_review_requirement_kind("human_review") is InternalizationReviewRequirementKind.HUMAN_REVIEW

    assert {kind.value for kind in InternalCandidateRiskKind} == {
        "insufficient_evidence",
        "unsafe_runtime_surface",
        "registry_mutation_risk",
        "tool_execution_risk",
        "memory_mutation_risk",
        "policy_activation_risk",
        "mission_installation_risk",
        "prompt_injection_risk",
        "ocel_schema_drift_risk",
        "external_dependency_risk",
        "provider_network_credential_risk",
        "command_browser_rpa_gateway_risk",
        "incompatible_with_ocel_spine",
        "unknown",
    }
    assert normalize_internal_candidate_risk_kind("unsafe_runtime_surface") is InternalCandidateRiskKind.UNSAFE_RUNTIME_SURFACE


def _refs():
    source_ref = build_internal_candidate_source_ref(
        "internal_candidate_source_ref:1",
        "digestible_pattern_signal",
        "digestion_signal:1",
        target_id="target:1",
        capability_entry_id="capability_entry:1",
        digestion_signal_id="digestion_signal:1",
        route_decision_id="route_decision:1",
        evidence_ref_ids=["evidence_ref:1"],
    )
    evidence_ref = build_internal_candidate_evidence_ref(
        "internal_candidate_evidence_ref:1",
        "route_signal",
        "Route signal evidence only.",
        "sufficient_for_review",
        source_evidence_ref_id="evidence_ref:1",
        limitations=["not runtime trust"],
    )
    return source_ref, evidence_ref


def test_source_and_evidence_refs_are_not_fetch_or_runtime_trust() -> None:
    source_ref, evidence_ref = _refs()

    assert isinstance(source_ref, InternalCandidateSourceRef)
    assert source_ref.fetches_source is False
    assert isinstance(evidence_ref, InternalCandidateEvidenceRef)
    assert evidence_ref.runtime_trust is False

    with pytest.raises(ValueError, match="source_ref_id"):
        build_internal_candidate_source_ref("", "kind", "source")
    with pytest.raises(ValueError, match="source_kind"):
        build_internal_candidate_source_ref("source:bad", "", "source")
    with pytest.raises(ValueError, match="source_id"):
        build_internal_candidate_source_ref("source:bad", "kind", "")
    with pytest.raises(ValueError, match="source fetch"):
        build_internal_candidate_source_ref("source:bad", "kind", "source", metadata={"source_ref_fetch": True})
    with pytest.raises(ValueError, match="evidence_ref_id"):
        build_internal_candidate_evidence_ref("", "kind", "summary")
    with pytest.raises(ValueError, match="evidence_kind"):
        build_internal_candidate_evidence_ref("evidence:bad", "", "summary")
    with pytest.raises(ValueError, match="evidence_summary"):
        build_internal_candidate_evidence_ref("evidence:bad", "kind", "")
    with pytest.raises(ValueError, match="runtime trust"):
        build_internal_candidate_evidence_ref("evidence:bad", "kind", "summary", metadata={"runtime_trust": True})


def test_all_internal_candidates_are_inactive_artifacts_only() -> None:
    source_ref, evidence_ref = _refs()
    base = {
        "source_refs": [source_ref],
        "evidence_refs": [evidence_ref],
        "risk_kinds": [InternalCandidateRiskKind.INSUFFICIENT_EVIDENCE],
        "required_reviews": [InternalizationReviewRequirementKind.SAFETY_REVIEW],
    }
    skill = build_internal_skill_candidate("candidate:skill", "Skill candidate", "Review skill contract.", "review_skill", **base)
    tool = build_internal_tool_contract_candidate("candidate:tool", "Tool candidate", "Review tool contract.", "review_tool", **base)
    mission = build_internal_mission_candidate("candidate:mission", "Mission candidate", "Review mission.", "review_mission", **base)
    policy = build_internal_policy_candidate("candidate:policy", "Policy candidate", "Review policy.", "review_policy", **base)
    memory = build_internal_memory_schema_candidate("candidate:memory", "Memory candidate", "Review memory schema.", "review_memory", **base)
    prompt = build_internal_prompt_pattern_candidate("candidate:prompt", "Prompt candidate", "Review prompt pattern.", "review_prompt", **base)
    trace = build_internal_trace_event_pattern_candidate("candidate:trace", "Trace candidate", "Review trace event.", "review_event", **base)
    envelope = build_internal_result_envelope_candidate("candidate:envelope", "Envelope candidate", "Review envelope.", "review_envelope", **base)

    assert isinstance(skill, InternalSkillCandidate)
    assert skill.active_skill is False
    assert REQUIRED_PROHIBITIONS.issubset(set(skill.prohibited_runtime_actions))
    assert isinstance(tool, InternalToolContractCandidate)
    assert tool.registered_tool is False
    assert isinstance(mission, InternalMissionCandidate)
    assert mission.installed_mission is False
    assert isinstance(policy, InternalPolicyCandidate)
    assert policy.active_policy is False
    assert isinstance(memory, InternalMemorySchemaCandidate)
    assert memory.memory_writer is False
    assert memory.persists_memory is False
    assert isinstance(prompt, InternalPromptPatternCandidate)
    assert prompt.prompt_injection is False
    assert isinstance(trace, InternalTraceEventPatternCandidate)
    assert trace.emits_ocel_event is False
    assert isinstance(envelope, InternalResultEnvelopeCandidate)
    assert envelope.raw_output_allowed is False
    assert envelope.memory_persistence_allowed is False
    assert envelope.result_ingestion is False
    for candidate in [skill, tool, mission, policy, memory, prompt, trace, envelope]:
        assert candidate.ready_for_activation is False
        assert candidate.ready_for_registry_mutation is False
        assert candidate.ready_for_execution is False
        assert candidate_preserves_no_activation(candidate) is True

    with pytest.raises(ValueError, match="ready_for_activation"):
        InternalSkillCandidate(
            "candidate:bad",
            InternalCandidateKind.INTERNAL_SKILL_CANDIDATE,
            InternalCandidateStatus.CANDIDATE,
            "title",
            "purpose",
            [],
            [],
            [],
            [],
            [],
            [],
            True,
            False,
            False,
            "skill",
            "kind",
            "input",
            "output",
            list(internalization.V0314_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
            [],
        )
    with pytest.raises(ValueError, match="side_effect_policy"):
        build_internal_tool_contract_candidate("candidate:bad", "Tool", "Purpose", "tool", side_effect_policy="execute command")
    with pytest.raises(ValueError, match="policy activation"):
        build_internal_policy_candidate("candidate:bad", "Policy", "Purpose", "policy", metadata={"policy_activation": True})
    with pytest.raises(ValueError, match="persist memory"):
        build_internal_memory_schema_candidate("candidate:bad", "Memory", "Purpose", "memory", metadata={"memory_mutation": True})
    with pytest.raises(ValueError, match="prompt injection"):
        build_internal_prompt_pattern_candidate("candidate:bad", "Prompt", "Purpose", "prompt", metadata={"prompt_injection": True})
    with pytest.raises(ValueError, match="OCEL events"):
        build_internal_trace_event_pattern_candidate("candidate:bad", "Trace", "Purpose", "event", metadata={"ocel_event_emission": True})
    with pytest.raises(ValueError, match="raw_output_allowed"):
        InternalResultEnvelopeCandidate(
            "candidate:bad",
            InternalCandidateKind.INTERNAL_RESULT_ENVELOPE_CANDIDATE,
            InternalCandidateStatus.CANDIDATE,
            "title",
            "purpose",
            [],
            [],
            [],
            [],
            [],
            [],
            False,
            False,
            False,
            "envelope",
            [],
            [],
            [],
            True,
            False,
        )


def _candidate_set_and_plan():
    source_ref, evidence_ref = _refs()
    skill = build_internal_skill_candidate(
        "candidate:skill",
        "Skill candidate",
        "Review skill contract.",
        "review_skill",
        source_refs=[source_ref],
        evidence_refs=[evidence_ref],
    )
    candidate_set = build_internal_candidate_set(
        "candidate_set:v0.31.4",
        source_digestion_output_id="digestion_output:v0.31.3",
        skill_candidates=[skill],
        dominion_required_source_refs=["digestion_signal:dominion"],
        evidence_refs=[evidence_ref],
    )
    step = build_internalization_plan_step(
        "plan_step:1",
        InternalizationPlanStepKind.DEFINE_CONTRACT,
        0,
        "Define candidate contract",
        "Write contract only; no implementation.",
        target_candidate_ids=[skill.candidate_id],
        required_reviews=[InternalizationReviewRequirementKind.SAFETY_REVIEW],
        expected_artifacts=["contract draft"],
    )
    review = build_internalization_review_requirement(
        "review_requirement:1",
        InternalizationReviewRequirementKind.SAFETY_REVIEW,
        "Safety review blocks activation and registry mutation.",
        target_candidate_ids=[skill.candidate_id],
    )
    plan = build_internalization_plan(
        "internalization_plan:v0.31.4",
        candidate_set.candidate_set_id,
        InternalizationPlanStatus.PLAN_READY,
        "Plan is ready for review only.",
        plan_steps=[step],
        review_requirements=[review],
        candidate_ids=[skill.candidate_id],
        evidence_refs=[evidence_ref],
    )
    return candidate_set, step, review, plan, evidence_ref


def test_candidate_set_plan_step_review_and_plan_are_non_runtime() -> None:
    candidate_set, step, review, plan, evidence_ref = _candidate_set_and_plan()

    assert isinstance(candidate_set, InternalCandidateSet)
    assert candidate_set.ready_for_activation is False
    assert candidate_set.ready_for_registry_mutation is False
    assert candidate_set.ready_for_execution is False
    assert candidate_set.is_registry is False
    assert candidate_set.creates_dominion_target is False
    assert candidate_set_preserves_no_registry_mutation(candidate_set) is True

    assert isinstance(step, InternalizationPlanStep)
    assert step.executes_step is False
    assert isinstance(review, InternalizationReviewRequirement)
    assert review.approval_granted is False
    assert review.blocks_activation is True
    assert review.blocks_registry_mutation is True

    assert isinstance(plan, InternalizationPlan)
    assert plan.ready_for_activation is False
    assert plan.ready_for_registry_mutation is False
    assert plan.ready_for_execution is False
    assert plan.no_execution_guarantee is True
    assert plan.no_registry_mutation_guarantee is True
    assert plan.no_skill_activation_guarantee is True
    assert plan.no_tool_registration_guarantee is True
    assert plan.no_mission_installation_guarantee is True
    assert plan.no_policy_activation_guarantee is True
    assert plan.no_memory_mutation_guarantee is True
    assert plan.is_implementation is False
    assert internalization_plan_preserves_no_execution(plan) is True
    assert internalization_plan_is_not_implementation(plan) is True

    with pytest.raises(ValueError, match="candidate_set_id"):
        build_internal_candidate_set("")
    with pytest.raises(ValueError, match="ready_for_registry_mutation"):
        InternalCandidateSet("candidate_set:bad", None, [], [], [], [], [], [], [], [], [], [], [], [], [], False, True, False)
    with pytest.raises(ValueError, match="order"):
        build_internalization_plan_step("step:bad", InternalizationPlanStepKind.UNKNOWN, -1, "title", "description")
    with pytest.raises(ValueError, match="execution"):
        build_internalization_plan_step("step:bad", InternalizationPlanStepKind.DEFINE_TEST, 0, "title", "description", metadata={"execution_step": True})
    with pytest.raises(ValueError, match="approval"):
        build_internalization_review_requirement("review:bad", InternalizationReviewRequirementKind.HUMAN_REVIEW, "reason", metadata={"approval_granted": True})
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        InternalizationPlan("plan:bad", "candidate_set", InternalizationPlanStatus.DRAFT, "summary", [], [], [], [], [], [], [], no_execution_guarantee=False)
    with pytest.raises(ValueError, match="ready_for_execution"):
        InternalizationPlan("plan:bad", "candidate_set", InternalizationPlanStatus.DRAFT, "summary", [], [], [], [], [], [], [], ready_for_execution=True)
    with pytest.raises(ValueError, match="implementation"):
        build_internalization_plan("plan:bad", "candidate_set", InternalizationPlanStatus.DRAFT, "summary", metadata={"implementation": True})


def test_no_op_run_preview_and_readiness_report_are_not_runtime_enablement() -> None:
    candidate_set, _, _, plan, evidence_ref = _candidate_set_and_plan()
    no_op = build_internalization_no_op_decision(
        "internalization_noop:1",
        "No candidates should be activated.",
        candidate_set.candidate_set_id,
        safe_alternatives=["defer"],
        evidence_refs=[evidence_ref],
    )
    preview = build_internalization_run_preview("internalization_preview:1", candidate_set.candidate_set_id)
    readiness = build_v0314_readiness_report(candidate_set, plan)

    assert isinstance(no_op, InternalizationNoOpDecision)
    assert no_op.is_failure is False
    assert no_op.executes_anything is False
    assert isinstance(preview, InternalizationRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_skill_activation_guarantee is True
    assert preview.no_tool_registration_guarantee is True
    assert preview.no_mission_installation_guarantee is True
    assert preview.no_policy_activation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False

    assert isinstance(readiness, V0314ReadinessReport)
    assert "v0.31.4" in readiness.version
    assert readiness.ready_for_activation is False
    assert readiness.ready_for_registry_mutation is False
    assert readiness.ready_for_execution is False
    assert readiness.runtime_enablement is False
    assert REQUIRED_PROHIBITIONS.issubset(set(readiness.prohibited_until_later_gate))
    assert v0314_readiness_report_is_not_runtime_ready(readiness) is True

    with pytest.raises(ValueError, match="no_op_id"):
        build_internalization_no_op_decision("", "reason")
    with pytest.raises(ValueError, match="reason"):
        build_internalization_no_op_decision("noop:bad", "")
    with pytest.raises(ValueError, match="run_preview_id"):
        build_internalization_run_preview("")
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        InternalizationRunPreview("preview:bad", None, [], [], [], no_execution_guarantee=False)
    with pytest.raises(ValueError, match="v0.31.4"):
        V0314ReadinessReport("readiness:bad", "v0.31.3", None, None, "summary", True, False)
    with pytest.raises(ValueError, match="ready_for_activation"):
        V0314ReadinessReport("readiness:bad", "v0.31.4", None, None, "summary", True, False, ready_for_activation=True)
    with pytest.raises(ValueError, match="runtime enablement"):
        V0314ReadinessReport("readiness:bad", "v0.31.4", None, None, "summary", True, False, metadata={"runtime_enablement": True})


def test_helpers_are_pure_conservative_candidate_plan_builders() -> None:
    helpers = [
        build_internal_candidate_source_ref,
        build_internal_candidate_evidence_ref,
        build_internal_skill_candidate,
        build_internal_tool_contract_candidate,
        build_internal_mission_candidate,
        build_internal_policy_candidate,
        build_internal_memory_schema_candidate,
        build_internal_prompt_pattern_candidate,
        build_internal_trace_event_pattern_candidate,
        build_internal_result_envelope_candidate,
        build_internal_candidate_set,
        build_internalization_plan_step,
        build_internalization_review_requirement,
        build_internalization_plan,
        build_internalization_no_op_decision,
        build_internalization_run_preview,
        build_v0314_readiness_report,
        candidate_preserves_no_activation,
        candidate_set_preserves_no_registry_mutation,
        internalization_plan_preserves_no_execution,
        internalization_plan_is_not_implementation,
        v0314_readiness_report_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_activation=True" not in source
        assert "ready_for_registry_mutation=True" not in source
        assert "ready_for_execution=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = inspect.getsource(internalization)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source

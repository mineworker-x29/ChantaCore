import pytest

from chanta_core.external_harness import (
    ExternalCapabilityRiskClass,
    ExternalCapabilityRiskClassification,
    ExternalCapabilityRiskRoute,
    ExternalDigestibilityAssessment,
    ExternalDigestibilityPosture,
    ExternalDigestionBlocker,
    ExternalDigestionBlockerKind,
    ExternalDigestionCandidateGenerationFinding,
    ExternalDigestionCandidateGenerationInput,
    ExternalDigestionCandidateGenerationReport,
    ExternalDigestionCandidateKind,
    ExternalDigestionCandidateNoRuntimeGuarantee,
    ExternalDigestionCandidateRunPreview,
    ExternalDigestionCandidateSet,
    ExternalDigestionEvidenceQuality,
    ExternalDigestionPatternKind,
    ExternalDigestionPatternSignal,
    ExternalDigestionRoute,
    ExternalDigestionSourceKind,
    ExternalDigestionSourceRef,
    ExternalHarnessDigestionCandidate,
    ExternalManifestRiskSurfaceKind,
    ExternalToInternalPatternMap,
    HarnessPatternDigestibilityReport,
    V0326ReadinessReport,
    build_external_capability_risk_classification,
    build_external_capability_risk_factor,
    build_external_digestibility_assessment,
    build_external_digestion_blocker,
    build_external_digestion_candidate_generation_finding,
    build_external_digestion_candidate_generation_input,
    build_external_digestion_candidate_generation_report,
    build_external_digestion_candidate_no_runtime_guarantee,
    build_external_digestion_candidate_run_preview,
    build_external_digestion_candidate_set,
    build_external_digestion_pattern_signal,
    build_external_digestion_source_ref,
    build_external_harness_digestion_candidate,
    build_external_skill_manifest_candidate,
    build_external_to_internal_pattern_map,
    build_external_tool_manifest_candidate,
    build_harness_pattern_digestibility_report,
    build_v0326_readiness_report,
    external_digestion_candidate_is_not_internal_candidate,
    external_digestion_candidate_set_is_not_registry,
    external_pattern_map_is_not_internalization_plan,
    infer_external_digestion_blockers_from_risk_classification,
    infer_external_digestion_candidate_kind_from_manifest_candidate,
    infer_external_digestion_pattern_kind_from_candidate_kind,
    infer_external_digestion_route_from_risk_classification,
    v0326_readiness_report_is_not_runtime_ready,
)


def test_external_digestion_taxonomies_include_required_values() -> None:
    assert {item.value for item in ExternalDigestionCandidateKind} >= {
        "skill_pattern_candidate",
        "tool_contract_pattern_candidate",
        "plugin_pattern_candidate",
        "mission_pattern_candidate",
        "gateway_contract_pattern_candidate",
        "provider_adapter_pattern_candidate",
        "profile_pattern_candidate",
        "memory_schema_pattern_candidate",
        "approval_policy_pattern_candidate",
        "audit_policy_pattern_candidate",
        "result_envelope_pattern_candidate",
        "ocel_trace_pattern_candidate",
        "prompt_pattern_candidate",
        "delegation_packet_pattern_candidate",
        "unknown",
    }
    assert {item.value for item in ExternalDigestionPatternKind} >= {
        "contract_pattern",
        "schema_pattern",
        "manifest_pattern",
        "workflow_pattern",
        "approval_boundary_pattern",
        "audit_boundary_pattern",
        "result_boundary_pattern",
        "ocel_trace_pattern",
        "prompt_pattern",
        "adapter_pattern",
        "routing_pattern",
        "no_op_pattern",
        "future_track_pattern",
        "unknown",
    }
    assert {item.value for item in ExternalDigestionRoute} >= {
        "send_to_v0327_internal_candidate_emitter",
        "send_to_v0328_dominion_candidate_emitter",
        "require_review",
        "defer",
        "reject",
        "block",
        "future_track",
        "no_op",
        "unknown",
    }
    assert {item.value for item in ExternalDigestibilityPosture} >= {
        "unknown",
        "not_digestible",
        "weak",
        "partial",
        "digestible",
        "digestible_with_gaps",
        "requires_review",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ExternalDigestionEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_digestion_candidate",
        "sufficient_for_v0327_review",
        "conflicting",
        "blocked",
    }
    assert {item.value for item in ExternalDigestionBlockerKind} >= {
        "insufficient_evidence",
        "conflicting_evidence",
        "missing_manifest_candidate",
        "missing_risk_classification",
        "blocked_risk_route",
        "dominion_required_route",
        "future_gate_required",
        "unsafe_runtime_surface",
        "plugin_loading_surface",
        "tool_invocation_surface",
        "mission_execution_surface",
        "provider_invocation_surface",
        "gateway_connection_surface",
        "credential_access_surface",
        "network_access_surface",
        "command_execution_surface",
        "memory_mutation_surface",
        "registry_mutation_surface",
        "incompatible_with_internal_triad",
        "unknown",
    }
    assert {item.value for item in ExternalDigestionSourceKind} >= {
        "external_capability_risk_classification",
        "external_capability_risk_map",
        "external_capability_boundary_map",
        "external_manifest_candidate",
        "external_manifest_candidate_set",
        "external_manifest_extraction_report",
        "opencode_observation_output",
        "openclaw_observation_output",
        "hermes_observation_output",
        "reference_file_inventory",
        "reference_corpus_snapshot",
        "manual_digestion_review",
        "unknown",
    }


def test_source_ref_pattern_signal_assessment_and_blocker_are_static_only() -> None:
    source_ref = build_external_digestion_source_ref(
        "digestion-source:1",
        ExternalDigestionSourceKind.EXTERNAL_CAPABILITY_RISK_CLASSIFICATION,
        "classification:digestible",
        manifest_candidate_id="candidate:skill",
        risk_classification_id="classification:digestible",
    )
    signal = build_external_digestion_pattern_signal(
        pattern_signal_id="pattern-signal:skill",
        source_ref_ids=[source_ref.source_ref_id],
        candidate_kind=ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        pattern_kind=ExternalDigestionPatternKind.CONTRACT_PATTERN,
        title="Static skill pattern",
        summary="Skill-like contract pattern found in static metadata.",
        extracted_pattern_summary="Inputs, outputs, and side-effect boundaries are descriptive only.",
        suggested_internal_artifact_kind="internal_skill_candidate",
    )
    assessment = build_external_digestibility_assessment(
        "assessment:digestible",
        pattern_signal_ids=[signal.pattern_signal_id],
        digestibility_posture=ExternalDigestibilityPosture.DIGESTIBLE,
        route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
        ready_for_v0327_internal_candidate_emitter=True,
    )
    blocker = build_external_digestion_blocker(
        "blocker:review",
        ExternalDigestionBlockerKind.INSUFFICIENT_EVIDENCE,
        reason="Additional review evidence is needed.",
    )

    assert isinstance(source_ref, ExternalDigestionSourceRef)
    assert source_ref.source_fetch is False
    assert source_ref.execution is False
    assert isinstance(signal, ExternalDigestionPatternSignal)
    assert signal.generated_code is False
    assert signal.suggested_artifact_creation is False
    assert signal.suggested_internal_artifact_kind == "internal_skill_candidate"
    assert isinstance(assessment, ExternalDigestibilityAssessment)
    assert assessment.ready_for_internal_candidate_creation is False
    assert assessment.ready_for_execution is False
    assert assessment.approval is False
    assert assessment.internalization is False
    assert isinstance(blocker, ExternalDigestionBlocker)
    assert blocker.blocks_v0327 is True
    assert blocker.remediation_execution is False

    with pytest.raises(ValueError):
        ExternalDigestionSourceRef(
            source_ref_id="bad",
            source_kind=ExternalDigestionSourceKind.REFERENCE_FILE_INVENTORY,
            source_id="source",
            metadata={"source_fetch": True},
        )
    with pytest.raises(ValueError):
        ExternalDigestionPatternSignal(
            pattern_signal_id="bad",
            source_ref_ids=[],
            candidate_kind=ExternalDigestionCandidateKind.UNKNOWN,
            pattern_kind=ExternalDigestionPatternKind.UNKNOWN,
            title="Bad",
            summary="Bad",
            extracted_pattern_summary="Bad",
            metadata={"generated_code": True},
        )
    with pytest.raises(ValueError):
        ExternalDigestibilityAssessment(
            assessment_id="bad",
            digestibility_posture=ExternalDigestibilityPosture.DIGESTIBLE,
            route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
            blocker_ids=["blocker:review"],
            ready_for_v0327_internal_candidate_emitter=True,
        )
    with pytest.raises(ValueError):
        ExternalDigestibilityAssessment(
            assessment_id="bad:internal",
            ready_for_internal_candidate_creation=True,
        )
    with pytest.raises(ValueError):
        ExternalDigestionBlocker(
            blocker_id="bad",
            blocker_kind=ExternalDigestionBlockerKind.UNKNOWN,
            metadata={"remediation": True},
        )


def test_pattern_map_candidate_and_candidate_set_do_not_emit_internal_artifacts() -> None:
    source_ref = build_external_digestion_source_ref(
        "digestion-source:skill",
        ExternalDigestionSourceKind.EXTERNAL_MANIFEST_CANDIDATE,
        "candidate:skill",
    )
    signal = build_external_digestion_pattern_signal(
        "pattern-signal:skill",
        [source_ref.source_ref_id],
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        ExternalDigestionPatternKind.CONTRACT_PATTERN,
        "Skill pattern",
        "Static skill pattern signal.",
        "Static skill contract shape.",
    )
    assessment = build_external_digestibility_assessment(
        "assessment:skill",
        pattern_signal_ids=[signal.pattern_signal_id],
        digestibility_posture=ExternalDigestibilityPosture.DIGESTIBLE,
        route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
        ready_for_v0327_internal_candidate_emitter=True,
    )
    pattern_map = build_external_to_internal_pattern_map(
        "pattern-map:skill",
        source_pattern_signal_ids=[signal.pattern_signal_id],
        source_manifest_candidate_ids=["candidate:skill"],
        source_risk_classification_ids=["classification:digestible"],
        suggested_internal_candidate_kind="internal_skill_candidate",
    )
    candidate = build_external_harness_digestion_candidate(
        "digestion-candidate:skill",
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        [source_ref],
        [signal],
        assessment,
        external_to_internal_pattern_map=pattern_map,
        source_manifest_candidate_ids=["candidate:skill"],
        source_risk_classification_ids=["classification:digestible"],
        status=ExternalDigestibilityPosture.DIGESTIBLE,
        route=ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
        ready_for_v0327_internal_candidate_emitter=True,
    )
    candidate_set = build_external_digestion_candidate_set(
        "digestion-candidate-set:1",
        candidates=[candidate],
        accepted_candidate_ids=[candidate.digestion_candidate_id],
        ready_for_v0327_internal_candidate_emitter=True,
    )

    assert isinstance(pattern_map, ExternalToInternalPatternMap)
    assert external_pattern_map_is_not_internalization_plan(pattern_map)
    assert isinstance(candidate, ExternalHarnessDigestionCandidate)
    assert external_digestion_candidate_is_not_internal_candidate(candidate)
    assert candidate.ready_for_internal_candidate_creation is False
    assert candidate.ready_for_internalization is False
    assert candidate.ready_for_execution is False
    assert isinstance(candidate_set, ExternalDigestionCandidateSet)
    assert external_digestion_candidate_set_is_not_registry(candidate_set)

    blocker = build_external_digestion_blocker("blocker:blocks", ExternalDigestionBlockerKind.BLOCKED_RISK_ROUTE)
    with pytest.raises(ValueError):
        ExternalHarnessDigestionCandidate(
            digestion_candidate_id="bad",
            candidate_kind=ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
            source_refs=[source_ref],
            pattern_signals=[signal],
            digestibility_assessment=assessment,
            blockers=[blocker],
            ready_for_v0327_internal_candidate_emitter=True,
        )
    with pytest.raises(ValueError):
        ExternalToInternalPatternMap(
            pattern_map_id="bad",
            ready_for_internal_candidate_emission=True,
        )
    with pytest.raises(ValueError):
        ExternalToInternalPatternMap(
            pattern_map_id="bad:plan",
            metadata={"internalization_plan": True},
        )
    with pytest.raises(ValueError):
        ExternalDigestionCandidateSet(
            candidate_set_id="bad",
            version="v0.32.6",
            metadata={"registry": True},
        )


def test_reports_input_finding_preview_guarantee_and_readiness_are_non_runtime() -> None:
    digestibility_report = build_harness_pattern_digestibility_report(
        "digestibility-report:1",
        pattern_signal_count=1,
        candidate_count=1,
        digestible_count=1,
        key_patterns=["contract_pattern"],
    )
    generation_input = build_external_digestion_candidate_generation_input(
        "generation-input:1",
        risk_classification_report_ids=["risk-report:1"],
        risk_map_ids=["risk-map:1"],
        boundary_map_ids=["boundary-map:1"],
        manifest_candidate_set_ids=["manifest-set:1"],
        requested_candidate_kinds=[ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE],
    )
    finding = build_external_digestion_candidate_generation_finding(
        "finding:skill",
        generation_input.generation_input_id,
        ["digestion-source:skill"],
        "candidate:skill",
        "classification:digestible",
        ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE,
        ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER,
        ExternalDigestibilityPosture.DIGESTIBLE,
        "Static skill pattern candidate selected for v0.32.7 handoff.",
        pattern_signal_ids=["pattern-signal:skill"],
    )
    generation_report = build_external_digestion_candidate_generation_report(
        "generation-report:1",
        generation_input.generation_input_id,
        digestibility_report_id=digestibility_report.digestibility_report_id,
        findings=[finding],
        generated_candidate_count=1,
        ready_for_v0327_internal_candidate_emitter=True,
    )
    preview = build_external_digestion_candidate_run_preview(
        planned_steps=["Select digestible risk classifications."],
        expected_artifacts=["ExternalHarnessDigestionCandidate"],
        explicitly_not_performed=["internal candidate creation", "internalization", "execution"],
    )
    guarantee = build_external_digestion_candidate_no_runtime_guarantee()
    readiness = build_v0326_readiness_report(
        generation_report_id=generation_report.report_id,
        digestibility_report_id=digestibility_report.digestibility_report_id,
        ready_for_v0327_internal_skill_candidate_emitter=True,
    )

    assert isinstance(digestibility_report, HarnessPatternDigestibilityReport)
    assert digestibility_report.ready_for_execution is False
    assert digestibility_report.runtime_certification is False
    assert digestibility_report.internal_candidate_emission is False
    assert isinstance(generation_input, ExternalDigestionCandidateGenerationInput)
    assert generation_input.execution_request is False
    assert "internal candidate creation" in generation_input.prohibited_runtime_actions
    assert "internalization" in generation_input.prohibited_runtime_actions
    assert "dominion target creation" in generation_input.prohibited_runtime_actions
    assert isinstance(finding, ExternalDigestionCandidateGenerationFinding)
    assert finding.internal_skill_candidate is False
    assert finding.certification is False
    assert isinstance(generation_report, ExternalDigestionCandidateGenerationReport)
    assert generation_report.internal_candidate_emission is False
    assert generation_report.runtime_generation is False
    assert generation_report.ready_for_internal_candidate_creation is False
    assert generation_report.ready_for_execution is False
    assert isinstance(preview, ExternalDigestionCandidateRunPreview)
    assert preview.execution is False
    assert all(getattr(preview, name) for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, ExternalDigestionCandidateNoRuntimeGuarantee)
    assert all(getattr(guarantee, name) for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(readiness, V0326ReadinessReport)
    assert v0326_readiness_report_is_not_runtime_ready(readiness)
    assert {
        "harness execution",
        "reference code execution",
        "install",
        "import runtime",
        "plugin loading",
        "external plugin loading",
        "tool registration",
        "tool invocation",
        "mission installation",
        "mission execution",
        "gateway connection",
        "provider invocation",
        "network",
        "credential",
        "secret file read",
        "command",
        "internal candidate creation",
        "internalization",
        "registry mutation",
        "memory mutation",
        "dominion target creation",
        "dominion decision creation",
        "OCEL emission",
    }.issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        HarnessPatternDigestibilityReport(
            digestibility_report_id="bad",
            version="v0.32.6",
            pattern_signal_count=-1,
        )
    with pytest.raises(ValueError):
        ExternalDigestionCandidateGenerationReport(
            report_id="bad",
            version="v0.32.6",
            generation_input_id="generation-input:1",
            ready_for_internal_candidate_creation=True,
        )
    for flag_name in (
        "ready_for_execution",
        "ready_for_internal_candidate_emission",
        "ready_for_internal_skill_candidate_creation",
        "ready_for_internal_tool_candidate_creation",
        "ready_for_internalization",
        "ready_for_registry_mutation",
        "ready_for_memory_mutation",
        "ready_for_plugin_loading",
        "ready_for_tool_registration",
        "ready_for_tool_invocation",
        "ready_for_mission_installation",
        "ready_for_provider_invocation",
        "ready_for_gateway_connection",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
    ):
        with pytest.raises(ValueError):
            V0326ReadinessReport(
                report_id=f"bad:{flag_name}",
                version="v0.32.6",
                **{flag_name: True},
            )


def test_manifest_candidates_and_risk_classifications_can_generate_external_candidates_without_execution(tmp_path) -> None:
    fake_root = tmp_path / "references"
    manifest_candidate = build_external_skill_manifest_candidate(
        "candidate:skill",
        "static-skill",
        risk_surfaces=[],
        metadata={"local_path_ref": str(fake_root)},
    )
    tool_candidate = build_external_tool_manifest_candidate("candidate:tool", "static-tool")
    factor = build_external_capability_risk_factor(
        "risk-factor:digestible",
        "contract_pattern",
        ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN,
        "low",
        "Static pattern is descriptive and digestible.",
    )
    digestible_classification = build_external_capability_risk_classification(
        "classification:digestible",
        target_manifest_candidate_id=manifest_candidate.manifest_candidate_id,
        risk_class=ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR,
        risk_factors=[factor],
        ready_for_v0326_digestion_candidate_generation=True,
    )
    dominion_classification = build_external_capability_risk_classification(
        "classification:dominion",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER,
        ready_for_v0328_dominion_candidate_emitter=True,
    )
    blocked_classification = build_external_capability_risk_classification(
        "classification:blocked",
        risk_class=ExternalCapabilityRiskClass.BLOCKED,
        route=ExternalCapabilityRiskRoute.BLOCK,
    )

    digestion_kind = infer_external_digestion_candidate_kind_from_manifest_candidate(manifest_candidate)
    tool_kind = infer_external_digestion_candidate_kind_from_manifest_candidate(tool_candidate)
    pattern_kind = infer_external_digestion_pattern_kind_from_candidate_kind(digestion_kind)
    route = infer_external_digestion_route_from_risk_classification(digestible_classification)

    assert digestion_kind == ExternalDigestionCandidateKind.SKILL_PATTERN_CANDIDATE
    assert tool_kind == ExternalDigestionCandidateKind.TOOL_CONTRACT_PATTERN_CANDIDATE
    assert pattern_kind == ExternalDigestionPatternKind.CONTRACT_PATTERN
    assert route == ExternalDigestionRoute.SEND_TO_V0327_INTERNAL_CANDIDATE_EMITTER
    assert infer_external_digestion_route_from_risk_classification(dominion_classification) == ExternalDigestionRoute.SEND_TO_V0328_DOMINION_CANDIDATE_EMITTER
    assert infer_external_digestion_blockers_from_risk_classification(dominion_classification) == [ExternalDigestionBlockerKind.DOMINION_REQUIRED_ROUTE]
    assert ExternalDigestionBlockerKind.BLOCKED_RISK_ROUTE in infer_external_digestion_blockers_from_risk_classification(blocked_classification)

    source_ref = build_external_digestion_source_ref(
        "digestion-source:generated",
        ExternalDigestionSourceKind.EXTERNAL_CAPABILITY_RISK_CLASSIFICATION,
        digestible_classification.classification_id,
        manifest_candidate_id=manifest_candidate.manifest_candidate_id,
        risk_classification_id=digestible_classification.classification_id,
    )
    signal = build_external_digestion_pattern_signal(
        "pattern-signal:generated",
        [source_ref.source_ref_id],
        digestion_kind,
        pattern_kind,
        "Generated external digestion signal",
        "Generated from static risk classification metadata.",
        "No code, runtime, or internal artifact is generated.",
    )
    assessment = build_external_digestibility_assessment(
        "assessment:generated",
        pattern_signal_ids=[signal.pattern_signal_id],
        digestibility_posture=ExternalDigestibilityPosture.DIGESTIBLE,
        route=route,
        ready_for_v0327_internal_candidate_emitter=True,
    )
    candidate = build_external_harness_digestion_candidate(
        "digestion-candidate:generated",
        digestion_kind,
        [source_ref],
        [signal],
        assessment,
        source_manifest_candidate_ids=[manifest_candidate.manifest_candidate_id],
        source_risk_classification_ids=[digestible_classification.classification_id],
        route=route,
        status=ExternalDigestibilityPosture.DIGESTIBLE,
        ready_for_v0327_internal_candidate_emitter=True,
    )

    assert external_digestion_candidate_is_not_internal_candidate(candidate)

    with pytest.raises(ValueError):
        ExternalHarnessDigestionCandidate(
            digestion_candidate_id="bad:internal",
            candidate_kind=digestion_kind,
            source_refs=[source_ref],
            pattern_signals=[signal],
            digestibility_assessment=assessment,
            metadata={"internal_skill_candidate": True},
        )
    with pytest.raises(ValueError):
        ExternalToInternalPatternMap(
            pattern_map_id="bad:internalization",
            metadata={"internalization_plan": True},
        )

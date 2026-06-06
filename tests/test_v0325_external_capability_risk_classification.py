import pytest

from chanta_core.external_harness import (
    ExternalCapabilityBoundaryKind,
    ExternalCapabilityBoundaryMap,
    ExternalCapabilityBoundaryRequirement,
    ExternalCapabilityFutureGateItem,
    ExternalCapabilityNoOpRecommendation,
    ExternalCapabilityReviewRequirement,
    ExternalCapabilityReviewRequirementKind,
    ExternalCapabilityRiskClass,
    ExternalCapabilityRiskClassification,
    ExternalCapabilityRiskClassificationFinding,
    ExternalCapabilityRiskClassificationInput,
    ExternalCapabilityRiskClassificationReport,
    ExternalCapabilityRiskClassificationRunPreview,
    ExternalCapabilityRiskClassificationStatus,
    ExternalCapabilityRiskEvidenceQuality,
    ExternalCapabilityRiskFactor,
    ExternalCapabilityRiskMap,
    ExternalCapabilityRiskNoRuntimeGuarantee,
    ExternalCapabilityRiskRoute,
    ExternalCapabilityRiskSeverity,
    ExternalCapabilityRiskSourceKind,
    ExternalCapabilityRiskSourceRef,
    ExternalManifestRiskSurfaceKind,
    V0325ReadinessReport,
    boundary_map_is_not_runtime_enforcement,
    build_external_capability_boundary_map,
    build_external_capability_boundary_requirement,
    build_external_capability_future_gate_item,
    build_external_capability_no_op_recommendation,
    build_external_capability_review_requirement,
    build_external_capability_risk_classification,
    build_external_capability_risk_classification_finding,
    build_external_capability_risk_classification_input,
    build_external_capability_risk_classification_report,
    build_external_capability_risk_classification_run_preview,
    build_external_capability_risk_factor,
    build_external_capability_risk_map,
    build_external_capability_risk_no_runtime_guarantee,
    build_external_capability_risk_source_ref,
    build_external_provider_manifest_candidate,
    build_external_skill_manifest_candidate,
    build_external_tool_manifest_candidate,
    build_v0325_readiness_report,
    capability_classification_is_not_permission,
    classify_manifest_candidate_risk,
    infer_boundary_kinds_from_risk_surfaces,
    infer_review_requirements_from_risk_surfaces,
    infer_risk_route_from_class_and_surfaces,
    risk_map_is_not_permission_map,
    v0325_readiness_report_is_not_runtime_ready,
)


def test_external_capability_risk_taxonomies_include_required_values() -> None:
    assert {item.value for item in ExternalCapabilityRiskClass} >= {
        "safe_descriptive",
        "digestible_pattern",
        "requires_review",
        "dominion_required",
        "blocked",
        "future_track",
        "no_op",
        "unknown",
    }
    assert {item.value for item in ExternalCapabilityRiskSeverity} >= {
        "unknown",
        "none",
        "low",
        "medium",
        "high",
        "critical",
        "blocked",
        "future_track",
    }
    assert {item.value for item in ExternalCapabilityRiskRoute} >= {
        "describe_only",
        "send_to_v0326_digestion_generator",
        "send_to_v0328_dominion_emitter",
        "require_review",
        "require_future_gate",
        "reject",
        "block",
        "no_op",
        "unknown",
    }
    assert {item.value for item in ExternalCapabilityBoundaryKind} >= {
        "no_execution",
        "no_reference_code_execution",
        "no_runtime_import",
        "no_dependency_install",
        "no_plugin_loading",
        "no_tool_registration",
        "no_tool_invocation",
        "no_mission_installation",
        "no_mission_execution",
        "no_provider_invocation",
        "no_gateway_connection",
        "no_channel_access",
        "no_message_send",
        "no_webhook_call",
        "no_workspace_write",
        "no_code_edit",
        "no_patch_application",
        "no_network_access",
        "no_credential_access",
        "no_secret_file_read",
        "no_command_execution",
        "no_browser_automation",
        "no_rpa_control",
        "no_registry_mutation",
        "no_memory_mutation",
        "no_private_data_access",
        "no_raw_output_persistence",
        "no_ocel_emission",
        "approval_required",
        "audit_required",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in ExternalCapabilityReviewRequirementKind} >= {
        "evidence_review",
        "boundary_review",
        "security_review",
        "privacy_review",
        "credential_review",
        "network_review",
        "command_review",
        "provider_review",
        "plugin_review",
        "gateway_review",
        "memory_review",
        "registry_review",
        "ocel_trace_review",
        "human_review",
        "future_gate_review",
        "unknown",
    }
    assert {item.value for item in ExternalCapabilityRiskClassificationStatus} >= {
        "unknown",
        "draft",
        "classified",
        "classified_with_gaps",
        "blocked",
        "deferred",
        "rejected",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ExternalCapabilityRiskEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_risk_classification",
        "sufficient_for_v0326_review",
        "sufficient_for_v0328_review",
        "conflicting",
        "blocked",
    }
    assert {item.value for item in ExternalCapabilityRiskSourceKind} >= {
        "external_manifest_candidate",
        "external_manifest_candidate_set",
        "external_manifest_extraction_report",
        "opencode_observation_output",
        "openclaw_observation_output",
        "hermes_observation_output",
        "reference_file_inventory",
        "reference_corpus_snapshot",
        "manual_risk_review",
        "sanitized_risk_manifest",
        "unknown",
    }


def test_source_ref_risk_factor_boundary_and_review_are_governance_only() -> None:
    source_ref = build_external_capability_risk_source_ref(
        source_ref_id="risk-source:1",
        source_kind=ExternalCapabilityRiskSourceKind.EXTERNAL_MANIFEST_CANDIDATE,
        source_id="candidate:tool",
        manifest_candidate_id="candidate:tool",
        reference_entry_ids=["entry:tool"],
    )
    factor = build_external_capability_risk_factor(
        risk_factor_id="risk-factor:tool-registration",
        risk_surface=ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION,
        risk_class=ExternalCapabilityRiskClass.REQUIRES_REVIEW,
        severity=ExternalCapabilityRiskSeverity.HIGH,
        summary="Tool registration remains review-gated static metadata.",
        boundary_kinds=[ExternalCapabilityBoundaryKind.NO_TOOL_REGISTRATION],
        review_requirements=[ExternalCapabilityReviewRequirementKind.REGISTRY_REVIEW],
    )
    boundary = build_external_capability_boundary_requirement(
        boundary_requirement_id="boundary:tool-registration",
        boundary_kind=ExternalCapabilityBoundaryKind.NO_TOOL_REGISTRATION,
        target_risk_factor_ids=[factor.risk_factor_id],
    )
    review = build_external_capability_review_requirement(
        review_requirement_id="review:tool-registration",
        requirement_kind=ExternalCapabilityReviewRequirementKind.REGISTRY_REVIEW,
        target_risk_factor_ids=[factor.risk_factor_id],
    )

    assert isinstance(source_ref, ExternalCapabilityRiskSourceRef)
    assert source_ref.source_fetch is False
    assert source_ref.execution is False
    assert isinstance(factor, ExternalCapabilityRiskFactor)
    assert factor.proof_of_exploitability is False
    assert factor.permission is False
    assert isinstance(boundary, ExternalCapabilityBoundaryRequirement)
    assert boundary.blocks_execution is True
    assert boundary.blocks_activation is True
    assert boundary.blocks_runtime_registration is True
    assert boundary.runtime_enforcement is False
    assert isinstance(review, ExternalCapabilityReviewRequirement)
    assert review.approval_granted is False
    assert review.approval is False

    with pytest.raises(ValueError):
        ExternalCapabilityRiskSourceRef(
            source_ref_id="bad",
            source_kind=ExternalCapabilityRiskSourceKind.REFERENCE_FILE_INVENTORY,
            source_id="source",
            metadata={"source_fetch": True},
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskFactor(
            risk_factor_id="bad",
            risk_surface="command_execution",
            risk_class=ExternalCapabilityRiskClass.BLOCKED,
            severity=ExternalCapabilityRiskSeverity.CRITICAL,
            summary="Missing required boundary/review.",
        )
    with pytest.raises(ValueError):
        ExternalCapabilityBoundaryRequirement(
            boundary_requirement_id="bad",
            boundary_kind=ExternalCapabilityBoundaryKind.NO_EXECUTION,
            blocks_execution=False,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityReviewRequirement(
            review_requirement_id="bad",
            requirement_kind=ExternalCapabilityReviewRequirementKind.HUMAN_REVIEW,
            approval_granted=True,
        )


def test_risk_classification_routes_are_not_permission_or_active_artifacts() -> None:
    source_ref = build_external_capability_risk_source_ref(
        "risk-source:digestible",
        ExternalCapabilityRiskSourceKind.SANITIZED_RISK_MANIFEST,
        "sanitized:pattern",
    )
    digestible = build_external_capability_risk_classification(
        classification_id="classification:digestible",
        source_refs=[source_ref],
        risk_class=ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR,
        severity=ExternalCapabilityRiskSeverity.LOW,
        status=ExternalCapabilityRiskClassificationStatus.CLASSIFIED,
        ready_for_v0326_digestion_candidate_generation=True,
    )
    dominion = build_external_capability_risk_classification(
        classification_id="classification:dominion",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER,
        severity=ExternalCapabilityRiskSeverity.HIGH,
        status=ExternalCapabilityRiskClassificationStatus.CLASSIFIED_WITH_GAPS,
        ready_for_v0328_dominion_candidate_emitter=True,
    )

    assert isinstance(digestible, ExternalCapabilityRiskClassification)
    assert capability_classification_is_not_permission(digestible)
    assert digestible.ready_for_v0326_digestion_candidate_generation is True
    assert digestible.digestion_candidate is False
    assert isinstance(dominion, ExternalCapabilityRiskClassification)
    assert capability_classification_is_not_permission(dominion)
    assert dominion.ready_for_v0328_dominion_candidate_emitter is True
    assert dominion.dominion_target is False

    blocking_boundary = build_external_capability_boundary_requirement(
        "boundary:blocking",
        ExternalCapabilityBoundaryKind.NO_COMMAND_EXECUTION,
    )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:permission",
            ready_for_capability_permission=True,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:certification",
            ready_for_runtime_certification=True,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:execution",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:v0326",
            risk_class=ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN,
            route=ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR,
            boundary_requirements=[blocking_boundary],
            ready_for_v0326_digestion_candidate_generation=True,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:active-artifact",
            metadata={"digestion_candidate": True},
        )
    with pytest.raises(ValueError):
        ExternalCapabilityRiskClassification(
            classification_id="bad:dominion",
            metadata={"dominion_target": True},
        )


def test_maps_noop_future_gate_input_finding_report_preview_guarantee_and_readiness_are_non_runtime() -> None:
    boundary = build_external_capability_boundary_requirement(
        "boundary:provider",
        ExternalCapabilityBoundaryKind.NO_PROVIDER_INVOCATION,
    )
    review = build_external_capability_review_requirement(
        "review:provider",
        ExternalCapabilityReviewRequirementKind.PROVIDER_REVIEW,
    )
    risk_map = build_external_capability_risk_map(
        "risk-map:1",
        classification_ids=["classification:provider"],
        dominion_required_classification_ids=["classification:provider"],
        high_risk_factor_ids=["risk-factor:provider"],
    )
    boundary_map = build_external_capability_boundary_map(
        "boundary-map:1",
        boundary_requirements=[boundary],
        review_requirements=[review],
        prohibited_runtime_surfaces=["provider_invocation"],
    )
    no_op = build_external_capability_no_op_recommendation(
        "no-op:unknown",
        reason="Unknown-only surface should remain descriptive or no-op.",
        safe_alternatives=["defer to later review"],
    )
    future_gate = build_external_capability_future_gate_item(
        "future-gate:provider",
        "provider-risk-review",
        required_artifacts=["risk classification evidence"],
        required_reviews=[ExternalCapabilityReviewRequirementKind.PROVIDER_REVIEW],
    )
    classification_input = build_external_capability_risk_classification_input(
        "risk-input:1",
        manifest_candidate_set_ids=["candidate-set:1"],
        manifest_extraction_report_ids=["manifest-report:1"],
        requested_risk_classes=[ExternalCapabilityRiskClass.DOMINION_REQUIRED],
    )
    finding = build_external_capability_risk_classification_finding(
        finding_id="finding:provider",
        classification_input_id=classification_input.classification_input_id,
        source_ref_ids=["risk-source:provider"],
        target_manifest_candidate_id="candidate:provider",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER,
        severity=ExternalCapabilityRiskSeverity.HIGH,
        summary="Provider capability requires dominion-route review.",
        risk_factor_ids=["risk-factor:provider"],
        boundary_requirement_ids=[boundary.boundary_requirement_id],
        review_requirement_ids=[review.review_requirement_id],
    )
    classification = build_external_capability_risk_classification(
        "classification:provider",
        risk_class=ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        route=ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER,
        severity=ExternalCapabilityRiskSeverity.HIGH,
    )
    report = build_external_capability_risk_classification_report(
        report_id="risk-report:1",
        classification_input_id=classification_input.classification_input_id,
        risk_map_id=risk_map.risk_map_id,
        boundary_map_id=boundary_map.boundary_map_id,
        classifications=[classification],
        findings=[finding],
        no_op_recommendations=[no_op],
        future_gate_items=[future_gate],
        classified_count=1,
    )
    preview = build_external_capability_risk_classification_run_preview(
        planned_steps=["Classify static manifest candidate risk surfaces."],
        expected_artifacts=["ExternalCapabilityRiskClassificationReport"],
        explicitly_not_performed=["permission", "runtime certification", "active candidate creation"],
    )
    guarantee = build_external_capability_risk_no_runtime_guarantee()
    readiness = build_v0325_readiness_report(
        classification_report_id=report.report_id,
        risk_map_id=risk_map.risk_map_id,
        boundary_map_id=boundary_map.boundary_map_id,
    )

    assert isinstance(risk_map, ExternalCapabilityRiskMap)
    assert risk_map_is_not_permission_map(risk_map)
    assert isinstance(boundary_map, ExternalCapabilityBoundaryMap)
    assert boundary_map_is_not_runtime_enforcement(boundary_map)
    assert isinstance(no_op, ExternalCapabilityNoOpRecommendation)
    assert no_op.failure is False
    assert no_op.execution is False
    assert isinstance(future_gate, ExternalCapabilityFutureGateItem)
    assert future_gate.ready_now is False
    assert future_gate.readiness is False
    assert isinstance(classification_input, ExternalCapabilityRiskClassificationInput)
    assert classification_input.execution_request is False
    assert "digestion candidate creation" in classification_input.prohibited_runtime_actions
    assert "dominion target creation" in classification_input.prohibited_runtime_actions
    assert isinstance(finding, ExternalCapabilityRiskClassificationFinding)
    assert finding.certification is False
    assert finding.permission is False
    assert isinstance(report, ExternalCapabilityRiskClassificationReport)
    assert report.ready_for_execution is False
    assert report.runtime_classification is False
    assert isinstance(preview, ExternalCapabilityRiskClassificationRunPreview)
    assert preview.execution is False
    assert all(getattr(preview, name) for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(guarantee, ExternalCapabilityRiskNoRuntimeGuarantee)
    assert all(getattr(guarantee, name) for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert isinstance(readiness, V0325ReadinessReport)
    assert v0325_readiness_report_is_not_runtime_ready(readiness)
    assert {
        "capability permission",
        "runtime certification",
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
        "digestion candidate creation",
        "internal candidate creation",
        "dominion target creation",
        "dominion decision creation",
        "registry mutation",
        "memory mutation",
        "OCEL emission",
    }.issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        ExternalCapabilityBoundaryMap(
            boundary_map_id="bad",
            version="v0.32.5",
            ready_for_runtime_enforcement=True,
        )
    with pytest.raises(ValueError):
        ExternalCapabilityFutureGateItem(
            future_gate_id="bad",
            gate_kind="gate",
            ready_now=True,
        )
    for flag_name in (
        "ready_for_digestion_candidate_creation",
        "ready_for_internal_candidate_creation",
        "ready_for_dominion_target_creation",
        "ready_for_dominion_decision_creation",
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
            V0325ReadinessReport(
                report_id=f"bad:{flag_name}",
                version="v0.32.5",
                **{flag_name: True},
            )


def test_manifest_candidates_can_be_classified_without_execution(tmp_path) -> None:
    fake_root = tmp_path / "references"
    safe_skill = build_external_skill_manifest_candidate(
        "candidate:skill:safe",
        "static-skill",
        risk_surfaces=[],
        metadata={"local_path_ref": str(fake_root)},
    )
    tool = build_external_tool_manifest_candidate("candidate:tool", "static-tool")
    provider = build_external_provider_manifest_candidate("candidate:provider", "static-provider")
    blocked = build_external_tool_manifest_candidate(
        "candidate:blocked",
        "blocked-tool",
        risk_surfaces=[ExternalManifestRiskSurfaceKind.COMMAND_EXECUTION],
    )

    assert classify_manifest_candidate_risk(safe_skill) == ExternalCapabilityRiskClass.SAFE_DESCRIPTIVE
    assert classify_manifest_candidate_risk(tool) == ExternalCapabilityRiskClass.REQUIRES_REVIEW
    assert classify_manifest_candidate_risk(provider) == ExternalCapabilityRiskClass.DOMINION_REQUIRED
    assert classify_manifest_candidate_risk(blocked) == ExternalCapabilityRiskClass.BLOCKED
    assert infer_risk_route_from_class_and_surfaces(
        ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN,
        [],
    ) == ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR
    assert infer_risk_route_from_class_and_surfaces(
        ExternalCapabilityRiskClass.DOMINION_REQUIRED,
        provider.risk_surfaces,
    ) == ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER
    provider_boundaries = infer_boundary_kinds_from_risk_surfaces(provider.risk_surfaces)
    provider_reviews = infer_review_requirements_from_risk_surfaces(provider.risk_surfaces)
    assert ExternalCapabilityBoundaryKind.NO_PROVIDER_INVOCATION in provider_boundaries
    assert ExternalCapabilityBoundaryKind.NO_NETWORK_ACCESS in provider_boundaries
    assert ExternalCapabilityBoundaryKind.NO_CREDENTIAL_ACCESS in provider_boundaries
    assert ExternalCapabilityReviewRequirementKind.PROVIDER_REVIEW in provider_reviews
    assert ExternalCapabilityReviewRequirementKind.NETWORK_REVIEW in provider_reviews
    assert ExternalCapabilityReviewRequirementKind.CREDENTIAL_REVIEW in provider_reviews

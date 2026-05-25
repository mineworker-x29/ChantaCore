from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_RESPONSE_ASSEMBLY_EFFECT_TYPES,
    AGENT_RESPONSE_ASSEMBLY_EVENT_TYPES,
    AGENT_RESPONSE_ASSEMBLY_OBJECT_TYPES,
    AGENT_RESPONSE_ASSEMBLY_RELATION_TYPES,
    AGENT_RESPONSE_ASSEMBLY_VERSION,
    AgentAnswerDraft,
    AgentAnswerDraftService,
    AgentAssembledResponse,
    AgentBlockedResponseDraft,
    AgentClaim,
    AgentClaimSupport,
    AgentClarificationResponseDraft,
    AgentDeferredResponseDraft,
    AgentEvidenceBindingPolicyService,
    AgentEvidenceBundle,
    AgentEvidenceBundleService,
    AgentEvidenceItem,
    AgentEvidenceSourceRef,
    AgentLimitationNote,
    AgentNoActionResponseDraft,
    AgentProviderInvocationReportService,
    AgentResponseAssemblyPolicyService,
    AgentResponseAssemblyReport,
    AgentResponseAssemblyReportService,
    AgentResponseAssemblyRequest,
    AgentResponseAssemblyTrace,
    AgentResponseSection,
    AgentSafetyGateReportService,
    AgentUncertaintyNote,
)
from chanta_core.cli.main import main


def _service() -> AgentResponseAssemblyReportService:
    return AgentResponseAssemblyReportService()


def test_response_assembly_policy_builds_with_v0256_boundaries() -> None:
    policy = AgentResponseAssemblyPolicyService().build_policy()

    assert policy.version == AGENT_RESPONSE_ASSEMBLY_VERSION
    assert policy.layer == "agent_surface"
    assert policy.deterministic_default is True
    assert policy.external_llm_response_generation_enabled is False
    assert policy.llm_factuality_judge_enabled is False
    assert policy.llm_safety_judge_enabled is False
    assert policy.response_assembly_enabled is True
    assert policy.response_emission_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.require_evidence_for_provider_claims is True
    assert policy.fact_inference_uncertainty_separation_required is True
    assert policy.provider_result_label_required is True
    assert policy.no_action_rationale_required is True
    assert policy.blocked_rationale_required is True
    assert policy.clarification_questions_required_when_selected is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_secret_output_forbidden is True
    assert policy.credential_output_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.final_conclusion_once is True
    assert policy.max_response_chars > 0
    assert policy.max_evidence_items > 0


def test_response_assembly_models_build() -> None:
    request = AgentResponseAssemblyRequest(request_id="assembly-request:test")
    source_ref = AgentEvidenceSourceRef(
        source_ref_id="source-ref:test",
        source_type="provider_result_ref",
        source_id="result-ref:test",
        provider_id="internal_provider:workspace_read_provider",
        provider_type="workspace_read_provider",
        sanitized_label="workspace provider result reference",
    )
    evidence_item = AgentEvidenceItem(
        evidence_item_id="evidence-item:test",
        evidence_kind="observed_provider_result",
        source_ref=source_ref,
        summary="provider observation",
        supports_claim_ids=["claim:test"],
        confidence="medium",
    )
    bundle = AgentEvidenceBundle(
        evidence_bundle_id="evidence-bundle:test",
        evidence_items=[evidence_item],
        evidence_count=1,
        provider_evidence_count=1,
    )
    claim = AgentClaim(
        claim_id="claim:test",
        claim_type="provider_observation",
        text="provider observation",
        confidence="medium",
        requires_evidence=True,
        evidence_item_ids=[evidence_item.evidence_item_id],
        unsupported=False,
    )
    support = AgentClaimSupport(
        support_id="support:test",
        claim_id=claim.claim_id,
        evidence_item_ids=[evidence_item.evidence_item_id],
        support_status="supported",
    )
    section = AgentResponseSection(
        section_id="section:test",
        section_type="observations",
        title="Observations",
        body="Observation body",
        claim_ids=[claim.claim_id],
        evidence_item_ids=[evidence_item.evidence_item_id],
        section_status="ready",
    )
    uncertainty = AgentUncertaintyNote(
        uncertainty_id="uncertainty:test",
        message="uncertain",
        cause="missing_evidence",
        affected_claim_ids=[claim.claim_id],
    )
    limitation = AgentLimitationNote(
        limitation_id="limitation:test",
        message="limited",
        limitation_type="future_track",
    )
    no_action = AgentNoActionResponseDraft(
        draft_id="no-action-draft:test",
        no_action_decision_ref={"id": "no-action"},
        rationale="rationale",
        safe_alternative=None,
        sections=[section],
    )
    clarification = AgentClarificationResponseDraft(
        draft_id="clarification-draft:test",
        clarification_decision_ref={"id": "clarification"},
        questions=["Which target?"],
        rationale="missing target",
        sections=[section],
    )
    blocked = AgentBlockedResponseDraft(
        draft_id="blocked-draft:test",
        blocked_decision_ref={"id": "blocked"},
        blocked_reason="policy",
        safe_alternative="safe alternative",
        sections=[section],
    )
    deferred = AgentDeferredResponseDraft(
        draft_id="deferred-draft:test",
        deferred_decision_ref={"id": "deferred"},
        deferred_to_track="v0.27.x",
        deferred_reason="future track",
        sections=[section],
    )
    answer = AgentAnswerDraft(
        draft_id="answer-draft:test",
        response_mode="provider_backed_answer",
        claims=[claim],
        claim_supports=[support],
        sections=[section],
        uncertainty_notes=[uncertainty],
        limitation_notes=[limitation],
        draft_status="ready",
        evidence_bundle_id=bundle.evidence_bundle_id,
    )
    assembled = AgentAssembledResponse(
        assembled_response_id="assembled:test",
        created_at="now",
        request_ref={"id": request.request_id},
        answer_draft=answer,
        response_text="text",
        response_status="assembled",
    )
    trace = AgentResponseAssemblyTrace(
        trace_id="trace:test",
        assembly_request_id=request.request_id,
    )
    report = AgentResponseAssemblyReport(
        report_id="report:test",
        policy=AgentResponseAssemblyPolicyService().build_policy(),
        request=request,
        evidence_binding_policy=AgentEvidenceBindingPolicyService().build_policy(),
        evidence_bundle=bundle,
        answer_draft=answer,
        assembled_response=assembled,
        assembly_trace=trace,
    )

    assert request.version == "v0.25.6"
    assert source_ref.raw_content_included is False
    assert evidence_item.raw_secret_included is False
    assert bundle.raw_provider_output_inline is False
    assert claim.claim_type == "provider_observation"
    assert support.support_status == "supported"
    assert section.section_status == "ready"
    assert uncertainty.cause == "missing_evidence"
    assert limitation.limitation_type == "future_track"
    assert no_action.rationale
    assert clarification.questions
    assert blocked.safe_alternative
    assert deferred.deferred_to_track == "v0.27.x"
    assert answer.final_conclusion_once is True
    assert assembled.response_assembled is True
    assert assembled.final_response_emitted is False
    assert trace.ocel_visible is True
    assert report.ready_for_v0_26 is False


def test_provider_invocation_report_evidence_seed_and_bundle_can_be_loaded() -> None:
    provider_report = AgentProviderInvocationReportService().build_report("Explain the project structure")
    report = _service().build_report(provider_report=provider_report)

    assert provider_report.evidence_seed.ready_for_evidence_binder is True
    assert provider_report.result_bundle.result_count >= 1
    assert report.request.provider_invocation_report_id == provider_report.report_id
    assert report.request.evidence_seed_id == provider_report.evidence_seed.evidence_seed_id
    assert report.evidence_bundle.provider_evidence_count >= 1
    assert report.answer_draft.response_mode == "provider_backed_answer"
    assert report.response_assembled is True
    assert report.final_response_emitted is False
    assert report.ready_for_v0_25_7 is True


def test_gate_outcome_can_build_non_provider_response_drafts() -> None:
    cases = [
        ("Do nothing and stop here", "no_action_response", "no_action_response_created"),
        ("unclear ambiguous target", "clarification_response", "clarification_response_created"),
        ("Print token=ghp_example and password=hunter2", "blocked_response", "blocked_response_created"),
        ("Promote this into persistent memory continuity", "deferred_response", "deferred_response_created"),
    ]
    for text, response_mode, finding_type in cases:
        safety_report = AgentSafetyGateReportService().build_report(text)
        report = _service().build_report(safety_gate_report=safety_report, use_provider_report=False)
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.answer_draft.response_mode == response_mode
        assert finding_type in finding_types
        assert report.provider_invoked is False
        assert report.ask_executed is False
        assert report.repl_started is False
        assert report.final_response_emitted is False
        assert report.ready_for_v0_25_7 is True


def test_evidence_binding_counts_and_sanitizes_refs() -> None:
    report = _service().build_report("Explain the project structure")
    bundle = report.evidence_bundle

    assert bundle.evidence_count >= 1
    assert bundle.provider_evidence_count >= 1
    assert bundle.policy_evidence_count >= 0
    assert bundle.uncertainty_evidence_count >= 0
    assert bundle.bundle_status in {"ready", "warning", "failed", "blocked"}
    assert bundle.raw_provider_output_inline is False
    assert bundle.raw_secret_output is False
    assert bundle.credential_exposed is False
    assert bundle.private_full_paths_included is False
    for item in bundle.evidence_items:
        assert item.source_ref is not None
        assert item.source_ref.raw_content_included is False
        assert item.source_ref.raw_secret_included is False
        assert item.source_ref.credential_included is False
        assert item.source_ref.private_full_path_included is False


def test_claim_support_and_separation_rules() -> None:
    report = _service().build_report("Explain the project structure")
    claims = report.answer_draft.claims
    supports = report.answer_draft.claim_supports
    claim_types = {claim.claim_type for claim in claims}

    assert "provider_observation" in claim_types
    assert "inference" in claim_types
    assert all(claim.evidence_item_ids for claim in claims if claim.requires_evidence)
    assert all(not claim.unsupported for claim in claims)
    assert all(support.support_status in {"supported", "weakly_supported", "unsupported", "not_required"} for support in supports)
    assert all(support.support_status == "supported" for support in supports)


def test_unsupported_claim_and_uncertainty_can_be_represented() -> None:
    empty_bundle = AgentEvidenceBundleService().build_bundle([])
    claims = __import__(
        "chanta_core.agent_surface.response_assembly",
        fromlist=["AgentClaimService"],
    ).AgentClaimService().build_claims(empty_bundle)
    supports = __import__(
        "chanta_core.agent_surface.response_assembly",
        fromlist=["AgentClaimSupportService"],
    ).AgentClaimSupportService().bind_claims_to_evidence(claims, empty_bundle)

    assert any(claim.unsupported for claim in claims)
    assert any(support.support_status == "unsupported" for support in supports)


def test_response_sections_and_conclusion_once() -> None:
    report = _service().build_report("Explain the project structure")
    sections = report.answer_draft.sections
    section_types = {section.section_type for section in sections}

    assert {"direct_answer", "observations", "evidence", "inference", "limitations", "final_conclusion"}.issubset(section_types)
    assert sum(1 for section in sections if section.section_type == "final_conclusion") == 1
    assert all(section.body for section in sections)
    assert all(section.section_status in {"ready", "warning", "blocked"} for section in sections)


def test_answer_draft_and_assembled_response_flags() -> None:
    report = _service().build_report("Explain the project structure")
    draft = report.answer_draft
    assembled = report.assembled_response

    assert draft.draft_status in {"ready", "warning", "failed", "blocked"}
    assert draft.raw_provider_output_inline is False
    assert draft.raw_secret_output is False
    assert draft.credential_exposed is False
    assert draft.private_full_paths_included is False
    assert assembled.response_text
    assert assembled.response_assembled is True
    assert assembled.final_response_emitted is False
    assert assembled.ask_executed is False
    assert assembled.repl_started is False
    assert assembled.provider_invoked_in_v0256 is False
    assert assembled.local_command_executed is False
    assert assembled.memory_promoted is False
    assert assembled.persona_mutated is False
    assert assembled.next_required_step == "v0.25.7 Ask / REPL Surface"


def test_response_assembly_trace_report_flags_and_readiness() -> None:
    report = _service().build_report("Explain the project structure")
    trace = report.assembly_trace

    assert trace.ocel_visible is True
    assert trace.pig_visible is True
    assert trace.ocpx_visible is True
    assert trace.raw_secret_in_trace is False
    assert trace.private_full_path_in_trace is False
    assert report.report_status in {"passed", "warning", "failed", "blocked"}
    assert report.ready_for_v0_25_7 is True
    assert report.ready_for_v0_26 is False
    assert report.response_assembled is True
    assert report.final_response_emitted is False
    assert report.evidence_bound is True
    assert report.unsupported_claim_count == 0
    assert report.limitation_note_count >= 1
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.llm_judge_used is False


def test_ocel_pig_ocpx_mapping_and_reports() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "agent_response_assembly_policy" in AGENT_RESPONSE_ASSEMBLY_OBJECT_TYPES
    assert "agent_response_assembly_requested" in AGENT_RESPONSE_ASSEMBLY_EVENT_TYPES
    assert "uses_agent_provider_evidence_seed" in AGENT_RESPONSE_ASSEMBLY_RELATION_TYPES
    assert "agent_response_assembled" in AGENT_RESPONSE_ASSEMBLY_EFFECT_TYPES
    assert pig["version"] == "v0.25.6"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "response_assembly_evidence_binder"
    assert pig["safety_boundary"]["response_assembled"] == "conditional"
    assert pig["safety_boundary"]["final_response_emitted"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["raw_provider_output_inline"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_response_assembled_evidence_bound"
    assert "AgentEvidenceBundleState" in ocpx["target_read_models"]
    assert "AgentAssembledResponseState" in ocpx["target_read_models"]


def test_cli_response_commands_render_sanitized_output(capsys) -> None:
    commands = [
        ["agent", "response", "assemble", "--provider-report-id", "demo"],
        ["agent", "response", "assemble", "--safety-report-id", "demo"],
        ["agent", "response", "evidence", "--report-id", "demo"],
        ["agent", "response", "draft", "--report-id", "demo"],
        ["agent", "response", "assembled", "--report-id", "demo"],
        ["agent", "response", "findings", "--report-id", "demo"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.25.6" in output
        assert "layer=agent_surface" in output
        assert "response_assembled=true" in output
        assert "final_response_emitted=false" in output
        assert "evidence_bound=true" in output
        assert "ready_for_v0_25_7=true" in output
        assert "ready_for_v0_26=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output
        assert "ask_executed=false" in output
        assert "repl_started=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "llm_judge_used=false" in output

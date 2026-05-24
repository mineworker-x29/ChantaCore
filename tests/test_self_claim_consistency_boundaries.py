from __future__ import annotations

from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    ClaimEvidenceMatch,
    ClaimEvidenceRequirement,
    ContradictionRegisterEntry,
    SelfClaim,
    SelfClaimConsistencyReport,
    SelfClaimConsistencyRequest,
    SelfClaimConsistencyService,
    SelfClaimSourceRef,
    SelfContradictionRegister,
)


RUNTIME_FILE = Path("src/chanta_core/deep_self_introspection/claim_consistency.py")
DOC_FILE = Path("docs/versions/v0.21/v0.21.7_self_claim_consistency.md")


def test_model_types_are_exported() -> None:
    assert SelfClaimConsistencyRequest
    assert SelfClaimSourceRef
    assert SelfClaim
    assert ClaimEvidenceRequirement
    assert ClaimEvidenceMatch
    assert ContradictionRegisterEntry
    assert SelfContradictionRegister
    assert SelfClaimConsistencyReport


def test_docs_define_version_identity_and_non_goals() -> None:
    content = DOC_FILE.read_text(encoding="utf-8")

    assert "Self-Claim Consistency & Contradiction Register" in content
    assert "자기 주장 정합성·모순 등록부" in content
    assert "LLM statement is not evidence" in content
    assert "Claim without OCEL evidence is not truth" in content
    assert "Contradiction register is not auto-correction" in content
    assert "Claim consistency check is not claim rewriting" in content
    assert "v0.21.6" in content
    assert "v0.21.8 Deep Self-Introspection Workbench" in content


def test_ocel_mapping_includes_claim_consistency_types() -> None:
    for object_type in [
        "self_claim",
        "self_claim_source",
        "claim_evidence_requirement",
        "claim_evidence_match",
        "claim_consistency_report",
        "claim_consistency_finding",
        "contradiction_register",
        "contradiction_register_entry",
        "unsupported_claim",
        "unverifiable_claim",
        "capability_truth_report",
        "runtime_boundary_truth_report",
        "policy_gate_truth_report",
        "trace_integrity_report",
        "context_projection_truth_report",
        "candidate_memory_boundary_report",
        "execution_envelope",
        "ocel_event_ref",
        "ocel_object_ref",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_claim_consistency_check_requested",
        "deep_self_claim_sources_collected",
        "deep_self_claims_extracted",
        "deep_self_claim_evidence_requirements_mapped",
        "deep_self_claim_evidence_matched",
        "deep_self_claim_consistency_checked",
        "deep_self_contradiction_detected",
        "deep_self_contradiction_register_created",
        "deep_self_claim_consistency_report_created",
        "deep_self_claim_consistency_warning_created",
        "deep_self_claim_consistency_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "claim_derived_from_source",
        "claim_requires_evidence",
        "claim_supported_by_evidence",
        "claim_missing_evidence",
        "claim_contradicted_by_evidence",
        "claim_contradicts_capability_truth",
        "claim_contradicts_runtime_boundary",
        "claim_contradicts_policy_gate",
        "claim_contradicts_trace_integrity",
        "claim_contradicts_context_projection",
        "claim_contradicts_candidate_memory_boundary",
        "registered_in_contradiction_register",
        "supports_claim_finding",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_candidate_memory_boundary",
        "derived_from_context_projection",
        "derived_from_trace_integrity",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES
    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_contradiction_register_does_not_auto_resolve_entries() -> None:
    service = SelfClaimConsistencyService()
    service.check_claim_consistency(
        SelfClaimConsistencyRequest(
            claim_payload={
                "claims": [
                    {
                        "claim_type": "policy_claim",
                        "normalized_claim": "policy permits permission grant creation",
                        "object_ref": {"permission_grant_creation_allowed": True},
                        "confidence": "high",
                    }
                ]
            }
        )
    )
    register = service.last_register

    assert register is not None
    assert register.read_only is True
    assert register.mutation_performed is False
    assert register.entries
    assert {entry.status for entry in register.entries} == {"open"}


def test_cli_output_is_sanitized() -> None:
    report = SelfClaimConsistencyService().check_claim_consistency(
        SelfClaimConsistencyRequest(
            claim_payload={
                "claims": [
                    {
                        "claim_id": "claim:summary",
                        "claim_type": "unsupported_claim",
                        "normalized_claim": "sanitized summary only",
                        "claim_text": "line one\nline two",
                        "confidence": "low",
                    }
                ]
            }
        )
    )
    service = SelfClaimConsistencyService()
    service.last_report = report
    output = service.render_cli("claim consistency", report=report)

    assert "sanitized summary only" in output
    assert "line one" not in output
    assert "raw_prompt_body_printed=False" in output
    assert "raw_transcript_printed=False" in output
    assert "private_full_paths_printed=False" in output
    assert "raw_secrets_printed=False" in output


def test_runtime_implementation_does_not_add_forbidden_calls() -> None:
    content = RUNTIME_FILE.read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "rewrite_claim(",
        "auto_correct(",
        "modify_response(",
        "rewrite_response(",
        "modify_prompt(",
        "promote_memory(",
        "memory_write(",
        "create_memory_entry(",
        "update_memory(",
        "persona_update(",
        "overlay_update(",
        "promote_candidate(",
        "materialize(",
        "apply_patch(",
        "write_file(",
        "repair_trace(",
        "backfill(",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    for token in forbidden_call_tokens:
        assert token not in content


def test_jsonl_is_not_canonical_store() -> None:
    service = SelfClaimConsistencyService()
    assert service.build_ocpx_projection()["canonical_store"] == "ocel"
    assert "jsonl" not in RUNTIME_FILE.read_text(encoding="utf-8").lower()

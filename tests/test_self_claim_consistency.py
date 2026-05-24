from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from chanta_core.deep_self_introspection import (
    SelfCapabilityRegistryAwarenessService,
    SelfClaimConsistencyRequest,
    SelfClaimConsistencyService,
)


FIXTURES = Path(__file__).parent / "fixtures"


def _claim(
    claim_type: str,
    *,
    claim_id: str | None = None,
    normalized_claim: str | None = None,
    predicate: str | None = None,
    object_ref: dict[str, object] | None = None,
    confidence: str = "high",
) -> dict[str, object]:
    return {
        "claim_id": claim_id or f"claim:{claim_type}",
        "claim_type": claim_type,
        "normalized_claim": normalized_claim or claim_type.replace("_", " "),
        "predicate": predicate or "asserts",
        "object_ref": object_ref or {},
        "confidence": confidence,
    }


def _report(*claims: dict[str, object]):
    return SelfClaimConsistencyService().check_claim_consistency(
        SelfClaimConsistencyRequest(claim_payload={"claims": list(claims)})
    )


def _finding_types(report) -> set[str]:
    return {finding.finding_type for finding in report.findings}


def test_claim_consistency_report_builds_from_structured_payload() -> None:
    report = _report(
        _claim(
            "capability_claim",
            object_ref={
                "skill_id": "skill:deep_self_capability_registry_view",
                "claimed_status": "implemented",
            },
        )
    )

    assert report.status == "passed"
    assert report.checked_claim_count == 1
    assert report.supported_claim_count == 1
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.source_refs[0].raw_content_included is False


def test_contradiction_register_builds_with_open_entries() -> None:
    service = SelfClaimConsistencyService()
    report = service.check_claim_consistency(
        SelfClaimConsistencyRequest(
            claim_payload={
                "claims": [
                    _claim(
                        "canonical_truth_claim",
                        object_ref={"target_status": "candidate_only"},
                    )
                ]
            }
        )
    )
    register = service.last_register

    assert report.status == "failed"
    assert register is not None
    assert register.read_only is True
    assert register.mutation_performed is False
    assert register.open_count == 1
    assert register.entries[0].status == "open"


def test_capability_claim_supported_by_truth_passes() -> None:
    report = _report(
        _claim(
            "capability_claim",
            object_ref={
                "skill_id": "skill:deep_self_policy_gate_map",
                "claimed_status": "implemented",
            },
        )
    )

    assert report.status == "passed"
    assert report.supported_claim_count == 1


def test_capability_claim_exceeding_registry_truth_fails() -> None:
    report = _report(
        _claim(
            "capability_claim",
            object_ref={
                "skill_id": "skill:missing_capability",
                "claimed_status": "implemented",
            },
        )
    )

    assert report.status == "failed"
    assert "capability_claim_without_registry" in _finding_types(report)


def test_execution_claim_with_envelope_and_event_passes() -> None:
    report = _report(
        _claim(
            "execution_claim",
            object_ref={"envelope_id": "envelope:1", "ocel_event_id": "event:1"},
        )
    )

    assert report.status == "passed"
    assert report.supported_claim_count == 1


def test_execution_claim_without_envelope_or_event_fails() -> None:
    missing_envelope = _report(_claim("execution_claim", object_ref={"ocel_event_id": "event:1"}))
    missing_event = _report(_claim("execution_claim", object_ref={"envelope_id": "envelope:1"}))

    assert missing_envelope.status == "failed"
    assert "execution_claim_without_envelope" in _finding_types(missing_envelope)
    assert missing_event.status == "failed"
    assert "execution_claim_without_ocel_event" in _finding_types(missing_event)


def test_read_search_and_verification_claims_require_evidence() -> None:
    read_report = _report(_claim("read_claim"))
    search_report = _report(_claim("search_claim"))
    verification_report = _report(_claim("verification_claim"))

    assert read_report.status == "failed"
    assert "read_claim_without_text_read_event" in _finding_types(read_report)
    assert search_report.status == "failed"
    assert "search_claim_without_search_result" in _finding_types(search_report)
    assert verification_report.status == "failed"
    assert "verification_claim_without_report" in _finding_types(verification_report)


def test_boundary_contradiction_claims_fail() -> None:
    cases = [
        ("promotion_claim", "promotion_claim_contradicts_boundary"),
        ("memory_claim", "memory_claim_contradicts_boundary"),
        ("materialization_claim", "materialization_claim_contradicts_boundary"),
        ("external_contact_claim", "external_contact_claim_contradicts_runtime"),
    ]
    for claim_type, finding_type in cases:
        report = _report(_claim(claim_type))
        assert report.status == "failed"
        assert finding_type in _finding_types(report)


def test_canonical_policy_runtime_and_raw_transcript_contradictions_fail() -> None:
    canonical = _report(_claim("canonical_truth_claim", object_ref={"target_status": "candidate_only"}))
    policy = _report(_claim("policy_claim", object_ref={"permission_grant_creation_allowed": True}))
    runtime = _report(_claim("runtime_boundary_claim", object_ref={"network_enabled": True}))
    raw_transcript = _report(_claim("raw_transcript_claim"))

    assert canonical.status == "failed"
    assert "canonical_truth_claim_on_candidate" in _finding_types(canonical)
    assert policy.status == "failed"
    assert "policy_claim_contradicts_gate" in _finding_types(policy)
    assert runtime.status == "failed"
    assert "runtime_claim_contradicts_boundary" in _finding_types(runtime)
    assert raw_transcript.status == "failed"
    assert "raw_transcript_claim_without_process_state" in _finding_types(raw_transcript)


def test_unsupported_free_form_claim_is_not_judged_by_llm() -> None:
    low_risk = _report(_claim("unsupported_claim", confidence="low"))
    high_risk = _report(_claim("unsupported_claim", confidence="high"))

    assert low_risk.status == "warning"
    assert low_risk.unverifiable_claim_count == 1
    assert "claim_unverifiable" in _finding_types(low_risk)
    assert high_risk.status == "failed"
    assert high_risk.unsupported_claim_count == 1
    assert "claim_unsupported" in _finding_types(high_risk)


def test_private_payload_blocks_report() -> None:
    report = SelfClaimConsistencyService().check_claim_consistency(
        SelfClaimConsistencyRequest(claim_payload={"private_payload": True, "claims": []})
    )

    assert report.status == "blocked"
    assert report.source_refs[0].raw_content_included is False
    assert "source_blocked" in _finding_types(report)


def test_claim_consistency_skills_are_implemented_and_previous_skills_remain_implemented() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    records = {record.skill_id: record for record in snapshot.records if record.skill_id}

    for skill_id in [
        "skill:deep_self_capability_registry_view",
        "skill:deep_self_capability_truth_check",
        "skill:deep_self_runtime_boundary_view",
        "skill:deep_self_runtime_boundary_truth_check",
        "skill:deep_self_policy_gate_map",
        "skill:deep_self_policy_gate_truth_check",
        "skill:deep_self_trace_integrity_check",
        "skill:deep_self_envelope_ocel_consistency",
        "skill:deep_self_context_projection_view",
        "skill:deep_self_context_projection_gap_report",
        "skill:deep_self_candidate_memory_boundary_report",
        "skill:deep_self_promotion_boundary_check",
        "skill:deep_self_claim_consistency_check",
        "skill:deep_self_contradiction_register",
    ]:
        assert records[skill_id].status == "implemented"
        assert records[skill_id].read_only is True
        assert records[skill_id].execution_enabled is False
        assert records[skill_id].canonical_promotion_enabled is False


def test_pig_and_ocpx_projection_build() -> None:
    service = SelfClaimConsistencyService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.7"
    assert pig["subject"] == "self_claim_consistency"
    assert "LLM statement is not evidence" in pig["principles"]
    assert "claim without OCEL evidence is not truth" in pig["principles"]
    assert "contradiction register is not auto-correction" in pig["principles"]
    assert "claim consistency check is not claim rewriting" in pig["principles"]
    assert pig["checks_capability_claims"] is True
    assert pig["checks_execution_claims"] is True
    assert pig["checks_memory_promotion_claims"] is True
    assert pig["checks_canonical_truth_claims"] is True
    assert pig["rewrites_claims"] is False
    assert pig["mutates_memory"] is False
    assert pig["uses_llm_judge"] is False
    assert ocpx["state"] == "self_claim_consistency_awareness"
    assert "SelfClaimConsistencyState" in ocpx["target_read_models"]
    assert "SelfContradictionRegisterState" in ocpx["target_read_models"]
    assert "SelfClaimEvidenceState" in ocpx["target_read_models"]
    assert "SelfUnsupportedClaimState" in ocpx["target_read_models"]
    assert "SelfUnverifiableClaimState" in ocpx["target_read_models"]


def test_cli_claim_consistency_and_contradictions_work() -> None:
    commands = [
        ["deep-self", "claim", "consistency", "--payload", str(FIXTURES / "self_claims_valid.json")],
        ["deep-self", "claim", "consistency", "--payload", str(FIXTURES / "self_claims_contradicted.json")],
        ["deep-self", "claim", "consistency", "--source-report", "report:self"],
        ["deep-self", "claim", "consistency", "--source-candidate", "candidate:self"],
        ["deep-self", "claim", "consistency", "--scope", "projection"],
        ["deep-self", "claim", "contradictions"],
        ["deep-self", "claim", "contradictions", "--severity", "error"],
        ["deep-self", "claim", "evidence", "--claim-id", "claim:valid-capability", "--payload", str(FIXTURES / "self_claims_valid.json")],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        if "self_claims_contradicted" not in " ".join(command):
            assert result.returncode == 0
        assert "Self-Claim Consistency & Contradiction Register" in result.stdout
        assert "checked_claim_count=" in result.stdout
        assert "supported_claim_count=" in result.stdout
        assert "unsupported_claim_count=" in result.stdout
        assert "contradicted_claim_count=" in result.stdout
        assert "unverifiable_claim_count=" in result.stdout
        assert "contradiction_register_open_count=" in result.stdout
        assert "No claim rewrite performed." in result.stdout
        assert "No memory mutation performed." in result.stdout
        assert "raw_prompt_body_printed=False" in result.stdout
        assert "raw_transcript_printed=False" in result.stdout

import pytest

from chanta_core.verification.read_only_skills import (
    ReadOnlyVerificationSkillOutcome,
    ReadOnlyVerificationSkillSpec,
)
from chanta_core.verification.errors import VerificationError


def test_read_only_verification_skill_spec_to_dict_requires_read_only() -> None:
    spec = ReadOnlyVerificationSkillSpec(
        skill_name="verify_file_exists",
        description="Observe path existence.",
        contract_type="file_existence",
        target_type="file",
        evidence_kind_on_pass="file_exists",
        evidence_kind_on_fail="file_missing",
        read_only=True,
        skill_attrs={"x": 1},
    )

    data = spec.to_dict()
    assert data["skill_name"] == "verify_file_exists"
    assert data["read_only"] is True
    assert data["skill_attrs"] == {"x": 1}

    with pytest.raises(VerificationError):
        ReadOnlyVerificationSkillSpec(
            skill_name="bad",
            description="bad",
            contract_type="manual",
            target_type="other",
            evidence_kind_on_pass="observation",
            evidence_kind_on_fail="observation",
            read_only=False,
        )


def test_read_only_verification_skill_outcome_to_dict_and_statuses() -> None:
    outcome = ReadOnlyVerificationSkillOutcome(
        skill_name="verify_runtime_python_info",
        passed=True,
        status="passed",
        evidence_kind="runtime_status",
        evidence_content="python",
        reason="observed",
        confidence=1.0,
        outcome_attrs={"read_only": True},
    )

    assert outcome.to_dict()["status"] == "passed"
    assert outcome.to_dict()["passed"] is True

    with pytest.raises(VerificationError):
        ReadOnlyVerificationSkillOutcome(
            skill_name="bad",
            passed=None,
            status="unknown",
            evidence_kind="observation",
            evidence_content="bad",
            reason=None,
            confidence=None,
        )

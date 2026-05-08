import pytest

from chanta_core.external.ids import (
    new_external_adapter_review_checklist_id,
    new_external_adapter_review_decision_id,
    new_external_adapter_review_finding_id,
    new_external_adapter_review_item_id,
    new_external_adapter_review_queue_id,
)
from chanta_core.external.review import (
    ExternalAdapterReviewChecklist,
    ExternalAdapterReviewDecision,
    ExternalAdapterReviewFinding,
    ExternalAdapterReviewItem,
    ExternalAdapterReviewQueue,
)
from chanta_core.external.errors import ExternalAdapterReviewDecisionError
from chanta_core.utility.time import utc_now_iso


def test_external_adapter_review_models_to_dict() -> None:
    now = utc_now_iso()
    queue = ExternalAdapterReviewQueue(
        queue_id=new_external_adapter_review_queue_id(),
        queue_name="external review",
        queue_type="external_capability",
        status="active",
        created_at=now,
        updated_at=now,
        item_ids=["item-1"],
        queue_attrs={"scope": "test"},
    )
    item = ExternalAdapterReviewItem(
        item_id=new_external_adapter_review_item_id(),
        queue_id=queue.queue_id,
        candidate_id="external_assimilation_candidate:test",
        descriptor_id="external_capability_descriptor:test",
        source_id="external_capability_source:test",
        risk_note_ids=["external_capability_risk_note:test"],
        priority=80,
        review_status="pending_review",
        assigned_reviewer="reviewer",
        created_at=now,
        updated_at=now,
        item_attrs={"non_activating": True},
    )
    checklist = ExternalAdapterReviewChecklist(
        checklist_id=new_external_adapter_review_checklist_id(),
        item_id=item.item_id,
        checklist_type="safety",
        required_checks=["candidate_disabled"],
        completed_checks=["candidate_disabled"],
        failed_checks=[],
        status="completed",
        created_at=now,
        updated_at=now,
        checklist_attrs={},
    )
    finding = ExternalAdapterReviewFinding(
        finding_id=new_external_adapter_review_finding_id(),
        item_id=item.item_id,
        finding_type="risk",
        status="open",
        severity="high",
        message="Review risk.",
        source_kind="risk_note",
        source_ref="external_capability_risk_note:test",
        created_at=now,
        finding_attrs={},
    )
    decision = ExternalAdapterReviewDecision(
        decision_id=new_external_adapter_review_decision_id(),
        item_id=item.item_id,
        queue_id=queue.queue_id,
        candidate_id=item.candidate_id,
        decision="approved_for_design",
        decided_by="tester",
        decision_reason="Design only.",
        finding_ids=[finding.finding_id],
        checklist_id=checklist.checklist_id,
        activation_allowed=False,
        runtime_registration_allowed=False,
        execution_enabled_after_decision=False,
        created_at=now,
        decision_attrs={},
    )

    assert queue.to_dict()["queue_id"].startswith("external_adapter_review_queue:")
    assert item.to_dict()["item_id"].startswith("external_adapter_review_item:")
    assert checklist.to_dict()["checklist_id"].startswith("external_adapter_review_checklist:")
    assert finding.to_dict()["finding_id"].startswith("external_adapter_review_finding:")
    assert decision.to_dict()["decision_id"].startswith("external_adapter_review_decision:")
    assert decision.activation_allowed is False
    assert decision.runtime_registration_allowed is False
    assert decision.execution_enabled_after_decision is False


def test_review_decision_rejects_activating_flags() -> None:
    now = utc_now_iso()
    with pytest.raises(ExternalAdapterReviewDecisionError):
        ExternalAdapterReviewDecision(
            decision_id=new_external_adapter_review_decision_id(),
            item_id="external_adapter_review_item:test",
            queue_id="external_adapter_review_queue:test",
            candidate_id="external_assimilation_candidate:test",
            decision="approved_for_design",
            decided_by=None,
            decision_reason=None,
            finding_ids=[],
            checklist_id=None,
            activation_allowed=True,
            runtime_registration_allowed=False,
            execution_enabled_after_decision=False,
            created_at=now,
            decision_attrs={},
        )

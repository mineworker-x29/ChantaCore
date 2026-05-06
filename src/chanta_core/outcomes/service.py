from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.outcomes.ids import (
    new_process_outcome_contract_id,
    new_process_outcome_criterion_id,
    new_process_outcome_evaluation_id,
    new_process_outcome_signal_id,
    new_process_outcome_target_id,
)
from chanta_core.outcomes.models import (
    ProcessOutcomeContract,
    ProcessOutcomeCriterion,
    ProcessOutcomeEvaluation,
    ProcessOutcomeSignal,
    ProcessOutcomeTarget,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.verification.models import VerificationResult


class ProcessOutcomeEvaluationService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()

    def register_contract(
        self,
        *,
        contract_name: str,
        contract_type: str,
        description: str | None = None,
        status: str = "active",
        target_type: str | None = None,
        required_verification_contract_ids: list[str] | None = None,
        min_required_pass_rate: float | None = None,
        min_evidence_coverage: float | None = None,
        severity: str | None = None,
        contract_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeContract:
        now = utc_now_iso()
        contract = ProcessOutcomeContract(
            contract_id=new_process_outcome_contract_id(),
            contract_name=contract_name,
            contract_type=contract_type,
            description=description,
            status=status,
            target_type=target_type,
            required_verification_contract_ids=list(required_verification_contract_ids or []),
            min_required_pass_rate=min_required_pass_rate,
            min_evidence_coverage=min_evidence_coverage,
            severity=severity,
            created_at=now,
            updated_at=now,
            contract_attrs=dict(contract_attrs or {}),
        )
        self._record_outcome_event(
            "process_outcome_contract_registered",
            contract=contract,
            event_attrs={},
            event_relations=[("contract_object", contract.contract_id)],
            object_relations=[],
        )
        return contract

    def update_contract(
        self,
        *,
        contract: ProcessOutcomeContract,
        description: str | None = None,
        status: str | None = None,
        severity: str | None = None,
        min_required_pass_rate: float | None = None,
        min_evidence_coverage: float | None = None,
        contract_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeContract:
        updated = replace(
            contract,
            description=contract.description if description is None else description,
            status=contract.status if status is None else status,
            severity=contract.severity if severity is None else severity,
            min_required_pass_rate=(
                contract.min_required_pass_rate
                if min_required_pass_rate is None
                else min_required_pass_rate
            ),
            min_evidence_coverage=(
                contract.min_evidence_coverage
                if min_evidence_coverage is None
                else min_evidence_coverage
            ),
            updated_at=utc_now_iso(),
            contract_attrs={**contract.contract_attrs, **dict(contract_attrs or {})},
        )
        self._record_outcome_event(
            "process_outcome_contract_updated",
            contract=updated,
            event_attrs={},
            event_relations=[("contract_object", updated.contract_id)],
            object_relations=[],
        )
        return updated

    def deprecate_contract(
        self,
        *,
        contract: ProcessOutcomeContract,
        reason: str | None = None,
    ) -> ProcessOutcomeContract:
        deprecated = replace(contract, status="deprecated", updated_at=utc_now_iso())
        self._record_outcome_event(
            "process_outcome_contract_deprecated",
            contract=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("contract_object", deprecated.contract_id)],
            object_relations=[],
        )
        return deprecated

    def register_criterion(
        self,
        *,
        contract_id: str,
        criterion_type: str,
        description: str,
        required: bool = True,
        weight: float | None = None,
        expected_statuses: list[str] | None = None,
        status: str = "active",
        criterion_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeCriterion:
        criterion = ProcessOutcomeCriterion(
            criterion_id=new_process_outcome_criterion_id(),
            contract_id=contract_id,
            criterion_type=criterion_type,
            description=description,
            required=required,
            weight=weight,
            expected_statuses=list(expected_statuses or ["passed"]),
            status=status,
            criterion_attrs=dict(criterion_attrs or {}),
        )
        self._record_outcome_event(
            "process_outcome_criterion_registered",
            criterion=criterion,
            event_attrs={},
            event_relations=[
                ("criterion_object", criterion.criterion_id),
                ("contract_object", contract_id),
            ],
            object_relations=[(criterion.criterion_id, contract_id, "belongs_to_contract")],
        )
        return criterion

    def register_target(
        self,
        *,
        target_type: str,
        target_ref: str,
        target_label: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
        process_instance_id: str | None = None,
        status: str = "active",
        target_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeTarget:
        target = ProcessOutcomeTarget(
            target_id=new_process_outcome_target_id(),
            target_type=target_type,
            target_ref=target_ref,
            target_label=target_label,
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
            process_instance_id=process_instance_id,
            status=status,
            created_at=utc_now_iso(),
            target_attrs=dict(target_attrs or {}),
        )
        event_relations = [("target_object", target.target_id)]
        object_relations: list[tuple[str, str, str]] = []
        if session_id:
            session_object_id = self._session_object_id(session_id)
            event_relations.append(("session_context", session_object_id))
            object_relations.append((target.target_id, session_object_id, "refers_to_session"))
        if turn_id:
            event_relations.append(("turn_context", turn_id))
            object_relations.append((target.target_id, turn_id, "refers_to_turn"))
        if message_id:
            event_relations.append(("message_context", message_id))
            object_relations.append((target.target_id, message_id, "refers_to_message"))
        if process_instance_id:
            event_relations.append(("process_context", process_instance_id))
            object_relations.append((target.target_id, process_instance_id, "refers_to_process_instance"))
        self._record_outcome_event(
            "process_outcome_target_registered",
            target=target,
            event_attrs={},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return target

    def record_signal(
        self,
        *,
        signal_type: str,
        signal_value: str,
        target_id: str | None = None,
        strength: float | None = None,
        source_kind: str | None = None,
        source_ref: str | None = None,
        signal_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeSignal:
        signal = ProcessOutcomeSignal(
            signal_id=new_process_outcome_signal_id(),
            target_id=target_id,
            signal_type=signal_type,
            signal_value=signal_value,
            strength=strength,
            source_kind=source_kind,
            source_ref=source_ref,
            created_at=utc_now_iso(),
            signal_attrs=dict(signal_attrs or {}),
        )
        event_relations = [("signal_object", signal.signal_id)]
        object_relations: list[tuple[str, str, str]] = []
        if target_id:
            event_relations.append(("target_object", target_id))
        if source_kind == "verification_result" and source_ref:
            event_relations.append(("verification_result_object", source_ref))
            object_relations.append((signal.signal_id, source_ref, "derived_from_verification_result"))
        if source_kind == "verification_evidence" and source_ref:
            event_relations.append(("verification_evidence_object", source_ref))
        self._record_outcome_event(
            "process_outcome_signal_recorded",
            signal=signal,
            event_attrs={"signal_type": signal_type, "source_kind": source_kind},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return signal

    def evaluate_from_verification_results(
        self,
        *,
        contract: ProcessOutcomeContract,
        target: ProcessOutcomeTarget,
        verification_results: list[VerificationResult],
        criteria: list[ProcessOutcomeCriterion] | None = None,
        reason: str | None = None,
        evaluation_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeEvaluation:
        self._record_outcome_event(
            "process_outcome_evaluation_started",
            contract=contract,
            target=target,
            event_attrs={"target_id": target.target_id},
            event_relations=[
                ("contract_object", contract.contract_id),
                ("target_object", target.target_id),
            ],
            object_relations=[
                (target.target_id, contract.contract_id, "evaluated_under_contract"),
            ],
        )

        stats = self._verification_stats(contract, verification_results)
        signals = [
            self.record_signal(
                target_id=target.target_id,
                signal_type=self._signal_type_for_status(result.status),
                signal_value=result.status,
                strength=result.confidence,
                source_kind="verification_result",
                source_ref=result.result_id,
                signal_attrs={
                    "contract_id": result.contract_id,
                    "verification_target_id": result.target_id,
                    "evidence_ids": list(result.evidence_ids),
                },
            )
            for result in verification_results
        ]
        passed_criteria_ids, failed_criteria_ids = self._evaluate_criteria(
            contract=contract,
            verification_results=verification_results,
            criteria=list(criteria or []),
            pass_rate=stats["pass_rate"],
            evidence_coverage=stats["evidence_coverage"],
        )
        outcome_status = self._outcome_status(
            contract=contract,
            verification_results=verification_results,
            pass_rate=stats["pass_rate"],
            evidence_coverage=stats["evidence_coverage"],
            failed_required_criterion=bool(failed_criteria_ids),
        )
        default_reason = self._evaluation_reason(outcome_status, stats)
        evaluation = self.record_evaluation(
            contract_id=contract.contract_id,
            target_id=target.target_id,
            outcome_status=outcome_status,
            score=stats["score"],
            confidence=stats["confidence"],
            evidence_coverage=stats["evidence_coverage"],
            passed_criteria_ids=passed_criteria_ids,
            failed_criteria_ids=failed_criteria_ids,
            signal_ids=[signal.signal_id for signal in signals],
            verification_result_ids=[result.result_id for result in verification_results],
            reason=reason or default_reason,
            evaluation_attrs={
                **dict(evaluation_attrs or {}),
                **stats,
                "evaluation_policy": "deterministic_verification_result_summary",
                "threshold_defaults": {
                    "min_required_pass_rate": 1.0,
                    "min_evidence_coverage": 1.0,
                },
                "verification_evidence_ids": self._evidence_ids(verification_results),
                "runtime_behavior_mutated": False,
                "tools_blocked_or_modified": False,
            },
        )
        for signal in signals:
            self._record_outcome_event(
                "process_outcome_signal_attached_to_evaluation",
                signal=signal,
                evaluation=evaluation,
                event_attrs={},
                event_relations=[
                    ("signal_object", signal.signal_id),
                    ("evaluation_object", evaluation.evaluation_id),
                ],
                object_relations=[(signal.signal_id, evaluation.evaluation_id, "supports_evaluation")],
            )
        return evaluation

    def record_evaluation(
        self,
        *,
        contract_id: str,
        target_id: str,
        outcome_status: str,
        score: float | None = None,
        confidence: float | None = None,
        evidence_coverage: float | None = None,
        passed_criteria_ids: list[str] | None = None,
        failed_criteria_ids: list[str] | None = None,
        signal_ids: list[str] | None = None,
        verification_result_ids: list[str] | None = None,
        reason: str | None = None,
        evaluation_attrs: dict[str, Any] | None = None,
    ) -> ProcessOutcomeEvaluation:
        evaluation = ProcessOutcomeEvaluation(
            evaluation_id=new_process_outcome_evaluation_id(),
            contract_id=contract_id,
            target_id=target_id,
            outcome_status=outcome_status,
            score=score,
            confidence=confidence,
            evidence_coverage=evidence_coverage,
            passed_criteria_ids=list(passed_criteria_ids or []),
            failed_criteria_ids=list(failed_criteria_ids or []),
            signal_ids=list(signal_ids or []),
            verification_result_ids=list(verification_result_ids or []),
            reason=reason,
            created_at=utc_now_iso(),
            evaluation_attrs=dict(evaluation_attrs or {}),
        )
        event_relations = [
            ("evaluation_object", evaluation.evaluation_id),
            ("contract_object", contract_id),
            ("target_object", target_id),
            *[("signal_object", signal_id) for signal_id in evaluation.signal_ids],
            *[("verification_result_object", result_id) for result_id in evaluation.verification_result_ids],
        ]
        object_relations = [
            (evaluation.evaluation_id, contract_id, "uses_contract"),
            (evaluation.evaluation_id, target_id, "evaluates_target"),
            *[
                (evaluation.evaluation_id, result_id, "based_on_verification_result")
                for result_id in evaluation.verification_result_ids
            ],
        ]
        for evidence_id in evaluation.evaluation_attrs.get("verification_evidence_ids", []):
            object_relations.append((evaluation.evaluation_id, str(evidence_id), "based_on_verification_evidence"))
        self._record_outcome_event(
            "process_outcome_evaluation_recorded",
            evaluation=evaluation,
            event_attrs={"outcome_status": outcome_status, "reason": reason},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        if outcome_status == "error":
            self._record_outcome_event(
                "process_outcome_evaluation_failed",
                evaluation=evaluation,
                event_attrs={"reason": reason},
                event_relations=[("evaluation_object", evaluation.evaluation_id)],
                object_relations=[],
            )
        if outcome_status == "skipped":
            self._record_outcome_event(
                "process_outcome_evaluation_skipped",
                evaluation=evaluation,
                event_attrs={"reason": reason},
                event_relations=[("evaluation_object", evaluation.evaluation_id)],
                object_relations=[],
            )
        return evaluation

    def attach_evaluation_to_process(
        self,
        *,
        evaluation_id: str,
        process_instance_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        self._record_outcome_event(
            "process_outcome_attached_to_process",
            event_attrs={"reason": reason},
            event_relations=[
                ("evaluation_object", evaluation_id),
                ("process_context", process_instance_id),
            ],
            object_relations=[(evaluation_id, process_instance_id, "attached_to_process_instance")],
        )
        return {
            "evaluation_id": evaluation_id,
            "process_instance_id": process_instance_id,
            "reason": reason,
            "process_status_changed": False,
            "runtime_behavior_mutated": False,
        }

    @staticmethod
    def _verification_stats(
        contract: ProcessOutcomeContract,
        verification_results: list[VerificationResult],
    ) -> dict[str, Any]:
        total = len(verification_results)
        passed = sum(1 for result in verification_results if result.status == "passed")
        failed = sum(1 for result in verification_results if result.status == "failed")
        inconclusive = sum(1 for result in verification_results if result.status == "inconclusive")
        skipped = sum(1 for result in verification_results if result.status == "skipped")
        error = sum(1 for result in verification_results if result.status == "error")
        with_evidence = sum(1 for result in verification_results if result.evidence_ids)
        required_contract_ids = list(contract.required_verification_contract_ids)
        if required_contract_ids:
            covered_required = {
                result.contract_id for result in verification_results if result.contract_id in required_contract_ids
            }
            passed_required = {
                result.contract_id
                for result in verification_results
                if result.contract_id in required_contract_ids and result.status == "passed"
            }
            required_coverage = len(covered_required) / len(required_contract_ids)
            required_pass_rate = len(passed_required) / len(required_contract_ids)
        else:
            required_coverage = None
            required_pass_rate = None
        pass_rate = passed / total if total else 0.0
        evidence_coverage = with_evidence / total if total else 0.0
        score = round(pass_rate * evidence_coverage, 6) if total else 0.0
        confidences = [
            float(result.confidence)
            for result in verification_results
            if result.confidence is not None
        ]
        confidence = sum(confidences) / len(confidences) if confidences else evidence_coverage
        return {
            "total_verification_count": total,
            "passed_count": passed,
            "failed_count": failed,
            "inconclusive_count": inconclusive,
            "skipped_count": skipped,
            "error_count": error,
            "pass_rate": round(pass_rate, 6),
            "evidence_coverage": round(evidence_coverage, 6),
            "score": round(score, 6),
            "confidence": round(confidence, 6),
            "required_contract_coverage": None if required_coverage is None else round(required_coverage, 6),
            "required_contract_pass_rate": None if required_pass_rate is None else round(required_pass_rate, 6),
        }

    @staticmethod
    def _evaluate_criteria(
        *,
        contract: ProcessOutcomeContract,
        verification_results: list[VerificationResult],
        criteria: list[ProcessOutcomeCriterion],
        pass_rate: float,
        evidence_coverage: float,
    ) -> tuple[list[str], list[str]]:
        passed_ids: list[str] = []
        failed_ids: list[str] = []
        statuses = [result.status for result in verification_results]
        required_contract_ids = list(contract.required_verification_contract_ids)
        for criterion in criteria:
            criterion_passed = True
            if criterion.criterion_type == "verification_passed":
                expected = set(criterion.expected_statuses or ["passed"])
                criterion_passed = bool(statuses) and all(status in expected for status in statuses)
            elif criterion.criterion_type == "verification_failed_absent":
                criterion_passed = "failed" not in statuses and "error" not in statuses
            elif criterion.criterion_type in {"evidence_coverage_minimum", "required_evidence_present"}:
                threshold = contract.min_evidence_coverage
                if threshold is None:
                    threshold = 1.0
                criterion_passed = evidence_coverage >= threshold
            elif criterion.criterion_type in {"trace_exists", "message_exists"}:
                criterion_passed = bool(criterion.criterion_attrs.get("observed"))
            elif criterion.criterion_type == "manual_review_required":
                criterion_passed = False
            if required_contract_ids and criterion.criterion_type == "verification_passed":
                passed_required = {
                    result.contract_id
                    for result in verification_results
                    if result.contract_id in required_contract_ids and result.status == "passed"
                }
                criterion_passed = criterion_passed and set(required_contract_ids).issubset(passed_required)
            if criterion_passed:
                passed_ids.append(criterion.criterion_id)
            elif criterion.required:
                failed_ids.append(criterion.criterion_id)
        if not criteria:
            min_pass_rate = contract.min_required_pass_rate if contract.min_required_pass_rate is not None else 1.0
            min_coverage = contract.min_evidence_coverage if contract.min_evidence_coverage is not None else 1.0
            if pass_rate >= min_pass_rate and evidence_coverage >= min_coverage and verification_results:
                passed_ids.append(f"{contract.contract_id}:thresholds")
        return passed_ids, failed_ids

    @staticmethod
    def _outcome_status(
        *,
        contract: ProcessOutcomeContract,
        verification_results: list[VerificationResult],
        pass_rate: float,
        evidence_coverage: float,
        failed_required_criterion: bool,
    ) -> str:
        if not verification_results:
            return "inconclusive"
        if all(result.status == "skipped" for result in verification_results):
            return "skipped"
        passed_count = sum(1 for result in verification_results if result.status == "passed")
        failed_count = sum(1 for result in verification_results if result.status == "failed")
        error_count = sum(1 for result in verification_results if result.status == "error")
        if error_count and not passed_count:
            return "error"
        if failed_required_criterion or failed_count:
            return "failed"
        min_pass_rate = contract.min_required_pass_rate if contract.min_required_pass_rate is not None else 1.0
        min_coverage = contract.min_evidence_coverage if contract.min_evidence_coverage is not None else 1.0
        if pass_rate >= min_pass_rate and evidence_coverage >= min_coverage:
            return "success"
        if passed_count > 0:
            return "partial_success"
        return "inconclusive"

    @staticmethod
    def _signal_type_for_status(status: str) -> str:
        return {
            "passed": "verification_passed",
            "failed": "verification_failed",
            "inconclusive": "verification_inconclusive",
            "skipped": "needs_review",
            "error": "error_signal",
        }.get(status, "other")

    @staticmethod
    def _evaluation_reason(outcome_status: str, stats: dict[str, Any]) -> str:
        return (
            f"Outcome {outcome_status}: pass_rate={stats['pass_rate']}, "
            f"evidence_coverage={stats['evidence_coverage']}, "
            f"total={stats['total_verification_count']}"
        )

    @staticmethod
    def _evidence_ids(verification_results: list[VerificationResult]) -> list[str]:
        evidence_ids: list[str] = []
        for result in verification_results:
            evidence_ids.extend(result.evidence_ids)
        return evidence_ids

    def _record_outcome_event(
        self,
        event_activity: str,
        *,
        contract: ProcessOutcomeContract | None = None,
        criterion: ProcessOutcomeCriterion | None = None,
        target: ProcessOutcomeTarget | None = None,
        signal: ProcessOutcomeSignal | None = None,
        evaluation: ProcessOutcomeEvaluation | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "enforcement_enabled": False,
                "process_outcome_evaluation_only": True,
            },
        )
        objects = self._objects_for_event(
            contract=contract,
            criterion=criterion,
            target=target,
            signal=signal,
            evaluation=evaluation,
            event_relations=event_relations,
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source, target_object_id=target_id, qualifier=qualifier)
            for source, target_id, qualifier in object_relations
            if source and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )

    def _objects_for_event(
        self,
        *,
        contract: ProcessOutcomeContract | None,
        criterion: ProcessOutcomeCriterion | None,
        target: ProcessOutcomeTarget | None,
        signal: ProcessOutcomeSignal | None,
        evaluation: ProcessOutcomeEvaluation | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if contract is not None:
            objects.append(self._contract_object(contract))
        if criterion is not None:
            objects.append(self._criterion_object(criterion))
        if target is not None:
            objects.append(self._target_object(target))
        if signal is not None:
            objects.append(self._signal_object(signal))
        if evaluation is not None:
            objects.append(self._evaluation_object(evaluation))

        known_ids = {item.object_id for item in objects}
        for qualifier, object_id in event_relations:
            if not object_id or object_id in known_ids:
                continue
            placeholder = self._placeholder_object(qualifier, object_id)
            if placeholder is not None:
                objects.append(placeholder)
                known_ids.add(object_id)
        return objects

    @staticmethod
    def _contract_object(contract: ProcessOutcomeContract) -> OCELObject:
        return OCELObject(
            object_id=contract.contract_id,
            object_type="process_outcome_contract",
            object_attrs={**contract.to_dict(), "object_key": contract.contract_id, "display_name": contract.contract_name},
        )

    @staticmethod
    def _criterion_object(criterion: ProcessOutcomeCriterion) -> OCELObject:
        return OCELObject(
            object_id=criterion.criterion_id,
            object_type="process_outcome_criterion",
            object_attrs={**criterion.to_dict(), "object_key": criterion.criterion_id, "display_name": criterion.criterion_type},
        )

    @staticmethod
    def _target_object(target: ProcessOutcomeTarget) -> OCELObject:
        return OCELObject(
            object_id=target.target_id,
            object_type="process_outcome_target",
            object_attrs={**target.to_dict(), "object_key": target.target_id, "display_name": target.target_label or target.target_ref},
        )

    @staticmethod
    def _signal_object(signal: ProcessOutcomeSignal) -> OCELObject:
        return OCELObject(
            object_id=signal.signal_id,
            object_type="process_outcome_signal",
            object_attrs={**signal.to_dict(), "object_key": signal.signal_id, "display_name": signal.signal_type},
        )

    @staticmethod
    def _evaluation_object(evaluation: ProcessOutcomeEvaluation) -> OCELObject:
        return OCELObject(
            object_id=evaluation.evaluation_id,
            object_type="process_outcome_evaluation",
            object_attrs={**evaluation.to_dict(), "object_key": evaluation.evaluation_id, "display_name": evaluation.outcome_status},
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "verification_result_object": "verification_result",
            "verification_evidence_object": "verification_evidence",
            "session_context": "session",
            "turn_context": "conversation_turn",
            "message_context": "message",
            "process_context": "process_instance",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(
            object_id=object_id,
            object_type=object_type,
            object_attrs={"object_key": object_id, "display_name": object_id},
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.verification.ids import (
    new_verification_contract_id,
    new_verification_evidence_id,
    new_verification_requirement_id,
    new_verification_result_id,
    new_verification_run_id,
    new_verification_target_id,
)
from chanta_core.verification.models import (
    VerificationContract,
    VerificationEvidence,
    VerificationRequirement,
    VerificationResult,
    VerificationRun,
    VerificationTarget,
    hash_content,
    preview_text,
)


class VerificationService:
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
        subject_type: str | None = None,
        required_evidence_kinds: list[str] | None = None,
        pass_criteria: dict[str, Any] | None = None,
        fail_criteria: dict[str, Any] | None = None,
        severity: str | None = None,
        contract_attrs: dict[str, Any] | None = None,
    ) -> VerificationContract:
        now = utc_now_iso()
        contract = VerificationContract(
            contract_id=new_verification_contract_id(),
            contract_name=contract_name,
            contract_type=contract_type,
            description=description,
            status=status,
            subject_type=subject_type,
            required_evidence_kinds=list(required_evidence_kinds or []),
            pass_criteria=dict(pass_criteria or {}),
            fail_criteria=dict(fail_criteria or {}),
            severity=severity,
            created_at=now,
            updated_at=now,
            contract_attrs=dict(contract_attrs or {}),
        )
        self._record_verification_event(
            "verification_contract_registered",
            contract=contract,
            event_attrs={},
            event_relations=[("contract_object", contract.contract_id)],
            object_relations=[],
        )
        return contract

    def update_contract(
        self,
        *,
        contract: VerificationContract,
        description: str | None = None,
        status: str | None = None,
        severity: str | None = None,
        contract_attrs: dict[str, Any] | None = None,
    ) -> VerificationContract:
        updated = replace(
            contract,
            description=contract.description if description is None else description,
            status=contract.status if status is None else status,
            severity=contract.severity if severity is None else severity,
            updated_at=utc_now_iso(),
            contract_attrs={**contract.contract_attrs, **dict(contract_attrs or {})},
        )
        self._record_verification_event(
            "verification_contract_updated",
            contract=updated,
            event_attrs={},
            event_relations=[("contract_object", updated.contract_id)],
            object_relations=[],
        )
        return updated

    def deprecate_contract(
        self,
        *,
        contract: VerificationContract,
        reason: str | None = None,
    ) -> VerificationContract:
        deprecated = replace(contract, status="deprecated", updated_at=utc_now_iso())
        self._record_verification_event(
            "verification_contract_deprecated",
            contract=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("contract_object", deprecated.contract_id)],
            object_relations=[],
        )
        return deprecated

    def register_target(
        self,
        *,
        target_type: str,
        target_ref: str,
        target_label: str | None = None,
        status: str = "active",
        target_attrs: dict[str, Any] | None = None,
    ) -> VerificationTarget:
        target = VerificationTarget(
            target_id=new_verification_target_id(),
            target_type=target_type,
            target_ref=target_ref,
            target_label=target_label,
            status=status,
            created_at=utc_now_iso(),
            target_attrs=dict(target_attrs or {}),
        )
        self._record_verification_event(
            "verification_target_registered",
            target=target,
            event_attrs={},
            event_relations=[("target_object", target.target_id)],
            object_relations=[],
        )
        return target

    def register_requirement(
        self,
        *,
        contract_id: str,
        requirement_type: str,
        description: str,
        required: bool = True,
        evidence_kind: str | None = None,
        priority: int | None = None,
        status: str = "active",
        requirement_attrs: dict[str, Any] | None = None,
    ) -> VerificationRequirement:
        requirement = VerificationRequirement(
            requirement_id=new_verification_requirement_id(),
            contract_id=contract_id,
            requirement_type=requirement_type,
            description=description,
            required=required,
            evidence_kind=evidence_kind,
            priority=priority,
            status=status,
            requirement_attrs=dict(requirement_attrs or {}),
        )
        self._record_verification_event(
            "verification_requirement_registered",
            requirement=requirement,
            event_attrs={},
            event_relations=[
                ("requirement_object", requirement.requirement_id),
                ("contract_object", contract_id),
            ],
            object_relations=[(requirement.requirement_id, contract_id, "belongs_to_contract")],
        )
        return requirement

    def start_run(
        self,
        *,
        contract_id: str,
        target_ids: list[str],
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        status: str = "running",
        run_attrs: dict[str, Any] | None = None,
    ) -> VerificationRun:
        run = VerificationRun(
            run_id=new_verification_run_id(),
            contract_id=contract_id,
            target_ids=list(target_ids),
            status=status,
            started_at=utc_now_iso(),
            completed_at=None,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            run_attrs=dict(run_attrs or {}),
        )
        self._record_run_event("verification_run_started", run, event_attrs={})
        return run

    def complete_run(
        self,
        *,
        run: VerificationRun,
        run_attrs: dict[str, Any] | None = None,
    ) -> VerificationRun:
        completed = replace(
            run,
            status="completed",
            completed_at=utc_now_iso(),
            run_attrs={**run.run_attrs, **dict(run_attrs or {})},
        )
        self._record_run_event("verification_run_completed", completed, event_attrs={})
        return completed

    def fail_run(
        self,
        *,
        run: VerificationRun,
        error_message: str,
        run_attrs: dict[str, Any] | None = None,
    ) -> VerificationRun:
        failed = replace(
            run,
            status="failed",
            completed_at=utc_now_iso(),
            run_attrs={**run.run_attrs, **dict(run_attrs or {}), "error_message": error_message},
        )
        self._record_run_event("verification_run_failed", failed, event_attrs={"error_message": error_message})
        return failed

    def skip_run(
        self,
        *,
        run: VerificationRun,
        reason: str | None = None,
        run_attrs: dict[str, Any] | None = None,
    ) -> VerificationRun:
        skipped = replace(
            run,
            status="skipped",
            completed_at=utc_now_iso(),
            run_attrs={**run.run_attrs, **dict(run_attrs or {}), "skip_reason": reason},
        )
        self._record_run_event("verification_run_skipped", skipped, event_attrs={"reason": reason})
        return skipped

    def record_evidence(
        self,
        *,
        evidence_kind: str,
        content: str,
        run_id: str | None = None,
        target_id: str | None = None,
        source_kind: str | None = None,
        confidence: float | None = None,
        evidence_attrs: dict[str, Any] | None = None,
    ) -> VerificationEvidence:
        evidence = VerificationEvidence(
            evidence_id=new_verification_evidence_id(),
            run_id=run_id,
            target_id=target_id,
            evidence_kind=evidence_kind,
            source_kind=source_kind,
            content=content,
            content_preview=preview_text(content),
            content_hash=hash_content(content),
            confidence=confidence,
            collected_at=utc_now_iso(),
            evidence_attrs=dict(evidence_attrs or {}),
        )
        event_relations = [("evidence_object", evidence.evidence_id)]
        object_relations: list[tuple[str, str, str]] = []
        if run_id:
            event_relations.append(("run_object", run_id))
            object_relations.append((evidence.evidence_id, run_id, "evidence_for_run"))
        if target_id:
            event_relations.append(("target_object", target_id))
            object_relations.append((evidence.evidence_id, target_id, "evidence_for_target"))
        self._record_verification_event(
            "verification_evidence_recorded",
            evidence=evidence,
            event_attrs={"evidence_kind": evidence_kind, "source_kind": source_kind},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return evidence

    def record_result(
        self,
        *,
        contract_id: str,
        status: str,
        run_id: str | None = None,
        target_id: str | None = None,
        confidence: float | None = None,
        reason: str | None = None,
        evidence_ids: list[str] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> VerificationResult:
        result = VerificationResult(
            result_id=new_verification_result_id(),
            run_id=run_id,
            contract_id=contract_id,
            target_id=target_id,
            status=status,
            confidence=confidence,
            reason=reason,
            evidence_ids=list(evidence_ids or []),
            created_at=utc_now_iso(),
            result_attrs=dict(result_attrs or {}),
        )
        event_relations = [
            ("result_object", result.result_id),
            ("contract_object", contract_id),
        ]
        object_relations = [(result.result_id, contract_id, "uses_contract")]
        if run_id:
            event_relations.append(("run_object", run_id))
            object_relations.append((result.result_id, run_id, "result_of_run"))
        if target_id:
            event_relations.append(("target_object", target_id))
            object_relations.append((result.result_id, target_id, "evaluates_target"))
        for evidence_id in result.evidence_ids:
            event_relations.append(("evidence_object", evidence_id))
            object_relations.append((result.result_id, evidence_id, "based_on_evidence"))
        self._record_verification_event(
            "verification_result_recorded",
            result=result,
            event_attrs={"status": status, "reason": reason},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return result

    def attach_result_to_process(
        self,
        *,
        result_id: str,
        process_instance_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        self._record_verification_event(
            "verification_result_attached_to_process",
            event_attrs={"reason": reason},
            event_relations=[
                ("result_object", result_id),
                ("process_context", process_instance_id),
            ],
            object_relations=[(result_id, process_instance_id, "attached_to_process_instance")],
        )
        return {
            "result_id": result_id,
            "process_instance_id": process_instance_id,
            "reason": reason,
            "evaluation_performed": False,
        }

    def _record_run_event(
        self,
        event_activity: str,
        run: VerificationRun,
        *,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations = [
            ("run_object", run.run_id),
            ("contract_object", run.contract_id),
            *[("target_object", target_id) for target_id in run.target_ids],
        ]
        object_relations = [
            (run.run_id, run.contract_id, "uses_contract"),
            *[(run.run_id, target_id, "targets") for target_id in run.target_ids],
        ]
        if run.session_id:
            event_relations.append(("session_context", self._session_object_id(run.session_id)))
            object_relations.append((run.run_id, self._session_object_id(run.session_id), "belongs_to_session"))
        if run.turn_id:
            event_relations.append(("turn_context", run.turn_id))
            object_relations.append((run.run_id, run.turn_id, "belongs_to_turn"))
        if run.process_instance_id:
            event_relations.append(("process_context", run.process_instance_id))
            object_relations.append((run.run_id, run.process_instance_id, "observes_process_instance"))
        self._record_verification_event(
            event_activity,
            run=run,
            event_attrs=event_attrs,
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_verification_event(
        self,
        event_activity: str,
        *,
        contract: VerificationContract | None = None,
        target: VerificationTarget | None = None,
        requirement: VerificationRequirement | None = None,
        run: VerificationRun | None = None,
        evidence: VerificationEvidence | None = None,
        result: VerificationResult | None = None,
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
                "verification_foundation_only": True,
            },
        )
        objects = self._objects_for_event(
            contract=contract,
            target=target,
            requirement=requirement,
            run=run,
            evidence=evidence,
            result=result,
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
        contract: VerificationContract | None,
        target: VerificationTarget | None,
        requirement: VerificationRequirement | None,
        run: VerificationRun | None,
        evidence: VerificationEvidence | None,
        result: VerificationResult | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if contract is not None:
            objects.append(self._contract_object(contract))
        if target is not None:
            objects.append(self._target_object(target))
        if requirement is not None:
            objects.append(self._requirement_object(requirement))
        if run is not None:
            objects.append(self._run_object(run))
        if evidence is not None:
            objects.append(self._evidence_object(evidence))
        if result is not None:
            objects.append(self._result_object(result))

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
    def _contract_object(contract: VerificationContract) -> OCELObject:
        return OCELObject(
            object_id=contract.contract_id,
            object_type="verification_contract",
            object_attrs={**contract.to_dict(), "object_key": contract.contract_id, "display_name": contract.contract_name},
        )

    @staticmethod
    def _target_object(target: VerificationTarget) -> OCELObject:
        return OCELObject(
            object_id=target.target_id,
            object_type="verification_target",
            object_attrs={**target.to_dict(), "object_key": target.target_id, "display_name": target.target_label or target.target_ref},
        )

    @staticmethod
    def _requirement_object(requirement: VerificationRequirement) -> OCELObject:
        return OCELObject(
            object_id=requirement.requirement_id,
            object_type="verification_requirement",
            object_attrs={**requirement.to_dict(), "object_key": requirement.requirement_id, "display_name": requirement.requirement_type},
        )

    @staticmethod
    def _run_object(run: VerificationRun) -> OCELObject:
        return OCELObject(
            object_id=run.run_id,
            object_type="verification_run",
            object_attrs={**run.to_dict(), "object_key": run.run_id, "display_name": run.status},
        )

    @staticmethod
    def _evidence_object(evidence: VerificationEvidence) -> OCELObject:
        return OCELObject(
            object_id=evidence.evidence_id,
            object_type="verification_evidence",
            object_attrs={**evidence.to_dict(), "object_key": evidence.evidence_id, "display_name": evidence.evidence_kind},
        )

    @staticmethod
    def _result_object(result: VerificationResult) -> OCELObject:
        return OCELObject(
            object_id=result.result_id,
            object_type="verification_result",
            object_attrs={**result.to_dict(), "object_key": result.result_id, "display_name": result.status},
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        if qualifier == "session_context":
            return OCELObject(object_id=object_id, object_type="session", object_attrs={"object_key": object_id, "display_name": object_id})
        if qualifier == "turn_context":
            return OCELObject(object_id=object_id, object_type="conversation_turn", object_attrs={"object_key": object_id, "display_name": object_id})
        if qualifier == "process_context":
            return OCELObject(object_id=object_id, object_type="process_instance", object_attrs={"object_key": object_id, "display_name": object_id})
        return None

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

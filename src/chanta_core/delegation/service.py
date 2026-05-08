from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.delegation.ids import (
    new_delegated_process_run_id,
    new_delegation_link_id,
    new_delegation_packet_id,
    new_delegation_result_id,
)
from chanta_core.delegation.models import (
    DelegatedProcessRun,
    DelegationLink,
    DelegationPacket,
    DelegationResult,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class DelegatedProcessRunService:
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

    def create_delegation_packet(
        self,
        *,
        goal: str,
        packet_name: str | None = None,
        context_summary: str | None = None,
        structured_inputs: dict[str, Any] | None = None,
        object_refs: list[dict[str, Any]] | None = None,
        allowed_capabilities: list[str] | None = None,
        expected_output_schema: dict[str, Any] | None = None,
        termination_conditions: dict[str, Any] | None = None,
        parent_session_id: str | None = None,
        parent_turn_id: str | None = None,
        parent_message_id: str | None = None,
        parent_process_instance_id: str | None = None,
        permission_request_ids: list[str] | None = None,
        session_permission_resolution_ids: list[str] | None = None,
        workspace_write_sandbox_decision_ids: list[str] | None = None,
        shell_network_pre_sandbox_decision_ids: list[str] | None = None,
        process_outcome_evaluation_ids: list[str] | None = None,
        packet_attrs: dict[str, Any] | None = None,
    ) -> DelegationPacket:
        packet = DelegationPacket(
            packet_id=new_delegation_packet_id(),
            packet_name=packet_name,
            parent_session_id=parent_session_id,
            parent_turn_id=parent_turn_id,
            parent_message_id=parent_message_id,
            parent_process_instance_id=parent_process_instance_id,
            goal=goal,
            context_summary=context_summary,
            structured_inputs=dict(structured_inputs or {}),
            object_refs=list(object_refs or []),
            allowed_capabilities=list(allowed_capabilities or []),
            expected_output_schema=expected_output_schema,
            termination_conditions=dict(termination_conditions or {}),
            permission_request_ids=list(permission_request_ids or []),
            session_permission_resolution_ids=list(session_permission_resolution_ids or []),
            workspace_write_sandbox_decision_ids=list(workspace_write_sandbox_decision_ids or []),
            shell_network_pre_sandbox_decision_ids=list(shell_network_pre_sandbox_decision_ids or []),
            process_outcome_evaluation_ids=list(process_outcome_evaluation_ids or []),
            created_at=utc_now_iso(),
            packet_attrs={**dict(packet_attrs or {}), "contains_full_parent_transcript": False},
        )
        event_relations, object_relations = self._packet_context_relations(packet)
        self._record_event(
            "delegation_packet_created",
            packet=packet,
            event_attrs={"goal": goal, "contains_full_parent_transcript": False},
            event_relations=[("packet_object", packet.packet_id), *event_relations],
            object_relations=object_relations,
        )
        if packet.permission_request_ids or packet.session_permission_resolution_ids:
            self._record_event(
                "delegation_permission_context_referenced",
                packet=packet,
                event_attrs={"permission_reference_count": len(packet.permission_request_ids)},
                event_relations=[("packet_object", packet.packet_id), *event_relations],
                object_relations=object_relations,
            )
        if (
            packet.workspace_write_sandbox_decision_ids
            or packet.shell_network_pre_sandbox_decision_ids
            or packet.process_outcome_evaluation_ids
        ):
            self._record_event(
                "delegation_safety_context_referenced",
                packet=packet,
                event_attrs={"safety_reference_count": self._safety_reference_count(packet)},
                event_relations=[("packet_object", packet.packet_id), *event_relations],
                object_relations=object_relations,
            )
        return packet

    def create_delegated_process_run(
        self,
        *,
        packet_id: str,
        parent_session_id: str | None = None,
        child_session_id: str | None = None,
        parent_process_instance_id: str | None = None,
        child_process_instance_id: str | None = None,
        delegation_type: str = "subprocess",
        isolation_mode: str = "packet_only",
        requester_type: str | None = None,
        requester_id: str | None = None,
        allowed_capabilities: list[str] | None = None,
        run_attrs: dict[str, Any] | None = None,
    ) -> DelegatedProcessRun:
        run = DelegatedProcessRun(
            delegated_run_id=new_delegated_process_run_id(),
            packet_id=packet_id,
            parent_session_id=parent_session_id,
            child_session_id=child_session_id,
            parent_process_instance_id=parent_process_instance_id,
            child_process_instance_id=child_process_instance_id,
            delegation_type=delegation_type,
            isolation_mode=isolation_mode,
            status="created",
            requested_at=utc_now_iso(),
            started_at=None,
            completed_at=None,
            failed_at=None,
            requester_type=requester_type,
            requester_id=requester_id,
            allowed_capabilities=list(allowed_capabilities or []),
            inherited_permissions=False,
            run_attrs={**dict(run_attrs or {}), "runtime_effect": False},
        )
        self._record_run_event("delegated_process_run_created", run=run, event_attrs={})
        return run

    def request_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(run, status="requested")
        self._record_run_event("delegated_process_requested", run=updated, event_attrs={"reason": reason})
        return updated

    def start_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(run, status="started", started_at=utc_now_iso())
        self._record_run_event("delegated_process_started", run=updated, event_attrs={"reason": reason})
        return updated

    def complete_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(run, status="completed", completed_at=utc_now_iso())
        self._record_run_event("delegated_process_completed", run=updated, event_attrs={"reason": reason})
        return updated

    def fail_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        failure: dict[str, Any] | None = None,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(
            run,
            status="failed",
            failed_at=utc_now_iso(),
            run_attrs={**run.run_attrs, "failure": dict(failure or {})},
        )
        self._record_run_event("delegated_process_failed", run=updated, event_attrs={"reason": reason, "failure": failure})
        return updated

    def cancel_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(run, status="cancelled", completed_at=utc_now_iso())
        self._record_run_event("delegated_process_cancelled", run=updated, event_attrs={"reason": reason})
        return updated

    def skip_delegated_process_run(
        self,
        *,
        run: DelegatedProcessRun,
        reason: str | None = None,
    ) -> DelegatedProcessRun:
        updated = replace(run, status="skipped", completed_at=utc_now_iso())
        self._record_run_event("delegated_process_skipped", run=updated, event_attrs={"reason": reason})
        return updated

    def record_delegation_result(
        self,
        *,
        delegated_run_id: str,
        packet_id: str,
        status: str,
        output_summary: str | None = None,
        output_payload: dict[str, Any] | None = None,
        evidence_refs: list[dict[str, Any]] | None = None,
        recommendation_refs: list[dict[str, Any]] | None = None,
        failure: dict[str, Any] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> DelegationResult:
        result = DelegationResult(
            result_id=new_delegation_result_id(),
            delegated_run_id=delegated_run_id,
            packet_id=packet_id,
            status=status,
            output_summary=output_summary,
            output_payload=dict(output_payload or {}),
            evidence_refs=list(evidence_refs or []),
            recommendation_refs=list(recommendation_refs or []),
            failure=failure,
            created_at=utc_now_iso(),
            result_attrs=dict(result_attrs or {}),
        )
        self._record_event(
            "delegation_result_recorded",
            result=result,
            event_attrs={"status": status},
            event_relations=[
                ("result_object", result.result_id),
                ("delegated_run_object", delegated_run_id),
                ("packet_object", packet_id),
            ],
            object_relations=[
                (result.result_id, delegated_run_id, "result_of_delegated_run"),
                (result.result_id, packet_id, "uses_packet"),
            ],
        )
        return result

    def record_delegation_link(
        self,
        *,
        delegated_run_id: str,
        parent_process_instance_id: str | None = None,
        child_process_instance_id: str | None = None,
        parent_session_id: str | None = None,
        child_session_id: str | None = None,
        relation_type: str = "delegated_to",
        link_attrs: dict[str, Any] | None = None,
    ) -> DelegationLink:
        link = DelegationLink(
            link_id=new_delegation_link_id(),
            delegated_run_id=delegated_run_id,
            parent_process_instance_id=parent_process_instance_id,
            child_process_instance_id=child_process_instance_id,
            parent_session_id=parent_session_id,
            child_session_id=child_session_id,
            relation_type=relation_type,
            created_at=utc_now_iso(),
            link_attrs=dict(link_attrs or {}),
        )
        event_relations, object_relations = self._link_context_relations(link)
        self._record_event(
            "delegation_link_recorded",
            link=link,
            event_attrs={"relation_type": relation_type},
            event_relations=[("link_object", link.link_id), ("delegated_run_object", delegated_run_id), *event_relations],
            object_relations=[(link.link_id, delegated_run_id, "links_delegated_run"), *object_relations],
        )
        return link

    def _record_run_event(
        self,
        event_activity: str,
        *,
        run: DelegatedProcessRun,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations, object_relations = self._run_context_relations(run)
        self._record_event(
            event_activity,
            run=run,
            event_attrs={"status": run.status, **event_attrs},
            event_relations=[
                ("delegated_run_object", run.delegated_run_id),
                ("packet_object", run.packet_id),
                *event_relations,
            ],
            object_relations=[
                (run.delegated_run_id, run.packet_id, "uses_packet"),
                *object_relations,
            ],
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        packet: DelegationPacket | None = None,
        run: DelegatedProcessRun | None = None,
        result: DelegationResult | None = None,
        link: DelegationLink | None = None,
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
                "delegation_model_only": True,
                "runtime_effect": False,
                "enforcement_enabled": False,
            },
        )
        objects = self._objects_for_event(
            packet=packet,
            run=run,
            result=result,
            link=link,
            event_relations=event_relations,
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source, target_object_id=target, qualifier=qualifier)
            for source, target, qualifier in object_relations
            if source and target
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _objects_for_event(
        self,
        *,
        packet: DelegationPacket | None,
        run: DelegatedProcessRun | None,
        result: DelegationResult | None,
        link: DelegationLink | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if packet is not None:
            objects.append(self._packet_object(packet))
        if run is not None:
            objects.append(self._run_object(run))
        if result is not None:
            objects.append(self._result_object(result))
        if link is not None:
            objects.append(self._link_object(link))
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
    def _packet_object(packet: DelegationPacket) -> OCELObject:
        return OCELObject(
            object_id=packet.packet_id,
            object_type="delegation_packet",
            object_attrs={
                **packet.to_dict(),
                "object_key": packet.packet_id,
                "display_name": packet.packet_name or packet.goal,
                "contains_full_parent_transcript": False,
            },
        )

    @staticmethod
    def _run_object(run: DelegatedProcessRun) -> OCELObject:
        return OCELObject(
            object_id=run.delegated_run_id,
            object_type="delegated_process_run",
            object_attrs={
                **run.to_dict(),
                "object_key": run.delegated_run_id,
                "display_name": run.delegation_type,
                "inherited_permissions": False,
            },
        )

    @staticmethod
    def _result_object(result: DelegationResult) -> OCELObject:
        return OCELObject(
            object_id=result.result_id,
            object_type="delegation_result",
            object_attrs={**result.to_dict(), "object_key": result.result_id, "display_name": result.status},
        )

    @staticmethod
    def _link_object(link: DelegationLink) -> OCELObject:
        return OCELObject(
            object_id=link.link_id,
            object_type="delegation_link",
            object_attrs={**link.to_dict(), "object_key": link.link_id, "display_name": link.relation_type},
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "parent_session": "session",
            "child_session": "session",
            "parent_turn": "conversation_turn",
            "parent_message": "message",
            "parent_process": "process_instance",
            "child_process": "process_instance",
            "permission_request_object": "permission_request",
            "session_permission_resolution_object": "session_permission_resolution",
            "workspace_write_decision_object": "workspace_write_sandbox_decision",
            "shell_network_decision_object": "shell_network_pre_sandbox_decision",
            "process_outcome_object": "process_outcome_evaluation",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id})

    def _packet_context_relations(self, packet: DelegationPacket) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if packet.parent_session_id:
            session_object_id = self._session_object_id(packet.parent_session_id)
            event_relations.append(("parent_session", session_object_id))
        if packet.parent_turn_id:
            event_relations.append(("parent_turn", packet.parent_turn_id))
        if packet.parent_message_id:
            event_relations.append(("parent_message", packet.parent_message_id))
        if packet.parent_process_instance_id:
            event_relations.append(("parent_process", packet.parent_process_instance_id))
        for request_id in packet.permission_request_ids:
            event_relations.append(("permission_request_object", request_id))
            object_relations.append((packet.packet_id, request_id, "references_permission_request"))
        for resolution_id in packet.session_permission_resolution_ids:
            event_relations.append(("session_permission_resolution_object", resolution_id))
            object_relations.append((packet.packet_id, resolution_id, "references_session_permission_resolution"))
        for decision_id in packet.workspace_write_sandbox_decision_ids:
            event_relations.append(("workspace_write_decision_object", decision_id))
            object_relations.append((packet.packet_id, decision_id, "references_workspace_write_decision"))
        for decision_id in packet.shell_network_pre_sandbox_decision_ids:
            event_relations.append(("shell_network_decision_object", decision_id))
            object_relations.append((packet.packet_id, decision_id, "references_shell_network_decision"))
        for evaluation_id in packet.process_outcome_evaluation_ids:
            event_relations.append(("process_outcome_object", evaluation_id))
            object_relations.append((packet.packet_id, evaluation_id, "references_process_outcome"))
        return event_relations, object_relations

    def _run_context_relations(self, run: DelegatedProcessRun) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if run.parent_session_id:
            session_object_id = self._session_object_id(run.parent_session_id)
            event_relations.append(("parent_session", session_object_id))
            object_relations.append((run.delegated_run_id, session_object_id, "parent_session"))
        if run.child_session_id:
            session_object_id = self._session_object_id(run.child_session_id)
            event_relations.append(("child_session", session_object_id))
            object_relations.append((run.delegated_run_id, session_object_id, "child_session"))
        if run.parent_process_instance_id:
            event_relations.append(("parent_process", run.parent_process_instance_id))
            object_relations.append((run.delegated_run_id, run.parent_process_instance_id, "parent_process_instance"))
        if run.child_process_instance_id:
            event_relations.append(("child_process", run.child_process_instance_id))
            object_relations.append((run.delegated_run_id, run.child_process_instance_id, "child_process_instance"))
        return event_relations, object_relations

    def _link_context_relations(self, link: DelegationLink) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if link.parent_session_id:
            event_relations.append(("parent_session", self._session_object_id(link.parent_session_id)))
        if link.child_session_id:
            event_relations.append(("child_session", self._session_object_id(link.child_session_id)))
        if link.parent_process_instance_id:
            event_relations.append(("parent_process", link.parent_process_instance_id))
        if link.child_process_instance_id:
            event_relations.append(("child_process", link.child_process_instance_id))
        return event_relations, object_relations

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"

    @staticmethod
    def _safety_reference_count(packet: DelegationPacket) -> int:
        return (
            len(packet.workspace_write_sandbox_decision_ids)
            + len(packet.shell_network_pre_sandbox_decision_ids)
            + len(packet.process_outcome_evaluation_ids)
        )

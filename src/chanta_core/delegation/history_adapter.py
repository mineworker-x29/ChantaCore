from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.delegation.conformance import DelegationConformanceFinding, DelegationConformanceResult
from chanta_core.delegation.models import DelegatedProcessRun, DelegationPacket, DelegationResult
from chanta_core.delegation.sidechain import (
    SidechainContext,
    SidechainContextEntry,
    SidechainContextSnapshot,
    SidechainReturnEnvelope,
)


def delegation_packets_to_history_entries(
    packets: list[DelegationPacket],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=packet.parent_session_id,
            process_instance_id=packet.parent_process_instance_id,
            role="context",
            content=f"Delegation packet: {packet.goal}",
            created_at=packet.created_at,
            source="delegation",
            priority=45,
            refs=[_packet_ref(packet)],
            entry_attrs={"packet_id": packet.packet_id, "packet_name": packet.packet_name},
        )
        for packet in packets
    ]


def delegated_process_runs_to_history_entries(
    runs: list[DelegatedProcessRun],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=run.parent_session_id,
            process_instance_id=run.parent_process_instance_id,
            role="context",
            content=f"Delegated process run: {run.status}\nType: {run.delegation_type}",
            created_at=run.requested_at,
            source="delegation",
            priority=_run_priority(run),
            refs=[_run_ref(run)],
            entry_attrs={"delegated_run_id": run.delegated_run_id, "status": run.status},
        )
        for run in runs
    ]


def delegation_results_to_history_entries(
    results: list[DelegationResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Delegation result: {result.status}\n{result.output_summary or ''}".rstrip(),
            created_at=result.created_at,
            source="delegation",
            priority=_result_priority(result),
            refs=[_result_ref(result)],
            entry_attrs={"result_id": result.result_id, "status": result.status},
        )
        for result in results
    ]


def sidechain_contexts_to_history_entries(
    contexts: list[SidechainContext],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=context.parent_session_id,
            process_instance_id=context.parent_process_instance_id,
            role="context",
            content=f"Sidechain context: {context.status}\nType: {context.context_type}",
            created_at=context.created_at,
            source="sidechain_context",
            priority=_sidechain_context_priority(context),
            refs=[_sidechain_context_ref(context)],
            entry_attrs={
                "sidechain_context_id": context.sidechain_context_id,
                "packet_id": context.packet_id,
                "status": context.status,
            },
        )
        for context in contexts
    ]


def sidechain_context_entries_to_history_entries(
    entries: list[SidechainContextEntry],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=_sidechain_entry_content(entry),
            created_at=entry.created_at,
            source="sidechain_context",
            priority=_sidechain_entry_priority(entry),
            refs=[_sidechain_entry_ref(entry)],
            entry_attrs={
                "sidechain_context_id": entry.sidechain_context_id,
                "entry_id": entry.entry_id,
                "entry_type": entry.entry_type,
            },
        )
        for entry in entries
    ]


def sidechain_context_snapshots_to_history_entries(
    snapshots: list[SidechainContextSnapshot],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Sidechain context snapshot: {snapshot.entry_count} entries\n{snapshot.summary or ''}".rstrip(),
            created_at=snapshot.created_at,
            source="sidechain_context",
            priority=45 if snapshot.summary else 35,
            refs=[_sidechain_snapshot_ref(snapshot)],
            entry_attrs={
                "sidechain_context_id": snapshot.sidechain_context_id,
                "snapshot_id": snapshot.snapshot_id,
                "packet_id": snapshot.packet_id,
            },
        )
        for snapshot in snapshots
    ]


def sidechain_return_envelopes_to_history_entries(
    envelopes: list[SidechainReturnEnvelope],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Sidechain return envelope: {envelope.status}\n{envelope.summary or ''}".rstrip(),
            created_at=envelope.created_at,
            source="sidechain_context",
            priority=_sidechain_envelope_priority(envelope),
            refs=[_sidechain_envelope_ref(envelope)],
            entry_attrs={
                "sidechain_context_id": envelope.sidechain_context_id,
                "envelope_id": envelope.envelope_id,
                "packet_id": envelope.packet_id,
                "delegated_run_id": envelope.delegated_run_id,
                "status": envelope.status,
            },
        )
        for envelope in envelopes
    ]


def delegation_conformance_findings_to_history_entries(
    findings: list[DelegationConformanceFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Delegation conformance finding: {finding.status}\n{finding.message}",
            created_at=finding.created_at,
            source="delegation_conformance",
            priority=_conformance_finding_priority(finding),
            refs=[_conformance_finding_ref(finding)],
            entry_attrs={
                "finding_id": finding.finding_id,
                "run_id": finding.run_id,
                "rule_id": finding.rule_id,
                "rule_type": finding.rule_type,
                "status": finding.status,
            },
        )
        for finding in findings
    ]


def delegation_conformance_results_to_history_entries(
    results: list[DelegationConformanceResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Delegation conformance result: {result.status}\n{result.reason or ''}".rstrip(),
            created_at=result.created_at,
            source="delegation_conformance",
            priority=_conformance_result_priority(result),
            refs=[_conformance_result_ref(result)],
            entry_attrs={
                "result_id": result.result_id,
                "run_id": result.run_id,
                "contract_id": result.contract_id,
                "status": result.status,
                "score": result.score,
            },
        )
        for result in results
    ]


def _packet_ref(packet: DelegationPacket) -> dict:
    return {
        "ref_type": "delegation_packet",
        "ref_id": packet.packet_id,
        "packet_id": packet.packet_id,
        "parent_session_id": packet.parent_session_id,
        "parent_process_instance_id": packet.parent_process_instance_id,
        "permission_request_ids": packet.permission_request_ids,
        "session_permission_resolution_ids": packet.session_permission_resolution_ids,
        "workspace_write_sandbox_decision_ids": packet.workspace_write_sandbox_decision_ids,
        "shell_network_pre_sandbox_decision_ids": packet.shell_network_pre_sandbox_decision_ids,
        "process_outcome_evaluation_ids": packet.process_outcome_evaluation_ids,
    }


def _run_ref(run: DelegatedProcessRun) -> dict:
    return {
        "ref_type": "delegated_process_run",
        "ref_id": run.delegated_run_id,
        "packet_id": run.packet_id,
        "delegated_run_id": run.delegated_run_id,
        "parent_session_id": run.parent_session_id,
        "child_session_id": run.child_session_id,
        "parent_process_instance_id": run.parent_process_instance_id,
        "child_process_instance_id": run.child_process_instance_id,
    }


def _result_ref(result: DelegationResult) -> dict:
    return {
        "ref_type": "delegation_result",
        "ref_id": result.result_id,
        "packet_id": result.packet_id,
        "delegated_run_id": result.delegated_run_id,
        "result_id": result.result_id,
        "evidence_refs": result.evidence_refs,
        "recommendation_refs": result.recommendation_refs,
    }


def _sidechain_context_ref(context: SidechainContext) -> dict:
    return {
        "ref_type": "sidechain_context",
        "ref_id": context.sidechain_context_id,
        "sidechain_context_id": context.sidechain_context_id,
        "packet_id": context.packet_id,
        "delegated_run_id": context.delegated_run_id,
        "parent_session_id": context.parent_session_id,
        "child_session_id": context.child_session_id,
        "parent_process_instance_id": context.parent_process_instance_id,
        "child_process_instance_id": context.child_process_instance_id,
        "entry_ids": context.entry_ids,
        "safety_ref_ids": context.safety_ref_ids,
    }


def _sidechain_entry_ref(entry: SidechainContextEntry) -> dict:
    return {
        "ref_type": "sidechain_context_entry",
        "ref_id": entry.entry_id,
        "sidechain_context_id": entry.sidechain_context_id,
        "entry_id": entry.entry_id,
        "entry_type": entry.entry_type,
        "source_kind": entry.source_kind,
        "source_ref": entry.source_ref,
    }


def _sidechain_snapshot_ref(snapshot: SidechainContextSnapshot) -> dict:
    return {
        "ref_type": "sidechain_context_snapshot",
        "ref_id": snapshot.snapshot_id,
        "sidechain_context_id": snapshot.sidechain_context_id,
        "snapshot_id": snapshot.snapshot_id,
        "packet_id": snapshot.packet_id,
        "delegated_run_id": snapshot.delegated_run_id,
        "entry_ids": snapshot.entry_ids,
    }


def _sidechain_envelope_ref(envelope: SidechainReturnEnvelope) -> dict:
    return {
        "ref_type": "sidechain_return_envelope",
        "ref_id": envelope.envelope_id,
        "sidechain_context_id": envelope.sidechain_context_id,
        "envelope_id": envelope.envelope_id,
        "packet_id": envelope.packet_id,
        "delegated_run_id": envelope.delegated_run_id,
        "evidence_refs": envelope.evidence_refs,
        "recommendation_refs": envelope.recommendation_refs,
    }


def _conformance_finding_ref(finding: DelegationConformanceFinding) -> dict:
    return {
        "ref_type": "delegation_conformance_finding",
        "ref_id": finding.finding_id,
        "finding_id": finding.finding_id,
        "run_id": finding.run_id,
        "rule_id": finding.rule_id,
        "rule_type": finding.rule_type,
        "subject_type": finding.subject_type,
        "subject_ref": finding.subject_ref,
        "evidence_refs": finding.evidence_refs,
    }


def _conformance_result_ref(result: DelegationConformanceResult) -> dict:
    return {
        "ref_type": "delegation_conformance_result",
        "ref_id": result.result_id,
        "result_id": result.result_id,
        "run_id": result.run_id,
        "contract_id": result.contract_id,
        "passed_finding_ids": result.passed_finding_ids,
        "failed_finding_ids": result.failed_finding_ids,
        "warning_finding_ids": result.warning_finding_ids,
        "skipped_finding_ids": result.skipped_finding_ids,
    }


def _run_priority(run: DelegatedProcessRun) -> int:
    if run.status == "failed":
        return 90
    if run.status in {"requested", "started", "completed"}:
        return 60
    if run.status in {"cancelled", "skipped"}:
        return 55
    return 40


def _result_priority(result: DelegationResult) -> int:
    if result.status == "failed":
        return 90
    if result.status == "inconclusive":
        return 80
    return 60


def _sidechain_context_priority(context: SidechainContext) -> int:
    if context.status == "error":
        return 90
    if context.status in {"ready", "sealed"}:
        return 60
    return 40


def _sidechain_entry_priority(entry: SidechainContextEntry) -> int:
    if entry.entry_type in {"permission_ref", "sandbox_ref", "risk_ref", "outcome_ref"}:
        return entry.priority or 80
    if entry.entry_type in {"goal", "context_summary"}:
        return entry.priority or 60
    return entry.priority or 45


def _sidechain_envelope_priority(envelope: SidechainReturnEnvelope) -> int:
    if envelope.status == "failed":
        return 90
    if envelope.status == "inconclusive":
        return 80
    return 60


def _sidechain_entry_content(entry: SidechainContextEntry) -> str:
    details = entry.content or entry.content_ref or ""
    return f"Sidechain context entry: {entry.entry_type}\n{details}".rstrip()


def _conformance_finding_priority(finding: DelegationConformanceFinding) -> int:
    if finding.status in {"failed", "error"}:
        return 90
    if finding.status == "warning":
        return 70
    if finding.status == "inconclusive":
        return 60
    return 45


def _conformance_result_priority(result: DelegationConformanceResult) -> int:
    if result.status in {"failed", "error"}:
        return 95
    if result.status == "needs_review":
        return 85
    if result.status == "inconclusive":
        return 70
    return 50

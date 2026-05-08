from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityRiskNote,
)
from chanta_core.external.mcp_plugin import (
    ExternalDescriptorSkeleton,
    ExternalDescriptorSkeletonValidation,
    MCPServerDescriptor,
    MCPToolDescriptor,
    PluginDescriptor,
    PluginEntrypointDescriptor,
)
from chanta_core.external.ocel_import import (
    ExternalOCELImportCandidate,
    ExternalOCELImportRiskNote,
    ExternalOCELPreviewSnapshot,
    ExternalOCELValidationResult,
)
from chanta_core.external.review import (
    ExternalAdapterReviewDecision,
    ExternalAdapterReviewFinding,
    ExternalAdapterReviewItem,
)
from chanta_core.external.views import ExternalCapabilityRegistrySnapshot


def external_capability_descriptors_to_history_entries(
    descriptors: list[ExternalCapabilityDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External capability descriptor: {descriptor.capability_name}\nType: {descriptor.capability_type}",
            created_at=descriptor.created_at,
            source="external_capability",
            priority=45 if descriptor.normalized else 35,
            refs=[_descriptor_ref(descriptor)],
            entry_attrs={
                "descriptor_id": descriptor.descriptor_id,
                "source_id": descriptor.source_id,
                "capability_type": descriptor.capability_type,
                "status": descriptor.status,
            },
        )
        for descriptor in descriptors
    ]


def external_assimilation_candidates_to_history_entries(
    candidates: list[ExternalAssimilationCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External assimilation candidate: {candidate.candidate_name}\nStatus: {candidate.activation_status}",
            created_at=candidate.created_at,
            source="external_capability",
            priority=_candidate_priority(candidate),
            refs=[_candidate_ref(candidate)],
            entry_attrs={
                "candidate_id": candidate.candidate_id,
                "descriptor_id": candidate.descriptor_id,
                "source_id": candidate.source_id,
                "review_status": candidate.review_status,
                "activation_status": candidate.activation_status,
                "execution_enabled": False,
            },
        )
        for candidate in candidates
    ]


def external_capability_risk_notes_to_history_entries(
    risk_notes: list[ExternalCapabilityRiskNote],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External capability risk note: {note.risk_level}\n{note.message}",
            created_at=note.created_at,
            source="external_capability",
            priority=_risk_priority(note),
            refs=[_risk_note_ref(note)],
            entry_attrs={
                "risk_note_id": note.risk_note_id,
                "descriptor_id": note.descriptor_id,
                "candidate_id": note.candidate_id,
                "risk_level": note.risk_level,
                "risk_categories": note.risk_categories,
                "review_required": note.review_required,
            },
        )
        for note in risk_notes
    ]


def external_capability_registry_snapshots_to_history_entries(
    snapshots: list[ExternalCapabilityRegistrySnapshot],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                "External capability registry snapshot: "
                f"{snapshot.snapshot_name or snapshot.snapshot_id}\n"
                f"Pending review: {snapshot.pending_review_count}\n"
                f"Execution-enabled candidates: {snapshot.execution_enabled_candidate_count}"
            ),
            created_at=snapshot.created_at,
            source="external_capability_view",
            priority=_snapshot_priority(snapshot),
            refs=[_snapshot_ref(snapshot)],
            entry_attrs={
                "snapshot_id": snapshot.snapshot_id,
                "disabled_candidate_count": snapshot.disabled_candidate_count,
                "execution_enabled_candidate_count": snapshot.execution_enabled_candidate_count,
                "pending_review_count": snapshot.pending_review_count,
                "high_risk_count": snapshot.high_risk_count,
                "critical_risk_count": snapshot.critical_risk_count,
            },
        )
        for snapshot in snapshots
    ]


def external_adapter_review_items_to_history_entries(
    items: list[ExternalAdapterReviewItem],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External adapter review item: {item.item_id}\nStatus: {item.review_status}",
            created_at=item.created_at,
            source="external_adapter_review",
            priority=_review_item_priority(item),
            refs=[_review_item_ref(item)],
            entry_attrs={
                "queue_id": item.queue_id,
                "item_id": item.item_id,
                "candidate_id": item.candidate_id,
                "descriptor_id": item.descriptor_id,
                "risk_note_ids": item.risk_note_ids,
                "review_status": item.review_status,
            },
        )
        for item in items
    ]


def external_adapter_review_findings_to_history_entries(
    findings: list[ExternalAdapterReviewFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External adapter review finding: {finding.finding_type}\n{finding.message}",
            created_at=finding.created_at,
            source="external_adapter_review",
            priority=_review_finding_priority(finding),
            refs=[_review_finding_ref(finding)],
            entry_attrs={
                "finding_id": finding.finding_id,
                "item_id": finding.item_id,
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
                "source_kind": finding.source_kind,
                "source_ref": finding.source_ref,
            },
        )
        for finding in findings
    ]


def external_adapter_review_decisions_to_history_entries(
    decisions: list[ExternalAdapterReviewDecision],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External adapter review decision: {decision.decision}",
            created_at=decision.created_at,
            source="external_adapter_review",
            priority=_review_decision_priority(decision),
            refs=[_review_decision_ref(decision)],
            entry_attrs={
                "decision_id": decision.decision_id,
                "queue_id": decision.queue_id,
                "item_id": decision.item_id,
                "candidate_id": decision.candidate_id,
                "decision": decision.decision,
                "finding_ids": decision.finding_ids,
                "checklist_id": decision.checklist_id,
                "activation_allowed": False,
                "runtime_registration_allowed": False,
                "execution_enabled_after_decision": False,
            },
        )
        for decision in decisions
    ]


def mcp_server_descriptors_to_history_entries(
    descriptors: list[MCPServerDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"MCP server descriptor: {descriptor.server_name}\nTransport: {descriptor.transport}",
            created_at=descriptor.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=45 if descriptor.status == "needs_review" else 35,
            refs=[_mcp_server_ref(descriptor)],
            entry_attrs={
                "mcp_server_id": descriptor.mcp_server_id,
                "source_id": descriptor.source_id,
                "external_descriptor_id": descriptor.external_descriptor_id,
                "status": descriptor.status,
            },
        )
        for descriptor in descriptors
    ]


def mcp_tool_descriptors_to_history_entries(
    descriptors: list[MCPToolDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"MCP tool descriptor: {descriptor.tool_name}",
            created_at=descriptor.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=45 if descriptor.status == "needs_review" else 35,
            refs=[_mcp_tool_ref(descriptor)],
            entry_attrs={
                "mcp_tool_id": descriptor.mcp_tool_id,
                "mcp_server_id": descriptor.mcp_server_id,
                "external_descriptor_id": descriptor.external_descriptor_id,
                "status": descriptor.status,
            },
        )
        for descriptor in descriptors
    ]


def plugin_descriptors_to_history_entries(
    descriptors: list[PluginDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Plugin descriptor: {descriptor.plugin_name}\nType: {descriptor.plugin_type}",
            created_at=descriptor.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=45 if descriptor.status == "needs_review" else 35,
            refs=[_plugin_ref(descriptor)],
            entry_attrs={
                "plugin_id": descriptor.plugin_id,
                "source_id": descriptor.source_id,
                "external_descriptor_id": descriptor.external_descriptor_id,
                "plugin_type": descriptor.plugin_type,
                "status": descriptor.status,
            },
        )
        for descriptor in descriptors
    ]


def plugin_entrypoint_descriptors_to_history_entries(
    descriptors: list[PluginEntrypointDescriptor],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"Plugin entrypoint descriptor: {descriptor.entrypoint_name or descriptor.entrypoint_ref}",
            created_at=descriptor.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=40,
            refs=[_plugin_entrypoint_ref(descriptor)],
            entry_attrs={
                "entrypoint_id": descriptor.entrypoint_id,
                "plugin_id": descriptor.plugin_id,
                "entrypoint_type": descriptor.entrypoint_type,
                "status": descriptor.status,
            },
        )
        for descriptor in descriptors
    ]


def external_descriptor_skeletons_to_history_entries(
    skeletons: list[ExternalDescriptorSkeleton],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External descriptor skeleton: {skeleton.normalized_name or skeleton.skeleton_type}",
            created_at=skeleton.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=_skeleton_priority(skeleton),
            refs=[_skeleton_ref(skeleton)],
            entry_attrs={
                "skeleton_id": skeleton.skeleton_id,
                "mcp_server_id": skeleton.mcp_server_id,
                "plugin_id": skeleton.plugin_id,
                "external_descriptor_id": skeleton.external_descriptor_id,
                "source_id": skeleton.source_id,
                "execution_enabled": False,
                "activation_status": skeleton.activation_status,
            },
        )
        for skeleton in skeletons
    ]


def external_descriptor_skeleton_validations_to_history_entries(
    validations: list[ExternalDescriptorSkeletonValidation],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External descriptor skeleton validation: {validation.status}",
            created_at=validation.created_at,
            source="mcp_plugin_descriptor_skeleton",
            priority=_skeleton_validation_priority(validation),
            refs=[_skeleton_validation_ref(validation)],
            entry_attrs={
                "validation_id": validation.validation_id,
                "skeleton_id": validation.skeleton_id,
                "status": validation.status,
                "failed_checks": validation.failed_checks,
                "warning_checks": validation.warning_checks,
            },
        )
        for validation in validations
    ]


def external_ocel_candidates_to_history_entries(
    candidates: list[ExternalOCELImportCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"External OCEL import candidate: {candidate.candidate_name or candidate.candidate_id}\n"
                f"Review: {candidate.review_status}\nMerge: {candidate.merge_status}"
            ),
            created_at=candidate.created_at,
            source="external_ocel_import",
            priority=75 if candidate.review_status == "pending_review" else 55,
            refs=[_external_ocel_candidate_ref(candidate)],
            entry_attrs={
                "candidate_id": candidate.candidate_id,
                "descriptor_id": candidate.descriptor_id,
                "source_id": candidate.source_id,
                "review_status": candidate.review_status,
                "merge_status": candidate.merge_status,
                "canonical_import_enabled": False,
            },
        )
        for candidate in candidates
    ]


def external_ocel_validation_results_to_history_entries(
    validations: list[ExternalOCELValidationResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External OCEL validation: {validation.status}\nSchema: {validation.schema_status}",
            created_at=validation.created_at,
            source="external_ocel_import",
            priority=_external_ocel_validation_priority(validation),
            refs=[_external_ocel_validation_ref(validation)],
            entry_attrs={
                "validation_id": validation.validation_id,
                "descriptor_id": validation.descriptor_id,
                "candidate_id": validation.candidate_id,
                "status": validation.status,
                "schema_status": validation.schema_status,
                "missing_fields": validation.missing_fields,
            },
        )
        for validation in validations
    ]


def external_ocel_preview_snapshots_to_history_entries(
    previews: list[ExternalOCELPreviewSnapshot],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                "External OCEL preview snapshot\n"
                f"Events/objects/relations: {preview.event_count}/{preview.object_count}/{preview.relation_count}"
            ),
            created_at=preview.created_at,
            source="external_ocel_import",
            priority=45 if preview.event_count else 35,
            refs=[_external_ocel_preview_ref(preview)],
            entry_attrs={
                "preview_id": preview.preview_id,
                "descriptor_id": preview.descriptor_id,
                "candidate_id": preview.candidate_id,
                "event_count": preview.event_count,
                "object_count": preview.object_count,
                "relation_count": preview.relation_count,
            },
        )
        for preview in previews
    ]


def external_ocel_risk_notes_to_history_entries(
    notes: list[ExternalOCELImportRiskNote],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=f"External OCEL risk note: {note.risk_level}\n{note.message}",
            created_at=note.created_at,
            source="external_ocel_import",
            priority=90 if note.risk_level in {"critical", "high"} else 75 if note.risk_level == "medium" else 50,
            refs=[_external_ocel_risk_ref(note)],
            entry_attrs={
                "risk_note_id": note.risk_note_id,
                "descriptor_id": note.descriptor_id,
                "candidate_id": note.candidate_id,
                "risk_level": note.risk_level,
                "risk_categories": note.risk_categories,
                "review_required": note.review_required,
            },
        )
        for note in notes
    ]


def _descriptor_ref(descriptor: ExternalCapabilityDescriptor) -> dict:
    return {
        "ref_type": "external_capability_descriptor",
        "ref_id": descriptor.descriptor_id,
        "descriptor_id": descriptor.descriptor_id,
        "source_id": descriptor.source_id,
    }


def _candidate_ref(candidate: ExternalAssimilationCandidate) -> dict:
    return {
        "ref_type": "external_assimilation_candidate",
        "ref_id": candidate.candidate_id,
        "candidate_id": candidate.candidate_id,
        "descriptor_id": candidate.descriptor_id,
        "source_id": candidate.source_id,
        "linked_tool_descriptor_id": candidate.linked_tool_descriptor_id,
        "linked_permission_scope_id": candidate.linked_permission_scope_id,
        "linked_risk_note_ids": candidate.linked_risk_note_ids,
    }


def _risk_note_ref(note: ExternalCapabilityRiskNote) -> dict:
    return {
        "ref_type": "external_capability_risk_note",
        "ref_id": note.risk_note_id,
        "risk_note_id": note.risk_note_id,
        "descriptor_id": note.descriptor_id,
        "candidate_id": note.candidate_id,
    }


def _snapshot_ref(snapshot: ExternalCapabilityRegistrySnapshot) -> dict:
    return {
        "ref_type": "external_capability_registry_snapshot",
        "ref_id": snapshot.snapshot_id,
        "snapshot_id": snapshot.snapshot_id,
        "source_ids": snapshot.source_ids,
        "descriptor_ids": snapshot.descriptor_ids,
        "candidate_ids": snapshot.candidate_ids,
        "risk_note_ids": snapshot.risk_note_ids,
    }


def _review_item_ref(item: ExternalAdapterReviewItem) -> dict:
    return {
        "ref_type": "external_adapter_review_item",
        "ref_id": item.item_id,
        "queue_id": item.queue_id,
        "item_id": item.item_id,
        "candidate_id": item.candidate_id,
        "descriptor_id": item.descriptor_id,
        "risk_note_ids": item.risk_note_ids,
    }


def _review_finding_ref(finding: ExternalAdapterReviewFinding) -> dict:
    return {
        "ref_type": "external_adapter_review_finding",
        "ref_id": finding.finding_id,
        "finding_id": finding.finding_id,
        "item_id": finding.item_id,
        "source_kind": finding.source_kind,
        "source_ref": finding.source_ref,
    }


def _review_decision_ref(decision: ExternalAdapterReviewDecision) -> dict:
    return {
        "ref_type": "external_adapter_review_decision",
        "ref_id": decision.decision_id,
        "decision_id": decision.decision_id,
        "queue_id": decision.queue_id,
        "item_id": decision.item_id,
        "candidate_id": decision.candidate_id,
        "finding_ids": decision.finding_ids,
        "checklist_id": decision.checklist_id,
    }


def _mcp_server_ref(descriptor: MCPServerDescriptor) -> dict:
    return {
        "ref_type": "mcp_server_descriptor",
        "ref_id": descriptor.mcp_server_id,
        "mcp_server_id": descriptor.mcp_server_id,
        "source_id": descriptor.source_id,
        "external_descriptor_id": descriptor.external_descriptor_id,
    }


def _mcp_tool_ref(descriptor: MCPToolDescriptor) -> dict:
    return {
        "ref_type": "mcp_tool_descriptor",
        "ref_id": descriptor.mcp_tool_id,
        "mcp_tool_id": descriptor.mcp_tool_id,
        "mcp_server_id": descriptor.mcp_server_id,
        "external_descriptor_id": descriptor.external_descriptor_id,
    }


def _plugin_ref(descriptor: PluginDescriptor) -> dict:
    return {
        "ref_type": "plugin_descriptor",
        "ref_id": descriptor.plugin_id,
        "plugin_id": descriptor.plugin_id,
        "source_id": descriptor.source_id,
        "external_descriptor_id": descriptor.external_descriptor_id,
    }


def _plugin_entrypoint_ref(descriptor: PluginEntrypointDescriptor) -> dict:
    return {
        "ref_type": "plugin_entrypoint_descriptor",
        "ref_id": descriptor.entrypoint_id,
        "entrypoint_id": descriptor.entrypoint_id,
        "plugin_id": descriptor.plugin_id,
    }


def _skeleton_ref(skeleton: ExternalDescriptorSkeleton) -> dict:
    return {
        "ref_type": "external_descriptor_skeleton",
        "ref_id": skeleton.skeleton_id,
        "skeleton_id": skeleton.skeleton_id,
        "source_id": skeleton.source_id,
        "external_descriptor_id": skeleton.external_descriptor_id,
        "mcp_server_id": skeleton.mcp_server_id,
        "plugin_id": skeleton.plugin_id,
    }


def _skeleton_validation_ref(validation: ExternalDescriptorSkeletonValidation) -> dict:
    return {
        "ref_type": "external_descriptor_skeleton_validation",
        "ref_id": validation.validation_id,
        "validation_id": validation.validation_id,
        "skeleton_id": validation.skeleton_id,
    }


def _external_ocel_candidate_ref(candidate: ExternalOCELImportCandidate) -> dict:
    return {
        "ref_type": "external_ocel_import_candidate",
        "ref_id": candidate.candidate_id,
        "candidate_id": candidate.candidate_id,
        "descriptor_id": candidate.descriptor_id,
        "source_id": candidate.source_id,
        "validation_result_ids": candidate.validation_result_ids,
        "preview_snapshot_ids": candidate.preview_snapshot_ids,
        "risk_note_ids": candidate.risk_note_ids,
    }


def _external_ocel_validation_ref(validation: ExternalOCELValidationResult) -> dict:
    return {
        "ref_type": "external_ocel_validation_result",
        "ref_id": validation.validation_id,
        "validation_id": validation.validation_id,
        "descriptor_id": validation.descriptor_id,
        "candidate_id": validation.candidate_id,
    }


def _external_ocel_preview_ref(preview: ExternalOCELPreviewSnapshot) -> dict:
    return {
        "ref_type": "external_ocel_preview_snapshot",
        "ref_id": preview.preview_id,
        "preview_id": preview.preview_id,
        "descriptor_id": preview.descriptor_id,
        "candidate_id": preview.candidate_id,
    }


def _external_ocel_risk_ref(note: ExternalOCELImportRiskNote) -> dict:
    return {
        "ref_type": "external_ocel_import_risk_note",
        "ref_id": note.risk_note_id,
        "risk_note_id": note.risk_note_id,
        "descriptor_id": note.descriptor_id,
        "candidate_id": note.candidate_id,
    }


def _candidate_priority(candidate: ExternalAssimilationCandidate) -> int:
    if candidate.review_status == "pending_review":
        return 70
    if candidate.activation_status == "disabled":
        return 55
    return 45


def _risk_priority(note: ExternalCapabilityRiskNote) -> int:
    if note.risk_level in {"critical", "high"}:
        return 90
    if note.risk_level == "medium":
        return 75
    return 50


def _snapshot_priority(snapshot: ExternalCapabilityRegistrySnapshot) -> int:
    if snapshot.execution_enabled_candidate_count > 0:
        return 95
    if snapshot.critical_risk_count > 0 or snapshot.high_risk_count > 0:
        return 90
    if snapshot.pending_review_count > 0:
        return 70
    return 55


def _review_item_priority(item: ExternalAdapterReviewItem) -> int:
    if item.review_status == "needs_more_info":
        return 80
    if item.review_status == "rejected":
        return 75
    if item.review_status == "pending_review":
        return 70
    if item.review_status == "approved_for_design":
        return 65
    return 55


def _review_finding_priority(finding: ExternalAdapterReviewFinding) -> int:
    if finding.severity in {"critical", "high"}:
        return 90
    if finding.severity == "medium":
        return 75
    return 55


def _review_decision_priority(decision: ExternalAdapterReviewDecision) -> int:
    if decision.decision == "needs_more_info":
        return 80
    if decision.decision == "rejected":
        return 75
    if decision.decision == "approved_for_design":
        return 65
    return 55


def _skeleton_priority(skeleton: ExternalDescriptorSkeleton) -> int:
    if any(item in {"critical", "high", "external_code_execution", "credential_access"} for item in skeleton.declared_risk_categories):
        return 90
    if skeleton.review_status == "needs_more_info":
        return 80
    if skeleton.review_status == "pending_review":
        return 70
    return 45


def _skeleton_validation_priority(validation: ExternalDescriptorSkeletonValidation) -> int:
    if validation.status == "failed":
        return 90
    if validation.status == "needs_review":
        return 75
    return 50


def _external_ocel_validation_priority(validation: ExternalOCELValidationResult) -> int:
    if validation.status in {"invalid", "error"}:
        return 90
    if validation.status in {"needs_review", "valid_with_warnings"}:
        return 75
    return 50

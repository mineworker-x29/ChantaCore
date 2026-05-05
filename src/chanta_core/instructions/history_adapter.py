from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.instructions.models import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
)


SKIP_STATUSES = {"deprecated", "archived", "withdrawn"}


def instruction_artifacts_to_history_entries(
    instructions: list[InstructionArtifact],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, instruction in enumerate(instructions):
        if instruction.status in SKIP_STATUSES:
            continue
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=instruction.body,
                created_at=instruction.updated_at,
                source="instruction",
                priority=instruction.priority or 70,
                refs=[
                    {
                        "ref_type": "instruction_artifact",
                        "ref_id": instruction.instruction_id,
                        "instruction_type": instruction.instruction_type,
                        "status": instruction.status,
                        "scope": instruction.scope,
                    }
                ],
                entry_attrs={
                    "instruction_id": instruction.instruction_id,
                    "source_index": index,
                },
            )
        )
    return entries


def project_rules_to_history_entries(
    rules: list[ProjectRule],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, rule in enumerate(rules):
        if rule.status in SKIP_STATUSES:
            continue
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=rule.text,
                created_at=rule.updated_at,
                source="project_rule",
                priority=rule.priority or 75,
                refs=[
                    {
                        "ref_type": "project_rule",
                        "ref_id": rule.rule_id,
                        "rule_type": rule.rule_type,
                        "source_instruction_id": rule.source_instruction_id,
                    }
                ],
                entry_attrs={"rule_id": rule.rule_id, "source_index": index},
            )
        )
    return entries


def user_preferences_to_history_entries(
    preferences: list[UserPreference],
) -> list[ContextHistoryEntry]:
    entries: list[ContextHistoryEntry] = []
    for index, preference in enumerate(preferences):
        if preference.status in SKIP_STATUSES:
            continue
        entries.append(
            ContextHistoryEntry(
                entry_id=new_context_history_entry_id(),
                session_id=None,
                process_instance_id=None,
                role="context",
                content=f"{preference.preference_key}: {preference.preference_value}",
                created_at=preference.updated_at,
                source="user_preference",
                priority=70,
                refs=[
                    {
                        "ref_type": "user_preference",
                        "ref_id": preference.preference_id,
                        "preference_key": preference.preference_key,
                        "confidence": preference.confidence,
                    }
                ],
                entry_attrs={
                    "preference_id": preference.preference_id,
                    "source_index": index,
                },
            )
        )
    return entries

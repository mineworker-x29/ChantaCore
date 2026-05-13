from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.observation_digest.models import (
    AgentBehaviorInference,
    AgentObservationSource,
    AgentProcessNarrative,
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
    ExternalSkillStaticProfile,
    ObservedAgentRun,
    ObservationDigestionFinding,
    ObservationDigestionResult,
)


def observation_sources_to_history_entries(sources: list[AgentObservationSource]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observation source inspected: {item.source_name}\nFormat: {item.source_format}",
            created_at=item.created_at,
            priority=45 if item.source_attrs.get("status") == "available" else 70,
            refs=[{"ref_type": "agent_observation_source", "ref_id": item.source_id}],
            attrs={"source_id": item.source_id, "source_format": item.source_format},
        )
        for item in sources
    ]


def observed_runs_to_history_entries(runs: list[ObservedAgentRun]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observed agent run: {item.observed_run_id}\nEvents: {item.event_count}",
            created_at=item.created_at,
            priority=55,
            refs=[{"ref_type": "observed_agent_run", "ref_id": item.observed_run_id}],
            attrs={"observed_run_id": item.observed_run_id, "event_count": item.event_count},
        )
        for item in runs
    ]


def behavior_inferences_to_history_entries(inferences: list[AgentBehaviorInference]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Agent behavior inference: {item.inferred_task_type or 'unknown'}\nOutcome: {item.outcome_inference}",
            created_at=item.created_at,
            priority=65,
            refs=[{"ref_type": "agent_behavior_inference", "ref_id": item.inference_id}],
            attrs={"inference_id": item.inference_id, "observed_run_id": item.observed_run_id},
        )
        for item in inferences
    ]


def process_narratives_to_history_entries(narratives: list[AgentProcessNarrative]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Agent process narrative: {item.title}\n{item.concise_summary}",
            created_at=item.created_at,
            priority=55,
            refs=[{"ref_type": "agent_process_narrative", "ref_id": item.narrative_id}],
            attrs={"narrative_id": item.narrative_id, "inference_id": item.inference_id},
        )
        for item in narratives
    ]


def external_skill_profiles_to_history_entries(profiles: list[ExternalSkillStaticProfile]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"External skill static profile: {item.declared_name or item.static_profile_id}",
            created_at=item.created_at,
            priority=50,
            refs=[{"ref_type": "external_skill_static_profile", "ref_id": item.static_profile_id}],
            attrs={"static_profile_id": item.static_profile_id, "source_descriptor_id": item.source_descriptor_id},
        )
        for item in profiles
    ]


def external_skill_assimilation_candidates_to_history_entries(
    candidates: list[ExternalSkillAssimilationCandidate],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=(
                f"External skill assimilation candidate: {item.proposed_chantacore_skill_id}\n"
                f"Review: {item.review_status}"
            ),
            created_at=item.created_at,
            priority=75 if item.review_status == "pending_review" else 60,
            refs=[{"ref_type": "external_skill_assimilation_candidate", "ref_id": item.candidate_id}],
            attrs={
                "candidate_id": item.candidate_id,
                "review_status": item.review_status,
                "canonical_import_enabled": False,
                "execution_enabled": False,
            },
        )
        for item in candidates
    ]


def external_skill_adapter_candidates_to_history_entries(
    candidates: list[ExternalSkillAdapterCandidate],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"External skill adapter candidate: {item.target_skill_id}\nReview required: {item.requires_review}",
            created_at=item.created_at,
            priority=70 if item.requires_review else 55,
            refs=[{"ref_type": "external_skill_adapter_candidate", "ref_id": item.adapter_candidate_id}],
            attrs={
                "adapter_candidate_id": item.adapter_candidate_id,
                "target_skill_id": item.target_skill_id,
                "requires_review": item.requires_review,
                "execution_enabled": False,
            },
        )
        for item in candidates
    ]


def observation_digestion_findings_to_history_entries(
    findings: list[ObservationDigestionFinding],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observation/Digestion finding: {item.finding_type}\n{item.message}",
            created_at=item.created_at,
            priority=_finding_priority(item),
            refs=[{"ref_type": "observation_digestion_finding", "ref_id": item.finding_id}],
            attrs={"finding_id": item.finding_id, "severity": item.severity, "status": item.status},
        )
        for item in findings
    ]


def observation_digestion_results_to_history_entries(
    results: list[ObservationDigestionResult],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observation/Digestion result: {item.operation_kind}\n{item.summary}",
            created_at=item.created_at,
            priority=60 if item.status == "completed" else 75,
            refs=[{"ref_type": "observation_digestion_result", "ref_id": item.result_id}],
            attrs={"result_id": item.result_id, "status": item.status, "operation_kind": item.operation_kind},
        )
        for item in results
    ]


def _entry(
    *,
    content: str,
    created_at: str,
    priority: int,
    refs: list[dict],
    attrs: dict,
) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=new_context_history_entry_id(),
        session_id=None,
        process_instance_id=None,
        role="context",
        content=content,
        created_at=created_at,
        source="observation_digest",
        priority=priority,
        refs=refs,
        entry_attrs=attrs,
    )


def _finding_priority(finding: ObservationDigestionFinding) -> int:
    if finding.finding_type in {"private_content_risk", "unsupported_format"}:
        return 90
    if finding.severity in {"critical", "high"}:
        return 85
    if finding.severity == "medium":
        return 70
    return 50

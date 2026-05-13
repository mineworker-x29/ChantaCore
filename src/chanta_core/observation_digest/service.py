from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.observation_digest.ids import (
    new_agent_behavior_inference_id,
    new_agent_observation_batch_id,
    new_agent_observation_normalized_event_id,
    new_agent_observation_source_id,
    new_agent_process_narrative_id,
    new_external_skill_adapter_candidate_id,
    new_external_skill_assimilation_candidate_id,
    new_external_skill_behavior_fingerprint_id,
    new_external_skill_source_descriptor_id,
    new_external_skill_static_profile_id,
    new_observation_digestion_finding_id,
    new_observation_digestion_result_id,
    new_observed_agent_run_id,
)
from chanta_core.observation_digest.models import (
    AgentBehaviorInference,
    AgentObservationBatch,
    AgentObservationNormalizedEvent,
    AgentObservationSource,
    AgentProcessNarrative,
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
    ExternalSkillBehaviorFingerprint,
    ExternalSkillSourceDescriptor,
    ExternalSkillStaticProfile,
    ObservedAgentRun,
    ObservationDigestionFinding,
    ObservationDigestionResult,
    clamp_confidence,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import (
    WorkspacePathViolationError,
    WorkspaceReadRootError,
    resolve_workspace_path,
)


OBSERVATION_SKILL_IDS = [
    "skill:agent_observation_source_inspect",
    "skill:agent_trace_observe",
    "skill:agent_observation_normalize",
    "skill:agent_behavior_infer",
    "skill:agent_process_narrative",
]
DIGESTION_SKILL_IDS = [
    "skill:external_skill_source_inspect",
    "skill:external_skill_static_digest",
    "skill:external_behavior_fingerprint",
    "skill:external_skill_assimilate",
    "skill:external_skill_adapter_candidate",
]
OBSERVATION_DIGESTION_SKILL_IDS = OBSERVATION_SKILL_IDS + DIGESTION_SKILL_IDS

OBSERVED_ACTIVITY_TAXONOMY = {
    "user_message_observed",
    "assistant_message_observed",
    "tool_call_observed",
    "tool_result_observed",
    "skill_invocation_observed",
    "permission_observed",
    "gate_observed",
    "file_read_observed",
    "file_search_observed",
    "summary_observed",
    "error_observed",
    "outcome_observed",
    "unknown_event_observed",
}

OBSERVATION_DIGESTION_OBJECT_TYPES = [
    "agent_observation_source",
    "agent_observation_batch",
    "agent_observation_normalized_event",
    "observed_agent_run",
    "agent_behavior_inference",
    "agent_process_narrative",
    "external_skill_source_descriptor",
    "external_skill_static_profile",
    "external_skill_behavior_fingerprint",
    "external_skill_assimilation_candidate",
    "external_skill_adapter_candidate",
    "observation_digestion_finding",
    "observation_digestion_result",
]

OBSERVATION_DIGESTION_EVENT_ACTIVITIES = [
    "agent_observation_source_inspected",
    "agent_observation_batch_created",
    "agent_observation_event_normalized",
    "observed_agent_run_created",
    "agent_behavior_inference_created",
    "agent_process_narrative_created",
    "external_skill_source_inspected",
    "external_skill_static_profile_created",
    "external_skill_behavior_fingerprint_created",
    "external_skill_assimilation_candidate_created",
    "external_skill_adapter_candidate_created",
    "observation_digestion_finding_recorded",
    "observation_digestion_result_recorded",
]

OBSERVATION_DIGESTION_RELATIONS = [
    "batch_from_source",
    "normalized_event_belongs_to_batch",
    "observed_run_derived_from_batch",
    "behavior_inference_interprets_run",
    "process_narrative_summarizes_inference",
    "static_profile_derived_from_source_descriptor",
    "behavior_fingerprint_derived_from_observed_run",
    "assimilation_candidate_uses_static_profile",
    "assimilation_candidate_uses_behavior_fingerprint",
    "adapter_candidate_belongs_to_assimilation_candidate",
    "finding_belongs_to_subject",
    "result_summarizes_operation",
]

_PRIVATE_PATH_PARTS = {"letters", "messages", "archive", "souls"}


class ObservationService:
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
        self.last_source: AgentObservationSource | None = None
        self.last_batch: AgentObservationBatch | None = None
        self.last_events: list[AgentObservationNormalizedEvent] = []
        self.last_run: ObservedAgentRun | None = None
        self.last_inference: AgentBehaviorInference | None = None
        self.last_narrative: AgentProcessNarrative | None = None
        self.last_findings: list[ObservationDigestionFinding] = []
        self.last_result: ObservationDigestionResult | None = None

    def inspect_observation_source(
        self,
        *,
        root_path: str,
        relative_path: str,
        source_runtime: str = "unknown",
        format_hint: str = "generic_jsonl",
        source_name: str | None = None,
    ) -> AgentObservationSource:
        target, finding = _safe_resolve(root_path, relative_path)
        if finding is not None:
            self.last_findings.append(finding)
            self._record_model("observation_digestion_finding_recorded", "observation_digestion_finding", finding.finding_id, finding)
            location_ref = None
            status = "blocked"
            size_bytes = 0
            exists = False
        else:
            exists = target.exists()
            size_bytes = target.stat().st_size if target.exists() and target.is_file() else 0
            location_ref = _redacted_ref(relative_path)
            status = "available" if exists else "missing"
        source = AgentObservationSource(
            source_id=new_agent_observation_source_id(),
            source_name=source_name or Path(relative_path).name or "observation_source",
            source_kind="agent_trace",
            source_runtime=source_runtime,
            source_version=None,
            source_format=format_hint,
            location_ref=location_ref,
            collection_mode="read_only_inspection",
            trusted=False,
            private=False,
            created_at=utc_now_iso(),
            source_attrs={
                "status": status,
                "exists": exists,
                "size_bytes": size_bytes,
                "read_only": True,
                "full_raw_body_stored": False,
                "external_execution_used": False,
            },
        )
        self.last_source = source
        self._record_model("agent_observation_source_inspected", "agent_observation_source", source.source_id, source)
        self.record_result(
            operation_kind="agent_observation_source_inspect",
            subject_ref=source.source_id,
            status=status,
            created_object_refs=[source.source_id],
            summary=f"Observation source inspected: status={status}.",
        )
        return source

    def parse_generic_jsonl_records(self, raw_text: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for index, line in enumerate(raw_text.splitlines()):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                loaded = json.loads(stripped)
            except json.JSONDecodeError:
                records.append({"_parse_error": True, "_line_index": index, "raw_preview": stripped[:200]})
                continue
            if isinstance(loaded, dict):
                loaded.setdefault("_line_index", index)
                records.append(loaded)
            else:
                records.append({"_unsupported_record": True, "_line_index": index, "raw_type": type(loaded).__name__})
        return records

    def normalize_observation_records(
        self,
        records: list[dict[str, Any]],
        *,
        batch_id: str,
        source_runtime: str = "unknown",
        source_format: str = "generic_jsonl",
    ) -> list[AgentObservationNormalizedEvent]:
        events = [
            _normalize_record(
                record,
                batch_id=batch_id,
                source_runtime=source_runtime,
                source_format=source_format,
            )
            for record in records
        ]
        self.last_events = events
        for event in events:
            self._record_model(
                "agent_observation_event_normalized",
                "agent_observation_normalized_event",
                event.normalized_event_id,
                event,
                links=[("agent_observation_batch_object", event.batch_id)],
                object_links=[(event.normalized_event_id, event.batch_id, "normalized_event_belongs_to_batch")],
            )
        return events

    def create_observation_batch(
        self,
        *,
        source: AgentObservationSource,
        raw_record_count: int,
        normalized_events: list[AgentObservationNormalizedEvent],
        input_format: str = "generic_jsonl",
        status: str = "completed",
    ) -> AgentObservationBatch:
        confidence = _mean([event.confidence for event in normalized_events], default=0.0)
        batch = AgentObservationBatch(
            batch_id=new_agent_observation_batch_id(),
            source_id=source.source_id,
            input_format=input_format,
            raw_record_count=raw_record_count,
            normalized_event_count=len(normalized_events),
            status=status,
            confidence=confidence,
            created_at=utc_now_iso(),
            batch_attrs={
                "read_only": True,
                "full_raw_body_stored": False,
                "line_delimited_store_created": False,
            },
        )
        self.last_batch = batch
        self._record_model(
            "agent_observation_batch_created",
            "agent_observation_batch",
            batch.batch_id,
            batch,
            links=[("agent_observation_source_object", source.source_id)],
            object_links=[(batch.batch_id, source.source_id, "batch_from_source")],
        )
        return batch

    def create_observed_run(
        self,
        *,
        source: AgentObservationSource,
        batch: AgentObservationBatch,
        normalized_events: list[AgentObservationNormalizedEvent],
        source_agent_id: str | None = None,
        source_session_id: str | None = None,
    ) -> "ObservedAgentRun":
        object_refs = {ref for event in normalized_events for ref in event.object_refs}
        run = ObservedAgentRun(
            observed_run_id=new_observed_agent_run_id(),
            source_id=source.source_id,
            batch_id=batch.batch_id,
            source_agent_id=source_agent_id,
            source_session_id=source_session_id or _first_event_attr(normalized_events, "session_id"),
            inferred_runtime=source.source_runtime,
            event_count=len(normalized_events),
            object_count=len(object_refs),
            relation_count=len(normalized_events) + len(object_refs),
            observation_confidence=_mean([event.confidence for event in normalized_events], default=batch.confidence),
            created_at=utc_now_iso(),
            run_attrs={
                "observed_activity_sequence": [event.observed_activity for event in normalized_events],
                "read_only": True,
            },
        )
        self.last_run = run
        self._record_model(
            "observed_agent_run_created",
            "observed_agent_run",
            run.observed_run_id,
            run,
            links=[
                ("agent_observation_source_object", source.source_id),
                ("agent_observation_batch_object", batch.batch_id),
            ],
            object_links=[(run.observed_run_id, batch.batch_id, "observed_run_derived_from_batch")],
        )
        return run

    def infer_behavior(
        self,
        *,
        observed_run: "ObservedAgentRun",
        normalized_events: list[AgentObservationNormalizedEvent] | None = None,
    ) -> AgentBehaviorInference:
        events = list(normalized_events or self.last_events)
        sequence = [event.observed_activity for event in events]
        tool_sequence = _event_names(events, "tool_name")
        skill_sequence = _event_names(events, "skill_id")
        failures = [event.observed_activity for event in events if event.observed_activity == "error_observed"]
        outcome = "failed_or_blocked" if failures else "observed_without_explicit_failure"
        inferred_goal = _infer_goal(sequence)
        inference = AgentBehaviorInference(
            inference_id=new_agent_behavior_inference_id(),
            observed_run_id=observed_run.observed_run_id,
            inferred_goal=inferred_goal,
            inferred_goal_confidence=0.55 if inferred_goal else 0.25,
            inferred_task_type=_infer_task_type(sequence),
            inferred_action_sequence=sequence,
            inferred_skill_sequence=skill_sequence,
            inferred_tool_sequence=tool_sequence,
            touched_object_types=sorted({ref.split(":", 1)[0] for event in events for ref in event.object_refs if ":" in ref}),
            outcome_inference=outcome,
            outcome_confidence=0.65 if events else 0.0,
            confirmed_observations=[
                f"{event.observed_activity} at {event.observed_timestamp or 'unknown_time'}"
                for event in events
            ],
            data_based_interpretations=[
                f"Observed {len(events)} normalized events from runtime {observed_run.inferred_runtime}.",
                f"Observed sequence contains {len(set(sequence))} distinct activity types.",
            ],
            likely_hypotheses=[
                "The run reflects an agent or harness interaction trace, but intent is inferred from event order only."
            ],
            estimates=[
                f"event_count_estimate={observed_run.event_count}",
                f"object_count_estimate={observed_run.object_count}",
            ],
            unknown_or_needs_verification=[
                "Original harness semantics are not verified.",
                "User goal is inferred unless explicitly present in observed rows.",
            ],
            failure_signals=failures,
            recovery_signals=[activity for activity in sequence if activity in {"tool_result_observed", "outcome_observed"}],
            evidence_refs=[event.evidence_ref for event in events if event.evidence_ref],
            uncertainty_notes=[
                "No LLM call was used for inference.",
                "Inference is deterministic and should be reviewed before promotion.",
            ],
            withdrawal_conditions=[
                "Withdraw if source rows are incomplete, synthetic, or mapped to the wrong runtime format.",
                "Withdraw if external evidence contradicts the observed event ordering.",
            ],
            created_at=utc_now_iso(),
            inference_attrs={
                "read_only": True,
                "llm_called": False,
                "external_execution_used": False,
            },
        )
        self.last_inference = inference
        self._record_model(
            "agent_behavior_inference_created",
            "agent_behavior_inference",
            inference.inference_id,
            inference,
            links=[("observed_agent_run_object", observed_run.observed_run_id)],
            object_links=[(inference.inference_id, observed_run.observed_run_id, "behavior_inference_interprets_run")],
        )
        return inference

    def create_process_narrative(
        self,
        *,
        observed_run: "ObservedAgentRun",
        inference: AgentBehaviorInference,
    ) -> AgentProcessNarrative:
        key_actions = inference.inferred_action_sequence[:10]
        narrative = AgentProcessNarrative(
            narrative_id=new_agent_process_narrative_id(),
            observed_run_id=observed_run.observed_run_id,
            inference_id=inference.inference_id,
            title=f"Observed agent process: {inference.inferred_task_type or 'unknown'}",
            concise_summary=(
                f"Observed {observed_run.event_count} events. "
                f"Outcome inference: {inference.outcome_inference or 'unknown'}."
            ),
            timeline=[f"{index + 1}. {activity}" for index, activity in enumerate(key_actions)],
            key_actions=key_actions,
            key_objects=inference.touched_object_types,
            blocked_or_failed_steps=inference.failure_signals,
            inferred_outcome=inference.outcome_inference,
            confidence=min(inference.inferred_goal_confidence, inference.outcome_confidence),
            created_at=utc_now_iso(),
            narrative_attrs={"read_only": True, "llm_called": False},
        )
        self.last_narrative = narrative
        self._record_model(
            "agent_process_narrative_created",
            "agent_process_narrative",
            narrative.narrative_id,
            narrative,
            links=[
                ("observed_agent_run_object", observed_run.observed_run_id),
                ("agent_behavior_inference_object", inference.inference_id),
            ],
            object_links=[
                (narrative.narrative_id, inference.inference_id, "process_narrative_summarizes_inference"),
                (narrative.narrative_id, observed_run.observed_run_id, "process_narrative_summarizes_run"),
            ],
        )
        return narrative

    def record_finding(
        self,
        *,
        subject_ref: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionFinding:
        finding = _finding(
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            finding_attrs=finding_attrs,
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digestion_finding_recorded",
            "observation_digestion_finding",
            finding.finding_id,
            finding,
            links=[("subject_object", subject_ref or "")],
            object_links=[(finding.finding_id, subject_ref or "", "finding_belongs_to_subject")],
        )
        return finding

    def record_result(
        self,
        *,
        operation_kind: str,
        subject_ref: str | None,
        status: str,
        created_object_refs: list[str],
        summary: str,
        findings: list[ObservationDigestionFinding] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionResult:
        active_findings = list(findings or self.last_findings)
        result = ObservationDigestionResult(
            result_id=new_observation_digestion_result_id(),
            operation_kind=operation_kind,
            subject_ref=subject_ref,
            status=status,
            created_object_refs=list(created_object_refs),
            finding_ids=[finding.finding_id for finding in active_findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "external_execution_used": False,
                "llm_called": False,
                "full_raw_body_stored": False,
                **dict(result_attrs or {}),
            },
        )
        self.last_result = result
        self._record_model(
            "observation_digestion_result_recorded",
            "observation_digestion_result",
            result.result_id,
            result,
            links=[("subject_object", subject_ref or "")]
            + [("created_object", item) for item in created_object_refs]
            + [("finding_object", item.finding_id) for item in active_findings],
            object_links=[(result.result_id, subject_ref or "", "result_summarizes_operation")],
        )
        return result

    def render_observation_cli(self, value: Any | None = None) -> str:
        item = value or self.last_result or self.last_run or self.last_source
        if item is None:
            return "Observation: unavailable"
        data = item.to_dict() if hasattr(item, "to_dict") else dict(item)
        lines = ["Observation"]
        attrs = (
            data.get("source_attrs")
            or data.get("batch_attrs")
            or data.get("run_attrs")
            or data.get("inference_attrs")
            or data.get("narrative_attrs")
            or {}
        )
        if data.get("status") is None and attrs.get("status") is not None:
            lines.append(f"status={attrs['status']}")
        for key in [
            "status",
            "source_id",
            "batch_id",
            "observed_run_id",
            "inference_id",
            "narrative_id",
            "raw_record_count",
            "normalized_event_count",
            "event_count",
            "summary",
        ]:
            if data.get(key) is not None:
                lines.append(f"{key}={data[key]}")
        if data.get("normalized_event_count") is None and self.last_batch is not None:
            lines.append(f"normalized_event_count={self.last_batch.normalized_event_count}")
        lines.append("read_only=true")
        lines.append("full_raw_body_stored=false")
        lines.append("external_execution_used=false")
        return "\n".join(lines)

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        _record(
            self.trace_service,
            activity,
            objects=[_object(object_type, object_id, model.to_dict())],
            links=[(f"{object_type}_object", object_id), *(links or [])],
            object_links=object_links or [],
        )


class DigestionService:
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
        self.last_source_descriptor: ExternalSkillSourceDescriptor | None = None
        self.last_static_profile: ExternalSkillStaticProfile | None = None
        self.last_fingerprint: ExternalSkillBehaviorFingerprint | None = None
        self.last_candidate: ExternalSkillAssimilationCandidate | None = None
        self.last_adapter_candidate: ExternalSkillAdapterCandidate | None = None
        self.last_findings: list[ObservationDigestionFinding] = []
        self.last_result: ObservationDigestionResult | None = None

    def inspect_external_skill_source(
        self,
        *,
        root_path: str,
        relative_path: str,
        vendor_hint: str | None = None,
    ) -> ExternalSkillSourceDescriptor:
        target, finding = _safe_resolve(root_path, relative_path)
        detected_files: list[str] = []
        manifests: list[str] = []
        status = "available"
        if finding is not None:
            self.last_findings.append(finding)
            self._record_model("observation_digestion_finding_recorded", "observation_digestion_finding", finding.finding_id, finding)
            status = "blocked"
        elif not target.exists():
            status = "missing"
        elif target.is_file():
            detected_files = [Path(relative_path).name]
            manifests = detected_files if Path(relative_path).name in {"SKILL.md", "plugin.json", "manifest.json"} else []
        else:
            for child in sorted(target.iterdir(), key=lambda item: item.name):
                if child.is_file():
                    detected_files.append(child.name)
                    if child.name in {"SKILL.md", "plugin.json", "manifest.json", "package.json"}:
                        manifests.append(child.name)
        descriptor = ExternalSkillSourceDescriptor(
            source_descriptor_id=new_external_skill_source_descriptor_id(),
            source_kind="external_skill_source",
            source_runtime="unknown",
            vendor_hint=vendor_hint,
            source_root_ref=_redacted_ref(relative_path) if status != "blocked" else None,
            detected_files=detected_files,
            detected_manifest_refs=manifests,
            confidence=0.8 if manifests else 0.45 if detected_files else 0.1,
            created_at=utc_now_iso(),
            descriptor_attrs={
                "status": status,
                "read_only": True,
                "full_raw_body_stored": False,
                "external_execution_used": False,
            },
        )
        self.last_source_descriptor = descriptor
        self._record_model(
            "external_skill_source_inspected",
            "external_skill_source_descriptor",
            descriptor.source_descriptor_id,
            descriptor,
        )
        self.record_result(
            operation_kind="external_skill_source_inspect",
            subject_ref=descriptor.source_descriptor_id,
            status=status,
            created_object_refs=[descriptor.source_descriptor_id],
            summary=f"External skill source inspected: files={len(detected_files)} manifests={len(manifests)}.",
        )
        return descriptor

    def create_static_profile(
        self,
        *,
        source_descriptor: ExternalSkillSourceDescriptor,
        root_path: str | None = None,
        relative_path: str | None = None,
    ) -> ExternalSkillStaticProfile:
        raw = ""
        source_ref = relative_path
        if root_path and relative_path:
            target, finding = _safe_resolve(root_path, relative_path)
            if finding is not None:
                self.last_findings.append(finding)
                self._record_model("observation_digestion_finding_recorded", "observation_digestion_finding", finding.finding_id, finding)
            elif target.exists() and target.is_file():
                raw = _read_text_preview(target, max_chars=4000)
            elif target.exists() and target.is_dir():
                skill_file = target / "SKILL.md"
                if skill_file.exists() and skill_file.is_file():
                    source_ref = str(Path(relative_path) / "SKILL.md")
                    raw = _read_text_preview(skill_file, max_chars=4000)
        profile = ExternalSkillStaticProfile(
            static_profile_id=new_external_skill_static_profile_id(),
            source_descriptor_id=source_descriptor.source_descriptor_id,
            declared_name=_extract_declared_name(raw, source_ref),
            declared_description=_extract_description(raw),
            declared_tools=_extract_list_like(raw, ["tool", "tools"]),
            declared_inputs=_extract_list_like(raw, ["input", "inputs", "parameters"]),
            declared_outputs=_extract_list_like(raw, ["output", "outputs", "returns"]),
            declared_risks=_extract_risks(raw),
            instruction_preview=_preview_text(raw, 600) if raw else None,
            confidence=0.75 if raw else 0.35,
            created_at=utc_now_iso(),
            profile_attrs={
                "source_ref": _redacted_ref(source_ref or ""),
                "content_hash": _hash_text(raw) if raw else None,
                "full_raw_body_stored": False,
                "read_only": True,
                "external_execution_used": False,
            },
        )
        self.last_static_profile = profile
        self._record_model(
            "external_skill_static_profile_created",
            "external_skill_static_profile",
            profile.static_profile_id,
            profile,
            links=[("external_skill_source_descriptor_object", source_descriptor.source_descriptor_id)],
            object_links=[
                (
                    profile.static_profile_id,
                    source_descriptor.source_descriptor_id,
                    "static_profile_derived_from_source_descriptor",
                )
            ],
        )
        return profile

    def create_behavior_fingerprint(
        self,
        *,
        observed_run: "ObservedAgentRun",
        normalized_events: list[AgentObservationNormalizedEvent] | None = None,
    ) -> ExternalSkillBehaviorFingerprint:
        events = list(normalized_events or [])
        sequence = [event.observed_activity for event in events] or list(observed_run.run_attrs.get("observed_activity_sequence") or [])
        risk_class = "read_only"
        side_effect_profile = "none_observed"
        if any(activity in {"file_read_observed", "file_search_observed"} for activity in sequence):
            risk_class = "read_only"
            side_effect_profile = "filesystem_read_observed"
        if any(activity == "error_observed" for activity in sequence):
            risk_class = "medium"
        fingerprint = ExternalSkillBehaviorFingerprint(
            fingerprint_id=new_external_skill_behavior_fingerprint_id(),
            observed_run_id=observed_run.observed_run_id,
            source_runtime=observed_run.inferred_runtime,
            source_skill_name=_first_event_attr(events, "skill_id"),
            source_tool_name=_first_event_attr(events, "tool_name"),
            observed_event_count=observed_run.event_count,
            observed_sequence=sequence,
            object_types_touched=sorted({ref.split(":", 1)[0] for event in events for ref in event.object_refs if ":" in ref}),
            input_shape_summary=_shape_summary([event.input_preview for event in events if event.input_preview]),
            output_shape_summary=_shape_summary([event.output_preview for event in events if event.output_preview]),
            side_effect_profile=side_effect_profile,
            permission_profile="permission_not_observed",
            verification_profile="deterministic_static_fingerprint",
            failure_modes=[activity for activity in sequence if activity == "error_observed"],
            recovery_patterns=[activity for activity in sequence if activity in {"tool_result_observed", "outcome_observed"}],
            recommended_chantacore_category="observation" if "observed" in " ".join(sequence) else "read_only",
            risk_class=risk_class,
            confidence=0.65 if sequence else 0.2,
            evidence_refs=[event.evidence_ref for event in events if event.evidence_ref],
            created_at=utc_now_iso(),
            fingerprint_attrs={
                "read_only": True,
                "external_execution_used": False,
                "llm_called": False,
            },
        )
        self.last_fingerprint = fingerprint
        self._record_model(
            "external_skill_behavior_fingerprint_created",
            "external_skill_behavior_fingerprint",
            fingerprint.fingerprint_id,
            fingerprint,
            links=[("observed_agent_run_object", observed_run.observed_run_id)],
            object_links=[
                (
                    fingerprint.fingerprint_id,
                    observed_run.observed_run_id,
                    "behavior_fingerprint_derived_from_observed_run",
                )
            ],
        )
        return fingerprint

    def create_assimilation_candidate(
        self,
        *,
        static_profile: ExternalSkillStaticProfile | None = None,
        behavior_fingerprint: ExternalSkillBehaviorFingerprint | None = None,
        source_runtime: str = "unknown",
        source_skill_ref: str | None = None,
    ) -> ExternalSkillAssimilationCandidate:
        name = static_profile.declared_name if static_profile else source_skill_ref
        normalized_name = _skill_id_tail(name or "external_skill_candidate")
        risk_class = behavior_fingerprint.risk_class if behavior_fingerprint else "unknown"
        candidate = ExternalSkillAssimilationCandidate(
            candidate_id=new_external_skill_assimilation_candidate_id(),
            source_runtime=source_runtime,
            source_skill_ref=source_skill_ref or name,
            source_kind="external_skill",
            static_profile_id=static_profile.static_profile_id if static_profile else None,
            behavior_fingerprint_id=behavior_fingerprint.fingerprint_id if behavior_fingerprint else None,
            proposed_chantacore_skill_id=f"skill:{normalized_name}",
            proposed_execution_type="review_only_candidate",
            adapter_candidate_ids=[],
            risk_class=risk_class,
            confidence=min(
                static_profile.confidence if static_profile else 0.35,
                behavior_fingerprint.confidence if behavior_fingerprint else 0.35,
            ),
            evidence_refs=[
                *(behavior_fingerprint.evidence_refs if behavior_fingerprint else []),
                *(["static_profile:" + static_profile.static_profile_id] if static_profile else []),
            ],
            review_status="pending_review",
            canonical_import_enabled=False,
            execution_enabled=False,
            created_at=utc_now_iso(),
            candidate_attrs={
                "read_only": True,
                "runtime_registered": False,
                "permission_grants_created": False,
                "external_execution_used": False,
            },
        )
        self.last_candidate = candidate
        object_links = []
        links = []
        if static_profile is not None:
            links.append(("external_skill_static_profile_object", static_profile.static_profile_id))
            object_links.append((candidate.candidate_id, static_profile.static_profile_id, "assimilation_candidate_uses_static_profile"))
        if behavior_fingerprint is not None:
            links.append(("external_skill_behavior_fingerprint_object", behavior_fingerprint.fingerprint_id))
            object_links.append(
                (
                    candidate.candidate_id,
                    behavior_fingerprint.fingerprint_id,
                    "assimilation_candidate_uses_behavior_fingerprint",
                )
            )
        self._record_model(
            "external_skill_assimilation_candidate_created",
            "external_skill_assimilation_candidate",
            candidate.candidate_id,
            candidate,
            links=links,
            object_links=object_links,
        )
        return candidate

    def create_adapter_candidate(
        self,
        *,
        candidate: ExternalSkillAssimilationCandidate,
        target_skill_id: str | None = None,
    ) -> ExternalSkillAdapterCandidate:
        adapter = ExternalSkillAdapterCandidate(
            adapter_candidate_id=new_external_skill_adapter_candidate_id(),
            source_skill_ref=candidate.source_skill_ref,
            target_skill_id=target_skill_id or candidate.proposed_chantacore_skill_id,
            mapping_type="static_review_candidate",
            mapping_confidence=min(candidate.confidence, 0.6),
            required_input_mapping={},
            output_mapping={},
            unsupported_features=["execution", "side_effects", "automatic_import"],
            requires_review=True,
            execution_enabled=False,
            created_at=utc_now_iso(),
            adapter_attrs={
                "candidate_id": candidate.candidate_id,
                "read_only": True,
                "runtime_registered": False,
                "external_execution_used": False,
            },
        )
        self.last_adapter_candidate = adapter
        updated_candidate = ExternalSkillAssimilationCandidate(
            **{
                **candidate.to_dict(),
                "adapter_candidate_ids": [*candidate.adapter_candidate_ids, adapter.adapter_candidate_id],
            }
        )
        self.last_candidate = updated_candidate
        self._record_model(
            "external_skill_adapter_candidate_created",
            "external_skill_adapter_candidate",
            adapter.adapter_candidate_id,
            adapter,
            links=[("external_skill_assimilation_candidate_object", candidate.candidate_id)],
            object_links=[
                (
                    adapter.adapter_candidate_id,
                    candidate.candidate_id,
                    "adapter_candidate_belongs_to_assimilation_candidate",
                )
            ],
        )
        return adapter

    def record_finding(
        self,
        *,
        subject_ref: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionFinding:
        finding = _finding(
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            finding_attrs=finding_attrs,
        )
        self.last_findings.append(finding)
        self._record_model("observation_digestion_finding_recorded", "observation_digestion_finding", finding.finding_id, finding)
        return finding

    def record_result(
        self,
        *,
        operation_kind: str,
        subject_ref: str | None,
        status: str,
        created_object_refs: list[str],
        summary: str,
        findings: list[ObservationDigestionFinding] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionResult:
        active_findings = list(findings or self.last_findings)
        result = ObservationDigestionResult(
            result_id=new_observation_digestion_result_id(),
            operation_kind=operation_kind,
            subject_ref=subject_ref,
            status=status,
            created_object_refs=list(created_object_refs),
            finding_ids=[finding.finding_id for finding in active_findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "canonical_import_enabled": False,
                "execution_enabled": False,
                "external_execution_used": False,
                "llm_called": False,
                "full_raw_body_stored": False,
                **dict(result_attrs or {}),
            },
        )
        self.last_result = result
        self._record_model(
            "observation_digestion_result_recorded",
            "observation_digestion_result",
            result.result_id,
            result,
        )
        return result

    def render_digestion_cli(self, value: Any | None = None) -> str:
        item = value or self.last_result or self.last_candidate or self.last_static_profile or self.last_source_descriptor
        if item is None:
            return "Digestion: unavailable"
        data = item.to_dict() if hasattr(item, "to_dict") else dict(item)
        lines = ["Digestion"]
        attrs = (
            data.get("descriptor_attrs")
            or data.get("profile_attrs")
            or data.get("fingerprint_attrs")
            or data.get("candidate_attrs")
            or data.get("adapter_attrs")
            or {}
        )
        if data.get("status") is None and attrs.get("status") is not None:
            lines.append(f"status={attrs['status']}")
        for key in [
            "status",
            "source_descriptor_id",
            "static_profile_id",
            "fingerprint_id",
            "candidate_id",
            "adapter_candidate_id",
            "review_status",
            "summary",
        ]:
            if data.get(key) is not None:
                lines.append(f"{key}={data[key]}")
        lines.append("read_only=true")
        lines.append("full_raw_body_stored=false")
        lines.append("canonical_import_enabled=false")
        lines.append("execution_enabled=false")
        lines.append("external_execution_used=false")
        return "\n".join(lines)

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        _record(
            self.trace_service,
            activity,
            objects=[_object(object_type, object_id, model.to_dict())],
            links=[(f"{object_type}_object", object_id), *(links or [])],
            object_links=object_links or [],
        )


def observed_run_from_dict(value: dict[str, Any]) -> ObservedAgentRun:
    from chanta_core.observation_digest.models import ObservedAgentRun

    return ObservedAgentRun(
        observed_run_id=str(value.get("observed_run_id") or new_observed_agent_run_id()),
        source_id=str(value.get("source_id") or ""),
        batch_id=str(value.get("batch_id") or ""),
        source_agent_id=value.get("source_agent_id"),
        source_session_id=value.get("source_session_id"),
        inferred_runtime=str(value.get("inferred_runtime") or "unknown"),
        event_count=int(value.get("event_count") or 0),
        object_count=int(value.get("object_count") or 0),
        relation_count=int(value.get("relation_count") or 0),
        observation_confidence=clamp_confidence(value.get("observation_confidence")),
        created_at=str(value.get("created_at") or utc_now_iso()),
        run_attrs=dict(value.get("run_attrs") or {}),
    )


def static_profile_from_dict(value: dict[str, Any]) -> ExternalSkillStaticProfile:
    return ExternalSkillStaticProfile(
        static_profile_id=str(value.get("static_profile_id") or new_external_skill_static_profile_id()),
        source_descriptor_id=str(value.get("source_descriptor_id") or ""),
        declared_name=value.get("declared_name"),
        declared_description=value.get("declared_description"),
        declared_tools=[str(item) for item in value.get("declared_tools") or []],
        declared_inputs=[str(item) for item in value.get("declared_inputs") or []],
        declared_outputs=[str(item) for item in value.get("declared_outputs") or []],
        declared_risks=[str(item) for item in value.get("declared_risks") or []],
        instruction_preview=value.get("instruction_preview"),
        confidence=clamp_confidence(value.get("confidence")),
        created_at=str(value.get("created_at") or utc_now_iso()),
        profile_attrs=dict(value.get("profile_attrs") or {}),
    )


def fingerprint_from_dict(value: dict[str, Any]) -> ExternalSkillBehaviorFingerprint:
    return ExternalSkillBehaviorFingerprint(
        fingerprint_id=str(value.get("fingerprint_id") or new_external_skill_behavior_fingerprint_id()),
        observed_run_id=str(value.get("observed_run_id") or ""),
        source_runtime=str(value.get("source_runtime") or "unknown"),
        source_skill_name=value.get("source_skill_name"),
        source_tool_name=value.get("source_tool_name"),
        observed_event_count=int(value.get("observed_event_count") or 0),
        observed_sequence=[str(item) for item in value.get("observed_sequence") or []],
        object_types_touched=[str(item) for item in value.get("object_types_touched") or []],
        input_shape_summary=dict(value.get("input_shape_summary") or {}),
        output_shape_summary=dict(value.get("output_shape_summary") or {}),
        side_effect_profile=str(value.get("side_effect_profile") or "unknown"),
        permission_profile=str(value.get("permission_profile") or "unknown"),
        verification_profile=str(value.get("verification_profile") or "unknown"),
        failure_modes=[str(item) for item in value.get("failure_modes") or []],
        recovery_patterns=[str(item) for item in value.get("recovery_patterns") or []],
        recommended_chantacore_category=str(value.get("recommended_chantacore_category") or "read_only"),
        risk_class=str(value.get("risk_class") or "unknown"),
        confidence=clamp_confidence(value.get("confidence")),
        evidence_refs=[str(item) for item in value.get("evidence_refs") or []],
        created_at=str(value.get("created_at") or utc_now_iso()),
        fingerprint_attrs=dict(value.get("fingerprint_attrs") or {}),
    )


def candidate_from_dict(value: dict[str, Any]) -> ExternalSkillAssimilationCandidate:
    return ExternalSkillAssimilationCandidate(
        candidate_id=str(value.get("candidate_id") or new_external_skill_assimilation_candidate_id()),
        source_runtime=str(value.get("source_runtime") or "unknown"),
        source_skill_ref=value.get("source_skill_ref"),
        source_kind=str(value.get("source_kind") or "external_skill"),
        static_profile_id=value.get("static_profile_id"),
        behavior_fingerprint_id=value.get("behavior_fingerprint_id"),
        proposed_chantacore_skill_id=str(value.get("proposed_chantacore_skill_id") or "skill:external_skill_candidate"),
        proposed_execution_type=str(value.get("proposed_execution_type") or "review_only_candidate"),
        adapter_candidate_ids=[str(item) for item in value.get("adapter_candidate_ids") or []],
        risk_class=str(value.get("risk_class") or "unknown"),
        confidence=clamp_confidence(value.get("confidence")),
        evidence_refs=[str(item) for item in value.get("evidence_refs") or []],
        review_status=str(value.get("review_status") or "pending_review"),
        canonical_import_enabled=bool(value.get("canonical_import_enabled", False)),
        execution_enabled=bool(value.get("execution_enabled", False)),
        created_at=str(value.get("created_at") or utc_now_iso()),
        candidate_attrs=dict(value.get("candidate_attrs") or {}),
    )


def inference_from_dict(value: dict[str, Any]) -> AgentBehaviorInference:
    return AgentBehaviorInference(
        inference_id=str(value.get("inference_id") or new_agent_behavior_inference_id()),
        observed_run_id=str(value.get("observed_run_id") or ""),
        inferred_goal=value.get("inferred_goal"),
        inferred_goal_confidence=clamp_confidence(value.get("inferred_goal_confidence")),
        inferred_task_type=value.get("inferred_task_type"),
        inferred_action_sequence=[str(item) for item in value.get("inferred_action_sequence") or []],
        inferred_skill_sequence=[str(item) for item in value.get("inferred_skill_sequence") or []],
        inferred_tool_sequence=[str(item) for item in value.get("inferred_tool_sequence") or []],
        touched_object_types=[str(item) for item in value.get("touched_object_types") or []],
        outcome_inference=value.get("outcome_inference"),
        outcome_confidence=clamp_confidence(value.get("outcome_confidence")),
        confirmed_observations=[str(item) for item in value.get("confirmed_observations") or []],
        data_based_interpretations=[str(item) for item in value.get("data_based_interpretations") or []],
        likely_hypotheses=[str(item) for item in value.get("likely_hypotheses") or []],
        estimates=[str(item) for item in value.get("estimates") or []],
        unknown_or_needs_verification=[str(item) for item in value.get("unknown_or_needs_verification") or []],
        failure_signals=[str(item) for item in value.get("failure_signals") or []],
        recovery_signals=[str(item) for item in value.get("recovery_signals") or []],
        evidence_refs=[str(item) for item in value.get("evidence_refs") or []],
        uncertainty_notes=[str(item) for item in value.get("uncertainty_notes") or []],
        withdrawal_conditions=[str(item) for item in value.get("withdrawal_conditions") or []],
        created_at=str(value.get("created_at") or utc_now_iso()),
        inference_attrs=dict(value.get("inference_attrs") or {}),
    )


def _normalize_record(
    record: dict[str, Any],
    *,
    batch_id: str,
    source_runtime: str,
    source_format: str,
) -> AgentObservationNormalizedEvent:
    activity, confidence, notes = _activity_for_record(record)
    timestamp = _first_string(record, ["timestamp", "created_at", "time"])
    source_event_id = _first_string(record, ["event_id", "id", "_line_index"])
    role = _first_string(record, ["role", "actor_type"])
    actor_type = role or _first_string(record, ["actor"])
    actor_ref = _first_string(record, ["actor_ref", "agent_id", "user_id"])
    object_refs = _object_refs_for_record(record)
    input_preview = _preview_text(_first_string(record, ["input", "prompt", "arguments", "args", "content"]), 240)
    output_preview = _preview_text(_first_string(record, ["output", "result", "response", "content"]), 240)
    return AgentObservationNormalizedEvent(
        normalized_event_id=new_agent_observation_normalized_event_id(),
        batch_id=batch_id,
        source_event_id=str(source_event_id) if source_event_id is not None else None,
        source_runtime=source_runtime,
        source_format=source_format,
        observed_activity=activity,
        observed_timestamp=timestamp,
        actor_type=actor_type,
        actor_ref=actor_ref,
        object_refs=object_refs,
        input_preview=input_preview,
        output_preview=output_preview,
        confidence=confidence,
        evidence_ref=f"record:{source_event_id}" if source_event_id is not None else None,
        uncertainty_notes=notes,
        created_at=utc_now_iso(),
        event_attrs={
            "raw_keys": sorted(str(key) for key in record.keys())[:40],
            "session_id": _first_string(record, ["session_id", "conversation_id"]),
            "tool_name": _first_string(record, ["tool", "tool_name", "name"]),
            "skill_id": _first_string(record, ["skill_id"]),
            "read_only": True,
            "full_raw_body_stored": False,
        },
    )


def _activity_for_record(record: dict[str, Any]) -> tuple[str, float, list[str]]:
    notes: list[str] = []
    if record.get("_parse_error"):
        return "error_observed", 0.7, ["JSONL row could not be parsed."]
    if record.get("error") is not None:
        return "error_observed", 0.9, []
    role = str(record.get("role") or "").casefold()
    if role == "user":
        return "user_message_observed", 0.95, []
    if role == "assistant":
        return "assistant_message_observed", 0.95, []
    keys = {str(key).casefold() for key in record}
    if keys & {"tool_result", "result", "output"}:
        return "tool_result_observed", 0.85, []
    if keys & {"tool", "tool_call", "tool_name", "name"}:
        return "tool_call_observed", 0.85, []
    if "skill_id" in keys:
        return "skill_invocation_observed", 0.85, []
    if "permission" in keys:
        return "permission_observed", 0.8, []
    if "gate" in keys:
        return "gate_observed", 0.8, []
    if "summary" in keys:
        return "summary_observed", 0.75, []
    notes.append("No known event marker matched the minimal taxonomy.")
    return "unknown_event_observed", 0.25, notes


def _safe_resolve(root_path: str, relative_path: str) -> tuple[Path, ObservationDigestionFinding | None]:
    lowered_parts = {part.casefold() for part in Path(relative_path).parts}
    if lowered_parts & _PRIVATE_PATH_PARTS:
        return Path(root_path), _finding(
            subject_ref=_redacted_ref(relative_path),
            finding_type="private_content_risk",
            status="blocked",
            severity="high",
            message="Path appears to target private message, letter, or archive material.",
            evidence_ref=None,
        )
    try:
        return resolve_workspace_path(root_path, relative_path), None
    except WorkspaceReadRootError as error:
        return Path(root_path), _finding(
            subject_ref=_redacted_ref(relative_path),
            finding_type="workspace_root_invalid",
            status="blocked",
            severity="high",
            message=str(error),
            evidence_ref=None,
        )
    except WorkspacePathViolationError as error:
        message = str(error)
        finding_type = "workspace_boundary_violation"
        folded = message.casefold()
        if "traversal" in folded:
            finding_type = "path_traversal"
        elif "absolute" in folded:
            finding_type = "absolute_path_not_allowed"
        elif "outside" in folded:
            finding_type = "outside_workspace"
        return Path(root_path), _finding(
            subject_ref=_redacted_ref(relative_path),
            finding_type=finding_type,
            status="blocked",
            severity="high",
            message=message,
            evidence_ref=None,
        )


def _finding(
    *,
    subject_ref: str | None,
    finding_type: str,
    status: str,
    severity: str,
    message: str,
    evidence_ref: str | None,
    finding_attrs: dict[str, Any] | None = None,
) -> ObservationDigestionFinding:
    return ObservationDigestionFinding(
        finding_id=new_observation_digestion_finding_id(),
        subject_ref=subject_ref,
        finding_type=finding_type,
        status=status,
        severity=severity,
        message=message,
        evidence_ref=evidence_ref,
        created_at=utc_now_iso(),
        finding_attrs={
            "read_only": True,
            "external_execution_used": False,
            "llm_called": False,
            **dict(finding_attrs or {}),
        },
    )


def _record(
    trace_service: TraceService,
    activity: str,
    *,
    objects: list[OCELObject],
    links: list[tuple[str, str]],
    object_links: list[tuple[str, str, str]],
) -> None:
    event = OCELEvent(
        event_id=f"evt:{uuid4()}",
        event_activity=activity,
        event_timestamp=utc_now_iso(),
        event_attrs={
            "runtime_event_type": activity,
            "source_runtime": "chanta_core",
            "observation_digest": True,
            "read_only": True,
            "external_execution_used": False,
            "external_harness_execution_used": False,
            "external_script_execution_used": False,
            "workspace_mutation_used": False,
            "shell_execution_used": False,
            "network_access_used": False,
            "mcp_connection_used": False,
            "plugin_loaded": False,
            "llm_called": False,
            "canonical_import_enabled": False,
            "execution_enabled": False,
            "full_raw_body_stored": False,
            "line_delimited_store_created": False,
        },
    )
    relations = [
        OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
        for qualifier, object_id in links
        if object_id
    ]
    relations.extend(
        OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
        for source_id, target_id, qualifier in object_links
        if source_id and target_id
    )
    trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )


def _read_text_preview(path: Path, *, max_chars: int) -> str:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    return text[:max_chars]


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _preview_text(value: Any, max_chars: int) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    else:
        text = str(value)
    return " ".join(text.split())[:max_chars]


def _redacted_ref(path: str) -> str:
    if not path:
        return "<root>"
    return str(Path(path).name or "<path>")


def _first_string(record: dict[str, Any], keys: list[str]) -> str | None:
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
        return str(value)
    return None


def _object_refs_for_record(record: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for key in ["file", "path", "relative_path", "tool", "tool_name", "skill_id", "object_id"]:
        value = record.get(key)
        if value:
            refs.append(f"{key}:{value}")
    return refs


def _mean(values: list[float], *, default: float) -> float:
    if not values:
        return default
    return clamp_confidence(sum(values) / len(values))


def _first_event_attr(events: list[AgentObservationNormalizedEvent], key: str) -> str | None:
    for event in events:
        value = event.event_attrs.get(key)
        if value:
            return str(value)
    return None


def _event_names(events: list[AgentObservationNormalizedEvent], key: str) -> list[str]:
    names: list[str] = []
    for event in events:
        value = event.event_attrs.get(key)
        if value:
            names.append(str(value))
    return names


def _infer_goal(sequence: list[str]) -> str | None:
    if not sequence:
        return None
    if "tool_call_observed" in sequence or "skill_invocation_observed" in sequence:
        return "complete_task_with_tool_or_skill_support"
    if "user_message_observed" in sequence and "assistant_message_observed" in sequence:
        return "respond_to_user_message"
    return "unknown_goal_from_observed_events"


def _infer_task_type(sequence: list[str]) -> str | None:
    if "error_observed" in sequence:
        return "failure_or_exception_handling"
    if "tool_call_observed" in sequence:
        return "tool_assisted_task"
    if "skill_invocation_observed" in sequence:
        return "skill_assisted_task"
    if "user_message_observed" in sequence:
        return "conversation"
    return None


def _extract_declared_name(raw: str, source_ref: str | None) -> str | None:
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or None
        if stripped.lower().startswith("name:"):
            return stripped.split(":", 1)[1].strip() or None
    if source_ref:
        return Path(source_ref).stem
    return None


def _extract_description(raw: str) -> str | None:
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("description:"):
            return stripped.split(":", 1)[1].strip()[:500]
    paragraphs = [line.strip() for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]
    return paragraphs[0][:500] if paragraphs else None


def _extract_list_like(raw: str, needles: list[str]) -> list[str]:
    values: list[str] = []
    lowered_needles = tuple(f"{needle}:" for needle in needles)
    for line in raw.splitlines():
        stripped = line.strip().lstrip("-").strip()
        lowered = stripped.lower()
        if lowered.startswith(lowered_needles):
            values.append(stripped.split(":", 1)[1].strip())
    return [value for value in values if value][:20]


def _extract_risks(raw: str) -> list[str]:
    risks = _extract_list_like(raw, ["risk", "risks", "permission", "permissions"])
    lowered = raw.casefold()
    for marker in ["filesystem", "network", "shell", "credential", "plugin", "mcp"]:
        if marker in lowered and marker not in risks:
            risks.append(marker)
    return risks[:20]


def _shape_summary(values: list[str]) -> dict[str, Any]:
    return {
        "item_count": len(values),
        "max_preview_chars": max((len(item) for item in values), default=0),
        "types": ["text"] if values else [],
    }


def _skill_id_tail(value: str) -> str:
    text = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    text = "_".join(part for part in text.split("_") if part)
    return text[:80] or "external_skill_candidate"

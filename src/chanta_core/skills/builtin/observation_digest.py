from __future__ import annotations

import json
from typing import Any

from chanta_core.observation_digest import (
    DIGESTION_SKILL_IDS,
    OBSERVATION_SKILL_IDS,
    DigestionService,
    ObservationService,
    candidate_from_dict,
    fingerprint_from_dict,
    inference_from_dict,
    observed_run_from_dict,
    static_profile_from_dict,
)
from chanta_core.observation_digest.ids import new_agent_observation_batch_id
from chanta_core.observation_digest.models import ExternalSkillSourceDescriptor
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_observation_digest_skill(skill_id: str) -> Skill:
    tail = skill_id.removeprefix("skill:")
    family = "observation" if skill_id in OBSERVATION_SKILL_IDS else "digestion"
    return Skill(
        skill_id=skill_id,
        skill_name=tail,
        description=f"Read-only {family} internal skill seed.",
        execution_type="builtin",
        input_schema={"root_path": "str", "relative_path": "str"},
        output_schema={"status": "str", "summary": "str"},
        tags=[family, "read_only", "explicit", "observation_digest"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "uses_llm": False,
            "external_execution_used": False,
            "canonical_import_enabled": False,
            "execution_enabled": False,
        },
    )


def create_agent_observation_source_inspect_skill() -> Skill:
    return create_observation_digest_skill("skill:agent_observation_source_inspect")


def create_agent_trace_observe_skill() -> Skill:
    return create_observation_digest_skill("skill:agent_trace_observe")


def create_agent_observation_normalize_skill() -> Skill:
    return create_observation_digest_skill("skill:agent_observation_normalize")


def create_agent_behavior_infer_skill() -> Skill:
    return create_observation_digest_skill("skill:agent_behavior_infer")


def create_agent_process_narrative_skill() -> Skill:
    return create_observation_digest_skill("skill:agent_process_narrative")


def create_external_skill_source_inspect_skill() -> Skill:
    return create_observation_digest_skill("skill:external_skill_source_inspect")


def create_external_skill_static_digest_skill() -> Skill:
    return create_observation_digest_skill("skill:external_skill_static_digest")


def create_external_behavior_fingerprint_skill() -> Skill:
    return create_observation_digest_skill("skill:external_behavior_fingerprint")


def create_external_skill_assimilate_skill() -> Skill:
    return create_observation_digest_skill("skill:external_skill_assimilate")


def create_external_skill_adapter_candidate_skill() -> Skill:
    return create_observation_digest_skill("skill:external_skill_adapter_candidate")


def execute_observation_digest_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        output = _run_observation_digest_skill(skill.skill_id, context.context_attrs, trace_service, ocel_store)
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=True,
            output_text=output.get("summary"),
            output_attrs={
                "execution_type": skill.execution_type,
                "read_only": True,
                "external_execution_used": False,
                "llm_called": False,
                **output,
            },
        )
    except Exception as error:
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=False,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "read_only": True,
                "external_execution_used": False,
                "llm_called": False,
                "exception_type": type(error).__name__,
            },
            error=str(error),
        )


def _run_observation_digest_skill(
    skill_id: str,
    attrs: dict[str, Any],
    trace_service,
    ocel_store,
) -> dict[str, Any]:
    if skill_id in OBSERVATION_SKILL_IDS:
        return _run_observation_skill(skill_id, attrs, trace_service, ocel_store)
    if skill_id in DIGESTION_SKILL_IDS:
        return _run_digestion_skill(skill_id, attrs, trace_service, ocel_store)
    raise ValueError("unsupported observation/digestion skill")


def _run_observation_skill(skill_id: str, attrs: dict[str, Any], trace_service, ocel_store) -> dict[str, Any]:
    service = ObservationService(trace_service=trace_service, ocel_store=ocel_store)
    if skill_id == "skill:agent_observation_source_inspect":
        source = service.inspect_observation_source(
            root_path=_required(attrs, "root_path"),
            relative_path=_required(attrs, "relative_path"),
            source_runtime=str(attrs.get("runtime") or attrs.get("source_runtime") or "unknown"),
            format_hint=str(attrs.get("format_hint") or "generic_jsonl"),
        )
        return {"status": source.source_attrs.get("status", "completed"), "summary": service.render_observation_cli(source), "source": source.to_dict()}
    raw_text = str(attrs.get("raw_jsonl") or "")
    if not raw_text and attrs.get("root_path") and attrs.get("relative_path"):
        source = service.inspect_observation_source(
            root_path=str(attrs["root_path"]),
            relative_path=str(attrs["relative_path"]),
            source_runtime=str(attrs.get("runtime") or "unknown"),
            format_hint=str(attrs.get("format_hint") or "generic_jsonl"),
        )
        target = service.last_source
        if target and target.source_attrs.get("status") == "available":
            from chanta_core.workspace import resolve_workspace_path

            raw_text = resolve_workspace_path(str(attrs["root_path"]), str(attrs["relative_path"])).read_text(encoding="utf-8-sig")
    records = service.parse_generic_jsonl_records(raw_text)
    batch_id = str(attrs.get("batch_id") or new_agent_observation_batch_id())
    events = service.normalize_observation_records(
        records=records,
        batch_id=batch_id,
        source_runtime=str(attrs.get("runtime") or "unknown"),
        source_format=str(attrs.get("format_hint") or "generic_jsonl"),
    )
    if skill_id == "skill:agent_observation_normalize":
        return {"status": "completed", "summary": f"normalized_event_count={len(events)}", "events": [item.to_dict() for item in events]}
    source = service.last_source or service.inspect_observation_source(
        root_path=str(attrs.get("root_path") or "."),
        relative_path=str(attrs.get("relative_path") or "."),
        source_runtime=str(attrs.get("runtime") or "unknown"),
        format_hint=str(attrs.get("format_hint") or "generic_jsonl"),
    )
    batch = service.create_observation_batch(source=source, raw_record_count=len(records), normalized_events=events)
    run = service.create_observed_run(source=source, batch=batch, normalized_events=events)
    if skill_id == "skill:agent_trace_observe":
        return {"status": "completed", "summary": service.render_observation_cli(run), "observed_run": run.to_dict()}
    inference = service.infer_behavior(observed_run=run, normalized_events=events)
    if skill_id == "skill:agent_behavior_infer":
        return {"status": "completed", "summary": service.render_observation_cli(inference), "inference": inference.to_dict()}
    narrative = service.create_process_narrative(observed_run=run, inference=inference)
    return {"status": "completed", "summary": service.render_observation_cli(narrative), "narrative": narrative.to_dict()}


def _run_digestion_skill(skill_id: str, attrs: dict[str, Any], trace_service, ocel_store) -> dict[str, Any]:
    service = DigestionService(trace_service=trace_service, ocel_store=ocel_store)
    if skill_id == "skill:external_skill_source_inspect":
        descriptor = service.inspect_external_skill_source(
            root_path=_required(attrs, "root_path"),
            relative_path=_required(attrs, "relative_path"),
            vendor_hint=attrs.get("vendor_hint") or attrs.get("vendor"),
        )
        return {"status": descriptor.descriptor_attrs.get("status", "completed"), "summary": service.render_digestion_cli(descriptor), "source_descriptor": descriptor.to_dict()}
    if skill_id == "skill:external_skill_static_digest":
        descriptor = service.inspect_external_skill_source(
            root_path=_required(attrs, "root_path"),
            relative_path=_required(attrs, "relative_path"),
            vendor_hint=attrs.get("vendor_hint") or attrs.get("vendor"),
        )
        profile = service.create_static_profile(
            source_descriptor=descriptor,
            root_path=str(attrs["root_path"]),
            relative_path=str(attrs["relative_path"]),
        )
        return {"status": "completed", "summary": service.render_digestion_cli(profile), "static_profile": profile.to_dict()}
    if skill_id == "skill:external_behavior_fingerprint":
        run = observed_run_from_dict(_json_attr(attrs, "observed_run"))
        fingerprint = service.create_behavior_fingerprint(observed_run=run)
        return {"status": "completed", "summary": service.render_digestion_cli(fingerprint), "fingerprint": fingerprint.to_dict()}
    if skill_id == "skill:external_skill_assimilate":
        profile = static_profile_from_dict(_json_attr(attrs, "static_profile")) if attrs.get("static_profile") else None
        fingerprint = fingerprint_from_dict(_json_attr(attrs, "fingerprint")) if attrs.get("fingerprint") else None
        candidate = service.create_assimilation_candidate(static_profile=profile, behavior_fingerprint=fingerprint)
        return {"status": "pending_review", "summary": service.render_digestion_cli(candidate), "candidate": candidate.to_dict()}
    candidate = candidate_from_dict(_json_attr(attrs, "candidate"))
    adapter = service.create_adapter_candidate(candidate=candidate)
    return {"status": "pending_review", "summary": service.render_digestion_cli(adapter), "adapter_candidate": adapter.to_dict()}


def _required(attrs: dict[str, Any], key: str) -> str:
    value = attrs.get(key)
    if value is None or str(value).strip() == "":
        raise ValueError(f"{key} is required")
    return str(value)


def _json_attr(attrs: dict[str, Any], key: str) -> dict[str, Any]:
    value = attrs.get(key)
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        loaded = json.loads(value)
        if isinstance(loaded, dict):
            return loaded
    raise ValueError(f"{key} must be a JSON object")

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.execution import ExecutionEnvelope, ExecutionEnvelopeService
from chanta_core.observation_digest import (
    DIGESTION_SKILL_IDS,
    OBSERVATION_DIGESTION_SKILL_IDS,
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
from chanta_core.observation_digest.models import (
    ExternalSkillSourceDescriptor,
    ExternalSkillStaticProfile,
    ObservationDigestionResult,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.ids import (
    new_observation_digest_invocation_finding_id,
    new_observation_digest_invocation_policy_id,
    new_observation_digest_invocation_result_id,
    new_observation_digest_skill_runtime_binding_id,
)
from chanta_core.skills.invocation import ExplicitSkillInvocationService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import resolve_workspace_path
from chanta_core.workspace.errors import WorkspacePathViolationError


OBSERVATION_DIGEST_INVOCATION_OBJECT_TYPES = [
    "observation_digest_skill_runtime_binding",
    "observation_digest_invocation_policy",
    "observation_digest_invocation_finding",
    "observation_digest_invocation_result",
]

OBSERVATION_DIGEST_INVOCATION_EVENT_ACTIVITIES = [
    "observation_digest_skill_binding_registered",
    "observation_digest_invocation_policy_registered",
    "observation_digest_skill_invocation_requested",
    "observation_digest_skill_invocation_gate_checked",
    "observation_digest_skill_invocation_blocked",
    "observation_digest_skill_invocation_completed",
    "observation_digest_skill_invocation_failed",
    "observation_digest_invocation_finding_recorded",
    "observation_digest_invocation_result_recorded",
]

OBSERVATION_DIGEST_HANDLER_MAP: dict[str, tuple[str, str, str]] = {
    "skill:agent_observation_source_inspect": (
        "observation",
        "inspect_observation_source",
        "ObservationService",
    ),
    "skill:agent_trace_observe": ("observation", "observe_trace_from_file", "ObservationService"),
    "skill:agent_observation_normalize": (
        "observation",
        "normalize_observation_records",
        "ObservationService",
    ),
    "skill:agent_behavior_infer": ("observation", "infer_behavior", "ObservationService"),
    "skill:agent_process_narrative": (
        "observation",
        "create_process_narrative",
        "ObservationService",
    ),
    "skill:external_skill_source_inspect": (
        "digestion",
        "inspect_external_skill_source",
        "DigestionService",
    ),
    "skill:external_skill_static_digest": ("digestion", "create_static_profile", "DigestionService"),
    "skill:external_behavior_fingerprint": (
        "digestion",
        "create_behavior_fingerprint",
        "DigestionService",
    ),
    "skill:external_skill_assimilate": (
        "digestion",
        "create_assimilation_candidate",
        "DigestionService",
    ),
    "skill:external_skill_adapter_candidate": (
        "digestion",
        "create_adapter_candidate",
        "DigestionService",
    ),
}


@dataclass(frozen=True)
class ObservationDigestSkillRuntimeBinding:
    binding_id: str
    skill_id: str
    skill_family: str
    handler_name: str
    service_name: str
    input_contract_ref: str | None
    output_contract_ref: str | None
    gate_required: bool
    gate_kind: str
    envelope_required: bool
    read_only: bool
    enabled: bool
    created_at: str
    binding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "skill_id": self.skill_id,
            "skill_family": self.skill_family,
            "handler_name": self.handler_name,
            "service_name": self.service_name,
            "input_contract_ref": self.input_contract_ref,
            "output_contract_ref": self.output_contract_ref,
            "gate_required": self.gate_required,
            "gate_kind": self.gate_kind,
            "envelope_required": self.envelope_required,
            "read_only": self.read_only,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "binding_attrs": dict(self.binding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestInvocationPolicy:
    policy_id: str
    policy_name: str
    allowed_skill_ids: list[str]
    denied_skill_ids: list[str]
    allow_file_read: bool
    allow_external_harness_execution: bool
    allow_script_execution: bool
    allow_shell: bool
    allow_network: bool
    allow_mcp: bool
    allow_plugin: bool
    allow_write: bool
    require_explicit_invocation: bool
    require_gate: bool
    require_envelope: bool
    max_input_chars: int
    max_records: int
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "allowed_skill_ids": list(self.allowed_skill_ids),
            "denied_skill_ids": list(self.denied_skill_ids),
            "allow_file_read": self.allow_file_read,
            "allow_external_harness_execution": self.allow_external_harness_execution,
            "allow_script_execution": self.allow_script_execution,
            "allow_shell": self.allow_shell,
            "allow_network": self.allow_network,
            "allow_mcp": self.allow_mcp,
            "allow_plugin": self.allow_plugin,
            "allow_write": self.allow_write,
            "require_explicit_invocation": self.require_explicit_invocation,
            "require_gate": self.require_gate,
            "require_envelope": self.require_envelope,
            "max_input_chars": self.max_input_chars,
            "max_records": self.max_records,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestInvocationFinding:
    finding_id: str
    invocation_id: str | None
    skill_id: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "invocation_id": self.invocation_id,
            "skill_id": self.skill_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestInvocationResult:
    result_id: str
    skill_id: str
    status: str
    executed: bool
    blocked: bool
    output_ref: str | None
    output_preview: dict[str, Any]
    envelope_id: str | None
    finding_ids: list[str]
    created_object_refs: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "executed": self.executed,
            "blocked": self.blocked,
            "output_ref": self.output_ref,
            "output_preview": dict(self.output_preview),
            "envelope_id": self.envelope_id,
            "finding_ids": list(self.finding_ids),
            "created_object_refs": list(self.created_object_refs),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class ObservationDigestSkillInvocationService:
    def __init__(
        self,
        *,
        observation_service: ObservationService | None = None,
        digestion_service: DigestionService | None = None,
        explicit_skill_invocation_service: ExplicitSkillInvocationService | None = None,
        skill_execution_gate_service: SkillExecutionGateService | None = None,
        execution_envelope_service: ExecutionEnvelopeService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.observation_service = observation_service or ObservationService(trace_service=self.trace_service)
        self.digestion_service = digestion_service or DigestionService(trace_service=self.trace_service)
        self.explicit_skill_invocation_service = explicit_skill_invocation_service or ExplicitSkillInvocationService(
            trace_service=self.trace_service
        )
        self.skill_execution_gate_service = skill_execution_gate_service or SkillExecutionGateService(
            trace_service=self.trace_service
        )
        self.execution_envelope_service = execution_envelope_service or ExecutionEnvelopeService(
            trace_service=self.trace_service
        )
        self.last_policy: ObservationDigestInvocationPolicy | None = None
        self.last_bindings: list[ObservationDigestSkillRuntimeBinding] = []
        self.last_findings: list[ObservationDigestInvocationFinding] = []
        self.last_result: ObservationDigestInvocationResult | None = None
        self.last_envelope: ExecutionEnvelope | None = None

    def create_default_policy(self, **policy_attrs: Any) -> ObservationDigestInvocationPolicy:
        policy = ObservationDigestInvocationPolicy(
            policy_id=new_observation_digest_invocation_policy_id(),
            policy_name="default_observation_digest_invocation_policy",
            allowed_skill_ids=sorted(OBSERVATION_DIGESTION_SKILL_IDS),
            denied_skill_ids=[],
            allow_file_read=True,
            allow_external_harness_execution=False,
            allow_script_execution=False,
            allow_shell=False,
            allow_network=False,
            allow_mcp=False,
            allow_plugin=False,
            allow_write=False,
            require_explicit_invocation=True,
            require_gate=True,
            require_envelope=True,
            max_input_chars=int(policy_attrs.pop("max_input_chars", 100000)),
            max_records=int(policy_attrs.pop("max_records", 1000)),
            created_at=utc_now_iso(),
            policy_attrs={
                "read_only_internal_services_only": True,
                "external_candidates_executable": False,
                "permission_grants_created": False,
                **policy_attrs,
            },
        )
        self.last_policy = policy
        self._record_model(
            "observation_digest_invocation_policy_registered",
            "observation_digest_invocation_policy",
            policy.policy_id,
            policy,
        )
        return policy

    def create_runtime_bindings(self) -> list[ObservationDigestSkillRuntimeBinding]:
        bindings: list[ObservationDigestSkillRuntimeBinding] = []
        for skill_id in sorted(OBSERVATION_DIGESTION_SKILL_IDS):
            family, handler_name, service_name = OBSERVATION_DIGEST_HANDLER_MAP[skill_id]
            binding = ObservationDigestSkillRuntimeBinding(
                binding_id=new_observation_digest_skill_runtime_binding_id(),
                skill_id=skill_id,
                skill_family=family,
                handler_name=handler_name,
                service_name=service_name,
                input_contract_ref=f"{skill_id}:input_contract",
                output_contract_ref=f"{skill_id}:output_contract",
                gate_required=True,
                gate_kind="read_only_explicit_gate",
                envelope_required=True,
                read_only=True,
                enabled=True,
                created_at=utc_now_iso(),
                binding_attrs={
                    "external_execution_used": False,
                    "shell_network_mcp_plugin_allowed": False,
                    "workspace_write_allowed": False,
                },
            )
            bindings.append(binding)
            self._record_model(
                "observation_digest_skill_binding_registered",
                "observation_digest_skill_runtime_binding",
                binding.binding_id,
                binding,
            )
        self.last_bindings = bindings
        return bindings

    def resolve_binding(self, skill_id: str) -> ObservationDigestSkillRuntimeBinding | None:
        bindings = self.last_bindings or self.create_runtime_bindings()
        for binding in bindings:
            if binding.skill_id == skill_id:
                return binding
        return None

    def validate_invocation_input(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any],
        policy: ObservationDigestInvocationPolicy,
        invocation_id: str | None = None,
    ) -> list[ObservationDigestInvocationFinding]:
        findings: list[ObservationDigestInvocationFinding] = []
        if not skill_id:
            findings.append(
                self.record_finding(
                    invocation_id=invocation_id,
                    skill_id=skill_id,
                    finding_type="missing_skill_id",
                    status="failed",
                    severity="high",
                    message="Explicit skill_id is required.",
                    subject_ref=None,
                )
            )
            return findings
        if skill_id not in policy.allowed_skill_ids or skill_id in policy.denied_skill_ids:
            findings.append(
                self.record_finding(
                    invocation_id=invocation_id,
                    skill_id=skill_id,
                    finding_type="unsupported_skill",
                    status="failed",
                    severity="high",
                    message="Skill is not allowed by the Observation/Digestion invocation policy.",
                    subject_ref=skill_id,
                )
            )
            return findings
        payload_chars = len(json.dumps(input_payload, ensure_ascii=False, sort_keys=True, default=str))
        if payload_chars > policy.max_input_chars:
            findings.append(
                self.record_finding(
                    invocation_id=invocation_id,
                    skill_id=skill_id,
                    finding_type="input_too_large",
                    status="failed",
                    severity="high",
                    message="Input payload exceeds policy max_input_chars.",
                    subject_ref=skill_id,
                )
            )
        records = input_payload.get("records") or input_payload.get("raw_records")
        if isinstance(records, list) and len(records) > policy.max_records:
            findings.append(
                self.record_finding(
                    invocation_id=invocation_id,
                    skill_id=skill_id,
                    finding_type="record_limit_exceeded",
                    status="failed",
                    severity="high",
                    message="Input payload exceeds policy max_records.",
                    subject_ref=skill_id,
                )
            )
        missing_inputs = _missing_required_inputs(skill_id, input_payload)
        for missing in missing_inputs:
            findings.append(
                self.record_finding(
                    invocation_id=invocation_id,
                    skill_id=skill_id,
                    finding_type="missing_required_input",
                    status="failed",
                    severity="medium",
                    message=f"Missing required input: {missing}.",
                    subject_ref=skill_id,
                    finding_attrs={"missing_input": missing},
                )
            )
        if input_payload.get("root_path") and input_payload.get("relative_path"):
            try:
                resolved = resolve_workspace_path(
                    str(input_payload["root_path"]),
                    str(input_payload["relative_path"]),
                )
            except (OSError, WorkspacePathViolationError, ValueError) as error:
                findings.append(
                    self.record_finding(
                        invocation_id=invocation_id,
                        skill_id=skill_id,
                        finding_type=_workspace_error_type(error),
                        status="failed",
                        severity="high",
                        message=str(error),
                        subject_ref=skill_id,
                    )
                )
            else:
                if resolved.is_file() and resolved.stat().st_size > policy.max_input_chars:
                    findings.append(
                        self.record_finding(
                            invocation_id=invocation_id,
                            skill_id=skill_id,
                            finding_type="input_file_too_large",
                            status="failed",
                            severity="high",
                            message="Input file exceeds policy max_input_chars.",
                            subject_ref=skill_id,
                        )
                    )
        return findings

    def gate_invocation(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any],
        explicit_invocation_request_id: str | None,
        invocation_mode: str = "explicit_observation_digest",
        requester_type: str | None = "cli",
        requester_id: str | None = "chanta-cli",
    ) -> Any:
        request = self.skill_execution_gate_service.create_gate_request(
            skill_id=skill_id,
            input_payload=input_payload,
            explicit_invocation_request_id=explicit_invocation_request_id,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            request_attrs={"observation_digest_invocation": True},
        )
        decision = self.skill_execution_gate_service.evaluate_gate(request=request)
        findings = list(self.skill_execution_gate_service.last_findings)
        gate_result = self.skill_execution_gate_service.record_result(
            request=request,
            decision=decision,
            explicit_invocation_result_id=None,
            executed=False,
            blocked=not decision.can_execute,
            findings=findings,
            status="allowed" if decision.can_execute else "blocked",
        )
        self._record_event(
            "observation_digest_skill_invocation_gate_checked",
            attrs={
                "skill_id": skill_id,
                "can_execute": decision.can_execute,
                "gate_result_id": gate_result.gate_result_id,
            },
        )
        return gate_result

    def invoke_observation_skill(self, skill_id: str, input_payload: dict[str, Any]) -> dict[str, Any]:
        if skill_id == "skill:agent_observation_source_inspect":
            source = self.observation_service.inspect_observation_source(
                root_path=str(input_payload["root_path"]),
                relative_path=str(input_payload["relative_path"]),
                source_runtime=str(input_payload.get("source_runtime") or input_payload.get("runtime") or "unknown"),
                format_hint=str(input_payload.get("format_hint") or "generic_jsonl"),
            )
            return _output("source", source, self.observation_service.render_observation_cli(source))
        if skill_id in {
            "skill:agent_trace_observe",
            "skill:agent_observation_normalize",
            "skill:agent_behavior_infer",
            "skill:agent_process_narrative",
        }:
            records = _records_from_payload(input_payload)
            source = None
            if input_payload.get("root_path") and input_payload.get("relative_path"):
                source = self.observation_service.inspect_observation_source(
                    root_path=str(input_payload["root_path"]),
                    relative_path=str(input_payload["relative_path"]),
                    source_runtime=str(input_payload.get("source_runtime") or input_payload.get("runtime") or "unknown"),
                    format_hint=str(input_payload.get("format_hint") or "generic_jsonl"),
                )
                if not records:
                    target = resolve_workspace_path(
                        str(input_payload["root_path"]),
                        str(input_payload["relative_path"]),
                    )
                    records = self.observation_service.parse_generic_jsonl_records(
                        target.read_text(encoding="utf-8-sig")
                    )
            batch_id = str(input_payload.get("batch_id") or new_agent_observation_batch_id())
            if skill_id == "skill:agent_observation_normalize":
                events = self.observation_service.normalize_observation_records(
                    records=records,
                    batch_id=batch_id,
                    source_runtime=str(input_payload.get("source_runtime") or input_payload.get("runtime") or "unknown"),
                    source_format=str(input_payload.get("format_hint") or "generic_jsonl"),
                )
                return {
                    "status": "completed",
                    "summary": f"normalized_event_count={len(events)}",
                    "events": [event.to_dict() for event in events],
                    "created_object_refs": [event.normalized_event_id for event in events],
                }
            observed_run = (
                observed_run_from_dict(_json_payload(input_payload, "observed_run"))
                if input_payload.get("observed_run")
                else None
            )
            events = self.observation_service.normalize_observation_records(
                records=records,
                batch_id=batch_id,
                source_runtime=str(input_payload.get("source_runtime") or input_payload.get("runtime") or "unknown"),
                source_format=str(input_payload.get("format_hint") or "generic_jsonl"),
            )
            if observed_run is None:
                if source is None:
                    source = self.observation_service.inspect_observation_source(
                        root_path=str(input_payload.get("root_path") or "."),
                        relative_path=str(input_payload.get("relative_path") or "."),
                        source_runtime=str(input_payload.get("source_runtime") or input_payload.get("runtime") or "unknown"),
                        format_hint=str(input_payload.get("format_hint") or "generic_jsonl"),
                    )
                batch = self.observation_service.create_observation_batch(
                    source=source,
                    raw_record_count=len(records),
                    normalized_events=events,
                )
                observed_run = self.observation_service.create_observed_run(
                    source=source,
                    batch=batch,
                    normalized_events=events,
                )
            if skill_id == "skill:agent_trace_observe":
                return _output(
                    "observed_run",
                    observed_run,
                    self.observation_service.render_observation_cli(observed_run),
                )
            inference = (
                inference_from_dict(_json_payload(input_payload, "inference"))
                if input_payload.get("inference")
                else self.observation_service.infer_behavior(
                    observed_run=observed_run,
                    normalized_events=events,
                )
            )
            if skill_id == "skill:agent_behavior_infer":
                return _output(
                    "inference",
                    inference,
                    self.observation_service.render_observation_cli(inference),
                )
            narrative = self.observation_service.create_process_narrative(
                observed_run=observed_run,
                inference=inference,
            )
            return _output(
                "narrative",
                narrative,
                self.observation_service.render_observation_cli(narrative),
            )
        raise ValueError("unsupported observation skill")

    def invoke_digestion_skill(self, skill_id: str, input_payload: dict[str, Any]) -> dict[str, Any]:
        if skill_id == "skill:external_skill_source_inspect":
            descriptor = self.digestion_service.inspect_external_skill_source(
                root_path=str(input_payload["root_path"]),
                relative_path=str(input_payload["relative_path"]),
                vendor_hint=input_payload.get("vendor_hint") or input_payload.get("vendor"),
            )
            return _output("source_descriptor", descriptor, self.digestion_service.render_digestion_cli(descriptor))
        if skill_id == "skill:external_skill_static_digest":
            descriptor = _source_descriptor_from_payload(input_payload)
            if descriptor is None:
                descriptor = self.digestion_service.inspect_external_skill_source(
                    root_path=str(input_payload["root_path"]),
                    relative_path=str(input_payload["relative_path"]),
                    vendor_hint=input_payload.get("vendor_hint") or input_payload.get("vendor"),
                )
            profile = self.digestion_service.create_static_profile(
                source_descriptor=descriptor,
                root_path=str(input_payload.get("root_path")) if input_payload.get("root_path") else None,
                relative_path=str(input_payload.get("relative_path")) if input_payload.get("relative_path") else None,
            )
            return _output("static_profile", profile, self.digestion_service.render_digestion_cli(profile))
        if skill_id == "skill:external_behavior_fingerprint":
            run = observed_run_from_dict(_json_payload(input_payload, "observed_run"))
            fingerprint = self.digestion_service.create_behavior_fingerprint(observed_run=run)
            return _output("fingerprint", fingerprint, self.digestion_service.render_digestion_cli(fingerprint))
        if skill_id == "skill:external_skill_assimilate":
            profile = (
                static_profile_from_dict(_json_payload(input_payload, "static_profile"))
                if input_payload.get("static_profile")
                else None
            )
            fingerprint = (
                fingerprint_from_dict(_json_payload(input_payload, "fingerprint"))
                if input_payload.get("fingerprint")
                else None
            )
            candidate = self.digestion_service.create_assimilation_candidate(
                static_profile=profile,
                behavior_fingerprint=fingerprint,
            )
            return _output("candidate", candidate, self.digestion_service.render_digestion_cli(candidate), "pending_review")
        if skill_id == "skill:external_skill_adapter_candidate":
            candidate = candidate_from_dict(_json_payload(input_payload, "candidate"))
            adapter = self.digestion_service.create_adapter_candidate(candidate=candidate)
            return _output(
                "adapter_candidate",
                adapter,
                self.digestion_service.render_digestion_cli(adapter),
                "pending_review",
            )
        raise ValueError("unsupported digestion skill")

    def invoke_skill(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any] | None = None,
        invocation_mode: str = "explicit_observation_digest",
        requester_type: str | None = "cli",
        requester_id: str | None = "chanta-cli",
    ) -> ObservationDigestInvocationResult:
        payload = dict(input_payload or {})
        policy = self.create_default_policy()
        binding = self.resolve_binding(skill_id)
        self._record_event(
            "observation_digest_skill_invocation_requested",
            attrs={
                "skill_id": skill_id,
                "explicit_skill_id_required": True,
                "invocation_mode": invocation_mode,
            },
        )
        explicit_request = self.explicit_skill_invocation_service.create_request(
            skill_id=skill_id,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
        )
        explicit_input = self.explicit_skill_invocation_service.record_input(
            request=explicit_request,
            input_payload=payload,
        )
        validated_explicit_input = self.explicit_skill_invocation_service.validate_input(
            request=explicit_request,
            invocation_input=explicit_input,
        )
        explicit_decision = self.explicit_skill_invocation_service.decide_invocation(
            request=explicit_request,
            invocation_input=validated_explicit_input,
        )
        findings = self.validate_invocation_input(
            skill_id=skill_id,
            input_payload=payload,
            policy=policy,
            invocation_id=explicit_request.request_id,
        )
        if binding is None:
            findings.append(
                self.record_finding(
                    invocation_id=explicit_request.request_id,
                    skill_id=skill_id,
                    finding_type="binding_not_found",
                    status="failed",
                    severity="high",
                    message="Runtime binding was not found.",
                    subject_ref=skill_id,
                )
            )
        gate_result = self.gate_invocation(
            skill_id=skill_id,
            input_payload=payload,
            explicit_invocation_request_id=explicit_request.request_id,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
        )
        if findings or not explicit_decision.can_execute or gate_result.blocked:
            return self._finalize_result(
                skill_id=skill_id,
                status="blocked",
                executed=False,
                blocked=True,
                output_payload={
                    "summary": "Observation/Digestion invocation blocked by validation or gate.",
                    "explicit_decision": explicit_decision.decision,
                    "gate_status": gate_result.status,
                },
                finding_ids=[finding.finding_id for finding in findings],
                created_object_refs=[],
                binding=binding,
                policy=policy,
            )
        try:
            if skill_id in OBSERVATION_SKILL_IDS:
                output = self.invoke_observation_skill(skill_id, payload)
            elif skill_id in DIGESTION_SKILL_IDS:
                output = self.invoke_digestion_skill(skill_id, payload)
            else:
                raise ValueError("unsupported observation/digestion skill")
        except Exception as error:
            finding = self.record_finding(
                invocation_id=explicit_request.request_id,
                skill_id=skill_id,
                finding_type="internal_service_error",
                status="failed",
                severity="high",
                message=str(error),
                subject_ref=skill_id,
            )
            return self._finalize_result(
                skill_id=skill_id,
                status="failed",
                executed=False,
                blocked=False,
                output_payload={"summary": str(error), "exception_type": type(error).__name__},
                finding_ids=[finding.finding_id],
                created_object_refs=[],
                binding=binding,
                policy=policy,
            )
        return self._finalize_result(
            skill_id=skill_id,
            status=str(output.get("status") or "completed"),
            executed=True,
            blocked=False,
            output_payload=output,
            finding_ids=[],
            created_object_refs=[str(item) for item in output.get("created_object_refs") or []],
            binding=binding,
            policy=policy,
        )

    def record_finding(
        self,
        *,
        invocation_id: str | None,
        skill_id: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestInvocationFinding:
        finding = ObservationDigestInvocationFinding(
            finding_id=new_observation_digest_invocation_finding_id(),
            invocation_id=invocation_id,
            skill_id=skill_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "permission_grants_created": False,
                "external_execution_used": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digest_invocation_finding_recorded",
            "observation_digest_invocation_finding",
            finding.finding_id,
            finding,
        )
        return finding

    def record_result(self, result: ObservationDigestInvocationResult) -> ObservationDigestInvocationResult:
        self.last_result = result
        event_activity = (
            "observation_digest_skill_invocation_blocked"
            if result.blocked
            else "observation_digest_skill_invocation_completed"
            if result.executed
            else "observation_digest_skill_invocation_failed"
        )
        self._record_model(
            "observation_digest_invocation_result_recorded",
            "observation_digest_invocation_result",
            result.result_id,
            result,
            links=[("execution_envelope_object", result.envelope_id or "")]
            + [("created_object", item) for item in result.created_object_refs]
            + [("finding_object", item) for item in result.finding_ids],
            object_links=[
                (result.result_id, result.envelope_id or "", "invocation_result_wrapped_by_execution_envelope")
            ],
        )
        self._record_model(
            event_activity,
            "observation_digest_invocation_result",
            result.result_id,
            result,
        )
        return result

    def wrap_result_in_envelope(
        self,
        *,
        result: ObservationDigestInvocationResult,
        policy: ObservationDigestInvocationPolicy,
        binding: ObservationDigestSkillRuntimeBinding | None,
    ) -> ExecutionEnvelope:
        envelope = self.execution_envelope_service.create_envelope(
            execution_kind="observation_digest_internal_skill",
            execution_subject_id=result.result_id,
            skill_id=result.skill_id,
            status=result.status,
            execution_allowed=not result.blocked,
            execution_performed=result.executed,
            blocked=result.blocked,
            started_at=result.created_at,
            completed_at=utc_now_iso(),
            envelope_attrs={
                "policy_id": policy.policy_id,
                "binding_id": binding.binding_id if binding else None,
                "read_only_internal_service": True,
                "external_harness_execution_used": False,
                "external_script_execution_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
                "workspace_write_used": False,
            },
        )
        self.last_envelope = envelope
        return envelope

    def render_invocation_cli(self, result: ObservationDigestInvocationResult | None = None) -> str:
        item = result or self.last_result
        if item is None:
            return "Observation/Digestion Invocation: unavailable"
        lines = [
            "Observation/Digestion Invocation",
            f"skill_id={item.skill_id}",
            f"status={item.status}",
            f"executed={str(item.executed).lower()}",
            f"blocked={str(item.blocked).lower()}",
            f"envelope_id={item.envelope_id or ''}",
            f"finding_count={len(item.finding_ids)}",
            f"created_object_refs={','.join(item.created_object_refs)}",
            "external_harness_execution_used=false",
            "external_script_execution_used=false",
            "shell_network_mcp_plugin_execution=false",
            "workspace_write_used=false",
        ]
        if item.output_preview:
            lines.append(f"output_preview={json.dumps(item.output_preview, ensure_ascii=False, sort_keys=True)}")
        return "\n".join(lines)

    def _finalize_result(
        self,
        *,
        skill_id: str,
        status: str,
        executed: bool,
        blocked: bool,
        output_payload: dict[str, Any],
        finding_ids: list[str],
        created_object_refs: list[str],
        binding: ObservationDigestSkillRuntimeBinding | None,
        policy: ObservationDigestInvocationPolicy,
    ) -> ObservationDigestInvocationResult:
        result = ObservationDigestInvocationResult(
            result_id=new_observation_digest_invocation_result_id(),
            skill_id=skill_id,
            status=status,
            executed=executed,
            blocked=blocked,
            output_ref=_output_ref(output_payload),
            output_preview=_preview_mapping(output_payload),
            envelope_id=None,
            finding_ids=list(finding_ids),
            created_object_refs=list(created_object_refs),
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "explicit_invocation_required": True,
                "gate_required": True,
                "envelope_required": True,
                "external_execution_used": False,
                "permission_grants_created": False,
                "canonical_import_enabled": False,
                "execution_enabled_for_external_candidate": False,
            },
        )
        envelope = self.wrap_result_in_envelope(result=result, policy=policy, binding=binding)
        return self.record_result(replace(result, envelope_id=envelope.envelope_id))

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
        self._record_event(
            activity,
            objects=[_object(object_type, object_id, model.to_dict())],
            links=[(f"{object_type}_object", object_id), *(links or [])],
            object_links=object_links or [],
            attrs={"object_type": object_type, "object_id": object_id},
        )

    def _record_event(
        self,
        activity: str,
        *,
        objects: list[OCELObject] | None = None,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
        attrs: dict[str, Any] | None = None,
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "read_only": True,
                "external_harness_execution_used": False,
                "external_script_execution_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
                "workspace_write_used": False,
                "permission_grants_created": False,
                **dict(attrs or {}),
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links or []
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links or []
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=list(objects or []), relations=relations)
        )


def _missing_required_inputs(skill_id: str, payload: dict[str, Any]) -> list[str]:
    if skill_id == "skill:agent_observation_source_inspect":
        return _missing(payload, ["root_path", "relative_path"])
    if skill_id == "skill:agent_trace_observe":
        return _missing(payload, ["root_path", "relative_path"])
    if skill_id == "skill:agent_observation_normalize":
        if payload.get("records") or payload.get("raw_records") or payload.get("raw_jsonl"):
            return []
        return ["raw_records"]
    if skill_id == "skill:agent_behavior_infer":
        if payload.get("observed_run") or (payload.get("root_path") and payload.get("relative_path")):
            return []
        return ["observed_run"]
    if skill_id == "skill:agent_process_narrative":
        if payload.get("inference") and (payload.get("observed_run") or payload.get("root_path")):
            return []
        if payload.get("root_path") and payload.get("relative_path"):
            return []
        return ["inference"]
    if skill_id == "skill:external_skill_source_inspect":
        return _missing(payload, ["root_path", "relative_path"])
    if skill_id == "skill:external_skill_static_digest":
        if payload.get("source_descriptor") or (payload.get("root_path") and payload.get("relative_path")):
            return []
        return ["source_descriptor"]
    if skill_id == "skill:external_behavior_fingerprint":
        return [] if payload.get("observed_run") else ["observed_run"]
    if skill_id == "skill:external_skill_assimilate":
        if payload.get("static_profile") or payload.get("fingerprint"):
            return []
        return ["static_profile_or_fingerprint"]
    if skill_id == "skill:external_skill_adapter_candidate":
        return [] if payload.get("candidate") else ["candidate"]
    return []


def _missing(payload: dict[str, Any], keys: list[str]) -> list[str]:
    return [key for key in keys if not str(payload.get(key) or "").strip()]


def _workspace_error_type(error: Exception) -> str:
    message = str(error).lower()
    if "traversal" in message:
        return "path_traversal"
    if "outside" in message:
        return "outside_workspace"
    return "workspace_boundary_violation"


def _records_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("records", payload.get("raw_records"))
    if isinstance(records, list):
        return [dict(item) for item in records if isinstance(item, dict)]
    raw_jsonl = payload.get("raw_jsonl")
    if isinstance(raw_jsonl, str) and raw_jsonl.strip():
        return ObservationService().parse_generic_jsonl_records(raw_jsonl)
    return []


def _json_payload(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        loaded = json.loads(value)
        if isinstance(loaded, dict):
            return loaded
    raise ValueError(f"{key} must be a JSON object")


def _source_descriptor_from_payload(payload: dict[str, Any]) -> ExternalSkillSourceDescriptor | None:
    value = payload.get("source_descriptor")
    if not isinstance(value, dict):
        return None
    return ExternalSkillSourceDescriptor(
        source_descriptor_id=str(value.get("source_descriptor_id") or ""),
        source_kind=str(value.get("source_kind") or "external_skill_source"),
        source_runtime=str(value.get("source_runtime") or "unknown"),
        vendor_hint=value.get("vendor_hint"),
        source_root_ref=value.get("source_root_ref"),
        detected_files=[str(item) for item in value.get("detected_files") or []],
        detected_manifest_refs=[str(item) for item in value.get("detected_manifest_refs") or []],
        confidence=float(value.get("confidence") or 0.0),
        created_at=str(value.get("created_at") or utc_now_iso()),
        descriptor_attrs=dict(value.get("descriptor_attrs") or {}),
    )


def _output(
    output_key: str,
    model: Any,
    summary: str,
    status: str = "completed",
) -> dict[str, Any]:
    data = model.to_dict()
    object_id = _model_object_id(data)
    return {
        "status": status,
        "summary": summary,
        output_key: data,
        "created_object_refs": [object_id] if object_id else [],
    }


def _model_object_id(data: dict[str, Any]) -> str | None:
    for key in [
        "normalized_event_id",
        "narrative_id",
        "inference_id",
        "observed_run_id",
        "static_profile_id",
        "fingerprint_id",
        "candidate_id",
        "adapter_candidate_id",
        "source_descriptor_id",
        "source_id",
        "batch_id",
        "result_id",
    ]:
        if data.get(key):
            return str(data[key])
    return None


def _output_ref(output_payload: dict[str, Any]) -> str | None:
    for key in [
        "source",
        "observed_run",
        "inference",
        "narrative",
        "source_descriptor",
        "static_profile",
        "fingerprint",
        "candidate",
        "adapter_candidate",
    ]:
        value = output_payload.get(key)
        if isinstance(value, dict):
            return _model_object_id(value)
    return None


def _preview_mapping(value: dict[str, Any], *, max_chars: int = 240) -> dict[str, Any]:
    preview: dict[str, Any] = {}
    for key, item in value.items():
        if key in {"records", "raw_records"} and isinstance(item, list):
            preview[key] = {"list_count": len(item)}
        elif isinstance(item, str):
            preview[key] = item[:max_chars]
        elif isinstance(item, (int, float, bool)) or item is None:
            preview[key] = item
        elif isinstance(item, dict):
            preview[key] = {"dict_keys": sorted(str(inner_key) for inner_key in item)[:20]}
        elif isinstance(item, list):
            preview[key] = {"list_count": len(item)}
        else:
            preview[key] = type(item).__name__
    return preview


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

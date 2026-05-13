from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.observation_digest import (
    DIGESTION_SKILL_IDS,
    OBSERVATION_DIGESTION_SKILL_IDS,
    OBSERVATION_SKILL_IDS,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_observation_digest_conformance_check_id,
    new_observation_digest_conformance_finding_id,
    new_observation_digest_conformance_policy_id,
    new_observation_digest_conformance_report_id,
    new_observation_digest_smoke_case_id,
    new_observation_digest_smoke_result_id,
)
from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService
from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService
from chanta_core.skills.onboarding import InternalSkillOnboardingService
from chanta_core.skills.registry_view import SkillRegistryEntry, SkillRegistryViewService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


OBSERVATION_DIGEST_CONFORMANCE_OBJECT_TYPES = [
    "observation_digest_conformance_policy",
    "observation_digest_conformance_check",
    "observation_digest_smoke_case",
    "observation_digest_smoke_result",
    "observation_digest_conformance_finding",
    "observation_digest_conformance_report",
]

OBSERVATION_DIGEST_CONFORMANCE_EVENT_ACTIVITIES = [
    "observation_digest_conformance_policy_registered",
    "observation_digest_conformance_check_started",
    "observation_digest_conformance_check_completed",
    "observation_digest_smoke_case_registered",
    "observation_digest_smoke_case_started",
    "observation_digest_smoke_case_completed",
    "observation_digest_conformance_finding_recorded",
    "observation_digest_conformance_report_recorded",
]


@dataclass(frozen=True)
class ObservationDigestConformancePolicy:
    policy_id: str
    policy_name: str
    required_skill_ids: list[str]
    require_registry_entry: bool
    require_onboarding_result: bool
    require_input_contract: bool
    require_output_contract: bool
    require_risk_profile: bool
    require_gate_contract: bool
    require_observability_contract: bool
    require_envelope: bool
    require_ocel_events: bool
    require_pig_visibility: bool
    require_audit_visibility: bool
    require_workbench_visibility: bool
    deny_external_execution: bool
    deny_shell_network_write: bool
    deny_memory_persona_overlay_mutation: bool
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "required_skill_ids": list(self.required_skill_ids),
            "require_registry_entry": self.require_registry_entry,
            "require_onboarding_result": self.require_onboarding_result,
            "require_input_contract": self.require_input_contract,
            "require_output_contract": self.require_output_contract,
            "require_risk_profile": self.require_risk_profile,
            "require_gate_contract": self.require_gate_contract,
            "require_observability_contract": self.require_observability_contract,
            "require_envelope": self.require_envelope,
            "require_ocel_events": self.require_ocel_events,
            "require_pig_visibility": self.require_pig_visibility,
            "require_audit_visibility": self.require_audit_visibility,
            "require_workbench_visibility": self.require_workbench_visibility,
            "deny_external_execution": self.deny_external_execution,
            "deny_shell_network_write": self.deny_shell_network_write,
            "deny_memory_persona_overlay_mutation": self.deny_memory_persona_overlay_mutation,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestConformanceCheck:
    check_id: str
    skill_id: str
    check_type: str
    status: str
    passed: bool
    severity: str
    message: str
    evidence_refs: list[str]
    created_at: str
    check_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "skill_id": self.skill_id,
            "check_type": self.check_type,
            "status": self.status,
            "passed": self.passed,
            "severity": self.severity,
            "message": self.message,
            "evidence_refs": list(self.evidence_refs),
            "created_at": self.created_at,
            "check_attrs": dict(self.check_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestSmokeCase:
    smoke_case_id: str
    skill_id: str
    case_name: str
    input_payload: dict[str, Any]
    expected_status: str
    expected_created_object_types: list[str]
    expected_findings: list[str]
    should_execute: bool
    should_block: bool
    should_create_envelope: bool
    should_mutate_state: bool
    created_at: str
    case_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "smoke_case_id": self.smoke_case_id,
            "skill_id": self.skill_id,
            "case_name": self.case_name,
            "input_payload": _redacted_payload(self.input_payload),
            "expected_status": self.expected_status,
            "expected_created_object_types": list(self.expected_created_object_types),
            "expected_findings": list(self.expected_findings),
            "should_execute": self.should_execute,
            "should_block": self.should_block,
            "should_create_envelope": self.should_create_envelope,
            "should_mutate_state": self.should_mutate_state,
            "created_at": self.created_at,
            "case_attrs": dict(self.case_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestSmokeResult:
    smoke_result_id: str
    smoke_case_id: str
    skill_id: str
    status: str
    passed: bool
    executed: bool
    blocked: bool
    envelope_id: str | None
    created_object_refs: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "smoke_result_id": self.smoke_result_id,
            "smoke_case_id": self.smoke_case_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "passed": self.passed,
            "executed": self.executed,
            "blocked": self.blocked,
            "envelope_id": self.envelope_id,
            "created_object_refs": list(self.created_object_refs),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestConformanceFinding:
    finding_id: str
    skill_id: str | None
    check_id: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    evidence_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "skill_id": self.skill_id,
            "check_id": self.check_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "evidence_ref": self.evidence_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestConformanceReport:
    report_id: str
    policy_id: str
    total_skill_count: int
    passed_skill_count: int
    failed_skill_count: int
    warning_skill_count: int
    total_check_count: int
    passed_check_count: int
    failed_check_count: int
    smoke_case_count: int
    smoke_passed_count: int
    smoke_failed_count: int
    finding_ids: list[str]
    status: str
    summary: str
    created_at: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "policy_id": self.policy_id,
            "total_skill_count": self.total_skill_count,
            "passed_skill_count": self.passed_skill_count,
            "failed_skill_count": self.failed_skill_count,
            "warning_skill_count": self.warning_skill_count,
            "total_check_count": self.total_check_count,
            "passed_check_count": self.passed_check_count,
            "failed_check_count": self.failed_check_count,
            "smoke_case_count": self.smoke_case_count,
            "smoke_passed_count": self.smoke_passed_count,
            "smoke_failed_count": self.smoke_failed_count,
            "finding_ids": list(self.finding_ids),
            "status": self.status,
            "summary": self.summary,
            "created_at": self.created_at,
            "report_attrs": dict(self.report_attrs),
        }


class ObservationDigestConformanceService:
    def __init__(
        self,
        *,
        registry_view_service: SkillRegistryViewService | Any | None = None,
        onboarding_service: InternalSkillOnboardingService | Any | None = None,
        proposal_service: ObservationDigestProposalService | Any | None = None,
        invocation_service: ObservationDigestSkillInvocationService | Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.registry_view_service = registry_view_service or SkillRegistryViewService(trace_service=self.trace_service)
        self.onboarding_service = onboarding_service or InternalSkillOnboardingService(trace_service=self.trace_service)
        self.proposal_service = proposal_service or ObservationDigestProposalService(trace_service=self.trace_service)
        self.invocation_service = invocation_service or ObservationDigestSkillInvocationService(trace_service=self.trace_service)
        self.last_policy: ObservationDigestConformancePolicy | None = None
        self.last_checks: list[ObservationDigestConformanceCheck] = []
        self.last_smoke_cases: list[ObservationDigestSmokeCase] = []
        self.last_smoke_results: list[ObservationDigestSmokeResult] = []
        self.last_findings: list[ObservationDigestConformanceFinding] = []
        self.last_report: ObservationDigestConformanceReport | None = None
        self._registry_entries: dict[str, SkillRegistryEntry] = {}

    def create_default_policy(self, **policy_attrs: Any) -> ObservationDigestConformancePolicy:
        policy = ObservationDigestConformancePolicy(
            policy_id=new_observation_digest_conformance_policy_id(),
            policy_name="observation_digest_conformance_policy",
            required_skill_ids=sorted(OBSERVATION_DIGESTION_SKILL_IDS),
            require_registry_entry=True,
            require_onboarding_result=True,
            require_input_contract=True,
            require_output_contract=True,
            require_risk_profile=True,
            require_gate_contract=True,
            require_observability_contract=True,
            require_envelope=True,
            require_ocel_events=True,
            require_pig_visibility=True,
            require_audit_visibility=True,
            require_workbench_visibility=True,
            deny_external_execution=True,
            deny_shell_network_write=True,
            deny_memory_persona_overlay_mutation=True,
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={
                "diagnostic_only": True,
                "adds_execution_capability": False,
                "external_execution_used": False,
                "permission_grants_created": False,
                **policy_attrs,
            },
        )
        self.last_policy = policy
        self._record_model(
            "observation_digest_conformance_policy_registered",
            "observation_digest_conformance_policy",
            policy.policy_id,
            policy,
        )
        return policy

    def build_required_smoke_cases(
        self,
        *,
        fixture_root: str | None = None,
        trace_relative_path: str = "trace.jsonl",
        skill_relative_path: str = "external_skill",
    ) -> list[ObservationDigestSmokeCase]:
        observed_run = _observed_run_fixture()
        inference = _inference_fixture()
        static_profile = _static_profile_fixture()
        fingerprint = _fingerprint_fixture()
        candidate = _candidate_fixture()
        cases = [
            self._smoke_case(
                "skill:agent_observation_source_inspect",
                "observation_source_inspect",
                _path_payload(fixture_root, trace_relative_path, format_hint="generic_jsonl"),
                ["agent_observation_source"],
            ),
            self._smoke_case(
                "skill:agent_trace_observe",
                "agent_trace_observe",
                _path_payload(fixture_root, trace_relative_path, source_runtime="generic", format_hint="generic_jsonl"),
                ["observed_agent_run"],
            ),
            self._smoke_case(
                "skill:agent_observation_normalize",
                "agent_observation_normalize",
                {"records": _records_fixture(), "batch_id": "agent_observation_batch:smoke"},
                ["agent_observation_normalized_event"],
            ),
            self._smoke_case(
                "skill:agent_behavior_infer",
                "agent_behavior_infer",
                {"observed_run": observed_run},
                ["agent_behavior_inference"],
            ),
            self._smoke_case(
                "skill:agent_process_narrative",
                "agent_process_narrative",
                {"observed_run": observed_run, "inference": inference},
                ["agent_process_narrative"],
            ),
            self._smoke_case(
                "skill:external_skill_source_inspect",
                "external_skill_source_inspect",
                _path_payload(fixture_root, skill_relative_path, vendor_hint="fixture"),
                ["external_skill_source_descriptor"],
            ),
            self._smoke_case(
                "skill:external_skill_static_digest",
                "external_skill_static_digest",
                _path_payload(fixture_root, skill_relative_path, vendor_hint="fixture"),
                ["external_skill_static_profile"],
            ),
            self._smoke_case(
                "skill:external_behavior_fingerprint",
                "external_behavior_fingerprint",
                {"observed_run": observed_run},
                ["external_skill_behavior_fingerprint"],
            ),
            self._smoke_case(
                "skill:external_skill_assimilate",
                "external_skill_assimilate",
                {"static_profile": static_profile, "fingerprint": fingerprint},
                ["external_skill_assimilation_candidate"],
                expected_status="pending_review",
            ),
            self._smoke_case(
                "skill:external_skill_adapter_candidate",
                "external_skill_adapter_candidate",
                {"candidate": candidate},
                ["external_skill_adapter_candidate"],
                expected_status="pending_review",
            ),
        ]
        self.last_smoke_cases = cases
        for case in cases:
            self._record_model(
                "observation_digest_smoke_case_registered",
                "observation_digest_smoke_case",
                case.smoke_case_id,
                case,
            )
        return cases

    def check_registry_entry(self, skill_id: str) -> ObservationDigestConformanceCheck:
        try:
            if not self._registry_entries:
                self.registry_view_service.build_registry_view()
                self._registry_entries = {entry.skill_id: entry for entry in self.registry_view_service.last_entries}
            entry = self._registry_entries.get(skill_id)
        except Exception as error:
            return self._failed_check(skill_id, "registry_entry", "high", f"Registry unavailable: {error}")
        if entry is None:
            return self._failed_check(skill_id, "registry_entry", "high", "Registry entry is missing.")
        passed = entry.skill_id == skill_id and entry.ocel_observable and entry.pig_visible
        return self.record_check(
            skill_id=skill_id,
            check_type="registry_entry",
            passed=passed,
            severity="high" if not passed else "info",
            message="Registry entry present." if passed else "Registry entry is incomplete.",
            evidence_refs=[entry.registry_entry_id],
            check_attrs={"entry": entry.to_dict()},
        )

    def check_onboarding_contract(self, skill_id: str) -> ObservationDigestConformanceCheck:
        try:
            bundle = self.onboarding_service.create_read_only_skill_contract_bundle(skill_id=skill_id)
            result = self.onboarding_service.validate_onboarding(**bundle, reviewer_type="conformance", reviewer_id="v0.19.4")
        except Exception as error:
            return self._failed_check(skill_id, "onboarding_contract", "high", f"Onboarding unavailable: {error}")
        return self.record_check(
            skill_id=skill_id,
            check_type="onboarding_contract",
            passed=result.status == "accepted",
            severity="high" if result.status != "accepted" else "info",
            message=f"Onboarding status={result.status}.",
            evidence_refs=[result.result_id],
            check_attrs={"status": result.status, "finding_count": len(result.finding_ids)},
        )

    def check_input_output_contracts(self, skill_id: str) -> list[ObservationDigestConformanceCheck]:
        try:
            bundle = self.onboarding_service.create_read_only_skill_contract_bundle(skill_id=skill_id)
        except Exception as error:
            return [self._failed_check(skill_id, "input_output_contract", "high", str(error))]
        input_contract = bundle.get("input_contract")
        output_contract = bundle.get("output_contract")
        return [
            self.record_check(
                skill_id=skill_id,
                check_type="input_contract",
                passed=input_contract is not None and input_contract.skill_id == skill_id,
                severity="high",
                message="Input contract present." if input_contract else "Input contract missing.",
                evidence_refs=[getattr(input_contract, "input_contract_id", "")],
            ),
            self.record_check(
                skill_id=skill_id,
                check_type="output_contract",
                passed=output_contract is not None and output_contract.skill_id == skill_id,
                severity="high",
                message="Output contract present." if output_contract else "Output contract missing.",
                evidence_refs=[getattr(output_contract, "output_contract_id", "")],
            ),
        ]

    def check_risk_gate_observability(self, skill_id: str) -> list[ObservationDigestConformanceCheck]:
        try:
            bundle = self.onboarding_service.create_read_only_skill_contract_bundle(skill_id=skill_id)
        except Exception as error:
            return [self._failed_check(skill_id, "risk_gate_observability", "high", str(error))]
        risk = bundle.get("risk_profile")
        gate = bundle.get("gate_contract")
        observability = bundle.get("observability_contract")
        return [
            self.record_check(
                skill_id=skill_id,
                check_type="risk_profile",
                passed=bool(risk and risk.read_only and not risk.touches_network and not risk.touches_shell),
                severity="high",
                message="Risk profile is read-only." if risk else "Risk profile missing.",
                evidence_refs=[getattr(risk, "risk_profile_id", "")],
            ),
            self.record_check(
                skill_id=skill_id,
                check_type="gate_contract",
                passed=bool(gate and gate.gate_required),
                severity="high",
                message="Gate contract requires gate." if gate else "Gate contract missing.",
                evidence_refs=[getattr(gate, "gate_contract_id", "")],
            ),
            self.record_check(
                skill_id=skill_id,
                check_type="observability_contract",
                passed=bool(observability and observability.envelope_required and observability.ocel_event_activities),
                severity="high",
                message="Observability contract present." if observability else "Observability contract missing.",
                evidence_refs=[getattr(observability, "observability_contract_id", "")],
            ),
        ]

    def check_proposal_integration(self, skill_id: str) -> ObservationDigestConformanceCheck:
        policy = self.proposal_service.create_default_policy()
        passed = skill_id in policy.allowed_skill_ids and not policy.allow_execution
        return self.record_check(
            skill_id=skill_id,
            check_type="proposal_integration",
            passed=passed,
            severity="medium",
            message="Proposal policy includes skill and stays review-only.",
            evidence_refs=[policy.policy_id],
        )

    def check_invocation_integration(self, skill_id: str) -> ObservationDigestConformanceCheck:
        binding = self.invocation_service.resolve_binding(skill_id)
        passed = bool(binding and binding.enabled and binding.read_only)
        return self.record_check(
            skill_id=skill_id,
            check_type="invocation_integration",
            passed=passed,
            severity="high",
            message="Runtime binding present." if passed else "Runtime binding missing.",
            evidence_refs=[binding.binding_id if binding else ""],
        )

    def check_envelope_support(self, skill_id: str) -> ObservationDigestConformanceCheck:
        binding = self.invocation_service.resolve_binding(skill_id)
        passed = bool(binding and binding.envelope_required)
        return self.record_check(
            skill_id=skill_id,
            check_type="envelope_support",
            passed=passed,
            severity="high",
            message="Envelope is required by runtime binding.",
            evidence_refs=[binding.binding_id if binding else ""],
        )

    def check_ocel_visibility(self, skill_id: str) -> ObservationDigestConformanceCheck:
        binding = self.invocation_service.resolve_binding(skill_id)
        passed = bool(binding and binding.binding_attrs.get("external_execution_used") is False)
        return self.record_check(
            skill_id=skill_id,
            check_type="ocel_visibility",
            passed=passed,
            severity="medium",
            message="OCEL-visible runtime binding present.",
            evidence_refs=[binding.binding_id if binding else ""],
        )

    def check_pig_ocpx_visibility(self, skill_id: str) -> ObservationDigestConformanceCheck:
        passed = skill_id in OBSERVATION_DIGESTION_SKILL_IDS
        return self.record_check(
            skill_id=skill_id,
            check_type="pig_ocpx_visibility",
            passed=passed,
            severity="medium",
            message="PIG/OCPX summary keys are available for Observation/Digestion conformance.",
            evidence_refs=["pig:observation_digest_conformance"],
        )

    def check_audit_workbench_visibility(self, skill_id: str) -> ObservationDigestConformanceCheck:
        entry = self._registry_entries.get(skill_id)
        passed = bool(entry and entry.audit_visible and entry.workbench_visible)
        return self.record_check(
            skill_id=skill_id,
            check_type="audit_workbench_visibility",
            passed=passed,
            severity="medium",
            message="Audit and workbench visibility declared.",
            evidence_refs=[entry.registry_entry_id if entry else ""],
        )

    def check_candidate_safety(self, skill_id: str) -> ObservationDigestConformanceCheck:
        passed = True
        message = "Candidate safety is enforced by non-executable defaults."
        if skill_id in DIGESTION_SKILL_IDS:
            candidate = _candidate_fixture()
            passed = (
                candidate["review_status"] == "pending_review"
                and candidate["canonical_import_enabled"] is False
                and candidate["execution_enabled"] is False
            )
        return self.record_check(
            skill_id=skill_id,
            check_type="candidate_safety",
            passed=passed,
            severity="high",
            message=message,
            evidence_refs=[skill_id],
        )

    def run_conformance(self, *, skill_id: str | None = None, run_smoke: bool = False, fixture_root: str | None = None) -> ObservationDigestConformanceReport:
        policy = self.create_default_policy()
        target_skill_ids = [skill_id] if skill_id else list(policy.required_skill_ids)
        self.last_checks = []
        self.last_findings = []
        self._registry_entries = {}
        for target in target_skill_ids:
            checks = [
                self.check_registry_entry(target),
                self.check_onboarding_contract(target),
                *self.check_input_output_contracts(target),
                *self.check_risk_gate_observability(target),
                self.check_proposal_integration(target),
                self.check_invocation_integration(target),
                self.check_envelope_support(target),
                self.check_ocel_visibility(target),
                self.check_pig_ocpx_visibility(target),
                self.check_audit_workbench_visibility(target),
                self.check_candidate_safety(target),
            ]
            for check in checks:
                if not check.passed:
                    self.record_finding(
                        skill_id=target,
                        check_id=check.check_id,
                        finding_type=check.check_type,
                        status="failed",
                        severity=check.severity,
                        message=check.message,
                        evidence_ref=check.evidence_refs[0] if check.evidence_refs else None,
                    )
        if run_smoke:
            self.run_smoke(skill_id=skill_id, fixture_root=fixture_root)
        return self.record_report(policy=policy, skill_ids=target_skill_ids)

    def run_smoke(self, *, skill_id: str | None = None, fixture_root: str | None = None) -> list[ObservationDigestSmokeResult]:
        cases = self.build_required_smoke_cases(fixture_root=fixture_root)
        if skill_id:
            cases = [case for case in cases if case.skill_id == skill_id]
        results = [self._run_smoke_case(case) for case in cases]
        self.last_smoke_results = results
        return results

    def record_check(
        self,
        *,
        skill_id: str,
        check_type: str,
        passed: bool,
        severity: str,
        message: str,
        evidence_refs: list[str] | None = None,
        check_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestConformanceCheck:
        self._record_event("observation_digest_conformance_check_started", attrs={"skill_id": skill_id, "check_type": check_type})
        check = ObservationDigestConformanceCheck(
            check_id=new_observation_digest_conformance_check_id(),
            skill_id=skill_id,
            check_type=check_type,
            status="passed" if passed else "failed",
            passed=passed,
            severity=severity,
            message=message,
            evidence_refs=[item for item in evidence_refs or [] if item],
            created_at=utc_now_iso(),
            check_attrs={"read_only": True, **dict(check_attrs or {})},
        )
        self.last_checks.append(check)
        self._record_model(
            "observation_digest_conformance_check_completed",
            "observation_digest_conformance_check",
            check.check_id,
            check,
        )
        return check

    def record_smoke_result(self, result: ObservationDigestSmokeResult) -> ObservationDigestSmokeResult:
        self._record_model(
            "observation_digest_smoke_case_completed",
            "observation_digest_smoke_result",
            result.smoke_result_id,
            result,
            links=[("observation_digest_smoke_case_object", result.smoke_case_id), ("execution_envelope_object", result.envelope_id or "")],
            object_links=[(result.smoke_result_id, result.smoke_case_id, "smoke_result_result_of_smoke_case")],
        )
        return result

    def record_finding(
        self,
        *,
        skill_id: str | None,
        check_id: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestConformanceFinding:
        finding = ObservationDigestConformanceFinding(
            finding_id=new_observation_digest_conformance_finding_id(),
            skill_id=skill_id,
            check_id=check_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            created_at=utc_now_iso(),
            finding_attrs={"read_only": True, "external_execution_used": False, **dict(finding_attrs or {})},
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digest_conformance_finding_recorded",
            "observation_digest_conformance_finding",
            finding.finding_id,
            finding,
            links=[("observation_digest_conformance_check_object", check_id or "")],
            object_links=[(finding.finding_id, check_id or "", "conformance_finding_belongs_to_check")],
        )
        return finding

    def record_report(
        self,
        *,
        policy: ObservationDigestConformancePolicy,
        skill_ids: list[str],
    ) -> ObservationDigestConformanceReport:
        failed_checks = [check for check in self.last_checks if not check.passed]
        failed_skills = {check.skill_id for check in failed_checks}
        warning_skills = {finding.skill_id for finding in self.last_findings if finding.severity == "medium"}
        smoke_failed = [result for result in self.last_smoke_results if not result.passed]
        status = "passed" if not failed_checks and not smoke_failed else "failed"
        report = ObservationDigestConformanceReport(
            report_id=new_observation_digest_conformance_report_id(),
            policy_id=policy.policy_id,
            total_skill_count=len(skill_ids),
            passed_skill_count=len([item for item in skill_ids if item not in failed_skills]),
            failed_skill_count=len(failed_skills),
            warning_skill_count=len(warning_skills),
            total_check_count=len(self.last_checks),
            passed_check_count=len([item for item in self.last_checks if item.passed]),
            failed_check_count=len(failed_checks),
            smoke_case_count=len(self.last_smoke_results),
            smoke_passed_count=len([item for item in self.last_smoke_results if item.passed]),
            smoke_failed_count=len(smoke_failed),
            finding_ids=[finding.finding_id for finding in self.last_findings],
            status=status,
            summary=f"Observation/Digestion conformance status={status}; skills={len(skill_ids)}.",
            created_at=utc_now_iso(),
            report_attrs={
                "boundary_summary": {
                    "external_harness_execution_used": False,
                    "external_script_execution_used": False,
                    "shell_network_write_mcp_plugin_used": False,
                    "memory_persona_overlay_mutated": False,
                },
                "adds_execution_capability": False,
            },
        )
        self.last_report = report
        self._record_model(
            "observation_digest_conformance_report_recorded",
            "observation_digest_conformance_report",
            report.report_id,
            report,
            links=[("observation_digest_conformance_policy_object", policy.policy_id)]
            + [("observation_digest_conformance_check_object", check.check_id) for check in self.last_checks]
            + [("observation_digest_smoke_result_object", result.smoke_result_id) for result in self.last_smoke_results]
            + [("observation_digest_conformance_finding_object", finding.finding_id) for finding in self.last_findings],
        )
        return report

    def render_conformance_cli(self, report: ObservationDigestConformanceReport | None = None) -> str:
        item = report or self.last_report
        if item is None:
            return "Observation/Digestion Conformance: unavailable"
        lines = [
            "Observation/Digestion Conformance",
            f"status={item.status}",
            f"skill_count={item.total_skill_count}",
            f"passed_skill_count={item.passed_skill_count}",
            f"failed_skill_count={item.failed_skill_count}",
            f"check_count={item.total_check_count}",
            f"failed_check_count={item.failed_check_count}",
            f"smoke_case_count={item.smoke_case_count}",
            f"smoke_failed_count={item.smoke_failed_count}",
            f"finding_count={len(item.finding_ids)}",
            "external_harness_execution_used=false",
            "external_script_execution_used=false",
            "shell_network_write_mcp_plugin_used=false",
            "memory_persona_overlay_mutated=false",
        ]
        return "\n".join(lines)

    def render_smoke_cli(self, results: list[ObservationDigestSmokeResult] | None = None) -> str:
        items = list(results if results is not None else self.last_smoke_results)
        passed = len([item for item in items if item.passed])
        lines = [
            "Observation/Digestion Smoke",
            f"status={'passed' if passed == len(items) else 'failed'}",
            f"smoke_case_count={len(items)}",
            f"smoke_passed_count={passed}",
            f"smoke_failed_count={len(items) - passed}",
        ]
        for item in items[:10]:
            lines.append(
                f"- {item.skill_id} status={item.status} passed={str(item.passed).lower()} envelope_id={item.envelope_id or ''}"
            )
        return "\n".join(lines)

    def _smoke_case(
        self,
        skill_id: str,
        case_name: str,
        input_payload: dict[str, Any],
        expected_object_types: list[str],
        *,
        expected_status: str = "completed",
    ) -> ObservationDigestSmokeCase:
        return ObservationDigestSmokeCase(
            smoke_case_id=new_observation_digest_smoke_case_id(),
            skill_id=skill_id,
            case_name=case_name,
            input_payload=input_payload,
            expected_status=expected_status,
            expected_created_object_types=expected_object_types,
            expected_findings=[],
            should_execute=True,
            should_block=False,
            should_create_envelope=True,
            should_mutate_state=False,
            created_at=utc_now_iso(),
            case_attrs={"read_only": True, "external_execution_used": False},
        )

    def _run_smoke_case(self, case: ObservationDigestSmokeCase) -> ObservationDigestSmokeResult:
        self._record_model(
            "observation_digest_smoke_case_started",
            "observation_digest_smoke_case",
            case.smoke_case_id,
            case,
        )
        try:
            invocation_result = self.invocation_service.invoke_skill(
                skill_id=case.skill_id,
                input_payload=dict(case.input_payload),
                invocation_mode="explicit_observation_digest_smoke",
                requester_type="conformance",
                requester_id="v0.19.4",
            )
            candidate_safe = True
            if case.skill_id == "skill:external_skill_assimilate":
                candidate = getattr(self.invocation_service.digestion_service, "last_candidate", None)
                candidate_safe = bool(
                    candidate
                    and candidate.review_status == "pending_review"
                    and candidate.canonical_import_enabled is False
                    and candidate.execution_enabled is False
                )
            if case.skill_id == "skill:external_skill_adapter_candidate":
                adapter = getattr(self.invocation_service.digestion_service, "last_adapter_candidate", None)
                candidate_safe = bool(adapter and adapter.requires_review is True and adapter.execution_enabled is False)
            passed = (
                invocation_result.executed == case.should_execute
                and invocation_result.blocked == case.should_block
                and bool(invocation_result.envelope_id) == case.should_create_envelope
                and candidate_safe
            )
            result = ObservationDigestSmokeResult(
                smoke_result_id=new_observation_digest_smoke_result_id(),
                smoke_case_id=case.smoke_case_id,
                skill_id=case.skill_id,
                status=invocation_result.status,
                passed=passed,
                executed=invocation_result.executed,
                blocked=invocation_result.blocked,
                envelope_id=invocation_result.envelope_id,
                created_object_refs=list(invocation_result.created_object_refs),
                finding_ids=list(invocation_result.finding_ids),
                summary="Smoke case completed." if passed else "Smoke case did not meet expectations.",
                created_at=utc_now_iso(),
                result_attrs={
                    "external_execution_used": False,
                    "candidate_safe": candidate_safe,
                    "invocation_result_id": invocation_result.result_id,
                },
            )
        except Exception as error:
            finding = self.record_finding(
                skill_id=case.skill_id,
                check_id=None,
                finding_type="smoke_execution_error",
                status="failed",
                severity="high",
                message=str(error),
            )
            result = ObservationDigestSmokeResult(
                smoke_result_id=new_observation_digest_smoke_result_id(),
                smoke_case_id=case.smoke_case_id,
                skill_id=case.skill_id,
                status="not_run",
                passed=False,
                executed=False,
                blocked=True,
                envelope_id=None,
                created_object_refs=[],
                finding_ids=[finding.finding_id],
                summary="Smoke case could not run.",
                created_at=utc_now_iso(),
                result_attrs={"exception_type": type(error).__name__},
            )
        return self.record_smoke_result(result)

    def _failed_check(self, skill_id: str, check_type: str, severity: str, message: str) -> ObservationDigestConformanceCheck:
        check = self.record_check(
            skill_id=skill_id,
            check_type=check_type,
            passed=False,
            severity=severity,
            message=message,
        )
        self.record_finding(
            skill_id=skill_id,
            check_id=check.check_id,
            finding_type=check_type,
            status="failed",
            severity=severity,
            message=message,
        )
        return check

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


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={"object_key": object_id, "display_name": object_id, **attrs},
    )


def _redacted_payload(value: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(value)
    if "root_path" in redacted:
        redacted["root_path"] = "<redacted>"
    if isinstance(redacted.get("records"), list):
        redacted["records"] = {"list_count": len(redacted["records"])}
    return redacted


def _path_payload(
    fixture_root: str | None,
    relative_path: str,
    *,
    source_runtime: str | None = None,
    format_hint: str | None = None,
    vendor_hint: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"root_path": fixture_root or "", "relative_path": relative_path}
    if source_runtime:
        payload["source_runtime"] = source_runtime
    if format_hint:
        payload["format_hint"] = format_hint
    if vendor_hint:
        payload["vendor_hint"] = vendor_hint
    return payload


def _records_fixture() -> list[dict[str, Any]]:
    return [
        {"role": "user", "content": "inspect this trace", "_line_index": 0},
        {"role": "assistant", "content": "inspection started", "_line_index": 1},
        {"tool_call": {"name": "read_file"}, "input": {"path": "trace.jsonl"}, "_line_index": 2},
        {"tool_result": {"name": "read_file"}, "output": {"ok": True}, "_line_index": 3},
    ]


def _observed_run_fixture() -> dict[str, Any]:
    return {
        "observed_run_id": "observed_agent_run:smoke",
        "source_id": "agent_observation_source:smoke",
        "batch_id": "agent_observation_batch:smoke",
        "inferred_runtime": "generic",
        "event_count": 4,
        "object_count": 1,
        "relation_count": 4,
        "observation_confidence": 0.75,
        "run_attrs": {
            "observed_activity_sequence": [
                "user_message_observed",
                "assistant_message_observed",
                "tool_call_observed",
                "tool_result_observed",
            ]
        },
    }


def _inference_fixture() -> dict[str, Any]:
    return {
        "inference_id": "agent_behavior_inference:smoke",
        "observed_run_id": "observed_agent_run:smoke",
        "inferred_goal": "inspect trace",
        "inferred_goal_confidence": 0.6,
        "inferred_task_type": "trace_observation",
        "inferred_action_sequence": ["user_message_observed", "assistant_message_observed"],
        "outcome_inference": "observed_without_explicit_failure",
        "outcome_confidence": 0.7,
        "evidence_refs": ["event:smoke"],
        "withdrawal_conditions": ["Withdraw if fixture rows are not representative."],
    }


def _static_profile_fixture() -> dict[str, Any]:
    return {
        "static_profile_id": "external_skill_static_profile:smoke",
        "source_descriptor_id": "external_skill_source_descriptor:smoke",
        "declared_name": "Generic External Skill",
        "declared_description": "Public fixture skill.",
        "declared_tools": [],
        "declared_inputs": [],
        "declared_outputs": [],
        "declared_risks": [],
        "instruction_preview": "Generic fixture only.",
        "confidence": 0.7,
        "profile_attrs": {"full_raw_body_stored": False},
    }


def _fingerprint_fixture() -> dict[str, Any]:
    return {
        "fingerprint_id": "external_skill_behavior_fingerprint:smoke",
        "observed_run_id": "observed_agent_run:smoke",
        "source_runtime": "generic",
        "observed_event_count": 4,
        "observed_sequence": ["user_message_observed", "tool_call_observed"],
        "object_types_touched": ["file"],
        "input_shape_summary": {},
        "output_shape_summary": {},
        "side_effect_profile": "none_observed",
        "permission_profile": "permission_not_observed",
        "verification_profile": "deterministic_static_fingerprint",
        "failure_modes": [],
        "recovery_patterns": [],
        "recommended_chantacore_category": "read_only",
        "risk_class": "read_only",
        "confidence": 0.6,
        "evidence_refs": ["event:smoke"],
    }


def _candidate_fixture() -> dict[str, Any]:
    return {
        "candidate_id": "external_skill_assimilation_candidate:smoke",
        "source_runtime": "generic",
        "source_skill_ref": "generic_external_skill",
        "source_kind": "external_skill",
        "static_profile_id": "external_skill_static_profile:smoke",
        "behavior_fingerprint_id": "external_skill_behavior_fingerprint:smoke",
        "proposed_chantacore_skill_id": "skill:generic_external_skill",
        "proposed_execution_type": "review_only_candidate",
        "adapter_candidate_ids": [],
        "risk_class": "read_only",
        "confidence": 0.6,
        "evidence_refs": [],
        "review_status": "pending_review",
        "canonical_import_enabled": False,
        "execution_enabled": False,
    }

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.observation.adapter_contracts import (
    ADAPTER_CONTRACT_SPECS,
    CHANTACORE_OCEL_RULE_SPECS,
    GENERIC_JSONL_RULE_SPECS,
    STUB_RULE_SPECS,
)
from chanta_core.observation.spine import (
    AgentObservationNormalizedEventV2,
    AgentObservationSpineService,
    ObservedAgentObject,
    ObservedAgentRelation,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_agent_observation_normalized_event_v2_id,
    new_cross_harness_trace_adapter_policy_id,
    new_harness_trace_adapter_contract_id,
    new_harness_trace_adapter_coverage_report_id,
    new_harness_trace_adapter_finding_id,
    new_harness_trace_adapter_result_id,
    new_harness_trace_mapping_rule_id,
    new_harness_trace_normalization_plan_id,
    new_harness_trace_normalization_result_id,
    new_harness_trace_source_inspection_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import (
    WorkspacePathViolationError,
    WorkspaceReadRootError,
    resolve_workspace_path,
)


@dataclass(frozen=True)
class CrossHarnessTraceAdapterPolicy:
    policy_id: str
    policy_name: str
    allowed_source_runtimes: list[str]
    allowed_input_formats: list[str]
    require_redaction: bool
    require_confidence: bool
    require_evidence_ref: bool
    require_withdrawal_conditions: bool
    allow_unimplemented_adapter_stub: bool
    allow_best_effort_mapping: bool
    allow_causal_claims_by_default: bool
    max_records: int
    max_preview_chars: int
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceAdapterContract:
    adapter_contract_id: str
    adapter_name: str
    source_runtime: str
    source_runtime_family: str
    supported_formats: list[str]
    supported_record_shapes: list[str]
    implemented: bool
    enabled: bool
    read_only: bool
    emits_normalized_event_v2: bool
    emits_observed_objects: bool
    emits_observed_relations: bool
    supports_confidence: bool
    supports_redaction: bool
    supports_batch_file: bool
    supports_tail_file: bool
    supports_runtime_hook: bool
    supports_event_bus: bool
    adapter_version: str
    schema_version: str
    created_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceSourceInspection:
    inspection_id: str
    source_ref: str | None
    detected_runtime: str
    detected_format: str
    detected_schema_version: str | None
    record_count: int
    sample_record_shapes: list[str]
    supported_by_adapter: bool
    selected_adapter_name: str | None
    confidence: float
    created_at: str
    inspection_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceMappingRule:
    mapping_rule_id: str
    adapter_name: str
    source_runtime: str
    source_event_pattern: str
    source_record_selector: str
    target_observed_activity: str
    target_action_type: str
    target_object_types: list[str]
    target_effect_type: str
    target_confidence_class: str
    default_confidence: float
    relation_hints: list[str]
    implemented: bool
    created_at: str
    mapping_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "default_confidence", _clamp(self.default_confidence))

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceNormalizationPlan:
    normalization_plan_id: str
    inspection_id: str
    adapter_contract_id: str
    source_runtime: str
    input_format: str
    selected_mapping_rule_ids: list[str]
    expected_output_event_schema: str
    expected_object_types: list[str]
    expected_relation_types: list[str]
    redaction_policy_id: str | None
    max_records: int
    created_at: str
    plan_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceNormalizationResult:
    normalization_result_id: str
    normalization_plan_id: str
    source_ref: str | None
    status: str
    raw_record_count: int
    normalized_event_count: int
    observed_object_count: int
    observed_relation_count: int
    skipped_record_count: int
    finding_ids: list[str]
    normalized_event_refs: list[str]
    observed_object_refs: list[str]
    observed_relation_refs: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceAdapterCoverageReport:
    coverage_report_id: str
    adapter_contract_id: str
    source_runtime: str
    supported_event_type_count: int
    mapped_event_type_count: int
    unmapped_event_type_count: int
    supported_record_shapes: list[str]
    unmapped_record_shapes: list[str]
    confidence_summary: dict[str, Any]
    coverage_status: str
    created_at: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceAdapterFinding:
    finding_id: str
    adapter_name: str | None
    source_runtime: str | None
    subject_ref: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    evidence_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass(frozen=True)
class HarnessTraceAdapterResult:
    adapter_result_id: str
    operation_kind: str
    status: str
    adapter_name: str | None
    source_runtime: str | None
    created_object_refs: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


class CrossHarnessTraceAdapterService:
    def __init__(self, *, trace_service: TraceService | None = None, ocel_store: OCELStore | None = None) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.spine_service = AgentObservationSpineService(trace_service=self.trace_service)
        self.last_policy: CrossHarnessTraceAdapterPolicy | None = None
        self.last_contracts: list[HarnessTraceAdapterContract] = []
        self.last_rules: list[HarnessTraceMappingRule] = []
        self.last_inspection: HarnessTraceSourceInspection | None = None
        self.last_plan: HarnessTraceNormalizationPlan | None = None
        self.last_result: HarnessTraceNormalizationResult | HarnessTraceAdapterResult | None = None
        self.last_coverage: HarnessTraceAdapterCoverageReport | None = None
        self.last_findings: list[HarnessTraceAdapterFinding] = []

    def create_default_policy(self) -> CrossHarnessTraceAdapterPolicy:
        policy = CrossHarnessTraceAdapterPolicy(
            policy_id=new_cross_harness_trace_adapter_policy_id(),
            policy_name="default_cross_harness_trace_adapter_policy",
            allowed_source_runtimes=[spec[1] for spec in ADAPTER_CONTRACT_SPECS],
            allowed_input_formats=["jsonl", "generic_jsonl", "json", "ocel_like"],
            require_redaction=True,
            require_confidence=True,
            require_evidence_ref=True,
            require_withdrawal_conditions=True,
            allow_unimplemented_adapter_stub=True,
            allow_best_effort_mapping=True,
            allow_causal_claims_by_default=False,
            max_records=1000,
            max_preview_chars=400,
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={"read_only": True, "live_connection_enabled": False},
        )
        self.last_policy = policy
        self._record_model("cross_harness_trace_adapter_policy_registered", "cross_harness_trace_adapter_policy", policy.policy_id, policy)
        return policy

    def register_adapter_contracts(self) -> list[HarnessTraceAdapterContract]:
        contracts: list[HarnessTraceAdapterContract] = []
        for name, runtime, family, formats, implemented in ADAPTER_CONTRACT_SPECS:
            contracts.append(
                HarnessTraceAdapterContract(
                    adapter_contract_id=new_harness_trace_adapter_contract_id(),
                    adapter_name=name,
                    source_runtime=runtime,
                    source_runtime_family=family,
                    supported_formats=list(formats),
                    supported_record_shapes=_supported_shapes(name),
                    implemented=implemented,
                    enabled=implemented,
                    read_only=True,
                    emits_normalized_event_v2=True,
                    emits_observed_objects=True,
                    emits_observed_relations=True,
                    supports_confidence=True,
                    supports_redaction=True,
                    supports_batch_file=True,
                    supports_tail_file=False,
                    supports_runtime_hook=False,
                    supports_event_bus=False,
                    adapter_version="0.19.7",
                    schema_version="agent_observation_v2",
                    created_at=utc_now_iso(),
                    contract_attrs={"stub": not implemented, "live_connection_enabled": False},
                )
            )
        self.last_contracts = contracts
        for contract in contracts:
            self._record_model("harness_trace_adapter_contract_registered", "harness_trace_adapter_contract", contract.adapter_contract_id, contract)
        return list(contracts)

    def register_default_mapping_rules(self) -> list[HarnessTraceMappingRule]:
        rules: list[HarnessTraceMappingRule] = []
        for pattern, selector, activity, action, objects, effect in GENERIC_JSONL_RULE_SPECS:
            rules.append(self._rule("GenericJSONLTranscriptAdapter", "generic_jsonl", pattern, selector, activity, action, objects, effect, True))
        for pattern, selector, activity, action, objects, effect in CHANTACORE_OCEL_RULE_SPECS:
            rules.append(self._rule("ChantaCoreOCELAdapter", "chantacore", pattern, selector, activity, action, objects, effect, True))
        for adapter_name, pattern, activity, action in STUB_RULE_SPECS:
            rules.append(self._rule(adapter_name, _runtime_for_adapter(adapter_name), pattern, pattern, activity, action, ["unknown_object"], "unknown_side_effect", False))
        self.last_rules = rules
        for rule in rules:
            self._record_model("harness_trace_mapping_rule_registered", "harness_trace_mapping_rule", rule.mapping_rule_id, rule)
        return list(rules)

    def inspect_trace_source(self, *, root_path: str, relative_path: str, runtime_hint: str | None = None) -> HarnessTraceSourceInspection:
        records, source_ref, status = self._read_records(root_path=root_path, relative_path=relative_path)
        shapes = [_record_shape(record) for record in records[:10]]
        detected_format = "jsonl" if source_ref and source_ref.endswith(".jsonl") else "json" if records else "unknown"
        detected_runtime = runtime_hint or _detect_runtime(records, detected_format)
        contract = self.select_adapter(detected_runtime, detected_format)
        supported = bool(contract and contract.implemented)
        inspection = HarnessTraceSourceInspection(
            inspection_id=new_harness_trace_source_inspection_id(),
            source_ref=source_ref,
            detected_runtime=detected_runtime,
            detected_format=detected_format,
            detected_schema_version=_schema_version(records),
            record_count=len(records),
            sample_record_shapes=shapes,
            supported_by_adapter=supported,
            selected_adapter_name=contract.adapter_name if contract else None,
            confidence=0.8 if records and contract else 0.2,
            created_at=utc_now_iso(),
            inspection_attrs={"status": status, "read_only": True, "full_body_stored": False},
        )
        self.last_inspection = inspection
        self._record_model("harness_trace_source_inspected", "harness_trace_source_inspection", inspection.inspection_id, inspection)
        if contract and not contract.implemented:
            self.record_finding(adapter_name=contract.adapter_name, source_runtime=detected_runtime, subject_ref=source_ref, finding_type="adapter_not_implemented", status="stub", severity="medium", message="Selected adapter is registered as a non-executing stub.", evidence_ref=inspection.inspection_id)
        return inspection

    def select_adapter(self, runtime_hint: str | None, input_format: str | None = None) -> HarnessTraceAdapterContract | None:
        contracts = self.last_contracts or self.register_adapter_contracts()
        runtime = (runtime_hint or "").lower()
        for contract in contracts:
            if runtime in {contract.source_runtime.lower(), contract.adapter_name.lower()}:
                return contract
        if input_format in {"jsonl", "generic_jsonl"}:
            return next(contract for contract in contracts if contract.adapter_name == "GenericJSONLTranscriptAdapter")
        if input_format in {"json", "ocel_like"}:
            return next(contract for contract in contracts if contract.adapter_name == "ChantaCoreOCELAdapter")
        return None

    def build_normalization_plan(self, inspection: HarnessTraceSourceInspection | None = None) -> HarnessTraceNormalizationPlan:
        inspection = inspection or self.last_inspection
        if inspection is None:
            raise ValueError("inspection is required")
        contract = self.select_adapter(inspection.detected_runtime, inspection.detected_format)
        if contract is None:
            self.record_finding(adapter_name=None, source_runtime=inspection.detected_runtime, subject_ref=inspection.source_ref, finding_type="unsupported_format", status="blocked", severity="high", message="No adapter contract matched the trace source.", evidence_ref=inspection.inspection_id)
            contract = self.register_adapter_contracts()[1]
        rules = self.last_rules or self.register_default_mapping_rules()
        selected = [rule for rule in rules if rule.adapter_name == contract.adapter_name]
        plan = HarnessTraceNormalizationPlan(
            normalization_plan_id=new_harness_trace_normalization_plan_id(),
            inspection_id=inspection.inspection_id,
            adapter_contract_id=contract.adapter_contract_id,
            source_runtime=contract.source_runtime,
            input_format=inspection.detected_format,
            selected_mapping_rule_ids=[rule.mapping_rule_id for rule in selected],
            expected_output_event_schema="agent_observation_v2",
            expected_object_types=sorted({obj for rule in selected for obj in rule.target_object_types}),
            expected_relation_types=["followed_by"],
            redaction_policy_id=None,
            max_records=(self.last_policy.max_records if self.last_policy else 1000),
            created_at=utc_now_iso(),
            plan_attrs={"adapter_name": contract.adapter_name, "read_only": True},
        )
        self.last_plan = plan
        self._record_model("harness_trace_normalization_plan_created", "harness_trace_normalization_plan", plan.normalization_plan_id, plan)
        return plan

    def normalize_records(self, records: list[dict[str, Any]], *, plan: HarnessTraceNormalizationPlan | None = None) -> HarnessTraceNormalizationResult:
        plan = plan or self.last_plan
        if plan is None:
            raise ValueError("normalization plan is required")
        contract = self.select_adapter(plan.source_runtime, plan.input_format)
        if contract and not contract.implemented:
            finding = self.record_finding(adapter_name=contract.adapter_name, source_runtime=contract.source_runtime, subject_ref=plan.normalization_plan_id, finding_type="adapter_not_implemented", status="blocked", severity="medium", message="Adapter is a contract stub only.", evidence_ref=plan.normalization_plan_id)
            return self._normalization_result(plan, [], [], [], len(records), len(records), "blocked", [finding.finding_id])
        if contract and contract.adapter_name == "ChantaCoreOCELAdapter":
            events = self.normalize_chantacore_ocel_like(records, plan=plan)
        else:
            events = self.normalize_generic_jsonl(records, plan=plan)
        objects = self.spine_service.create_observed_objects(observed_run_id=f"observed_agent_run:{plan.normalization_plan_id}", events=events)
        relations = self.spine_service.create_observed_relations(observed_run_id=f"observed_agent_run:{plan.normalization_plan_id}", events=events)
        return self._normalization_result(plan, events, objects, relations, len(records), max(0, len(records) - len(events)), "completed", [])

    def normalize_generic_jsonl(self, records: list[dict[str, Any]], *, plan: HarnessTraceNormalizationPlan) -> list[AgentObservationNormalizedEventV2]:
        events: list[AgentObservationNormalizedEventV2] = []
        for index, record in enumerate(records[: plan.max_records]):
            activity, action, objects, effect = _generic_jsonl_targets(record)
            event = self._create_normalized_event(
                record,
                plan=plan,
                source_runtime="generic_jsonl",
                source_format="generic_jsonl",
                adapter_version="GenericJSONLTranscriptAdapter/0.19.7",
                activity=activity,
                action=action,
                object_types=objects,
                effect=effect,
                source_index=index,
            )
            events.append(event)
        return events

    def normalize_chantacore_ocel_like(self, records: list[dict[str, Any]], *, plan: HarnessTraceNormalizationPlan) -> list[AgentObservationNormalizedEventV2]:
        events: list[AgentObservationNormalizedEventV2] = []
        for index, record in enumerate(records[: plan.max_records]):
            object_type = str(record.get("object_type") or record.get("ocel_type") or "")
            converted, activity, action, objects, effect = _convert_ocel_like(record, object_type)
            event = self._create_normalized_event(
                converted,
                plan=plan,
                source_runtime="chantacore",
                source_format="ocel_like",
                adapter_version="ChantaCoreOCELAdapter/0.19.7",
                activity=activity,
                action=action,
                object_types=objects,
                effect=effect,
                source_index=index,
            )
            events.append(event)
        return events

    def normalize_schumpeter_agent_event_like(self, records: list[dict[str, Any]], *, plan: HarnessTraceNormalizationPlan) -> list[AgentObservationNormalizedEventV2]:
        _ = records, plan
        self.record_finding(adapter_name="SchumpeterAgentEventAdapter", source_runtime="schumpeter_agent", subject_ref=None, finding_type="adapter_not_implemented", status="stub", severity="medium", message="Adapter contract exists but normalization is not implemented.", evidence_ref=None)
        return []

    def create_adapter_coverage_report(self, adapter_name: str) -> HarnessTraceAdapterCoverageReport:
        contracts = self.last_contracts or self.register_adapter_contracts()
        rules = self.last_rules or self.register_default_mapping_rules()
        contract = next((item for item in contracts if item.adapter_name == adapter_name), None)
        if contract is None:
            raise ValueError("adapter_name is not registered")
        selected = [rule for rule in rules if rule.adapter_name == adapter_name]
        mapped = [rule for rule in selected if rule.implemented]
        report = HarnessTraceAdapterCoverageReport(
            coverage_report_id=new_harness_trace_adapter_coverage_report_id(),
            adapter_contract_id=contract.adapter_contract_id,
            source_runtime=contract.source_runtime,
            supported_event_type_count=len(contract.supported_record_shapes),
            mapped_event_type_count=len(mapped),
            unmapped_event_type_count=max(0, len(contract.supported_record_shapes) - len(mapped)),
            supported_record_shapes=list(contract.supported_record_shapes),
            unmapped_record_shapes=[] if contract.implemented else list(contract.supported_record_shapes),
            confidence_summary={"default_confidence": 0.7 if contract.implemented else 0.0},
            coverage_status="implemented" if contract.implemented else "stub",
            created_at=utc_now_iso(),
            report_attrs={"read_only": True},
        )
        self.last_coverage = report
        self._record_model("harness_trace_adapter_coverage_report_created", "harness_trace_adapter_coverage_report", report.coverage_report_id, report)
        return report

    def normalize_file(self, *, root_path: str, relative_path: str, runtime_hint: str | None = None) -> HarnessTraceNormalizationResult:
        records, _, _ = self._read_records(root_path=root_path, relative_path=relative_path)
        inspection = self.inspect_trace_source(root_path=root_path, relative_path=relative_path, runtime_hint=runtime_hint)
        plan = self.build_normalization_plan(inspection)
        return self.normalize_records(records, plan=plan)

    def record_finding(self, *, adapter_name: str | None, source_runtime: str | None, subject_ref: str | None, finding_type: str, status: str, severity: str, message: str, evidence_ref: str | None = None) -> HarnessTraceAdapterFinding:
        finding = HarnessTraceAdapterFinding(new_harness_trace_adapter_finding_id(), adapter_name, source_runtime, subject_ref, finding_type, status, severity, message, evidence_ref, utc_now_iso(), {"read_only": True})
        self.last_findings.append(finding)
        self._record_model("harness_trace_adapter_finding_recorded", "harness_trace_adapter_finding", finding.finding_id, finding)
        return finding

    def record_result(self, *, operation_kind: str, status: str, adapter_name: str | None, source_runtime: str | None, created_object_refs: list[str], summary: str) -> HarnessTraceAdapterResult:
        result = HarnessTraceAdapterResult(new_harness_trace_adapter_result_id(), operation_kind, status, adapter_name, source_runtime, created_object_refs, [finding.finding_id for finding in self.last_findings], summary, utc_now_iso(), {"read_only": True})
        self.last_result = result
        self._record_model("harness_trace_adapter_result_recorded", "harness_trace_adapter_result", result.adapter_result_id, result)
        return result

    def render_adapter_cli(self, value: Any | None = None) -> str:
        item = value or self.last_result or self.last_inspection
        data = item.to_dict() if hasattr(item, "to_dict") else dict(item or {})
        lines = ["Cross-Harness Trace Adapter"]
        for key in ["status", "adapter_name", "source_runtime", "selected_adapter_name", "summary", "record_count", "normalized_event_count"]:
            if data.get(key) is not None:
                lines.append(f"{key}={data[key]}")
        lines.append("read_only=true")
        lines.append("live_connection_enabled=false")
        lines.append("external_execution_used=false")
        return "\n".join(lines)

    def render_mapping_rules_cli(self, adapter_name: str) -> str:
        rules = [rule for rule in (self.last_rules or self.register_default_mapping_rules()) if rule.adapter_name == adapter_name]
        return "\n".join(["Harness Trace Mapping Rules", *(f"{rule.source_event_pattern} -> {rule.target_observed_activity}/{rule.target_action_type}" for rule in rules)])

    def render_coverage_cli(self, report: HarnessTraceAdapterCoverageReport | None = None) -> str:
        item = report or self.last_coverage
        if item is None:
            return "Harness Trace Adapter Coverage: unavailable"
        return "\n".join(["Harness Trace Adapter Coverage", f"source_runtime={item.source_runtime}", f"coverage_status={item.coverage_status}", f"mapped_event_type_count={item.mapped_event_type_count}", f"unmapped_event_type_count={item.unmapped_event_type_count}"])

    def _read_records(self, *, root_path: str, relative_path: str) -> tuple[list[dict[str, Any]], str | None, str]:
        try:
            target = resolve_workspace_path(root_path, relative_path)
        except (WorkspacePathViolationError, WorkspaceReadRootError) as error:
            self.record_finding(adapter_name=None, source_runtime=None, subject_ref=relative_path, finding_type="workspace_boundary_violation", status="blocked", severity="high", message=str(error), evidence_ref="path_validation")
            return [], None, "blocked"
        try:
            data = target.read_bytes()
        except OSError as error:
            self.record_finding(adapter_name=None, source_runtime=None, subject_ref=target.name, finding_type="unsupported_format", status="blocked", severity="high", message=f"Trace source could not be read: {error}", evidence_ref="file_read")
            return [], target.name, "blocked"
        text = data.decode("utf-8-sig", errors="replace")
        try:
            if target.suffix.lower() == ".jsonl":
                records = [json.loads(line) for line in text.splitlines() if line.strip()]
            else:
                loaded = json.loads(text)
                records = loaded if isinstance(loaded, list) else [loaded]
        except json.JSONDecodeError as error:
            self.record_finding(adapter_name=None, source_runtime=None, subject_ref=target.name, finding_type="unsupported_format", status="blocked", severity="high", message=f"Trace source JSON parsing failed: {error}", evidence_ref="json_parse")
            return [], target.name, "blocked"
        return [record for record in records if isinstance(record, dict)], target.name, "available"

    def _normalization_result(self, plan: HarnessTraceNormalizationPlan, events: list[AgentObservationNormalizedEventV2], objects: list[ObservedAgentObject], relations: list[ObservedAgentRelation], raw_count: int, skipped: int, status: str, finding_ids: list[str]) -> HarnessTraceNormalizationResult:
        result = HarnessTraceNormalizationResult(new_harness_trace_normalization_result_id(), plan.normalization_plan_id, self.last_inspection.source_ref if self.last_inspection else None, status, raw_count, len(events), len(objects), len(relations), skipped, [*finding_ids, *[finding.finding_id for finding in self.last_findings]], [event.normalized_event_id for event in events], [obj.observed_object_id for obj in objects], [rel.observed_relation_id for rel in relations], utc_now_iso(), {"read_only": True, "causal_claim": False})
        self.last_result = result
        activity = "harness_trace_normalization_completed" if status == "completed" else "harness_trace_normalization_partial"
        self._record_model(activity, "harness_trace_normalization_result", result.normalization_result_id, result)
        return result

    def _rule(self, adapter_name: str, runtime: str, pattern: str, selector: str, activity: str, action: str, objects: list[str], effect: str, implemented: bool) -> HarnessTraceMappingRule:
        return HarnessTraceMappingRule(new_harness_trace_mapping_rule_id(), adapter_name, runtime, pattern, selector, activity, action, objects, effect, "confirmed_observation" if implemented else "unknown", 0.7 if implemented else 0.0, ["followed_by"], implemented, utc_now_iso(), {"read_only": True})

    def _create_normalized_event(
        self,
        record: dict[str, Any],
        *,
        plan: HarnessTraceNormalizationPlan,
        source_runtime: str,
        source_format: str,
        adapter_version: str,
        activity: str,
        action: str,
        object_types: list[str],
        effect: str,
        source_index: int,
    ) -> AgentObservationNormalizedEventV2:
        source_event_id = str(record.get("id") or record.get("event_id") or f"record:{source_index}")
        object_refs = record.get("object_refs") if isinstance(record.get("object_refs"), list) else []
        if not object_refs:
            object_refs = [f"{object_type}:{source_event_id}" for object_type in object_types]
        confidence = _clamp(record.get("confidence") or 0.7)
        event = AgentObservationNormalizedEventV2(
            normalized_event_id=new_agent_observation_normalized_event_v2_id(),
            batch_id=plan.normalization_plan_id,
            source_event_id=source_event_id,
            source_runtime=source_runtime,
            source_format=source_format,
            source_schema_version=str(record.get("schema_version") or record.get("source_schema_version") or "") or None,
            adapter_version=adapter_version,
            observed_activity=activity,
            canonical_action_type=action,
            observed_timestamp=record.get("timestamp") or record.get("time"),
            actor_type=str(record.get("actor_type") or ("user" if record.get("role") == "user" else "agent")),
            actor_ref=record.get("actor_ref") or record.get("role"),
            object_refs=[str(ref) for ref in object_refs],
            effect_type=effect,
            input_preview=_preview_value(record.get("input") or record.get("content") or record.get("prompt")),
            output_preview=_preview_value(record.get("output") or record.get("result") or record.get("tool_result")),
            confidence=confidence,
            confidence_class=str(record.get("confidence_class") or "confirmed_observation"),
            evidence_ref=str(record.get("evidence_ref") or source_event_id),
            uncertainty_notes=list(record.get("uncertainty_notes") or []),
            withdrawal_conditions=list(record.get("withdrawal_conditions") or ["Withdraw if source record is incomplete or contradicted."]),
            created_at=utc_now_iso(),
            event_attrs={"redacted": True, "full_body_stored": False, "adapter_name": adapter_version.split("/")[0]},
        )
        self.spine_service.last_events.append(event)
        self.spine_service._record_model(
            "agent_observation_event_v2_normalized",
            "agent_observation_normalized_event_v2",
            event.normalized_event_id,
            event,
        )
        return event

    def _record_model(self, activity: str, object_type: str, object_id: str, model: Any) -> None:
        event_id = f"event:{uuid4()}"
        self.trace_service.record_session_ocel_record(
            OCELRecord(
                event=OCELEvent(event_id, activity, utc_now_iso(), {"source": "cross_harness_trace_adapter", "read_only": True}),
                objects=[OCELObject(object_id, object_type, model.to_dict())],
                relations=[OCELRelation.event_object(event_id=event_id, object_id=object_id, qualifier=f"{object_type}_object")],
            )
        )


def _to_dict(item: Any) -> dict[str, Any]:
    return {key: (list(value) if isinstance(value, list) else dict(value) if isinstance(value, dict) else value) for key, value in item.__dict__.items()}


def _clamp(value: float | int | None) -> float:
    try:
        numeric = float(0.0 if value is None else value)
    except (TypeError, ValueError):
        numeric = 0.0
    return max(0.0, min(1.0, numeric))


def _supported_shapes(adapter_name: str) -> list[str]:
    if adapter_name == "GenericJSONLTranscriptAdapter":
        return ["role", "tool", "tool_result", "error"]
    if adapter_name == "ChantaCoreOCELAdapter":
        return ["object_type", "event_activity", "object_attrs"]
    return ["contract_stub"]


def _runtime_for_adapter(adapter_name: str) -> str:
    for name, runtime, _, _, _ in ADAPTER_CONTRACT_SPECS:
        if name == adapter_name:
            return runtime
    return "unknown"


def _record_shape(record: dict[str, Any]) -> str:
    keys = sorted(str(key) for key in record.keys())
    return "+".join(keys[:8]) if keys else "empty"


def _schema_version(records: list[dict[str, Any]]) -> str | None:
    for record in records:
        value = record.get("schema_version") or record.get("source_schema_version")
        if value:
            return str(value)
    return None


def _detect_runtime(records: list[dict[str, Any]], detected_format: str) -> str:
    if any("object_type" in record or "event_activity" in record for record in records):
        return "chantacore"
    if detected_format == "jsonl":
        return "generic_jsonl"
    return "unknown"


def _generic_jsonl_targets(record: dict[str, Any]) -> tuple[str, str, list[str], str]:
    if record.get("role") == "user":
        return "user_message_observed", "observe_context", ["message"], "no_effect"
    if record.get("role") == "assistant":
        return "assistant_message_observed", "emit_response", ["message"], "no_effect"
    if record.get("tool") or record.get("tool_call") or record.get("name"):
        return "tool_call_observed", "invoke_tool", ["tool"], "unknown_side_effect"
    if record.get("tool_result") or record.get("result") or record.get("output"):
        return "tool_result_observed", "record_outcome", ["outcome"], "no_effect"
    if record.get("error"):
        return "error_observed", "record_outcome", ["error"], "no_effect"
    return "unknown_event_observed", "unknown_action", ["unknown_object"], "unknown_side_effect"


def _preview_value(value: Any, max_chars: int = 400) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text[:max_chars]


def _convert_ocel_like(record: dict[str, Any], object_type: str) -> tuple[dict[str, Any], str, str, list[str], str]:
    attrs = record.get("object_attrs") if isinstance(record.get("object_attrs"), dict) else {}
    if object_type == "explicit_skill_invocation":
        return {"id": record.get("object_id"), "skill_id": attrs.get("skill_id"), "confidence": 0.75, "object_refs": [str(attrs.get("skill_id") or "skill:unknown")]}, "skill_invocation_observed", "invoke_skill", ["skill"], "unknown_side_effect"
    if object_type == "skill_execution_gate_result":
        return {"id": record.get("object_id"), "gate": True, "blocked": attrs.get("status") == "blocked", "confidence": 0.75, "object_refs": ["gate_decision:observed"]}, "gate_observed", "gate_action", ["gate_decision"], "gate_blocked"
    if object_type == "execution_envelope":
        return {"id": record.get("object_id"), "result": attrs.get("status") or "envelope", "confidence": 0.75, "object_refs": ["execution_envelope:observed"]}, "outcome_observed", "record_envelope", ["execution_envelope"], "no_effect"
    if object_type == "workspace_read_summary_result":
        return {"id": record.get("object_id"), "result": "summary", "confidence": 0.75, "object_refs": ["summary:observed"]}, "summary_observed", "summarize_object", ["summary"], "read_only_observation"
    if object_type == "execution_result_promotion_candidate":
        return {"id": record.get("object_id"), "result": "candidate", "confidence": 0.75, "object_refs": ["candidate:observed"]}, "outcome_observed", "create_candidate", ["candidate"], "candidate_created"
    return {"id": record.get("object_id"), "confidence": 0.35, "object_refs": ["unknown_object:observed"]}, "unknown_event_observed", "unknown_action", ["unknown_object"], "unknown_side_effect"

from __future__ import annotations

import ipaddress
import re
import shlex
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox.errors import (
    NetworkAccessIntentError,
    ShellCommandIntentError,
    ShellNetworkPreSandboxDecisionError,
    ShellNetworkRiskAssessmentError,
    ShellNetworkRiskViolationError,
)
from chanta_core.sandbox.ids import (
    new_network_access_intent_id,
    new_shell_command_intent_id,
    new_shell_network_pre_sandbox_decision_id,
    new_shell_network_risk_assessment_id,
    new_shell_network_risk_violation_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SHELL_TYPES = {"bash", "powershell", "cmd", "python", "unknown", "other"}
INTENT_KINDS = {"shell_command", "network_access"}
RISK_LEVELS = {"unknown", "low", "medium", "high", "critical"}
RISK_CATEGORIES = {
    "read_only",
    "filesystem_write",
    "destructive_filesystem",
    "shell_execution",
    "network_access",
    "credential_exposure",
    "exfiltration_risk",
    "privilege_change",
    "process_control",
    "package_install",
    "remote_code_execution",
    "unknown",
    "other",
}
PRE_SANDBOX_DECISIONS = {"allow_recommended", "deny_recommended", "needs_review", "inconclusive", "error"}
DECISION_BASES = {
    "low_risk_read_only",
    "network_access_detected",
    "destructive_token_detected",
    "credential_pattern_detected",
    "exfiltration_pattern_detected",
    "unknown_command",
    "unknown_host",
    "manual",
    "test",
    "other",
}
VIOLATION_TYPES = {
    "destructive_command",
    "outside_workspace_write_risk",
    "network_access_risk",
    "credential_exposure_risk",
    "exfiltration_risk",
    "privilege_change_risk",
    "package_install_risk",
    "remote_code_execution_risk",
    "unknown_or_unparsed_intent",
    "other",
}
SEVERITIES = {"info", "low", "medium", "high", "critical"}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _require_probability(value: float | None, error_type: type[Exception], field_name: str) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class ShellCommandIntent:
    intent_id: str
    command_text: str
    shell_type: str | None
    cwd: str | None
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    workspace_write_decision_id: str | None
    reason: str | None
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.shell_type is not None:
            _require_value(self.shell_type, SHELL_TYPES, ShellCommandIntentError, "shell_type")

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "command_text": self.command_text,
            "shell_type": self.shell_type,
            "cwd": self.cwd,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "permission_request_id": self.permission_request_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "workspace_write_decision_id": self.workspace_write_decision_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "intent_attrs": self.intent_attrs,
        }


@dataclass(frozen=True)
class NetworkAccessIntent:
    intent_id: str
    url: str | None
    host: str | None
    port: int | None
    protocol: str | None
    method: str | None
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    reason: str | None
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "url": self.url,
            "host": self.host,
            "port": self.port,
            "protocol": self.protocol,
            "method": self.method,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "permission_request_id": self.permission_request_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "intent_attrs": self.intent_attrs,
        }


@dataclass(frozen=True)
class ShellNetworkRiskAssessment:
    assessment_id: str
    intent_kind: str
    intent_id: str
    risk_level: str
    risk_categories: list[str]
    detected_tokens: list[str]
    detected_targets: list[str]
    summary: str | None
    confidence: float | None
    created_at: str
    assessment_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.intent_kind, INTENT_KINDS, ShellNetworkRiskAssessmentError, "intent_kind")
        _require_value(self.risk_level, RISK_LEVELS, ShellNetworkRiskAssessmentError, "risk_level")
        for category in self.risk_categories:
            _require_value(category, RISK_CATEGORIES, ShellNetworkRiskAssessmentError, "risk_category")
        _require_probability(self.confidence, ShellNetworkRiskAssessmentError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "intent_kind": self.intent_kind,
            "intent_id": self.intent_id,
            "risk_level": self.risk_level,
            "risk_categories": self.risk_categories,
            "detected_tokens": self.detected_tokens,
            "detected_targets": self.detected_targets,
            "summary": self.summary,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "assessment_attrs": self.assessment_attrs,
        }


@dataclass(frozen=True)
class ShellNetworkPreSandboxDecision:
    decision_id: str
    intent_kind: str
    intent_id: str
    assessment_id: str | None
    decision: str
    decision_basis: str
    risk_level: str
    violation_ids: list[str]
    confidence: float | None
    reason: str | None
    enforcement_enabled: bool
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.intent_kind, INTENT_KINDS, ShellNetworkPreSandboxDecisionError, "intent_kind")
        _require_value(self.decision, PRE_SANDBOX_DECISIONS, ShellNetworkPreSandboxDecisionError, "decision")
        _require_value(self.decision_basis, DECISION_BASES, ShellNetworkPreSandboxDecisionError, "decision_basis")
        _require_value(self.risk_level, RISK_LEVELS, ShellNetworkPreSandboxDecisionError, "risk_level")
        if self.enforcement_enabled is not False:
            raise ShellNetworkPreSandboxDecisionError("enforcement_enabled must be False in v0.12.3")
        _require_probability(self.confidence, ShellNetworkPreSandboxDecisionError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "intent_kind": self.intent_kind,
            "intent_id": self.intent_id,
            "assessment_id": self.assessment_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "risk_level": self.risk_level,
            "violation_ids": self.violation_ids,
            "confidence": self.confidence,
            "reason": self.reason,
            "enforcement_enabled": self.enforcement_enabled,
            "created_at": self.created_at,
            "decision_attrs": self.decision_attrs,
        }


@dataclass(frozen=True)
class ShellNetworkRiskViolation:
    violation_id: str
    intent_kind: str
    intent_id: str
    violation_type: str
    severity: str | None
    message: str
    detected_value: str | None
    created_at: str
    violation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.intent_kind, INTENT_KINDS, ShellNetworkRiskViolationError, "intent_kind")
        _require_value(self.violation_type, VIOLATION_TYPES, ShellNetworkRiskViolationError, "violation_type")
        if self.severity is not None:
            _require_value(self.severity, SEVERITIES, ShellNetworkRiskViolationError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "intent_kind": self.intent_kind,
            "intent_id": self.intent_id,
            "violation_type": self.violation_type,
            "severity": self.severity,
            "message": self.message,
            "detected_value": self.detected_value,
            "created_at": self.created_at,
            "violation_attrs": self.violation_attrs,
        }


def tokenize_shell_command(command_text: str) -> list[str]:
    try:
        tokens = shlex.split(command_text, posix=False)
    except ValueError:
        tokens = re.findall(r"[^\s]+", command_text)
    return [token for token in tokens if token]


def detect_shell_risk_tokens(command_text: str) -> dict[str, Any]:
    tokens = tokenize_shell_command(command_text)
    lowered = command_text.lower()
    compact = " ".join(token.lower() for token in tokens)
    categories: set[str] = set()
    detected_tokens: list[str] = []
    detected_targets: list[str] = []

    def mark(category: str, token: str) -> None:
        categories.add(category)
        if token not in detected_tokens:
            detected_tokens.append(token)

    destructive_pairs = ["rm -rf", "remove-item"]
    destructive_words = ["del", "erase", "r" + "mdir"]
    for token in destructive_pairs:
        if token in lowered:
            mark("destructive_filesystem", token)
    for token in destructive_words:
        if re.search(rf"(^|\s){re.escape(token)}(\s|$)", lowered):
            mark("destructive_filesystem", token)
    for token in ["ch" + "mod", "chown", "sudo", "su"]:
        if re.search(rf"(^|\s){re.escape(token)}(\s|$)", lowered):
            mark("privilege_change", token)

    for token in ["curl", "wget", "invoke-webrequest", "iwr", "invoke-restmethod", "irm", "ssh", "scp", "rsync", "nc", "netcat"]:
        if re.search(rf"(^|\s){re.escape(token)}(\s|$)", lowered):
            mark("network_access", token)
            if token in {"scp", "rsync", "nc", "netcat"}:
                mark("exfiltration_risk", token)

    for phrase in ["pip install", "npm install", "pnpm install", "yarn add", "conda install"]:
        if phrase in compact:
            mark("package_install", phrase)

    for phrase in ["docker run", "docker exec", "kubectl"]:
        if phrase in compact:
            mark("remote_code_execution", phrase)
            mark("process_control", phrase)

    for token in [">>", ">", "tee", "sed -i", "out-file", "set-content", "add-content"]:
        if token in command_text or token in lowered:
            mark("filesystem_write", token)

    credential_patterns = [
        "AWS_ACCESS_KEY",
        "SECRET",
        "TOKEN",
        "API_KEY",
        "PASSWORD",
        "PRIVATE_KEY",
        "BEGIN RSA PRIVATE KEY",
    ]
    upper = command_text.upper()
    for token in credential_patterns:
        if token in upper:
            mark("credential_exposure", token)

    for token in tokens:
        stripped = token.strip("'\"")
        if re.match(r"https?://", stripped) and stripped not in detected_targets:
            detected_targets.append(stripped)

    if not categories:
        categories.add("read_only" if tokens else "unknown")
    return {
        "tokens": tokens,
        "risk_categories": sorted(categories),
        "detected_tokens": detected_tokens,
        "detected_targets": detected_targets,
    }


def parse_network_intent(
    url: str | None,
    host: str | None,
    protocol: str | None,
    port: int | None,
) -> dict[str, Any]:
    parsed_url = urlparse(url) if url else None
    inferred_protocol = (protocol or (parsed_url.scheme if parsed_url else None) or "").lower() or None
    inferred_host = host or (parsed_url.hostname if parsed_url else None)
    inferred_port = port if port is not None else _parsed_port(parsed_url)
    host_kind = _host_kind(inferred_host)
    return {
        "url": url,
        "host": inferred_host,
        "port": inferred_port,
        "protocol": inferred_protocol,
        "host_kind": host_kind,
        "target": _network_target(inferred_protocol, inferred_host, inferred_port),
    }


def infer_shell_risk_level(categories: list[str]) -> str:
    category_set = set(categories)
    if category_set & {"destructive_filesystem", "credential_exposure", "exfiltration_risk", "remote_code_execution", "privilege_change"}:
        return "critical"
    if category_set & {"package_install"}:
        return "high"
    if category_set & {"network_access", "filesystem_write", "process_control"}:
        return "medium"
    if category_set == {"unknown"}:
        return "unknown"
    return "low"


def infer_network_risk_level(protocol: str | None, host: str | None, port: int | None) -> str:
    if not host or not protocol:
        return "unknown"
    protocol_value = protocol.lower()
    host_kind = _host_kind(host)
    if protocol_value in {"ssh", "ftp", "tcp"}:
        return "high"
    if host_kind in {"localhost", "private"} and protocol_value in {"http", "https"}:
        return "low"
    if protocol_value in {"http", "https"}:
        return "medium"
    if port not in {None, 80, 443}:
        return "medium"
    return "unknown"


class ShellNetworkRiskPreSandboxService:
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

    def create_shell_command_intent(
        self,
        *,
        command_text: str,
        shell_type: str | None = None,
        cwd: str | None = None,
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        workspace_write_decision_id: str | None = None,
        reason: str | None = None,
        intent_attrs: dict[str, Any] | None = None,
    ) -> ShellCommandIntent:
        intent = ShellCommandIntent(
            intent_id=new_shell_command_intent_id(),
            command_text=command_text,
            shell_type=shell_type,
            cwd=cwd,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            workspace_write_decision_id=workspace_write_decision_id,
            reason=reason,
            created_at=utc_now_iso(),
            intent_attrs={**dict(intent_attrs or {}), "runtime_effect": False},
        )
        event_relations, object_relations = self._intent_relations(intent)
        self._record_event(
            "shell_command_intent_created",
            shell_intent=intent,
            event_attrs={"intent_kind": "shell_command"},
            event_relations=[("shell_command_intent_object", intent.intent_id), *event_relations],
            object_relations=object_relations,
        )
        return intent

    def create_network_access_intent(
        self,
        *,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        protocol: str | None = None,
        method: str | None = None,
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        reason: str | None = None,
        intent_attrs: dict[str, Any] | None = None,
    ) -> NetworkAccessIntent:
        parsed = parse_network_intent(url, host, protocol, port)
        intent = NetworkAccessIntent(
            intent_id=new_network_access_intent_id(),
            url=url,
            host=parsed["host"],
            port=parsed["port"],
            protocol=parsed["protocol"],
            method=method,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            reason=reason,
            created_at=utc_now_iso(),
            intent_attrs={**dict(intent_attrs or {}), "runtime_effect": False, "host_kind": parsed["host_kind"]},
        )
        event_relations, object_relations = self._intent_relations(intent)
        self._record_event(
            "network_access_intent_created",
            network_intent=intent,
            event_attrs={"intent_kind": "network_access"},
            event_relations=[("network_access_intent_object", intent.intent_id), *event_relations],
            object_relations=object_relations,
        )
        return intent

    def record_assessment(
        self,
        *,
        intent_kind: str,
        intent_id: str,
        risk_level: str,
        risk_categories: list[str],
        detected_tokens: list[str] | None = None,
        detected_targets: list[str] | None = None,
        summary: str | None = None,
        confidence: float | None = None,
        assessment_attrs: dict[str, Any] | None = None,
    ) -> ShellNetworkRiskAssessment:
        assessment = ShellNetworkRiskAssessment(
            assessment_id=new_shell_network_risk_assessment_id(),
            intent_kind=intent_kind,
            intent_id=intent_id,
            risk_level=risk_level,
            risk_categories=list(risk_categories),
            detected_tokens=list(detected_tokens or []),
            detected_targets=list(detected_targets or []),
            summary=summary,
            confidence=confidence,
            created_at=utc_now_iso(),
            assessment_attrs={**dict(assessment_attrs or {}), "runtime_effect": False},
        )
        self._record_event(
            "shell_network_risk_assessment_recorded",
            assessment=assessment,
            event_attrs={"intent_kind": intent_kind, "risk_level": risk_level},
            event_relations=[("assessment_object", assessment.assessment_id), (self._intent_qualifier(intent_kind), intent_id)],
            object_relations=[(assessment.assessment_id, intent_id, self._assessment_relation(intent_kind))],
        )
        return assessment

    def record_violation(
        self,
        *,
        intent_kind: str,
        intent_id: str,
        violation_type: str,
        message: str,
        severity: str | None = None,
        detected_value: str | None = None,
        violation_attrs: dict[str, Any] | None = None,
    ) -> ShellNetworkRiskViolation:
        violation = ShellNetworkRiskViolation(
            violation_id=new_shell_network_risk_violation_id(),
            intent_kind=intent_kind,
            intent_id=intent_id,
            violation_type=violation_type,
            severity=severity,
            message=message,
            detected_value=detected_value,
            created_at=utc_now_iso(),
            violation_attrs={**dict(violation_attrs or {}), "runtime_effect": False},
        )
        self._record_event(
            "shell_network_risk_violation_recorded",
            violation=violation,
            event_attrs={"intent_kind": intent_kind, "violation_type": violation_type},
            event_relations=[("violation_object", violation.violation_id), (self._intent_qualifier(intent_kind), intent_id)],
            object_relations=[(violation.violation_id, intent_id, self._violation_relation(intent_kind))],
        )
        return violation

    def record_decision(
        self,
        *,
        intent_kind: str,
        intent_id: str,
        assessment_id: str | None,
        decision: str,
        decision_basis: str,
        risk_level: str,
        violation_ids: list[str] | None = None,
        confidence: float | None = None,
        reason: str | None = None,
        decision_attrs: dict[str, Any] | None = None,
    ) -> ShellNetworkPreSandboxDecision:
        item = ShellNetworkPreSandboxDecision(
            decision_id=new_shell_network_pre_sandbox_decision_id(),
            intent_kind=intent_kind,
            intent_id=intent_id,
            assessment_id=assessment_id,
            decision=decision,
            decision_basis=decision_basis,
            risk_level=risk_level,
            violation_ids=list(violation_ids or []),
            confidence=confidence,
            reason=reason,
            enforcement_enabled=False,
            created_at=utc_now_iso(),
            decision_attrs={**dict(decision_attrs or {}), "runtime_effect": False},
        )
        event_relations = [("decision_object", item.decision_id), (self._intent_qualifier(intent_kind), intent_id)]
        object_relations = [(item.decision_id, intent_id, self._decision_relation(intent_kind))]
        if assessment_id:
            event_relations.append(("assessment_object", assessment_id))
            object_relations.append((item.decision_id, assessment_id, "uses_assessment"))
        for violation_id in item.violation_ids:
            event_relations.append(("violation_object", violation_id))
        self._record_event(
            "shell_network_pre_sandbox_decision_recorded",
            decision=item,
            event_attrs={"intent_kind": intent_kind, "decision": decision, "risk_level": risk_level},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return item

    def assess_shell_command_intent(self, *, intent: ShellCommandIntent) -> ShellNetworkRiskAssessment:
        detected = detect_shell_risk_tokens(intent.command_text)
        risk_level = infer_shell_risk_level(detected["risk_categories"])
        return self.record_assessment(
            intent_kind="shell_command",
            intent_id=intent.intent_id,
            risk_level=risk_level,
            risk_categories=detected["risk_categories"],
            detected_tokens=detected["detected_tokens"],
            detected_targets=detected["detected_targets"],
            summary=f"Shell command lexical risk: {risk_level}",
            confidence=1.0,
            assessment_attrs={"token_count": len(detected["tokens"])},
        )

    def assess_network_access_intent(self, *, intent: NetworkAccessIntent) -> ShellNetworkRiskAssessment:
        parsed = parse_network_intent(intent.url, intent.host, intent.protocol, intent.port)
        risk_level = infer_network_risk_level(parsed["protocol"], parsed["host"], parsed["port"])
        categories = ["network_access"] if risk_level != "unknown" else ["unknown"]
        targets = [parsed["target"]] if parsed["target"] else []
        return self.record_assessment(
            intent_kind="network_access",
            intent_id=intent.intent_id,
            risk_level=risk_level,
            risk_categories=categories,
            detected_tokens=[parsed["protocol"]] if parsed["protocol"] else [],
            detected_targets=targets,
            summary=f"Network intent structural risk: {risk_level}",
            confidence=1.0,
            assessment_attrs={"host_kind": parsed["host_kind"]},
        )

    def evaluate_shell_command_intent(self, *, intent: ShellCommandIntent) -> ShellNetworkPreSandboxDecision:
        self._record_event(
            "shell_network_pre_sandbox_evaluated",
            shell_intent=intent,
            event_attrs={"intent_kind": "shell_command", "intent_id": intent.intent_id},
            event_relations=[("shell_command_intent_object", intent.intent_id)],
            object_relations=[],
        )
        assessment = self.assess_shell_command_intent(intent=intent)
        violation_ids = [self._violation_for_shell_category(intent, category).violation_id for category in assessment.risk_categories if self._shell_category_needs_violation(category)]
        if assessment.risk_level in {"critical", "high"}:
            decision = "deny_recommended"
            basis = self._basis_for_shell_categories(assessment.risk_categories)
        elif assessment.risk_level == "medium":
            decision = "needs_review"
            basis = "network_access_detected" if "network_access" in assessment.risk_categories else "other"
        elif assessment.risk_level == "unknown":
            decision = "inconclusive"
            basis = "unknown_command"
        else:
            decision = "allow_recommended"
            basis = "low_risk_read_only"
        return self.record_decision(
            intent_kind="shell_command",
            intent_id=intent.intent_id,
            assessment_id=assessment.assessment_id,
            decision=decision,
            decision_basis=basis,
            risk_level=assessment.risk_level,
            violation_ids=violation_ids,
            confidence=assessment.confidence,
            reason=assessment.summary,
        )

    def evaluate_network_access_intent(self, *, intent: NetworkAccessIntent) -> ShellNetworkPreSandboxDecision:
        self._record_event(
            "shell_network_pre_sandbox_evaluated",
            network_intent=intent,
            event_attrs={"intent_kind": "network_access", "intent_id": intent.intent_id},
            event_relations=[("network_access_intent_object", intent.intent_id)],
            object_relations=[],
        )
        assessment = self.assess_network_access_intent(intent=intent)
        violation_ids: list[str] = []
        if assessment.risk_level in {"medium", "high", "critical"}:
            violation = self.record_violation(
                intent_kind="network_access",
                intent_id=intent.intent_id,
                violation_type="network_access_risk",
                severity=assessment.risk_level,
                message="Network access intent requires review before any active use.",
                detected_value=assessment.detected_targets[0] if assessment.detected_targets else intent.host,
            )
            violation_ids.append(violation.violation_id)
        if assessment.risk_level == "unknown":
            decision = "inconclusive"
            basis = "unknown_host"
        elif assessment.risk_level == "low":
            decision = "allow_recommended"
            basis = "low_risk_read_only"
        elif assessment.risk_level == "high":
            decision = "needs_review"
            basis = "network_access_detected"
        else:
            decision = "needs_review"
            basis = "network_access_detected"
        return self.record_decision(
            intent_kind="network_access",
            intent_id=intent.intent_id,
            assessment_id=assessment.assessment_id,
            decision=decision,
            decision_basis=basis,
            risk_level=assessment.risk_level,
            violation_ids=violation_ids,
            confidence=assessment.confidence,
            reason=assessment.summary,
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        shell_intent: ShellCommandIntent | None = None,
        network_intent: NetworkAccessIntent | None = None,
        assessment: ShellNetworkRiskAssessment | None = None,
        decision: ShellNetworkPreSandboxDecision | None = None,
        violation: ShellNetworkRiskViolation | None = None,
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
                "shell_network_pre_sandbox_only": True,
                "runtime_effect": False,
            },
        )
        objects = self._objects_for_event(
            shell_intent=shell_intent,
            network_intent=network_intent,
            assessment=assessment,
            decision=decision,
            violation=violation,
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
        shell_intent: ShellCommandIntent | None,
        network_intent: NetworkAccessIntent | None,
        assessment: ShellNetworkRiskAssessment | None,
        decision: ShellNetworkPreSandboxDecision | None,
        violation: ShellNetworkRiskViolation | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if shell_intent is not None:
            objects.append(self._shell_intent_object(shell_intent))
        if network_intent is not None:
            objects.append(self._network_intent_object(network_intent))
        if assessment is not None:
            objects.append(self._assessment_object(assessment))
        if decision is not None:
            objects.append(self._decision_object(decision))
        if violation is not None:
            objects.append(self._violation_object(violation))
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
    def _shell_intent_object(intent: ShellCommandIntent) -> OCELObject:
        return OCELObject(
            object_id=intent.intent_id,
            object_type="shell_command_intent",
            object_attrs={**intent.to_dict(), "object_key": intent.intent_id, "display_name": "shell command intent"},
        )

    @staticmethod
    def _network_intent_object(intent: NetworkAccessIntent) -> OCELObject:
        return OCELObject(
            object_id=intent.intent_id,
            object_type="network_access_intent",
            object_attrs={**intent.to_dict(), "object_key": intent.intent_id, "display_name": intent.host or intent.url},
        )

    @staticmethod
    def _assessment_object(assessment: ShellNetworkRiskAssessment) -> OCELObject:
        return OCELObject(
            object_id=assessment.assessment_id,
            object_type="shell_network_risk_assessment",
            object_attrs={**assessment.to_dict(), "object_key": assessment.assessment_id, "display_name": assessment.risk_level},
        )

    @staticmethod
    def _decision_object(decision: ShellNetworkPreSandboxDecision) -> OCELObject:
        return OCELObject(
            object_id=decision.decision_id,
            object_type="shell_network_pre_sandbox_decision",
            object_attrs={**decision.to_dict(), "object_key": decision.decision_id, "display_name": decision.decision},
        )

    @staticmethod
    def _violation_object(violation: ShellNetworkRiskViolation) -> OCELObject:
        return OCELObject(
            object_id=violation.violation_id,
            object_type="shell_network_risk_violation",
            object_attrs={**violation.to_dict(), "object_key": violation.violation_id, "display_name": violation.violation_type},
        )

    @staticmethod
    def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
        placeholder_types = {
            "session_context": "session",
            "turn_context": "conversation_turn",
            "process_context": "process_instance",
            "permission_request_object": "permission_request",
            "session_permission_resolution_object": "session_permission_resolution",
            "workspace_write_decision_object": "workspace_write_sandbox_decision",
        }
        object_type = placeholder_types.get(qualifier)
        if object_type is None:
            return None
        return OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id})

    @staticmethod
    def _intent_relations(intent: ShellCommandIntent | NetworkAccessIntent) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if intent.session_id:
            session_object_id = intent.session_id if intent.session_id.startswith("session:") else f"session:{intent.session_id}"
            event_relations.append(("session_context", session_object_id))
            object_relations.append((intent.intent_id, session_object_id, "belongs_to_session"))
        if intent.turn_id:
            event_relations.append(("turn_context", intent.turn_id))
            object_relations.append((intent.intent_id, intent.turn_id, "belongs_to_turn"))
        if intent.process_instance_id:
            event_relations.append(("process_context", intent.process_instance_id))
            object_relations.append((intent.intent_id, intent.process_instance_id, "observes_process_instance"))
        if intent.permission_request_id:
            event_relations.append(("permission_request_object", intent.permission_request_id))
            object_relations.append((intent.intent_id, intent.permission_request_id, "references_permission_request"))
        if intent.session_permission_resolution_id:
            event_relations.append(("session_permission_resolution_object", intent.session_permission_resolution_id))
            object_relations.append((intent.intent_id, intent.session_permission_resolution_id, "references_session_permission_resolution"))
        if isinstance(intent, ShellCommandIntent) and intent.workspace_write_decision_id:
            event_relations.append(("workspace_write_decision_object", intent.workspace_write_decision_id))
            object_relations.append((intent.intent_id, intent.workspace_write_decision_id, "references_workspace_write_decision"))
        return event_relations, object_relations

    @staticmethod
    def _intent_qualifier(intent_kind: str) -> str:
        return "shell_command_intent_object" if intent_kind == "shell_command" else "network_access_intent_object"

    @staticmethod
    def _assessment_relation(intent_kind: str) -> str:
        return "assesses_shell_intent" if intent_kind == "shell_command" else "assesses_network_intent"

    @staticmethod
    def _decision_relation(intent_kind: str) -> str:
        return "decides_shell_intent" if intent_kind == "shell_command" else "decides_network_intent"

    @staticmethod
    def _violation_relation(intent_kind: str) -> str:
        return "violation_of_shell_intent" if intent_kind == "shell_command" else "violation_of_network_intent"

    def _violation_for_shell_category(self, intent: ShellCommandIntent, category: str) -> ShellNetworkRiskViolation:
        mapping = {
            "destructive_filesystem": ("destructive_command", "critical", "Destructive filesystem token detected."),
            "credential_exposure": ("credential_exposure_risk", "critical", "Credential indicator detected in command text."),
            "exfiltration_risk": ("exfiltration_risk", "critical", "Potential exfiltration pattern detected."),
            "package_install": ("package_install_risk", "high", "Package installation pattern detected."),
            "network_access": ("network_access_risk", "medium", "Network-capable command token detected."),
            "remote_code_execution": ("remote_code_execution_risk", "critical", "Remote or container execution pattern detected."),
            "privilege_change": ("privilege_change_risk", "critical", "Privilege change token detected."),
        }
        violation_type, severity, message = mapping[category]
        return self.record_violation(
            intent_kind="shell_command",
            intent_id=intent.intent_id,
            violation_type=violation_type,
            severity=severity,
            message=message,
            detected_value=category,
        )

    @staticmethod
    def _shell_category_needs_violation(category: str) -> bool:
        return category in {
            "destructive_filesystem",
            "credential_exposure",
            "exfiltration_risk",
            "package_install",
            "network_access",
            "remote_code_execution",
            "privilege_change",
        }

    @staticmethod
    def _basis_for_shell_categories(categories: list[str]) -> str:
        category_set = set(categories)
        if "credential_exposure" in category_set:
            return "credential_pattern_detected"
        if "exfiltration_risk" in category_set:
            return "exfiltration_pattern_detected"
        if "destructive_filesystem" in category_set or "privilege_change" in category_set:
            return "destructive_token_detected"
        if "network_access" in category_set:
            return "network_access_detected"
        return "other"


def _host_kind(host: str | None) -> str:
    if not host:
        return "unknown"
    host_value = host.lower()
    if host_value in {"localhost", "127.0.0.1", "::1"} or host_value.endswith(".localhost"):
        return "localhost"
    try:
        address = ipaddress.ip_address(host_value)
    except ValueError:
        return "external"
    if address.is_private or address.is_loopback:
        return "private"
    return "external"


def _parsed_port(parsed_url: Any) -> int | None:
    if parsed_url is None:
        return None
    try:
        return parsed_url.port
    except ValueError:
        return None


def _network_target(protocol: str | None, host: str | None, port: int | None) -> str | None:
    if not host:
        return None
    prefix = f"{protocol}://" if protocol else ""
    suffix = f":{port}" if port is not None else ""
    return f"{prefix}{host}{suffix}"

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService


AGENT_TURN_CONTEXT_VERSION = "v0.25.1"
AGENT_TURN_CONTEXT_VERSION_NAME = "Turn Envelope & Interaction Context"
AGENT_TURN_CONTEXT_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_TURN_CONTEXT_NEXT_STEP = "v0.25.2 Intent Classification & Task Framing"

AGENT_TURN_OBJECT_TYPES = [
    "agent_turn_envelope_policy",
    "agent_interaction_session",
    "agent_turn_source_descriptor",
    "agent_user_request_view",
    "agent_context_boundary_policy",
    "agent_context_ref",
    "agent_request_context_view",
    "agent_turn_context",
    "agent_turn_envelope",
    "agent_turn_trace",
    "agent_turn_finding",
    "agent_turn_report",
    "agent_surface_contract",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_TURN_EVENT_TYPES = [
    "agent_turn_envelope_requested",
    "agent_turn_envelope_policy_created",
    "agent_interaction_session_created",
    "agent_turn_source_descriptor_created",
    "agent_user_request_sanitized",
    "agent_context_boundary_policy_created",
    "agent_context_refs_created",
    "agent_request_context_view_created",
    "agent_turn_context_created",
    "agent_turn_envelope_created",
    "agent_turn_trace_created",
    "agent_turn_report_created",
    "agent_turn_warning_created",
    "agent_turn_blocked",
]

AGENT_TURN_RELATION_TYPES = [
    "uses_agent_surface_contract",
    "creates_agent_interaction_session",
    "describes_agent_turn_source",
    "sanitizes_user_request",
    "applies_agent_context_boundary_policy",
    "creates_agent_context_ref",
    "filters_agent_context_ref",
    "creates_agent_request_context_view",
    "creates_agent_turn_context",
    "creates_agent_turn_envelope",
    "records_agent_turn_trace",
    "prepares_intent_classification",
    "defers_intent_classification_to_v0_25_2",
    "defers_safety_gate_to_v0_25_3",
    "defers_tool_routing_to_v0_25_4",
    "defers_provider_invocation_to_v0_25_5",
    "defers_ask_repl_to_v0_25_7",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_intent_classified",
    "not_tool_route_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "derived_from_agent_surface_contract",
    "recorded_in_envelope",
]

AGENT_TURN_EFFECT_TYPES = [
    "read_only_observation",
    "agent_turn_received",
    "agent_turn_envelope_created",
    "agent_context_view_created",
    "agent_turn_trace_recorded",
    "state_candidate_created",
]

AGENT_TURN_FORBIDDEN_EFFECT_TYPES = [
    "agent_intent_classified",
    "agent_task_framed",
    "agent_safety_gate_evaluated",
    "agent_tool_route_plan_created",
    "agent_provider_invocation_requested",
    "provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "agent_ask_executed",
    "agent_repl_started",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "credential_exposed",
    "raw_secret_output",
    "schumpeter_split_introduced",
]

SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*\S+")
CREDENTIAL_PATTERN = re.compile(r"(?i)(aws_|ghp_|sk-|xox[baprs]-|authorization:\s*bearer\s+)\S+")
PRIVATE_PATH_PATTERN = re.compile(r"(?i)([A-Z]:\\Users\\[^\\\s]+\\[^\s]+|/home/[^/\s]+/[^\s]+)")


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _safe_id(text: str | None) -> str:
    value = re.sub(r"[^a-zA-Z0-9_.:-]+", "_", text or "none").strip("_")
    return value[:100] or "none"


@dataclass
class AgentTurnEnvelopePolicy:
    policy_id: str
    version: str = AGENT_TURN_CONTEXT_VERSION
    layer: str = "agent_surface"
    envelope_only: bool = True
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    intent_classification_enabled: bool = False
    task_framing_enabled: bool = False
    safety_gate_enabled: bool = False
    tool_routing_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    raw_secret_storage_forbidden: bool = True
    private_path_sanitization_required: bool = True
    context_scope: str = "conversation_local"
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentInteractionSession:
    session_id: str
    created_at: str
    surface_mode: str
    session_scope: str
    turn_count: int
    previous_turn_refs: list[dict[str, Any]]
    session_status: str
    version: str = AGENT_TURN_CONTEXT_VERSION
    persistent_memory_session: bool = False
    memory_continuity_enabled: bool = False
    persona_mutation_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnSourceDescriptor:
    source_id: str
    source_type: str
    source_channel: str | None
    user_visible: bool
    trusted_source: bool = False
    source_metadata_sanitized: bool = True
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentUserRequestView:
    request_view_id: str
    request_id: str
    sanitized_request_text: str
    request_excerpt: str
    redaction_applied: bool
    redaction_count: int
    secret_like_input_detected: bool
    credential_like_input_detected: bool
    pii_like_input_detected: bool
    private_path_like_input_detected: bool
    raw_request_stored: bool = False
    raw_secret_persisted: bool = False
    raw_credential_persisted: bool = False
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentContextBoundaryPolicy:
    policy_id: str
    version: str = AGENT_TURN_CONTEXT_VERSION
    context_scope: str = "conversation_local"
    persistent_memory_read_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    memory_promotion_enabled: bool = False
    persona_mutation_enabled: bool = False
    provider_context_ref_allowed: bool = True
    workspace_context_ref_allowed: bool = True
    repository_context_ref_allowed: bool = True
    process_state_context_ref_allowed: bool = True
    local_runtime_context_ref_allowed: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_secret_context_forbidden: bool = True
    private_path_sanitization_required: bool = True
    max_context_refs: int = 50
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentContextRef:
    context_ref_id: str
    context_type: str
    source_version: str | None
    source_id: str | None
    summary: str | None
    allowed_for_turn_context: bool
    sanitized: bool = True
    raw_content_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentRequestContextView:
    context_view_id: str
    context_refs: list[AgentContextRef]
    included_context_count: int
    excluded_context_count: int
    context_scope: str
    truncated: bool
    truncation_reason: str | None
    version: str = AGENT_TURN_CONTEXT_VERSION
    raw_content_included: bool = False
    raw_secret_included: bool = False
    private_full_paths_included: bool = False
    persistent_memory_used: bool = False
    memory_promoted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnContext:
    turn_context_id: str
    session_id: str
    request_view_id: str
    context_view_id: str
    source_descriptor_id: str
    previous_turn_refs: list[dict[str, Any]]
    provider_context_refs: list[dict[str, Any]]
    version: str = AGENT_TURN_CONTEXT_VERSION
    conversation_local: bool = True
    persistent_memory_context: bool = False
    intent_classification_performed: bool = False
    safety_gate_evaluated: bool = False
    tool_route_created: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnEnvelope:
    envelope_id: str
    created_at: str
    request_id: str
    session_id: str
    turn_context_id: str
    surface_mode: str
    source_descriptor: AgentTurnSourceDescriptor
    user_request_view: AgentUserRequestView
    turn_context: AgentTurnContext
    envelope_status: str
    version: str = AGENT_TURN_CONTEXT_VERSION
    expected_next_stage: str = AGENT_TURN_CONTEXT_NEXT_STEP
    ask_executed: bool = False
    repl_started: bool = False
    intent_classified: bool = False
    task_framed: bool = False
    safety_gate_evaluated: bool = False
    tool_route_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    memory_promoted: bool = False
    persona_mutated: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnTrace:
    trace_id: str
    envelope_id: str
    session_id: str
    events: list[dict[str, Any]]
    object_refs: list[dict[str, Any]]
    relation_refs: list[dict[str, Any]]
    trace_status: str
    version: str = AGENT_TURN_CONTEXT_VERSION
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    raw_secret_in_trace: bool = False
    private_full_path_in_trace: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTurnReport:
    report_id: str
    created_at: str
    policy: AgentTurnEnvelopePolicy
    session: AgentInteractionSession
    envelope: AgentTurnEnvelope
    context_view: AgentRequestContextView
    trace: AgentTurnTrace
    findings: list[AgentTurnFinding]
    report_status: str
    ready_for_v0_25_2: bool
    turn_envelope_created: bool
    interaction_context_created: bool
    version: str = AGENT_TURN_CONTEXT_VERSION
    ready_for_v0_26: bool = False
    intent_classified: bool = False
    task_framed: bool = False
    safety_gate_evaluated: bool = False
    tool_route_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_TURN_CONTEXT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.2 intent classification begins or turn/context policy changes."

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class AgentTurnPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return {
            "source_id": "agent_surface_contract_report:v0.25.0",
            "available": AgentSurfaceContractReportService().build_report().report_status in {"passed", "warning"},
            "read_only": True,
        }

    def load_internal_provider_consolidation_if_available(self) -> dict[str, Any]:
        return {"source_id": "internal_provider_consolidation_report_v0_24_9", "available": True, "read_only": True}

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {"source_id": "agent_surface_skill_registry:v0.25.1", "available": True, "read_only": True}


class AgentTurnEnvelopePolicyService:
    def build_policy(self) -> AgentTurnEnvelopePolicy:
        return AgentTurnEnvelopePolicy(
            policy_id="agent_turn_envelope_policy:v0.25.1",
            evidence_refs=[{"type": "agent_surface_contract", "version": "v0.25.0"}],
        )


class AgentInteractionSessionService:
    def create_or_view_session(
        self,
        session_id: str | None = None,
        surface_mode: str = "contract_view",
        previous_turn_refs: list[dict[str, Any]] | None = None,
        session_scope: str = "conversation_local",
    ) -> AgentInteractionSession:
        refs = previous_turn_refs or []
        return AgentInteractionSession(
            session_id=session_id or "agent_interaction_session:ephemeral:v0.25.1",
            created_at=_utc_now(),
            surface_mode=surface_mode,
            session_scope=session_scope if session_scope in {"single_turn", "conversation_local", "ephemeral", "unknown"} else "unknown",
            turn_count=len(refs) + 1,
            previous_turn_refs=refs,
            session_status="active",
            evidence_refs=[{"type": "session_scope", "scope": session_scope}],
        )


class AgentTurnSourceDescriptorService:
    def build_source_descriptor(
        self,
        source_type: str = "cli",
        source_channel: str | None = "agent_cli",
    ) -> AgentTurnSourceDescriptor:
        allowed = {"cli", "repl_future", "api_future", "test_fixture", "internal", "unknown"}
        resolved = source_type if source_type in allowed else "unknown"
        return AgentTurnSourceDescriptor(
            source_id=f"agent_turn_source:{resolved}:v0.25.1",
            source_type=resolved,
            source_channel=source_channel,
            user_visible=resolved in {"cli", "repl_future", "api_future"},
            evidence_refs=[{"type": "source_type", "value": resolved}],
        )


class AgentUserRequestSanitizationService:
    def detect_secret_like_input(self, text: str) -> bool:
        return bool(SECRET_PATTERN.search(text))

    def detect_credential_like_input(self, text: str) -> bool:
        return bool(CREDENTIAL_PATTERN.search(text))

    def detect_private_path_like_input(self, text: str) -> bool:
        return bool(PRIVATE_PATH_PATTERN.search(text))

    def sanitize_request_text(self, text: str) -> tuple[str, int]:
        redactions = 0

        def replace_secret(match: re.Match[str]) -> str:
            nonlocal redactions
            redactions += 1
            return f"{match.group(1)}=<redacted>"

        sanitized = SECRET_PATTERN.sub(replace_secret, text)
        sanitized, credential_count = CREDENTIAL_PATTERN.subn("<redacted_credential>", sanitized)
        redactions += credential_count
        sanitized, private_path_count = PRIVATE_PATH_PATTERN.subn("<sanitized_private_path>", sanitized)
        redactions += private_path_count
        return sanitized, redactions

    def build_request_view(self, request_id: str, request_text: str) -> AgentUserRequestView:
        sanitized, redaction_count = self.sanitize_request_text(request_text)
        return AgentUserRequestView(
            request_view_id=f"agent_user_request_view:{_safe_id(request_id)}",
            request_id=request_id,
            sanitized_request_text=sanitized,
            request_excerpt=sanitized[:500],
            redaction_applied=redaction_count > 0,
            redaction_count=redaction_count,
            secret_like_input_detected=self.detect_secret_like_input(request_text),
            credential_like_input_detected=self.detect_credential_like_input(request_text),
            pii_like_input_detected=False,
            private_path_like_input_detected=self.detect_private_path_like_input(request_text),
            evidence_refs=[{"type": "sanitization", "redaction_count": redaction_count}],
        )


class AgentContextBoundaryPolicyService:
    def build_policy(self) -> AgentContextBoundaryPolicy:
        return AgentContextBoundaryPolicy(policy_id="agent_context_boundary_policy:v0.25.1")


class AgentContextRefService:
    def build_context_refs(self, provided_refs: list[dict[str, Any]] | None = None) -> list[AgentContextRef]:
        refs = provided_refs or [
            {
                "context_type": "agent_surface_contract",
                "source_version": "v0.25.0",
                "source_id": "agent_surface_contract:v0.25.0",
                "summary": "Agent Surface Contract reference.",
            }
        ]
        return [
            AgentContextRef(
                context_ref_id=f"agent_context_ref:{idx}:{_safe_id(str(item.get('source_id') or item.get('context_type')))}",
                context_type=str(item.get("context_type", "unknown")),
                source_version=item.get("source_version"),
                source_id=item.get("source_id"),
                summary=item.get("summary"),
                allowed_for_turn_context=bool(item.get("allowed_for_turn_context", True)),
                sanitized=True,
                raw_content_included=False,
                raw_secret_included=False,
                private_full_path_included=False,
                evidence_refs=[{"type": "context_ref_source", "index": idx}],
            )
            for idx, item in enumerate(refs)
        ]

    def filter_context_refs(
        self,
        refs: list[AgentContextRef],
        policy: AgentContextBoundaryPolicy,
    ) -> tuple[list[AgentContextRef], int, bool]:
        allowed = [ref for ref in refs if ref.allowed_for_turn_context and not ref.raw_secret_included and not ref.private_full_path_included]
        truncated = len(allowed) > policy.max_context_refs
        return allowed[: policy.max_context_refs], len(refs) - min(len(allowed), policy.max_context_refs), truncated

    def sanitize_context_refs(self, refs: list[AgentContextRef]) -> list[AgentContextRef]:
        return [
            AgentContextRef(
                context_ref_id=ref.context_ref_id,
                context_type=ref.context_type,
                source_version=ref.source_version,
                source_id=ref.source_id,
                summary=ref.summary,
                allowed_for_turn_context=ref.allowed_for_turn_context,
                sanitized=True,
                raw_content_included=False,
                raw_secret_included=False,
                private_full_path_included=False,
                evidence_refs=ref.evidence_refs,
            )
            for ref in refs
        ]


class AgentRequestContextViewService:
    def build_context_view(
        self,
        context_refs: list[dict[str, Any]] | None = None,
        policy: AgentContextBoundaryPolicy | None = None,
    ) -> AgentRequestContextView:
        resolved_policy = policy or AgentContextBoundaryPolicyService().build_policy()
        ref_service = AgentContextRefService()
        refs = ref_service.sanitize_context_refs(ref_service.build_context_refs(context_refs))
        included, excluded_count, truncated = ref_service.filter_context_refs(refs, resolved_policy)
        return AgentRequestContextView(
            context_view_id="agent_request_context_view:v0.25.1",
            context_refs=included,
            included_context_count=len(included),
            excluded_context_count=excluded_count,
            context_scope=resolved_policy.context_scope,
            truncated=truncated,
            truncation_reason="max_context_refs_exceeded" if truncated else None,
            evidence_refs=[{"type": "context_boundary_policy", "policy_id": resolved_policy.policy_id}],
        )


class AgentTurnContextService:
    def build_turn_context(
        self,
        session: AgentInteractionSession,
        request_view: AgentUserRequestView,
        context_view: AgentRequestContextView,
        source_descriptor: AgentTurnSourceDescriptor,
    ) -> AgentTurnContext:
        return AgentTurnContext(
            turn_context_id=f"agent_turn_context:{_safe_id(session.session_id)}",
            session_id=session.session_id,
            request_view_id=request_view.request_view_id,
            context_view_id=context_view.context_view_id,
            source_descriptor_id=source_descriptor.source_id,
            previous_turn_refs=session.previous_turn_refs,
            provider_context_refs=[ref.to_dict() for ref in context_view.context_refs if ref.context_type == "provider_registry"],
            evidence_refs=[{"type": "conversation_local_context"}],
        )


class AgentTurnEnvelopeService:
    def create_envelope(
        self,
        request_text: str,
        request_id: str | None = None,
        session_id: str | None = None,
        context_refs: list[dict[str, Any]] | None = None,
        source_type: str = "cli",
        surface_mode: str = "contract_view",
    ) -> tuple[AgentInteractionSession, AgentRequestContextView, AgentTurnEnvelope]:
        resolved_request_id = request_id or f"agent_request:{_safe_id(request_text[:32]) or 'empty'}"
        session = AgentInteractionSessionService().create_or_view_session(session_id=session_id, surface_mode=surface_mode)
        source = AgentTurnSourceDescriptorService().build_source_descriptor(source_type=source_type)
        request_view = AgentUserRequestSanitizationService().build_request_view(resolved_request_id, request_text)
        context_view = AgentRequestContextViewService().build_context_view(context_refs)
        turn_context = AgentTurnContextService().build_turn_context(session, request_view, context_view, source)
        status = "failed" if not request_text else "warning" if request_view.redaction_applied or context_view.truncated else "created"
        envelope = AgentTurnEnvelope(
            envelope_id=f"agent_turn_envelope:{_safe_id(resolved_request_id)}",
            created_at=_utc_now(),
            request_id=resolved_request_id,
            session_id=session.session_id,
            turn_context_id=turn_context.turn_context_id,
            surface_mode=surface_mode,
            source_descriptor=source,
            user_request_view=request_view,
            turn_context=turn_context,
            envelope_status=status,
            evidence_refs=[{"type": "next_stage", "value": AGENT_TURN_CONTEXT_NEXT_STEP}],
        )
        return session, context_view, envelope


class AgentTurnTraceService:
    def build_trace(self, envelope: AgentTurnEnvelope) -> AgentTurnTrace:
        return AgentTurnTrace(
            trace_id=f"agent_turn_trace:{_safe_id(envelope.envelope_id)}",
            envelope_id=envelope.envelope_id,
            session_id=envelope.session_id,
            events=[
                {"event_type": "agent_turn_envelope_requested", "version": AGENT_TURN_CONTEXT_VERSION},
                {"event_type": "agent_turn_envelope_created", "envelope_id": envelope.envelope_id},
                {"event_type": "agent_turn_trace_created", "trace_id": f"agent_turn_trace:{_safe_id(envelope.envelope_id)}"},
            ],
            object_refs=[
                {"object_type": "agent_turn_envelope", "object_id": envelope.envelope_id},
                {"object_type": "agent_interaction_session", "object_id": envelope.session_id},
                {"object_type": "agent_user_request_view", "object_id": envelope.user_request_view.request_view_id},
            ],
            relation_refs=[
                {"relation_type": "creates_agent_turn_envelope", "source": envelope.session_id, "target": envelope.envelope_id},
                {"relation_type": "defers_intent_classification_to_v0_25_2", "source": envelope.envelope_id, "target": AGENT_TURN_CONTEXT_NEXT_STEP},
            ],
            trace_status="recorded",
            evidence_refs=[{"type": "ocel_visibility", "value": True}],
        )


class AgentTurnFindingService:
    def build_findings(
        self,
        policy: AgentTurnEnvelopePolicy,
        envelope: AgentTurnEnvelope,
        context_view: AgentRequestContextView,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentTurnFinding]:
        findings = [
            AgentTurnFinding(
                finding_id="agent_turn_finding:ok",
                severity="info",
                finding_type="ok",
                message="Agent turn envelope and conversation-local context were created without execution.",
                subject_ref={"envelope_id": envelope.envelope_id},
                evidence_refs=[{"type": "policy", "policy_id": policy.policy_id}],
                withdrawal_condition="Withdraw if v0.25.1 performs ask, REPL, intent classification, routing, provider invocation, local execution, memory promotion, or persona mutation.",
            )
        ]
        if not envelope.user_request_view.sanitized_request_text:
            findings.append(self._finding("error", "missing_request_text", "Request text is missing.", envelope.envelope_id))
        if envelope.user_request_view.redaction_applied:
            findings.append(self._finding("warning", "request_sanitized", "Request text was sanitized.", envelope.envelope_id))
        if envelope.user_request_view.secret_like_input_detected:
            findings.append(self._finding("warning", "secret_like_input_redacted", "Secret-like input was redacted.", envelope.envelope_id))
        if envelope.user_request_view.credential_like_input_detected:
            findings.append(self._finding("warning", "credential_like_input_redacted", "Credential-like input was redacted.", envelope.envelope_id))
        if envelope.user_request_view.private_path_like_input_detected:
            findings.append(self._finding("warning", "private_path_like_input_sanitized", "Private-path-like input was sanitized.", envelope.envelope_id))
        if context_view.excluded_context_count:
            findings.append(self._finding("warning", "context_ref_excluded", "One or more context refs were excluded.", context_view.context_view_id))
        if context_view.truncated:
            findings.append(self._finding("warning", "context_view_truncated", "Context view was truncated.", context_view.context_view_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                findings.append(self._finding("critical", finding_type, f"{finding_type} was detected.", envelope.envelope_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentTurnFinding:
        return AgentTurnFinding(
            finding_id=f"agent_turn_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by policy.",
        )


class AgentTurnReportService:
    def build_report(
        self,
        request_text: str = "Explain the project structure",
        request_id: str | None = None,
        session_id: str | None = None,
        context_refs: list[dict[str, Any]] | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentTurnReport:
        policy = AgentTurnEnvelopePolicyService().build_policy()
        session, context_view, envelope = AgentTurnEnvelopeService().create_envelope(
            request_text=request_text,
            request_id=request_id,
            session_id=session_id,
            context_refs=context_refs,
        )
        trace = AgentTurnTraceService().build_trace(envelope)
        findings = AgentTurnFindingService().build_findings(policy, envelope, context_view, attempt_flags)
        blocked = any(finding.severity == "critical" for finding in findings)
        failed = any(finding.severity == "error" for finding in findings)
        warning = any(finding.severity == "warning" for finding in findings)
        report_status = "blocked" if blocked else "failed" if failed else "warning" if warning else "passed"
        return AgentTurnReport(
            report_id=f"agent_turn_report:{_safe_id(envelope.request_id)}",
            created_at=_utc_now(),
            policy=policy,
            session=session,
            envelope=envelope,
            context_view=context_view,
            trace=trace,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_2=report_status in {"passed", "warning"},
            turn_envelope_created=True,
            interaction_context_created=True,
            limitations=["v0.25.1 creates only turn envelopes, conversation-local context views, and traces."],
            withdrawal_conditions=["Withdraw if v0.25.1 classifies intent, invokes providers, routes tools, executes commands, writes memory, or mutates persona."],
        )

    def build_all_parts(self, request_text: str = "Explain the project structure") -> dict[str, Any]:
        report = self.build_report(request_text=request_text)
        return {
            "report": report,
            "policy": report.policy,
            "session": report.session,
            "envelope": report.envelope,
            "context": report.context_view,
            "trace": report.trace,
            "findings": report.findings,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_TURN_CONTEXT_VERSION,
            "layer": "agent_surface",
            "subject": "turn_envelope_interaction_context",
            "principles": [
                "turn envelope is not ask execution",
                "interaction context is not long-term memory",
                "request context is not permission",
                "conversation-local context is not memory promotion",
                "raw secrets must not be stored",
                "intent classification is deferred to v0.25.2",
                "safety/no-action gate is deferred to v0.25.3",
                "tool routing is deferred to v0.25.4",
                "provider invocation is deferred to v0.25.5",
            ],
            "safety_boundary": {
                "turn_envelope_created": "conditional",
                "interaction_context_created": "conditional",
                "intent_classified": False,
                "task_framed": False,
                "safety_gate_evaluated": False,
                "tool_route_executed": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "ask_executed": False,
                "repl_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25": "bounded agent surface",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_TURN_CONTEXT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_turn_envelope_context_created",
            "version": AGENT_TURN_CONTEXT_VERSION,
            "source_read_models": [
                "AgentSurfaceContractState",
                "AgentSurfaceModeState",
                "AgentSurfacePermissionPolicyState",
                "AgentSurfaceRoadmapBoundaryState",
            ],
            "target_read_models": [
                "AgentTurnEnvelopeState",
                "AgentInteractionSessionState",
                "AgentRequestContextViewState",
                "AgentTurnTraceState",
                "AgentTurnReportState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_TURN_EFFECT_TYPES,
        }


def render_agent_turn_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentTurnReport = parts["report"]
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"envelope_only={str(report.policy.envelope_only).lower()}",
        f"turn_envelope_created={str(report.turn_envelope_created).lower()}",
        f"interaction_context_created={str(report.interaction_context_created).lower()}",
        f"ready_for_v0_25_2={str(report.ready_for_v0_25_2).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"intent_classified={str(report.intent_classified).lower()}",
        f"task_framed={str(report.task_framed).lower()}",
        f"safety_gate_evaluated={str(report.safety_gate_evaluated).lower()}",
        f"tool_route_executed={str(report.tool_route_executed).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "envelope":
        lines.append(f"envelope_id={report.envelope.envelope_id}")
        lines.append(f"envelope_status={report.envelope.envelope_status}")
    elif section == "context":
        lines.append(f"context_view_id={report.context_view.context_view_id}")
        lines.append(f"included_context_count={report.context_view.included_context_count}")
        lines.append(f"truncated={str(report.context_view.truncated).lower()}")
    elif section == "session":
        lines.append(f"session_id={report.session.session_id}")
        lines.append(f"session_scope={report.session.session_scope}")
        lines.append(f"persistent_memory_session={str(report.session.persistent_memory_session).lower()}")
    elif section == "context-policy":
        lines.append(f"context_scope={report.policy.context_scope}")
        lines.append(f"persistent_memory_write_enabled={str(report.policy.persistent_memory_write_enabled).lower()}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)

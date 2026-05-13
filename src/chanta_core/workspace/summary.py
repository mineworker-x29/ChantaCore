from __future__ import annotations

import ast
import json
import re
import tomllib
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.ids import (
    new_workspace_read_summary_candidate_id,
    new_workspace_read_summary_finding_id,
    new_workspace_read_summary_policy_id,
    new_workspace_read_summary_request_id,
    new_workspace_read_summary_result_id,
    new_workspace_read_summary_section_id,
)
from chanta_core.workspace.read_service import WorkspaceReadService, hash_content, preview_text


SUPPORTED_INPUT_KINDS = ["markdown", "text", "json", "yaml", "toml", "python", "generic_text"]


@dataclass(frozen=True)
class WorkspaceReadSummaryPolicy:
    policy_id: str
    policy_name: str
    supported_input_kinds: list[str]
    max_input_chars: int
    max_preview_chars: int
    max_sections: int
    max_section_preview_chars: int
    allow_llm_summary: bool
    allow_private_summary: bool
    require_review_for_promotion: bool
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "supported_input_kinds": list(self.supported_input_kinds), "policy_attrs": dict(self.policy_attrs)}


@dataclass(frozen=True)
class WorkspaceReadSummaryRequest:
    summary_request_id: str
    envelope_id: str | None
    output_snapshot_id: str | None
    artifact_ref_id: str | None
    source_kind: str
    source_ref: str | None
    input_kind: str
    file_name: str | None
    relative_path_redacted: str | None
    requested_by: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "request_attrs": dict(self.request_attrs)}


@dataclass(frozen=True)
class WorkspaceReadSummarySection:
    section_id: str
    summary_request_id: str
    section_type: str
    title: str
    level: int | None
    order_index: int
    preview: str
    char_count: int
    line_start: int | None
    line_end: int | None
    created_at: str
    section_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "section_attrs": dict(self.section_attrs)}


@dataclass(frozen=True)
class WorkspaceReadSummaryResult:
    summary_result_id: str
    summary_request_id: str
    status: str
    input_kind: str
    summary_title: str
    summary_text: str
    section_ids: list[str]
    input_char_count: int
    input_line_count: int
    truncated: bool
    private: bool
    sensitive: bool
    finding_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "section_ids": list(self.section_ids), "finding_ids": list(self.finding_ids), "result_attrs": dict(self.result_attrs)}


@dataclass(frozen=True)
class WorkspaceReadSummaryCandidate:
    summary_candidate_id: str
    summary_result_id: str
    envelope_id: str | None
    target_kind: str
    candidate_title: str
    candidate_preview: str
    candidate_hash: str
    review_status: str
    promotion_candidate_id: str | None
    canonical_promotion_enabled: bool
    created_at: str
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "candidate_attrs": dict(self.candidate_attrs)}


@dataclass(frozen=True)
class WorkspaceReadSummaryFinding:
    finding_id: str
    summary_request_id: str
    summary_result_id: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "finding_attrs": dict(self.finding_attrs)}


class WorkspaceReadSummarizationService:
    def __init__(
        self,
        *,
        promotion_service: Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.ocel_store = ocel_store or OCELStore()
        self.trace_service = trace_service or TraceService(ocel_store=self.ocel_store)
        self.promotion_service = promotion_service
        self.last_policy: WorkspaceReadSummaryPolicy | None = None
        self.last_request: WorkspaceReadSummaryRequest | None = None
        self.last_sections: list[WorkspaceReadSummarySection] = []
        self.last_findings: list[WorkspaceReadSummaryFinding] = []
        self.last_result: WorkspaceReadSummaryResult | None = None
        self.last_candidate: WorkspaceReadSummaryCandidate | None = None

    def create_default_policy(self) -> WorkspaceReadSummaryPolicy:
        policy = WorkspaceReadSummaryPolicy(
            policy_id=new_workspace_read_summary_policy_id(),
            policy_name="Default Workspace Read Summary Policy",
            supported_input_kinds=list(SUPPORTED_INPUT_KINDS),
            max_input_chars=100000,
            max_preview_chars=2000,
            max_sections=40,
            max_section_preview_chars=500,
            allow_llm_summary=False,
            allow_private_summary=True,
            require_review_for_promotion=True,
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={
                "deterministic": True,
                "memory_entries_written": False,
                "persona_updated": False,
                "overlay_updated": False,
            },
        )
        self.last_policy = policy
        self._record("workspace_read_summary_policy_registered", [_object("workspace_read_summary_policy", policy.policy_id, policy.to_dict())], [("workspace_read_summary_policy_object", policy.policy_id)], [], {"status": policy.status})
        return policy

    def create_summary_request(
        self,
        *,
        input_kind: str,
        file_name: str | None = None,
        relative_path: str | None = None,
        envelope_id: str | None = None,
        output_snapshot_id: str | None = None,
        artifact_ref_id: str | None = None,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> WorkspaceReadSummaryRequest:
        source_ref = output_snapshot_id or artifact_ref_id or envelope_id
        request = WorkspaceReadSummaryRequest(
            summary_request_id=new_workspace_read_summary_request_id(),
            envelope_id=envelope_id,
            output_snapshot_id=output_snapshot_id,
            artifact_ref_id=artifact_ref_id,
            source_kind="workspace_text" if source_ref is None else "execution_output",
            source_ref=source_ref,
            input_kind=input_kind,
            file_name=file_name,
            relative_path_redacted="<REDACTED_PATH>" if relative_path else None,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            created_at=utc_now_iso(),
            request_attrs={"deterministic": True, "uses_llm": False, "full_body_stored": False},
        )
        self.last_request = request
        links = [("workspace_read_summary_request_object", request.summary_request_id)]
        if envelope_id:
            links.append(("execution_envelope_object", envelope_id))
        if output_snapshot_id:
            links.append(("execution_output_snapshot_object", output_snapshot_id))
        if artifact_ref_id:
            links.append(("execution_artifact_ref_object", artifact_ref_id))
        self._record("workspace_read_summary_requested", [_object("workspace_read_summary_request", request.summary_request_id, request.to_dict())], links, [], {"input_kind": input_kind})
        return request

    def summarize_from_text(
        self,
        *,
        text: str,
        input_kind: str,
        file_name: str | None = None,
        relative_path: str | None = None,
        envelope_id: str | None = None,
        output_snapshot_id: str | None = None,
        artifact_ref_id: str | None = None,
        private: bool = False,
        policy: WorkspaceReadSummaryPolicy | None = None,
    ) -> WorkspaceReadSummaryResult:
        active_policy = policy or self.create_default_policy()
        self.last_sections = []
        self.last_findings = []
        kind = _normalize_kind(input_kind, file_name)
        request = self.create_summary_request(
            input_kind=kind,
            file_name=file_name,
            relative_path=relative_path,
            envelope_id=envelope_id,
            output_snapshot_id=output_snapshot_id,
            artifact_ref_id=artifact_ref_id,
        )
        if kind not in active_policy.supported_input_kinds:
            self.record_finding(request=request, result_id=None, finding_type="unsupported_input_kind", status="unsupported", severity="medium", message="Input kind is not supported.", subject_ref=kind)
            return self.record_result(request=request, status="unsupported", input_kind=kind, summary_title="Unsupported input", summary_text="", text=text, truncated=False, private=private, sensitive=False)
        truncated = len(text) > active_policy.max_input_chars
        source_text = text[: active_policy.max_input_chars] if truncated else text
        if truncated:
            self.record_finding(request=request, result_id=None, finding_type="input_truncated", status="truncated", severity="medium", message="Input was truncated before summarization.", subject_ref=str(len(text)))
        summary_title, summary_text, section_specs = self._summarize_by_kind(kind, source_text, active_policy)
        for index, spec in enumerate(section_specs[: active_policy.max_sections]):
            self.record_section(request=request, order_index=index, **spec)
        return self.record_result(
            request=request,
            status="completed",
            input_kind=kind,
            summary_title=summary_title,
            summary_text=summary_text[: active_policy.max_preview_chars],
            text=source_text,
            truncated=truncated,
            private=private,
            sensitive=_has_sensitive_marker(source_text),
        )

    def summarize_from_execution_output(self, *, output_preview: Any, input_kind: str, envelope_id: str | None = None, output_snapshot_id: str | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=_preview_to_text(output_preview), input_kind=input_kind, envelope_id=envelope_id, output_snapshot_id=output_snapshot_id)

    def summarize_from_envelope(self, *, envelope_id: str, output_preview: Any, input_kind: str) -> WorkspaceReadSummaryResult:
        return self.summarize_from_execution_output(output_preview=output_preview, input_kind=input_kind, envelope_id=envelope_id)

    def summarize_markdown(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="markdown", policy=policy)

    def summarize_plain_text(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="text", policy=policy)

    def summarize_json(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="json", policy=policy)

    def summarize_yaml(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="yaml", policy=policy)

    def summarize_toml(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="toml", policy=policy)

    def summarize_python(self, text: str, policy: WorkspaceReadSummaryPolicy | None = None) -> WorkspaceReadSummaryResult:
        return self.summarize_from_text(text=text, input_kind="python", policy=policy)

    def record_section(self, *, request: WorkspaceReadSummaryRequest, section_type: str, title: str, level: int | None, order_index: int, preview: str, char_count: int, line_start: int | None = None, line_end: int | None = None, section_attrs: dict[str, Any] | None = None) -> WorkspaceReadSummarySection:
        section = WorkspaceReadSummarySection(new_workspace_read_summary_section_id(), request.summary_request_id, section_type, title, level, order_index, preview, char_count, line_start, line_end, utc_now_iso(), {"full_body_stored": False, **dict(section_attrs or {})})
        self.last_sections.append(section)
        self._record("workspace_read_summary_section_created", [_object("workspace_read_summary_section", section.section_id, section.to_dict())], [("workspace_read_summary_section_object", section.section_id), ("workspace_read_summary_request_object", request.summary_request_id)], [(section.section_id, request.summary_request_id, "belongs_to_request")], {"section_type": section_type})
        return section

    def record_finding(self, *, request: WorkspaceReadSummaryRequest, result_id: str | None, finding_type: str, status: str, severity: str, message: str, subject_ref: str | None = None) -> WorkspaceReadSummaryFinding:
        finding = WorkspaceReadSummaryFinding(new_workspace_read_summary_finding_id(), request.summary_request_id, result_id, finding_type, status, severity, message, subject_ref, utc_now_iso(), {"uses_llm": False})
        self.last_findings.append(finding)
        self._record("workspace_read_summary_finding_recorded", [_object("workspace_read_summary_finding", finding.finding_id, finding.to_dict())], [("workspace_read_summary_finding_object", finding.finding_id), ("workspace_read_summary_request_object", request.summary_request_id)], [(finding.finding_id, request.summary_request_id, "belongs_to_request")], {"finding_type": finding_type, "status": status})
        return finding

    def record_result(self, *, request: WorkspaceReadSummaryRequest, status: str, input_kind: str, summary_title: str, summary_text: str, text: str, truncated: bool, private: bool, sensitive: bool) -> WorkspaceReadSummaryResult:
        result = WorkspaceReadSummaryResult(new_workspace_read_summary_result_id(), request.summary_request_id, status, input_kind, summary_title, summary_text, [item.section_id for item in self.last_sections], len(text), len(text.splitlines()), truncated, private, sensitive, [item.finding_id for item in self.last_findings], utc_now_iso(), {"uses_llm": False, "memory_entries_written": False, "persona_updated": False, "overlay_updated": False, "full_body_stored": False})
        self.last_result = result
        for idx, finding in enumerate(self.last_findings):
            if finding.summary_result_id is None:
                self.last_findings[idx] = WorkspaceReadSummaryFinding(finding.finding_id, finding.summary_request_id, result.summary_result_id, finding.finding_type, finding.status, finding.severity, finding.message, finding.subject_ref, finding.created_at, finding.finding_attrs)
        activity = "workspace_read_summary_completed" if status == "completed" else ("workspace_read_summary_skipped" if status == "unsupported" else "workspace_read_summary_failed")
        self._record(activity, [_object("workspace_read_summary_result", result.summary_result_id, result.to_dict())], [("workspace_read_summary_result_object", result.summary_result_id), ("workspace_read_summary_request_object", request.summary_request_id)], [(result.summary_result_id, request.summary_request_id, "summarizes_request")] + [(result.summary_result_id, sid, "includes_section") for sid in result.section_ids], {"status": status, "input_kind": input_kind})
        return result

    def create_summary_candidate(self, *, result: WorkspaceReadSummaryResult, target_kind: str = "workspace_summary_candidate", promotion_candidate_id: str | None = None) -> WorkspaceReadSummaryCandidate:
        candidate = WorkspaceReadSummaryCandidate(new_workspace_read_summary_candidate_id(), result.summary_result_id, self.last_request.envelope_id if self.last_request else None, target_kind, result.summary_title, preview_text(result.summary_text), hash_content(result.summary_text), "pending_review", promotion_candidate_id, False, utc_now_iso(), {"canonical_promotion_enabled": False, "memory_entries_written": False, "persona_updated": False, "overlay_updated": False})
        self.last_candidate = candidate
        links = [("workspace_read_summary_candidate_object", candidate.summary_candidate_id), ("workspace_read_summary_result_object", result.summary_result_id)]
        if promotion_candidate_id:
            links.append(("execution_result_promotion_candidate_object", promotion_candidate_id))
        self._record("workspace_read_summary_candidate_created", [_object("workspace_read_summary_candidate", candidate.summary_candidate_id, candidate.to_dict())], links, [(candidate.summary_candidate_id, result.summary_result_id, "derived_from_summary_result")], {"target_kind": target_kind, "review_status": candidate.review_status})
        return candidate

    def render_summary_cli(self, result: WorkspaceReadSummaryResult | None = None) -> str:
        item = result or self.last_result
        if item is None:
            return "Workspace Read Summary: unavailable"
        return "\n".join(["Workspace Read Summary", f"status={item.status}", f"summary_result_id={item.summary_result_id}", f"input_kind={item.input_kind}", f"title={item.summary_title}", f"section_count={len(item.section_ids)}", f"truncated={str(item.truncated).lower()}", f"canonical_promotion_enabled=false", item.summary_text])

    def _summarize_by_kind(self, kind: str, text: str, policy: WorkspaceReadSummaryPolicy) -> tuple[str, str, list[dict[str, Any]]]:
        if kind == "markdown":
            return _summarize_markdown(text, policy)
        if kind in {"text", "generic_text"}:
            return _summarize_text(text, policy)
        if kind == "json":
            return _summarize_json(text)
        if kind == "yaml":
            return _summarize_yaml(text)
        if kind == "toml":
            return _summarize_toml(text)
        if kind == "python":
            return _summarize_python(text, policy)
        return _summarize_text(text, policy)

    def _record(self, activity: str, objects: list[OCELObject], links: list[tuple[str, str]], object_links: list[tuple[str, str, str]], attrs: dict[str, Any]) -> None:
        event = OCELEvent(f"evt:{uuid4()}", activity, utc_now_iso(), {**attrs, "runtime_event_type": activity, "source_runtime": "chanta_core", "workspace_read_summary": True, "deterministic": True, "uses_llm": False, "skills_executed": False, "permission_grants_created": False})
        relations = [OCELRelation.event_object(event_id=event.event_id, object_id=oid, qualifier=q) for q, oid in links if oid]
        relations.extend(OCELRelation.object_object(source_object_id=s, target_object_id=t, qualifier=q) for s, t, q in object_links if s and t)
        self.trace_service.record_session_ocel_record(OCELRecord(event, objects, relations))


def summarize_file_via_workspace_read(*, root_path: str, relative_path: str, ocel_store: OCELStore | None = None) -> WorkspaceReadSummaryResult:
    read_service = WorkspaceReadService(ocel_store=ocel_store)
    root = read_service.register_read_root(root_path)
    read_result = read_service.read_workspace_text_file(root=root, relative_path=relative_path)
    service = WorkspaceReadSummarizationService(ocel_store=ocel_store)
    if read_result.denied:
        request = service.create_summary_request(input_kind="generic_text", file_name=relative_path, relative_path=relative_path)
        service.record_finding(request=request, result_id=None, finding_type="workspace_read_denied", status="failed", severity="high", message="Workspace read was denied.", subject_ref=relative_path)
        return service.record_result(request=request, status="failed", input_kind="generic_text", summary_title="Workspace read denied", summary_text="", text="", truncated=False, private=False, sensitive=False)
    return service.summarize_from_text(text=read_result.content, input_kind=_normalize_kind("auto", relative_path), file_name=relative_path, relative_path=relative_path)


def summary_result_from_dict(value: dict[str, Any]) -> WorkspaceReadSummaryResult:
    return WorkspaceReadSummaryResult(
        summary_result_id=str(value["summary_result_id"]),
        summary_request_id=str(value["summary_request_id"]),
        status=str(value.get("status") or "unknown"),
        input_kind=str(value.get("input_kind") or "generic_text"),
        summary_title=str(value.get("summary_title") or "Workspace Read Summary"),
        summary_text=str(value.get("summary_text") or ""),
        section_ids=list(value.get("section_ids") or []),
        input_char_count=int(value.get("input_char_count") or 0),
        input_line_count=int(value.get("input_line_count") or 0),
        truncated=bool(value.get("truncated")),
        private=bool(value.get("private")),
        sensitive=bool(value.get("sensitive")),
        finding_ids=list(value.get("finding_ids") or []),
        created_at=str(value.get("created_at") or utc_now_iso()),
        result_attrs=dict(value.get("result_attrs") or {}),
    )


def _summarize_markdown(text: str, policy: WorkspaceReadSummaryPolicy) -> tuple[str, str, list[dict[str, Any]]]:
    sections = []
    lines = text.splitlines()
    for line_no, line in enumerate(lines, start=1):
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            sections.append({"section_type": "markdown_heading", "title": match.group(2).strip(), "level": len(match.group(1)), "preview": "", "char_count": len(line), "line_start": line_no, "line_end": line_no})
    outline = [f"{'#' * (item['level'] or 1)} {item['title']}" for item in sections[: policy.max_sections]]
    title = sections[0]["title"] if sections else "Markdown summary"
    return title, "\n".join(outline) if outline else preview_text(text, policy.max_preview_chars), sections


def _summarize_text(text: str, policy: WorkspaceReadSummaryPolicy) -> tuple[str, str, list[dict[str, Any]]]:
    lines = text.splitlines()
    preview = "\n".join(lines[:10])[: policy.max_preview_chars]
    return "Text summary", f"Lines: {len(lines)}\nCharacters: {len(text)}\nPreview:\n{preview}", [{"section_type": "text_preview", "title": "Preview", "level": None, "preview": preview[: policy.max_section_preview_chars], "char_count": len(preview), "line_start": 1 if lines else None, "line_end": min(10, len(lines)) if lines else None}]


def _summarize_json(text: str) -> tuple[str, str, list[dict[str, Any]]]:
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            items = {str(k): type(v).__name__ for k, v in value.items()}
            summary = "JSON keys: " + ", ".join(f"{k}:{v}" for k, v in items.items())
        elif isinstance(value, list):
            summary = f"JSON list length: {len(value)}"
        else:
            summary = f"JSON root type: {type(value).__name__}"
    except Exception as error:
        summary = f"JSON parse failed: {error}"
    return "JSON summary", summary, [{"section_type": "json_shallow_keys", "title": "Top-level", "level": None, "preview": summary, "char_count": len(summary), "line_start": None, "line_end": None}]


def _summarize_yaml(text: str) -> tuple[str, str, list[dict[str, Any]]]:
    keys = [line.split(":", 1)[0].strip() for line in text.splitlines() if line and not line.startswith((" ", "-")) and ":" in line]
    summary = "YAML keys: " + ", ".join(keys[:40]) if keys else "YAML shallow summary unavailable; fallback preview used."
    return "YAML summary", summary, [{"section_type": "yaml_shallow_keys", "title": "Top-level", "level": None, "preview": summary, "char_count": len(summary), "line_start": None, "line_end": None}]


def _summarize_toml(text: str) -> tuple[str, str, list[dict[str, Any]]]:
    try:
        value = tomllib.loads(text)
        keys = sorted(str(key) for key in value)
        summary = "TOML keys: " + ", ".join(keys)
    except Exception as error:
        summary = f"TOML parse failed: {error}"
    return "TOML summary", summary, [{"section_type": "toml_shallow_keys", "title": "Top-level", "level": None, "preview": summary, "char_count": len(summary), "line_start": None, "line_end": None}]


def _summarize_python(text: str, policy: WorkspaceReadSummaryPolicy) -> tuple[str, str, list[dict[str, Any]]]:
    try:
        tree = ast.parse(text)
        imports = []
        symbols = []
        doc = ast.get_docstring(tree) or ""
        for node in tree.body:
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbols.append(node.name)
    except SyntaxError:
        imports = re.findall(r"^(?:import|from)\s+([\w.]+)", text, flags=re.MULTILINE)
        symbols = re.findall(r"^(?:def|class)\s+(\w+)", text, flags=re.MULTILINE)
        doc = ""
    summary = f"Imports: {', '.join(imports) or 'none'}\nSymbols: {', '.join(symbols) or 'none'}"
    if doc:
        summary += f"\nDocstring: {doc[:policy.max_section_preview_chars]}"
    sections = [
        {"section_type": "python_imports", "title": "Imports", "level": None, "preview": ", ".join(imports), "char_count": len(", ".join(imports)), "line_start": None, "line_end": None},
        {"section_type": "python_symbols", "title": "Symbols", "level": None, "preview": ", ".join(symbols), "char_count": len(", ".join(symbols)), "line_start": None, "line_end": None},
    ]
    return "Python summary", summary, sections


def _normalize_kind(input_kind: str, file_name: str | None) -> str:
    if input_kind != "auto":
        return input_kind
    suffix = (file_name or "").rsplit(".", 1)[-1].lower() if "." in (file_name or "") else ""
    return {"md": "markdown", "markdown": "markdown", "txt": "text", "json": "json", "yaml": "yaml", "yml": "yaml", "toml": "toml", "py": "python"}.get(suffix, "generic_text")


def _preview_to_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _has_sensitive_marker(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ["<redacted>", "secret", "token", "password", "credential"])


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(object_id, object_type, {"object_key": object_id, "display_name": object_id, **attrs})

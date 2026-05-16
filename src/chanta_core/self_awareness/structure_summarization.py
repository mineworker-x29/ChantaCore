from __future__ import annotations

import ast
import json
import re
import tomllib
from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.code_text_perception import (
    SelfCodeTextPerceptionSkillService,
    SelfTextReadPolicyService,
    SelfTextReadRequest,
    SelfTextRedactionFinding,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
    WorkspacePathResolution,
)


STRUCTURE_SUMMARY_EFFECTS = [READ_ONLY_OBSERVATION_EFFECT, "state_candidate_created"]
STRUCTURE_DEFAULT_MAX_BYTES = 65536
STRUCTURE_DEFAULT_MAX_LINES = 1000
STRUCTURE_MAX_BYTES_CAP = 65536
STRUCTURE_MAX_LINES_CAP = 1000
STRUCTURE_ALLOWED_MODES = {"auto", "markdown", "python", "json", "yaml", "toml", "plain_text"}
MARKDOWN_SUFFIXES = {".md", ".markdown", ".rst"}
PYTHON_SUFFIXES = {".py"}
JSON_SUFFIXES = {".json"}
YAML_SUFFIXES = {".yaml", ".yml"}
TOML_SUFFIXES = {".toml"}


@dataclass(frozen=True)
class SelfStructureSummaryRequest:
    path: str
    root_id: str | None = None
    summary_mode: str = "auto"
    max_bytes: int = STRUCTURE_DEFAULT_MAX_BYTES
    max_lines: int = STRUCTURE_DEFAULT_MAX_LINES
    include_private_sections: bool = False
    include_body_preview: bool = False

    def normalized(self) -> "SelfStructureSummaryRequest":
        mode = self.summary_mode if self.summary_mode in STRUCTURE_ALLOWED_MODES else "auto"
        return SelfStructureSummaryRequest(
            path=self.path or "",
            root_id=self.root_id,
            summary_mode=mode,
            max_bytes=min(max(1, int(self.max_bytes)), STRUCTURE_MAX_BYTES_CAP),
            max_lines=min(max(1, int(self.max_lines)), STRUCTURE_MAX_LINES_CAP),
            include_private_sections=bool(self.include_private_sections),
            include_body_preview=bool(self.include_body_preview),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "root_id": self.root_id,
            "summary_mode": self.summary_mode,
            "max_bytes": self.max_bytes,
            "max_lines": self.max_lines,
            "include_private_sections": self.include_private_sections,
            "include_body_preview": self.include_body_preview,
        }


@dataclass(frozen=True)
class SelfStructureSummaryPolicyDecision:
    allowed: bool
    blocked: bool
    finding_type: str
    reason: str | None
    path_resolution: WorkspacePathResolution
    detected_kind: str | None
    effective_summary_mode: str
    effective_max_bytes: int
    effective_max_lines: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "blocked": self.blocked,
            "finding_type": self.finding_type,
            "reason": self.reason,
            "path_resolution": self.path_resolution.to_dict(),
            "detected_kind": self.detected_kind,
            "effective_summary_mode": self.effective_summary_mode,
            "effective_max_bytes": self.effective_max_bytes,
            "effective_max_lines": self.effective_max_lines,
        }


@dataclass(frozen=True)
class MarkdownHeadingRef:
    level: int
    title: str
    line_number: int
    slug: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "title": self.title,
            "line_number": self.line_number,
            "slug": self.slug,
        }


@dataclass(frozen=True)
class MarkdownStructureSummary:
    headings: list[MarkdownHeadingRef]
    heading_count: int
    max_heading_depth: int
    has_frontmatter: bool
    frontmatter_keys: list[str]
    section_line_ranges: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "headings": [item.to_dict() for item in self.headings],
            "heading_count": self.heading_count,
            "max_heading_depth": self.max_heading_depth,
            "has_frontmatter": self.has_frontmatter,
            "frontmatter_keys": list(self.frontmatter_keys),
            "section_line_ranges": [dict(item) for item in self.section_line_ranges],
        }


@dataclass(frozen=True)
class PythonSymbolRef:
    symbol_type: Literal["import", "from_import", "function", "async_function", "class", "assignment"]
    name: str
    line_number: int
    end_line_number: int | None
    parent: str | None
    decorators: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol_type": self.symbol_type,
            "name": self.name,
            "line_number": self.line_number,
            "end_line_number": self.end_line_number,
            "parent": self.parent,
            "decorators": list(self.decorators),
        }


@dataclass(frozen=True)
class PythonSymbolSummary:
    imports: list[PythonSymbolRef]
    top_level_functions: list[PythonSymbolRef]
    top_level_classes: list[PythonSymbolRef]
    top_level_assignments: list[PythonSymbolRef]
    parse_error: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "imports": [item.to_dict() for item in self.imports],
            "top_level_functions": [item.to_dict() for item in self.top_level_functions],
            "top_level_classes": [item.to_dict() for item in self.top_level_classes],
            "top_level_assignments": [item.to_dict() for item in self.top_level_assignments],
            "parse_error": self.parse_error,
        }


@dataclass(frozen=True)
class ShallowKeySummary:
    file_kind: Literal["json", "yaml", "toml"]
    top_level_keys: list[str]
    nested_key_preview: dict[str, list[str]]
    parse_error: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_kind": self.file_kind,
            "top_level_keys": list(self.top_level_keys),
            "nested_key_preview": {key: list(value) for key, value in self.nested_key_preview.items()},
            "parse_error": self.parse_error,
        }


@dataclass(frozen=True)
class PlainTextPreviewSummary:
    first_non_empty_lines: list[str]
    line_count_seen: int
    bytes_seen: int
    truncated: bool
    redacted: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "first_non_empty_lines": list(self.first_non_empty_lines),
            "line_count_seen": self.line_count_seen,
            "bytes_seen": self.bytes_seen,
            "truncated": self.truncated,
            "redacted": self.redacted,
        }


@dataclass(frozen=True)
class SelfStructureSummaryCandidate:
    candidate_id: str
    source_path: str
    root_id: str
    relative_path: str
    summary_kind: str
    markdown: MarkdownStructureSummary | None
    python: PythonSymbolSummary | None
    shallow_keys: ShallowKeySummary | None
    plain_text: PlainTextPreviewSummary | None
    redaction_findings: list[SelfTextRedactionFinding]
    evidence_refs: list[dict[str, Any]]
    limitations: list[str]
    confidence: Literal["high", "medium", "low"]
    review_status: str = "candidate_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False
    policy_decision: SelfStructureSummaryPolicyDecision | None = None
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_path": self.source_path,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "summary_kind": self.summary_kind,
            "markdown": self.markdown.to_dict() if self.markdown else None,
            "python": self.python.to_dict() if self.python else None,
            "shallow_keys": self.shallow_keys.to_dict() if self.shallow_keys else None,
            "plain_text": self.plain_text.to_dict() if self.plain_text else None,
            "redaction_findings": [item.to_dict() for item in self.redaction_findings],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "limitations": list(self.limitations),
            "confidence": self.confidence,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
            "policy_decision": self.policy_decision.to_dict() if self.policy_decision else None,
            "candidate_attrs": dict(self.candidate_attrs),
        }


class SelfStructureSummaryPolicyService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.text_policy_service = SelfTextReadPolicyService(path_policy_service=self.path_policy_service)

    def decide(self, request: SelfStructureSummaryRequest) -> SelfStructureSummaryPolicyDecision:
        normalized = request.normalized()
        text_decision = self.text_policy_service.decide(
            SelfTextReadRequest(
                path=normalized.path,
                root_id=normalized.root_id,
                max_bytes=normalized.max_bytes,
                max_lines=normalized.max_lines,
            )
        )
        detected_kind = _detect_kind(normalized.path)
        mode = _effective_mode(normalized.summary_mode, detected_kind)
        if text_decision.blocked:
            return _policy_decision(
                request=normalized,
                path_resolution=text_decision.path_resolution,
                detected_kind=detected_kind,
                mode=mode,
                finding_type=text_decision.finding_type,
                reason=text_decision.reason,
                allowed=False,
            )
        if mode == "unsupported":
            return _policy_decision(
                request=normalized,
                path_resolution=text_decision.path_resolution,
                detected_kind=detected_kind,
                mode=mode,
                finding_type="unsupported_file_kind",
                reason="Unsupported file kind for deterministic structure summary.",
                allowed=False,
            )
        return _policy_decision(
            request=normalized,
            path_resolution=text_decision.path_resolution,
            detected_kind=detected_kind,
            mode=mode,
            finding_type="ok",
            reason=None,
            allowed=True,
        )


class MarkdownStructureExtractor:
    def extract(self, text: str) -> MarkdownStructureSummary:
        lines = text.splitlines()
        frontmatter_keys: list[str] = []
        body_start = 0
        if lines and lines[0].strip() == "---":
            for index, line in enumerate(lines[1:], start=2):
                if line.strip() == "---":
                    body_start = index
                    break
                key = _line_key(line)
                if key:
                    frontmatter_keys.append(key)
        headings: list[MarkdownHeadingRef] = []
        for line_number, line in enumerate(lines, start=1):
            if line_number <= body_start:
                continue
            match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if not match:
                continue
            title = match.group(2).strip()
            headings.append(
                MarkdownHeadingRef(
                    level=len(match.group(1)),
                    title=title,
                    line_number=line_number,
                    slug=_slug(title),
                )
            )
        return MarkdownStructureSummary(
            headings=headings,
            heading_count=len(headings),
            max_heading_depth=max((item.level for item in headings), default=0),
            has_frontmatter=bool(frontmatter_keys) or body_start > 0,
            frontmatter_keys=frontmatter_keys,
            section_line_ranges=_section_ranges(headings, len(lines)),
        )


class PythonSymbolExtractor:
    def extract(self, text: str) -> PythonSymbolSummary:
        try:
            tree = ast.parse(text)
        except SyntaxError as error:
            return PythonSymbolSummary([], [], [], [], parse_error=str(error))
        imports: list[PythonSymbolRef] = []
        functions: list[PythonSymbolRef] = []
        classes: list[PythonSymbolRef] = []
        assignments: list[PythonSymbolRef] = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(_symbol("import", alias.asname or alias.name, node, decorators=[]))
            elif isinstance(node, ast.ImportFrom):
                module = "." * node.level + (node.module or "")
                for alias in node.names:
                    imports.append(_symbol("from_import", f"{module}.{alias.name}".strip("."), node, decorators=[]))
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append(_symbol("async_function", node.name, node, decorators=_decorators(node)))
            elif isinstance(node, ast.FunctionDef):
                functions.append(_symbol("function", node.name, node, decorators=_decorators(node)))
            elif isinstance(node, ast.ClassDef):
                classes.append(_symbol("class", node.name, node, decorators=_decorators(node)))
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                for name in _assignment_names(node):
                    assignments.append(_symbol("assignment", name, node, decorators=[]))
        return PythonSymbolSummary(imports, functions, classes, assignments, parse_error=None)


class ShallowKeyExtractor:
    def extract(self, text: str, file_kind: str) -> ShallowKeySummary:
        try:
            if file_kind == "json":
                loaded = json.loads(text)
                return _mapping_summary("json", loaded)
            if file_kind == "toml":
                loaded = tomllib.loads(text)
                return _mapping_summary("toml", loaded)
            if file_kind == "yaml":
                return _yaml_summary(text)
        except Exception as error:
            return ShallowKeySummary(file_kind=file_kind, top_level_keys=[], nested_key_preview={}, parse_error=str(error))
        return ShallowKeySummary(file_kind="yaml", top_level_keys=[], nested_key_preview={}, parse_error="unsupported")


class SelfStructureSummaryService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.policy_service = SelfStructureSummaryPolicyService(path_policy_service=self.path_policy_service)
        self.text_service = SelfCodeTextPerceptionSkillService(path_policy_service=self.path_policy_service)
        self.markdown_extractor = MarkdownStructureExtractor()
        self.python_extractor = PythonSymbolExtractor()
        self.shallow_key_extractor = ShallowKeyExtractor()

    def summarize(self, request: SelfStructureSummaryRequest) -> SelfStructureSummaryCandidate:
        normalized = request.normalized()
        decision = self.policy_service.decide(normalized)
        if decision.blocked:
            return _blocked_candidate(normalized, decision)
        read_result = self.text_service.read_text(
            SelfTextReadRequest(
                path=normalized.path,
                root_id=normalized.root_id,
                max_bytes=decision.effective_max_bytes,
                max_lines=decision.effective_max_lines,
            )
        )
        if read_result.blocked or read_result.slice is None:
            blocked_decision = _policy_decision(
                request=normalized,
                path_resolution=decision.path_resolution,
                detected_kind=decision.detected_kind,
                mode=decision.effective_summary_mode,
                finding_type=read_result.policy_decision.finding_type,
                reason=read_result.policy_decision.reason,
                allowed=False,
            )
            return _blocked_candidate(normalized, blocked_decision)
        text = read_result.slice.content
        markdown = None
        python = None
        shallow_keys = None
        plain_text = None
        mode = decision.effective_summary_mode
        limitations: list[str] = []
        if mode == "markdown":
            markdown = self.markdown_extractor.extract(text)
        elif mode == "python":
            python = self.python_extractor.extract(text)
            if python.parse_error:
                limitations.append(f"parse_error: {python.parse_error}")
        elif mode in {"json", "yaml", "toml"}:
            shallow_keys = self.shallow_key_extractor.extract(text, mode)
            if shallow_keys.parse_error:
                limitations.append(f"parse_error: {shallow_keys.parse_error}")
        elif mode == "plain_text":
            plain_text = _plain_text_preview(read_result.slice.content, read_result.slice.bytes_read, read_result.slice.truncated, bool(read_result.redaction_findings))
        if read_result.slice.truncated:
            limitations.append("truncated_by_read_budget")
        return SelfStructureSummaryCandidate(
            candidate_id=f"self_structure_summary_candidate:{uuid4()}",
            source_path=normalized.path,
            root_id=decision.path_resolution.root_id or "workspace_root:primary",
            relative_path=read_result.slice.relative_path,
            summary_kind=mode,
            markdown=markdown,
            python=python,
            shallow_keys=shallow_keys,
            plain_text=plain_text,
            redaction_findings=read_result.redaction_findings,
            evidence_refs=[
                {"relative_path": read_result.slice.relative_path},
                {"summary_mode": mode},
                {"line_range": [read_result.slice.start_line, read_result.slice.end_line]},
            ],
            limitations=limitations,
            confidence="medium" if limitations else "high",
            policy_decision=decision,
            candidate_attrs=_candidate_attrs(),
        )


class SelfStructureSummarizationSkillService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.summary_service = SelfStructureSummaryService(path_policy_service=path_policy_service)

    def summarize_markdown_structure(self, request: SelfStructureSummaryRequest) -> SelfStructureSummaryCandidate:
        return self.summary_service.summarize(SelfStructureSummaryRequest(**{**request.to_dict(), "summary_mode": "markdown"}))

    def summarize_python_symbols(self, request: SelfStructureSummaryRequest) -> SelfStructureSummaryCandidate:
        return self.summary_service.summarize(SelfStructureSummaryRequest(**{**request.to_dict(), "summary_mode": "python"}))

    def summarize(self, request: SelfStructureSummaryRequest) -> SelfStructureSummaryCandidate:
        return self.summary_service.summarize(request)


def _policy_decision(
    *,
    request: SelfStructureSummaryRequest,
    path_resolution: WorkspacePathResolution,
    detected_kind: str | None,
    mode: str,
    finding_type: str,
    reason: str | None,
    allowed: bool,
) -> SelfStructureSummaryPolicyDecision:
    return SelfStructureSummaryPolicyDecision(
        allowed=allowed,
        blocked=not allowed,
        finding_type=finding_type,
        reason=reason,
        path_resolution=path_resolution,
        detected_kind=detected_kind,
        effective_summary_mode=mode,
        effective_max_bytes=request.max_bytes,
        effective_max_lines=request.max_lines,
    )


def _blocked_candidate(
    request: SelfStructureSummaryRequest,
    decision: SelfStructureSummaryPolicyDecision,
) -> SelfStructureSummaryCandidate:
    return SelfStructureSummaryCandidate(
        candidate_id=f"self_structure_summary_candidate:{uuid4()}",
        source_path=request.path,
        root_id=decision.path_resolution.root_id or "workspace_root:primary",
        relative_path=decision.path_resolution.normalized_path,
        summary_kind=decision.effective_summary_mode,
        markdown=None,
        python=None,
        shallow_keys=None,
        plain_text=None,
        redaction_findings=[],
        evidence_refs=[{"finding_type": decision.finding_type}],
        limitations=[decision.reason or decision.finding_type],
        confidence="low",
        policy_decision=decision,
        candidate_attrs=_candidate_attrs(blocked=True),
    )


def _detect_kind(path: str) -> str | None:
    suffix = "." + path.rsplit(".", 1)[-1].casefold() if "." in path else ""
    if suffix in MARKDOWN_SUFFIXES:
        return "markdown"
    if suffix in PYTHON_SUFFIXES:
        return "python"
    if suffix in JSON_SUFFIXES:
        return "json"
    if suffix in YAML_SUFFIXES:
        return "yaml"
    if suffix in TOML_SUFFIXES:
        return "toml"
    if suffix in {".txt", ".log", ".rst"}:
        return "plain_text"
    return None


def _effective_mode(requested: str, detected: str | None) -> str:
    if requested == "auto":
        return detected or "plain_text"
    if requested == "plain_text":
        return "plain_text"
    if requested == detected:
        return requested
    return "unsupported"


def _line_key(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or ":" not in stripped:
        return None
    key = stripped.split(":", 1)[0].strip().strip("\"'")
    return key or None


def _slug(title: str) -> str:
    lowered = title.casefold()
    slug = re.sub(r"[^a-z0-9가-힣]+", "-", lowered).strip("-")
    return slug or title


def _section_ranges(headings: list[MarkdownHeadingRef], line_count: int) -> list[dict[str, Any]]:
    ranges: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        next_line = headings[index + 1].line_number if index + 1 < len(headings) else line_count + 1
        ranges.append(
            {
                "title": heading.title,
                "level": heading.level,
                "start_line": heading.line_number,
                "end_line": max(heading.line_number, next_line - 1),
            }
        )
    return ranges


def _symbol(symbol_type: str, name: str, node: ast.AST, *, decorators: list[str]) -> PythonSymbolRef:
    return PythonSymbolRef(
        symbol_type=symbol_type,  # type: ignore[arg-type]
        name=name,
        line_number=getattr(node, "lineno", 0),
        end_line_number=getattr(node, "end_lineno", None),
        parent=None,
        decorators=decorators,
    )


def _decorators(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    names: list[str] = []
    for decorator in node.decorator_list:
        names.append(_node_name(decorator))
    return [name for name in names if name]


def _node_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _node_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    if isinstance(node, ast.Call):
        return _node_name(node.func)
    return type(node).__name__


def _assignment_names(node: ast.Assign | ast.AnnAssign) -> list[str]:
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    names: list[str] = []
    for target in targets:
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            names.extend(item.id for item in target.elts if isinstance(item, ast.Name))
    return names


def _mapping_summary(file_kind: str, loaded: Any) -> ShallowKeySummary:
    if not isinstance(loaded, dict):
        return ShallowKeySummary(file_kind=file_kind, top_level_keys=[], nested_key_preview={}, parse_error="top level is not a mapping")  # type: ignore[arg-type]
    keys = [str(key) for key in loaded.keys()]
    nested = {
        str(key): [str(inner) for inner in value.keys()][:20]
        for key, value in loaded.items()
        if isinstance(value, dict)
    }
    return ShallowKeySummary(file_kind=file_kind, top_level_keys=keys, nested_key_preview=nested, parse_error=None)  # type: ignore[arg-type]


def _yaml_summary(text: str) -> ShallowKeySummary:
    keys: list[str] = []
    nested: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        indent = len(line) - len(line.lstrip(" "))
        key = _line_key(line)
        if not key:
            continue
        if indent == 0:
            keys.append(key)
            current = key
        elif current:
            nested.setdefault(current, []).append(key)
    return ShallowKeySummary(file_kind="yaml", top_level_keys=keys, nested_key_preview=nested, parse_error=None)


def _plain_text_preview(text: str, bytes_seen: int, truncated: bool, redacted: bool) -> PlainTextPreviewSummary:
    first_lines = [line.strip() for line in text.splitlines() if line.strip()][:10]
    return PlainTextPreviewSummary(
        first_non_empty_lines=first_lines,
        line_count_seen=len(text.splitlines()),
        bytes_seen=bytes_seen,
        truncated=truncated,
        redacted=redacted,
    )


def _candidate_attrs(*, blocked: bool = False) -> dict[str, Any]:
    return {
        "effect_types": list(STRUCTURE_SUMMARY_EFFECTS),
        "read_only": True,
        "policy_gated": True,
        "deterministic_structure_extraction": True,
        "model_summary_used": False,
        "canonical_promotion_enabled": False,
        "promoted": False,
        "blocked": blocked,
        "workspace_write_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
    }

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
    WorkspacePathResolution,
)


TextReadMode = Literal["preview", "line_range", "head", "tail"]
FileKind = Literal["text", "binary", "unknown", "blocked_secret", "oversized"] | None

TEXT_READ_DEFAULT_MAX_BYTES = 16384
TEXT_READ_DEFAULT_MAX_LINES = 300
TEXT_READ_MAX_BYTES_CAP = 65536
TEXT_READ_MAX_LINES_CAP = 1000
TEXT_SAMPLE_BYTES = 4096
TEXT_ALLOWED_SUFFIXES = {
    ".cfg",
    ".css",
    ".csv",
    ".ini",
    ".js",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_ALLOWED_FILENAMES = {"README", "LICENSE", "NOTICE"}
SECRET_BLOCKED_SUFFIXES = {
    ".crt",
    ".cer",
    ".der",
    ".key",
    ".p12",
    ".pfx",
    ".pem",
}
SECRET_BLOCKED_NAMES = {
    ".env",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}


@dataclass(frozen=True)
class SelfTextReadRequest:
    path: str
    root_id: str | None = None
    mode: TextReadMode = "preview"
    start_line: int | None = None
    end_line: int | None = None
    max_bytes: int = TEXT_READ_DEFAULT_MAX_BYTES
    max_lines: int = TEXT_READ_DEFAULT_MAX_LINES
    allow_redacted_secret_preview: bool = False

    def normalized(self) -> "SelfTextReadRequest":
        mode = self.mode if self.mode in {"preview", "line_range", "head", "tail"} else "preview"
        max_bytes = min(max(1, int(self.max_bytes)), TEXT_READ_MAX_BYTES_CAP)
        max_lines = min(max(1, int(self.max_lines)), TEXT_READ_MAX_LINES_CAP)
        start_line = self.start_line
        end_line = self.end_line
        if mode == "line_range":
            start_line = max(1, int(start_line or 1))
            end_line = max(start_line, int(end_line or start_line))
        return SelfTextReadRequest(
            path=self.path or "",
            root_id=self.root_id,
            mode=mode,
            start_line=start_line,
            end_line=end_line,
            max_bytes=max_bytes,
            max_lines=max_lines,
            allow_redacted_secret_preview=bool(self.allow_redacted_secret_preview),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "root_id": self.root_id,
            "mode": self.mode,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "max_bytes": self.max_bytes,
            "max_lines": self.max_lines,
            "allow_redacted_secret_preview": self.allow_redacted_secret_preview,
        }


@dataclass(frozen=True)
class SelfTextReadPolicyDecision:
    allowed: bool
    blocked: bool
    finding_type: str
    reason: str | None
    path_resolution: WorkspacePathResolution
    file_kind: FileKind
    detected_suffix: str | None
    size_bytes: int | None
    read_mode: str
    effective_max_bytes: int
    effective_max_lines: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "blocked": self.blocked,
            "finding_type": self.finding_type,
            "reason": self.reason,
            "path_resolution": self.path_resolution.to_dict(),
            "file_kind": self.file_kind,
            "detected_suffix": self.detected_suffix,
            "size_bytes": self.size_bytes,
            "read_mode": self.read_mode,
            "effective_max_bytes": self.effective_max_bytes,
            "effective_max_lines": self.effective_max_lines,
        }


@dataclass(frozen=True)
class SelfTextSlice:
    path: str
    root_id: str | None
    relative_path: str
    start_line: int
    end_line: int
    content: str
    bytes_read: int
    lines_read: int
    truncated: bool
    redacted: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "content": self.content,
            "bytes_read": self.bytes_read,
            "lines_read": self.lines_read,
            "truncated": self.truncated,
            "redacted": self.redacted,
        }


@dataclass(frozen=True)
class SelfTextRedactionFinding:
    finding_id: str
    finding_type: str
    line_number: int
    redaction_applied: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "finding_type": self.finding_type,
            "line_number": self.line_number,
            "redaction_applied": self.redaction_applied,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SelfTextReadResult:
    result_id: str
    request: SelfTextReadRequest
    policy_decision: SelfTextReadPolicyDecision
    slice: SelfTextSlice | None
    redaction_findings: list[SelfTextRedactionFinding]
    evidence_refs: list[str]
    blocked: bool
    warnings: list[str]
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request": self.request.to_dict(),
            "policy_decision": self.policy_decision.to_dict(),
            "slice": self.slice.to_dict() if self.slice else None,
            "redaction_findings": [item.to_dict() for item in self.redaction_findings],
            "evidence_refs": list(self.evidence_refs),
            "blocked": self.blocked,
            "warnings": list(self.warnings),
            "result_attrs": dict(self.result_attrs),
        }


class SelfTextReadPolicyService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()

    def classify_file_for_text_read(self, path_resolution: WorkspacePathResolution) -> tuple[FileKind, str | None, int | None, str | None]:
        if path_resolution.blocked:
            return None, None, None, path_resolution.reason
        path = Path(path_resolution.canonical_path)
        suffix = path.suffix.casefold()
        if _is_secret_like_file(path):
            try:
                size = path.stat().st_size if path.exists() and path.is_file() else None
            except OSError:
                size = None
            return "blocked_secret", suffix, size, "Secret-like files are blocked by policy."
        try:
            if not path.exists():
                return None, suffix, None, "The requested file does not exist."
            if not path.is_file():
                return None, suffix, None, "The requested path is not a file."
            stat = path.stat()
        except OSError as error:
            return "unknown", suffix, None, str(error)
        try:
            with path.open("rb") as handle:
                sample = handle.read(TEXT_SAMPLE_BYTES)
        except OSError as error:
            return "unknown", suffix, stat.st_size, str(error)
        if _looks_binary(sample):
            return "binary", suffix, stat.st_size, "Binary files are blocked."
        if not _is_supported_text_name(path):
            return None, suffix, stat.st_size, "The file extension is not supported for text perception."
        return "text", suffix, stat.st_size, None

    def decide(self, request: SelfTextReadRequest) -> SelfTextReadPolicyDecision:
        normalized = request.normalized()
        resolution = self.path_policy_service.resolve_path(normalized.path, root_id=normalized.root_id)
        effective_max_bytes = normalized.max_bytes
        effective_max_lines = normalized.max_lines
        if resolution.blocked:
            return _decision(
                request=normalized,
                resolution=resolution,
                finding_type=_map_path_finding(resolution.finding_type),
                reason=resolution.reason,
                file_kind=None,
                suffix=None,
                size_bytes=None,
                allowed=False,
            )
        file_kind, suffix, size_bytes, reason = self.classify_file_for_text_read(resolution)
        if reason:
            finding = _finding_from_classification(file_kind, reason)
            return _decision(
                request=normalized,
                resolution=resolution,
                finding_type=finding,
                reason=reason,
                file_kind=file_kind,
                suffix=suffix,
                size_bytes=size_bytes,
                allowed=False,
            )
        return SelfTextReadPolicyDecision(
            allowed=True,
            blocked=False,
            finding_type="ok",
            reason=None,
            path_resolution=resolution,
            file_kind=file_kind,
            detected_suffix=suffix,
            size_bytes=size_bytes,
            read_mode=normalized.mode,
            effective_max_bytes=effective_max_bytes,
            effective_max_lines=effective_max_lines,
        )


class SelfTextReaderService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.redaction_service = SelfTextRedactionService()

    def read_text_slice(
        self,
        request: SelfTextReadRequest,
        decision: SelfTextReadPolicyDecision,
    ) -> tuple[SelfTextSlice | None, list[SelfTextRedactionFinding], list[str]]:
        normalized = request.normalized()
        if not decision.allowed:
            return None, [], []
        path = Path(decision.path_resolution.canonical_path)
        try:
            selected_lines, start_line, end_line, bytes_read, truncated = _read_limited_lines(path, normalized, decision)
        except UnicodeDecodeError:
            return None, [], ["decode_error"]
        content = "".join(selected_lines)
        redacted_content, findings = self.redaction_service.redact(content, start_line=start_line)
        relative_path = Path(decision.path_resolution.canonical_path).relative_to(
            self.path_policy_service.workspace_root
        ).as_posix()
        text_slice = SelfTextSlice(
            path=normalized.path,
            root_id=decision.path_resolution.root_id,
            relative_path=relative_path,
            start_line=start_line,
            end_line=end_line,
            content=redacted_content,
            bytes_read=bytes_read,
            lines_read=len(selected_lines),
            truncated=truncated,
            redacted=bool(findings),
        )
        return text_slice, findings, []


class SelfTextRedactionService:
    def redact(self, text: str, *, start_line: int = 1) -> tuple[str, list[SelfTextRedactionFinding]]:
        redacted_lines: list[str] = []
        findings: list[SelfTextRedactionFinding] = []
        for offset, line in enumerate(text.splitlines(keepends=True)):
            line_number = start_line + offset
            redacted_line, line_findings = _redact_line(line, line_number)
            redacted_lines.append(redacted_line)
            findings.extend(line_findings)
        return "".join(redacted_lines), findings


class SelfCodeTextPerceptionSkillService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.policy_service = SelfTextReadPolicyService(path_policy_service=self.path_policy_service)
        self.reader_service = SelfTextReaderService(path_policy_service=self.path_policy_service)

    def read_text(self, request: SelfTextReadRequest) -> SelfTextReadResult:
        normalized = request.normalized()
        decision = self.policy_service.decide(normalized)
        if decision.blocked:
            return SelfTextReadResult(
                result_id=f"self_text_read_result:{uuid4()}",
                request=normalized,
                policy_decision=decision,
                slice=None,
                redaction_findings=[],
                evidence_refs=[decision.finding_type],
                blocked=True,
                warnings=[decision.reason] if decision.reason else [],
                result_attrs=_result_attrs(skills_executed=True),
            )
        text_slice, findings, warnings = self.reader_service.read_text_slice(normalized, decision)
        if "decode_error" in warnings:
            blocked_decision = SelfTextReadPolicyDecision(
                allowed=False,
                blocked=True,
                finding_type="decode_error",
                reason="The file could not be decoded as UTF-8 text.",
                path_resolution=decision.path_resolution,
                file_kind="unknown",
                detected_suffix=decision.detected_suffix,
                size_bytes=decision.size_bytes,
                read_mode=decision.read_mode,
                effective_max_bytes=decision.effective_max_bytes,
                effective_max_lines=decision.effective_max_lines,
            )
            return SelfTextReadResult(
                result_id=f"self_text_read_result:{uuid4()}",
                request=normalized,
                policy_decision=blocked_decision,
                slice=None,
                redaction_findings=[],
                evidence_refs=["decode_error"],
                blocked=True,
                warnings=["The file could not be decoded as UTF-8 text."],
                result_attrs=_result_attrs(skills_executed=True),
            )
        evidence_refs = [
            decision.path_resolution.root_id or "workspace_root:primary",
            "bounded_text_slice",
        ]
        if text_slice and text_slice.redacted:
            evidence_refs.append("redaction_applied")
        return SelfTextReadResult(
            result_id=f"self_text_read_result:{uuid4()}",
            request=normalized,
            policy_decision=decision,
            slice=text_slice,
            redaction_findings=findings,
            evidence_refs=evidence_refs,
            blocked=False,
            warnings=warnings,
            result_attrs=_result_attrs(skills_executed=True),
        )


def _decision(
    *,
    request: SelfTextReadRequest,
    resolution: WorkspacePathResolution,
    finding_type: str,
    reason: str,
    file_kind: FileKind,
    suffix: str | None,
    size_bytes: int | None,
    allowed: bool,
) -> SelfTextReadPolicyDecision:
    return SelfTextReadPolicyDecision(
        allowed=allowed,
        blocked=not allowed,
        finding_type=finding_type,
        reason=reason,
        path_resolution=resolution,
        file_kind=file_kind,
        detected_suffix=suffix,
        size_bytes=size_bytes,
        read_mode=request.mode,
        effective_max_bytes=request.max_bytes,
        effective_max_lines=request.max_lines,
    )


def _read_limited_lines(
    path: Path,
    request: SelfTextReadRequest,
    decision: SelfTextReadPolicyDecision,
) -> tuple[list[str], int, int, int, bool]:
    max_bytes = decision.effective_max_bytes
    max_lines = decision.effective_max_lines
    if request.mode == "tail":
        return _read_tail_lines(path, max_bytes=max_bytes, max_lines=max_lines)
    selected: list[str] = []
    bytes_read = 0
    truncated = False
    start_line = 1
    end_line = 0
    if request.mode == "line_range":
        start_line = int(request.start_line or 1)
        requested_end = int(request.end_line or start_line)
    else:
        requested_end = max_lines
    with path.open("r", encoding="utf-8", errors="strict") as handle:
        for line_number, line in enumerate(handle, start=1):
            if request.mode == "line_range" and line_number < start_line:
                continue
            if request.mode == "line_range" and line_number > requested_end:
                break
            if request.mode in {"preview", "head"} and len(selected) >= max_lines:
                truncated = True
                break
            next_bytes = len(line.encode("utf-8"))
            if bytes_read + next_bytes > max_bytes:
                remaining = max_bytes - bytes_read
                if remaining > 0:
                    encoded = line.encode("utf-8")[:remaining]
                    selected.append(encoded.decode("utf-8", errors="ignore"))
                    bytes_read = max_bytes
                    end_line = line_number
                truncated = True
                break
            selected.append(line)
            bytes_read += next_bytes
            end_line = line_number
            if request.mode == "line_range" and len(selected) >= max_lines:
                truncated = True
                break
    if selected and request.mode != "line_range":
        start_line = 1
    return selected, start_line, end_line, bytes_read, truncated


def _read_tail_lines(path: Path, *, max_bytes: int, max_lines: int) -> tuple[list[str], int, int, int, bool]:
    selected: list[tuple[int, str, int]] = []
    bytes_read = 0
    truncated = False
    with path.open("r", encoding="utf-8", errors="strict") as handle:
        for line_number, line in enumerate(handle, start=1):
            line_bytes = len(line.encode("utf-8"))
            selected.append((line_number, line, line_bytes))
            bytes_read += line_bytes
            while selected and (len(selected) > max_lines or bytes_read > max_bytes):
                _, _, removed_bytes = selected.pop(0)
                bytes_read -= removed_bytes
                truncated = True
    if not selected:
        return [], 1, 0, 0, truncated
    start_line = selected[0][0]
    end_line = selected[-1][0]
    return [line for _, line, _ in selected], start_line, end_line, bytes_read, truncated


def _redact_line(line: str, line_number: int) -> tuple[str, list[SelfTextRedactionFinding]]:
    redacted = line
    findings: list[SelfTextRedactionFinding] = []
    private_member_path_pattern = (
        r"D:\\ChantaResearchGroup\\"
        + r"ChantaResearchGroup"
        + r"_Members\\[^\s`'\"<>]+"
    )
    patterns = [
        ("private_path", re.compile(private_member_path_pattern)),
        ("secret_like", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("secret_like", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
        ("credential_assignment", re.compile(r"(?i)(\b(password|api[_-]?key|secret|token)\b\s*[:=]\s*)[^#\s]+")),
        ("credential_like", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")),
        ("credential_like", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
        ("high_entropy", re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")),
    ]
    for finding_type, pattern in patterns:
        if pattern.search(redacted):
            if finding_type == "credential_assignment":
                redacted = pattern.sub(r"\1[REDACTED]", redacted)
                finding_type = "credential_like"
            else:
                redacted = pattern.sub("[REDACTED]", redacted)
            findings.append(
                SelfTextRedactionFinding(
                    finding_id=f"self_text_redaction_finding:{uuid4()}",
                    finding_type=finding_type,
                    line_number=line_number,
                    redaction_applied=True,
                    reason=f"{finding_type} text redacted",
                )
            )
    return redacted, findings


def _map_path_finding(finding_type: str) -> str:
    if finding_type == "path_traversal":
        return "path_traversal"
    if finding_type == "outside_workspace" or finding_type == "absolute_path_not_allowed":
        return "outside_workspace"
    if finding_type == "private_boundary":
        return "private_boundary"
    if finding_type == "symlink_blocked":
        return "symlink_escape"
    return finding_type


def _finding_from_classification(file_kind: FileKind, reason: str) -> str:
    folded = reason.casefold()
    if "does not exist" in folded:
        return "not_found"
    if "not a file" in folded:
        return "not_file"
    if file_kind == "binary":
        return "binary_file_blocked"
    if file_kind == "blocked_secret":
        return "secret_file_blocked"
    if "extension" in folded:
        return "unsupported_extension"
    return "decode_error" if "decode" in folded else "unsupported_extension"


def _is_secret_like_file(path: Path) -> bool:
    name = path.name.casefold()
    if name in SECRET_BLOCKED_NAMES or name.startswith(".env."):
        return True
    if path.suffix.casefold() in SECRET_BLOCKED_SUFFIXES:
        return True
    return False


def _is_supported_text_name(path: Path) -> bool:
    if path.suffix.casefold() in TEXT_ALLOWED_SUFFIXES:
        return True
    return path.name in TEXT_ALLOWED_FILENAMES


def _looks_binary(sample: bytes) -> bool:
    if b"\x00" in sample:
        return True
    if not sample:
        return False
    text_control = sum(1 for byte in sample if byte < 9 or (13 < byte < 32))
    return text_control / max(len(sample), 1) > 0.15


def _result_attrs(*, skills_executed: bool) -> dict[str, Any]:
    return {
        "effect_type": READ_ONLY_OBSERVATION_EFFECT,
        "read_only": True,
        "bounded_read": True,
        "policy_gated": True,
        "redaction_enabled": True,
        "skills_executed": skills_executed,
        "workspace_write_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
        "workspace_search_used": False,
        "summary_used": False,
        "symbol_parse_used": False,
    }

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonaSourceImportError
from chanta_core.persona.ids import (
    new_persona_assimilation_draft_id,
    new_persona_projection_candidate_id,
    new_persona_source_id,
    new_persona_source_ingestion_candidate_id,
    new_persona_source_manifest_id,
    new_persona_source_risk_note_id,
    new_persona_source_validation_result_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


DEFAULT_INCLUDE_PATTERNS = ["*.md", "*.txt", "*.html", "**/*.md", "**/*.txt", "**/*.html"]
DEFAULT_EXCLUDE_PATTERNS = [
    "letters/**",
    "**/letters/**",
    "messages/**",
    "**/messages/**",
    "archive/**",
    "**/archive/**",
    "message_to_*.md",
    "**/message_to_*.md",
    "letter_to_*.md",
    "**/letter_to_*.md",
]
DEFAULT_ALLOWED_EXTENSIONS = [".md", ".txt", ".html"]


@dataclass(frozen=True)
class PersonaSource:
    source_id: str
    source_name: str
    source_type: str
    source_ref: str
    media_type: str
    content_hash: str
    content_preview: str
    content_length: int
    trust_level: str
    private: bool
    status: str
    created_at: str
    source_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "media_type": self.media_type,
            "content_hash": self.content_hash,
            "content_preview": self.content_preview,
            "content_length": self.content_length,
            "trust_level": self.trust_level,
            "private": self.private,
            "status": self.status,
            "created_at": self.created_at,
            "source_attrs": dict(self.source_attrs),
        }


@dataclass(frozen=True)
class PersonaSourceManifest:
    manifest_id: str
    manifest_name: str
    source_root: str
    include_patterns: list[str]
    exclude_patterns: list[str]
    source_ids: list[str]
    created_at: str
    manifest_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "manifest_name": self.manifest_name,
            "source_root": self.source_root,
            "include_patterns": list(self.include_patterns),
            "exclude_patterns": list(self.exclude_patterns),
            "source_ids": list(self.source_ids),
            "created_at": self.created_at,
            "manifest_attrs": dict(self.manifest_attrs),
        }


@dataclass(frozen=True)
class PersonaSourceIngestionCandidate:
    candidate_id: str
    manifest_id: str
    source_ids: list[str]
    candidate_type: str
    review_status: str
    canonical_import_enabled: bool
    private: bool
    recommended_next_step: str
    created_at: str
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "manifest_id": self.manifest_id,
            "source_ids": list(self.source_ids),
            "candidate_type": self.candidate_type,
            "review_status": self.review_status,
            "canonical_import_enabled": self.canonical_import_enabled,
            "private": self.private,
            "recommended_next_step": self.recommended_next_step,
            "created_at": self.created_at,
            "candidate_attrs": dict(self.candidate_attrs),
        }


@dataclass(frozen=True)
class PersonaSourceValidationResult:
    validation_id: str
    candidate_id: str
    source_id: str
    status: str
    validation_kind: str
    missing_fields: list[str]
    warning_messages: list[str]
    error_messages: list[str]
    created_at: str
    validation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "candidate_id": self.candidate_id,
            "source_id": self.source_id,
            "status": self.status,
            "validation_kind": self.validation_kind,
            "missing_fields": list(self.missing_fields),
            "warning_messages": list(self.warning_messages),
            "error_messages": list(self.error_messages),
            "created_at": self.created_at,
            "validation_attrs": dict(self.validation_attrs),
        }


@dataclass(frozen=True)
class PersonaAssimilationDraft:
    draft_id: str
    candidate_id: str
    source_ids: list[str]
    draft_type: str
    title: str
    identity_points: list[str]
    role_points: list[str]
    boundary_points: list[str]
    style_points: list[str]
    safety_points: list[str]
    unresolved_questions: list[str]
    created_at: str
    draft_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "candidate_id": self.candidate_id,
            "source_ids": list(self.source_ids),
            "draft_type": self.draft_type,
            "title": self.title,
            "identity_points": list(self.identity_points),
            "role_points": list(self.role_points),
            "boundary_points": list(self.boundary_points),
            "style_points": list(self.style_points),
            "safety_points": list(self.safety_points),
            "unresolved_questions": list(self.unresolved_questions),
            "created_at": self.created_at,
            "draft_attrs": dict(self.draft_attrs),
        }


@dataclass(frozen=True)
class PersonaProjectionCandidate:
    projection_candidate_id: str
    draft_id: str
    candidate_id: str
    projection_type: str
    projected_blocks: list[dict[str, Any]]
    total_chars: int
    truncated: bool
    canonical_import_enabled: bool
    created_at: str
    projection_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_candidate_id": self.projection_candidate_id,
            "draft_id": self.draft_id,
            "candidate_id": self.candidate_id,
            "projection_type": self.projection_type,
            "projected_blocks": [dict(item) for item in self.projected_blocks],
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "canonical_import_enabled": self.canonical_import_enabled,
            "created_at": self.created_at,
            "projection_attrs": dict(self.projection_attrs),
        }


@dataclass(frozen=True)
class PersonaSourceRiskNote:
    risk_note_id: str
    source_id: str
    candidate_id: str
    risk_level: str
    risk_categories: list[str]
    message: str
    review_required: bool
    created_at: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_note_id": self.risk_note_id,
            "source_id": self.source_id,
            "candidate_id": self.candidate_id,
            "risk_level": self.risk_level,
            "risk_categories": list(self.risk_categories),
            "message": self.message,
            "review_required": self.review_required,
            "created_at": self.created_at,
            "risk_attrs": dict(self.risk_attrs),
        }


class PersonaSourceStagedImportService:
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
        self._texts_by_source_id: dict[str, str] = {}

    def register_source_from_text(
        self,
        *,
        source_name: str,
        text: str,
        source_ref: str | None = None,
        media_type: str = "text/plain",
        trust_level: str = "unreviewed",
        private: bool = False,
        status: str = "staged",
        source_attrs: dict[str, Any] | None = None,
    ) -> PersonaSource:
        source_type = detect_source_type(source_ref or source_name, media_type)
        normalized_text = strip_html_to_text(text) if source_type == "html" else text
        source = PersonaSource(
            source_id=new_persona_source_id(),
            source_name=source_name,
            source_type=source_type,
            source_ref=source_ref or source_name,
            media_type=media_type,
            content_hash=hash_text(normalized_text),
            content_preview=preview_text(normalized_text),
            content_length=len(normalized_text),
            trust_level=trust_level,
            private=private,
            status=status,
            created_at=utc_now_iso(),
            source_attrs={
                "canonical_persona_source": False,
                "staged_candidate_only": True,
                "body_stored_in_model": False,
                **dict(source_attrs or {}),
            },
        )
        self._texts_by_source_id[source.source_id] = normalized_text
        self._record(
            "persona_source_registered",
            objects=[_object("persona_source", source.source_id, source.to_dict())],
            links=[("source_object", source.source_id)],
            object_links=[],
            attrs={"source_type": source.source_type, "private": source.private},
        )
        return source

    def register_source_from_file(
        self,
        path: str | Path,
        *,
        source_root: str | Path | None = None,
        allowed_extensions: list[str] | None = None,
        max_bytes: int = 262144,
        trust_level: str = "unreviewed",
        private: bool = False,
    ) -> PersonaSource:
        resolved_path = Path(path).resolve(strict=False)
        text = safe_read_text_file(
            resolved_path,
            source_root=source_root,
            max_bytes=max_bytes,
            allowed_extensions=allowed_extensions or DEFAULT_ALLOWED_EXTENSIONS,
        )
        source_type = detect_source_type(str(resolved_path))
        media_type = {
            "markdown": "text/markdown",
            "html": "text/html",
            "text": "text/plain",
        }[source_type]
        return self.register_source_from_text(
            source_name=resolved_path.name,
            text=text,
            source_ref=str(resolved_path),
            media_type=media_type,
            trust_level=trust_level,
            private=private,
            source_attrs={
                "file_path": str(resolved_path),
                "file_extension": resolved_path.suffix.casefold(),
            },
        )

    def discover_sources(
        self,
        source_root: str | Path,
        *,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        allowed_extensions: list[str] | None = None,
        private: bool = False,
    ) -> list[PersonaSource]:
        root = Path(source_root).resolve(strict=False)
        if not root.exists() or not root.is_dir():
            raise PersonaSourceImportError(f"source_root does not exist: {root}")
        include = include_patterns or DEFAULT_INCLUDE_PATTERNS
        exclude = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
        sources: list[PersonaSource] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative_path = _relative_posix(path, root)
            if _matches_any(relative_path, exclude) or _matches_any(path.name, exclude):
                continue
            if not (_matches_any(relative_path, include) or _matches_any(path.name, include)):
                continue
            sources.append(
                self.register_source_from_file(
                    path,
                    source_root=root,
                    allowed_extensions=allowed_extensions,
                    private=private,
                )
            )
        return sources

    def create_manifest(
        self,
        *,
        manifest_name: str,
        source_root: str | Path,
        sources: list[PersonaSource],
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        manifest_attrs: dict[str, Any] | None = None,
    ) -> PersonaSourceManifest:
        manifest = PersonaSourceManifest(
            manifest_id=new_persona_source_manifest_id(),
            manifest_name=manifest_name,
            source_root=str(Path(source_root).resolve(strict=False)),
            include_patterns=list(include_patterns or DEFAULT_INCLUDE_PATTERNS),
            exclude_patterns=list(exclude_patterns or DEFAULT_EXCLUDE_PATTERNS),
            source_ids=[source.source_id for source in sources],
            created_at=utc_now_iso(),
            manifest_attrs={
                "canonical_persona_source": False,
                "source_count": len(sources),
                **dict(manifest_attrs or {}),
            },
        )
        self._record(
            "persona_source_manifest_created",
            objects=[_object("persona_source_manifest", manifest.manifest_id, manifest.to_dict())],
            links=[("manifest_object", manifest.manifest_id)]
            + [("source_object", source.source_id) for source in sources],
            object_links=[
                (manifest.manifest_id, source.source_id, "includes_source")
                for source in sources
            ],
            attrs={"source_count": len(sources)},
        )
        return manifest

    def validate_source(
        self,
        source: PersonaSource,
        *,
        candidate_id: str | None = None,
        validation_kind: str = "source_shape",
    ) -> PersonaSourceValidationResult:
        missing = [
            field_name
            for field_name in ["source_id", "source_name", "source_type", "content_hash"]
            if not getattr(source, field_name)
        ]
        warnings: list[str] = []
        errors: list[str] = []
        if source.source_type not in {"markdown", "text", "html"}:
            errors.append("unsupported source_type")
        if source.content_length <= 0:
            errors.append("empty source content")
        if source.private:
            warnings.append("source marked private; avoid public projection output")
        status = "invalid" if missing or errors else ("needs_review" if warnings else "valid")
        validation = PersonaSourceValidationResult(
            validation_id=new_persona_source_validation_result_id(),
            candidate_id=candidate_id or "",
            source_id=source.source_id,
            status=status,
            validation_kind=validation_kind,
            missing_fields=missing,
            warning_messages=warnings,
            error_messages=errors,
            created_at=utc_now_iso(),
            validation_attrs={"canonical_persona_source": False},
        )
        self._record_validation(validation, source_id=source.source_id, candidate_id=candidate_id)
        return validation

    def validate_candidate(
        self,
        candidate: PersonaSourceIngestionCandidate,
        sources: list[PersonaSource],
    ) -> list[PersonaSourceValidationResult]:
        validations = [
            self.validate_source(source, candidate_id=candidate.candidate_id)
            for source in sources
        ]
        if not sources:
            validations.append(
                PersonaSourceValidationResult(
                    validation_id=new_persona_source_validation_result_id(),
                    candidate_id=candidate.candidate_id,
                    source_id="",
                    status="invalid",
                    validation_kind="candidate_shape",
                    missing_fields=["source_ids"],
                    warning_messages=[],
                    error_messages=["candidate has no sources"],
                    created_at=utc_now_iso(),
                    validation_attrs={"canonical_persona_source": False},
                )
            )
            self._record_validation(validations[-1], source_id=None, candidate_id=candidate.candidate_id)
        return validations

    def create_ingestion_candidate(
        self,
        *,
        manifest: PersonaSourceManifest,
        sources: list[PersonaSource],
        candidate_type: str = "staged_persona_source_import",
        review_status: str = "pending_review",
        private: bool = False,
        recommended_next_step: str = "review_before_projection",
    ) -> PersonaSourceIngestionCandidate:
        candidate = PersonaSourceIngestionCandidate(
            candidate_id=new_persona_source_ingestion_candidate_id(),
            manifest_id=manifest.manifest_id,
            source_ids=[source.source_id for source in sources],
            candidate_type=candidate_type,
            review_status=review_status,
            canonical_import_enabled=False,
            private=private,
            recommended_next_step=recommended_next_step,
            created_at=utc_now_iso(),
            candidate_attrs={
                "source_count": len(sources),
                "canonical_persona_source": False,
                "auto_activation_enabled": False,
            },
        )
        self._record(
            "persona_source_ingestion_candidate_created",
            objects=[
                _object(
                    "persona_source_ingestion_candidate",
                    candidate.candidate_id,
                    candidate.to_dict(),
                )
            ],
            links=[("candidate_object", candidate.candidate_id), ("manifest_object", manifest.manifest_id)]
            + [("source_object", source.source_id) for source in sources],
            object_links=[(candidate.candidate_id, manifest.manifest_id, "uses_manifest")]
            + [(candidate.candidate_id, source.source_id, "uses_source") for source in sources],
            attrs={
                "review_status": candidate.review_status,
                "canonical_import_enabled": False,
            },
        )
        return candidate

    def create_assimilation_draft(
        self,
        *,
        candidate: PersonaSourceIngestionCandidate,
        sources: list[PersonaSource],
        draft_type: str = "deterministic_persona_points",
        title: str = "Staged persona assimilation draft",
    ) -> PersonaAssimilationDraft:
        combined = "\n".join(self._texts_by_source_id.get(source.source_id, source.content_preview) for source in sources)
        points = extract_persona_points(combined)
        draft = PersonaAssimilationDraft(
            draft_id=new_persona_assimilation_draft_id(),
            candidate_id=candidate.candidate_id,
            source_ids=[source.source_id for source in sources],
            draft_type=draft_type,
            title=title,
            identity_points=points["identity_points"],
            role_points=points["role_points"],
            boundary_points=points["boundary_points"],
            style_points=points["style_points"],
            safety_points=points["safety_points"],
            unresolved_questions=points["unresolved_questions"],
            created_at=utc_now_iso(),
            draft_attrs={
                "deterministic_extraction": True,
                "uses_llm": False,
                "canonical_import_enabled": False,
            },
        )
        self._record(
            "persona_assimilation_draft_created",
            objects=[_object("persona_assimilation_draft", draft.draft_id, draft.to_dict())],
            links=[("draft_object", draft.draft_id), ("candidate_object", candidate.candidate_id)]
            + [("source_object", source.source_id) for source in sources],
            object_links=[(draft.draft_id, candidate.candidate_id, "derived_from_candidate")]
            + [(draft.draft_id, source.source_id, "derived_from_source") for source in sources],
            attrs={"draft_type": draft.draft_type},
        )
        return draft

    def create_projection_candidate(
        self,
        *,
        draft: PersonaAssimilationDraft,
        candidate: PersonaSourceIngestionCandidate,
        projection_type: str = "bounded_prompt_candidate",
        max_chars: int = 4000,
    ) -> PersonaProjectionCandidate:
        blocks = [
            {"block_type": "identity", "items": draft.identity_points},
            {"block_type": "role", "items": draft.role_points},
            {"block_type": "boundary", "items": draft.boundary_points},
            {"block_type": "style", "items": draft.style_points},
            {"block_type": "safety", "items": draft.safety_points},
            {"block_type": "unresolved_questions", "items": draft.unresolved_questions},
        ]
        projected, total_chars, truncated = _bound_projection_blocks(blocks, max_chars=max_chars)
        projection = PersonaProjectionCandidate(
            projection_candidate_id=new_persona_projection_candidate_id(),
            draft_id=draft.draft_id,
            candidate_id=candidate.candidate_id,
            projection_type=projection_type,
            projected_blocks=projected,
            total_chars=total_chars,
            truncated=truncated,
            canonical_import_enabled=False,
            created_at=utc_now_iso(),
            projection_attrs={
                "max_chars": max_chars,
                "prompt_candidate_only": True,
                "auto_activation_enabled": False,
            },
        )
        self._record(
            "persona_projection_candidate_created",
            objects=[
                _object(
                    "persona_projection_candidate",
                    projection.projection_candidate_id,
                    projection.to_dict(),
                )
            ],
            links=[
                ("projection_candidate_object", projection.projection_candidate_id),
                ("draft_object", draft.draft_id),
                ("candidate_object", candidate.candidate_id),
            ],
            object_links=[
                (projection.projection_candidate_id, draft.draft_id, "projects_draft"),
                (projection.projection_candidate_id, candidate.candidate_id, "projects_candidate"),
            ],
            attrs={
                "projection_type": projection.projection_type,
                "canonical_import_enabled": False,
                "truncated": projection.truncated,
            },
        )
        return projection

    def record_risk_note(
        self,
        *,
        source_id: str,
        candidate_id: str,
        risk_level: str,
        risk_categories: list[str],
        message: str,
        review_required: bool = True,
        risk_attrs: dict[str, Any] | None = None,
    ) -> PersonaSourceRiskNote:
        note = PersonaSourceRiskNote(
            risk_note_id=new_persona_source_risk_note_id(),
            source_id=source_id,
            candidate_id=candidate_id,
            risk_level=risk_level,
            risk_categories=list(risk_categories),
            message=message,
            review_required=review_required,
            created_at=utc_now_iso(),
            risk_attrs=dict(risk_attrs or {}),
        )
        self._record(
            "persona_source_risk_note_recorded",
            objects=[_object("persona_source_risk_note", note.risk_note_id, note.to_dict())],
            links=[
                ("risk_note_object", note.risk_note_id),
                ("source_object", source_id),
                ("candidate_object", candidate_id),
            ],
            object_links=[
                (note.risk_note_id, source_id, "describes_source"),
                (note.risk_note_id, candidate_id, "describes_candidate"),
            ],
            attrs={"risk_level": risk_level, "review_required": review_required},
        )
        if review_required:
            self._record(
                "persona_source_review_required",
                objects=[_object("persona_source_risk_note", note.risk_note_id, note.to_dict())],
                links=[("risk_note_object", note.risk_note_id)],
                object_links=[],
                attrs={"risk_level": risk_level},
            )
        return note

    def _record_validation(
        self,
        validation: PersonaSourceValidationResult,
        *,
        source_id: str | None,
        candidate_id: str | None,
    ) -> None:
        links = [("validation_object", validation.validation_id)]
        object_links: list[tuple[str, str, str]] = []
        if source_id:
            links.append(("source_object", source_id))
            object_links.append((validation.validation_id, source_id, "validates_source"))
        if candidate_id:
            links.append(("candidate_object", candidate_id))
            object_links.append((validation.validation_id, candidate_id, "validates_candidate"))
        self._record(
            "persona_source_validation_recorded",
            objects=[
                _object(
                    "persona_source_validation_result",
                    validation.validation_id,
                    validation.to_dict(),
                )
            ],
            links=links,
            object_links=object_links,
            attrs={"status": validation.status, "validation_kind": validation.validation_kind},
        )
        if validation.status == "invalid":
            self._record(
                "persona_source_rejected",
                objects=[
                    _object(
                        "persona_source_validation_result",
                        validation.validation_id,
                        validation.to_dict(),
                    )
                ],
                links=[("validation_object", validation.validation_id)],
                object_links=[],
                attrs={"validation_kind": validation.validation_kind},
            )

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "persona_source_staged_import": True,
                "canonical_import_enabled": False,
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
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preview_text(text: str, max_chars: int = 2000) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[:max_chars].rstrip() + " [preview truncated]"


def detect_source_type(path_or_name: str | None, media_type: str | None = None) -> str:
    media = (media_type or "").casefold()
    name = (path_or_name or "").casefold()
    if "html" in media or name.endswith(".html"):
        return "html"
    if "markdown" in media or name.endswith(".md"):
        return "markdown"
    return "text"


def strip_html_to_text(html: str) -> str:
    without_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    without_tags = re.sub(r"(?s)<[^>]+>", " ", without_scripts)
    return unescape(" ".join(without_tags.split())).replace("\xa0", " ")


def extract_persona_points(text: str) -> dict[str, list[str]]:
    buckets = {
        "identity_points": [],
        "role_points": [],
        "boundary_points": [],
        "style_points": [],
        "safety_points": [],
        "unresolved_questions": [],
    }
    current = "role_points"
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("-*0123456789. ").strip()
        if not line:
            continue
        lowered = line.casefold()
        if "identity" in lowered or "who" in lowered:
            current = "identity_points"
        elif "role" in lowered or "assist" in lowered:
            current = "role_points"
        elif "boundary" in lowered or "must not" in lowered or "cannot" in lowered:
            current = "boundary_points"
        elif "style" in lowered or "tone" in lowered:
            current = "style_points"
        elif "safety" in lowered or "private" in lowered or "permission" in lowered:
            current = "safety_points"
        if "?" in line:
            _append_unique(buckets["unresolved_questions"], line)
        elif not line.startswith("#"):
            _append_unique(buckets[current], line)
    for key, fallback in [
        ("identity_points", "No identity point extracted; keep under review."),
        ("role_points", "No role point extracted; keep under review."),
        ("boundary_points", "No boundary point extracted; require explicit review."),
        ("style_points", "No style point extracted; keep neutral style."),
        ("safety_points", "No safety point extracted; do not activate automatically."),
    ]:
        if not buckets[key]:
            buckets[key].append(fallback)
    return buckets


def validate_allowed_extension(path: Path, allowed_extensions: list[str]) -> None:
    suffix = path.suffix.casefold()
    allowed = {item.casefold() for item in allowed_extensions}
    if suffix not in allowed:
        raise PersonaSourceImportError(f"Unsupported source extension: {suffix}")


def safe_read_text_file(
    path: str | Path,
    *,
    source_root: str | Path | None = None,
    max_bytes: int = 262144,
    allowed_extensions: list[str] | None = None,
) -> str:
    resolved_path = Path(path).resolve(strict=False)
    if source_root is not None:
        resolved_path.relative_to(Path(source_root).resolve(strict=False))
    validate_allowed_extension(resolved_path, allowed_extensions or DEFAULT_ALLOWED_EXTENSIONS)
    if not resolved_path.exists() or not resolved_path.is_file():
        raise FileNotFoundError(str(resolved_path))
    size = resolved_path.stat().st_size
    if size > max_bytes:
        raise PersonaSourceImportError(f"Persona source file exceeds max_bytes: {size}")
    data = resolved_path.read_bytes()
    if b"\x00" in data:
        raise PersonaSourceImportError("Persona source file appears to be binary")
    return data.decode("utf-8")


def _bound_projection_blocks(
    blocks: list[dict[str, Any]],
    *,
    max_chars: int,
) -> tuple[list[dict[str, Any]], int, bool]:
    projected: list[dict[str, Any]] = []
    total = 0
    truncated = False
    for block in blocks:
        items = [str(item) for item in block.get("items", [])]
        kept_items: list[str] = []
        for item in items:
            remaining = max_chars - total
            if remaining <= 0:
                truncated = True
                break
            rendered = item if len(item) <= remaining else item[:remaining]
            if len(rendered) < len(item):
                truncated = True
            kept_items.append(rendered)
            total += len(rendered)
        if kept_items:
            projected.append({**block, "items": kept_items})
        if truncated:
            break
    return projected, total, truncated


def _matches_any(value: str, patterns: list[str]) -> bool:
    from fnmatch import fnmatchcase

    normalized = value.replace("\\", "/").casefold()
    return any(fnmatchcase(normalized, pattern.replace("\\", "/").casefold()) for pattern in patterns)


def _relative_posix(path: Path, root: Path) -> str:
    return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()


def _append_unique(items: list[str], item: str) -> None:
    if item not in items:
        items.append(item)


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

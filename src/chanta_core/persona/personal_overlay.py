from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonalOverlayError
from chanta_core.persona.ids import (
    new_personal_overlay_boundary_finding_id,
    new_personal_directory_config_id,
    new_personal_overlay_load_request_id,
    new_personal_overlay_load_result_id,
    new_personal_directory_manifest_id,
    new_personal_projection_ref_id,
)
from chanta_core.persona.source_import import hash_text, preview_text
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


DEFAULT_PERSONAL_DIRECTORY_ENV_KEY = "CHANTA_PERSONAL_DIRECTORY_ROOT"
EXCLUDED_ROOT_NAMES = ["letters", "messages", "archive"]
EXCLUDED_SOURCE_PATTERNS = ["message_to_*.md", "letter_to_*.md"]
PROMPT_PROJECTION_DIRS = ["overlay", "profiles", "mode_loadouts"]


@dataclass(frozen=True)
class PersonalDirectoryConfig:
    config_id: str
    directory_name: str
    directory_root: str
    config_source: str | None
    private: bool
    status: str
    created_at: str
    config_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "directory_name": self.directory_name,
            "directory_root": self.directory_root,
            "config_source": self.config_source,
            "private": self.private,
            "status": self.status,
            "created_at": self.created_at,
            "config_attrs": dict(self.config_attrs),
        }


@dataclass(frozen=True)
class PersonalDirectoryManifest:
    manifest_id: str
    config_id: str | None
    directory_root: str
    source_root: str | None
    overlay_dir: str | None
    profiles_dir: str | None
    mode_loadouts_dir: str | None
    validation_dir: str | None
    source_manifest_ref: str | None
    available_projection_refs: list[dict[str, Any]]
    available_profile_refs: list[dict[str, Any]]
    available_loadout_refs: list[dict[str, Any]]
    excluded_roots: list[str]
    created_at: str
    manifest_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "config_id": self.config_id,
            "directory_root": self.directory_root,
            "source_root": self.source_root,
            "overlay_dir": self.overlay_dir,
            "profiles_dir": self.profiles_dir,
            "mode_loadouts_dir": self.mode_loadouts_dir,
            "validation_dir": self.validation_dir,
            "source_manifest_ref": self.source_manifest_ref,
            "available_projection_refs": [dict(item) for item in self.available_projection_refs],
            "available_profile_refs": [dict(item) for item in self.available_profile_refs],
            "available_loadout_refs": [dict(item) for item in self.available_loadout_refs],
            "excluded_roots": list(self.excluded_roots),
            "created_at": self.created_at,
            "manifest_attrs": dict(self.manifest_attrs),
        }


@dataclass(frozen=True)
class PersonalOverlayLoadRequest:
    request_id: str
    manifest_id: str
    requested_projection: str | None
    requested_profile: str | None
    requested_mode: str | None
    session_id: str | None
    turn_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "manifest_id": self.manifest_id,
            "requested_projection": self.requested_projection,
            "requested_profile": self.requested_profile,
            "requested_mode": self.requested_mode,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class PersonalProjectionRef:
    projection_ref_id: str
    manifest_id: str
    projection_name: str
    projection_path: str
    projection_kind: str
    content_hash: str | None
    content_preview: str
    total_chars: int | None
    private: bool
    safe_for_prompt: bool
    created_at: str
    ref_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_ref_id": self.projection_ref_id,
            "manifest_id": self.manifest_id,
            "projection_name": self.projection_name,
            "projection_path": self.projection_path,
            "projection_kind": self.projection_kind,
            "content_hash": self.content_hash,
            "content_preview": self.content_preview,
            "total_chars": self.total_chars,
            "private": self.private,
            "safe_for_prompt": self.safe_for_prompt,
            "created_at": self.created_at,
            "ref_attrs": dict(self.ref_attrs),
        }


@dataclass(frozen=True)
class PersonalOverlayLoadResult:
    result_id: str
    request_id: str
    manifest_id: str
    loaded_projection_ref_ids: list[str]
    rendered_blocks: list[dict[str, Any]]
    total_chars: int
    truncated: bool
    denied: bool
    finding_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "manifest_id": self.manifest_id,
            "loaded_projection_ref_ids": list(self.loaded_projection_ref_ids),
            "rendered_blocks": list(self.rendered_blocks),
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "denied": self.denied,
            "finding_ids": list(self.finding_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class PersonalOverlayBoundaryFinding:
    finding_id: str
    manifest_id: str | None
    request_id: str | None
    finding_type: str
    status: str
    severity: str | None
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "manifest_id": self.manifest_id,
            "request_id": self.request_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


class PersonalOverlayLoaderService:
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
        self._projection_paths_by_ref_id: dict[str, Path] = {}

    def load_config_from_env(
        self,
        env_key: str = DEFAULT_PERSONAL_DIRECTORY_ENV_KEY,
        directory_name: str = "personal_directory",
    ) -> PersonalDirectoryConfig | None:
        root = os.environ.get(env_key)
        if not root:
            return None
        return self.register_config(
            directory_name=directory_name,
            directory_root=root,
            config_source=f"env:{env_key}",
        )

    def register_config(
        self,
        *,
        directory_name: str,
        directory_root: str | Path,
        config_source: str = "explicit_input",
        private: bool = True,
        status: str = "registered",
        config_attrs: dict[str, Any] | None = None,
    ) -> PersonalDirectoryConfig:
        root = Path(directory_root).resolve(strict=False)
        config = PersonalDirectoryConfig(
            config_id=new_personal_directory_config_id(),
            directory_name=directory_name,
            directory_root=str(root),
            config_source=config_source,
            private=private,
            status=status,
            created_at=utc_now_iso(),
            config_attrs={
                "root_hash": _path_hash(root),
                "root_basename": root.name,
                **dict(config_attrs or {}),
            },
        )
        self._record(
            "personal_directory_config_registered",
            objects=[_object("personal_directory_config", config.config_id, config.to_dict())],
            links=[("config_object", config.config_id)],
            object_links=[],
            attrs={"config_source": config.config_source, "private": config.private},
        )
        return config

    def load_manifest(self, config: PersonalDirectoryConfig) -> PersonalDirectoryManifest:
        root = Path(config.directory_root).resolve(strict=False)
        if not root.exists() or not root.is_dir():
            raise PersonalOverlayError("Personal Directory root does not exist or is not a directory")
        source_root = root / "source"
        overlay_dir = root / "overlay"
        profiles_dir = root / "profiles"
        mode_loadouts_dir = root / "mode_loadouts"
        validation_dir = root / "validation"
        excluded_roots = [str(root / name) for name in EXCLUDED_ROOT_NAMES if (root / name).exists()]
        source_manifest = overlay_dir / "source_manifest.json"
        manifest = PersonalDirectoryManifest(
            manifest_id=new_personal_directory_manifest_id(),
            config_id=config.config_id,
            directory_root=str(root),
            source_root=str(source_root),
            overlay_dir=str(overlay_dir),
            profiles_dir=str(profiles_dir),
            mode_loadouts_dir=str(mode_loadouts_dir),
            validation_dir=str(validation_dir),
            source_manifest_ref=str(source_manifest) if source_manifest.exists() else None,
            available_projection_refs=_manifest_ref_summaries(overlay_dir, "core_projection"),
            available_profile_refs=_manifest_ref_summaries(profiles_dir, "profile_projection"),
            available_loadout_refs=_manifest_ref_summaries(mode_loadouts_dir, "mode_loadout")
            if mode_loadouts_dir.exists()
            else [],
            excluded_roots=excluded_roots,
            created_at=utc_now_iso(),
            manifest_attrs={
                "root_hash": _path_hash(root),
                "source_root_present": source_root.exists(),
                "overlay_dir_present": overlay_dir.exists(),
                "profiles_dir_present": profiles_dir.exists(),
                "mode_loadouts_dir_present": mode_loadouts_dir.exists(),
                "validation_dir_present": validation_dir.exists(),
                "letters_excluded": True,
                "messages_excluded": True,
                "archive_excluded": True,
            },
        )
        self._record(
            "personal_directory_manifest_loaded",
            objects=[
                _object("personal_directory_manifest", manifest.manifest_id, manifest.to_dict())
            ],
            links=[
                ("manifest_object", manifest.manifest_id),
                ("config_object", config.config_id),
            ],
            object_links=[(manifest.manifest_id, config.config_id, "uses_config")],
            attrs={
                "projection_ref_count": len(manifest.available_projection_refs),
                "loadout_ref_count": len(manifest.available_loadout_refs),
            },
        )
        return manifest

    def check_overlay_boundaries(
        self,
        manifest: PersonalDirectoryManifest,
        public_repo_root: str | Path | None = None,
    ) -> list[PersonalOverlayBoundaryFinding]:
        findings: list[PersonalOverlayBoundaryFinding] = []
        root = Path(manifest.directory_root).resolve(strict=False)
        source_root = Path(manifest.source_root).resolve(strict=False)
        if public_repo_root is not None and _is_relative_to(
            root,
            Path(public_repo_root).resolve(strict=False),
        ):
            findings.append(
                self._finding(
                    manifest_id=manifest.manifest_id,
                    finding_type="personal_root_inside_public_repo",
                    status="failed",
                    severity="high",
                    message="Personal Directory root is inside the public repository boundary.",
                    subject_ref=_redacted_path_ref(root),
                )
            )
        for excluded in manifest.excluded_roots:
            if _is_relative_to(Path(excluded).resolve(strict=False), source_root):
                findings.append(
                    self._finding(
                        manifest_id=manifest.manifest_id,
                        finding_type="letters_source_import_attempt",
                        status="failed",
                        severity="high",
                        message="An excluded Personal Directory area appears under source.",
                        subject_ref=_redacted_path_ref(Path(excluded)),
                    )
                )
        if source_root.exists():
            for path in sorted(source_root.rglob("*")):
                if not path.is_file():
                    continue
                relative = path.relative_to(source_root).as_posix().casefold()
                name = path.name.casefold()
                relative_parts = relative.split("/")
                if "letters" in relative_parts:
                    findings.append(
                        self._finding(
                            manifest_id=manifest.manifest_id,
                            finding_type="letters_source_import_attempt",
                            status="failed",
                            severity="high",
                            message="Letters area appears under source.",
                            subject_ref=_redacted_path_ref(path),
                        )
                    )
                if "messages" in relative_parts:
                    findings.append(
                        self._finding(
                            manifest_id=manifest.manifest_id,
                            finding_type="messages_source_import_attempt",
                            status="failed",
                            severity="high",
                            message="Messages area appears under source.",
                            subject_ref=_redacted_path_ref(path),
                        )
                    )
                if "archive" in relative_parts:
                    findings.append(
                        self._finding(
                            manifest_id=manifest.manifest_id,
                            finding_type="private_content_leak_risk",
                            status="failed",
                            severity="high",
                            message="Archive area appears under source.",
                            subject_ref=_redacted_path_ref(path),
                        )
                    )
                if name.startswith("message_to_") or name.startswith("letter_to_"):
                    findings.append(
                        self._finding(
                            manifest_id=manifest.manifest_id,
                            finding_type="letters_source_import_attempt",
                            status="failed",
                            severity="high",
                            message="Message-like private note filename appears under source.",
                            subject_ref=_redacted_path_ref(path),
                        )
                    )
        for directory_ref in [manifest.overlay_dir, manifest.profiles_dir, manifest.mode_loadouts_dir]:
            if directory_ref is None:
                continue
            directory = Path(directory_ref)
            if not directory.exists():
                continue
            for path in sorted(directory.glob("*.md")):
                if not _is_relative_to(path.resolve(strict=False), root):
                    findings.append(
                        self._finding(
                            manifest_id=manifest.manifest_id,
                            finding_type="unsafe_projection_ref",
                            status="failed",
                            severity="high",
                            message="Projection path resolves outside the Personal Directory root.",
                            subject_ref=_redacted_path_ref(path),
                        )
                    )
        self._record(
            "personal_overlay_boundary_checked",
            objects=[_object("personal_directory_manifest", manifest.manifest_id, manifest.to_dict())]
            + [
                _object("personal_overlay_boundary_finding", finding.finding_id, finding.to_dict())
                for finding in findings
            ],
            links=[("manifest_object", manifest.manifest_id)]
            + [("finding_object", finding.finding_id) for finding in findings],
            object_links=[(finding.finding_id, manifest.manifest_id, "checks_manifest") for finding in findings],
            attrs={
                "finding_count": len(findings),
                "failed_count": sum(1 for finding in findings if finding.status == "failed"),
            },
        )
        return findings

    def register_projection_refs(
        self,
        manifest: PersonalDirectoryManifest,
        *,
        max_preview_chars: int = 1000,
    ) -> list[PersonalProjectionRef]:
        root = Path(manifest.directory_root).resolve(strict=False)
        refs: list[PersonalProjectionRef] = []
        for directory_name, projection_kind in [
            ("overlay", "core_projection"),
            ("profiles", "profile_projection"),
            ("mode_loadouts", "mode_loadout"),
        ]:
            directory = root / directory_name
            if not directory.exists():
                continue
            for path in sorted(directory.glob("*.md")):
                resolved = path.resolve(strict=False)
                safe = _is_relative_to(resolved, root) and directory_name in PROMPT_PROJECTION_DIRS
                text = _safe_read_projection_file(resolved, source_root=root)
                ref = PersonalProjectionRef(
                    projection_ref_id=new_personal_projection_ref_id(),
                    manifest_id=manifest.manifest_id,
                    projection_name=path.stem,
                    projection_path=str(resolved),
                    projection_kind=projection_kind,
                    content_hash=hash_text(text),
                    content_preview=preview_text(text, max_chars=max_preview_chars),
                    total_chars=len(text),
                    private=True,
                    safe_for_prompt=safe,
                    created_at=utc_now_iso(),
                    ref_attrs={
                        "path_hash": _path_hash(resolved),
                        "path_basename": resolved.name,
                        "source_body": False,
                        "prompt_projection_ref": True,
                    },
                )
                self._projection_paths_by_ref_id[ref.projection_ref_id] = resolved
                refs.append(ref)
                self._record(
                    "personal_projection_ref_registered",
                    objects=[
                        _object(
                            "personal_projection_ref",
                            ref.projection_ref_id,
                            ref.to_dict(),
                        )
                    ],
                    links=[
                        ("projection_ref_object", ref.projection_ref_id),
                        ("manifest_object", manifest.manifest_id),
                    ],
                    object_links=[(ref.projection_ref_id, manifest.manifest_id, "belongs_to_manifest")],
                    attrs={
                        "projection_kind": ref.projection_kind,
                        "safe_for_prompt": ref.safe_for_prompt,
                    },
                )
        return refs

    def load_projection_for_prompt(
        self,
        *,
        manifest: PersonalDirectoryManifest,
        projection_refs: list[PersonalProjectionRef],
        requested_projection: str | None = None,
        requested_profile: str | None = None,
        requested_mode: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        max_chars: int = 6000,
        boundary_findings: list[PersonalOverlayBoundaryFinding] | None = None,
    ) -> PersonalOverlayLoadResult:
        request = PersonalOverlayLoadRequest(
            request_id=new_personal_overlay_load_request_id(),
            manifest_id=manifest.manifest_id,
            requested_projection=requested_projection,
            requested_profile=requested_profile,
            requested_mode=requested_mode,
            session_id=session_id,
            turn_id=turn_id,
            created_at=utc_now_iso(),
            request_attrs={"max_chars": max_chars},
        )
        self._record(
            "personal_overlay_load_requested",
            objects=[
                _object("personal_overlay_load_request", request.request_id, request.to_dict())
            ],
            links=[
                ("load_request_object", request.request_id),
                ("manifest_object", manifest.manifest_id),
            ],
            object_links=[(request.request_id, manifest.manifest_id, "uses_manifest")],
            attrs={
                "requested_mode": requested_mode or "",
                "requested_profile": requested_profile or "",
                "requested_projection": requested_projection or "",
            },
        )
        findings = list(boundary_findings or [])
        unsafe_findings = [finding for finding in findings if finding.status == "failed"]
        selected_refs = [
            ref
            for ref in projection_refs
            if ref.safe_for_prompt
            and _matches_requested_ref(
                ref,
                requested_projection=requested_projection,
                requested_profile=requested_profile,
                requested_mode=requested_mode,
            )
        ]
        denied = bool(unsafe_findings)
        rendered_blocks: list[dict[str, Any]] = []
        loaded_ids: list[str] = []
        total_chars = 0
        truncated = False
        if not denied:
            for ref in selected_refs:
                path = self._projection_paths_by_ref_id.get(ref.projection_ref_id)
                if path is None:
                    continue
                text = _safe_read_projection_file(path, source_root=Path(manifest.directory_root))
                remaining = max_chars - total_chars
                if remaining <= 0:
                    truncated = True
                    break
                rendered = text if len(text) <= remaining else text[:remaining]
                if len(rendered) < len(text):
                    truncated = True
                rendered_blocks.append(
                    {
                        "projection_ref_id": ref.projection_ref_id,
                        "projection_name": ref.projection_name,
                        "projection_kind": ref.projection_kind,
                        "content": rendered,
                    }
                )
                loaded_ids.append(ref.projection_ref_id)
                total_chars += len(rendered)
                if truncated:
                    break
        result = PersonalOverlayLoadResult(
            result_id=new_personal_overlay_load_result_id(),
            request_id=request.request_id,
            manifest_id=manifest.manifest_id,
            loaded_projection_ref_ids=loaded_ids,
            rendered_blocks=rendered_blocks,
            total_chars=total_chars,
            truncated=truncated,
            denied=denied,
            finding_ids=[finding.finding_id for finding in unsafe_findings],
            created_at=utc_now_iso(),
            result_attrs={
                "source_bodies_loaded": False,
                "auto_activation_enabled": False,
                "permission_grants_created": False,
            },
        )
        event_activity = "personal_overlay_load_denied" if denied else "personal_overlay_load_completed"
        self._record(
            event_activity,
            objects=[
                _object("personal_overlay_load_request", request.request_id, request.to_dict()),
                _object("personal_overlay_load_result", result.result_id, result.to_dict()),
            ],
            links=[
                ("load_request_object", request.request_id),
                ("load_result_object", result.result_id),
                ("manifest_object", manifest.manifest_id),
            ]
            + [("projection_ref_object", ref_id) for ref_id in loaded_ids]
            + [("finding_object", finding.finding_id) for finding in unsafe_findings],
            object_links=[(result.result_id, request.request_id, "belongs_to_request")]
            + [(result.result_id, ref_id, "includes_projection_ref") for ref_id in loaded_ids]
            + [(finding.finding_id, request.request_id, "checks_request") for finding in unsafe_findings],
            attrs={
                "denied": result.denied,
                "truncated": result.truncated,
                "loaded_projection_ref_count": len(loaded_ids),
            },
        )
        if not denied and rendered_blocks:
            self._record(
                "personal_projection_attached_to_prompt",
                objects=[_object("personal_overlay_load_result", result.result_id, result.to_dict())],
                links=[("load_result_object", result.result_id)],
                object_links=[],
                attrs={"total_chars": result.total_chars},
            )
        return result

    def render_personal_overlay_block(self, result: PersonalOverlayLoadResult) -> str | None:
        if result.denied or not result.rendered_blocks:
            return None
        body = "\n\n".join(str(block.get("content") or "") for block in result.rendered_blocks)
        return (
            "Personal Overlay projection:\n"
            "Boundary: local-only optional projection; source files and letters are not canonical persona.\n"
            f"{body}"
        )

    def _finding(
        self,
        *,
        manifest_id: str,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str,
        request_id: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> PersonalOverlayBoundaryFinding:
        finding = PersonalOverlayBoundaryFinding(
            finding_id=new_personal_overlay_boundary_finding_id(),
            manifest_id=manifest_id,
            request_id=request_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs=dict(finding_attrs or {}),
        )
        self._record(
            "personal_overlay_boundary_finding_recorded",
            objects=[
                _object(
                    "personal_overlay_boundary_finding",
                    finding.finding_id,
                    finding.to_dict(),
                )
            ],
            links=[("finding_object", finding.finding_id), ("manifest_object", manifest_id)],
            object_links=[(finding.finding_id, manifest_id, "checks_manifest")],
            attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
            },
        )
        return finding

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
                "personal_overlay_boundary": True,
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


def _safe_read_projection_file(path: Path, *, source_root: Path, max_bytes: int = 262144) -> str:
    resolved = path.resolve(strict=False)
    if not _is_relative_to(resolved, source_root.resolve(strict=False)):
        raise PersonalOverlayError("projection path is outside Personal Directory root")
    if resolved.suffix.casefold() != ".md":
        raise PersonalOverlayError("Personal Overlay prompt projections must be markdown files")
    if not resolved.exists() or not resolved.is_file():
        raise FileNotFoundError(str(resolved))
    size = resolved.stat().st_size
    if size > max_bytes:
        raise PersonalOverlayError("Personal Overlay projection file exceeds max_bytes")
    data = resolved.read_bytes()
    if b"\x00" in data:
        raise PersonalOverlayError("Personal Overlay projection file appears to be binary")
    return data.decode("utf-8")


def _matches_requested_ref(
    ref: PersonalProjectionRef,
    *,
    requested_projection: str | None,
    requested_profile: str | None,
    requested_mode: str | None,
) -> bool:
    name = ref.projection_name.casefold()
    if requested_projection and requested_projection.casefold() not in name:
        return False
    if requested_profile and requested_profile.casefold() not in name:
        return False
    if requested_mode and requested_mode.casefold() not in name:
        return False
    return True


def _manifest_ref_summaries(directory: Path, projection_kind: str) -> list[dict[str, Any]]:
    if not directory.exists() or not directory.is_dir():
        return []
    return [
        {
            "name": path.stem,
            "kind": projection_kind,
            "path_basename": path.name,
            "path_hash": _path_hash(path),
        }
        for path in sorted(directory.glob("*.md"))
    ]


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def _path_hash(path: Path) -> str:
    return hashlib.sha256(str(path.resolve(strict=False)).encode("utf-8")).hexdigest()


def _redacted_path_ref(path: Path) -> str:
    resolved = path.resolve(strict=False)
    return f"{resolved.name}:{_path_hash(resolved)[:12]}"


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



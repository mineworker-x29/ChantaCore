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
    new_personal_cli_command_result_id,
    new_personal_runtime_config_view_id,
    new_personal_runtime_diagnostic_id,
    new_personal_runtime_health_check_id,
    new_personal_runtime_status_snapshot_id,
)
from chanta_core.persona.personal_conformance import PersonalConformanceService
from chanta_core.persona.personal_overlay import (
    DEFAULT_PERSONAL_DIRECTORY_ENV_KEY,
    PersonalDirectoryConfig,
    PersonalDirectoryManifest,
    PersonalOverlayBoundaryFinding,
    PersonalOverlayLoaderService,
    PersonalProjectionRef,
)
from chanta_core.persona.personal_smoke_test import PersonalRuntimeSmokeTestService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class PersonalRuntimeConfigView:
    config_view_id: str
    personal_directory_configured: bool
    directory_root_redacted: str | None
    config_source: str | None
    env_key_used: str
    created_at: str
    config_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_view_id": self.config_view_id,
            "personal_directory_configured": self.personal_directory_configured,
            "directory_root_redacted": self.directory_root_redacted,
            "config_source": self.config_source,
            "env_key_used": self.env_key_used,
            "created_at": self.created_at,
            "config_attrs": dict(self.config_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeStatusSnapshot:
    status_id: str
    config_view_id: str
    manifest_id: str | None
    personal_directory_configured: bool
    source_root_present: bool
    overlay_dir_present: bool
    profiles_dir_present: bool
    mode_loadouts_dir_present: bool
    validation_dir_present: bool
    letters_dir_excluded: bool
    messages_dir_excluded: bool
    archive_dir_excluded: bool
    available_projection_count: int
    available_profile_count: int
    available_loadout_count: int
    conformance_status: str
    smoke_status: str
    created_at: str
    status_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_id": self.status_id,
            "config_view_id": self.config_view_id,
            "manifest_id": self.manifest_id,
            "personal_directory_configured": self.personal_directory_configured,
            "source_root_present": self.source_root_present,
            "overlay_dir_present": self.overlay_dir_present,
            "profiles_dir_present": self.profiles_dir_present,
            "mode_loadouts_dir_present": self.mode_loadouts_dir_present,
            "validation_dir_present": self.validation_dir_present,
            "letters_dir_excluded": self.letters_dir_excluded,
            "messages_dir_excluded": self.messages_dir_excluded,
            "archive_dir_excluded": self.archive_dir_excluded,
            "available_projection_count": self.available_projection_count,
            "available_profile_count": self.available_profile_count,
            "available_loadout_count": self.available_loadout_count,
            "conformance_status": self.conformance_status,
            "smoke_status": self.smoke_status,
            "created_at": self.created_at,
            "status_attrs": dict(self.status_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeHealthCheck:
    health_check_id: str
    status_id: str
    check_type: str
    status: str
    severity: str
    message: str
    created_at: str
    check_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "health_check_id": self.health_check_id,
            "status_id": self.status_id,
            "check_type": self.check_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "created_at": self.created_at,
            "check_attrs": dict(self.check_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeDiagnostic:
    diagnostic_id: str
    command_name: str
    status: str
    severity: str
    message: str
    recommendation: str | None
    created_at: str
    diagnostic_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "diagnostic_id": self.diagnostic_id,
            "command_name": self.command_name,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "recommendation": self.recommendation,
            "created_at": self.created_at,
            "diagnostic_attrs": dict(self.diagnostic_attrs),
        }


@dataclass(frozen=True)
class PersonalCLICommandResult:
    result_id: str
    command_name: str
    exit_code: int
    status: str
    summary: str
    diagnostic_ids: list[str]
    status_snapshot_id: str | None
    conformance_result_ids: list[str]
    smoke_result_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "command_name": self.command_name,
            "exit_code": self.exit_code,
            "status": self.status,
            "summary": self.summary,
            "diagnostic_ids": list(self.diagnostic_ids),
            "status_snapshot_id": self.status_snapshot_id,
            "conformance_result_ids": list(self.conformance_result_ids),
            "smoke_result_ids": list(self.smoke_result_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class PersonalRuntimeSurfaceService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
        overlay_loader_service: PersonalOverlayLoaderService | None = None,
        conformance_service: PersonalConformanceService | None = None,
        smoke_test_service: PersonalRuntimeSmokeTestService | None = None,
        public_repo_root: str | Path | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.overlay_loader_service = overlay_loader_service or PersonalOverlayLoaderService(
            trace_service=self.trace_service
        )
        self.conformance_service = conformance_service or PersonalConformanceService(
            trace_service=self.trace_service
        )
        self.smoke_test_service = smoke_test_service or PersonalRuntimeSmokeTestService(
            trace_service=self.trace_service
        )
        self.public_repo_root = Path(public_repo_root).resolve(strict=False) if public_repo_root else None
        self.last_config_view: PersonalRuntimeConfigView | None = None
        self.last_status_snapshot: PersonalRuntimeStatusSnapshot | None = None
        self.last_health_checks: list[PersonalRuntimeHealthCheck] = []
        self.last_diagnostics: list[PersonalRuntimeDiagnostic] = []
        self.last_cli_result: PersonalCLICommandResult | None = None

    def load_config_view(
        self,
        env_key: str = DEFAULT_PERSONAL_DIRECTORY_ENV_KEY,
        *,
        show_paths: bool = False,
    ) -> PersonalRuntimeConfigView:
        root_value = os.environ.get(env_key)
        root = Path(root_value).resolve(strict=False) if root_value else None
        config_view = PersonalRuntimeConfigView(
            config_view_id=new_personal_runtime_config_view_id(),
            personal_directory_configured=bool(root_value),
            directory_root_redacted=_display_path(root, show_paths=show_paths) if root else None,
            config_source=f"env:{env_key}" if root_value else None,
            env_key_used=env_key,
            created_at=utc_now_iso(),
            config_attrs={
                "root_hash": _path_hash(root) if root else None,
                "root_basename": root.name if root else None,
                "directory_root_raw": str(root) if root else None,
                "directory_exists": bool(root.exists() and root.is_dir()) if root else False,
                "path_redacted": bool(root) and not show_paths,
                "source_bodies_printed": False,
                "mode_activation_enabled": False,
                "capability_grants_created": False,
            },
        )
        self.last_config_view = config_view
        self._record(
            "personal_runtime_config_view_created",
            objects=[
                _object(
                    "personal_runtime_config_view",
                    config_view.config_view_id,
                    _public_attrs(config_view.to_dict()),
                )
            ],
            links=[("config_view_object", config_view.config_view_id)],
            object_links=[],
            attrs={
                "personal_directory_configured": config_view.personal_directory_configured,
                "path_redacted": config_view.config_attrs.get("path_redacted", False),
            },
        )
        return config_view

    def build_status_snapshot(
        self,
        config_view: PersonalRuntimeConfigView,
        manifest: PersonalDirectoryManifest | None = None,
    ) -> PersonalRuntimeStatusSnapshot:
        manifest_attrs = manifest.manifest_attrs if manifest is not None else {}
        status = PersonalRuntimeStatusSnapshot(
            status_id=new_personal_runtime_status_snapshot_id(),
            config_view_id=config_view.config_view_id,
            manifest_id=manifest.manifest_id if manifest is not None else None,
            personal_directory_configured=config_view.personal_directory_configured,
            source_root_present=bool(manifest_attrs.get("source_root_present")),
            overlay_dir_present=bool(manifest_attrs.get("overlay_dir_present")),
            profiles_dir_present=bool(manifest_attrs.get("profiles_dir_present")),
            mode_loadouts_dir_present=bool(manifest_attrs.get("mode_loadouts_dir_present")),
            validation_dir_present=bool(manifest_attrs.get("validation_dir_present")),
            letters_dir_excluded=bool(manifest_attrs.get("letters_excluded")),
            messages_dir_excluded=bool(manifest_attrs.get("messages_excluded")),
            archive_dir_excluded=bool(manifest_attrs.get("archive_excluded")),
            available_projection_count=len(manifest.available_projection_refs) if manifest else 0,
            available_profile_count=len(manifest.available_profile_refs) if manifest else 0,
            available_loadout_count=len(manifest.available_loadout_refs) if manifest else 0,
            conformance_status="not_run",
            smoke_status="not_run",
            created_at=utc_now_iso(),
            status_attrs={
                "directory_root": config_view.directory_root_redacted,
                "directory_exists": bool(config_view.config_attrs.get("directory_exists")),
                "path_redacted": bool(config_view.config_attrs.get("path_redacted")),
                "source_bodies_printed": False,
                "letters_read_as_source": False,
                "messages_read_as_source": False,
                "archive_read_as_source": False,
                "mode_activation_enabled": False,
                "capability_grants_created": False,
            },
        )
        self.last_status_snapshot = status
        self._record(
            "personal_runtime_status_snapshot_created",
            objects=[
                _object(
                    "personal_runtime_status_snapshot",
                    status.status_id,
                    status.to_dict(),
                )
            ],
            links=[
                ("status_snapshot_object", status.status_id),
                ("config_view_object", config_view.config_view_id),
            ],
            object_links=[(status.status_id, config_view.config_view_id, "references_config_view")],
            attrs={
                "personal_directory_configured": status.personal_directory_configured,
                "projection_count": status.available_projection_count,
                "loadout_count": status.available_loadout_count,
            },
        )
        return status

    def run_health_checks(
        self,
        status_snapshot: PersonalRuntimeStatusSnapshot,
    ) -> list[PersonalRuntimeHealthCheck]:
        checks = [
            self._health_check(
                status_snapshot,
                "config_present",
                status="passed" if status_snapshot.personal_directory_configured else "warning",
                severity="medium" if not status_snapshot.personal_directory_configured else "low",
                message=(
                    "Personal Directory is configured."
                    if status_snapshot.personal_directory_configured
                    else "Personal Directory is not configured."
                ),
            ),
            self._health_check(
                status_snapshot,
                "directory_exists",
                status="passed" if status_snapshot.status_attrs.get("directory_exists") else "warning",
                severity="medium",
                message=(
                    "Configured Personal Directory exists."
                    if status_snapshot.status_attrs.get("directory_exists")
                    else "Configured Personal Directory is missing or unavailable."
                ),
            ),
            self._health_check(
                status_snapshot,
                "source_boundary",
                status="passed" if status_snapshot.source_root_present else "warning",
                severity="medium",
                message="Personal Source root presence checked.",
            ),
            self._health_check(
                status_snapshot,
                "overlay_present",
                status="passed" if status_snapshot.overlay_dir_present else "warning",
                severity="medium",
                message="Personal Overlay directory presence checked.",
            ),
            self._health_check(
                status_snapshot,
                "mode_loadouts_present",
                status="passed" if status_snapshot.mode_loadouts_dir_present else "warning",
                severity="medium",
                message="Personal Mode loadouts directory presence checked.",
            ),
            self._health_check(
                status_snapshot,
                "letters_excluded",
                status="passed" if status_snapshot.letters_dir_excluded else "warning",
                severity="high",
                message="Letters area is excluded from Personal Source.",
            ),
            self._health_check(
                status_snapshot,
                "messages_excluded",
                status="passed" if status_snapshot.messages_dir_excluded else "warning",
                severity="high",
                message="Messages area is excluded from Personal Source.",
            ),
            self._health_check(
                status_snapshot,
                "archive_excluded",
                status="passed" if status_snapshot.archive_dir_excluded else "warning",
                severity="high",
                message="Archive area is excluded from Personal Source.",
            ),
            self._health_check(
                status_snapshot,
                "private_path_redacted",
                status="passed" if status_snapshot.status_attrs.get("path_redacted") else "warning",
                severity="medium",
                message="Personal Directory path redaction checked.",
            ),
        ]
        self.last_health_checks = checks
        return checks

    def run_personal_status(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        return self._run_summary_command("personal status", show_paths=show_paths)

    def run_personal_config(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        return self._run_summary_command("personal config", show_paths=show_paths)

    def run_personal_sources(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        return self._run_summary_command("personal sources", show_paths=show_paths)

    def run_personal_overlays(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        return self._run_summary_command("personal overlays", show_paths=show_paths)

    def run_personal_modes(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        return self._run_summary_command("personal modes", show_paths=show_paths)

    def run_personal_validate(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        command_name = "personal validate"
        self._record_command_started(command_name)
        config_view = self.load_config_view(show_paths=show_paths)
        if not config_view.personal_directory_configured:
            snapshot = self.build_status_snapshot(config_view)
            diagnostic = self._diagnostic(
                command_name,
                status="failed",
                severity="medium",
                message="Personal Directory is not configured.",
                recommendation=f"Set {config_view.env_key_used} to run Personal Conformance.",
            )
            return self._command_result(
                command_name,
                exit_code=1,
                status="failed",
                summary="Personal Conformance was not run because no Personal Directory is configured.",
                diagnostics=[diagnostic],
                status_snapshot=snapshot,
            )
        manifest, projection_refs, boundary_findings, diagnostics = self._load_runtime_inputs(
            config_view,
            command_name=command_name,
            show_paths=show_paths,
        )
        snapshot = self.build_status_snapshot(config_view, manifest=manifest)
        if manifest is None:
            return self._command_result(
                command_name,
                exit_code=1,
                status="failed",
                summary="Personal Conformance could not load a Personal Directory manifest.",
                diagnostics=diagnostics,
                status_snapshot=snapshot,
            )
        _, conformance_result, _ = self.conformance_service.evaluate_personal_overlay_conformance(
            manifest=manifest,
            projection_refs=projection_refs,
            boundary_findings=boundary_findings,
            public_repo_root=self.public_repo_root,
        )
        updated_snapshot = PersonalRuntimeStatusSnapshot(
            **{**snapshot.to_dict(), "conformance_status": conformance_result.status}
        )
        self.last_status_snapshot = updated_snapshot
        return self._command_result(
            command_name,
            exit_code=0 if conformance_result.status in {"passed", "needs_review"} else 1,
            status=conformance_result.status,
            summary=(
                "Personal Conformance completed: "
                f"status={conformance_result.status}; score={conformance_result.score}."
            ),
            diagnostics=diagnostics,
            status_snapshot=updated_snapshot,
            conformance_result_ids=[conformance_result.result_id],
        )

    def run_personal_smoke(self, *, show_paths: bool = False) -> PersonalCLICommandResult:
        command_name = "personal smoke"
        self._record_command_started(command_name)
        config_view = self.load_config_view(show_paths=show_paths)
        if not config_view.personal_directory_configured:
            snapshot = self.build_status_snapshot(config_view)
            diagnostic = self._diagnostic(
                command_name,
                status="failed",
                severity="medium",
                message="Personal Directory is not configured.",
                recommendation=f"Set {config_view.env_key_used} to run deterministic Personal Runtime smoke checks.",
            )
            return self._command_result(
                command_name,
                exit_code=1,
                status="failed",
                summary="Personal Runtime Smoke Test was not run because no Personal Directory is configured.",
                diagnostics=[diagnostic],
                status_snapshot=snapshot,
            )
        manifest, _, _, diagnostics = self._load_runtime_inputs(
            config_view,
            command_name=command_name,
            show_paths=show_paths,
        )
        snapshot = self.build_status_snapshot(config_view, manifest=manifest)
        if manifest is None:
            return self._command_result(
                command_name,
                exit_code=1,
                status="failed",
                summary="Personal Runtime Smoke Test could not load a Personal Directory manifest.",
                diagnostics=diagnostics,
                status_snapshot=snapshot,
            )
        smoke_result = self._run_deterministic_smoke()
        updated_snapshot = PersonalRuntimeStatusSnapshot(
            **{**snapshot.to_dict(), "smoke_status": smoke_result.status}
        )
        self.last_status_snapshot = updated_snapshot
        return self._command_result(
            command_name,
            exit_code=0 if smoke_result.status in {"passed", "needs_review"} else 1,
            status=smoke_result.status,
            summary=(
                "Personal Runtime Smoke Test completed: "
                f"status={smoke_result.status}; score={smoke_result.score}."
            ),
            diagnostics=diagnostics,
            status_snapshot=updated_snapshot,
            smoke_result_ids=[smoke_result.result_id],
        )

    def render_cli_result(
        self,
        result: PersonalCLICommandResult,
        *,
        status_snapshot: PersonalRuntimeStatusSnapshot | None = None,
        diagnostics: list[PersonalRuntimeDiagnostic] | None = None,
        health_checks: list[PersonalRuntimeHealthCheck] | None = None,
    ) -> str:
        snapshot = status_snapshot or self.last_status_snapshot
        diagnostics = diagnostics if diagnostics is not None else self.last_diagnostics
        health_checks = health_checks if health_checks is not None else self.last_health_checks
        lines = [
            f"Personal Runtime CLI command={result.command_name}",
            f"status={result.status}",
            f"exit_code={result.exit_code}",
            f"summary={result.summary}",
        ]
        if snapshot is not None:
            lines.extend(
                [
                    f"personal_directory_configured={snapshot.personal_directory_configured}",
                    f"directory_root={snapshot.status_attrs.get('directory_root') or 'not configured'}",
                    f"source_root_present={snapshot.source_root_present}",
                    f"overlay_dir_present={snapshot.overlay_dir_present}",
                    f"profiles_dir_present={snapshot.profiles_dir_present}",
                    f"mode_loadouts_dir_present={snapshot.mode_loadouts_dir_present}",
                    f"validation_dir_present={snapshot.validation_dir_present}",
                    f"projection_count={snapshot.available_projection_count}",
                    f"profile_count={snapshot.available_profile_count}",
                    f"loadout_count={snapshot.available_loadout_count}",
                    f"conformance_status={snapshot.conformance_status}",
                    f"smoke_status={snapshot.smoke_status}",
                    f"paths_redacted={snapshot.status_attrs.get('path_redacted')}",
                ]
            )
        for diagnostic in diagnostics:
            lines.append(
                "diagnostic="
                f"{diagnostic.status}:{diagnostic.severity}:{diagnostic.message}"
            )
            if diagnostic.recommendation:
                lines.append(f"recommendation={diagnostic.recommendation}")
        if health_checks:
            rendered_checks = ", ".join(
                f"{check.check_type}:{check.status}" for check in health_checks
            )
            lines.append(f"health_checks={rendered_checks}")
        lines.append("source_bodies_printed=false")
        lines.append("mode_activation_enabled=false")
        lines.append("capability_grants_created=false")
        return "\n".join(lines)

    def _run_summary_command(self, command_name: str, *, show_paths: bool) -> PersonalCLICommandResult:
        self._record_command_started(command_name)
        config_view = self.load_config_view(show_paths=show_paths)
        manifest = None
        diagnostics: list[PersonalRuntimeDiagnostic] = []
        if config_view.personal_directory_configured:
            manifest, _, _, diagnostics = self._load_runtime_inputs(
                config_view,
                command_name=command_name,
                show_paths=show_paths,
            )
        snapshot = self.build_status_snapshot(config_view, manifest=manifest)
        checks = self.run_health_checks(snapshot)
        status = "noop" if not config_view.personal_directory_configured else _summary_status(checks)
        summary = (
            "No Personal Directory is configured; command completed without side effects."
            if status == "noop"
            else "Personal Runtime configuration summarized without reading source bodies."
        )
        return self._command_result(
            command_name,
            exit_code=0,
            status=status,
            summary=summary,
            diagnostics=diagnostics,
            status_snapshot=snapshot,
        )

    def _load_runtime_inputs(
        self,
        config_view: PersonalRuntimeConfigView,
        *,
        command_name: str,
        show_paths: bool,
    ) -> tuple[
        PersonalDirectoryManifest | None,
        list[PersonalProjectionRef],
        list[PersonalOverlayBoundaryFinding],
        list[PersonalRuntimeDiagnostic],
    ]:
        root = config_view.config_attrs.get("directory_root_raw")
        diagnostics: list[PersonalRuntimeDiagnostic] = []
        if not root:
            return None, [], [], diagnostics
        try:
            config = self.overlay_loader_service.register_config(
                directory_name="personal_directory",
                directory_root=str(root),
                config_source=config_view.config_source or "env",
                private=True,
                config_attrs={"runtime_surface": True},
            )
            manifest = self.overlay_loader_service.load_manifest(config)
            boundary_findings = self.overlay_loader_service.check_overlay_boundaries(
                manifest,
                public_repo_root=self.public_repo_root,
            )
            projection_refs = self.overlay_loader_service.register_projection_refs(
                manifest,
                max_preview_chars=0,
            )
            return manifest, projection_refs, boundary_findings, diagnostics
        except (FileNotFoundError, PersonalOverlayError, OSError) as error:
            diagnostics.append(
                self._diagnostic(
                    command_name,
                    status="failed",
                    severity="medium",
                    message=f"Personal Directory manifest could not be loaded: {type(error).__name__}.",
                    recommendation="Check that the configured Personal Directory exists and has the expected layout.",
                    diagnostic_attrs={
                        "path_ref": config_view.directory_root_redacted if not show_paths else str(root),
                    },
                )
            )
            return None, [], [], diagnostics

    def _run_deterministic_smoke(self):
        mode_name = "personal_runtime_cli_mode"
        runtime_kind = "local_runtime"
        scenario = self.smoke_test_service.create_scenario(
            scenario_name="personal_runtime_cli_boundary",
            scenario_type="personal_runtime_cli",
            description="Deterministic Personal Runtime CLI boundary smoke test.",
            private=True,
        )
        cases = self.smoke_test_service.create_default_boundary_smoke_cases(
            scenario=scenario,
            mode_name=mode_name,
            runtime_kind=runtime_kind,
        )
        shared_output = (
            f"{mode_name} reports its role boundary. "
            "There is no ambient filesystem access; file access requires explicit skill. "
            "This runtime cannot directly run tests. "
            "Local operation distinguishes explicit skills from ambient capabilities. "
            "Letters are not persona source."
        )
        return self.smoke_test_service.run_cases_against_static_outputs(
            scenario=scenario,
            cases=cases,
            outputs_by_case_id={case.case_id: shared_output for case in cases},
            observed_mode=mode_name,
            observed_runtime_kind=runtime_kind,
            observed_capabilities=[
                {"capability_name": "network_access", "availability": "not_implemented"},
                {"capability_name": "shell_execution", "availability": "not_implemented"},
            ],
        )

    def _health_check(
        self,
        status_snapshot: PersonalRuntimeStatusSnapshot,
        check_type: str,
        *,
        status: str,
        severity: str,
        message: str,
    ) -> PersonalRuntimeHealthCheck:
        check = PersonalRuntimeHealthCheck(
            health_check_id=new_personal_runtime_health_check_id(),
            status_id=status_snapshot.status_id,
            check_type=check_type,
            status=status,
            severity=severity,
            message=message,
            created_at=utc_now_iso(),
            check_attrs={"diagnostic_read_only": True},
        )
        self._record(
            "personal_runtime_health_check_recorded",
            objects=[
                _object(
                    "personal_runtime_health_check",
                    check.health_check_id,
                    check.to_dict(),
                )
            ],
            links=[
                ("health_check_object", check.health_check_id),
                ("status_snapshot_object", status_snapshot.status_id),
            ],
            object_links=[(check.health_check_id, status_snapshot.status_id, "checks_status_snapshot")],
            attrs={"check_type": check.check_type, "status": check.status, "severity": check.severity},
        )
        return check

    def _diagnostic(
        self,
        command_name: str,
        *,
        status: str,
        severity: str,
        message: str,
        recommendation: str | None,
        diagnostic_attrs: dict[str, Any] | None = None,
    ) -> PersonalRuntimeDiagnostic:
        diagnostic = PersonalRuntimeDiagnostic(
            diagnostic_id=new_personal_runtime_diagnostic_id(),
            command_name=command_name,
            status=status,
            severity=severity,
            message=message,
            recommendation=recommendation,
            created_at=utc_now_iso(),
            diagnostic_attrs={
                "diagnostic_read_only": True,
                "source_bodies_printed": False,
                **dict(diagnostic_attrs or {}),
            },
        )
        self._record(
            "personal_runtime_diagnostic_recorded",
            objects=[
                _object(
                    "personal_runtime_diagnostic",
                    diagnostic.diagnostic_id,
                    diagnostic.to_dict(),
                )
            ],
            links=[("diagnostic_object", diagnostic.diagnostic_id)],
            object_links=[],
            attrs={
                "command_name": command_name,
                "status": status,
                "severity": severity,
            },
        )
        return diagnostic

    def _command_result(
        self,
        command_name: str,
        *,
        exit_code: int,
        status: str,
        summary: str,
        diagnostics: list[PersonalRuntimeDiagnostic],
        status_snapshot: PersonalRuntimeStatusSnapshot | None,
        conformance_result_ids: list[str] | None = None,
        smoke_result_ids: list[str] | None = None,
    ) -> PersonalCLICommandResult:
        self.last_diagnostics = list(diagnostics)
        result = PersonalCLICommandResult(
            result_id=new_personal_cli_command_result_id(),
            command_name=command_name,
            exit_code=exit_code,
            status=status,
            summary=summary,
            diagnostic_ids=[item.diagnostic_id for item in diagnostics],
            status_snapshot_id=status_snapshot.status_id if status_snapshot else None,
            conformance_result_ids=list(conformance_result_ids or []),
            smoke_result_ids=list(smoke_result_ids or []),
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "source_bodies_printed": False,
                "letters_read_as_source": False,
                "messages_read_as_source": False,
                "archive_read_as_source": False,
                "mode_activation_enabled": False,
                "capability_grants_created": False,
                "tool_execution_used": False,
                "model_call_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
                "line_delimited_runtime_store_created": False,
            },
        )
        self.last_cli_result = result
        event_activity = (
            "personal_cli_command_noop"
            if status == "noop"
            else "personal_cli_command_failed"
            if exit_code
            else "personal_cli_command_completed"
        )
        objects = [_object("personal_cli_command_result", result.result_id, result.to_dict())]
        links = [("cli_command_result_object", result.result_id)]
        object_links: list[tuple[str, str, str]] = []
        if status_snapshot is not None:
            links.append(("status_snapshot_object", status_snapshot.status_id))
            object_links.append((result.result_id, status_snapshot.status_id, "references_status_snapshot"))
        for diagnostic in diagnostics:
            links.append(("diagnostic_object", diagnostic.diagnostic_id))
            object_links.append((result.result_id, diagnostic.diagnostic_id, "references_diagnostic"))
        self._record(
            event_activity,
            objects=objects,
            links=links,
            object_links=object_links,
            attrs={"command_name": command_name, "status": status, "exit_code": exit_code},
        )
        return result

    def _record_command_started(self, command_name: str) -> None:
        self._record(
            "personal_cli_command_started",
            objects=[],
            links=[],
            object_links=[],
            attrs={"command_name": command_name},
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
                "personal_runtime_surface": True,
                "read_only": True,
                "source_bodies_printed": False,
                "mode_activation_enabled": False,
                "capability_grants_created": False,
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
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )


def _summary_status(checks: list[PersonalRuntimeHealthCheck]) -> str:
    failed = any(check.status in {"failed", "error"} for check in checks)
    warnings = any(check.status == "warning" for check in checks)
    return "failed" if failed else "needs_review" if warnings else "passed"


def _display_path(path: Path, *, show_paths: bool) -> str:
    return str(path) if show_paths else _redacted_path_ref(path)


def _path_hash(path: Path | None) -> str | None:
    if path is None:
        return None
    return hashlib.sha256(str(path.resolve(strict=False)).encode("utf-8")).hexdigest()


def _redacted_path_ref(path: Path) -> str:
    return f"<redacted:{path.name}:{(_path_hash(path) or '')[:12]}>"


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


def _public_attrs(attrs: dict[str, Any]) -> dict[str, Any]:
    copied = dict(attrs)
    config_attrs = dict(copied.get("config_attrs") or {})
    config_attrs.pop("directory_root_raw", None)
    copied["config_attrs"] = config_attrs
    return copied

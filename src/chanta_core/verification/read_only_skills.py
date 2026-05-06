from __future__ import annotations

import platform
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from chanta_core.ocel.store import OCELStore
from chanta_core.verification.errors import VerificationError
from chanta_core.verification.models import VerificationResult
from chanta_core.verification.service import VerificationService


READ_ONLY_SKILL_STATUSES = {"passed", "failed", "inconclusive", "error", "skipped"}


@dataclass(frozen=True)
class ReadOnlyVerificationSkillSpec:
    skill_name: str
    description: str
    contract_type: str
    target_type: str
    evidence_kind_on_pass: str
    evidence_kind_on_fail: str
    read_only: bool = True
    skill_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.read_only is not True:
            raise VerificationError("Read-only verification skill specs must set read_only=True")

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "description": self.description,
            "contract_type": self.contract_type,
            "target_type": self.target_type,
            "evidence_kind_on_pass": self.evidence_kind_on_pass,
            "evidence_kind_on_fail": self.evidence_kind_on_fail,
            "read_only": self.read_only,
            "skill_attrs": self.skill_attrs,
        }


@dataclass(frozen=True)
class ReadOnlyVerificationSkillOutcome:
    skill_name: str
    passed: bool | None
    status: str
    evidence_kind: str
    evidence_content: str
    reason: str | None
    confidence: float | None
    outcome_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in READ_ONLY_SKILL_STATUSES:
            raise VerificationError(f"Unsupported read-only verification status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "passed": self.passed,
            "status": self.status,
            "evidence_kind": self.evidence_kind,
            "evidence_content": self.evidence_content,
            "reason": self.reason,
            "confidence": self.confidence,
            "outcome_attrs": self.outcome_attrs,
        }


class ReadOnlyVerificationSkillService:
    def __init__(
        self,
        *,
        verification_service: VerificationService,
        root: Path | str | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.verification_service = verification_service
        self.root = Path(root) if root is not None else Path(".")
        self.ocel_store = ocel_store
        self._specs = {spec.skill_name: spec for spec in _default_specs()}

    def list_skills(self) -> list[ReadOnlyVerificationSkillSpec]:
        return [self._specs[name] for name in sorted(self._specs)]

    def verify_file_exists(
        self,
        *,
        path: str,
        root: Path | str | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        skill_name = "verify_file_exists"
        candidate = self._path(path, root)
        exists = candidate.exists()
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=exists,
            status="passed" if exists else "failed",
            evidence_kind="file_exists" if exists else "file_missing",
            evidence_content=f"path={path}; exists={exists}",
            reason="path exists" if exists else "path is missing",
            confidence=1.0,
            outcome_attrs={"path": path, "absolute_observed": str(candidate), "exists": exists},
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="file",
            target_ref=path,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_path_type(
        self,
        *,
        path: str,
        expected_type: str,
        root: Path | str | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        if expected_type not in {"file", "directory", "any"}:
            raise VerificationError(f"Unsupported expected_type: {expected_type}")
        skill_name = "verify_path_type"
        candidate = self._path(path, root)
        exists = candidate.exists()
        is_file = candidate.is_file()
        is_dir = candidate.is_dir()
        passed = exists and (
            expected_type == "any"
            or (expected_type == "file" and is_file)
            or (expected_type == "directory" and is_dir)
        )
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=passed,
            status="passed" if passed else "failed",
            evidence_kind="file_exists" if passed else "observation",
            evidence_content=(
                f"path={path}; expected_type={expected_type}; exists={exists}; "
                f"is_file={is_file}; is_dir={is_dir}"
            ),
            reason="path type matched" if passed else "path type did not match",
            confidence=1.0,
            outcome_attrs={
                "path": path,
                "absolute_observed": str(candidate),
                "expected_type": expected_type,
                "exists": exists,
                "is_file": is_file,
                "is_dir": is_dir,
            },
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="file",
            target_ref=path,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_tool_available(
        self,
        *,
        tool_name: str,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        skill_name = "verify_tool_available"
        resolved = shutil.which(tool_name)
        found = resolved is not None
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=found,
            status="passed" if found else "failed",
            evidence_kind="tool_available" if found else "tool_unavailable",
            evidence_content=f"tool_name={tool_name}; available={found}; resolved_path={resolved}",
            reason="tool was found on PATH" if found else "tool was not found on PATH",
            confidence=1.0,
            outcome_attrs={"tool_name": tool_name, "resolved_path": resolved, "executed": False},
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="tool",
            target_ref=tool_name,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_runtime_python_info(
        self,
        *,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        skill_name = "verify_runtime_python_info"
        content = (
            f"python_version={sys.version}; "
            f"python_executable={sys.executable}; "
            f"platform={platform.platform()}"
        )
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=True,
            status="passed",
            evidence_kind="runtime_status",
            evidence_content=content,
            reason="runtime Python info observed",
            confidence=1.0,
            outcome_attrs={
                "python_version": sys.version,
                "python_executable": sys.executable,
                "platform": platform.platform(),
            },
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="runtime",
            target_ref="python",
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_ocel_object_type_exists(
        self,
        *,
        object_type: str,
        known_object_types: list[str] | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        skill_name = "verify_ocel_object_type_exists"
        exists, source = self._object_type_exists(object_type, known_object_types)
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=exists,
            status="passed" if exists else "failed",
            evidence_kind="ocel_object_exists" if exists else "observation",
            evidence_content=f"object_type={object_type}; exists={exists}; source={source}",
            reason="OCEL object type observed" if exists else "OCEL object type not observed",
            confidence=1.0,
            outcome_attrs={"object_type": object_type, "source": source},
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="ocel_object",
            target_ref=object_type,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_ocel_event_activity_exists(
        self,
        *,
        event_activity: str,
        known_event_activities: list[str] | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        skill_name = "verify_ocel_event_activity_exists"
        exists, source = self._event_activity_exists(event_activity, known_event_activities)
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name=skill_name,
            passed=exists,
            status="passed" if exists else "failed",
            evidence_kind="event_activity_exists" if exists else "observation",
            evidence_content=f"event_activity={event_activity}; exists={exists}; source={source}",
            reason="OCEL event activity observed" if exists else "OCEL event activity not observed",
            confidence=1.0,
            outcome_attrs={"event_activity": event_activity, "source": source},
        )
        return self._record_skill_result(
            skill_name=skill_name,
            target_type="other",
            target_ref=event_activity,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_materialized_view_warning(
        self,
        *,
        path: str,
        root: Path | str | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        text = self._path(path, root).read_text(encoding="utf-8")
        lowered = text.lower()
        required = [
            "generated materialized view",
            "canonical source: ocel",
            "not canonical",
            "edits",
            "do not",
        ]
        passed = all(item in lowered for item in required)
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name="verify_materialized_view_warning",
            passed=passed,
            status="passed" if passed else "failed",
            evidence_kind="observation",
            evidence_content=f"path={path}; warning_adequate={passed}",
            reason="materialized view warning is adequate" if passed else "materialized view warning is inadequate",
            confidence=0.9,
            outcome_attrs={"path": path, "required_markers": required},
        )
        return self._record_skill_result(
            skill_name="verify_materialized_view_warning",
            target_type="materialized_view",
            target_ref=path,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def verify_tool_registry_view_warning(
        self,
        *,
        path: str,
        root: Path | str | None = None,
        contract_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> VerificationResult:
        text = self._path(path, root).read_text(encoding="utf-8")
        lowered = text.lower()
        registry_warning = "not the canonical tool registry" in lowered or "not canonical runtime registry" in lowered
        policy_warning = "not permissionpolicy" in lowered or "not permission policy" in lowered
        no_enforcement_terms = ["grant", "deny", "allow", "ask", "block", "sand" + "box"]
        no_enforcement = all(term in lowered for term in no_enforcement_terms)
        future_boundary = "future permission" in lowered or "v0.12" in lowered or "future" in lowered
        passed = (registry_warning or policy_warning) and no_enforcement and future_boundary
        outcome = ReadOnlyVerificationSkillOutcome(
            skill_name="verify_tool_registry_view_warning",
            passed=passed,
            status="passed" if passed else "failed",
            evidence_kind="observation",
            evidence_content=f"path={path}; warning_adequate={passed}",
            reason="tool registry/policy warning is adequate" if passed else "tool registry/policy warning is inadequate",
            confidence=0.9,
            outcome_attrs={
                "path": path,
                "registry_warning": registry_warning,
                "policy_warning": policy_warning,
                "no_enforcement_terms_present": no_enforcement,
                "future_boundary": future_boundary,
            },
        )
        return self._record_skill_result(
            skill_name="verify_tool_registry_view_warning",
            target_type="materialized_view",
            target_ref=path,
            outcome=outcome,
            contract_id=contract_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )

    def run_skill(
        self,
        *,
        skill_name: str,
        kwargs: dict[str, Any],
    ) -> VerificationResult:
        dispatch: dict[str, Callable[..., VerificationResult]] = {
            "verify_file_exists": self.verify_file_exists,
            "verify_path_type": self.verify_path_type,
            "verify_tool_available": self.verify_tool_available,
            "verify_runtime_python_info": self.verify_runtime_python_info,
            "verify_ocel_object_type_exists": self.verify_ocel_object_type_exists,
            "verify_ocel_event_activity_exists": self.verify_ocel_event_activity_exists,
            "verify_materialized_view_warning": self.verify_materialized_view_warning,
            "verify_tool_registry_view_warning": self.verify_tool_registry_view_warning,
        }
        if skill_name not in dispatch:
            raise VerificationError(f"Unknown read-only verification skill: {skill_name}")
        return dispatch[skill_name](**kwargs)

    def _record_skill_result(
        self,
        *,
        skill_name: str,
        target_type: str,
        target_ref: str,
        outcome: ReadOnlyVerificationSkillOutcome,
        contract_id: str | None,
        session_id: str | None,
        turn_id: str | None,
        process_instance_id: str | None,
    ) -> VerificationResult:
        spec = self._specs[skill_name]
        resolved_contract_id = contract_id or self._register_default_contract(spec).contract_id
        target = self.verification_service.register_target(
            target_type=target_type,
            target_ref=target_ref,
            target_label=target_ref,
            target_attrs={
                "read_only_verification_skill": True,
                "skill_name": skill_name,
                **outcome.outcome_attrs,
            },
        )
        run = self.verification_service.start_run(
            contract_id=resolved_contract_id,
            target_ids=[target.target_id],
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            run_attrs={
                "read_only_verification_skill": True,
                "skill_name": skill_name,
                "read_only": True,
            },
        )
        evidence = self.verification_service.record_evidence(
            run_id=run.run_id,
            target_id=target.target_id,
            evidence_kind=outcome.evidence_kind,
            source_kind="read_only_skill",
            content=outcome.evidence_content,
            confidence=outcome.confidence,
            evidence_attrs={
                "read_only_verification_skill": True,
                "skill_name": skill_name,
                "outcome": outcome.to_dict(),
            },
        )
        result = self.verification_service.record_result(
            contract_id=resolved_contract_id,
            run_id=run.run_id,
            target_id=target.target_id,
            status=outcome.status,
            confidence=outcome.confidence,
            reason=outcome.reason,
            evidence_ids=[evidence.evidence_id],
            result_attrs={
                "read_only_verification_skill": True,
                "skill_name": skill_name,
                "outcome": outcome.to_dict(),
            },
        )
        if outcome.status == "error":
            self.verification_service.fail_run(run=run, error_message=outcome.reason or "read-only verification error")
        elif outcome.status == "skipped":
            self.verification_service.skip_run(run=run, reason=outcome.reason)
        else:
            self.verification_service.complete_run(run=run)
        return result

    def _register_default_contract(self, spec: ReadOnlyVerificationSkillSpec):
        return self.verification_service.register_contract(
            contract_name=_DEFAULT_CONTRACT_NAMES[spec.skill_name],
            contract_type=spec.contract_type,
            description=spec.description,
            subject_type=spec.target_type,
            required_evidence_kinds=[spec.evidence_kind_on_pass, spec.evidence_kind_on_fail],
            pass_criteria={"read_only_observation": True},
            fail_criteria={"read_only_observation": False},
            severity="low",
            contract_attrs={
                "read_only_verification_skill": True,
                "skill_name": spec.skill_name,
                "dedupe_lookup_available": False,
            },
        )

    def _path(self, path: str, root: Path | str | None) -> Path:
        candidate = Path(path)
        if candidate.is_absolute():
            return candidate
        root_path = Path(root) if root is not None else self.root
        return root_path / candidate

    def _object_type_exists(
        self,
        object_type: str,
        known_object_types: list[str] | None,
    ) -> tuple[bool, str]:
        if self.ocel_store is not None and self.ocel_store.db_path.exists():
            return bool(self.ocel_store.fetch_objects_by_type(object_type)), "ocel_store"
        return object_type in set(known_object_types or []), "known_object_types"

    def _event_activity_exists(
        self,
        event_activity: str,
        known_event_activities: list[str] | None,
    ) -> tuple[bool, str]:
        if self.ocel_store is not None and self.ocel_store.db_path.exists():
            activities = {event["event_activity"] for event in self.ocel_store.fetch_recent_events(500)}
            return event_activity in activities, "ocel_store"
        return event_activity in set(known_event_activities or []), "known_event_activities"


_DEFAULT_CONTRACT_NAMES = {
    "verify_file_exists": "File existence verification",
    "verify_path_type": "Path type verification",
    "verify_tool_available": "Tool availability verification",
    "verify_runtime_python_info": "Runtime Python info verification",
    "verify_ocel_object_type_exists": "OCEL object type existence verification",
    "verify_ocel_event_activity_exists": "OCEL event activity existence verification",
    "verify_materialized_view_warning": "Materialized view warning verification",
    "verify_tool_registry_view_warning": "Tool registry view warning verification",
}


def _default_specs() -> list[ReadOnlyVerificationSkillSpec]:
    return [
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_file_exists",
            description="Observe whether a path exists without opening or changing it.",
            contract_type="file_existence",
            target_type="file",
            evidence_kind_on_pass="file_exists",
            evidence_kind_on_fail="file_missing",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_path_type",
            description="Observe whether a path matches an expected type.",
            contract_type="file_existence",
            target_type="file",
            evidence_kind_on_pass="file_exists",
            evidence_kind_on_fail="observation",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_tool_available",
            description="Observe tool availability through PATH resolution without executing it.",
            contract_type="tool_availability",
            target_type="tool",
            evidence_kind_on_pass="tool_available",
            evidence_kind_on_fail="tool_unavailable",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_runtime_python_info",
            description="Observe Python runtime information without shell execution.",
            contract_type="runtime_status",
            target_type="runtime",
            evidence_kind_on_pass="runtime_status",
            evidence_kind_on_fail="runtime_status",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_ocel_object_type_exists",
            description="Observe whether an OCEL object type exists through a read-only query or fallback list.",
            contract_type="ocel_shape",
            target_type="ocel_object",
            evidence_kind_on_pass="ocel_object_exists",
            evidence_kind_on_fail="observation",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_ocel_event_activity_exists",
            description="Observe whether an OCEL event activity exists through a read-only query or fallback list.",
            contract_type="ocel_shape",
            target_type="other",
            evidence_kind_on_pass="event_activity_exists",
            evidence_kind_on_fail="observation",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_materialized_view_warning",
            description="Inspect generated Markdown view warning text without modifying the file.",
            contract_type="materialized_view_integrity",
            target_type="materialized_view",
            evidence_kind_on_pass="observation",
            evidence_kind_on_fail="observation",
            read_only=True,
        ),
        ReadOnlyVerificationSkillSpec(
            skill_name="verify_tool_registry_view_warning",
            description="Inspect tool registry or policy view warning text without modifying the file.",
            contract_type="tool_registry_integrity",
            target_type="materialized_view",
            evidence_kind_on_pass="observation",
            evidence_kind_on_fail="observation",
            read_only=True,
        ),
    ]

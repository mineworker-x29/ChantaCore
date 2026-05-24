from __future__ import annotations

import subprocess
import sys

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    CONTRACT_ONLY_FOLLOWUP_SKILL_IDS,
    PATCH_CANDIDATE_CREATE_SKILL_ID,
    REQUEST_CREATE_SKILL_ID,
    ModificationTargetResolver,
    PatchCandidate,
    PatchConstraintBuilder,
    PatchIntentClassifier,
    PatchPreliminaryRiskService,
    PatchScopeBuilder,
    SelfModificationNeedsMoreInputCandidate,
    SelfModificationNoActionCandidate,
    SelfModificationRegistryService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
)


def test_modification_request_and_patch_candidate_can_be_created() -> None:
    service = SelfModificationRequestCandidateService()
    result = service.create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )

    assert result.request.request_id.startswith("self_modification_request:")
    assert result.request.request_status == "candidate_created"
    assert result.patch_candidate is not None
    assert isinstance(result.patch_candidate, PatchCandidate)
    assert result.patch_candidate.candidate_id.startswith("patch_candidate:")
    assert result.patch_candidate.lifecycle_state == "candidate_created"
    assert result.patch_candidate.candidate_status == "candidate_only"
    assert result.patch_candidate.review_status == "pending_review"
    assert result.patch_candidate.target_refs[0].relative_path == "README.md"


def test_patch_candidate_safety_flags_remain_disabled() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    candidate = result.patch_candidate
    assert candidate is not None

    assert candidate.requires_diff_preview is True
    assert candidate.requires_static_safety_check is True
    assert candidate.requires_dry_run is True
    assert candidate.requires_human_review is True
    assert candidate.requires_apply_gate is True
    assert candidate.requires_rollback_plan is True
    assert candidate.requires_post_apply_verification is True
    assert candidate.diff_generated is False
    assert candidate.dry_run_checked is False
    assert candidate.review_approved is False
    assert candidate.apply_gate_opened is False
    assert candidate.applied is False
    assert candidate.file_write_enabled is False
    assert candidate.apply_patch_enabled is False
    assert candidate.materialized is False
    assert candidate.execution_enabled is False
    assert candidate.canonical_promotion_enabled is False
    assert candidate.promoted is False
    assert candidate.preliminary_risk.safe_to_generate_diff is False
    assert candidate.preliminary_risk.safe_to_apply is False


def test_missing_target_creates_needs_more_input_candidate() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=[])
    )

    assert result.patch_candidate is None
    assert isinstance(result.needs_more_input_candidate, SelfModificationNeedsMoreInputCandidate)
    assert result.needs_more_input_candidate.recommended_review_decision == "needs_more_input"
    assert result.needs_more_input_candidate.candidate_status == "candidate_only"
    assert result.needs_more_input_candidate.applied is False
    assert "target_path" in result.needs_more_input_candidate.missing_inputs


def test_forbidden_patch_type_creates_no_action_candidate() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(
            goal_text="delete generated output",
            target_paths=["README.md"],
            requested_patch_type="delete_file",
        )
    )

    assert result.patch_candidate is None
    assert isinstance(result.no_action_candidate, SelfModificationNoActionCandidate)
    assert result.no_action_candidate.recommended_review_decision == "no_action"
    assert result.no_action_candidate.candidate_status == "candidate_only"
    assert result.no_action_candidate.applied is False
    assert result.request.intent.forbidden_patch_type_detected is True


def test_scope_private_secret_and_generated_risks_are_detected() -> None:
    service = SelfModificationRequestCandidateService()

    too_many = service.create_request_and_candidate(
        SelfModificationRequestCreateRequest(
            goal_text="docs cleanup",
            target_paths=["README.md", "pyproject.toml"],
            max_target_files=1,
        )
    )
    assert too_many.request.scope.scope_status == "blocked"
    assert "target_scope_exceeds_limit" in too_many.request.scope.scope_risk_reasons

    private_result = service.create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["private/example.md"])
    )
    assert private_result.request.scope.scope_status == "blocked"
    assert "private_boundary_risk" in private_result.request.scope.scope_risk_reasons

    secret_result = service.create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="config cleanup", target_paths=[".env"])
    )
    assert secret_result.request.target_refs[0].secret_file_risk is True
    assert secret_result.request.scope.scope_status == "blocked"

    generated_result = service.create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="cleanup generated file", target_paths=["build/generated.py"])
    )
    assert generated_result.request.target_refs[0].generated_file_risk is True


def test_intent_scope_constraints_and_risk_services_are_deterministic() -> None:
    request = SelfModificationRequestCreateRequest(
        goal_text="fix test config docs cleanup refactor",
        target_paths=["README.md"],
    )
    targets = ModificationTargetResolver().resolve_targets(request)
    intent = PatchIntentClassifier().classify(request)
    scope = PatchScopeBuilder().build_scope(targets, request)
    constraints = PatchConstraintBuilder().build_constraints(request, targets)
    risk = PatchPreliminaryRiskService().assess(request, targets, intent, scope, constraints)

    assert intent.intent_type in {"docs", "test", "config", "bugfix", "refactor", "cleanup", "unknown"}
    assert intent.requires_diff_generation is True
    assert intent.requires_file_content is False
    assert scope.target_count == 1
    assert scope.scope_status in {"ok", "warning", "blocked", "needs_more_input"}
    constraint_types = {item.constraint_type for item in constraints}
    assert "no_file_write_in_v0_22_1" in constraint_types
    assert "no_apply_patch_in_v0_22_1" in constraint_types
    assert "diff_generation_deferred_to_v0_22_2" in constraint_types
    assert "requires_workspace_path_policy" in constraint_types
    assert "requires_diff_preview" in constraint_types
    assert "requires_static_safety_check" in constraint_types
    assert "requires_dry_run" in constraint_types
    assert "requires_human_review" in constraint_types
    assert "requires_apply_gate" in constraint_types
    assert "requires_rollback_plan" in constraint_types
    assert "requires_post_apply_verification" in constraint_types
    assert risk.requires_review is True
    assert risk.safe_to_generate_diff is False
    assert risk.safe_to_apply is False


def test_v0_22_1_skill_statuses_are_candidate_only_without_enabling_followups() -> None:
    contracts = SelfModificationRegistryService().list_skill_contracts()
    by_id = {item["skill_id"]: item for item in contracts}

    assert by_id[REQUEST_CREATE_SKILL_ID]["status"] == "implemented"
    assert by_id[REQUEST_CREATE_SKILL_ID]["candidate_only"] is True
    assert by_id[PATCH_CANDIDATE_CREATE_SKILL_ID]["status"] == "implemented"
    assert by_id[PATCH_CANDIDATE_CREATE_SKILL_ID]["candidate_only"] is True
    for skill_id in CONTRACT_ONLY_FOLLOWUP_SKILL_IDS:
        assert by_id[skill_id]["status"] == "contract_only"
        assert by_id[skill_id]["stub"] is True
        assert by_id[skill_id]["non_executable"] is True
        assert by_id[skill_id]["file_write_enabled"] is False
        assert by_id[skill_id]["apply_patch_enabled"] is False
        assert by_id[skill_id]["diff_generation_enabled"] is False


def test_ocel_pig_and_ocpx_visibility_exist() -> None:
    service = SelfModificationRequestCandidateService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "modification_request" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "patch_candidate" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "self_modification_patch_candidate_created" in SELF_MODIFICATION_OCEL_EVENT_TYPES
    assert "produces_patch_candidate" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.22.1"
    assert pig["subject"] == "modification_request_patch_candidate"
    assert pig["file_write_enabled"] is False
    assert pig["apply_patch_enabled"] is False
    assert pig["diff_generation_enabled"] is False
    assert pig["patch_apply_enabled"] is False
    assert pig["llm_patch_generation_enabled"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_request_patch_candidate_created"
    assert "SelfModificationRequestState" in ocpx["target_read_models"]
    assert "PatchCandidateState" in ocpx["target_read_models"]
    assert "PatchPreliminaryRiskState" in ocpx["target_read_models"]
    assert "PatchCandidateFindingState" in ocpx["target_read_models"]


def test_self_modification_request_candidate_cli_commands() -> None:
    commands = [
        ["request", "create", "--goal", "docs cleanup", "--target", "README.md"],
        ["candidate", "create", "--goal", "docs cleanup", "--target", "README.md"],
        ["candidate", "list"],
        ["candidate", "view", "--candidate-id", "patch_candidate:test"],
        ["request", "view", "--request-id", "self_modification_request:test"],
        ["candidate", "risks", "--candidate-id", "patch_candidate:test"],
        ["pig-report"],
        ["ocpx-projection"],
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "layer=self_modification_safety" in completed.stdout
        assert "file_write_enabled=false" in completed.stdout
        assert "apply_patch_enabled=false" in completed.stdout
        assert "No file mutation occurred." in completed.stdout
        assert "raw_file_content_printed=False" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout

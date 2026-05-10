from chanta_core.persona.personal_prompt_activation import (
    PersonalPromptActivationBlock,
    PersonalPromptActivationConfig,
    PersonalPromptActivationFinding,
    PersonalPromptActivationRequest,
    PersonalPromptActivationResult,
)


def test_personal_prompt_activation_models_to_dict() -> None:
    created_at = "2026-01-01T00:00:00Z"
    config = PersonalPromptActivationConfig(
        config_id="personal_prompt_activation_config:test",
        personal_directory_configured=True,
        selected_mode_name="public_safe_mode",
        selected_profile_name="public_safe_profile",
        runtime_kind="local_runtime",
        activation_source="test",
        max_chars=8000,
        require_conformance_pass=False,
        require_smoke_pass=False,
        private=True,
        status="active",
        created_at=created_at,
        config_attrs={"source_bodies_loaded": False},
    )
    request = PersonalPromptActivationRequest(
        request_id="personal_prompt_activation_request:test",
        config_id=config.config_id,
        session_id="session:test",
        turn_id="turn:test",
        selected_mode_name=config.selected_mode_name,
        selected_profile_name=config.selected_profile_name,
        runtime_kind=config.runtime_kind,
        requested_by="test",
        created_at=created_at,
    )
    block = PersonalPromptActivationBlock(
        block_id="personal_prompt_activation_block:test",
        request_id=request.request_id,
        block_type="personal_mode_loadout",
        title="Personal Mode Loadout",
        content="bounded prompt block",
        source_kind="personal_mode_loadout",
        source_ref="personal_mode_loadout:test",
        private=True,
        safe_for_prompt=True,
        total_chars=20,
        created_at=created_at,
    )
    finding = PersonalPromptActivationFinding(
        finding_id="personal_prompt_activation_finding:test",
        request_id=request.request_id,
        result_id=None,
        finding_type="missing_selected_mode",
        status="skipped",
        severity="medium",
        message="checked",
        subject_ref=None,
        created_at=created_at,
    )
    result = PersonalPromptActivationResult(
        result_id="personal_prompt_activation_result:test",
        request_id=request.request_id,
        status="attached",
        activation_scope="prompt_context_only",
        attached_block_ids=[block.block_id],
        total_chars=block.total_chars,
        truncated=False,
        denied=False,
        finding_ids=[finding.finding_id],
        created_at=created_at,
    )

    assert config.to_dict()["activation_source"] == "test"
    assert request.to_dict()["selected_mode_name"] == "public_safe_mode"
    assert block.to_dict()["safe_for_prompt"] is True
    assert finding.to_dict()["finding_type"] == "missing_selected_mode"
    assert result.to_dict()["activation_scope"] == "prompt_context_only"

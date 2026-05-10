from chanta_core.persona.history_adapter import (
    personal_prompt_activation_blocks_to_history_entries,
    personal_prompt_activation_findings_to_history_entries,
    personal_prompt_activation_results_to_history_entries,
)
from chanta_core.persona.personal_prompt_activation import (
    PersonalPromptActivationBlock,
    PersonalPromptActivationFinding,
    PersonalPromptActivationResult,
)


def test_personal_prompt_activation_history_entries() -> None:
    created_at = "2026-01-01T00:00:00Z"
    block = PersonalPromptActivationBlock(
        block_id="personal_prompt_activation_block:test",
        request_id="personal_prompt_activation_request:test",
        block_type="personal_mode_loadout",
        title="Personal Mode Loadout",
        content="bounded",
        source_kind="personal_mode_loadout",
        source_ref="personal_mode_loadout:test",
        private=True,
        safe_for_prompt=True,
        total_chars=7,
        created_at=created_at,
    )
    finding = PersonalPromptActivationFinding(
        finding_id="personal_prompt_activation_finding:test",
        request_id=block.request_id,
        result_id=None,
        finding_type="unsafe_overlay_projection",
        status="failed",
        severity="high",
        message="checked",
        subject_ref=None,
        created_at=created_at,
    )
    result = PersonalPromptActivationResult(
        result_id="personal_prompt_activation_result:test",
        request_id=block.request_id,
        status="denied",
        activation_scope="none",
        attached_block_ids=[],
        total_chars=0,
        truncated=False,
        denied=True,
        finding_ids=[finding.finding_id],
        created_at=created_at,
    )

    result_entry = personal_prompt_activation_results_to_history_entries([result])[0]
    block_entry = personal_prompt_activation_blocks_to_history_entries([block])[0]
    finding_entry = personal_prompt_activation_findings_to_history_entries([finding])[0]

    assert result_entry.source == "personal_prompt_activation"
    assert result_entry.priority == 90
    assert block_entry.priority == 60
    assert finding_entry.priority == 90

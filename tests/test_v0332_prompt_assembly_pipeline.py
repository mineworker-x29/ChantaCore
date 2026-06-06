import pytest

from chanta_core.agent_runtime import (
    PromptAssemblyBlockKind,
    PromptAssemblyBlockPlacement,
    PromptAssemblyBlockTrustLevel,
    PromptAssemblyFlagSet,
    PromptAssemblyInput,
    PromptAssemblyNoRuntimeGuarantee,
    PromptAssemblyOutput,
    PromptAssemblyOutputFormat,
    PromptAssemblyPlan,
    PromptAssemblyReadinessLevel,
    PromptAssemblyReport,
    PromptAssemblyRiskKind,
    PromptAssemblyRunPreview,
    PromptAssemblySourceKind,
    PromptAssemblySourceRef,
    PromptAssemblyStatus,
    PromptAssemblyValidationReport,
    PromptBoundaryBlock,
    PromptContextBlock,
    PromptInjectionRiskSignal,
    PromptReferenceContextBlock,
    PromptToolAvailabilityBlock,
    V0332ReadinessReport,
    assemble_prompt_from_blocks,
    build_agent_profile_runtime_flags,
    build_agent_runtime_loadout,
    build_agent_runtime_profile,
    build_prompt_assembly_flags,
    build_prompt_assembly_input,
    build_prompt_assembly_no_runtime_guarantee,
    build_prompt_assembly_plan,
    build_prompt_assembly_report,
    build_prompt_assembly_run_preview,
    build_prompt_assembly_source_ref,
    build_prompt_boundary_block,
    build_prompt_context_block,
    build_prompt_evidence_block,
    build_prompt_injection_risk_signal,
    build_prompt_output_contract_block,
    build_prompt_policy_block,
    build_prompt_profile_block,
    build_prompt_profile_block_from_runtime_profile,
    build_prompt_prohibited_action_block,
    build_prompt_reference_context_block,
    build_prompt_task_block,
    build_prompt_tool_availability_block,
    build_v0332_readiness_report,
    prompt_assembly_flags_preserve_runtime_false,
    prompt_output_is_not_model_invocation,
    prompt_reference_block_preserves_no_file_access,
    v0332_readiness_report_is_not_runtime_ready,
    validate_prompt_block_order,
)
from chanta_core.agent_runtime.prompt_assembly import (
    DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS,
    RUNTIME_FLAG_NAMES,
)


def test_prompt_assembly_taxonomies_and_flags_are_non_runtime():
    assert "runtime_boundary" in {item.value for item in PromptAssemblyBlockKind}
    assert "reference_context" in {item.value for item in PromptAssemblyBlockKind}
    assert "trusted_runtime_boundary" in {item.value for item in PromptAssemblyBlockTrustLevel}
    assert "untrusted_external_reference" in {item.value for item in PromptAssemblyBlockTrustLevel}
    assert "system_boundary_section" in {item.value for item in PromptAssemblyBlockPlacement}
    assert "excluded" in {item.value for item in PromptAssemblyBlockPlacement}
    assert "opencode_reference_context" in {item.value for item in PromptAssemblySourceKind}
    assert "hermes_reference_context" in {item.value for item in PromptAssemblySourceKind}
    assert "assembled" in {item.value for item in PromptAssemblyStatus}
    assert "prompt_payload_ready" in {item.value for item in PromptAssemblyReadinessLevel}
    assert "prompt_injection_risk" in {item.value for item in PromptAssemblyRiskKind}
    assert "message_list" in {item.value for item in PromptAssemblyOutputFormat}

    flags = build_prompt_assembly_flags(
        prompt_payload_constructed=True,
        ready_for_v0333_session_runtime=True,
        ready_for_v0336_agent_step_runner=True,
    )

    assert flags.prompt_payload_constructed is True
    assert flags.ready_for_v0333_session_runtime is True
    assert flags.ready_for_v0336_agent_step_runner is True
    assert prompt_assembly_flags_preserve_runtime_false(flags)

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            PromptAssemblyFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.2",
                **{flag_name: True},
            )


def test_source_refs_and_context_blocks_preserve_trust_boundaries():
    source_ref = build_prompt_assembly_source_ref(
        "source:task",
        PromptAssemblySourceKind.USER_TASK,
        "task:1",
        "In-memory user task summary.",
        trust_level=PromptAssemblyBlockTrustLevel.USER_SUPPLIED,
    )
    boundary_block = build_prompt_context_block(
        "block:boundary",
        PromptAssemblyBlockKind.RUNTIME_BOUNDARY,
        "Boundary",
        "No model invocation, no tool execution.",
        trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY,
        placement=PromptAssemblyBlockPlacement.SYSTEM_BOUNDARY_SECTION,
        source_refs=[source_ref],
        is_instructional=True,
    )
    reference_block = build_prompt_context_block(
        "block:reference",
        PromptAssemblyBlockKind.REFERENCE_CONTEXT,
        "OpenCode/Hermes Reference Notes",
        "references/OpenCode and references/Hermes are path refs only.",
        trust_level=PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE,
        placement=PromptAssemblyBlockPlacement.REFERENCE_CONTEXT_SECTION,
        risk_kinds=[PromptAssemblyRiskKind.UNTRUSTED_REFERENCE_INSTRUCTION_RISK],
        is_untrusted=True,
    )

    assert source_ref.fetch is False
    assert source_ref.file_read is False
    assert source_ref.execution is False
    assert boundary_block.execution is False
    assert reference_block.execution is False
    assert reference_block.is_instructional is False

    with pytest.raises(ValueError):
        PromptAssemblySourceRef(
            source_ref_id="source:bad",
            source_kind=PromptAssemblySourceKind.REFERENCE_CONTEXT,
            source_id="references/OpenCode",
            source_summary="bad",
            metadata={"file_read": True},
        )
    with pytest.raises(ValueError):
        PromptContextBlock(
            block_id="block:bad:instructional",
            block_kind=PromptAssemblyBlockKind.REFERENCE_CONTEXT,
            trust_level=PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE,
            placement=PromptAssemblyBlockPlacement.REFERENCE_CONTEXT_SECTION,
            title="bad",
            content="bad",
            is_instructional=True,
        )
    with pytest.raises(ValueError):
        PromptContextBlock(
            block_id="block:bad:boundary",
            block_kind=PromptAssemblyBlockKind.REFERENCE_CONTEXT,
            trust_level=PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE,
            placement=PromptAssemblyBlockPlacement.SYSTEM_BOUNDARY_SECTION,
            title="bad",
            content="bad",
        )
    with pytest.raises(ValueError):
        PromptContextBlock(
            block_id="block:bad:excluded",
            block_kind=PromptAssemblyBlockKind.TASK,
            trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_INTERNAL,
            placement=PromptAssemblyBlockPlacement.EXCLUDED,
            title="bad",
            content="bad",
            excluded=True,
        )
    with pytest.raises(ValueError):
        PromptContextBlock(
            block_id="block:bad:boundary-trust",
            block_kind=PromptAssemblyBlockKind.RUNTIME_BOUNDARY,
            trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_INTERNAL,
            placement=PromptAssemblyBlockPlacement.SYSTEM_BOUNDARY_SECTION,
            title="bad",
            content="bad",
        )


def test_specialized_prompt_blocks_are_contract_only():
    source_ref = build_prompt_assembly_source_ref("source:specialized")
    boundary = build_prompt_boundary_block(
        "boundary:1",
        non_negotiable_rules=["PromptAssemblyOutput is not a model call."],
        source_refs=[source_ref],
    )
    profile = build_prompt_profile_block("profile:1", source_refs=[source_ref])
    policy = build_prompt_policy_block("policy:1", source_refs=[source_ref])
    task = build_prompt_task_block("task:1", "Assemble v0.33.2 prompt payload.", source_refs=[source_ref])
    reference = build_prompt_reference_context_block("reference:1", source_refs=[source_ref])
    tools = build_prompt_tool_availability_block(
        "tools:1",
        unavailable_tool_names=["provider", "shell"],
        future_tool_names=["safe_readonly_tool_registry:v0.33.4"],
        source_refs=[source_ref],
    )
    evidence = build_prompt_evidence_block("evidence:1", evidence_refs=["tests:test_v0332"], source_refs=[source_ref])
    output_contract = build_prompt_output_contract_block("output:1", required_sections=["summary"])
    prohibited = build_prompt_prohibited_action_block("prohibited:1")

    assert set(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS).issubset(set(boundary.prohibited_runtime_actions))
    assert boundary.runtime_enforcement is False
    assert profile.active_session is False
    assert policy.active_policy_enforcement is False
    assert task.command_execution is False
    assert reference.opencode_reference_note is not None
    assert reference.hermes_reference_note is not None
    assert prompt_reference_block_preserves_no_file_access(reference)
    assert tools.ready_for_tool_execution is False
    assert tools.tool_execution is False
    assert evidence.runtime_trust is False
    assert output_contract.implementation is False
    assert set(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS).issubset(set(prohibited.prohibited_actions))

    with pytest.raises(ValueError):
        PromptBoundaryBlock(
            boundary_block_id="boundary:bad",
            runtime_boundary_summary="bad",
            permission_gate_summary="bad",
            prohibited_runtime_actions=["model invocation"],
        )
    with pytest.raises(ValueError):
        PromptReferenceContextBlock(
            reference_context_block_id="reference:bad",
            reference_summary="bad",
            trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY,
        )
    with pytest.raises(ValueError):
        PromptToolAvailabilityBlock(
            tool_block_id="tools:bad",
            summary="bad",
            ready_for_tool_execution=True,
        )


def test_input_plan_validation_output_and_report_are_not_invocation():
    source_ref = build_prompt_assembly_source_ref("source:assembly")
    assembly_input = build_prompt_assembly_input(
        "input:1",
        "Assemble bounded prompt.",
        source_refs=[source_ref],
        token_budget_limit=2048,
    )
    plan = build_prompt_assembly_plan("plan:1", assembly_input.assembly_input_id)
    boundary_block = build_prompt_context_block(
        "block:boundary",
        PromptAssemblyBlockKind.RUNTIME_BOUNDARY,
        "Boundary",
        "No model invocation.",
        trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_RUNTIME_BOUNDARY,
        placement=PromptAssemblyBlockPlacement.SYSTEM_BOUNDARY_SECTION,
        is_instructional=True,
    )
    task_block = build_prompt_context_block(
        "block:task",
        PromptAssemblyBlockKind.TASK,
        "Task",
        "Create PromptAssemblyOutput.",
        trust_level=PromptAssemblyBlockTrustLevel.USER_SUPPLIED,
        placement=PromptAssemblyBlockPlacement.TASK_SECTION,
    )
    validation = validate_prompt_block_order([boundary_block, task_block], assembly_input.assembly_input_id)
    risk = build_prompt_injection_risk_signal("risk:1", affected_block_ids=[task_block.block_id])
    output = assemble_prompt_from_blocks(
        assembly_input,
        [boundary_block, task_block],
        output_format=PromptAssemblyOutputFormat.MESSAGE_LIST,
    )
    report = build_prompt_assembly_report(
        "report:1",
        assembly_input.assembly_input_id,
        prompt_output_id=output.prompt_output_id,
        validation_report_id=output.validation_report_id,
        assembled_block_count=len(output.ordered_blocks),
        risk_signal_count=0,
        ready_for_v0333_session_runtime=True,
        ready_for_v0336_agent_step_runner=True,
    )

    assert set(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS).issubset(set(assembly_input.prohibited_runtime_actions))
    assert assembly_input.model_invocation_request is False
    assert plan.ready_for_prompt_payload_construction is True
    assert plan.ready_for_model_invocation is False
    assert plan.model_invocation is False
    assert validation.validation_passed is True
    assert validation.ready_for_model_invocation is False
    assert validation.runtime_enforcement is False
    assert risk.advisory_only is True
    assert prompt_output_is_not_model_invocation(output)
    assert output.assembled_prompt_text is not None
    assert output.assembled_messages
    assert report.ready_for_model_invocation is False
    assert report.model_invocation is False

    with pytest.raises(ValueError):
        PromptAssemblyInput(
            assembly_input_id="input:bad",
            source_version="v0.33.2",
            runtime_profile_id=None,
            runtime_boundary_id=None,
            task_summary="bad",
            token_budget_limit=0,
        )
    with pytest.raises(ValueError):
        PromptAssemblyPlan(
            plan_id="plan:bad",
            assembly_input_id=assembly_input.assembly_input_id,
            ready_for_model_invocation=True,
        )
    with pytest.raises(ValueError):
        PromptAssemblyValidationReport(
            validation_report_id="validation:bad",
            assembly_input_id=assembly_input.assembly_input_id,
            blocked_block_ids=["blocked"],
            validation_passed=True,
        )
    with pytest.raises(ValueError):
        PromptAssemblyOutput(
            prompt_output_id="output:bad",
            assembly_input_id=assembly_input.assembly_input_id,
            output_format=PromptAssemblyOutputFormat.MESSAGE_LIST,
            ready_for_model_invocation=True,
        )
    with pytest.raises(ValueError):
        PromptAssemblyReport(
            report_id="report:bad",
            version="v0.33.2",
            assembly_input_id=assembly_input.assembly_input_id,
            prompt_output_id=None,
            validation_report_id=None,
            status=PromptAssemblyStatus.BLOCKED,
            readiness_level=PromptAssemblyReadinessLevel.BLOCKED,
            summary="bad",
            ready_for_v0333_session_runtime=True,
            blocked_items=["blocked"],
        )


def test_preview_guarantee_readiness_and_fake_profile_prompt_assembly_are_conservative():
    preview = build_prompt_assembly_run_preview("preview:1")
    guarantee = build_prompt_assembly_no_runtime_guarantee("guarantee:1")
    readiness = build_v0332_readiness_report(
        "readiness:1",
        ready_for_v0333_session_runtime=True,
        ready_for_v0336_agent_step_runner=True,
        completed_items=["prompt assembly contract"],
    )
    runtime_profile = build_agent_runtime_profile(
        "profile:fake",
        build_agent_runtime_loadout("loadout:fake"),
        build_agent_profile_runtime_flags(ready_for_v0332_prompt_assembly=True),
    )
    source_ref = build_prompt_assembly_source_ref(
        "source:fake-profile",
        PromptAssemblySourceKind.AGENT_RUNTIME_PROFILE,
        runtime_profile.runtime_profile_id,
        "Fake in-memory AgentRuntimeProfile.",
        trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_PROFILE,
    )
    profile_block = build_prompt_profile_block_from_runtime_profile(runtime_profile, source_refs=[source_ref])
    profile_context_block = build_prompt_context_block(
        "block:profile",
        PromptAssemblyBlockKind.PROFILE,
        profile_block.profile_name,
        profile_block.constraints_summary,
        trust_level=PromptAssemblyBlockTrustLevel.TRUSTED_PROFILE,
        placement=PromptAssemblyBlockPlacement.PROFILE_SECTION,
    )
    reference_context_block = build_prompt_context_block(
        "block:reference",
        PromptAssemblyBlockKind.REFERENCE_CONTEXT,
        "Reference Context",
        "references/OpenCode and references/Hermes are read-only design/reference context only.",
        trust_level=PromptAssemblyBlockTrustLevel.UNTRUSTED_EXTERNAL_REFERENCE,
        placement=PromptAssemblyBlockPlacement.REFERENCE_CONTEXT_SECTION,
        is_untrusted=True,
    )
    assembly_input = build_prompt_assembly_input(
        "input:fake",
        "Assemble prompt with fake profile and reference path refs.",
        runtime_profile_id=runtime_profile.runtime_profile_id,
        source_refs=[source_ref],
    )
    output = assemble_prompt_from_blocks(assembly_input, [profile_context_block, reference_context_block])

    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert preview.execution is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0332_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_PROMPT_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))
    assert prompt_output_is_not_model_invocation(output)
    assert "references/OpenCode" in output.assembled_prompt_text
    assert "references/Hermes" in output.assembled_prompt_text

    with pytest.raises(ValueError):
        PromptAssemblyRunPreview(
            run_preview_id="preview:bad",
            no_model_invocation_guarantee=False,
        )
    with pytest.raises(ValueError):
        PromptAssemblyNoRuntimeGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.2",
            no_reference_file_access=False,
        )
    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0332ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.2",
                **{flag_name: True},
            )

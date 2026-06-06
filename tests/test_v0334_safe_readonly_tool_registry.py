import pytest

from chanta_core.agent_runtime import (
    ReadOnlyToolBlockedAction,
    ReadOnlyToolBlockReasonKind,
    ReadOnlyToolCallProposal,
    ReadOnlyToolCapabilityKind,
    ReadOnlyToolDescriptor,
    ReadOnlyToolExecutionPosture,
    ReadOnlyToolInputSchema,
    ReadOnlyToolKind,
    ReadOnlyToolOutputSchema,
    ReadOnlyToolPermissionDecision,
    ReadOnlyToolPermissionDecisionKind,
    ReadOnlyToolRegistry,
    ReadOnlyToolRegistryFlagSet,
    ReadOnlyToolRegistryNoExecutionGuarantee,
    ReadOnlyToolRegistryReport,
    ReadOnlyToolRegistryRunPreview,
    ReadOnlyToolRegistryStatus,
    ReadOnlyToolRegistryValidationReport,
    ReadOnlyToolSafetyLevel,
    ReadOnlyToolSafetyPolicy,
    ReadOnlyToolSourceKind,
    ReadOnlyToolSourceRef,
    ReadOnlyToolSurfaceKind,
    V0334ReadinessReport,
    build_readonly_tool_blocked_action,
    build_readonly_tool_call_proposal,
    build_readonly_tool_descriptor,
    build_readonly_tool_input_schema,
    build_readonly_tool_output_schema,
    build_readonly_tool_permission_decision,
    build_readonly_tool_registry,
    build_readonly_tool_registry_flags,
    build_readonly_tool_registry_no_execution_guarantee,
    build_readonly_tool_registry_report,
    build_readonly_tool_registry_run_preview,
    build_readonly_tool_safety_policy,
    build_readonly_tool_source_ref,
    build_v0334_readiness_report,
    default_safe_readonly_tool_descriptors,
    evaluate_readonly_tool_call_proposal,
    readonly_tool_decision_is_not_invocation,
    readonly_tool_descriptor_is_not_executable,
    readonly_tool_registry_flags_preserve_runtime_false,
    readonly_tool_registry_is_not_runtime_registry,
    v0334_readiness_report_is_not_runtime_ready,
    validate_readonly_tool_descriptor,
    validate_readonly_tool_registry,
)
from chanta_core.agent_runtime.readonly_tools import (
    DEFAULT_PROHIBITED_FILE_PATTERNS,
    DEFAULT_TOOL_PROHIBITED_ACTIONS,
    RUNTIME_FLAG_NAMES,
)


def test_readonly_tool_taxonomies_and_flags_are_non_runtime():
    assert "inspect_project_tree_readonly" in {item.value for item in ReadOnlyToolKind}
    assert "read_text_file_safe" in {item.value for item in ReadOnlyToolKind}
    assert "describe_registry" in {item.value for item in ReadOnlyToolCapabilityKind}
    assert "prohibited_secret_file" in {item.value for item in ReadOnlyToolSurfaceKind}
    assert "safe_readonly_future_gate" in {item.value for item in ReadOnlyToolSafetyLevel}
    assert "registry_ready_with_gaps" in {item.value for item in ReadOnlyToolRegistryStatus}
    assert "allow_future_readonly_execution" in {item.value for item in ReadOnlyToolPermissionDecisionKind}
    assert "workspace_inspection_not_enabled" in {item.value for item in ReadOnlyToolBlockReasonKind}
    assert "opencode_reference_context_ref" in {item.value for item in ReadOnlyToolSourceKind}
    assert "no_execution" in {item.value for item in ReadOnlyToolExecutionPosture}

    flags = build_readonly_tool_registry_flags(
        registry_metadata_constructed=True,
        descriptor_validation_available=True,
        call_proposal_validation_available=True,
        ready_for_v0335_workspace_inspection=True,
        ready_for_v0336_agent_step_runner=True,
    )

    assert flags.registry_metadata_constructed is True
    assert flags.descriptor_validation_available is True
    assert flags.call_proposal_validation_available is True
    assert flags.ready_for_v0335_workspace_inspection is True
    assert flags.ready_for_v0336_agent_step_runner is True
    assert readonly_tool_registry_flags_preserve_runtime_false(flags)

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            ReadOnlyToolRegistryFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.4",
                **{flag_name: True},
            )


def test_source_schema_policy_and_descriptor_are_non_executable():
    source = build_readonly_tool_source_ref(
        "source:descriptor",
        ReadOnlyToolSourceKind.MANUAL_TOOL_DESCRIPTOR,
        "descriptor:manual",
        "In-memory descriptor metadata.",
    )
    input_schema = build_readonly_tool_input_schema(
        "schema:input",
        ReadOnlyToolKind.INSPECT_PROJECT_TREE_READONLY,
        required_fields=["path_ref"],
        max_path_depth=3,
        max_result_items=50,
    )
    output_schema = build_readonly_tool_output_schema(
        "schema:output",
        ReadOnlyToolKind.INSPECT_PROJECT_TREE_READONLY,
        output_fields=["items"],
        redacted_fields=["path"],
        forbidden_fields=["raw_content"],
    )
    policy = build_readonly_tool_safety_policy(
        "policy:tree",
        ReadOnlyToolKind.INSPECT_PROJECT_TREE_READONLY,
        safety_level=ReadOnlyToolSafetyLevel.SAFE_METADATA_ONLY,
        allowed_surfaces=[ReadOnlyToolSurfaceKind.PROJECT_TREE_METADATA],
    )
    descriptor = build_readonly_tool_descriptor(
        "descriptor:tree",
        "inspect_project_tree_readonly",
        ReadOnlyToolKind.INSPECT_PROJECT_TREE_READONLY,
        capability_kinds=[ReadOnlyToolCapabilityKind.INSPECT_TREE],
        surface_kinds=[ReadOnlyToolSurfaceKind.PROJECT_TREE_METADATA],
        input_schema=input_schema,
        output_schema=output_schema,
        safety_policy=policy,
        source_refs=[source],
        enabled_in_registry=True,
    )

    assert source.fetch is False
    assert source.file_read is False
    assert source.execution is False
    assert input_schema.input_execution is False
    assert set(DEFAULT_PROHIBITED_FILE_PATTERNS).issubset(set(input_schema.prohibited_patterns))
    assert output_schema.raw_output_allowed is False
    assert output_schema.output_persistence is False
    assert policy.allow_workspace_read is False
    assert policy.allow_reference_read is False
    assert policy.allow_secret_read is False
    assert policy.allow_network is False
    assert policy.allow_command is False
    assert policy.allow_write is False
    assert policy.requires_permission_gate is True
    assert policy.execution is False
    assert readonly_tool_descriptor_is_not_executable(descriptor)
    assert descriptor.enabled_in_registry is True

    with pytest.raises(ValueError):
        ReadOnlyToolSourceRef(
            source_ref_id="source:bad",
            source_kind=ReadOnlyToolSourceKind.REFERENCE_CONTEXT_REF,
            source_id="references/OpenCode",
            source_summary="bad",
            metadata={"file_read": True},
        )
    with pytest.raises(ValueError):
        ReadOnlyToolInputSchema(
            input_schema_id="schema:bad",
            tool_kind=ReadOnlyToolKind.READ_TEXT_FILE_SAFE,
            prohibited_patterns=["*.tmp"],
        )
    with pytest.raises(ValueError):
        ReadOnlyToolOutputSchema(
            output_schema_id="schema:bad:output",
            tool_kind=ReadOnlyToolKind.READ_TEXT_FILE_SAFE,
            raw_output_allowed=True,
        )
    for flag_name in (
        "allow_workspace_read",
        "allow_reference_read",
        "allow_secret_read",
        "allow_binary_read",
        "allow_network",
        "allow_command",
        "allow_write",
        "allow_registry_mutation",
        "allow_memory_mutation",
    ):
        with pytest.raises(ValueError):
            ReadOnlyToolSafetyPolicy(
                safety_policy_id=f"policy:bad:{flag_name}",
                tool_kind=ReadOnlyToolKind.READ_TEXT_FILE_SAFE,
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        ReadOnlyToolDescriptor(
            tool_descriptor_id="descriptor:bad",
            tool_name="bad",
            tool_kind=ReadOnlyToolKind.TEST_READONLY_TOOL,
            capability_kinds=[ReadOnlyToolCapabilityKind.INSPECT_METADATA],
            surface_kinds=[ReadOnlyToolSurfaceKind.REGISTRY_METADATA],
            input_schema=build_readonly_tool_input_schema("schema:bad:input"),
            output_schema=build_readonly_tool_output_schema("schema:bad:out"),
            safety_policy=build_readonly_tool_safety_policy("policy:bad"),
            executable_in_v0334=True,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolDescriptor(
            tool_descriptor_id="descriptor:bad:surface",
            tool_name="bad_surface",
            tool_kind=ReadOnlyToolKind.TEST_READONLY_TOOL,
            capability_kinds=[ReadOnlyToolCapabilityKind.INSPECT_METADATA],
            surface_kinds=[ReadOnlyToolSurfaceKind.PROHIBITED_COMMAND],
            input_schema=build_readonly_tool_input_schema("schema:bad:surface:input"),
            output_schema=build_readonly_tool_output_schema("schema:bad:surface:out"),
            safety_policy=build_readonly_tool_safety_policy("policy:bad:surface"),
        )


def test_registry_proposal_decision_and_blocked_action_are_not_invocation():
    descriptors = default_safe_readonly_tool_descriptors()
    registry = build_readonly_tool_registry(
        "registry:1",
        descriptors=descriptors,
        ready_for_v0335_workspace_inspection=True,
        ready_for_v0336_agent_step_runner=True,
    )
    proposal = build_readonly_tool_call_proposal(
        "proposal:registry",
        "describe_registry",
        requested_tool_kind=ReadOnlyToolKind.TEST_READONLY_TOOL,
        requested_capability=ReadOnlyToolCapabilityKind.DESCRIBE_REGISTRY,
        requested_surface=ReadOnlyToolSurfaceKind.REGISTRY_METADATA,
    )
    decision = evaluate_readonly_tool_call_proposal(registry, proposal)
    unknown = build_readonly_tool_call_proposal(
        "proposal:unknown",
        "unknown_tool",
        requested_tool_kind=ReadOnlyToolKind.UNKNOWN,
        requested_capability=ReadOnlyToolCapabilityKind.UNKNOWN,
        requested_surface=ReadOnlyToolSurfaceKind.REGISTRY_METADATA,
    )
    unknown_decision = evaluate_readonly_tool_call_proposal(registry, unknown)
    blocked = build_readonly_tool_call_proposal(
        "proposal:blocked",
        "describe_registry",
        requested_tool_kind=ReadOnlyToolKind.TEST_READONLY_TOOL,
        requested_capability=ReadOnlyToolCapabilityKind.INSPECT_METADATA,
        requested_surface=ReadOnlyToolSurfaceKind.PROHIBITED_COMMAND,
    )
    blocked_decision = evaluate_readonly_tool_call_proposal(registry, blocked)
    blocked_action = build_readonly_tool_blocked_action(
        "blocked:1",
        proposal_id=blocked.proposal_id,
        decision_id=blocked_decision.decision_id,
        tool_name=blocked.requested_tool_name,
        block_reasons=[ReadOnlyToolBlockReasonKind.COMMAND_EXECUTION_RISK],
        risk_surfaces=[ReadOnlyToolSurfaceKind.PROHIBITED_COMMAND],
    )

    assert all(readonly_tool_descriptor_is_not_executable(descriptor) for descriptor in descriptors)
    assert readonly_tool_registry_is_not_runtime_registry(registry)
    assert registry.ready_for_v0335_workspace_inspection is True
    assert proposal.ready_for_tool_execution is False
    assert proposal.invocation is False
    assert decision.decision_kind == ReadOnlyToolPermissionDecisionKind.ALLOW_REGISTRY_METADATA_ONLY
    assert decision.allowed_only_for_registry_metadata is True
    assert readonly_tool_decision_is_not_invocation(decision)
    assert unknown_decision.decision_kind == ReadOnlyToolPermissionDecisionKind.BLOCK
    assert ReadOnlyToolBlockReasonKind.TOOL_NOT_REGISTERED in unknown_decision.block_reasons
    assert blocked_decision.decision_kind == ReadOnlyToolPermissionDecisionKind.BLOCK
    assert ReadOnlyToolBlockReasonKind.COMMAND_EXECUTION_RISK in blocked_decision.block_reasons
    assert blocked_action.safe_outcome is True

    with pytest.raises(ValueError):
        ReadOnlyToolCallProposal(
            proposal_id="proposal:bad",
            requested_tool_name="bad",
            requested_tool_kind=ReadOnlyToolKind.TEST_READONLY_TOOL,
            requested_capability=ReadOnlyToolCapabilityKind.INSPECT_METADATA,
            requested_surface=ReadOnlyToolSurfaceKind.REGISTRY_METADATA,
            ready_for_tool_execution=True,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolPermissionDecision(
            decision_id="decision:bad",
            proposal_id=proposal.proposal_id,
            requested_tool_name=proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.ALLOW_FUTURE_READONLY_EXECUTION,
            reason="bad",
            execution_allowed=True,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolPermissionDecision(
            decision_id="decision:bad:side",
            proposal_id=proposal.proposal_id,
            requested_tool_name=proposal.requested_tool_name,
            decision_kind=ReadOnlyToolPermissionDecisionKind.ALLOW_FUTURE_READONLY_EXECUTION,
            reason="bad",
            runtime_side_effect_allowed=True,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolRegistry(
            registry_id="registry:bad",
            version="v0.33.4",
            status=ReadOnlyToolRegistryStatus.REGISTRY_READY,
            registry_flags=build_readonly_tool_registry_flags(),
            ready_for_tool_execution=True,
        )


def test_validation_reports_preview_guarantee_and_readiness_are_non_runtime():
    descriptors = default_safe_readonly_tool_descriptors()
    registry = build_readonly_tool_registry("registry:validation", descriptors=descriptors)
    descriptor_report = validate_readonly_tool_descriptor(descriptors[0])
    registry_report = validate_readonly_tool_registry(registry)
    validation_report = ReadOnlyToolRegistryValidationReport(
        validation_report_id="validation:blocked",
        invalid_descriptor_ids=["descriptor:invalid"],
        validation_passed=False,
        summary="Blocked descriptors prevent validation pass.",
    )
    report = build_readonly_tool_registry_report(
        "report:1",
        registry_id=registry.registry_id,
        validation_report_id=registry_report.validation_report_id,
        descriptor_count=len(descriptors),
        enabled_descriptor_count=len(registry.enabled_tool_names),
        ready_for_v0335_workspace_inspection=True,
        ready_for_v0336_agent_step_runner=True,
    )
    preview = build_readonly_tool_registry_run_preview("preview:1", registry_id=registry.registry_id)
    guarantee = build_readonly_tool_registry_no_execution_guarantee("guarantee:1")
    readiness = build_v0334_readiness_report(
        "readiness:1",
        registry_id=registry.registry_id,
        registry_report_id=report.report_id,
        validation_report_id=registry_report.validation_report_id,
        ready_for_v0335_workspace_inspection=True,
        ready_for_v0336_agent_step_runner=True,
        completed_items=["read-only tool registry contract"],
    )

    assert descriptor_report.validation_passed is True
    assert registry_report.validation_passed is True
    assert validation_report.ready_for_tool_execution is False
    assert validation_report.runtime_certification is False
    assert report.ready_for_tool_execution is False
    assert report.tool_execution is False
    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert preview.execution is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0334_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_TOOL_PROHIBITED_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        ReadOnlyToolRegistryValidationReport(
            validation_report_id="validation:bad",
            invalid_descriptor_ids=["invalid"],
            validation_passed=True,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolRegistryReport(
            report_id="report:bad",
            version="v0.33.4",
            registry_id=None,
            validation_report_id=None,
            status=ReadOnlyToolRegistryStatus.BLOCKED,
            summary="bad",
            ready_for_v0335_workspace_inspection=True,
            blocked_items=["blocked"],
        )
    with pytest.raises(ValueError):
        ReadOnlyToolRegistryRunPreview(
            run_preview_id="preview:bad",
            no_file_read_guarantee=False,
        )
    with pytest.raises(ValueError):
        ReadOnlyToolRegistryNoExecutionGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.4",
            no_reference_file_access=False,
        )
    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0334ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.4",
                **{flag_name: True},
            )

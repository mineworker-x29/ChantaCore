from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from chanta_core.execution.audit import ExecutionAuditService
from chanta_core.execution.promotion import (
    ExecutionResultPromotionService,
    artifact_ref_from_dict,
    candidate_from_dict,
    envelope_from_dict,
    outcome_summary_from_dict,
    output_snapshot_from_dict,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.observation_digest import (
    DigestionService,
    ObservationDigestionEcosystemConsolidationService,
    ObservationService,
    candidate_from_dict,
    fingerprint_from_dict,
    inference_from_dict,
    observed_run_from_dict,
    static_profile_from_dict,
)
from chanta_core.observation import AgentObservationSpineService, CrossHarnessTraceAdapterService
from chanta_core.observation_digest.ids import new_agent_observation_batch_id
from chanta_core.digestion import (
    ExternalSkillStaticDigestionService,
    ObservationToDigestionAdapterBuilderService,
    behavior_inference_v2_from_dict,
)
from chanta_core.workspace import resolve_workspace_path
from chanta_core.persona.personal_runtime_surface import PersonalRuntimeSurfaceService
from chanta_core.runtime.workbench import PersonalRuntimeWorkbenchService
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService
from chanta_core.skills.proposal import SkillProposalRouterService
from chanta_core.skills.proposal_review import (
    SkillProposalReviewService,
    normalize_review_decision,
    proposal_from_json,
)
from chanta_core.skills.onboarding import (
    DEFAULT_READ_ONLY_CANDIDATE_SKILL_IDS,
    InternalSkillOnboardingService,
    descriptor_from_json,
)
from chanta_core.skills.reviewed_execution_bridge import (
    ReviewedExecutionBridgeService,
    load_bridge_inputs_from_json,
    proposal_from_dict as bridge_proposal_from_dict,
    review_decision_from_dict,
    review_result_from_dict,
)
from chanta_core.skills.registry_view import SkillRegistryViewService
from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService
from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService
from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessConformanceService,
    SelfAwarenessConsolidationService,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfAwarenessWorkbenchRequest,
    SelfAwarenessWorkbenchService,
    SelfDirectedIntentionRequest,
    SelfWorkspacePathPolicyService,
)
from chanta_core.deep_self_introspection import (
    DeepSelfIntrospectionConformanceService,
    DeepSelfIntrospectionRegistryService,
    DeepSelfIntrospectionReportService,
    SelfCapabilityRegistryAwarenessService,
    SelfCapabilityRegistryViewRequest,
)
from chanta_core.runtime.chat_service import ChatService
from chanta_core.settings.app_settings import load_app_settings
from chanta_core.workspace.summary import (
    WorkspaceReadSummarizationService,
    summarize_file_via_workspace_read,
    summary_result_from_dict,
)


EMPTY_MODEL_RESPONSE_MESSAGE = (
    "[empty model response: the configured LLM returned no assistant content]"
)
LLM_PROVIDER_UNAVAILABLE_MESSAGE = (
    "[LLM provider unavailable: no model is loaded. Load a model in the local "
    "provider, then retry.]"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chanta-cli",
        description="CLI for the ChantaCore trace-aware local runtime.",
    )
    subparsers = parser.add_subparsers(dest="command")

    ask_parser = subparsers.add_parser("ask", help="Send a single prompt.")
    ask_parser.add_argument("prompt", nargs="?", help="Prompt text. Reads stdin if omitted.")
    ask_parser.add_argument("--session-id", help="Reuse an existing session id.")

    repl_parser = subparsers.add_parser("repl", help="Start an interactive chat session.")
    repl_parser.add_argument("--session-id", help="Reuse an existing session id.")

    subparsers.add_parser("show-config", help="Print resolved runtime configuration.")

    personal_parser = subparsers.add_parser(
        "personal",
        help="Inspect local Personal Runtime configuration.",
    )
    personal_subparsers = personal_parser.add_subparsers(dest="personal_command")
    for name in ["status", "config", "sources", "overlays", "modes", "validate", "smoke"]:
        command_parser = personal_subparsers.add_parser(
            name,
            help=f"Run Personal Runtime {name} diagnostics.",
        )
        command_parser.add_argument(
            "--show-paths",
            action="store_true",
            help="Show configured local paths instead of redacted path references.",
        )

    skill_parser = subparsers.add_parser(
        "skill",
        help="Run explicit read-only skill invocations.",
    )
    skill_subparsers = skill_parser.add_subparsers(dest="skill_command")
    skill_run_parser = skill_subparsers.add_parser(
        "run",
        help="Run a registered skill by explicit skill_id and explicit input.",
    )
    skill_run_parser.add_argument("skill_id", nargs="?", help="Explicit skill_id to run.")
    skill_run_parser.add_argument("--skill-id", dest="skill_id_option", help="Explicit skill_id to run.")
    skill_run_parser.add_argument("--input-json", help="JSON object input payload.")
    skill_run_parser.add_argument("--input-json-file", help="Path to a UTF-8 JSON object input payload file.")
    skill_run_parser.add_argument("--root", dest="root_path", help="Workspace read root for read-only skills.")
    skill_run_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skill_run_parser.add_argument("--recursive", action="store_true", help="List files recursively.")
    skill_run_parser.add_argument("--max-results", type=int, help="Maximum file list results.")
    skill_gate_run_parser = skill_subparsers.add_parser(
        "gate-run",
        help="Evaluate the read-only execution gate, then run only if allowed.",
    )
    skill_gate_run_parser.add_argument("skill_id", nargs="?", help="Explicit skill_id to gate-run.")
    skill_gate_run_parser.add_argument("--skill-id", dest="skill_id_option", help="Explicit skill_id to gate-run.")
    skill_gate_run_parser.add_argument("--input-json", help="JSON object input payload.")
    skill_gate_run_parser.add_argument("--input-json-file", help="Path to a UTF-8 JSON object input payload file.")
    skill_gate_run_parser.add_argument("--root", dest="root_path", help="Workspace read root for read-only skills.")
    skill_gate_run_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skill_gate_run_parser.add_argument("--recursive", action="store_true", help="List files recursively.")
    skill_gate_run_parser.add_argument("--max-results", type=int, help="Maximum file list results.")
    skill_propose_parser = skill_subparsers.add_parser(
        "propose",
        help="Create a review-only explicit skill invocation proposal from a prompt.",
    )
    skill_propose_parser.add_argument("prompt", nargs="?", help="Prompt to analyze. Reads stdin if omitted.")
    skill_propose_parser.add_argument("--text", help="Prompt text to analyze.")
    skill_propose_parser.add_argument("--family", help="Proposal family to use.")
    skill_propose_parser.add_argument("--root", dest="root_path", help="Workspace read root for proposal payload.")
    skill_propose_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skill_propose_parser.add_argument("--source-runtime", help="Source runtime hint.")
    skill_propose_parser.add_argument("--format", dest="format_hint", help="Source format hint.")
    skill_propose_parser.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    skill_propose_parser.add_argument("--recursive", action="store_true", help="Suggest recursive file listing.")
    skill_propose_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    skill_review_parser = skill_subparsers.add_parser(
        "review",
        help="Review a skill proposal without executing it.",
    )
    skill_review_parser.add_argument("proposal_id", nargs="?", help="Proposal id. Persistence is not available yet.")
    skill_review_parser.add_argument("--decision", required=True, help="Review decision or decision alias.")
    skill_review_parser.add_argument("--reason", help="Human-readable review reason.")
    skill_review_parser.add_argument(
        "--from-proposal-json-file",
        help="Path to a UTF-8 JSON object produced from a SkillInvocationProposal.",
    )
    skill_review_parser.add_argument("--reviewer-type", default="human", help="Reviewer type.")
    skill_review_parser.add_argument("--reviewer-id", default="cli", help="Reviewer id.")
    skill_review_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    skill_bridge_parser = skill_subparsers.add_parser(
        "bridge",
        help="Bridge an approved reviewed proposal through the read-only gate.",
    )
    skill_bridge_parser.add_argument(
        "review_result_id",
        nargs="?",
        help="Review result id. Persistence is not available yet.",
    )
    skill_bridge_parser.add_argument("--proposal-json-file", help="Path to a SkillInvocationProposal JSON file.")
    skill_bridge_parser.add_argument(
        "--review-json-file",
        help="Path to review JSON containing review_decision and optional review_result.",
    )
    skill_bridge_parser.add_argument(
        "--bridge-json-file",
        help="Path to combined JSON containing proposal, review_decision, and optional review_result.",
    )
    skill_bridge_parser.add_argument("--json", action="store_true", help="Print result as JSON.")

    skills_parser = subparsers.add_parser(
        "skills",
        help="Inspect internal skill contracts without executing skills.",
    )
    skills_subparsers = skills_parser.add_subparsers(dest="skills_command")
    onboarding_parser = skills_subparsers.add_parser(
        "onboarding",
        help="Inspect Internal Skill Onboarding contracts.",
    )
    onboarding_subparsers = onboarding_parser.add_subparsers(dest="onboarding_command")
    onboarding_list = onboarding_subparsers.add_parser("list", help="List read-only onboarding candidates.")
    onboarding_list.add_argument("--json", action="store_true", help="Print result as JSON.")
    onboarding_show = onboarding_subparsers.add_parser("show", help="Show a read-only onboarding candidate.")
    onboarding_show.add_argument("skill_id", help="Internal skill id.")
    onboarding_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    onboarding_check = onboarding_subparsers.add_parser("check", help="Validate a read-only onboarding candidate.")
    onboarding_check.add_argument("--skill-id", required=True, help="Internal skill id.")
    onboarding_check.add_argument("--json", action="store_true", help="Print result as JSON.")
    onboarding_validate = onboarding_subparsers.add_parser("validate", help="Validate a descriptor JSON file.")
    onboarding_validate.add_argument("--descriptor-json-file", required=True, help="Path to descriptor JSON.")
    onboarding_validate.add_argument("--json", action="store_true", help="Print result as JSON.")
    skills_propose_parser = skills_subparsers.add_parser(
        "propose",
        help="Create a review-only skill proposal from text.",
    )
    skills_propose_parser.add_argument("prompt", nargs="?", help="Prompt to analyze. Reads stdin if omitted.")
    skills_propose_parser.add_argument("--text", help="Prompt text to analyze.")
    skills_propose_parser.add_argument("--family", help="Proposal family to use.")
    skills_propose_parser.add_argument("--root", dest="root_path", help="Workspace read root for proposal payload.")
    skills_propose_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skills_propose_parser.add_argument("--source-runtime", help="Source runtime hint.")
    skills_propose_parser.add_argument("--format", dest="format_hint", help="Source format hint.")
    skills_propose_parser.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    skills_propose_parser.add_argument("--recursive", action="store_true", help="Suggest recursive file listing.")
    skills_propose_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    registry_parser = skills_subparsers.add_parser(
        "registry",
        help="Render the read-only Observation/Digestion skill registry view.",
    )
    registry_subparsers = registry_parser.add_subparsers(dest="registry_command")
    registry_list = registry_subparsers.add_parser("list", help="List registry entries.")
    _add_registry_filter_options(registry_list)
    registry_show = registry_subparsers.add_parser("show", help="Show one registry entry.")
    registry_show.add_argument("skill_id", help="Skill id.")
    registry_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    for command_name in ["observation", "digestion", "external-candidates", "risk", "observability", "findings"]:
        command_parser = registry_subparsers.add_parser(
            command_name,
            help=f"Render registry {command_name} view.",
        )
        _add_registry_filter_options(command_parser)

    execution_parser = subparsers.add_parser(
        "execution",
        help="Query and audit existing execution envelopes without executing skills.",
    )
    execution_subparsers = execution_parser.add_subparsers(dest="execution_command")
    for command_name in ["list", "recent", "audit"]:
        command_parser = execution_subparsers.add_parser(
            command_name,
            help=f"Run read-only execution envelope {command_name}.",
        )
        _add_execution_query_options(command_parser)
    execution_show_parser = execution_subparsers.add_parser(
        "show",
        help="Show one execution envelope by id.",
    )
    execution_show_parser.add_argument("envelope_id", help="Execution envelope id.")
    _add_execution_query_options(execution_show_parser)

    promotion_parser = subparsers.add_parser(
        "promotion",
        help="Create and review execution result promotion candidates without promoting.",
    )
    promotion_subparsers = promotion_parser.add_subparsers(dest="promotion_command")
    promotion_candidate_parser = promotion_subparsers.add_parser(
        "candidate-from-envelope",
        help="Create a review-only promotion candidate from an execution envelope.",
    )
    promotion_candidate_parser.add_argument("envelope_id", nargs="?", help="Execution envelope id.")
    promotion_candidate_parser.add_argument("--target", required=True, help="Promotion candidate target kind.")
    promotion_candidate_parser.add_argument("--title", help="Candidate title.")
    promotion_candidate_parser.add_argument("--private", action="store_true", help="Mark candidate private.")
    promotion_candidate_parser.add_argument("--envelope-json-file", help="Path to envelope JSON input.")
    promotion_candidate_parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    promotion_candidate_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    promotion_list_parser = promotion_subparsers.add_parser("list", help="List promotion candidates.")
    promotion_list_parser.add_argument("--limit", type=int, default=20, help="Maximum candidates to show.")
    promotion_list_parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    promotion_list_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    promotion_show_parser = promotion_subparsers.add_parser("show", help="Show a promotion candidate.")
    promotion_show_parser.add_argument("candidate_id", help="Promotion candidate id.")
    promotion_show_parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    promotion_show_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    promotion_review_parser = promotion_subparsers.add_parser("review", help="Review a promotion candidate.")
    promotion_review_parser.add_argument("candidate_id", help="Promotion candidate id.")
    promotion_review_parser.add_argument("--decision", required=True, help="Promotion review decision.")
    promotion_review_parser.add_argument("--reason", help="Review reason.")
    promotion_review_parser.add_argument("--reviewer-type", default="human", help="Reviewer type.")
    promotion_review_parser.add_argument("--reviewer-id", default="cli", help="Reviewer id.")
    promotion_review_parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    promotion_review_parser.add_argument("--json", action="store_true", help="Print result as JSON.")

    workspace_summary_parser = subparsers.add_parser(
        "workspace-summary",
        help="Create deterministic read-only workspace summaries.",
    )
    workspace_summary_subparsers = workspace_summary_parser.add_subparsers(dest="workspace_summary_command")
    workspace_summary_from_file = workspace_summary_subparsers.add_parser(
        "from-file",
        help="Summarize a workspace file through safe read handling.",
    )
    workspace_summary_from_file.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    workspace_summary_from_file.add_argument("--path", required=True, dest="relative_path", help="Relative workspace path.")
    workspace_summary_from_file.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    workspace_summary_from_file.add_argument("--json", action="store_true", help="Print result as JSON.")
    workspace_summary_from_envelope = workspace_summary_subparsers.add_parser(
        "from-envelope",
        help="Summarize an execution output preview by envelope id.",
    )
    workspace_summary_from_envelope.add_argument("envelope_id", help="Execution envelope id.")
    workspace_summary_from_envelope.add_argument("--input-kind", default="generic_text", help="Input kind.")
    workspace_summary_from_envelope.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    workspace_summary_from_envelope.add_argument("--json", action="store_true", help="Print result as JSON.")
    workspace_summary_show = workspace_summary_subparsers.add_parser("show", help="Show a summary result.")
    workspace_summary_show.add_argument("summary_result_id", help="Summary result id.")
    workspace_summary_show.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    workspace_summary_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    workspace_summary_candidate = workspace_summary_subparsers.add_parser("candidate", help="Create a pending review summary candidate.")
    workspace_summary_candidate.add_argument("summary_result_id", help="Summary result id.")
    workspace_summary_candidate.add_argument("--target", required=True, help="Candidate target kind.")
    workspace_summary_candidate.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    workspace_summary_candidate.add_argument("--json", action="store_true", help="Print result as JSON.")

    observe_parser = subparsers.add_parser(
        "observe",
        help="Read-only agent trace observation diagnostics.",
    )
    observe_subparsers = observe_parser.add_subparsers(dest="observe_command")
    observe_source = observe_subparsers.add_parser("source-inspect", help="Inspect an observation source.")
    observe_source.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_source.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    observe_source.add_argument("--runtime", default="unknown", help="Source runtime hint.")
    observe_source.add_argument("--format", dest="format_hint", default="generic_jsonl", help="Source format hint.")
    observe_source.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_trace = observe_subparsers.add_parser("trace", help="Observe a generic JSONL trace.")
    observe_trace.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_trace.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    observe_trace.add_argument("--runtime", default="unknown", help="Source runtime hint.")
    observe_trace.add_argument("--format", dest="format_hint", default="generic_jsonl", help="Source format hint.")
    observe_trace.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_infer = observe_subparsers.add_parser("infer", help="Create deterministic behavior inference.")
    observe_infer.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    observe_infer.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_narrative = observe_subparsers.add_parser("narrative", help="Create deterministic process narrative.")
    observe_narrative.add_argument("--inference-json-file", required=True, help="AgentBehaviorInference JSON file.")
    observe_narrative.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_propose = observe_subparsers.add_parser("propose", help="Create a review-only observation proposal.")
    observe_propose.add_argument("text", help="Prompt text to analyze.")
    observe_propose.add_argument("--root", dest="root_path", help="Workspace read root for proposal payload.")
    observe_propose.add_argument("--path", dest="relative_path", help="Relative source path.")
    observe_propose.add_argument("--source-runtime", help="Source runtime hint.")
    observe_propose.add_argument("--format", dest="format_hint", help="Source format hint.")
    observe_propose.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_run = observe_subparsers.add_parser("run", help="Run gated read-only observation skill.")
    observe_run_subparsers = observe_run.add_subparsers(dest="observe_run_command")
    observe_run_source = observe_run_subparsers.add_parser("source-inspect", help="Run source inspection.")
    observe_run_source.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_run_source.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    observe_run_source.add_argument("--format", dest="format_hint", default="generic_jsonl", help="Source format hint.")
    observe_run_source.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_run_trace = observe_run_subparsers.add_parser("trace", help="Run generic JSONL trace observation.")
    observe_run_trace.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_run_trace.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    observe_run_trace.add_argument("--runtime", dest="source_runtime", default="unknown", help="Source runtime hint.")
    observe_run_trace.add_argument("--format", dest="format_hint", default="generic_jsonl", help="Source format hint.")
    observe_run_trace.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_run_normalize = observe_run_subparsers.add_parser("normalize", help="Run event normalization.")
    observe_run_normalize.add_argument("--batch-json-file", required=True, help="Batch or records JSON file.")
    observe_run_normalize.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_run_infer = observe_run_subparsers.add_parser("infer", help="Run behavior inference.")
    observe_run_infer.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    observe_run_infer.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_run_narrative = observe_run_subparsers.add_parser("narrative", help="Run process narrative.")
    observe_run_narrative.add_argument("--inference-json-file", required=True, help="AgentBehaviorInference JSON file.")
    observe_run_narrative.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_spine = observe_subparsers.add_parser("spine", help="Agent Observation Spine diagnostics.")
    observe_spine_subparsers = observe_spine.add_subparsers(dest="observe_spine_command")
    for command_name in ["ontology", "adapters", "collectors", "runtimes", "redaction-policy", "export-policy", "fleet-snapshot"]:
        command_parser = observe_spine_subparsers.add_parser(command_name, help=f"Render spine {command_name}.")
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_spine_normalize = observe_spine_subparsers.add_parser("normalize", help="Normalize one event into V2 shape.")
    observe_spine_normalize.add_argument("--event-json-file", required=True, help="Event JSON file.")
    observe_spine_normalize.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_spine_infer = observe_spine_subparsers.add_parser("infer", help="Create behavior inference V2.")
    observe_spine_infer.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    observe_spine_infer.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters = observe_subparsers.add_parser("adapters", help="Cross-harness trace adapter contracts.")
    observe_adapters_subparsers = observe_adapters.add_subparsers(dest="observe_adapters_command")
    observe_adapters_list = observe_adapters_subparsers.add_parser("list", help="List registered trace adapters.")
    observe_adapters_list.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_show = observe_adapters_subparsers.add_parser("show", help="Show one trace adapter contract.")
    observe_adapters_show.add_argument("adapter_name", help="Adapter name.")
    observe_adapters_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_inspect = observe_adapters_subparsers.add_parser("inspect-source", help="Inspect a trace source shape.")
    observe_adapters_inspect.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_adapters_inspect.add_argument("--path", required=True, dest="relative_path", help="Relative trace path.")
    observe_adapters_inspect.add_argument("--runtime", dest="runtime_hint", help="Source runtime hint.")
    observe_adapters_inspect.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_plan = observe_adapters_subparsers.add_parser("plan", help="Create a normalization plan.")
    observe_adapters_plan.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_adapters_plan.add_argument("--path", required=True, dest="relative_path", help="Relative trace path.")
    observe_adapters_plan.add_argument("--runtime", dest="runtime_hint", help="Source runtime hint.")
    observe_adapters_plan.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_normalize = observe_adapters_subparsers.add_parser("normalize", help="Normalize a supported trace source.")
    observe_adapters_normalize.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    observe_adapters_normalize.add_argument("--path", required=True, dest="relative_path", help="Relative trace path.")
    observe_adapters_normalize.add_argument("--runtime", dest="runtime_hint", help="Source runtime hint.")
    observe_adapters_normalize.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_rules = observe_adapters_subparsers.add_parser("mapping-rules", help="Show adapter mapping rules.")
    observe_adapters_rules.add_argument("adapter_name", help="Adapter name.")
    observe_adapters_rules.add_argument("--json", action="store_true", help="Print result as JSON.")
    observe_adapters_coverage = observe_adapters_subparsers.add_parser("coverage", help="Show adapter coverage.")
    observe_adapters_coverage.add_argument("adapter_name", help="Adapter name.")
    observe_adapters_coverage.add_argument("--json", action="store_true", help="Print result as JSON.")

    digest_parser = subparsers.add_parser(
        "digest",
        help="Read-only external skill digestion diagnostics.",
    )
    digest_subparsers = digest_parser.add_subparsers(dest="digest_command")
    digest_source = digest_subparsers.add_parser("source-inspect", help="Inspect an external skill source.")
    digest_source.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_source.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_source.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_source.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_inventory = digest_subparsers.add_parser("inventory", help="Inventory external skill resources read-only.")
    digest_inventory.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_inventory.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_inventory.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_static = digest_subparsers.add_parser("static", help="Create a static external skill profile.")
    digest_static.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_static.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_static.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_static.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_risk = digest_subparsers.add_parser("risk", help="Infer static risk for an external skill source.")
    digest_risk.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_risk.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_risk.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_risk.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_report = digest_subparsers.add_parser("report", help="Render expanded static digestion report.")
    digest_report.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_report.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_report.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_report.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_fingerprint = digest_subparsers.add_parser("fingerprint", help="Create behavior fingerprint.")
    digest_fingerprint.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    digest_fingerprint.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_assimilate = digest_subparsers.add_parser("assimilate", help="Create non-executable assimilation candidate.")
    digest_assimilate.add_argument("--static-profile-json-file", help="ExternalSkillStaticProfile JSON file.")
    digest_assimilate.add_argument("--fingerprint-json-file", help="ExternalSkillBehaviorFingerprint JSON file.")
    digest_assimilate.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_adapter = digest_subparsers.add_parser("adapter-candidate", help="Create non-executable adapter candidate.")
    digest_adapter.add_argument("--candidate-json-file", required=True, help="ExternalSkillAssimilationCandidate JSON file.")
    digest_adapter.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_adapter_build = digest_subparsers.add_parser(
        "adapter-build",
        help="Build review-only adapter candidates from observed behavior.",
    )
    digest_adapter_build_subparsers = digest_adapter_build.add_subparsers(dest="adapter_build_command")
    adapter_from_inference = digest_adapter_build_subparsers.add_parser(
        "from-inference",
        help="Build adapter candidates from AgentBehaviorInferenceV2 JSON.",
    )
    adapter_from_inference.add_argument("--inference-json-file", required=True, help="AgentBehaviorInferenceV2 JSON file.")
    adapter_from_inference.add_argument("--json", action="store_true", help="Print result as JSON.")
    adapter_from_fingerprint = digest_adapter_build_subparsers.add_parser(
        "from-fingerprint",
        help="Build adapter candidates from ExternalSkillBehaviorFingerprint JSON.",
    )
    adapter_from_fingerprint.add_argument(
        "--fingerprint-json-file",
        required=True,
        help="ExternalSkillBehaviorFingerprint JSON file.",
    )
    adapter_from_fingerprint.add_argument("--json", action="store_true", help="Print result as JSON.")
    adapter_from_run = digest_adapter_build_subparsers.add_parser(
        "from-observed-run",
        help="Build adapter candidates from ObservedAgentRun JSON.",
    )
    adapter_from_run.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    adapter_from_run.add_argument("--json", action="store_true", help="Print result as JSON.")
    adapter_show = digest_adapter_build_subparsers.add_parser("show", help="Show a local adapter candidate id.")
    adapter_show.add_argument("adapter_candidate_id", help="Adapter candidate id.")
    adapter_unsupported = digest_adapter_build_subparsers.add_parser(
        "unsupported",
        help="Show unsupported features for a local adapter candidate id.",
    )
    adapter_unsupported.add_argument("adapter_candidate_id", help="Adapter candidate id.")
    digest_propose = digest_subparsers.add_parser("propose", help="Create a review-only digestion proposal.")
    digest_propose.add_argument("text", help="Prompt text to analyze.")
    digest_propose.add_argument("--root", dest="root_path", help="Workspace read root for proposal payload.")
    digest_propose.add_argument("--path", dest="relative_path", help="Relative source path.")
    digest_propose.add_argument("--source-runtime", help="Source runtime hint.")
    digest_propose.add_argument("--format", dest="format_hint", help="Source format hint.")
    digest_propose.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_propose.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_run = digest_subparsers.add_parser("run", help="Run gated read-only digestion skill.")
    digest_run_subparsers = digest_run.add_subparsers(dest="digest_run_command")
    digest_run_source = digest_run_subparsers.add_parser("source-inspect", help="Run external source inspection.")
    digest_run_source.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_run_source.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_run_source.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_run_source.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_run_static = digest_run_subparsers.add_parser("static", help="Run static external skill digest.")
    digest_run_static.add_argument("--root", required=True, dest="root_path", help="Workspace read root.")
    digest_run_static.add_argument("--path", required=True, dest="relative_path", help="Relative source path.")
    digest_run_static.add_argument("--vendor", dest="vendor_hint", help="Vendor/runtime hint.")
    digest_run_static.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_run_fingerprint = digest_run_subparsers.add_parser("fingerprint", help="Run behavior fingerprint.")
    digest_run_fingerprint.add_argument("--observed-run-json-file", required=True, help="ObservedAgentRun JSON file.")
    digest_run_fingerprint.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_run_assimilate = digest_run_subparsers.add_parser("assimilate", help="Run candidate assimilation.")
    digest_run_assimilate.add_argument("--static-profile-json-file", help="ExternalSkillStaticProfile JSON file.")
    digest_run_assimilate.add_argument("--fingerprint-json-file", help="ExternalSkillBehaviorFingerprint JSON file.")
    digest_run_assimilate.add_argument("--json", action="store_true", help="Print result as JSON.")
    digest_run_adapter = digest_run_subparsers.add_parser("adapter-candidate", help="Run adapter candidate creation.")
    digest_run_adapter.add_argument("--candidate-json-file", required=True, help="ExternalSkillAssimilationCandidate JSON file.")
    digest_run_adapter.add_argument("--json", action="store_true", help="Print result as JSON.")

    observe_digest_parser = subparsers.add_parser(
        "observe-digest",
        help="Read-only Observation/Digestion conformance diagnostics.",
    )
    observe_digest_subparsers = observe_digest_parser.add_subparsers(dest="observe_digest_command")
    od_conformance = observe_digest_subparsers.add_parser("conformance", help="Run conformance and smoke checks.")
    od_conf_subparsers = od_conformance.add_subparsers(dest="conformance_command")
    od_conf_run = od_conf_subparsers.add_parser("run", help="Run static conformance checks.")
    od_conf_run.add_argument("--skill-id", help="Limit checks to one skill id.")
    od_conf_run.add_argument("--fixture-root", help="Optional fixture root for smoke-enabled run.")
    od_conf_run.add_argument("--smoke", action="store_true", help="Also run smoke cases.")
    od_conf_run.add_argument("--json", action="store_true", help="Print result as JSON.")
    od_conf_smoke = od_conf_subparsers.add_parser("smoke", help="Run smoke cases.")
    od_conf_smoke.add_argument("--skill-id", help="Limit smoke to one skill id.")
    od_conf_smoke.add_argument("--fixture-root", help="Fixture root for path-based smoke cases.")
    od_conf_smoke.add_argument("--json", action="store_true", help="Print result as JSON.")
    od_conf_report = od_conf_subparsers.add_parser("report", help="Run conformance and render a report.")
    od_conf_report.add_argument("--skill-id", help="Limit report to one skill id.")
    od_conf_report.add_argument("--json", action="store_true", help="Print result as JSON.")
    od_conf_check = od_conf_subparsers.add_parser("check-skill", help="Run conformance checks for one skill.")
    od_conf_check.add_argument("skill_id", help="Observation/Digestion skill id.")
    od_conf_check.add_argument("--json", action="store_true", help="Print result as JSON.")
    od_conf_findings = od_conf_subparsers.add_parser("findings", help="Render conformance findings.")
    od_conf_findings.add_argument("--limit", type=int, default=20, help="Maximum findings to show.")
    od_conf_findings.add_argument("--json", action="store_true", help="Print result as JSON.")
    od_ecosystem = observe_digest_subparsers.add_parser(
        "ecosystem",
        help="Summarize the Observation/Digestion ecosystem.",
    )
    od_ecosystem_subparsers = od_ecosystem.add_subparsers(dest="ecosystem_command")
    for command_name in ["snapshot", "components", "capabilities", "safety", "gaps", "manifest", "report"]:
        command_parser = od_ecosystem_subparsers.add_parser(
            command_name,
            help=f"Render ecosystem {command_name}.",
        )
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
        command_parser.add_argument("--limit", type=int, default=20, help="Maximum rows to show.")

    self_awareness_parser = subparsers.add_parser(
        "self-awareness",
        help="Inspect read-only Self-Awareness Layer contracts.",
    )
    self_awareness_subparsers = self_awareness_parser.add_subparsers(dest="self_awareness_command")
    self_awareness_registry = self_awareness_subparsers.add_parser("registry", help="List self-awareness contracts.")
    self_awareness_registry.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_show = self_awareness_subparsers.add_parser("show", help="Show one self-awareness contract.")
    self_awareness_show.add_argument("skill_id", help="Self-awareness skill id.")
    self_awareness_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    for command_name in ["conformance", "pig-report", "ocpx-projection"]:
        command_parser = self_awareness_subparsers.add_parser(
            command_name,
            help=f"Render self-awareness {command_name}.",
        )
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_workspace = self_awareness_subparsers.add_parser(
        "workspace",
        help="Run metadata-only self-workspace awareness commands.",
    )
    self_awareness_workspace_subparsers = self_awareness_workspace.add_subparsers(dest="self_awareness_workspace_command")
    workspace_roots = self_awareness_workspace_subparsers.add_parser("roots", help="List workspace root aliases.")
    workspace_roots.add_argument("--json", action="store_true", help="Print result as JSON.")
    workspace_verify = self_awareness_workspace_subparsers.add_parser("verify-path", help="Verify a workspace path.")
    workspace_verify.add_argument("input_path", help="Workspace-relative path to verify.")
    workspace_verify.add_argument("--json", action="store_true", help="Print result as JSON.")
    workspace_inventory = self_awareness_workspace_subparsers.add_parser(
        "inventory",
        help="Build a metadata-only workspace inventory.",
    )
    workspace_inventory.add_argument("relative_path", nargs="?", default=".", help="Workspace-relative path to inventory.")
    workspace_inventory.add_argument("--max-depth", type=int, default=3, help="Maximum traversal depth.")
    workspace_inventory.add_argument("--max-entries", type=int, default=500, help="Maximum returned entries.")
    workspace_inventory.add_argument("--include-hidden", action="store_true", help="Include hidden paths.")
    workspace_inventory.add_argument("--include-ignored", action="store_true", help="Include noisy default-excluded paths.")
    workspace_inventory.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_text = self_awareness_subparsers.add_parser(
        "text",
        help="Run bounded redacted self-code/text perception commands.",
    )
    self_awareness_text_subparsers = self_awareness_text.add_subparsers(dest="self_awareness_text_command")
    text_read = self_awareness_text_subparsers.add_parser("read", help="Read a bounded redacted text slice.")
    text_read.add_argument("path", help="Workspace-relative file path.")
    text_read.add_argument("--mode", choices=["preview", "line_range", "head", "tail"], default="preview")
    text_read.add_argument("--start-line", type=int)
    text_read.add_argument("--end-line", type=int)
    text_read.add_argument("--max-bytes", type=int, default=16384)
    text_read.add_argument("--max-lines", type=int, default=300)
    text_read.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_search = self_awareness_subparsers.add_parser(
        "search",
        help="Run bounded redacted literal workspace search.",
    )
    self_awareness_search.add_argument("query", help="Literal query to search for.")
    self_awareness_search.add_argument("--path", dest="relative_path", default=".", help="Workspace-relative search root.")
    self_awareness_search.add_argument("--include", dest="include_globs", action="append", default=[], help="Include glob.")
    self_awareness_search.add_argument("--exclude", dest="exclude_globs", action="append", default=[], help="Exclude glob.")
    self_awareness_search.add_argument("--case-sensitive", action="store_true", help="Use case-sensitive literal matching.")
    self_awareness_search.add_argument("--context-lines", type=int, default=2, help="Context lines around each match.")
    self_awareness_search.add_argument("--max-files", type=int, default=200, help="Maximum files to scan.")
    self_awareness_search.add_argument("--max-matches", type=int, default=200, help="Maximum matches to return.")
    self_awareness_search.add_argument("--max-matches-per-file", type=int, default=20, help="Maximum matches per file.")
    self_awareness_search.add_argument("--max-bytes-per-file", type=int, default=65536, help="Maximum bytes per file.")
    self_awareness_search.add_argument("--max-total-bytes", type=int, default=1048576, help="Maximum bytes across files.")
    self_awareness_search.add_argument("--include-hidden", action="store_true", help="Include hidden paths.")
    self_awareness_search.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_summarize = self_awareness_subparsers.add_parser(
        "summarize",
        help="Create deterministic self-structure summary candidates.",
    )
    self_awareness_summarize.add_argument("summary_mode", choices=["auto", "markdown", "python", "json", "yaml", "toml", "plain_text"])
    self_awareness_summarize.add_argument("path", help="Workspace-relative file path.")
    self_awareness_summarize.add_argument("--max-bytes", type=int, default=65536)
    self_awareness_summarize.add_argument("--max-lines", type=int, default=1000)
    self_awareness_summarize.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_project = self_awareness_subparsers.add_parser(
        "project",
        help="Run metadata-only self-project structure awareness commands.",
    )
    self_awareness_project_subparsers = self_awareness_project.add_subparsers(dest="self_awareness_project_command")
    project_structure = self_awareness_project_subparsers.add_parser(
        "structure",
        help="Build a deterministic project surface structure candidate.",
    )
    project_structure.add_argument("--path", dest="relative_path", default=".", help="Workspace-relative directory path.")
    project_structure.add_argument("--max-depth", type=int, default=5)
    project_structure.add_argument("--max-entries", type=int, default=2000)
    project_structure.add_argument("--include-hidden", action="store_true")
    project_structure.add_argument("--include-ignored", action="store_true")
    project_structure.add_argument("--no-summary-candidates", action="store_true")
    project_structure.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_verify = self_awareness_subparsers.add_parser(
        "verify",
        help="Run deterministic self-surface verification commands.",
    )
    self_awareness_verify_subparsers = self_awareness_verify.add_subparsers(dest="self_awareness_verify_command")
    verify_surface = self_awareness_verify_subparsers.add_parser(
        "surface",
        help="Verify a self-awareness output surface.",
    )
    verify_surface.add_argument("--target-type")
    verify_surface.add_argument("--target-id")
    verify_surface.add_argument("--target-payload", help="JSON object file containing the target payload.")
    verify_surface.add_argument("--strictness", choices=["lenient", "standard", "strict"], default="standard")
    verify_surface.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_intention = self_awareness_subparsers.add_parser(
        "intention",
        help="Create candidate-only self-directed intention bundles.",
    )
    self_awareness_intention_subparsers = self_awareness_intention.add_subparsers(dest="self_awareness_intention_command")
    intention_candidates = self_awareness_intention_subparsers.add_parser(
        "candidates",
        help="Create plan/todo/no-action/needs-more-input intention candidates.",
    )
    intention_candidates.add_argument("--goal", dest="goal_text", help="Goal text for the candidate bundle.")
    intention_candidates.add_argument("--source-candidate", dest="source_candidate_ids", action="append", default=[])
    intention_candidates.add_argument("--source-report", dest="source_report_ids", action="append", default=[])
    intention_candidates.add_argument("--include-no-action", action="store_true", help="Include no-action candidate.")
    intention_candidates.add_argument("--strictness", choices=["lenient", "standard", "strict"], default="standard")
    intention_candidates.add_argument("--json", action="store_true", help="Print result as JSON.")
    self_awareness_workbench = self_awareness_subparsers.add_parser(
        "workbench",
        help="Render the read-only Self-Awareness operator workbench.",
    )
    self_awareness_workbench.add_argument(
        "--section",
        choices=["overview", "registry", "coverage", "candidates", "verification", "audit", "risks", "timeline", "pig", "ocpx"],
        default="overview",
    )
    self_awareness_workbench.add_argument("--limit", type=int, default=20, help="Maximum recent refs to show.")
    self_awareness_workbench.add_argument("--json", action="store_true", help="Print result as JSON.")
    for alias_name, section_name in [("status", "overview"), ("audit", "audit"), ("coverage", "coverage")]:
        alias_parser = self_awareness_subparsers.add_parser(
            alias_name,
            help=f"Render Self-Awareness Workbench {section_name}.",
        )
        alias_parser.set_defaults(self_awareness_workbench_alias_section=section_name)
        alias_parser.add_argument("--limit", type=int, default=20, help="Maximum recent refs to show.")
        alias_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    for command_name in [
        "consolidate",
        "release-manifest",
        "gap-register",
        "safety-report",
        "capability-map",
        "coverage-matrix",
    ]:
        command_parser = self_awareness_subparsers.add_parser(
            command_name,
            help=f"Render self-awareness {command_name}.",
        )
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")

    deep_self_parser = subparsers.add_parser(
        "deep-self",
        help="Inspect read-only Deep Self-Introspection contracts.",
    )
    deep_self_subparsers = deep_self_parser.add_subparsers(dest="deep_self_command")
    for command_name in ["contract", "subjects", "conformance", "pig-report", "ocpx-projection"]:
        command_parser = deep_self_subparsers.add_parser(
            command_name,
            help=f"Render deep self-introspection {command_name}.",
        )
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    deep_self_show = deep_self_subparsers.add_parser("show", help="Show one deep self-introspection subject.")
    deep_self_show.add_argument("subject_id", help="Deep self-introspection subject id.")
    deep_self_show.add_argument("--json", action="store_true", help="Print result as JSON.")
    deep_self_capability = deep_self_subparsers.add_parser(
        "capability",
        help="Render read-only self-capability registry awareness views.",
    )
    deep_self_capability_subparsers = deep_self_capability.add_subparsers(dest="deep_self_capability_command")
    capability_registry = deep_self_capability_subparsers.add_parser(
        "registry",
        help="Render the self-capability registry snapshot.",
    )
    capability_registry.add_argument("--status", dest="status_filter")
    capability_registry.add_argument("--layer", dest="layer_filter")
    capability_registry.add_argument("--json", action="store_true", help="Print result as JSON.")
    capability_truth = deep_self_capability_subparsers.add_parser(
        "truth-check",
        help="Run read-only capability truth checks.",
    )
    capability_truth.add_argument("--claims", help="JSON file containing claim dictionaries.")
    capability_truth.add_argument("--json", action="store_true", help="Print result as JSON.")
    for command_name in ["risks", "observability"]:
        command_parser = deep_self_capability_subparsers.add_parser(
            command_name,
            help=f"Render self-capability {command_name}.",
        )
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")

    workbench_parser = subparsers.add_parser(
        "workbench",
        help="Render a read-only Personal Runtime operator workbench.",
    )
    workbench_subparsers = workbench_parser.add_subparsers(dest="workbench_command")
    for command_name in ["status", "recent", "pending", "blockers", "candidates", "summaries", "health"]:
        command_parser = workbench_subparsers.add_parser(
            command_name,
            help=f"Render Workbench {command_name}.",
        )
        command_parser.add_argument("--limit", type=int, default=20, help="Maximum items to show.")
        command_parser.add_argument("--show-paths", action="store_true", help="Show path-like fields.")
        command_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
        command_parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")
    return parser


def _add_registry_filter_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--layer", dest="skill_layer", help="Filter by skill layer.")
    parser.add_argument("--origin", dest="skill_origin", help="Filter by skill origin.")
    parser.add_argument("--risk-class", dest="risk_class", help="Filter by risk class.")
    parser.add_argument("--status", help="Filter by status.")
    parser.add_argument("--enabled", choices=["true", "false"], help="Filter by enabled state.")
    parser.add_argument(
        "--execution-enabled",
        choices=["true", "false"],
        help="Filter by execution-enabled state.",
    )
    parser.add_argument("--limit", type=int, help="Maximum entries to render.")
    parser.add_argument("--json", action="store_true", help="Print result as JSON.")


def _add_execution_query_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--skill-id", help="Filter by skill id.")
    parser.add_argument("--status", help="Filter by envelope status.")
    parser.add_argument("--session-id", help="Filter by session id.")
    parser.add_argument("--blocked", action="store_true", help="Filter to blocked envelopes.")
    parser.add_argument("--failed", action="store_true", help="Filter to failed/error envelopes.")
    parser.add_argument("--limit", type=int, help="Maximum records to return.")
    parser.add_argument("--show-paths", action="store_true", help="Show path-like fields.")
    parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    parser.add_argument("--ocel-db", help="Path to the OCEL SQLite database.")


def resolve_prompt(direct_prompt: str | None) -> str:
    if direct_prompt:
        return direct_prompt
    if not sys.stdin.isatty():
        content = sys.stdin.read().strip()
        if content:
            return content
    raise SystemExit("prompt is required when stdin is empty")


def format_assistant_output(response_text: str) -> str:
    if response_text.strip():
        return response_text
    return EMPTY_MODEL_RESPONSE_MESSAGE


def format_runtime_error(error: Exception) -> str:
    message = str(error)
    if "No models loaded" in message:
        return LLM_PROVIDER_UNAVAILABLE_MESSAGE
    if message.strip():
        return f"[runtime error: {message}]"
    return "[runtime error: no details available]"


def run_ask(args: argparse.Namespace) -> int:
    load_app_settings()
    prompt = resolve_prompt(args.prompt)
    try:
        result = AgentRuntime().run(prompt, session_id=args.session_id)
    except Exception as error:
        print(format_runtime_error(error), file=sys.stderr)
        return 1
    print(format_assistant_output(result.response_text))
    return 0


def run_repl(args: argparse.Namespace) -> int:
    load_app_settings()
    chat = ChatService()
    session_id = args.session_id
    print("Interactive session started. Type /exit to quit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            print()
            return 0

        if not user_input:
            continue
        if user_input == "/exit":
            return 0

        try:
            response_text = chat.chat(user_input, session_id=session_id)
        except Exception as error:
            print(f"assistant> {format_runtime_error(error)}")
            continue
        print(f"assistant> {format_assistant_output(response_text)}")


def run_show_config() -> int:
    settings = load_app_settings()
    print(f"env_file={settings.env_file or 'not loaded'}")
    print(f"provider={settings.llm.provider}")
    print(f"base_url={settings.llm.base_url}")
    print(f"model={settings.llm.model}")
    print(f"api_key={'set' if settings.llm.api_key else 'missing'}")
    print(f"timeout_seconds={settings.llm.timeout_seconds}")
    return 0


def run_personal(args: argparse.Namespace) -> int:
    if not args.personal_command:
        print("personal command is required", file=sys.stderr)
        return 1
    service = PersonalRuntimeSurfaceService()
    command = args.personal_command.replace("-", "_")
    runner = getattr(service, f"run_personal_{command}")
    result = runner(show_paths=bool(args.show_paths))
    print(service.render_cli_result(result))
    return result.exit_code


def _safe_received_preview(value: str | None, *, max_chars: int = 240) -> str:
    if value is None:
        return "<empty>"
    normalized = value.replace("\r", "\\r").replace("\n", "\\n")
    if len(normalized) > max_chars:
        normalized = f"{normalized[:max_chars]}..."
    return normalized


def _load_skill_input_payload(args: argparse.Namespace) -> tuple[dict[str, object] | None, int]:
    if args.input_json and args.input_json_file:
        print(
            "[explicit skill invocation error: use either --input-json or --input-json-file, not both]",
            file=sys.stderr,
        )
        return None, 1
    raw_payload: str | None = None
    payload_source = "empty"
    if args.input_json_file:
        payload_source = "input_json_file"
        try:
            raw_payload = Path(args.input_json_file).read_text(encoding="utf-8-sig")
        except OSError as error:
            print(
                f"[explicit skill invocation error: could not read --input-json-file: {error}]",
                file=sys.stderr,
            )
            return None, 1
    elif args.input_json:
        payload_source = "input_json"
        raw_payload = args.input_json
    else:
        return {}, 0

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as error:
        print(
            "[explicit skill invocation error: invalid JSON input: "
            f"{error.msg}; source={payload_source}; "
            f"received_preview={_safe_received_preview(raw_payload)}]",
            file=sys.stderr,
        )
        return None, 1
    if not isinstance(payload, dict):
        print(
            "[explicit skill invocation error: input payload must be a JSON object; "
            f"source={payload_source}; received_preview={_safe_received_preview(raw_payload)}]",
            file=sys.stderr,
        )
        return None, 1
    return payload, 0


def _load_proposal_json_file(path: str) -> tuple[object | None, int]:
    try:
        raw = Path(path).read_text(encoding="utf-8-sig")
    except OSError as error:
        print(f"[skill proposal review error: could not read proposal JSON file: {error}]", file=sys.stderr)
        return None, 1
    try:
        proposal = proposal_from_json(raw)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"[skill proposal review error: invalid proposal JSON: {error}]", file=sys.stderr)
        return None, 1
    return proposal, 0


def _load_bridge_inputs(args: argparse.Namespace) -> tuple[tuple[object, object, object | None] | None, int]:
    if args.bridge_json_file:
        if args.proposal_json_file or args.review_json_file:
            print(
                "[reviewed execution bridge error: use --bridge-json-file or the proposal/review pair, not both]",
                file=sys.stderr,
            )
            return None, 1
        try:
            raw = Path(args.bridge_json_file).read_text(encoding="utf-8-sig")
            return load_bridge_inputs_from_json(raw), 0
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            print(f"[reviewed execution bridge error: invalid bridge JSON: {error}]", file=sys.stderr)
            return None, 1
    if not args.proposal_json_file or not args.review_json_file:
        if args.review_result_id:
            print(
                "[reviewed execution bridge error: review/proposal persistence is not available; "
                "use --bridge-json-file or --proposal-json-file with --review-json-file]",
                file=sys.stderr,
            )
        else:
            print(
                "[reviewed execution bridge error: --bridge-json-file or proposal/review JSON files are required]",
                file=sys.stderr,
            )
        return None, 1
    try:
        proposal_raw = Path(args.proposal_json_file).read_text(encoding="utf-8-sig")
        review_raw = Path(args.review_json_file).read_text(encoding="utf-8-sig")
        proposal_value = json.loads(proposal_raw)
        review_value = json.loads(review_raw)
        if not isinstance(proposal_value, dict) or not isinstance(review_value, dict):
            raise ValueError("proposal and review JSON files must contain objects")
        proposal = bridge_proposal_from_dict(proposal_value)
        decision_value = review_value.get("review_decision", review_value)
        if not isinstance(decision_value, dict):
            raise ValueError("review JSON must contain a review_decision object")
        review_decision = review_decision_from_dict(decision_value)
        result_value = review_value.get("review_result")
        review_result = review_result_from_dict(result_value) if isinstance(result_value, dict) else None
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"[reviewed execution bridge error: invalid proposal/review JSON: {error}]", file=sys.stderr)
        return None, 1
    return (proposal, review_decision, review_result), 0


def _load_promotion_envelope(args: argparse.Namespace, store: OCELStore):
    if args.envelope_json_file:
        try:
            raw = Path(args.envelope_json_file).read_text(encoding="utf-8-sig")
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("envelope JSON must be an object")
            envelope_value = payload.get("envelope", payload)
            if not isinstance(envelope_value, dict):
                raise ValueError("envelope JSON must contain an envelope object")
            return (
                envelope_from_dict(envelope_value),
                output_snapshot_from_dict(payload.get("output_snapshot")),
                outcome_summary_from_dict(payload.get("outcome_summary")),
                artifact_ref_from_dict(payload.get("artifact_ref")),
                0,
            )
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            print(f"[promotion error: invalid envelope JSON: {error}]", file=sys.stderr)
            return None, None, None, None, 1
    if not args.envelope_id:
        print("[promotion error: envelope_id or --envelope-json-file is required]", file=sys.stderr)
        return None, None, None, None, 1
    envelope_rows = store.fetch_objects_by_type("execution_envelope")
    envelope = None
    for row in envelope_rows:
        attrs = row["object_attrs"]
        if attrs.get("envelope_id") == args.envelope_id:
            envelope = envelope_from_dict(attrs)
            break
    if envelope is None:
        print("[promotion error: execution envelope not found]", file=sys.stderr)
        return None, None, None, None, 1
    output_snapshot = _latest_related_object(
        store.fetch_objects_by_type("execution_output_snapshot"),
        args.envelope_id,
        output_snapshot_from_dict,
    )
    outcome_summary = _latest_related_object(
        store.fetch_objects_by_type("execution_outcome_summary"),
        args.envelope_id,
        outcome_summary_from_dict,
    )
    artifact_ref = _latest_related_object(
        store.fetch_objects_by_type("execution_artifact_ref"),
        args.envelope_id,
        artifact_ref_from_dict,
    )
    return envelope, output_snapshot, outcome_summary, artifact_ref, 0


def _latest_related_object(rows, envelope_id: str, loader):
    matches = [row["object_attrs"] for row in rows if row["object_attrs"].get("envelope_id") == envelope_id]
    if not matches:
        return None
    matches.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
    return loader(matches[0])


def run_skill(args: argparse.Namespace) -> int:
    if args.skill_command == "propose":
        prompt = args.text if args.text is not None else resolve_prompt(args.prompt)
        if args.family == "observation-digestion":
            service = ObservationDigestProposalService()
            result = service.propose(
                prompt,
                root_path=args.root_path,
                relative_path=args.relative_path,
                source_runtime=args.source_runtime,
                format_hint=args.format_hint,
                vendor_hint=args.vendor_hint,
            )
            if args.json:
                print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
            else:
                print(service.render_proposal_summary(result))
            return 0 if result.status in {"proposal_created", "partial", "needs_more_input"} else 1
        service = SkillProposalRouterService()
        result = service.propose_from_prompt(
            user_prompt=prompt,
            root_path=args.root_path,
            relative_path=args.relative_path,
            recursive=True if args.recursive else None,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_proposal_summary(result))
        return 0 if result.status in {"proposal_available", "incomplete"} else 1
    if args.skill_command == "review":
        if not args.from_proposal_json_file:
            if args.proposal_id:
                print(
                    "[skill proposal review error: proposal persistence is not available; "
                    "use --from-proposal-json-file]",
                    file=sys.stderr,
                )
            else:
                print(
                    "[skill proposal review error: --from-proposal-json-file is required]",
                    file=sys.stderr,
                )
            return 1
        proposal, proposal_exit_code = _load_proposal_json_file(args.from_proposal_json_file)
        if proposal is None:
            return proposal_exit_code
        service = SkillProposalReviewService()
        result = service.review_proposal(
            proposal=proposal,
            decision=normalize_review_decision(args.decision),
            reviewer_type=args.reviewer_type,
            reviewer_id=args.reviewer_id,
            reason=args.reason,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_review_summary(result))
        return 0 if result.status in {"approved", "rejected", "no_action", "needs_more_input", "revise_proposal", "needs_review"} else 1
    if args.skill_command == "bridge":
        loaded, load_exit_code = _load_bridge_inputs(args)
        if loaded is None:
            return load_exit_code
        proposal, review_decision, review_result = loaded
        service = ReviewedExecutionBridgeService()
        result = service.bridge_reviewed_proposal(
            proposal=proposal,
            review_decision=review_decision,
            review_result=review_result,
            invocation_mode="explicit_cli",
            requester_type="cli",
            requester_id="chanta-cli",
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_bridge_summary(result))
        return 0 if result.executed else 1
    if args.skill_command not in {"run", "gate-run"}:
        print("skill command is required", file=sys.stderr)
        return 1
    skill_id = args.skill_id_option or args.skill_id
    if not skill_id:
        print("[explicit skill invocation error: skill_id is required]", file=sys.stderr)
        return 1
    payload, payload_exit_code = _load_skill_input_payload(args)
    if payload is None:
        return payload_exit_code
    if args.root_path:
        payload["root_path"] = args.root_path
    if args.relative_path:
        payload["relative_path"] = args.relative_path
    if args.recursive:
        payload["recursive"] = True
    if args.max_results is not None:
        payload["max_results"] = args.max_results
    if args.skill_command == "gate-run":
        service = SkillExecutionGateService()
        result = service.gate_explicit_invocation(
            skill_id=skill_id,
            input_payload=payload,
            invocation_mode="explicit_cli",
            requester_type="cli",
            requester_id="chanta-cli",
        )
        print(service.render_gate_summary(result))
        return 0 if result.executed else 1
    service = ExplicitSkillInvocationService()
    result = service.invoke_explicit_skill(
        skill_id=skill_id,
        input_payload=payload,
        invocation_mode="explicit_cli",
        requester_type="cli",
        requester_id="chanta-cli",
    )
    print(service.render_invocation_summary(result))
    return 0 if result.status == "completed" else 1


def run_skills(args: argparse.Namespace) -> int:
    if args.skills_command == "registry":
        return run_skill_registry(args)
    if args.skills_command == "propose":
        prompt = args.text if args.text is not None else resolve_prompt(args.prompt)
        if args.family == "observation-digestion":
            service = ObservationDigestProposalService()
            result = service.propose(
                prompt,
                root_path=args.root_path,
                relative_path=args.relative_path,
                source_runtime=args.source_runtime,
                format_hint=args.format_hint,
                vendor_hint=args.vendor_hint,
            )
            if args.json:
                print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
            else:
                print(service.render_proposal_summary(result))
            return 0 if result.status in {"proposal_created", "partial", "needs_more_input"} else 1
        service = SkillProposalRouterService()
        result = service.propose_from_prompt(
            user_prompt=prompt,
            root_path=args.root_path,
            relative_path=args.relative_path,
            recursive=True if args.recursive else None,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_proposal_summary(result))
        return 0 if result.status in {"proposal_available", "incomplete"} else 1
    if args.skills_command != "onboarding" or not args.onboarding_command:
        print("skills onboarding command is required", file=sys.stderr)
        return 1
    service = InternalSkillOnboardingService()
    if args.onboarding_command == "list":
        descriptors = service.default_read_only_descriptor_candidates()
        if args.json:
            print(json.dumps([item.to_dict() for item in descriptors], ensure_ascii=False, sort_keys=True))
        else:
            print("Internal Skill Onboarding candidates")
            for item in descriptors:
                print(f"{item.skill_id} | {item.capability_category} | enabled_by_default=false")
        return 0
    if args.onboarding_command == "show":
        if args.skill_id not in DEFAULT_READ_ONLY_CANDIDATE_SKILL_IDS:
            print("[internal skill onboarding error: descriptor not found]", file=sys.stderr)
            return 1
        bundle = service.create_read_only_skill_contract_bundle(skill_id=args.skill_id)
        descriptor = bundle["descriptor"]
        if args.json:
            print(json.dumps(descriptor.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Internal Skill Descriptor")
            print(f"skill_id={descriptor.skill_id}")
            print(f"capability_category={descriptor.capability_category}")
            print(f"risk_class={descriptor.risk_class}")
            print("enabled_by_default=false")
            print("runtime_registered=false")
        return 0
    if args.onboarding_command == "check":
        if args.skill_id not in DEFAULT_READ_ONLY_CANDIDATE_SKILL_IDS:
            print("[internal skill onboarding error: descriptor not found]", file=sys.stderr)
            return 1
        bundle = service.create_read_only_skill_contract_bundle(skill_id=args.skill_id)
        result = service.validate_onboarding(**bundle, reviewer_type="cli", reviewer_id="chanta-cli")
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_onboarding_summary(result))
        return 0 if result.status in {"accepted", "needs_fix", "blocked", "rejected"} else 1
    if args.onboarding_command == "validate":
        try:
            raw = Path(args.descriptor_json_file).read_text(encoding="utf-8-sig")
            descriptor = descriptor_from_json(raw)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"[internal skill onboarding error: invalid descriptor JSON: {error}]", file=sys.stderr)
            return 1
        result = service.validate_onboarding(
            descriptor=descriptor,
            reviewer_type="cli",
            reviewer_id="chanta-cli",
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_onboarding_summary(result))
        return 0 if result.status in {"accepted", "needs_fix", "blocked", "rejected"} else 1
    print("unsupported skills onboarding command", file=sys.stderr)
    return 1


def run_skill_registry(args: argparse.Namespace) -> int:
    if not getattr(args, "registry_command", None):
        print("skills registry command is required", file=sys.stderr)
        return 1
    service = SkillRegistryViewService()
    service.build_registry_view()
    command = args.registry_command
    if command == "show":
        matches = [item for item in service.last_entries if item.skill_id == args.skill_id]
        service.record_result(command_name="show", entries=matches, status="completed" if matches else "not_found")
        if args.json:
            print(json.dumps([item.to_dict() for item in matches], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_registry_detail(args.skill_id))
        return 0 if matches else 1
    entries = list(service.last_entries)
    if command == "observation":
        entries = service.apply_filter(entries, skill_layer="internal_observation", limit=args.limit)
    elif command == "digestion":
        entries = service.apply_filter(entries, skill_layer="internal_digestion", limit=args.limit)
    elif command == "external-candidates":
        entries = service.apply_filter(entries, skill_layer="external_candidate", limit=args.limit)
    elif command == "list":
        entries = service.apply_filter(
            entries,
            skill_layer=args.skill_layer,
            skill_origin=args.skill_origin,
            risk_class=args.risk_class,
            status=args.status,
            enabled=_bool_arg(args.enabled),
            execution_enabled=_bool_arg(args.execution_enabled),
            limit=args.limit,
        )
    elif command in {"risk", "observability", "findings"}:
        entries = service.apply_filter(
            entries,
            skill_layer=args.skill_layer,
            skill_origin=args.skill_origin,
            risk_class=args.risk_class,
            status=args.status,
            enabled=_bool_arg(args.enabled),
            execution_enabled=_bool_arg(args.execution_enabled),
            limit=args.limit,
        )
    else:
        print("unsupported skills registry command", file=sys.stderr)
        return 1
    service.record_result(command_name=command, entries=entries)
    if args.json:
        payload: object
        if command == "findings":
            payload = [item.to_dict() for item in service.last_findings]
        else:
            payload = [item.to_dict() for item in entries]
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    elif command == "risk":
        print(service.render_registry_risk_view(entries))
    elif command == "observability":
        print(service.render_registry_observability_view(entries))
    elif command == "findings":
        print(service.render_registry_findings())
    else:
        print(service.render_registry_table(entries))
    return 0


def _bool_arg(value: str | None) -> bool | None:
    if value is None:
        return None
    return value == "true"


def run_execution(args: argparse.Namespace) -> int:
    if not args.execution_command:
        print("execution command is required", file=sys.stderr)
        return 1
    service = ExecutionAuditService(
        ocel_store=OCELStore(args.ocel_db) if getattr(args, "ocel_db", None) else None
    )
    kwargs = {
        "skill_id": getattr(args, "skill_id", None),
        "status": getattr(args, "status", None),
        "session_id": getattr(args, "session_id", None),
        "blocked": True if getattr(args, "blocked", False) else None,
        "failed": True if getattr(args, "failed", False) else None,
        "limit": getattr(args, "limit", None),
        "show_paths": bool(getattr(args, "show_paths", False)),
        "requested_by": "chanta-cli",
    }
    if args.execution_command == "list":
        result = service.query_envelopes(query_type="list", **kwargs)
        renderer = service.render_audit_table
    elif args.execution_command == "recent":
        result = service.recent_envelopes(**kwargs)
        renderer = service.render_audit_table
    elif args.execution_command == "audit":
        result = service.audit_envelopes(**kwargs)
        renderer = service.render_audit_table
    elif args.execution_command == "show":
        result = service.show_envelope(args.envelope_id, **kwargs)
        renderer = service.render_audit_detail
    else:
        print("unsupported execution command", file=sys.stderr)
        return 1
    if args.json:
        print(
            json.dumps(
                {
                    "result": result.to_dict(),
                    "record_views": [item.to_dict() for item in service.last_record_views],
                    "findings": [item.to_dict() for item in service.last_findings],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print(renderer(result))
    return 0 if result.status == "completed" else 1


def run_promotion(args: argparse.Namespace) -> int:
    if not args.promotion_command:
        print("promotion command is required", file=sys.stderr)
        return 1
    store = OCELStore(args.ocel_db) if getattr(args, "ocel_db", None) else OCELStore()
    service = ExecutionResultPromotionService(ocel_store=store)
    if args.promotion_command == "candidate-from-envelope":
        envelope, output_snapshot, outcome_summary, artifact_ref, exit_code = _load_promotion_envelope(args, store)
        if envelope is None:
            return exit_code
        result = service.create_candidate_from_envelope(
            envelope=envelope,
            output_snapshot=output_snapshot,
            outcome_summary=outcome_summary,
            artifact_ref=artifact_ref,
            target_kind=args.target,
            candidate_title=args.title,
            private=bool(args.private),
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "result": result.to_dict(),
                        "candidate": service.last_candidate.to_dict() if service.last_candidate else None,
                        "findings": [finding.to_dict() for finding in service.last_findings],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(service.render_promotion_cli(result))
        return 0 if result.status == "pending_review" else 1
    if args.promotion_command == "list":
        candidates = service.list_candidates(limit=args.limit)
        if args.json:
            print(json.dumps([candidate.to_dict() for candidate in candidates], ensure_ascii=False, sort_keys=True))
        else:
            if not candidates:
                print("Execution Result Promotion candidates: none")
            else:
                print("Execution Result Promotion candidates")
                for item in candidates:
                    print(f"{item.candidate_id} | {item.target_kind} | {item.review_status}")
        return 0
    if args.promotion_command == "show":
        candidate = service.show_candidate(args.candidate_id)
        if candidate is None:
            print("[promotion error: candidate not found]", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(candidate.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Execution Result Promotion Candidate")
            print(f"candidate_id={candidate.candidate_id}")
            print(f"target_kind={candidate.target_kind}")
            print(f"review_status={candidate.review_status}")
            print(f"canonical_promotion_enabled={str(candidate.canonical_promotion_enabled).lower()}")
        return 0
    if args.promotion_command == "review":
        candidate = service.show_candidate(args.candidate_id)
        if candidate is None:
            print("[promotion error: candidate not found]", file=sys.stderr)
            return 1
        result = service.review_candidate(
            candidate=candidate,
            decision=args.decision,
            reviewer_type=args.reviewer_type,
            reviewer_id=args.reviewer_id,
            reason=args.reason,
            requested_by="chanta-cli",
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "result": result.to_dict(),
                        "decision": service.last_decision.to_dict() if service.last_decision else None,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(service.render_promotion_cli(result))
        return 0 if result.status in {"approved_for_later_promotion", "rejected", "no_action", "needs_more_info", "archived"} else 1
    print("unsupported promotion command", file=sys.stderr)
    return 1


def _load_summary_result(store: OCELStore, summary_result_id: str):
    for row in store.fetch_objects_by_type("workspace_read_summary_result"):
        attrs = row["object_attrs"]
        if attrs.get("summary_result_id") == summary_result_id:
            return summary_result_from_dict(attrs)
    return None


def _latest_output_preview_for_envelope(store: OCELStore, envelope_id: str):
    rows = [
        row["object_attrs"]
        for row in store.fetch_objects_by_type("execution_output_snapshot")
        if row["object_attrs"].get("envelope_id") == envelope_id
    ]
    if not rows:
        return None, None
    rows.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
    return rows[0].get("output_preview") or {}, rows[0].get("output_snapshot_id")


def run_workspace_summary(args: argparse.Namespace) -> int:
    if not args.workspace_summary_command:
        print("workspace-summary command is required", file=sys.stderr)
        return 1
    store = OCELStore(args.ocel_db) if getattr(args, "ocel_db", None) else OCELStore()
    service = WorkspaceReadSummarizationService(ocel_store=store)
    if args.workspace_summary_command == "from-file":
        result = summarize_file_via_workspace_read(
            root_path=args.root_path,
            relative_path=args.relative_path,
            ocel_store=store,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(WorkspaceReadSummarizationService(ocel_store=store).render_summary_cli(result))
        return 0 if result.status == "completed" else 1
    if args.workspace_summary_command == "from-envelope":
        preview, output_snapshot_id = _latest_output_preview_for_envelope(store, args.envelope_id)
        if preview is None:
            print("[workspace-summary error: envelope output preview not found]", file=sys.stderr)
            return 1
        result = service.summarize_from_execution_output(
            output_preview=preview,
            input_kind=args.input_kind,
            envelope_id=args.envelope_id,
            output_snapshot_id=output_snapshot_id,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_summary_cli(result))
        return 0 if result.status == "completed" else 1
    if args.workspace_summary_command == "show":
        result = _load_summary_result(store, args.summary_result_id)
        if result is None:
            print("[workspace-summary error: summary result not found]", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_summary_cli(result))
        return 0
    if args.workspace_summary_command == "candidate":
        result = _load_summary_result(store, args.summary_result_id)
        if result is None:
            print("[workspace-summary error: summary result not found]", file=sys.stderr)
            return 1
        candidate = service.create_summary_candidate(result=result, target_kind=args.target)
        if args.json:
            print(json.dumps(candidate.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Workspace Read Summary Candidate")
            print(f"summary_candidate_id={candidate.summary_candidate_id}")
            print(f"review_status={candidate.review_status}")
            print("canonical_promotion_enabled=false")
        return 0
    print("unsupported workspace-summary command", file=sys.stderr)
    return 1


def run_observe(args: argparse.Namespace) -> int:
    if not args.observe_command:
        print("observe command is required", file=sys.stderr)
        return 1
    if args.observe_command == "run":
        return _run_observe_invocation(args)
    if args.observe_command == "spine":
        return _run_observe_spine(args)
    if args.observe_command == "adapters":
        return _run_observe_adapters(args)
    if args.observe_command == "propose":
        service = ObservationDigestProposalService()
        result = service.propose(
            args.text,
            root_path=args.root_path,
            relative_path=args.relative_path,
            source_runtime=args.source_runtime,
            format_hint=args.format_hint,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_proposal_summary(result))
        return 0 if result.status in {"proposal_created", "partial", "needs_more_input"} else 1
    service = ObservationService()
    if args.observe_command == "source-inspect":
        source = service.inspect_observation_source(
            root_path=args.root_path,
            relative_path=args.relative_path,
            source_runtime=args.runtime,
            format_hint=args.format_hint,
        )
        if args.json:
            print(json.dumps(source.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_observation_cli(source))
        return 0 if source.source_attrs.get("status") != "blocked" else 1
    if args.observe_command == "trace":
        source = service.inspect_observation_source(
            root_path=args.root_path,
            relative_path=args.relative_path,
            source_runtime=args.runtime,
            format_hint=args.format_hint,
        )
        if source.source_attrs.get("status") == "blocked":
            print(service.render_observation_cli(source))
            return 1
        try:
            raw_text = resolve_workspace_path(args.root_path, args.relative_path).read_text(encoding="utf-8-sig")
        except OSError as error:
            print(f"[observe error: {error}]", file=sys.stderr)
            return 1
        records = service.parse_generic_jsonl_records(raw_text)
        batch_id = new_agent_observation_batch_id()
        events = service.normalize_observation_records(
            records=records,
            batch_id=batch_id,
            source_runtime=args.runtime,
            source_format=args.format_hint,
        )
        batch = service.create_observation_batch(source=source, raw_record_count=len(records), normalized_events=events)
        run = service.create_observed_run(source=source, batch=batch, normalized_events=events)
        if args.json:
            print(json.dumps(run.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_observation_cli(run))
        return 0
    if args.observe_command == "infer":
        loaded = _load_json_object(args.observed_run_json_file)
        run = observed_run_from_dict(loaded)
        inference = service.infer_behavior(observed_run=run)
        if args.json:
            print(json.dumps(inference.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_observation_cli(inference))
        return 0
    if args.observe_command == "narrative":
        loaded = _load_json_object(args.inference_json_file)
        inference = inference_from_dict(loaded)
        run = observed_run_from_dict({"observed_run_id": inference.observed_run_id})
        narrative = service.create_process_narrative(observed_run=run, inference=inference)
        if args.json:
            print(json.dumps(narrative.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_observation_cli(narrative))
        return 0
    print("unsupported observe command", file=sys.stderr)
    return 1


def run_digest(args: argparse.Namespace) -> int:
    if not args.digest_command:
        print("digest command is required", file=sys.stderr)
        return 1
    if args.digest_command == "run":
        return _run_digest_invocation(args)
    if args.digest_command == "propose":
        service = ObservationDigestProposalService()
        result = service.propose(
            args.text,
            root_path=args.root_path,
            relative_path=args.relative_path,
            source_runtime=args.source_runtime,
            format_hint=args.format_hint,
            vendor_hint=args.vendor_hint,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_proposal_summary(result))
        return 0 if result.status in {"proposal_created", "partial", "needs_more_input"} else 1
    if args.digest_command == "adapter-build":
        return _run_digest_adapter_build(args)
    service = DigestionService()
    if args.digest_command == "source-inspect":
        descriptor = service.inspect_external_skill_source(
            root_path=args.root_path,
            relative_path=args.relative_path,
            vendor_hint=args.vendor_hint,
        )
        if args.json:
            print(json.dumps(descriptor.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_digestion_cli(descriptor))
        return 0 if descriptor.descriptor_attrs.get("status") != "blocked" else 1
    if args.digest_command == "inventory":
        static_service = ExternalSkillStaticDigestionService()
        descriptor = static_service.digestion_service.inspect_external_skill_source(
            root_path=args.root_path,
            relative_path=args.relative_path,
        )
        inventory = static_service.inspect_resource_inventory(
            root_path=args.root_path,
            relative_path=args.relative_path,
            source_descriptor=descriptor,
        )
        if args.json:
            print(json.dumps(inventory.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(static_service.render_static_digestion_cli(inventory))
        return 0 if inventory.inventory_attrs.get("status") != "blocked" else 1
    if args.digest_command == "static":
        static_service = ExternalSkillStaticDigestionService()
        report = static_service.create_static_digestion_report(
            root_path=args.root_path,
            relative_path=args.relative_path,
            vendor_hint=args.vendor_hint,
        )
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(static_service.render_static_digestion_cli(report))
        return 0 if report.status != "blocked" else 1
    if args.digest_command == "risk":
        static_service = ExternalSkillStaticDigestionService()
        report = static_service.create_static_digestion_report(
            root_path=args.root_path,
            relative_path=args.relative_path,
            vendor_hint=args.vendor_hint,
            create_candidate=False,
            create_adapter_hints=False,
        )
        payload = static_service.last_risk_profile or report
        if args.json:
            print(json.dumps(payload.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(static_service.render_static_digestion_cli(payload))
        return 0 if report.status != "blocked" else 1
    if args.digest_command == "report":
        static_service = ExternalSkillStaticDigestionService()
        report = static_service.create_static_digestion_report(
            root_path=args.root_path,
            relative_path=args.relative_path,
            vendor_hint=args.vendor_hint,
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "report": report.to_dict(),
                        "findings": [finding.to_dict() for finding in static_service.last_findings],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(static_service.render_static_digestion_cli(report))
        return 0 if report.status != "blocked" else 1
    if args.digest_command == "fingerprint":
        run = observed_run_from_dict(_load_json_object(args.observed_run_json_file))
        fingerprint = service.create_behavior_fingerprint(observed_run=run)
        if args.json:
            print(json.dumps(fingerprint.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_digestion_cli(fingerprint))
        return 0
    if args.digest_command == "assimilate":
        profile = (
            static_profile_from_dict(_load_json_object(args.static_profile_json_file))
            if args.static_profile_json_file
            else None
        )
        fingerprint = (
            fingerprint_from_dict(_load_json_object(args.fingerprint_json_file))
            if args.fingerprint_json_file
            else None
        )
        candidate = service.create_assimilation_candidate(
            static_profile=profile,
            behavior_fingerprint=fingerprint,
        )
        if args.json:
            print(json.dumps(candidate.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_digestion_cli(candidate))
        return 0
    if args.digest_command == "adapter-candidate":
        candidate = candidate_from_dict(_load_json_object(args.candidate_json_file))
        adapter = service.create_adapter_candidate(candidate=candidate)
        if args.json:
            print(json.dumps(adapter.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_digestion_cli(adapter))
        return 0
    print("unsupported digest command", file=sys.stderr)
    return 1


def _run_digest_adapter_build(args: argparse.Namespace) -> int:
    if not args.adapter_build_command:
        print("digest adapter-build command is required", file=sys.stderr)
        return 1
    service = ObservationToDigestionAdapterBuilderService()
    if args.adapter_build_command == "from-inference":
        inference = behavior_inference_v2_from_dict(_load_json_object(args.inference_json_file))
        result = service.build_from_behavior_inference(inference)
        if args.json:
            print(
                json.dumps(
                    {
                        "result": result.to_dict(),
                        "observed_capabilities": [item.to_dict() for item in service.last_observed_capabilities],
                        "target_skill_candidates": [item.to_dict() for item in service.last_target_candidates],
                        "adapter_candidates": [item.to_dict() for item in service.last_adapter_candidates],
                        "unsupported_features": [item.to_dict() for item in service.last_unsupported_features],
                        "findings": [item.to_dict() for item in service.last_findings],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(service.render_adapter_build_cli(result))
        return 0
    if args.adapter_build_command == "from-fingerprint":
        fingerprint = fingerprint_from_dict(_load_json_object(args.fingerprint_json_file))
        result = service.build_from_behavior_fingerprint(fingerprint)
        if args.json:
            print(
                json.dumps(
                    {
                        "result": result.to_dict(),
                        "observed_capabilities": [item.to_dict() for item in service.last_observed_capabilities],
                        "target_skill_candidates": [item.to_dict() for item in service.last_target_candidates],
                        "adapter_candidates": [item.to_dict() for item in service.last_adapter_candidates],
                        "unsupported_features": [item.to_dict() for item in service.last_unsupported_features],
                        "findings": [item.to_dict() for item in service.last_findings],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(service.render_adapter_build_cli(result))
        return 0
    if args.adapter_build_command == "from-observed-run":
        observed_run = observed_run_from_dict(_load_json_object(args.observed_run_json_file))
        result = service.build_from_observed_run(observed_run)
        if args.json:
            print(
                json.dumps(
                    {
                        "result": result.to_dict(),
                        "observed_capabilities": [item.to_dict() for item in service.last_observed_capabilities],
                        "target_skill_candidates": [item.to_dict() for item in service.last_target_candidates],
                        "adapter_candidates": [item.to_dict() for item in service.last_adapter_candidates],
                        "unsupported_features": [item.to_dict() for item in service.last_unsupported_features],
                        "findings": [item.to_dict() for item in service.last_findings],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(service.render_adapter_build_cli(result))
        return 0
    if args.adapter_build_command == "show":
        print("adapter_candidate_id=" + args.adapter_candidate_id)
        print("review_status=unknown")
        print("canonical_import_enabled=false")
        print("execution_enabled=false")
        print("note=show is read-only and requires a current build context or OCEL query surface.")
        return 0
    if args.adapter_build_command == "unsupported":
        print("adapter_candidate_id=" + args.adapter_candidate_id)
        print("unsupported_features=unknown")
        print("note=unsupported is read-only and requires a current build context or OCEL query surface.")
        return 0
    print("unsupported digest adapter-build command", file=sys.stderr)
    return 1


def _run_observe_spine(args: argparse.Namespace) -> int:
    if not args.observe_spine_command:
        print("observe spine command is required", file=sys.stderr)
        return 1
    service = AgentObservationSpineService()
    command = args.observe_spine_command
    if command == "ontology":
        terms = service.register_movement_ontology_terms()
        service.record_result(
            operation_kind="spine_ontology",
            status="completed",
            created_object_refs=[term.ontology_term_id for term in terms],
            summary=f"Registered {len(terms)} movement ontology terms.",
        )
        if args.json:
            print(json.dumps([term.to_dict() for term in terms], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_ontology_cli())
        return 0
    if command == "adapters":
        adapters = service.register_adapter_profiles()
        if args.json:
            print(json.dumps([adapter.to_dict() for adapter in adapters], ensure_ascii=False, sort_keys=True))
        else:
            print("Agent Observation Adapter Profiles")
            for adapter in adapters:
                print(f"{adapter.adapter_name} | runtime={adapter.source_runtime} | implemented={str(adapter.implemented).lower()}")
            print("execution_enabled=false")
        return 0
    if command == "collectors":
        collectors = service.register_collector_contracts()
        if args.json:
            print(json.dumps([collector.to_dict() for collector in collectors], ensure_ascii=False, sort_keys=True))
        else:
            print("Agent Observation Collector Contracts")
            for collector in collectors:
                print(f"{collector.collector_kind} | implemented={str(collector.implemented).lower()} | enabled={str(collector.enabled).lower()}")
            print("live_sidecar_enabled=false")
            print("event_bus_enabled=false")
        return 0
    if command == "runtimes":
        runtime = service.register_runtime_descriptor()
        if args.json:
            print(json.dumps(runtime.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Agent Runtime Descriptor")
            print(f"runtime_descriptor_id={runtime.runtime_descriptor_id}")
            print(f"runtime_name={runtime.runtime_name}")
            print(f"supports_jsonl_transcript={str(runtime.supports_jsonl_transcript).lower()}")
        return 0
    if command == "normalize":
        event = _load_json_object(args.event_json_file)
        normalized = service.normalize_event_v2(event)
        if args.json:
            print(json.dumps(normalized.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_spine_summary(normalized))
        return 0
    if command == "infer":
        run = observed_run_from_dict(_load_json_object(args.observed_run_json_file))
        inference = service.create_behavior_inference_v2(observed_run=run)
        if args.json:
            print(json.dumps(inference.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_spine_summary(inference))
        return 0
    if command == "redaction-policy":
        policy = service.create_redaction_policy()
        if args.json:
            print(json.dumps(policy.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Observation Redaction Policy")
            print(f"redaction_policy_id={policy.redaction_policy_id}")
            print(f"redact_private_paths={str(policy.redact_private_paths).lower()}")
            print(f"redact_full_bodies={str(policy.redact_full_bodies).lower()}")
            print(f"redact_secrets={str(policy.redact_secrets).lower()}")
        return 0
    if command == "export-policy":
        policy = service.create_export_policy()
        if args.json:
            print(json.dumps(policy.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Observation Export Policy")
            print(f"export_policy_id={policy.export_policy_id}")
            print(f"allow_raw_transcript_export={str(policy.allow_raw_transcript_export).lower()}")
            print(f"allow_full_file_body_export={str(policy.allow_full_file_body_export).lower()}")
            print(f"require_redaction={str(policy.require_redaction).lower()}")
        return 0
    if command == "fleet-snapshot":
        snapshot = service.create_fleet_snapshot()
        if args.json:
            print(json.dumps(snapshot.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_fleet_snapshot_cli(snapshot))
        return 0
    print("unsupported observe spine command", file=sys.stderr)
    return 1


def _run_observe_adapters(args: argparse.Namespace) -> int:
    if not args.observe_adapters_command:
        print("observe adapters command is required", file=sys.stderr)
        return 1
    service = CrossHarnessTraceAdapterService()
    service.create_default_policy()
    command = args.observe_adapters_command
    if command == "list":
        contracts = service.register_adapter_contracts()
        if args.json:
            print(json.dumps([item.to_dict() for item in contracts], ensure_ascii=False, sort_keys=True))
        else:
            print("Cross-Harness Trace Adapters")
            for item in contracts:
                print(f"{item.adapter_name} | runtime={item.source_runtime} | implemented={str(item.implemented).lower()} | read_only=true")
        return 0
    if command == "show":
        contracts = service.register_adapter_contracts()
        contract = next((item for item in contracts if item.adapter_name == args.adapter_name), None)
        if contract is None:
            print("[observe adapters error: adapter not found]", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(contract.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_adapter_cli(contract))
        return 0
    if command == "inspect-source":
        inspection = service.inspect_trace_source(root_path=args.root_path, relative_path=args.relative_path, runtime_hint=args.runtime_hint)
        if args.json:
            print(json.dumps(inspection.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_adapter_cli(inspection))
        return 0 if inspection.inspection_attrs.get("status") != "blocked" else 1
    if command == "plan":
        inspection = service.inspect_trace_source(root_path=args.root_path, relative_path=args.relative_path, runtime_hint=args.runtime_hint)
        plan = service.build_normalization_plan(inspection)
        payload = {
            "status": "planned",
            "adapter_name": plan.plan_attrs.get("adapter_name"),
            "source_runtime": plan.source_runtime,
            "summary": f"mapping_rules={len(plan.selected_mapping_rule_ids)}",
        }
        if args.json:
            print(json.dumps(plan.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_adapter_cli(payload))
        return 0
    if command == "normalize":
        result = service.normalize_file(root_path=args.root_path, relative_path=args.relative_path, runtime_hint=args.runtime_hint)
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_adapter_cli(result))
        return 0 if result.status == "completed" else 1
    if command == "mapping-rules":
        rules = [rule for rule in service.register_default_mapping_rules() if rule.adapter_name == args.adapter_name]
        if args.json:
            print(json.dumps([item.to_dict() for item in rules], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_mapping_rules_cli(args.adapter_name))
        return 0 if rules else 1
    if command == "coverage":
        try:
            report = service.create_adapter_coverage_report(args.adapter_name)
        except ValueError as error:
            print(f"[observe adapters error: {error}]", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_coverage_cli(report))
        return 0
    print("unsupported observe adapters command", file=sys.stderr)
    return 1


def _print_invocation_result(
    service: ObservationDigestSkillInvocationService,
    result,
    *,
    as_json: bool,
) -> int:
    if as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
    else:
        print(service.render_invocation_cli(result))
    return 0 if result.executed and not result.blocked else 1


def _run_observe_invocation(args: argparse.Namespace) -> int:
    if not args.observe_run_command:
        print("observe run command is required", file=sys.stderr)
        return 1
    service = ObservationDigestSkillInvocationService()
    command = args.observe_run_command
    payload: dict[str, object] = {}
    skill_id = ""
    if command == "source-inspect":
        skill_id = "skill:agent_observation_source_inspect"
        payload = {
            "root_path": args.root_path,
            "relative_path": args.relative_path,
            "format_hint": args.format_hint,
        }
    elif command == "trace":
        skill_id = "skill:agent_trace_observe"
        payload = {
            "root_path": args.root_path,
            "relative_path": args.relative_path,
            "source_runtime": args.source_runtime,
            "format_hint": args.format_hint,
        }
    elif command == "normalize":
        skill_id = "skill:agent_observation_normalize"
        loaded = _load_json_object(args.batch_json_file)
        records = loaded.get("records", loaded.get("raw_records"))
        payload = {
            "records": records if isinstance(records, list) else [],
            "batch_id": loaded.get("batch_id"),
            "source_runtime": loaded.get("source_runtime", "unknown"),
            "format_hint": loaded.get("format_hint", loaded.get("source_format", "generic_jsonl")),
        }
    elif command == "infer":
        skill_id = "skill:agent_behavior_infer"
        payload = {"observed_run": _load_json_object(args.observed_run_json_file)}
    elif command == "narrative":
        skill_id = "skill:agent_process_narrative"
        inference = _load_json_object(args.inference_json_file)
        payload = {
            "inference": inference,
            "observed_run": {"observed_run_id": inference.get("observed_run_id")},
        }
    else:
        print("unsupported observe run command", file=sys.stderr)
        return 1
    result = service.invoke_skill(skill_id=skill_id, input_payload=payload)
    return _print_invocation_result(service, result, as_json=bool(args.json))


def _run_digest_invocation(args: argparse.Namespace) -> int:
    if not args.digest_run_command:
        print("digest run command is required", file=sys.stderr)
        return 1
    service = ObservationDigestSkillInvocationService()
    command = args.digest_run_command
    payload: dict[str, object] = {}
    skill_id = ""
    if command == "source-inspect":
        skill_id = "skill:external_skill_source_inspect"
        payload = {
            "root_path": args.root_path,
            "relative_path": args.relative_path,
            "vendor_hint": args.vendor_hint,
        }
    elif command == "static":
        skill_id = "skill:external_skill_static_digest"
        payload = {
            "root_path": args.root_path,
            "relative_path": args.relative_path,
            "vendor_hint": args.vendor_hint,
        }
    elif command == "fingerprint":
        skill_id = "skill:external_behavior_fingerprint"
        payload = {"observed_run": _load_json_object(args.observed_run_json_file)}
    elif command == "assimilate":
        skill_id = "skill:external_skill_assimilate"
        if args.static_profile_json_file:
            payload["static_profile"] = _load_json_object(args.static_profile_json_file)
        if args.fingerprint_json_file:
            payload["fingerprint"] = _load_json_object(args.fingerprint_json_file)
    elif command == "adapter-candidate":
        skill_id = "skill:external_skill_adapter_candidate"
        payload = {"candidate": _load_json_object(args.candidate_json_file)}
    else:
        print("unsupported digest run command", file=sys.stderr)
        return 1
    result = service.invoke_skill(skill_id=skill_id, input_payload=payload)
    return _print_invocation_result(service, result, as_json=bool(args.json))


def run_observe_digest(args: argparse.Namespace) -> int:
    if args.observe_digest_command == "ecosystem":
        return _run_observe_digest_ecosystem(args)
    if args.observe_digest_command != "conformance" or not args.conformance_command:
        print("observe-digest conformance command is required", file=sys.stderr)
        return 1
    service = ObservationDigestConformanceService()
    if args.conformance_command in {"run", "report"}:
        report = service.run_conformance(
            skill_id=getattr(args, "skill_id", None),
            run_smoke=bool(getattr(args, "smoke", False)),
            fixture_root=getattr(args, "fixture_root", None),
        )
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_conformance_cli(report))
        return 0 if report.status == "passed" else 1
    if args.conformance_command == "check-skill":
        report = service.run_conformance(skill_id=args.skill_id)
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_conformance_cli(report))
        return 0 if report.status == "passed" else 1
    if args.conformance_command == "smoke":
        results = service.run_smoke(
            skill_id=getattr(args, "skill_id", None),
            fixture_root=getattr(args, "fixture_root", None),
        )
        if args.json:
            print(json.dumps([item.to_dict() for item in results], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_smoke_cli(results))
        return 0 if all(item.passed for item in results) else 1
    if args.conformance_command == "findings":
        report = service.run_conformance()
        findings = service.last_findings[: max(0, int(args.limit))]
        if args.json:
            print(json.dumps([item.to_dict() for item in findings], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_conformance_cli(report))
            for finding in findings:
                print(f"- {finding.skill_id or ''} {finding.finding_type} severity={finding.severity}")
        return 0 if report.status == "passed" else 1
    print("unsupported observe-digest conformance command", file=sys.stderr)
    return 1


def _run_observe_digest_ecosystem(args: argparse.Namespace) -> int:
    if not args.ecosystem_command:
        print("observe-digest ecosystem command is required", file=sys.stderr)
        return 1
    service = ObservationDigestionEcosystemConsolidationService()
    report = service.consolidate()
    command = args.ecosystem_command
    limit = max(0, int(getattr(args, "limit", 20)))
    if command == "snapshot":
        payload = service.last_snapshot
        if args.json:
            print(json.dumps(payload.to_dict() if payload else {}, ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_ecosystem_summary())
        return 0
    if command == "components":
        items = service.last_components[:limit]
        if args.json:
            print(json.dumps([item.to_dict() for item in items], ensure_ascii=False, sort_keys=True))
        else:
            print("Observation/Digestion Ecosystem Components")
            for item in items:
                print(f"- {item.component_kind}: {item.component_name} readiness={item.readiness_level}")
        return 0
    if command == "capabilities":
        if args.json:
            print(json.dumps([item.to_dict() for item in service.last_capability_maps[:limit]], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_capability_map_cli(limit=limit))
        return 0
    if command == "safety":
        safety = service.last_safety_report
        if args.json:
            print(json.dumps(safety.to_dict() if safety else {}, ensure_ascii=False, sort_keys=True))
        else:
            assert safety is not None
            print("Observation/Digestion Safety Boundary")
            print(f"external_harness_execution_allowed={str(safety.external_harness_execution_allowed).lower()}")
            print(f"external_script_execution_allowed={str(safety.external_script_execution_allowed).lower()}")
            print(f"shell_allowed={str(safety.shell_allowed).lower()}")
            print(f"network_allowed={str(safety.network_allowed).lower()}")
            print(f"write_allowed={str(safety.write_allowed).lower()}")
            print(f"mcp_allowed={str(safety.mcp_allowed).lower()}")
            print(f"plugin_allowed={str(safety.plugin_allowed).lower()}")
            print(f"memory_mutation_allowed={str(safety.memory_mutation_allowed).lower()}")
            print(f"persona_mutation_allowed={str(safety.persona_mutation_allowed).lower()}")
            print(f"overlay_mutation_allowed={str(safety.overlay_mutation_allowed).lower()}")
        return 0
    if command == "gaps":
        if args.json:
            print(json.dumps([item.to_dict() for item in service.last_gap_registers[:limit]], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_gap_register_cli(limit=limit))
        return 0
    if command == "manifest":
        manifest = service.last_release_manifest
        if args.json:
            print(json.dumps(manifest.to_dict() if manifest else {}, ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_release_manifest_cli())
        return 0
    if command == "report":
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_ecosystem_summary())
            print(f"report_status={report.status}")
            print(f"future_gap_count={len(service.last_gap_registers)}")
        return 0
    print("unsupported observe-digest ecosystem command", file=sys.stderr)
    return 1


def run_self_awareness(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_command", None)
    if not command:
        print("self-awareness command is required", file=sys.stderr)
        return 1
    registry = SelfAwarenessRegistryService()
    conformance = SelfAwarenessConformanceService(registry)
    reports = SelfAwarenessReportService(registry_service=registry, conformance_service=conformance)
    if command == "registry":
        contracts = registry.list_contracts()
        summary = registry.summarize_layer()
        if args.json:
            print(
                json.dumps(
                    {
                        "summary": summary,
                        "contracts": [item.to_dict() for item in contracts],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print("Self-Awareness Registry")
            print("layer=self_awareness")
            print(f"state={summary['state']}")
            print(f"contract_count={len(contracts)}")
            print(f"implemented_count={summary['implemented_count']}")
            print(f"read_only_observation_count={summary['read_only_observation_count']}")
            print(f"execution_enabled_count={summary['execution_enabled_count']}")
            print(f"canonical_mutation_enabled_count={summary['canonical_mutation_enabled_count']}")
            print(f"dangerous_capability_count={summary['dangerous_capability_count']}")
            print(f"write_mutation_count={summary['write_mutation_count']}")
            print(f"shell_usage_count={summary['shell_usage_count']}")
            print(f"network_usage_count={summary['network_usage_count']}")
            print(f"memory_mutation_count={summary['memory_mutation_count']}")
            print(f"persona_mutation_count={summary['persona_mutation_count']}")
            print(f"overlay_mutation_count={summary['overlay_mutation_count']}")
            for item in contracts:
                print(
                    f"- {item.skill_id} layer={item.layer} "
                    f"implementation_status={item.implementation_status} "
                    f"effect_type={item.effect_type} "
                    f"execution_enabled={str(item.execution_enabled).lower()}"
                )
        return 0
    if command == "show":
        contract = registry.get_contract(args.skill_id)
        if contract is None:
            print("Self-Awareness Contract\nstatus=not_found", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(contract.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print("Self-Awareness Contract")
            print(f"skill_id={contract.skill_id}")
            print(f"layer={contract.layer}")
            print(f"state={contract.capability.state}")
            print(f"implementation_status={contract.implementation_status}")
            print(f"effect_type={contract.effect_type}")
            print(f"execution_enabled={str(contract.execution_enabled).lower()}")
            print(f"canonical_mutation_enabled={str(contract.canonical_mutation_enabled).lower()}")
            print(f"read_only={str(contract.risk_profile.read_only).lower()}")
            print(f"dangerous_capability={str(contract.risk_profile.dangerous_capability).lower()}")
        return 0
    if command == "conformance":
        report = conformance.run_conformance()
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(conformance.render_conformance_cli(report))
        return 0 if report.passed else 1
    if command == "pig-report":
        report = reports.build_pig_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        else:
            print(reports.render_pig_report_cli())
        return 0
    if command == "ocpx-projection":
        projection = reports.build_ocpx_projection()
        if args.json:
            print(json.dumps(projection, ensure_ascii=False, sort_keys=True))
        else:
            print(reports.render_ocpx_projection_cli())
        return 0
    if command in {"workbench", "status", "audit", "coverage"}:
        return _run_self_awareness_workbench(args)
    if command in {
        "consolidate",
        "release-manifest",
        "gap-register",
        "safety-report",
        "capability-map",
        "coverage-matrix",
    }:
        return _run_self_awareness_consolidation(args)
    if command == "workspace":
        return _run_self_awareness_workspace(args)
    if command == "text":
        return _run_self_awareness_text(args)
    if command == "search":
        return _run_self_awareness_search(args)
    if command == "summarize":
        return _run_self_awareness_summarize(args)
    if command == "project":
        return _run_self_awareness_project(args)
    if command == "verify":
        return _run_self_awareness_verify(args)
    if command == "intention":
        return _run_self_awareness_intention(args)
    print("unsupported self-awareness command", file=sys.stderr)
    return 1


def _run_self_awareness_workbench(args: argparse.Namespace) -> int:
    section = getattr(args, "self_awareness_workbench_alias_section", None) or getattr(args, "section", "overview")
    request = SelfAwarenessWorkbenchRequest(section=section, max_recent_items=getattr(args, "limit", 20)).normalized()
    service = SelfAwarenessWorkbenchService()
    snapshot = service.build_snapshot(request)
    if args.json:
        print(json.dumps(snapshot.to_dict(), ensure_ascii=False, sort_keys=True))
    else:
        print(service.render_cli(snapshot, section=section))
    return 0


def _run_self_awareness_consolidation(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_command", "consolidate")
    service = SelfAwarenessConsolidationService()
    report = service.consolidate()
    if args.json:
        payload: dict[str, object]
        if command == "release-manifest":
            payload = service.last_release_manifest.to_dict() if service.last_release_manifest else {}
        elif command == "gap-register":
            payload = service.last_gap_register.to_dict() if service.last_gap_register else {}
        elif command == "safety-report":
            payload = service.last_safety_report.to_dict() if service.last_safety_report else {}
        elif command == "capability-map":
            payload = service.last_capability_map.to_dict() if service.last_capability_map else {}
        elif command == "coverage-matrix":
            payload = service.last_coverage_matrix.to_dict() if service.last_coverage_matrix else {}
        else:
            payload = report.to_dict()
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(service.render_cli(command))
    return 0


def _run_self_awareness_workspace(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_workspace_command", None)
    if not command:
        print("self-awareness workspace command is required", file=sys.stderr)
        return 1
    root_path = str(Path.cwd())
    path_policy = SelfWorkspacePathPolicyService(workspace_root=root_path)
    if command == "roots":
        roots = path_policy.list_workspace_roots()
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "root_id": item.root_id,
                            "display_name": item.display_name,
                            "source": item.source,
                            "is_primary": item.is_primary,
                            "is_private_boundary": item.is_private_boundary,
                            "path_ref": "<workspace-root>",
                            "effect": READ_ONLY_OBSERVATION_EFFECT,
                        }
                        for item in roots
                    ],
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print("Self-Workspace Roots")
            print(f"effect={READ_ONLY_OBSERVATION_EFFECT}")
            for item in roots:
                print(
                    f"- root_id={item.root_id} display_name={item.display_name} "
                    f"source={item.source} is_primary={str(item.is_primary).lower()} path_ref=<workspace-root>"
                )
        return 0
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    if command == "verify-path":
        payload = {"root_path": root_path, "input_path": args.input_path}
        gate_result = gate.gate_explicit_invocation(
            skill_id="skill:self_awareness_path_verify",
            input_payload=payload,
            invocation_mode="self_workspace_awareness_cli",
        )
        output = _last_invocation_output(invocation)
        if args.json:
            print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
        else:
            print("Self-Workspace Path Verification")
            print(f"effect={READ_ONLY_OBSERVATION_EFFECT}")
            print(f"gate_status={gate_result.status}")
            print(f"executed={str(gate_result.executed).lower()}")
            print(f"blocked={str(gate_result.blocked).lower()}")
            print(f"input_path={args.input_path}")
            if output:
                print(f"within_workspace={str(output.get('within_workspace', False)).lower()}")
                print(f"finding_type={output.get('finding_type')}")
                print(f"reason={output.get('reason')}")
            elif gate.last_decision is not None:
                print(f"finding_type={gate.last_decision.decision_basis}")
                print(f"reason={gate.last_decision.reason}")
        return 0 if gate_result.executed else 1
    if command == "inventory":
        payload = {
            "root_path": root_path,
            "relative_path": args.relative_path,
            "max_depth": args.max_depth,
            "max_entries": args.max_entries,
            "include_hidden": bool(args.include_hidden),
            "include_ignored": bool(args.include_ignored),
        }
        gate_result = gate.gate_explicit_invocation(
            skill_id="skill:self_awareness_workspace_inventory",
            input_payload=payload,
            invocation_mode="self_workspace_awareness_cli",
        )
        output = _last_invocation_output(invocation)
        if args.json:
            print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
        else:
            print("Self-Workspace Inventory")
            print(f"effect={READ_ONLY_OBSERVATION_EFFECT}")
            print(f"gate_status={gate_result.status}")
            print(f"executed={str(gate_result.executed).lower()}")
            print(f"blocked={str(gate_result.blocked).lower()}")
            print(f"requested_path={args.relative_path}")
            print(f"truncated={str(output.get('truncated', False)).lower()}")
            print(f"total_entries_seen={output.get('total_entries_seen', 0)}")
            print(f"total_entries_returned={output.get('total_entries_returned', 0)}")
            print(f"excluded_count={output.get('excluded_count', 0)}")
            for item in list(output.get("entries") or [])[:20]:
                print(
                    f"- {item.get('relative_path')} type={item.get('entry_type')} "
                    f"depth={item.get('depth')} size_bytes={item.get('size_bytes')}"
                )
        return 0 if gate_result.executed else 1
    print("unsupported self-awareness workspace command", file=sys.stderr)
    return 1


def _last_invocation_output(invocation: ExplicitSkillInvocationService) -> dict:
    result = invocation.last_result
    if result is None:
        return {}
    output_payload = result.output_payload
    output_attrs = output_payload.get("output_attrs")
    return dict(output_attrs) if isinstance(output_attrs, dict) else {}


def _run_self_awareness_text(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_text_command", None)
    if command != "read":
        print("self-awareness text read command is required", file=sys.stderr)
        return 1
    root_path = str(Path.cwd())
    mode = "line_range" if args.mode == "preview" and (args.start_line or args.end_line) else args.mode
    payload = {
        "root_path": root_path,
        "path": args.path,
        "mode": mode,
        "start_line": args.start_line,
        "end_line": args.end_line,
        "max_bytes": args.max_bytes,
        "max_lines": args.max_lines,
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_text_read",
        input_payload=payload,
        invocation_mode="self_code_text_perception_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Code/Text Perception")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        result = output
        decision = result.get("policy_decision") if isinstance(result.get("policy_decision"), dict) else {}
        text_slice = result.get("slice") if isinstance(result.get("slice"), dict) else None
        print(f"path={args.path}")
        print(f"mode={decision.get('read_mode', args.mode)}")
        if text_slice:
            print(f"relative_path={text_slice.get('relative_path')}")
            print(f"line_range={text_slice.get('start_line')}-{text_slice.get('end_line')}")
            print(f"bytes_read={text_slice.get('bytes_read')}")
            print(f"lines_read={text_slice.get('lines_read')}")
            print(f"truncated={str(text_slice.get('truncated', False)).lower()}")
            print(f"redacted={str(text_slice.get('redacted', False)).lower()}")
            print("content:")
            print(text_slice.get("content", ""))
        else:
            print(f"finding_type={decision.get('finding_type', gate.last_decision.decision_basis if gate.last_decision else 'blocked')}")
            print(f"reason={decision.get('reason', gate.last_decision.reason if gate.last_decision else '')}")
            print("content_printed=false")
    return 0 if gate_result.executed else 1


def _run_self_awareness_search(args: argparse.Namespace) -> int:
    root_path = str(Path.cwd())
    payload = {
        "root_path": root_path,
        "query": args.query,
        "relative_path": args.relative_path,
        "include_globs": list(args.include_globs or []),
        "exclude_globs": list(args.exclude_globs or []),
        "case_sensitive": bool(args.case_sensitive),
        "match_mode": "literal",
        "context_lines": args.context_lines,
        "max_files": args.max_files,
        "max_matches": args.max_matches,
        "max_matches_per_file": args.max_matches_per_file,
        "max_bytes_per_file": args.max_bytes_per_file,
        "max_total_bytes": args.max_total_bytes,
        "include_hidden": bool(args.include_hidden),
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_workspace_search",
        input_payload=payload,
        invocation_mode="self_code_search_awareness_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Code Search Awareness")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        print(f"query={args.query}")
        decision = output.get("policy_decision") if isinstance(output.get("policy_decision"), dict) else {}
        print(f"mode={decision.get('effective_match_mode', 'literal')}")
        print(f"path={args.relative_path}")
        print(f"files_scanned={output.get('files_scanned', 0)}")
        print(f"files_skipped={output.get('files_skipped', 0)}")
        print(f"files_blocked={output.get('files_blocked', 0)}")
        print(f"match_count={len(output.get('matches') or [])}")
        print(f"truncated={str(output.get('truncated', False)).lower()}")
        if output.get("truncated_reason"):
            print(f"truncated_reason={output.get('truncated_reason')}")
        if gate_result.blocked:
            print(f"finding_type={decision.get('finding_type', gate.last_decision.decision_basis if gate.last_decision else 'blocked')}")
            print(f"reason={decision.get('reason', gate.last_decision.reason if gate.last_decision else '')}")
            print("content_printed=false")
        elif not output.get("matches"):
            print("matches=none")
        else:
            for match in output.get("matches") or []:
                snippet = match.get("snippet") if isinstance(match.get("snippet"), dict) else {}
                print(
                    f"- {match.get('relative_path')}:{match.get('line_number')} "
                    f"columns={match.get('column_start')}-{match.get('column_end')} "
                    f"redacted={str(snippet.get('redacted', False)).lower()}"
                )
                for line in snippet.get("before") or []:
                    print(f"  | {_safe_cli_text(line)}")
                print(f"  > {_safe_cli_text(snippet.get('line', ''))}")
                for line in snippet.get("after") or []:
                    print(f"  | {_safe_cli_text(line)}")
    return 0 if gate_result.executed else 1


def _run_self_awareness_summarize(args: argparse.Namespace) -> int:
    root_path = str(Path.cwd())
    mode = args.summary_mode
    skill_id = (
        "skill:self_awareness_python_symbols"
        if mode == "python"
        else "skill:self_awareness_markdown_structure"
    )
    payload = {
        "root_path": root_path,
        "path": args.path,
        "summary_mode": mode,
        "max_bytes": args.max_bytes,
        "max_lines": args.max_lines,
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id=skill_id,
        input_payload=payload,
        invocation_mode="self_structure_summarization_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Structure Summarization")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}+state_candidate_created")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        print(f"path={args.path}")
        print(f"candidate_id={output.get('candidate_id', '')}")
        print(f"summary_kind={output.get('summary_kind', mode)}")
        print(f"review_status={output.get('review_status', 'candidate_only')}")
        print(f"canonical_promotion_enabled={str(output.get('canonical_promotion_enabled', False)).lower()}")
        print(f"promoted={str(output.get('promoted', False)).lower()}")
        decision = output.get("policy_decision") if isinstance(output.get("policy_decision"), dict) else {}
        if gate_result.blocked:
            print(f"finding_type={decision.get('finding_type', gate.last_decision.decision_basis if gate.last_decision else 'blocked')}")
            print(f"reason={decision.get('reason', gate.last_decision.reason if gate.last_decision else '')}")
            print("content_printed=false")
        elif output.get("markdown"):
            markdown = output["markdown"]
            print(f"heading_count={markdown.get('heading_count', 0)}")
            print(f"max_heading_depth={markdown.get('max_heading_depth', 0)}")
            print(f"frontmatter_keys={','.join(markdown.get('frontmatter_keys') or [])}")
            for item in markdown.get("headings") or []:
                print(f"- h{item.get('level')} line={item.get('line_number')} title={_safe_cli_text(item.get('title', ''))}")
        elif output.get("python"):
            python = output["python"]
            print(f"import_count={len(python.get('imports') or [])}")
            print(f"function_count={len(python.get('top_level_functions') or [])}")
            print(f"class_count={len(python.get('top_level_classes') or [])}")
            print(f"assignment_count={len(python.get('top_level_assignments') or [])}")
            if python.get("parse_error"):
                print(f"parse_error={_safe_cli_text(python.get('parse_error'))}")
        elif output.get("shallow_keys"):
            shallow = output["shallow_keys"]
            print(f"file_kind={shallow.get('file_kind')}")
            print(f"top_level_keys={','.join(shallow.get('top_level_keys') or [])}")
            if shallow.get("parse_error"):
                print(f"parse_error={_safe_cli_text(shallow.get('parse_error'))}")
        elif output.get("plain_text"):
            preview = output["plain_text"]
            print(f"line_count_seen={preview.get('line_count_seen', 0)}")
            print(f"truncated={str(preview.get('truncated', False)).lower()}")
            print(f"redacted={str(preview.get('redacted', False)).lower()}")
            for line in preview.get("first_non_empty_lines") or []:
                print(f"- {_safe_cli_text(line)}")
    return 0 if gate_result.executed else 1


def _run_self_awareness_project(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_project_command", None)
    if command != "structure":
        print("self-awareness project structure command is required", file=sys.stderr)
        return 1
    root_path = str(Path.cwd())
    payload = {
        "root_path": root_path,
        "relative_path": args.relative_path,
        "max_depth": args.max_depth,
        "max_entries": args.max_entries,
        "include_hidden": bool(args.include_hidden),
        "include_ignored": bool(args.include_ignored),
        "include_summary_candidates": not bool(args.no_summary_candidates),
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_project_structure",
        input_payload=payload,
        invocation_mode="self_project_structure_awareness_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Project Structure Awareness")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}+state_candidate_created")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        print(f"path={args.relative_path}")
        print(f"candidate_id={output.get('candidate_id', '')}")
        print(f"review_status={output.get('review_status', 'candidate_only')}")
        print(f"canonical_promotion_enabled={str(output.get('canonical_promotion_enabled', False)).lower()}")
        print(f"promoted={str(output.get('promoted', False)).lower()}")
        print(f"truncated={str(output.get('truncated', False)).lower()}")
        if output.get("truncated_reason"):
            print(f"truncated_reason={output.get('truncated_reason')}")
        decision = output.get("policy_decision") if isinstance(output.get("policy_decision"), dict) else {}
        if gate_result.blocked:
            print(f"finding_type={decision.get('finding_type', gate.last_decision.decision_basis if gate.last_decision else 'blocked')}")
            print(f"reason={decision.get('reason', gate.last_decision.reason if gate.last_decision else '')}")
            print("content_printed=false")
        else:
            distribution = output.get("file_distribution") if isinstance(output.get("file_distribution"), dict) else {}
            surfaces = list(output.get("surface_candidates") or [])
            nodes = list(output.get("tree_nodes") or [])
            print(f"tree_node_count={len(nodes)}")
            print(f"total_files={distribution.get('total_files', 0)}")
            print(f"total_dirs={distribution.get('total_dirs', 0)}")
            print(f"surface_candidate_count={len(surfaces)}")
            print("tree_preview:")
            for node in nodes[:20]:
                print(
                    f"- {node.get('relative_path')} type={node.get('node_type')} "
                    f"depth={node.get('depth')} kind={node.get('file_kind')}"
                )
            print("surface_candidates:")
            for item in surfaces[:20]:
                print(
                    f"- {item.get('candidate_type')} path={item.get('relative_path')} "
                    f"confidence={item.get('confidence')}"
                )
            print("content_printed=false")
    return 0 if gate_result.executed else 1


def _run_self_awareness_verify(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_verify_command", None)
    if command != "surface":
        print("self-awareness verify surface command is required", file=sys.stderr)
        return 1
    root_path = str(Path.cwd())
    payload_data = _load_json_object(args.target_payload) if getattr(args, "target_payload", None) else {}
    target_type = args.target_type or payload_data.get("target_type") or _infer_self_awareness_target_type(payload_data)
    target_id = args.target_id or payload_data.get("candidate_id") or payload_data.get("report_id") or payload_data.get("target_id")
    payload = {
        "root_path": root_path,
        "target_type": target_type,
        "target_id": target_id,
        "target_payload": payload_data,
        "strictness": args.strictness,
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_surface_verify",
        input_payload=payload,
        invocation_mode="self_surface_verification_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Surface Verification")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}+state_candidate_created")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        print(f"target_type={target_type}")
        print(f"target_id={target_id or ''}")
        print(f"status={output.get('status', 'blocked')}")
        print(f"report_id={output.get('report_id', '')}")
        print(f"review_status={output.get('review_status', 'candidate_only')}")
        print(f"canonical_promotion_enabled={str(output.get('canonical_promotion_enabled', False)).lower()}")
        print(f"promoted={str(output.get('promoted', False)).lower()}")
        findings = list(output.get("findings") or [])
        for severity in ["info", "warning", "error", "critical"]:
            print(f"{severity}_finding_count={sum(1 for item in findings if item.get('severity') == severity)}")
        evidence = output.get("evidence_coverage") if isinstance(output.get("evidence_coverage"), dict) else {}
        boundary = output.get("boundary_status") if isinstance(output.get("boundary_status"), dict) else {}
        candidate = output.get("candidate_status") if isinstance(output.get("candidate_status"), dict) else {}
        print(f"evidence_coverage={evidence.get('coverage_status', 'not_applicable')}")
        print(f"boundary_status={boundary.get('boundary_status', 'warning')}")
        print(f"candidate_status={candidate.get('candidate_status', 'warning')}")
        for item in findings[:10]:
            print(
                f"- severity={item.get('severity')} type={item.get('finding_type')} "
                f"message={_safe_cli_text(item.get('message', ''))}"
            )
        print("content_printed=false")
    return 0 if gate_result.executed else 1


def _run_self_awareness_intention(args: argparse.Namespace) -> int:
    command = getattr(args, "self_awareness_intention_command", None)
    if command != "candidates":
        print("self-awareness intention candidates command is required", file=sys.stderr)
        return 1
    root_path = str(Path.cwd())
    include_no_action = bool(args.include_no_action) or True
    request = SelfDirectedIntentionRequest(
        goal_text=args.goal_text,
        source_candidate_ids=list(args.source_candidate_ids or []),
        source_report_ids=list(args.source_report_ids or []),
        strictness=args.strictness,
        include_no_action=include_no_action,
    ).normalized()
    payload = {
        "root_path": root_path,
        **request.to_dict(),
    }
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    gate_result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_plan_candidate",
        input_payload=payload,
        invocation_mode="self_directed_intention_candidate_cli",
    )
    output = _last_invocation_output(invocation)
    if args.json:
        print(json.dumps({"gate": gate_result.to_dict(), "output": output}, ensure_ascii=False, sort_keys=True))
    else:
        print("Self-Directed Intention Candidate")
        print(f"effect={READ_ONLY_OBSERVATION_EFFECT}+state_candidate_created")
        print(f"gate_status={gate_result.status}")
        print(f"executed={str(gate_result.executed).lower()}")
        print(f"blocked={str(gate_result.blocked).lower()}")
        print(f"bundle_id={output.get('bundle_id', '')}")
        print(f"review_status={output.get('review_status', 'candidate_only')}")
        print(f"plan_candidate_count={len(output.get('plan_candidates') or [])}")
        print(f"todo_candidate_count={len(output.get('todo_candidates') or [])}")
        print(f"no_action_candidate_count={len(output.get('no_action_candidates') or [])}")
        print(f"needs_more_input_candidate_count={len(output.get('needs_more_input_candidates') or [])}")
        print(f"execution_enabled={str(output.get('execution_enabled', False)).lower()}")
        print(f"materialized={str(output.get('materialized', False)).lower()}")
        print(f"canonical_promotion_enabled={str(output.get('canonical_promotion_enabled', False)).lower()}")
        print(f"promoted={str(output.get('promoted', False)).lower()}")
        print("no_actual_execution_occurred=true")
        print("content_printed=false")
    return 0 if gate_result.executed else 1


def run_deep_self(args: argparse.Namespace) -> int:
    if not args.deep_self_command:
        print("deep-self command is required", file=sys.stderr)
        return 1
    registry = DeepSelfIntrospectionRegistryService()
    conformance = DeepSelfIntrospectionConformanceService(registry)
    reports = DeepSelfIntrospectionReportService(
        registry_service=registry,
        conformance_service=conformance,
    )
    if args.deep_self_command == "contract":
        contract = registry.build_contract()
        if args.json:
            print(json.dumps(contract.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(_render_deep_self_contract(contract.to_dict()))
        return 0
    if args.deep_self_command == "subjects":
        subjects = registry.list_subjects()
        if args.json:
            print(json.dumps([item.to_dict() for item in subjects], ensure_ascii=False, sort_keys=True))
        else:
            print(_render_deep_self_subjects([item.to_dict() for item in subjects]))
        return 0
    if args.deep_self_command == "show":
        subject = registry.get_subject(args.subject_id)
        if subject is None:
            print("Deep Self-Introspection subject\nstatus=not_found", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(subject.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(_render_deep_self_subject(subject.to_dict()))
        return 0
    if args.deep_self_command == "conformance":
        report = conformance.run_conformance()
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(conformance.render_conformance_cli())
        return 0 if report.passed else 1
    if args.deep_self_command == "pig-report":
        report = reports.build_pig_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        else:
            print(reports.render_pig_report_cli())
        return 0
    if args.deep_self_command == "ocpx-projection":
        projection = reports.build_ocpx_projection()
        if args.json:
            print(json.dumps(projection, ensure_ascii=False, sort_keys=True))
        else:
            print(reports.render_ocpx_projection_cli())
        return 0
    if args.deep_self_command == "capability":
        return _run_deep_self_capability(args)
    raise SystemExit(f"unsupported deep-self command: {args.deep_self_command}")


def _run_deep_self_capability(args: argparse.Namespace) -> int:
    if not args.deep_self_capability_command:
        print("deep-self capability command is required", file=sys.stderr)
        return 1
    service = SelfCapabilityRegistryAwarenessService()
    command = args.deep_self_capability_command
    if command == "registry":
        request = SelfCapabilityRegistryViewRequest(
            layer_filter=getattr(args, "layer_filter", None),
            status_filter=getattr(args, "status_filter", None),
        )
        snapshot = service.view_registry(request)
        if args.json:
            print(json.dumps(snapshot.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_cli("capability registry", snapshot=snapshot))
        return 0
    if command == "truth-check":
        claims = _load_claims(getattr(args, "claims", None))
        report = service.truth_check(optional_claims=claims)
        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_cli("capability truth-check", report=report))
        return 0 if report.status in {"passed", "warning"} else 1
    snapshot = service.view_registry()
    if command == "risks":
        if args.json:
            print(json.dumps([item.to_dict() for item in snapshot.risk_views], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_cli("capability risks", snapshot=snapshot))
        return 0
    if command == "observability":
        report = service.truth_check()
        if args.json:
            print(json.dumps([item.to_dict() for item in snapshot.observability_views], ensure_ascii=False, sort_keys=True))
        else:
            print(service.render_cli("capability observability", snapshot=snapshot, report=report))
        return 0
    raise SystemExit(f"unsupported deep-self capability command: {command}")


def _load_claims(path: str | None) -> list[dict[str, object]] | None:
    if not path:
        return None
    loaded = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(loaded, list) or not all(isinstance(item, dict) for item in loaded):
        raise SystemExit("claims file must contain a list of objects")
    return loaded


def _render_deep_self_contract(contract: dict[str, object]) -> str:
    risk = contract["risk_profile"]
    if not isinstance(risk, dict):
        risk = {}
    return "\n".join(
        [
            "Deep Self-Introspection Contract",
            f"version={contract.get('version', 'v0.21.0')}",
            "layer=deep_self_introspection",
            f"status={contract.get('status', 'contract_only')}",
            "read_only=True",
            "ocel_native=True",
            f"seed_subjects={','.join(item['subject_id'] for item in contract.get('subjects', []) if isinstance(item, dict))}",
            f"seed_skill_ids={','.join(str(item) for item in contract.get('seed_skill_ids', []))}",
            f"mutation_enabled={str(bool(risk.get('mutates_workspace') or risk.get('mutates_memory') or risk.get('mutates_persona') or risk.get('mutates_overlay')))}",
            f"execution_enabled={str(bool(risk.get('uses_shell') or risk.get('uses_network') or risk.get('uses_mcp') or risk.get('loads_plugin') or risk.get('executes_external_harness')))}",
            f"permission_escalation_enabled={str(bool(risk.get('grants_permission')))}",
            f"llm_judge_enabled={str(bool(risk.get('uses_llm_judge')))}",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
    )


def _render_deep_self_subjects(subjects: list[dict[str, object]]) -> str:
    lines = [
        "Deep Self-Introspection Subjects",
        "layer=deep_self_introspection",
        "status=contract_only",
        "read_only=True",
        "ocel_native=True",
    ]
    for subject in subjects:
        lines.append(f"- subject={subject.get('subject_id')} status={subject.get('status', 'contract_only')}")
    lines.extend(
        [
            "mutation_enabled=False",
            "execution_enabled=False",
            "permission_escalation_enabled=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
    )
    return "\n".join(lines)


def _render_deep_self_subject(subject: dict[str, object]) -> str:
    return "\n".join(
        [
            "Deep Self-Introspection Subject",
            "layer=deep_self_introspection",
            f"subject_id={subject.get('subject_id')}",
            f"status={subject.get('status', 'contract_only')}",
            "read_only=True",
            "ocel_native=True",
            f"required_source_objects={','.join(str(item) for item in subject.get('required_source_objects', []))}",
            f"required_read_models={','.join(str(item) for item in subject.get('required_read_models', []))}",
            "mutation_enabled=False",
            "execution_enabled=False",
            "permission_escalation_enabled=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
    )


def _safe_cli_text(value: object) -> str:
    text = str(value)
    encoding = sys.stdout.encoding or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def _infer_self_awareness_target_type(payload: dict) -> str:
    if not payload:
        return "self_awareness_layer"
    if "matches" in payload:
        return "workspace_search_result"
    if "tree_nodes" in payload or "surface_candidates" in payload:
        return "project_structure_candidate"
    if "markdown" in payload or "python" in payload or "summary_kind" in payload:
        return "structure_summary_candidate"
    if "entries" in payload and "total_entries_returned" in payload:
        return "workspace_inventory_report"
    if "slice" in payload or "policy_decision" in payload:
        return "text_read_result"
    return "self_awareness_layer"


def _load_json_object(path: str) -> dict:
    loaded = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(loaded, dict):
        raise SystemExit(f"JSON file must contain an object: {path}")
    return loaded


def run_workbench(args: argparse.Namespace) -> int:
    if not args.workbench_command:
        print("workbench command is required", file=sys.stderr)
        return 1
    store = OCELStore(args.ocel_db) if getattr(args, "ocel_db", None) else OCELStore()
    service = PersonalRuntimeWorkbenchService(ocel_store=store)
    snapshot = service.build_snapshot(limit=args.limit, show_paths=bool(args.show_paths))
    result = service.record_result(snapshot=snapshot, command_name=args.workbench_command)
    renderers = {
        "status": service.render_workbench_status,
        "recent": service.render_workbench_recent,
        "pending": service.render_workbench_pending,
        "blockers": service.render_workbench_blockers,
        "candidates": service.render_workbench_candidates,
        "summaries": service.render_workbench_summaries,
        "health": service.render_workbench_health,
    }
    if args.json:
        print(
            json.dumps(
                {
                    "snapshot": snapshot.to_dict(),
                    "result": result.to_dict(),
                    "panels": [item.to_dict() for item in service.last_panels],
                    "pending_items": [item.to_dict() for item in service.last_pending_items],
                    "recent_activities": [item.to_dict() for item in service.last_recent_activities],
                    "findings": [item.to_dict() for item in service.last_findings],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print(renderers[args.workbench_command](result))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        if not sys.stdin.isatty():
            return run_ask(parser.parse_args(["ask"]))
        parser.print_help()
        return 1

    if args.command == "ask":
        return run_ask(args)
    if args.command == "repl":
        return run_repl(args)
    if args.command == "show-config":
        return run_show_config()
    if args.command == "personal":
        return run_personal(args)
    if args.command == "skill":
        return run_skill(args)
    if args.command == "skills":
        return run_skills(args)
    if args.command == "execution":
        return run_execution(args)
    if args.command == "promotion":
        return run_promotion(args)
    if args.command == "workspace-summary":
        return run_workspace_summary(args)
    if args.command == "observe":
        return run_observe(args)
    if args.command == "digest":
        return run_digest(args)
    if args.command == "observe-digest":
        return run_observe_digest(args)
    if args.command == "self-awareness":
        return run_self_awareness(args)
    if args.command == "deep-self":
        return run_deep_self(args)
    if args.command == "workbench":
        return run_workbench(args)
    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

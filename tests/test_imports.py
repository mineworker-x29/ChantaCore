from chanta_core.agents.profile import AgentProfile
from chanta_core.delegation.packet import DelegationPacket
from chanta_core.editing import (
    EditProposal,
    EditProposalService,
    EditProposalStore,
    PatchApplication,
    PatchApplicationService,
    PatchApplicationStore,
    PatchApproval,
    PatchBackupService,
    create_unified_diff,
)
from chanta_core.instructions import (
    InstructionArtifact,
    InstructionService,
    ProjectRule,
    UserPreference,
    instruction_artifacts_to_history_entries,
    project_rules_to_history_entries,
    user_preferences_to_history_entries,
)
from chanta_core.context import (
    AutoCompactPolicy,
    AutoCompactRequest,
    AutoCompactResult,
    AutoCompactSummarizer,
    CollapsedContextManifest,
    ContextAssemblySnapshot,
    ContextAuditService,
    ContextCollapsePolicy,
    ContextBlock,
    ContextBlockSnapshot,
    ContextBudget,
    ContextReference,
    ContextHistoryBuilder,
    ContextHistoryEntry,
    ContextHistoryPolicy,
    ContextMessageSnapshot,
    ContextCompactionPipeline,
    ContextCompactionReadinessChecker,
    ContextCompactionReporter,
    ContextCompactionResult,
    ContextRenderer,
    ContextSnapshotPolicy,
    ContextSnapshotStore,
    MicrocompactPolicy,
    SessionContextPolicy,
    compact_activity_sequence,
    compact_json_like_text,
    compact_lines,
    compact_mapping,
    compact_report_text,
    make_preview,
    redact_sensitive_text,
)
from chanta_core.context.layers import (
    AutoCompactLayer,
    BudgetReductionLayer,
    ContextCollapseLayer,
    MicrocompactLayer,
    SnipLayer,
)
from chanta_core.llm import LLMClient
from chanta_core.memory.memory_record import MemoryRecord
from chanta_core.memory import (
    MemoryEntry,
    MemoryRevision,
    MemoryService,
    memory_entries_to_history_entries,
)
from chanta_core.missions.mission import Mission
from chanta_core.ocel.external_import import (
    ExternalOCELIngestionService,
    ExternalOCELNormalizer,
)
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.export import OCELExporter
from chanta_core.ocel.factory import OCELFactory
from chanta_core.ocel.importers import OCELImporter
from chanta_core.ocel.ingestion import OCELIngestionBatch, OCELIngestionResult
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.query import OCELQueryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.ocpx.variant import OCPXVariantSummary
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.artifacts import PIArtifact
from chanta_core.pig.assimilation import HumanPIAssimilator
from chanta_core.pig.diagnostics import PIGDiagnosticService
from chanta_core.pig.builder import PIGBuilder
from chanta_core.pig.conformance import (
    PIGConformanceIssue,
    PIGConformanceReport,
    PIGConformanceService,
)
from chanta_core.pig.context import PIGContext
from chanta_core.pig.evidence import PIEvidenceRef
from chanta_core.pig.feedback import PIGFeedbackService
from chanta_core.pig.guidance import PIGGuidance, PIGGuidanceService
from chanta_core.pig.inspector import PISubstrateInspection, PISubstrateInspector
from chanta_core.pig.models import PIGGraph
from chanta_core.pig.queue_conformance import (
    PIGQueueConformanceService,
    QueueConformanceIssue,
    QueueConformanceReport,
)
from chanta_core.pig.recommendations import PIGRecommendationService
from chanta_core.pig.reports import ProcessRunReport, PIGReportService
from chanta_core.pig.service import PIGService
from chanta_core.prompts.assembly import PromptAssemblyService
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.runtime.chat_service import ChatService
from chanta_core.runtime.decision import (
    DecisionContext,
    DecisionPolicy,
    DecisionScorer,
    DecisionService,
    ProcessDecision,
)
from chanta_core.repo import (
    RepoFileMatch,
    RepoScanner,
    RepoSearchResult,
    RepoSearchService,
    RepoSymbol,
    RepoSymbolScanner,
    RepoTextMatch,
)
from chanta_core.scheduler import (
    ProcessSchedule,
    ProcessScheduleStore,
    ScheduleEvaluation,
    ScheduleEvaluator,
    SchedulerRunner,
    SchedulerService,
)
from chanta_core.session import (
    AgentSession,
    ConversationTurn,
    SessionMessage,
    SessionService,
    session_messages_to_history_entries,
)
from chanta_core.runtime.loop import (
    ProcessActivityDecider,
    ProcessContextAssembler,
    ProcessObservation,
    ProcessRunEvaluator,
    ProcessRunLoop,
    ProcessRunPolicy,
    ProcessRunResult,
    ProcessRunState,
)
from chanta_core.skills.builtin import (
    create_apply_approved_patch_skill,
    builtin_llm_chat_skill,
    create_check_self_conformance_skill,
    create_echo_skill,
    create_ingest_human_pi_skill,
    create_inspect_ocel_recent_skill,
    create_llm_chat_skill,
    create_propose_file_edit_skill,
    create_run_worker_once_skill,
    create_run_scheduler_once_skill,
    create_summarize_pi_artifacts_skill,
    create_summarize_process_trace_skill,
    create_summarize_text_skill,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.errors import SkillRegistryError, SkillValidationError
from chanta_core.skills.executor import SkillExecutionPolicy, SkillExecutor
from chanta_core.skills.registry import SkillRegistry
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools import (
    Tool,
    ToolAuthorization,
    ToolAuthorizationError,
    ToolDispatchError,
    ToolDispatcher,
    ToolExecutionContext,
    ToolPolicy,
    ToolRegistry,
    ToolRegistryError,
    ToolRequest,
    ToolResult,
    ToolValidationError,
)
from chanta_core.tools.permission_rules import ToolPermissionRule, ToolPermissionRuleSet
from chanta_core.tools.permissions import ToolPermissionDecision
from chanta_core.tools.risk import ToolOperationRisk, ToolRiskClassifier
from chanta_core.tools.builtin.workspace import (
    create_workspace_tool,
    execute_workspace_tool,
)
from chanta_core.tools.builtin.repo import create_repo_tool, execute_repo_tool
from chanta_core.tools.builtin.edit import create_edit_tool, execute_edit_tool
from chanta_core.tools.builtin.worker import create_worker_tool, execute_worker_tool
from chanta_core.tools.builtin.scheduler import create_scheduler_tool, execute_scheduler_tool
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import (
    WorkspaceAccessError,
    WorkspaceConfig,
    WorkspaceInspector,
    WorkspacePathGuard,
)
from chanta_core.workers import (
    ProcessJob,
    ProcessJobInvalidTransitionError,
    ProcessJobStore,
    ProcessJobStateMachine,
    ProcessJobStateTransition,
    Worker,
    WorkerHeartbeat,
    WorkerHeartbeatStore,
    WorkerQueueService,
    WorkerRunner,
)


def test_required_imports() -> None:
    assert LLMClient is not None
    assert EditProposal is not None
    assert EditProposalService is not None
    assert EditProposalStore is not None
    assert PatchApproval is not None
    assert PatchApplication is not None
    assert PatchApplicationStore is not None
    assert PatchApplicationService is not None
    assert PatchBackupService is not None
    assert create_unified_diff is not None
    assert InstructionArtifact is not None
    assert InstructionService is not None
    assert ProjectRule is not None
    assert UserPreference is not None
    assert instruction_artifacts_to_history_entries is not None
    assert project_rules_to_history_entries is not None
    assert user_preferences_to_history_entries is not None
    assert ContextBlock is not None
    assert ContextBlockSnapshot is not None
    assert ContextAssemblySnapshot is not None
    assert ContextAuditService is not None
    assert AutoCompactPolicy is not None
    assert AutoCompactRequest is not None
    assert AutoCompactResult is not None
    assert AutoCompactSummarizer is not None
    assert ContextBudget is not None
    assert CollapsedContextManifest is not None
    assert ContextCollapsePolicy is not None
    assert ContextReference is not None
    assert ContextHistoryBuilder is not None
    assert ContextHistoryEntry is not None
    assert ContextHistoryPolicy is not None
    assert ContextMessageSnapshot is not None
    assert ContextCompactionPipeline is not None
    assert ContextCompactionReadinessChecker is not None
    assert ContextCompactionReporter is not None
    assert ContextCompactionResult is not None
    assert ContextRenderer is not None
    assert ContextSnapshotPolicy is not None
    assert ContextSnapshotStore is not None
    assert MicrocompactPolicy is not None
    assert SessionContextPolicy is not None
    assert compact_lines is not None
    assert compact_activity_sequence is not None
    assert compact_mapping is not None
    assert compact_json_like_text is not None
    assert compact_report_text is not None
    assert make_preview is not None
    assert redact_sensitive_text is not None
    assert BudgetReductionLayer is not None
    assert SnipLayer is not None
    assert MicrocompactLayer is not None
    assert ContextCollapseLayer is not None
    assert AutoCompactLayer is not None
    assert AgentRuntime is not None
    assert ChatService is not None
    assert ProcessActivityDecider is not None
    assert ProcessContextAssembler is not None
    assert ProcessObservation is not None
    assert ProcessRunEvaluator is not None
    assert ProcessRunLoop is not None
    assert ProcessRunPolicy is not None
    assert ProcessRunResult is not None
    assert ProcessRunState is not None
    assert AgentProfile is not None
    assert PromptAssemblyService is not None
    assert AgentEvent is not None
    assert TraceService is not None
    assert MemoryRecord is not None
    assert MemoryEntry is not None
    assert MemoryRevision is not None
    assert MemoryService is not None
    assert memory_entries_to_history_entries is not None
    assert Skill is not None
    assert SkillExecutionContext is not None
    assert SkillExecutionResult is not None
    assert SkillExecutionPolicy is not None
    assert SkillExecutor is not None
    assert SkillRegistryError is not None
    assert SkillValidationError is not None
    assert SkillRegistry is not None
    assert Tool is not None
    assert ToolAuthorization is not None
    assert ToolAuthorizationError is not None
    assert ToolDispatchError is not None
    assert ToolDispatcher is not None
    assert ToolExecutionContext is not None
    assert ToolPolicy is not None
    assert ToolRegistry is not None
    assert ToolRegistryError is not None
    assert ToolRequest is not None
    assert ToolResult is not None
    assert ToolValidationError is not None
    assert ToolPermissionDecision is not None
    assert ToolRiskClassifier is not None
    assert ToolOperationRisk is not None
    assert ToolPermissionRule is not None
    assert ToolPermissionRuleSet is not None
    assert create_workspace_tool is not None
    assert execute_workspace_tool is not None
    assert WorkspaceAccessError is not None
    assert WorkspaceConfig is not None
    assert WorkspaceInspector is not None
    assert WorkspacePathGuard is not None
    assert RepoFileMatch is not None
    assert RepoScanner is not None
    assert RepoSearchResult is not None
    assert RepoSearchService is not None
    assert RepoSymbol is not None
    assert RepoSymbolScanner is not None
    assert RepoTextMatch is not None
    assert create_repo_tool is not None
    assert execute_repo_tool is not None
    assert create_edit_tool is not None
    assert execute_edit_tool is not None
    assert create_worker_tool is not None
    assert execute_worker_tool is not None
    assert create_scheduler_tool is not None
    assert execute_scheduler_tool is not None
    assert ProcessSchedule is not None
    assert ProcessScheduleStore is not None
    assert ScheduleEvaluation is not None
    assert ScheduleEvaluator is not None
    assert SchedulerService is not None
    assert SchedulerRunner is not None
    assert AgentSession is not None
    assert ConversationTurn is not None
    assert SessionMessage is not None
    assert SessionService is not None
    assert session_messages_to_history_entries is not None
    assert ProcessJob is not None
    assert ProcessJobInvalidTransitionError is not None
    assert ProcessJobStore is not None
    assert ProcessJobStateMachine is not None
    assert ProcessJobStateTransition is not None
    assert Worker is not None
    assert WorkerHeartbeat is not None
    assert WorkerHeartbeatStore is not None
    assert WorkerQueueService is not None
    assert WorkerRunner is not None
    assert builtin_llm_chat_skill is not None
    assert create_apply_approved_patch_skill is not None
    assert create_check_self_conformance_skill is not None
    assert create_echo_skill is not None
    assert create_ingest_human_pi_skill is not None
    assert create_inspect_ocel_recent_skill is not None
    assert create_llm_chat_skill is not None
    assert create_propose_file_edit_skill is not None
    assert create_run_worker_once_skill is not None
    assert create_run_scheduler_once_skill is not None
    assert create_summarize_pi_artifacts_skill is not None
    assert create_summarize_process_trace_skill is not None
    assert create_summarize_text_skill is not None
    assert Mission is not None
    assert DelegationPacket is not None
    assert OCELObject is not None
    assert OCELEvent is not None
    assert OCELRelation is not None
    assert OCELRecord is not None
    assert OCELStore is not None
    assert OCELFactory is not None
    assert OCELExporter is not None
    assert OCELImporter is not None
    assert ExternalOCELSource is not None
    assert ExternalOCELNormalizer is not None
    assert ExternalOCELIngestionService is not None
    assert OCELIngestionBatch is not None
    assert OCELIngestionResult is not None
    assert OCELValidator is not None
    assert OCELQueryService is not None
    assert OCPXLoader is not None
    assert OCPXEngine is not None
    assert OCPXProcessView is not None
    assert OCPXVariantSummary is not None
    assert PIGService is not None
    assert PIGBuilder is not None
    assert PIGConformanceIssue is not None
    assert PIGConformanceReport is not None
    assert PIGConformanceService is not None
    assert PIGContext is not None
    assert PIGFeedbackService is not None
    assert PIGGuidance is not None
    assert PIGGuidanceService is not None
    assert PIGReportService is not None
    assert QueueConformanceIssue is not None
    assert QueueConformanceReport is not None
    assert PIGQueueConformanceService is not None
    assert PISubstrateInspection is not None
    assert PISubstrateInspector is not None
    assert ProcessRunReport is not None
    assert PIArtifact is not None
    assert PIArtifactStore is not None
    assert PIEvidenceRef is not None
    assert HumanPIAssimilator is not None
    assert PIGGraph is not None
    assert PIGDiagnosticService is not None
    assert PIGRecommendationService is not None
    assert DecisionContext is not None
    assert DecisionPolicy is not None
    assert ProcessDecision is not None
    assert DecisionScorer is not None
    assert DecisionService is not None
    assert utc_now_iso is not None

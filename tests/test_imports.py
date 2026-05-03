from chanta_core.agents.profile import AgentProfile
from chanta_core.delegation.packet import DelegationPacket
from chanta_core.llm import LLMClient
from chanta_core.memory.memory_record import MemoryRecord
from chanta_core.missions.mission import Mission
from chanta_core.ocel.external_import import (
    ExternalOCELIngestionService,
    ExternalOCELNormalizer,
)
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.factory import OCELFactory
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
    builtin_llm_chat_skill,
    create_check_self_conformance_skill,
    create_echo_skill,
    create_ingest_human_pi_skill,
    create_inspect_ocel_recent_skill,
    create_llm_chat_skill,
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
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def test_required_imports() -> None:
    assert LLMClient is not None
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
    assert builtin_llm_chat_skill is not None
    assert create_check_self_conformance_skill is not None
    assert create_echo_skill is not None
    assert create_ingest_human_pi_skill is not None
    assert create_inspect_ocel_recent_skill is not None
    assert create_llm_chat_skill is not None
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

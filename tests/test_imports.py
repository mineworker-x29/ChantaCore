from chanta_core.agents.profile import AgentProfile
from chanta_core.delegation.packet import DelegationPacket
from chanta_core.llm import LLMClient
from chanta_core.memory.memory_record import MemoryRecord
from chanta_core.missions.mission import Mission
from chanta_core.ocel.factory import OCELFactory
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.ocel.query import OCELQueryService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.diagnostics import PIGDiagnosticService
from chanta_core.pig.builder import PIGBuilder
from chanta_core.pig.models import PIGGraph
from chanta_core.pig.recommendations import PIGRecommendationService
from chanta_core.pig.service import PIGService
from chanta_core.prompts.assembly import PromptAssemblyService
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.runtime.chat_service import ChatService
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
from chanta_core.skills.skill import Skill
from chanta_core.skills.registry import SkillRegistry
from chanta_core.skills.builtin import builtin_llm_chat_skill
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
    assert SkillRegistry is not None
    assert builtin_llm_chat_skill is not None
    assert Mission is not None
    assert DelegationPacket is not None
    assert OCELObject is not None
    assert OCELEvent is not None
    assert OCELRelation is not None
    assert OCELRecord is not None
    assert OCELStore is not None
    assert OCELFactory is not None
    assert OCELValidator is not None
    assert OCELQueryService is not None
    assert OCPXLoader is not None
    assert OCPXEngine is not None
    assert OCPXProcessView is not None
    assert PIGService is not None
    assert PIGBuilder is not None
    assert PIGGraph is not None
    assert PIGDiagnosticService is not None
    assert PIGRecommendationService is not None
    assert utc_now_iso is not None

from __future__ import annotations

from pathlib import Path

from chanta_core.capabilities import CapabilityDecisionSurfaceService
from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.ocel.factory import short_hash
from chanta_core.persona import PersonaLoadingService, PersonalOverlayLoaderService
from chanta_core.prompts.assembly import PromptAssemblyService
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.runtime.loop.process_run_loop import ProcessRunLoop
from chanta_core.runtime.run_result import AgentRunResult
from chanta_core.session import SessionContextAssembler, SessionService
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.trace_service import TraceService


class AgentRuntime:
    def __init__(
        self,
        *,
        llm_client: LLMClient | None = None,
        prompt_assembly: PromptAssemblyService | None = None,
        trace_service: TraceService | None = None,
        agent_profile: AgentProfile | None = None,
        skill_registry: SkillRegistry | None = None,
        process_run_loop: ProcessRunLoop | None = None,
        session_service: SessionService | None = None,
        session_context_assembler: SessionContextAssembler | None = None,
        capability_decision_surface_service: CapabilityDecisionSurfaceService | None = None,
        persona_loading_service: PersonaLoadingService | None = None,
        personal_overlay_loader_service: PersonalOverlayLoaderService | None = None,
        personal_overlay_public_repo_root: str | Path | None = None,
        enable_session_context_projection: bool = True,
        enable_capability_decision_surface: bool = True,
        enable_persona_projection: bool = True,
        enable_personal_overlay: bool = True,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_assembly = prompt_assembly or PromptAssemblyService()
        self.trace_service = trace_service or TraceService()
        self.agent_profile = agent_profile or load_default_agent_profile()
        self.skill_registry = skill_registry or SkillRegistry()
        self.process_run_loop = process_run_loop
        self.session_service = session_service or SessionService(
            trace_service=self.trace_service
        )
        self.session_context_assembler = session_context_assembler or SessionContextAssembler(
            trace_service=self.trace_service
        )
        self.capability_decision_surface_service = (
            capability_decision_surface_service
            or CapabilityDecisionSurfaceService(trace_service=self.trace_service)
        )
        self.persona_loading_service = persona_loading_service or PersonaLoadingService(
            trace_service=self.trace_service
        )
        self.personal_overlay_loader_service = (
            personal_overlay_loader_service
            or PersonalOverlayLoaderService(trace_service=self.trace_service)
        )
        self.personal_overlay_public_repo_root = personal_overlay_public_repo_root
        self.enable_session_context_projection = enable_session_context_projection
        self.enable_capability_decision_surface = enable_capability_decision_surface
        self.enable_persona_projection = enable_persona_projection
        self.enable_personal_overlay = enable_personal_overlay

    def run(
        self,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentRunResult:
        process_instance_id = None
        if session_id:
            process_instance_id = (
                f"process_instance:{short_hash(f'{session_id}:{user_input}:process')}"
            )
        context = ExecutionContext.create(
            agent_id=self.agent_profile.agent_id,
            user_input=user_input,
            session_id=session_id,
            metadata=(
                {"process_instance_id": process_instance_id}
                if process_instance_id
                else None
            ),
        )
        if process_instance_id is None:
            process_instance_id = (
                f"process_instance:{short_hash(f'{context.session_id}:{user_input}:process')}"
            )
            context.metadata["process_instance_id"] = process_instance_id
        events: list[AgentEvent] = []
        turn_id: str | None = None
        user_message_id: str | None = None
        assistant_message_id: str | None = None

        loop: ProcessRunLoop | None = None
        try:
            self.session_service.start_session(
                session_id=context.session_id,
                agent_id=context.agent_id,
            )
            turn = self.session_service.start_turn(
                session_id=context.session_id,
                process_instance_id=process_instance_id,
            )
            turn_id = turn.turn_id
            user_message = self.session_service.record_user_message(
                session_id=context.session_id,
                turn_id=turn_id,
                content=context.user_input,
                message_attrs={"process_instance_id": process_instance_id},
            )
            user_message_id = user_message.message_id
            events.append(
                self.trace_service.record_user_request_received(
                    context,
                    profile=self.agent_profile,
                )
            )
            events.append(
                self.trace_service.record_run_started(
                    context,
                    profile=self.agent_profile,
                )
            )
            prompt_messages: list[dict[str, str]] | None = None
            persona_projection_block: str | None = None
            capability_decision_surface_block: str | None = None
            if self.enable_persona_projection:
                try:
                    persona_bundle = self.persona_loading_service.create_default_agent_persona(
                        agent_name=context.agent_id,
                        runtime_path="default_agent_repl_llm_chat",
                    )
                    persona_projection_block = (
                        self.persona_loading_service.render_projection_block(
                            persona_bundle.projection
                        )
                    )
                    context.metadata["persona_projection_id"] = (
                        persona_bundle.projection.projection_id
                    )
                    context.metadata["persona_loadout_id"] = (
                        persona_bundle.loadout.loadout_id
                    )
                except Exception as error:
                    context.metadata["persona_projection_warning"] = str(error)
            if self.enable_personal_overlay:
                try:
                    config = self.personal_overlay_loader_service.load_config_from_env()
                    if config is not None:
                        manifest = self.personal_overlay_loader_service.load_manifest(config)
                        findings = self.personal_overlay_loader_service.check_overlay_boundaries(
                            manifest,
                            public_repo_root=self.personal_overlay_public_repo_root or Path.cwd(),
                        )
                        refs = self.personal_overlay_loader_service.register_projection_refs(
                            manifest
                        )
                        load_result = self.personal_overlay_loader_service.load_projection_for_prompt(
                            manifest=manifest,
                            projection_refs=refs,
                            session_id=context.session_id,
                            turn_id=turn_id,
                            max_chars=4000,
                            boundary_findings=findings,
                        )
                        block = self.personal_overlay_loader_service.render_personal_overlay_block(
                            load_result
                        )
                        if block:
                            persona_projection_block = (
                                f"{persona_projection_block}\n\n{block}"
                                if persona_projection_block
                                else block
                            )
                        context.metadata["personal_directory_manifest_id"] = manifest.manifest_id
                        context.metadata["personal_overlay_load_result_id"] = load_result.result_id
                        context.metadata["personal_overlay_denied"] = load_result.denied
                except Exception as error:
                    context.metadata["personal_overlay_warning"] = str(error)
            if self.enable_capability_decision_surface:
                try:
                    capability_surface = (
                        self.capability_decision_surface_service.build_decision_surface(
                            context.user_input,
                            session_id=context.session_id,
                            turn_id=turn_id,
                            message_id=user_message_id,
                        )
                    )
                    capability_decision_surface_block = (
                        self.capability_decision_surface_service.render_decision_surface_block(
                            capability_surface
                        )
                    )
                    context.metadata["capability_decision_surface_id"] = (
                        capability_surface.surface_id
                    )
                    context.metadata["capability_decision_overall_availability"] = (
                        capability_surface.overall_availability
                    )
                    context.metadata["capability_decision_can_fulfill_now"] = (
                        capability_surface.can_fulfill_now
                    )
                except Exception as error:
                    context.metadata["capability_decision_surface_warning"] = str(error)
            if self.enable_session_context_projection:
                try:
                    prior_messages = self.session_service.fetch_session_messages(
                        context.session_id
                    )
                    turns = self.session_service.fetch_session_turns(context.session_id)
                    projection = (
                        self.session_context_assembler.assemble_projection_from_messages(
                            session_id=context.session_id,
                            messages=prior_messages,
                            turns=turns,
                            exclude_message_ids=[user_message_id],
                        )
                    )
                    prompt_messages = (
                        self.session_context_assembler.render_projection_to_llm_messages(
                            projection=projection,
                            system_prompt=self.agent_profile.system_prompt,
                            persona_projection_block=persona_projection_block,
                            capability_profile_block=capability_decision_surface_block,
                            current_user_message=context.user_input,
                            avoid_duplicate_current_message=True,
                        )
                    )
                    context.metadata["session_context_projection_id"] = (
                        projection.projection_id
                    )
                    context.metadata["session_context_projection_messages"] = (
                        projection.total_messages
                    )
                    context.metadata["session_context_projection_truncated"] = (
                        projection.truncated
                    )
                except Exception as error:
                    context.metadata["session_context_projection_warning"] = str(error)
            loop = self.process_run_loop or ProcessRunLoop(
                llm_client=self.llm_client,
                trace_service=self.trace_service,
                skill_registry=self.skill_registry,
                agent_profile=self.agent_profile,
            )
            loop_result = loop.run(
                process_instance_id=process_instance_id,
                session_id=context.session_id,
                agent_id=context.agent_id,
                user_input=context.user_input,
                system_prompt=self.agent_profile.system_prompt,
                prompt_messages=prompt_messages,
            )
            events.extend(loop.events)
            response_text = loop_result.response_text
            assistant_message = self.session_service.record_assistant_message(
                session_id=context.session_id,
                turn_id=turn_id,
                content=response_text,
                message_attrs={"process_instance_id": process_instance_id},
            )
            assistant_message_id = assistant_message.message_id
            self.session_service.complete_turn(
                session_id=context.session_id,
                turn_id=turn_id,
                user_message_id=user_message_id,
                assistant_message_id=assistant_message_id,
                process_instance_id=process_instance_id,
            )
        except Exception as error:
            if loop is not None:
                events.extend(loop.events)
            if turn_id is not None:
                self.session_service.fail_turn(
                    session_id=context.session_id,
                    turn_id=turn_id,
                    error=str(error),
                    process_instance_id=process_instance_id,
                )
            if not events or events[-1].event_type != "process_instance_failed":
                events.append(
                    self.trace_service.record_process_instance_failed(
                        context,
                        error,
                        profile=self.agent_profile,
                    )
                )
            raise

        return AgentRunResult(
            session_id=context.session_id,
            agent_id=context.agent_id,
            user_input=context.user_input,
            response_text=response_text,
            events=events,
            metadata={
                **context.metadata,
                "process_instance_id": process_instance_id,
                "turn_id": turn_id,
                "user_message_id": user_message_id,
                "assistant_message_id": assistant_message_id,
            },
        )


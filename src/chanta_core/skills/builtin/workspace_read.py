from __future__ import annotations

from pathlib import Path
from typing import Any

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.workspace import WorkspaceReadService


def create_list_workspace_files_skill() -> Skill:
    return Skill(
        skill_id="skill:list_workspace_files",
        skill_name="list_workspace_files",
        description="List files under an explicit workspace read root without reading file content.",
        execution_type="builtin",
        input_schema={"root_path": "str", "relative_path": "str"},
        output_schema={"entries": "list"},
        tags=["workspace", "read_only", "explicit"],
        skill_attrs={"is_builtin": True, "read_only": True, "ambient_access": False},
    )


def create_read_workspace_text_file_skill() -> Skill:
    return Skill(
        skill_id="skill:read_workspace_text_file",
        skill_name="read_workspace_text_file",
        description="Read a bounded text file under an explicit workspace read root.",
        execution_type="builtin",
        input_schema={"root_path": "str", "relative_path": "str"},
        output_schema={"content": "str"},
        tags=["workspace", "read_only", "explicit"],
        skill_attrs={"is_builtin": True, "read_only": True, "ambient_access": False},
    )


def create_summarize_workspace_markdown_skill() -> Skill:
    return Skill(
        skill_id="skill:summarize_workspace_markdown",
        skill_name="summarize_workspace_markdown",
        description="Create a deterministic heading/preview summary for a markdown file under a workspace read root.",
        execution_type="builtin",
        input_schema={"root_path": "str", "relative_path": "str"},
        output_schema={"summary": "str"},
        tags=["workspace", "read_only", "markdown", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "uses_llm": False,
        },
    )


def execute_list_workspace_files_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        service = WorkspaceReadService(trace_service=trace_service, ocel_store=ocel_store)
        root = service.register_read_root(root_path)
        result = service.list_workspace_files(
            root=root,
            relative_path=str(context.context_attrs.get("relative_path") or "."),
            pattern=context.context_attrs.get("pattern"),
            recursive=bool(context.context_attrs.get("recursive", False)),
            max_results=int(context.context_attrs.get("max_results", 200)),
            session_id=context.session_id,
            process_instance_id=context.process_instance_id,
        )
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not bool(result.violation_ids),
            output_text=f"{result.total_entries} workspace entries",
            output_attrs={"execution_type": skill.execution_type, **result.to_dict()},
            error=None if not result.violation_ids else "Workspace file list denied",
        )
    except Exception as error:
        return _failure(skill, error)


def execute_read_workspace_text_file_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        relative_path = _required(context, "relative_path")
        service = WorkspaceReadService(trace_service=trace_service, ocel_store=ocel_store)
        root = service.register_read_root(root_path)
        result = service.read_workspace_text_file(
            root=root,
            relative_path=relative_path,
            max_bytes=int(context.context_attrs.get("max_bytes", 262144)),
            max_chars=int(context.context_attrs.get("max_chars", 120000)),
            encoding=str(context.context_attrs.get("encoding") or "utf-8"),
            session_id=context.session_id,
            process_instance_id=context.process_instance_id,
        )
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not result.denied,
            output_text=result.content,
            output_attrs={"execution_type": skill.execution_type, **result.to_dict()},
            error=None if not result.denied else "Workspace text file read denied",
        )
    except Exception as error:
        return _failure(skill, error)


def execute_summarize_workspace_markdown_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        relative_path = _required(context, "relative_path")
        service = WorkspaceReadService(trace_service=trace_service, ocel_store=ocel_store)
        root = service.register_read_root(root_path)
        result = service.summarize_workspace_markdown(
            root=root,
            relative_path=relative_path,
            max_bytes=int(context.context_attrs.get("max_bytes", 262144)),
            max_chars=int(context.context_attrs.get("max_chars", 120000)),
            summary_style=str(context.context_attrs.get("summary_style") or "outline_preview"),
            session_id=context.session_id,
            process_instance_id=context.process_instance_id,
        )
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not result.denied,
            output_text=result.summary,
            output_attrs={"execution_type": skill.execution_type, **result.to_dict()},
            error=None if not result.denied else "Workspace markdown summary denied",
        )
    except Exception as error:
        return _failure(skill, error)


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for explicit workspace read skills")
    return str(Path(str(value)) if key == "root_path" else value)


def _failure(skill: Skill, error: Exception) -> SkillExecutionResult:
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=False,
        output_text=None,
        output_attrs={
            "execution_type": skill.execution_type,
            "exception_type": type(error).__name__,
            "read_only": True,
        },
        error=str(error),
    )

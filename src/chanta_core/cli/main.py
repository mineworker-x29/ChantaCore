from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from chanta_core.persona.personal_runtime_surface import PersonalRuntimeSurfaceService
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService
from chanta_core.skills.proposal import SkillProposalRouterService
from chanta_core.runtime.chat_service import ChatService
from chanta_core.settings.app_settings import load_app_settings


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
    skill_gate_run_parser.add_argument("--root", dest="root_path", help="Workspace read root for read-only skills.")
    skill_gate_run_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skill_gate_run_parser.add_argument("--recursive", action="store_true", help="List files recursively.")
    skill_gate_run_parser.add_argument("--max-results", type=int, help="Maximum file list results.")
    skill_propose_parser = skill_subparsers.add_parser(
        "propose",
        help="Create a review-only explicit skill invocation proposal from a prompt.",
    )
    skill_propose_parser.add_argument("prompt", nargs="?", help="Prompt to analyze. Reads stdin if omitted.")
    skill_propose_parser.add_argument("--root", dest="root_path", help="Workspace read root for proposal payload.")
    skill_propose_parser.add_argument("--path", dest="relative_path", help="Relative workspace path.")
    skill_propose_parser.add_argument("--recursive", action="store_true", help="Suggest recursive file listing.")
    skill_propose_parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    return parser


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


def run_skill(args: argparse.Namespace) -> int:
    if args.skill_command == "propose":
        prompt = resolve_prompt(args.prompt)
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
    if args.skill_command not in {"run", "gate-run"}:
        print("skill command is required", file=sys.stderr)
        return 1
    skill_id = args.skill_id_option or args.skill_id
    if not skill_id:
        print("[explicit skill invocation error: skill_id is required]", file=sys.stderr)
        return 1
    try:
        payload = json.loads(args.input_json) if args.input_json else {}
        if not isinstance(payload, dict):
            print("[explicit skill invocation error: --input-json must be a JSON object]", file=sys.stderr)
            return 1
    except json.JSONDecodeError as error:
        print(f"[explicit skill invocation error: invalid JSON input: {error.msg}]", file=sys.stderr)
        return 1
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
    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

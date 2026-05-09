from __future__ import annotations

import argparse
import sys
from typing import Sequence

from chanta_core.runtime.agent_runtime import AgentRuntime
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
    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

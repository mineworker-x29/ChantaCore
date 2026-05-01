from __future__ import annotations

import argparse
import sys
from typing import Sequence

from chanta_core.llm.client import create_llm_client
from chanta_core.llm.messages import ChatMessage
from chanta_core.llm.types import ChatRequest
from chanta_core.settings.app_settings import AppSettings, load_app_settings
from chanta_core.settings.llm_settings import LLMSettings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chanta-cli",
        description="CLI for OpenAI-compatible LLM endpoints such as LM Studio.",
    )
    subparsers = parser.add_subparsers(dest="command")

    ask_parser = subparsers.add_parser("ask", help="Send a single prompt.")
    ask_parser.add_argument("prompt", nargs="?", help="Prompt text. Reads stdin if omitted.")
    ask_parser.add_argument("--system", help="Optional system prompt.")
    ask_parser.add_argument("--model", help="Override the configured model.")
    ask_parser.add_argument("--base-url", help="Override the configured base URL.")
    ask_parser.add_argument("--api-key", help="Override the configured API key.")
    ask_parser.add_argument("--temperature", type=float, help="Sampling temperature.")
    ask_parser.add_argument("--max-tokens", type=int, help="Maximum completion tokens.")

    repl_parser = subparsers.add_parser("repl", help="Start an interactive chat session.")
    repl_parser.add_argument("--system", help="Optional system prompt.")
    repl_parser.add_argument("--model", help="Override the configured model.")
    repl_parser.add_argument("--base-url", help="Override the configured base URL.")
    repl_parser.add_argument("--api-key", help="Override the configured API key.")
    repl_parser.add_argument("--temperature", type=float, help="Sampling temperature.")
    repl_parser.add_argument("--max-tokens", type=int, help="Maximum completion tokens.")

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


def build_runtime_settings(args: argparse.Namespace) -> AppSettings:
    current = load_app_settings()
    llm = LLMSettings(
        provider=current.llm.provider,
        base_url=args.base_url or current.llm.base_url,
        api_key=args.api_key or current.llm.api_key,
        model=args.model or current.llm.model,
        timeout_seconds=current.llm.timeout_seconds,
    )
    return AppSettings(env_file=current.env_file, llm=llm)


def build_request(
    prompt: str,
    system_prompt: str | None,
    temperature: float | None,
    max_tokens: int | None,
) -> ChatRequest:
    messages: list[ChatMessage] = []
    if system_prompt:
        messages.append(ChatMessage(role="system", content=system_prompt))
    messages.append(ChatMessage(role="user", content=prompt))
    return ChatRequest(messages=messages, temperature=temperature, max_tokens=max_tokens)


def run_ask(args: argparse.Namespace) -> int:
    settings = build_runtime_settings(args)
    client = create_llm_client(settings.llm)
    prompt = resolve_prompt(args.prompt)
    response = client.chat(build_request(prompt, args.system, args.temperature, args.max_tokens))
    print(response.text)
    return 0


def run_repl(args: argparse.Namespace) -> int:
    settings = build_runtime_settings(args)
    client = create_llm_client(settings.llm)

    history: list[ChatMessage] = []
    if args.system:
        history.append(ChatMessage(role="system", content=args.system))

    print("Interactive session started. Type /exit to quit, /reset to clear history.")
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
        if user_input == "/reset":
            history = [history[0]] if history and history[0].role == "system" else []
            print("history cleared")
            continue

        history.append(ChatMessage(role="user", content=user_input))
        response = client.chat(
            ChatRequest(
                messages=history,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
        )
        print(f"assistant> {response.text}")
        history.append(ChatMessage(role="assistant", content=response.text))


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

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from chanta_core.agent_surface import AgentAskReplReportService, AgentReplSessionService, render_agent_ask_repl_cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m chanta_core.agent", description="v0.25.7 bounded agent ask/repl surface.")
    subparsers = parser.add_subparsers(dest="command")
    ask_parser = subparsers.add_parser("ask", help="Execute one synchronous bounded ask turn.")
    ask_parser.add_argument("prompt", nargs="?")
    ask_parser.add_argument("--text")
    ask_parser.add_argument("--assembled-response-id")
    repl_parser = subparsers.add_parser("repl", help="Render a user-driven REPL session start view.")
    repl_parser.add_argument("--session-id")
    repl_parser.add_argument("--text", default="Explain the project structure")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "ask":
        text = args.text or args.prompt or "Explain the project structure"
        parts = AgentAskReplReportService().build_all_parts(
            user_text=text,
            source_type="cli",
            assembled_response_id=args.assembled_response_id,
        )
        print(render_agent_ask_repl_cli(parts, section="ask"))
        return 0 if parts["report"].report_status in {"passed", "warning"} else 1
    if args.command == "repl":
        session = AgentReplSessionService().start_session(args.session_id)
        report = AgentAskReplReportService().build_repl_start_report(session)
        parts = {
            "report": report,
            "repl_session": report.repl_session,
            "session_state": report.session_state,
        }
        print(render_agent_ask_repl_cli(parts, section="session"))
        return 0 if report.report_status in {"passed", "warning"} else 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

from dotenv import load_dotenv
import sys

from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.agent_runtime import AgentRuntime


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    load_dotenv()
    runtime = AgentRuntime()
    result = runtime.run("Say hello from ChantaCore runtime in one sentence.")
    print(result.response_text)
    print("session_id:", result.session_id)
    print("events:", [event.event_type for event in result.events])
    print(
        "activities:",
        [
            event["event_activity"]
            for event in OCELStore().fetch_events_by_session(result.session_id)
        ],
    )


if __name__ == "__main__":
    main()

from dotenv import load_dotenv

from chanta_core.runtime.agent_runtime import AgentRuntime


def main() -> None:
    load_dotenv()
    runtime = AgentRuntime()
    result = runtime.run("Say hello from ChantaCore runtime in one sentence.")
    print(result.response_text)
    print("session_id:", result.session_id)
    print("events:", [event.event_type for event in result.events])


if __name__ == "__main__":
    main()

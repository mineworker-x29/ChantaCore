from dotenv import load_dotenv
import sys

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocel.query import OCELQueryService
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.runtime.agent_runtime import AgentRuntime


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    load_dotenv()
    runtime = AgentRuntime()
    result = runtime.run("Say hello from ChantaCore OCEL runtime in one sentence.")
    print(result.response_text)
    print("session_id:", result.session_id)

    store = OCELStore()
    loader = OCPXLoader(store)
    process_instances = loader.load_session_process_instances(result.session_id)
    print("process_instance_ids:", [item["object_id"] for item in process_instances])
    print("event_count:", store.fetch_event_count())
    print("object_count:", store.fetch_object_count())
    print("event_object_relations:", store.fetch_event_object_relation_count())
    print("object_object_relations:", store.fetch_object_object_relation_count())

    validator = OCELValidator()
    query = OCELQueryService(store)
    print("validation:", validator.validate_structure())
    print("session_trace:", validator.validate_session_trace(result.session_id))
    print("duplicate_relations:", validator.validate_duplicate_relations())
    print(
        "recent_event_activities:",
        [event["event_activity"] for event in store.fetch_recent_events(limit=10)],
    )
    print("session_summary:", query.session_summary(result.session_id))


if __name__ == "__main__":
    main()

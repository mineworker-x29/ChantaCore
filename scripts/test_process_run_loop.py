from dotenv import load_dotenv
import sys

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.runtime.agent_runtime import AgentRuntime


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    load_dotenv()
    runtime = AgentRuntime()
    result = runtime.run("Say hello from the ChantaCore process run loop.")

    store = OCELStore()
    loader = OCPXLoader(store)
    process_instances = loader.load_session_process_instances(result.session_id)
    process_instance_id = (
        process_instances[0]["object_id"] if process_instances else None
    )
    view = (
        loader.load_process_instance_view(process_instance_id)
        if process_instance_id
        else loader.load_session_view(result.session_id)
    )
    engine = OCPXEngine()

    print("response_text:", result.response_text)
    print("session_id:", result.session_id)
    print("process_instance_id:", process_instance_id)
    print("activity_sequence:", engine.activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()

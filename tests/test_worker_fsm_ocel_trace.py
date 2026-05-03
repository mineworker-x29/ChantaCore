from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.traces.trace_service import TraceService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def test_worker_queue_fsm_transitions_are_ocel_traceable(tmp_path) -> None:
    store = OCELStore(tmp_path / "worker-fsm.sqlite")
    trace_service = TraceService(ocel_store=store)
    queue = WorkerQueueService(
        ProcessJobStore(tmp_path / "jobs.jsonl"),
        trace_service=trace_service,
    )

    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = queue.claim_next("worker:fsm")
    running = queue.mark_running(claimed.job_id, "worker:fsm")
    queue.mark_completed(running.job_id, "worker:fsm", "process_instance:fsm")

    events = store.fetch_recent_events(50)
    activities = [event["event_activity"] for event in events]
    assert "enqueue_process_job" in activities
    assert "claim_process_job" in activities
    assert "start_worker_job" in activities
    assert "complete_worker_job" in activities

    transition_events = [
        event
        for event in events
        if event["event_activity"] in {"claim_process_job", "start_worker_job", "complete_worker_job"}
    ]
    assert all(event["event_attrs"]["transition_valid"] is True for event in transition_events)
    assert any(event["event_attrs"]["from_status"] == "running" for event in transition_events)
    assert any(event["event_attrs"]["to_status"] == "completed" for event in transition_events)
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
    assert queue.job_store.get(job.job_id).status == "completed"

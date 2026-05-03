from dataclasses import dataclass, field

from chanta_core.workers import (
    ProcessJobStore,
    WorkerHeartbeatStore,
    WorkerQueueService,
    WorkerRunner,
)


@dataclass(frozen=True)
class FakeProcessResult:
    process_instance_id: str
    status: str = "completed"
    result_attrs: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "result_attrs": self.result_attrs,
        }


class CompletingLoop:
    def run(self, **kwargs):
        return FakeProcessResult(process_instance_id=kwargs["process_instance_id"])


class FailingLoop:
    def run(self, **_kwargs):
        raise RuntimeError("loop failed")


def setup(tmp_path, loop_factory):
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    heartbeats = WorkerHeartbeatStore(tmp_path / "heartbeats.jsonl")
    return queue, heartbeats, WorkerRunner(
        queue_service=queue,
        heartbeat_store=heartbeats,
        process_run_loop_factory=loop_factory,
    )


def test_run_once_idle_when_no_jobs(tmp_path) -> None:
    queue, heartbeats, runner = setup(tmp_path, CompletingLoop)

    result = runner.run_once()

    assert result["status"] == "idle"
    assert result["job"] is None
    assert heartbeats.recent()


def test_run_once_completes_job(tmp_path) -> None:
    queue, heartbeats, runner = setup(tmp_path, CompletingLoop)
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")

    result = runner.run_once()

    assert result["status"] == "completed"
    assert queue.job_store.get(job.job_id).status == "completed"
    assert [item.status for item in heartbeats.recent(10)]


def test_run_once_fails_job_on_exception(tmp_path) -> None:
    queue, heartbeats, runner = setup(tmp_path, FailingLoop)
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")

    result = runner.run_once()

    assert result["status"] == "failed"
    assert queue.job_store.get(job.job_id).status == "failed"
    assert queue.job_store.get(job.job_id).last_error == "loop failed"


def test_run_once_retry_behavior(tmp_path) -> None:
    queue, heartbeats, runner = setup(tmp_path, FailingLoop)
    job = queue.enqueue_process_run(user_input="run", agent_id="agent", max_retries=1)

    result = runner.run_once()

    assert result["status"] == "retried"
    assert queue.job_store.get(job.job_id).status == "queued"
    assert queue.job_store.get(job.job_id).retry_count == 1

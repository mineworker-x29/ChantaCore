from dataclasses import replace

from chanta_core.pig.queue_conformance import PIGQueueConformanceService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def test_completed_job_conformant_with_lifecycle_sequence(tmp_path) -> None:
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = queue.claim_next("worker:one")
    running = queue.mark_running(claimed.job_id, "worker:one")
    completed = queue.mark_completed(running.job_id, "worker:one")

    report = PIGQueueConformanceService(job_store=queue.job_store).check_job_sequence(
        completed,
        [
            "enqueue_process_job",
            "claim_process_job",
            "start_worker_job",
            "complete_worker_job",
        ],
    )

    assert report.status == "conformant"
    assert report.summary["advisory"] is True


def test_failed_job_with_last_error_has_no_missing_failure_issue(tmp_path) -> None:
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    claimed = queue.claim_next("worker:one")
    running = queue.mark_running(claimed.job_id, "worker:one")
    failed = queue.mark_failed(running.job_id, "worker:one", "boom")

    report = PIGQueueConformanceService(job_store=queue.job_store).check_job_sequence(failed)

    assert "missing_failure_evidence" not in [issue.issue_type for issue in report.issues]


def test_retry_count_over_max_retries_is_nonconformant(tmp_path) -> None:
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    bad = replace(job, retry_count=2, max_retries=1)

    report = PIGQueueConformanceService(job_store=queue.job_store).check_job_sequence(bad)

    assert report.status == "nonconformant"
    assert "retry_limit_exceeded" in [issue.issue_type for issue in report.issues]


def test_cancelled_completed_conflict_produces_issue(tmp_path) -> None:
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    bad = replace(job, status="cancelled", completed_at="2026-01-01T00:00:00Z")

    report = PIGQueueConformanceService(job_store=queue.job_store).check_job_sequence(bad)

    assert report.status == "nonconformant"
    assert "cancelled_completed_conflict" in [issue.issue_type for issue in report.issues]


def test_claimed_job_missing_worker_produces_warning(tmp_path) -> None:
    queue = WorkerQueueService(ProcessJobStore(tmp_path / "jobs.jsonl"))
    job = queue.enqueue_process_run(user_input="run", agent_id="agent")
    bad = replace(job, status="claimed", claimed_by_worker_id=None)

    report = PIGQueueConformanceService(job_store=queue.job_store).check_job_sequence(bad)

    assert report.status == "warning"
    assert "missing_claimed_worker" in [issue.issue_type for issue in report.issues]

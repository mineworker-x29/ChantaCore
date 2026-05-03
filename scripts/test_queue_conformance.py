from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.pig.queue_conformance import PIGQueueConformanceService
from chanta_core.workers import ProcessJobStore, WorkerQueueService


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = ProcessJobStore(Path(tmp) / "jobs.jsonl")
        queue = WorkerQueueService(store)
        job = queue.enqueue_process_run(user_input="queue conformance", agent_id="agent")
        claimed = queue.claim_next("worker:script")
        running = queue.mark_running(claimed.job_id, "worker:script")
        completed = queue.mark_completed(running.job_id, "worker:script")
        report = PIGQueueConformanceService(job_store=store).check_job_sequence(
            completed,
            [
                "enqueue_process_job",
                "claim_process_job",
                "start_worker_job",
                "complete_worker_job",
            ],
        )
        recent = PIGQueueConformanceService(job_store=store).check_recent_jobs()
        print(f"job_id={job.job_id}")
        print(f"job_report_status={report.status}")
        print(f"recent_report_status={recent.status}")
        print(f"issue_count={recent.summary['issue_count']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.workers import ProcessJobStore, WorkerQueueService


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = ProcessJobStore(Path(tmp) / "jobs.jsonl")
        queue = WorkerQueueService(store)
        job = queue.enqueue_process_run(
            user_input="queued background process",
            agent_id="chanta_core_default",
            priority=1,
            max_retries=1,
        )
        claimed = queue.claim_next("worker:script")
        print(f"job_id={job.job_id}")
        print(f"claimed_status={claimed.status if claimed else None}")
        print(f"summary={queue.summary()}")


if __name__ == "__main__":
    main()

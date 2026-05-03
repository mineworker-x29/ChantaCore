from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path

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


class FakeLoop:
    def run(self, **kwargs):
        return FakeProcessResult(process_instance_id=kwargs["process_instance_id"])


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        queue = WorkerQueueService(ProcessJobStore(Path(tmp) / "jobs.jsonl"))
        heartbeats = WorkerHeartbeatStore(Path(tmp) / "heartbeats.jsonl")
        queue.enqueue_process_run(user_input="fake worker job", agent_id="chanta_core_default")
        runner = WorkerRunner(
            queue_service=queue,
            heartbeat_store=heartbeats,
            process_run_loop_factory=FakeLoop,
        )
        result = runner.run_once()
        print(f"run_once_status={result['status']}")
        print(f"summary={queue.summary()}")
        print(f"heartbeats={len(heartbeats.recent(10))}")


if __name__ == "__main__":
    main()

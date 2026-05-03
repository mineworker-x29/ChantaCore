from chanta_core.workers.errors import (
    ProcessJobClaimError,
    ProcessJobError,
    ProcessJobInvalidTransitionError,
    ProcessJobNotFoundError,
    WorkerError,
    WorkerRunError,
)
from chanta_core.workers.fsm import ProcessJobStateMachine, ProcessJobStateTransition
from chanta_core.workers.heartbeat import WorkerHeartbeat, WorkerHeartbeatStore
from chanta_core.workers.job import ProcessJob, new_process_job_id
from chanta_core.workers.queue import WorkerQueueService
from chanta_core.workers.store import ProcessJobStore
from chanta_core.workers.worker import Worker, new_worker_id

__all__ = [
    "ProcessJob",
    "ProcessJobClaimError",
    "ProcessJobError",
    "ProcessJobInvalidTransitionError",
    "ProcessJobStateMachine",
    "ProcessJobStateTransition",
    "ProcessJobNotFoundError",
    "ProcessJobStore",
    "Worker",
    "WorkerError",
    "WorkerHeartbeat",
    "WorkerHeartbeatStore",
    "WorkerQueueService",
    "WorkerRunError",
    "WorkerRunner",
    "new_process_job_id",
    "new_worker_id",
]


def __getattr__(name: str):
    if name == "WorkerRunner":
        from chanta_core.workers.runner import WorkerRunner

        return WorkerRunner
    raise AttributeError(name)

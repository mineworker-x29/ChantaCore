from chanta_core.scheduler.errors import (
    ProcessScheduleError,
    ProcessScheduleNotFoundError,
    ScheduleEvaluationError,
    SchedulerError,
)
from chanta_core.scheduler.evaluator import ScheduleEvaluation, ScheduleEvaluator
from chanta_core.scheduler.schedule import ProcessSchedule, new_process_schedule_id
from chanta_core.scheduler.service import SchedulerService
from chanta_core.scheduler.store import ProcessScheduleStore

__all__ = [
    "ProcessSchedule",
    "ProcessScheduleError",
    "ProcessScheduleNotFoundError",
    "ProcessScheduleStore",
    "ScheduleEvaluation",
    "ScheduleEvaluationError",
    "ScheduleEvaluator",
    "SchedulerError",
    "SchedulerRunner",
    "SchedulerService",
    "new_process_schedule_id",
]


def __getattr__(name: str):
    if name == "SchedulerRunner":
        from chanta_core.scheduler.runner import SchedulerRunner

        return SchedulerRunner
    raise AttributeError(name)

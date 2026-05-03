class SchedulerError(RuntimeError):
    pass


class ProcessScheduleError(SchedulerError):
    pass


class ProcessScheduleNotFoundError(ProcessScheduleError):
    pass


class ScheduleEvaluationError(SchedulerError):
    pass

class WorkerError(RuntimeError):
    pass


class ProcessJobError(WorkerError):
    pass


class ProcessJobNotFoundError(ProcessJobError):
    pass


class ProcessJobClaimError(ProcessJobError):
    pass


class ProcessJobInvalidTransitionError(ProcessJobError):
    pass


class WorkerRunError(WorkerError):
    pass

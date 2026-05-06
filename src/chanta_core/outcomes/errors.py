class ProcessOutcomeError(Exception):
    """Base error for process outcome evaluation."""


class ProcessOutcomeContractError(ProcessOutcomeError):
    """Raised when a process outcome contract is invalid."""


class ProcessOutcomeCriterionError(ProcessOutcomeError):
    """Raised when a process outcome criterion is invalid."""


class ProcessOutcomeTargetError(ProcessOutcomeError):
    """Raised when a process outcome target is invalid."""


class ProcessOutcomeSignalError(ProcessOutcomeError):
    """Raised when a process outcome signal is invalid."""


class ProcessOutcomeEvaluationError(ProcessOutcomeError):
    """Raised when a process outcome evaluation is invalid."""

class VerificationError(Exception):
    """Base error for verification contract substrate failures."""


class VerificationContractError(VerificationError):
    pass


class VerificationTargetError(VerificationError):
    pass


class VerificationRequirementError(VerificationError):
    pass


class VerificationRunError(VerificationError):
    pass


class VerificationEvidenceError(VerificationError):
    pass


class VerificationResultError(VerificationError):
    pass

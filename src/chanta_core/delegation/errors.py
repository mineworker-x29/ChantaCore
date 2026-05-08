from __future__ import annotations


class DelegationError(ValueError):
    pass


class DelegationPacketError(DelegationError):
    pass


class DelegatedProcessRunError(DelegationError):
    pass


class DelegationResultError(DelegationError):
    pass


class DelegationLinkError(DelegationError):
    pass


class SidechainContextError(DelegationError):
    pass


class SidechainContextEntryError(DelegationError):
    pass


class SidechainContextSnapshotError(DelegationError):
    pass


class SidechainReturnEnvelopeError(DelegationError):
    pass


class DelegationConformanceError(DelegationError):
    pass


class DelegationConformanceContractError(DelegationConformanceError):
    pass


class DelegationConformanceRuleError(DelegationConformanceError):
    pass


class DelegationConformanceRunError(DelegationConformanceError):
    pass


class DelegationConformanceFindingError(DelegationConformanceError):
    pass


class DelegationConformanceResultError(DelegationConformanceError):
    pass

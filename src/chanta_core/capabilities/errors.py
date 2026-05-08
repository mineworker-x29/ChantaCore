class CapabilityDecisionSurfaceError(Exception):
    """Base error for runtime capability decision surface failures."""


class CapabilityRequestIntentError(CapabilityDecisionSurfaceError):
    """Raised when a capability request intent is invalid."""


class CapabilityRequirementError(CapabilityDecisionSurfaceError):
    """Raised when a capability requirement is invalid."""


class CapabilityDecisionError(CapabilityDecisionSurfaceError):
    """Raised when a capability decision is invalid."""


class CapabilityDecisionEvidenceError(CapabilityDecisionSurfaceError):
    """Raised when capability decision evidence is invalid."""

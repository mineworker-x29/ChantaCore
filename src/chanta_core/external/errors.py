class ExternalCapabilityError(Exception):
    """Base error for external capability descriptor import."""


class ExternalCapabilitySourceError(ExternalCapabilityError):
    pass


class ExternalCapabilityDescriptorError(ExternalCapabilityError):
    pass


class ExternalCapabilityImportBatchError(ExternalCapabilityError):
    pass


class ExternalCapabilityNormalizationError(ExternalCapabilityError):
    pass


class ExternalAssimilationCandidateError(ExternalCapabilityError):
    pass


class ExternalCapabilityRiskNoteError(ExternalCapabilityError):
    pass


class ExternalCapabilityRegistryViewError(ExternalCapabilityError):
    pass


class ExternalCapabilityRegistrySnapshotError(ExternalCapabilityError):
    pass


class ExternalCapabilityViewRenderError(ExternalCapabilityError):
    pass


class ExternalAdapterReviewError(ExternalCapabilityError):
    """Base error for external adapter review queue records."""


class ExternalAdapterReviewQueueError(ExternalAdapterReviewError):
    pass


class ExternalAdapterReviewItemError(ExternalAdapterReviewError):
    pass


class ExternalAdapterReviewChecklistError(ExternalAdapterReviewError):
    pass


class ExternalAdapterReviewFindingError(ExternalAdapterReviewError):
    pass


class ExternalAdapterReviewDecisionError(ExternalAdapterReviewError):
    pass


class MCPPluginDescriptorError(ExternalCapabilityError):
    """Base error for MCP/plugin descriptor skeleton records."""


class MCPServerDescriptorError(MCPPluginDescriptorError):
    pass


class MCPToolDescriptorError(MCPPluginDescriptorError):
    pass


class PluginDescriptorError(MCPPluginDescriptorError):
    pass


class PluginEntrypointDescriptorError(MCPPluginDescriptorError):
    pass


class ExternalDescriptorSkeletonError(MCPPluginDescriptorError):
    pass


class ExternalDescriptorSkeletonValidationError(MCPPluginDescriptorError):
    pass


class ExternalOCELImportError(ExternalCapabilityError):
    """Base error for external OCEL import candidate records."""


class ExternalOCELSourceError(ExternalOCELImportError):
    pass


class ExternalOCELPayloadDescriptorError(ExternalOCELImportError):
    pass


class ExternalOCELImportCandidateError(ExternalOCELImportError):
    pass


class ExternalOCELValidationError(ExternalOCELImportError):
    pass


class ExternalOCELPreviewError(ExternalOCELImportError):
    pass


class ExternalOCELRiskNoteError(ExternalOCELImportError):
    pass

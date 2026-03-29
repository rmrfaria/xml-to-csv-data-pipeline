"""Custom exceptions for the data pipeline."""


class DataPipelineError(Exception):
    """Base exception for the data pipeline."""


class DownloadError(DataPipelineError):
    """Raised when a download operation fails."""


class XMLParseError(DataPipelineError):
    """Raised when XML parsing fails."""


class DLTINSLinkNotFoundError(DataPipelineError):
    """Raised when the DLTINS link cannot be found in the XML."""


class ZipExtractionError(DataPipelineError):
    """Raised when extracting ZIP content fails."""


class StorageError(DataPipelineError):
    """Raised when storing data fails."""

"""Storage clients for simulated cloud uploads."""

import logging
from pathlib import Path

from data_pipeline.exceptions import StorageError

LOGGER = logging.getLogger(__name__)


class S3StorageClient:
    """Simulated S3 storage client for CSV uploads."""

    def upload_file(self, local_path: Path, destination_path: str) -> None:
        """Simulate uploading a file to an S3 destination.

        Args:
            local_path: The local file path to upload.
            destination_path: The target S3 path.

        Raises:
            StorageError: If the local file does not exist or the S3 path is invalid.
        """
        if not local_path.exists():
            raise StorageError(f"Local file does not exist: {local_path}")

        if not destination_path.startswith("s3://"):
            raise StorageError(
                f"Invalid S3 destination path: {destination_path}. "
                "Expected path starting with 's3://'."
            )

        LOGGER.info(
            "Simulated upload of file %s to S3 destination %s",
            local_path,
            destination_path,
        )

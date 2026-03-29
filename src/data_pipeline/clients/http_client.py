"""HTTP client utilities for downloading remote content."""

import logging

import requests
from requests import Response

from data_pipeline.exceptions import DownloadError

LOGGER = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client for downloading text and binary content."""

    def download_text(self, url: str, timeout: int = 30) -> str:
        """Download text content from a URL.

        Args:
            url: The URL to download from.
            timeout: Request timeout in seconds.

        Returns:
            The response body as text.

        Raises:
            DownloadError: If the download fails.
        """
        response = self._get(url, timeout)
        return response.text

    def download_bytes(self, url: str, timeout: int = 30) -> bytes:
        """Download binary content from a URL.

        Args:
            url: The URL to download from.
            timeout: Request timeout in seconds.

        Returns:
            The response body as bytes.

        Raises:
            DownloadError: If the download fails.
        """
        response = self._get(url, timeout)
        return response.content

    def _get(self, url: str, timeout: int) -> Response:
        """Execute a GET request and validate the response.

        Args:
            url: The URL to request.
            timeout: Request timeout in seconds.

        Returns:
            A successful HTTP response.

        Raises:
            DownloadError: If the request fails.
        """
        LOGGER.info("Downloading content from %s", url)

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            LOGGER.exception("Failed to download content from %s", url)
            raise DownloadError(f"Failed to download content from {url}") from exc

        LOGGER.info("Successfully downloaded content from %s", url)
        return response

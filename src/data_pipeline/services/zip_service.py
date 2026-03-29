"""Services for extracting XML content from ZIP archives."""

import zipfile
from io import BytesIO

from data_pipeline.exceptions import ZipExtractionError


class ZipService:
    """Service for extracting XML files from ZIP archives."""

    def extract_xml_content(self, zip_bytes: bytes) -> str:
        """Extract the first XML file content from ZIP bytes.

        Args:
            zip_bytes: ZIP archive content as bytes.

        Returns:
            The extracted XML file content as a UTF-8 string.

        Raises:
            ZipExtractionError: If the ZIP is invalid or no XML file is found.
        """
        try:
            with zipfile.ZipFile(BytesIO(zip_bytes)) as zip_file:
                xml_file_names = [
                    file_name
                    for file_name in zip_file.namelist()
                    if file_name.lower().endswith(".xml")
                ]

                if not xml_file_names:
                    raise ZipExtractionError("No XML file found inside ZIP archive.")

                with zip_file.open(xml_file_names[0]) as xml_file:
                    return xml_file.read().decode("utf-8")
        except zipfile.BadZipFile as exc:
            raise ZipExtractionError("Invalid ZIP archive.") from exc
        except OSError as exc:
            raise ZipExtractionError("Failed to extract XML from ZIP archive.") from exc

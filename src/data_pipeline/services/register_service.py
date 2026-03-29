"""Services for parsing the ESMA register XML."""

import xml.etree.ElementTree as ET

from data_pipeline.exceptions import DLTINSLinkNotFoundError, XMLParseError


class RegisterService:
    """Service for extracting download links from the register XML."""

    def extract_second_dltins_link(self, xml_content: str) -> str:
        """Extract the second DLTINS download link from the register XML.

        Args:
            xml_content: The XML content returned by the register endpoint.

        Returns:
            The second download link for entries whose file type is DLTINS.

        Raises:
            XMLParseError: If the XML content cannot be parsed.
            DLTINSLinkNotFoundError: If fewer than two DLTINS links are found.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            raise XMLParseError("Failed to parse register XML content.") from exc

        dltins_links: list[str] = []

        for doc in root.findall(".//doc"):
            file_type = self._get_field_value(doc, "file_type")
            download_link = self._get_field_value(doc, "download_link")

            if file_type == "DLTINS" and download_link:
                dltins_links.append(download_link)

        if len(dltins_links) < 2:
            raise DLTINSLinkNotFoundError(
                "Could not find a second DLTINS download link in the register XML."
            )

        return dltins_links[1]

    @staticmethod
    def _get_field_value(doc_element: ET.Element, field_name: str) -> str | None:
        """Extract a field value from a register XML doc element.

        Args:
            doc_element: The XML element representing a register document.
            field_name: The name attribute of the field to extract.

        Returns:
            The field text value if found, otherwise None.
        """
        element = doc_element.find(f"./str[@name='{field_name}']")
        return element.text if element is not None else None

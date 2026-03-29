"""Services for parsing instrument XML data."""

import xml.etree.ElementTree as ET

from data_pipeline.exceptions import XMLParseError
from data_pipeline.models.instrument import InstrumentRecord


class InstrumentXMLService:
    """Service for extracting instrument records from instrument XML."""

    def parse_instruments(self, xml_content: str) -> list[InstrumentRecord]:
        """Parse instrument XML content into instrument records.

        Args:
            xml_content: The XML content extracted from the ZIP archive.

        Returns:
            A list of parsed instrument records.

        Raises:
            XMLParseError: If the XML content cannot be parsed.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            raise XMLParseError("Failed to parse instrument XML content.") from exc

        namespace = {
            "biz": "urn:iso:std:iso:20022:tech:xsd:head.003.001.01",
            "auth": "urn:iso:std:iso:20022:tech:xsd:auth.036.001.02",
        }

        instrument_records: list[InstrumentRecord] = []

        for instrument in root.findall(".//auth:FinInstrm", namespace):
            general_attributes = instrument.find("auth:FinInstrmGnlAttrbts", namespace)

            record = InstrumentRecord(
                instrument_id=self._get_child_text(
                    general_attributes, "auth:Id", namespace
                ),
                full_name=self._get_child_text(
                    general_attributes, "auth:FullNm", namespace
                ),
                classification_type=self._get_child_text(
                    general_attributes, "auth:ClssfctnTp", namespace
                ),
                commodity_derivative_indicator=self._get_child_text(
                    general_attributes, "auth:CmmdtyDerivInd", namespace
                ),
                national_currency=self._get_child_text(
                    general_attributes, "auth:NtnlCcy", namespace
                ),
                issuer=self._get_child_text(instrument, "auth:Issr", namespace),
            )
            instrument_records.append(record)

        return instrument_records

    @staticmethod
    def _get_child_text(
        element: ET.Element | None,
        child_path: str,
        namespace: dict[str, str],
    ) -> str | None:
        """Extract text from a child XML element.

        Args:
            element: The parent XML element.
            child_path: The child path to search for.
            namespace: The XML namespace mapping.

        Returns:
            The child text if found, otherwise None.
        """
        if element is None:
            return None

        child = element.find(child_path, namespace)
        return child.text if child is not None else None

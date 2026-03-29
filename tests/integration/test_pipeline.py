"""Integration test for the pipeline service."""

import zipfile
from io import BytesIO

from data_pipeline.services.dataframe_service import DataFrameService
from data_pipeline.services.instrument_xml_service import InstrumentXMLService
from data_pipeline.services.pipeline_service import PipelineService
from data_pipeline.services.register_service import RegisterService
from data_pipeline.services.zip_service import ZipService


class FakeHTTPClient:
    """Fake HTTP client for integration testing."""

    def __init__(self, register_xml: str, zip_bytes: bytes) -> None:
        """Initialize the fake client with predefined responses.

        Args:
            register_xml: Fake register XML response.
            zip_bytes: Fake ZIP response bytes.
        """
        self.register_xml = register_xml
        self.zip_bytes = zip_bytes

    def download_text(self, url: str, timeout: int = 30) -> str:
        """Return fake register XML content.

        Args:
            url: The requested URL.
            timeout: Request timeout in seconds.

        Returns:
            The fake register XML content.
        """
        return self.register_xml

    def download_bytes(self, url: str, timeout: int = 30) -> bytes:
        """Return fake ZIP content.

        Args:
            url: The requested URL.
            timeout: Request timeout in seconds.

        Returns:
            The fake ZIP bytes.
        """
        return self.zip_bytes


def create_zip_with_xml(xml_content: str) -> bytes:
    """Create an in-memory ZIP archive containing one XML file.

    Args:
        xml_content: The XML content to include in the ZIP.

    Returns:
        ZIP archive bytes.
    """
    buffer = BytesIO()

    with zipfile.ZipFile(
        buffer, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as zip_file:
        zip_file.writestr("sample.xml", xml_content)

    return buffer.getvalue()


def test_pipeline_runs_end_to_end(tmp_path) -> None:
    """Test that the pipeline runs end-to-end and generates the expected CSV."""
    register_xml = """
    <response>
        <result>
            <doc>
                <str name="file_type">DLTINS</str>
                <str name="download_link">link_1.zip</str>
            </doc>
            <doc>
                <str name="file_type">DLTINS</str>
                <str name="download_link">link_2.zip</str>
            </doc>
        </result>
    </response>
    """

    instrument_xml = """
    <root xmlns="urn:iso:std:iso:20022:tech:xsd:auth.036.001.02">
        <FinInstrm>
            <ModfdRcrd>
                <FinInstrmGnlAttrbts>
                    <Id>ID123</Id>
                    <FullNm>Alpha</FullNm>
                    <ClssfctnTp>TYPE</ClssfctnTp>
                    <CmmdtyDerivInd>false</CmmdtyDerivInd>
                    <NtnlCcy>EUR</NtnlCcy>
                </FinInstrmGnlAttrbts>
                <Issr>ISSUER123</Issr>
            </ModfdRcrd>
        </FinInstrm>
    </root>
    """

    zip_bytes = create_zip_with_xml(instrument_xml)
    http_client = FakeHTTPClient(register_xml=register_xml, zip_bytes=zip_bytes)
    dataframe_service = DataFrameService()
    output_path = tmp_path / "instruments.csv"

    pipeline = PipelineService(
        http_client=http_client,
        register_service=RegisterService(),
        zip_service=ZipService(),
        instrument_service=InstrumentXMLService(),
        dataframe_service=dataframe_service,
    )

    result_path = pipeline.run(output_path=output_path)

    assert result_path == output_path
    assert output_path.exists()

    csv_content = output_path.read_text(encoding="utf-8")
    assert "FinInstrmGnlAttrbts.Id" in csv_content
    assert "Alpha" in csv_content
    assert "YES" in csv_content

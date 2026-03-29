"""Unit tests for the InstrumentXMLService."""

from data_pipeline.services.instrument_xml_service import InstrumentXMLService


def test_parse_instruments_extracts_expected_fields() -> None:
    """Test parsing of instrument XML into records."""
    service = InstrumentXMLService()

    xml_content = """
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

    records = service.parse_instruments(xml_content)

    assert len(records) == 1

    record = records[0]

    assert record.instrument_id == "ID123"
    assert record.full_name == "Alpha"
    assert record.classification_type == "TYPE"
    assert record.commodity_derivative_indicator == "false"
    assert record.national_currency == "EUR"
    assert record.issuer == "ISSUER123"

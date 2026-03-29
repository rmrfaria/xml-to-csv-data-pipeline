"""Unit tests for the RegisterService."""

import pytest

from data_pipeline.exceptions import DLTINSLinkNotFoundError
from data_pipeline.services.register_service import RegisterService


def test_extract_second_dltins_link() -> None:
    """Test extraction of the second DLTINS link from XML."""
    service = RegisterService()

    xml_content = """
    <response>
        <result>
            <doc>
                <str name="file_type">DLTINS</str>
                <str name="download_link">link_1.zip</str>
            </doc>
            <doc>
                <str name="file_type">OTHER</str>
                <str name="download_link">ignore.zip</str>
            </doc>
            <doc>
                <str name="file_type">DLTINS</str>
                <str name="download_link">link_2.zip</str>
            </doc>
        </result>
    </response>
    """

    result = service.extract_second_dltins_link(xml_content)

    assert result == "link_2.zip"


def test_raises_error_if_not_enough_dltins_links() -> None:
    """Test that an error is raised if fewer than two DLTINS links exist."""
    service = RegisterService()

    xml_content = """
    <response>
        <result>
            <doc>
                <str name="file_type">DLTINS</str>
                <str name="download_link">only_one.zip</str>
            </doc>
        </result>
    </response>
    """

    with pytest.raises(DLTINSLinkNotFoundError):
        service.extract_second_dltins_link(xml_content)

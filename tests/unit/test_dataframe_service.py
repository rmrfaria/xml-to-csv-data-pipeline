"""Unit tests for the DataFrameService."""

from data_pipeline.models.instrument import InstrumentRecord
from data_pipeline.services.dataframe_service import DataFrameService


def test_to_dataframe_adds_expected_columns_and_values() -> None:
    """Test that the DataFrame contains the required columns and derived values."""
    service = DataFrameService()

    records = [
        InstrumentRecord(
            instrument_id="ID1",
            full_name="Banana",
            classification_type="TYPE1",
            commodity_derivative_indicator="false",
            national_currency="EUR",
            issuer="ISSUER1",
        ),
        InstrumentRecord(
            instrument_id="ID2",
            full_name=None,
            classification_type="TYPE2",
            commodity_derivative_indicator="true",
            national_currency="USD",
            issuer="ISSUER2",
        ),
    ]

    dataframe = service.to_dataframe(records)

    assert list(dataframe.columns) == [
        "FinInstrmGnlAttrbts.Id",
        "FinInstrmGnlAttrbts.FullNm",
        "FinInstrmGnlAttrbts.ClssfctnTp",
        "FinInstrmGnlAttrbts.CmmdtyDerivInd",
        "FinInstrmGnlAttrbts.NtnlCcy",
        "Issr",
        "a_count",
        "contains_a",
    ]

    assert dataframe.loc[0, "a_count"] == 3
    assert dataframe.loc[0, "contains_a"] == "YES"

    assert dataframe.loc[1, "a_count"] == 0
    assert dataframe.loc[1, "contains_a"] == "NO"

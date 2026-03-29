"""Services for transforming instrument records into tabular data."""

from pathlib import Path

import pandas as pd

from data_pipeline.config import CSV_COLUMNS
from data_pipeline.models.instrument import InstrumentRecord


class DataFrameService:
    """Service for converting instrument records into a CSV-ready DataFrame."""

    def to_dataframe(self, records: list[InstrumentRecord]) -> pd.DataFrame:
        """Convert instrument records into a pandas DataFrame.

        Args:
            records: The parsed instrument records.

        Returns:
            A DataFrame with the required output columns.
        """
        data = [
            {
                "FinInstrmGnlAttrbts.Id": record.instrument_id,
                "FinInstrmGnlAttrbts.FullNm": record.full_name,
                "FinInstrmGnlAttrbts.ClssfctnTp": record.classification_type,
                "FinInstrmGnlAttrbts.CmmdtyDerivInd": (
                    record.commodity_derivative_indicator
                ),
                "FinInstrmGnlAttrbts.NtnlCcy": record.national_currency,
                "Issr": record.issuer,
            }
            for record in records
        ]

        dataframe = pd.DataFrame(data)
        dataframe["a_count"] = dataframe["FinInstrmGnlAttrbts.FullNm"].apply(
            self._count_lowercase_a
        )
        dataframe["contains_a"] = dataframe["a_count"].apply(
            lambda count: "YES" if count > 0 else "NO"
        )

        return dataframe[CSV_COLUMNS]

    def save_csv(self, dataframe: pd.DataFrame, output_path: Path) -> None:
        """Save a DataFrame to CSV.

        Args:
            dataframe: The DataFrame to save.
            output_path: The target CSV file path.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)

    @staticmethod
    def _count_lowercase_a(value: str | None) -> int:
        """Count lowercase 'a' characters in a string.

        Args:
            value: The input string.

        Returns:
            The number of lowercase 'a' characters, or 0 if missing.
        """
        if not isinstance(value, str):
            return 0

        return value.count("a")

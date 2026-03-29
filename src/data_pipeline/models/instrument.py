"""Data models for financial instrument records."""

from dataclasses import dataclass


@dataclass
class InstrumentRecord:
    """Represents a financial instrument record extracted from the XML."""

    instrument_id: str | None
    full_name: str | None
    classification_type: str | None
    commodity_derivative_indicator: str | None
    national_currency: str | None
    issuer: str | None

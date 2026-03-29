"""Application configuration for the XML to CSV data pipeline."""

from pathlib import Path

REGISTER_URL: str = (
    "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
    "?q=*"
    "&fq=publication_date:[2021-01-17T00:00:00Z TO 2021-01-19T23:59:59Z]"
    "&wt=xml&indent=true&start=0&rows=100"
)

OUTPUT_DIR: Path = Path("output")
OUTPUT_FILE_NAME: str = "instruments.csv"
OUTPUT_FILE_PATH: Path = OUTPUT_DIR / OUTPUT_FILE_NAME

CSV_COLUMNS: list[str] = [
    "FinInstrmGnlAttrbts.Id",
    "FinInstrmGnlAttrbts.FullNm",
    "FinInstrmGnlAttrbts.ClssfctnTp",
    "FinInstrmGnlAttrbts.CmmdtyDerivInd",
    "FinInstrmGnlAttrbts.NtnlCcy",
    "Issr",
    "a_count",
    "contains_a",
]

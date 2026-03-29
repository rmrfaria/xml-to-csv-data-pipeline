# XML to CSV Data Pipeline

This project implements a data pipeline that retrieves financial instrument data from the ESMA register, processes it, and outputs a structured CSV file.

## Overview

The pipeline performs the following steps:

1. Fetches register data from the ESMA endpoint
2. Extracts the second DLTINS file link
3. Downloads and extracts the ZIP archive
4. Parses instrument XML data
5. Transforms the data into a tabular format
6. Generates a CSV file with derived fields

## Output

The resulting CSV contains the following columns:

- FinInstrmGnlAttrbts.Id
- FinInstrmGnlAttrbts.FullNm
- FinInstrmGnlAttrbts.ClssfctnTp
- FinInstrmGnlAttrbts.CmmdtyDerivInd
- FinInstrmGnlAttrbts.NtnlCcy
- Issr
- a_count
- contains_a

## How to Run

```bash
export PYTHONPATH=src
python -m data_pipeline.main
```

On Windows (PowerShell)

```bash
$env:PYTHONPATH="src"
python -m data_pipeline.main
```

## Testing

Run all tests:

```bash
pytest
```

## Project Structure

src/data_pipeline/
  clients/          # HTTP client
  services/         # Core pipeline logic
  models/           # Data structures
  config.py         # Configuration
  exceptions.py     # Custom exceptions
  logging_config.py # Logging setup
  main.py           # Entry point

tests/
  unit/
  integration/

## Design Notes

- The pipeline is structured using separation of concerns (clients, services, models)
- XML parsing is handled explicitly with namespace awareness
- Data transformation is isolated using pandas
- Custom exceptions improve error clarity
- Logging is centralized and consistent
- Unit and integration tests ensure correctness
- CI is configured using GitHub Actions

## Assumptions

- The second DLTINS file is required as per specification
- XML encoding is UTF-8
- Missing values are handled gracefully in transformations

## Technologies

- Python 3.12
- pandas
- pytest
- ruff
"""Pipeline orchestration service for the XML to CSV workflow."""

import logging
from pathlib import Path

from data_pipeline.clients.http_client import HTTPClient
from data_pipeline.config import OUTPUT_FILE_PATH, REGISTER_URL, S3_DESTINATION_PATH
from data_pipeline.services.dataframe_service import DataFrameService
from data_pipeline.services.instrument_xml_service import InstrumentXMLService
from data_pipeline.services.register_service import RegisterService
from data_pipeline.services.zip_service import ZipService
from data_pipeline.storage.s3_storage import S3StorageClient

LOGGER = logging.getLogger(__name__)


class PipelineService:
    """Service that orchestrates the full XML to CSV pipeline."""

    def __init__(
        self,
        http_client: HTTPClient,
        register_service: RegisterService,
        zip_service: ZipService,
        instrument_service: InstrumentXMLService,
        dataframe_service: DataFrameService,
        storage_client: S3StorageClient,
    ) -> None:
        """Initialize the pipeline with its dependencies.

        Args:
            http_client: Client used to download remote content.
            register_service: Service used to extract the DLTINS link.
            zip_service: Service used to extract XML from ZIP archives.
            instrument_service: Service used to parse instrument XML data.
            dataframe_service: Service used to transform records into a DataFrame.
        """
        self.http_client = http_client
        self.register_service = register_service
        self.zip_service = zip_service
        self.instrument_service = instrument_service
        self.dataframe_service = dataframe_service
        self.storage_client = storage_client

    def run(self, output_path: Path = OUTPUT_FILE_PATH) -> Path:
        """Execute the full pipeline and return the output CSV path.

        Returns:
            The path to the generated CSV file.
        """
        LOGGER.info("Starting XML to CSV pipeline")

        register_xml = self.http_client.download_text(REGISTER_URL)
        zip_url = self.register_service.extract_second_dltins_link(register_xml)

        LOGGER.info("Selected DLTINS ZIP URL: %s", zip_url)

        zip_bytes = self.http_client.download_bytes(zip_url)
        instrument_xml = self.zip_service.extract_xml_content(zip_bytes)

        records = self.instrument_service.parse_instruments(instrument_xml)
        LOGGER.info("Parsed %s instrument records", len(records))

        dataframe = self.dataframe_service.to_dataframe(records)
        self.dataframe_service.save_csv(dataframe, output_path)

        self.storage_client.upload_file(output_path, S3_DESTINATION_PATH)

        LOGGER.info("CSV successfully written to %s", output_path)
        return output_path

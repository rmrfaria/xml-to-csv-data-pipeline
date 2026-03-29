"""Application entry point for the XML to CSV data pipeline."""

from data_pipeline.clients.http_client import HTTPClient
from data_pipeline.logging_config import configure_logging
from data_pipeline.services.dataframe_service import DataFrameService
from data_pipeline.services.instrument_xml_service import InstrumentXMLService
from data_pipeline.services.pipeline_service import PipelineService
from data_pipeline.services.register_service import RegisterService
from data_pipeline.services.zip_service import ZipService
from data_pipeline.storage.s3_storage import S3StorageClient


def main() -> None:
    """Run the XML to CSV data pipeline."""
    configure_logging()

    pipeline_service = PipelineService(
        http_client=HTTPClient(),
        register_service=RegisterService(),
        zip_service=ZipService(),
        instrument_service=InstrumentXMLService(),
        dataframe_service=DataFrameService(),
        storage_client=S3StorageClient(),
    )
    pipeline_service.run()


if __name__ == "__main__":
    main()

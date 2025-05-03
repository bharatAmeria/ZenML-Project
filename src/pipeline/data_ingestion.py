import sys
from zenml.pipelines import pipeline
from src.constants import *
from src.components.data_ingestion import IngestData
from src.logger import logging
from src.exception import MyException

@pipeline(enable_cache=True)
class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        data_ingestion = IngestData()
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
    except MyException as e:
            raise MyException(e, sys)
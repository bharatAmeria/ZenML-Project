import sys
import pandas as pd

from zenml.pipelines import pipeline
from src.constants import *
from src.config import Config
from src.logger import logging
from src.exception import MyException
from src.components.data_preprocessing import DataPreprocessing

@pipeline(enable_cache=True)
class DataProcessingPipeline:
    def __init__(self):
        pass

    def main():

        logging.info(">>>>>Data Preprocessing Started...<<<<<")
        data_processing = DataPreprocessing()
        data_processing.handle_data()
        logging.info(">>>>>Data Preprocessing Completed<<<<<\n")

        return 


if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} started <<<<<<")
        obj = DataProcessingPipeline()
        obj.main()
        logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} completed <<<<<<\nx==========x")
    except MyException as e:
            raise MyException(e, sys)

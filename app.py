import sys
import pandas as pd
from zenml import pipeline, step
from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.components.dataIngestion import download_file_step, extract_zip_step
from src.components.data_preprocessing import DataPreProcessing, DataPreprocessStrategy
from src.components.model import ModelTrainingConfig, ModelTraining
from src.config import CONFIG

@step
def ingest_data():
    try:
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
        zip_path = download_file_step()
        extract_zip_step(zip_path)
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(f"Error during ingestion: {e}")
        raise MyException(e, sys)

@step
def preprocess_data():
    """
    ZenML step that preprocesses the raw data using the strategy pattern.
    """
    try:
        raw_data = pd.read_csv(CONFIG["data_path"])
        strategy = DataPreprocessStrategy()
        processor = DataPreProcessing(data=raw_data, strategy=strategy)
        processed_df = processor.handle_data()
        return processed_df
    except Exception as e:
        raise MyException(e, sys)


@step
def train_model():
    try:
        df = pd.read_csv(CONFIG["processed_data_path"])
        logging.info(">>>>>Model Training Started...<<<<<")
        model_training_strategy = ModelTraining(data=df, strategy=ModelTrainingConfig())
        train = model_training_strategy.handle_training()
        logging.info(">>>>>Model Training Completed<<<<<\n")
        return train
    except MyException as e:
        logging.exception(e, sys)
        raise e
    

@pipeline
def training_pipeline():
    ingest_data()
    preprocess_data()
    train_model()


# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":
    try:
        training_pipeline()
    except Exception as e:
        logging.error("Pipeline failed")
        raise e
import sys
import pandas as pd
from zenml.pipelines import pipeline
from src.logger import logging
from src.exception import MyException
from src.components.model import ModelTraining
from src.config import CONFIG

@pipeline(enable_cache=True)
class ModelPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        
        df = pd.read_csv(CONFIG["processed_data_path"])

        logging.info(">>>>>Model Training Started...<<<<<")
        model_training_strategy = ModelTraining()
        X_train, X_test, y_train, y_test = model_training_strategy.train_test_split()
        model_training_strategy.handle_training(X_train, X_test, y_train, y_test)

        logging.info(">>>>>Model Training Completed<<<<<\n")

        return training
    
if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage started <<<<<<")
        obj = ModelPipeline()
        obj.main()
        logging.info(f">>>>>> stage completed <<<<<<\nx==========x")
    except MyException as e:
            raise MyException(e, sys)
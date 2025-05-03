import os
import sys
import pandas as pd
import numpy as np

from zenml import step
from config import Config
from src.logger import logging
from src.exception import MyException

class DataPreprocessing:
    """
    Data preprocessing strategy which preprocesses the data.
    """
    def __init__(self):
        logging.info("Data Preprocessing class initialized.")

    @step
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Removes columns which are not required, fills missing values with median average values,
        and converts the data type to float.
        """
        try:
            Config.validate()
            data = pd.read_csv("")
            
            df = data
            df.drop('Unnamed: 0', axis=1, inplace=True)
            df.drop_duplicates(inplace=True)

            to_drop = df[df['average_rain_fall_mm_per_year'].apply(self.isStr)].index
            df = df.drop(to_drop)

            df['average_rain_fall_mm_per_year'] = df['average_rain_fall_mm_per_year'].astype(np.float64)

            save_path = Config.PROCESSED_DATA
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_csv(save_path, index=False)
            logging.info(f"Successfully saved processed data to {save_path}")

        except Exception as e:
            logging.error("Error occurred in Processing data", exc_info=True)
            raise MyException(e, sys)
        
    def isStr(self, obj):
        try:
            float(obj)
            return False
        except:
            return True
 
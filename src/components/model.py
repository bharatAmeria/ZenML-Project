import os
import sys
import joblib
import numpy as np
import pandas as pd
from zenml.steps import step

from src.config import Config
from src.logger import logging
from src.exception import MyException

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error,r2_score

class ModelTraining:

    def __init__(self):
        pass

    @step
    def handle_training(self, X_train: pd.DataFrame, X_test: pd.DataFrame, 
                     y_train: pd.Series, y_test: pd.Series):

        try:
            ohe = OneHotEncoder(drop='first')
            scale = StandardScaler()

            preprocesser = ColumnTransformer(
                    transformers = [
                        ('StandardScale', scale, [0, 1, 2, 3]), 
                        ('OHE', ohe, [4, 5]),
                    ],
                    remainder='passthrough'
            )

            X_train_dummy = preprocesser.fit_transform(X_train)
            X_test_dummy = preprocesser.transform(X_test)
            preprocesser.get_feature_names_out(col[:-1])

            models = {
                    'lr':LinearRegression(),
                    'lss':Lasso(),
                    'Rid':Ridge(),
                    'Dtr':DecisionTreeRegressor()
                }
            
            for name, md in models.items():
                md.fit(X_train_dummy,y_train)
                y_pred = md.predict(X_test_dummy)

                print(f"{name} : mae : {mean_absolute_error(y_test,y_pred)} score : {r2_score(y_test,y_pred)}")

            dtr = DecisionTreeRegressor()
            dtr.fit(X_train_dummy,y_train)
            dtr.predict(X_test_dummy)

        except Exception as e:
            logging.error("Error occurred while extracting zip file", exc_info=True)
            raise MyException(e, sys)

    @step  
    def train_test_split(self, df: pd.DataFrame):
        try:
            # Select specific columns
            col = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 
                'avg_temp', 'Area', 'Item', 'hg/ha_yield']
            df = df[col]
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            logging.info("Data preparation and splitting completed successfully.")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"Error during data preparation: {str(e)}")
            raise MyException(e, sys)

 
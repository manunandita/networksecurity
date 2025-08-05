import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifact_entity import DataArtifacts

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URL_PATH=os.getenv("MONGO_DB_URL")

class DataIngestion():
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def extract_data_from_mongodb(self):
        try:
            self.mongo_db=MongoClient(MONGO_URL_PATH)
            data=self.mongo_db[self.data_ingestion_config.database_name][self.data_ingestion_config.collection_name]
            df=pd.DataFrame(list(data.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_to_feature(self,dataframe:pd.DataFrame):
        try:
            dir_path=os.path.dirname(self.data_ingestion_config.feature_data_dir)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(self.data_ingestion_config.feature_data_dir,header=True,index=False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_train_test_split(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("train test split initiated")

            train_dir=os.path.dirname(self.data_ingestion_config.train_data_dir)
            os.makedirs(train_dir,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.train_data_dir,index=False,header=True)

            logging.info("train data has ingested to train.csv file")

            test_dir=os.path.dirname(self.data_ingestion_config.test_data_dir)
            os.makedirs(test_dir,exist_ok=True)
            test_set.to_csv(self.data_ingestion_config.test_data_dir,index=False,header=True)

            logging.info("test data has ingested to test.csv file")


        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_ingestion(self):
        try:
            dataframe=self.extract_data_from_mongodb()
            df=self.export_data_to_feature(dataframe)
            self.initiate_train_test_split(df)
            data_ingested_artifacts=DataArtifacts(self.data_ingestion_config.train_data_dir,self.data_ingestion_config.test_data_dir)
            return data_ingested_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
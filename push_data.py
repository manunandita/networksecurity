from dotenv import load_dotenv
import os
from pymongo import MongoClient
import sys

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataPush():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=data.to_dict(orient="records")
            logging.info("data converted csv to json")
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection
            self.mongodb_url=MongoClient(MONGO_DB_URL)
            self.database=self.mongodb_url[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info("data inserted to mongodb")
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=="__main__":
    FILE_PATH_URL="network_data/phisingData.csv"
    DATABASE="ML_project"
    COLLECTION="phising_data"
    networkobj=NetworkDataPush()
    records=networkobj.csv_to_json(FILE_PATH_URL)
    no_of_records=networkobj.insert_data_to_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)
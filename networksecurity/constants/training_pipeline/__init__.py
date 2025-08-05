import os
import sys
import numpy as np
import pandas as pd

DATA_INGESTION_COLLECTION_NAME:str="phising_data"
DATA_INGESTION_DATABASE_NAME:str="ML_project"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

TARGET_COLUMN="Result"
TRAIN_DATA:str="train.csv"
TEST_DATA:str="test.csv"
PIPELINE_DIR:str="networksecurity"
ARTIFACTS_DIR:str="artifacts"
DATA_FILE_DIR:str="phising_data.csv"
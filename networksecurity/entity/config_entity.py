import os
from datetime import datetime
from networksecurity.constants import training_pipeline


class TrainingPipeline():
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%Y_%m_%d_%H_%M_%S")
        self.timestamp:str=timestamp
        self.pipeline_name=training_pipeline.PIPELINE_DIR
        self.artifacts_name=training_pipeline.ARTIFACTS_DIR
        self.artifacts_dir=os.path.join(self.artifacts_name,timestamp)


class DataIngestionConfig():
    def __init__(self,training_pipeline_config:TrainingPipeline):
        self.data_ingestion_dir=os.path.join(
            training_pipeline_config.artifacts_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_data_dir=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.DATA_FILE_DIR
        )
        self.train_data_dir=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED,training_pipeline.TRAIN_DATA
        )
        self.test_data_dir=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED,training_pipeline.TEST_DATA
        )
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeline
import sys


if __name__=="__main__":
    try:
        logging.info("calling the main folder")
        training_pipeline_obj=TrainingPipeline()
        data_config_obj=DataIngestionConfig(training_pipeline_obj)
        data_obj=DataIngestion(data_config_obj)
        path=data_obj.initiate_data_ingestion()
        print(path)

        logging.info("path of train and test has been printed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeline,DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifacts,DataIngestionArtifacts

import sys


if __name__=="__main__":
    try:
        logging.info("calling the main folder")
        training_pipeline_obj=TrainingPipeline()
        data_ingestion_obj=DataIngestionConfig(training_pipeline_obj)
        data_obj=DataIngestion(data_ingestion_obj)
        path=data_obj.initiate_data_ingestion()
        print(path)

        data_validation_obj=DataValidationConfig(training_pipeline_obj)
        data_valid_obj=DataValidation(path,data_validation_obj)
        path_validation=data_valid_obj.initiate_data_validation()
        print(path_validation)

        logging.info("path of train and test has been printed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
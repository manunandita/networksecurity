from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants import training_pipeline
from networksecurity.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation():
    def __init__(self,
                 data_ingested_artifacts:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingested_artifacts=data_ingested_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path) 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_no_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            no_of_columns=len(self._schema_config["columns"])
            logging.info(f"required number of columns {no_of_columns}")
            logging.info(f"the dataframe has {len(dataframe.columns)} columns")
            if len(dataframe.columns)==no_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_columns(self,data_frame:pd.DataFrame) -> bool:
        try:
            numeric_columns=self._schema_config["numerical_columns"]
            for column in range(len(numeric_columns)):
                if list(data_frame.columns)[column]==numeric_columns[column]:
                    return True
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self,base_data:pd.DataFrame,current_data:pd.DataFrame,threshold=.05) -> bool:
        try:
            report={}
            status=False
            for column in base_data.columns:
                d1=base_data[column]
                d2=current_data[column]
                is_same_dist,p_value=ks_2samp(d1,d2)
                if threshold<=p_value:
                    is_drift=False
                else:
                    is_drift=True
                    status=True
                report.update(
                {column:{
                    "pvalue":float(p_value),
                    "is drift exist":is_drift
                }}
                )
            drift_report_file_path=self.data_validation_config.drift_report_dir
            write_yaml_file(drift_report_file_path,report,status)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def initiate_data_validation(self):
        try:
            train_file_path=self.data_ingested_artifacts.train_file_path
            test_file_path=self.data_ingested_artifacts.test_file_path

            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            train_status=self.validate_no_of_columns(train_dataframe)
            if train_status==False:
                logging.info("train data has not same number of columns")

            test_status=self.validate_no_of_columns(test_dataframe)
            if test_status==False:
                logging.info("test data has not same number of columns")

            train_numeric_status=self.validate_numerical_columns(train_dataframe)
            if train_numeric_status==False:
                logging.info("train data has not same numerical columns")

            test_numeric_status=self.validate_numerical_columns(test_dataframe)
            if test_numeric_status==False:
                logging.info("test data has not same numerical columns")

            status=self.detect_data_drift(train_dataframe,test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_dir)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_dir,index=False,header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_dir,index=False,header=True
            )
            data_validation_artifacts=DataValidationArtifacts(
                validation_status=status,
                valid_train_path=self.data_validation_config.valid_train_dir,
                valid_test_path=self.data_validation_config.valid_test_dir,
                invalid_train_path=None,
                invalid_test_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_dir
            )
            return data_validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
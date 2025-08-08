import dill
import yaml
import pickle
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import os,sys

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path,content,report) -> None:
    try:
        dir_path=os.path.dirname(file_path)
        if report==True:
            if os.path.exists(file_path):
               os.remove(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
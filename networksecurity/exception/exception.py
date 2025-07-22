from networksecurity.logging.logger import logging
import sys

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        _,_,exc_tb=error_details.exc_info()

        self.error_message=error_message
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured as [{0}] in file [{1}] in line number [{2}]".format(self.error_message,self.lineno,self.filename)
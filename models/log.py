"""Logger class for applications"""
__author__ = "Vitali Muladze"


import inspect
import logging
from logging.handlers import SMTPHandler

from flask import has_request_context, request

from source.configuration import files, mail_config


class RequestFormatter(logging.Formatter):
    """Request parser for application"""
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter('[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s in %(module)s: %(message)s')


class Logger:
    logging_format = formatter
    logger_name = 'FaissServer'
    logger_file_info = files.log_file_info
    logger_file_error = files.log_file_error

    def __init__(self):
        """Create logger instance which handles file insertion and printing"""
        # Create logger formatter and instance
        self.log = logging.getLogger(self.logger_name)
        self.log.setLevel(logging.DEBUG)
        log_formatter = self.logging_format
        # Info type logs formatter
        file_handler_info = logging.FileHandler(self.logger_file_info, mode='a', encoding="utf-8")
        file_handler_info.setFormatter(log_formatter)
        file_handler_info.setLevel(logging.INFO)
        self.log.addHandler(file_handler_info)
        # Error type logs formatter
        file_handler_error = logging.FileHandler(self.logger_file_error, mode='a', encoding="latin-1")
        file_handler_error.setFormatter(log_formatter)
        file_handler_error.setLevel(logging.ERROR)
        self.log.addHandler(file_handler_error)
        # Send errors to mail
        mail_handler = SMTPHandler(
            mailhost=mail_config.host,
            fromaddr=mail_config.sender,
            toaddrs=mail_config.send_mail_to,
            subject='Internal Control services Application Error'
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(log_formatter)
        self.log.addHandler(mail_handler)

    def log_event(self, message: str = "", error: bool = False) -> None:
        """Function for logging events"""
        # Get the message which contains function, line and message
        message = "{} at line {}: {}".upper().format(*self.__get_call_info(), message)
        if error:
            self.log.error(message)
        else:
            self.log.info(message)

    @staticmethod
    def __get_call_info():
        """Get the function and line from calling"""
        stack = inspect.stack()
        line = stack[2][2]
        _function = stack[2][3]

        return _function.upper(), line

    def get_logger(self):
        return self.log

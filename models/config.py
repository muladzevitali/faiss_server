"""Configuration class for applications"""
__author__ = "Vitali Muladze"

import configparser
import os

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")


class OracleDatabase:
    """Configuration class for oracle databases"""

    def __init__(self):
        self.database_uri = config["DATABASE"]["URI"]

    def get_connection_string(self) -> str:
        return "sqlite:///" + os.path.join(os.getcwd(), self.database_uri)


class Application:
    """Configuration class for an application"""
    SECRET_KEY = config["APPLICATION"]["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True if config["APPLICATION"][
                                                 "SQLALCHEMY_TRACK_MODIFICATIONS"] is "true" else False
    SQLALCHEMY_ECHO = True if config["APPLICATION"]["SQLALCHEMY_ECHO"] is "true" else False
    SQLALCHEMY_DATABASE_URI = OracleDatabase().get_connection_string()
    WTF_CSRF_SECRET_KEY = "SecretBogGe"

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def create_all_folders():
        os.makedirs(Files.media_path, exist_ok=True)
        os.makedirs("media/logs", exist_ok=True)


class Files:
    """Configuration class for files"""
    media_path = config["FILES"]["MEDIA_PATH"]
    log_file_info = config["LOGGER"]["LOG_FILE_INFO"]
    log_file_error = config["LOGGER"]["LOG_FILE_ERROR"]
    index_path = config["FILES"]["FAISS_INDEX_PATH"]
    backup_index_path = config["FILES"]["BACKUP_INDEX_PATH"]


class MailConfiguration:
    """Configuration class for mail"""
    host = config["MAIL"]["HOST"]
    port = config["MAIL"]["PORT"]
    sender = config["MAIL"]["FROM"]
    send_mail_to = config["LOGGER"]["SEND_MAIL_TO"]


class FaissConfiguration:
    dimension = int(config["FAISS_DATABASE"]["INDEX_DIMENSION"])

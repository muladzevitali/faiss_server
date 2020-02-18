"""Common functions and objects for application different parts"""
__author__ = "Vitali Muladze"

import atexit
import functools

from flask import request
from flask_restful import abort
from jwt import decode, DecodeError, ExpiredSignatureError

from models.faiss_database import FaissIndex
from models.users import User
from source.configuration import (application_config, files, faiss_configuration)

faiss_index = FaissIndex(files.index_path, faiss_configuration.dimension)


def exit_handler(index: FaissIndex) -> None:
    """
    Write faiss in the disk on process termination
    :param index: faiss index
    """
    index.to_disk(files.backup_index_path)


# Register the function at exit
atexit.register(exit_handler, faiss_index)


def login_required(method):
    """
    Check if the user is logged in
    """

    @functools.wraps(method)
    def wrapper(_):
        # Get the token from header
        token = request.headers.get('Authorization')
        if not token:
            abort(http_status_code=401, message='Authorization required.')
        try:
            # Try to decode the token
            decoded = decode(token, application_config.SECRET_KEY, algorithms='HS256')
        except DecodeError:
            abort(http_status_code=403, message='Token invalid.')
            return
        except ExpiredSignatureError:
            abort(http_status_code=403, message='Token expired.')
            return
        # Get the username from decoded token
        username = decoded['username']
        # Check if the username exist in our database
        user = User.query.get(username)
        if not user:
            abort(http_status_code=404, message='User not found.')

        return method(user)

    return wrapper

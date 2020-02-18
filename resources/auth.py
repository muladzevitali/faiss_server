"""Authorization endpoints for applications"""
__author__ = "Vitali Muladze"

import datetime

from flask import request, current_app
from flask_restful import Resource, abort
from jwt import encode
from werkzeug.local import LocalProxy

from apps import db
from models.users import User
from source.configuration import application_config

logger = LocalProxy(lambda: current_app.logger)


class Register(Resource):
    """Register a user"""

    def post(self):
        # Get username and password from request
        username = request.json.get('username')
        password = request.json.get('password')
        # Check if password is short
        if len(password) < 8:
            logger.info(f"username: {username} tried to register with short password.")
            abort(http_status_code=401, message='Password too short.')
        # Check if username is already taken
        if User.query.get(username):
            logger.info(f"username: {username} tried to register with already taken username.")
            abort(http_status_code=402, message='Username already taken.')
        # Create new user
        new_user = User(username=username)
        new_user.hash_password(password)
        new_user.active = False
        # Insert user into the database
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"username: {username} registered for the service.")

        return {'username': username}


class Login(Resource):
    """User authorization"""

    def post(self):
        # Get username and password from request
        username = request.json.get('username')
        password = request.json.get('password')
        # Find specified username in database
        user = User.query.get(username)
        # If no user was found
        if not user:
            logger.info(f"username: {username} tried to login with wrong username.")
            abort(http_status_code=404, message='User not found.')
        # Verify the password
        if not user.verify_password(password):
            logger.info(f"username: {username} tried to login with wrong password.")
            abort(http_status_code=406, message='Password incorrect.')
        # Expiration date for each user
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=24 * 30)
        # Encode user information to get a token
        encoded = encode({'username': username, 'exp': expiration_date},
                         application_config.SECRET_KEY, algorithm='HS256')
        logger.info(f"username: {username} logged in the system with token: {encoded.decode('utf-8')}.")

        return {'username': username, 'token': encoded.decode('utf-8')}

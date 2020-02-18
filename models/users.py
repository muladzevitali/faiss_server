"""User class for applications"""
__author__ = "Vitali Muladze"

from passlib.apps import custom_app_context as pwd_context

from apps import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer)
    username = db.Column(db.String(32), primary_key=True, index=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)

    def hash_password(self, password: str) -> None:
        """
        Hash the password
        :param password: password to hash
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify the password
        :param password: password to verify with the user password
        :return: Are they equal or not
        """
        return pwd_context.verify(password, self.password_hash)

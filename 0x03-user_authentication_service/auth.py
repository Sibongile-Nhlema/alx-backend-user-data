#!/usr/bin/env python3
'''
Auth module
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    '''
    Hashes a password string using bcrypt
    returns the hashed password in bytes
    '''
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed_bytes


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        Registers a user with the provided email and password.
        '''
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''
        Validate login credentials.
        '''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

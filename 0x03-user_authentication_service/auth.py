#!/usr/bin/env python3
'''
Auth module
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


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

    def create_session(self, email: str) -> str:
        '''
        Create a new session for the user and return the session ID
        '''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    '''
    Generate a new UUID and return it as a string.
    '''
    return str(uuid.uuid4())

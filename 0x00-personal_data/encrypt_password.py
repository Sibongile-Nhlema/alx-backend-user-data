#!/usr/bin/env python3
'''
function that expects one string argument name password and returns a salted,
hashed password, which is a byte string.
'''
import bcrypt


def is_valid(hashed_pwd: bytes, password: str) -> bool:
    """
    Args:
        hashed_pwd (bytes): hashed password to compare with
        password (str): plaintext password
    Returns:
        bool: True matche, otherwise False.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pwd)


def hash_password(password: str) -> bytes:
    '''
    Args:
        password (str): password to hash.
    Returns:
        bytes: hashed password as bytes.
    '''
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd

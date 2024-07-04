#!/usr/bin/env python3
'''
function that expects one string argument name password and returns a salted,
hashed password, which is a byte string.
'''
import bcrypt


def is_valid(hash_password: bytes, password: str) -> bool:
    """
    Args:
        hashed_pwd (bytes): hashed password to compare with
        password (str): plaintext password
    Returns:
        bool: True matche, otherwise False.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)


def hash_password(password: str) -> bytes:
    '''
    Args:
        password (str): password to hash.
    Returns:
        bytes: hashed password as bytes.
    '''
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password

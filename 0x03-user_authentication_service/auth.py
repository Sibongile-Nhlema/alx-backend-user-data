#!/usr/bin/env python3
'''
Auth module
'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''
    Hashes a password string using bcrypt
    returns the hashed password in bytes
    '''
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed_bytes

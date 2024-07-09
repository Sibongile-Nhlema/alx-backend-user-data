#!/usr/bin/env python3
'''
This module houses the Auth Class
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    A class to manage API authentication
    '''
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        '''
        Checks if authentication is required for the given path.
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''
        Retrieves the authorization header from the request.
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Retrieves information about the current user from the request.
        '''
        return None

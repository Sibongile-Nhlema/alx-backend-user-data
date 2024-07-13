#!/usr/bin/env python3
'''
This module houses the Auth Class
'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''
    A class to manage API authentication
    '''
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        '''
        Checks if authentication is required for the given path.
        '''
        if not path:
            return True

        if not excluded_paths:
            return True

        normal_path = path.rstrip('/') + '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if normal_path == excluded_path:
                    return False
            else:
                if normal_path == excluded_path + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
        Retrieves the authorization header from the request.
        '''
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Retrieves information about the current user from the request.
        '''
        return None

    def session_cookie(self, request=None):
        '''
        Retrieves the session cookie value from a request.

        Args:
            request: request object.
        Returns:
            str: value of the session cookie or None
        '''
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        session_cookie = request.cookies.get(session_name)
        return session_cookie

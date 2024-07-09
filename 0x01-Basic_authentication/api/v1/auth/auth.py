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

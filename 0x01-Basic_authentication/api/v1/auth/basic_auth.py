#!/usr/bin/env python3
'''
Module for the implementaion of Basic Auth
'''
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    '''
    Class for the BasicAuth implementation
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
        function that returns the Base64 part of the Authorization
        header for a Basic Authentication
        '''
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        base64_part = authorization_header.split(" ")[1].strip()

        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        Function that returns the decoded value of a Base64
        string base64_authorization_header
        '''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        Extracts user email and password from Base64 decoded value.
        '''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''
        method that returns the User instance based on his email and password.
        '''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user_list = User.search({'email': user_email})
        if not user_list:
            return None
        else:
            user = user_list[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Method to retrieve the User instance for a request.
        '''
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if not base64_header:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if not user_email or not user_pwd:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)

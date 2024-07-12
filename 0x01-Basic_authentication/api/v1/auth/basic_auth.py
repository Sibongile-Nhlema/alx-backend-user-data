#!/usr/bin/env python3
'''
Module for the implementaion of Basic Auth
'''
from api.v1.auth.auth import Auth
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
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

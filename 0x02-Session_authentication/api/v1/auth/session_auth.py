#!/usr/bin/env python3
'''
Module for the implementaion of SessionAuth
'''
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''
    Class for the SessionAuth implementation
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        Creates a Session ID for a user_id.

        Args:
            user_id (str): ID of the user for whom the session is created.

        Returns:
            str: generated Session ID or None
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Retrieves a User ID based on a Session ID.

        Args:
            session_id (str): Session ID to find.
        Returns:
            str: User ID or None
        '''
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

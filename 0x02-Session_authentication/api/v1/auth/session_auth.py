#!/usr/bin/env python3
'''
Module for the implementaion of SessionAuth
'''
from api.v1.auth.auth import Auth
import uuid
from models.user import User


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

    def current_user(self, request=None):
        '''
        Returns a User instance based on a cookie value
        '''
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes user session / logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True

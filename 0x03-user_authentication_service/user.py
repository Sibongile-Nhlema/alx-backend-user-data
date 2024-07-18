#!/usr/bin/env python3
'''
SQLAlchemy model, Users
'''
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    '''
    SQLAlchemy model for the users table.

    Attributes:
        id (int): primary key
        email (str): user's email address
        hashed_password (str): user's hashed password
        session_id (str): user's session ID
        reset_token (str): user's reset token

    '''
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

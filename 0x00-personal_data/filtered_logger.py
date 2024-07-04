#!/usr/bin/env python3
'''
Module that handles the filter_datum function
'''
import re
import logging
from typing import List, Tuple
import os
import mysql.connector


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    Connects to a MySQL db using credentials from env variables
    '''
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # make the connection to the database
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection


def get_logger() -> logging.Logger:
    '''
    Creates and configures a logger for user
    data with RedactingFormatter
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()

    # Create a RedactingFormatter and set it for the StreamHandler
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
    Args:
        fields (List[str]): list of strings of all fields to obfuscate
        redaction (str): string of the field will be obfuscated.
        message (str): string of the log line.
        separator (str): string of characters
    Returns:
        str: The log message with specified fields obfuscated.
    '''
    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"

    def replace(match):
        '''
        replaces the matched value with the redaction string
        '''
        field_name = match.group(1)
        return f"{field_name}={redaction}"

    obfuscated_message = re.sub(pattern, replace, message)

    return obfuscated_message


class RedactingFormatter(logging.Formatter):
    '''
    Redacting Formatter class for obfuscating sensitive
    information in log messages.
    '''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        Initializes the RedactingFormatter
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        Args:
            record (logging.LogRecord): The log record to be formatted.
        Returns:
            str: The formatted log message with sensitive fields obfuscated.
        '''
        original_message = super(RedactingFormatter, self).format(record)

        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        return filtered_message

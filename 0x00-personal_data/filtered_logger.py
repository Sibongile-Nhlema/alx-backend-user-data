#!/usr/bin/env python3
'''
Module that handles the filter_datum function
'''
import re
import logging
from typing import List


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

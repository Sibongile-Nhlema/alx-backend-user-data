#!/usr/bin/env python3
'''
Module that handles the filter_datum function
'''
import re
from typing import List


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

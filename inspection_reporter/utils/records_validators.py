from django.core.exceptions import ValidationError

from inspection_reporter.utils.records_constants import ABBREV_STATE

import re
from datetime import datetime


def valid_char(val):
    """Checks a string for non alphabetic characters."""
    if not val.isalpha():
        raise ValidationError(
            'field must only contain letters, no numbers or special characters'
        )


def valid_state_abbrev(val):
    """validates state code"""
    val = val.upper()
    if val not in ABBREV_STATE:
        raise ValidationError(
            'not a valid state abbreviation'
        )


def valid_zip(val):
    """assuming 5 digit zip"""
    if not val.isdigit():
        raise ValidationError(
            'should be a simple 5 digit zip code'
        )


def has_invalid_char(val):
    special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return special_chars.search(val)


def valid_address(val):
    """tests for valid street name and suffix"""
    if has_invalid_char(val):
        raise ValidationError(
            'address can not have [@_!$%^&*()<>?/\|}{~:]'
        )
    name = val.split(' ')
    name_length = len(name)
    if name_length <= 1:
        raise ValidationError(
            'address must be at least a street number and street name')


def valid_score(val):
    if val > 100 or val < 0:
        raise ValidationError(
            'score must be 0 - 100'
        )


def valid_date(val):
    if val > datetime.date(datetime.now()):
        raise ValidationError(
            'no future date allowed'
        )


def valid_id(val):
    if val < 0:
        raise ValidationError(
            'must be a non negative integer')

from rest_framework.serializers import ValidationError
from inspection_reporter.utils.records_constants import ABBREV_STATE

def is_valid_char(val):
    """Checks a string for non alphabetic characters."""
    if val.isalpha():
        return val
    else:
        raise ValidationError(
            'field must only contain letters, no numbers or special characters'
        )

def is_valid_state_abbrev(val):
    """validates state code"""
    val = val.upper()
    if val in ABBREV_STATE:
        return val
    else:
        raise ValidationError(
            'not a valid state abbreviation'
    )
    
def is_valid_zip(val):
    """assuming 5 digit zip"""
    if val.isdigit():
        return val
    else:
        raise ValidationError(
        'should be a simple 5 digit zip code'
    )

def is_valid_address(val):
    """tests for valid street name and suffix"""
    return val

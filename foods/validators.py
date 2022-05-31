
from django.core.exceptions import ValidationError


def article_number_validator(value):
    ''' Check if the current value contains only digits. '''
    if not value.isdigit():
        raise ValidationError('The article number `%(value)s` contains non-digit characters', params={
            'value': value
        })
    if len(value) != 13 and len(value) != 8:
        raise ValidationError('The article number `%(value)s` has an invalid length', params={
            'value': value
        })

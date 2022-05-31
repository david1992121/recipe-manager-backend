from django.core.exceptions import ValidationError
from pycountry import currencies


def currency_code_validator(value):
    ''' Check if the currency code value is valid. '''
    if currencies.get(alpha_3=value) is None:
        raise ValidationError(
            'The currency code `%(value)s` is not valid',
            params={
                'value': value})


def rate_validator(value):
    ''' Check if the rate is valid for a positive floating number. '''
    try:
        f = float(value)
    except BaseException:
        raise ValidationError('The rate `%(value)s` is not valid', params={
            'value': value
        })

    if f <= 0:
        raise ValidationError('The rate `%(value)s` is not positive', params={
            'value': value
        })

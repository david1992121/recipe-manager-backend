from django.conf import settings


def convert_to_str(value):
    return str(round(value, settings.COST_PRECISION))

from django.core.exceptions import ImproperlyConfigured
try:
    from json_field.fields import JSONField
except (ImportError, ImproperlyConfigured):
    pass # fails when imported by setup.py, no worries

__version__ = '0.4.2'

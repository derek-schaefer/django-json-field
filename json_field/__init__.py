try:
    from json_field.fields import JSONField
except ImportError:
    pass # fails when imported by setup.py, no worries

__version__ = '0.3'

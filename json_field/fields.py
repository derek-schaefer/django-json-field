from json_field.forms import JSONFormField

from django.db import models
from django.utils import simplejson as json
from django.core import exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

import re
from datetime import datetime
try:
    from dateutil import parser as date_parser
except ImportError:
    raise ImproperlyConfigured('The "dateutil" library is required and was not found.')

try:
    JSON_DECODE_ERROR = json.JSONDecodeError # simplejson
except AttributeError:
    JSON_DECODE_ERROR = ValueError # other

TIME_RE = re.compile(r'^\d{2}:\d{2}:\d{2}')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}(?!T)')
DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T')

class JSONDecoder(json.JSONDecoder):
    """ Recursive JSON to Python deserialization. """

    _recursable_types = [str, unicode, list, dict]

    def _is_recursive(self, obj):
        return type(obj) in JSONDecoder._recursable_types

    def decode(self, obj, *args, **kwargs):
        if not kwargs.get('recurse', False):
            obj = super(JSONDecoder, self).decode(obj, *args, **kwargs)
        if isinstance(obj, list):
            for i in xrange(len(obj)):
                item = obj[i]
                if self._is_recursive(item):
                    obj[i] = self.decode(item, recurse=True)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if self._is_recursive(value):
                    obj[key] = self.decode(value, recurse=True)
        elif isinstance(obj, basestring):
            if TIME_RE.match(obj):
                try:
                    return date_parser.parse(obj).time()
                except ValueError:
                    pass
            if DATE_RE.match(obj):
                try:
                    return date_parser.parse(obj).date()
                except ValueError:
                    pass
            if DATETIME_RE.match(obj):
                try:
                    return date_parser.parse(obj)
                except ValueError:
                    pass
        return obj

class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    __metaclass__ = models.SubfieldBase

    description = 'JSON object'

    def __init__(self, *args, **kwargs):
        self.default_error_messages = {
            'invalid': _(u'Enter a valid JSON object')
        }
        self._db_type = kwargs.pop('db_type', None)
        self.simple_formfield = kwargs.pop('simple_formfield', False)

        encoder = kwargs.pop('encoder', DjangoJSONEncoder)
        decoder = kwargs.pop('decoder', JSONDecoder)
        encoder_kwargs = kwargs.pop('encoder_kwargs', {})
        decoder_kwargs = kwargs.pop('decoder_kwargs', {})
        if not encoder_kwargs and encoder:
            encoder_kwargs.update({'cls':encoder})
        if not decoder_kwargs and decoder:
            decoder_kwargs.update({'cls':decoder})
        self.encoder_kwargs = encoder_kwargs
        self.decoder_kwargs = decoder_kwargs

        kwargs['default'] = kwargs.get('default', 'null')
        kwargs['help_text'] = kwargs.get('help_text', self.default_error_messages['invalid'])

        super(JSONField, self).__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        if self._db_type:
            return self._db_type
        return super(JSONField, self).db_type(*args, **kwargs)

    def to_python(self, value):
        if value is None: # allow blank objects
            return None
        if isinstance(value, basestring):
            try:
                value = json.loads(value, **self.decoder_kwargs)
            except JSON_DECODE_ERROR:
                pass
        return value

    def get_db_prep_value(self, value, *args, **kwargs):
        if self.null and value is None and not kwargs.get('force'):
            return None
        return json.dumps(value, **self.encoder_kwargs)

    def value_to_string(self, obj):
        return self.get_db_prep_value(self._get_val_from_obj(obj))

    def value_from_object(self, obj):
        return json.dumps(super(JSONField, self).value_from_object(obj), **self.encoder_kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': kwargs.get('form_class', JSONFormField),
            'simple': self.simple_formfield,
            'encoder_kwargs': self.encoder_kwargs,
            'decoder_kwargs': self.decoder_kwargs,
        }
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def contribute_to_class(self, cls, name):
        super(JSONField, self).contribute_to_class(cls, name)

        def get_json(model_instance):
            return self.get_db_prep_value(getattr(model_instance, self.attname, None), force=True)
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, value):
            return setattr(model_instance, self.attname, self.to_python(value))
        setattr(cls, 'set_%s_json' % self.name, set_json)

try:
    # add support for South migrations
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^json_field\.fields\.JSONField'])
except ImportError:
    pass

from json_field.forms import JSONFormField

from django.db import models
from django.utils import simplejson as json
from django.core import exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext as _

import decimal
from datetime import datetime
from dateutil import parser as date_parser

class JSONDecoder(json.JSONDecoder):

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
            try:
                return decimal.Decimal(obj) # first since dateutil will consume this
            except decimal.InvalidOperation:
                pass
            try:
                return datetime.strptime(obj, '%H:%M:%S.%f').time() # with microsecond
            except ValueError:
                pass
            try:
                return datetime.strptime(obj, '%H:%M:%S').time() # without microsecond
            except ValueError:
                pass
            try:
                return datetime.strptime(obj, '%Y-%m-%d').date() # simple date
            except ValueError:
                pass
            try:
                return date_parser.parse(obj) # supports multiple formats
            except ValueError:
                pass
        return obj

class JSONField(models.TextField):
    """ Stores and loads valid JSON objects. """

    __metaclass__ = models.SubfieldBase

    description = 'JSON object'

    default_error_messages = {
        'invalid': _(u'Enter a valid JSON object')
    }

    def __init__(self, *args, **kwargs):
        self._db_type = kwargs.pop('db_type', None)
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
        kwargs['default'] = kwargs.get('default', {})
        kwargs['help_text'] = kwargs.get('help_text', self.default_error_messages['invalid'])
        super(JSONField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        if self._db_type:
            return self._db_type
        return super(JSONField, self).db_type(connection)

    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, basestring):
            try:
                value = json.loads(value, **self.decoder_kwargs)
            except json.JSONDecodeError:
                pass
        return value

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return json.dumps(value, **self.encoder_kwargs)

    def value_to_string(self, obj):
        return self.get_db_prep_value(self._get_val_from_obj(obj))

    def value_from_object(self, obj):
        return json.dumps(super(JSONField, self).value_from_object(obj), **self.encoder_kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': kwargs.get('form_class', JSONFormField),
            'encoder_kwargs': self.encoder_kwargs,
            'decoder_kwargs': self.decoder_kwargs,
        }
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

try:
    # add support for South migrations
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^json_field\.fields\.JSONField'])
except ImportError:
    pass

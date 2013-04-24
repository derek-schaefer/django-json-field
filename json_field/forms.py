from django.forms import fields, util
from django.utils import simplejson as json

import datetime
from decimal import Decimal

class JSONFormField(fields.Field):

    def __init__(self, *args, **kwargs):
        from .fields import JSONEncoder, JSONDecoder
        self.evaluate = kwargs.pop('evaluate', False)
        self.encoder_kwargs = kwargs.pop('encoder_kwargs', {'cls':JSONEncoder})
        self.decoder_kwargs = kwargs.pop('decoder_kwargs', {'cls':JSONDecoder, 'parse_float':Decimal})
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # Have to jump through a few hoops to make this reliable
        value = super(JSONFormField, self).clean(value)

        # allow an empty value on an optional field
        if value is None:
            return value

        ## Got to get rid of newlines for validation to work
        # Data newlines are escaped so this is safe
        value = value.replace('\r', '').replace('\n', '')

        if self.evaluate:
            json_globals = { # "safety" first!
                '__builtins__': None,
                'datetime': datetime,
            }
            json_locals = { # value compatibility
                'null': None,
                'true': True,
                'false': False,
            }
            try:
                value = json.dumps(eval(value, json_globals, json_locals), **self.encoder_kwargs)
            except Exception as e: # eval can throw many different errors
                raise util.ValidationError('%s (Caught "%s")' % (self.help_text, e))

        try:
            json.loads(value, **self.decoder_kwargs)
        except ValueError as e:
            raise util.ValidationError('%s (Caught "%s")' % (self.help_text, e))

        return value

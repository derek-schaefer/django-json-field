from django.forms import fields, util
from django.utils import simplejson as json

import datetime
import decimal

class JSONFormField(fields.Field):

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        self.encoder_kwargs = kwargs.pop('encoder_kwargs')
        self.decoder_kwargs = kwargs.pop('decoder_kwargs')
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # Have to jump through a few hoops to make this reliable
        value = super(JSONFormField, self).clean(value)

        ## Got to get rid of newlines for validation to work
        # Data newlines are escaped so this is safe
        value = value.replace('\r', '').replace('\n', '')

        json_globals = { # safety first!
            '__builtins__': None,
        }
        if not self.simple: # optional restriction
            json_globals.update({
                'datetime': datetime,
                'Decimal': decimal.Decimal,
            })
        json_locals = { # value compatibility
            'null': None,
            'true': True,
            'false': False,
        }
        try:
            value = json.dumps(eval(value, json_globals, json_locals), **self.encoder_kwargs)
        except Exception, e: # eval can throw many different errors
            raise util.ValidationError('%s (Caught "%s")' % (self.help_text, e))

        try:
            json.loads(value, **self.decoder_kwargs)
        except ValueError, e:
            raise util.ValidationError('%s (Caught "%s")' % (self.help_text, e))

        return value

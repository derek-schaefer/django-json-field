from django.forms import fields, util
from django.utils import simplejson as json

import datetime
import decimal

class JSONFormField(fields.Field):

    def __init__(self, *args, **kwargs):
        self.encoder_kwargs = kwargs.pop('encoder_kwargs')
        self.decoder_kwargs = kwargs.pop('decoder_kwargs')
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # Have to jump through a few hoops to make this reliable
        value = super(JSONFormField, self).clean(value)
        json_globals = {
            '__builtins__': None,
            'datetime': datetime,
            'Decimal': decimal.Decimal,
        }
        value = json.dumps(eval(value, json_globals, {}), **self.encoder_kwargs)
        try:
            json.loads(value, **self.decoder_kwargs)
        except ValueError, e:
            raise util.ValidationError(self.help_text)
        return value

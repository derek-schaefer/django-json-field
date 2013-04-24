from __future__ import unicode_literals
from .models import Test

from json_field.forms import JSONFormField

from django import forms

class ModelForm(forms.ModelForm):
    class Meta:
        model = Test

class TestForm(forms.Form):
    json = JSONFormField()

class OptionalForm(forms.Form):
    json = JSONFormField(required=False)

class EvalForm(forms.Form):
    json = JSONFormField(evaluate=True)

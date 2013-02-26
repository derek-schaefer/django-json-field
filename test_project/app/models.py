from json_field import JSONField

from django.db import models

class Test(models.Model):

    json = JSONField()
    json_eager = JSONField(lazy=False)
    json_null = JSONField(blank=True, null=True, evaluate_formfield=True)

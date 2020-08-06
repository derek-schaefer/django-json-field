Django JSON Field
=================

**NOTE: This project is seeking new active maintainers.**

``django-json-field`` contains a flexible JSONField and associated form field. The model field is not only capable of serializing common JSON data types (int, float, decimal, string, time, date, datetime, etc.) but also lazily deserializing them so they can be accessed and modified as normal Python objects within Django.

A form field is also provided. It will accept serialized representations:

    ``{"date": "2012-04-23T19:16:54.133", "num": "1.2399"}``

And also provides safe access to the ``datetime`` module for explicit use:

    ``{"date": datetime.datetime(2012, 4, 23, 19, 16, 54, 133000)}``

While the JSON string will not be deserialized until it is accessed it can still be a performance concern, so you may find it valuable to disable the custom deserializer (``JSONField(decoder=None)``).

``django-json-field`` is also compatible with South and Python 3.

Installation
------------

Install from PyPI:

    ``pip install django-json-field``

If installing manually, first install the dependencies:

    ``pip install python-dateutil six``

Install from GitHub:

    ``git clone git://github.com/derek-schaefer/django-json-field.git``

    ``pip install -e git+git://github.com/derek-schaefer/django-json-field.git#egg=json_field``

Configuration
-------------

Add ``json_field`` to your ``PYTHONPATH`` and ``INSTALLED_APPS`` setting:

::

    INSTALLED_APPS = (
        ...
        'json_field',
        ...
    )

That's all!

Usage
-----

Add a ``JSONField`` to your model like any other field.

::

    from json_field import JSONField
    from django.db import models
    
    class MyModel(models.Model):
    
        json = JSONField()

``JSONField`` also has a few additional optional parameters.

 - ``default``: Falls back on ``"null"`` if not provided and ``null=False``, otherwise ``None``
 - ``db_type``: Allows you to specify the column type (default: ``text``)
 - ``lazy``: Defer deserialization until the field is directly accessed (default: ``True``)
 - ``encoder``: Custom JSON encoder (default: ``DjangoJSONEncoder``)
 - ``decoder``: Custom JSON decoder (default: ``json_field.fields.JSONDecoder``)
 - ``encoder_kwargs``: Specify all arguments to the encoder (overrides ``encoder``)
 - ``decoder_kwargs``: Specify all arguments to the decoder (overrides ``decoder``)
 - ``evaluate_formfield``: Evaluate (risky) and enable use of the ``datetime`` module in the form field (default: ``False``)

License
-------

``django-json-field`` is licensed under the New BSD license.

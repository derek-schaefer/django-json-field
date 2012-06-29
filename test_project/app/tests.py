from test_project.app.models import Test

from django.test import TestCase
from django.db.utils import IntegrityError

import datetime
from decimal import Decimal

class JSONFieldTest(TestCase):

    def test_simple(self):
        t1 = Test.objects.create(json=123)
        self.assertEqual(123, Test.objects.get(pk=t1.pk).json)
        t2 = Test.objects.create(json='123')
        self.assertEqual(123, Test.objects.get(pk=t2.pk).json)
        t3 = Test.objects.create(json=[123])
        self.assertEqual([123], Test.objects.get(pk=t3.pk).json)
        t4 = Test.objects.create(json='[123]')
        self.assertEqual([123], Test.objects.get(pk=t4.pk).json)
        t5 = Test.objects.create(json={'test':[1,2,3]})
        self.assertEqual({'test':[1,2,3]}, Test.objects.get(pk=t5.pk).json)
        t6 = Test.objects.create(json='{"test":[1,2,3]}')
        self.assertEqual({'test':[1,2,3]}, Test.objects.get(pk=t6.pk).json)

    def test_null(self):
        t1 = Test.objects.create(json=None)
        self.assertEqual(None, t1.json)
        self.assertEqual('null', t1.get_json_json())
        t2 = Test.objects.create(json='')
        self.assertEqual(None, t2.json)
        self.assertEqual('null', t2.get_json_json())
        t3 = Test.objects.create(json_null=None)
        self.assertEqual(None, t3.json_null)
        self.assertEqual('null', t3.get_json_null_json())
        t4 = Test.objects.create(json_null='')
        self.assertEqual(None, t4.json_null)
        self.assertEqual('null', t4.get_json_null_json())

    def test_decimal(self):
        t1 = Test.objects.create(json=Decimal(1.24))
        self.assertEqual(Decimal(1.24), Test.objects.get(pk=t1.pk).json)
        t2 = Test.objects.create(json={'test':[{'test':Decimal(1.24)}]})
        self.assertEqual({'test':[{'test':Decimal(1.24)}]}, Test.objects.get(pk=t2.pk).json)

    def test_time(self):
        now = datetime.datetime.now().time()
        t1 = Test.objects.create(json=now)
        # JSON does not have microsecond precision, round to millisecond
        now_rounded = now.replace(microsecond=(int(now.microsecond) / 1000) * 1000)
        self.assertEqual(now_rounded, Test.objects.get(pk=t1.pk).json)
        t2 = Test.objects.create(json={'time':[now]})
        self.assertEqual({'time':[now_rounded]}, Test.objects.get(pk=t2.pk).json)

    def test_date(self):
        today = datetime.date.today()
        t1 = Test.objects.create(json=today)
        self.assertEqual(today, Test.objects.get(pk=t1.pk).json)
        t2 = Test.objects.create(json={'today':today})
        self.assertEqual({'today':today}, Test.objects.get(pk=t2.pk).json)

    def test_datetime(self):
        now = datetime.datetime.now()
        t1 = Test.objects.create(json=now)
        # JSON does not have microsecond precision, round to millisecond
        now_rounded = now.replace(microsecond=(int(now.microsecond) / 1000) * 1000)
        self.assertEqual(now_rounded, Test.objects.get(pk=t1.pk).json)
        t2 = Test.objects.create(json={'test':[{'test':now}]})
        self.assertEqual({'test':[{'test':now_rounded}]}, Test.objects.get(pk=t2.pk).json)

    def test_get_set_json(self):
        t1 = Test.objects.create(json={'test':123})
        self.assertEqual({'test':123}, t1.json)
        self.assertEqual('{"test": 123}', t1.get_json_json())
        t2 = Test.objects.create()
        self.assertEqual(None, t2.json)
        self.assertEqual('null', t2.get_json_json())
        self.assertEqual(None, t2.json_null)
        self.assertEqual('null', t2.get_json_null_json())
        t3 = Test.objects.create(json=[1,2,3])
        self.assertEqual([1,2,3], t3.json)
        self.assertEqual('[1, 2, 3]', t3.get_json_json())
        t3.set_json_json('[1, 2, 3, 4, 5]')
        self.assertEqual([1, 2, 3, 4, 5], t3.json)
        self.assertEqual('[1, 2, 3, 4, 5]', t3.get_json_json())
        t3.set_json_json(123)
        self.assertEqual(123, t3.json)
        self.assertEqual('123', t3.get_json_json())

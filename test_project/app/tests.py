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
        with self.assertRaises(IntegrityError):
            Test.objects.create(json=None)
        with self.assertRaises(IntegrityError):
            Test.objects.create(json='')
        Test.objects.create(json_null=None)
        Test.objects.create(json_null='')

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

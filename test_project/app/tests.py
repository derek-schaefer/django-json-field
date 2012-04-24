from test_project.app.models import Test

from django.test import TestCase
from django.db.utils import IntegrityError

from decimal import Decimal

class JSONFieldTest(TestCase):

    def test_simple(self):
        t1 = Test.objects.create(json=123)
        self.assertEqual(123, t1.json)
        t2 = Test.objects.create(json='123')
        self.assertEqual(123, t2.json)
        t3 = Test.objects.create(json=[123])
        self.assertEqual([123], t3.json)
        t4 = Test.objects.create(json='[123]')
        self.assertEqual([123], t4.json)
        t5 = Test.objects.create(json={'test':[1,2,3]})
        self.assertEqual({'test':[1,2,3]}, t5.json)
        t6 = Test.objects.create(json='{"test":[1,2,3]}')
        self.assertEqual({'test':[1,2,3]}, t6.json)

    def test_null(self):
        with self.assertRaises(IntegrityError):
            Test.objects.create(json=None)
        with self.assertRaises(IntegrityError):
            Test.objects.create(json='')
        Test.objects.create(json_null=None)
        Test.objects.create(json_null='')

    def test_decimal(self):
        t1 = Test.objects.create(json=Decimal(1.24))
        self.assertEqual(Decimal(1.24), t1.json)
        t2 = Test.objects.create(json={'test':[{'test':Decimal(1.24)}]})
        self.assertEqual({'test':[{'test':Decimal(1.24)}]}, t2.json)

    def test_time(self):
        pass

    def test_date(self):
        pass

    def test_datetime(self):
        pass

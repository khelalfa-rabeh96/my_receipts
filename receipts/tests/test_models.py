from django.test import TestCase
from django.db import  transaction
from decimal import Decimal, DecimalException

from django.core.exceptions import ValidationError
from receipts.models import Receipt

class ReceiptModelTest(TestCase):
    def setUp(self):
        self.first_total_amount = 1000.1
        self.second_total_amount = 2000.2
        self.total_amount_with_exceed_max_digits = 123456789


    def test_saving_and_retrieving_receipts(self):
        Receipt.objects.create(total_amount=self.first_total_amount)
        Receipt.objects.create(total_amount=self.second_total_amount)
        
        saved_receipts = Receipt.objects.all()
        self.assertEqual(saved_receipts.count(), 2)

        self.assertEqual(
            saved_receipts[0].total_amount, 
            Decimal(f'{self.first_total_amount}')
        )
        self.assertEqual(
            saved_receipts[1].total_amount, 
            Decimal(f'{self.second_total_amount}')
        )
    
    def test_total_amount_default_value(self):
        first_receipt = Receipt.objects.create()
        self.assertEqual(first_receipt.total_amount, 0)
    
    # with sqlite max_digits validation will work, decimal_places won't
    def test_total_amount_max_digits(self):
        with transaction.atomic():
            with self.assertRaises(DecimalException): 
                Receipt.objects.create(total_amount = self.total_amount_with_exceed_max_digits)

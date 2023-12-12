from decimal import Decimal, DecimalException
import datetime

from django.test import TestCase
from django.db import  transaction

from django.core.exceptions import ValidationError
from receipts.models import Receipt

class ReceiptModelTest(TestCase):
    def setUp(self):
        self.first_total_amount = 1000.1
        self.second_total_amount = 2000.2
        self.total_amount_with_exceed_max_digits = 123456789
        self.item_list = "item1, item2"

    def test_saving_and_retrieving_receipts(self):
        Receipt.objects.create(total_amount=self.first_total_amount, item_list="item1, item2")
        Receipt.objects.create(total_amount=self.second_total_amount, item_list="item1, item2")
        
        saved_receipts = Receipt.objects.all()
        self.assertEqual(saved_receipts.count(), 2)

        self.assertEqual(
            saved_receipts[0].total_amount, 
            Decimal(f'{self.first_total_amount}')
        )
        self.assertEqual(saved_receipts[0].item_list, self.item_list)
        
        self.assertEqual(
            saved_receipts[1].total_amount, 
            Decimal(f'{self.second_total_amount}')
        )
        self.assertEqual(saved_receipts[1].item_list, self.item_list)
    
    def test_total_amount_default_value(self):
        first_receipt = Receipt.objects.create()
        self.assertEqual(first_receipt.total_amount, 0)
    
    # with sqlite max_digits validation will work, decimal_places won't
    def test_total_amount_max_digits(self):
        with transaction.atomic():
            with self.assertRaises(DecimalException): 
                Receipt.objects.create(total_amount = self.total_amount_with_exceed_max_digits)

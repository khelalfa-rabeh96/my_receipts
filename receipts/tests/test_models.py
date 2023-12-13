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
        self.store_name = 'Walmart'
        self.total_amount_with_exceed_max_digits = 123456789
        self.item_list = "item1, item2"
        self.date_of_purchase =  datetime.date.today() - datetime.timedelta(days=1)

    def test_saving_and_retrieving_receipts(self):
        Receipt.objects.create(
            store_name=self.store_name,
            total_amount=self.first_total_amount, 
            date_of_purchase=self.date_of_purchase,
            item_list="item1, item2"
        )
        Receipt.objects.create(
            store_name=self.store_name,
            total_amount=self.second_total_amount, 
            date_of_purchase=self.date_of_purchase,
            item_list="item1, item2"
        )
        
        saved_receipts = Receipt.objects.all()
        self.assertEqual(saved_receipts.count(), 2)

        self.assertEqual(
            saved_receipts[0].total_amount, 
            Decimal(f'{self.first_total_amount}')
        )
        self.assertEqual(saved_receipts[0].item_list, self.item_list)
        self.assertEqual(saved_receipts[0].store_name, self.store_name)
        self.assertEqual(saved_receipts[0].date_of_purchase, self.date_of_purchase)
        
        self.assertEqual(
            saved_receipts[1].total_amount, 
            Decimal(f'{self.second_total_amount}')
        )
        self.assertEqual(saved_receipts[1].item_list, self.item_list)
        self.assertEqual(saved_receipts[1].store_name, self.store_name)
        self.assertEqual(saved_receipts[1].date_of_purchase, self.date_of_purchase)
    
    def test_total_amount_default_value(self):
        first_receipt = Receipt.objects.create(item_list="item1", store_name="walmart")
        self.assertEqual(first_receipt.total_amount, 0)
    

    def test_date_of_purchase_default_value(self):
        first_receipt = Receipt.objects.create(item_list="item1", store_name="walmart")
        self.assertEqual(first_receipt.date_of_purchase, datetime.date.today())
    
    # with sqlite max_digits validation will work, decimal_places won't
    def test_total_amount_max_digits(self):
        with transaction.atomic():
            with self.assertRaises(DecimalException): 
                Receipt.objects.create(total_amount = self.total_amount_with_exceed_max_digits)

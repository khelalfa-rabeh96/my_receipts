import datetime

from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from receipts.views import receipts_list, NewReceiptView
from receipts.models import Receipt
from receipts.forms import ReceiptModelForm

class ReceiptListTest(TestCase):
    def setUp(self):
        self.url = reverse('receipts:receipt-list')

    def test_root_url_resolves_to_receipts_list_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, receipts_list)
    
    def test_receipt_list_view_uses_receipt_list_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_list.html')

    def test_displays_all_receipt_receipt(self):
        Receipt.objects.create(store_name="walmart", total_amount=1000, item_list="item1, item2")
        Receipt.objects.create(store_name='KFC', total_amount=2000, item_list="item3, item4")

        response = self.client.get(self.url)

        self.assertIn('1000', response.content.decode())
        self.assertIn('item1, item2', response.content.decode())

        self.assertIn('2000', response.content.decode())
        self.assertIn('item3, item4', response.content.decode())


class NewReceiptTest(TestCase):
    def setUp(self):
        self.url = reverse('receipts:new-receipt')
    
    def test_new_receipt_url_resolves_to_new_receipt_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, NewReceiptView.as_view().__name__)
    
    def test_new_receipt_view_uses_new_receipt_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'new_receipt.html')
    
    def test_new_receipt_view_can_save_a_POST_request(self):
        data = {
            'store_name': 'Walmart', 
            'total_amount': 1000 , 
            'date_of_purchase': datetime.date.today(),
            "item_list": "item1, item2",
        }
        self.client.post(self.url, data=data)
        
        self.assertEqual(Receipt.objects.count(), 1)
        receipt = Receipt.objects.first()
        self.assertEqual(receipt.store_name, data['store_name'])
        self.assertEqual(receipt.total_amount, data['total_amount'])
        self.assertEqual(receipt.date_of_purchase, data['date_of_purchase'])
        self.assertEqual(receipt.item_list, data['item_list'])
        
    
    def test_redirects_after_successful_POST_new_receipt_to_receipt_list(self):
        data = data={'store_name': 'Walmart', 'total_amount': 1000, 'item_list': 'item1, item2'}
        response = self.client.post(
            self.url, 
            data
        )
        self.assertRedirects(response, reverse('receipts:receipt-list'))
    
    def test_required_item_list(self):
        data = {'store_name': 'Walmart', 'total_amount': 1000}
        response = self.client.post(self.url, data=data)
        self.assertEqual(Receipt.objects.count(), 0)
    
    def test_required_store_name(self):
        data={'total_amount': 1000, 'item_list': 'item1, item2'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(Receipt.objects.count(), 0)
    
    def test_stay_at_new_receipt_page_after_unsuccessfuly_POST_new_receipt(self):
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertTemplateUsed(response, 'new_receipt.html')

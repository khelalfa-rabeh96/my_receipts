from django.urls import resolve
from django.test import TestCase
from receipts.views import receipts_list
from receipts.models import Receipt

class ReceiptListTest(TestCase):
    def test_root_url_resolves_to_receipts_list_view(self):
        found = resolve('/')
        self.assertEqual(found.func, receipts_list)
    
    def test_receipt_list_view_uses_receipt_list_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'receipt_list.html')

    def test_receipt_list_view_can_save_a_POST_request(self):
        total_amount = 1000
        response = self.client.post('/', data={'new_total_amount': total_amount})
        
        self.assertEqual(Receipt.objects.count(), 1)
        new_receipt = Receipt.objects.first()
        self.assertEqual(new_receipt.total_amount, total_amount)
    
    def test_redirects_after_POST_new_receipt(self):
        response = self.client.post('/', data={'new_total_amount': 1000})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displays_all_receipt_receipt(self):
        Receipt.objects.create(total_amount=1000)
        Receipt.objects.create(total_amount=2000)

        response = self.client.get('/')

        self.assertIn('1000', response.content.decode())
        self.assertIn('2000', response.content.decode())
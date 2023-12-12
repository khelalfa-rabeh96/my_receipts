from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from receipts.views import receipts_list, new_receipt
from receipts.models import Receipt

class ReceiptListTest(TestCase):
    def setUp(self):
        self.url = reverse('receipt-list')

    def test_root_url_resolves_to_receipts_list_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, receipts_list)
    
    def test_receipt_list_view_uses_receipt_list_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_list.html')

    def test_displays_all_receipt_receipt(self):
        Receipt.objects.create(total_amount=1000)
        Receipt.objects.create(total_amount=2000)

        response = self.client.get(self.url)

        self.assertIn('1000', response.content.decode())
        self.assertIn('2000', response.content.decode())


class NewReceiptTest(TestCase):
    def setUp(self):
        self.url = reverse('new-receipt')
    
    def test_new_receipt_url_resolves_to_new_receipt_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, new_receipt)
    
    def test_new_receipt_view_uses_new_receipt_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'new_receipt.html')
    
    def test_receipt_list_view_can_save_a_POST_request(self):
        total_amount = 1000
        self.client.post(self.url, data={'new_total_amount': total_amount})
        
        self.assertEqual(Receipt.objects.count(), 1)
        receipt = Receipt.objects.first()
        self.assertEqual(receipt.total_amount, total_amount)
    
    def test_redirects_after_POST_new_receipt(self):
        response = self.client.post(self.url, data={'new_total_amount': 1000})
        self.assertRedirects(response, reverse('receipt-list'))

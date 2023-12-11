from django.urls import resolve
from django.test import TestCase
from receipts.views import receipts_list


class ReceiptListTest(TestCase):
    def test_root_url_resolves_to_receipts_list_view(self):
        found = resolve('/')
        self.assertEqual(found.func, receipts_list)
    
    def test_receipt_list_view_uses_receipt_list_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'receipt_list.html')

    def test_receipt_list_view_can_save_a_POST_request(self):
        response = self.client.post('/', data={'new_total_amount': 1000})
        self.assertIn('1000', response.content.decode())
        self.assertTemplateUsed(response, 'receipt_list.html')
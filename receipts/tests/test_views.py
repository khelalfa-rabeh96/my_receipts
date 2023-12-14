import datetime

from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from receipts.views import receipts_list, receipt_detail_view, NewReceiptView, ReceiptEditView
from receipts.models import Receipt

MOCK_RECEIPT_DATA =  {
    'store_name': 'Walmart', 
    'total_amount': 1000 , 
    'date_of_purchase': datetime.date.today(),
    "item_list": "item1, item2",
}

MOCK_UPDATED_RECEIPT_DATA = {
    'store_name': 'Walmart', 
    'total_amount': 1000 , 
    'date_of_purchase': datetime.date.today() - datetime.timedelta(days=2),
    "item_list": "updated items",
}

class ReceiptListTest(TestCase):
    def setUp(self):
        self.url = reverse('receipts:receipt-list')

    def test_receipt_list_url_resolves_to_receipts_list_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, receipts_list)
    
    def test_receipt_list_view_uses_receipt_list_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_list.html')

    def test_displays_all_receipts_with_item_list_and_total_amount(self):
        Receipt.objects.create(store_name="walmart", total_amount=1000, item_list="item1, item2")
        Receipt.objects.create(store_name='KFC', total_amount=2000, item_list="item3, item4")

        response = self.client.get(self.url)

        self.assertIn('1000', response.content.decode())
        self.assertIn('item1, item2', response.content.decode())

        self.assertIn('2000', response.content.decode())
        self.assertIn('item3, item4', response.content.decode())
    
    def test_receipt_list_displays_only_first_25_chars_from_item_list_while_the_rest_continued_with_dots(self):
        item_list = "12345678901234567890123456789"
        expected_item_list_displayed = "123456789012345678901234…"
        Receipt.objects.create(store_name='KFC', total_amount=2000, item_list=item_list)
        
        response = self.client.get(self.url)
        self.assertIn(expected_item_list_displayed, response.content.decode())


class NewReceiptTest(TestCase):
    def setUp(self):
        self.url = reverse('receipts:new-receipt')
    
    def test_new_receipt_url_resolves_to_new_receipt_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, NewReceiptView.as_view().__name__)
    
    def test_new_receipt_view_uses_new_receipt_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'new_receipt.html')
    
    def test_new_receipt_view_can_add_new_receipt_with_a_POST_request(self):
        self.client.post(self.url, data=MOCK_RECEIPT_DATA)
        
        self.assertEqual(Receipt.objects.count(), 1)
        receipt = Receipt.objects.first()

        self.assertEqual(receipt.store_name, MOCK_RECEIPT_DATA['store_name'])
        self.assertEqual(receipt.total_amount, MOCK_RECEIPT_DATA['total_amount'])
        self.assertEqual(receipt.date_of_purchase, MOCK_RECEIPT_DATA['date_of_purchase'])
        self.assertEqual(receipt.item_list, MOCK_RECEIPT_DATA['item_list'])
        
    
    def test_redirects_to_receipt_list_after_successfully_POSTING_new_receipt(self):
        response = self.client.post(self.url, MOCK_RECEIPT_DATA)
        self.assertRedirects(response, reverse('receipts:receipt-list'))
    
    def test_can_not_POST_new_receipt_without_item_list(self):
        data = {'store_name': 'Walmart', 'total_amount': 1000}
        self.client.post(self.url, data=data)

        self.assertEqual(Receipt.objects.count(), 0)
    
    def test_can_not_POST_new_receipt_without_store_name(self):
        data={'total_amount': 1000, 'item_list': 'item1, item2'}
        self.client.post(self.url, data=data)

        self.assertEqual(Receipt.objects.count(), 0)
    
    def test_stay_at_new_receipt_page_after_unsuccessfuly_POST_new_receipt_due_to_form_validation(self):
        response = self.client.post(self.url, data={})
        self.assertTemplateUsed(response, 'new_receipt.html')


class ReceiptDetailViewTest(TestCase):
    def setUp(self):
        self.receipt = Receipt.objects.create(**MOCK_RECEIPT_DATA)
        self.url = reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk})
    
    def test_receipt_detail_url_resolves_to_receipts_detail_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, receipt_detail_view)
    
    def test_receipt_detail_view_uses_receipt_detail_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_detail.html')
    
    def test_receipt_view_displays_receipts_details(self):
        response = self.client.get(self.url)
        self.assertIn(self.receipt.store_name, response.content.decode())
        self.assertIn(f'{self.receipt.total_amount}', response.content.decode())
        
        # Date should be displayed as 'Dec. 15, 2023'
        self.assertIn(f'{self.receipt.date_of_purchase.strftime("%b. %d, %Y")}', response.content.decode())
        self.assertIn(self.receipt.item_list, response.content.decode())
    
    def test_trying_to_get_non_existed_receipt_redirects_to_404_page(self):
        after_last_id = Receipt.objects.count() + 1
        response = self.client.get(reverse('receipts:receipt-detail', kwargs={'pk': after_last_id}))
        
        self.assertTemplateUsed(response, '404.html')
    

class ReceiptEditView(TestCase):
    def setUp(self):
        self.receipt = Receipt.objects.create(**MOCK_RECEIPT_DATA)
        self.url = reverse('receipts:receipt-edit', kwargs={'pk': self.receipt.pk})
    
    def test_receipt_edit_view_uses_receipt_edit_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_edit.html')
    
    def test_receipt_edit_view_can_edit_a_receipt_with_a_POST_request(self):
        self.client.post(self.url, data=MOCK_UPDATED_RECEIPT_DATA)
        receipt = Receipt.objects.first()

        self.assertEqual(receipt.store_name, MOCK_UPDATED_RECEIPT_DATA['store_name'])
        self.assertEqual(receipt.total_amount, MOCK_UPDATED_RECEIPT_DATA['total_amount'])
        self.assertEqual(receipt.date_of_purchase, MOCK_UPDATED_RECEIPT_DATA['date_of_purchase'])
        self.assertEqual(receipt.item_list, MOCK_UPDATED_RECEIPT_DATA['item_list'])
    
    def test_redirects_to_receipt_detail_view_after_successfully_editing_a_receipt(self):
        response = self.client.post(self.url, MOCK_RECEIPT_DATA)
        self.assertRedirects(response, reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk}))


class ReceipDeleteView(TestCase):
    def setUp(self):
        self.receipt = Receipt.objects.create(**MOCK_RECEIPT_DATA)
        self.url = reverse('receipts:receipt-delete', kwargs={'pk': self.receipt.pk})

    def test_receipt_delete_view_uses_receipt_delete_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_delete.html')
    
    def test_receipt_delete_view_can_delete_a_receipt_with_a_POST_request(self):
        self.client.post(self.url, {})
        self.assertEqual(Receipt.objects.filter(pk=self.receipt.pk).count(), 0)
    
    def test_receipt_delete_view_redirects_to_receipt_list_view_after_successfuly_delete_a_receipt(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('receipts:receipt-list'))
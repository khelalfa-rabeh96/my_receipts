import datetime

from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from receipts.views import receipts_list, NewReceiptView, receipt_detail_view, ReceiptEditView
from receipts.models import Receipt

class ReceiptDetailViewTest(TestCase):
    def setUp(self):
        self.receipt_data = {
            "store_name": 'KFC', 
            "total_amount": 19.9, 
            "date_of_purchase": datetime.date.today(),
            "item_list": 'Fries chicken, Apple Juice, Hotdogs'
        }
        self.receipt = Receipt.objects.create(**self.receipt_data)
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
    
    def test_get_non_existed_receipt_redirects_to_404_page(self):
        after_last_id = Receipt.objects.count() + 1
        response = self.client.get(reverse('receipts:receipt-detail', kwargs={'pk': after_last_id}))
        self.assertTemplateUsed(response, '404.html')
    

class ReceiptListTest(TestCase):
    def setUp(self):
        self.url = reverse('receipts:receipt-list')

    def test_root_url_resolves_to_receipts_list_view(self):
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
        data = {
            'store_name': 'Walmart', 
            'total_amount': 1000, 
            'item_list': 'item1, item2', 
            "date_of_purchase": datetime.date.today()
        }
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
    
    def test_stay_at_new_receipt_page_after_unsuccessfuly_POST_new_receipt_due_to_form_validation(self):
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertTemplateUsed(response, 'new_receipt.html')


class ReceiptEditView(TestCase):
    def setUp(self):
        self.receipt_data = {
            "store_name": 'KFC', 
            "total_amount": 19.9, 
            "date_of_purchase": datetime.date.today(),
            "item_list": 'Fries chicken, Apple Juice, Hotdogs'
        }
        self.receipt = Receipt.objects.create(**self.receipt_data)
        self.url = reverse('receipts:receipt-edit', kwargs={'pk': self.receipt.pk})
    
    def test_receipt_edit_view_uses_receipt_edit_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'receipt_edit.html')
    
    def test_receipt_edit_view_can_edit_a_receipt(self):
        updated_data = {
            'store_name': 'Walmart', 
            'total_amount': 1000 , 
            'date_of_purchase': datetime.date.today() - datetime.timedelta(days=2),
            "item_list": "updated items",
        }
        self.client.post(self.url, data=updated_data)
        
        receipt = Receipt.objects.first()
        self.assertEqual(receipt.store_name, updated_data['store_name'])
        self.assertEqual(receipt.total_amount, updated_data['total_amount'])
        self.assertEqual(receipt.date_of_purchase, updated_data['date_of_purchase'])
        self.assertEqual(receipt.item_list, updated_data['item_list'])
    
    def test_redirects_after_successful_POST_new_receipt_to_receipt_list(self):
        response = self.client.post(self.url, self.receipt_data)
        self.assertRedirects(response, reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk}))
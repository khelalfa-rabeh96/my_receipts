from django.urls import resolve
from django.test import TestCase
from receipts.views import receipts_list


class ReceiptListTest(TestCase):
    def test_root_url_resolves_to_receipts_list_view(self):
        found = resolve('/')
        self.assertEqual(found.func, receipts_list)
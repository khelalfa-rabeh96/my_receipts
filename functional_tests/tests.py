import time
import datetime

from decimal import Decimal
from django.test import TestCase
from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import environ

from receipts.models import Receipt

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

MAX_WAIT = 10

class BaseTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=env('GECKODRIVER_PATH'))
        self.driver = webdriver.Firefox(service=service)


class ReceiptListTest(BaseTest):
    def setUp(self):
        super(ReceiptListTest, self).setUp()
        self.receipt = Receipt.objects.create(store_name="KFC", item_list="item1")
        self.url = reverse('receipts:receipt-list')
    
    def tearDown(self):
        self.driver.close()

    def test_navigating_to_home_redirects_you_to_receipts_list_page(self):
        self.driver.get(self.live_server_url)
        time.sleep(1)
        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-list')
        )
    
    def test_receipt_list_item_redirects_to_receipt_detail_when_click_on_it(self):
        self.driver.get(self.live_server_url + self.url)
        my_receipt_list = self.driver.find_element(By.ID,'my_receipt_list')
        receipts = my_receipt_list.find_elements(By.CSS_SELECTOR,'li a')
        
        first_receipt = receipts[0]
        first_receipt.click()
        
        time.sleep(1)

        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk})
        )
    
    def test_navigate_from_receipt_list_page_to_new_receipt_page_when_clicking_ona_add_button(self):
        self.driver.get(self.live_server_url + self.url)
        add_btn = self.driver.find_element(By.ID,'add-receipt')
        
        add_btn.click()
        
        time.sleep(1)

        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:new-receipt')
        )
    

class NewReceiptTest(BaseTest):
    def setUp(self):
        super(NewReceiptTest, self).setUp()
        self.store_name = "Walmart"
        self.total_amount = 2566.2
        self.date_of_purchase = datetime.date.today()
        self.item_list = "Apple, Banana, Orange"
        self.url = reverse('receipts:new-receipt')
    
    def tearDown(self):
        self.driver.close()

    def get_number_with_two_decimal_places(self, number):
        return format(Decimal(number), '.2f')

    def wait_and_check_for_new_receipt_in_receipt_list(self):
        start_time = time.time()
        while True:
            try:
                my_receipt_list = self.driver.find_element(By.ID,'my_receipt_list')
                receipts = my_receipt_list.find_elements(By.TAG_NAME,'li')
                self.assertIn(
                    self.get_number_with_two_decimal_places(self.total_amount), 
                    [row.text for row in receipts][-1]
                )

                self.assertIn(
                    self.item_list[0:10], 
                    [row.text for row in receipts][-1]
                )
                
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def check_for_successful_message_after_creating_new_receipt(self):
        flash_messages = self.driver.find_element(By.ID,'flash_messages')
        self.assertIn("An new receipt was created successfully", flash_messages.text)

    def test_can_create_new_receipt_and_see_it_in_receipt_list(self):
        self.driver.get(self.live_server_url + self.url)
        self.assertIn('New Receipt', self.driver.title)
        
        # The Authed user finds a header text as 'New Receipt'
        header_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('New Receipt', header_text)

        # The Authed user invited to add a new receipt by filling a form
        store_name_input = self.driver.find_element(By.ID,'store_name')
        total_amount_input = self.driver.find_element(By.ID,'total_amount')
        date_of_purchase_input = self.driver.find_element(By.ID,'date_of_purchase')
        item_list_input = self.driver.find_element(By.ID,'item_list')


        # # The Authed user start to fill the form fields
        store_name_input.send_keys(self.store_name)
        total_amount_input.send_keys(self.total_amount)
        
        #date_of_purchase_input.click()
        date_of_purchase = self.date_of_purchase.strftime('%Y-%m-%d')
        self.driver.execute_script(
            f"arguments[0].setAttribute('value', '{date_of_purchase}')", 
            date_of_purchase_input
        )
        item_list_input.send_keys(self.item_list)
        
        # The The Authed hits enter
        submit_btn = self.driver.find_element(By.ID,'submit_btn')
        submit_btn.click()

        #self.wait_for_total_amount_in_receipt_list(self.total_amount)

        time.sleep(1)

        # make sure the user get redirect to receipt list page after submitting new receipt
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('receipts:receipt-list'))
        self.wait_and_check_for_new_receipt_in_receipt_list() 

        self.check_for_successful_message_after_creating_new_receipt()   


class ReceiptDetailTest(BaseTest):
    def setUp(self):
        super(ReceiptDetailTest, self).setUp()
        self.receipt = Receipt.objects.create(store_name="KFC", item_list="item1")
        self.url = reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk})
    
    def tearDown(self):
        self.driver.close()

    def test_can_navigate_from_receipt_detail_page_to_receipt_edit_page(self):
        self.driver.get(self.live_server_url + self.url)
        receipt_edit_btn = self.driver.find_element(By.ID,'receipt-edit')        
        receipt_edit_btn.click()
        
        time.sleep(1)

        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-edit', kwargs={'pk': self.receipt.pk})
        )
    
    def test_can_navigate_from_receipt_detail_page_to_receipt_delete_page(self):
        self.driver.get(self.live_server_url + self.url)
        receipt_edit_btn = self.driver.find_element(By.ID,'receipt-delete')        
        receipt_edit_btn.click()
        
        time.sleep(1)

        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-delete', kwargs={'pk': self.receipt.pk})
        )

class ReceiptDeleteTest(BaseTest):
    def setUp(self):
        super(ReceiptDeleteTest, self).setUp()
        self.receipt = Receipt.objects.create(store_name="KFC", item_list="item1")
        self.url = reverse('receipts:receipt-delete', kwargs={'pk': self.receipt.pk})

    def tearDown(self):
        self.driver.close()

    def test_get_back_from_receipt_delete_view_to_receipt_detail_view_via_cancel_btn(self):
        self.driver.get(self.live_server_url + self.url)
        cancel_delete = self.driver.find_element(By.ID,'cancel-delete')
        
        cancel_delete.click()
        time.sleep(1)
        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk})
        )
    

class ReceiptEditTest(BaseTest):
    def setUp(self):
        super(ReceiptEditTest, self).setUp()
        self.receipt = Receipt.objects.create(store_name="KFC", item_list="item1")
        self.url = reverse('receipts:receipt-edit', kwargs={'pk': self.receipt.pk})
    
    def tearDown(self):
        self.driver.close()

    def test_receipt_form_edit_fields_are_bounded_with_receipt_properties(self):
        self.driver.get(self.live_server_url + self.url)
        store_name_input = self.driver.find_element(By.ID,'store_name')
        total_amount_input = self.driver.find_element(By.ID,'total_amount')
        date_of_purchase_input = self.driver.find_element(By.ID,'date_of_purchase')
        item_list_input = self.driver.find_element(By.ID,'item_list')

        self.assertEqual(store_name_input.get_attribute('value'), self.receipt.store_name)
        self.assertEqual(float(total_amount_input.get_attribute('value')), float(self.receipt.total_amount))
        self.assertEqual(date_of_purchase_input.get_attribute('value'), self.receipt.date_of_purchase.strftime('%Y-%m-%d'))
        self.assertEqual(item_list_input.get_attribute('value'), self.receipt.item_list)
    
    def test_get_back_from_receipt_edit_view_to_receipt_detail_view_via_cancel_btn(self):
        self.driver.get(self.live_server_url + self.url)
        cancel_edit = self.driver.find_element(By.ID,'cancel-edit')
        
        cancel_edit.click()
        time.sleep(1)
        self.assertEqual(
            self.driver.current_url, 
            self.live_server_url + reverse('receipts:receipt-detail', kwargs={'pk': self.receipt.pk})
        )

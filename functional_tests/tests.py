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

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

MAX_WAIT = 10


class NewListTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=env('GECKODRIVER_PATH'))
        self.driver = webdriver.Firefox(service=service)
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
            f"arguments[0].setAttribute('value', {date_of_purchase})", 
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


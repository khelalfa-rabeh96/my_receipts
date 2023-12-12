import time

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


class NewReceiptTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=env('GECKODRIVER_PATH'))
        self.driver = webdriver.Firefox(service=service)
        self.total_amount = 2566.23
        self.url = reverse('new-receipt')

    def tearDown(self):
        self.driver.close()
    
    def get_number_with_two_decimal_places(self, number):
        return format(Decimal(number), '.2f')

    def wait_for_total_amount_in_receipt_list(self, total_amount):
        start_time = time.time()
        while True:
            try:
                my_receipt_list = self.driver.find_element(By.ID,'my_receipt_list')
                receipts = my_receipt_list.find_elements(By.TAG_NAME,'li')
                self.assertIn(
                    self.get_number_with_two_decimal_places(total_amount), 
                    [row.text for row in receipts]
                )
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_create_new_receipt_and_see_it_in_receipt_list(self):
        self.driver.get(self.live_server_url + self.url)
        self.assertIn('New Receipt', self.driver.title)
        
        # The Authed user finds a header text as 'New Receipt'
        header_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('New Receipt', header_text)

        # The Authed user invited to add a My receiptss to his list by filling the form
        # The Authed user find field to enter the total amount
        total_amount_input = self.driver.find_element(By.ID,'new_total_amount')
        
        # The The Authed user types a number into the total amount field
        total_amount_input.send_keys(self.total_amount)

        # The The Authed hits enter
        total_amount_input.send_keys(Keys.ENTER)
        self.wait_for_total_amount_in_receipt_list(self.total_amount)

        time.sleep(1)

        # make sure the user get redirect to receipt list page after submitting new receipt
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('receipt-list'))
        self.wait_for_total_amount_in_receipt_list(self.total_amount)
        
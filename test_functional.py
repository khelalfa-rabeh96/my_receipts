import time

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class NewVisitorTest(TestCase):
    def setUp(self):
        service = Service(executable_path=env('GECKODRIVER_PATH'))
        self.driver = webdriver.Firefox(service=service)
        self.total_amount = 2566

    def tearDown(self):
        self.driver.close()

    def check_for_total_amount_in_receipt_list(self, total_amount):
        my_receipt_list = self.driver.find_element(By.ID,'my_receipt_list')
        receipts = my_receipt_list.find_elements(By.TAG_NAME,'li')
        self.assertIn(f'{total_amount}', [row.text for row in receipts])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.driver.get('http://localhost:8000')
        self.assertIn('My Receipts', self.driver.title)
    
    
        # The Authed user finds a header text as 'My Receipts'
        header_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('My Receipts', header_text)

        # The Authed user invited to add a new receipts to his list by filling the form
        # The Authed user find field to enter the total amount
        total_amount_input = self.driver.find_element(By.ID,'new_total_amount')
        
        # The The Authed user types a number into the total amount field
        total_amount_input.send_keys(self.total_amount)

        # The The Authed hits enter
        total_amount_input.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_total_amount_in_receipt_list(self.total_amount)

        # The The Authed user adds another total amount field
        total_amount_input = self.driver.find_element(By.ID,'new_total_amount')
        total_amount_input.send_keys(self.total_amount + 10)
        total_amount_input.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_total_amount_in_receipt_list(self.total_amount)
        self.check_for_total_amount_in_receipt_list(self.total_amount + 10)




import environ

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class NewVisitorTest(TestCase):
    def setUp(self):
        service = Service(executable_path=env('GECKODRIVER_PATH'))
        self.driver = webdriver.Firefox(service=service)

    def tearDown(self):
        self.driver.close()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.driver.get('http://localhost:8000')
        self.assertIn('The install worked successfully! Congratulations!', self.driver.title)

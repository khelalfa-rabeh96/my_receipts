from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="/home/rabah/Downloads/softwares/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get('http://localhost:8000')
assert 'Django' in driver.title

driver.close()
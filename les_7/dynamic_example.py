from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

options = Options
options.add_argument("start-maximazed")

service = Service('chromedriver')
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.implicitly_wait(15)
driver.get('https://5ka.ru/special_offers')

button_lacation = driver.find_element(By.XPATH, "//button[contains(@class, 'location-confirm__tton')]")
button_lacation.click()
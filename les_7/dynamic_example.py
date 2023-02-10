from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options
options.add_argument("start-maximazed")

service = Service('chromedriver')
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.implicitly_wait(15)
driver.get('https://5ka.ru/special_offers')

button_location = driver.find_element(By.XPATH, "//button[@class='btn-main focus-btn location-confirm__button red']")
button_location.click()

button_cookie = driver.find_element(By.XPATH, "//button[@class='btn-main focus-btn red small']")
button_cookie.click()

page = 1

while True and page < 100:
    wait = WebDriverWait(driver, 15)
    page += 1
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='add-more-btn']")))
        #button = driver.find_element(By.XPATH, "//button[@class='add-more-btn']")
        button.click()
    except TimeoutException:
        print("Кнопку найти не удалось")
        break

goods = driver.find_element(By.XPATH, "//div[@class='product-card item']")
for good in goods:
    good_name = good.find_element(By.XPATH, ".//div[@class='item-name']").text

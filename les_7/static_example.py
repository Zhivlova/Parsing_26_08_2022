from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

service = Service('chromedriver')
driver = webdriver.Chrome(service=service)

driver.get('https://gb.ru/login')

element = driver.find_element(By.ID, "user_email")
element.send_keys("zhivchik13@yandex.ru")
element = driver.find_element(By.ID, "user_password")
element.send_keys("test1234")
element.send_keys(Keys.ENTER)

element = driver.find_element(By.XPATH, "//div[@class='mn-dropdown mn-dropdown__profile mn-dropdown_position-right']//a")
profile_link = element.get_attribute('href')
driver.get(profile_link)

element = driver.find_element(By.XPATH, "//a[@class='text-sm btn-primary relative inline-block wrap']")
edit_profile_link = element.get_attribute('href')
driver.get(edit_profile_link)

element_timezone = driver.find_element(By.NAME, "user[time-zone")
select = Select(element_timezone)
select.select_by_value("Saratov")
element_timezone.submit()
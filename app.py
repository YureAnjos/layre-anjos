from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import dotenv
import os
from time import sleep

paths = {
  'email_input': '//*[@id="email-input"]',
  'password_input': '//*[@id="password-input"]',
  'login_button': '//*[@id="login-button"]'
}

dotenv.load_dotenv()

service = Service(GeckoDriverManager().install())
browser = webdriver.Firefox(service=service)

browser.get('https://app.smartpos.net.br')

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, paths['email_input'])))
browser.find_element(By.XPATH, paths['email_input']).send_keys(os.getenv('EMAIL'))
browser.find_element(By.XPATH, paths['password_input']).send_keys(os.getenv('PASSWORD'))

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, paths['login_button'])))
browser.find_element(By.XPATH, paths['login_button']).click()

sleep(5)

browser.get('https://app.smartpos.net.br/dashboard/cadastros/produtos?textFilter=1264')

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="edit-product-1264-dropdown"]')))
dropdown_button = browser.find_element(By.XPATH, '//*[@id="edit-product-1264-dropdown"]')
edit_button = browser.find_element(By.XPATH, '//*[@id="edit-product-1264-button"]')
edit_button_parent = edit_button.find_element(By.XPATH, '..')

browser.execute_script("arguments[0].scrollIntoView(true)", dropdown_button)
browser.execute_script("arguments[0].style.display = 'block';", edit_button_parent)

WebDriverWait(browser, 10).until(
    lambda driver: driver.execute_script(
        "return document.documentElement.scrollTop + window.innerHeight >= arguments[0].getBoundingClientRect().top + window.pageYOffset",
        dropdown_button
    )
)

WebDriverWait(browser, 10).until(
  EC.element_to_be_clickable((By.XPATH, '//*[@id="edit-product-1264-button"]'))
)

edit_button.click()

# //*[@id="email-input"]
# //*[@id="password-input"]
# //*[@id="login-button"]
# //*[@id="search-input"]

# //*[@id="edit-product-1264-button"]
# https://app.smartpos.net.br/dashboard/cadastros/produtos?textFilter=1264
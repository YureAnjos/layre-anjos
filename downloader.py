from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from time import time
import dotenv
import os

paths = {
  'email_input': '//*[@id="email-input"]',
  'password_input': '//*[@id="password-input"]',
  'login_button': '//*[@id="login-button"]',
  'download_button': '/html/body/div[1]/div[2]/main/div[3]/div/div[5]/button[1]'
}

dest_dir = os.path.join(os.getcwd(), 'Files', 'Products')

dotenv.load_dotenv()

options = webdriver.FirefoxOptions()
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', dest_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Tipos MIME para planilhas

service = Service(GeckoDriverManager().install())
browser = webdriver.Firefox(service=service, options=options)

browser.get('https://app.smartpos.net.br')

WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, paths['email_input'])))
browser.find_element(By.XPATH, paths['email_input']).send_keys(os.getenv('EMAIL'))
browser.find_element(By.XPATH, paths['password_input']).send_keys(os.getenv('PASSWORD'))

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, paths['login_button'])))
browser.find_element(By.XPATH, paths['login_button']).click()

browser.get('https://app.smartpos.net.br/dashboard/cadastros/produtos')
# WebDriverWait(browser, 10).until(EC.url_contains('dashboard/cadastros/produtos'))
sleep(5)

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, paths['download_button'])))
browser.find_element(By.XPATH, paths['download_button']).click()
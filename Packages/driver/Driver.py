import os
import time
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
# import settings.urls as urls
# import settings.paths as paths
# import settings.constants as constants
from .settings import urls
from .settings import paths
from .settings import constants
from .utils.BackupManager import BackupManager

class Driver:
  def __init__(self):
    load_dotenv()

    self._downloadDir = Path.cwd() / 'files' / 'products'
    self._downloadDir.mkdir(parents=True, exist_ok=True)

    options = webdriver.FirefoxOptions()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', str(self._downloadDir))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Tipos MIME para planilhas

    service = Service(GeckoDriverManager().install())
    self.browser = webdriver.Firefox(service=service, options=options)
    self.wait = WebDriverWait(self.browser, constants.elementWaitThreshold)
    self.backupManager = BackupManager(Path.cwd() / 'files' / 'backups')

  def _findElement(self, xpath):
    return self.browser.find_element(By.XPATH, xpath)

  def _waitForElement(self, xpath):
    self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

  def _waitForClickable(self, xpath):
    self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

  def _scrollToElement(self, xpath):
    element = self._findElement(xpath)
    self.browser.execute_script('arguments[0].scrollIntoView(true);', element)
    self.wait.until(
      lambda driver: self.browser.execute_script(
        "return document.documentElement.scrollTop + window.innerHeight >= arguments[0].getBoundingClientRect().top + window.pageYOffset",
        element
      )
    )

  def _login(self):
    self.browser.get(urls.mainPageUrl)

    self._waitForElement(paths.emailInput)
    self._findElement(paths.emailInput).send_keys(os.getenv('EMAIL'))
    self._findElement(paths.passwordInput).send_keys(os.getenv('PASSWORD'))

    self._waitForClickable(paths.loginButton)
    self._findElement(paths.loginButton).click()
    self.wait.until(EC.url_contains('dashboard'))

  def _clearProductsDirectory(self):
    try:
      for filePath in self._downloadDir.glob('*'):
        filePath.unlink()
    except OSError as e:
      print(f"Error clearing download directory: {e}")

  def downloadLatestProducts(self):
    fileName = None

    try:
      self._clearProductsDirectory()
      self._login()

      self.browser.get(urls.productsPageUrl)

      self._waitForElement(paths.downloadButton)
      self._scrollToElement(paths.downloadButton) # ensure that the element is appearing
      self._findElement(paths.downloadButton).click()

      startTime = time.time()
      while time.time() - startTime < constants.productsDownloadThreshold:
        files = list(self._downloadDir.glob('*.xlsx'))
        for file in files:
          if not file.name.endswith('.part'):
            fileName = file.name
            break
        if fileName:
          break
        time.sleep(1)

      if fileName:
        self.backupManager.saveBackup(self._downloadDir, fileName)

    except Exception as e:
            print(f"Error downloading products: {e}")

    finally:
      self.browser.quit()

    return str(self._downloadDir / fileName)

# driver = Driver()
# name = driver.downloadLatestProducts()
# print('observa: ', name)
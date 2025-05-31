from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import dotenv, os
import settings.urls as urls
import settings.paths as paths
import settings.constants as constants
import time

class Driver:
  def __init__(self):
    dotenv.load_dotenv()

    self._destDir = os.path.join(os.getcwd(), 'files', 'products')

    if not os.path.exists(self._destDir):
      os.makedirs(self._destDir)

    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', self._destDir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Tipos MIME para planilhas

    self.browser = webdriver.Firefox(service=service, options=options)

  def _getElement(self, path):
    return self.browser.find_element(By.XPATH, path)
  
  def _getElementAndSendKeys(self, path, keys):
    self._getElement(path).send_keys(keys)

  def _getElementAndClick(self, path):
    self._getElement(path).click()

  def _awaitPresence(self, path):
    WebDriverWait(self.browser, constants.elementWaitThreshold).until(EC.presence_of_element_located((By.XPATH, path)))

  def _awaitClickable(self, path):
    WebDriverWait(self.browser, constants.elementWaitThreshold).until(EC.element_to_be_clickable((By.XPATH, path)))

  def _login(self):
    self.browser.get(urls.mainPageUrl)

    self._awaitPresence(paths.emailInput)
    self._getElementAndSendKeys(paths.emailInput, os.getenv('EMAIL'))
    self._getElementAndSendKeys(paths.passwordInput, os.getenv('PASSWORD'))

    self._awaitClickable(paths.loginButton)
    self._getElementAndClick(paths.loginButton)
    WebDriverWait(self.browser, 10).until(EC.url_contains('dashboard'))

  def _clearProductsDirectory(self):
    try:
      for fileName in os.listdir(self._destDir):
        filePath = os.path.join(self._destDir, fileName)
        os.remove(filePath)
    except Exception as ex:
      print(ex)

  def getLatestProducts(self):
    fileName = None

    try:
      self._clearProductsDirectory()
      self._login()

      self.browser.get(urls.productsPageUrl)

      self._awaitClickable(paths.downloadButton)
      self._getElementAndClick(paths.downloadButton)

      startTime = time.time()
      while (time.time() - startTime) < constants.productsDownloadThreshold:
        files = os.listdir(self._destDir)
        if len(files) > 0:
          file = files[0]

          if file.endswith('.xlsx') and not file.endswith('.part'):
            fileName = file
            break

        time.sleep(1)
    except Exception as ex:
      print(ex)

    return fileName

driver = Driver()
name = driver.getLatestProducts()
print(name)
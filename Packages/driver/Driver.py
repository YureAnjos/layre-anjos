import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from .settings import urls
from .settings import paths
from .settings import constants
from .utils.BackupManager import BackupManager

class Driver:
    def __init__(self):
        load_dotenv()

        self._downloadDir = Path.cwd() / 'files' / 'products'
        self._downloadDir.mkdir(parents=True, exist_ok=True)

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        # Configure Chrome to download files to the specified directory without prompting
        options.add_experimental_option("prefs", {
            "download.default_directory": str(self._downloadDir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.minimize_window()
        self.wait = WebDriverWait(self.browser, constants.elementWaitThreshold)
        self.backupManager = BackupManager(Path.cwd() / 'files' / 'backups')

        self._login()

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
            # self._login()

            self.browser.get(urls.productsPageUrl)

            self._waitForElement(paths.downloadButton)
            self._scrollToElement(paths.downloadButton)  # Ensure that the element is visible
            self._findElement(paths.downloadButton).click()

            startTime = time.time()
            while time.time() - startTime < constants.productsDownloadThreshold:
                files = list(self._downloadDir.glob('*.xlsx'))
                for file in files:
                    if not file.name.endswith('.crdownload'):  # Chrome uses .crdownload for incomplete downloads
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
    
    def getLatestProducts(self):
        products = self.backupManager.getLatestFile()
        return products
    
    def uploadProducts(self, path):
        try:
            # self._login()

            self.browser.get(urls.uploadPageUrl)
            self.browser.maximize_window()

            self._waitForElement(paths.uploadInput)
            self._findElement(paths.uploadInput).send_keys(path)

            self._waitForElement(paths.captchaIframe)
            self._scrollToElement(paths.captchaIframe)
            recaptcha_iframe = self._findElement(paths.captchaIframe)
            self.browser.switch_to.frame(recaptcha_iframe)

            self._waitForElement(paths.captchaAnchor)
            self._waitForClickable(paths.captchaAnchor)
            self._findElement(paths.captchaAnchor).click()

            WebDriverWait(self.browser, 60).until(
                lambda driver: self._findElement(paths.captchaAnchor).get_attribute('aria-checked') == 'true'
            )

            self.browser.switch_to.default_content()

            self._findElement(paths.uploadButton).click()

            while True:
                try:
                    self.browser.current_url
                    time.sleep(1)
                except Exception as e:
                    break

        except Exception as e:
            print(e)

        finally:
            try:
                self.browser.quit()
            except Exception:
                pass
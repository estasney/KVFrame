from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

from selenium.webdriver.common.by import By


"""
Custom Exceptions
"""


class ElementNotFound(Exception):

    def __init__(self, message, url):

        super().__init__(message)

        self.url = url



"""
Custom Selenium Waits
"""


class NomadDriver(object):

    def __init__(self, service_path):
        self.service_path = service_path
        self.driver = self.start_driver()
        self.wait = WebDriverWait(self.driver, 20)

    @property
    def driver_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_extension("scraper/selector_gadget.crx")
        return chrome_options

    @property
    def page_source(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def find_element(self, by, value):
        elements = self.driver.find_element(by, value)
        return elements

    def find_elements(self, by, value):
        elements = self.driver.find_elements(by, value)
        return elements


    def start_driver(self):
        driver = webdriver.Chrome(executable_path=self.service_path, chrome_options=self.driver_options)
        return driver

    def maximize_window(self):
        if self.driver:
            self.driver.maximize_window()

    def shutdown(self):
        if self.driver:
            try:
                self.driver.close()
                self.driver.quit()
            except WebDriverException:
                pass
        self.driver.find_element()


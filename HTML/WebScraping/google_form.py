import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

class GoogleForm:

    def __init__(self):
        """
        Constructor to initialize URL and selenium driver.
        Attributes:
        - url (str): The URL of the Google Form to fill.
        - driver (webdriver): The Selenium WebDriver instance.
        """

        self.url = os.getenv("GOOGLE_FORM")
        self.driver = self.create_selenium_driver()

    def create_selenium_driver(self):
        """
        Create and return a Selenium WebDriver instance with specified options.
        :return: Selenium WebDriver instance.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        # user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_form(self):
        """
        Navigate to the Google Form URL using the Selenium WebDriver.
        :return: None
        """
        self.driver.get(self.url)
        time.sleep(2)
        print(f"Current URL: {self.driver.current_url}")

    def fill_address(self, address):
        """
        Fill in the address field in the Google Form.
        :param address:
        """
        address_input = self.driver.find_element(By.XPATH,
                                                 '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.clear()
        address_input.send_keys(address, Keys.ENTER)

    def fill_href(self, href):
        """
        Fill in the href field in the Google Form.
        :param href:
        """
        address_input = self.driver.find_element(By.XPATH,
                                                 '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.clear()
        address_input.send_keys(href, Keys.ENTER)

    def fill_price(self, price):
        """
        Fill in the price field in the Google Form.
        :param price:
        """
        address_input = self.driver.find_element(By.XPATH,
                                                 '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.clear()
        address_input.send_keys(price, Keys.ENTER)

    def submit_form(self):
        """
        Submit the Google Form.
        """
        submit_button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_button.click()

    def submit_another(self):
        """
        Click the "Submit another response" link after submitting the form.
        """
        submit_icon = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        submit_icon.click()
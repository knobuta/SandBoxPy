import os

import requests
from bs4 import BeautifulSoup

class ZillowClone:

    def __init__(self):
        """
        Constructor to initialize URL and soup object.

        Attributes:
        - url (str): The URL of the Zillow clone website to scrape.
        - soup (BeautifulSoup): The BeautifulSoup object for parsing HTML content.
        """
        self.url = os.getenv("ZILLOW_CLONE")
        self.soup = self.create_soup()

    def create_soup(self):
        """
        Create soup object from the URL.

        :return: BeautifulSoup object if the request is successful, None otherwise.
        """

        # Min header
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7"
        }
        print(self.url)
        request = requests.get(self.url, headers=headers)
        if request.status_code == 200:
            return BeautifulSoup(request.content, "html.parser")
        else:
            print("Error code:", request.status_code)
            return None

    def get_rent_info(self):
        """
        Scrape rent information from the soup object.

        :return: List of lists containing rent information [href, address, price].
        2D list format: [[href, address, price], [...], ... ]
        """
        infos_list = [] # create list of info list. 2D list

        all_rents = self.soup.select('#grid-search-results > ul > li')
        num_rents = len(all_rents)
        print("Number of rents:", num_rents)

        # Information to list of list.
        # NOTE: Skipping to remove pipe from the address
        # NOTE: Skipping to format the price.
        for rent in all_rents:
            href = rent.find('a')['href']
            address = rent.find('address').text.strip() # Remove white spaces from the front/back.
            price = rent.find('span').text
            info = [href, address, price]
            infos_list.append(info)
        return infos_list

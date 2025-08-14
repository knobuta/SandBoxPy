import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DataManager:
    def __init__(self):
        """
        Constructor for initializing a new object to manage/manipulate flight data

        Paramters:
        - _user: Username to access Sheety
        - _password: Password to access Sheety
        - _endpoint: Endpoint for API call to Sheety
        - _authorization: Authentication parameter to access Sheety
        - sheet_info: dict to accumulate flight information
        """

        self._user = os.environ.get("SHEETY_USER")
        self._password = os.environ.get("SHEETY_PASSWD")
        self._endpoint = os.environ.get("SHEETY_ENDPOINT")
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.sheet_info = {}

    def get_sheet_info(self):
        """
        Use the Sheety API to GET all the data in the sheet and return it in dict format.

        :return: List of rows in dict format: {col1: val1, col2: val2,...}
        """
        response = requests.get(url=self._endpoint, auth=self._authorization)
        data = response.json()
        self.sheet_info = data["prices"]  # keep all data in prices sheet as dict
        return self.sheet_info

    def put_sheet_info(self):
        for city in self.sheet_info:
            sheety_body = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self._endpoint}/{city['id']}",
                auth=self._authorization,
                json=sheety_body
            )
            print(f"Response to put request to Sheety is {response.text}")
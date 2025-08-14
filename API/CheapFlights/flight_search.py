import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        """
        Constructor for initializing a new object to access to Amadeus API to get airport code

        Paramters:
        - _api_key: Key to access Amadeus API
        - _api_secret: Secret Key to access Amadeus API
        - _token_endpoint: Endpoint to get token to access Amadeus API
        - _token: Token to access Amadeus API. Only key and secret key do not work.
        - _city_endpoint: Endpoint to get the iata code(s) of given city name.
        - params: dict to accumulate flight information
        """
        self._api_key = os.environ.get("AMAD_API_KEY")
        self._api_secret = os.environ.get("AMAD_API_SECRET")
        self._token_endpoint = os.environ.get("AMAD_TOKEN_ENDPOINT")
        self._token = self._get_new_token()
        self._city_endpoint = os.environ.get("AMAD_CITY_ENDPOINT")
        # self.params = {}
        # self.search_info = {}

    def _get_new_token(self):
        """
        Generates the authentication token used for accessing the Amadeus API and returns it.

        :return: The new access token obtained from the API response as str.
        """

        # Header with content type as per Amadeus documentation
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # POST request to the Amadeus token endpoint with API key and API secret
        # to obtain a new client credentials token.
        params = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=self._token_endpoint, headers=headers, data=params)

        # New bearer token. Typically expires in 1799 seconds (30min)
        #print(f"Your token is {response.json()['access_token']}")
        #print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        """
        GET the IATA code for a specified city using the Amadeus Location API.

        :param: city_name as string
        :return: iata code if found.  "N/A" or "Not Found" otherwise
        """

        headers = {"Authorization": f"Bearer {self._token}"} # Use generated token above

        # GET iata code from CITY_ENDPOINT.
        # 1 city can have multiple airports.
        params = {
            'keyword': city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=self._city_endpoint, headers=headers, params=params)

        # Error handling
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()['data'][0]['iataCode'] # Use the first one
        except IndexError:
            print(f"IndexError: Data array is empty for {city_name}.")
            return "N/A"
        except TypeError:
            print(f"KeyError: 'iataCode' key is missing {city_name}.")
            return "Not Found"

        return code
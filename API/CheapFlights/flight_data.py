import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch

# Load environment variables from .env file
load_dotenv()
offer_endpoint = os.environ.get("AMAD_OFFER_ENDPOINT")

class FlightData(FlightSearch):

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, adults, currency, nonstop):
        """
        Constructor for initializing a new flight data instance with specific travel details.

        Note: Inheriting FlightSearch class from flight_search

        :param price: The cost of the flight.
        :param origin_airport: The IATA code for the flight's origin airport.
        :param destination_airport: The IATA code for the flight's destination airport.
        :param out_date: The departure date for the flight.
        :param return_date: The return date for the flight.
        :param adults: Number of adults to travel.
        :param currency: Currency to use.
        :param nonstop: true or false
        """

        super().__init__()
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.adults = adults
        self.currency = currency
        self.nonstop = nonstop

    def find_cheaper_flights(self):
        """
        Parses flight data received from the Amadeus API to identify the flights
        with the price cheaper than the specified price.

        :return: All the flights with cheaper price.
        """
        cheaper_flights = []

        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "originLocationCode": self.origin_airport,
            "destinationLocationCode": self.destination_airport,
            "departureDate": self.out_date,
            "returnDate": self.return_date,
            "adults": self.adults,
            "currencyCode": self.currency,
            "nonStop": self.nonstop,
        }

        # Find the flights cheaper than the target price.
        try:
            response = requests.get(url=offer_endpoint, headers=headers, params=params)
            for flight in response.json()["data"]:
                this_price = float(flight["price"]["grandTotal"])
                if this_price < float(self.price):
                    #print(f"{this_price} is cheaper than {self.price}")
                    cheaper_flights.append(flight)
        except IndexError:
            print(f"IndexError: Data array is empty for {self.out_date}. Skipping to the next.")
        except KeyError:
            print(f"KeyError: Response is not empty, but no data for {self.out_date}. Skipping to the next.")

        return cheaper_flights

    def find_cheapest_flight(self, flights):
        prices = []
        for data in flights:
            prices.append(data["price"]["grandTotal"])
            #print(f"Price is {data["price"]["grandTotal"]}")

        min_price = min(prices)
        min_index = prices.index(min_price)
        min_flight = flights[min_index]

        # Create flight_data object
        origin = min_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = min_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        out_date = min_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = min_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
        cheapest_flight = FlightData(min_price, origin, destination, out_date, return_date, adults=self.adults, currency=self.currency, nonstop=self.nonstop)

        return cheapest_flight

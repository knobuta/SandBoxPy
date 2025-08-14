# Cheap Flight Finder: One of the capstone projects for Udemy 100-days-of-code
# https://www.udemy.com/course/100-days-of-code/learn/lecture/21927934#questions
# Example source code is here: https://gist.github.com/TheMuellenator/150d346a928e4c5dac17005e213634bc

"""
1. Register for Sheety and make a table in Google doc available via Sheety.
    a. Table has destination city, itata code of the cities, and target Lowest Price
2. Register for Amadeus Search API
3. Get the destination from the sheet and look for the cheapest flight available with Amadeus search.
4. Email (not SMS) the cheapest flight to yourself.

TODO: Setup WhatsApp and try SMS instead of email.
"""

from datetime import datetime, timedelta, time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# global variables
ORIGIN = "LON" # London
NONSTOP = "true"
ADULTS = 1
CURRENCY = "GBP" # British pound
DEPARTDATE = datetime.today() + timedelta(days=1) # tomorrow
RETURNDATE = DEPARTDATE + timedelta(days=180) # 3 month later

# -------------------- SHEETY: GET CURRENT DATA in SHEET -------------------- #
data_manager = DataManager()
sheet_data = data_manager.get_sheet_info() # Get current data

# -------------------- AMADEUS: GET IATACODE AND PUT it in SHEET -------------------- #
# IF iataCode is empty in the sheet, access to Amadeus, find iataCode and update iataCode column of the sheet.
if sheet_data[0]["iataCode"] == "": # IF iataCode is empty
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    #print(f"sheet_data:\n {sheet_data}")

    data_manager.sheet_info = sheet_data # update the sheet with iata code
    data_manager.put_sheet_info() # Put the info in sheety
else:
    print(f"sheet_data has iataCode.  Nothing to do.")

# -------------------- AMADEUS: GET CHEAP FLIGHT AND EMAIL -------------------- #
sheet_data = [{'city': 'San Francisco', 'iataCode': 'SFO', 'id': 9, 'lowestPrice': 1000}]

cheapest_flight = ""
for i in range(len(sheet_data)):
    dest_city = sheet_data[i]["city"]
    iata = sheet_data[i]["iataCode"]
    target_price = sheet_data[i]["lowestPrice"]
    flight_info = FlightData(target_price, ORIGIN, iata, DEPARTDATE.strftime("%Y-%m-%d"), RETURNDATE.strftime("%Y-%m-%d"), ADULTS, CURRENCY, NONSTOP)

    cheaper_flights = flight_info.find_cheaper_flights()
    if len(cheaper_flights) > 0:
        print(f"There are {len(cheaper_flights)} flights to {dest_city} with less than {target_price} {CURRENCY}")
        cheapest_flight = flight_info.find_cheapest_flight(cheaper_flights)
        print(f"Cheapest flight is {cheapest_flight.price} {cheapest_flight.currency}")
    else:
        print(f"No flight cheaper than {target_price} to {dest_city}")

    # Slowing down requests to avoid rate limit
    #time.sleep(2)

notification = NotificationManager(cheapest_flight.price, cheapest_flight.origin_airport, cheapest_flight.destination_airport, cheapest_flight.out_date)
notification.send_mail()
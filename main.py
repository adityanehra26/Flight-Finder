# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
import json

from_city = "DEL"  # delhi
sheet_data = None

sheet = DataManager()
flight_data = FlightData()
flight = FlightSearch(fly_from=from_city)



sheet_data = sheet.get_sheet_data()         # getting sheet data


# ======================================= Search flight ======================================= #
def search_flight_and_update_sheet():
    cities = flight.flight_search(sheet_data)
    sheet.update_price_and_link(cities)
    # saving data locally
    with open("price.json", 'w') as file:
        json_obj = json.dumps(cities, indent=4)
        file.write(json_obj)

search_flight_and_update_sheet()
# ======================================= Updating Sheet IATA Code ================================================= #
def update_iata_code():
    city_with_code = flight_data.find_iata_code(sheet_data)  # getting city code

    for i in range(len(sheet_data)):  # updating data locally
        sheet_data[i]['iataCode'] = city_with_code[sheet_data[i]['city']]

    sheet.update_destination_code()  # updating data in sheet with new data

    json_obj = json.dumps(sheet_data, indent=4)
    with open('data.json', 'w') as file:
        file.write(json_obj)  # in local file

import requests
from datetime import datetime


class FlightSearch:

    # This class is responsible for talking to the Flight Search API.
    API_KEY = " "
    header = {'apikey': " "}

    def __init__(self, **kwargs):
        self.__flight_search_endpoint = "https://tequila-api.kiwi.com/v2"
        self.fly_from = kwargs['fly_from'].title()
        self.fly_to = None
        self.date_from = datetime.now().strftime("%d/%m/%Y")
        self.date_to = datetime(day=datetime.now().day, month=(int(self.date_from[3:5])+6),
                                year=datetime.now().year).strftime("%d/%m/%Y")
        self.flight_data = None

    def flight_search(self, sheet):
        endpoint = f"{self.__flight_search_endpoint}/search"
        city_with_lowest_price ={}
        for city_data in sheet:
            print(city_data["iataCode"])
            booking_data = {
                "curr": "INR",
                "fly_from": "DEL", "fly_to": city_data["iataCode"],
                "date_from": self.date_from, "date_to": self.date_to
            }
            response = requests.get(url=endpoint, params=booking_data, headers=FlightSearch.header)
            city_with_lowest_price[city_data["city"]] = [response.json()['data'][0]['price'], response.json()['data'][0]['deep_link']]
        return city_with_lowest_price

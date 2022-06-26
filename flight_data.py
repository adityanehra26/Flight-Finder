import requests

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.header = {'apikey': "7o5ryRrAi-ojU0t3X2QO2c76tK3lLFHp"}
        self.__flight_search_endpoint = "https://tequila-api.kiwi.com"

    def find_iata_code(self, sheet_data):
        endpoint = f"{self.__flight_search_endpoint}/locations/query"
        city_with_iata = {}
        for city_data in sheet_data:
            query = {
                'term': city_data['city']
            }
            response = requests.get(url=endpoint, params=query, headers=self.header)
            city_with_iata[city_data['city']] = response.json()['locations'][0]['code']
        return city_with_iata
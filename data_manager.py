import requests
import json
import smtplib

class DataManager:

    def __init__(self):
        self.sheet_endpoint = "https://api.sheety.co/b4f312f17a051bf84fff621275c9c358/flightDeals/prices"
        self.sheet_data = None

    def get_sheet_data(self):
        response = requests.get(url=self.sheet_endpoint)
        self.sheet_data = response.json()['prices']

        json_obj = json.dumps(self.sheet_data, indent=4)  # adding data to json obj
        file = open(file="data.json",mode='w')
        file.write(json_obj)
        file.close()

        return self.sheet_data

    def update_price_and_link(self, price_data):
        j=0
        send_mail = False
        price_drop_list = {}
        for i in price_data:
            if int(price_data[i][0]) < int(self.sheet_data[j]["lowestPrice"]):
                send_mail = True
                update_endpoint = f"{self.sheet_endpoint}/{self.sheet_data[j]['id']}"
                update = {
                    'price': {
                        'lowestPrice': price_data[i][0],
                        'link': price_data[i][1]
                    }
                }
                price_drop_list[i] = price_data[i]
                response = requests.put(url=update_endpoint, json=update)
            j+= 1

        if send_mail:
            mail_id = "studydemo26@gmail.com"
            password = "Root@2021"
            send_to = "gullupagal@gmail.com"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=mail_id, password=password)
                connection.sendmail(from_addr=mail_id, to_addrs=send_to, msg=f"Subject: Price Drop Alert\n\n"
                                                                             f"Price Drop Cities : {list(price_drop_list.keys())}\n"
                                                                             f"Check Price list : https://docs.google.com/spreadsheets/d/1gBFPraK-Izcildmxpw8vbjJxJoEBuoMJvkxsL8-Q270/edit#gid=0")

    def update_destination_code(self):
        j=0
        for i in self.sheet_data:
            update_endpoint = f"{self.sheet_endpoint}/{i['id']}"
            update = {
                'price': {
                    'iataCode': i['iataCode']
                }
            }
            j += 1
            response = requests.put(url=update_endpoint, json=update)

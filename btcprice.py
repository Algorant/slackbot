import requests
import json


def getBitcoinPrice():
    URL = "https://www.bitstamp.net/api/ticker/"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)["last"])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitstamp API")

# current_price = getBitcoinPrice()
# print(f"The current BTC price is ${current_price}")

from smartapi import SmartConnect
import pandas as pd
import urllib.request
from datetime import datetime
import traceback
from config import hist_api_key, hist_secret_key, client_code, client_password

obj = SmartConnect(api_key=hist_api_key)

data = obj.generateSession(client_code, client_password)

try:
    historicParam = {
        "exchange": "NSE",
        "symboltoken": "3045",
        "interval": "ONE_MINUTE",
        "fromdate": "2021-09-01 00:00",
        "todate": "2021-09-02 23:59"
    }
    historic_data = obj.getCandleData(historicParam)
    price_df = pd.DataFrame(historic_data['data'])
    price_df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    price_df.to_csv('data/sbin_sept1_2021.csv', index=False)
    # logout
    try:
        logout = obj.terminateSession(client_code)
        print("Logout Successfull")
    except Exception as e:
        print("Logout failed: {}".format(e))
except Exception as e:
    historic_data = dict()
    print("No Data Found")
    print("Historic Api failed: {}".format(e))
    print(traceback.print_exc())


def get_ticker_file():
    """
    A function to get all available instruments at Angel Broking
    This is primarily used to get the symbol tokenCode
    """
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    symbol_data = urllib.request.urlopen(url).read().decode()
    df = pd.read_json(symbol_data)

    return df

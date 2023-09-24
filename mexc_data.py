import requests, datetime, time
import pandas as pd
from urllib.parse import urlencode
def get_all_future_symbols():
    url = "https://contract.mexc.com/api/v1/contract/detail"
    response = requests.get(url)
    if response.status_code == 200:
    # The request was successful, so print the response content
        data = response.json()['data']
        symbol_name = [item["symbol"] for item in data]
    else:
    # The request failed, so print the error code
        symbol_name = f'Request failed with error code {response.status_code}'
    return symbol_name

def get_symbol_data(symbol,interval,start,end):
    #interval: Min1、Min5、Min15、Min30、Min60、Hour4、Hour8、Day1、Week1、Month1,default: Min1
    #convert time to timestamp
    start_data_object = datetime.datetime.strptime(start,'%Y-%m-%d')
    end_data_object = datetime.datetime.strptime(end,'%Y-%m-%d')
    start_timestamp = int(time.mktime(start_data_object.timetuple()))
    end_timestamp = int(time.mktime(end_data_object.timetuple()))
    #get the url
    base_url = f'https://contract.mexc.com/api/v1/contract/kline/{symbol}'
    params = {
    "interval": interval,
    "start": start_timestamp,
    "end": end_timestamp
    }
    encoded_params = urlencode(params)
    final_url = f"{base_url}?{encoded_params}"
    #get the data
    response = requests.get(final_url)
    data = response.json()
    df = pd.DataFrame(data['data'])
    return df


def get_all_the_data(symbollist,interval,start,end):
    while True:
        try:
            data = pd.DataFrame()
            for symbol in symbollist:
                print(symbol)
                symbol = symbol
                df = get_symbol_data(symbol,interval,start,end)
                df.insert(0, 'symbol', symbol)
                data = pd.concat([data,df])
            break
        except:
           print("An error occurred while getting data. Retrying in 5 seconds...")
           time.sleep(5) 
    return data
import tkinter as tk
import logging
import requests
import pprint

'''

logger = logging.getLogger()

formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
logging.info("Simply repeating all shit")

response = requests.get("https://testnet.binancefuture.com/fapi/v1/exchangeInfo")
'''


class Name():

    url = 'https://api.binance.com'

    def __init__(self):
        pass

    def doggy(self, endpoint: str, params=None):

        response = requests.get(self.url + endpoint, params)

        if response.status_code == 200:
            return response
        raise ValueError(
            f"The Status code is {response.status_code}"
        )

    def check_time(self):

        answer = self.doggy(endpoint='/api/v3/time').json()['serverTime'] // 1000

        return answer

    def another_func(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000

        res = self.doggy(endpoint='/api/v3/klines', params=data).json()
        lst = []
        for i in res:
            lst.append([i[0], i[1], i[2]])
        return lst


'''def func():
    lst = []
    for info in response.json()['symbols']:
        lst.append(info['baseAsset'])

    return lst

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Created!")
    l = func()
    i=0
    j=0
    for t in l:
        label_widget = tk.Label(root, text= t, borderwidth = 1, width = 8, fg = 'white')
        label_widget.grid(column= i, row = j, sticky = 'ew')
        j+=1
        if j == 8:
            j=0
            i+=1
        else:
            continue
    root.mainloop()'''
t = Name()
print(t.another_func(symbol = 'BTCUSDT', interval="4h"))


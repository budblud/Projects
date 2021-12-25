import logging
import pprint
import requests
import time
import jsonify
import hmac
import hashlib
from urllib.parse import urlencode
import websocket


logger = logging.getLogger()
logger.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(format)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)

class StatusCodeIsWrong(ValueError):
    pass

class BinanceSamples():

    base_url = 'https://api.binance.com'
    api_key = 'x5kcUh8UNy7FgoY7i1ddgFFFjsaNd6vw01xwxeRUuHWCGqdLFYn68xGYXXlWqGvQ'
    secret_key = 'urfwzOCqYjOwalQ6GeK314128AySVe8T1z5lXFyUQ8JroWuvFIblVTn2Iyypn3r4'
    wss_url = 'wss://stream.binance.com/ws'

    def __init__(self, ans):

        self.prices = dict()
        self.ans = ans

        self.headers = {'X-MBX-APIKEY':self.api_key}
        if self.ans == True:
            print('Everything goes well')
        else:
            raise StatusCodeIsWrong(
                "ANS IS NOT TRUE!"
        )


    def endpoint_request(self,method, endpoint: str, params = None):

        if method.upper() == 'GET':
            response = requests.get(self.base_url + endpoint, params, headers=self.headers)
            print(response.status_code, response.json())
        elif method.upper() == 'POST':
            response = requests.post(self.base_url + endpoint, params, headers=self.headers)
        elif method.upper() == 'DELETE':
            response = requests.post(self.base_url + endpoint, params, headers=self.headers)
        else:
            raise StatusCodeIsWrong(
                "You need to chose among (get, post, delete)!"
            )

        if response.status_code == 200:
            logger.info("Message about successful connectivity!")
            return response
        raise StatusCodeIsWrong(
            f"The Status code is {response.status_code}."
        )

    def generate_signature(self, data):
        return hmac.new(self.secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def check_server_time(self):

        server_time = self.endpoint_request('get','/api/v3/time', params=None).json()['serverTime'] // 1000
        datetime = time.strftime('%A, %Y-%m-%d %H:%M:%S', time.localtime(server_time))

        return datetime

    def get_historical_candles(self, symbol: str, interval) -> list:

        data = dict()
        data["symbol"] = symbol
        data["interval"] = interval
        data["limit"] = 1000

        #candles = requests.get(f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}').json()
        candles = self.endpoint_request('get', endpoint='/api/v3/klines', params=data).json()

        list_of_candles = []

        for c in candles:
            list_of_candles.append([c[0], c[1], c[2], c[3], c[4]])

        return list_of_candles


    def get_bid_ask(self, symbol: str):

        data = dict()
        data['symbol'] = symbol

        ob_data = self.endpoint_request('get','/api/v3/ticker/bookTicker', params=data).json()

        if symbol not in self.prices:
            self.prices[symbol] = {'bid': float(ob_data[0]['bidPrice']), 'ask': float(ob_data[0]['askPrice'])}
        else:
            self.prices[symbol]['bid'] = float(ob_data['bidPrice'])
            self.prices[symbol]['ask'] = float(ob_data['askPrice'])

        return self.prices[symbol]

    def get_balance(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)#где есть (HMAC SHA256) нужно уводить signature
        #для этого надо создать функцию generate_signature

        account_data = self.endpoint_request('get', '/api/v3/account', params = data).json()

        lst = []

        for item in account_data['balances']:
            if float(item['free']) != float(0):
                lst.append(item)

        if len(lst) == 0:
            return "You don't have any asset yet"
        else:
            return lst



    def place_order(self, symbol: str, side, quantity, price, stopPrice):
        data = dict()

        data['symbol'] = symbol.upper()
        data['side'] = side
        data['quantity'] = quantity
        data['price'] = price
        data['stopPrice'] = stopPrice
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        res = self.endpoint_request('post', '/api/v3/order/oco', params=data).json()

        return res

    def get_order_status(self, symbol, order_id):

        data = dict()

        data['symbol'] = symbol
        data['order_id'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        res = self.endpoint_request('get', '/api/v3/order', params=data).json()
        return res

    def cancel_order(self, symbol):

        data = dict()

        data['symbol'] = symbol
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        res = self.endpoint_request('delete', '/api/v3/orderList', params=data)

        return res

    def get_ws(self):

        ws = websocket.WebSocketApp(self.wss_url,
                                    on_open=self.on_open,
                                    on_close=self.on_close,
                                    on_error= self.on_error,
                                    on_message=self.on_message
                                    )

    def on_open(self):
        logger.info('Binance connection opened')

    def on_close(self):
        logger.warning('Binance WebSocket connection closed')

    def on_error(self, msg):
        logger.error(f"Binance connection error {msg}")

    def on_message(self,msg):
        print(msg)

binance = BinanceSamples(True)
binance.endpoint_request(method= "GET",endpoint="/api/v3/exchangeInfo")

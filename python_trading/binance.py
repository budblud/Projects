import hashlib

import requests
import logging
import pprint
import time
import hmac
import hashlib
from urllib.parse import urlencode

import websocket
import threading
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#create an instance of the format of output message
format = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

#create file where we want to receive logs to
#then set a format of it + set level of messages(INFO, ERROR, etc)
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(format)
file_handler.setLevel(logging.INFO)

#add the file handler into the logger
logger.addHandler(file_handler)

class Binance:

    publicKey = "eTHLygBxADptedZDmdXljcz9FhV9oQWxsu1NL5803WfOC7WuIi4yyMDu72maXKP4"
    secretKey = "k88NVVIMwHY4B9IbYwjvL9Hlpi5ZKCK6Wd35T77weKrAOxFyPB1Bpb4UY64df0jt"
    wssBaseEndPoint = "wss://stream.binance.com:9443/ws"

    headers = {"X-MBX-APIKEY":publicKey}

    defaultUrl = "https://api.binance.com"

    def __init__(self, runOrno: bool):

        self.prices = dict()
        self.ws = None

        self.id = 1
        if runOrno==True:
            #тк у нас после запуска программы ниче после нее не будет выполнятся(потому что она зациклиться)
            #нам надо сделать так чтобы она работала паралельно и в этом нам помогает threading library
            #t = threading.Thread(target=self.startWs()) просто в скобках указываем функцию, которую хотим запустить в параллели
            t = threading.Thread(target=self.startWs())
            #и запускаем с помощью .start()
            t.start()
        else:
            raise ValueError

    def createSignature(self,data):
        return hmac.new(self.secretKey.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def makeRequest(self, method: str, endPoint: str, data):
        if method.upper() == "GET":
            response = requests.get(self.defaultUrl + endPoint, params=data, headers=self.headers)
        elif method.upper() == "POST":
            response = requests.post(self.defaultUrl + endPoint, params=data, headers=self.headers)
        elif method.upper() == "DELETE":
            response = requests.delete(self.defaultUrl + endPoint, params=data, headers=self.headers)
        else:
            raise ValueError

        if response.status_code == 200:
            return response.json()
        else:
            logger.info("Something went wrong...")

    def getContracts(self, symbol):

        data = dict()
        data["symbol"] = symbol
        exchangeInfo = self.makeRequest(method="GET", endPoint= "/api/v3/exchangeInfo", data= data)

        pprint.pprint(exchangeInfo)

    def getHistoricalCandles(self,symbol,interval):
        data = dict()
        data["symbol"] = symbol
        data["interval"] = interval
        data["limit"] = 1000
        candles = self.makeRequest(method='get', endPoint="/api/v3/klines", data = data)
        return candles

    def getBidAsk(self, symbol):

        data = dict()
        data["symbol"] = symbol
        orderBookInfo = self.makeRequest(method='get', endPoint="/api/v3/ticker/bookTicker", data = data)

        if orderBookInfo is not None:
            self.prices[orderBookInfo["symbol"]] = {"bidPrice" : orderBookInfo["bidPrice"], "askPrice" : orderBookInfo["askPrice"]}

        return self.prices,orderBookInfo

    def currentTime(self):
        response = self.makeRequest(method= "GET",endPoint="/api/v3/time", data= None)['serverTime'] // 1000
        datetime = time.strftime('%A, %Y-%m-%d %H:%M:%S', time.localtime(response))
        return response

    def getBalance(self, type):
        data = dict()
        data["type"] = type
        data["limit"] = 5
        data["timestamp"] = int(time.time()*1000)
        data["signature"] = self.createSignature(data=data)

        response = self.makeRequest(method= "GET", endPoint="/sapi/v1/accountSnapshot", data = data)
        return response['snapshotVos'][0]['data']['balances']

    def placeOrder(self,symbol,side,quantity,type,timeInForce=None,price=None):

        data = dict()
        data["symbol"] =symbol
        data["side"] =side
        data["type"] =type
        data["quantity"] =quantity


        if timeInForce is not None:
            data["timeInForce"] =timeInForce

        if price is not None:
            data["price"] =price

        data["timestamp"] =int(time.time()*1000)
        data["signature"] = self.createSignature(data=data)

        response = self.makeRequest(method="POST", endPoint="/api/v3/order", data=data)
        return response

    def cancelOrder(self,symbol,orderId):

        data = dict()
        data["symbol"] = symbol
        data["orderId"] = orderId

        data["timestamp"] = int(time.time()*1000)
        data["signature"] = self.createSignature(data=data)

        response = self.makeRequest(method="DELETE", endPoint="/api/v3/order", data=data)

    def getOrderStatus(self, symbol, orderId):

        data = dict()
        data["symbol"] = symbol
        data["orderId"] = orderId
        data["timestamp"] = int(time.time()*1000)
        data["signature"] = self.createSignature(data=data)

        orderStatus = self.makeRequest(method="GET", endPoint="/api/v3/order", data=data)

        return orderStatus

    def startWs(self):
        #делаем инстанс вебсокета, параметры входа: url, on_open, on_close,on_message
        #on_open - функция, которая выводит что-то когда наш код запускается + получает команды откуда запрашивать
        #on_close - функция, которая выводит что-то когда вы interupt ваш код
        #on_message - получает от startWs сообщение(в параметры) и выводит их

        self.ws = websocket.WebSocketApp(self.wssBaseEndPoint, on_open=self.onOpen, on_close=self.onClose,
                                    on_message=self.onMessage)
        #ws.run_forever() - запускает бесконечный цикл запросов
        #on_open - запрашивает инфу с помощью функции которая внутри---->
        #инфа которая возвращается идет в on_message(msg)------->
        #внутри on_message(msg) изменяется если надо------>
        #выводится на экран

        self.ws.run_forever()

    def onOpen(self,ws):
        #на открытии вебсокет должен получать инструкции куда отправлять запрос
        logger.info("The connection is opened successfully!")
        #запускаем функцию которая будет запрышивать инфу
        self.subscribeToTheChannel("btcusdt", "1m")

    def onClose(self,close_status_code,close_msg):
        logger.info("The connection is closed!")

    '''def onError(self,ws,question,error):
        logger.info(f"Error has occured: {error}, {question}")'''

    def onMessage(self,ws,msg):
        #тут мы модифицируем сообщение, выводим то, что нам надо
        data = json.loads(msg)
        d = dict()
        d["openPrice"]=data['k']['o']
        d["closePrice"]=data['k']['c']
        d["highPrice"]=data['k']['h']
        d["lowerPrice"]=data['k']['l']
        d["volume"]=data['k']['v']
        print(d)
        #print(msg)


    def subscribeToTheChannel(self,symbol: str, interval: str):
        #сначала смотрим requirements для того, чтобы получать инфу
        #params всегда находятся в list
        #.send отправляет данные
        # #
        # #
        data = dict()
        data["method"] = "SUBSCRIBE"
        data["id"] = self.id
        data["params"] = []
        data["params"].append(symbol.lower() + "@kline_" + interval.lower())

        self.id += 1
        #отправляет все параметры и "подписывается на chanel"
        self.ws.send(json.dumps(data))

binance = Binance(True)

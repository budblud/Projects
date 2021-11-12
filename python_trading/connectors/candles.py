from binance_future import BinanceSamples
import logging

logger = logging.getLogger()
binance = BinanceSamples()
server_time = binance.endpoint_request('/api/v3/time').json()['serverTime'] // 1000
api = 'https://api.binance.com/api/v1/klines'

def some_function(symbol, interval, limit, startTime, endTime):

    data = dict()
    data['symbol'] = symbol
    data['interval'] = interval
    data['limit'] = limit
    data['startTime'] = startTime
    data['endTime'] = endTime

    res = binance.endpoint_request('/api/v1/klines', params = data)

    lst = []

    for item in res:
        lst.append([item[1], item[4]])

    return lst

some_function(symbol='BTCUSDT', interval='4h', limit=1000, startTime=server_time, endTime=server_time-14400000000)


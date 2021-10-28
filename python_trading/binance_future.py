import logging
import requests
import pprint

logger = logging.Logger

def get_contracts():
    response_object = requests.get('https://testnet.binancefuture.com/dapi/v1/exchangeInfo')

    print(response_object.status_code)

    contracts = []
    for contract in response_object.json()['symbols']:
        contracts.append(contract['pair'])

    return contracts



print(get_contracts())



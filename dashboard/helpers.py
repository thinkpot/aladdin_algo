import json

from accounts.models import Client
import requests
from SmartApi import SmartConnect


class AliceBlue:
    def __init__(self, user):
        self.user = user
        self.session_id = Client.objects.get(user=self.user).session_id
        self.base_url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api'

    def get_profile(self, cv):
        url = self.base_url+'/customer/accountDetails'
        headers = {
            "Authorization": "Bearer {0}".format(self.session_id),
            "Content-Type": "application/json"
        }
        response = requests.get(url=url, headers=headers)
        response = response.json()
        cv['profile'] = dict()
        cv['profile']['full_name'] = response.get('accountName')
        cv['profile']['client_user_id'] = response.get('accountId')
        cv['profile']['broker'] = response.get('sBrokerName')

        return cv

    def get_position_book(self, cv):
        url = self.base_url + '/positionAndHoldings/positionBook'
        headers = {
            "Authorization": "Bearer {0}".format(self.session_id),
            "Content-Type": "application/json"
        }
        payload = json.dumps({"ret": "DAY"})
        response = requests.post(url=url, headers=headers, data=payload)
        response = response.json()
        cv['position_book'] = dict()

        if response.get('stat') != 'Not_Ok':
            cv['position_book']['today_realisedprofitloss'] = sum([ float(rpl['realisedprofitloss']) for rpl in response])
            cv['position_book']['error'] = False
        else:
            cv['position_book']['error'] = True

        return cv

    def place_options_order(self, symbol):
        url = self.base_url + '/placeOrder/executePlaceOrder'
        headers = {
            "Authorization": "Bearer {0}".format(self.session_id),
            "Content-Type": "application/json"
        }
        order_details = {
            "discqty": "25",
            "trading_symbol": "NIFTY 26SEP24 27000 CE",
            "exch": "NFO",
            "transtype": "BUY",
            "ret": "DAY",
            "prctyp": "MKT",
            "qty": "25",
            "symbol_id": "65916",
            "pCode": "MIS",
            "complexty": "REGULAR",
            "orderTag": "order1"
        }
        response = requests.post(url=url, headers=headers, data=order_details)
        response = response.json()
        print("Response ", response)
        return True


class Angelone:
    def __init__(self, user):
        self.user = user
        self.auth_token = Client.objects.get(user=self.user).access_token
        self.base_url = 'https://apiconnect.angelbroking.com'
        self.client = Client.objects.get(user=self.user)
        self.headers = {
            "Authorization": self.auth_token,
            "Content-Type": "application/json",
            'X-PrivateKey': self.client.client_id,
            'X-ClientLocalIP': '127.0.0.1',
            'X-ClientPublicIP': '106.193.147.98',
            'X-MACAddress': '10:94:bb:d6:82:3a',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB'
        }

    def get_profile(self, cv):
        url = self.base_url+'/rest/secure/angelbroking/user/v1/getProfile'
        response = requests.get(url=url, headers=self.headers)
        response = response.json()

        cv['profile'] = dict()
        cv['profile']['full_name'] = response.get('data').get('name')
        cv['profile']['client_user_id'] = response.get('data').get('clientcode')
        cv['profile']['broker'] = response.get('data').get('broker')

        return cv

    def get_capital(self, cv):
        url = self.base_url + '/rest/secure/angelbroking/user/v1/getRMS'
        response = requests.get(url=url, headers=self.headers)
        response = response.json()
        cv['capital'] = dict()
        cv['capital']['availablecash'] = response.get('data').get('availablecash')

        return cv

    def get_position_book(self, cv):
        url = self.base_url + '/rest/secure/angelbroking/order/v1/getPosition'
        response = requests.get(url=url, headers=self.headers)
        response = response.json()
        if response['data'] is not None:
            cv['position_book'] = dict()
            cv['position_book']['today_realisedprofitloss'] = sum([float(position['realised']) for position in response.get('data')])

            current_capital = float(self.get_capital({})['capital']['availablecash'])
            previous_capital = current_capital + abs(cv['position_book']['today_realisedprofitloss'])

            cv['position_book']['today_per_realisedprofitloss'] = round(((current_capital - (previous_capital) ) / previous_capital )*100, 2)

        return cv

    def get_trade_book(self, cv):
        url = self.base_url + '/rest/secure/angelbroking/order/v1/getTradeBook'
        response = requests.get(url=url, headers=self.headers)
        response = response.json()
        if response['data'] is not None:
            cv['trade_book']['trades'] = response.get('data')

        return cv

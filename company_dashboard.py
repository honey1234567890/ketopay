from utilities import make_request
import requests
import firebase_admin
from firebase_admin import db
from flask import Flask

databaseURL = 'https://pythondatabase-1a4c2-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate('pythondatabase-1a4c2-firebase-adminsdk-rv5ve-a9337d0952.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})

url = "https://api.coindcx.com/exchange/ticker"
url_2 = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/inr/usd.json"


def get_USDTINR_price():
    response = requests.get(url)
    data = response.json()
    for i in data:
        if i['market'] == 'USDTINR':
            current_price = float(i['ask']) + 1
    return current_price


def currency_factor(currency1, currency2):
    api_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/" + currency1.lower() + "/" + currency2.lower() + ".json"
    currency_factors = requests.get(api_url).json()[currency2.lower()]
    return currency_factors


#  fee=1, company charge = 1
def calculate_profit(amount_in_usd):
    sum_in_usd_inr = amount_in_usd * currency_factor('USD', 'INR')
    company_charge = 1 / 100 * sum_in_usd_inr
    print(sum_in_usd_inr)
    sum_in_usdt_inr = amount_in_usd * get_USDTINR_price()
    print(sum_in_usdt_inr)
    fee = 1 / 100 * (sum_in_usd_inr)
    net_in_rs = ((sum_in_usdt_inr + company_charge)) - (sum_in_usd_inr + (fee * 2))
    net_in_dollars = net_in_rs * currency_factor('INR', 'USD')
    profit_percent = (net_in_rs / sum_in_usd_inr) * 100
    text = 'With a USDT price of ' + str(get_USDTINR_price()) + ', we get a profit of ' + str(
        net_in_rs) + ' with a profit percentage of ' + str(profit_percent)
    return text, profit_percent, net_in_dollars


def total_transaction_value():
    amount = 0
    ref = db.reference('/all_transactions')
    for i in list(ref.get()):
        r = db.reference('/all_transactions/' + i)
        local_amount = r.get()['amount']
        currency = r.get()['currency']
        if currency != "USD":
            amount_in_usd = currency_factor(currency, "USD") * local_amount
            amount = amount + amount_in_usd
        else:
            amount = amount + local_amount
    return amount


def total_profit():
    a = calculate_profit(total_transaction_value())
    return a


def calculate_profit_on_transaction(paymentId):
    ref = db.reference('/all_transactions')
    r = db.reference('/all_transactions/' + paymentId)
    local_amount = r.get()['amount']
    currency = r.get()['currency']
    if currency != "USD":
        amount_in_usd = local_amount * currency_factor(currency, "USD")
        print(amount_in_usd)
    else:
        amount_in_usd = local_amount
    a = calculate_profit(amount_in_usd)
    return a


def total_transactions():
    ref = db.reference('/all_transactions')
    return len(list(ref.get()))


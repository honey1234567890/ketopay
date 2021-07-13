from time import time
from utilities import make_request
from pprint import pprint
from datetime import datetime


def get_all_transactions(customer_id):
    path = "/v1/payments?customer=" + customer_id
    a = make_request(method="get", path=path)
    list_of_all_transactions = a['data']

    transaction_data = {}

    for i in list_of_all_transactions:
        transaction_data[i['id']] = {
            'amount': i['amount'],
            'currency': i['currency_code'],
            'country_code': i['country_code'],
            'payment_method': i['payment_method_data']['type'],
            'paid': i['paid'],
            'time': datetime.fromtimestamp(i['paid_at']).ctime(),
         }

    return transaction_data


def get_latest_transaction_data(customerId):
    a = list(get_all_transactions(customerId))
    latest_transaction_id = a[len(a) - 1]
    latest_data = get_all_transactions(customerId)[latest_transaction_id]
    return latest_data,latest_transaction_id

cust_payment_data,cust_payment_id=get_latest_transaction_data('cus_e8f86168fee0da3c34edb8fc0124c530')
payment_time=cust_payment_data['time']
a=payment_time.split()
payment_time_day=a[2]
payment_time_month=a[1]
print(payment_time_day)
print(payment_time_month)
print(payment_time)
print (cust_payment_id)

response = make_request(method='get',
                        path='/v1/payments?limit=1')
company_latest_transaction_id=response['data'][0]['id']
print(company_latest_transaction_id)
if cust_payment_id==company_latest_transaction_id:
    print("payment Captured")
else:
    print("Payment not captured")
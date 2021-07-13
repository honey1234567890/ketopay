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

pprint(get_latest_transaction_data('cus_2e669e621e9665362bcfda3db381c2de'))
response = make_request(method='get',
                        path='/v1/payments?limit=1')
#pprint(response['data'])
pprint(response['data'][0]['id'])
pprint(response['data'][0]['customer_token'])
pprint(response['data'][0]['paid'])
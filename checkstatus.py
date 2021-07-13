from utilities import make_request
from pprint import pprint

companylasttransaction= make_request(method='get',path="/v1/payments?limit=1")
companylasttransaction=companylasttransaction['data'][0]['customer_token']
pprint(companylasttransaction)

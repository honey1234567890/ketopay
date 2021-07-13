from pprint import pprint

from utilities import make_request

customer_data = {
    'addresses': [],
    'business_vat_id': '123456789',
    'created_at': 1625234223,
    'default_payment_method': '',
    'delinquent': False,
    'description': '',
    'discount': None,
    'email': 'shilpadoe@rapyd.net',
    'ewallet': '',
    'id': 'cus_47104c73444d548cbe69952bbaf7f665',
    'invoice_prefix': 'JD-',
    'metadata': {'merchant_defined': True},
    'name': 'Amogh Saraf',
    'payment_methods': None,
    'phone_number': '+14155559993',
    'subscriptions': None
}
result = make_request(method='post', path='/v1/customers/cus_47104c73444d548cbe69952bbaf7f665', body=customer_data)
pprint(result)
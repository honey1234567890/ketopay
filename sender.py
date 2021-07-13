from utilities import make_request
from pprint import pprint
body={
    "currency": "USD",
    "country": "US",
    "entity_type": "company",
    "company_name":"Keto2",
    "identification_type": "identification_id",
    "identification_value": "123457890",
    "phone_number": "1234569870",
    "occupation": "salesman",
    "source_of_income": "salary",
    "date_of_birth": "12/12/1980",
    "address": "123 Main Street",
    "purpose_code": "salary",
    "beneficiary_relationship": "friend"
}
results = make_request(method='post',
                           path='/v1/payouts/sender',
                           body=body)
pprint(results)
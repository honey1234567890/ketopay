from utilities import make_request
from pprint import pprint

def bank_account_fields(country, currency):
    list_payout_methods_by_country = make_request(method="get",
                                                  path="/v1/payouts/supported_types?beneficiary_country=" + country + "&payout_currency=" + currency + '&category=bank')
    list_payout_methods_by_country = list_payout_methods_by_country['data']
    pprint(list_payout_methods_by_country)

bank_account_fields("CA","CAD")
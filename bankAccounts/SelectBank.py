from utilities import make_request
from pprint import pprint


def bank_accounts(country, currency):
    list_payout_methods_by_country = make_request(method="get",
                                                  path="/v1/payouts/supported_types?beneficiary_country=" + country + "&payout_currency=" + currency + '&category=bank')
    list_payout_methods_by_country = list_payout_methods_by_country['data']
    payout_method_by_country_type_bank_type = []
    payout_method_by_country_type_bank_name = []
    for payout_type in list_payout_methods_by_country:
        payout_method_by_country_type_bank_type.append(payout_type['payout_method_type'])
        payout_method_by_country_type_bank_name.append(payout_type['name'])
    pprint(payout_method_by_country_type_bank_name)
    dict_a={}
    for i in range(len(payout_method_by_country_type_bank_name)):
      dict_a[payout_method_by_country_type_bank_name[i]]=payout_method_by_country_type_bank_type[i]
    return payout_method_by_country_type_bank_name,payout_method_by_country_type_bank_type
    

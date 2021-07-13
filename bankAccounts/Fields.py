
from utilities import make_request
from pprint import pprint
def bank_account_fields(country, currency, bank_method_type_selected):
    list_payout_methods_by_country = make_request(method="get",
                                                  path="/v1/payouts/supported_types?beneficiary_country=" + country + "&payout_currency=" + currency + '&category=bank')
    list_payout_methods_by_country = list_payout_methods_by_country['data']
    payout_method_by_country_type_bank_type = []
    payout_method_by_country_type_bank_name = []
    for payout_type in list_payout_methods_by_country:
        payout_method_by_country_type_bank_type.append(payout_type['payout_method_type'])
        payout_method_by_country_type_bank_name.append(payout_type['name'])

    bank_method_type_selected = bank_method_type_selected  # "in_allahabadbank_bank"  # bank method selected
    b = make_request(method="get",
                     path="/v1/payouts/" + bank_method_type_selected + "/details?sender_country=US&sender_currency"
                                                                       "=USD&beneficiary_country=" + country +
                          "&payout_currency=" + currency +
                          "&sender_entity_type=company&beneficiary_entity_type=individual&payout_amount=10")
    required_fields = []
    required_field = b['data']["beneficiary_required_fields"]
    for i in required_field:
        required_fields.append(i['name'])

    pprint(required_fields)
    return required_fields
    
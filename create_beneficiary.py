from pprint import pprint

from utilities import make_request


def create_beneficiary(country, currency, first_name, last_name, identification_value, phone_number, account_no,
                       bank_branch_code):

    beneficiary_details_2 = {
        "category": "bank",
        "country": country,
        "currency": currency,
        "entity_type": "individual",
        "first_name": first_name,
        "last_name": last_name,
        "identification_type": "identification_id",
        "identification_value": identification_value,
        "payout_method_type":"in_allahabadbank_bank",
        "phone_number": phone_number,
        "account_number": account_no,
        "bank_branch_code": bank_branch_code
    }

    result = make_request(method='post',
                          path='/v1/payouts/beneficiary',
                          body=beneficiary_details_2)
    return pprint(result)


from pprint import pprint

from utilities import make_request


# Send payment link to sender direcly
def send_payment_link(amount, country, currency, customerId):
    comment = 'Transfer the money to company first'
    body = {
        "amount": amount,
        "complete_payment_url": "/send_success",
        "country": country,
        "currency": currency,
        "customer": customerId,
        "requested_currency": "USD",
        "fixed_side": "buy",
        "error_payment_url": "http://example.com/error",
        "merchant_reference_id": "950ae8c6-78",
        "cardholder_preferred_currency": True,
        "language": "en",
        "metadata": {
            "merchant_defined": True
        },
        "ewallet": "ewallet_95fd207029e27b020c22b0e6262e75c4",  # Company's USD Wallet
        "payment_method_type_categories": [
            "cash",
            "bank_transfer",

        ],
    }
    result = make_request(method='post', path='/v1/checkout', body=body)
    pprint(result)

send_payment_link("5000", "IN","INR", "cus_066600669ac32e8a4dc11590330256de")


# Send payment link to payee's email
def request_payment(amount, country_of_the_payer, currency_of_the_payer, customerId_of_the_payer):
    body = {
        "amount": amount,
        "complete_payment_url": "/send_success",
        "country": country_of_the_payer,  # Country of the guy who is paying
        "currency": currency_of_the_payer,  # Currency of the guy who is paying
        "customer": customerId_of_the_payer,  # customerId of the guy who is paying, which you can get by email
        "requested_currency": "USD",
        "fixed_side": "buy",
        "error_payment_url": "http://example.com/error",
        "merchant_reference_id": "950ae8c6-78",
        "cardholder_preferred_currency": True,
        "language": "en",
        "payment_method_type_categories": [
            "cash",
            "bank_transfer",

        ],
        "metadata": {
            "merchant_defined": True
        },
        "ewallet": "ewallet_95fd207029e27b020c22b0e6262e75c4",  # Company's USD Wallet

    }
    result = make_request(method='post', path='/v1/checkout', body=body)
    token = result['data']['id']
    complete_url = "https://sandboxcheckout.rapyd.net/?token=" + token
    return complete_url



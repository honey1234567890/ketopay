from utilities import make_request
from utilities import create_customer


def create_wallet(email, name, country_code, phone_number):
    a = create_customer(email, name, country_code, phone_number)
    b = a.split('_')
    wallet_suffix = b[1]
    wallet_prefix = 'wal'
    wallet_id = wallet_prefix + "_" + wallet_suffix
    amount_deposited = 0
    return wallet_id, amount_deposited


def create_new_wallet(customerId):
    b = customerId.split('_')
    wallet_suffix = b[1]
    wallet_prefix = 'wal'
    wallet_id = wallet_prefix + "_" + wallet_suffix
    return wallet_id


print(create_wallet("abcd@gmail.com", " Tagore", "+91", "8789074044"))


def store_money_in_wallet(amount, country, currency, customerId):
    body = {
        "amount": amount,
        "complete_payment_url": "http://localhost/complete",
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
        "payment_method_type": None
    }
    result = make_request(method='post', path='/v1/checkout', body=body)
    token = result['data']['id']
    complete_url = "https://sandboxcheckout.rapyd.net/?token=" + token
    return complete_url

from utilities import make_request

import firebase_admin
from firebase_admin import db
from pprint import pprint
from get_customer_id import get_customerId_by_email

databaseURL = 'https://payyed-d3a31-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate('payyed-d3a31-firebase-adminsdk-phsz7-03435e06e4.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})


def payout(receiver_email, payout_amount):
    sender = make_request(method="get", path="/v1/payouts/sender/sender_c4657332125d21a92f1e9995b75bdd8f")
    ref_parent = db.reference('/all_customers/')
    beneficiary_customer_id = get_customerId_by_email(receiver_email)
    beneficiary_details = ref_parent.child(beneficiary_customer_id).child('beneficiary').get()
    receiver_profile_details = ref_parent.child(beneficiary_customer_id).child('profile').get()
    dummy_body={
        "beneficiary": {
            beneficiary_details
        },
        "sender": sender['data'],
        "ewallet": "ewallet_95fd207029e27b020c22b0e6262e75c4",
        "sender_country": "US",
        "sender_currency": "USD",
        "sender_entity_type": "company",
        "description": "Payout from Keto",
        "beneficiary_country": receiver_profile_details['country'],
        "beneficiary_entity_type": 'individual',
        "confirm_automatically": False,
        "payout_amount": payout_amount,
        "payout_currency": receiver_profile_details['currency'],
        "payout_method_type": beneficiary_details['payout_method_type'],
        "metadata": {
            "merchant_defined": True
        }
    }
    a = make_request(method="post", path="/v1/payouts/", body=dummy_body)
    fx_rate = a['data']['fx_rate']
    payout_id = a['data']['id']
    make_request(method='delete',path=f'/v1/payouts/{payout_id}')
    payout_amount_2 = fx_rate * payout_amount
    body = {
        "beneficiary": {
            beneficiary_details
        },
        "sender": sender['data'],
        "ewallet": "ewallet_95fd207029e27b020c22b0e6262e75c4",
        "sender_country": "US",
        "sender_currency": "USD",
        "sender_entity_type": "company",
        "description": "Payout from Keto",
        "beneficiary_country": receiver_profile_details['country'],
        "beneficiary_entity_type": 'individual',
        "confirm_automatically": True,
        "payout_amount": payout_amount_2,
        "payout_currency": receiver_profile_details['currency'],
        "payout_method_type": beneficiary_details['payout_method_type'],
        "metadata": {
            "merchant_defined": True
        }
    }
    make_request(method="post", path="/v1/payouts/", body=body)
    return 'Successful',fx_rate

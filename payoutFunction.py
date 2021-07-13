import firebase_admin
from firebase_admin import db
from pprint import pprint
from utilities import make_request
from datetime import datetime
from pprint import pprint

databaseURL = 'https://payment-gateway-f5a88-default-rtdb.asia-southeast1.firebasedatabase.app'
cred_obj = firebase_admin.credentials.Certificate('payment-gateway-f5a88-firebase-adminsdk-qb5my-ab2fd7c3cb.json')
#default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})


def withdraw_money_local_currency(customerId,amount):
    sender = make_request(method="get", path="/v1/payouts/sender/sender_5e9a334f29efbea3b1f3c5f5077b6106")
    ref_parent = db.reference('customers')
    beneficiary_details = ref_parent.child(customerId).child('beneficiary').get()
    receiver_profile_details = ref_parent.child(customerId).child('Profile').get()
    body = {
        "beneficiary": beneficiary_details,
        "sender": sender['data'],
        "ewallet": "ewallet_5a117052ee9351138f6038834b10433a",
        "sender_country": "US",
        "sender_currency": "USD",
        "sender_entity_type": "company",
        "description": "Payout from Keto",
        "beneficiary_country": receiver_profile_details['country'],
        "beneficiary_entity_type": 'individual',
        "confirm_automatically": True,
        "payout_amount": amount,
        "payout_currency": receiver_profile_details['currency'],
        "payout_method_type": beneficiary_details['banktype'],
        "metadata": {
            "merchant_defined": True
        }
    }
    response = make_request(method="post", path="/v1/payouts/", body=body)
    pprint(response)
    #Complete Payout
    payout_id = response['data']['id']
    amount = response['data']['amount']
    payment_time = datetime.fromtimestamp(response['data']['created_at']).ctime().split()
    payment_time_day=payment_time[2]
    payment_time_month=payment_time[1]
    results = make_request(method='post',
                           path=f'/v1/payouts/complete/{payout_id}/{amount}')
    wallet_current_balance=ref_parent.child(customerId).child('wallet/balance').get()
    wallet_current_balance=int(wallet_current_balance)
    wallet_updated_balance=wallet_current_balance-int(amount)
    ref_parent.child(customerId).child('wallet').update({"balance":wallet_updated_balance})
    data={
        "amount":str(amount)+receiver_profile_details['currency'],
        "action":"Withdrawn from Wallet",
        "id":payout_id,
        "status":"Completed",
        "date_day":payment_time_day,
        "date_month":payment_time_month,
        "date_year":payment_time[0]
    }
    ref_parent.child(customerId).child('transactions').child(payout_id).update(data)
    return response,results
    
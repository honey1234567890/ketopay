import json

import firebase_admin
from firebase_admin import db
from pprint import pprint

databaseURL = 'https://payment-gateway-f5a88-default-rtdb.asia-southeast1.firebasedatabase.app/'
cred_obj = firebase_admin.credentials.Certificate('payment-gateway-f5a88-firebase-adminsdk-qb5my-ab2fd7c3cb.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})


def get_customerId_by_email(email):
    ref = db.reference('customers')

    for i in list(ref.get()):
        r = db.reference('customers/' + i)
        r = r.child('Profile').get()['email']
        if r == email:
            return i

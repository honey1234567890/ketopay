from get_customer_id import get_customerId_by_email
from pprint import pprint
from flask import config
from datetime import datetime
import pyrebase

from utilities import make_request

config = {
    "apiKey": "AIzaSyDi0s4cV7eeultcnZTEkyQp7FchO5L6TGo",
    "authDomain": "payment-gateway-f5a88.firebaseapp.com",
    "databaseURL": "https://payment-gateway-f5a88-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "payment-gateway-f5a88",
    "storageBucket": "payment-gateway-f5a88.appspot.com",
    "messagingSenderId": "413267159482",
    "appId": "1:413267159482:web:69047cd2cd5bddae4ad583"
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()
def send_payment(amount,country,currency,customer_id,email):
 checkout_page={
    "amount": amount,
    "complete_payment_url": "http://mediapipe-com.stackstaging.com/",
    "country": country,
    "currency": currency,
    "customer": customer_id,
    "error_payment_url": "http://www.rapyd.net",
    "merchant_reference_id": "950ae8c6-79",
    "language": "en",
    "metadata": {
        "merchant_defined": True
    },
    "payment_method_type_categories": [
        "bank_redirect",
        "cash",
        "card",
        "ewallet",
        "bank_transfer"
    ]
  }
 result = make_request(method='post', path='/v1/checkout', body=checkout_page)
 payment_time = datetime.fromtimestamp(result['data']['timestamp']).ctime().split()
 token = result['data']['id']
 sender_transactions_data={
     "id":token,
     "amount":amount+" "+currency,
     "action":"Sent to "+email,
     "status":"Processing",
     "date_day":payment_time[2],
     "date_month":payment_time[1],
     "date_year":payment_time[0]
 }
 receiver_customer_id=get_customerId_by_email(email)
 sender_emailid=db.child("customers").child(customer_id).child("Profile/email").get().val()
 receiver_transactions_data={
     "id":token,
     "amount":amount+" "+currency,
     "action":"Money Received From"+" "+sender_emailid,
     "status":"Processing",
     "date_day":payment_time[2],
     "date_month":payment_time[1],
     "date_year":payment_time[0]
 }
 db.child("customers").child(customer_id).child("transactions").child(token).update(sender_transactions_data)
 db.child("customers").child(receiver_customer_id).child("transactions").child(token).update(receiver_transactions_data)
 pprint(result)
 return result["data"]["redirect_url"]
 
  

def request_payment(amount,country,currency,customer_id,email):
 checkout_page={
    "amount": amount,
    "complete_payment_url": "http://mediapipe-com.stackstaging.com/",
    "country": country,
    "currency": currency,
    "customer": customer_id,
    "error_payment_url": "http://www.rapyd.net",
    "merchant_reference_id": "950ae8c6-79",
    "language": "en",
    "metadata": {
        "merchant_defined": True
    },
    "payment_method_type_categories": [
        "bank_redirect",
        "cash",
        "card",
        "ewallet",
        "bank_transfer"
    ]
  }
 result = make_request(method='post', path='/v1/checkout', body=checkout_page)
 payment_time = datetime.fromtimestamp(result['data']['timestamp']).ctime().split()
 token = result['data']['id']
 requester_email_id=db.child("customers").child(customer_id).child("Profile/email").get().val()
 requester_transactions_data={
     "checkout_id":token,
     "amount":amount+" "+currency,
     "action":"Requested from "+email,
     "status":"Processing",
     "date_day":payment_time[2],
     "date_month":payment_time[1],
     "date_year":payment_time[0]
 }
 payee_customer_id=get_customerId_by_email(email)
 payee_transaction_data={
     "checkout_id":token,
     "amount":amount+" "+currency,
     "action":"Payment Pending for "+requester_email_id,
     "status":"Processing",
     "date_day":payment_time[2],
     "date_month":payment_time[1],
     "date_year":payment_time[0]
 }
 db.child("customers").child(customer_id).child("transactions").child(token).update(requester_transactions_data)
 db.child("customers").child(payee_customer_id).child("transactions").child(token).update(payee_transaction_data)
 pprint(result)
 return result["data"]["redirect_url"]
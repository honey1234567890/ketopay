from utilities import make_request
from datetime import datetime
import pyrebase
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
def walletDeposit(amount,country,currency,customer_id):
 checkout_page={
    "amount": amount,
    "complete_payment_url": "https://ketopayment.herokuapp.com/sendsuccess",
    'complete_checkout_url': "https://ketopayment.herokuapp.com/sendsuccess",
    "country": country,
    "currency": currency,
    "customer": customer_id,
    "error_payment_url": "https://ketopayment.herokuapp.com/dashboard",
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
 current_wallet_balance=db.child("customers/"+customer_id+"/wallet/balance").get().val()
 current_wallet_balance=int(current_wallet_balance)
 amount=int(amount)
 wallet_balance=current_wallet_balance+amount
 db.child("customers/"+customer_id+"/wallet").update({"balance":wallet_balance})
 data={
        "amount":str(amount)+currency,
        "action":"Deposited to Wallet",
        "id":token,
        "status":"Completed",
        "date_day":payment_time[2],
        "date_month":payment_time[1],
        "date_year":payment_time[0]
    }
 db.child("customers").child(customer_id).child('transactions').child(token).update(data)
 return result["data"]["redirect_url"]

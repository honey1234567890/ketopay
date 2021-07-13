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

def checkWithdraw(withdrawing_amount,customer_id):
 current_amount = int(db.child("customers").child(customer_id).child("wallet/balance").get().val())
 withdrawing_amount=int(withdrawing_amount)
 balance_left=current_amount-withdrawing_amount
 if balance_left>= 0:
    value=1
 else:
    value=0
 print(value)
 return value
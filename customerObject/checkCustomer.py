from utilities import make_request
from pprint import pprint
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

def check_customer(email):
    all_users = db.child("customers").get()
    for user in all_users.each():
     customer_id=user.key()
     print(customer_id)
     path="customers/"+customer_id+"/Profile/email"
     customer_email=db.child(path).get().val()
     print(customer_email)
     if (customer_email==email) :
      value=1
      return value

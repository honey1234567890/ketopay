
from pprint import pprint

from flask import config

from utilities import make_request
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

def create_customer(email,name,phn_num,country,countryCurrency): 
  customer ={
    "business_vat_id": "123456789",
    "email":email,
    "invoice_prefix": "JD-",
    "metadata": {
    	"merchant_defined": True
    },
    "name": name,
    "phone_number":phn_num,
  }
  result = make_request(method='post', path='/v1/customers', body=customer)
  pprint(result)
  cust_id=result["data"]["id"]
  cust_name=result["data"]["name"]
  cust_email=result["data"]["email"]
  cust_phone=result["data"]["phone_number"]
  profile_data={
    "Profile" : {
        "id": cust_id,
        "name":cust_name,
        "email":cust_email,
        "phone_number":cust_phone,
        "country":country,
        "currency":countryCurrency
    }
  }
  wallet=create_new_wallet(cust_id)
  print(wallet)
  db.child("customers").child(cust_id).set(profile_data)
  db.child("customers").child(cust_id).child("wallet").set({"wallet id":wallet,"balance":0,"currency":countryCurrency})
  
  
def create_new_wallet(cust_Id):
    b = cust_Id.split('_')
    wallet_suffix = b[1]
    wallet_prefix = 'wal'
    wallet_id = wallet_prefix + "_" + wallet_suffix
    return wallet_id

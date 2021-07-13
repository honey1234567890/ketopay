from pprint import pprint
import pyrebase


config={"apiKey": "AIzaSyDi0s4cV7eeultcnZTEkyQp7FchO5L6TGo",
    "authDomain": "payment-gateway-f5a88.firebaseapp.com",
    "databaseURL": "https://payment-gateway-f5a88-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "payment-gateway-f5a88",
    "storageBucket": "payment-gateway-f5a88.appspot.com",
    "messagingSenderId": "413267159482",
    "appId": "1:413267159482:web:69047cd2cd5bddae4ad583"}

firebase=pyrebase.initialize_app(config)
db=firebase.database()
all_transactions=db.child("customers").child("cus_e8f86168fee0da3c34edb8fc0124c530").child("transactions").get()
print(all_transactions)
a=[]
for user in all_transactions.each():
 a.append(user.val()) # {name": "Mortimer 'Morty' Smith"}
pprint(a)
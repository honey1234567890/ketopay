import pyrebase
config={
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

def general_function(customer_id):
 print(db.child("customers").child(customer_id).child("Profile/email").get().val())


general_function("cus_6161402ff91465f800fd1e55a62e3d6c")
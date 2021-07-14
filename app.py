from checkWithdrawFeasibility import checkWithdraw
from payoutFunction import withdraw_money_local_currency
from wallet_deposit import walletDeposit
from customerObject.checkCustomer import check_customer
from bankAccounts.Fields import bank_account_fields
from bankAccounts.SelectBank import bank_accounts
from send_Request_Payment import request_payment, send_payment
from customerObject.createCust import create_customer
from flask import Flask, render_template, request, redirect, session, url_for

import pyrebase
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)
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
auth=firebase.auth()
db=firebase.database()
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
      try:
       firstname=request.form['Fname']
       lastname=request.form['Lname']
       usr_name=" ".join((firstname,lastname))
       mobile=request.form['mobile']
       usr_email=request.form['email']
       password=request.form['user_pwd']
       countryVariable=request.form['country'].split()
       country=countryVariable[0]
       countryCode=countryVariable[1]
       countryCurrency=countryVariable[2]
       auth.create_user_with_email_and_password(usr_email,password)
       create_customer(usr_email,usr_name,countryCode+mobile,country,countryCurrency)
       return redirect('/login')
      except:
        existing_account='Email Already in Use'
        return render_template('signup.html', existing_message=existing_account)   
    return render_template('signup.html')


@app.route("/login", methods=["GET","POST"])
def login():
    try:
       session['usr']
       all_users = db.child("customers").get()
       for user in all_users.each():
            customer_id=user.key()
            path="customers/"+customer_id+"/Profile/session"
            customer_session=db.child(path).get().val()
            if (customer_session==session['usr']) :
              customer_name=db.child("customers").child(customer_id).child("Profile/name").get().val() 
              return render_template("dashboard.html",username=customer_name)
    except:
        if request.method == "POST":
         try:
          email = request.form["email"]
          password = request.form["user_pwd"]
          user = auth.sign_in_with_email_and_password(email, password)
          user = auth.refresh(user['refreshToken'])
          user_id = user['idToken']
          session['usr'] = user_id
          print(session['usr'])
          all_users = db.child("customers").get()
          for user in all_users.each():
           customer_id=user.key()
           path="customers/"+customer_id+"/Profile/email"
           customer_email=db.child(path).get().val()
           if (customer_email==email) :
            db.child("customers").child(customer_id).child("Profile").update({"session":session['usr']})
            customer_name=db.child("customers").child(customer_id).child("Profile/name").get().val()
            if db.child("customers").child(customer_id).child("beneficiary").get().val() is None:
                return redirect("/verification")
            else:
                return redirect("/dashboard")
         except:
           wrng_message="Invalid Credentials"
           return render_template('login.html',wrng_msg=wrng_message)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    try:
        session['usr']
        all_users = db.child("customers").get()
        for user in all_users.each():
            customer_id=user.key()
            path="customers/"+customer_id+"/Profile/session"
            customer_session=db.child(path).get().val()
            if (customer_session==session['usr']) :
              customer_name=db.child("customers").child(customer_id).child("Profile/name").get().val()
              cust_id=customer_id
        wallet_balance=db.child("customers/"+cust_id+"/wallet/balance").get().val() 
        currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()     
        if  db.child("customers").child(cust_id).child("transactions").get().val() is None:
            err_msg="No Transactions"
            return render_template("dashboard.html",username=customer_name,err_msg=err_msg,balance=wallet_balance,currency=currency)
        else:
         all_transactions=db.child("customers").child(cust_id).child("transactions").get()
         a=[]
         for user in all_transactions.each():
          a.append(user.val())
         return render_template("dashboard.html",username=customer_name,transactions=a,balance=wallet_balance,currency=currency)
    except KeyError:
        return redirect('/login')


@app.route('/send',methods=["GET","POST"])
def send():
    try:
        session['usr']
        all_users = db.child("customers").get()
        for user in all_users.each():
            customer_id=user.key()
            path="customers/"+customer_id+"/Profile/session"
            customer_session=db.child(path).get().val()
            if (customer_session==session['usr']) :
              cust_id=customer_id
        if request.method=="POST":
           receiver_email=request.form['email']
           amount=request.form['amount']
           payer_id=cust_id
           countryandcode=request.form['currency'].split()
           country=countryandcode[0]
           currency=countryandcode[1]
           print(receiver_email)
           email_check=check_customer(receiver_email)
           if email_check==1:
            payment_url=send_payment(amount,country,currency,payer_id,receiver_email)
            return render_template("send-money-confirm.html", email=receiver_email,amount=amount,currency=currency,payment_url=payment_url)
           else:
            error_message="Email was not found linked with the existing customers"
            return render_template("send-money.html", error_message=error_message)
    except KeyError:
        return redirect('/login')
    return render_template("send-money.html")

@app.route('/request', methods=["GET","POST"])
def money_request():
    try:
        session['usr']
        all_users = db.child("customers").get()
        for user in all_users.each():
            customer_id=user.key()
            path="customers/"+customer_id+"/Profile/session"
            customer_session=db.child(path).get().val()
            if (customer_session==session['usr']) :
              cust_id=customer_id
        if request.method=="POST":
           email=request.form['email']
           amount=request.form['amount']
           payer_id=cust_id
           countryandcode=request.form['currency'].split()
           country=countryandcode[0]
           currency=countryandcode[1]
           email_check=check_customer(email)
           if email_check==1:
            payment_url=request_payment(amount,country,currency,payer_id,email)
            return render_template("request-money-success.html", email=email,amount=amount,currency=currency,payment_url=payment_url)
           else:
            error_message="Email was not found linked with the existing customers" 
            return render_template("request-money.html", error_message=error_message)  
    except KeyError:
        return redirect("/login")
    return render_template("request-money.html")


@app.route('/verification',methods=["GET","POST"])
def verification():
    session['usr']
    all_users = db.child("customers").get()
    for user in all_users.each():
        customer_id=user.key()
        path="customers/"+customer_id+"/Profile/session"
        customer_session=db.child(path).get().val()
        if (customer_session==session['usr']) :
         cust_id=customer_id
    country=db.child("customers/"+cust_id+"/Profile/country").get().val()
    currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()
    a,b=bank_accounts(country,currency)
    if request.method=="POST":
        bankname=request.form['banktype']
        print(bankname)
        for i in range(len(a)):
          if a[i]==bankname:
             banktype=b[i]
        print(banktype)
        db.child("customers/"+cust_id+"/beneficiary").update({"banktype":banktype,"bankname":bankname})
        return redirect("/add_bank_account")
    return render_template("login-3.html",banks=a)

@app.route('/add_bank_account',methods=["GET","POST"])
def add_bank_account():
    session['usr']
    all_users = db.child("customers").get()
    for user in all_users.each():
        customer_id=user.key()
        path="customers/"+customer_id+"/Profile/session"
        customer_session=db.child(path).get().val()
        if (customer_session==session['usr']) :
         cust_id=customer_id
    country=db.child("customers/"+cust_id+"/Profile/country").get().val()
    currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()
    banktype=db.child("customers/"+cust_id+"/beneficiary/banktype").get().val()
    c=bank_account_fields(country,currency,banktype)
    if request.method=="POST":
      b={}
      answer=[]
      f = request.form
      for key in f.keys():
       for value in f.getlist(key):
        #a=dict(key,":",value)
        b[key]=value
        answer.append(value)
      print(b)
      db.child("customers/"+cust_id+"/beneficiary").update(b)
      db.child("customers/"+cust_id+"/beneficiary").update({"identification_type":"identification_id"})
      return redirect("/dashboard")  
    return render_template("add-bank-account.html",fields=c)


    
@app.route('/sendsuccess')
def send_success():
    return render_template("send-money-success.html")

@app.route('/wallet-deposit',methods=["GET","POST"])
def wallet_deposit():
 try:
    session['usr']
    all_users = db.child("customers").get()
    for user in all_users.each():
        customer_id=user.key()
        path="customers/"+customer_id+"/Profile/session"
        customer_session=db.child(path).get().val()
        if (customer_session==session['usr']) :
         cust_id=customer_id
    currency=currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()
    wallet_balance=db.child("customers/"+cust_id+"/wallet/balance").get().val()
    country=db.child("customers/"+cust_id+"/Profile/country").get().val()
    if request.method == "POST":
        amount=request.form['amount']
        payment_url=walletDeposit(amount,country,currency,cust_id)
        return render_template("wallet-money-deposit-confirm.html",amount=amount,currency=currency,payment_url=payment_url)
    return render_template("wallet-money-deposit.html",currency=currency,balance=wallet_balance)
 except KeyError:
     return redirect("/login")

@app.route('/wallet-withdraw',methods=["GET","POST"])
def wallet_withdraw():
  try:
    session['usr']
    all_users = db.child("customers").get()
    for user in all_users.each():
        customer_id=user.key()
        path="customers/"+customer_id+"/Profile/session"
        customer_session=db.child(path).get().val()
        if (customer_session==session['usr']) :
         cust_id=customer_id
         cust_email=db.child("customers/"+cust_id+"/Profile/email").get().val()
    current_balance=db.child("customers/"+cust_id+"/wallet/balance").get().val()
    currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()
    if request.method=="POST":
        currency=db.child("customers/"+cust_id+"/Profile/currency").get().val()
        withdrawing_amount=request.form['amount']
        w_a=int(withdrawing_amount)
        check=checkWithdraw(withdrawing_amount,cust_id)
        if check==1:
         withdraw_money_local_currency(cust_id,w_a)
         return render_template('withdraw-money-success.html',amount=withdrawing_amount,currency=currency)
        else:
         err_msg="Withdrawing Amount Exceeding the Limit"
         return render_template("wallet-money-withdraw.html",current_balance=current_balance,currency=currency,err_msg=err_msg)
    return render_template("wallet-money-withdraw.html",current_balance=current_balance,currency=currency)
  except KeyError:
      return redirect("/login")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

@app.route('/admin')
def administration():
    return render_template('dashboard_company.html')




if __name__ == "__main__":
    app.run(debug=True)

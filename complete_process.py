import firebase_admin
from firebase_admin import db
from create_customer import create_customer
from bank_account_requiredFields import bank_account_fields
from beneficiary import create_new_beneficiary, get_beneficiary_details
from wallet import create_new_wallet, store_money_in_wallet
from send_and_request_payment import send_payment_link
from transaction_by_customer import get_latest_transaction_data
from get_customer_id import get_customerId_by_email
from request_payout import payout
from utilities import make_request

databaseURL = 'https://payment-gateway-f5a88-default-rtdb.asia-southeast1.firebasedatabase.app/'
cred_obj = firebase_admin.credentials.Certificate('payment-gateway-f5a88-firebase-adminsdk-qb5my-ab2fd7c3cb.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})
ref_parent = db.reference('customers')


# Sign Up
def signUp(email, password, name, country_code, phone_number):
    # Phone Number should be with country code
    customer_Id = create_customer(email, name, country_code, phone_number)
    if customer_Id is not None:
        data_tree_profile = {
            customer_Id: {
                'profile': {
                    'name': name,
                    'email': email,
                    'password': password,
                    'phone_number': phone_number,
                    'country': country_code
                }
            }
        }
        ref_parent.update(data_tree_profile)
        return customer_Id


# Login
def login(email, password):
    email_entered_customerId = get_customerId_by_email(email)
    password_of_this_entered_email = ref_parent.child(email_entered_customerId).child('profile').get()['password']
    if password == password_of_this_entered_email:
        name = ref_parent.child(email_entered_customerId).child('profile').get()['name']
        return email_entered_customerId, name
    else:
        return 'Wrong credentials'


# Basic Details
def basic_details(customer_Id):
    profile_details = ref_parent.child(customer_Id).child('profile').get()
    transaction_details = ref_parent.child(customer_Id).child('transactions').get()
    wallet_details = ref_parent.child(customer_Id).child('wallet').get()
    beneficiary_details = ref_parent.child(customer_Id).child('beneficiary').get()
    verification_details = ref_parent.child(customer_Id).child('verification').get()
    return profile_details, transaction_details, wallet_details, beneficiary_details, verification_details


current_customer = 'cus_1234'
profile_details, transaction_details, wallet_details, beneficiary_details, verification_details = basic_details(
    current_customer)


# Verification
def verification(customer_Id):
    data_tree_verification = {
        'verification': {
            'verified': True
        },
    }
    ref_parent.child(customer_Id).update(data_tree_verification)
    return True


# Add bank account
def add_bank_account(country, currency, customer_Id, bank_method_type_selected, answers):
    required_Fields_list = bank_account_fields(country, currency, customer_Id, bank_method_type_selected)
    # After the required fields  is filled. save all the response as a list : requiredFieldsAnswerList    
    a, beneficiary_id = create_new_beneficiary(required_Fields_list, answers)
    if a == 1:
        # Get beneficiary details
        b = get_beneficiary_details(beneficiary_id)
        b['payout_method_type'] = bank_method_type_selected
        data_tree_beneficiary = {
            'beneficiary': b,
        }
        ref_parent.child(customer_Id).update(data_tree_beneficiary)
        print('Successfully added beneficiary and bank account')
    else:
        print('Try again')

def required_field_list(country, currency, customer_Id, bank_method_type_selected):
    required_Fields_list = bank_account_fields(country, currency, customer_Id, bank_method_type_selected)
    return required_Fields_list

    
# Add new wallet
def create_wallet(customer_Id):
    walletId = create_new_wallet(customer_Id)
    data_tree_wallet = {
        'wallet': {
            'wallet_id': walletId,
        }
    }
    ref_parent.child(customer_Id).update(data_tree_wallet)


# Store funds in wallet
def add_funds_to_wallet(customer_Id, walletId, amount_deposited):
    currency_user = profile_details['currency']
    country_user = profile_details['country']
    payment_url = store_money_in_wallet(amount_deposited, country_user, currency_user, customer_Id)

    # After the customer has paid , money comes into company's wallet , storing this data in firebase
    amount_to_be_returned = amount_deposited + (5 / 100) * amount_deposited
    data_tree_wallet_2 = {
        'wallet': {
            'wallet_id': walletId,
            'currency': currency_user,
            'amount_deposited': amount_deposited,
            'time_period_months': 1,
            'amount_to_be_returned': amount_to_be_returned,
            'amount_returned': False
        }
    }
    ref_parent.child(customer_Id).update(data_tree_wallet_2)
    return "Amount added to wallet:" + amount_deposited


# Send Money to someone
def send_money(customer_Id, receiver_email, amount_to_send):
    sender_email = profile_details['email']
    sender_country = profile_details['country']
    sender_currency = profile_details['currency']
    sender_payment_url = send_payment_link(amount_to_send, sender_country, sender_currency, customer_Id)

    def payment_completed(customer_Id):
        t_data, t_id = get_latest_transaction_data(customer_Id)
        response = make_request(method='get', path=f'/v1/payments?limit=1')
        if (response['data'][0]['id'] == t_id) and (response['data'][0]['customer_token'] == customer_Id) and (
                response['data'][0]['paid'] == 'True'):
            save_transaction_data_send_and_payout(customer_Id, receiver_email, sender_email, amount_to_send)
        else:
            return False

    return sender_payment_url, payment_completed
    # Create transaction data for the customer
    # Get transaction data of the customer first


# Request Money from someone
def request_money(customer_Id, sender_email, amount):
    sender_customer_Id = get_customerId_by_email(sender_email)
    profile_details, transaction_details, wallet_details, beneficiary_details, verification_details = basic_details(
        sender_customer_Id)
    sender_country = profile_details['country']
    sender_currency = profile_details['currency']

    sender_payment_url = send_payment_link(amount, sender_country, sender_currency, customer_Id)

    def payment_completed(customer_Id):
        t_data, t_id = get_latest_transaction_data(customer_Id)
        response = make_request(method='get', path=f'/v1/payments?limit=1')
        if (response['data'][0]['id'] == t_id) and (response['data'][0]['customer_token'] == customer_Id) and (
                response['data'][0]['paid'] == 'True'):
            transaction, transaction_id = get_latest_transaction_data(sender_customer_Id)
            transaction['to'] = ref_parent.child(customer_Id).child('profile').get()['email']
            transaction['from'] = sender_email
            transaction['end'] = 'paid'
            data_tree_transactions = {
                'transactions': {
                    transaction_id: {
                        transaction
                    }
                }
            }
            ref_parent.child(sender_customer_Id).update(data_tree_transactions)
            # Set transaction data of receiver

            transaction, transaction_id = get_latest_transaction_data(sender_customer_Id)
            transaction['to'] = ref_parent.child(customer_Id).child('profile').get()['email']
            transaction['from'] = sender_email
            transaction['end'] = 'received'
            data_tree_transaction_receiver = {
                'transactions': {
                    transaction_id: {
                        transaction
                    }
                }
            }
            ref_parent.child(customer_Id).update(data_tree_transaction_receiver)
            # Initiate company's process
            # send payout
            a, b = payout(ref_parent.child(customer_Id).child('profile').get()['email'], amount)
            fx_rate = b
        else:
            return False

    return sender_payment_url, payment_completed


def save_transaction_data_send_and_payout(customer_Id, receiver_email, sender_email, amount):
    transaction, transaction_id = get_latest_transaction_data(customer_Id)
    transaction['to'] = receiver_email
    transaction['from'] = sender_email
    transaction['end'] = 'paid'
    data_tree_transactions = {
        'transactions': {
            transaction_id: {
                transaction
            }
        }
    }
    ref_parent.child(customer_Id).update(data_tree_transactions)
    # Set transaction data of receiver
    receiver_customerId = get_customerId_by_email(receiver_email)
    transaction, transaction_id = get_latest_transaction_data(customer_Id)
    transaction['to'] = receiver_email
    transaction['from'] = sender_email
    transaction['end'] = 'received'

    data_tree_transaction_receiver = {
        'transactions': {
            transaction_id: {
                transaction
            }
        }
    }
    ref_parent.child(receiver_customerId).update(data_tree_transaction_receiver)
    # Initiate company's process
    # send payout
    a, b = payout(receiver_email, amount)
    fx_rate = b
    return "Payment successful"

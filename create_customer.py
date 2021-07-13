

from utilities import make_request


def create_customer(email, name, country_code, phone_number):
    customer = {

        "email": email,
        "invoice_prefix": "JD-",
        "metadata": {
            "merchant_defined": True
        },
        "name": name,
        "phone_number":  country_code+phone_number

    }
    result = make_request(method='post', path='/v1/customers', body=customer)
    if result['status']['status'] == "ERROR":
        return result['status']['error_code']
    else:
        return result['data']['id']  # returns ID of the customer


print(create_customer("abcd@gmail.com", "Choya Tagore", "+91", "8789074044"))

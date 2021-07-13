from utilities import make_request
# customer_id='Cus_2961874e38f5c2853c12f6094673830c'
# print(make_request(method="get", path="/v1/payments?customer=Cus_2961874e38f5c2853c12f6094673830c"))


from pprint import pprint

from utilities import make_request

a = make_request(method="get", path="/v1/payouts/sender/sender_c4657332125d21a92f1e9995b75bdd8f")

b = make_request(method="get",
                 path="/v1/payouts/ca_general_bank/details?sender_country=US&sender_currency=USD&beneficiary_country"
                      "=CA&payout_currency=CAD&sender_entity_type=company&beneficiary_entity_type=individual"
                      "&payout_amount=10")

required_fields=[]
required_field = b['data']["beneficiary_required_fields"]
for i in required_field:
    required_fields.append(i['name'])

#print(required_fields)
country = "CA"
currency= "CAD"
#list_payout_methods_by_countryt = make_request(method="get",
#                                                  path="/payouts/supported_types?beneficiary_country=" + country + "&payout_currency=" + currency + '&category=bank')
#print(list_payout_methods_by_countryt)
#list_payout_methods_by_countryt = make_request(method="get",path="/v1/payouts/supported_types?beneficiary_country="+country+"&payout_currency="+currency+'&category=bank')
#print(list_payout_methods_by_countryt)
#a = make_request(method="get",path="/v1/payouts/supported_types?beneficiary_country=US&payout_currency=USD&category=bank")
#pprint(a)
dict_final = dict()
a = ['fox','cat','dog']
b= ['animal','pon','double']
for i in range(len(a)):
    dict_final.update({a[i]: b[i]})

print(dict_final)





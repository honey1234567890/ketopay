
from pprint import pprint

from utilities import make_request


def create_new_beneficiary(fields_list, fields_answer_list):
    beneficiary = dict()
    if len(fields_list) == len(fields_answer_list):
        for i in range(len(fields_list)):
            beneficiary.update({fields_list[i]: fields_answer_list[i]})

        result = make_request(method='post',
                              path='/v1/payouts/beneficiary',
                              body=beneficiary)
        return 1, result['data']['id']
    else:
        return 'Fields missing'
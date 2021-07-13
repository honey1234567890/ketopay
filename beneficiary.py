from utilities import make_request


def create_new_beneficiar(fields_list, fields_answer_list):
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


def get_beneficiary_details(beneficiary_id):
    results = make_request(method='get', path=f'/v1/payouts/beneficiary/{beneficiary_id}')
    return results['data']

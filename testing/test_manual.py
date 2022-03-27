##############################################################################
# This file performed how the project can be manually tested.
# You can leverage it as a reference for your own test cases.
##############################################################################

# External modules
import json
import random
import sys

# Internal modules
sys.path.append("..")
from static import url_init, url_wallet, url_deposits, url_withdrawals
from util import make_request, generate_customer_xid, generate_reference_id

if __name__ == '__main__':
    print("######################### /api/v1/init ###########################")

    make_request('GET', '/')

    ### Setup request
    # Automatically genearate some customer_xid
    body_1 = generate_customer_xid()
    body_2 = generate_customer_xid()
    body_3 = generate_customer_xid()

    # Case 1: Initialize successfully - POST
    token_1 = json.loads(make_request('POST', url_init, data=body_1))
    token_2 = json.loads(make_request('POST', url_init, data=body_2))
    token_3 = json.loads(make_request('POST', url_init, data=body_3))

    # Case 2: Fail - POST
    # Reason: Existed Token
    make_request('POST', url_init, data=body_1)

    # Case 3: Fail - POST
    # Reason: Missing customer_xid field
    # Mess: "Missing data for required field."
    make_request('POST', url_init)

    # Case 4: Fail - GET
    # Reason: Invalid method
    make_request('GET', url_init, data=body_1) # 405

    print("######################### /api/v1/wallet #########################")

    ### Setup request
    # The header should have a valid token which was returned by /api/v1/init
    header_1 = {
        'Authorization': 'Token ' + token_1["data"]["token"]
    }
    header_2 = {
        'Authorization': 'Token ' + token_2["data"]["token"]
    }
    header_3 = {
        'Authorization': 'Token ' + token_3["data"]["token"]
    }
    header_wrong = {
        'Authorization': 'invalid_token'
    }
    # The request body for method PATCH
    body = {'is_disabled': 'true'}
    body_uper = {'is_disabled': 'True'}
    body_wrong_1 = {'is_disabled': 'wrong_value'}
    body_wrong_2 = {'wrong_key': 'wrong_value'}

    # # Case 1: Enable wallet successfully - POST
    make_request('POST', url_wallet, headers=header_1)
    make_request('POST', url_wallet, headers=header_2)

    # # Case 2: Fail - POST
    # # Reason: This wallet is already enabled before.
    # # Mess: "Already enabled"
    make_request('POST', url_wallet, headers=header_1)

    # # Case 3: Fail - POST
    # # Reason: Invalid token / empty header
    make_request('POST', url_wallet, headers=header_wrong)
    make_request('POST', url_wallet)

    # # Case 4: View wallet successfully - GET
    make_request('GET', url_wallet, headers=header_1)
    make_request('GET', url_wallet, headers=header_2)

    # # Case 5: Fail - GET
    # # Reason: Invalid token / empty header / the wallet is not activate
    make_request('GET', url_wallet, headers=header_wrong)
    make_request('GET', url_wallet)
    make_request('GET', url_wallet, headers=header_3)

    # Case 6: Disable wallet successfully - PATCH
    make_request('PATCH', url_wallet, data=body_uper, headers=header_1)

    # Case 7: Fail - PATCH
    # Reason: Invalid token / empty header / empty body / the wallet is not activated
    make_request('PATCH', url_wallet, data=body, headers=header_wrong)
    make_request('PATCH', url_wallet, data=body)
    make_request('PATCH', url_wallet, headers=header_1)
    make_request('PATCH', url_wallet, data=body, headers=header_1)
    make_request('PATCH', url_wallet, data=body, headers=header_3)
    make_request('PATCH', url_wallet, data=body_wrong_1, headers=header_1)
    make_request('PATCH', url_wallet, data=body_wrong_2, headers=header_1)
    # Only header_2 can return 200 because those other wallets are not activated
    make_request('GET', url_wallet, headers=header_1)
    make_request('GET', url_wallet, headers=header_2) # 200
    make_request('GET', url_wallet, headers=header_3)

    print("######################### /api/v1/wallet/deposits ################")
    print("######################### /api/v1/wallet/withdrawals #############")

    ### Setup request
    # The header should have a valid token which was returned by /api/v1/init
    # enabled wallet = header_2
    # The request body for deposits and withdrawals
    body_wallet_1 = {
        'amount': random.randint(1, 9999999),
        'reference_id' : generate_reference_id()
    }

    body_wallet_2 = {
        'amount': random.randint(1, 9999999),
        'reference_id' : generate_reference_id()
    }
    body_wallet_3 = {
        'amount': random.randint(1, 9999999),
        'reference_id' : generate_reference_id()
    }
    body_wallet_4 = {
        'amount': random.randint(1, 9999999),
        'reference_id' : generate_reference_id()
    }

    # Case 1: Missing any required field
    make_request('POST', url_deposits)
    make_request('POST', url_withdrawals)
    make_request('POST', url_deposits, data=body_wallet_1)
    make_request('POST', url_withdrawals, data=body_wallet_1)
    make_request('POST', url_deposits, headers=header_2)
    make_request('POST', url_withdrawals, headers=header_2)

    make_request('POST', url_wallet, headers=header_1)
    make_request('GET', url_wallet, headers=header_1) # 200
    make_request('GET', url_wallet, headers=header_2) # 200
    make_request('GET', url_wallet, headers=header_3)


    make_request('POST', url_deposits, data=body_wallet_1, headers=header_3) # not activated
    make_request('POST', url_withdrawals, data=body_wallet_2, headers=header_3) # not activated

    make_request('POST', url_deposits, data=body_wallet_1, headers=header_1)
    make_request('POST', url_deposits, data=body_wallet_2, headers=header_1)
    make_request('POST', url_deposits, data=body_wallet_3, headers=header_1)

    make_request('POST', url_withdrawals, data=body_wallet_2, headers=header_1)
    make_request('POST', url_withdrawals, data=body_wallet_2, headers=header_1)
    make_request('POST', url_withdrawals, data=body_wallet_2, headers=header_1)
    make_request('POST', url_withdrawals, data=body_wallet_2, headers=header_1)

    make_request('POST', url_deposits, data=body_wallet_3, headers=header_2)
    make_request('POST', url_deposits, data=body_wallet_4, headers=header_2)
    make_request('POST', url_withdrawals, data=body_wallet_4, headers=header_2)

    make_request('GET', url_wallet, headers=header_1) # 200
    make_request('GET', url_wallet, headers=header_2) # 200
# External modules
from datetime import datetime
from flask import Flask, request
from flask_api import status
from functools import wraps
import hashlib
import uuid

# Internal modules
from decorator import validate_header_decorator, validate_body_decorator
from static import url_init, url_wallet, url_deposits, url_withdrawals
from util import is_enabled_wallet, is_initialized_wallet

app = Flask(__name__)
token_dict = {}
active_wallets = {}

@app.route("/")
def route():
    return "JULO - Your Mini Wallet"

@app.route(url_init, methods=["POST"])
@validate_body_decorator
def api_v1_init():
    # POST Initialize my account for wallet
    rval = {}
    error = ''
    customer_xid = request.form['customer_xid']

    token = hashlib.md5()
    token.update(customer_xid.encode())
    token = token.hexdigest()
    if token in token_dict.keys():
        error = 'Existed Token'
    else:
        token_dict[token] = customer_xid
    if not error:
        rval['status'] = 'success'
        rval['data'] = {'token': token}
        return rval
    else:
        rval['status'] = 'fail'
        rval['data'] = {'error': {'customer_xid': [error]}}
        return rval, status.HTTP_400_BAD_REQUEST

@app.route(url_wallet, methods=["POST"])
@validate_header_decorator
def api_v1_wallet_post():
    # POST Enable my wallet
    rval = {}
    token = request.headers['Authorization'].split()[1]

    if not is_initialized_wallet(token, token_dict):
        rval['status'] = 'fail'
        rval['data'] = {'error': 'This wallet need to be initialized first.'}
        return rval, status.HTTP_400_BAD_REQUEST

    if is_enabled_wallet(token, active_wallets):
        rval['status'] = 'fail'
        rval['data'] = {'error': 'Already enabled'}
        return rval, status.HTTP_400_BAD_REQUEST
    else:
        rval['status'] = 'success'
        wallet = {
            "id": str(uuid.uuid1()),
            "owned_by": token_dict[token],
            "status": "enabled",
            "enabled_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "balance": 0
        }
        active_wallets[token] = wallet
        rval['data'] = {'wallet': wallet}
        print("ACTIVE_WALLETS: " + str(len(active_wallets)))
        # print(active_wallets)
        return rval

@app.route(url_wallet)
@validate_header_decorator
def api_v1_wallet_get():
    # GET View my wallet balance
    rval = {}
    token = request.headers['Authorization'].split()[1]

    if not is_enabled_wallet(token, active_wallets):
        rval['status'] = 'fail'
        rval['data'] = {'error': 'This wallet is not activated.'}
        return rval, status.HTTP_400_BAD_REQUEST
    else:
        rval['status'] = 'success'
        rval['data'] = {'wallet': active_wallets[token]}
        return rval

@app.route('/api/v1/wallet', methods=["PATCH"])
@validate_body_decorator
@validate_header_decorator
def api_v1_wallet_delete():
    # PATCH Disable my wallet
    rval = {}
    error = ''
    token = request.headers['Authorization'].split()[1]
    is_disabled = request.form['is_disabled'].lower()

    if not is_enabled_wallet(token, active_wallets):
        error = 'This wallet is not activated.'
    if is_disabled != 'true':
        error = 'Invalid value %s.' % is_disabled
    if error:
        rval['status'] = 'fail'
        rval['data'] = {'error': error}
        return rval, status.HTTP_400_BAD_REQUEST
    else:
        disabled_wallet = active_wallets[token]
        active_wallets.pop(token)
        rval['status'] = 'success'
        disabled_wallet['status'] = 'disabled'
        disabled_wallet.pop('enabled_at')
        disabled_wallet['disabled_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rval['data'] = {'wallet': disabled_wallet}
        print("ACTIVE_WALLETS: " + str(len(active_wallets)))
        # print(active_wallets)
        return rval


@app.route(url_deposits, methods=["POST"])
@validate_body_decorator
@validate_header_decorator
def api_v1_deposits_post():
    # POST Add virtual money to my wallet
    rval = {}
    token = request.headers['Authorization'].split()[1]
    amount = request.form['amount']
    # reference_id = request.form['reference_id']

    if not is_enabled_wallet(token, active_wallets):
        rval['status'] = 'fail'
        rval['data'] = {'error': 'This wallet is not activated.'}
        return rval, status.HTTP_400_BAD_REQUEST

    active_wallets[token]["balance"] += int(amount)
    deposit = {
        "id": str(uuid.uuid4()),
        "deposited_by": str(uuid.uuid4()),
        "status": "success",
        "deposited_at": datetime.now().strftime('%Y-%m-%d%H:%M:%S'),
        "amount": amount,
        "reference_id": str(uuid.uuid4())
    }
    rval['status'] = 'success'
    rval['data'] = {'deposit': deposit}
    return rval

@app.route(url_withdrawals, methods=["POST"])
@validate_body_decorator
@validate_header_decorator
def api_v1_withdrawals_post():
    # POST Use virtual money from my wallet
    rval = {}
    token = request.headers['Authorization'].split()[1]
    amount = request.form['amount']
    # reference_id = request.form['reference_id']

    if not is_enabled_wallet(token, active_wallets):
        rval['status'] = 'fail'
        rval['data'] = {'error': 'This wallet is not activated.'}
        return rval, status.HTTP_400_BAD_REQUEST

    if active_wallets[token]["balance"] - int(amount) < 0:
        rval['status'] = 'fail'
        rval['data'] = {'error': 'Your balance is smaller than the withdrawal'}
        return rval, status.HTTP_400_BAD_REQUEST

    active_wallets[token]["balance"] -= int(amount)
    withdrawal = {
        "id": str(uuid.uuid4()),
        "withdrawn_by": str(uuid.uuid4()),
        "status": "success",
        "withdrawn_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "amount": amount,
        "reference_id": str(uuid.uuid4())
    }
    rval['status'] = 'success'
    rval['data'] = {'withdrawal': withdrawal}
    return rval

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

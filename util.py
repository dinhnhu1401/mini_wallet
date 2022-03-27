# External modules
from flask_api import status
import requests
import uuid

def render_as_json():
    pass

def validate_field(form, field):
    return '' if form.get(field) else 'Missing data for required field.'

def validate_token(token_raw):
    error = ''
    if token_raw.split()[0] == 'Token' and len(token_raw.split()) == 2:
        token_raw = token_raw.split()[1]
    else:
        error = 'Invalid Format %s' % token_raw
    return [error, token_raw]

def validate_header(header):
    rval = {}
    token = ''
    error = validate_field(header, 'Authorization')
    if not error:
        error, token = validate_token(header.get('Authorization'))
    if error:
        rval['status'] = 'fail'
        rval['data'] = {'error': error}
        return rval, status.HTTP_401_UNAUTHORIZED
    return token

def validate_body(form, body_fields):
    rval = {}
    for f in body_fields:
        error = validate_field(form, f)
        if error:
            rval['status'] = 'fail'
            rval['data'] = {'error': error}
            return rval, status.HTTP_400_BAD_REQUEST
        rval[f] = form.get(f)
    return rval

def is_enabled_wallet(token, active_wallets):
    return True if token in active_wallets.keys() else False

def make_request(method, api, data={}, headers={}):
    url = "http://localhost:5000" + api
    response = requests.request(method=method, url=url, data=data, headers=headers)
    print(method, api, response.status_code, "Body", data, "Header", headers)
    print("Response", response.text)
    return response.text

def generate_customer_xid():
    return {'customer_xid': str(uuid.uuid4())}

def generate_reference_id():
    return str(uuid.uuid4())
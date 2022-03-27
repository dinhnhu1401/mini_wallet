# External modules
from flask import request
from flask_api import status
from functools import wraps

# Internal modules
from util import validate_body, validate_header
from static import api_fields

def validate_header_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        res_head = validate_header(request.headers)
        if len(res_head) != 2:
            return f(*args, **kwargs)
        return res_head
    return wrapper

def validate_body_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # print(request.url_rule, request.method)
        if request.method in ['POST', 'PATCH']:
            if str(request.url_rule) in api_fields.keys():
                res_body = validate_body(request.form, api_fields[str(request.url_rule)])
                if type(res_body) is not tuple:
                    return f(*args, **kwargs)
        return res_body
    return wrapper

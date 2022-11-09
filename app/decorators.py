from functools import wraps
from flask import g, request, redirect, url_for
from os import environ

def free_api_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if key != "FREE":
            return False
        return f(*args, **kwargs)
    return decorated_function

def paid_api_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if key != "PAID":
            return False
        return f(*args, **kwargs)
    return decorated_function

def rapidapi_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rapid_header = request.headers.get("X-RapidAPI-Proxy-Secret")
        if not rapid_header:
            return False
        if rapid_header != os.environ.get("RAPID_PROXY_SECRET"):
            return False
        return f(*args, **kwargs)
    return decorated_function
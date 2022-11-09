import functools
from flask import request
from app.models import User

def limiter(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        api_key = request.headers.get("x-api-key")
        limited = User().check_if_limited(api_key)
        
        if not limited[1]:
            return {
                "title" : "An error occurred",
                "status" : 400,
                "detail": limited[0]
            }, 400

        return f(*args, **kws)
    return decorated_function

def any_key_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        api_key = request.headers.get("x-api-key")
        
        if not api_key:
            return {
                "title" : "An error occurred",
                "status" : 400,
                "detail": "No API Key Provided."
            }, 400
        
        if not User().validate_api_key(api_key):
            return {
                "title" : "An error occurred",
                "status" : 400,
                "detail": "Invalid API Key"
            }, 400
        return f(*args, **kws)
    return decorated_function

def premium_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        api_key = request.headers.get("x-api-key")
        
        if not api_key:
            return {
                "title" : "An error occurred",
                "status" : 400,
                "detail": "No API Key Provided."
            }, 400

        validate_premium = User().validate_premium_api_key(api_key)
        
        if not validate_premium[1]:
            if "error" not in validate_premium[0]:
                return {
                    "title" : "An error occurred",
                    "status" : 400,
                    "detail": "Invalid API Key"
                }, 400
            else:
                return {
                    "title" : "An error occurred",
                    "status" : 400,
                    "detail": validate_premium[0]["error"]
                }, 400
            
        return f(*args, **kws)
    return decorated_function
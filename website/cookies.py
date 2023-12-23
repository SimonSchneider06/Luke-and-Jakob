from flask import current_app as app
from flask import request

def cookies_asked():
    '''
        Check if cookies have already a value assigned
    '''
    value = request.cookies.get("cookie_consent")
    if value == "true" or value == "false":
        return True
    else:
        return False
    
def cookies_allowed():
    '''
        Check if cookies are allowed
    '''
    value = request.cookies.get("cookie_consent")
    return value == "true"
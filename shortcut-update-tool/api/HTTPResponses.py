from flask import Response
import json

def add_access_control(resp):
    # adds the correct access control to a given response
    # in our case we just always want all
    resp.headers['Access-Control-Allow-Origin'] = '*'

def make_json_response( resp_dict:dict, status=200):
    # receives a dictionary and crafts the Flask JSON response object for it
    resp = Response(
        response=json.dumps(resp_dict), status=status, mimetype="text/plain"
    )

    # add_access_control(resp)
    resp.headers['Content-type'] = 'application/json'
    return resp

def error_response(status:int, message:str=None, error_json=None):
    # crafts an erroneous message with the status and returns it
    
    if message is not None:
        content = { 'message': message }

    elif error_json is not None:
        content = error_json

    else:
        raise Exception('No content provided')

    resp = Response(
        response=json.dumps(content), status=status, mimetype="text/plain"
    )

    # resp.headers['Access-Control-Allow-Origin'] = '*'
    if error_json is not None: resp.headers['Content-type'] = 'application/json'
    return resp

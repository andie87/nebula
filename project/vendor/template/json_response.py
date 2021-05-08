""" Template Response. """
from time import time
from collections import OrderedDict
from http import HTTPStatus

def render_response(result, process_time=time(), request_body={}, total_records=0, status=200):
    """ render_response: for rendering response. """
    response = OrderedDict()
    response['response_code'] = status
    response['response_message'] = "success" if status == 200 else ""
    response['response_version'] = "1"
    response['data'] = result
    
    return response

def render_error_response(error_message, process_time=time(), request_body={}, status="OV00001"):
    """ render_error_response: for rendering error response."""
    response = OrderedDict()
    response['response_code'] = status
    response['response_message'] = error_message
    response['response_version'] = "1"
    response['data'] = OrderedDict()
    response['data']['is_error'] = True
    response['data']['error_message'] = error_message

    return response

#  new success and error response convention
def render_api_success_response(result, process_time=time(), request_body={}, total_records=0, status=200):
    """ render_response: for rendering response. """
    response = OrderedDict()
    response['response_code'] = status
    response['response_message'] = "success"
    response['response_version'] = "1"
    response['data'] = result
    return response

def render_api_error_response(error_message="", error_list=[], process_time=time(), request_body={}, status=400):

    """ render_error_response: for rendering error response."""
    response = OrderedDict()
    response['response_code'] = status
    response['response_message'] = error_message
    response['response_version'] = "1"
    response['data'] = OrderedDict()
    response['data']['status'] = status
    response['data']['detail'] = error_list
    response['data']['process_time'] = process_time

    return response

#  new success and error response convention
def render_api_dashboard_success_response(result, process_time=time(), request_body={}, total_records=0, status=200):
    """ render_response: for rendering response. """
    response = OrderedDict()
    response['response_code'] = status
    response['response_message'] = "success" if status == 200 else ""
    response['response_version'] = "1"
    response['data'] = result
    return response

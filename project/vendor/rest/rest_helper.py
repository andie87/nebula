import json
import requests
from http import HTTPStatus
import time
from vendor import datadog

from django.conf import settings

class RestHelper(object):
    __default_users = []
    __default_message_id = 0
    __timeout_message = "there was timeout when connecting to Campaign Tracker API"


    def __init__(self, **config):
        """ __init__ : initializing mailerlite instance. """
        pass

    def send_request(self, method, url, payload, vendor_name, header={}, auth="" ):
        """used to send message to campaign tracker"""
        print(url)
        start_time = time.time()
        status = False
        
        # some header that passing by executor is NONE 
        if header:
            headers = header
        else : 
            headers = {}
            
        headers['Content-Type'] = 'application/json'
        if method.lower() == "get":
            headers = {}
            if payload:
                payload = json.dumps(payload)
            
        else:
            payload = json.dumps(payload)

        try:
            retry_state = True
            trial_count = 0
            while retry_state:
                
                if auth:
                    response = requests.request(method, url, data=payload, headers=headers, auth=auth, verify=False, timeout=settings.TIMEOUT_LIMIT)
                else:
                    response = requests.request(method, url, headers=headers, data=payload,  verify=False, timeout=settings.TIMEOUT_LIMIT)
                       
                # if httpcode related please do immidiate retry
                

                print(response.status_code)
                if response.status_code in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]:
                    retry_state = False
                else:
                    
                    trial_count += 1
                    time.sleep(5)
                    if trial_count >= 3:
                        retry_state = False
                
                print("trial count {}".format(trial_count))
                datadog.write_vendor_event( vendor_name, response.status_code, start_time=start_time, error="")
            
            if response.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]:
                msg = 'Error HTTP Code : {}. Detail : {}'.format(response.status_code, response.text)
                return False, msg
            
            # if response.status_code in [HTTPStatus.NO_CONTENT]:
            #     datadog.write_vendor_event( vendor_name, response.status_code, start_time=start_time, error="NO CONTENT")
            #     return True, ''
            
            datadog.write_vendor_event(vendor_name, response.status_code, start_time=start_time, error="")
            return True, response.json()

        # if exception as agreement use global retry
        except requests.exceptions.Timeout:
            datadog.write_vendor_event( vendor_name, 504, start_time=start_time, error="TIME OUT")
            return status, self.__timeout_message
        except requests.exceptions.ConnectionError as err:
            datadog.write_vendor_event( vendor_name, 503, start_time=start_time, error="CONNECTION ERROR")
            return status, err
        except requests.exceptions.RequestException as err:
            datadog.write_vendor_event( vendor_name, 500, start_time=start_time, error=str(err))
            return status, err
        except requests.exceptions.HTTPError as err:
            datadog.write_vendor_event( vendor_name, 500, start_time=start_time, error=str(err))
            return status, err
        except Exception as err:
            datadog.write_vendor_event( vendor_name, 500, start_time=start_time, error=str(err))
            return status, err

  

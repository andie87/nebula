# -*- coding: utf-8 -*-
import json
import datetime
import time
import pytz

from django.conf import  settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Api
from vendor.template import json_response
from vendor.logger.logger import AccessLogMiddleware

class gateway(APIView):
    authentication_classes = ()

    logger = AccessLogMiddleware()

    def operation(self, request):
        time_log = datetime.datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%dT%H:%M:%S")
        start_time = (time.time())
        path = request.path_info.split('/')
        if len(path) < 2:
            resp = json_response.render_api_error_response("bad url request", error_list=[],
                                                           process_time=(time.time() - start_time),
                                                           request_body={},
                                                           status=400)

            self.logger.logging(user="", path=request.get_full_path(), service_name="", time_stamp=time_log,
                                response_time=(time.time() - start_time),
                                request_body=(json.loads(request.body)) if request.method.lower() != 'get' else "",
                                response=resp, status_code=400)

            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        
        apimodel = Api.objects.filter(name=path[2])
        if apimodel.count() != 1:
            resp = json_response.render_api_error_response("wrong API Gateway config", error_list=[],
                                                           process_time=(time.time() - start_time),
                                                           request_body={},
                                                           status=400)
            # logger
            self.logger.logging(user="", path=request.get_full_path(), service_name=path[2], time_stamp=time_log,
                                response_time=(time.time() - start_time),
                                request_body=(json.loads(request.body)) if request.method.lower() != 'get' else "",
                                response=resp, status_code=400)

            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        valid, msg, username = apimodel[0].check_plugin(request)
        if not valid:
            resp = json_response.render_api_error_response(msg, error_list=[],
                                                           process_time=(time.time() - start_time),
                                                           request_body={},
                                                           status=403)
            # logger
            self.logger.logging(user=username, path=request.get_full_path(), service_name=path[2], time_stamp=time_log,
                                response_time=(time.time() - start_time),
                                request_body=(json.loads(request.body)) if request.method.lower() != 'get' else "",
                                response=resp, status_code=403)

            return Response(resp, status=status.HTTP_403_FORBIDDEN)

        # go to resource
        res = apimodel[0].send_request(request)
        if res.headers.get('Content-Type', '').lower().startswith('application/json'):
            data = json.dumps(request.data)
        else:
            data = res.content


        #logger
        self.logger.logging(user=username, path=request.get_full_path(), service_name=path[2], time_stamp=time_log,
                            response_time=(time.time() - start_time), request_body= request.data if res.headers.get('Content-Type', '').lower() == 'application/json' else "",
                            response=data, status_code=res.status_code)

        return Response(data=data, status=res.status_code)
    
    def get(self, request):
        return self.operation(request)

    def post(self, request):
        return self.operation(request)

    def put(self, request):
        return self.operation(request)
    
    def patch(self, request):
        return self.operation(request)
    
    def delete(self, request):
        return self.operation(request)

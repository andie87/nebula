from collections import OrderedDict
from rest_framework.decorators import api_view
from vendor.template import json_response
from rest_framework.response import Response


@api_view(['GET'])
def ping(request):
    """ index: sample index page."""
    data = OrderedDict()
    data['message'] = "I'm alive !!"
    data['status'] = "OK"

    resp = json_response.render_response(data)
    return Response(resp)
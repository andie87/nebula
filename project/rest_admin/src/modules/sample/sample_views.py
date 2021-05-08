""" Sample Views. """
from collections import OrderedDict
from time import time

from rest_framework import status
from rest_framework.response import Response

from vendor.template import json_response

from .sample_models import Sample

def index(request):
    """ index: sample index page."""
    start_time = time()
    data = Sample.objects.all()
    if data:
        result = (OrderedDict(
            id=value.id,
            type='brands',
            attributes=OrderedDict(
                name=value.name,
                age=value.age,
                email=value.email,
                about=value.about,
            )
        ) for value in data)
    else:
        result = []
    
    resp = json_response.render_response(result, start_time)
    return Response(resp, status=status.HTTP_200_OK)

def new(request):
    """ new: new sample. """
    return None

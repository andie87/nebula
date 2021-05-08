from datadog import statsd
from django.conf import settings
import os
import time


def write_vendor_event( vendor_name, http_code, start_time=0, error="", path=""):
    elapse_time = time.time() - start_time
    env = os.environ['DJANGO_ENV']

    statsd.gauge(f"anl.api_resources.{vendor_name}.vendor.gauge", elapse_time,
                tags=["env:{}".format(env), 
                "group:Big-Data-auth-user-management",
                "http_code:{}".format(http_code),
                "path:{}".format(path),
                "error:{}".format(error),
            ])

    statsd.increment(f"anl.api_resources.{vendor_name}.vendor",
                tags=["env:{}".format(env), 
                "group:Big-Data-auth-user-management",
                "http_code:{}".format(http_code),
                "channel:{}".format(path),
                "error:{}".format(error),
            ])
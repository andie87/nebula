from rest_framework import throttling

class GatewayRateThrottle(throttling.SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'gateway'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        elif 'HTTP_AUTHORIZATION' in request.META:
            ident = request.META['HTTP_AUTHORIZATION']
        elif 'HTTP_SIGNATURE' in request.META:
            ident = request.META['HTTP_SIGNATURE']
        elif 'HTTP_APIKEY' in request.META:
            ident = request.META['HTTP_APIKEY']
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

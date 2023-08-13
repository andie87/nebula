import redis
import pickle
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import get_authorization_header, BasicAuthentication


class CacheBasicAuthentication(BasicAuthentication):
    def __init__(self):
        if settings.REDIS_PASSWORD:
            self.redis_ins = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,
                                               password=settings.REDIS_PASSWORD)
        else:
            self.redis_ins = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        auth = get_authorization_header(request).split()

        key_redis = f'apigateway:user:basic-auth:{userid}{(auth[1]).decode("utf-8")}'
        user = self.redis_ins.get(key_redis)

        if user:
            user = pickle.loads(user)
            return user, None

        if not user:
            credentials = {
                get_user_model().USERNAME_FIELD: userid,
                'password': password
            }
            user = authenticate(request=request, **credentials)

            if user is None:
                raise exceptions.AuthenticationFailed(('Invalid username/password.'))

            if not user.is_active:
                raise exceptions.AuthenticationFailed(('User inactive or deleted.'))

            # self.set(key_cache, user, 300)
            self.redis_ins.set(key_redis, pickle.dumps(user), ex=3600)
            return user, None



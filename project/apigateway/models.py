# -*- coding: utf-8 -*-
import requests, json
import secrets
import time
import hmac, hashlib, base64
import random, string, re
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import get_authorization_header, BasicAuthentication
from .auth import CacheBasicAuthentication
from django.conf import  settings

def alphanumerica_and_space_only(value):
    valid = re.match(r'^[a-zA-Z\d\-_\s]+$', value) is not None
    if not valid:
        raise ValidationError("only alphabets , numeric, dash ( - ) and space are allowed")


# Create your models here.
class Consumer(models.Model):

    def generate_key():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

    def generate_secret():
        return secrets.token_urlsafe(32)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=64, default=generate_key)
    secretkey = models.CharField(max_length=256, default=generate_secret)
    description = models.TextField(blank=True, null=True)
    created_by =  models.ForeignKey( User,
        verbose_name="Created By user ID",
        on_delete=models.SET_NULL,
        related_name="created_by_user_id",
        db_column='created_by', blank=True, null=True
    )

    modified_by =  models.ForeignKey( User,
        verbose_name="Modified By user ID",
        on_delete=models.SET_NULL,
        related_name="modified_by_user_id",
        db_column='modified_by', blank=True, null=True
    )

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

class Api(models.Model):
    PLUGIN_CHOICE_LIST  = (
        (0, _('Passthrough')),
        (1, _('Basic auth')),
        (2, _('Key auth')),
        (3, _('Server auth')),
        (4, _('HMAC')),
    )
    name = models.CharField(max_length=128, unique=True, validators=[alphanumerica_and_space_only])
    request_path = models.CharField(max_length=255, editable=False)
    upstream_url = models.CharField(max_length=255)
    plugin = models.IntegerField(choices=PLUGIN_CHOICE_LIST, default=0)
    consumers = models.ManyToManyField(Consumer, blank=True)
    description = models.TextField(blank=True, null=True)
    created_by =  models.ForeignKey( User,
        verbose_name="Created By API user ID",
        on_delete=models.SET_NULL,
        related_name="created_by_api_user_id",
        db_column='created_by', blank=True, null=True
    )

    modified_by =  models.ForeignKey( User,
        verbose_name="Modified By API user ID",
        on_delete=models.SET_NULL,
        related_name="modified_by_api_user_id",
        db_column='modified_by', blank=True, null=True
    )
    
    @property
    def exposed_url(self):
        return "{}/service{}/".format(settings.DEFAULT_REDIRECT_URL, self.request_path)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().replace(" ","-")
        self.request_path = f"/{self.name}"
        super(Api, self).save(*args, **kwargs)


    def check_plugin(self, request):
        if self.plugin == 0:
            return True, '', ''
            
        elif self.plugin == 1:
            try:
                #print((request.body))

                auth = get_authorization_header(request).split()
                if not auth or auth[0].lower() != b'basic':
                    raise ValueError('Invalid basic header. No credentials provided.')

                if len(auth) == 1:
                    raise ValueError('Invalid basic header. No credentials provided.')


            except Exception as err:
                return False, str(err), ""
            #auth = BasicAuthentication()

            auth = CacheBasicAuthentication()
            try:
                user, password = auth.authenticate(request)
            except Exception as err:
                return False, f'Authentication credentials were not provided {str(err)}', ''

            if self.consumers.filter(user=user):
                return True, '', user.username
            else:
                return False, 'permission not allowed', user.username if user else ""

        elif self.plugin == 2:
            apikey = request.META.get('HTTP_APIKEY')
            consumers = self.consumers.all()
            for consumer in consumers:
                if apikey == consumer.apikey:
                    return True, '', consumer.user.username
            return False, 'apikey need', ''

        elif self.plugin == 3:
            consumer = self.consumers.all()
            if not consumer:
                return False, 'consumer need', ""
            request.META['HTTP_AUTHORIZATION'] = requests.auth._basic_auth_str(consumer[0].user.username, consumer[0].apikey)
            return True, '', consumer[0].user.username

        elif self.plugin == 4:
            consumers = self.consumers.all()
            server_timestamp = int(time.time())

            try:
                apikey = request.META.get('HTTP_APIKEY')
                path = request.get_full_path().split('?')[0]
                request_time = request.META.get('HTTP_TIME')
                method  = request.method
                body = ""
                hmac = request.META.get('HTTP_SIGNATURE')
                if method != 'GET':
                    a_list = request.body.decode('utf-8').split()
                    new_string = "".join(a_list)
                    body = new_string

                delta_time = int(request_time) - server_timestamp
                if delta_time > 60:
                    return False, 'signature expired', ""

            except Exception as err:
                return False, 'wrong header', ''



            if not consumers:
                return False, 'consumer need', ""

            for consumer in consumers:
                if apikey == consumer.apikey:
                    status , msg = self.validate_hmac(path, method, request_time, body, consumer.secretkey,hmac )
                    if not status:
                        return False, 'invalid Hmac', consumer.user.username
                    return True, '', consumer.user.username
            return False, 'invalid apikey', ''

        else:
            raise NotImplementedError("plugin %d not implemented" % self.plugin)

    def validate_hmac(self, path, method, time, body, secret, incoming_signature):
        try:
            data = ("%s%s%s%s" % (path, method, time, body)).encode()
            token = secret.encode()
            signature = base64.b64encode(hmac.new(token, data, digestmod=hashlib.sha256).digest()).decode()
            if signature == incoming_signature:
                return True, "valid Hmac"

        except Exception as e:
            print(e)
            return False, str(e)
        return False, "invalid hmac"


    def send_request(self, request):
        headers = {}
        if self.plugin != 1 and request.META.get('HTTP_AUTHORIZATION'):
            headers['authorization'] = request.META.get('HTTP_AUTHORIZATION')
        # headers['content-type'] = request.content_type

        strip = '/service' + self.request_path
        full_path = request.get_full_path()[len(strip):]
        url = self.upstream_url + full_path

        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }

        for k,v in request.FILES.items():
            request.data.pop(k)
        
        if request.content_type and request.content_type.lower()=='application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type
        else:
            data = request.data

        return method_map[method](url, headers=headers, data=data, files=request.FILES, verify=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
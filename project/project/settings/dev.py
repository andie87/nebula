"""
Django settings for project staging.



Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from .base import *
import os

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'api_management',
        'USER': 'app_apimgmt',
        'PASSWORD': 'app_APIMGMT@123#',
        'HOST': 'ec2-54-255-145-17.ap-southeast-1.compute.amazonaws.com',
        'PORT': '3306',
    }
}

DEBUG = True

ASSET_ROOT = os.path.join(os.path.dirname(BASE_DIR), "project/assets")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:30001/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

BROKER_KAFKA = 'localhost:9092'
TOPIC_KAFKA = ["API_GATEWAY_LOG"]


CONFLUENT_KAFKA_PRODUCER = {"bootstrap.servers": BROKER_KAFKA,
                            "retries": "5"}

KAFKA_PRODUCER = Producer(CONFLUENT_KAFKA_PRODUCER)


REDIS_HOST = 'localhost'
REDIS_PASSWORD = None
REDIS_PORT = 6379


CONFLUENT_KAFKA_CONSUMER = {"bootstrap.servers": BROKER_KAFKA,\
                            "group.id": "apigwlistener",\
                            "enable.auto.commit": True,\
                            "session.timeout.ms": 6000,\
                            "default.topic.config": {"auto.offset.reset": "smallest"}\
                            }

INDEX_NAME = 'apigw_log'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',
        'user': '5/minute',
        'gateway': '{}/minute'.format(os.environ.get('RATE_LIMIT', '100'))
    }
}

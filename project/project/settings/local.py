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
        'NAME': 'api_gateway',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



DEBUG = True

ASSET_ROOT = os.path.join(os.path.dirname(BASE_DIR), "project/assets")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

PORT = 7051

ENV = 'local'

BROKER_KAFKA = 'localhost:9092'
#TOPIC_KAFKA = "API_GATEWAY_LOG"


CONFLUENT_KAFKA_PRODUCER = {"bootstrap.servers": BROKER_KAFKA,
                            "retries": "5"}

KAFKA_PRODUCER = Producer(CONFLUENT_KAFKA_PRODUCER)


REDIS_HOST = 'localhost'
REDIS_PASSWORD = None

BROKER_KAFKA = 'localhost:9092'
TOPIC_KAFKA = ["API_GATEWAY_LOG"]


CONFLUENT_KAFKA_CONSUMER = {"bootstrap.servers": BROKER_KAFKA,\
                            "group.id": "apigwlistener",\
                            "enable.auto.commit": True,\
                            "session.timeout.ms": 6000,\
                            "default.topic.config": {"auto.offset.reset": "smallest"}\
                            }

INDEX_NAME = 'apigw_log'





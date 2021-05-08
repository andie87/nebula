"""
Django settings for project staging.
created by derta isyajora rakhman
date :  7 October 2020
email : derta.isyajora@ovo.id

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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
        # 'NAME': 'fsmp_auth_user_mgmt',
        # 'USER': 'postgres',
        # 'PASSWORD': 'qazwer123',
        # 'HOST': '34.101.83.119',
        # 'PORT': '5432',
    }
}

DEBUG = True

ASSET_ROOT = os.path.join(os.path.dirname(BASE_DIR), "project/assets")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'TIMEOUT': None,
        'LOCATION': [
            'localhost:11211'
        ]
    }
}

REDIS_HOST = os.environ.get('REDIS_HOST', '')
# REDIS_HOST = '10.10.189.219'
REDIS_PASSWORD = None

PORT = 7051

ENV = 'staging'

WEBVIEW_AUTH = HTTPBasicAuth(
    'webview',
    'qazwer123'
)

print(ENV)

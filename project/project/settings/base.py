import os
from vendor.kafka.helper import Producer

#from datadog import initialize, statsd

###############################################################
# start intialize datadog for all service
# statsd_host: < DATA DOG PROXY >
# statsd_hosL < DATA DOG PORT > DEFAULT 8125
##############################################################

# options = {
#     'statsd_host':'10.30.216.101',
#     'statsd_port':8125
# }
# initialize(**options)


# Build paths  inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
#ENV = os.environ.get('DJANGO_ENV', 'development')
#LOADER = '{0}.{1}'.format('loader', ENV)
#CONF = __import__(LOADER, globals(), locals(), [ENV], 1)

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'd11_nasa(%4q$b0^d*4lel+7r9xvg0b@5__x05%#cx@9-9)sg@'
SECRET_KEY = 'nebula_Develop3r123_Dev!!!'

# TEST TRIGGER ##

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'apigateway.apps.RestApiGatewayConfig',
    'rest_framework',
    'rest_admin.apps.RestAdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notifications',
    'django_extensions',
    'polymorphic'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

ROOT_URLCONF = 'project.urls'

X_FRAME_OPTIONS = 'ALLOWALL'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
#            os.path.join(BASE_DIR, '../templates'),
            os.path.join(BASE_DIR, '../rest_api/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Kinetica
# https://www.kinetica.com/docs/6.1/tutorials/python_guide.html
# https://www.kinetica.com/docs/6.1/api/python/index.html




# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ACCESS_LOG_PATH = os.path.join(os.path.dirname(BASE_DIR), "project/accesslog")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        "json": {
            '()': 'json_log_formatter.JSONFormatter',
        },
        'debugging': {
            'format': "[{asctime}] [{levelname}] {message}",
            'datefmt': "%Y-%m-%d %H:%M:%S %z",
            'style': "{"
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/access.accesslog'.format(ACCESS_LOG_PATH),
            'formatter' : 'json',
            'when': 'midnight', # daily, you can use 'midnight' as well
            'interval' : 1,
            'backupCount': 100, # 100 days backup
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'debugging',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'GriffinLog': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'debugging.logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIMEOUT_LIMIT = 100


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATICFILES_DIRS = [
    #os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "/static"),
    os.path.join(BASE_DIR, "static"),
    #os.path.join(BASE_DIR, "/www/static")
]

ASSETS_FOLDER = os.path.join(os.path.dirname(BASE_DIR),"project/assets")

LOG_FOLDER = os.path.join(os.path.dirname(BASE_DIR),"log")

FILE_ROOT = os.path.join(BASE_DIR, "temp")

ASSET_ROOT = os.path.join(BASE_DIR, "assets")
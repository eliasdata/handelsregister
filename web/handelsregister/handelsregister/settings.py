"""
Django settings for handelsregister project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
import re
import sys

from authorization_django import levels as authorization_levels


def get_docker_host():
    """
    Looks for the DOCKER_HOST environment variable to find the VM
    running docker-machine.

    If the environment variable is not found, it is assumed that
    you're running docker on localhost.
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'


# noinspection PyBroadException
def in_docker():
    """
    Checks pid 1 cgroup settings to check with reasonable certainty we're in a
    docker env.
    :return: true when running in a docker container, false otherwise
    """
    try:
        return ':/docker/' in open('/proc/1/cgroup', 'r').read()
    except:
        return False


OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

OVERRIDE_EL_HOST_VAR = 'ELASTIC_HOST_OVERRIDE'
OVERRIDE_EL_PORT_VAR = 'ELASTIC_PORT_OVERRIDE'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LocationKey:
    local = 'local'
    docker = 'docker'
    override = 'override'


def get_database_key():
    if os.getenv(OVERRIDE_HOST_ENV_VAR):
        return LocationKey.override
    elif in_docker():
        return LocationKey.docker

    return LocationKey.local


DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'handelsregister'),
        'USER': os.getenv('DATABASE_USER', 'handelsregister'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432',
        'CONN_MAX_AGE': 5,
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'handelsregister'),
        'USER': os.getenv('DATABASE_USER', 'handelsregister'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5406',
        'CONN_MAX_AGE': 5,
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'handelsregister'),
        'USER': os.getenv('DATABASE_USER', 'handelsregister'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432'),
        'CONN_MAX_AGE': 5,
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

VBO_URI = "https://api.data.amsterdam.nl/bag/verblijfsobject/"

# SECURITY WARNING: keep the secret key used in production secret!
insecure_key = 'insecure'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', insecure_key)
DEBUG = SECRET_KEY == insecure_key

ALLOWED_HOSTS = ['*']

PARTIAL_IMPORT = {
    'numerator': 0,
    'denominator': 1,
}

PROJECT_APPS = [
    'handelsregister',
    'datasets.kvkdump',
    'datasets.hr',
    'datasets.sbicodes',
    'geo_views',
]

DATAPUNT_API_URL = os.getenv(
    # note the ending /
    'DATAPUNT_API_URL', 'https://api.data.amsterdam.nl/')


# Application definition
INSTALLED_APPS = PROJECT_APPS + [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django_filters',

    'django_extensions',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_swagger',

]

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')

MIDDLEWARE = [
    'authorization_django.authorization_middleware',
]

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',)


ROOT_URLCONF = 'handelsregister.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'handelsregister.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DUMP_DIR = 'mks-dump'

ELK_PORT = os.getenv(OVERRIDE_EL_PORT_VAR, '9200')

ELASTIC_OPTIONS = {
    LocationKey.docker: ["http://elasticsearch:9200"],
    LocationKey.local: [f"http://{get_docker_host()}:9200"],
    LocationKey.override: [
        f"http://{os.getenv(OVERRIDE_EL_HOST_VAR)}:{ELK_PORT}"],    # noqa
}
ELASTIC_SEARCH_HOSTS = ELASTIC_OPTIONS[get_database_key()]

ELASTIC_INDICES = {
    'HR': 'handelsregister',
}

PARTIAL_IMPORT = {
    'numerator': 0,
    'denominator': 1,
}

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING:
    for k, v in ELASTIC_INDICES.items():
        ELASTIC_INDICES[k] += 'test'

BATCH_SETTINGS = dict(
    batch_size=4000
)

REST_FRAMEWORK = dict(
    PAGE_SIZE=100,

    UNAUTHENTICATED_USER={},
    UNAUTHENTICATED_TOKEN={},

    MAX_PAGINATE_BY=100,
    DEFAULT_AUTHENTICATION_CLASSES=(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    DEFAULT_PAGINATION_CLASS='drf_hal_json.pagination.HalPageNumberPagination',
    DEFAULT_PARSER_CLASSES=('drf_hal_json.parsers.JsonHalParser',),
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    DEFAULT_FILTER_BACKENDS=(
        'rest_framework.filters.DjangoFilterBackend',
        # 'rest_framework.filters.OrderingFilter',

    ),
    COERCE_DECIMAL_TO_STRING=True,
)

# SWAGGER

swag_path = 'https://acc.api.data.amsterdam.nl/handelsregister/docs'

if DEBUG:
    swag_path = '127.0.0.1:8000/handelsregister/docs'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',

    'enabled_methods': [
        'get',
    ],

    'api_key': '',
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,

    'is_authenticated': False,
    'is_superuser': False,

    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,

    'protocol': 'https' if not DEBUG else '',
    'base_path': swag_path,

    'info': {
        'contact': 'atlas.basisinformatie@amsterdam.nl',
        'description': 'This is the Handelsregister API server.',
        'license': 'Not known yet',
        'licenseUrl': '://www.amsterdam.nl/stelselpedia/',
        'termsOfServiceUrl': 'https://data.amsterdam.nl/terms/',
        'title': 'Handelsregister',
    },

    'doc_expansion': 'list',

    'SECURITY_DEFINITIONS': {
        'oauth2': {
            'type': 'oauth2',
            'authorizationUrl': DATAPUNT_API_URL + "oauth2/authorize",
            'flow': 'implicit',
            'scopes': {
                authorization_levels.SCOPE_HR_R: "Toegang HR",
            }
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/static/'

HEALTH_MODEL = 'hr.MaatschappelijkeActiviteit'

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', '127.0.0.1')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_GELF_UDP_PORT', 12201))



# Security
DATAPUNT_AUTHZ = {
    'JWT_SECRET_KEY': os.getenv(
        'JWT_SHARED_SECRET_KEY', 'insecureeeeeeeeeeeeeee'),
    'JWT_ALGORITHM': 'HS256',
    'MIN_SCOPE': authorization_levels.SCOPE_HR_R,
    'FORCED_ANONYMOUS_ROUTES': ('/status/', '/handelsregister/docs/')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },

        'graypy': {
            'level': 'ERROR',
            'class': 'graypy.GELFHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT,
        },

    },

    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'graypy'],
    },

    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },

        # Debug all batch jobs
        'doc': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'index': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },

        'search': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'elasticsearch': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'urllib3': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'factory.containers': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        'factory.generate': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        'requests.packages.urllib3.connectionpool': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Log all unhandled exceptions
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

    },
}

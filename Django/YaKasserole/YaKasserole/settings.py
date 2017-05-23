"""
Django settings for YaKasserole project.

Generated by 'django-admin startproject' using Django 2.0.dev20170311172729.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7$&$ym162b#@_403*dy+by5&%13ctg3k$ron$3c0^5mgv)(_d4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/'
#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
#EMAIL_HOST = 'mail.example.com'
#EMAIL_PORT = 465

#Secure website
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#paiement sécurisé
PAYMENT_HOST = 'localhost:8080'
PAYMENT_USES_SSL = False
PAYMENT_MODEL = 'comptes.Payment'
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {'capture': False})}

# Application definition

INSTALLED_APPS = [
    'atelier.apps.AtelierConfig',
    'community.apps.CommunityConfig',
    'recette.apps.RecetteConfig',
    'comptes.apps.ComptesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # active https
    'djangosecure',
    'sslserver',
    #paiement sécurisé
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = [
    # active https
    'djangosecure.middleware.SecurityMiddleware',
        ]

ROOT_URLCONF = 'YaKasserole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TIME_INPUT_FORMATS = [
    '%H:%M:%S',
    '%H:%M',
    '%M',
]

WSGI_APPLICATION = 'YaKasserole.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yakasserole',
        'USER': 'django_root',
        'PASSWORD': 'h&-e_né4&à73à_e238dè*ù:;',
        'HOST': '/tmp',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '../static')]

MEDIA_ROOT = os.path.join(BASE_DIR, '../pictures')

# FormSetFactories require this for the django multiple formset plugin

AJAX_LOOKUP_CHANNELS = {
    'recette': {
        'model' : 'recette.Etape'
    }
}

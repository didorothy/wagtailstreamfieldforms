from os import environ
import os.path

from django.urls import reverse_lazy

SITE_DIR = os.path.dirname(os.path.abspath(__file__))


# Security

SECRET_KEY = environ.get('SECRET_KEY', '')

DEBUG = True

ALLOWED_HOSTS = [] + environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # wagtail
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.styleguide',

    'modelcluster',
    'taggit',

    # app specific
    'example',
    'wagtailstreamfieldforms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_DIR, 'db.sqlite3'),
    }
}


# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'Django <no_reply@example.com>'
#EMAIL_HOST = environ.get('EMAIL_HOST')
#EMAIL_PORT = environ.get('EMAIL_PORT')
#EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
#EMAIL_USE_TLS = False
#EMAIL_USE_SSL = False


# Authentication

AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = reverse_lazy('admin:login')
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'


# Internationalization

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    os.path.join(SITE_DIR, "static"),
]
STATIC_URL = "/static/"
MEDIA_URL = "/media/"


# Wagtail

WAGTAIL_SITE_NAME = 'example.com'

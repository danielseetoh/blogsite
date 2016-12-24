"""
Django settings for Blogsite project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7z3v+umx3#oxbkmuq%iu%*1t6p1_)rmng=fensi(%#t@kvkx++'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# changed to allow heroku to access
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Blogsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Blogsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    # Sensitive stuff here. Should think about shifting it to a hidden directory? Or is settings already hidden.
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogsite',
        'USER': 'daniel',
        'PASSWORD': 'daniel',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# for uploading to heroku, following heroku's env var for database_url format
if ((os.environ.get('DATABASE_URL')!='localhost') and os.environ.get('DATABASE_URL')):

    # split the environment variable up into the respective fields
    database_credentials = os.environ.get('DATABASE_URL')
    first_delimiter = database_credentials.find('://')+2
    second_delimiter = database_credentials.find(':', first_delimiter+1)
    third_delimiter = database_credentials.find('@', second_delimiter+1)
    fourth_delimiter = database_credentials.find(':', third_delimiter+1)
    fifth_delimiter = database_credentials.find('/', fourth_delimiter+1)
    name = database_credentials[fifth_delimiter+1:]
    user = database_credentials[first_delimiter+1:second_delimiter]
    password = database_credentials[second_delimiter+1:third_delimiter]
    host = database_credentials[third_delimiter+1:fourth_delimiter]
    port = database_credentials[fourth_delimiter+1:fifth_delimiter]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

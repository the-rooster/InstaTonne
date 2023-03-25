"""
Django settings for InstaTonne project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import sys
import django_on_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Configure this before deployment
HOSTNAME = os.environ["HOSTNAME"] if "HOSTNAME" in os.environ else "http://127.0.0.1:8000"
FRONTEND = os.environ["FRONTEND"] if "FRONTEND" in os.environ else "http://127.0.0.1:5173"

print(HOSTNAME,FRONTEND)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else 'django-insecure-&*@f6gvr9uj@kzi*dyrenhrxjraelqzm9bf6zb3r7#ge#c!u5+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['cmput404-group6-instatonne.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'InstaTonneApis.apps.InstatonneapisConfig',
    'drf_yasg'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# This will need to be updated to allow other groups to connect to us
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # allow frontend
    "http://localhost:3000", # allow tests
    "http://127.0.0.1:5173",
    "https://t20-social-distribution.herokuapp.com",
    "https://social-distribution-media.herokuapp.com",
    "https://group-13-epic-app.herokuapp.com",
    "https://epic-app.vercel.app",
    HOSTNAME,
    FRONTEND,
    "https://group-13-epic-app.herokuapp.com",
    "https://social-distribution-media.herokuapp.com",
    "https://t20-social-distribution.herokuapp.com"
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173", # allow frontend
    "http://localhost:3000", # allow tests
    "http://127.0.0.1:5173",
    HOSTNAME,
    FRONTEND,
    "https://group-13-epic-app.herokuapp.com",
    "https://social-distribution-media.herokuapp.com",
    "https://t20-social-distribution.herokuapp.com"
]

CORS_ALLOW_HEADERS = [
    "X-CSRFToken",
    "Cookie",
    "Authorization",
    "Content-Type"
]

CSRF_COOKIE_HTTPONLY = False



CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'InstaTonne.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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



WSGI_APPLICATION = 'InstaTonne.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

print("BASE DIR",BASE_DIR)
STATIC_URL = 'assets/'
STATIC_ROOT = BASE_DIR / 'assets_go_here'
print("STATIC ROOT",STATIC_ROOT)

STATICFILES_DIRS = [
    BASE_DIR / 'templates/assets',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
     ),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


django_on_heroku.settings(locals(),staticfiles=False)
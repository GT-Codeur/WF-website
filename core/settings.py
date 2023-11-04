"""Django settings for wf_website project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import os
import sys

import dj_database_url
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

# Disable logging while running tests
if len(sys.argv) > 1 and sys.argv[1] == "test":
    logging.disable(logging.CRITICAL)

default_allowed_hosts = "127.0.0.1,localhost,westernfriend.eu.ngrok.io"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", default_allowed_hosts).split(",")

default_csrf_trusted_origins = "http://127.0.0.1,https://127.0.0.1,http://localhost,https://localhost,https://westernfriend.eu.ngrok.io"

CSRF_TRUSTED_ORIGINS = os.getenv(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default_csrf_trusted_origins,
).split(",")

CORE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(CORE_DIR)


SECURE_REFERRER_POLICY = "strict-origin"
# Allow PayPal to open up in-context pop-ups
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() in ("true", "1")

if DEBUG:
    SECRET_KEY = "not-so-secret-key"
else:
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "WARNING"),
        },
    },
}

# if SENTRY_DSN is set, then we are running in production
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
    )

# Settings related to DigitalOcean Spaces
# Note: for now, we are using the AWS naming-convention from Boto3
USE_SPACES = os.getenv("DJANGO_USE_SPACES", "False") == "True"
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "sfo3")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_LOCATION = os.getenv("AWS_LOCATION", "static")
PUBLIC_MEDIA_LOCATION = os.getenv("PUBLIC_MEDIA_LOCATION", "media")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

AUTH_USER_MODEL = "accounts.User"

CART_SESSION_ID = "cart"

# PayPal settings
PAYPAL_CLIENT_ENVIRONMENT = os.getenv("PAYPAL_CLIENT_ENVIRONMENT", "sandbox")
PAYPAL_API_URL = (
    "https://api-m.paypal.com"
    if PAYPAL_CLIENT_ENVIRONMENT.lower() == "production"
    else "https://api-m.sandbox.paypal.com"
)
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

# TODO: enable PayPal webhook support
# PAYPAL_WEBHOOK_ID = os.getenv("PAYPAL_WEBHOOK_ID")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # First party (apps from this project)
    "accounts",
    "addresses",
    "cart",
    "common",
    "community",
    "contact",
    "content_migration",
    "documents",
    "events",
    "facets",
    "forms",
    "home",
    "library",
    "memorials",
    "navigation",
    "news",
    "orders",
    "payment.apps.PaymentConfig",
    "paypal",
    "search",
    "store",
    "subscription",
    "magazine",
    "tags",
    "blocks",
    "wf_pages",
    # Third party (apps that have been installed)
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_flatpickr",
    "modelcluster",
    "storages",
    "taggit",
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail_color_panel",
    "wagtailmedia",
    # Contrib (apps that are included in Django)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(CORE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
            "debug": True if DEBUG else False,
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL")

NOT_COLLECTING_STATICFILES = len(sys.argv) > 1 and sys.argv[1] != "collectstatic"

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    # Default to using local development environment
    if NOT_COLLECTING_STATICFILES:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "wf_website",
                "USER": "postgres",
                "PASSWORD": "postgres",
                "HOST": "localhost",
                "PORT": "5432",
            },
        }


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
WAGTAIL_I18N_ENABLED = True


USE_TZ = True
TIME_ZONE = "America/Los_Angeles"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(CORE_DIR, "static"),
]

if USE_SPACES:
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{ AWS_STORAGE_BUCKET_NAME }/{AWS_LOCATION}/"

    STORAGES = {
        "default": {
            "BACKEND": "core.storage_backends.MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "core.storage_backends.StaticStorage",
        },
    }

    MEDIA_URL = (
        f"{AWS_S3_ENDPOINT_URL}/{ AWS_STORAGE_BUCKET_NAME }/{PUBLIC_MEDIA_LOCATION}/"
    )

    # Prevent setting URL querystring parameters
    # which are causing 403 errors on DigitalOcean Spaces
    AWS_QUERYSTRING_AUTH = False
else:
    STATIC_URL = "/static/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"


# Wagtail settings
WAGTAIL_SITE_NAME = "Western Friend"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "https://westernfriend.org"

# Email settings
EMAIL_HOST = os.getenv("EMAIL_HOST", None)
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = (
    os.getenv("EMAIL_USE_SSL", "False") == "True"
)  # SSL is less secure than TLS
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "tech@westernfriend.org",
)

# if the EMAIL authentication environment variables are set,
# then we can use the SMTP backend
if (
    EMAIL_HOST is not None
    and EMAIL_HOST_USER is not None
    and EMAIL_HOST_PASSWORD is not None
):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "/admin"


INTERNAL_IPS = [
    "127.0.0.1",
]

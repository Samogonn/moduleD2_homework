from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django_filters",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_apscheduler",
    "rest_framework",
    "news",
    "accounts",
]


SITE_ID = 1

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/news/"
LOGOUT_REDIRECT_URL = "/news/"

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_FORMS = {"signup": "accounts.models.BasicSignupForm"}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

WSGI_APPLICATION = "config.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache_files"),
    }
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [BASE_DIR / "static"]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25


ADMINS = [
    ("admin", "admin@example.com"),
]


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "console_debug": {"format": "%(asctime)s %(levelname)s %(message)s"},
#         "console_path": {"format": "%(pathname)s"},
#         "file_general": {"format": "%(asctime)s %(levelname)s %(module)s %(message)s"},
#         "file_error": {"format": "%(asctime)s %(levelname)s %(message)s %(pathname)s"},
#         "file_security": {"format": "%(asctime)s %(levelname)s %(module)s %(message)s"},
#     },
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         },
#         "require_debug_false": {
#             "()": "django.utils.log.RequireDebugFalse",
#         },
#     },
#     "handlers": {
#         "console_debug": {
#             "level": "DEBUG",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#             "formatter": "console_debug",
#         },
#         "console_path": {
#             "level": "WARNING",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#             "formatter": "console_path",
#         },
#         "file_general": {
#             "level": "INFO",
#             "filters": ["require_debug_true"],
#             "class": "logging.FileHandler",
#             "filename": f"{BASE_DIR}/config/logs/general.log",
#             "formatter": "file_general",
#         },
#         "file_error": {
#             "level": "INFO",
#             "filters": ["require_debug_true"],
#             "class": "logging.FileHandler",
#             "filename": f"{BASE_DIR}/config/logs/errors.log",
#             "formatter": "file_error",
#         },
#         "file_security": {
#             "level": "INFO",
#             "filters": ["require_debug_true"],
#             "class": "logging.FileHandler",
#             "filename": f"{BASE_DIR}/config/logs/security.log",
#             "formatter": "file_security",
#         },
#         "mail_admins": {
#             "level": "ERROR",
#             "filters": ["require_debug_false"],
#             "class": "django.utils.log.AdminEmailHandler",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console_debug", "console_path", "file_general"],
#             "propagate": True,
#             "level": "DEBUG",
#         },
#         "django.request": {
#             "handlers": ["file_error", "mail_admins"],
#             "propagate": True,
#             "level": "ERROR",
#         },
#         "django.server": {
#             "handlers": ["file_error", "mail_admins"],
#             "propagate": True,
#             "level": "ERROR",
#         },
#         "django.template": {
#             "handlers": ["file_error"],
#             "propagate": True,
#             "level": "ERROR",
#         },
#         "django.db_backends": {
#             "handlers": ["file_error"],
#             "propagate": True,
#             "level": "ERROR",
#         },
#         "django.security": {
#             "handlers": ["file_security"],
#             "propagate": True,
#             "level": "INFO",
#         },
#     },
# }


# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

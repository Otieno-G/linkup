import os
from pathlib import Path
from dotenv import load_dotenv # Import to load local .env file
import dj_database_url # Import for production PostgreSQL configuration

# Load environment variables from .env file (if it exists)
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# Read SECRET_KEY from environment variable (secure practice)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-h^9&#m^&n&y3g5-m^mxa6o87#v+&b1)=-9g+*o)2$t-zq^jo9h')

# SECURITY WARNING: don't run with debug turned on in production!
# Read DEBUG from environment, default to False for production safety
DEBUG = os.getenv('DEBUG', 'False') == 'True' 

# Add production hosts (Render URL, etc.) here
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
if not DEBUG and os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'widget_tweaks',

    # Your apps (Ensure profiles uses the AppConfig path to register signals!)
    'profiles.apps.ProfilesConfig', 
    'posts', 
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

ROOT_URLCONF = 'linkup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'linkup.wsgi.application'

# -----------------
# 🎯 DATABASE CONFIGURATION (Production vs. Local)
# -----------------

# 1. Production (PostgreSQL) Configuration: Use DATABASE_URL environment variable
if os.getenv('DATABASE_URL'):
    # Use dj_database_url to parse the PostgreSQL URL for production
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600)
    }

# 2. Local Development (MySQL) Configuration: Fallback if DATABASE_URL is NOT set
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DATABASE', 'linkup_local_db'),
            'USER': os.getenv('MYSQL_USER', 'root'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
            'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
            'OPTIONS': {
                # Recommended setting for MySQL compatibility
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'profiles' / 'static',
]

# Media files (User Uploads - required for profile pictures and post images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication redirects (used with django.contrib.auth.urls)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
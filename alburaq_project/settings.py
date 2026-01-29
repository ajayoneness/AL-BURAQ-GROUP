"""
Django settings for alburaq_project project.
AL BURAQ GROUP - International Trade & Logistics
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-urqcgz+5yc#caxo$_hhd3bdkt+rnmte-_sp3r=w+3_u$m2g^du'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'parler',
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local apps
    'apps.core',
    'apps.pages',
    'apps.faq',
    'apps.store',
    'apps.orders',
    'apps.accounts',
    'apps.tracking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For language switching
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alburaq_project.urls'

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
                'django.template.context_processors.i18n',
                'apps.core.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'alburaq_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization - Multilingual Support
LANGUAGE_CODE = 'ar'  # Default language: Arabic

TIME_ZONE = 'Asia/Shanghai'  # China timezone

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
    ('fr', 'Français'),
    ('zh-hans', '中文'),
    ('tr', 'Türkçe'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('ru', 'Русский'),
]

# RTL languages
RTL_LANGUAGES = ['ar']

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Parler settings for model translations
PARLER_LANGUAGES = {
    None: (
        {'code': 'ar'},
        {'code': 'en'},
        {'code': 'fr'},
        {'code': 'zh-hans'},
        {'code': 'tr'},
        {'code': 'es'},
        {'code': 'it'},
        {'code': 'ru'},
    ),
    'default': {
        'fallback': 'ar',
        'hide_untranslated': False,
    }
}


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Login/Logout URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'


# Company Settings
COMPANY_NAME = 'AL BURAQ GROUP'
COMPANY_EMAIL = 'alburaqgroupcn@gmail.com'
COMPANY_PHONE = '+8619557959148'
COMPANY_WHATSAPP = '+8619557959148'

SOCIAL_LINKS = {
    'tiktok': 'https://www.tiktok.com/@alburaqgroup',
    'instagram': 'https://www.instagram.com/alburaq.cn/',
    'youtube': 'https://www.youtube.com/@alburaqcn',
    'facebook': 'https://www.facebook.com/profile.php?id=61578631592555',
}
# Reload translations trigger again

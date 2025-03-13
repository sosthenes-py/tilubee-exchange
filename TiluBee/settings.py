# Below are things to do before going live
#TODO: At email_sender.py, uncomment email sending method and check to verify email does send
#TODO: At user.mixins, in customLoginMixin, uncomment the session checking block
#TODO: Run the code below this settings page to populate tickers
#TODO: In coinroto script, run the commented code below it to generate crm's BaseWallet


from pathlib import Path
from decouple import config
import firebase_admin
from firebase_admin import credentials, auth

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.99.48', 'localhost', '127.0.0.1', '.app.github.dev']


cred = credentials.Certificate("crm/firebase/firebase_credentials.json")
firebase_admin.initialize_app(cred)


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'user_auth',
    'transactions',
    'crm',
    'payment_utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crm.firebase.middleware.FirebaseAuthMiddleware'
]

ROOT_URLCONF = 'TiluBee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CSRF_TRUSTED_ORIGINS = [ 
    "http://localhost:8000",
    "https://refactored-disco-wr7gpvj5rv9wfgww4-8000.app.github.dev"
]

WSGI_APPLICATION = 'TiluBee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.AppUser'

LOGIN_REDIRECT_URL = '/app/wallet'
LOGOUT_REDIRECT_URL = '/auth/login'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_SMTP_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER_EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_USER_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_USER_EMAIL')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',  # This is where you place your static files (app_name, images, etc.)
# ]
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Setup Tickers
# from payment_utils.models import Ticker
# from payment_utils.tickers import COINS_DICT
# available_tickers = Ticker.objects.all()
# tickers_to_add = []
# for coin_short, coin_long in COINS_DICT.items():
#     if coin_short not in available_tickers.values('coin_short'):
#         tickers_to_add.append(Ticker(coin_short=coin_short, coin_long=coin_long))
# if tickers_to_add:
#     Ticker.objects.bulk_create(tickers_to_add)


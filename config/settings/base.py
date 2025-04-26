from pathlib import Path
import environ
from datetime import timedelta

# Load environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# change env debug 
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / '.env')

# === Core Security ===
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

# === Installed Apps ===
DJANGO_APPS = [
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # Authentication and permissions
    'django.contrib.contenttypes', # Required for generic relationships
    'django.contrib.sessions',     # Stores session data (e.g., login info)
    'django.contrib.messages',     # Flash messages framework
    'django.contrib.staticfiles',  # Handles serving static assets
]


THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.clients',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Security headers (e.g., HTTPS)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Stores session data (cookies)
    'django.middleware.common.CommonMiddleware',             # Handles some general HTTP improvements
    'django.middleware.csrf.CsrfViewMiddleware',             # Prevents Cross-Site Request Forgery attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Enables request.user
    'django.contrib.messages.middleware.MessageMiddleware',    # Enables flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protects against iframe attacks
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# === Templates ===
# templates settings
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

# === Database ===
# DEFINED IN dev.py or prod.py

# === Auth User Model ===
# custom auth user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# === Password Validation ===
# validates passwords with specific settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Localization ===
LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='en-us')
TIME_ZONE = env('DJANGO_TIMEZONE', default='UTC')
USE_I18N = True
USE_TZ = True

# === Static & Media ===
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === Primary Key Field ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === REST Framework ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
    "SIGNING_KEY": SECRET_KEY,  
    "ALGORITHM": "HS256"
}
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-ccow$tz_=9%dxu4(0%^(z%nx32#s@(zt9$ih@)5l54yny)wm-0'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'skohen1956-8000.theiadocker.net',
    ('https://skohen1956-8000.theianext-0-labs-prod-misc-tools-us-east-0'
     '.proxy.cognitiveclass.ai'),
    ('https://skohen1956-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01'
     '.proxy.cognitiveclass.ai'),
    ('https://skohen1956-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01'
     '.proxy.cognitiveclass.ai/admin/login/?next=/admin/'),
]

CSRF_TRUSTED_ORIGINS = [
    ('https://skohen1956-8000.theianext-0-labs-prod-misc-tools-us-east-0'
     '.proxy.cognitiveclass.ai'),
    'https://skohen1956-8000.theiadocker.net',
    ('https://skohen1956-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01'
     '.proxy.cognitiveclass.ai'),
    ('https://skohen1956-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01'
     '.proxy.cognitiveclass.ai/admin/login/?next=/admin/'),
]

# Authentication Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Static files and media directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/static'),
    os.path.join(BASE_DIR, 'frontend/build'),
    os.path.join(BASE_DIR, 'frontend/build/static'),
]

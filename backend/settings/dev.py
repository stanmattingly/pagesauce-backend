from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b&eeuk(!h!*gn0ae*r#i-+jc6$sdm-24wsipk%8-(n2#-x=#^+'

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'
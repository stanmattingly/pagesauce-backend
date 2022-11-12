from .common import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b&eeuk(!h!*gn0ae*r#i-+jc6$sdm-24wsipk%8-(n2#-x=#^+99999'

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
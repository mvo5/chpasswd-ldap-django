from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CHPASSWD_DOMAIN="uni-trier.de"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chpasswd_db',
        'USER': 'chpasswd',
        'PASSWORD': open(os.path.join(
            os.path.dirname(__file__), "db-password")).read(),
        'HOST': 'localhost',
        'PORT': '',
    }
}

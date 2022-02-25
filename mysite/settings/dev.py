from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "hqb(yysfnbsij)9h2bnd)-y#sezp#f%7r%u1(8@u6@8nxn)qsd"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

BASE_URL = "https://local.wagtail.org"

try:
    from .local import *
except ImportError:
    pass

from .shared_settings import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = 'genericfrontend1_0'
ALLOWED_HOSTS = []

# Development DataBase setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'apiautomationdb',
#         'USER': 'apiautomationdb',
#         'PASSWORD': 'Cf9zFy61VTwzWAHWXL4o',
#         'HOST': 'apiautomation-dbi.co1bdjlevwzl.ap-south-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# AWS S3 bucket,cloudfront setup


AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_ACCESS_KEY_ID = 'AKIAJFPSNFVE4PGGQTCQ'
AWS_ARN = 'arn:aws:sns:us-east-1:232459418842:snstesting'
AWS_REGION = "us-east-1"
AWS_SECRET_ACCESS_KEY = 'NKQH9JKf2OVo1FNO8Y+k568VyyfaVwtMovuyqsMy'
AWS_STORAGE_BUCKET_NAME = 'genericfrontend-1.0'
CLOUDFRONT_DOMAIN = "d2fm57jdyqhtpt.cloudfront.net"
CLOUDFRONT_ID = "E3VOI3YLR6YO1Q"
CLOUDFRONT_CNAME = "genericfrontend.page"
# to make sure the url that the files are served from this domain
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN
AWS_DEFAUlT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


# For Local disable below part
# AWS_LOCATION = 'static'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


AWS_PUBLIC_MEDIA_LOCATION = 'static/media'
DEFAULT_FILE_STORAGE = 'common.utilities.file_storage.PublicMediaStorage'
AWS_PRIVATE_MEDIA_LOCATION = 'static/files'
PRIVATE_FILE_STORAGE = 'includes.s3_storage.PrivateMediaStorage'
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

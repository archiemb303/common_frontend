from .shared_settings import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


sentry_sdk.init(
    dsn="https://cc42c54189b2416a99f64e8f630660cc@o463434.ingest.sentry.io/5468438",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEBUG = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = 'abkaro1_0'
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
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_ACCESS_KEY_ID = 'AKIAJFPSNFVE4PGGQTCQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_ARN = 'arn:aws:sns:us-east-1:232459418842:snstesting'
AWS_REGION = "us-east-1"
AWS_STORAGE_BUCKET_NAME = 'akstage-media'
CLOUDFRONT_DOMAIN = "d14qfvm28ubfpo.cloudfront.net"
CLOUDFRONT_ID = "EK6F4GRE09B1Q"

# to make sure the url that the files are served from this domain
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN
AWS_DEFAUlT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# AWS_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_REGION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_PUBLIC_MEDIA_LOCATION = 'static/media/user_media'
DEFAULT_FILE_STORAGE = 'common.utilities.file_storage.PublicMediaStorage'
AWS_PRE_MEDIA_LOCATION = 'static/media/skill_images'
AWS_PRIVATE_MEDIA_LOCATION = 'static/files'
PRIVATE_FILE_STORAGE = 'includes.s3_storage.PrivateMediaStorage'
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880


USER_DEFINED_MEDIA_URL = 'https://d14qfvm28ubfpo.cloudfront.net/static/media/user_media/'
PREDEFINED_MEDIA_URL = 'https://d14qfvm28ubfpo.cloudfront.net/static/media/skill_images/'

# chat related
ASGI_APPLICATION = 'abkaro.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
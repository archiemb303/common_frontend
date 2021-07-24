from .shared_settings import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Sentry setup for loggers
sentry_sdk.init(
    dsn="https://3b349ceec36b46788dd2e52ba156931b@sentry.io/5173333",
    integrations=[DjangoIntegration()],send_default_pii=True)
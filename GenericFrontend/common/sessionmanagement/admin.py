from django.contrib import admin
from .models import UserSessionsStatus
from .models import UserSessions

# Register your models here.
admin.site.register(UserSessionsStatus)
admin.site.register(UserSessions)

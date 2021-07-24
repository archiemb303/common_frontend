from django.contrib import admin
from .models import VendorStatus
from .models import Vendor
from .models import TokenStatus
from .models import TokenType
from .models import ApiTokens

# Register your models here.

admin.site.register(Vendor)
admin.site.register(VendorStatus)
admin.site.register(TokenStatus)
admin.site.register(TokenType)
admin.site.register(ApiTokens)

from django.contrib import admin
from .models import *

# Register your models here.
# class UserCredentialsAdmin(admin.ModelAdmin):
#     list_display = ('email_id', 'password')
admin.site.register(SourceStatus)
admin.site.register(Sources)
admin.site.register(Uuid)
admin.site.register(EmailVerificationStatus)
admin.site.register(EmailVerificationOtp)
admin.site.register(EmailVerification)
admin.site.register(MobileVerificationStatus)
admin.site.register(MobileVerification)
# admin.site.register(UserCredentials, UserCredentialsAdmin)
admin.site.register(UserCredentials)
admin.site.register(UserProfileStatus)
admin.site.register(DpFlag)
admin.site.register(UserProfile)
admin.site.register(UuidToProfileIdMapStatus)
admin.site.register(UuidToProfileIdMap)
admin.site.register(AddBio)
admin.site.register(CaptchaStatus)
admin.site.register(Captcha)
# admin.site.register(SocialLoginSecretKeyStatus)
# admin.site.register(SocialLoginSecretKey)

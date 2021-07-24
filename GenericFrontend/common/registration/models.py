# # from django.db import models
from django.db import models
from common.location.models import Cities, Countries
from common.apiauthentication.models import Vendor
from datetime import datetime, timedelta, date
import uuid
#
# # Create your models here.
#
# # Create your models here.
# '''
# This File Contains Following Tables
# 1. EmailverificationStatus
# 2. EmailVerification
# 3. UserCredentials
# 4. Uuid
# 5. UserProfileStatus
# 6. DpFlag
# 7. UserProfile
# 8. UuidToProfileIdMapStatus
# 9. UuidToProfileIdMap
# 10.UserSessionsStatus
# 11.UserSessions
# '''
#
class SourceStatus(models.Model):
    status_id = models.AutoField(primary_key=True, default=1)
    status_name = models.CharField(max_length=100)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)

    def __str__(self):
        return str(self.status_id)
#
class Sources(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=100)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)
    source_keys = models.CharField(max_length=10000,default=None) #this should be a json with key value pairs
    source_status = models.ForeignKey(SourceStatus, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.source_id)
#
class Uuid(models.Model):
    uuid_id = models.CharField(primary_key=True, blank=True, max_length=100, unique=True, default=uuid.uuid4, editable=False)
    source_uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=True)
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)
    vendor = models.ForeignKey(Vendor, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uuid_id)
# #
# # # class UuidMobile(models.Model):
# # #     uuid_mobile_id = models.CharField(primary_key=True, blank=True, max_length=100, unique=True, default=uuid.uuid4, editable=False)
# # #     phone_number = models.IntegerField(default=0)
# # #     country_id = models.ForeignKey(Countries, default=1, on_delete=models.CASCADE)
# # #     otp = models.IntegerField(default=20)
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     # uuid_mobile_verification_id = models.IntegerField(default=1)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #     def __str__(self):
# # #         return str(self.uuid_mobile_id)
# #
# #
class EmailVerificationStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)

    def __str__(self):
        return str(self.status_id)
#
#
class EmailVerification(models.Model):
    emailverification_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    email_id = models.CharField(max_length=100, default=None)
    activation_key = models.CharField(max_length=100, default=None)
    activation_status = models.ForeignKey(EmailVerificationStatus, on_delete=models.CASCADE)
    uuid = models.ForeignKey(Uuid, on_delete=models.CASCADE) #need to revisit
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)

    def __str__(self):
        return str(self.emailverification_id)
#
#
class EmailVerificationOtp(models.Model):
    emailverificationotp_id = models.AutoField(primary_key=True)
    # first_name = models.CharField(max_length=100, default=None)
    # last_name = models.CharField(max_length=100, default=None)
    email_id = models.CharField(max_length=100, default=None)
    otp = models.IntegerField(default=20)
    emailverificationotp_status = models.ForeignKey(EmailVerificationStatus, on_delete=models.CASCADE)
    uuid = models.ForeignKey(Uuid, on_delete=models.CASCADE) #need to revisit
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    history = models.CharField(max_length=10000000, default=None, null=True)

    def __str__(self):
        return str(self.emailverificationotp_id)

class MobileVerificationStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)
#
#
class MobileVerification(models.Model):
    mobileverification_id = models.AutoField(primary_key=True)
    phone_number = models.BigIntegerField(default=0) #does it or does it not include country code
    country_id = models.ForeignKey(Countries, default=1, on_delete=models.CASCADE)
    otp = models.IntegerField(default=20)
    login_count = models.IntegerField(default=0) #moved up from mobile credentials table
    uuid_id = models.ForeignKey(Uuid, on_delete=models.CASCADE)
    mobileverification_status = models.ForeignKey(MobileVerificationStatus, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    # uuid_mobile_verification_id = models.IntegerField(default=1)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.mobileverification_id)
# #
# # # not needed
# # # class UserMobileCredentials(models.Model):
# # #     cred_id = models.AutoField(primary_key=True)
# # #     mobile_verification_id = models.ForeignKey(MobileVerification, on_delete=models.CASCADE)
# # #     login_count = models.IntegerField(default=0)
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #
# # #     def __str__(self):
# # #         return str(self.cred_id)
# #
# #
class UserCredentials(models.Model):
    cred_id = models.AutoField(primary_key=True) #change name to cred_id instead of native_id
    email_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    forgot_pwd_key = models.CharField(max_length=100)
    forgot_pwd_time = models.DateTimeField(blank=True)
    account_verification_id = models.ForeignKey(EmailVerification, on_delete=models.CASCADE)
    login_count = models.IntegerField(default=0)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.cred_id)
# #
# #
class UserProfileStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)

class UserProfileCompletionStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


#
#
class DpFlag(models.Model):
    flag_id = models.AutoField(primary_key=True)
    flag_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.flag_id)


class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    sex = models.CharField(max_length=100, default=None)
    date_of_birth = models.DateField(default=None, null=True, blank=True)
    orientation = models.CharField(max_length=100, default=None)
    profile_status = models.ForeignKey(UserProfileStatus, on_delete=models.CASCADE, default=None)
    profile_completion_status = models.ForeignKey(UserProfileCompletionStatus, on_delete=models.CASCADE, default=None)
    web_profile_key = models.CharField(max_length=100, default=None)
    android_app_profile_key = models.CharField(max_length=100, default=None)
    ios_app_profile_key = models.CharField(max_length=100, default=None)
    global_profile_key = models.CharField(max_length=100, default=None)
    city_id = models.ForeignKey(Cities,  on_delete=models.CASCADE, default=None, null=True)
    dp_flag = models.ForeignKey(DpFlag, on_delete=models.CASCADE, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.profile_id)
#
# #
class UuidToProfileIdMapStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)
# #
# #
class UuidToProfileIdMap(models.Model):
    map_id = models.AutoField(primary_key=True)
    uuid_id = models.ForeignKey(Uuid, on_delete=models.CASCADE)
    # uuid_mobile_verification = models.ForeignKey(Uuid_Mobile, default=1, on_delete=models.CASCADE)
    # uuid_mobile_id = models.ForeignKey(Uuid_Mobile, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.ForeignKey(UuidToProfileIdMapStatus, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.map_id)
# #
class AddBio(models.Model):
    bio_id = models.AutoField(primary_key=True)
    short_description = models.TextField(default=None, blank=True)
    profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.bio_id)
# #
# #
# # # class UuidMobileToProfileIdMapStatus(models.Model):
# # #     status_id = models.AutoField(primary_key=True)
# # #     status_name = models.CharField(max_length=100, default=None)
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #
# # #     def __str__(self):
# # #         return str(self.status_id)
# #
# #
# # # class UuidMobileToProfileIdMap(models.Model):
# # #     map_id = models.AutoField(primary_key=True)
# # #     uuid_mobile = models.ForeignKey(UuidMobile, on_delete=models.CASCADE)
# # #     # uuid_mobile_verification = models.ForeignKey(Uuid_Mobile, default=1, on_delete=models.CASCADE)
# # #     # uuid_mobile_id = models.ForeignKey(Uuid_Mobile, on_delete=models.CASCADE)
# # #     profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
# # #     status = models.ForeignKey(UuidMobileToProfileIdMapStatus, on_delete=models.CASCADE)
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #
# # #     def __str__(self):
# # #         return str(self.map_id)
# #
class CaptchaStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)

    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


class Captcha(models.Model):
    captcha_id = models.AutoField(primary_key=True)
    captcha_key = models.CharField(max_length=100, default=None)
    status = models.ForeignKey(CaptchaStatus, on_delete=models.CASCADE)

    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.captcha_id)


class WdSocialLoginSecretKeyStatus(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length=100, default =  None)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length =100,default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length =100,default=None)
    def __str__(self):
        return str(self.status_id)


class WdSocialLoginSecretKey(models.Model):
    socialloginsecretkey_id = models.AutoField(primary_key=True)
    socialloginsecret_key = models.CharField(max_length=100, default=None)
    status = models.ForeignKey(WdSocialLoginSecretKeyStatus, on_delete=models.CASCADE)
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.CharField(max_length =100,default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length =100,default=None)
    def __str__(self):
        return str(self.socialloginsecretkey_id)

# #
# #
# # # class SocialLoginSecretKeyStatus(models.Model):
# # #     status_id = models.AutoField(primary_key=True)
# # #     status_name = models.CharField(max_length=100, default=None)
# # #
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #
# # #     def __str__(self):
# # #         return str(self.status_id)
# # #
# # #
# # # class SocialLoginSecretKey(models.Model):
# # #     socialloginsecretkey_id = models.AutoField(primary_key=True)
# # #     socialloginsecret_key = models.CharField(max_length=100, default=None)
# # #     status = models.ForeignKey(SocialLoginSecretKeyStatus, on_delete=models.CASCADE)
# # #     source = models.CharField(max_length=100, default=None)
# # #     added_date = models.DateTimeField(default=datetime.now)
# # #     added_by = models.CharField(max_length=100, default=None)
# # #     last_modified_date = models.DateTimeField(default=datetime.now)
# # #     last_modified_by = models.CharField(max_length=100, default=None)
# # #
# #     def __str__(self):
# #         return str(self.socialloginsecretkey_id)
#
#

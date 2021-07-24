from .models import *
from rest_framework import serializers


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = '__all__'

class EmailVerificationOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationOtp
        fields = '__all__'
class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = '__all__'

class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = '__all__'

class UuidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uuid
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AddBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBio
        fields = '__all__'


class UuidToProfileIdMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = UuidToProfileIdMap
        fields = '__all__'


class MobileVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileVerification
        fields = '__all__'


class SourceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceStatus
        fields = '__all__'


class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = '__all__'


class EmailVerificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationStatus
        fields = '__all__'


class MobileVerificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileVerificationStatus
        fields = '__all__'


class UserProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileStatus
        fields = '__all__'


class UserProfileCompletionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileCompletionStatus
        fields = '__all__'


class DpFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpFlag
        fields = '__all__'


class UuidToProfileIdMapStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UuidToProfileIdMapStatus
        fields = '__all__'


class CaptchaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptchaStatus
        fields = '__all__'


class WdSocialLoginSecretKeyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WdSocialLoginSecretKeyStatus
        fields = '__all__'

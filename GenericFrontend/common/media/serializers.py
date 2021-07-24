from rest_framework import serializers
from .models import *

class MediasStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibraryStatus
        fields = ('__all__')


class MediasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibrary
        fields = ('__all__')


class MediasCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibrary
        fields = ['media_id','file_content']


class DpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dp
        fields = '__all__'


class DpMediaCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dp
        fields = ['dp_id', 'profile_id', 'media_id']
        depth = 1


class DpStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpStatus
        fields = '__all__'







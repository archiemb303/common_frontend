from .models import *
from rest_framework import serializers


class PostLoginTicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLoginTicketStatus
        fields = '__all__'


class PostLoginTicketTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLoginTicketTypes
        fields = '__all__'


class PostLoginTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLoginTickets
        fields = '__all__'


class PostLoginTicketsRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLoginTicketsReplies
        fields = '__all__'


class PostLoginCommonQuestionsByTicketTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLoginCommonQuestionsByTicketTypes
        fields = '__all__'


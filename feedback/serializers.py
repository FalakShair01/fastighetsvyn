from rest_framework import serializers
from .models import AdminFeedback, TenantsFeedback
from django.contrib.auth import get_user_model
from users.serializers import TenantSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "username", "phone", "address", "profile"]


class AdminFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = AdminFeedback
        fields = ['id', 'title', 'description', 'image', 'is_done', 'is_archive', 'created_at', 'updated_at', 'user']


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantsFeedback
        fields = '__all__'

class GetUserFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tenant = TenantSerializer(read_only=True)
    class Meta:
        model = TenantsFeedback
        fields = ['id', 'user', 'tenant', 'full_name', 'email', 'phone', 'comment', 'image', 'is_done', 'is_archive', 'created_at', 'updated_at']


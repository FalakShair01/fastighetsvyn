from rest_framework import serializers
from .models import AdminNotifications
from feedback.serializers import AdminFeedbackSerializer
from services.models import UserDevelopmentServices, UserMaintenanceServices
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "username", "phone", "address", "profile"]

class DevelopmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'development', 'user']

class MaintenanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserMaintenanceServices
        fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'maintenance', 'user']

class AdminNotificationsSerializer(serializers.ModelSerializer):
    feedback = AdminFeedbackSerializer(read_only=True)
    development = DevelopmentSerializer(read_only=True)
    maintenance = MaintenanceSerializer(read_only=True)
    class Meta:
        model = AdminNotifications
        fields = ['id', 'title', 'description', 'is_read', 'created_at', 'updated_at', 'feedback', 'development', 'maintenance']
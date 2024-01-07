from rest_framework import serializers
from .models import AdminFeedback
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "username", "phone", "address"]


class AdminFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = AdminFeedback
        fields = ['id', 'title', 'description', 'image','is_done', 'created_at', 'updated_at', 'user']
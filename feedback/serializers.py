from rest_framework import serializers
from .models import AdminFeedback, UserFeedback
from django.contrib.auth import get_user_model
from users.models import Tenant
from property.serializers import PropertySerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "address", "profile"]


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "name", "appartment_no", "email", "phone", "profile"]

class AdminFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminFeedback
        fields = [
            "id",
            "title",
            "description",
            "image",
            "is_done",
            "is_archive",
            "created_at",
            "updated_at",
            "user",
        ]


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = "__all__"


class GetUserFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tenant = TenantSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = UserFeedback
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "comment",
            "image",
            "is_done",
            "is_archive",
            "user",
            "tenant",
            "property",
            "created_at",
            "updated_at",
        ]

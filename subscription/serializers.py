from rest_framework import serializers
from users.models import User


class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["subscription_type", "subscription_status"]

class CreateCheckoutSessionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    price_id = serializers.CharField()
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()

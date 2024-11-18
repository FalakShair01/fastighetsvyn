from rest_framework import serializers
from users.models import User
from .models import Subscription

class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["subscription_type", "subscription_status"]

class CreateCheckoutSessionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    price_id = serializers.CharField()
    

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Subscription
        fields = '__all__'
from rest_framework import serializers
from users.models import User

class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['subscription_type', 'subscription_status']


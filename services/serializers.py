from rest_framework import serializers
from .models import Development, UserDevelopmentServices


class DevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Development
        fields = '__all__'


class UserDevelopmentServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'development', 'status', 'started_date', 'end_date']
from rest_framework import serializers
from .models import Homepage

class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homepage
        fields = '__all__'
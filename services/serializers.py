from rest_framework import serializers
from .models import Development, UserDevelopmentServices, Maintenance, UserMaintenanceServices


class DevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Development
        fields = '__all__'


class UserDevelopmentServicesSerializer(serializers.ModelSerializer):
    development = DevelopmentSerializer(read_only=True)
    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'status', 'started_date', 'end_date', 'development']

# Maintaince
class MaintainceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'


class UserMaintenanceServicesSerializer(serializers.ModelSerializer):
    maintenance = MaintainceSerializer(read_only=True)
    class Meta:
        model = UserMaintenanceServices
        fields = ['id', 'status', 'started_date', 'end_date', 'maintenance']

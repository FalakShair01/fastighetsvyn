from rest_framework import serializers
from .models import Development, UserDevelopmentServices, Maintenance, UserMaintenanceServices


class DevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Development
        fields = '__all__'


# class UserDevelopmentServicesSerializer(serializers.ModelSerializer):
#     development = DevelopmentSerializer(read_only=True)
#     class Meta:
#         model = UserDevelopmentServices
#         fields = ['id', 'status', 'started_date', 'end_date', 'development']


class UserDevelopmentServicesSerializer(serializers.ModelSerializer):
    development = DevelopmentSerializer(read_only=True)

    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'status', 'started_date', 'end_date', 'development']

    def create(self, validated_data):
        development_id = self.initial_data.get('development')
        development = Development.objects.get(pk=development_id)
        user_dev_service = UserDevelopmentServices.objects.create(development=development, **validated_data)
        return user_dev_service


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

    def create(self, validated_data):
        maintenance_id = self.initial_data.get('maintenance')
        maintenance = Maintenance.objects.get(pk=maintenance_id)
        user_dev_service = UserMaintenanceServices.objects.create(maintenance=maintenance, **validated_data)
        return user_dev_service


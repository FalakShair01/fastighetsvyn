from rest_framework import serializers
from .models import Development, UserDevelopmentServices, Maintenance, UserMaintenanceServices
from django.contrib.auth import get_user_model
from property.serializers import PropertySerializer
from property.models import Property
from users.serializers import ServiceProviderSerializer
from users.models import ServiceProvider
from django.shortcuts import get_object_or_404

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "username", "phone", "address", "profile"]

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
    property = PropertySerializer(read_only=True)

    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'development', 'property']

    def create(self, validated_data):
        development_id = self.initial_data.get('development')
        property_id = self.initial_data.get('property')

        development = Development.objects.get(pk=development_id)
        property = Property.objects.get(pk=property_id)

        user_dev_service = UserDevelopmentServices.objects.create(development=development, property=property, **validated_data)
        return user_dev_service
    
# Maintaince
class MaintainceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'


class UserMaintenanceServicesSerializer(serializers.ModelSerializer):
    maintenance = MaintainceSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = UserMaintenanceServices
        fields = ['id','status', 'comment','iteration', 'day', 'date', 'time', 'frequency', 'started_date', 'end_date', 'maintenance', 'property', 'service_provider']
        
    def create(self, validated_data):
        maintenance_id = self.initial_data.get('maintenance')
        property_id = self.initial_data.get('property')
        maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
        property = get_object_or_404(Property, pk=property_id)
        user_dev_service = UserMaintenanceServices.objects.create(property=property, maintenance=maintenance, **validated_data)
        return user_dev_service
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['service_provider'] = ServiceProviderSerializer(instance.service_provider).data
        return representation

    
class AdminMaintenanceStatusSerializer(serializers.ModelSerializer):
    maintenance = MaintainceSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    # service_provider = ServiceProviderSerializer(read_only=True)
    class Meta:
        model = UserMaintenanceServices
        fields = ['id','status', 'comment','iteration', 'day', 'date', 'time', 'frequency', 'started_date', 'end_date', 'maintenance', 'property','user', 'service_provider']
        # fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'maintenance', 'property', 'user']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['service_provider'] = ServiceProviderSerializer(instance.service_provider).data
        return representation

class AdminDevelopmentStatusSerializer(serializers.ModelSerializer):
    development = DevelopmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = UserDevelopmentServices
        fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'development', 'property', 'user']

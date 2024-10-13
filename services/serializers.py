from rest_framework import serializers
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    OrderMaintenanceServices,
    ExternalSelfServices,
    SelfServiceProvider,
    ServiceDocumentFolder,
    ServiceFile,
    OrderServiceDocumentFolder,
    OrderServiceFile
)
from django.contrib.auth import get_user_model
from property.serializers import PropertySerializer
from property.models import Property
from users.serializers import ServiceProviderSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "address", "profile"]


class DevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Development
        fields = "__all__"


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
        fields = [
            "id",
            "status",
            "comment",
            "started_date",
            "end_date",
            "development",
            "property",
        ]

    def create(self, validated_data):
        development_id = self.initial_data.get("development")
        property_id = self.initial_data.get("property")

        development = Development.objects.get(pk=development_id)
        property = Property.objects.get(pk=property_id)

        user_dev_service = UserDevelopmentServices.objects.create(
            development=development, property=property, **validated_data
        )
        return user_dev_service


# Maintaince
class MaintainceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"

class OrderMaintenanceServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMaintenanceServices
        fields = [
            "id",
            "maintenance",
            "properties",
            "start_date",
            "frequency",
            "frequency_clarification",
            "access_details",
            "service_provider",
            "status",
            "comment",
        ]

class OrderServiceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderServiceFile
        fields = ['id', 'folder', 'file']

class OrderServiceDocumentFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderServiceDocumentFolder
        fields = ['id', 'name', 'order_service']

class AdminDevelopmentStatusSerializer(serializers.ModelSerializer):
    development = DevelopmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = UserDevelopmentServices
        fields = [
            "id",
            "status",
            "comment",
            "started_date",
            "end_date",
            "development",
            "property",
            "user",
        ]

class SelfServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfServiceProvider
        fields = ['id', 'foretag', 'namn', 'telefon', 'e_post']

class ServiceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFile
        fields = ['id', 'folder', 'file']

class ServiceDocumentFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDocumentFolder
        fields = ['id', 'name', 'manual_service']

class ExternalSelfServicesSerializer(serializers.ModelSerializer):
    kontaktuppgifter_till_ansvarig_leverantor = SelfServiceProviderSerializer()
    property_details = PropertySerializer(source='vilka_byggnader_omfattas', many=True, read_only=True)
    total_property_count = serializers.SerializerMethodField()

    class Meta:
        model = ExternalSelfServices
        fields = [
            'id', 'benamning_av_tjanst', 'kostnad_per_manad', 'vilka_byggnader_omfattas',
            'beskrivning', 'startdatum_for_underhallstjanst', 'hur_ofta_utfor_denna_tjanst',
            'fortydligande_av_tjanstens_frekvens', 'access', 'kontaktuppgifter_till_ansvarig_leverantor', 
            'anteckningar', 'total_property_count', 'property_details'
        ]
    
    def get_total_property_count(self, obj):
        user = self.context['request'].user
        return Property.objects.filter(user=user).count()

    def create(self, validated_data):
        provider_data = validated_data.pop('kontaktuppgifter_till_ansvarig_leverantor')
        byggnader_data = validated_data.pop('vilka_byggnader_omfattas')

        provider = SelfServiceProvider.objects.create(**provider_data)

        external_service = ExternalSelfServices.objects.create(
            kontaktuppgifter_till_ansvarig_leverantor=provider,
            **validated_data
        )

        external_service.vilka_byggnader_omfattas.set(byggnader_data)

        return external_service

    def update(self, instance, validated_data):
        # Handle the nested update for SelfServiceProvider
        provider_data = validated_data.pop('kontaktuppgifter_till_ansvarig_leverantor', None)
        byggnader_data = validated_data.pop('vilka_byggnader_omfattas', None)

        # Update many-to-many relationship if present
        if byggnader_data is not None:
            instance.vilka_byggnader_omfattas.set(byggnader_data)

        # Update the SelfServiceProvider details if provided
        if provider_data:
            provider_instance = instance.kontaktuppgifter_till_ansvarig_leverantor
            if provider_instance:
                # Update the existing provider instance
                for attr, value in provider_data.items():
                    setattr(provider_instance, attr, value)
                provider_instance.save()
            else:
                # Create a new provider if one doesn't exist
                new_provider = SelfServiceProvider.objects.create(**provider_data)
                instance.kontaktuppgifter_till_ansvarig_leverantor = new_provider

        # Update the rest of the fields in ExternalSelfServices
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

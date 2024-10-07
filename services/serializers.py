from rest_framework import serializers
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    UserMaintenanceServices,
    ExternalSelfServices,
    SelfServiceProvider,
    ServiceDocumentFolder,
    ServiceDocument
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


class UserMaintenanceServicesSerializer(serializers.ModelSerializer):
    maintenance = MaintainceSerializer(read_only=True)
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = UserMaintenanceServices
        fields = [
            "id",
            "status",
            "comment",
            "iteration",
            "day",
            "date",
            "time",
            "frequency",
            "started_date",
            "end_date",
            "maintenance",
            "properties",
            "service_provider",
        ]

    def create(self, validated_data):
        maintenance_id = self.initial_data.get("maintenance")
        properties_ids = self.initial_data.get("properties", [])
        maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
        properties = Property.objects.filter(id__in=properties_ids)
        user_dev_service = UserMaintenanceServices.objects.create(
            maintenance=maintenance, **validated_data
        )
        user_dev_service.properties.set(properties)
        return user_dev_service

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["service_provider"] = ServiceProviderSerializer(
            instance.service_provider
        ).data
        return representation


# class UserMaintenanceServicesSerializer(serializers.ModelSerializer):
#     maintenance = MaintainceSerializer(read_only=True)
#     property = PropertySerializer(read_only=True)

#     class Meta:
#         model = UserMaintenanceServices
#         fields = ['id','status', 'comment','iteration', 'day', 'date', 'time', 'frequency', 'started_date', 'end_date', 'maintenance', 'property', 'service_provider']

#     def create(self, validated_data):
#         maintenance_id = self.initial_data.get('maintenance')
#         property_id = self.initial_data.get('property')
#         maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
#         property = get_object_or_404(Property, pk=property_id)
#         user_dev_service = UserMaintenanceServices.objects.create(property=property, maintenance=maintenance, **validated_data)
#         return user_dev_service

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['service_provider'] = ServiceProviderSerializer(instance.service_provider).data
#         return representation


class AdminMaintenanceStatusSerializer(serializers.ModelSerializer):
    maintenance = MaintainceSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    # service_provider = ServiceProviderSerializer(read_only=True)
    class Meta:
        model = UserMaintenanceServices
        fields = [
            "id",
            "status",
            "comment",
            "iteration",
            "day",
            "date",
            "time",
            "frequency",
            "started_date",
            "end_date",
            "maintenance",
            "property",
            "user",
            "service_provider",
        ]
        # fields = ['id', 'status', 'comment', 'started_date', 'end_date', 'maintenance', 'property', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["service_provider"] = ServiceProviderSerializer(
            instance.service_provider
        ).data
        return representation


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

class ServiceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDocument
        fields = ['id', 'file']

class ServiceDocumentFolderSerializer(serializers.ModelSerializer):
    documents = ServiceDocumentSerializer(many=True, required=False)

    class Meta:
        model = ServiceDocumentFolder
        fields = ['id', 'name', 'documents']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['documents'] = ServiceDocumentSerializer(instance.documents.all(), many=True).data
        return representation

class ExternalSelfServicesSerializer(serializers.ModelSerializer):
    kontaktuppgifter_till_ansvarig_leverantor = SelfServiceProviderSerializer()
    documents_folder = ServiceDocumentFolderSerializer()

    class Meta:
        model = ExternalSelfServices
        fields = [
            'id', 'benamning_av_tjanst', 'kostnad_per_manad', 'vilka_byggnader_omfattas',
            'beskrivning', 'startdatum_for_underhallstjanst', 'hur_ofta_utfor_denna_tjanst',
            'fortydligande_av_tjanstens_frekvens', 'access', 'kontaktuppgifter_till_ansvarig_leverantor', 
            'documents_folder', 'anteckningar'
        ]

    def create(self, validated_data):
        # Extract provider data, folder data, and buildings data
        provider_data = validated_data.pop('kontaktuppgifter_till_ansvarig_leverantor')
        folder_data = validated_data.pop('documents_folder')
        buildings_data = validated_data.pop('vilka_byggnader_omfattas', [])
        
        # Create the provider instance
        provider = SelfServiceProvider.objects.create(**provider_data)
        
        # Create the service with the provider
        service = ExternalSelfServices.objects.create(
            kontaktuppgifter_till_ansvarig_leverantor=provider, **validated_data
        )
        
        # Handle document folder creation
        documents_data = folder_data.pop('documents', [])
        folder = ServiceDocumentFolder.objects.create(manual_service=service, **folder_data)
        
        # Handle document creation
        for document_data in documents_data:
            ServiceDocument.objects.create(folder=folder, **document_data)
        
        # Associate buildings with the service
        service.vilka_byggnader_omfattas.set(buildings_data)

        return service

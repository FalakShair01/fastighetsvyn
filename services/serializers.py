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
        fields = '__all__'

class ServiceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDocument
        fields = '__all__'

class ServiceDocumentFolderSerializer(serializers.ModelSerializer):
    documents = ServiceDocumentSerializer(many=True)

    class Meta:
        model = ServiceDocumentFolder
        fields = ['name', 'documents']  # Folder name and related documents

    def create(self, validated_data):
        documents_data = validated_data.pop('documents')
        folder = ServiceDocumentFolder.objects.create(**validated_data)
        for document_data in documents_data:
            ServiceDocument.objects.create(folder=folder, **document_data)
        return folder

class ExternalSelfServicesSerializer(serializers.ModelSerializer):
    kontaktuppgifter_till_ansvarig_leverantor = SelfServiceProviderSerializer()
    relevanta_dokument = ServiceDocumentFolderSerializer()

    class Meta:
        model = ExternalSelfServices
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data
        provider_data = validated_data.pop('kontaktuppgifter_till_ansvarig_leverantor')
        document_folder_data = validated_data.pop('relevanta_dokument')

        # Create SelfServiceProvider
        provider = SelfServiceProvider.objects.create(**provider_data)

        # Create ServiceDocumentFolder and its associated documents
        document_folder = ServiceDocumentFolderSerializer().create(document_folder_data)

        # Create ExternalSelfServices with related provider and document folder
        external_self_service = ExternalSelfServices.objects.create(
            kontaktuppgifter_till_ansvarig_leverantor=provider,
            relevanta_dokument=document_folder,
            **validated_data
        )
        return external_self_service

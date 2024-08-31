from rest_framework import serializers
from .models import Property, Document, Folder


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        # fields = ('id', 'byggnad', 'fond', 'ansvarig_AM', 'yta', 'loa', 'bta', 'lokal_elproduktion',
        #           'installered_effekt', 'geo_energi', 'epc_tal', 'address', 'picture', 'longitude', 'latitude')


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ("id", "name", "created_at", "updated_at")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "file",
        )


class ChartSerializer(serializers.Serializer):
    fond = serializers.CharField(max_length=200)
    percentage = serializers.CharField(max_length=200)

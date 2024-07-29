from rest_framework import serializers
from .models import Homepage, DocumentPageDetail, Documents

class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homepage
        fields = '__all__'


class DocumentPageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentPageDetail
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'
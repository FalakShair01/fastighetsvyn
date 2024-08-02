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


class ContactUsFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    message = serializers.CharField()
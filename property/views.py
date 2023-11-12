from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Property, Document
from .serializers import PropertySerializer, DocumentSerializer


# Create your views here.

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.request.user.properties.all()


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)
    

class PropertyDocumentView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_instance = generics.get_object_or_404(Property, id=self.kwargs['property_id'], user=self.request.user)
        return serializer.save(property=property_instance)

    def get_queryset(self):
        property_instance = generics.get_object_or_404(Property, id=self.kwargs['property_id'], user=self.request.user)
        return property_instance.documents.all()
    

class DeleteDocumentView(generics.DestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        property_id = self.kwargs['property_id']
        document_id = self.kwargs['document_id']
        property_instance = generics.get_object_or_404(Property, id=property_id, user = self.request.user)
        return generics.get_object_or_404(Document, property=property_instance, id=document_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Document deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

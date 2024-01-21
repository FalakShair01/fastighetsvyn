import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from .models import Property, Document, Folder
from .serializers import PropertySerializer, DocumentSerializer, ChartSerializer, FolderSerializer
from django_filters import rest_framework as filters
from django.db.models import Count
from django.http import HttpResponse
import csv
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import models


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'fond': ['in','exact'],
            'byggnad': ['in','exact'],
            'ansvarig_AM': ['in','exact'],
            'yta': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'loa': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'bta': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'installered_effekt': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'epc_tal': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'lokal_elproduktion': ['exact'],
            'geo_energi': ['exact'],
        }

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PropertyFilter
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Property.objects.filter(user=self.request.user).order_by('-created_at')


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete the associated picture file from the directory
        picture_path = instance.picture.path
        if picture_path and os.path.exists(picture_path):
            os.remove(picture_path)

        # Call the superclass's destroy method to delete the database record
        self.perform_destroy(instance)

        return Response({"detail": "Property deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class FolderViewset(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property = generics.get_object_or_404(Property, id=self.kwargs['property_id'], user=self.request.user)
        return serializer.save(property=property)
    
    def get_queryset(self):
        property_instance = generics.get_object_or_404(Property, id=self.kwargs['property_id'], user=self.request.user)
        return property_instance.folders.all()
    

class PropertyDocumentView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        folder_instance = generics.get_object_or_404(Folder, id=self.kwargs['folder_id'])
        return serializer.save(folder=folder_instance)

    def get_queryset(self):
        folder_instance = generics.get_object_or_404(Folder, id=self.kwargs['folder_id'])
        return folder_instance.documents.all()
    

class DeleteDocumentView(generics.DestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        folder_instance = generics.get_object_or_404(Folder, id=folder_id)
        return generics.get_object_or_404(Document, folder=folder_instance, id=document_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete the associated file from the directory
        file_path = instance.file.path
        if os.path.exists(file_path):
            os.remove(file_path)

        self.perform_destroy(instance)
        return Response({"detail": "Document deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class GetPieChartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Property.objects.filter(user=request.user)
        total_fond = data.count()

        # Annotate the queryset with the count for each 'fond'
        fonds_with_counts = data.values('fond').annotate(count=Count('fond'))

        result = []

        for item in fonds_with_counts:
            fond_name = item['fond']
            count = item['count']
            percentage = (count / total_fond) * 100

            # Append the result as a dictionary
            result.append({fond_name: round(percentage, 1)})  # Round to 1 decimal place

        return Response(result)


class PropertyExportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def get(self, request):
        # Apply the same filters as in PropertyFilter
        property_filter = PropertyFilter(request.GET, queryset=Property.objects.filter(user=request.user))
        filtered_properties = property_filter.qs

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="properties_export.csv"'

        writer = csv.writer(response)

        # Write CSV header excluding created_at and updated_at
        header_fields = ['byggnad', 'fond', 'ansvarig_AM', 'yta', 'loa', 'bta', 'lokal_elproduktion', 'installered_effekt', 'geo_energi', 'epc_tal', 'address']
        writer.writerow(header_fields)

        # Write data rows
        for property in filtered_properties:
            data_row = [self.get_field_value(property, field) for field in header_fields]
            writer.writerow(data_row)

        return response

    def get_field_value(self, instance, field_name):
        field = Property._meta.get_field(field_name)
        value = getattr(instance, field_name)
        
        if isinstance(field, models.BigAutoField):
            return ''  # Exclude BigAutoField from CSV export
        elif isinstance(field, models.DateTimeField):
            return value.strftime('%Y-%m-%d %H:%M:%S') if value else ''
        else:
            return str(value)
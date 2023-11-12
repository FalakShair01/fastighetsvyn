from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Property, Document
from .serializers import PropertySerializer, DocumentSerializer
from django_filters import rest_framework as filters

class PropertyFilter(filters.FilterSet):
    lokal_elproduktion = filters.BooleanFilter()
    geo_energi = filters.BooleanFilter()

    byggnad = filters.CharFilter(lookup_expr='exact')
    fond = filters.CharFilter(lookup_expr='exact')
    ansvarig_AM = filters.CharFilter(lookup_expr='exact')
    yta = filters.NumberFilter(lookup_expr='exact')
    loa = filters.NumberFilter(lookup_expr='exact')
    bta = filters.NumberFilter(lookup_expr='exact')
    installered_effekt = filters.NumberFilter(lookup_expr='exact')
    epc_tal = filters.NumberFilter(lookup_expr='exact')

    yta__lt = filters.NumberFilter(field_name='yta', lookup_expr='lt')
    yta__lte = filters.NumberFilter(field_name='yta', lookup_expr='lte')
    yta__gt = filters.NumberFilter(field_name='yta', lookup_expr='gt')
    yta__gte = filters.NumberFilter(field_name='yta', lookup_expr='gte')

    loa__lt = filters.NumberFilter(field_name='loa', lookup_expr='lt')
    loa__gt = filters.NumberFilter(field_name='loa', lookup_expr='gt')
    loa__lte = filters.NumberFilter(field_name='loa', lookup_expr='lte')
    loa__gte = filters.NumberFilter(field_name='loa', lookup_expr='gte')

    bta__lt = filters.NumberFilter(field_name='bta', lookup_expr='lt')
    bta__gt = filters.NumberFilter(field_name='bta', lookup_expr='gt')
    bta__lte = filters.NumberFilter(field_name='bta', lookup_expr='lte')
    bta__gte = filters.NumberFilter(field_name='bta', lookup_expr='gte')

    installered_effekt__lt = filters.NumberFilter(field_name='installered_effekt', lookup_expr='lt')
    installered_effekt__gt = filters.NumberFilter(field_name='installered_effekt', lookup_expr='gt')
    installered_effekt__lte = filters.NumberFilter(field_name='installered_effekt', lookup_expr='lte')
    installered_effekt__gte = filters.NumberFilter(field_name='installered_effekt', lookup_expr='gte')

    epc_tal__lt = filters.NumberFilter(field_name='epc_tal', lookup_expr='lt')
    epc_tal__gt = filters.NumberFilter(field_name='epc_tal', lookup_expr='gt')
    epc_tal__lte = filters.NumberFilter(field_name='epc_tal', lookup_expr='lte')
    epc_tal__gte = filters.NumberFilter(field_name='epc_tal', lookup_expr='gte')

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['picture']


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

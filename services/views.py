from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import Http404
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    UserMaintenanceServices,
    ExternalSelfServices,
    ServiceDocument,
    ServiceDocumentFolder
)
from .serializers import (
    DevelopmentSerializer,
    UserDevelopmentServicesSerializer,
    MaintainceSerializer,
    UserMaintenanceServicesSerializer,
    AdminMaintenanceStatusSerializer,
    AdminDevelopmentStatusSerializer,
    ExternalSelfServicesSerializer,
    ServiceDocumentFolderSerializer,
    ServiceDocumentSerializer,
    SelfServiceProviderSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsAdminOrReadOnly
from .filters import UserMaintenanceFilter, UserDevelopmentFilter, DevelopmentFilter, MaintenanceFilter
from rest_framework import serializers

# Create your views here.


class DevelopmentViewset(viewsets.ModelViewSet):
    queryset = Development.objects.all()
    serializer_class = DevelopmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = DevelopmentFilter

class UserDevelopmentServicesViewset(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = UserDevelopmentServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserDevelopmentFilter

    def get_queryset(self):
        return UserDevelopmentServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Maintenance Service
class MaintenanceViewset(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintainceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = MaintenanceFilter


class UserMaintenanceViewset(viewsets.ModelViewSet):
    queryset = UserMaintenanceServices.objects.all()
    serializer_class = UserMaintenanceServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserMaintenanceFilter

    def get_queryset(self):
        return UserMaintenanceServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Admin See All Pending, Active ,Completed
class AdminDevelopemStatusView(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = AdminDevelopmentStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserDevelopmentFilter

class AdminMaintenanceStatusView(viewsets.ModelViewSet):
    queryset = UserMaintenanceServices.objects.all()
    serializer_class = AdminMaintenanceStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserMaintenanceFilter

class ExternalSelfServiceViewSet(viewsets.ModelViewSet):
    queryset = ExternalSelfServices.objects.all()
    serializer_class = ExternalSelfServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return services belonging to the authenticated user
        return ExternalSelfServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the user when creating a new service
        serializer.save(user=self.request.user)

class DocumentFolderViewset(viewsets.ModelViewSet):
    queryset = ServiceDocumentFolder.objects.all()
    serializer_class = ServiceDocumentFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ServiceDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DocumentDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            document = ServiceDocument.objects.get(id=pk)
        except ServiceDocument.DoesNotExist:
            raise Http404("Document not found.")
        document.delete()
        return Response({"msg": "Document Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)

class UploadDocumentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        manual_service = request.data.get('manual_service')
        files = request.FILES.getlist('file')

        if not files:
            return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        folder_serializer = ServiceDocumentFolderSerializer(data={'manual_service': manual_service, "name": "Dokument"})
        folder_serializer.is_valid(raise_exception=True)
        folder_instance = folder_serializer.save()

        for file in files:
            document_serializer = ServiceDocumentSerializer(data={'folder': folder_instance.id, 'file': file})
            document_serializer.is_valid(raise_exception=True)
            document_serializer.save()

        return Response({'msg': 'Files Uploaded Successfully'}, status=status.HTTP_201_CREATED)

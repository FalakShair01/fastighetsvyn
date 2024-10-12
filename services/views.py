from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import Http404
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    OrderMaintenanceServices,
    ExternalSelfServices,
    ServiceFile,
    ServiceDocumentFolder
)
from .serializers import (
    DevelopmentSerializer,
    UserDevelopmentServicesSerializer,
    MaintainceSerializer,
    OrderMaintenanceServicesSerializer,
    AdminMaintenanceStatusSerializer,
    AdminDevelopmentStatusSerializer,
    ExternalSelfServicesSerializer,
    ServiceDocumentFolderSerializer,
    ServiceFileSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsAdminOrReadOnly
from .filters import OrderMaintenanceFilter, UserDevelopmentFilter, DevelopmentFilter, MaintenanceFilter
from django.shortcuts import get_object_or_404
from property.serializers import PropertySerializer
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

class OrderMaintenanceAPIView(APIView):
    def post(self, request):
        pass

class OrderMaintenanceViewset(viewsets.ModelViewSet):
    queryset = OrderMaintenanceServices.objects.all()
    serializer_class = OrderMaintenanceServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = OrderMaintenanceFilter

    def get_queryset(self):
        return OrderMaintenanceServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Admin See All Pending, Active ,Completed
class AdminDevelopemStatusView(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = AdminDevelopmentStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserDevelopmentFilter

class AdminMaintenanceStatusView(viewsets.ModelViewSet):
    queryset = OrderMaintenanceServices.objects.all()
    serializer_class = AdminMaintenanceStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = OrderMaintenanceFilter

class ExternalSelfServiceViewSet(viewsets.ModelViewSet):
    queryset = ExternalSelfServices.objects.all()
    serializer_class = ExternalSelfServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return services belonging to the authenticated user
        return ExternalSelfServices.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically assign the user when creating a new service
        serializer.save(user=self.request.user)

class ListDocumentFolderView(APIView):
    def get(self, request, manual_service):
        try:
            documents = ServiceDocumentFolder.objects.filter(manual_service=manual_service)
            if not documents.exists():
                return Response({"detail": "No documents found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ServiceDocumentFolderSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ExternalSelfServices.DoesNotExist:
            return Response({"error": "Manual service not found."}, status=status.HTTP_404_NOT_FOUND)

class CreateDocumentFolderView(generics.CreateAPIView):
    queryset = ServiceDocumentFolder.objects.all()
    serializer_class = ServiceDocumentFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentFolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceDocumentFolder.objects.all()
    serializer_class = ServiceDocumentFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ServiceFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FileRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, folder_id):
        folder = get_object_or_404(ServiceDocumentFolder, id=folder_id)        
        files = ServiceFile.objects.filter(folder=folder)
        serializer = ServiceFileSerializer(files, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            file = ServiceFile.objects.get(id=pk)
        except ServiceFile.DoesNotExist:
            raise Http404("file not found.")
        file.delete()
        return Response({"msg": "File Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)

class UploadFileAPIView(APIView):
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
            document_serializer = ServiceFileSerializer(data={'folder': folder_instance.id, 'file': file})
            document_serializer.is_valid(raise_exception=True)
            document_serializer.save()

        return Response({'msg': 'Files Uploaded Successfully'}, status=status.HTTP_201_CREATED)

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
    ServiceDocumentFolder,
    OrderServiceDocumentFolder,
    OrderServiceFile
)
from .serializers import (
    DevelopmentSerializer,
    UserDevelopmentServicesSerializer,
    MaintainceSerializer,
    AdminDevelopmentStatusSerializer,
    ExternalSelfServicesSerializer,
    ServiceDocumentFolderSerializer,
    ServiceFileSerializer,
    OrderMaintenanceServicesSerializer,
    OrderServiceDocumentFolderSerializer,
    OrderServiceFileSerializer
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

# Admin See All Pending, Active ,Completed
class AdminDevelopemStatusView(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = AdminDevelopmentStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserDevelopmentFilter

# Maintenance Service
class MaintenanceViewset(viewsets.ModelViewSet):
    """This Viewset is used by admin to create service"""
    queryset = Maintenance.objects.all()
    serializer_class = MaintainceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = MaintenanceFilter

class CreateOrderMaintenanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        files = request.FILES.getlist('file')
        serializer = OrderMaintenanceServicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_instance = serializer.save(user=request.user)
        folder_instance = OrderServiceDocumentFolder.objects.create(name="Dokument", order_service=order_instance)
        if files:
            for file in files:  # Iterate through uploaded files
                image_serializer = OrderServiceFileSerializer(data={"folder": folder_instance.id, "file": file})
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListOrderMaintenanceAPIView(APIView):
    def get(self, request):
        status_filter = request.query_params.get('status', 'Pending') 
        if request.user.role == "ADMIN":
            order_service = OrderMaintenanceServices.objects.filter(status=status_filter)
        else:
            order_service = OrderMaintenanceServices.objects.filter(user=request.user, status=status_filter)
        serializer = OrderMaintenanceServicesSerializer(order_service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateOrderMaintenanceAPIView(APIView):
    def patch(self, request, pk):
        order_service = get_object_or_404(OrderMaintenanceServices, pk=pk)        
        serializer = OrderMaintenanceServicesSerializer(order_service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DeleteOrderMaintenanceAPIView(APIView):
    def delete(self, request, pk):
        order_service = get_object_or_404(OrderMaintenanceServices, pk=pk)
        order_service.delete()
        return Response({'message': 'service deleted'},status=status.HTTP_204_NO_CONTENT)

class ListOrderDocumentFolderView(APIView):
    def get(self, request, order_service):
        try:
            documents = OrderServiceDocumentFolder.objects.filter(order_service=order_service)
            if not documents.exists():
                return Response({"detail": "No documents found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderServiceDocumentFolderSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except OrderServiceDocumentFolder.DoesNotExist:
            return Response({"error": "service not found."}, status=status.HTTP_404_NOT_FOUND)

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

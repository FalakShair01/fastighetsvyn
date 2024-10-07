from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework import permissions
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

class ExternalSelfServiceView(generics.ListCreateAPIView):
    queryset = ExternalSelfServices.objects.all()
    serializer_class = ExternalSelfServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return ExternalSelfServices.objects.filter(user=self.request.user)

class ExternalSelfServiceDetailView(generics.RetrieveDestroyAPIView):
    queryset = ExternalSelfServices.objects.all()
    serializer_class = ExternalSelfServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExternalSelfServiceDetailUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            external_self_service = ExternalSelfServices.objects.get(pk=pk)
        except ExternalSelfServices.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExternalSelfServicesSerializer(external_self_service, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle updates to the many-to-many field
            if 'vilka_byggnader_omfattas' in request.data:
                buildings_data = request.data.pop('vilka_byggnader_omfattas')
                # Use set to update many-to-many relationship
                external_self_service.vilka_byggnader_omfattas.set(buildings_data)

            # Check for nested updates
            if 'kontaktuppgifter_till_ansvarig_leverantor' in request.data:
                provider_data = request.data.pop('kontaktuppgifter_till_ansvarig_leverantor')
                
                if external_self_service.kontaktuppgifter_till_ansvarig_leverantor:
                    provider_serializer = SelfServiceProviderSerializer(
                        external_self_service.kontaktuppgifter_till_ansvarig_leverantor,
                        data=provider_data,
                        partial=True
                    )
                else:
                    provider_serializer = SelfServiceProviderSerializer(data=provider_data)
                    
                if provider_serializer.is_valid():
                    provider_serializer.save()
                else:
                    return Response(provider_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Now update the main ExternalSelfServices instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentFolderCreateAPIView(generics.CreateAPIView):
    queryset = ServiceDocumentFolder.objects.all()
    serializer_class = ServiceDocumentFolderSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentFolderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceDocumentFolder.objects.all()
    serializer_class = ServiceDocumentFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentCreateAPIView(generics.CreateAPIView):
    queryset = ServiceDocument.objects.all()
    serializer_class = ServiceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Add parsers to handle multipart data

    def perform_create(self, serializer):
        # Ensure folder exists and attach document to folder
        folder_id = self.request.data.get('folder_id')
        try:
            folder = ServiceDocumentFolder.objects.get(id=folder_id)
            serializer.save(folder=folder)
        except ServiceDocumentFolder.DoesNotExist:
            raise serializers.ValidationError({'folder': 'Folder does not exist.'})


class DocumentRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ServiceDocument.objects.all()
    serializer_class = ServiceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

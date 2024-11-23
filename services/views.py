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
from property.models import Property
from users.models import ServiceProvider
from users.serializers import ServiceProviderSerializer
from decimal import Decimal

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
            for file in files:
                image_serializer = OrderServiceFileSerializer(data={"folder": folder_instance.id, "file": file})
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListOrderMaintenanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status', 'Pending')
        
        if request.user.role == "ADMIN":
            order_service = OrderMaintenanceServices.objects.filter(status=status_filter)
        else:
            order_service = OrderMaintenanceServices.objects.filter(user=request.user, status=status_filter)

        serializer = OrderMaintenanceServicesSerializer(order_service, many=True)

        maintenance_ids = [data['maintenance'] for data in serializer.data]
        property_ids = [prop.id for data in serializer.data for prop in Property.objects.filter(id__in=data['properties'])]

        # Prefetch Maintenance and Properties
        maintenance_objects = Maintenance.objects.filter(id__in=maintenance_ids)
        property_objects = Property.objects.filter(id__in=property_ids)

        result = []
        maintenance_dict = {maintenance.id: MaintainceSerializer(maintenance).data for maintenance in maintenance_objects}
        property_dict = {property.id: PropertySerializer(property).data for property in property_objects}
        total_property_count = Property.objects.filter(user=request.user).count()

        total_cost = 0  # To track the total cost

        for data in serializer.data:
            # Calculate cost for each maintenance service
            maintenance_id = data['maintenance']
            maintenance = maintenance_dict.get(maintenance_id, None)
            if maintenance:
                total_cost += Decimal(maintenance['price'])  # Sum up prices
            
            data['maintenance'] = maintenance
            data['properties'] = [property_dict.get(prop_id) for prop_id in data['properties']]
            data['total_property_count'] = total_property_count

            if data['service_provider']:
                service_provider = ServiceProvider.objects.filter(id=data['service_provider']).first()
                if service_provider:
                    data['service_provider'] = ServiceProviderSerializer(service_provider).data
                else:
                    data['service_provider'] = None
            else:
                data['service_provider'] = None

            result.append(data)

        # Add total cost to the response
        response_data = {
            'results': result,
            'total_cost': total_cost
        }

        return Response(response_data, status=status.HTTP_200_OK)

class RetrieveOrderMaintenanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        # Retrieve the order maintenance service by its primary key (ID)
        order_service = get_object_or_404(OrderMaintenanceServices, pk=pk)

        # Check if the user is allowed to retrieve this service
        if request.user.role != "ADMIN" and order_service.user != request.user:
            return Response({"detail": "Not authorized to view this service."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the service data
        serializer = OrderMaintenanceServicesSerializer(order_service)

        # Prefetch related data
        maintenance_obj = order_service.maintenance
        maintenance_data = MaintainceSerializer(maintenance_obj).data if maintenance_obj else None

        properties_objs = order_service.properties.all()
        properties_data = [PropertySerializer(prop).data for prop in properties_objs]

        service_provider_obj = order_service.service_provider
        service_provider_data = ServiceProviderSerializer(service_provider_obj).data if service_provider_obj else None

        # Get total property count for the user
        total_property_count = Property.objects.filter(user=request.user).count()

        # Build the result response
        result = serializer.data
        result['maintenance'] = maintenance_data
        result['properties'] = properties_data
        result['service_provider'] = service_provider_data
        result['total_property_count'] = total_property_count

        return Response(result, status=status.HTTP_200_OK)


class UpdateOrderMaintenanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        order_service = get_object_or_404(OrderMaintenanceServices, pk=pk)        
        serializer = OrderMaintenanceServicesSerializer(order_service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DeleteOrderMaintenanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        order_service = get_object_or_404(OrderMaintenanceServices, pk=pk)
        order_service.delete()
        return Response({'message': 'service deleted'},status=status.HTTP_204_NO_CONTENT)

class ListOrderServiceFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, order_service):
        folders = OrderServiceDocumentFolder.objects.filter(order_service=order_service)
        serializer = OrderServiceDocumentFolderSerializer(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateOrderServiceFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = OrderServiceDocumentFolderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateOrderServiceFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, id):
        folder = get_object_or_404(OrderServiceDocumentFolder, id=id)
        serializer = OrderServiceDocumentFolderSerializer(folder, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteOrderServiceFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        folder = get_object_or_404(OrderServiceDocumentFolder, id=id)
        folder.delete()
        return Response({'message': 'Folder deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CreateOrderServiceFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = OrderServiceFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteOrderServiceFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        try:
            file = OrderServiceFile.objects.get(id=pk)
        except OrderServiceFile.DoesNotExist:
            raise Http404("file not found.")
        file.delete()
        return Response({"msg": "File Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)

class ListOrderServiceFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, folder_id):
        try:
            folder = OrderServiceDocumentFolder.objects.get(id=folder_id)
            files = OrderServiceFile.objects.filter(folder=folder)
            serializer = ServiceFileSerializer(files, many=True)        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrderServiceDocumentFolder.DoesNotExist:
            raise Http404("folder not found.")
        
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Calculate total cost for the authenticated user
        total_cost = sum(
            float(service.kostnad_per_manad) for service in queryset if service.kostnad_per_manad.isdigit()
        )

        # Include total cost in the response
        return Response({
            "total_cost": total_cost,
            "results": serializer.data
        })

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
    """This view is used for upload manual service file and service cover image"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        manual_service = request.data.get('manual_service')
        files = request.FILES.getlist('file')
        cover_image = request.FILES.get('cover_image', None)

        if not manual_service:
            return Response({'error': 'Manual service ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create folder instance for document
        folder_serializer = ServiceDocumentFolderSerializer(data={'manual_service': manual_service, "name": "Dokument"})
        folder_serializer.is_valid(raise_exception=True)
        folder_instance = folder_serializer.save()

        # Save each file in the folder
        for file in files:
            document_serializer = ServiceFileSerializer(data={'folder': folder_instance.id, 'file': file})
            document_serializer.is_valid(raise_exception=True)
            document_serializer.save()

        # Update cover image if provided
        if cover_image:
            service_instance = ExternalSelfServices.objects.get(id=manual_service)
            service_instance.cover_image = cover_image
            service_instance.save()

            message = 'Files and cover image uploaded successfully.'
        else:
            message = 'Files uploaded successfully.'

        return Response({'msg': message}, status=status.HTTP_201_CREATED)

class CombinedServicesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get External Self Service data
        external_services = ExternalSelfServices.objects.filter(user=request.user).order_by('-created_at')
        external_service_serializer = ExternalSelfServicesSerializer(external_services, many=True, context={'request': request})
        
        # Calculate total cost for external services
        total_external_cost = sum(
            float(service['kostnad_per_manad']) for service in external_service_serializer.data if str(service['kostnad_per_manad']).isdigit()
        )
        order_service = OrderMaintenanceServices.objects.filter(user=request.user, status="Active")
        
        order_service_serializer = OrderMaintenanceServicesSerializer(order_service, many=True)

        maintenance_ids = [data['maintenance'] for data in order_service_serializer.data]
        property_ids = [
            prop.id for data in order_service_serializer.data for prop in Property.objects.filter(id__in=data['properties'])
        ]
        
        # Prefetch Maintenance and Properties
        maintenance_objects = Maintenance.objects.filter(id__in=maintenance_ids)
        property_objects = Property.objects.filter(id__in=property_ids)

        maintenance_dict = {maintenance.id: MaintainceSerializer(maintenance).data for maintenance in maintenance_objects}
        property_dict = {property.id: PropertySerializer(property).data for property in property_objects}

        total_property_count = Property.objects.filter(user=request.user).count()

        total_order_cost = 0  # To track the total cost of orders
        combined_result = []
        
        # Add order maintenance data
        for data in order_service_serializer.data:
            maintenance_id = data['maintenance']
            maintenance = maintenance_dict.get(maintenance_id, None)
            if maintenance:
                total_order_cost += Decimal(maintenance['price'])  # Sum up prices
                
            data['maintenance'] = maintenance
            data['properties'] = [property_dict.get(prop_id) for prop_id in data['properties']]
            data['total_property_count'] = total_property_count

            if data['service_provider']:
                service_provider = ServiceProvider.objects.filter(id=data['service_provider']).first()
                if service_provider:
                    data['service_provider'] = ServiceProviderSerializer(service_provider).data
                else:
                    data['service_provider'] = None
            else:
                data['service_provider'] = None

            combined_result.append(data)
        
        # Combine the results from both ExternalSelfServices and OrderMaintenanceServices
        combined_data = {
            "total_external_cost": total_external_cost,
            "external_services": external_service_serializer.data,
            "total_order_cost": total_order_cost,
            "order_maintenance": combined_result,
            "sum": total_external_cost + total_order_cost
        }
        
        return Response(combined_data, status=status.HTTP_200_OK)

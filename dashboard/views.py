from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from property.models import Property
from services.models import UserMaintenanceServices
from rest_framework.permissions import IsAuthenticated
from users.serializers import ServiceProviderSerializer
from django.db.models import Sum
from services.models import UserMaintenanceServices

# Create your views here.


class UserDashboardstatusCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(user=request.user)
        
        # Count the number of buildings
        building_count = properties.count()

        # Sum the total number of apartments across all buildings
        total_apartments = properties.aggregate(
            total_apartments=Sum('antal_bostäder')
        )['total_apartments'] or 0

        # Filter active maintenance services
        active_maintenance_services = UserMaintenanceServices.objects.filter(
            user=request.user, status="Active"
        )

        # Count active maintenance services
        active_maintenance_count = active_maintenance_services.count()

        # Calculate the fixed maintenance cost (sum of prices of active services)
        fixed_cost = active_maintenance_services.aggregate(
            total_cost=Sum('maintenance__price')
        )['total_cost'] or 0

        data = {
            "buildings": building_count,
            "appartments": total_apartments,
            "active_maintenance": active_maintenance_count,
            "fixed_maintenance": fixed_cost,
        }
        return Response(data, status=status.HTTP_200_OK)


class UserDashboardServiceProvider(APIView):
    def get(self, request):
        # Query UserMaintenanceServices to get active services for the current user
        active_services = UserMaintenanceServices.objects.filter(
            user=request.user,
            status="Active",
            service_provider__isnull=False,  # Exclude instances where service_provider is null
        ).select_related("service_provider")

        # Collect unique service provider instances
        unique_service_providers = set(
            service.service_provider for service in active_services
        )

        # Serialize the unique service provider instances
        serializer = ServiceProviderSerializer(unique_service_providers, many=True)

        return Response(serializer.data)

class DashboardTable(APIView):
    def get(self, request):
        pass
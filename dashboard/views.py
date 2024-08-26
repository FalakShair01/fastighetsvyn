from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from property.models import Property
from django.db.models import Count, Sum
from services.models import Maintenance, UserMaintenanceServices
from rest_framework.permissions import IsAuthenticated
from users.serializers import ServiceProviderSerializer

# Create your views here.

class UserDashboardstatusCount(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        properties_count = Property.objects.filter(user=request.user).count()

        # yta_sum = Property.objects.filter(user=request.user).aggregate(total_yta=Sum('yta'))['total_yta'] or 0
        # active_services = UserMaintenanceServices.objects.filter(user=request.user, status='Active')

        # Initialize total price
        ongoing_cost = 0

        # Iterate over active services and sum up their prices
        # for service in active_services:
            # ongoing_cost += service.maintenance.price
        
        data = {
            'total_properties': properties_count,
            'area': 10000,
            'ongoing_cost': ongoing_cost
        }
        return Response(data, status=status.HTTP_200_OK)
    
class UserDashboardServiceProvider(APIView):
    def get(self, request):
        # Query UserMaintenanceServices to get active services for the current user
        active_services = UserMaintenanceServices.objects.filter(
            user=request.user,
            status='Active',
            service_provider__isnull=False  # Exclude instances where service_provider is null
        ).select_related('service_provider')

        # Collect unique service provider instances
        unique_service_providers = set(service.service_provider for service in active_services)

        # Serialize the unique service provider instances
        serializer = ServiceProviderSerializer(unique_service_providers, many=True)

        return Response(serializer.data)
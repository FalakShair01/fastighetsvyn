from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from property.models import Property
from django.db.models import Count, Sum
from services.models import Maintenance, UserMaintenanceServices
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserDashboardstatusCount(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        properties_count = Property.objects.filter(user=request.user).count()

        yta_sum = Property.objects.aggregate(total_yta=Sum('yta'))['total_yta'] or 0
        active_services = UserMaintenanceServices.objects.filter(user=request.user, status='Active')

        # Initialize total price
        ongoing_cost = 0

        # Iterate over active services and sum up their prices
        for service in active_services:
            ongoing_cost += service.maintenance.price
        
        data = {
            'total_properties': properties_count,
            'area': yta_sum,
            'ongoing_cost': ongoing_cost
        }
        return Response(data, status=status.HTTP_200_OK)
from django_filters import rest_framework as filters
from .models import UserDevelopmentServices, UserMaintenanceServices, Maintenance, Development

class UserDevelopmentFilter(filters.FilterSet):
    class Meta:
        model = UserDevelopmentServices
        fields = {
            'status': ['exact']
        }


class UserMaintenanceFilter(filters.FilterSet):
    class Meta:
        model = UserMaintenanceServices
        fields = {
            'status': ['exact']
        }


class DevelopmentFilter(filters.FilterSet):
    class Meta:
        model = Development
        fields ={
            'type' : ['in', 'exact']
        }
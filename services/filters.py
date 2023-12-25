from django_filters import rest_framework as filters
from .models import UserDevelopmentServices, UserMaintenanceServices


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
from django_filters import rest_framework as filters
from .models import UserDevelopmentServices, UserMaintenanceServices, Maintenance, Development
from property.models import Property

class UserDevelopmentFilter(filters.FilterSet):
    class Meta:
        model = UserDevelopmentServices
        fields = {
            'status': ['exact']
        }


class UserMaintenanceFilter(filters.FilterSet):
    properties = filters.ModelMultipleChoiceFilter(
        field_name='properties',
        queryset=Property.objects.all(),
        to_field_name='id',
    )

    class Meta:
        model = UserMaintenanceServices
        fields = {
            'status': ['exact'],
            'properties': ['exact'],
        }

class DevelopmentFilter(filters.FilterSet):
    class Meta:
        model = Development
        fields ={
            'type' : ['in', 'exact', 'icontains']
        }
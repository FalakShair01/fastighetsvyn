from django_filters import rest_framework as filters
from .models import (
    UserDevelopmentServices,
    OrderMaintenanceServices,
    Development,
    Maintenance
)
from property.models import Property


class UserDevelopmentFilter(filters.FilterSet):
    class Meta:
        model = UserDevelopmentServices
        fields = {"status": ["exact"]}

class MaintenanceFilter(filters.FilterSet):
    class Meta:
        model = Maintenance
        fields = {"is_admin": ["exact"]}

class OrderMaintenanceFilter(filters.FilterSet):
    properties = filters.ModelMultipleChoiceFilter(
        field_name="properties",
        queryset=Property.objects.all(),
        to_field_name="id",
    )

    class Meta:
        model = OrderMaintenanceServices
        fields = {
            "status": ["exact"],
            "properties": ["exact"],
        }


class DevelopmentFilter(filters.FilterSet):
    class Meta:
        model = Development
        fields = {"type": ["in", "exact", "icontains"]}

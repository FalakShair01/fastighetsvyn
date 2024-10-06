from django_filters import rest_framework as filters
from .models import Tenant


class TenantFilter(filters.FilterSet):
    class Meta:
        model = Tenant
        fields = {
            "name": ["in", "exact"],
            "property": ["in", "exact"],
            "email": ["in", "exact"],
            "phone": ["in", "exact"],
            "comment": ["in", "exact"],
        }

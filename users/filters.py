from django_filters import rest_framework as filters
from .models import Tenant


class TenantFilter(filters.FilterSet):
    class Meta:
        model = Tenant
        fields = {
            "name": ["in"],
            "property": ["in"],
            "email": ["exact"],
            "phone": ["in"],
            "comment": ["in"],
        }

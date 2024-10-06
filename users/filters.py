from django_filters import rest_framework as filters
from .models import Tenant

class TenantFilter(filters.FilterSet):
    email = filters.CharFilter(method='filter_by_emails')
    property = filters.CharFilter(method='filter_by_properties')

    class Meta:
        model = Tenant
        fields = {
            "name": ["in", "exact"],
            "property": ["exact"],  # Use exact for single property filtering.
            "email": ["exact"],
            "phone": ["in", "exact"],
            "comment": ["in", "exact"],
        }

    def filter_by_emails(self, queryset, name, value):
        emails = value.split(',')
        return queryset.filter(email__in=emails)

    def filter_by_properties(self, queryset, name, value):
        properties = value.split(',')
        return queryset.filter(property__id__in=properties)

from django_filters import rest_framework as filters
from .models import Tenant


class TenantFilter(filters.FilterSet):
    email = filters.CharFilter(method='filter_by_emails')

    class Meta:
        model = Tenant
        fields = {
            "name": ["in", "exact"],
            "property": ["in", "exact"],
            "email": ["exact"], 
            "phone": ["in", "exact"],
            "comment": ["in", "exact"],
        }

    def filter_by_emails(self, queryset, name, value):
        emails = value.split(',')
        return queryset.filter(email__in=emails)

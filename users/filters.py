from django_filters import rest_framework as filters
from .models import Tenant

class TenantFilter(filters.FilterSet):
    email = filters.CharFilter(method='filter_by_emails')
    property = filters.CharFilter(method='filter_by_properties')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # Allow partial match for name
    phone = filters.CharFilter(method='filter_by_phone')  # Custom method for phone
    comment = filters.CharFilter(method='filter_by_comments')  # Custom method for comments

    class Meta:
        model = Tenant
        fields = {
            "property": ["exact"],  # Use exact for single property filtering.
            "email": ["exact"],
        }

    def filter_by_emails(self, queryset, name, value):
        emails = value.split(',')
        return queryset.filter(email__in=emails)

    def filter_by_properties(self, queryset, name, value):
        properties = value.split(',')
        return queryset.filter(property__id__in=properties)

    def filter_by_phone(self, queryset, name, value):
        phones = value.split(',')
        return queryset.filter(phone__in=phones) 

    def filter_by_comments(self, queryset, name, value):
        return queryset.filter(comment__icontains=value) 

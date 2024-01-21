from django_filters import rest_framework as filters
from .models import AdminNotifications

class IsNotificationsRead(filters.FilterSet):
    class Meta:
        model = AdminNotifications
        fields = {
            'is_read': ['exact']
        }


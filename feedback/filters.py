from .models import AdminFeedback, TenantsFeedback
from django_filters import rest_framework as filters

class MarkAsDoneFilter(filters.FilterSet):
    class Meta:
        model = AdminFeedback
        fields  ={
            'is_done': ['exact']
        }


class UserFeedbackMarkAsDoneFilter(filters.FilterSet):
    class Meta:
        model = TenantsFeedback
        fields  ={
            'is_done': ['exact']
        }
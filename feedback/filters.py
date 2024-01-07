from .models import AdminFeedback
from django_filters import rest_framework as filters

class MarkAsDoneFilter(filters.FilterSet):
    class Meta:
        model = AdminFeedback
        fields  ={
            'is_done': ['exact']
        }
from .models import AdminFeedback, UserFeedback
from django_filters import rest_framework as filters


class MarkAsDoneFilter(filters.FilterSet):
    class Meta:
        model = AdminFeedback
        fields = {"is_done": ["exact"], "is_archive": ["exact"]}


class UserFeedbackMarkAsDoneFilter(filters.FilterSet):
    class Meta:
        model = UserFeedback
        fields = {"is_done": ["exact"], "is_archive": ["exact"]}

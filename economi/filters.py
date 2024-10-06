from django_filters import rest_framework as filters
from .models import Expense
from property.models import Property

class ExpenseFilter(filters.FilterSet):
    # start_date = filters.DateFilter(field_name="date_of_transaction", lookup_expr='gte')
    # end_date = filters.DateFilter(field_name="date_of_transaction", lookup_expr='lte')
    type_of_transaction = filters.CharFilter(lookup_expr='icontains')
    type_of_cost_or_revenue = filters.CharFilter(lookup_expr='icontains')
    account = filters.CharFilter(lookup_expr='icontains')
    building = filters.ModelMultipleChoiceFilter(queryset=Property.objects.all())  # Allow multiple buildings

    class Meta:
        model = Expense
        fields = [
            'type_of_transaction',
            'type_of_cost_or_revenue',
            'account',
            'building',
            # 'start_date',
            # 'end_date'
        ]

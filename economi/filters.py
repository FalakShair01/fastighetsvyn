from django_filters import rest_framework as filters
from .models import Expense
from property.models import Property


class ExpenseFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date_of_transaction", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date_of_transaction", lookup_expr='lte')
    type_of_transaction = filters.CharFilter(field_name='type_of_transaction', lookup_expr='icontains')
    type_of_cost_or_revenue = filters.CharFilter(field_name='type_of_cost_or_revenue', lookup_expr='icontains')
    account = filters.CharFilter(field_name='account', lookup_expr='in')  # Use __in lookup for multiple accounts
    building = filters.ModelMultipleChoiceFilter(queryset=Property.objects.all(), to_field_name='id')  # Allow multiple buildings
    total_sum = filters.BaseInFilter(field_name='total_sum')  # Allows filtering by multiple total_sum values
    value_added_tax = filters.BaseInFilter(field_name='value_added_tax')  # Allows filtering by multiple VAT values
    comment = filters.CharFilter(field_name='comment', lookup_expr='icontains')

    class Meta:
        model = Expense
        fields = [
            'type_of_transaction',
            'type_of_cost_or_revenue',
            'account',
            'building',
            'start_date',
            'end_date',
            'total_sum',
            'value_added_tax',
            'comment',
        ]


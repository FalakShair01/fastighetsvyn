from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from property.models import Property
import pandas as pd
from datetime import datetime


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'building', 'type_of_transaction']


    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date_of_transaction__range=[start_date, end_date])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]


class BalanceIllustrationView(APIView):
    def get(self, request):
        # Retrieve the year from the query parameters, default to the current year
        year = request.query_params.get('year', timezone.now().year)
        
        try:
            year = int(year)
        except ValueError:
            return Response({'error': 'Invalid year'}, status=400)
        
        # Filter expenses by the specified year using timezone-aware dates
        start_date = timezone.make_aware(timezone.datetime(year, 1, 1))
        end_date = timezone.make_aware(timezone.datetime(year + 1, 1, 1))
        
        # Aggregate the total cost with case-insensitive filtering and year filter
        total_cost = Expense.objects.filter(
            type_of_transaction__iexact='cost',
            date_of_transaction__range=(start_date, end_date)
        ).aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        
        # Aggregate the total revenue with case-insensitive filtering and year filter
        total_revenue = Expense.objects.filter(
            type_of_transaction__iexact='revenue',
            date_of_transaction__range=(start_date, end_date)
        ).aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        
        # Return the results as a JSON response
        return Response({
            'total_cost': total_cost,
            'total_revenue': total_revenue
        })
    
# class YearlyExpenseView(APIView):
#     def get(self, request):
#         # Get current year or specify the year if needed
#         year = request.query_params.get('year', timezone.now().year)

#         # List of types to include in the response
#         # types_of_interest = ['Energy', 'Water', 'Rent', 'Maintenance']
#         types_of_interest = ['Energi', 'Vatten', 'Totala utgifter', 'Intäkter']

#         # Filter and aggregate data
#         data = (
#             Expense.objects
#             .filter(date_of_transaction__year=year, type_of_cost_or_revenue__in=types_of_interest)
#             .annotate(month=TruncMonth('date_of_transaction'))
#             .values('month', 'type_of_cost_or_revenue')
#             .annotate(total_amount=Sum('total_sum'))
#             .order_by('month', 'type_of_cost_or_revenue')
#         )

#         # Prepare data for chart
#         monthly_data = {}
#         for item in data:
#             month = item['month'].strftime('%Y-%m')  # Format month as 'YYYY-MM'
#             if month not in monthly_data:
#                 monthly_data[month] = {type_name: 0 for type_name in types_of_interest}

#             monthly_data[month][item['type_of_cost_or_revenue']] = item['total_amount']

#         # Convert to lists for charting
#         labels = sorted(monthly_data.keys())
#         series_data = [
#             {
#                 'name': type_name,
#                 'data': [monthly_data.get(month, {}).get(type_name, 0) for month in labels]
#             }
#             for type_name in types_of_interest
#         ]

#         return Response({
#             'labels': labels,
#             'series': series_data
#         })


class YearlyExpenseView(APIView):
    def get(self, request):
        year = request.query_params.get('year', timezone.now().year)
        try:
            year = int(year)  # Ensure year is an integer
        except ValueError:
            year = timezone.now().year
        # List of types to include in the response
        types_of_interest = ['Energi', 'Vatten', 'Totala utgifter', 'Intäkter']

        # Generate a list of all months in the year with custom formatting
        all_months = [datetime(year, month, 1).strftime('%b \'%y') for month in range(1, 13)]

        # Filter and aggregate data
        data = (
            Expense.objects
            .filter(date_of_transaction__year=year, type_of_cost_or_revenue__in=types_of_interest)
            .annotate(month=TruncMonth('date_of_transaction'))
            .values('month', 'type_of_cost_or_revenue')
            .annotate(total_amount=Sum('total_sum'))
            .order_by('month', 'type_of_cost_or_revenue')
        )

        # Initialize data for each type and month
        monthly_data = {month: {type_name: 0 for type_name in types_of_interest} for month in all_months}

        # Populate data from the query
        for item in data:
            month = item['month'].strftime('%b \'%y')
            monthly_data[month][item['type_of_cost_or_revenue']] = item['total_amount']

        # Convert to lists for charting
        labels = all_months
        series_data = [
            {
                'name': type_name,
                'data': [monthly_data[month].get(type_name, 0) for month in labels]
            }
            for type_name in types_of_interest
        ]

        return Response({
            'labels': labels,
            'series': series_data
        })


class ImportExpensesView(APIView):
    def post(self, request, *args, **kwargs):
        
        file = request.FILES['file']
        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file)

            # Check if necessary columns exist in the DataFrame
            required_columns = ['type_of_transaction', 'type_of_cost_or_revenue', 'date_of_transaction', 'total_sum', 'value_added_tax', 'account', 'building', 'comment']
            if not all(column in df.columns for column in required_columns):
                return Response({'detail': 'Missing required columns in the uploaded file.'}, status=status.HTTP_400_BAD_REQUEST)

            # Iterate through the rows of the dataframe
            for _, row in df.iterrows():
                try:
                # Get Property object
                    building = Property.objects.get(byggnad__iexact=row['building'])
                except Property.DoesNotExist:
                    building = None

                # Create Expense object
                Expense.objects.create(
                    user=request.user,  # Assuming the user is the logged-in user
                    type_of_transaction=row['type_of_transaction'],
                    type_of_cost_or_revenue=row['type_of_cost_or_revenue'],
                    date_of_transaction=row['date_of_transaction'],
                    total_sum=row['total_sum'],
                    value_added_tax=row['value_added_tax'],
                    account=row['account'],
                    building=building,
                    comment=row['comment'],
                    attachment=None  # Handle attachments as needed
                )

            return Response({'detail': 'Expenses imported successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Error processing file: {e}'}, status=status.HTTP_400_BAD_REQUEST)

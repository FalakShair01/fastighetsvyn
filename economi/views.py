from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from property.models import Property
import pandas as pd
from django.utils.timezone import make_aware, make_naive
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from .filters import ExpenseFilter
from django.utils.dateparse import parse_date
from decimal import Decimal


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user).order_by('-date_of_transaction')  
        # start_date = self.request.query_params.get("start_date")
        # end_date = self.request.query_params.get("end_date")

        # if start_date and end_date:
        #     queryset = queryset.filter(
        #         date_of_transaction__range=[start_date, end_date]
        #     )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

class BalanceIllustrationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Parse start_date and end_date from query params, if available
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Convert start_date and end_date to date objects if provided, otherwise None
        if start_date_str:
            start_date = parse_date(start_date_str)
        else:
            start_date = None
        
        if end_date_str:
            end_date = parse_date(end_date_str)
        else:
            end_date = None

        # Get the distinct months where the user has any transaction
        if start_date and end_date:
            months_with_data = Expense.objects.filter(user=user, date_of_transaction__range=[start_date, end_date]) \
                .annotate(month=TruncMonth('date_of_transaction')).values('month').distinct().count()
        else:
            months_with_data = Expense.objects.filter(user=user).annotate(
                month=TruncMonth('date_of_transaction')
            ).values('month').distinct().count()

        # Current month
        current_month = date.today().replace(day=1)

        # Calculate total and monthly average for 'Cost' with date filter if available
        cost_expenses = Expense.objects.filter(user=user, type_of_transaction='Cost')
        if start_date and end_date:
            cost_expenses = cost_expenses.filter(date_of_transaction__range=[start_date, end_date])

        cost_monthly_data = cost_expenses.annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(
            total_sum=Sum('total_sum')
        ).order_by('month')

        total_cost_sum = cost_monthly_data.aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        
        if months_with_data > 0:
            cost_monthly_average = total_cost_sum / months_with_data
        else:
            cost_monthly_average = 0

        # Calculate total and monthly average for 'Revenue' with date filter if available
        revenue_expenses = Expense.objects.filter(user=user, type_of_transaction='Revenue')
        if start_date and end_date:
            revenue_expenses = revenue_expenses.filter(date_of_transaction__range=[start_date, end_date])

        revenue_monthly_data = revenue_expenses.annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(
            total_sum=Sum('total_sum')
        ).order_by('month')

        total_revenue_sum = revenue_monthly_data.aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        
        if months_with_data > 0:
            revenue_monthly_average = total_revenue_sum / months_with_data
        else:
            revenue_monthly_average = 0

        # Get current month's total for Cost
        current_month_cost = cost_expenses.filter(date_of_transaction__month=current_month.month).aggregate(
            total_sum=Sum('total_sum')
        )['total_sum'] or 0

        # Get current month's total for Revenue
        current_month_revenue = revenue_expenses.filter(date_of_transaction__month=current_month.month).aggregate(
            total_sum=Sum('total_sum')
        )['total_sum'] or 0

        # Calculate the percentage for Cost
        if cost_monthly_average > 0:
            cost_percentage = (current_month_cost / cost_monthly_average) * 100
            cost_percentage = min(cost_percentage, 100)  # Cap at 100%
        else:
            cost_percentage = 0

        # Calculate the percentage for Revenue
        if revenue_monthly_average > 0:
            revenue_percentage = (current_month_revenue / revenue_monthly_average) * 100
            revenue_percentage = min(revenue_percentage, 100)  # Cap at 100%

            # Subtract 0.1 from the percentage if it is exactly 100
            if revenue_percentage == cost_percentage:
                revenue_percentage -= Decimal('0.1')
        else:
            revenue_percentage = 0

        # Return the result as a JSON response
        return Response({
            'total_cost': round(cost_percentage, 2), # percentage_of_current_month
            'total_revenue': round(revenue_percentage, 2),  # percentage_of_current_month
            'cost_monthly_average': round(cost_monthly_average, 2),
            'revenue_monthly_average': round(revenue_monthly_average, 2),
            'total_cost_sum': current_month_cost,
            'total_revenue_sum': current_month_revenue,
            'sum': current_month_cost + current_month_revenue
        })
   # return Response({
        #     'cost': {
        #         'total_sum': total_cost_sum,
        #         'months_with_data': months_with_data,
        #         'monthly_average': round(cost_monthly_average, 2),
        #         'current_month_total': round(current_month_cost, 2),
        #         'percentage_of_current_month': round(cost_percentage, 2)  # Percentage to be used in circle
        #     },
        #     'revenue': {
        #         'total_sum': total_revenue_sum,
        #         'months_with_data': months_with_data,
        #         'monthly_average': round(revenue_monthly_average, 2),
        #         'current_month_total': round(current_month_revenue, 2),
        #         'percentage_of_current_month': round(revenue_percentage, 2)  # Percentage to be used in circle
        #     }
        # })


class YearlyExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get start_date and end_date from query parameters, if provided
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Parse dates or set default values (last 12 months)
        if start_date_str:
            start_date = timezone.datetime.fromisoformat(start_date_str)
            if timezone.is_aware(start_date):
                start_date = timezone.make_naive(start_date)
        else:
            start_date = timezone.now() - timedelta(days=365)  # Default to approx. last 12 months
            start_date = timezone.make_naive(start_date)

        if end_date_str:
            end_date = timezone.datetime.fromisoformat(end_date_str)
            if timezone.is_aware(end_date):
                end_date = timezone.make_naive(end_date)
        else:
            end_date = timezone.now()  # Default to the current date
            end_date = timezone.make_naive(end_date)

        # Map of Swedish month names
        month_map = {
            "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "May": "Maj",
            "Jun": "Jun", "Jul": "Jul", "Aug": "Aug", "Sep": "Sep", "Oct": "Okt",
            "Nov": "Nov", "Dec": "Dec"
        }

        # Generate month labels in Swedish from start_date to end_date
        all_months = []
        current_month = start_date.replace(day=1)
        while current_month <= end_date.replace(day=1):
            month_abbr = current_month.strftime("%b")
            swedish_month_label = f"{month_map[month_abbr]} '{current_month.strftime('%y')}"
            all_months.append(swedish_month_label)
            current_month += relativedelta(months=1)

        # List of types to include in the response
        types_of_interest = ["Energi", "Vatten", "Totala utgifter", "Intäkter"]

        # Base queryset for filtering expenses within the date range
        base_queryset = Expense.objects.filter(
            user=request.user,
            date_of_transaction__range=[start_date, end_date]
        ).annotate(
            month=TruncMonth("date_of_transaction")
        ).values("month", "type_of_cost_or_revenue", "type_of_transaction").annotate(total_amount=Sum("total_sum"))

        # Initialize data for each type and month
        monthly_data = {
            month: {type_name: 0 for type_name in types_of_interest}
            for month in all_months
        }

        # Populate data for each type and month
        for item in base_queryset:
            month_abbr = item["month"].strftime("%b")
            month = f"{month_map[month_abbr]} '{item['month'].strftime('%y')}"
            type_of_cost_or_revenue = item["type_of_cost_or_revenue"]
            type_of_transaction = item["type_of_transaction"]

            if month in monthly_data:
                if type_of_cost_or_revenue in ["Energi", "Vatten"]:
                    monthly_data[month][type_of_cost_or_revenue] += item["total_amount"]

                # Map "Cost" to "Totala utgifter" and "Revenue" to "Intäkter"
                if type_of_transaction == "Cost":
                    monthly_data[month]["Totala utgifter"] += item["total_amount"]
                elif type_of_transaction == "Revenue":
                    monthly_data[month]["Intäkter"] += item["total_amount"]

        # Convert data to lists for charting
        series_data = [
            {
                "name": type_name,
                "data": [monthly_data[month].get(type_name, 0) for month in all_months],
            }
            for type_name in types_of_interest
        ]

        return Response({"labels": all_months, "series": series_data})

class ImportExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            if "file" not in request.FILES:
                return Response(
                    {"detail": "No file provided in the request."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Assuming the file is uploaded as a CSV
            file = request.FILES["file"]
            file_extension = file.name.split(".")[-1].lower()

            if file_extension == "csv":
                # Read the CSV file
                df = pd.read_csv(file)
            elif file_extension in ["xls", "xlsx"]:
                # Read the Excel file
                df = pd.read_excel(file)
            else:
                return Response(
                    {"detail": "Unsupported file format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if necessary columns exist in the DataFrame
            required_columns = [
                "type_of_transaction",
                "type_of_cost_or_revenue",
                "date_of_transaction",
                "total_sum",
                "value_added_tax",
                "account",
                "building",
                "comment",
            ]
            if not all(column in df.columns for column in required_columns):
                return Response(
                    {"detail": "Missing required columns in the uploaded file."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Iterate through the rows of the dataframe
            for _, row in df.iterrows():
                try:
                    # Get Property object
                    building = Property.objects.get(byggnad__iexact=row["building"])
                except Property.DoesNotExist:
                    building = None

                # Create Expense object
                Expense.objects.create(
                    user=request.user,  # Assuming the user is the logged-in user
                    type_of_transaction=row["type_of_transaction"],
                    type_of_cost_or_revenue=row["type_of_cost_or_revenue"],
                    date_of_transaction=row["date_of_transaction"],
                    total_sum=row["total_sum"],
                    value_added_tax=row["value_added_tax"],
                    account=row["account"],
                    building=building,
                    comment=row["comment"],
                    attachment=None,  # Handle attachments as needed
                )

            return Response(
                {"detail": "Expenses imported successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": f"Error processing file: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

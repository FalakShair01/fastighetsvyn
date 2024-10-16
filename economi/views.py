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
from datetime import datetime, date
from .filters import ExpenseFilter

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user)
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
        
        # Get all distinct months where the user has any transaction
        months_with_data = Expense.objects.filter(user=user).annotate(
            month=TruncMonth('date_of_transaction')
        ).values('month').distinct().count()

        # Current month
        current_month = date.today().replace(day=1)

        # Calculate total and monthly average for 'Cost'
        cost_expenses = Expense.objects.filter(user=user, type_of_transaction='Cost')
        cost_monthly_data = cost_expenses.annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(
            total_sum=Sum('total_sum')
        ).order_by('month')
        
        total_cost_sum = cost_monthly_data.aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        
        if months_with_data > 0:
            cost_monthly_average = total_cost_sum / months_with_data
        else:
            cost_monthly_average = 0

        # Calculate total and monthly average for 'Revenue'
        revenue_expenses = Expense.objects.filter(user=user, type_of_transaction='Revenue')
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
        else:
            revenue_percentage = 0

        # Return the result as a JSON response
        return Response({
            'total_cost': round(cost_percentage, 2), # percentage_of_current_month
            'total_revenue': round(revenue_percentage, 2),  # percentage_of_current_month
            'cost_monthly_average': round(cost_monthly_average, 2),
            'revenue_monthly_average': round(revenue_monthly_average, 2),
            'total_cost_sum': total_cost_sum,
            'total_revenue_sum': total_revenue_sum,
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
        year = request.query_params.get("year", timezone.now().year)
        try:
            year = int(year)  # Ensure year is an integer
        except ValueError:
            year = timezone.now().year

        # List of types to include in the response
        types_of_interest = ["Energi", "Vatten", "Totala utgifter", "Intäkter"]

        # Generate a list of all months in the year with custom formatting
        all_months = [
            datetime(year, month, 1).strftime("%b '%y") for month in range(1, 13)
        ]

        # Base queryset for filtering expenses in the specified year
        base_queryset = Expense.objects.filter(
            user=request.user,
            date_of_transaction__year=year
        ).annotate(
            month=TruncMonth("date_of_transaction")
        ).values("month", "type_of_cost_or_revenue", "type_of_transaction").annotate(total_amount=Sum("total_sum"))

        # Filter for "Energi" and "Vatten" in the `type_of_cost_or_revenue` field
        energy_water_data = base_queryset.filter(type_of_cost_or_revenue__in=["Energi", "Vatten"])

        # Filter for "Cost" and "Revenue" in the `type_of_transaction` field
        cost_revenue_data = base_queryset.filter(type_of_transaction__in=["Cost", "Revenue"])

        # Initialize data for each type and month
        monthly_data = {
            month: {type_name: 0 for type_name in types_of_interest}
            for month in all_months
        }

        # Populate data for "Energi" and "Vatten"
        for item in energy_water_data:
            month = item["month"].strftime("%b '%y")
            monthly_data[month][item["type_of_cost_or_revenue"]] = item["total_amount"]

        # Populate data for "Cost" and "Revenue" (mapped to "Totala utgifter" and "Intäkter")
        for item in cost_revenue_data:
            month = item["month"].strftime("%b '%y")
            type_name = item["type_of_transaction"]

            # Map "Cost" to "Totala utgifter" and "Revenue" to "Intäkter"
            if type_name == "Cost":
                type_name = "Totala utgifter"
            elif type_name == "Revenue":
                type_name = "Intäkter"

            monthly_data[month][type_name] = item["total_amount"]

        # Convert to lists for charting
        labels = all_months
        series_data = [
            {
                "name": type_name,
                "data": [monthly_data[month].get(type_name, 0) for month in labels],
            }
            for type_name in types_of_interest
        ]

        return Response({"labels": labels, "series": series_data})


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

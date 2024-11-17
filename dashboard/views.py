from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from property.models import Property
from services.models import OrderMaintenanceServices
from rest_framework.permissions import IsAuthenticated
from users.serializers import ServiceProviderSerializer
from django.db.models import Sum, Avg, Count
from economi.models import Expense
from datetime import timedelta, date
from django.utils import timezone
from django.db.models.functions import TruncMonth
from blog.models import Blog
from feedback.models import UserFeedback
# Create your views here.


class UserDashboardstatusCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(user=request.user)
        
        # Count the number of buildings
        building_count = properties.count()

        # Sum the total number of apartments across all buildings
        total_apartments = properties.aggregate(
            total_apartments=Sum('antal_bostäder')
        )['total_apartments'] or 0

        # Filter active maintenance services
        active_maintenance_services = OrderMaintenanceServices.objects.filter(
            user=request.user, status="Active"
        )

        # Count active maintenance services
        active_maintenance_count = active_maintenance_services.count()

        # Calculate the fixed maintenance cost (sum of prices of active services)
        fixed_cost = active_maintenance_services.aggregate(
            total_cost=Sum('maintenance__price')
        )['total_cost'] or 0

        data = {
            "buildings": building_count,
            "appartments": total_apartments,
            "active_maintenance": active_maintenance_count,
            "fixed_maintenance": fixed_cost,
        }
        return Response(data, status=status.HTTP_200_OK)


class UserDashboardServiceProvider(APIView):
    def get(self, request):
        # Query OrderMaintenanceServices to get active services for the current user
        active_services = OrderMaintenanceServices.objects.filter(
            user=request.user,
            status="Active",
            service_provider__isnull=False,  # Exclude instances where service_provider is null
        ).select_related("service_provider")

        # Collect unique service provider instances
        unique_service_providers = set(
            service.service_provider for service in active_services
        )

        # Serialize the unique service provider instances
        serializer = ServiceProviderSerializer(unique_service_providers, many=True)

        return Response(serializer.data)

class DashboardStatsTable(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get the current date and the date 30 days ago (timezone-aware)
        today = timezone.now().date()
        past_30_days = timezone.now() - timedelta(days=30)

        # Get all distinct months where the user has any transaction
        months_with_data = Expense.objects.filter(user=user).annotate(
            month=TruncMonth('date_of_transaction')
        ).values('month').distinct().count()

        print(f"months_with_data: {months_with_data}")

        # Current month (timezone-aware)
        current_month = timezone.now().replace(day=1)

        # ---------------------------- Cost Calculations ---------------------------- #
        # Sum up total cost for the past 30 days
        past_30_days_cost = Expense.objects.filter(
            user=user, type_of_transaction='Cost', date_of_transaction__gte=past_30_days
        ).aggregate(total_sum=Sum('total_sum'))['total_sum'] or 0

        # print(f"past_30_days_cost: {past_30_days_cost}")

        # Calculate monthly average for 'Cost'
        cost_expenses = Expense.objects.filter(user=user, type_of_transaction='Cost')
        cost_monthly_data = cost_expenses.annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(
            total_sum=Sum('total_sum')
        ).order_by('month')

        total_cost_sum = cost_monthly_data.aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        cost_monthly_average = total_cost_sum / months_with_data if months_with_data > 0 else 0
        # print(f"total_cost_sum: {total_cost_sum}")
        # print(f"cost_monthly_average: {cost_monthly_average}")

        # Get current month's total for Cost (timezone-aware)
        current_month_cost = cost_expenses.filter(
            date_of_transaction__month=current_month.month
        ).aggregate(total_sum=Sum('total_sum'))['total_sum'] or 0
        # print(f"current_month_cost: {current_month_cost}")

        # Calculate the percentage difference for Cost
        # cost_difference = ((current_month_cost / cost_monthly_average) * 100 - 100) if cost_monthly_average > 0 else 0
        cost_difference = ((past_30_days_cost / cost_monthly_average) * 100 - 100) if cost_monthly_average > 0 else 0
        cost_difference = min(cost_difference, 100)  # Cap at 100%
        # print(f"cost_difference: {cost_difference}")

        # ---------------------------- Revenue Calculations ---------------------------- #
        # Sum up total revenue for the past 30 days
        past_30_days_revenue = Expense.objects.filter(
            user=user, type_of_transaction='Revenue', date_of_transaction__gte=past_30_days
        ).aggregate(total_sum=Sum('total_sum'))['total_sum'] or 0

        # Calculate monthly average for 'Revenue'
        revenue_expenses = Expense.objects.filter(user=user, type_of_transaction='Revenue')
        revenue_monthly_data = revenue_expenses.annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(
            total_sum=Sum('total_sum')
        ).order_by('month')

        total_revenue_sum = revenue_monthly_data.aggregate(Sum('total_sum'))['total_sum__sum'] or 0
        revenue_monthly_average = total_revenue_sum / months_with_data if months_with_data > 0 else 0


        # Get current month's total for Revenue (timezone-aware)
        current_month_revenue = revenue_expenses.filter(
            date_of_transaction__month=current_month.month
        ).aggregate(total_sum=Sum('total_sum'))['total_sum'] or 0

        # Calculate the percentage difference for Revenue
        # revenue_difference = ((current_month_revenue / revenue_monthly_average) * 100 - 100) if revenue_monthly_average > 0 else 0
        revenue_difference = ((past_30_days_revenue / revenue_monthly_average) * 100 - 100) if revenue_monthly_average > 0 else 0
        revenue_difference = min(revenue_difference, 100)  # Cap at 100%

        # ---------------------------- Blog Calculations ---------------------------- #
        months_with_blogs = Blog.objects.filter(user=user).annotate(
            month=TruncMonth('created_at')
        ).values('month').distinct().count()

        past_30_days_blogs = Blog.objects.filter(user=user, created_at__gte=past_30_days).count()

        total_blogs = Blog.objects.filter(user=user).count()
        blogs_avg_per_month = total_blogs / months_with_blogs if months_with_blogs > 0 else 0

        current_month_blogs = Blog.objects.filter(
            user=user, created_at__month=current_month.month
        ).count()

        # blogs_difference = ((current_month_blogs / blogs_avg_per_month) * 100 - 100) if blogs_avg_per_month > 0 else 0
        blogs_difference = ((past_30_days_blogs / blogs_avg_per_month) * 100 - 100) if blogs_avg_per_month > 0 else 0
        blogs_difference = min(blogs_difference, 100)

        # ---------------------------- Feedback Calculations ---------------------------- #
        months_with_feedbacks = UserFeedback.objects.filter(user=user).annotate(
            month=TruncMonth('created_at')
        ).values('month').distinct().count()

        past_30_days_feedbacks = UserFeedback.objects.filter(user=user, created_at__gte=past_30_days).count()

        total_feedbacks = UserFeedback.objects.filter(user=user).count()
        feedbacks_avg_per_month = total_feedbacks / months_with_feedbacks if months_with_feedbacks > 0 else 0

        current_month_feedbacks = UserFeedback.objects.filter(
            user=user, created_at__month=current_month.month
        ).count()

        # feedbacks_difference = ((current_month_feedbacks / feedbacks_avg_per_month) * 100 - 100) if feedbacks_avg_per_month > 0 else 0
        feedbacks_difference = ((past_30_days_feedbacks / feedbacks_avg_per_month) * 100 - 100) if feedbacks_avg_per_month > 0 else 0
        feedbacks_difference = min(feedbacks_difference, 100)

        # ---------------------------- Response Data ---------------------------- #
        data = [
            {
                "name": "Intäkter",  # Revenue
                "past_30_days": round(past_30_days_revenue, 2),
                "avg_total_per_month": round(revenue_monthly_average),  # No decimals
                "difference": round(revenue_difference, 2)
            },
            {
                "name": "Utgifter",  # Costs/Expenses
                "past_30_days": round(past_30_days_cost, 2),
                "avg_total_per_month": round(cost_monthly_average),  # No decimals
                "difference": round(cost_difference, 2)
            },
            {
                "name": "Feedback & idéer",
                "past_30_days": past_30_days_feedbacks,
                "avg_total_per_month": round(feedbacks_avg_per_month, 1),
                "difference": round(feedbacks_difference, 2)
            },
            {
                "name": "Publicerade Nyhetsbrev",
                "past_30_days": past_30_days_blogs,
                "avg_total_per_month": round(blogs_avg_per_month, 1),
                "difference": round(blogs_difference, 2)
            }
        ]
        return Response(data, status=status.HTTP_200_OK)

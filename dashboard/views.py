from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from property.models import Property
from services.models import UserMaintenanceServices
from rest_framework.permissions import IsAuthenticated
from users.serializers import ServiceProviderSerializer
from django.db.models import Sum, Avg, Count
from services.models import UserMaintenanceServices
from economi.models import Expense
from datetime import timedelta
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
        active_maintenance_services = UserMaintenanceServices.objects.filter(
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
        # Query UserMaintenanceServices to get active services for the current user
        active_services = UserMaintenanceServices.objects.filter(
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
        today = timezone.now().date()
        start_date = today - timedelta(days=30)

        # Filter expenses and revenues for the past 30 days
        expenses_last_30_days = Expense.objects.filter(
            user=user,
            date_of_transaction__gte=start_date,
            type_of_cost_or_revenue__iexact="Cost"
        ).aggregate(total=Sum('total_sum'))['total'] or 0

        revenue_last_30_days = Expense.objects.filter(
            user=user,
            date_of_transaction__gte=start_date,
            type_of_cost_or_revenue__iexact="Revenue"
        ).aggregate(total=Sum('total_sum'))['total'] or 0

        # Calculate average per month for the current year, excluding months with no data
        def calculate_avg_per_month(expense_type):
            year_start = today.replace(month=1, day=1)
            monthly_totals = Expense.objects.filter(
                user=user,
                type_of_cost_or_revenue__iexact=expense_type,
                date_of_transaction__gte=year_start
            ).annotate(month=TruncMonth('date_of_transaction')).values('month').annotate(total=Sum('total_sum')).values('total')
            
            # Filter out months with no data
            total_months = monthly_totals.count()
            if total_months > 0:
                avg_total_per_month = monthly_totals.aggregate(avg_total=Avg('total'))['avg_total'] or 0
            else:
                avg_total_per_month = 0
            
            return avg_total_per_month

        expenses_avg_per_month = calculate_avg_per_month("Cost")
        revenue_avg_per_month = calculate_avg_per_month("Revenue")

        # Calculate the percentage difference between past 30 days and average per month
        def calculate_percentage_difference(past_30_days, avg_per_month):
            if avg_per_month == 0:
                return 0
            return ((past_30_days - avg_per_month) / avg_per_month) * 100

        expenses_difference = calculate_percentage_difference(expenses_last_30_days, expenses_avg_per_month)
        revenue_difference = calculate_percentage_difference(revenue_last_30_days, revenue_avg_per_month)

        # Calculate feedback metrics
        feedbacks_last_30_days = UserFeedback.objects.filter(
            user=user,
            created_at__gte=start_date
        ).count()

        def calculate_feedbacks_avg_per_month():
            year_start = today.replace(month=1, day=1)
            monthly_totals = UserFeedback.objects.filter(
                user=user,
                created_at__gte=year_start
            ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).values('total')
            
            # Filter out months with no data
            total_months = monthly_totals.count()
            if total_months > 0:
                avg_total_per_month = monthly_totals.aggregate(avg_total=Avg('total'))['avg_total'] or 0
            else:
                avg_total_per_month = 0
            
            return avg_total_per_month

        feedbacks_avg_per_month = calculate_feedbacks_avg_per_month()

        recent_feedbacks = UserFeedback.objects.filter(
            user=user,
            created_at__month=today.month
        ).count()

        previous_feedbacks = UserFeedback.objects.filter(
            user=user,
            created_at__month=(today - timedelta(days=30)).month
        ).count()

        feedbacks_difference = calculate_percentage_difference(recent_feedbacks, feedbacks_avg_per_month)

        # Calculate blog metrics
        blogs_last_30_days = Blog.objects.filter(
            user=user,
            created_at__gte=start_date
        ).count()

        def calculate_blogs_avg_per_month():
            year_start = today.replace(month=1, day=1)
            monthly_totals = Blog.objects.filter(
                user=user,
                created_at__gte=year_start
            ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).values('total')
            
            # Filter out months with no data
            total_months = monthly_totals.count()
            if total_months > 0:
                avg_total_per_month = monthly_totals.aggregate(avg_total=Avg('total'))['avg_total'] or 0
            else:
                avg_total_per_month = 0
            
            return avg_total_per_month

        blogs_avg_per_month = calculate_blogs_avg_per_month()

        recent_blogs = Blog.objects.filter(
            user=user,
            created_at__month=today.month
        ).count()

        previous_blogs = Blog.objects.filter(
            user=user,
            created_at__month=(today - timedelta(days=30)).month
        ).count()

        blogs_difference = calculate_percentage_difference(recent_blogs, blogs_avg_per_month)

        data = {
            "revenue": {
                "past_30_days": revenue_last_30_days,
                "avg_total_per_month": revenue_avg_per_month,
                "difference": revenue_difference
            },
            "expenses_or_cost": {
                "past_30_days": expenses_last_30_days,
                "avg_total_per_month": expenses_avg_per_month,
                "difference": expenses_difference
            },
            "feedbacks": {
                "past_30_days": feedbacks_last_30_days,
                "avg_total_per_month": feedbacks_avg_per_month,
                "difference": feedbacks_difference
            },
            "blogs_publications": {
                "past_30_days": blogs_last_30_days,
                "avg_total_per_month": blogs_avg_per_month,
                "difference": blogs_difference
            }
        }
        return Response(data, status=status.HTTP_200_OK)

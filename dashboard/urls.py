from django.urls import path
from .views import UserDashboardstatusCount, UserDashboardServiceProvider, DashboardStatsTable

urlpatterns = [
    path("user-dashboard-count/", UserDashboardstatusCount.as_view()),
    path("user-service-provider/", UserDashboardServiceProvider.as_view()),
    path("user-table-stats/", DashboardStatsTable.as_view()),
]

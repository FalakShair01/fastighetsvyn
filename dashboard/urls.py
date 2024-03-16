from django.urls import path
from .views import UserDashboardstatusCount

urlpatterns = [
    path('user-dashboard-count/', UserDashboardstatusCount.as_view())
]
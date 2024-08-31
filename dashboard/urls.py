from django.urls import path
from .views import UserDashboardstatusCount, UserDashboardServiceProvider

urlpatterns = [
    path("user-dashboard-count/", UserDashboardstatusCount.as_view()),
    path("user-service-provider/", UserDashboardServiceProvider.as_view()),
]

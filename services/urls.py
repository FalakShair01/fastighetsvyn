from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DevelopmentViewset, UserDevelopmentServicesViewset, MaintenanceViewset, 
                    UserMaintenanceViewset, AdminDevelopemStatusView, AdminMaintenanceStatusView )
router = DefaultRouter()

router.register('development', DevelopmentViewset, basename='development-service'),
router.register('maintenance', MaintenanceViewset, basename='maintenance-service')
router.register('user/development', UserDevelopmentServicesViewset),
router.register('user/maintenance', UserMaintenanceViewset, basename='user-maintenance')
router.register('admin/development', AdminDevelopemStatusView, basename='admin-development')
router.register('admin/maintenance', AdminMaintenanceStatusView, basename='admin-maintenance')



urlpatterns = [
    path('', include(router.urls))
]
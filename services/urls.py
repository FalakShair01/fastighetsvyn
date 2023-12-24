from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DevelopmentViewset, UserDevelopmentServicesViewset, MaintenanceViewset, UserMaintenanceViewset
router = DefaultRouter()

router.register('development', DevelopmentViewset, basename='development-service'),
router.register('user/development', UserDevelopmentServicesViewset),
router.register('maintenance', MaintenanceViewset, basename='maintenance-service')
router.register('user/maintenance', UserMaintenanceViewset, basename='user-maintenance')


urlpatterns = [
    path('', include(router.urls))
]
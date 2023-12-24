from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DevelopmentViewset, UserDevelopmentServicesView, MaintenanceViewset
router = DefaultRouter()

router.register('development', DevelopmentViewset, basename='development-service'),
router.register('user/services', UserDevelopmentServicesView),
router.register('maintenance', MaintenanceViewset, basename='maintenance-service')


urlpatterns = [
    path('', include(router.urls))
]
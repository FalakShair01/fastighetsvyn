from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DevelopmentViewset, UserDevelopmentServicesView
router = DefaultRouter()

router.register('development', DevelopmentViewset, basename='development-service'),
router.register('user/services', UserDevelopmentServicesView),


urlpatterns = [
    path('', include(router.urls))
]
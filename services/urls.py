from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DevelopmentViewset, UserDevelopmentServicesView
router = DefaultRouter()

router.register('development', DevelopmentViewset, basename='development-service')

urlpatterns = [
    path('development/services/', UserDevelopmentServicesView.as_view()),
    path('', include(router.urls))
]
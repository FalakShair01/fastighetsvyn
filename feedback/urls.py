from django.urls import path, include
from .views import AdminFeedbackViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('admin-feedbacks', AdminFeedbackViewset, basename='admin-feedbacks')


urlpatterns = [
    path('', include(router.urls)),   
]
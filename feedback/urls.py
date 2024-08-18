from django.urls import path, include
from .views import AdminFeedbackViewset, UserFeedbackView, UserFeedbackviewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('admin-feedbacks', AdminFeedbackViewset, basename='admin-feedbacks')
router.register('tenant-feedback', UserFeedbackviewset, basename='tenant-feedback')


urlpatterns = [
    path('tenant-feedback/<username_slug>/', UserFeedbackView.as_view()),
    path('', include(router.urls)),  
]
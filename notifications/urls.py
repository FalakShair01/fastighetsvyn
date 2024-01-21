from django.urls import path, include
from .views import AdminNotificationsViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notify/admin', AdminNotificationsViewset)

urlpatterns = [
    path('', include(router.urls))
]
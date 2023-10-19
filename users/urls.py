from django.urls import path, include
from .views import UserRegisterView, ProfileView, TenantView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tenant', TenantView, basename='tenant-create')

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register"),
    path("profile", ProfileView.as_view(), name="profile"),
    path('', include(router.urls)),
]

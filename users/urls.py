from django.urls import path, include
from .views import (UserRegisterView,VerifyEmail, ProfileView, TenantView, ChangePasswordView, 
                    SendPasswordResetEmailView, ResetPasswordView, LoginView, RemoveUserProfile, 
                    RemoveTenantProfile, UserViewset, ManagersViewset, ServerProviderViewset, DemoRequestView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user/tenant', TenantView, basename='tenant-create')
router.register(r'user/management', UserViewset, basename='user-management')
router.register(r'user/manager', ManagersViewset)
router.register(r'service-provider', ServerProviderViewset)
router.register(r'demo-requests', DemoRequestView)

urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="register"),
    path("user/email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/profile/", ProfileView.as_view(), name="profile"),
    path("user/remove-profile/", RemoveUserProfile.as_view(), name="remove-profile"),
    path("user/remove-tenant-profile/<int:pk>/", RemoveTenantProfile.as_view(), name="remove-tenant-profile/"),
    path("user/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("user/reset-password-email/", SendPasswordResetEmailView.as_view(), name="reset-password-email"),
    path("user/reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path('', include(router.urls)),
]
